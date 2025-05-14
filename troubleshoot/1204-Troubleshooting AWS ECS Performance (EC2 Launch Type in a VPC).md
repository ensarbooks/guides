# Troubleshooting AWS ECS Performance (EC2 Launch Type in a VPC)

Amazon Elastic Container Service (ECS) on EC2 provides a powerful platform for running web applications in Docker containers, but performance issues can arise at both the container level and the EC2 instance level. This comprehensive guide will help you troubleshoot CPU, memory, and network performance problems in an ECS cluster (using the EC2 launch type within a VPC), and provide best practices for tuning ECS task definitions, scaling services, and optimizing the underlying EC2 and VPC configuration. We will cover ECS task definition parameters, service scaling strategies, EC2 instance types (and features like CPU credits and enhanced networking), VPC-level considerations (subnets, NAT gateways, security groups), interpreting CloudWatch metrics and logs, and step-by-step troubleshooting scenarios. Monitoring solutions (CloudWatch, Prometheus, Datadog, X-Ray) and common pitfalls with proactive avoidance measures are also discussed. The goal is to ensure your web application on ECS runs efficiently and reliably.

## Introduction

Running a web application on AWS ECS with EC2 launch type means you are managing not only containerized application performance but also the underlying EC2 instances and VPC network environment. Poorly tuned containers or misconfigured infrastructure can lead to high response times, CPU spikes, out-of-memory errors, or network bottlenecks. In this guide, we take a deep dive into diagnosing and resolving such issues. We assume a typical architecture where web application containers run as ECS tasks on EC2 container instances in private subnets, behind a load balancer, with Internet access via NAT gateway. We will use a structured approach to identify performance bottlenecks at each layer (application, container, host, and network) and illustrate troubleshooting with examples.

**Scope:** We focus on ECS clusters using EC2 launch type (not Fargate), so container tasks are hosted on EC2 instances. Both the containers and the EC2 instances can experience CPU, memory, or network issues. We will explore ECS-specific configurations (task CPU/memory settings, task placement, scaling) as well as EC2 and VPC configurations (instance type selection, networking setup). All examples are oriented towards web applications (e.g. services behind an Application Load Balancer serving user requests).

## ECS on EC2 Architecture Overview

Before troubleshooting, it’s important to understand the architecture of an ECS cluster on EC2 and how containers, instances, and networking fit together:

&#x20;_Figure: Example architecture of a web application running on ECS (EC2 launch type). An Auto Scaling group of EC2 container instances (orange) across multiple Availability Zones runs the application’s container tasks. An Application Load Balancer (ALB) routes user traffic to the containers. The cluster uses other AWS services like Amazon RDS for the database (purple icon), and AWS CloudWatch for monitoring (pink icon). IAM roles and AWS Secrets Manager provide credentials and configuration. This highly available setup in a VPC spans public subnets for the ALB and private subnets for the ECS instances._

**ECS Cluster and Container Instances:** In ECS with EC2 launch type, you manage a cluster of EC2 instances (called _container instances_) that register with ECS. Each container instance runs the **ECS agent** and a Docker daemon, allowing it to run containers as instructed by the ECS control plane. The ECS cluster is simply a logical group of these instances. The cluster can span multiple Availability Zones for high availability. Tasks (which are one or more containers defined by a task definition) are scheduled onto these EC2 instances.

**Task Definitions and Services:** An ECS **task definition** is a blueprint for containers – it specifies the Docker image, CPU units, memory, ports, and other settings for each container. An ECS **service** ensures that a specified number of tasks are running and can optionally attach them behind a load balancer for distribution of traffic. The service scheduler will place tasks on available container instances according to defined placement strategies and will replace tasks if they stop or become unhealthy.

**Networking (VPC):** In a VPC, ECS tasks can use different network modes. The most common for modern ECS services is `awsvpc` network mode, where each task gets its own elastic network interface (ENI) and a private IP address in your subnets. This mode allows tasks to appear as first-class network entities in the VPC. Alternatively, `bridge` or `host` network modes use the EC2 instance’s network (shared or host networking). In a typical web app deployment, ECS container instances are often in **private subnets** (no direct internet access), while a load balancer is in **public subnets** to accept public traffic and forward it to the tasks. Internet-bound traffic from tasks in private subnets goes out via a **NAT gateway** in a public subnet.

&#x20;_Figure: ECS container instance in a private subnet accessing the internet through a NAT gateway. The EC2 host (orange) runs an application container and has only a private IP (172.31.16.1) in the private subnet. The NAT gateway (purple) in a public subnet routes outbound traffic to the Internet Gateway, allowing the container to reach external services while preventing inbound internet access directly to the private host._

**Load Balancing:** For web services, an Application Load Balancer (ALB) is commonly used to distribute requests to ECS tasks. The ALB operates at layer 7 and can perform health checks on containers. If tasks become unhealthy or unresponsive, the ALB can mark them out of service. ALB metrics (such as request count, latency, HTTP 5xx errors) are important to correlate with ECS metrics during troubleshooting.

**Key AWS Components:** Other important components in this architecture include IAM roles (e.g., giving the ECS tasks permission to access AWS resources), Amazon CloudWatch (for logs and metrics), and possibly AWS Secrets Manager or Parameter Store (for application configuration). While these aren’t directly part of performance, misconfiguration (like missing permissions causing timeouts when accessing secrets, etc.) can indirectly affect application behavior.

With this context, we can now dive into specific areas of performance: CPU utilization, memory usage, and network throughput, examining both container-level and host-level aspects.

## CPU and Memory Performance in ECS

Performance issues often manifest as high CPU usage (leading to slow processing or request timeouts) or high memory usage (leading to garbage collection stalls or out-of-memory crashes). In ECS, CPU and memory resources are managed at two levels: **container (task) level** and **EC2 instance level**. We will explore how ECS allocates and limits these resources and how to detect and fix problems in each category.

### Container-Level CPU and Memory Management

Each ECS task definition specifies how much CPU and memory the task’s containers are allocated. Properly tuning these values is crucial for performance:

- **CPU Units:** In ECS, CPU is specified in _CPU units_. 1024 CPU units = 1 vCPU (approximately one physical core or hyperthread). If an ECS task is allocated 512 CPU units, it means it “reserves” half of a CPU core on the host. Importantly, ECS applies this as a _share_ constraint using Linux CFS scheduling – if other containers are idle, a container can use more than its allocated share (burst), but if the CPU is contested, the shares determine priority. In practice, if one container is allocated 512 units and another 512 units on a 1 vCPU host, each should get \~50% of CPU when both are busy; if one is idle, the other can use \~100%. There is no hard CPU cap by default (ECS does not impose a strict CPU limit, it uses the share system), so tasks can utilize spare capacity. This flexible share-based usage is beneficial for performance, but it means a noisy container can starve others if all are busy – thus, oversubscription should be done carefully.

- **Memory (Soft vs Hard Limits):** ECS task definitions can specify a **hard memory limit** (`memory`) and an optional **soft limit** (`memoryReservation`) for each container. The hard limit is the maximum memory the container can use – if it tries to exceed this, it will be terminated (OOM-killed by Docker). The soft limit is a reservation that ensures the ECS scheduler places the task only if that amount of memory is available on the host, but the container is allowed to exceed it at runtime (up to the hard limit or until host runs out). If only a soft limit is set (and no hard limit), the container can use memory up to the host’s capacity. If only a hard limit is set (no separate soft), that hard value also acts as the reservation.

  In a memory contention situation on the host (total usage exceeding physical RAM), the Linux Out-Of-Memory (OOM) killer will start killing processes. The kernel will preferentially kill containers that have exceeded their soft limits (or have no limit) before those under their reserved memory, but this is not guaranteed – it depends on kernel heuristics. The key point is that setting a soft limit allows some memory bursting and overcommit, whereas the hard limit is a strict ceiling. For stable production environments, it’s often wise to set a hard limit to avoid any single container using all host memory.

**Implications for Troubleshooting:** Misconfigured CPU or memory settings can cause performance problems:

- If CPU units are set too low relative to the container’s needs, the container might get throttled when other tasks are running. Symptoms include high CPU steal or wait time inside the container, and the application not using full CPU even when it appears busy. In CloudWatch Container Insights, the **CPU utilization** for the task might hit 100% (meaning it’s using all its allocated units) while the host CPU might still have headroom. The solution is often to allocate more CPU units to that task or reduce concurrency on that host.

- If no CPU limits are set at all (which is allowed), tasks can compete freely. This gives flexibility but means a single busy container can max out the host CPU. This might be fine in dev/test (where over-commitment saves cost) but in production it can cause unpredictable latency. ECS allows overcommitting CPU (scheduling more total CPU units than the host has) since idle containers don’t use their allocation, but if all become busy, the host CPU will be fully utilized and tasks will slow down.

- If memory is set too low (especially the hard limit), the container might be killed if it exceeds that, causing the ECS service to restart it (and users might see errors during that time). If memory is set too high (beyond what the application actually needs), it reserves host memory unnecessarily, possibly preventing other tasks from being scheduled.

- **OutOfMemory (OOM) Events:** These are common in container environments. An ECS task that gets killed due to OOM will usually have an exit code 137. In the ECS console or AWS CLI (`aws ecs describe-tasks`), you might see **“Essential container in task exited”** with reason OOM. CloudWatch Logs for the container might show an error like “Container killed due to memory usage”. The ECS agent log or `/var/log/messages` on the EC2 instance can also record the Linux OOM killer action. If you suspect OOM, check the ECS **stopped task** reason and any log output. The fix could be to increase the container memory hard limit in the task definition or find and fix a memory leak in the application. AWS documentation notes that an error "OutOfMemoryError: Container killed due to memory usage" indicates the container used more memory than allocated in the task definition. Ensuring your task definition’s memory matches the app’s requirements (plus some headroom) is critical.

- **Memory Reservation Pitfall:** If you use only soft limits (`memoryReservation`) without a hard limit, containers can consume more memory when available, which is good for bursty usage. But if multiple containers all burst and exceed their reservations, the host can run out of memory and then **any** container might get OOM-killed by the kernel (not necessarily the one that exceeded its reservation). In such scenarios, you might see one service’s container killed even though another service’s container caused the memory spike – simply because the kernel chose the one with the higher OOM score. To avoid this, consider setting hard limits, or at least ensure the sum of reservations does not exceed host RAM by too much.

