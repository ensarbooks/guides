# Advanced Deployment Guide: React Frontend & Spring Boot Backend on On‑Premises Kubernetes

Deploying a modern web application on an on-premises Kubernetes cluster involves many steps and best practices. This comprehensive guide walks through the entire process of deploying a **React** frontend and **Spring Boot** backend on a bare-metal (on-premises) Kubernetes cluster. We cover everything from setting up the cluster, containerizing applications, writing Kubernetes manifests, integrating a database, to CI/CD pipelines, scaling, monitoring, and disaster recovery. Each section provides detailed explanations, step-by-step examples, and code snippets to help you successfully implement a production-grade deployment.

## 1. Setting Up the Kubernetes Cluster (On-Premises)

Setting up an on-premises Kubernetes cluster is the foundation for everything that follows. Unlike managed cloud services, on-premises deployments require you to install and configure the cluster components manually, handle networking, and plan for storage and security from the start. In this section, we will cover installing Kubernetes on bare-metal servers (or VMs), configuring networking via a Container Network Interface (CNI) plugin, setting up persistent storage solutions, and ensuring basic security configurations.

### 1.1 Cluster Installation and Initialization

**Kubernetes Components**: An on-prem cluster typically consists of one or more **master (control plane) nodes** and multiple **worker nodes**. The control plane runs components like the API server, scheduler, and etcd (the cluster database), while worker nodes run the container runtime and host your application Pods.

**Installation Tools**: A common approach to install Kubernetes on-prem is using **kubeadm**, which automates the setup of control plane and worker nodes. You will also need to install a container runtime (such as Docker or containerd) on each node, as well as Kubernetes utilities like `kubelet` (the node agent) and `kubectl` (the CLI tool). Below is a high-level step-by-step setup:

1. **Install Docker on All Nodes** – Kubernetes requires a container runtime. Install Docker (or another runtime) on the master and worker nodes. For example, on Ubuntu you can use the Docker installation script:

   ```bash
   sudo apt-get update
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   docker version
   ```

   Ensure that Docker is running on each node ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Docker%20installation%3A)) ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Now%2C%20check%20the%20status%20of,running%20on%20all%20the%20nodes)). After installation, consider configuring Docker’s cgroup driver to `systemd` (which aligns with kubelet’s default cgroup driver), as recommended by Kubernetes for stability ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Change%20the%20cgroupdriver%20to%20systemd,Kubernetes%20recommended%20cgroupdriver%20is%20system)) ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Look%20for%20the%20command%3A)).

2. **Disable Swap** – Kubernetes cannot run with swap enabled on the host, as it can lead to instability. Disable swap on all nodes:

   ```bash
   sudo swapoff -a
   ```

   Also remove or comment out any swap entry in `/etc/fstab` to prevent it from activating on reboot ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Follow%20the%20below%20commands%20step,in%20master%20nodes)).

3. **Install Kubernetes Binaries** – Install kubeadm, kubelet, and kubectl on all nodes. For example, on Ubuntu you might use apt or snap:

   ```bash
   sudo apt-get update && sudo apt-get install -y apt-transport-https curl
   curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
   sudo apt-get install -y kubelet kubeadm kubectl
   ```

   Ensure they are installed at matching versions. (The snippet above adds the official Kubernetes apt repository. Adjust for your OS as needed.) ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=apt,https))

4. **Initialize the Master Node** – On the designated control-plane machine, run kubeadm init. You should specify a **Pod network CIDR** (an IP range for Pods) if you plan to use certain network plugins. For example:

   ```bash
   sudo kubeadm init --pod-network-cidr=10.211.0.0/16
   ```

   This will initialize the Kubernetes control plane. It may take a few minutes. Once complete, kubeadm will output a success message and a **join token** command for worker nodes ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=%23%20kubeadm%20init%20%E2%80%93pod)). It will also prompt you to set up your local kubeconfig (to use `kubectl`):

   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```

   After this, `kubectl get nodes` should show the master node as Ready (once networking is configured).

5. **Join Worker Nodes** – On each worker node, execute the join command provided by `kubeadm init`. It will look similar to:

   ```bash
   sudo kubeadm join <MASTER_IP>:6443 --token <token> \
       --discovery-token-ca-cert-hash sha256:<hash>
   ```

   This command includes the master’s IP/hostname, a token, and a CA hash for secure discovery. Run this as root on each worker to connect it to the cluster ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=Then%20you%20can%20join%20any,each%20worker%20node%20as%20root)). After joining, you can check on the master:

   ```bash
   kubectl get nodes
   ```

   and you should see the workers in the Ready state (once networking is up).

6. **Deploy a Pod Network (CNI)** – By default, the cluster will not schedule Pods until a network plugin is installed (the master node will show status `NotReady` for workers due to no CNI). Choose a CNI plugin such as **Flannel** or **Calico** and apply its manifest. For example, to install Flannel:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
   ```
   This command (run on the master using `kubectl`) will set up Flannel for inter-pod networking ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=The%20cluster%20is%20ready,network%20connectivity%20to%20this%20cluster)). Flannel uses the CIDR you provided (10.211.0.0/16 in the example) for Pod IPs. If you prefer, you can use **Calico** instead, which offers network policy features and often better performance and reliability than Flannel ([Best of 2023: Setting up Kubernetes in an On-Premises Environment - Cloud Native Now](https://cloudnativenow.com/features/setting-up-kubernetes-in-an-on-premises-environment/#:~:text=flannel)). Calico can be installed by applying the Calico manifest (from docs.projectcalico).  
   After the network plugin is installed, the node statuses should turn **Ready** (you can verify with `kubectl get nodes`).

After completing these steps, you have a basic Kubernetes cluster up and running on-premises. You can verify the cluster health with: `kubectl cluster-info` and `kubectl get pods -A` (to see system pods running). The cluster is now ready to run your applications.

> **Note:** Ensure all nodes can resolve each other’s hostnames (e.g., via `/etc/hosts` or DNS) if you used hostnames in kubeadm. Also open necessary firewall ports between nodes (e.g., 6443 for API server, 10250 for kubelet, etc.). On on-prem hardware, you might need to set up IP routing or use flannel’s host-gw mode if nodes are on different subnets.

### 1.2 Networking Configuration for On-Premises

Networking in on-premises Kubernetes requires some planning since you don't have a cloud provider to automatically provide load balancers or address management. Here are key considerations:

- **Pod Network (CNI)**: As mentioned, you must deploy a CNI plugin. Flannel (simple overlay) or Calico (routing and network policy) are popular. Calico not only enables networking but also allows defining NetworkPolicies for security. Choose a CNI that fits your needs (for most basic setups, Flannel is easy; for more advanced policy control, Calico is recommended).

- **Service Networking**: Kubernetes assigns a virtual IP (ClusterIP) to each Service. This is handled by kube-proxy using IPTables or IPVS rules. Ensure the **service CIDR** (usually set by kubeadm or defaults) does not clash with your host network. The default service CIDR is often `10.96.0.0/12` (you can customize it via kubeadm config if needed).

- **Ingress and External Access**: On-premises clusters don’t have a built-in cloud load balancer for Services of type LoadBalancer. You have a few options to expose services externally:
  - Use **NodePort Services** and put an external load balancer (e.g., an HAProxy or F5 appliance) in front of the node IPs. For example, you can configure HAProxy to forward traffic to the NodePort of each node ([How to expose Ingress Controller service for on premise Kubernetes?](https://www.reddit.com/r/kubernetes/comments/p31ej3/how_to_expose_ingress_controller_service_for_on/#:~:text=Kubernetes%3F%20www,Use%20Metallb%2C)).
  - Deploy **MetalLB**, a bare-metal load-balancer implementation. MetalLB can allocate external IPs from a pool to Services of type LoadBalancer, effectively acting as a software load balancer within your cluster ([How to expose Ingress Controller service for on premise Kubernetes?](https://www.reddit.com/r/kubernetes/comments/p31ej3/how_to_expose_ingress_controller_service_for_on/#:~:text=Kubernetes%3F%20www,Use%20Metallb%2C)).
  - Use an **Ingress Controller** (more on this in section 5) combined with either NodePort or MetalLB. A common setup is to run **NGINX Ingress Controller** on the cluster, which listens on a NodePort or LoadBalancer IP and routes incoming HTTP/HTTPS traffic to your services. On-premises, you might expose the Ingress controller via MetalLB or a fixed node IP.

In summary, plan how external clients will reach your cluster’s services. In a production on-prem environment, a combination of MetalLB (for providing IPs) and an NGINX Ingress Controller (for HTTP routing) is a solid approach, as it provides both L4 and L7 load balancing.

### 1.3 Storage Solutions for Persistent Data

On-premises Kubernetes clusters need a strategy for **persistent storage** because you can’t rely on cloud-managed storage classes (like EBS, etc.). Kubernetes supports several approaches:

- **Networked Storage (NAS/SAN)**: If you have an existing NAS or SAN in your data center, you can create PersistentVolumes that use NFS mounts or iSCSI volumes. For example, you might set up an NFS server and then define a `StorageClass` and external provisioner for NFS.
- **Local Storage**: Use local disks on the nodes. This can be as simple as hostPath volumes (not recommended for production as they’re tied to a specific node) or using local persistent volumes with the Kubernetes local static provisioner. Local storage is fast but doesn’t natively handle redundancy.
- **Distributed Storage Solutions**: Deploy a distributed storage system in-cluster. Examples: **Ceph** (via Rook operator), **GlusterFS**, **OpenEBS**, or **Longhorn**. These run on your cluster and provide dynamic provisioning of volumes with replication. For instance, Rook/Ceph can manage block and file storage across nodes; Longhorn by Rancher is another CNCF project for block storage.
- **StatefulSets**: For stateful applications like databases, use StatefulSets which work with PersistentVolumeClaims to ensure each replica gets a unique volume. **StatefulSets ensure each pod has a stable identity and persistent storage**, which is crucial for databases ([Deploying PostgreSQL in a Kubernetes Cluster](https://alphabsolutions.com/blog/deploying-postgresql-in-a-kubernetes-cluster/#:~:text=Deploying%20PostgreSQL%20in%20a%20Kubernetes,maintaining%20data%20consistency%20and%20resilience)).

A simple starting point is to use NFS for shared storage (set up an NFS server, then create PersistentVolumes referencing it). For more advanced, consider Rook/Ceph which will give you a pool of storage across your nodes and allow dynamic volume claims.

Make sure to create appropriate **StorageClass** objects if you have dynamic provisioning enabled. For example, if using NFS with a provisioner, create a StorageClass named “nfs-client” and annotate the provisioner pod to handle PVCs. If using Rook, it will create a StorageClass for Ceph by default.

**Tip:** Even if your initial application (React + Spring Boot) is stateless, you will likely need storage for the database. Plan and test your storage setup before deploying the database to ensure data persistence and reliability.

### 1.4 Security Considerations in Cluster Setup

Before deploying any apps, secure the cluster itself:

- **RBAC**: Kubernetes **Role-Based Access Control** should be enabled (it is on by default in kubeadm for v1.8+). RBAC lets you control who can perform actions on which resources. You should create limited scope roles for components or admins as needed. For example, avoid using the `kube-admin` user for daily operations; instead create a user with limited permissions.
- **Network Segmentation**: Ensure etcd and the API server are not exposed on public networks. On-prem, keep the control plane nodes in a secure network segment. Use firewalls to restrict access to the Kubernetes API (port 6443) only to trusted networks or VPNs. Protect etcd (default port 2379) similarly – etcd contains all cluster state, including secrets, so access to etcd = access to everything ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=3,Firewall%20and%20Encryption)) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=Since%20etcd%20stores%20the%20state,use%20it%20to%20elevate%20privileges)).
- **Minimal Linux OS**: Use a minimal, hardened OS for your nodes (e.g., Ubuntu Server, CentOS, or Container-Optimized OS). Keep the OS updated with security patches. Disable unnecessary services on these nodes to reduce attack surface.
- **Rootless Containers**: Where possible, run application containers as non-root users. This can be enforced via Kubernetes SecurityContext (we will discuss in Section 5). Also consider enabling Pod Security Standards (baseline or restricted modes) which prevent privileged containers or dangerous host mounts.
- **Certificates**: Kubernetes components use TLS for communication (kubeadm does this automatically). Ensure those certificates are in place. For ingress (web traffic), plan for TLS certificates for your application domains (you might use Let’s Encrypt via cert-manager, or your own CA).
- **Audit Logging**: If this is a production cluster, enable Kubernetes audit logs to record API actions, which can be useful for security audits or troubleshooting.
- **Secrets Encryption**: By default, K8s Secrets are stored base64-encoded in etcd (not encrypted). For extra security, you can enable **encryption at rest** for Secrets so that etcd stores them encrypted ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=Turn%20on%20encryption%20at%20rest,for%20etcd%20secrets)) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=Kubernetes%20nodes%20must%20be%20on,to%20the%20general%20corporate%20network)). This requires configuring the API server with an encryption config.