**Task CPU and Memory Monitoring:** Use CloudWatch Container Insights or ECS service utilization metrics to monitor task-level CPU and memory usage. ECS provides service-level metrics like **Service CPU Utilization** and **Service Memory Utilization**, which show the percentage of the task’s allocated CPU/Memory currently in use. For example, if a service has tasks each with 512 CPU units allocated, and one task is using 256 CPU units on average (i.e., half a vCPU), that’s 50% CPU utilization for that task. ECS reports these metrics by aggregating the agent’s 20-second samples into CloudWatch. High values (near 100%) indicate the task is fully using its allocated resource. Memory utilization above 100% is possible **if only a soft limit was set**, because the task can exceed the reservation. If you see memory utilization hitting 100% (or going above), it’s a sign the task may be at risk of OOM if it tries to grow further – consider increasing the memory allocation.

**Application-Level Tuning:** Container resources are one side; the application’s own configuration is the other. For example, if running Java inside a container, ensure the JVM’s max heap (`-Xmx`) is set below the container’s memory limit to avoid the JVM thinking more memory is available than actually is (which would lead to OOM). Many languages and runtimes have container-awareness now or environment variables to tweak (e.g., Node’s max_old_space_size, Python’s multiprocessing should consider CPU count, etc.). A container might also exhibit high CPU because of inefficient code or lack of caching – while troubleshooting, distinguish between issues that are purely resource allocation vs. issues in the application logic (for which APM tools or profiling might be needed).

### EC2 Instance-Level CPU and Memory

The EC2 instances themselves provide the physical resources that tasks consume. Even if each container is tuned, the cluster can face performance issues if the underlying instances are under-provisioned, mis-provisioned, or exhausted.

**Instance Sizing and Type:** Choose the right EC2 instance type for your workload. Key considerations include vCPU count, memory size, network performance, and the **burstable vs fixed performance** nature of the instance.

- **Burstable (T2/T3/T4g) vs Fixed Performance (M5, C5, etc.):** AWS T-family (T2, T3, T4g) instances use the **CPU credit** mechanism. They have a baseline CPU performance and accumulate credits when idle which can be spent to burst above baseline. For example, a `t3.medium` has 2 vCPUs and a baseline of 20% per vCPU (so 20% of 2 vCPUs = 40% of a single vCPU baseline). It earns 24 credits per hour per vCPU, etc. If your ECS cluster runs on T instances and the tasks continuously use high CPU, the CPU credits can be exhausted. **When credits run out, the instance CPU is throttled to the baseline%, causing severe performance degradation**. This manifests as the EC2 CloudWatch metric **CPUCreditBalance** dropping to 0 and **CPUUtilization** flattening at the baseline (e.g., \~20-30%). If you see an ECS host stuck at e.g. 20% CPU usage despite tasks needing more, it’s likely throttled. The solution is to either enable T2/T3 Unlimited (which charges for extra credits so CPU can go beyond baseline) or switch to a non-burstable instance type. For production web apps with steady load, M5, C5, or C6i families (depending on needs for memory or compute) are often more appropriate to ensure consistent CPU performance.

- **CPU and Memory Balance:** The ratio of CPU to memory in the instance should align with your tasks. If you run memory-heavy tasks, use memory-optimized instances (R5, R6 series). If CPU-heavy, use compute-optimized (C5, C6). A general-purpose (M5, M6) might be used for balanced needs. Also consider instance size: a larger instance can host more tasks, but concentrates load – a failure would drop more tasks at once. Smaller instances give more granular scaling but add overhead (each instance uses some baseline memory for OS, etc.). Always ensure the sum of task reservations (or usages) doesn’t regularly exceed the instance resources.

- **Memory on Instances:** ECS doesn’t directly throttle memory at the instance level (other than not scheduling tasks beyond available memory). But if you overcommit with soft limits, the EC2 instance can run out of RAM and start swapping or OOM-killing tasks. For Linux instances, check OS metrics like memory usage and swap usage (you can use CloudWatch Agent or SSH in to run `free -m`). Ideally, swap should be minimal (ECS-optimized AMIs often have swap off by default) because swapping will slow down applications drastically. If you consistently approach instance memory limits, either reduce task memory usage or scale out to more instances.

- **EC2 CPU Steal:** On an oversubscribed host (especially burstable instances out of credits or if running on a hypervisor with contention), you might see CPU steal time in OS metrics. This indicates the VM is ready to run tasks but the hypervisor isn’t giving it CPU (common in credit starvation). If you can, use CloudWatch metrics or a monitoring agent to see instance-level metrics like **CPUSteal** or **CPU Ready** (in VMware terms). AWS doesn’t expose steal in basic metrics, but high-level signs are the same as credit exhaustion.

**Enhanced Networking (ENA):** Modern EC2 instances on the Nitro platform support **enhanced networking** via the Elastic Network Adapter (ENA). ENA provides higher bandwidth (up to 100 Gbps on some instances) and higher packets per second, with lower latency and lower CPU overhead for networking. All current-gen instance types (e.g., C5, M5, etc.) have ENA enabled by default when using AWS-provided AMIs (like Amazon Linux). If you use a custom AMI, ensure the ENA driver is installed and ENA is enabled on the instance. For ECS, using enhanced networking means your containers can push more throughput without bottlenecking the instance. If network traffic is heavy (many requests or high volume), not having ENA could constrain throughput. Check the **Network** performance rating of your instance (e.g., “Up to 10 Gbps” or “25 Gbps”) in AWS docs and ensure it matches your needs.

**AMI Optimizations:** AWS provides **ECS-optimized AMIs** (Amazon Linux-based) which come pre-installed with Docker, the ECS agent, and are tuned for container workloads. Using the latest ECS-optimized AMI (or Amazon Linux 2/2023 with ECS agent) ensures you have recent Docker versions, kernel updates, and agent improvements. For example, the Amazon Linux 2023 ECS AMI uses the XFS filesystem and the `overlay2` storage driver for Docker by default (with a 30 GiB volume by default for everything). This is a good general setup. If you use a generic Linux AMI, ensure Docker is configured with a performant storage driver (overlay2 is recommended over older devicemapper loopback, which had poor performance). Also update the ECS agent periodically – old agent versions might have bugs or not report metrics properly. The ECS-optimized AMI also has sensible sysctl settings and collects instance-level metrics by default (if you enable CloudWatch agent). Always consider applying system and security updates as provided (the ECS AMIs can be updated via SSM parameter to latest at cluster launch). In short, a well-maintained AMI avoids many host-level performance pitfalls.

**EC2 Disk I/O:** Although the focus is CPU, memory, network, don’t ignore disk I/O if your application writes logs or temp files. ECS-optimized AMIs store Docker images and container writable layers on the instance (EBS or instance store). If that disk is slow or full, it could cause container operations to lag (e.g., slow image pulls or logging). Using gp3 EBS volumes for the instance with sufficient IOPS, or instance store for ephemeral data if available, can help. Check if any processes on the host (or containers) are consuming a lot of disk bandwidth (cloud metrics for EBS Burst Balance, etc., if applicable).

**Monitoring Host Metrics:** CloudWatch provides metrics per EC2 instance such as CPUUtilization, NetworkIn/Out, DiskRead/Write bytes, etc. For memory and disk, you need CloudWatch Agent or another tool because basic CloudWatch doesn’t have instance memory by default. Enabling **CloudWatch Agent with StatsD/collectd** on ECS instances (or using CloudWatch Container Insights at the cluster level) can expose memory, disk, and even per-container stats. High CPUUtilization at the instance level might indicate either too many tasks on that instance or one task monopolizing it. If one instance is at 100% and others are idle, it could be a placement issue (all tasks landed on one node – see placement strategies later). Balancing load across instances or scaling out more instances can alleviate that.

### ECS Task Definition Tuning and Task Placement

Now that we’ve covered the raw resources, let’s discuss how ECS allows you to **tune task definitions** and how tasks are **placed** onto instances, which significantly affects performance and availability.

**Task Definition Tuning:** Beyond CPU and memory, a task definition has other parameters that can impact performance:

- **Docker Parameters:** For example, `ulimits` (you might raise `nofile` if your app needs many file descriptors for network connections), `logConfiguration` (choosing the awslogs driver with proper buffer settings to avoid blocking on logs), and `portMappings` (host vs awsvpc mode differences). Ensure logs don’t overwhelm the container – the default AWS Logs driver buffers logs in memory; huge bursts of log output can use memory or CPU. If your app is extremely chatty in logging, consider adjusting logging levels or using a sidecar for log shipping.

- **Health Check Grace Period:** When using ECS with load balancer, set an appropriate health check grace period (time after task start before ALB health checks start). If it’s too short, the ALB might mark the container unhealthy if it hasn’t fully started, causing ECS to kill and restart it repeatedly which looks like a performance issue (though it’s a config issue).

- **Environment Variables & Config:** Tuning application-specific env vars (like turning on caching, adjusting thread pools) is part of tuning, though specific to your app. As a general pattern, ensure that the container has enough threads or worker processes to utilize the CPU given (but not so many that it context-switches excessively). For example, a Node.js container (single-threaded for JS) won’t use multiple CPUs unless using clustering; so scaling out more tasks might be needed for multi-core usage.

- **Ephemeral Storage:** By default, tasks have some ephemeral disk space (on ECS EC2 it’s the host’s Docker storage). If your app needs to write large files (like for processing), use ECS ephemeral storage setting (you can allocate up to 200 GiB ephemeral storage per task in newer ECS versions) or mount EFS volumes. If disk space is too low, tasks could error out writing to disk.

**Service Auto Scaling Strategies:** ECS services can be configured to scale the number of tasks based on load. Proper scaling ensures performance during traffic spikes:

- **Target Tracking Scaling:** This is often recommended for simplicity. You select a metric like CPU utilization or request count and a target value. ECS Service Auto Scaling will create CloudWatch alarms and adjust the desired count of tasks to maintain that target. For example, keep average CPU at 50% – if it goes higher, add tasks; if lower, remove tasks. For web apps behind ALB, you might scale on ALB’s RequestCountPerTarget or on custom metrics (like latency or queue depth).

- **Step Scaling (and Simple Scaling):** These allow more granular control with CloudWatch alarms triggering specific scale adjustments. For instance, if CPU > 80% for 5 minutes, add 2 tasks (step scaling). If > 90%, add 4 tasks, etc. Step scaling can add capacity faster when load surges, at the cost of complexity. Target tracking is often sufficient, but step scaling can be combined for safety (e.g., a step policy to add a big chunk at 90% usage to avoid lag).

- **Cooldown and Stability:** Avoid too frequent scale actions. Ensure there's a cooldown period so the system stabilizes after scaling before another action. If tasks take time to initialize, consider that in scaling (e.g., scale out early at 60% CPU to give new tasks time to spin up before things get critical at 90%).

- **Cluster Capacity:** Auto scaling tasks only helps if the cluster has available EC2 capacity to place them. It’s vital to also manage **Cluster Auto Scaling** – using ECS Capacity Providers or external automation – to add EC2 instances when needed. Otherwise, you might scale out tasks and they get stuck in `PENDING` because no host has resources.

**Task Placement Constraints & Strategies:** By default, ECS tries to spread tasks across instances and AZs (for services). But you can customize placement:

- **Placement Strategies:** ECS supports strategies like `spread`, `binpack`, and `random`. For example, `spread across AZ` (which is default for services) will distribute one task per AZ before adding a second in an AZ. `spread across instance` ensures even spread on hosts. `binpack` will attempt to pack tasks on as few instances as possible (based on either CPU or memory) – useful to minimize cost or when you want to fully load instances before using new ones. However, **binpack can cause performance hotspots**: if you binpack on memory, ECS will fill an instance’s memory with tasks, which might also end up using a lot of CPU, potentially maxing out one instance while others are empty. This could be fine if the instance can handle it, but it means if that instance fails or reboots, many tasks are impacted at once. `spread` gives better resilience at slight cost of leaving some capacity unused. **Recommendation:** For most web apps, use `spread` (by AZ and maybe by instance) to avoid putting all load on one box. Use `binpack` if you are sure it won’t overload and you want to optimize for cost.

- **Placement Constraints:** These are hard rules. The two types are `distinctInstance` and `memberOf`. `distinctInstance` ensures each task of the service runs on a different instance – good for high availability (no two tasks of same service on same host). This can prevent one host failure from taking out all tasks of a service. If you run multiple tasks for the same service, consider using distinctInstance unless you have more tasks than instances. `memberOf` allows you to restrict tasks to instances that have a certain attribute. For example, only place on instances of a certain type or with a custom attribute (like attribute `role = backend`). This is used if you have heterogenous instances or need to isolate certain workloads (e.g., GPU tasks to GPU-equipped instances).

- **When Placement Causes Issues:** If you set a constraint that is too strict, ECS might not be able to place tasks at all. A common scenario: using `distinctInstance` but your cluster only has one instance – the second task will remain pending (“unable to place task because no container instance met requirements” in the ECS service events). Or using `memberOf` with an expression that matches zero instances (typo or none registered). Always check ECS **Service Events** in the console if tasks are not starting. You might see messages like _“unable to place a task because no container instance met all of its requirements”_. These events often specify the reason (e.g., insufficient memory or no instances in group). If the message mentions _“placement constraint”_, revisit your constraints. Remember, placement constraints are binding – ECS won’t violate them. Strategies are best-effort, not guaranteed. So a strategy of spread might not perfectly spread if not possible, but a constraint of distinctInstance will outright prevent placement if not enough instances.

- **Case: Tasks Stuck in PENDING:** Suppose you scaled your service from 2 to 4 tasks, but only 3 are running and 1 is pending. Investigate:

  - Check service events for "unable to place". If it says insufficient CPU or memory, your instances are out of room – either scale out the cluster (add instances) or use smaller task sizes. If it says placement constraint, adjust or add instances to satisfy it.
  - If using awsvpc networking, a hidden constraint is ENI availability. Each task on awsvpc consumes an ENI from the instance’s quota. Smaller instances have lower ENI limits (e.g., a t2.small might only allow a few ENIs). If the limit is hit, tasks can’t attach network interfaces and will fail placement. Solution: choose an instance with higher ENI limits (larger instance or a Nitro instance) or reduce tasks per instance. ECS service events would show an error about unable to attach ENI in that case.
  - Another subtle issue: if cluster has instances in multiple AZ, but your service’s subnets (if specified) are only in one AZ, ECS will only place in that AZ, perhaps leaving other instances unused. Ensure your ECS service is configured with all relevant subnets so it can use all AZs.

**Scaling EC2 Instances (Cluster Capacity):** AWS introduced **ECS Cluster Auto Scaling (CAS)** with capacity providers. You can configure a capacity provider with an Auto Scaling Group (ASG) for your instances, and ECS will scale the ASG based on task needs. For example, you can set a target of 75% cluster utilization; when tasks’ combined CPU reservations exceed that, ECS will scale out the ASG. This helps ensure when you scale services, the cluster grows automatically. Without CAS, you should monitor CloudWatch metrics like **ClusterMemoryReservation** and **ClusterCPUReservation** (these metrics show percentage of total registered resources that are reserved) – when these approach 100%, it means if you try to schedule more tasks, they’ll wait. Proactively add instances or terminate some tasks or use CAS to manage it.

In summary, tune your task definitions to accurately reflect resource needs, use scaling to handle variable load, and use placement strategies/constraints to balance performance and availability. Next, we look at the **VPC and network level** aspects of performance.

## Network Performance and VPC Considerations

Network issues can cause slow responses or timeouts in web applications. In ECS on EC2, network performance is a factor of both the container networking mode and the VPC infrastructure (subnets, routes, gateways, security settings). Let’s break down potential network-related bottlenecks:

### Container Networking Modes and Performance

ECS supports several network modes for tasks:

- **awsvpc:** Each task gets its own network interface (ENI) and is directly in the VPC subnet with its own IP. This mode offers maximum isolation and behaves like a separate host on the network. Performance-wise, it uses the EC2 instance’s ENA capabilities but dedicates an ENI per task. The overhead includes attaching/detaching ENIs (which has a rate limit) and slightly higher memory usage on the host per ENI. Throughput per ENI can also be limited, but usually the instance’s overall bandwidth is the main limit. Awsvpc is the recommended mode for most use cases, especially when using service discovery or needing each task addressable (for example, for service mesh or direct communication).
- **host:** The container shares the host’s network stack. If your container runs on port 80, it binds the host’s port 80. This mode has very low overhead (no NAT, no extra interfaces) – effectively the same performance as running the process on the host itself. It’s good for cases where you need high packet rates or low latency (some people use host mode for game servers or real-time systems). However, you cannot run multiple containers on the same port on one host (since they’d conflict on host port).
- **bridge:** This is Docker’s default NAT mode. Containers get an internal IP on a Docker bridge (usually `172.x` address) on the host, and the host performs NAT for outgoing traffic, and port mappings for incoming. Bridge mode adds a little overhead due to NAT (iptables translation of addresses) and can become a bottleneck with many containers or high throughput. It’s generally fine for moderate loads, but awsvpc has largely replaced it for ECS because awsvpc gives each container an actual VPC IP (which is simpler for connectivity and security).

**Performance tip:** If you experience high network latency or low throughput:

- Check if you’re using bridge mode and hitting any Linux NAT limits (like conntrack table might be an issue if tens of thousands of connections). With awsvpc, connections are tracked per ENI similarly but since each task has its own IP, this spreads the load.
- If using awsvpc, ensure the ENI’s security group isn’t causing packets to be excessively filtered (though SG processing is at instance level, it’s usually not the bottleneck).
- Host mode can squeeze out a bit more performance for certain scenarios at the expense of isolation. For a web app behind an ALB, host or awsvpc both work (ALB can route to instances by instance port for host mode, or to IP addresses for awsvpc mode). Awsvpc is typically preferred unless you specifically need to avoid the ENI attachment time or want to bypass the AWS networking stack.

**DNS and Service Discovery:** If tasks need to talk to each other (microservices), consider using AWS Cloud Map or ECS Service Discovery (or the newer ECS Service Connect). If misconfigured DNS, it can cause slow lookups. For example, a common oversight is not enabling DNS hostnames in the VPC for internal service names or not configuring the container’s `/etc/resolv.conf` to use the VPC DNS. Ensure that the ECS instances’ DHCP options set includes the VPC DNS server (usually the VPC base IP + 2). Also, internal AWS services should be accessed via their VPC endpoints if possible to improve speed and not go through NAT (for example, writing to S3 or calling AWS APIs – VPC endpoints can reduce latency and cost).

### VPC Subnets, Routes, and NAT Gateway

**Subnet Configuration:** The placement of ECS instances in subnets (public or private) influences network flow:

- **Private Subnets + NAT (common pattern):** ECS instances are in private subnets (no direct internet). Outbound traffic goes to a NAT gateway in a public subnet, then out to the Internet Gateway (IGW). This is secure and typical for web apps that don’t need direct inbound access (since inbound comes via ALB).
- **Public Subnets:** ECS instances could be in public subnets (with public IPs). They can directly access the internet via IGW and also receive inbound traffic. This is less secure (instances exposed, rely on security group) but sometimes used for simplicity or if instances themselves serve traffic (not common with ECS since usually ALB is used).

For a web app, we usually have ALB in public subnets, instances in private. Ensure your **route tables** are correct: private subnets should have a default route to the NAT gateway; public subnets have default route to IGW. If mis-routed, instances may not reach the internet or vice versa.

**NAT Gateway Performance:** NAT Gateways are managed by AWS and scale automatically from 5 Gbps up to 100 Gbps of throughput. They can handle a large number of concurrent connections (up to 55,000 connections per ENI and can be scaled by allocating multiple public IPs if needed, reaching hundreds of thousands of connections). It’s unlikely to be a bandwidth bottleneck unless you run extremely network-intensive workloads. However, two considerations:

- **NAT Gateway Capacity:** While it scales, there have been cases where extremely sudden bursts of traffic see some latency as it scales up. If your application does something like suddenly initiate tens of thousands of connections (e.g., mass update job), monitor the NAT Gateway CloudWatch metrics. Key metrics include ActiveConnectionCount, PacketDropCount, etc. If ActiveConnectionCount is near the limits or if you see drops, you might need to distribute load across multiple NAT gateways (e.g., split your private subnets such that two NAT gateways serve different subnets).
- **Cost of NAT:** This is tangential to performance, but a common “issue” is high NAT data processing costs if your app sends a lot of data out. It doesn’t directly slow performance, but if teams try to avoid cost by removing NAT or shutting it down, then private instances lose connectivity. A performance-affecting scenario is if someone accidentally deletes the NAT gateway or misconfigures routes to save cost – instances would then not reach internet, causing failures (e.g., failing to reach external API endpoints, or failing to pull container images from ECR if ECR VPC endpoint not used).