Remember, on-prem Kubernetes means you are the admin at all levels. Following the **principle of least privilege** is key. Use RBAC to restrict what each component or user can do (e.g., your CI/CD service account only able to deploy to specific namespaces, etc.) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=RBAC%20can%20help%20you%20define,ABAC)). Also, regularly apply security updates to Kubernetes (plan how to upgrade your cluster periodically) and to the node OS.

With the cluster ready and secure, we can move on to packaging our applications into containers.

## 2. Building and Containerizing the Applications

In this section, we will containerize both the React frontend and the Spring Boot backend. Containerizing applications means packaging the application code and runtime environment into Docker images. We’ll discuss **Dockerfile best practices**, using **multi-stage builds** to optimize image size, and how to handle dependencies. The goal is to produce lean, secure, and efficient images for both the UI and API components.

### 2.1 Containerizing the React Frontend

A React application (built with tools like Create React App) is ultimately a static bundle of HTML, JS, and CSS that can be served by any web server. We will use Docker to create an image that builds the React app and then serves it via **NGINX**.

**Dockerfile for React (Multi-stage)**: We use a multi-stage Docker build to keep the final image small and secure. The first stage will use Node.js to compile the React app, and the second stage will use NGINX to serve the static files. For example:

```Dockerfile
# Stage 1: Build the React app
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

In this Dockerfile: the **build stage** installs dependencies and runs the `npm run build` script, producing a production-ready static bundle in the `build/` directory. The **production stage** starts from a lightweight NGINX image and simply copies the build artifacts into NGINX’s default `html` directory. We expose port 80 and run NGINX in the foreground.

This approach yields a very small final image containing only NGINX and the static files (no Node.js runtime or source code is included). It’s also more secure, as it excludes development dependencies and the Node runtime from the running container ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Nginx%20efficiently%20serves%20static%20files)). According to Docker’s official guide, this multi-stage method results in **smaller image size** and **enhanced security**, and NGINX provides efficient static file serving ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Runs%20Nginx%20in%20the%20foreground)) ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)).

**Best Practices for React Dockerfile**:

- Use an official Node image (like `node:18-alpine`) for the build stage to keep it lightweight.
- Use an official NGINX (alpine) image for serving. Alpine-based images are smaller (but be mindful of any Alpine-specific issues with glibc if you had native dependencies).
- Include a **.dockerignore** file to avoid copying unnecessary files (e.g., node_modules if you install inside Docker, or local environment files) to the image build context.
- Do not run the development server (`npm start`) in production containers – always build the optimized static files for production (`npm run build`), which does minification and other optimizations.
- If needed, you can configure NGINX by dropping in a custom nginx.conf, for example to handle routing (for a React single-page app, you often set `try_files /index.html` for unknown routes). You could copy a custom config in the Dockerfile if the default is not sufficient.

After building the Docker image (e.g., run `docker build -t my-react-app:latest .` in the React project directory), test it locally: run a container and ensure you can access the React app on port 80. This image will be deployed to K8s.

### 2.2 Containerizing the Spring Boot Backend

The Spring Boot backend will be packaged as a self-contained JAR (Java archive). We can containerize it by copying the JAR into a Java runtime image. However, building the JAR itself can be heavy (involving Maven/Gradle and downloading dependencies), so we’ll use a multi-stage Docker build for efficiency.

**Build Process**: You likely have a `pom.xml` (for Maven) or `build.gradle` (for Gradle). We’ll assume a Maven build in this example.

**Dockerfile for Spring Boot** (multi-stage):

```Dockerfile
# Stage 1: Build the Spring Boot jar
FROM maven:3.8.7-openjdk-17 AS builder
WORKDIR /app
COPY pom.xml ./
RUN mvn dependency:go-offline  # caches dependencies
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Run the Spring Boot application
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
# Optionally, add a non-root user:
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

In this Dockerfile:

- The **builder stage** uses a Maven image with JDK 17 to compile the application. We first copy the `pom.xml` and fetch dependencies (this helps leverage caching), then copy the source and run `mvn package`. After this stage, we have the fat JAR (let’s say `myapp-1.0.jar`) in the `target` directory.
- The **runtime stage** uses a slim JRE image (here Eclipse Temurin JRE 17 Alpine). We copy the JAR from the builder. We create a user `appuser` to avoid running as root. We set the entrypoint to run the jar. Only port 8080 is exposed.