**NACLs and Routing:** Network ACLs (NACLs) at the subnet level can also affect traffic. If NACLs are overly restrictive (stateless), they might be blocking or slowing down connections (though stateless filtering shouldn’t slow, it would just drop). Ensure NACLs allow ephemeral ports back in for responses if you’ve customized them. Typically, it’s easier to rely on security groups for controlling traffic.

### Security Groups Misconfigurations

Security Groups (SGs) are the firewall for EC2 instances and ENIs. Misconfigurations here often appear like network performance issues (timeouts or refused connections):

- **Inbound Rules:** For your ALB to communicate with ECS tasks, the tasks’ security group must allow traffic from the ALB’s security group or subnet on the relevant port. If you forget this, the health checks and traffic from ALB to tasks will fail or be sporadic. This can look like the service is unresponsive. Always verify: ALB SG allows incoming from anywhere on port 80/443, and ECS instance/task SG allows incoming from ALB SG on the task’s port.
- **Outbound Rules:** By default, security groups allow all outbound. If someone tightened them, the ECS tasks might not reach external services (for example, if outbound DNS (port 53) or HTTPS (443) is blocked, the app might hang on external API calls or image pull might fail). Ensure outbound to needed services is permitted. A typical SG setup is to leave outbound open or specifically allow outbound to known external IPs if strict.
- **SG Dependencies:** If your tasks talk to an RDS database, the RDS SG must allow the task’s SG. If that’s missing, connections will time out. If a task calls an internal service on another ECS service, check the SGs allow traffic between them (maybe use a common SG or rules to allow each other).
- **Connection Tracking Limits:** Unlikely in normal use, but extremely high connection churn on a single SG might stress connection tracking. AWS SGs handle a lot, so this is rare, but if each task rapidly opens/closes thousands of connections, the SG’s state table might lag. Usually, you’d see host CPU from the vpc firewall engine spike if that were the case.

**Diagnosing Network Issues:**

- Use **VPC Flow Logs** in problematic subnets to see if traffic is being rejected (the flow log will show dispositions ACCEPT or REJECT). For example, flows from instance to some IP might be rejected due to SG or NACL. Flow logs can pinpoint which rule (they show a status code).
- Use traceroute/ping from the container or EC2 host. You can use ECS Exec or SSH to the instance and then enter the container’s namespace to test connectivity. If ping to an external host fails, check DNS resolution (perhaps the instance can’t resolve if VPC DNS or Route 53 resolver is broken).
- Check the **Container’s /etc/resolv.conf** if the app can’t resolve DNS. It should point to the VPC DNS IP (like 172.31.0.2 in default VPC CIDR). If not, maybe the Docker daemon is misconfigured or you have a custom DNS setting.

### Enhanced Networking and Throughput

We touched on ENA under EC2 CPU/Network. To reiterate in network context: ensure **enhanced networking** is enabled. All Nitro instances have it by default, but if using older generation (like M4, C4) ensure the `ixgbevf` driver is installed (for those, which use Intel VF). If not, network performance will be limited and CPU usage for network interrupts will be higher.

**Throughput Limits per Instance:** Each instance type has documented bandwidth (“Up to X Gbps” or a range). For example, an m5.large is “Up to 10 Gbps”. This typically means at baseline it can do a certain amount and can burst to 10. If your tasks collectively push more than that, you’ll be capped. We rarely see this in typical web apps (10 Gbps is a lot of web traffic), but if streaming or large file transfers, choose bigger instances which have higher network performance. Instances like m5n or c5n have enhanced networking with guaranteed higher bandwidth.

**Packets Per Second (PPS):** Small instance types can also be limited by PPS (not just raw bandwidth). If you handle many tiny requests (lots of small packets), you could hit a PPS bottleneck. This usually shows as increased latency once you hit the limit. Solution: larger instance or distribute load.

**Monitoring Network:** CloudWatch metrics per instance (NetworkIn/Out) can tell you bytes, but not directly bandwidth usage unless you know the time interval (the graph will show a spike in bytes per 5-min). If you see consistently high values (and near the documented max for the instance type), it’s a sign to scale out or up. Container Insights can show network usage per task, which is handy to identify which service is using bandwidth.

### VPC Endpoints and Internal Traffic

For performance and security, consider using VPC Endpoints for services your tasks call:

- If your web app calls AWS services (S3, DynamoDB, SQS, etc.), using a VPC interface endpoint means those calls don’t go out via NAT and back in – saving latency and NAT bandwidth. This can significantly reduce load on NAT gateway and improve throughput for those calls.
- For example, pulling container images from ECR at startup: you can use an ECR VPC endpoint so the image pull stays within the AWS network, making it faster and not dependent on NAT/IGW.

### Summary of Network Best Practices:

- Place ECS tasks in appropriate subnets (usually private with NAT for outbound).
- Ensure NAT gateway is present and scaled for any heavy outbound traffic.
- Use security groups to allow necessary traffic (ALB to instances, instance to DB, etc.) and double-check if facing timeouts.
- Use awsvpc network mode for isolation and simpler security, unless you have a specific need for host networking.
- Enable enhanced networking (ENA) for high throughput, and consider instance types with higher network capability if needed.
- Monitor network metrics and consider VPC endpoints for internal AWS service calls to reduce external dependency.

Next, we’ll move into **interpreting metrics and logs** which tie everything together and then go through concrete troubleshooting scenarios step-by-step.

## Interpreting CloudWatch Metrics, Logs, and Custom Metrics

Effective troubleshooting relies on good observability. In AWS, the primary tools are Amazon CloudWatch (for metrics and logs) and the ECS console/events for real-time info. We’ll also mention custom metrics and log analysis.

### Key CloudWatch Metrics for ECS and EC2

Understanding which metrics to monitor will help pinpoint issues:

- **ECS Service Metrics:** As noted, ECS reports CPU and Memory utilization for services. These are found in CloudWatch under the `ECS/ContainerInsights` or as custom metrics if using the old method. High values indicate tasks are at their limits. ECS also reports a RunningTaskCount metric per service. If DesiredTaskCount != RunningTaskCount, something’s wrong (either scaling in progress or tasks failing to start).

- **ECS Cluster Metrics:** If you enabled CloudWatch Container Insights for ECS, you get cluster-level aggregation like total CPU reserved vs available, total memory reserved vs available, etc. If not, you still have the data via AWS APIs: you can describe cluster or look at CloudWatch metrics for ECS like `CPUReservation` and `MemoryReservation` (percentage). These show how full the cluster is. If 100%, you cannot schedule more tasks – a classic cause for pending tasks.

- **EC2 Instance Metrics:**

  - _CPUUtilization:_ primary indicator of CPU load. If consistently high (near 100%), check tasks on that instance. If it’s a burstable instance, also check CPUCreditBalance – if that is 0 and CPUUtilization flatlines at some value (like 20%), you’ve hit the throttle.
  - _NetworkIn/Out:_ to see traffic levels. A sudden drop might indicate a network issue, a sudden spike might correlate with high latency (maybe saturating link).
  - _StatusCheckFailed:_ if an instance is failing health checks (could be due to high CPU causing soft lockups or networking issues).
  - _Memory (Custom):_ If you install CloudWatch agent, you can get MemUsage % and available memory. For container instances, memory being near 100% is dangerous (host OOM likely).

- **Application Load Balancer Metrics:** These complement ECS metrics:

  - _RequestCount:_ overall load. If this increases and your service didn’t scale accordingly, each task gets more load -> higher CPU etc.
  - _TargetResponseTime:_ average latency. If this jumps while ECS CPU is high, likely CPU-bound. If latency jumps but CPU is low, maybe external dependency issue or network.
  - _HTTP 5xx errors:_ Many 5xx from your targets might indicate containers are failing under load (e.g., throwing errors or being OOM-killed causing 502/504 to client).
  - _HealthyHostCount:_ If this flaps, tasks might be failing health checks (perhaps due to memory/CPU starvation making them unresponsive). ALB health check failures often precede an ECS service replacement.

- **NAT Gateway Metrics:** For network egress problems, CloudWatch has metrics like ActiveConnectionCount, ErrorPortAllocation (if it can’t assign a port – rare), BytesIn/Out. If ActiveConnectionCount is at 64,000+ it might be reaching a soft limit (each NAT Gateway by default can handle \~55k concurrent to a single IP; AWS improved multi-IP handling recently). If there are ErrorPortAllocations or PacketDropCount, definitely something to look at – could mean tasks are opening connections faster than NAT can keep up at that moment.

### Container Logs and What to Look For

ECS allows sending container stdout/stderr to CloudWatch Logs (via log driver). Ensure this is enabled (`awslogs` driver or FireLens etc.), otherwise you might have to SSH to instances to get Docker logs.

In CloudWatch Logs for your application container:

- Look for **exception stack traces** or error messages. These often directly pinpoint the issue (e.g., “OutOfMemoryError” or “Timeout connecting to DB”).
- If the container was OOM-killed, sometimes you see a log like “Killed” right before shutdown, or nothing at all (sudden stop). The ECS agent will log an event though.
- If the app is slow, maybe thread dumps or warnings appear (e.g., a Java app might log GC pauses).
- For CPU issues, the app might not log anything; you might need to infer via response time logs. If the app logs each request and you see response times increase as CPU goes high, that’s a correlation.

ECS agent and daemon logs:

- The ECS agent on each instance logs to `/var/log/ecs/ecs-agent.log`. If tasks won’t start, check this for errors pulling images or connecting to ECS backend.
- Docker daemon logs (`/var/log/docker` or `journalctl -u docker`) might show if container was OOM-killed or if there was a crash.

**Log Aggregation and Analysis:** If logs are in CloudWatch, you can use CloudWatch Logs Insights – a query language to filter logs. For example, find all occurrences of "ERROR" or count OOM events in a time range. This helps quantify how often an issue occurs.

### Custom Metrics & Application Metrics

Sometimes CloudWatch’s system metrics aren’t enough. Custom metrics (perhaps emitted by your application, or collected via a sidecar/agent) can provide deeper insight:

- **Examples:** Number of active user sessions, length of an internal queue, garbage collection pause time, etc. These can expose whether the app logic is the bottleneck.
- If using Prometheus (discussed later), your app can expose metrics that you scrape.
- If using CloudWatch, you can put custom metrics via the AWS SDK (for example, push a metric for “CacheHitRate”). These can then be alarmed or graphed.

**ECS CloudWatch Container Insights:** When enabled, this feature uses embedded CloudWatch agent on the ECS instances (or in Fargate’s case, the platform) to collect more metrics:

- It can give per-container CPU and memory without you setting up anything. Also disk I/O per task and network per task.
- It can even provide a “Summary” of top tasks by CPU/memory.
- Enable it when you create the cluster or via AWS CLI – it’s very useful for troubleshooting because you can pinpoint which container is using resources most.

### Example: Reading a CPU Spike in Metrics

To illustrate: Suppose your service latency spiked at 12:00. You check CloudWatch:

- ALB RequestCount surged at 11:55, doubling traffic.
- ECS Service CPU Utilization went from 50% to 95% around 12:00, meaning tasks were maxing out their CPU (each using nearly all allocated units).
- ECS Service set desired count from 4 to 8 tasks at 12:05 (you see a CloudWatch alarm or ECS event that scaling kicked in).
- By 12:10, with 8 tasks, CPU Utilization came down to 60% and latency recovered by 12:15.

From this, the timeline shows that auto-scaling was a bit slow to react, and during the interval 12:00-12:10 the tasks were overloaded, causing latency issues. The solution might be to adjust scaling to trigger at lower utilization or add 4 tasks instead of 2 (step scaling).

Another example: memory leak:

- CloudWatch custom metric (if using Container Insights) shows Service memory utilization climbing from 60% to 99% over several hours.
- At the same time, you see in CloudWatch Logs an increasing frequency of Garbage Collection messages, then finally an **OutOfMemoryError** at the time a task died.
- ECS Service events: “task X stopped (exit code 137, OOM)” around that time.
- All evidence suggests a memory leak or unexpected load causing memory exhaustion. Short-term fix: increase the task’s memory limit or restart tasks periodically. Long-term fix: find the leak in code.

By correlating metrics and logs, you can often triangulate the cause.

Next, let’s walk through **step-by-step troubleshooting scenarios** tying together these approaches for typical issues.

## Step-by-Step Troubleshooting Scenarios

In this section, we’ll present several common performance problem scenarios with a systematic approach to investigate and resolve each. Each scenario will include the symptoms, diagnostic steps (with example commands or observations), and the solution or mitigation.

### Scenario 1: High CPU Utilization Causing Slow Responses

**Symptoms:** Users report that the web application is slow under load. Pages take long to load especially during traffic peaks. The ALB target response time metric shows increased latency. In CloudWatch, the ECS service’s CPU utilization is near 100% during these slow periods.

**Troubleshooting Steps:**

1. **Identify the Scope:** Check if the high CPU is at the container level or instance level. Go to CloudWatch metrics:

   - ECS Service CPU utilization is \~95-100% during incidents (meaning tasks are maxed out).
   - Look at EC2 CPUUtilization for the instances hosting those tasks. If each instance is also near 100%, it means tasks collectively saturate the host.
   - If instance CPU is lower but task CPU is at 100%, it could mean the task’s CPU units are fully used but the instance has other capacity (maybe other tasks aren’t using their share).
   - In our case, assume both tasks and instances are at limit (so, we are truly CPU-bound).

2. **Examine Task Placement:** Are tasks evenly spread? Check ECS console or use CLI `aws ecs list-tasks` and `aws ecs describe-tasks` to see which container instances they landed on. If you find that one instance has multiple tasks all hitting CPU 100% while another instance is relatively idle:

   - Possibly a placement issue (maybe not enough tasks to spread or placement strategy not ideal). If only one instance had tasks, then that instance CPU is 100% and others 0% – solution: spread tasks or increase desired tasks across instances.

3. **Check Instance Type (Burstable?):** Are we on T3 instances? If yes, check CPU credit balance:

   - Use CloudWatch or AWS CLI (`aws cloudwatch get-metric-statistics --metric CPUCreditBalance`). If credit balance is 0 during the event, the CPU might be throttled.
   - Look at CloudWatch CPUUtilization: if it plateaus at a specific value (like 30%) despite expecting higher, that’s a sign of credit throttling.
   - _If throttled:_ The fix is to enable unlimited mode or switch to M or C family. As a quick mitigation, scale out to more T3 instances (each gets its own baseline and credits). Long term, consider other instance types.

4. **Application Logs:** Check application logs for anything indicating slowness:

   - Perhaps threads are timing out or there is a specific operation repeatedly logged.
   - If the app itself logs a profiling info (like “processed X requests in Y seconds”), see if that drops.

5. **Runtime Diagnostics:** During high CPU, it can help to get a snapshot:

   - Use ECS Exec to connect to one of the running containers (if it’s Linux): `aws ecs execute-command --cluster myCluster --task <task-id> --container myAppContainer --command "top -b -n1"` to see process CPU inside the container, or run a profiler if available.
   - Alternatively, SSH to the EC2 and run `docker stats` or `top`: identify if it’s the application process consuming CPU or something else (e.g., a sidecar or a stuck system process).
   - 99% of the time, it will be the app process (e.g., a Java process using 200% CPU on a 2 vCPU system meaning 2 cores fully busy).

6. **Scale or Optimize:** Short-term relief is to reduce load or add capacity:

   - If possible, increase ECS service desired count so load is spread. Ensure cluster has room or scale the cluster.
   - Since this is a web app, adding tasks will linearly add capacity (assuming stateless).
   - Check auto-scaling config – maybe it wasn’t aggressive enough. If using target tracking on CPU 80%, but traffic spiked quickly, there might be lag. Consider a step scaling policy to add a chunk of tasks when CPU > 90%.
   - If already at max tasks you can run, then instance scaling is needed. Add more EC2 instances to the cluster.

7. **Investigate Code Efficiency:** High CPU could be due to inefficient code (e.g., N+1 database queries, lack of caching, heavy JSON parsing, etc.). Profile the application offline or in a test with similar load:

   - Use APM tools or profiling in a load test environment to identify hotspots.
   - This goes beyond AWS, but it’s the long-term fix if scaling up is undesirable.

8. **Outcome:** After adding 2 more instances and doubling task count, CPU dropped to \~50% per task at peak and response times returned to normal. Auto-scaling policy was adjusted to scale out faster. We also identified a potential code bottleneck (missing cache on a frequently called API) which the dev team will fix in the next release, which should further reduce CPU load.

### Scenario 2: Memory Leak and Out-of-Memory Crashes

**Symptoms:** The ECS service has tasks that keep restarting periodically. Users occasionally get errors as requests are dropped. In ECS console, you notice tasks stopping with exit code 137. In CloudWatch, service memory utilization creeps up over time and then drops suddenly (repeat pattern), suggesting tasks use more and more memory then get killed and restarted.

**Troubleshooting Steps:**

1. **Confirm OOM Kills:** Exit code 137 and the ECS service events likely indicate OOM. Check ECS service events:

   - You might see: “service myService (port 8080) task 12345678 died due to OutOfMemoryError.” Or an event like “Container killed due to memory usage”.
   - If the event isn’t clear, connect to the container instance and inspect `/var/log/messages` around the time of a crash for “Kernel OOM” messages. It often logs which process was killed and why (e.g., “Killed process 12345 (java) total-vm:… out of memory”).
   - CloudWatch Logs for the container might show an exception (if the app caught it) or simply end abruptly.

2. **Memory Utilization Metrics:** Look at CloudWatch Container Insights for that task or service:

   - Likely you see memory usage steadily increasing (e.g., 500MB -> 800MB -> task restarts when hitting 1024MB limit).
   - If the usage was near the hard limit (memory), then the container was terminated by Docker once it tried to exceed it.
   - If only soft limit was set, the host might have run out of memory. Check host memory at that time (if you have CloudWatch agent memory metrics or look at swap usage on host).

3. **Check Task Definition Limits:** What is the memory hard limit set to?

   - Say it’s 1GB. The app might be hitting that.
   - Consider increasing it temporarily to see if tasks stabilize (maybe the app legitimately needs more memory under load).
   - However, if this looks like a leak (monotonic increase), raising limit might just delay the crash.
   - Example: You set it to 2GB, now tasks run twice as long before OOM. That’s a clue it’s likely a leak or unbounded usage.

4. **Collect Diagnostic Data from Container:**

   - Use ECS Exec or kubectl (if using ECS Anywhere with K8s, but here with ECS exec): run `heap dump` or memory profiling tool inside the container (for Java, jmap; for Python, tracemalloc snapshot; for Node, --inspect memory snapshots).
   - If not possible in production, replicate in staging by running a soak test.
   - The goal is to identify what in the app is consuming memory – e.g., a cache that never evicts, or large objects accumulating.

5. **Inspect Logs for Errors:** Sometimes memory pressure causes other errors, e.g., OutOfMemoryError in logs or GC overhead warnings.

   - Indeed, the logs showed “java.lang.OutOfMemoryError: Java heap space” just before the container died. That confirms a leak or undersized heap.

6. **Solutions:**

   - **Code Fix:** Find and fix the memory leak. This is the ultimate resolution.
   - **Increase Memory or Use Soft Limits:** As a stop-gap, you could allocate more memory to the task so it doesn’t OOM so fast. But without code fix, it might still eventually leak.
   - **Add a Memory Liveness Probe:** If possible, make the app detect its own high memory and restart gracefully (though on ECS, you’d rely on external monitors).
   - **Schedule Restarts:** Not ideal, but some teams schedule daily task restarts during low traffic to clear memory, as a band-aid for leaks.
   - **Enable Swap (if appropriate):** ECS allows setting a swap space in task (linuxParameters). If your app can tolerate swapping (most cannot without performance hit), this could save it from immediate OOM by swapping some memory to disk. But likely not useful for a web app due to latency impact.

7. **Verify Fix:** After deploying a code update that fixes the leak (e.g., cleared a cache properly), monitor memory: it should plateau at some stable level instead of endlessly rising. No more task restarts should occur.

8. **Preventive Measure:** Implement CloudWatch alarms on memory usage. For example, an alarm if service memory utilization > 90% for 15 minutes, so you get notified before OOM kills happen. Also, use AWS X-Ray or other tracing to ensure no requests are gradually consuming more memory (sometimes a particular request pattern triggers the leak).

### Scenario 3: Network Latency and Throughput Bottleneck