This yields a production image containing just the JRE and the application jar. It’s much smaller than using a full JDK or Maven environment in production. For example, using a multi-stage Docker build can **reduce a Spring Boot image size significantly**, since the final image has no build tools and only the JRE needed to run ([Multi-stage Docker build for React and Spring - The official voice of the Obeo experts](https://blog.obeosoft.com/multi-stage-docker-build-for-react-and-spring#:~:text=consider%20a%20Spring,That%20would%20be%20an%20issue)) (which aligns with removing “useless code at runtime” as noted in the Obeo blog ([Multi-stage Docker build for React and Spring - The official voice of the Obeo experts](https://blog.obeosoft.com/multi-stage-docker-build-for-react-and-spring#:~:text=The%20Docker%20container%20used%20to,That%20would%20be%20an%20issue)) ([Multi-stage Docker build for React and Spring - The official voice of the Obeo experts](https://blog.obeosoft.com/multi-stage-docker-build-for-react-and-spring#:~:text=consider%20a%20Spring,That%20would%20be%20an%20issue))).

**Best Practices for Spring Boot Dockerfile**:

- Use a specific base image tag (e.g., a specific version of the JRE) to ensure consistency.
- Avoid running as root in the container. We added a user in the Dockerfile for better security.
- Externalize configuration (don’t bake passwords or environment-specific configs into the image – we will use ConfigMaps/Secrets in K8s).
- If the JAR has a fixed name, you can use that instead of `*.jar` copy. Here we assumed only one jar in target.
- Consider the JVM memory settings: in K8s, if you set resource limits, the JVM might need `-XX:+UseContainerSupport` (which is default in newer Java versions) or other flags to respect container limits. You can also pass JAVA_OPTS via environment variables in the Deployment manifest to tune heap size (e.g., `-Xmx`). This ensures the Java app plays nicely with Kubernetes resource management.

After building the image (e.g., `docker build -t my-springboot-app:latest .`), test it by running the container and hitting the exposed API (it should run on port 8080).

### 2.3 Docker Build and Image Optimization Tips

Regardless of tech stack, some general containerization best practices apply:

- **Small Base Images**: Use Alpine or slim variants when possible. But be cautious: some libraries may expect glibc (which Alpine replaces with musl). For Java, Alpine JRE is fine; for Node, Alpine is common and works for most cases.
- **Multi-stage Builds**: We demonstrated multi-stage builds for both apps. This is a key best practice to reduce image size and attack surface ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=)). Only include what’s necessary to run the app in the final stage ([How to Dockerize a React App: A Step-by-Step Guide for Developers | Docker](https://www.docker.com/blog/how-to-dockerize-react-app/#:~:text=,Nginx%20efficiently%20serves%20static%20files)).
- **Layer Caching**: Order your Dockerfile commands to maximize use of layer cache. For example, copy only pom.xml and run `mvn dependency:go-offline` before copying the rest of the code – this way, if only your source code changes but not dependencies, the dependency layer is cached. Similarly for Node: copy package.json and do `npm install` first, then copy app code.
- **.dockerignore**: Use it to ignore files not needed in the image (e.g., `.git`, local `.env` files, build caches). This reduces build context size and improves build speed.
- **Security**: Do not include secrets in the image. Also, update base images regularly for security patches (or use Dependabot/renovate to alert for base image updates). You can also use tools like Docker Bench or Trivy to scan images for vulnerabilities.
- **Entrypoint vs CMD**: For Spring Boot, we used ENTRYPOINT so that the container will always run the jar. Ensure your container runs in foreground (don’t use `systemd` or such inside container). Both our examples run as foreground processes (Nginx in “daemon off” mode, Java as main process), which is correct for Docker/K8s.
- **Testing**: Test the containers locally or in a test cluster. For the React app, ensure static files served correctly (maybe test a refresh of a deep link to ensure proper routing). For Spring Boot, ensure it can connect to a database (we will configure that via environment variables in Kubernetes).

By following these practices, you will have two Docker images: e.g., `myregistry/react-frontend:1.0` and `myregistry/spring-backend:1.0`. Next, we will deploy these to Kubernetes with appropriate configuration.

## 3. Kubernetes Deployment Configuration (YAML Manifests)

With container images ready, the next step is to write Kubernetes manifest files (YAML) to deploy them. We will create **Deployment** objects to manage our pods, **Service** objects to expose them internally (and via Ingress externally), and use **ConfigMaps/Secrets** for configuration. This section provides examples of these YAML files and explains how to configure them for our React and Spring Boot apps.

### 3.1 Deployments and Services

**Deployments** ensure that a specified number of pod replicas are running at all times and allow rolling updates to new versions ([Kubernetes Deployment: Strategies, Explanation, and Examples](https://kodekloud.com/blog/kubernetes-deployments/#:~:text=According%20to%20the%20Kubernetes%20documentation%3A)). We will create one Deployment for the React frontend and one for the Spring Boot backend. Each Deployment will manage pods running the respective Docker image.

**Services** provide stable networking for pods. A Service will group the pods by a selector (e.g., all pods with `app: springboot-backend`) and give them a stable IP and DNS name. We will likely use a **ClusterIP** Service for the backend (for internal communication) and another for the frontend if needed (though the frontend might be mainly accessed via Ingress). In an on-prem cluster, we’ll use an Ingress to route external HTTP traffic to the frontend and backend, instead of exposing the Service directly via NodePort.

Let’s write example manifests:

**Spring Boot Backend Deployment (`backend-deployment.yaml`):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: springboot-backend
  labels:
    app: springboot-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: springboot-backend
  template:
    metadata:
      labels:
        app: springboot-backend
    spec:
      containers:
        - name: backend
          image: myregistry/springboot-backend:1.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              valueFrom:
                configMapKeyRef:
                  name: backend-config # assume we define in a ConfigMap
                  key: spring.datasource.url
            - name: SPRING_DATASOURCE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: db-credentials # pulling sensitive data from a Secret
                  key: db_user
            - name: SPRING_DATASOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: db_password
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1024Mi"
              cpu: "1"
```

A few things to note in this backend Deployment:

- We set `replicas: 3` to have 3 instances of the backend for high availability.
- The `selector` and template `labels` ensure the Deployment knows which pods it manages (they must match).
- The container image is our Spring Boot image. It opens port 8080.
- **Environment Variables**: We define `SPRING_DATASOURCE_URL`, `USERNAME`, and `PASSWORD` from a ConfigMap and Secret. This is how we feed configuration (like database connection info) into the app without baking it into the image. The Spring Boot app would be coded to read these from environment or have them mapped to Spring’s config. (We’ll define the ConfigMap/Secret later in this section.)
- **Probes**: We added liveness and readiness probes. These are best practices:
  - The liveness probe hits `/actuator/health` (assuming Spring Boot Actuator is on). If the app gets stuck, Kubernetes will restart the container.
  - The readiness probe also hits health. Only when this passes will the Service send traffic to the pod. This prevents sending traffic to an unready instance (for example, during startup or if it’s overloaded).
- **Resources**: We set resource requests and limits. This ensures Kubernetes knows that each pod needs, e.g., 0.5 CPU and 512Mi memory (and can use up to 1 CPU/1Gi). This is critical for the scheduler to place pods and for stable performance. We will refine scaling in Section 7, but it’s good to set these now.

**Spring Boot Service (`backend-service.yaml`):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: springboot-backend
spec:
  selector:
    app: springboot-backend
  ports:
    - port: 8080 # Service port
      targetPort: 8080 # container port
      protocol: TCP
  clusterIP: None # optional: by setting ClusterIP None, we make it Headless (useful for direct DNS, or if using statefulset). For typical deployment, remove this line.
```

This Service selects the backend pods and exposes port 8080 internally. Without a `type`, it defaults to ClusterIP (internal only). We could make it `NodePort` if we wanted direct access, but instead we will use an Ingress for external access. The clusterIP: None is shown as an option if you needed a headless service (for discovery), but for a stateless backend behind an ingress, a normal ClusterIP is fine (just omit clusterIP field entirely to get an auto ClusterIP).

We will later configure an Ingress so that external clients can reach this service (e.g., by hitting `https://<domain>/api/` and routing to this service).

**React Frontend Deployment (`frontend-deployment.yaml`):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: react-frontend
  labels:
    app: react-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: react-frontend
  template:
    metadata:
      labels:
        app: react-frontend
    spec:
      containers:
        - name: frontend
          image: myregistry/react-frontend:1.0
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

This is simpler. We run 2 replicas of NGINX serving the React app. It listens on port 80. We allocate some minimal resources for it (frontends often need less). We might not need special config or env vars for the React app container, since it’s just static files. (If the React app needs to know the API URL, you might have built that into the bundle or could supply it via a ConfigMap-mounted config file or environment. But typically for a static SPA, you can use relative URLs or an environment substitution at build time.)

**React Service (`frontend-service.yaml`):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: react-frontend
spec:
  selector:
    app: react-frontend
  ports:
    - port: 80 # cluster IP port
      targetPort: 80 # container port
  type: ClusterIP
```

This service exposes the frontend pods internally on port 80. We will definitely expose the frontend via Ingress for external users. Alternatively, one could use a LoadBalancer service (if MetalLB is installed) to directly get an IP for the UI, but using an Ingress is more common for web apps as it allows host-based or path-based routing and TLS termination in one place.

At this point, if you apply these deployments and services (`kubectl apply -f backend-deployment.yaml,backend-service.yaml,frontend-deployment.yaml,frontend-service.yaml`), you would have pods running your app. But they may not fully function yet because:

- The backend likely needs a database connection (we provided env vars for it).
- The Ingress (external routing) is not set up yet.
- The ConfigMap/Secret for configuration are not created yet.

So next, we handle configuration (ConfigMap, Secret) and then ingress/networking.

### 3.2 ConfigMaps for Application Configuration

A **ConfigMap** is a Kubernetes object to store non-confidential configuration in key-value form. It allows you to decouple config from the container image, so you can modify config without rebuilding images ([ConfigMaps | Kubernetes](https://kubernetes.io/docs/concepts/configuration/configmap/#:~:text=A%20ConfigMap%20is%20an%20API,files%20in%20a%20%20108)) ([ConfigMaps | Kubernetes](https://kubernetes.io/docs/concepts/configuration/configmap/#:~:text=A%20ConfigMap%20allows%20you%20to,your%20applications%20are%20easily%20portable)). In our case, we might use a ConfigMap to store Spring Boot application properties that we want to override, or any other config (for example, the JDBC URL, or feature flags).

In the Deployment, we referenced a ConfigMap named `backend-config` for the key `spring.datasource.url`. Let’s define that:

**Backend ConfigMap (`backend-config.yaml`):**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
data:
  spring.datasource.url: "jdbc:postgresql://postgres-service:5432/mydatabase"
  spring.jpa.show-sql: "false"
  # ... any other Spring Boot overrides
```

This ConfigMap has a key for the JDBC URL. We point it to a host `postgres-service:5432/mydatabase` (assuming we will have a Service for the DB). We could also put things like `spring.redis.host`, etc., if needed, or any config the app reads from environment or `application.properties`. In Spring Boot, by default environment variables of the form `SPRING_DATASOURCE_URL` map to `spring.datasource.url` property. We chose to load it via env var in the Deployment. Alternatively, we could mount this ConfigMap as a properties file. For simplicity, environment variables are fine.

Kubernetes ConfigMaps are not encrypted (and not meant for secrets). They are great for env vars, config files, etc. Using a ConfigMap avoids baking these values in Docker image or hard-coding in manifests, making it easy to change per environment (dev/staging/prod) ([ConfigMaps - Kubernetes](https://kubernetes.io/docs/concepts/configuration/configmap/#:~:text=A%20ConfigMap%20allows%20you%20to,your%20applications%20are%20easily%20portable)) ([Streamlining Kubernetes with ConfigMap and Secrets - Devtron](https://devtron.ai/blog/kubernetes-configmaps-secrets/#:~:text=A%20ConfigMap%20allows%20you%20to,your%20applications%20are%20easily%20portable)).

After creating the ConfigMap, the backend pods will be able to pull in that config on next deploy. (If a ConfigMap is updated, pods won’t automatically get the new data unless restarted or if mounted as volume with special settings. A common approach is to roll the Deployment when config changes, e.g., by changing an annotation on the Deployment to trigger new pods.)

The React frontend may also use a ConfigMap if it needed any runtime configuration. However, since React is built into static files, typically you don’t have dynamic config (unless you serve a special config JSON or use environment substitution at container startup – beyond our scope here). So we might not need a ConfigMap for the React app.

### 3.3 Secrets for Sensitive Data

Kubernetes **Secrets** are like ConfigMaps but intended for sensitive data (passwords, API keys, etc.). They are base64-encoded in etcd (not truly encrypted by default, but better than plaintext in manifest) ([Secrets | Kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/#:~:text=A%20Secret%20is%20an%20object,data%20in%20your%20application%20code)) ([Secrets | Kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/#:~:text=Secrets%20are%20similar%20to%20ConfigMaps,intended%20to%20hold%20confidential%20data)). Use Secrets for things like database passwords, certificates, etc.

In our Deployment, we referenced a Secret `db-credentials` for `db_user` and `db_password`. Let’s create that:

**Database Credentials Secret (`db-credentials.yaml`):**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  db_user: dXNlcm5hbWU= # base64 encoded value of "username"
  db_password: cGFzc3dvcmQ= # base64 encoded value of "password"
```

Here, you must base64-encode the values. (For example, `echo -n 'username' | base64` -> `dXNlcm5hbWU=`). We put the encoded strings in the YAML. When applied, this secret holds the credentials. In our Deployment env, we set the env var to pull from `secretKeyRef` of this secret.

**Important**: Don’t commit actual secrets to version control. Typically, you might apply secrets via a separate mechanism or use tooling to manage them. But for completeness, we show it in YAML here. Also, consider enabling encryption at rest for secrets as mentioned, so that even in etcd they aren’t just base64 (which is trivially decodable) ([Kubernetes: Secrets - Claire Lee](https://yuminlee2.medium.com/kubernetes-secrets-4287b5a83606#:~:text=Secret%20data%20in%20Kubernetes%20is,value%20pairs%20in%20a%20Secret)).

Now the Spring Boot app on startup will get these env vars (`SPRING_DATASOURCE_USERNAME`, etc.) and should connect to the DB. We will set up the DB in the next section.

The React app likely doesn’t require a Secret. If it needed something like an API key for a third-party service, you could also provide it via a Secret and maybe have the React app read it (but since React is static, usually such keys are public or embedded at build time, or you use your backend as a proxy).

### 3.4 Ingress Configuration

While not explicitly listed in this section’s title, deploying on Kubernetes often involves using an **Ingress** resource to route external traffic. We will cover Ingress in detail in Section 5 (Networking & Security), but to complete the picture: you would define an Ingress that routes requests to the React frontend service and (perhaps) some paths to the backend service.

For example, if you have a domain `myapp.example.com`, you might have:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  rules:
    - host: "myapp.example.com"
      http:
        paths:
          - path: "/"
            pathType: Prefix
            backend:
              service:
                name: react-frontend
                port:
                  number: 80
          - path: "/api/"
            pathType: Prefix
            backend:
              service:
                name: springboot-backend
                port:
                  number: 8080
```

This would send all requests to `/api/...` to the Spring Boot service (assuming your Spring Boot app serves API at `/api`), and everything else to the React service. The React app will handle client-side routing for its subpaths. We would also attach a TLS certificate to this Ingress for HTTPS (via a secret).

We’ll revisit Ingress in the networking section, but keep in mind to create it when deploying.

**Summary**: We have now prepared the core manifests:

- Deployment and Service for frontend and backend.
- ConfigMap for backend configuration.
- Secret for DB credentials.
- (Ingress for routing, to be applied once ingress controller is up.)

Apply all these manifests with `kubectl apply -f`. After that, the Pods should come up. You can run `kubectl get pods` to see statuses. Ideally they go to Running state and pass readiness probes. If a pod is CrashLooping or not ready, you’d need to troubleshoot (see section 10 for common issues).

In the next section, we’ll address the database setup, which is crucial for the Spring Boot backend to actually function.

## 4. Database Integration (PostgreSQL/MySQL Setup)

Most real-world applications need a database. In our scenario, assume Spring Boot connects to a relational database (like PostgreSQL or MySQL). We have two choices for the database in an on-prem Kubernetes deployment:

- **Run the database inside the Kubernetes cluster** (as a StatefulSet or Deployment with PersistentVolume).
- **Use an external database service** (outside the cluster, e.g., a dedicated DB server or an RDS-like service if available on-prem).

We will discuss how to set up a database in-cluster using Kubernetes constructs, and also what to consider if using an external DB.

### 4.1 Deploying a Database in the Cluster

Running a database on Kubernetes is feasible and common on-prem, especially if you don’t have a managed DB service. Kubernetes’ **StatefulSet** is the recommended controller for database workloads because it provides stable pod identities and persistent storage for each replica ([Deploying PostgreSQL in a Kubernetes Cluster](https://alphabsolutions.com/blog/deploying-postgresql-in-a-kubernetes-cluster/#:~:text=Deploying%20PostgreSQL%20in%20a%20Kubernetes,maintaining%20data%20consistency%20and%20resilience)).

Let’s say we choose PostgreSQL for our app. We can deploy Postgres with a PersistentVolumeClaim for data storage. For demonstration:

**PostgreSQL StatefulSet (`postgres-statefulset.yaml`):**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres" # headless service for stable DNS
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:14-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: mydatabase
            - name: POSTGRES_USER
              value: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: db_password # reusing the secret for password
          volumeMounts:
            - name: db-data
              mountPath: /var/lib/postgresql/data
              subPath: postgres-data
  volumeClaimTemplates:
    - metadata:
        name: db-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 5Gi
```

Explanation:

- We use a StatefulSet with replica 1 (a single Postgres instance). If we needed HA, we might deploy 1 primary and maybe set up a replication, but that’s complex. Many production deployments use a single primary and rely on backup/restore for DR, or use a more advanced operator like CrunchyData or Zalando Postgres Operator for HA. We’ll keep it one pod for simplicity.
- `serviceName: "postgres"` and a headless service (we’d also create a Service with clusterIP None named "postgres") provides a stable DNS `postgres-0.postgres` for the pod. However, since we have 1 replica, a normal Service with selector is fine too. But StatefulSet demands a serviceName for governing service.
- Env vars configure the database name, user, and password. We use the same Secret we created to supply the password to the DB.
- The **volumeClaimTemplates** will create a PersistentVolumeClaim for each replica (here just one) named `db-data`. We request 5Gi storage. This assumes you have a default StorageClass that can provision volumes (on-prem, you must ensure this - e.g., via NFS or Ceph as discussed). If not, you’d create a PV manually and match it by claim.
- The volume is mounted at Postgres’s data directory.

Apply the above YAML to create the DB. It will spin up a Postgres pod. The first run will initialize the database with the given user/password and database.

Also create a Service for Postgres (if not using headless or even with headless for simplicity):

**Postgres Service (`postgres-service.yaml`):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  clusterIP: None # headless, or omit for ClusterIP
```

Here we make it headless (ClusterIP None) meaning DNS queries for `postgres-service` will return the pod’s IP directly (no load balancing, since only one). This could also be normal ClusterIP since single pod. In our ConfigMap for Spring Boot we used `postgres-service:5432/mydatabase` as JDBC URL, which aligns with this service name and DB name.

**Considerations**:

- **Persistence**: The PVC ensures data persists if the pod restarts or moves nodes. Make sure your storage is reliable (on-prem, perhaps an NFS share or a RAIDed disk on the node). If the node running Postgres dies, with RWX (ReadWriteOnce) volume, Kubernetes can’t just start it on another node unless using something like rook/ceph which replicates data. So, plan for that: either use a distributed storage or be prepared to restore from backup if a node is lost. This is a single-point-of-failure unless you have replication.
- **Backup**: We will cover backup later, but for DB specifically, consider scheduled backups (e.g., `pg_dump` to an external location or volume snapshots).
- **Resource Requirements**: Databases might need more memory or CPU. Allocate appropriately in the StatefulSet spec with `resources:` for the container to avoid issues under load.
- **Security**: The example above is simplistic (user and password in env). Consider using stronger auth and restricting network access. By default, this service is only accessible within the cluster. If needed, you could enable TLS for Postgres or other hardening.

Using an **Operator**: There are Kubernetes Operators for databases (like the Zalando Postgres Operator, or MySQL Operator) that automate many tasks (like backups, failover). Those are advanced but worthwhile if running DB in production on K8s long-term.

### 4.2 Connecting the Application to the Database

Now that the DB is running in the cluster, our Spring Boot backend should be able to connect. We set environment variables for Spring DataSource URL, user, pass. Ensure that:

- The `SPRING_DATASOURCE_URL` uses the service name `postgres-service` which should resolve to the Postgres Pod’s IP.
- The service and backend are in the same Kubernetes namespace (if not, you’d need to include the namespace in the DNS, e.g., `postgres-service.<namespace>.svc.cluster.local`).
- The Postgres container started successfully with that user/pass. (By default, the official image will create the user and database on first launch using those env vars.)

When the Spring Boot pods start, they will attempt to connect to the DB. If the DB isn’t ready yet, Spring Boot might fail on startup. To handle that, you could:

- Increase the retry logic or initialization tolerance in the app.
- Ensure ordering: Since K8s doesn’t guarantee startup order, you might deploy the DB first and verify it's running, then deploy the backend. Or use an initContainer in the backend to wait for DB availability (some use simple scripts to poll the DB port).
- Alternatively, use Kubernetes readiness probes: the backend pod won’t receive traffic until ready, but that doesn’t stop it from trying to connect to DB on startup.

For initial deployments, deploying DB first is a practical approach. In a CI/CD or Helm chart, you might include hooks or just document that dependency.

### 4.3 Using an External Database Service

If you have an existing database server (outside Kubernetes), you may choose not to run the DB in the cluster. In that case:

- **Connectivity**: Ensure the Kubernetes pods can reach the external DB host (routing, firewall, etc.). On-prem, that might mean the cluster nodes have network access to the DB VLAN or the DB is in the same network.
- **Service Representation**: You can still create a Kubernetes Service of type **ExternalName** to represent the external DB by DNS name. For example:
  ```yaml
  kind: Service
  metadata:
    name: postgres-service
  spec:
    type: ExternalName
    externalName: actual.db.host.example.com
    ports:
      - port: 5432
  ```
  This way, the apps can still use `postgres-service` as hostname (it will resolve to the externalName). Alternatively, just put the external host in the ConfigMap directly.
- **Secrets**: Provide credentials as Secrets similarly.
- **Security**: Use TLS if connecting to DB over network, and restrict access (maybe the cluster nodes’ IPs are allowed on the DB’s firewall).

External DB means Kubernetes won’t manage it. You have to handle backup/DR at the DB level. But it might be a good approach if the DB is a critical component managed by a separate team or if you have a highly available database setup externally.

### 4.4 Database Best Practices in Kubernetes

Regardless of internal/external:

- **Initialization**: If the app requires certain tables or seed data, ensure the database is initialized. For example, you could use Kubernetes Jobs or init-containers to run migrations (Flyway, Liquibase, etc.) before the app starts.
- **Environment Config**: The JDBC URL in config might differ between environments (dev/staging/prod). Use ConfigMaps/Secrets per environment or Helm chart values to inject the correct values.
- **Scaling DB**: If more capacity is needed, you scale the DB (vertical scaling or adding replicas if using a cluster). Apps might not change, but monitor DB performance as you scale the application pods.
- **Monitoring**: Include the database in monitoring. If inside K8s, you can use exporters (e.g., PostgreSQL exporter for Prometheus) to track DB metrics.

At this point, we have a fully deployed stack in Kubernetes: React frontend, Spring Boot backend, and a PostgreSQL database, all configured and running. Next, we will discuss networking and security in more depth, including ingress setup, service mesh, and RBAC.

## 5. Networking & Security

This section covers how to expose the application to users (Ingress setup), how to secure traffic within the cluster (network policies, service mesh), and Kubernetes security best practices like RBAC and pod security. Networking and security are grouped because many network features have security implications (e.g., restricting access).

### 5.1 Ingress Controllers and External Access

**Ingress Controller**: In Kubernetes, an Ingress is an API object that defines rules for routing external HTTP/HTTPS traffic to Services. However, it’s just a definition – you need an Ingress Controller (like a running pod) that watches these objects and programs a load balancer (like NGINX or Traefik) accordingly. On cloud, a cloud LB might back it, but on-prem, the common solution is to deploy the **Ingress-NGINX controller** as a Deployment/DaemonSet in the cluster.

To set up NGINX Ingress on-prem:

- Deploy the ingress-nginx controller (you can use the official Helm chart or manifest). This typically creates a Service of type NodePort or LoadBalancer for the ingress controller.
- If using MetalLB, you can make the ingress controller Service of type LoadBalancer, and MetalLB will allocate an IP for it (maybe an IP on your LAN). Otherwise, NodePort could be used and then you configure an external L4 load balancer or DNS round-robin to the node IPs.

For example, to install via manifest:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v<version>/deploy/static/provider/baremetal/deploy.yaml
```

(This deploys ingress-nginx suitable for baremetal. The exact URL might change with versions; consult ingress-nginx docs.)

Once the controller is running, you create **Ingress** objects like the one we described in section 3.4. The controller will configure its internal Nginx to route accordingly.

**TLS/Certificates**: It’s highly recommended to serve your app over HTTPS. Obtain a TLS certificate for your domain:

- Use **Let’s Encrypt** with the **cert-manager** in Kubernetes. Cert-manager will create certificate objects and a controller will get LE to sign them, storing the certs in Secrets. In your Ingress, you then reference the TLS secret and enable TLS.
- Or, manually provide a Secret with your TLS cert and key.

For example, if using cert-manager, an Issuer and Certificate resource can automate getting `myapp.example.com` cert, and then your Ingress spec includes:

```yaml
tls:
  - hosts:
      - myapp.example.com
    secretName: myapp-tls
```

The ingress controller will use that secret’s cert.

**DNS**: Point your domain (or a subdomain) to the IP address of the ingress controller (or to your external LB that forwards to it). On-prem, you might configure DNS A record for `myapp.example.com` to the MetalLB provided IP or a VIP.

Now, with ingress in place, users can hit `http(s)://myapp.example.com/` and reach the React frontend, and `.../api/...` will proxy to the Spring Boot service as defined. The ingress controller handles URL path routing and can also do other things like TLS termination and even basic auth or IP whitelist (via annotations), if configured.

### 5.2 Service Mesh (Advanced Networking)

For advanced traffic management and security, some deployments use a **Service Mesh** such as **Istio** or **Linkerd**. A service mesh is a dedicated infrastructure layer that controls service-to-service communication in the cluster. It typically involves sidecar proxies (like Envoy) injected into pods.

**Capabilities of Service Mesh**:

- **Traffic routing**: Fine-grained control like canary releases, traffic splitting (e.g., send 10% traffic to a new version), fault injection for testing, retries, and timeouts, all configured outside of application code.
- **Observability**: Detailed metrics and traces for service communications (e.g., request success rates, latencies).
- **Security**: Automatic **mTLS** (mutual TLS) for all communication between services, providing encryption in transit and authentication of services ([Service Mesh Security with Istio | overcast blog](https://overcast.blog/service-mesh-security-with-istio-d08198a9520e#:~:text=Istio%20is%20an%20open,for%20protecting%20communication%20between%20services)) ([Service Mesh Security with Istio | overcast blog](https://overcast.blog/service-mesh-security-with-istio-d08198a9520e#:~:text=Istio%20provides%20out,the%20communicating%20services%20are%20verified)). Istio, for example, can encrypt all pod-to-pod traffic so that even within the cluster, if someone intercepts, they see only encrypted data. It also offers policy layers (who can talk to whom) and fine-grained RBAC at the service level.

In our context, a service mesh isn’t strictly required, but if we had many microservices, it could be beneficial. Istio’s security features (mTLS, authZ) are particularly valuable for zero-trust networks ([Service Mesh Security with Istio | overcast blog](https://overcast.blog/service-mesh-security-with-istio-d08198a9520e#:~:text=Istio%20is%20an%20open,for%20protecting%20communication%20between%20services)) ([Service Mesh Security with Istio | overcast blog](https://overcast.blog/service-mesh-security-with-istio-d08198a9520e#:~:text=Istio%20provides%20out,the%20communicating%20services%20are%20verified)). It ensures every service communication is encrypted and verified, which can prevent certain attacks and eavesdropping. Service mesh also eases some networking issues by standardizing how to do timeouts or circuit breakers without modifying app code.

To use Istio on-prem, you’d install Istio (either via Helm or Istio’s operator). It will create an ingressgateway (which can replace or complement NGINX ingress) and inject sidecars. For a small deployment, this might be overkill, but it is an advanced option.

If not using a full mesh, you can still implement some security:

- Enable network policies using something like Calico (if installed). **NetworkPolicies** let you restrict what traffic a pod can receive or send based on labels and namespaces. For instance, you can say “only allow pods with label app=react-frontend to talk to pods with app=springboot-backend on port 8080, and deny other access”. By default, all pods in a cluster can talk to each other (if not isolated by policies). Locking that down is good practice for defense in depth ([Kubernetes Security Best Practices in 2025](https://www.practical-devsecops.com/kubernetes-security-best-practices/#:~:text=Kubernetes%20Security%20Best%20Practices%20in,Update%20Kubernetes%20Regularly%20%C2%B7%206)).
- Even without a service mesh, you can do mTLS at the application level or use a sidecar like Linkerd which focuses mainly on transparent mTLS and metrics without as much complexity as Istio.

In summary, service mesh is optional but provides powerful features for large-scale or security-sensitive deployments. Istio in particular offers a comprehensive set of tools for traffic management and secure communication (authentication, authorization, audit) ([How Istio's mTLS Traffic Encryption Works as Part of a Zero Trust ...](https://tetrate.io/blog/how-istios-mtls-traffic-encryption-works-as-part-of-a-zero-trust-security-posture/#:~:text=How%20Istio%27s%20mTLS%20Traffic%20Encryption,mTLS)) ([Service Mesh Security with Istio | overcast blog](https://overcast.blog/service-mesh-security-with-istio-d08198a9520e#:~:text=Istio%20is%20an%20open,for%20protecting%20communication%20between%20services)). If you foresee needing such capabilities (or you require end-to-end encryption within your cluster for compliance), consider evaluating a mesh.

### 5.3 Role-Based Access Control (RBAC)

Kubernetes RBAC is a key security feature that controls _who_ can do _what_ in the cluster. It operates by defining **Roles** (a set of permissions on resources) and **RoleBindings** (or ClusterRoleBindings) that attach those roles to users or service accounts.

**Default RBAC**: When you set up the cluster, a default ClusterRole called `cluster-admin` is usually given to the initial user (for example, kubeadm sets up a user in `~/.kube/config` with admin). You should be careful with this powerful access.

**Principle of Least Privilege**: Create specific service accounts for components like your CI/CD pipeline or any in-cluster app that needs to call the Kubernetes API, and give them only the permissions necessary. For instance, if using Argo CD (discussed later), it will need read/write on certain resources, but you wouldn’t give it full cluster-admin if not needed.

For our deployment:

- The React and Spring Boot applications themselves likely do not call the Kubernetes API, so they can run under the default service account in their namespace with no special permissions (default service account has no rights if RBAC is on).
- If you deploy something like a metrics server or ingress controller, they often come with recommended RBAC roles in their manifests (e.g., ingress controller might need to watch Ingress resources, etc.).
- You as a developer or admin should create separate Kubernetes credentials for yourself vs the CI system. For example, a Jenkins service account that can only do `kubectl deploy` in a specific namespace.

**RBAC Example**: Suppose we want to allow a CI/CD pipeline to deploy to the namespace "production". You could create:

```yaml
kind: Role
metadata:
  name: deployer
  namespace: production
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: [""]
    resources: ["services", "configmaps", "secrets"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

(This Role allows full management of deployments, services, configmaps, secrets in prod namespace.)

Then bind it:

```yaml
kind: RoleBinding
metadata:
  name: jenkins-deployer-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: jenkins-sa
    namespace: cicd
roleRef:
  kind: Role
  name: deployer
  apiGroup: rbac.authorization.k8s.io
```

This binds the Role to a service account `jenkins-sa` (perhaps defined in a cicd namespace). That service account token would be used by Jenkins to perform deployments. By limiting to specific resources and namespace, you ensure Jenkins can’t, say, read all secrets cluster-wide or modify things in kube-system, etc. **Even when debugging, avoid just giving cluster-admin rights** to service accounts; restrict to what is necessary ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=legacy%20Attribute%20Based%20Access%20Control,ABAC)) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=When%20using%20RBAC%2C%20prefer%20namespace,necessary%20for%20your%20specific%20situation)).

**ClusterRoles** vs Roles: If you need cluster-wide permissions (like listing nodes, or managing CRDs), ClusterRole is used. For most app-level things, a Role (namespace-scoped) is sufficient.

**Kubernetes API Access**: By default, the cluster doesn’t have authentication for end-users out of the box (for on-prem, you might use certificates or static token files). It’s recommended to integrate with an identity provider (OpenID Connect, etc.) for user auth if multiple people will operate the cluster ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=2.%20Use%20Third,API%20Server)). But that’s more cluster admin stuff. For now, just ensure only authorized people have the kubeconfig.

### 5.4 Pod Security and Best Practices

Beyond RBAC (which is access to API), consider security at the pod level:

- Run pods with a **read-only root filesystem** if possible and with a specific non-root user. We configured the Spring Boot container to use `appuser`. The NGINX one by default runs as root (to bind 80) but you can configure it to run as non-root on a higher port, or use NGINX’s securityContext to drop privileges. Kubernetes `securityContext` in the manifest can enforce non-root (`runAsNonRoot: true`) and can drop Linux capabilities, etc.
- Use **Pod Security Standards**: There are Baseline and Restricted levels. You can enforce these per namespace. This ensures, for example, that no pod runs with privileged mode or host mounts in a given namespace, which greatly reduces risk.
- Keep the cluster’s attack surface low: disable anonymous access to the API (kubeadm does by default), consider enabling audit logs to detect suspicious API use, and use network policies to limit pod communication (e.g., the database pod only accepts traffic from the backend pods’ labels).

**Network Policies**: For example, to restrict the Postgres service to only be reachable by the backend app in the same namespace:

```yaml
kind: NetworkPolicy
metadata:
  name: db-access
  namespace: yourapp
spec:
  podSelector:
    matchLabels:
      app: postgres
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: springboot-backend
      ports:
        - protocol: TCP
          port: 5432
```

This says pods labeled app=postgres only allow ingress from pods labeled app=springboot-backend on port 5432. Everything else is blocked (by default, NetworkPolicy is deny-by-default for any pod selected when at least one policy exists for it). For this to work, you need a network plugin supporting NetworkPolicy (Calico, Cilium, etc., Flannel by itself doesn’t support network policy unless combined with something like Canal or NetworkPolicy controller).

**Image Security**: Ensure images are from trusted sources. You might want to scan your images for vulnerabilities (in CI pipelines or using tools like Trivy or Clare). Also, enforce imagePullPolicy appropriately (IfNotPresent vs Always for dev vs prod).

To summarize security best practices:

1. **Enable RBAC** and avoid wild-card permissions ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=RBAC%20can%20help%20you%20define,ABAC)).
2. **Network segmentation**: limit access to API and between pods (use network policies) ([Kubernetes Security Best Practices in 2025](https://www.practical-devsecops.com/kubernetes-security-best-practices/#:~:text=Kubernetes%20Security%20Best%20Practices%20in,Update%20Kubernetes%20Regularly%20%C2%B7%206)).
3. **Use namespaces** to separate environments or teams and apply policies accordingly.
4. **Secure etcd and K8s components** (TLS, firewall) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=3,Firewall%20and%20Encryption)) ([Kubernetes Security Best Practices: 10 Steps to Securing K8s](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/#:~:text=Since%20etcd%20stores%20the%20state,use%20it%20to%20elevate%20privileges)).
5. **Run least privilege pods** (no privileged containers unless absolutely needed, no hostPath volumes unless needed, drop capabilities).
6. **Keep software updated**: apply Kubernetes patches, rotate certs when needed (kubeadm cert renewal), update base images.
7. **Monitor**: Use tools to monitor for security events (some use Falco for runtime security monitoring, or cloud-native firewall). Also, ensure logging (discussed later) so you have an audit trail.

By adhering to these networking and security practices, your deployment will be resilient against many common attacks or misconfigurations. Now, let’s focus on how to continuously build and deploy these apps with CI/CD pipelines.

## 6. CI/CD Pipelines (Automated Build and Deployment)

Manually building images and applying manifests is not sustainable. We want a Continuous Integration and Continuous Deployment (CI/CD) pipeline to automate building Docker images, pushing them to a registry, and deploying to Kubernetes. This section explores implementing CI/CD using tools like **Jenkins**, **GitHub Actions**, and **Argo CD** (for GitOps). We will highlight how to integrate these with our Kubernetes deployment process.

### 6.1 CI Pipeline: Building and Pushing Images

Regardless of the CI tool, the steps for CI (Continuous Integration) are:

1. **Code push** triggers the pipeline.
2. **Build and test**: e.g., run `npm test` for React, `mvn test` for Spring Boot.
3. **Build container images** for each component.
4. **Push images to a registry** (e.g., Docker Hub, Harbor, ECR, etc.).

For instance, using Jenkins:

- You might set up a Jenkins job (Pipeline) that checks out code from Git, then uses Docker to build the images, and pushes them. Jenkins can run on your cluster or outside, but needs access to Docker or a Docker daemon (or use Kaniko/BuildKit for building in cluster without privileged docker).
- The Jenkinsfile (pipeline as code) would have stages: Checkout, Build (Docker build), Push.

An example Jenkins Pipeline snippet (groovy syntax) might be:

```groovy
pipeline {
  agent any
  stages {
    stage('Checkout Source') {
      steps {
        git url: 'https://github.com/your/repo.git', branch: 'main'
      }
    }
    stage('Build Images') {
      steps {
        sh 'docker build -t myregistry/react-frontend:${BUILD_NUMBER} -f frontend/Dockerfile frontend/'
        sh 'docker build -t myregistry/spring-backend:${BUILD_NUMBER} -f backend/Dockerfile backend/'
      }
    }
    stage('Push Images') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
          sh 'docker push myregistry/react-frontend:${BUILD_NUMBER}'
          sh 'docker push myregistry/spring-backend:${BUILD_NUMBER}'
        }
      }
    }
    // Deployment stage will be next
  }
}
```

This is a simplified example. In practice, you might also tag with `latest` or a git commit SHA, and handle versioning carefully. The pipeline logs in to Docker registry and pushes. Credentials are stored securely in Jenkins (`docker-hub-creds` id in this case) ([Deploying a Dockerized Application to the Kubernetes Cluster using Jenkins - Simple Talk](https://www.red-gate.com/simple-talk/devops/containers-and-virtualization/deploying-a-dockerized-application-to-the-kubernetes-cluster-using-jenkins/#:~:text=This%20Jenkins%20Pipeline%20stage%20will,app)).

With Jenkins, after pushing, you can use Kubernetes CLI or plugins to deploy:

- Jenkins has a Kubernetes plugin where you can use a `kubernetesDeploy` step to apply YAML files ([Deploying a Dockerized Application to the Kubernetes Cluster using Jenkins - Simple Talk](https://www.red-gate.com/simple-talk/devops/containers-and-virtualization/deploying-a-dockerized-application-to-the-kubernetes-cluster-using-jenkins/#:~:text=kubernetesDeploy%28configs%3A%20)) ([Deploying a Dockerized Application to the Kubernetes Cluster using Jenkins - Simple Talk](https://www.red-gate.com/simple-talk/devops/containers-and-virtualization/deploying-a-dockerized-application-to-the-kubernetes-cluster-using-jenkins/#:~:text=The%20Jenkinsfile%20will%20create%20a,Jenkins%20Pipeline%20with%20four%20stages)). For example, if your manifest files are in the repo (perhaps templated with the image tag), you could do:
  ```groovy
  stage('Deploy to Kubernetes') {
    steps {
      kubernetesDeploy configs: "k8s/*.yaml", kubeconfigId: 'my-kubeconfig'
    }
  }
  ```
  This would apply all YAMLs in the k8s folder (you’d have updated the image tag in those YAMLs or use `--record`).
  In the RedGate example pipeline, after pushing, they pull the new image on the cluster and update the deployment ([Deploying a Dockerized Application to the Kubernetes Cluster using Jenkins - Simple Talk](https://www.red-gate.com/simple-talk/devops/containers-and-virtualization/deploying-a-dockerized-application-to-the-kubernetes-cluster-using-jenkins/#:~:text=)) ([Deploying a Dockerized Application to the Kubernetes Cluster using Jenkins - Simple Talk](https://www.red-gate.com/simple-talk/devops/containers-and-virtualization/deploying-a-dockerized-application-to-the-kubernetes-cluster-using-jenkins/#:~:text=It%20will%20pull%20bravinwasike%2Freact,js%20container%20to%20Kubernetes)).

Alternatively, you can use `kubectl` inside Jenkins:

```groovy
sh 'kubectl set image deployment/springboot-backend backend=myregistry/spring-backend:${BUILD_NUMBER} -n mynamespace'
```

to update the Deployment’s image. Or apply a new manifest.

**GitHub Actions**: If your code is on GitHub, Actions is a convenient CI tool:

- You can use Docker build and push actions. For example, `docker/build-push-action` to build and push an image (we saw that in Nic Wortel’s blog) ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=,github.sha)) ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=,the%20repository%20in%20this%20job)).
- Then use `azure/k8s-deploy` action (despite the name, it works for any Kubernetes) to apply manifests ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=cluster.%20We%27ll%20use%20the%20azure%2Fk8s,can%20commit%20the%20manifest%20files)) ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=,kubernetes%2Fdeployment.yaml%20kubernetes%2Fingress.yaml%20kubernetes%2Fservice.yaml)). This action can even substitute image tags in the manifest for you ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=cluster.%20We%27ll%20use%20the%20azure%2Fk8s,the%20deployment%20manifest%20but%20our)).
- You need to provide it credentials to the cluster. One way is to use a Kubernetes service account token (not ideal to put in GitHub secrets), or better, if your cluster API is reachable, use `kubectl` with a Kubeconfig secret, or setup OIDC between GitHub and your cluster (GitHub OIDC -> short-lived token).
- For simplicity, many use the approach: store `KUBECONFIG` as a secret and then use `actions-runner` or `kubectl` to apply.

An example GitHub Actions workflow (pseudo):

```yaml
name: CI-CD
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/login-action@v2
        with:
          registry: myregistry.com
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_PASS }}
      - uses: docker/build-push-action@v3
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          tags: myregistry/react-frontend:${{ github.sha }}
      - uses: docker/build-push-action@v3
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: myregistry/spring-backend:${{ github.sha }}
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Set Kubernetes context
        uses: azure/k8s-set-context@v2
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBECONFIG }}
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v1
        with:
          manifests: |
            k8s/backend-deployment.yaml
            k8s/frontend-deployment.yaml
          images: |
            myregistry/react-frontend:${{ github.sha }}
            myregistry/spring-backend:${{ github.sha }}
```

This is illustrative. The `azure/k8s-deploy` will replace the image references in the given manifests with the provided images (with the commit SHA tag) and apply them ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=cluster.%20We%27ll%20use%20the%20azure%2Fk8s,the%20deployment%20manifest%20but%20our)) ([Continuous deployment to Kubernetes with GitHub Actions](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions#:~:text=uses%3A%20azure%2Fk8s,github.sha)). This ensures the new pods pull the new image. Only on pushes to main branch do we deploy (you can restrict, e.g., only on successful tests, etc., and maybe only to a dev cluster or use environment protection for prod).

**Argo CD (GitOps)**: Argo CD approaches deployment differently. Instead of the CI pipeline pushing changes to the cluster, you push changes to a **Git repository containing your K8s manifests** (for example, you update the image tag in a YAML stored in a git repo). Argo CD, running in the cluster, continuously monitors that git repo (you define an Argo CD Application pointing to a path in a repo) and applies any changes to the cluster.

The GitOps flow is:

- CI builds and pushes image.
- CI might update a Kubernetes manifest or Helm values file in a git repo (like a “deploy” repo) to use the new image tag, then commits and pushes it.
- ArgoCD notices the commit and syncs the cluster to match the git state (which includes pulling the new image tag).

Argo CD provides a nice UI to see differences, supports automated sync or manual (for approvals), and can handle multiple environments by using separate git paths or branches, etc.

Using Argo CD can separate concerns: developers commit desired state, and Argo ensures cluster matches it. It also means you don’t need to give your CI pipeline direct access to the cluster (Argo has the access inside cluster). This can be a security benefit.

**Choosing Tools**: Jenkins is classic and might be preferred if you have it in-house. GitHub Actions is cloud-based and good if code is on GitHub (and easy to set up for open source or smaller teams). ArgoCD is great for GitOps style and desired state management, especially if you favor pull-based deployment. They can also coexist: e.g., Actions builds images, then triggers Argo sync by committing manifest changes.

For completeness, other CI/CD mentions:

- **Jenkins X** (Jenkins for Kubernetes with more automation),
- **Tekton pipelines** (Kubernetes-native CI),
- **Flux CD** (another GitOps tool like ArgoCD),
- **Spinnaker** (CD tool),
- **GitLab CI** (if using GitLab).

The principles remain: automate everything from build to deploy, keep secrets out of pipeline logs, and ensure a reliable delivery process.

**CI/CD for our app**:

- We should ensure that when a developer merges code to main, within a short time the new version is running on the cluster.
- We also likely maintain different environments (dev, staging, prod) – you might have separate namespaces or clusters for these. The pipeline can deploy to a dev environment automatically, but for prod maybe require a manual approval or use ArgoCD with manual sync.
- Container image tags: using unique tags (like git SHA or build number) for each build is recommended over “latest”, as it is easier to track and avoids caching issues. The deployment YAML will be updated accordingly.

At the end of this pipeline setup, you have an automated process: commit code -> CI builds images -> CD deploys to K8s. This reduces human error and accelerates delivery.

Next, we address scaling and load balancing to ensure the app can handle increased traffic.

## 7. Scaling & Load Balancing

One of the strengths of Kubernetes is easy scaling of applications and built-in load balancing. In this section, we’ll discuss how to scale our application pods horizontally, how Kubernetes distributes traffic, and how to optimize resource usage. We’ll also touch on scaling the cluster itself and ensuring high availability.

### 7.1 Horizontal Pod Autoscaling (HPA)

**Horizontal Pod Autoscaler** (HPA) is a Kubernetes mechanism that automatically adjusts the number of pod replicas for a deployment based on observed metrics (like CPU usage or custom metrics) ([Horizontal Pod Autoscaling | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#:~:text=In%20Kubernetes%2C%20a%20HorizontalPodAutoscaler%20automatically,the%20workload%20to%20match%20demand)) ([Horizontal Pod Autoscaling | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#:~:text=Horizontal%20scaling%20means%20that%20the,already%20running%20for%20the%20workload)). For our Spring Boot deployment, if CPU usage goes high under load, HPA can increase the replicas, and later scale down when idle.

To use HPA, you need:

- Metrics to scale on. By default, Kubernetes uses CPU or memory metrics via the **Metrics Server**. Ensure you have the metrics-server deployed in your cluster (it’s often not installed by default on kubeadm clusters, you can deploy it easily).
- Define the HPA object with target deployment, target metric and thresholds.

Example HPA YAML for the backend:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: springboot-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

This says: maintain the deployment `springboot-backend` between 3 and 10 pods, scaling so that CPU usage stays around 50% on average ([HorizontalPodAutoscaler Walkthrough | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#:~:text=minReplicas%3A%201%20maxReplicas%3A%2010%20metrics%3A,target%3A%20type%3A%20Utilization%20averageUtilization%3A%2050)) ([HorizontalPodAutoscaler Walkthrough | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#:~:text=status%3A%20observedGeneration%3A%201%20lastScaleTime%3A%20%3Csome,currentReplicas%3A%201%20desiredReplicas%3A%201%20currentMetrics)). If all pods are over 50% CPU, the HPA controller will increase replicas (maybe by 1 at a time) and check again. If they’re underutilized and above minReplicas, it will scale down. HPA checks metrics periodically (default 15s or 30s intervals).

We set minReplicas to 3 (same as our spec) so it won’t drop below initial, and max 10 for safety. The threshold 50% means if current usage is 100% on each, it will try doubling pods to bring usage down roughly by half.

Apply this HPA. You can view HPA with `kubectl get hpa`. To test it, you could put load on the app (maybe a load test hitting it) and watch `kubectl get deploy` to see replicas count increase.

For the React frontend (NGINX), you can also autoscale if needed (based on CPU or even on something like network traffic if you integrate custom metrics). Often, the backend is more CPU-bound.

Remember:

- HPA requires metrics-server. Check `kubectl top pods` works (that indicates metrics available).
- HPA by CPU utilization uses the resource requests as the baseline (if type Utilization, 50% of what? It’s 50% of the request unless set differently). For example, if each pod requests 500m CPU, 50% means 250m usage as target.
- You can also autoscale on memory or custom metrics (using `type: AverageValue` or external metrics through Prometheus Adapter, etc.), but CPU is common.

**Vertical scaling**: We focus on horizontal (more pods). Vertical Pod Autoscaler (VPA) exists to recommend or adjust resource requests/limits for pods based on usage, but it typically isn’t used to dynamically change running pods (it can in off hours or with restart). It’s more advisory. HPA is primary for autoscaling.

### 7.2 Load Balancing and Service Exposure

Kubernetes has multiple layers of load balancing:

- **Internal Service LB**: Within the cluster, a Service of type ClusterIP will round-robin requests to its pods. If you use the default kube-proxy (iptables mode), it randomizes selection. In IPVS mode, it’s a weighted round robin. This distribution is usually sufficient to balance traffic evenly among pods.
- **Ingress Load Balancing**: The ingress controller (NGINX) we set up will also load balance incoming requests across the pods of a service. For example, if 5 backend pods exist, the NGINX ingress by default will round-robin among them. It uses the Service endpoints to know them.
- **External Load Balancer**: On-prem, if you used MetalLB or an external L4 LB, that handles distributing traffic to the ingress controller instances or nodes. If you run multiple ingress controller pods on multiple nodes, MetalLB could advertise a single IP that any of those pods can serve. Usually, ingress-nginx on bare metal might run as DaemonSet on all nodes with hostPort 80/443, and MetalLB directs traffic to any node (which then goes to the local ingress pod). Or NodePorts and an external load balancer device splitting across nodes.

From an application perspective, the main thing is that Kubernetes services handle load balancing automatically – you don’t have to manage upstream lists in your apps. The Spring Boot instances all get traffic via the service or ingress.

**Scaling the Services**:

- If you scale Spring Boot from 3 to 6 replicas (manually or via HPA), the Service will automatically include the new pods. Ingress will within seconds pick up new Endpoints.
- Scaling the React front is similar.

**Cluster Scaling**: On-prem scaling of nodes is manual (unless integrated with an infrastructure API). If you need to add more compute power, you add a new node (e.g., new VM or bare metal machine) and run kubeadm join. The scheduler will then have more resources to place pods. There is a Kubernetes **Cluster Autoscaler** project which can work with on-prem virtualization or bare metal if properly set up (it can run custom scripts to create new VMs, etc.), but commonly it’s used on cloud to request new VMs. On-prem, you might instead rely on a virtualization platform’s automation or just do it manually. Since it’s advanced, we skip automation of adding nodes.

**High Availability**: Make sure not to run everything on one node. Spread out pods by using anti-affinity if needed (K8s usually spreads replicas across nodes if resources allow). For example, two Spring Boot pods might land on two different nodes, so if one node goes down, you still have one pod on the other. You can enforce this with a PodAntiAffinity rule in the Deployment spec, requiring pods with same app not to co-locate.

**Resource Optimization**:

- Start with requests/limits as we set. Monitor actual usage.
- Overcommitting: Kubernetes allows scheduling pods such that sum of requests can exceed capacity (since not all apps peak at same time). But don’t overcommit too much, especially memory (if memory is exhausted, pods get OOM killed). CPU overcommit is more tolerable (just causes throttling).
- Use monitoring (Prometheus) to see if pods consistently underuse their allocations, you can reduce requests to allow more pods per node, or if they frequently hit limits, increase them or add more pods/nodes.
- Set up **liveness probes** to auto-restart stuck pods (we did that), and **readiness probes** to ensure only healthy pods get traffic – this indirectly helps load balancing by removing unhealthy endpoints.

In summary, Kubernetes will handle load balancing between pods and with HPA can automatically scale pods horizontally to meet demand. You as the operator need to ensure metrics are available and set appropriate thresholds and limits. Also, plan your node scaling in advance if expecting significantly more pods.

### 7.3 Load Testing and Capacity Planning

Though not explicitly requested, it's worth mentioning:

- After setting up autoscaling, do a load test to see at what point pods scale up and if performance is linear. Adjust HPA thresholds if needed (maybe target 70% CPU to allow higher utilization per pod before scaling).
- Plan capacity: if each Spring Boot can handle X requests per second, and you need 10X, ensure HPA maxReplicas is enough and you have enough nodes/CPU to run those pods.
- If using database, ensure it can handle increased load from more app pods (DB might become a bottleneck when app scaled out, so consider DB scaling or connection pooling limits).

Now that scaling and load balancing are configured, our application should be able to handle variable load. Next, we focus on monitoring and logging to maintain visibility into the system.

## 8. Monitoring & Logging

Monitoring and logging are critical for observing the health of the system, diagnosing issues, and capacity planning. In this section, we will set up **Prometheus and Grafana** for metrics monitoring, and an **ELK (Elasticsearch, Logstash/Fluentd, Kibana) stack** for centralized logging. We’ll also mention alternatives and how to integrate with our Spring Boot and React apps.

### 8.1 Metrics Monitoring with Prometheus and Grafana

**Prometheus** is a popular open-source monitoring system that scrapes metrics from endpoints (usually HTTP endpoints exposing metrics in a specific format) and stores them in a time-series database. **Grafana** is a visualization tool that can query Prometheus to display dashboards of these metrics.

In Kubernetes, a typical monitoring setup is the **Prometheus Operator** (or kube-prometheus stack) which sets up Prometheus, Grafana, and Alertmanager.
However, one can also deploy Prometheus and Grafana separately using Helm charts:

- The Prometheus chart will deploy Prometheus server, and optionally exporters.
- The Grafana chart deploys Grafana and can even provision dashboards automatically.

For our use-case:

- **Cluster metrics**: We want to monitor CPU/memory of nodes and pods. The metrics-server provides some, but Prometheus can get more detail through exporters like **node-exporter** (for node hardware stats) and scraping **cAdvisor** (Kubelet exposes container stats).
- **Application metrics**: Spring Boot can expose metrics via Actuator (if included). For example, Spring Boot + Micrometer can expose metrics on `/actuator/prometheus`. We should ensure our Spring Boot app has the Prometheus endpoint enabled (by adding the micrometer-registry-prometheus dependency and appropriate config). This will give metrics like request rates, response times, JVM memory, etc.
- The React app itself doesn’t expose metrics (it’s static), but NGINX metrics could be gathered (NGINX Plus has stats, or use an exporter stub status if needed). This is lower priority.

**Installing Prometheus**:
One quick method: use **kube-prometheus-stack** Helm chart (by Prometheus community). It includes Grafana.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack
```

This will deploy a whole suite in, say, monitoring namespace. It sets up scraping of Kubernetes components automatically using ServiceMonitors.

Alternatively, deploy Prometheus Operator manifests from GitHub. The result is Prometheus running in cluster, scraping all pods that have the appropriate annotations or ServiceMonitors.

**Scraping our app**: We can either annotate the Spring Boot service or pod to be scraped by Prometheus. For example, if using Prom Operator, create a `ServiceMonitor` like:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: springboot-sm
  labels:
    release: monitoring # matches the label of Prom instance
spec:
  selector:
    matchLabels:
      app: springboot-backend
  endpoints:
    - port: 8080
      path: /actuator/prometheus
```

This tells Prom to scrape pods of service with app label `springboot-backend` on port 8080 at that path. Or simpler, annotate the pod template:

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/actuator/prometheus"
```

If using the community Prom helm, it respects those annotations and will scrape automatically.

**Grafana**:
Once Prometheus is collecting metrics, Grafana can display them. Grafana will be accessible via a Service (often NodePort or LoadBalancer). You’d login (the chart often sets admin password or you provide it), add Prometheus as a data source (or the helm may do it already), and import dashboards.

- There are prebuilt dashboards for Kubernetes cluster, nodes (for node-exporter metrics), etc. The kube-prom-stack actually comes with many dashboards.
- You can also create a custom dashboard for the Spring Boot metrics (for example, graph request count, error count, GC times, etc).
- Grafana can be exposed via the same ingress controller or as a separate domain (e.g., grafana.mycluster.local).

With Prometheus and Grafana in place, you’ll have **visual insight**:

- CPU/Memory usage of each component (and HPA behaviors).
- Custom app metrics like number of orders processed, etc., if you instrument them.
- Ability to set up **alerts** in Prometheus (like if CPU > 90% for 5 min, or pod restart looping). The PrometheusOperator includes Alertmanager; you can configure it to send emails or Slack alerts on conditions.

### 8.2 Logging with EFK (Elasticsearch, Fluentd, Kibana)

**Centralized Logging** means instead of logging to local files on each container (which in K8s, you access via `kubectl logs`), you collect all logs to a central store. This allows searching across pods, persisting logs even after pods die, and troubleshooting easier.

A common stack is **EFK**:

- **Fluentd** (or Fluent Bit) as the log collector (the "L" in ELK is traditionally Logstash, but Fluentd is lighter and often used in Kubernetes).
- **Elasticsearch** as the storage and search engine for logs.
- **Kibana** as the web UI to query and visualize logs.

Deployment:

- **Fluentd/FluentBit**: Typically run as a **DaemonSet** on all nodes. It tails the container logs (from `/var/log/containers` or the Docker/CRIO log directory) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=In%20this%20tutorial%20we%E2%80%99ll%20use,will%20be%20indexed%20and%20stored)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=we%E2%80%99ll%20set%20up%20on%20our,will%20be%20indexed%20and%20stored)), adds metadata (pod name, namespace, etc.), and ships to Elasticsearch.
  - There are ready DaemonSet configs that come with the Fluentd image and necessary plugins. For example, the DigitalOcean tutorial provides YAMLs where Fluentd uses the kubernetes metadata filter ([Managing Kubernetes Logging with Elasticsearch, Fluentd, and ...](https://medium.com/@platform.engineers/managing-kubernetes-logging-with-elasticsearch-fluentd-and-kibana-efk-stack-c1a17824cf16#:~:text=Fluentd%20is%20a%20data%20collector,It%20is)) ([Logging for Kubernetes: Fluentd and ElasticSearch - MetricFire](https://www.metricfire.com/blog/logging-for-kubernetes-fluentd-and-elasticsearch/#:~:text=Logging%20for%20Kubernetes%3A%20Fluentd%20and,It%20offers%20support%20for)).
  - Fluent Bit is a lighter alternative, can forward to Fluentd or directly to Elastic.
- **Elasticsearch**: You can deploy ES in the cluster (it's heavy: requires more memory, possibly multiple nodes for HA). The DO tutorial uses a StatefulSet for a 3-node ES cluster ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=will%20be%20indexed%20and%20stored)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=Before%20you%20begin%20with%20this,the%20following%20available%20to%20you)). Make sure to allocate enough memory and storage (and possibly use persistent volumes).
- **Kibana**: Deploy as a Deployment, connect it to Elasticsearch service, and expose it (maybe behind an ingress or port-forward).

Since setting up ES can be memory-intensive, some on-prem users skip full ELK and use lighter solutions:

- **Loki** (by Grafana) for logs: works with Promtail (log shipper) and stores logs efficiently, queryable via Grafana. This is easier to manage than Elastic for some.
- **Graylog** or other systems, or even Splunk if company has it.

However, assuming EFK:
Once up, Kibana allows you to search logs. For example, filter by `kubernetes.pod_name:"springboot-backend-xyz"` to see logs from one pod, or search for an error across all pods in a namespace.

**Spring Boot logging**: Ensure your Spring Boot logs to stdout (by default, Spring Boot does log to console). Those will be captured by Fluentd. If you have JSON logging, even better for filtering.

**React/NGINX logging**: NGINX logs access and error to stdout/stderr in the container (depending on config). The default docker image might log access to stdout. Fluentd will capture those too. You can then analyze access logs in Kibana if needed (e.g., number of requests, IPs - but for heavy analysis, maybe use Prometheus metrics or a separate analytics pipeline).

**Retention**: Logging can consume a lot of storage. Decide how long to keep logs (e.g., 7 days). Elasticsearch indices can be set to delete older data or use ILM (Index Lifecycle Management). Alternatively, use smaller volume or offload to S3 (EFK can archive logs to object storage after some time, etc., if needed).

**Best Practices**:

- Do not log excessively at debug level in production; it will overload the system. Use info/warn/error appropriately.
- Mask or avoid logging sensitive info (GDPR, etc).
- Separate log streams if needed (some use different indices per namespace or app).
- Monitor your logging pipeline: if Fluentd or ES goes down, make sure it doesn’t crash your nodes by filling up disk. Usually, container logs on node are limited by size (Docker by default rotates at 100MB x 10 files = 1GB per container). Fluentd should handle backpressure but watch out.

Once this is in place, you can troubleshoot issues by checking logs in Kibana. For example, if the Spring Boot app throws an exception stacktrace, you search it in Kibana across all pods to quickly find when and where it happened. This is much easier than kubectl into each pod.

**Integration with Alerts**: You could set up Kibana alerting or use Prometheus to alert on log patterns (Promtail+Loki can alert on log events). But a simple approach is to at least have logs centralized so you can investigate after receiving an alert.

At this point, with Prometheus/Grafana and EFK, you have full **observability**:

- Metrics (for status and alerting),
- Logs (for deep dive into errors),
- If needed, you might add **Tracing** (e.g., Jaeger) if you have a distributed system and want to trace requests. Spring Boot can integrate with OpenTelemetry. That’s an advanced topic beyond our scope here.

Monitoring and logging ensure you can maintain the system effectively. Now we proceed to planning for the worst (backups and disaster recovery).

## 9. Backup & Disaster Recovery

No system is complete without a backup and disaster recovery plan. On-premises deployments are especially susceptible to hardware failures or other disasters (power outage, etc.), so you need to have a strategy to backup critical data and be able to restore your application in case of failure. In this section, we will cover what to backup in a Kubernetes context (etcd, persistent data, manifests) and how to automate backups using tools like **Velero**. We’ll also discuss disaster recovery processes.

### 9.1 Kubernetes Cluster Backups

A Kubernetes cluster’s **state** is primarily stored in etcd (the key-value store for all cluster data: Deployments, ConfigMaps, Secrets, etc.). Additionally, any persistent data stored in volumes (like our PostgreSQL PVC or any uploaded files, etc.) needs backup.

**What to backup** ([Kubernetes Backup: Complete guide with Velero Tutorial](https://www.kubecost.com/kubernetes-best-practices/kubernetes-backup/#:~:text=Kubernetes%20resources%20you%20should%20back,up)):

- **Etcd database**: If you lose all master nodes, you can recreate them if you have an etcd snapshot. Etcd can be backed up by taking snapshots (etcdctl snapshot save). If using kubeadm, the etcd data is typically under `/var/lib/etcd`. Regular etcd backups (e.g., cron job on master node) are recommended.
- **Kubernetes Resources (Manifests)**: You likely have your manifests in Git (infrastructure as code). If so, you can restore by re-applying them. If not, consider using `kubectl export` or Velero to backup cluster objects like Deployments, Services, etc. Velero can back up all cluster resources (excluding secrets optionally) and restore them on a new cluster.
- **Persistent Volume data**: e.g., the Postgres data. This needs backup at the application level (SQL dumps) and/or volume snapshots. Velero can integrate with storage providers to snapshot volumes (on-prem, it can call restic to backup PVs to an object store).
- **Configuration**: Things like TLS certificates or any external config not in etcd. But most should be in Secrets/ConfigMaps which are in etcd.

**Velero** ([Velero](https://velero.io/#:~:text=Velero%20Velero%20is%20an%20open,cluster%20resources%20and%20persistent%20volumes)) ([Velero](https://velero.io/#:~:text=Velero%20is%20an%20open%20source,cluster%20resources%20and%20persistent%20volumes)):
Velero is an open source tool by VMware for K8s backup/restore. It can back up cluster resources and volumes to cloud storage (S3, etc.) or NFS. On-prem, you can point Velero to an S3-compatible storage (if you have a NAS that supports object storage, or even MinIO deployed in cluster for backup storage). Velero runs as a deployment and coordinates backups (on-demand or scheduled).

Velero usage:

- Install Velero server in cluster (via `velero install` CLI or helm chart) with credentials for your backup storage.
- Create a backup schedule, e.g., daily backups at midnight, retaining last X days: `velero create schedule daily --schedule="@midnight" --ttl 720h` (720h = 30 days) ([Disaster recovery - Velero Docs](https://velero.io/docs/main/disaster-case/#:~:text=The%20default%20backup%20retention%20period%2C,to%20change%20this%20as%20necessary)).
- Velero will back up all objects (or you can scope it to certain namespaces). It can also backup PVCs via restic (Velero can auto annotate PVCs for restic if enabled).

In a disaster, you could install a fresh cluster and Velero, then do `velero restore backupname` to reinstate all the objects and persistent data (if using restic, it will copy data from the backup).

If not using Velero, consider manual backups:

- Etcd: Take snapshot. Example:
  ```bash
  ETCD_POD=$(kubectl -n kube-system get pods -l component=etcd -o name)
  kubectl -n kube-system exec $ETCD_POD -- etcdctl snapshot save /tmp/etcd-snapshot.db
  kubectl cp kube-system/$ETCD_POD:/tmp/etcd-snapshot.db ./etcd-snapshot.db
  ```
  Do that periodically and store the snapshot off the cluster.
- Database: Use a tool like `pg_dumpall` in a CronJob or external script to backup the Postgres to a file, and then perhaps upload to remote storage.
- Files: If there were any (not in our case beyond DB), ensure those volumes are backed up (NFS drives could have their own backup).

**Disaster Recovery Process**:

- **Partial failure (node lost)**: If a worker node dies, Kubernetes will reschedule pods to other nodes (provided volumes are accessible or those pods are stateless). For stateful (DB) pods, if the node with the only Postgres died and storage was local to it, that’s a problem. Ideally, use network storage so that a new pod can start on another node using the same PVC (which is possible if storage is networked and accessModes allow).
  If using Rook/Ceph or similar, it would replicate and handle a node loss gracefully by relocating data.
- **Master node loss**: If one master (control-plane) node fails and you only had one, cluster control is down (though apps keep running). To recover, you would need to restore etcd on a new master (or if you set up an HA control plane with 3 masters, one down is fine). For single-master clusters, backup etcd frequently. To recover, you can init a new master with `kubeadm init --experimental-control-plane` or similar and point it to restore from etcd snapshot.
- **Complete cluster loss**: Worst-case scenario, cluster and all nodes gone (fire, etc.). In that case, having everything in code + backups means you can rebuild on new hardware:
  1. Create new cluster (new masters/nodes).
  2. Restore etcd if available _or_ reapply manifests from Git.
  3. Restore volumes: perhaps using Velero to recreate PVCs and restic to restore data into them, or by restoring from DB backups.
  4. Basically, recreate the environment and deploy apps, then restore data (import DB backup into new DB pod).

This underscores that backing up the **data** (DB) is crucial, because everything else (deployments, etc.) you likely have in source control. Many teams choose GitOps partly so the source of truth is git rather than needing cluster backups for manifests.

**Backup Storage**:
Store backups off-site if possible (off the cluster, and maybe off the premises for true DR). For instance, copy etcd backups and DB dumps to cloud storage or a different physical location. This protects against a site-wide event.

**Testing Restores**:
It’s not enough to take backups; occasionally test that you can restore. Perhaps have a staging cluster where you try to restore last night’s backup to ensure the process works and the backup is valid.

**Kubernetes Upgrade**:
Another aspect of DR is upgrading Kubernetes versions periodically (e.g., from 1.25 to 1.26). Plan this when you can afford downtime or do rolling upgrade if multi-master. Always have backups before an upgrade in case you need to rollback (though rollback of cluster version is non-trivial, usually you restore from backup if it fails).

By implementing regular backups and having a DR plan, you mitigate the risk of catastrophic data loss or prolonged downtime. Document the procedures so that if a different engineer has to perform the recovery, they know the steps.

## 10. Best Practices & Troubleshooting

Finally, we compile a list of best practices and common issues/troubleshooting tips during deployment and operation. Even with everything set up, deployments can face performance issues or failures. This section provides guidance on performance tuning the apps on Kubernetes, debugging techniques, and addressing common errors like CrashLoopBackOff, ImagePullBackOff, etc.

### 10.1 Performance Tuning and Best Practices

- **Use appropriate resource requests/limits**: We emphasized this earlier. Setting these helps the scheduler and avoids resource contention. If an app is memory-intensive, give it a higher memory request to avoid being packed with others on a node. Avoid setting limits too low such that the app gets OOM-killed. Monitor and adjust.
- **Optimize the JVM for Kubernetes**: If using Java, consider enabling container-aware settings (Java 11+ does this by default). You might set `-XX:MaxRAMPercentage=75.0` for example to only use 75% of container memory. Also, tune garbage collection if needed for low-memory environments.
- **Connection pooling**: Ensure your Spring Boot app’s DB connection pool is sized appropriately. If you scale pods, the total number of DB connections = connections per pod \* number of pods. Make sure the DB can handle that or adjust pool size or use a proxy like PgBouncer if needed.
- **Readiness probes**: Use them to signal when an app is ready. For instance, don’t route traffic to Spring Boot until it finished heavy initialization. We did set a readiness probe. This helps avoid failed requests during rollout.
- **Rolling update strategy**: By default, Deployment does rolling updates (update a few at a time). For Spring Boot, which might be heavy, consider tweaking `maxUnavailable` or `maxSurge` if needed (e.g., allow one extra pod at rollout time to ensure capacity, etc.). Also, if downtime is unacceptable, ensure `maxUnavailable=0` so it always launches a new one before downing an old one.
- **Thread pools**: If your backend handles many concurrent requests, ensure its thread pool (tomcat or undertow in Spring Boot) is sized enough. Defaults might be 200, which is fine mostly. Monitor and adjust if you see saturation.
- **Static content**: Offload where possible (we serve via NGINX, which is good at static serving; alternatively, could serve React via a CDN if that was an option).
- **Networking**: For on-prem, network can be a bottleneck if using overlays (flannel VXLAN adds overhead). If high throughput is needed, consider using Calico in IP-in-IP mode or direct routing, or even kubernetes with SR-IOV for specific workloads.
- **Pod affinity/anti-affinity**: Use them to spread pods across nodes for resilience. We touched on anti-affinity for HA. Also consider colocation if needed (e.g., if two services chat a lot, you might want them on same node to reduce latency – but that’s advanced and often not needed).
- **Resource Quotas & Limits**: If multiple teams share cluster, implement ResourceQuota and LimitRange per namespace to enforce fair usage and default limits, preventing one team from hogging all resources unintentionally.
- **Security context**: Run containers as non-root where possible for safety. Also consider enabling seccomp profiles or AppArmor for your pods (there are default profiles that reduce kernel attack surface).
- **Upgrade strategy**: Keep Kubernetes version and application dependencies up to date. Do upgrades in test cluster first. For apps, use liveness probes to auto-recover if something goes wrong, but also set up proper monitoring to catch performance regressions after new deployments.

### 10.2 Common Issues and Troubleshooting Tips

Even with best practices, you will encounter issues. Here are some common ones and how to address them:

- **CrashLoopBackOff**: This status means a pod is starting, crashing, and restarting repeatedly ([CrashLoopBackOff in K8s - Red Hat Learning Community](https://learn.redhat.com/t5/DO280-Red-Hat-OpenShift/CrashLoopBackOff-in-K8s/td-p/35221#:~:text=CrashLoopBackOff%20in%20K8s%20,containers%20running%20within%20the%20pod)) ([Kubernetes CrashLoopBackOff: What it is, and how to fix it? - Sysdig](https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/#:~:text=The%20memory%20limits%20are%20too,is%20Out%20Of%20Memory)). Causes can be:
  - Application crash on startup (check logs: `kubectl logs <pod> -p` to see previous container log or current log). Maybe a missing configuration or environment variable (e.g., wrong DB host causing exception).
  - Port conflict or something preventing start (if you tried to run multiple processes in one container, etc.).
  - OOMKilled (out of memory) can also show as CrashLoopBackOff if the process is killed by kernel. `kubectl describe pod` and look at the last state of container to see if OOMKilled.
  - To troubleshoot: describe the pod to see events. Use `kubectl logs` to get application output. Adjust config or resources depending on findings ([Understanding Kubernetes CrashLoopBackOff & How to Fix It](https://www.groundcover.com/kubernetes-troubleshooting/crashloopbackoff#:~:text=It%20www,%C2%B7%20Dig%20through%20container)) ([How to fix and prevent CrashLoopBackOff events in Kubernetes](https://www.gremlin.com/blog/how-to-fix-kubernetes-crashloopbackoff#:~:text=How%20to%20fix%20and%20prevent,that%20contributed%20to%20a%20crash)).
  - If it’s due to waiting on DB, maybe the app should handle retry or you introduce an initContainer to wait for DB readiness.
- **ImagePullBackOff / ErrImagePull**: The pod cannot pull the container image. Possible reasons:
  - Wrong image name or tag (typo or the image wasn’t pushed). Verify the image exists in registry.
  - Not logged into registry (if a private registry). You might need to create a Secret of type docker-registry and add `imagePullSecrets` in the deployment.
  - Network issue reaching registry.
  - Fix by checking `kubectl describe pod` events to see error message and correct the cause (push image, fix secret, etc.).
- **Crash on one pod, not others**: Could be data-related (one instance got a heavy request and failed). Or a node issue. Check if only pods on a certain node fail – maybe that node has issue (disk full, etc.). `kubectl get nodes` to see if node conditions are all Normal.
- **High Restart Count**: If you see pods restarting occasionally (but not a constant CrashLoop), maybe liveness probe is killing them. If liveness probe is too strict (e.g., your app took slightly longer and was killed), tune the probe (increase timeout or failureThreshold).
- **Can’t connect to service**: For example, frontend can’t call backend. Possible causes:
  - Service not found: Did you use the correct service name and port? Check DNS resolution inside a pod (`kubectl exec -it <pod> -- nslookup springboot-backend`).
  - DNS issues: If CoreDNS is not working, maybe it crashed. Ensure kube-dns or CoreDNS pods are running in kube-system.
  - Network policy blocking: If you set NetworkPolicies, ensure they allow the needed traffic.
  - Cross-namespace: If frontend and backend in different namespaces, service DNS is `svc-name.namespace.svc.cluster.local` or use ExternalName. Or deploy them in same namespace or set up correct DNS query. Usually keep them in same namespace for simplicity unless multi-tenancy reasons.
- **Ingress not working**: If you get 404 or no response:
  - Check Ingress controller pod logs.
  - Is the ingress resource correctly defined (host, paths match)?
  - Did you configure DNS to point to the ingress controller IP?
  - If using self-signed cert or missing cert, maybe browser is blocking (check in browser dev tools).
  - `kubectl describe ingress` to see if it picked up rules and events (it might say no address if ingress controller not functioning).
- **Certificates issues**: If Let’s Encrypt failed, use `kubectl describe certificate` (if cert-manager) to see events (maybe DNS challenge failed).
- **PersistentVolume not attaching**: If a pod stays in Pending with “Volume not found” or “Volume not bound”:
  - Check PVC status (`kubectl get pvc`). If Pending, storage class might not be provisioning. Create a PV manually or fix storage class.
  - If Bound but pod still can’t mount, maybe the node doesn’t have access to that storage (like an iSCSI path error). Check events on pod for mount failures.
- **Resource exhaustion**: If pods are getting OOMKilled (check `kubectl get events` or describe pod events for OOMKilled messages), you need to increase memory limits or reduce usage. If node itself is out of memory, you might see `kubectl describe node` events with system OOM. In such case, either add nodes or reduce total load or increase node memory.
- **Debugging**: Use `kubectl exec` to get a shell in a running container for on-the-fly diagnostics (e.g., exec into Spring Boot container and run `curl http://localhost:8080/actuator/health` or check env vars).

  - If a container won’t start (CrashLoop), you can copy the same image and run it with an override command like sleep, to get inside and poke around. For example: `kubectl run debug --image=myimage --restart=Never -- sleep 1d` then exec into it. This is useful if some dependency is missing and you want to inspect container filesystem or environment.
  - Kubernetes also has ephemeral containers for debugging (if enabled) which can attach a debugger container to a running pod without exec (for more complex scenarios).

- **Viewing Events**: Remember `kubectl describe` is your friend for debugging. It shows events related to pods, services, etc. For example, if a pod couldn’t schedule, events will say why (e.g., insufficient CPU on nodes, or affinity rules unsatisfied, etc.).

Common causes for CrashLoopBackOff include misconfiguration, insufficient memory (leading to OOM) ([Kubernetes CrashLoopBackOff: What it is, and how to fix it? - Sysdig](https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/#:~:text=Sysdig%20sysdig,is%20Out%20Of%20Memory)), or dependency not available. For ImagePull issues, it’s usually credentials or typos.

### 10.3 Continuous Improvement and Maintenance

Deployment is not a one-time task. Continuously improve by:

- Updating images to reduce vulnerabilities (watch security feeds for your base images or use tools that alert).
- Improving CI/CD: e.g., add automated tests, security scans in pipeline, etc.
- Regularly checking cluster components (like upgrading the ingress controller, etc., when improvements come).
- Documenting the system for team knowledge.

By following the best practices and being prepared to troubleshoot, you can ensure a smooth operation of your React + Spring Boot application on Kubernetes. The key is to monitor proactively, automate where possible, and apply lessons from any incidents to prevent them in the future.

---

**Conclusion:** In this extensive guide, we’ve covered setting up a production-ready on-premises Kubernetes cluster, containerizing a React frontend and Spring Boot backend, deploying them with all necessary Kubernetes resources, integrating a database, and setting up the surrounding ecosystem (CI/CD, scaling, monitoring, logging, security, backups). By following these steps and best practices, you can deploy applications reliably on Kubernetes and maintain them effectively. Kubernetes has a learning curve, but once the pieces are in place, it provides a powerful platform for running microservices at scale. Happy deploying!