**Symptoms:** The application works but during peak usage, users experience timeouts or very slow responses for certain features. For example, API calls to a third-party service sometimes time out. The web app itself sometimes logs errors that it cannot reach an external API. Other times, pages load partially. These issues correlate with high traffic times. CPU and memory on ECS tasks look fine.

**Troubleshooting Steps:**

1. **Identify if it’s internal or external network issue:**

   - If the app itself (serving its own pages) is slow, and not just external API calls, suspect general network saturation.
   - If only calls to an external API (e.g., payment gateway) are failing, maybe that external API rate-limited or your NAT gateway or internet connectivity is the issue.

2. **Check EC2 Network Metrics:** In CloudWatch, check the **NetworkOut** metric on the NAT Gateway (if available) and on the ECS instances:

   - Are we pushing a lot of bandwidth? If NetworkOut is at the max for instance type (check instance specs), that’s a red flag. E.g., an instance with “Up to 1 Gbps” might show 125 MB/s (1 Gbps) usage steadily.
   - Check **ActiveConnectionCount** on NAT gateway CloudWatch metrics. If it’s extremely high (tens of thousands), we may be hitting connection limits.
   - Also, see **PacketDropCount** on NAT gateway; any non-zero suggests connections dropped (possible ephemeral port exhaustion or too many concurrent flows).

3. **Examine NAT Gateway Limits:** AWS states 5 Gbps scaling to 100 Gbps and around 55k concurrent connections per IP by default. If you need more, AWS can now allow multiple IPs on NAT for more connections.

   - If your app opens many connections (e.g., lots of DB connections through NAT, or many external calls), consider reusing connections or introducing keep-alive to reduce churn.
   - If NAT is indeed the bottleneck, one strategy: if possible, deploy another NAT gateway and split load (e.g., half the instances use NAT A, half use NAT B by being in different private subnets). This is advanced and costs more, but can distribute connections.

4. **Security Group / NACL issues:** Are timeouts caused by misconfigurations?

   - If the external API is being called through a VPC endpoint or proxy, ensure those SGs allow the traffic.
   - If the service is calling an API that requires static IP, maybe NAT’s IP is not whitelisted by them (leading to timeouts). Then you’d need an Elastic IP or NAT config specifically.

5. **DNS issues:** Sometimes high latency is due to DNS lookups if the code isn’t caching DNS properly.

   - If each request does DNS lookup for an external host, that adds latency. You might see in logs or X-Ray traces that DNS resolution took long.
   - Solution: enable DNS caching in app or use VPC DNS. Also, check if the instance’s DNS resolver is functioning (CloudWatch Metric “DNSResolutionTime” if any? Usually not directly available, but you can test manually).

6. **Perform a traceroute from inside a container:** See where the delay is:

   - Maybe it hangs at the NAT gateway or beyond. If an external provider is slow, nothing you can do except maybe switch provider or escalate to them.
   - If it hangs immediately, could be DNS or SG blocking.

7. **Scale Out or Up:** If network throughput on instances is the issue, scaling out (more instances, each handles a share of connections) or scaling up (bigger instance with better network) will help.

   - For instance, moving from t3.small (limited net) to t3.large (better net) or to m5.large which has higher baseline bandwidth.
   - If using Fargate-like approach was an option, that’s not in scope here, but just note ECS EC2 you manage instance networking.

8. **Outcome:** In our case, we found the NAT gateway had extremely high active connections and some packet drops during peak. We mitigated by enabling HTTP keep-alive in the application for external API calls (reducing new connections), and by upgrading the instances to m5.xlarge (which provide higher network throughput). We also added a VPC Endpoint for S3 since a lot of traffic was going to S3 (offloading that from NAT). After these changes, network metrics are well below limits and no more timeouts observed.

### Scenario 4: ECS Service Not Scaling as Expected (Insufficient Capacity)

**Symptoms:** You increased the desired count of an ECS service or an auto-scaling event tried to add tasks, but some tasks are stuck in `PENDING` state and never launch. Or the service is auto-scaling but cannot reach the new desired count. Users might be unaffected at first (just less capacity than expected), but if a task was replaced and cannot start, capacity drops.

**Troubleshooting Steps:**

1. **Check ECS Service Events:** The first place is ECS service events tab. Often very explicit:

   - e.g., “Service unable to place task because no container instance met all requirements. Needed 512MB memory, 256 CPU; available 200 CPU on instance i-abc, 0 CPU on i-def” etc.
   - Or “unable to place task because of placement constraints”.
   - If using Capacity Provider with managed scaling, possibly “could not scale ASG fast enough” type messages.

2. **Identify Resource Shortage vs Constraint:**

   - If message mentions CPU or memory, it’s a capacity shortage. All instances are full. Verify by checking cluster metrics (CPUReservation maybe 100%). Solution: add more EC2 instances (either manually or ensure Auto Scaling Group can scale).
   - If it mentions **ports**, sometimes with host networking if a port is already taken on all hosts, you can’t place more tasks. (For awsvpc, each task gets its own IP so ports don’t conflict, but for host mode they do).
   - If it mentions **ENI** or **IP**, likely the ENI limit. Each instance type can only attach so many ENIs (including primary). For example, a c5.large can handle up to 3 ENIs (1 primary + 2 tasks in awsvpc). If you already have 2 tasks with awsvpc on that instance, a third won’t fit because no ENI slot. The event might say “Resource: ENI” not available.

     - You can confirm by checking the ECS instance attributes: each container instance has attributes like `ecs.available-enis`. Or see AWS docs for “ENI per instance limit”.
     - Solution: use bigger instances with higher ENI limits or spread tasks to more instances (again means adding instances). Another solution is using ECS Task networking with trunking (for hundreds of tasks per instance) but that’s a more complex setup and beyond scope.

3. **Placement Constraints Issues:**

   - If using `distinctInstance` and you requested more tasks than instances, the extra will pend. Either remove that constraint or add instances. For example, distinctInstance with 3 tasks but cluster only 2 instances will leave 1 pending.
   - If using `memberOf` constraint like instance type = m5, but your ASG accidentally had an m4, it will never place. Adjust the constraint or instance type.

4. **EC2 Auto Scaling Group:** Check if the ASG for the ECS cluster is at capacity or has scaling events:

   - Perhaps CAS (cluster auto scaling) should have added an instance but didn’t because of a misconfiguration or hitting ASG max.
   - Increase the ASG max size or manually trigger adding an instance. Once a new instance registers, ECS will place the pending tasks (assuming no other constraints).

5. **Iam Role Issues (less likely for performance, but):** If tasks fail to start for reasons like cannot pull image or no permission, that shows up differently (task goes to STOPPED with error). But for completeness: ensure the ECS agent has the correct IAM role (with ECSInstanceRole) so it can register properly. If agent can’t register, ECS will think no capacity even if instance running.

6. **Solution Implementation:** If the cluster lacked resources:

   - Add more instances. E.g., scale ASG from 3 to 5. Wait for them to join. ECS will automatically deploy pending tasks there.
   - Remove or relax a constraint if it was artificial (maybe you used distinctInstance by habit but in a dev environment you only have one instance – just remove it for that).
   - If ENI limits were reached and you can’t add instances (due to cost or region limits), consider switching some tasks to bridge mode if possible (not recommended normally) or reduce tasks per instance.

7. **Verification:** The ECS service should reach the desired count and show all tasks RUNNING. Service events will show “Successfully placed task” messages. Also check that the new tasks pass health checks (so they actually take traffic). If ALB target group shows some targets unhealthy, that’s a different issue (maybe the app isn’t coming up properly, or SG not allowing health check port).

### Scenario 5: VPC Misconfiguration Causing Connectivity Issues

**Symptoms:** After a deployment or infrastructure change, the application entirely fails to work. All tasks are running, but none of the requests succeed. Users see timeouts. CloudWatch metrics show no traffic reaching tasks, or perhaps ALB 5xx errors. This scenario is like a sudden outage due to network misconfig.

**Troubleshooting Steps:**

1. **Check ALB Health Checks:** Go to the ALB target group in AWS console:

   - Are targets (ECS tasks) healthy or unhealthy? If unhealthy, the ALB isn’t connecting to them.
   - If tasks are unhealthy, describe target health; it might say “Target not responding” or “Connection timed out”.
   - This indicates the network path from ALB to container is broken.

2. **Security Group Review:** Perhaps a security group was changed:

   - Ensure the ECS tasks’ security group allows traffic from the ALB’s security group on the target port.
   - If someone removed that rule, all health checks and traffic would be blocked (ALB can’t reach tasks -> tasks marked unhealthy -> no traffic flows).
   - Fix: re-add the rule (`Inbound: allow traffic from sg-ALB on port XYZ`).

3. **Subnet Routing:** If ECS tasks are in private subnets and ALB in public, check the route tables:

   - Private subnets should have a route to NAT for internet, but they also need local routing for ALB (which they have by default since ALB is in same VPC).
   - If someone accidentally changed the VPC ACLs to block traffic between subnets or removed the ALB’s subnet association, that could break.
   - Check NACLs: if a NACL on the tasks’ subnet now has an outbound rule that doesn’t include ALB’s subnet range or ephemeral ports, return traffic might be dropped. Default NACL allows all, but if custom, ensure ephemeral port range (1024-65535) is allowed back in.

4. **DNS or Configuration:** If using Service Discovery, maybe the service connect endpoint changed. But for an ALB scenario, likely not applicable.

   - However, if using AWS Cloud Map for internal comms, ensure those names still resolve. Not likely to cause complete outage for external users though.

5. **Test Connectivity Manually:**

   - From an ECS container instance (SSH), try to reach the ALB:

     - `curl http://<task-ip>:<port>` from the ALB node (if you can get on ALB node via debug which is not trivial; instead curl from instance to itself to simulate).

   - Alternatively, spin up a test EC2 in same private subnet and attempt to reach the task container’s IP\:port. If that fails, it’s SG or NACL.
   - Use `telnet taskIP port` or `nc` to test connection.

6. **Common Mistake:** Deploying tasks in the wrong subnets:

   - Perhaps someone updated the service to use a new subnet (maybe a private subnet in a different AZ that the ALB isn’t in). If the ALB isn’t in that AZ or not configured to route there, those tasks wouldn’t get traffic. Actually ALB target group auto registers instances by AZ if enabled – check ALB is set to include the new AZ.
   - If tasks launched in an AZ where the ALB has no subnet (target group would show them but “unavailable AZ”), then solution: add an ALB subnet for that AZ or restrict tasks to only AZs ALB covers.

7. **Solution:** For our example, it turned out a security group rule was deleted during a cleanup. We quickly re-added the rule to allow the ALB’s SG to reach the ECS tasks on the application port. Immediately, ALB health checks started passing and traffic flowed normally again.

8. **Follow-up:** Implement an AWS Config rule or at least documentation to not remove that crucial rule. Also, set up CloudWatch alarms on ALB UnHealthyHostCount or TargetResponseTime so that if this happens, ops can be alerted to check SG configuration quickly.

These scenarios demonstrate a process: observe symptoms, correlate with metrics/logs, find the likely cause, apply fixes, then verify. Next, we will discuss tools that can make monitoring and troubleshooting easier and more proactive.

## Monitoring and Alerting Solutions

Proactive monitoring and quick debugging are greatly aided by specialized tools. AWS provides some native solutions (CloudWatch, X-Ray), and there are popular third-party tools (Prometheus/Grafana, Datadog, etc.) that integrate well with ECS. Here we overview how each can help with performance issues:

### Amazon CloudWatch for ECS

CloudWatch is the default monitoring service in AWS and integrates tightly with ECS:

- **Metrics & Dashboards:** CloudWatch automatically collects ECS service metrics (if enabled) for CPU/Mem, plus the EC2 metrics. You can create custom CloudWatch Dashboards showing your ECS cluster overview: e.g., a graph of Service CPU alongside ALB request count, etc. This makes it easier to see cause/effect.
- **Logs:** With the CloudWatch Logs agent or by using the `awslogs` log driver for containers, all application logs go to CloudWatch. You can then use Logs Insights as mentioned to search them.
- **Alarms:** Set up CloudWatch Alarms for key metrics. Examples:

  - CPUUtilization > 85% on any instance for 5 minutes -> trigger an alarm (could tie into scaling or at least notify you).
  - Service MemoryUtilization > 90% -> alarm (potential memory leak).
  - ALB 5xx error count > 0 for N minutes -> alarm (could indicate tasks failing).
  - UnHealthyHostCount > 0 for target group -> alarm.
  - These alerts can go to SNS or an Ops team email/Slack.

- **CloudWatch Container Insights:** If you enable this, it not only gathers metrics but also provides **Service Map** and **ECS Prometheus** integration. It can show you a map of your ECS services and some relationships, and you can also ingest Prometheus metrics (if your containers expose them) into CloudWatch. This reduces the need to run a separate Prom server if you prefer AWS-managed approach.
- **Logging ECS Agent:** CloudWatch can also collect OS logs – you might consider capturing `/var/log/ecs/ecs-agent.log` into CloudWatch for easier viewing of any agent issues.

CloudWatch is very useful but sometimes you need deeper application insights or retention beyond 15 months, etc. That’s where tools like Prometheus and Datadog come in.

### Prometheus and Grafana

**Prometheus** is an open-source monitoring system that scrapes metrics from instrumented applications (typically on `/metrics` endpoint). In an ECS context:

- You can run Prometheus on ECS itself (there are guides to deploy Prometheus in the cluster), or use Amazon Managed Prometheus (AMP) as a service.
- For Prometheus to discover ECS tasks, you could use service discovery scripts or ECS Service Discovery (Cloud Map) or simply static config if tasks have fixed endpoints (less likely).
- An easier way: Use the CloudWatch agent in Prometheus-scraping mode. AWS provides a mode where CloudWatch agent runs on each instance, scrapes Prometheus metrics from tasks (for example, any container exposing port 9102 metrics), and pushes them to CloudWatch.
- **Grafana:** Once metrics are in Prom or CloudWatch, Grafana can graph them. Grafana can also pull directly from CloudWatch (there’s a CloudWatch data source plugin). Amazon Managed Grafana is an AWS service that can integrate with both CloudWatch and AMP (Prometheus).
- Use cases:

  - Plot custom app metrics (like query per second, internal queue length) alongside ECS metrics on Grafana dashboards.
  - Create alerts in Grafana or use Alertmanager (if using Prom stack) to notify on anomalies.

Prometheus is particularly good if your team is already using it and has instrumentation in the code (e.g., using client libraries to record latency histograms, etc.). It gives more granular data than CloudWatch (which is typically 1-minute resolution, though you can get 1-second for Container Insights metrics, but at cost).

### Datadog

Datadog is a hosted monitoring and APM solution with strong container support:

- **ECS Integration:** Datadog has an ECS integration that can pull CloudWatch metrics and also run the Datadog Agent as a sidecar or daemon on each ECS host. The agent can auto-detect containers and collect metrics (CPU, memory, network) and send to Datadog.
- **APM (Application Performance Monitoring):** You can use Datadog APM to instrument your application for deep tracing. This can show, for instance, which function or DB query in a request is slow, helping you pinpoint code issues rather than infra.
- **Dashboards:** Datadog provides out-of-the-box dashboards for ECS, and you can create custom ones. For example, a dashboard with container-level metrics and overlay events (Datadog can show deploy events, etc.).
- **Alerts:** Datadog’s alerting is very flexible (and they have anomaly detection, etc.). You might set an alert like “if container OOMKilled count > 0 in 5m, alert” or “if 95th percentile latency > X”.
- **Log Management:** Datadog can also ingest logs; you can send ECS logs to Datadog and then use their log analytics (similar to CloudWatch Logs Insights but unified with metrics/traces).
- The advantage is one platform for metrics, traces, and logs (the so-called “three pillars of observability”). Many teams use Datadog to reduce the manual work of integrating open-source tools.

Given our topic, Datadog’s **ECS monitoring** can directly capture ECS service events and metrics. It will, for example, know if tasks are being stopped or started. Datadog also knows the concept of an ECS cluster and can filter metrics by cluster, service, etc., making it easy to slice and dice.

### AWS X-Ray (Distributed Tracing)

AWS X-Ray is a distributed tracing service helpful for analyzing performance across services:

- If your web application calls multiple other services (e.g., microservices architecture or external APIs), X-Ray can trace a user request as it goes through the system.
- By instrumenting your application (either using the X-Ray SDK in your code or enabling X-Ray daemon/agent in ECS tasks), you can get traces showing segments like: Web request -> Service A (50ms) -> Service B (200ms) -> external API (500ms). This helps pinpoint that, say, the external API call is the slow part.
- **Service graph:** X-Ray will generate a service map that shows nodes for each service and latency/error rates between them. For example, it could show that your ECS service calls DynamoDB and external API, with average latencies and error counts.
- **Sampling:** X-Ray can sample a subset of requests or all (for low volume) and gives detailed timeline of each. You can see, for instance, that 5% of requests are slow and those all correspond to a specific path or user type.
- For ECS, you typically run the X-Ray daemon as a sidecar container that the main app talks to, which then sends traces to X-Ray service. AWS has documentation for running the X-Ray daemon in ECS (either as a daemon service on each host or sidecar per task).
- Using X-Ray, one might find that the app is slow not because of CPU, but because it’s waiting on a slow SQL query or an HTTP call. That then directs the fix (optimize the query, add caching, etc.) rather than scaling infra.

For example, imagine our Scenario 1 (High CPU). If we had X-Ray, we might see that during high load, a particular function’s segment takes 90% of the time. If that was some heavy computation, we’d know code optimization needed. Or if it shows a lot of time in “downstream API call” segment, then the CPU might be high partially because threads are waiting (maybe not the best example, but X-Ray shines in multi-tier apps).

### Other Tools and Considerations

- **AWS CloudTrail & Config:** These help audit changes. If a performance issue was triggered by an infrastructure change (like SG rule deletion or ECS config change), CloudTrail events can show who did what and when. AWS Config can alert on changes like “SG ingress removed” which could catch mistakes before they cause an outage.
- **Flamegraphs and Profiler:** If you need to profile CPU, tools like `pyroscope`, `Parca` (continuous profiling) or simply capturing `perf` or `Go pprof` data from running containers can help advanced users see where CPU cycles are going. Some APM tools integrate this (e.g., Datadog has always-on profiler for some languages).
- **EKSes:** If some teams prefer Kubernetes, EKS with Prom/Grafana and others might be considered – but that’s out of scope here as we stick to ECS on EC2.

### Setting up a Monitoring Stack (Example):

For a robust setup, you might use a combination:

- CloudWatch for basic infrastructure alarms (cheap and native).
- Prometheus + Grafana for detailed app metrics and custom metrics dashboards.
- AWS X-Ray for tracing between microservices.
- Datadog or similar if you want a unified SaaS solution (it could replace the Prom/Grafana and maybe even do tracing).

The key is to ensure **alerting** is in place so that when CPU is high or memory is leaking or latency is up, the on-call team is notified. Also, having historical data helps root cause analysis – e.g., you can compare performance before/after a deployment.

Armed with monitoring, you can often catch performance problems early (for instance, you’d see memory usage trending up days before it OOMs and fix the leak).

## Common Performance Pitfalls and How to Avoid Them

Finally, let’s summarize some common pitfalls we’ve implicitly touched and how to proactively avoid them in an ECS on EC2 environment:

- **Insufficient Resource Allocation:** One pitfall is underestimating resource needs – e.g., giving a container too little memory or CPU. The container might work fine under low load but collapse under real load. **Avoidance:** Load test your application to understand its resource profile. Set CPU/memory in task def a bit higher than the peak needed (with some headroom). Monitor actual usage in prod and adjust if needed (don’t just set and forget).
- **Overallocation and Overcommit:** The opposite – packing too many tasks into too few instances to save cost. This can lead to contention and throttling. **Avoidance:** Use auto scaling on both tasks and instances. Keep average utilization moderate (like 50-70%) so spikes can be absorbed. If you deliberately overcommit (perhaps in dev), at least know the risk and don’t do it in production.
- **Ignoring CPU Credit Mechanism:** Deploying prod workloads on T2/T3 without monitoring credits. It works fine in tests (short bursts) but fails over long high load. **Avoidance:** If using burstable instances, either enable unlimited mode or have alarms on CPUCreditBalance. Consider scheduling workloads (like batch jobs) when credits are likely available. For critical steady workloads, prefer fixed-perf instances.
- **Not Updating AMIs/Software:** Running an old ECS-optimized AMI or outdated Docker can degrade performance (memory leaks in old Docker versions, etc.). **Avoidance:** Regularly update your ECS container instances. AWS releases new optimized AMIs periodically. You can do rolling replacements of instances in the cluster (drain one, terminate, let ASG bring new one). Also update ECS agent – new versions have improvements.
- **Logging Too Much:** Writing enormous amounts of log data can IO throttle your container or incur huge network use if shipping logs. **Avoidance:** Adjust log levels in production to only what's needed. Use asynchronous logging if possible. If using CloudWatch Logs, be mindful of the 1MB/s log ingestion throttle per stream.
- **No Paging/Swapping Strategy:** If your container or instance runs out of memory, Linux will OOM kill without warning if no swap. **Avoidance:** For critical apps, consider enabling a small swap file at host level as a buffer. Or in ECS task (`linuxParameters`) you can allow swap for the container with a limit. This might slow things instead of killing, giving you time to detect. But ideally, never hit OOM by proper sizing.
- **Single AZ deployments:** Not exactly performance, but availability. If you run all tasks in one AZ and that AZ has an issue, your app will go down or have increased latency cross-AZ. **Avoidance:** Always span at least 2 AZs for production ECS services. Use ALB to balance. And in placement, ensure tasks in different AZs (the default does this).
- **Incorrect Timeouts and Retries:** If the ALB or client has shorter timeouts than the server or vice versa, you might get errors while processes still churning. E.g., ALB idle timeout is 60s by default – if your container sometimes takes 70s to respond (not great, but if), ALB will cut it at 60s causing a 504. **Avoidance:** Make sure timeouts are configured consistently. Better, ensure your app responds in reasonable time (and if not, consider breaking the work or using async/background processing).
- **No Backpressure control:** If your service gets overloaded, ideally it should reject some requests quickly (e.g., HTTP 503) instead of queueing everything and timing out. Without this, high load can cause cascading slowness. **Avoidance:** Implement concurrency limits in your app (like max threads or use a queue with limit) so that beyond certain load, you fail fast, allowing load balancer to perhaps route to other instances or trigger scaling.
- **Security Group Overly Open or Complex:** Allowing 0.0.0.0/0 on all ports ingress is a security risk. But also having extremely granular SG for each microservice can become hard to manage and even hit AWS SG per interface limits if not careful. **Avoidance:** Use a sensible middle ground: cluster-level SG or per-app SG and allow broad ports as needed (like allow service A SG to talk to service B SG on any port if on awsvpc and you trust them, or at least specific ports). Keep rules tidy.
- **Not Draining Instances:** When you scale down the cluster or deploy new AMI, if you terminate instances without draining, tasks will die abruptly which might drop user sessions. **Avoidance:** Use ECS Instance Drain functionality (set container instance state to DRAINING or if using ASG with capacity providers, it can do it). This ensures tasks are stopped gracefully (connections drained by ALB).
- **Large Container Images:** If your container image is huge (e.g., 2GB), launching new tasks will be slow (time to pull image). If auto-scaling triggers new tasks, they might take a long time to become ready, leading to temporary performance issues if scaling can’t catch up quickly. **Avoidance:** Optimize Docker images (remove unnecessary layers, use smaller base images). Also, enable ECR caching or pull through cache if possible. You could also pre-pull images on instances (perhaps via a daemon task) before a deployment.
- **EBS Bottlenecks:** If using EBS-backed storage heavily (maybe a container doing a lot of writes to an attached volume), hitting IOPS limits can slow things. **Avoidance:** Use appropriate volume type (io1/gp3 with enough IOPS). Or use instance store for ephemeral data if available.

**Proactive Measures Summary:**

- Implement autoscaling with headroom.
- Monitor everything (CPU, mem, latency, etc.) and set alerts.
- Do chaos testing or stress testing to see where the system breaks, then fix those weaknesses.
- Keep architecture diagrams and knowledge up-to-date so during an incident, you know where to look (e.g., “Oh, this service calls that one, which might be slow, etc.”).
- Have runbooks for known issues (like “if CPU credit exhausted, do X, Y”).

## Case Studies

Let’s consider a couple of real-world style case studies that tie many of these elements together:

### Case Study 1: CPU Throttling on Burstable Instances

**Background:** A startup deployed their ECS cluster on a single t3.medium instance to save cost, running 2 tasks of a web service. It worked fine in low traffic. As traffic grew, they noticed the application became extremely slow and unresponsive for periods of time, even though logs showed only moderate request volume.

**Investigation:** Through CloudWatch, they saw that CPUUtilization was capped around 30%. The ECS service CPU utilization metric was maxed at 100% (each task trying to use more CPU but couldn’t). The t3.medium’s CPUCreditBalance was zero during these events. Essentially, they ran out of CPU credits and the instance was throttled to baseline 20% of 2 vCPUs (which is 0.4 vCPU effective). The tasks were CPU-hungry (each could use 1 vCPU under load), but the burstable instance couldn’t sustain it.

**Solution:** They immediately changed the ECS instances to t3.medium _Unlimited_ mode, which allowed burst beyond credits by incurring charges. This relieved throttling (CPU could go to 70-80% now). Then they planned a move to t3.large which has higher baseline and more credits, and ultimately to m5.large for consistent performance. After switching to m5.large, CPU could go to 100% of 2 vCPUs when needed, and latency issues disappeared. They also set up an alarm for CPUCreditBalance low, in case any burstable instance is used in the future by mistake.

**Learnings:** Burstable instances can save cost but must be monitored. For a constant load web service, they decided the cost savings weren’t worth the unpredictable performance. Now they use burstable types only for dev/test or very spiky workloads that mostly stay idle.

### Case Study 2: NAT Gateway Connectivity and Scaling Out

**Background:** A company had an ECS service that called external third-party APIs (payment processing, OAuth provider). The ECS tasks were in private subnets with a NAT gateway for egress. Under normal load, everything was fine. On Black Friday, traffic spiked 5x. They had auto-scaled ECS tasks and EC2 instances to handle CPU, and the tasks themselves remained healthy (CPU \~70%, memory \~60%). However, customers experienced a high rate of payment failures and timeout errors during checkout.

**Investigation:** It was clear CPU wasn’t the issue. They looked at the NAT Gateway CloudWatch metrics and found ActiveConnectionCount near 55,000 (the soft limit per IP) and saw the metric `ConnectionAttemptCount` was much higher than `ConnectionEstablishedCount`, meaning not all connections succeeded. Essentially, the NAT gateway became a bottleneck for outbound calls. Because all tasks (about 50 tasks) were using one NAT gateway to reach the payment API, the concurrent connections during the spike saturated what one NAT gateway could comfortably handle in bursts. Some connection attempts were timing out or being dropped (PacketDropCount showed some drops).

**Solution:** As an immediate fix, they divided the ECS tasks across two private subnets each with its own NAT Gateway (each AZ had one). This effectively split the outbound load between two NAT gateways (since tasks in subnet A use NAT-A, subnet B use NAT-B). This increased the available connection pool. They also implemented HTTP connection reuse in their app – previously, for each payment request, the code opened a new TCP connection to the API. They changed it to use a keep-alive connection pool, which drastically reduced the churn of connections. With these changes, the next traffic spike was handled without issue (ActiveConnectionCount stayed well below limits, and no timeouts).

They later calculated that a single NAT can actually handle a lot of throughput, but the burst of new connections was the culprit – by reusing connections, they not only reduced latency but also pressure on NAT.

**Learnings:** Monitor and understand your network egress patterns. NAT Gateway is robust but not infinite. If you have a very network-heavy use case (lots of concurrent connections), plan to mitigate (multiple NATs or VPC endpoints if to AWS services, or use an ALB/NLB with internet-facing if possible). Also, efficient use of connections at the application layer can improve performance significantly.

### Case Study 3: Memory Leak Post-Deployment

**Background:** An ECS service (Node.js based) was updated to a new version. A week later, the team noticed the service’s tasks were restarting every few hours. This hadn’t happened before.

**Investigation:** They used CloudWatch Container Insights metrics and saw a clear trend: each task’s memory usage was climbing steadily about 50MB per hour until it hit the 512MB hard limit, then the container got OOM-killed (exit 137). The cycle would repeat. Comparing to before the deployment, memory usage used to plateau around 300MB. Therefore, the new release likely introduced a memory leak.

They pulled logs and found no errors. They used ECS Exec to trigger Node’s heap snapshot at different times and analyzed them (using Node’s built-in inspector). The heap snapshots revealed an accumulating array of objects that were never freed. They tracked this to a bug in the new code where responses were being cached in an in-memory array without eviction.

**Solution:** They issued a hotfix release that properly cleared the cache or limited its size. In the meantime, they increased the task’s memory limit to 700MB so it wouldn’t crash so frequently (knowing Node might still climb, but slower). After the fix, memory usage stabilized around 280MB consistently. No more OOM events.

**Learnings:** Even with good monitoring, memory leaks can slip in during deployments. They implemented a canary system – now they deploy the new version to one task while others run old version, and watch memory for a day. If it leaks, they catch it on the canary before rolling out to all. They also set up a CloudWatch Logs Insight query to look for “OOM” or “Killed” in ECS agent logs to quickly identify any future OOM kills.

These case studies emphasize the importance of comprehensive monitoring and a deep understanding of how ECS tasks utilize underlying resources.

## Conclusion

Troubleshooting performance issues in AWS ECS (EC2 launch type) involves a multi-layer approach: from inside the container (application code and runtime behavior) to the ECS abstractions (task definitions, scheduling) down to the EC2 infrastructure and VPC network. By carefully monitoring CPU, memory, and network metrics and analyzing logs, one can usually pinpoint the bottleneck – be it CPU starvation, memory exhaustion, network misconfiguration, or external dependency slowness.

In summary, ensure your ECS task definitions are well-tuned (neither under- nor over-allocating resources), leverage ECS service auto-scaling to match capacity with load, and maintain the EC2 instances with the right instance types and AMIs for optimal performance. At the VPC level, configure subnets, NAT gateways, and security groups correctly to provide reliable connectivity. Use CloudWatch and other tooling (Prometheus, Datadog, X-Ray) to gain visibility into the system’s behavior over time. With proactive alerts on key metrics, you can often address issues before they impact users – for example, catching a memory leak early or scaling out when CPU begins to spike.

AWS ECS, when properly configured and monitored, can run web applications at scale efficiently. Performance issues are manageable through the strategies discussed: identifying symptoms, correlating with possible causes (using data), and then iteratively improving the configuration or code. By learning from common pitfalls and past incidents, you can build a resilient ECS deployment that not only handles current traffic smoothly but also adapts to growth and spikes gracefully.
