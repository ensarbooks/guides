# Deploying a Full-Stack Application in an On-Prem Kubernetes Cluster with ArgoCD

This guide provides a comprehensive, step-by-step walkthrough for deploying a full-stack application (React frontend, Spring Boot backend, and MySQL database) on an **on-premises Kubernetes cluster**, using **ArgoCD** to manage Continuous Integration/Continuous Deployment (CI/CD) through GitOps. We will cover everything from setting up the Kubernetes cluster on bare-metal or virtual machines, to deploying and scaling the application, to implementing monitoring, logging, and security best practices. The guide is organized into the following sections:

1. **Setting Up Kubernetes On-Prem** – Installing Kubernetes on bare-metal/VMs, configuring networking and storage, RBAC, and cluster security.
2. **Installing and Configuring ArgoCD** – Deploying ArgoCD in Kubernetes, connecting Git repositories, and defining GitOps workflows for CI/CD.
3. **Application Deployment** – Writing Kubernetes manifests for the React frontend, Spring Boot backend, and MySQL database, including Ingress routing and secure management of environment variables and secrets.
4. **Database Management** – Running MySQL in Kubernetes with persistent storage, backup strategies, and failover mechanisms for high availability.
5. **CI/CD Pipeline with ArgoCD** – Automating deployments via GitOps, and handling rollbacks and versioning of releases.
6. **Scaling and Performance Optimization** – Implementing horizontal/vertical scaling for workloads and optimizing resource usage.
7. **Monitoring and Logging** – Setting up Prometheus and Grafana for metrics monitoring, and an EFK (Elasticsearch, Fluentd, Kibana) stack for centralized logging.
8. **Security Best Practices** – Enabling TLS with cert-manager, applying network policies and RBAC, and scanning for vulnerabilities.
9. **Testing and Debugging in Kubernetes** – Troubleshooting common issues and using Kubernetes tools (`kubectl`, logs) for debugging deployments.

Each section includes clear explanations, **code snippets** (YAML manifests, Bash commands, configuration files) and, where relevant, references to external documentation or best practices (in the format 【source†lines】). The content is structured with logical headings and short paragraphs for readability, and bullet-point steps or tips where appropriate. Let’s dive in.

## 1. Setting Up Kubernetes On-Prem

Setting up a production-grade Kubernetes cluster on-premises involves preparing your infrastructure, installing the Kubernetes components, and configuring the cluster for networking, storage, and security. On-prem (self-managed) Kubernetes gives you full control but also requires you to manage complexities that cloud providers typically handle for you ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=%28DIY%29%2C%20or%20self,challenge%20can%20be%20most%20apparent)) ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=3,to%20your%20data%20center%20configuration)). In this section, we will cover:

- **Installation**: How to install Kubernetes on bare-metal servers or virtual machines (VMs), using tools like kubeadm.
- **Networking**: Configuring pod networking (via a Container Network Interface plugin) and service networking (including options for load balancing on bare-metal).
- **Storage**: Setting up persistent storage solutions (using Persistent Volumes and CSI drivers) for stateful workloads like databases.
- **RBAC**: Enabling and utilizing Role-Based Access Control to manage user permissions.
- **Basic Security**: Initial steps to secure the cluster (API server access, certificates, etc.).

### 1.1 Installing Kubernetes on Bare-Metal Servers or VMs

**Planning the Cluster**: First, decide the number of nodes and their roles. For high availability in production, plan for multiple control plane (master) nodes and several worker nodes. For example, you might use 3 master nodes and 3+ worker nodes to tolerate failures. (For a simpler test setup, 1 master and 2 workers could suffice, but this is not HA.) Ensure each server (physical or VM) meets recommended requirements (e.g., a modern Linux OS, adequate CPU/RAM, and network connectivity between nodes).

**Prepare the OS**: On each server, install a supported Linux distribution (e.g., Ubuntu, CentOS/RHEL, or Debian). Update the system and disable swap (Kubernetes requires swap off for stability):

```bash
# On each node (run as root or with sudo):
swapoff -a                 # disable swap
sed -i '/swap/d' /etc/fstab  # remove swap entry to keep it off on reboot
```

Enable necessary kernel modules and settings. For example, ensure that bridged traffic is passed to iptables (so Kubernetes networking can function properly):

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
overlay
EOF

sudo modprobe br_netfilter
sudo modprobe overlay

# Set sysctl params for networking
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system  # apply sysctl settings
```

Install a container runtime on each node. Kubernetes supports containerd, CRI-O, Docker (dockershim deprecated). For example, to install containerd:

```bash
sudo apt-get update && sudo apt-get install -y containerd
# Configure containerd and start it (specific steps depend on OS; ensure systemd cgroup driver if using Kubernetes defaults)
```

**Install kubeadm, kubelet, kubectl**: Kubernetes provides `kubeadm` (for cluster bootstrapping), `kubelet` (node agent), and `kubectl` (command-line client). Install these on all nodes. For example, on Ubuntu 20.04+:

```bash
# Add Kubernetes apt repository
sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] \
  https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install specific version of kubelet, kubeadm, kubectl (e.g., 1.27.x)
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl  # prevent automatic updates
```

Verify that `kubeadm`, `kubectl`, and `kubelet` are installed by checking their versions (`kubeadm version`, etc.).

**Initialize the Control Plane**: Pick one node to be the first control plane (master). Use `kubeadm init` to bootstrap the cluster. For example:

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

- `--pod-network-cidr` specifies a CIDR for the pod network. This example uses Flannel’s default CIDR; if using Calico or others, you might choose a different subnet or none (for Calico’s default).
- On an HA setup, additional flags are needed (e.g., `--control-plane-endpoint` with a VIP or load balancer address, etc.), but for a single master this is sufficient.

`kubeadm` will output a lot of information and, importantly, a **join command** for worker nodes. It will also by default set up the Kubernetes control-plane components (API server, etcd, controller manager, scheduler) and enable RBAC authorization. After a successful init, do the following on the master node:

```bash
# Set up local kubectl access (as regular user, assuming ~/.kube exists)
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

This copies the admin kubeconfig to your user directory so you can use `kubectl`. Now verify the master is up:

```bash
kubectl get nodes
# You should see the master node with STATUS Ready (or soon after initializing).
```

**Join Worker Nodes**: On each worker node, run the join command that `kubeadm init` provided. It will look similar to:

```bash
sudo kubeadm join <MASTER_IP>:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
```

This command makes the worker node join the cluster and register with the control plane ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=kubeadm%20token%20create%20)) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=sudo%20kubeadm%20join%2010.128.0.37%3A6443%20,hash%20sha256%3A37f94469b58bcc8f26a4aa44441fb17196a585b37288f85e22475b00c36f1c61)). If you misplaced the join command or token, you can regenerate it on the master with `kubeadm token create --print-join-command` ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=If%20you%20missed%20copying%20the,token%20with%20the%20join%20command)). After joining all workers, check on the master:

```bash
kubectl get nodes -o wide
```

You should see all your nodes (master and workers) listed. (By default, the master node is tainted to not schedule regular pods; only system pods run there. This is fine for production. For testing, you can remove the taint to use the master as a worker with `kubectl taint nodes --all node-role.kubernetes.io/control-plane-` ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=By%20default%2C%20apps%20won%E2%80%99t%20get,apps%2C%20taint%20the%20master%20node)).)

At this point, the core cluster is up but **not ready to run pods** until a network plugin is installed (next section).

### 1.2 Configuring Networking and Storage

**Pod Network (CNI Plugin)**: Kubernetes doesn’t come with a built-in pod network, so after bringing up the cluster you must install a CNI (Container Network Interface) plugin. Popular choices for on-prem include **Calico**, **Flannel**, **Weave Net**, and others. Calico is often favored for its network policy support. To install Calico, for example, you can apply the official Calico manifest:

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

This will set up Calico’s operator, daemon sets, etc., enabling networking for pods. If using Flannel, you’d use Flannel’s YAML (which expects the `--pod-network-cidr=10.244.0.0/16` we provided to kubeadm). After installing the CNI plugin, the cluster’s CoreDNS pods should become Running and you can deploy pods across nodes. The DevOps guide confirms installing a network plugin like Calico to enable pod networking and network policies ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=Kubeadm%20does%20not%20configure%20any,networking%20and%20enable%20network%20policy)) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=Execute%20the%20following%20commands%20to,plugin%20operator%20on%20the%20cluster)).

**Service Networking (Load Balancing)**: On a cloud Kubernetes, a Service of type `LoadBalancer` would provision a cloud load balancer. On-prem, you have a few options:

- Use **NodePort** or **Ingress** for external access in smaller setups (NodePort exposes a port on each node, which can be less flexible).
- Deploy a software load balancer like **MetalLB** if you want `LoadBalancer` Services to work. MetalLB can allocate an external IP from a pool to services on bare-metal, acting as a load balancer within your network ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=2,workload%20needs%20can%20help%20save)). For example, to install MetalLB: create a ConfigMap with an IP range and deploy MetalLB’s controller/speaker pods. This will allow you to expose services with an external IP in a bare-metal environment ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=2,workload%20needs%20can%20help%20save)).

- Use an external load balancer appliance (like F5, Citrix ADC) integrated with Kubernetes Service `LoadBalancer` (usually via a cloud provider plugin or manual configuration).

For this guide, we assume either MetalLB is set up for `LoadBalancer` resources or that we will primarily use **Ingress** (see section 3.4) to expose the web application. In any case, ensure that your networking solution allows access to cluster services from your LAN or users.

**Persistent Storage Solutions**: Most real-world applications need persistent storage (especially databases). On-prem, you need to integrate Kubernetes with storage systems:

- If you have a NAS or SAN, you can use **NFS** or **iSCSI** with the appropriate Kubernetes **CSI driver**. Many storage vendors provide CSI drivers to let you dynamically provision Persistent Volumes on their storage from Kubernetes ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=unless%20you%20are%20using%20a,premises)). For example, you could use an NFS server with the NFS-Subdir-External-Provisioner for dynamic PVs, or a Ceph cluster with Rook CSI, etc.

- In simpler setups, you might use **hostPath** (not recommended for multi-node production, as it ties data to one node) or a **Local PV** provisioner for local disks. There are also lightweight storage solutions like OpenEBS or Longhorn that can replicate data across nodes.

For our MySQL database (section 3.3), we will use a PersistentVolumeClaim (PVC) that binds to a storage class. Make sure your cluster has a **default StorageClass** configured (check with `kubectl get storageclass`). If not, set one up (for example, if using NFS provisioner or others, mark it as default). This allows PVCs to automatically get a PV. Storage is critical for stateful apps ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=5,premises)), so verify this before deployment.

**Example**: If using a simple NFS provisioner, you might deploy it and then create a StorageClass like:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-sc
provisioner: example.com/nfs # provisioner name as provided by the NFS driver
mountOptions:
  - vers=4.1
parameters:
  archiveOnDelete: "false"
```

Mark it as default if needed (`storageclass.kubernetes.io/is-default-class: "true"` annotation). Later, when we create a PVC for MySQL, it will use this class to provision storage.

### 1.3 Setting Up Role-Based Access Control (RBAC)

Kubernetes RBAC is a mechanism to regulate access to cluster APIs and resources. By default (if using kubeadm with recent Kubernetes versions), RBAC is enabled on the API server. This means you need appropriate Roles/ClusterRoles and RoleBindings/ClusterRoleBindings for users or service accounts to perform actions.

**Kubeadm default**: The kubeadm init process typically enables RBAC (authorization mode `--authorization-mode=Node,RBAC`). It also creates some default ClusterRoles (like `cluster-admin`, `edit`, `view`) and binds system components. As a cluster administrator, you initially have full rights via the admin kubeconfig.

**Creating RBAC rules**: To allow other users or to limit service accounts, you define YAML manifests. For example, suppose you want to create a read-only user for viewing cluster resources. You would create a ServiceAccount, a ClusterRole with read permissions, and a ClusterRoleBinding to bind the account to that role:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: readonly-user
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-all
rules:
  - apiGroups: ["", "apps", "batch"] # "" indicates core API group
    resources: ["*"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-all-binding
subjects:
  - kind: ServiceAccount
    name: readonly-user
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: read-all
  apiGroup: rbac.authorization.k8s.io
```

This would grant the `readonly-user` ServiceAccount read access to all resources. In practice, you might create user accounts via X.509 certificates or OIDC and bind them to roles, but that’s outside our scope. The key is: **apply least privilege**. Only give components the access they need ([K8s security - What are YOUR best practices? : r/kubernetes - Reddit](https://www.reddit.com/r/kubernetes/comments/1as69kc/k8s_security_what_are_your_best_practices/#:~:text=Proper%20Kubernetes%20cluster%20configuration%20,)). We will see RBAC again when setting up ArgoCD (which needs certain privileges to deploy manifests) and Fluentd (which needed a ClusterRole to read pod metadata ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=rules%3A%20,list)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=kind%3A%20ClusterRoleBinding%20apiVersion%3A%20rbac,kind%3A%20ServiceAccount))).

**Note**: For basic cluster operation, you might not need to configure extra RBAC initially, but be aware that any dashboard or CI system you use should get its own service account with proper role bindings instead of using the admin credentials.

### 1.4 Securing the Kubernetes Cluster

Security is critical from the get-go. Here are initial steps and best practices to secure your on-prem cluster:

- **APIServer access**: Limit access to the Kubernetes API. Ideally, keep it on a private network. If you need remote kubectl access, consider using a VPN or secure ingress. Ensure the API server is behind a firewall and only reachable by trusted IPs or users. By default, kubeadm configures API server with TLS (self-signed certificates in `/etc/kubernetes/pki`). Keep those certificates safe. You can also use your own Certificate Authority (CA) for Kubernetes if needed (kubeadm allows providing custom CA certs) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=How%20to%20use%20Custom%20CA,Certificates%20With%20Kubeadm)) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=In%20this%20post%2C%20we%20learned,step%20by%20step%20using%20kubeadm)).

- **Etcd security**: The etcd database (which stores cluster state, including Secrets) should also be secured. By default, etcd is secured with TLS (certs in the same pki folder) and only accessible from localhost on the master. If you run multi-master, etcd communication is also TLS-secured. Ensure firewall rules prevent etcd port (2379) access from unauthorized sources.

- **RBAC and API controls**: We already covered RBAC for API permissions. Additionally, consider enabling **audit logging** on the API server to log access attempts, and use admission controllers for extra security (PodSecurityPolicy was one way, now replaced by Pod Security Standards (Baseline/Restricted) or Open Policy Agent Gatekeeper for custom policies).

- **Node Security**: Lock down the nodes – only Kubernetes and necessary services should run. Ensure the network is segmented so that only known traffic can reach the nodes (e.g., database clients or app users shouldn’t directly access pod network). Kubernetes can enforce **Network Policies** at the pod level (more on this in Security Best Practices section 8.2) to restrict inter-pod traffic.

- **Upgrades and Patching**: Keep Kubernetes versions up to date. Plan a **upgrade strategy**: since on-prem doesn’t auto-upgrade, you need to periodically upgrade (Kubernetes does minor releases about every 3 months) ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=you%20can%20integrate%20your%20existing,have%20specific%20capabilities%20around%20K8s)). Test upgrades on a non-prod cluster first due to possible API changes ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=when%20a%20new%20upstream%20version,prem%20implementation.%20Or%20you%20may)). Also, regularly patch the OS and container runtime for security updates.

- **Cluster Monitoring**: Have monitoring in place for your cluster’s health (section 7 covers Prometheus). Also consider using security tools to scan your cluster configuration against benchmarks (for example, run **kube-bench** for CIS Kubernetes Benchmark compliance checks).

- **Backups**: Backup etcd data regularly (especially before upgrades) ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=1,data%20center%20and%20infrastructure%20downtimes)). You can use `etcdctl snapshot save` or set up an automated job. This will allow recovery of cluster state if you lose all masters.

These steps set the stage for a **secure and stable** Kubernetes foundation. With the cluster up and running, we can proceed to install ArgoCD for GitOps-based deployment.

## 2. Installing and Configuring ArgoCD

**ArgoCD** is a popular declarative GitOps CD (Continuous Deployment) tool for Kubernetes. It watches your Git repositories for changes in Kubernetes manifests and automatically applies them to your cluster, ensuring the live state matches the Git (desired) state ([Argo CD Deploying an Application - Kube by Example](https://kubebyexample.com/learning-paths/argo-cd/argo-cd-deploying-application#:~:text=Argo%20CD%20Deploying%20an%20Application,state%20on%20your%20Kubernetes%20installation)). We will install ArgoCD in the on-prem cluster and configure it to manage our application’s deployment manifests.

### 2.1 Setting Up ArgoCD on Kubernetes

ArgoCD itself runs as a set of pods inside Kubernetes. The official installation provides either YAML manifests or a Helm chart. Here, we’ll use the manifest approach (straightforward for beginners):

1. **Install ArgoCD in a Separate Namespace**: It’s best practice to run ArgoCD in its own namespace (commonly named `argocd`). Use kubectl to create the namespace and apply the install manifest:

   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

   This will create all the necessary ArgoCD components (Deployments for api server, repo server, application controller, etc., plus Services, ConfigMaps, Secrets, CRDs, etc.) ([How To Setup Argo CD On Kubernetes [Beginners Guide]](https://devopscube.com/setup-argo-cd-using-helm/#:~:text=It%20creates%20many%20Kubernetes%20objects,scoped%20%26%20cluster%20scoped%20resources)). After a minute, run `kubectl get pods -n argocd` to see pods like `argocd-server`, `argocd-repo-server`, `argocd-application-controller`, etc. All should reach Running status.

2. **Expose ArgoCD API/UI**: By default, ArgoCD’s server is exposed internally (ClusterIP service on port 443). To access the ArgoCD web UI or use `argocd` CLI, you have a few options on-prem:

   - For testing, do a port-forward: `kubectl port-forward svc/argocd-server -n argocd 8080:443` and then access https://localhost:8080. This shows ArgoCD’s UI (you’ll get a self-signed cert warning) ([How To Setup Argo CD On Kubernetes [Beginners Guide]](https://devopscube.com/setup-argo-cd-using-helm/#:~:text=You%20can%20access%20the%20ArgoCD,the%20following%20port%20warding%20command)).
   - For production, you’d likely want to expose it via an Ingress or a LoadBalancer service. If you have an ingress controller (like Nginx Ingress) set up, you can create an Ingress resource for `argocd-server` (with TLS). Or if using MetalLB, change the `argocd-server` service to type LoadBalancer by editing the service or using a Helm install option.

   For simplicity, we’ll assume using port-forward or NodePort while configuring. (Later, we can set up an Ingress for ArgoCD UI under our domain, see section 8.1 for TLS).

3. **Login to ArgoCD**: The default ArgoCD install creates an admin account. The default username is `admin` and the password is auto-generated. Fetch the initial admin password from the ArgoCD secret:

   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret \
       -o jsonpath="{.data.password}" | base64 -d && echo
   ```

   Use that password to login either via the web UI or CLI. For CLI, first download the ArgoCD CLI binary (from the ArgoCD releases page) and log in:

   ```bash
   argocd login <argocd_server_address> --username admin --password <password>
   ```

   (If using port-forward, server address is `localhost:8080`). On first login via UI, you’ll see the ArgoCD dashboard ([How To Setup Argo CD On Kubernetes [Beginners Guide]](https://devopscube.com/setup-argo-cd-using-helm/#:~:text=To%20login%20to%20the%20UI%2C,need%20a%20username%20and%20password)). It will show no applications yet (just the ArgoCD itself).

4. (Optional) **Change Admin Password**: It’s wise to change the default admin password or create new user accounts. You can change it in the UI or via CLI:
   ```bash
   argocd account update-password
   ```
   And follow prompts. For production, you might integrate ArgoCD with an SSO/OIDC or LDAP for user management (beyond scope here).

At this point, ArgoCD is running. Next, we connect it to our Git repository containing the application’s Kubernetes manifests.

### 2.2 Connecting Git Repositories and Configuring Manifests

ArgoCD uses **Git repositories** as the source of truth for application manifests. We need to provide ArgoCD with the repository URL and the path where our Kubernetes YAMLs reside. There are two ways to configure ArgoCD applications: via the web UI/CLI, or by creating Kubernetes `Application` objects (ArgoCD CRD) in YAML (declarative approach). We will illustrate using YAML (which can itself be applied via `kubectl` or managed in Git for GitOps of ArgoCD itself).

**Prepare a Git Repository**: Suppose we have a Git repository (e.g., in GitHub or an internal Git server) called `fullstack-k8s-manifests`. This will hold the Kubernetes manifests for our React, Spring Boot, and MySQL components (we’ll create those manifests in section 3). The repo could be structured as follows:

```
fullstack-k8s-manifests/
├── README.md
├── base/  (optional if using kustomize)
├── dev/   (manifests for dev environment, optional)
└── prod/  (manifests for prod environment)
      ├── frontend-deployment.yaml
      ├── backend-deployment.yaml
      ├── mysql-statefulset.yaml
      ├── frontend-service.yaml
      ├── backend-service.yaml
      ├── mysql-service.yaml
      ├── ingress.yaml
      ├── configmap.yaml (if any)
      └── secret.yaml (or sealed-secret.yaml)
```

For simplicity, we might put all manifests in one folder (e.g., `prod/` or even the root). The key is that ArgoCD needs to know the repo URL, the revision (branch/tag/commit), and the path within the repo to use.

**Create an ArgoCD Application**: An ArgoCD `Application` is a custom resource that defines a relationship between the Git repo (source) and the cluster (destination and namespace). We can define it in YAML:

```yaml
# fullstack-app-argocd.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fullstack-app # ArgoCD application name
  namespace: argocd # ArgoCD's namespace (where the ArgoCD app CRD is created)
spec:
  project: default # use default project unless you created a custom ArgoCD project
  source:
    repoURL: ssh://git@github.com/YourOrg/fullstack-k8s-manifests.git
    targetRevision: main # branch to track (could be tag or commit SHA)
    path: prod # path in the repo where manifests are
  destination:
    server: https://kubernetes.default.svc # URL of the cluster API (in-cluster)
    namespace: fullstack-prod # namespace to deploy the app resources
  syncPolicy:
    automated:
      prune: true # allows ArgoCD to delete resources that are not in Git
      selfHeal: true # allows ArgoCD to correct drift automatically
    syncOptions:
      - CreateNamespace=true # auto-create the namespace if it doesn't exist
```

Let’s break down important fields:

- `repoURL`: URL of your Git repository. It can be HTTPS or SSH. If the repo is private, you’ll need to **give ArgoCD access credentials**. For HTTPS repos, ArgoCD can use username/password or personal access token; for SSH, you need to add your SSH private key to ArgoCD. You can do that via CLI (`argocd repo add <repo-url> --ssh-private-key-path ~/id_rsa`) or create a secret in `argocd` namespace. In our case above (`ssh://git@github.com/...`), we’d ensure ArgoCD has the deploy key.

- `targetRevision`: the Git branch or tag. Using a tag or commit hash can pin a version; using a branch (like `main` or `master`) follows the latest commits on that branch.

- `path`: the directory in the repo. Here we use `prod`, assuming our manifests for production are in `prod/` directory of the repo.

- `destination`: which cluster and namespace to deploy to. `server: https://kubernetes.default.svc` with in-cluster URL tells ArgoCD to deploy to the same cluster it’s running in (you can also manage external clusters by registering them with ArgoCD, but not needed for on-prem single cluster). `namespace: fullstack-prod` means all resources will go into a namespace called “fullstack-prod”. We should ensure this namespace exists or let ArgoCD create it (that’s what `CreateNamespace=true` in syncOptions does).

- `syncPolicy`: we enable automated sync. This means ArgoCD will automatically apply changes from Git **without manual intervention**. We also allow prune, so if we remove a manifest from Git, ArgoCD will delete the corresponding resource in the cluster. `selfHeal` means if someone manually changes something in the cluster (out of band), ArgoCD will notice the drift and revert it to match Git. This fully enforces the GitOps paradigm. (In some cases, teams choose manual sync or disable auto prune, requiring manual approval for changes – that’s configurable based on your needs.)

Apply this `Application` manifest:

```bash
kubectl apply -f fullstack-app-argocd.yaml
```

Now, in the ArgoCD UI, you should see a new application “fullstack-app”. It will try to sync automatically. If your manifests are already in the repo, it will create all those Kubernetes objects in the cluster. If manifests are not there or incomplete, the app might show an error or out-of-sync status. We’ll be populating the repo with manifests in the next section.

**ArgoCD Application Example**: The above manifest is in line with ArgoCD’s specification. For instance, an official example (guestbook app) shows similar fields for source and destination ([Application Specification Reference - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/#:~:text=,project%3A%20default)) ([Application Specification Reference - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/#:~:text=,Helm%20repo%20instead%20of%20git)). We used `automated` sync, but note that during initial setup you might set `syncPolicy: {} ` (empty) to not auto-deploy until you verify configuration. You can always toggle auto-sync later.

**Connecting the Repo (Alternate via UI)**: Alternatively, you could have done the following via ArgoCD UI:

- In **Settings -> Repositories**, add your Git repo credentials (especially if private). ArgoCD stores them securely (as Secrets in its namespace).
- Click **New Application** in UI, fill in the form (app name, project, repo URL, path, cluster, namespace, etc.), and save.

Either way, ArgoCD now knows where to pull manifests from.

### 2.3 Defining GitOps Workflows

With ArgoCD set up, let’s outline the **GitOps workflow** for our CI/CD pipeline:

1. **Git as Source of Truth**: All environment configuration and deployment manifests are stored in Git. For our app, that means the YAML files for Deployments, Services, Ingress, etc., live in the Git repo we configured. They reference container images by tag (e.g., `myapp-backend:v1.0.0`). Initially, these could be set to a “dev” tag or an initial version.

2. **Continuous Integration (CI)**: We will likely have a separate process (outside of ArgoCD’s scope) to build the application code into container images. For example, a Jenkins pipeline or GitHub Actions workflow could:

   - Detect a commit in the application source code repo (one for frontend, one for backend).
   - Run tests, then build a Docker image for the React app and the Spring Boot app.
   - Push the images to a container registry (e.g., Harbor on-prem, Docker Hub, etc.).
   - Update the Kubernetes manifest repository with the new image tag (for example, update the Deployment YAML to use `myapp-backend:v1.0.1`). This step could be automated by the CI pipeline or by a GitOps bot. (There are tools like ArgoCD Image Updater that can watch registries and update manifests, but a simple approach is your CI does a git commit to the manifest repo).

3. **Git Push triggers Deployment**: When the manifest repo receives the updated YAML (say via a commit "Update backend image to v1.0.1"), ArgoCD notices this change. ArgoCD polls Git periodically (every 3 minutes by default). We can also configure a **Webhook** from our Git server to ArgoCD, so that ArgoCD gets notified immediately of a commit and triggers a sync ([How To Setup Argo CD On Kubernetes [Beginners Guide]](https://devopscube.com/setup-argo-cd-using-helm/#:~:text=way,to%20deploy%20application%20using%20ArgoCD)). (ArgoCD has a built-in webhook endpoint for GitHub, GitLab, etc.)

4. **ArgoCD Syncs Changes**: ArgoCD pulls the latest manifests at that commit and does a **sync** operation. This means applying the changed Deployment (which causes Kubernetes to perform a rolling update of the pods with the new image). ArgoCD UI will show the app transitioning from OutOfSync to Synced, and you can see the new replica set being created.

5. **Continuous Deployment**: This way, every code change that passes CI and is merged to the main branch (and hence updates the Kubernetes manifests) triggers an automatic deployment to the cluster. This is the essence of GitOps CI/CD.

6. **Rollbacks and History**: Each Git commit is essentially a version of the desired state. If a problem is detected in version v1.0.1, we can revert the manifest repository to the previous commit (v1.0.0). ArgoCD will detect that and perform a rollback (by changing the Deployment back). Additionally, ArgoCD itself keeps a **history** of sync operations. You can use the ArgoCD UI or CLI to rollback to a previous **History ID** directly ([argocd app rollback Command Reference - Argo CD - Read the Docs](https://argo-cd.readthedocs.io/en/latest/user-guide/commands/argocd_app_rollback/#:~:text=cd,flags%5D)) ([Argocd app rollback - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/release-2.0/user-guide/commands/argocd_app_rollback/#:~:text=Argocd%20app%20rollback%20,prune%20Allow)). For example: `argocd app rollback fullstack-app 2` would roll back to deployment #2 in history. Under the hood, this uses the stored manifests from that sync. (Note: if auto-sync is on, ArgoCD temporarily pauses it or you should revert the git commit as well to avoid re-reverting forward).

7. **Validation**: This workflow assumes changes are tested before being pushed to the manifest repo. Some teams use multiple environments (dev, staging, prod) each with their own ArgoCD app and perhaps separate branches or folders in Git for manifests. In this guide, we focus on one environment, but know that GitOps scales to multi-env by using either separate repos or directory structure and ArgoCD Applications (or ApplicationSet CRs) for each.

**GitOps Benefits**: By using this workflow, we get version control, traceability (each change is a commit with history), and the ability to rollback by reverting code. The cluster state is **self-documenting** (just check Git for what should be deployed). Also, no manual kubectl or imperative commands are needed in the deployment process – the CD system takes care of it once code is merged.

We have now configured the cluster and ArgoCD. Next, we'll create the actual **Kubernetes manifests** for our application and push them to the repo so ArgoCD can deploy them.

## 3. Application Deployment

Our full-stack application consists of three main components:

- **React frontend** – a single-page application (SPA) that will be served as static files (HTML/JS/CSS) to users’ browsers.
- **Spring Boot backend** – a RESTful API server (for example) that the frontend calls for data. This will run as a Java application.
- **MySQL database** – a relational database to store persistent data, used by the Spring Boot application.

We will deploy each of these in Kubernetes. In a Kubernetes context:

- React and Spring Boot will each run in one or more **pods** (managed by Deployments). They are stateless services.
- MySQL will run in a pod with persistent storage (managed by a Deployment or StatefulSet). It’s stateful.
- We will create **Service** objects to allow internal communication (e.g., Spring Boot -> MySQL, and possibly React -> Spring Boot if not going via client).
- We will create an **Ingress** to route external HTTP traffic to the React frontend and the Spring Boot service.
- Configuration (like database connection strings) and **secrets** (like DB credentials) will be provided via Kubernetes ConfigMaps/Secrets rather than hard-coded.

Let’s go through each component’s manifest and then the ingress and secrets.

### 3.1 Kubernetes Manifests for the React Frontend

The React app, once built, is just static files. Typically, you might use a simple web server (like **NGINX** or Apache httpd) to serve those files. Another approach is to use a Node.js server, but NGINX is more common for static SPAs. For this guide, assume we have built the React app (via `npm run build`) and created a Docker image that packages the static files with an NGINX server.

For example, a Dockerfile might look like:

```Dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY public public
COPY src src
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# Copy a custom nginx.conf if needed (to handle routing)
```

This produces an image, say `myregistry.com/myapp-frontend:1.0.0`.

Now the Kubernetes **Deployment** for the React frontend:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  namespace: fullstack-prod
  labels:
    app: myapp-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp-frontend
  template:
    metadata:
      labels:
        app: myapp-frontend
    spec:
      containers:
        - name: myapp-frontend
          image: myregistry.com/myapp-frontend:1.0.0
          ports:
            - containerPort: 80 # NGINX serves on port 80
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 250m
              memory: 256Mi
          readinessProbe:
            httpGet:
              path: / # try to fetch the index page
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
          # No env vars needed for purely static content (if any config, could mount ConfigMap)
```

Key points:

- We run 2 replicas of the frontend for higher availability (if one pod restarts during an update, the other serves traffic) and potentially load balancing.
- The pod template has a label `app: myapp-frontend` which the selector matches (this ties into the Service we’ll create).
- The container uses the built image and exposes port 80 (NGINX default HTTP port).
- We defined resource requests/limits to ensure the pod gets at least 0.1 CPU and 128Mi memory and max 0.25 CPU/256Mi. Adjust based on actual needs.
- A readiness probe checks that the server returns HTTP 200 on “/” – once NGINX is serving files, the pod becomes ready.
- If we needed to provide some runtime configuration (maybe the API endpoint), we could mount a small ConfigMap or use an environment variable that NGINX or the app reads. In many SPA setups, the API URL is fixed or relative. We’ll assume it’s relative or the same domain, so no special config needed for now.

Next, the Service for the frontend:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: fullstack-prod
spec:
  selector:
    app: myapp-frontend
  ports:
    - port: 80 # service port
      targetPort: 80 # container port to forward to
      protocol: TCP
  type: ClusterIP
```

This Service will get a cluster-internal IP and route traffic to any pods with label `app: myapp-frontend` on port 80. Since we will use an Ingress, we don’t need NodePort or LoadBalancer on this service; ClusterIP is fine (Ingress controller will route to it).

Now, the React app will be accessible inside the cluster via `frontend-service:80`. Through the Ingress (configured later), it will be accessible outside.

### 3.2 Kubernetes Manifests for the Spring Boot Backend

The Spring Boot application (let’s assume it’s a REST API) will be packaged as a Docker image, e.g., `myregistry.com/myapp-backend:1.0.0`. It likely listens on port 8080 by default. It also needs configuration for connecting to the MySQL database (JDBC URL, user, password), which we will supply via environment variables or config.

First, create a **Secret** for database credentials (since Spring Boot needs to authenticate to MySQL). We will assume a DB name and user we want:

- DB name: `myappdb`
- DB user: `myappuser`
- DB password: (generate a strong password, e.g., `S3cReTpw`)

And MySQL root password for completeness (though the app will use the user, not root). Let’s create one Secret YAML to hold these:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-db-secret
  namespace: fullstack-prod
type: Opaque
data:
  mysql-root-password: { { base64_encode("RootPassword123") } }
  mysql-user: { { base64_encode("myappuser") } }
  mysql-password: { { base64_encode("S3cReTpw") } }
  mysql-database: { { base64_encode("myappdb") } }
```

_(Note: replace the values with base64 of your actual passwords; `echo -n "RootPassword123" | base64` etc.)_

This Secret will be mounted in both the MySQL deployment (for root password) and the Spring Boot deployment (for user credentials).

Now the **Deployment** for Spring Boot:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
  namespace: fullstack-prod
  labels:
    app: myapp-backend
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
        - name: myapp-backend
          image: myregistry.com/myapp-backend:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              value: jdbc:mysql://mysql-service.fullstack-prod.svc.cluster.local:3306/myappdb
            - name: SPRING_DATASOURCE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-user
            - name: SPRING_DATASOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-password
            - name: SPRING_DATASOURCE_DRIVER_CLASS_NAME
              value: com.mysql.cj.jdbc.Driver
            - name: SPRING_JPA_HIBERNATE_DDL_AUTO
              value: update
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /actuator/health # assuming actuator health endpoint
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
```

Explanation:

- 2 replicas of the backend as well, for fault tolerance and load (if needed).
- Container image for Spring Boot.
- Environment variables:
  - `SPRING_DATASOURCE_URL` is set to the JDBC URL for MySQL. We reference the MySQL Service (`mysql-service`) which we will create, in the same namespace (`fullstack-prod`). In Kubernetes DNS, it will resolve as `mysql-service.fullstack-prod.svc.cluster.local`. Port 3306 is default MySQL port. And the database name appended.
  - Username and password are pulled from the Secret using `valueFrom: secretKeyRef`. This is secure because the secret is not exposed in plain text in the manifest (just referenced). Only the key and secret name are given. At runtime, the env var is populated from the Secret. **Important**: Make sure the service account running this pod has access to that secret (by default, in the same namespace, it does).
  - We also set driver class (not always needed if Spring Boot auto-detects via URL) and perhaps JPA auto ddl (just an example, optional).
- Resource requests/limits given moderately.
- Probes: We assume the Spring Boot app has Actuator health endpoint. Liveness probe checks it starting at 30s (so the app has time to start), readiness at 10s. This ensures traffic isn’t sent until app is ready, and if app hangs, liveness will eventually restart it.

Now, the Service for the backend:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: fullstack-prod
spec:
  selector:
    app: myapp-backend
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP
```

This service lets other pods in the cluster reach the backend via `backend-service:8080`. We’ll use the Ingress to expose it outside to users (if needed). Actually, for a web app, typically users don’t call backend directly; the frontend does. The frontend could call backend via the Ingress as well (if CORS and such are handled) or we might not even expose backend to public except through the same domain. We’ll address that in Ingress.

### 3.3 Kubernetes Manifest for MySQL Database

Deploying MySQL in Kubernetes requires special attention because it is a stateful service. We will deploy it with persistent storage and only 1 replica for now (no replication yet in this simple setup). For production, one might consider running MySQL as a primary-replica setup or using a MySQL Operator for HA; we discuss that in section 4. For now, a single MySQL instance with backups is our approach.

We’ll use a Kubernetes **StatefulSet** for MySQL. A StatefulSet is the recommended workload for databases, as it ensures stable network identity and storage for the pod.

**Persistent Volume Claim**: We need a PVC for MySQL data. In a StatefulSet, we can have it create one PVC per replica via `volumeClaimTemplates`. If only 1 replica, it’s just one PVC.

First, ensure a StorageClass is available (from section 1.2). We’ll assume a default StorageClass is set (e.g., `standard` or our `nfs-sc`). We request, say, 10Gi of storage for MySQL.

**Secret for MySQL**: We already created `myapp-db-secret` with user and password. We also have `mysql-root-password` in there. The MySQL Docker image can use the environment variable `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` to initialize the database on first run ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,name%3A%20mysql%20containerPort%3A%203306%20volumeMounts)) ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=env%3A%20,name%3A%20data%20mountPath%3A%20%2Fvar%2Flib%2Fmysql)). We’ll use those.

MySQL deployment manifest (StatefulSet):

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
  namespace: fullstack-prod
spec:
  serviceName: mysql-headless # headless service for DNS (will create below)
  replicas: 1
  selector:
    matchLabels:
      app: myapp-mysql
  template:
    metadata:
      labels:
        app: myapp-mysql
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: mysql
          image: mysql:8.0 # using official MySQL image
          ports:
            - containerPort: 3306
              name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-root-password
            - name: MYSQL_DATABASE
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-database
            - name: MYSQL_USER
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-user
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-db-secret
                  key: mysql-password
          volumeMounts:
            - name: data
              mountPath: /var/lib/mysql
      volumes: [] # not used (we'll use volumeClaimTemplates for persistence)
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
        storageClassName: standard # or your storage class name
```

Breakdown:

- `serviceName: mysql-headless` means we will create a headless service named `mysql-headless` which is needed for stable DNS of the StatefulSet pods. Even with 1 replica, it’s good to include.
- `replicas: 1` for now.
- Pod template has label `app: myapp-mysql`.
- We set `terminationGracePeriodSeconds: 30` to give MySQL up to 30 seconds to shutdown on pod kill (MySQL will flush and stop).
- Container:
  - MySQL 8.0 image.
  - Env vars: root password, and an app database and user from our secret. On first startup, the MySQL entrypoint will create a database named `myappdb` and a user `myappuser` with that password and grant it access ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,name%3A%20mysql%20containerPort%3A%203306%20volumeMounts)). This saves us from manually running SQL to create the schema user.
  - We mount a volume at `/var/lib/mysql` which is where MySQL stores data. The `volumeMounts` references a volume named `data`.
- `volumeClaimTemplates`: This is a section unique to StatefulSets. It will create a PVC for each replica with the given spec. We name it "data", matching the volumeMount. It requests 10Gi storage with access mode RWO. We specify the storage class. This will result in a PVC named `data-mysql-0` (because the pod will be mysql-0 since it's the first replica). The PVC will be bound to an actual PV (via dynamic provisioning on our storage class). The pod will then have that storage mounted.

We also need to create Services for MySQL. Typically:

- A **Headless Service** for the StatefulSet (`mysql-headless` as named) to govern DNS for pods.
- A regular Service for clients to connect. In our case, only the Spring Boot app connects internally, so a ClusterIP is fine.

Headless Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
  namespace: fullstack-prod
  labels:
    app: myapp-mysql
spec:
  clusterIP: None # headless
  selector:
    app: myapp-mysql
  ports:
    - name: mysql
      port: 3306
      targetPort: 3306
```

The headless service with `clusterIP: None` ensures that DNS A records are created for each pod (`mysql-0.mysql-headless.fullstack-prod.svc.cluster.local`). This is more useful when we have multiple replicas (like mysql-1, mysql-2 for primary/replicas). With one replica, it’s not strictly needed, but we include for completeness.

The regular Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: fullstack-prod
spec:
  selector:
    app: myapp-mysql
  ports:
    - name: mysql
      port: 3306
      targetPort: 3306
  type: ClusterIP
```

We named it `mysql-service` which we used in the Spring Boot’s JDBC URL. This Service will route to the MySQL pod on port 3306. It selects the same label `app: myapp-mysql` (so it’ll pick up mysql-0 pod). If in future we have replicas, a client could use this service to connect to any (for reads), but typically you’d separate writer and reader services. For now, we consider single instance.

**Note**: The official Kubernetes example for MySQL StatefulSet uses similar concepts and shows a headless service and how each replica gets a DNS name ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,io%2Fname%3A%20mysql%20spec)) ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=kubectl%20apply%20)). We simplified to one replica. The example also uses an init container and xtrabackup for cloning data to replicas ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,C%20%2Fvar%2Flib%2Fmysql)) ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=%5B%5B%20%24ordinal%20,name%3A%20data%20mountPath%3A%20%2Fvar%2Flib%2Fmysql)), which is not needed in our single instance case.

### 3.4 Setting Up Ingress for External Access

Now we have services internally for frontend, backend, and database. The database service will _not_ be exposed externally (only accessible within cluster). The **frontend and backend** need to be reachable by end users or at least by the end user's browser.

In a typical setup, we would expose only the **frontend** to the end user. The React app then makes XHR/fetch calls to the backend API. We have two choices:

- Expose the backend as a separate DNS (e.g. api.myapp.com) or path, and let the frontend call that.
- Or serve the frontend and backend under one domain – for example, requests to `/` go to frontend, requests to `/api/` go to backend. This avoids CORS issues since it’s same origin.

We will do the latter for simplicity using a single Ingress with **path-based routing**:

- `http://myapp.example.com/` and everything not under `/api/` -> goes to frontend-service.
- `http://myapp.example.com/api/` (and sub-paths) -> goes to backend-service.

This way, the React app can call `/api/...` and it will hit the backend. No separate domain needed.

Ensure you have an **Ingress Controller** installed in the cluster (like NGINX Ingress Controller) since on bare-metal, Kubernetes doesn’t have a native ingress by default. If not installed, you can install NGINX Ingress with:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.0/deploy/static/provider/baremetal/deploy.yaml
```

(This deploys the necessary controller pods and config on a bare-metal environment). Once the ingress controller pods are running (in `ingress-nginx` namespace typically), you can create Ingress resources.

Ingress resource for our app:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: fullstack-prod
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    # (We will add TLS annotation later in security section)
spec:
  rules:
    - host: myapp.example.com # replace with your domain
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 8080
          - path: /(.*)
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

Explanation:

- We specify a host (myapp.example.com). You need DNS (or host file for testing) to point this domain to the ingress controller’s external IP (or the node IP for bare-metal, depending how ingress is set up).
- The first path rule uses a regex-like syntax (the `(/|$)(.*)` along with rewrite-target annotation) to capture anything starting with `/api` and route to backend. The annotation `rewrite-target: /$2` will remove the `/api` base before sending to the service (so backend sees the path after /api).
  - Alternatively, if backend is expecting /api in its routes, we could drop rewrite and just let it pass through.
  - Nginx Ingress’s usage of regex requires the annotation for rewrite in older versions; with pathType Prefix, we might simply use `/api` prefix without regex if backend expects `/api` as part of its context. Simpler: use `path: /api` and it will prefix match (meaning /api, /api/v1, etc. all match).
- The second path catches all other requests (`/(.*)` essentially everything not matched by /api) and sends to frontend.
- `pathType: Prefix` indicates prefix matching (with the given pattern).
- We might also want a rule to send `/api` itself (without trailing slash) to backend; our regex covers both `/api/` and `/api` due to the `(/|$)` part.

**Verify**: With this ingress, if you hit `http://myapp.example.com/`, you'll get the React app. If the React app makes a call to `/api/hello`, the request goes to the ingress, which matches `/api` prefix, routes to backend-service on port 8080. Backend responds, the ingress passes it back.

Later, we will secure this with TLS (see Security section). For now, it’s HTTP.

The ingress controller will need to be accessible. On bare-metal, the Nginx ingress by default creates a Service of type NodePort. You might change it to use MetalLB with LoadBalancer or just use host ports. But verifying ingress setup is out-of-scope – just ensure that `myapp.example.com` resolves and reaches the controller (often by using a host on the same network and pointing domain to one of the node IPs).

### 3.5 Managing Environment Variables and Secrets Securely

We have introduced some Secrets and Config in our manifests (database credentials, etc.). It’s crucial to handle these securely:

- **Kubernetes Secrets**: We used a Secret for DB password. Kubernetes Secrets are base64-encoded by default, not encrypted, when stored in etcd. Ensure your etcd is secure (network restricted) and consider enabling **encryption at rest** for Secrets in the cluster (a config option for kube-apiserver with an encryption config file). That way even if someone gets etcd access, they can’t easily read secrets ([How To Use “Sealed Secrets” In Kubernetes. - Medium](https://medium.com/@abdullah.devops.91/how-to-use-sealed-secrets-in-kubernetes-b6c69c84d1c2#:~:text=This%20process%20ensures%20that%20sensitive,the%20cluster%2C%20providing%20a)).

- **GitOps and Secrets**: Storing secret manifests in Git is tricky because you don’t want to expose the plaintext values. Options:
  - Use a tool like **Sealed Secrets** by Bitnami. Sealed Secrets allow you to store an encrypted secret in Git, which can only be decrypted by the cluster’s controller. You encrypt the Secret with the cluster’s public key; the SealedSecrets controller (running in cluster) will decrypt it into a real Secret ([How To Encrypt Kubernetes Secrets Using Sealed Secrets (Detailed Guide)](https://devopscube.com/sealed-secrets-kubernetes/#:~:text=Storing%20Kubernetes%20Secret%20manifest%20files,means%20anyone%20can%20decode%20them)) ([How To Encrypt Kubernetes Secrets Using Sealed Secrets (Detailed Guide)](https://devopscube.com/sealed-secrets-kubernetes/#:~:text=This%20is%20where%20Sealed%20Secrets,tools%20with%207000%2B%20Github%20Stars)). This way, your Git repo can safely contain `sealedsecret` YAMLs (which are useless to an attacker without the key).
  - Use **SOPS** (by Mozilla) with KMS/PGP to encrypt secret files in Git.
  - Or, do not store them at all in Git – instead, manually create the Secret in the cluster (out-of-band) or use an external secret store with something like External Secrets Operator or HashiCorp Vault. However, this breaks the fully declarative model slightly.

Given our scenario, a straightforward way is to use Sealed Secrets. For brevity, we won’t detail installation, but it involves installing the controller and using the `kubeseal` CLI to encrypt an existing Secret manifest ([How To Encrypt Kubernetes Secrets Using Sealed Secrets (Detailed Guide)](https://devopscube.com/sealed-secrets-kubernetes/#:~:text=This%20is%20where%20Sealed%20Secrets,tools%20with%207000%2B%20Github%20Stars)). The result is a SealedSecret resource that the controller will turn into a Secret inside the cluster. For example:

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: myapp-db-secret
  namespace: fullstack-prod
spec:
  encryptedData:
    mysql-root-password: AgB8z+... (huge base64 string)
    mysql-user: AXSDFg...
    mysql-password: <encrypted>
    mysql-database: <encrypted>
```

ArgoCD can manage SealedSecrets (they are just another Kubernetes resource). This way, the actual sensitive values are encrypted in Git, satisfying security.

- **ConfigMaps**: We didn’t explicitly use a ConfigMap, but if we had non-sensitive configs (like feature flags, etc.), those could be in a ConfigMap and stored in Git as YAML (that’s fine since not sensitive). Pods can mount them or env var from them.

- **Avoid Hardcoding**: No secret or password should be hardcoded in the Deployment manifest or container image. Always use references to secrets or config. For instance, our Spring Boot image should not have the DB password baked in – we pass it via env var.

- **Service Account Permissions**: Limit which service accounts can read which secrets. In Kubernetes, a pod can only directly use secrets in the same namespace, and you can use RBAC to restrict if needed. By default, any pod in a namespace could potentially read any secret if it had the credentials, but normal pods run under the `default` service account which has no list/get secrets permission. Only if a pod tries to access the secret via API (which it shouldn’t) would RBAC matter. Mounting the secret as env or volume is allowed because you explicitly gave the pod that secret reference.

- **Externalizing configuration**: For more complex scenarios, consider using a dedicated config service or HashiCorp Vault (with Vault Agent injector to inject secrets). But that adds complexity beyond our scope.

In summary, manage environment variables through ConfigMaps/Secrets, and manage Secrets carefully (encryption at rest, and encrypted in Git or not in Git) ([How To Encrypt Kubernetes Secrets Using Sealed Secrets (Detailed Guide)](https://devopscube.com/sealed-secrets-kubernetes/#:~:text=Storing%20Kubernetes%20Secret%20manifest%20files,means%20anyone%20can%20decode%20them)). ArgoCD will apply them as part of sync. We have now deployed all pieces of our app in manifests.

At this stage, if you push all these YAMLs to the Git repo and let ArgoCD sync, you should have:

- `frontend-deployment` and `frontend-service` running.
- `backend-deployment` and `backend-service` running (likely crash looping until database is up, so ordering is something to consider – it may fail a few times until DB comes up).
- `mysql` StatefulSet running with a PVC and `mysql-service`.
- Once MySQL starts (which might take a bit for initial init), the Spring Boot app should eventually connect (it might retry if it fails at first – ensure the app has retry logic or you might need to deploy MySQL first, then backend).
- Ingress configured (if the controller is there) allowing external traffic.

ArgoCD will show the application as **Synced** (once everything is created) and hopefully **Healthy** (which depends on checks like readiness of deployments). You can then test by visiting the app URL.

With the app up and running, we move on to how to manage and maintain it: database concerns, CI/CD pipeline details, scaling, etc.

## 4. Database Management

Operating a database in Kubernetes requires planning for data persistence, backup, and (if high availability is needed) failover. We will address:

- Setting up MySQL with a Persistent Volume (which we did in manifest form), and verifying data survives pod restarts.
- Backup strategies for MySQL data on-prem.
- Options for failover or replication to avoid downtime if the MySQL pod or node fails.

### 4.1 Deploying MySQL with Persistent Volume Claims (PVC)

In section 3.3, we deployed MySQL with a PVC. Let’s elaborate on that:

- The **PersistentVolumeClaim** ensures that MySQL’s data directory is backed by durable storage on the cluster. If the MySQL pod is rescheduled to another node (say the original node fails or you delete the pod), the PVC can reattach to the new pod (depending on storage type). If using network storage (NFS, iSCSI, etc.), it can attach to any node. If using local hostPath, that wouldn’t survive a move to another node. Therefore, using a network storage class or some form of distributed storage is important for true persistence in multi-node cluster ([Kubernetes On-Premises: Why and How](https://platform9.com/blog/kubernetes-on-premises-why-and-how/#:~:text=5,premises)).
- We should verify that if MySQL pod restarts, the data in `/var/lib/mysql` persists (tables, etc. remain).

**Storage Class and Access Modes**: We used `ReadWriteOnce`, meaning only one node can mount that PVC at a time (which is typical for most PV types). That’s fine because we only run one MySQL pod (or even if we run a primary-replica, each would have its own PVC). Some storage (like NFS) could allow ReadWriteMany, but MySQL generally doesn’t use a shared volume between two instances (except in special HA setups).

**StatefulSet benefits**: With StatefulSet, if we scaled to 3, each replica would get its own PVC (e.g., data-mysql-0, data-mysql-1, data-mysql-2). They would each have a copy of data only from init (the official example uses init containers to copy data from master to replicas using backups ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,C%20%2Fvar%2Flib%2Fmysql)) ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=%5B%5B%20%24ordinal%20,name%3A%20data%20mountPath%3A%20%2Fvar%2Flib%2Fmysql))). But simply scaling MySQL StatefulSet to 3 without additional config will end up with 3 independent MySQL servers (not knowing about each other). That’s why additional setup is needed for replication.

For now, with one instance, **ensure the following**:

- The `mysql` container has `MYSQL_DATABASE` and other env set, so on first launch it created the DB and user. This is one-time (it doesn’t recreate if data directory already has mysql files).
- The headless service `mysql-headless` provides stable DNS name (`mysql-0.mysql-headless.fullstack-prod.svc...`) which the official chart example uses for connecting replicas to primary. In our case, not used, but if we ever add a second replica for read, we’d have to set up replication user and config.

**Verification**: You can exec into the MySQL pod and create a sample table to ensure persistence:

```bash
kubectl exec -it mysql-0 -n fullstack-prod -- mysql -u root -p$ROOT_PASSWORD myappdb
mysql> CREATE TABLE test (id INT PRIMARY KEY, name VARCHAR(50));
mysql> INSERT INTO test VALUES (1, 'foo');
mysql> SELECT * FROM test;
```

Then exit, delete the pod:

```bash
kubectl delete pod mysql-0 -n fullstack-prod
```

Kubernetes will restart the pod (StatefulSet ensures it comes back). Exec again and ensure the table `test` and data are still there, proving PVC persisted it.

### 4.2 Backups and Restore Strategies

Even with persistent volumes, you need backups in case data is corrupted or accidentally deleted (by a bug or user). On-prem, you likely don’t have a managed database service, so you must implement backups yourself. Several approaches:

- **mysqldump or mysqlsh**: You can run a Kubernetes CronJob that periodically executes `mysqldump` to dump all databases to a file, then upload that file to an external storage (like an NFS backup location, or a cloud storage, etc.). For example, a CronJob that runs daily at midnight:

  ```yaml
  apiVersion: batch/v1
  kind: CronJob
  metadata:
    name: mysql-backup
    namespace: fullstack-prod
  spec:
    schedule: "0 0 * * *"
    jobTemplate:
      spec:
        template:
          spec:
            containers:
              - name: backup
                image: mysql:8.0
                args:
                  - /bin/sh
                  - -c
                  - |
                    mysqldump -u myappuser -p$MYSQL_PASSWORD myappdb > /backup/myappdb-$(date +%F).sql
                    # (Add command to copy /backup to permanent location, e.g., aws s3 cp or scp to NAS)
                env:
                  - name: MYSQL_PASSWORD
                    valueFrom:
                      secretKeyRef:
                        name: myapp-db-secret
                        key: mysql-password
                volumeMounts:
                  - name: backup-vol
                    mountPath: /backup
            restartPolicy: OnFailure
            volumes:
              - name: backup-vol
                persistentVolumeClaim:
                  claimName: mysql-backup-pvc # A PVC for storing backups temporarily
  ```

  This is a simplified example; in practice you’d include the host, user, etc. If you have a large DB, `mysqldump` might be slow and resource intensive; you might prefer **MySQL binlog backups** or incremental backups.

- **Volume Snapshots**: If your storage class supports CSI Volume Snapshots, you can snapshot the volume periodically. For example, using Kubernetes `VolumeSnapshot` CRD and perhaps a CronJob to create snapshots. This captures the volume state (best done when DB is quiesced or with filesystem freeze – not trivial with MySQL unless you flush tables). Snapshots can be restored to new PVCs if needed.

- **External backup tooling**: Use existing solutions like **Percona XtraBackup** for MySQL (which can do hot backups). You could run a sidecar container in the MySQL pod that periodically does XtraBackup, or a separate job that uses XtraBackup to copy data files.

- **Off-site backups**: Always transfer backups off the cluster (so if the cluster dies, you have a copy). Upload dumps to a remote server or cloud storage.

We won’t implement actual backup scripts here, but the key is to schedule it and monitor it. Test restoring as well: simulate losing data and ensure you can recreate the DB from backup on a new MySQL instance.

### 4.3 Failover Mechanisms and High Availability

Running a single MySQL pod has a single point of failure: if the pod or node goes down, your app loses its DB until it’s restored. Solutions for HA:

- **MySQL Primary-Replica**: Configure MySQL replication. For example, run 1 primary and 1 or 2 replicas. Only primary handles writes, replicas can handle reads. In event of primary failure, you manually or via an orchestrator promote a replica to primary. Kubernetes doesn’t automate this natively.

  - To implement, you’d launch multiple MySQL instances. The Kubernetes example used a StatefulSet of 3 with one being “ordinal 0” as primary and others as secondaries, using an init to clone data ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=,C%20%2Fvar%2Flib%2Fmysql)). It sets super-read-only on replicas via config ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=primary.cnf%3A%20%7C%20,only)) ([Run a Replicated Stateful Application | Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-replicated-stateful-application/#:~:text=%5Bmysqld%5D%20log,only)). This is advanced – effectively writing your own MySQL cluster setup in K8s. You’d also need to redirect the backend to whichever is primary. That could be via the headless service DNS (e.g., always use `mysql-0.mysql-headless` as primary). If primary fails and is down, you’d have to manually designate a new one (unless you use something like mysql-router or an operator).
  - You might also create two services: one for primary (pointing to mysql-0), one for any (for reads).

- **MySQL InnoDB Cluster or Group Replication**: Newer MySQL versions and Oracle provide InnoDB Cluster which can do multi-primary replication with automatic failover. Running that requires running MySQL shell commands to setup the cluster. There is a tutorial for MySQL InnoDB Cluster on Kubernetes (for example, Google’s guide) ([Deploy a stateful MySQL cluster on GKE | Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/tutorials/stateful-workloads/mysql#:~:text=Deploy%20a%20stateful%20MySQL%20cluster,middleware%20on%20your%20GKE%20cluster)). That might be overkill for now, but it’s an option.

- **MySQL Operators**: There are Kubernetes Operators (controllers) that manage MySQL clustering:

  - _Percona Kubernetes Operator for MySQL_ (XtraDB Cluster, which is Galera-based multi-master).
  - _Oracle MySQL Operator_ (official, for InnoDB cluster).
  - _Vitess_ (a sharding solution for MySQL, used at large scale, but heavy).
    Using an operator can simplify deploying a highly available MySQL cluster. For example, the operator might handle spawning replicas, syncing them, performing automated failover if primary fails, etc.

- **Cold Standby**: At minimum, have a process to quickly restore from backup to a new MySQL instance if the main one fails catastrophically. Not ideal due to downtime, but a strategy if full HA is not needed or too complex.

For our use-case (a small full-stack app on-prem), a simple approach:

- Keep nightly backups.
- Possibly run a second MySQL instance as replica (so you can offload reads or at least have an up-to-date copy). If primary fails, promote the replica manually. This requires enabling binary log on primary and configuring replica with `CHANGE MASTER TO...` commands. Could be done as part of init script.

**Failover testing**: If you set up replication, test failover:

- Kill the primary pod, ensure replica can be promoted and app can switch (maybe by changing a service endpoint).
- Without automation, you'd have to change the Service to point to the new primary, etc.

Given the complexity, many prefer to use an external managed DB or an operator. But learning to do it in K8s is instructive.

**Conclusion**: For production, evaluate the level of HA needed. If downtime of a few minutes is acceptable, a single MySQL with backups might be okay (Kubernetes will restart the pod quickly on failure though, possibly within tens of seconds). If near-zero downtime, implement a redundancy mechanism.

We will proceed with the assumption of a single MySQL (with good backups) for simplicity, but the above outlines pathways to improve availability.

Now that our database considerations are addressed, let’s focus on the CI/CD aspects with ArgoCD and how to manage releases and rollbacks.

## 5. CI/CD Pipeline with ArgoCD

We’ve configured ArgoCD to deploy changes from Git automatically (Continuous Deployment). In a full CI/CD pipeline, CI (Continuous Integration) is the part that builds and tests the code, then feeds into CD. ArgoCD covers the CD portion by applying changes to the cluster. Here we discuss how to automate the entire pipeline and how to handle versioning and rollbacks.

### 5.1 Automating Deployments via GitOps

**Continuous Integration (CI)**: Use your preferred CI tool (Jenkins, GitLab CI, GitHub Actions, etc.) to build Docker images for the frontend and backend:

- When code is pushed to the main branch of the frontend repository, CI runs tests and then builds a new Docker image for the React app and pushes it to the registry.
- Same for backend repository.

After building images, the CI pipeline should update the Kubernetes manifests with the new image tags. There are a few strategies:

- **Monorepo**: If the code and manifests are in one repository, the CI can directly commit the updated Deployment YAML (with new image tag) to that same repo.
- **Separate repos**: If manifests are in a separate GitOps repo, the CI pipeline needs credentials to push to that repo. It would create a commit updating, say, `backend-deployment.yaml` to image `myapp-backend:v1.0.1`. Ideally, use a pull request and then merge to main for traceability.

Once the manifest repo is updated, ArgoCD will detect the commit and sync. Alternatively, you might configure a webhook: e.g., GitHub/GitLab webhook to ArgoCD’s endpoint (usually `https://argocd-server/api/webhook`). This will prompt ArgoCD to fetch the update immediately ([How To Setup Argo CD On Kubernetes [Beginners Guide]](https://devopscube.com/setup-argo-cd-using-helm/#:~:text=way,to%20deploy%20application%20using%20ArgoCD)). This reduces deployment latency (no waiting up to 3 minutes for poll).

**Git Commit = Single Source of Truth**: Each deployment is tied to a Git commit ID. It’s best practice to include references to application version in the commit. For example, a commit message like “Deploy backend v1.0.1, frontend v1.0.3” along with maybe tags.

**Example Workflow**:

1. Dev merges code to `main` in backend repo (version 1.0.1).
2. Jenkins builds and pushes `myapp-backend:1.0.1`.
3. Jenkins then clones the gitops repo, updates `backend-deployment.yaml` to `image: myapp-backend:1.0.1`, commits “Update backend image to v1.0.1” and pushes.
4. ArgoCD (auto-sync on) sees new commit, syncs it. Within a minute or two, Kubernetes rolling update begins for backend Deployment.
5. ArgoCD marks app synced and healthy if all is well.

We do similar for frontend (maybe separate pipeline). If the frontend and backend versions need to be coordinated, you might update both images in one commit to manifest repo (ensuring compatibility).

One can also tag the Git repo with release tags or use GitOps to promote between environments (e.g., dev branch for dev cluster, main for prod cluster, etc.)

**Handling Database Migrations**: A complete pipeline should also consider DB migrations (like running Liquibase or Flyway for the new schema before or after deploying new backend). This can be done via a Kubernetes Job or as part of app startup. Plan migration steps such that they are also triggered in the pipeline and managed via GitOps if possible.

### 5.2 Handling Rollbacks and Versioning

Despite best efforts, deployments can sometimes introduce issues that require rollback. With ArgoCD and Kubernetes, we have a few ways to revert to a known good state:

- **Git Revert/Checkout**: The pure GitOps way is to use Git to revert the change that introduced the problem. For instance, if v1.0.1 of backend is bad, revert the commit in the manifest repo that updated to v1.0.1, which effectively puts it back to v1.0.0. ArgoCD will sync and Kubernetes will perform a new rolling update back to the old image. This provides a full audit trail (the revert commit). This approach is clean but might be slower (you need to push a revert commit, wait for sync).

- **ArgoCD Rollback via History**: ArgoCD keeps a history of each sync (deployment). You can see this in the UI (App -> History). Each sync operation is identified by a revision (the Git commit ID) and an ID number. ArgoCD CLI has a command to rollback to a previous deployment state:

  ```
  argocd app rollback <APPNAME> <ID>
  ```

  If you omit ID, it rolls back to the previous revision ([argocd app rollback Command Reference - Argo CD - Read the Docs](https://argo-cd.readthedocs.io/en/latest/user-guide/commands/argocd_app_rollback/#:~:text=cd,flags%5D)). For example, `argocd app rollback fullstack-app 1` might roll back to the first deployment. This is quick and doesn't require a Git revert. However, note that when you do this, the cluster will now be out of sync with Git (because you manually changed it). ArgoCD by default will notice and either consider it OutOfSync or if auto-sync is on, it might try to “correct” it forward again. To avoid that, ArgoCD temporarily disables auto-sync on that app when a manual rollback is done (or you can disable auto-sync first) ([How do you manage rollbacks in a GitOps environment ... - Reddit](https://www.reddit.com/r/kubernetes/comments/1cjw033/how_do_you_manage_rollbacks_in_a_gitops/#:~:text=Reddit%20www,Upvote)). In practice, you’d use this if you need a rapid recovery and will later update Git to match (so eventually, commit the rollback in Git or fix the issue and redeploy).

- **kubectl rollback**: Kubernetes Deployments have a `kubectl rollout undo deployment/<name>` command which will switch to the previous ReplicaSet. If you quickly catch an error right after deploying, you could use this. But doing so would make the cluster deviate from Git, and ArgoCD would likely put it back (because ArgoCD notices the image tag in Git vs live). So this is not recommended if ArgoCD is managing it, unless you also adjust Git or pause ArgoCD.

- **Argo Rollouts**: A mention for completeness: ArgoCD’s sibling project **Argo Rollouts** allows advanced deployment strategies (blue-green, canary) and can integrate with ArgoCD. With Rollouts, you can automatically abort a rollout if health checks fail and fallback. That might be overkill here, but a consideration for minimizing manual rollbacks.

**Versioning**: Tag your Docker images with version numbers or Git SHAs, and use those in manifests (avoid `:latest` in production). This way, it’s clear what version is running. ArgoCD shows the image tag in the UI for each deployment resource.

**Git Tags/Releases**: You can configure `targetRevision` in the ArgoCD Application to follow a Git tag (e.g., “prod-v1.2”). Then to deploy a new version, you move the tag in Git to point to a new commit (which can be done in CI). Some teams prefer a promotion by updating tags instead of directly writing to certain branches.

**Testing before Prod**: Use a staging environment to test new releases (ArgoCD can manage multiple apps). For example, once CI builds a new image, it first updates the staging cluster’s manifests. If all good in staging, promote to prod (perhaps by a pull request or tag update). This reduces chances of bad deploys hitting prod.

**Rollback Example**: Suppose after deploying backend v1.0.1, we discover a bug causing errors. We decide to rollback:

- We quickly run `argocd app rollback fullstack-app 2` (assuming 2 was the previous healthy sync). This switches the deployment back to v1.0.0 within a minute. The site is back to stable.
- Then we commit a revert in Git (or fix the issue in code for v1.0.2).
- ArgoCD is set to auto-sync off during rollback (if not, we might have had to disable it). We now re-enable auto-sync and let it sync to the reverted manifest in Git, which matches what’s running.

ArgoCD makes rollbacks fairly straightforward, as long as you handle the Git state accordingly.

**Handling Database in Rollback**: One caution: if the new version ran a DB migration that changed schema, rolling back the app might be incompatible with the new schema. This is a common challenge. Solutions:

- Write backward-compatible migrations (so old app still runs).
- Or have the rollback also roll back the schema (which may not be trivial).
- The best practice is to do migrations in a separate step and have the app be tolerant to newer schema (e.g., additive changes only).

Wrap up: Use Git as your primary control for versioning deployments. Use ArgoCD’s automation to deploy, and leverage its history to rollback quickly when needed. Always follow up by reconciling the Git state. Regularly prune old ReplicaSets and images to avoid resource bloat (Kubernetes keeps old ReplicaSets unless you set revisionHistoryLimit).

Now that CI/CD and deployments are managed, we focus on scaling and optimizing performance of our app in the cluster.

## 6. Scaling and Performance Optimization

One advantage of Kubernetes is easy scaling of applications. We will ensure our application can scale to meet demand. Additionally, we want to optimize resource usage so that we aren't over-provisioning or under-provisioning resources. This section covers:

- Horizontal scaling of pods (adding more replicas under load).
- Vertical scaling (adjusting CPU/memory for pods).
- Optimizing resource requests/limits and cluster node usage.

### 6.1 Horizontal Pod Scaling (Autoscaling)

**Horizontal Pod Autoscaler (HPA)**: Kubernetes can automatically scale the number of pod replicas based on metrics like CPU utilization or custom metrics. For our stateless components (frontend and backend), HPA is appropriate. MySQL (stateful) typically is not auto-scaled (scaling DBs is manual due to data consistency issues).

We likely want to scale the Spring Boot backend based on CPU or request load, since that is the component doing most processing. The React frontend (NGINX serving static files) can also be scaled if there's extremely high traffic, but often NGINX can handle a lot per pod. Still, we can set up HPA for it too if needed.

**Metrics Server**: Ensure the cluster has the Metrics Server installed (for CPU/memory metrics). Many Kubernetes installs include it; if not, you can install via the official YAML.

Let’s configure an HPA for the backend:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: fullstack-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

This HPA means:

- Target the backend Deployment.
- Keep at least 2 pods (so even at idle we don't go below 2).
- Up to 10 pods max.
- Metric: if average CPU utilization across pods goes above 50%, the HPA will add pods. It tries to maintain 50% CPU usage. For instance, if each pod requests 200m CPU, 50% of that is 100m. So if each pod is using >100m on average, add more pods.

We used the autoscaling/v2 API which allows multiple metrics and custom ones, but here just CPU. We could also target memory or custom app metrics (like requests per second if integrated with Prometheus adapter).

For frontend, we can have a similar HPA:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: fullstack-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend-deployment
  minReplicas: 2
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 20
```

Maybe a lower CPU target since NGINX should be mostly idle until heavy load. If each uses very little CPU, HPA might never need to scale beyond 2.

**Test HPA**: You can simulate load to see scaling. For CPU, use a load testing tool hitting the backend and watch `kubectl get hpa -w`. The HPA fetches metrics from Metrics Server (which scrapes the kubelet). If it decides to scale, it will change the Deployment's replica count accordingly ([HorizontalPodAutoscaler Walkthrough | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#:~:text=Horizontal%20scaling%20means%20that%20the,already%20running%20for%20the%20workload)) ([HorizontalPodAutoscaler Walkthrough | Kubernetes](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#:~:text=If%20the%20load%20decreases%2C%20and,to%20scale%20back%20down)). Ensure that your app can handle being scaled (it’s stateless, so should be fine; Spring Boot might need sticky sessions if it had session state, but likely stateless API).

**Cluster Node Scaling**: Horizontal scaling at pod level is good, but if all nodes become full, you may need to add nodes. On cloud, Cluster Autoscaler can automate adding VMs. On-prem, you might integrate with virtualization or do it manually. For example, if using VMware, you could have a script to clone a new VM and join the cluster with kubeadm join. Tools like **Cluster API** or **kubeadm automation** could help. Alternatively, ensure you have enough nodes to handle your max load in advance.

### 6.2 Vertical Scaling (Resource Optimization)

**Vertical Pod Autoscaler (VPA)**: This is a component that can suggest or even automatically adjust the requests/limits of pods based on observed usage. It’s not as commonly in full use (because if it auto-adjusts a running pod’s requests, it often needs to restart the pod). Many use it in recommendation mode. Given complexity, we might skip deploying VPA, but you should periodically review resource usage.

**Monitor and Adjust**:

- Use monitoring (Prometheus, see next section) to see how much CPU and memory each component uses over time.
- If you see that the backend never uses more than 100m CPU but you requested 200m each, you might lower the request to 100m to pack pods more tightly.
- If you see it often hits the limit 500m and gets throttled, maybe increase limit or add more pods via HPA.
- Memory: ensure memory usage is below requests to avoid OOMKills.

For MySQL, vertical scaling means perhaps allocating more memory for innodb buffer pool or more CPU if needed. That’s done by changing the resource limits in its manifest and maybe MySQL configs. You can also scale MySQL vertically by moving it to a node with more resources (if your cluster has heterogeneous nodes or if you label a node for database and schedule it there with nodeSelector, etc.).

**Resource Requests/limits best practice**:

- Set requests equal to a bit above average usage to ensure scheduler knows how to bin-pack.
- Set limits to a safe max that the app can handle. For CPU, going above request just means best-effort usage (no harm except potentially affecting others). For memory, going above limit triggers OOM kill of the container, so avoid too low memory limit.
- Do not set no limits at all in production, as a runaway process could consume all node memory.

**Scaling the Cluster**:

- If your app grows, monitor the node usage. If CPU on nodes is >80% or memory >80% consistently, it might be time to add another node to avoid saturation.
- On-prem, possibly have some spare nodes that can join quickly (or run more VMs).
- If using a cloud bursting approach, maybe integrate with an autoscaler to get VMs from cloud when needed (advanced hybrid model).

### 6.3 Optimizing Resource Utilization

Beyond scaling, some performance optimizations:

- **Load Balancing**: The Kubernetes Services distribute traffic among pods. Ensure the service uses a suitable session affinity if needed (by default it’s random/round-robin). For our stateless services, default is fine.
- **Connection pooling**: The backend should pool DB connections to avoid overhead. Also the DB max connections should be tuned to handle multiple pods. For example, if each Spring Boot pod opens 10 connections in pool and we scale to 10 pods, that’s 100 connections; ensure MySQL `max_connections` is above that. Adjust MySQL config via ConfigMap if needed.
- **Threading**: Spring Boot by default might use a fixed thread pool for requests; ensure it’s sized well for CPU cores available. If CPU is high and threads are saturated, more pods (horizontal scaling) helps more than vertical in many cases due to Java and GC scaling.
- **Caching**: Implement caching at the app level if appropriate to reduce DB hits. E.g., if some data is frequently read, caching in memory or using Redis (could deploy that in cluster).
- **Front-end optimization**: Serve static content compressed (NGINX can handle gzip). Use a CDN if possible for front-end assets (though on-prem cluster might not easily integrate a CDN, but if some parts can be moved to a static file server outside).
- **Limits vs throughput**: experiment with different resource settings to see how throughput changes. For example, giving the backend more CPU (limit) might increase throughput per pod up to a point.

One can use tools like **Kubernetes resource recommendations (Goldilocks)** which runs VPA in recommend mode to suggest better requests/limits based on historical usage.

Finally, ensure to remove unused resources (old ReplicaSets left behind if any, Completed Jobs, etc.) to free up overhead.

With scaling and resources optimized, we ensure the app runs efficiently. Next, we cover monitoring and logging to observe these metrics and debug if issues arise.

## 7. Monitoring and Logging

Running an application in production requires visibility into its performance and behavior. We need to monitor metrics (CPU, memory, response times, etc.) and gather logs from all components. In a Kubernetes environment, this typically involves a combination of **Prometheus & Grafana** for metrics, and an **EFK (Elasticsearch-Fluentd-Kibana)** stack for logs. We will discuss setting those up and best practices.

### 7.1 Monitoring with Prometheus and Grafana

**Prometheus** is a popular open-source monitoring system and time-series database. It will scrape metrics from our cluster and applications. **Grafana** is a dashboard tool to visualize those metrics.

**Deploying Prometheus**: The easiest way is to use the **kube-prometheus-stack** Helm chart (which includes Prometheus, Grafana, Alertmanager, etc.). Alternatively, use the Prometheus Operator which provides CRDs to configure Prometheus. For a simpler approach, we can deploy Prometheus and Grafana separately:

- **Prometheus**: deploy a Deployment or StatefulSet for Prometheus server, along with a Service and ConfigMap for its configuration (including scrape targets).
- **Grafana**: deploy a Deployment for Grafana, a Service, and possibly an Ingress to view it.

Using Helm (if allowed in your ops process) would be:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

This installs a whole suite (Prometheus, Grafana, node-exporter, kube-state-metrics, etc.) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=As%20a%20next%20step%2C%20you,stack%20on%20the%20Kubeadm%20cluster)) ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=I%20have%20published%20a%20detailed,kube%20state%20metrics%20and%20Grafana)).

For understanding, let's highlight what we need:

- **Node Exporter**: runs on each node to provide node-level metrics (CPU, mem, disk usage).
- **Kube-State-Metrics**: a service that converts Kubernetes API state into metrics (e.g., number of pods, deployment replicas, etc.).
- Prometheus server configured to scrape:

  - Kubernetes components (cAdvisor and kubelet for container metrics, API server metrics, etc.).
  - Node exporter and kube-state-metrics.
  - ArgoCD metrics (ArgoCD provides some if we want to monitor sync status).
  - **Application metrics**: If we want application-specific metrics (like HTTP request rate, error rate), we need the app to expose metrics. Spring Boot can expose Actuator metrics (Prometheus format) at `/actuator/prometheus` if enabled. We could configure Prometheus to scrape the backend-service on that path. Similarly, for NGINX, we could export metrics if needed via an exporter.

- **Grafana**: can be configured with dashboards. The kube-prometheus-stack provides many pre-built dashboards for cluster monitoring (CPU usage per node, etc., out-of-box).

If not using helm, you can apply the manifests from the kube-prometheus project (which is maintained by Prometheus Operator).

**After deployment**:

- You might port-forward Grafana (default service might be ClusterIP). Or expose via ingress to view graphs.
- Import some dashboards: for example, a JVM dashboard for Spring Boot (to see GC, threads, etc.), a MySQL dashboard (if you install mysqld exporter).
- Set up alerts in Prometheus/Alertmanager: e.g., alert if CPU > 90% for 5m, if HTTP error rate spiking, etc. The stack usually includes some default alerts.

**Resource impact**: Monitoring stack itself consumes resources, so allocate perhaps a couple of CPUs and a few GB of RAM for Prometheus, etc., depending on retention and scrape frequency.

### 7.2 Aggregating Logs with EFK Stack (Elasticsearch, Fluentd, Kibana)

Collecting logs from all pods in a central system makes debugging easier. The **EFK** stack is a common solution:

- **Fluentd**: an agent that runs on each node (DaemonSet) to collect logs. It can read logs from the container runtime (e.g., Docker or containerd log files) and forward them to Elasticsearch (after filtering/tagging).
- **Elasticsearch**: a search engine/data store that stores logs and allows querying them.
- **Kibana**: a web UI for Elasticsearch, to visualize and search logs.

**Deployment**:

- Create a namespace (e.g., `kube-logging`).
- Deploy Elasticsearch. Often as a StatefulSet with 2-3 replicas (for HA) and PVCs for storing indices. The DigitalOcean tutorial deploys 3 Pods for ES ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=,in%20the%20official%20documentation)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=stack%2C%20and%20if%20not%20scale,in%20the%20official%20documentation)). If resource is a concern, you might start with 1 or 2 nodes of ES (but then HA is compromised).
- Deploy Kibana (one Deployment, no persistence needed, just connects to ES).
- Deploy Fluentd as a DaemonSet on all worker nodes. Fluentd needs permissions to read logs from the host filesystem and to send to ES.

From the DO tutorial:

- They create `kube-logging` namespace ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=Step%201%20%E2%80%94%20Creating%20a,Namespace)).
- They deploy an ES StatefulSet with a headless service, set memory limits, etc. (We saw volumeMounts for data in that tutorial ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=apiVersion%3A%20apps%2Fv1%20kind%3A%20StatefulSet%20metadata%3A,cluster)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=match%20at%20L926%20apiVersion%3A%20apps%2Fv1,kind%3A%20Deployment%20metadata%3A%20name%3A%20kibana))).
- Kibana Deployment listening on port (usually 5601).
- Fluentd DaemonSet with config via ConfigMap (pointing FLUENT_ELASTICSEARCH_HOST to the ES service).
- Fluentd also had a ServiceAccount and ClusterRole to read Kubernetes metadata (to enrich logs with pod labels) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=rules%3A%20,list)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=kind%3A%20ClusterRoleBinding%20apiVersion%3A%20rbac,io%20subjects)). We saw that in the DO snippet.

Important bits for Fluentd:

- Mount `/var/log/` and `/var/lib/docker/containers` (for Docker, or for containerd, often `/var/log/pods` and `/var/log/containers`) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=,name%3A%20varlibdockercontainers%20hostPath%3A%20path%3A%20%2Fvar%2Flib%2Fdocker%2Fcontainers)) ([How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes#:~:text=Next%2C%20we%20mount%20the%20,the%20end%20of%20the%20block)). In DO's YAML, they did hostPath mounts for those and gave Fluentd read access.
- Use appropriate Fluentd config to tail files from those directories (the standard fluentd-kubernetes image has this logic).

**Alternatively**:

- **Fluent Bit**: a lighter weight log forwarder (C-based). You can use that similarly as DaemonSet sending to ES or even directly to a SaaS logging service.
- **Elastic Cloud**: Instead of running Elasticsearch on-prem (which can be resource heavy and require maintenance), some choose to send logs to a cloud service (Elastic Cloud, Loggly, etc.). But since this is on-prem scenario, presumably we keep it local.

**Kibana**: Once up, you configure index patterns (like `logstash-*` if using logstash prefix, or fluentd default). Then you can search logs. For example, filter by `kubernetes.pod_name:"backend-deployment-abc123"` to see backend logs, or by namespace, etc. Fluentd often attaches fields like `kubernetes.labels.app` which we can use (so you can search logs for app: myapp-backend to get all pods of that deployment).

Set retention policy on Elasticsearch (to not consume infinite disk - e.g., keep 7 days of logs, or use ILM policies in ES).

**Logging best practices**:

- Use structured logging in apps (JSON) if possible for easier parsing. Fluentd can parse JSON logs into fields.
- Avoid too verbose logs in production (set appropriate log levels) to control volume.
- Monitor the Fluentd resource usage – if it's high, consider filtering out logs you don’t need, or sample them.
- Secure the logging stack (at least internal-only, or put basic auth on Kibana if exposing it).

### 7.3 Metrics and Log Dashboards

Once metrics and logs are flowing:

- Create Grafana dashboards for key metrics. For example:
  - **Infrastructure Dashboard**: CPU/Memory usage per node, pod counts, etc. (the kube-prometheus has these).
  - **Application Dashboard**: e.g., use Spring Boot's Micrometer metrics. If Actuator is on, you get metrics like http_server_requests (count of API calls, response times, etc.), jvm_memory_used, etc. Create graphs for request rate, error rate, response time p95, DB connection count, GC times, etc.
  - **Database Dashboard**: If you deploy a MySQL exporter (there is a mysqld_exporter container you could run as a sidecar or as a separate deployment pointing to MySQL), you can get DB stats (queries per second, buffer pool usage, etc.). Or at least monitor MySQL container resource usage from cAdvisor metrics.
- Set up **Alerts**: Possibly the kube-prom-stack includes some, but you might add:
  - Alert if HTTP 5xx errors exceed threshold (if you push a custom metric or if using something like Istio or ingress metrics).
  - Alert if MySQL down (no scrape or using liveness).
  - Alert if disk space on nodes for PVs running low.
  - ArgoCD health alerts if sync fails (ArgoCD can integrate with notifications, they have ArgoCD Notifications component that can send Slack messages on failures).

All these ensure you can detect problems early and have the data to diagnose them.

We have now instrumented our app and cluster for observability.

Finally, we address remaining security best practices and then debugging tips.

## 8. Security Best Practices

Security is a broad topic, but we will focus on a few key areas relevant to our on-prem Kubernetes deployment:

- Enabling TLS for application traffic and possibly internal components.
- Implementing network isolation and least privilege (Network Policies, Pod Security).
- Image and dependency vulnerability scanning and general hardening.

### 8.1 Configuring TLS and Cert-Manager

For any externally exposed service (like our Ingress at myapp.example.com, or ArgoCD UI), use **TLS encryption**. We don’t want to serve over plain HTTP in production.

**cert-manager** is a Kubernetes add-on that automates obtaining and renewing TLS certificates, often from Let’s Encrypt or internal CAs:

- Install cert-manager in the cluster (it’s a deployment plus CRDs for Certificate, Issuer, etc.). Typically: `kubectl apply -f https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml` to install it.
- Create an **Issuer** or **ClusterIssuer** for Let’s Encrypt. For example, a ClusterIssuer for LE Staging (for testing) and then one for production:

  ```yaml
  apiVersion: cert-manager.io/v1
  kind: ClusterIssuer
  metadata:
    name: letsencrypt-prod
  spec:
    acme:
      server: https://acme-v02.api.letsencrypt.org/directory
      email: ops@mycompany.com
      privateKeySecretRef:
        name: acme-account-key
      solvers:
        - http01:
            ingress:
              class: nginx
  ```

  This configures ACME HTTP-01 challenge using our ingress controller.

- Then, request a Certificate for `myapp.example.com`:

  ```yaml
  apiVersion: cert-manager.io/v1
  kind: Certificate
  metadata:
    name: myapp-tls
    namespace: fullstack-prod
  spec:
    secretName: myapp-tls-secret
    issuerRef:
      name: letsencrypt-prod
      kind: ClusterIssuer
    commonName: myapp.example.com
    dnsNames:
      - myapp.example.com
  ```

  Cert-manager will create `myapp-tls-secret` with the TLS key and cert if the ACME challenge succeeds.

- Update the Ingress to use TLS:

  ```yaml
  spec:
    tls:
      - hosts:
          - myapp.example.com
        secretName: myapp-tls-secret
  ```

  Remove any `rewrite-target` that might interfere with ACME challenge path, or ensure `cert-manager` adds an appropriate challenge ingress (it usually does).

- For ArgoCD server (if exposing via ingress), you can similarly create a certificate.

Alternatively, if not using cert-manager, at least use a self-signed cert or manually provide certs for TLS. But cert-manager greatly eases automation.

Also ensure internal communication can be TLS if needed:

- By default, Kubernetes API communication is TLS.
- If you have services that talk to each other within cluster, it's often over cluster network (which might be considered secure if within same trusted network). If zero-trust needed, consider service mesh with mTLS (Istio or Linkerd).
- For database: currently our Spring Boot communicates with MySQL over plain TCP within cluster. If worried, one could set up MySQL with SSL and use TLS connection.

### 8.2 Implementing Network Policies and Pod Security Policies

**Network Policies**: By default, all pods in a cluster can talk to each other (within network). For better security (defense in depth), we can restrict allowed connections using NetworkPolicy objects. Note: Your CNI plugin (Calico, etc.) must support network policy (Calico does ([How To Setup Kubernetes Cluster Using Kubeadm - Easy Guide](https://devopscube.com/setup-kubernetes-cluster-kubeadm/#:~:text=Kubeadm%20does%20not%20configure%20any,networking%20and%20enable%20network%20policy))).

For example, to ensure only the backend pods can talk to MySQL, and nothing else in the cluster can:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-access-policy
  namespace: fullstack-prod
spec:
  podSelector:
    matchLabels:
      app: myapp-mysql
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: myapp-backend
      ports:
        - protocol: TCP
          port: 3306
```

This says: for pods labeled app: myapp-mysql, only allow ingress from pods labeled app: myapp-backend on TCP 3306. All other ingress to MySQL is blocked. Outgoing (from MySQL) is not restricted here.

We might also restrict backend to only receive traffic from frontend or ingress:

```yaml
kind: NetworkPolicy
metadata:
  name: backend-access
  namespace: fullstack-prod
spec:
  podSelector:
    matchLabels:
      app: myapp-backend
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: myapp-frontend
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
  ports:
    - protocol: TCP
      port: 8080
```

This example allows backend to get traffic from pods with app: myapp-frontend (if the front end calls it directly, not likely) and from ingress-nginx namespace (the ingress controller pods). That covers user traffic via ingress. So random other pods cannot call the backend API.

We can similarly lock down the frontend to only get traffic from ingress controller (or none at all if it's only via ingress).

Additionally, one often implements a **default deny** policy in each namespace to isolate by default ([Security Checklist | Kubernetes](https://kubernetes.io/docs/concepts/security/security-checklist/#:~:text=%2A%20CNI%20plugins%20in,namespace%2C%20selecting%20all%20pods%2C%20denying)) ([Security Checklist | Kubernetes](https://kubernetes.io/docs/concepts/security/security-checklist/#:~:text=is%20most%20commonly%20done%20through,that%20no%20workloads%20is%20missed)). For example, an NP with podSelector={} (all pods) and no from, policyTypes Ingress, which means deny all ingress unless allowed by another policy.

**Pod Security**: Kubernetes used to have PodSecurityPolicies (PSP) to restrict pod specs (like no privileged containers, no host mounts, etc.). PSP is deprecated now, replaced by **Pod Security Admission** based on Pod Security Standards (PSS). This can be enabled by configuring the admission controller to enforce `baseline` or `restricted` policies on the namespace. On newer clusters (1.24+), you can label namespaces with `pod-security.kubernetes.io/enforce: baseline` (or restricted) to enforce those standards.

- _Restricted_ policy ensures:
  - No running as root (unless explicitly allowed).
  - No privilege escalation.
  - Only specific volume types (no hostPath).
  - Applies seccomp, etc., by default.
- _Baseline_ is a bit more lenient.

It's good to enforce at least baseline cluster-wide, and restricted for sensitive workloads.

**RBAC for Kube API**: We covered RBAC earlier for user permissions. Make sure no one has cluster-admin unless necessary. Create specific roles for CI or ArgoCD if needed. ArgoCD for example by default runs with cluster-admin in its namespace (the install manifest created clusterroles). If security requirements are tight, you might scope ArgoCD's permissions to only certain namespaces, etc.

**Container Security Context**:

- Ensure images run as non-root user when possible. For example, our MySQL image runs as mysql user by default (I think). Nginx can be configured to run as non-root (www-data). Spring Boot we can build the image to use a non-root UID.
- Set `readOnlyRootFilesystem: true` for containers that don't need to write in container FS (likely for frontend).
- Set `runAsUser` and `runAsGroup` in Pod securityContext if needed to ensure correct UID.
- Drop unnecessary Linux capabilities (e.g., no need for NET_ADMIN, etc. in most app containers).
- Use seccomp profiles if possible (like docker default or a hardened one).
- These can often be auto-enforced if using restricted PodSecurity standard.

**Image Vulnerability Scanning**:

- Use tools like **Trivy** or **Clair** to scan your container images for known vulnerabilities (CVEs) in OS packages or libraries. This can be integrated in the CI pipeline. For example, run `trivy image myapp-backend:1.0.0` after build, and fail the build if severe vulns are found.
- Keep base images updated (e.g., update the Node or OpenJDK base periodically to get security fixes).

**Dependency scanning**:

- Also scan application dependencies (e.g., use OWASP Dependency Check or Snyk) to catch vulnerable libs in your Maven or NPM packages.

**Regular Updates**:

- Update Kubernetes itself for patches (on-prem requires manual upgrades).
- Update third-party apps (ArgoCD, Prometheus, etc.) regularly for security fixes.

**Access Controls**:

- Limit access to the ArgoCD UI (don't expose to world, or secure with auth).
- If you have a Kubernetes Dashboard, secure it or don’t install it (it has had vulnerabilities).
- Use unique strong passwords for database users, etc., which we did via secrets.

By following these practices, we significantly harden the deployment:

- TLS encryption ensures data privacy in transit ([Securing Your Kubernetes Cluster - Palo Alto Networks](https://www.paloaltonetworks.com/cyberpedia/kubernetes-cluster-security#:~:text=Networks%20www,are%20encrypted%2C%20protecting%20against)).
- Network policies enforce a zero-trust network model within cluster (only allow needed communication) ([Security Checklist | Kubernetes](https://kubernetes.io/docs/concepts/security/security-checklist/#:~:text=%2A%20CNI%20plugins%20in,namespace%2C%20selecting%20all%20pods%2C%20denying)).
- Pod security prevents container breakout or misuse of privileges.
- Scanning reduces risk of running vulnerable images.
- RBAC ensures an attacker who gets into one component can't easily escalate to others.

Security is an ongoing process; periodically review and test (e.g., run **Pen tests** or use tools like Kube-bench for config checks, Kube-hunter for cluster vuln scan, etc.). Also ensure backup of critical data (we did for MySQL) in case of ransomware or deletion.

With security covered, the last section is about testing and debugging: how to troubleshoot issues in this Kubernetes setup.

## 9. Testing and Debugging in Kubernetes

Deploying on Kubernetes introduces new challenges in debugging compared to a single VM deployment. In this section, we discuss:

- Common deployment issues and how to resolve them.
- Tools and commands (`kubectl` etc.) for debugging pods and services.
- Tips for diagnosing issues in our React/Spring/MySQL stack specifically.

### 9.1 Troubleshooting Common Deployment Issues

**Issue: Pod is in CrashLoopBackOff**  
This means a pod starts, then crashes, and Kubernetes is restarting it in a loop ([Kubernetes CrashLoopBackOff: What it is, and how to fix it? - Sysdig](https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/#:~:text=Sysdig%20sysdig,the%20logs%20%E2%80%93%20kubectl)). Likely causes:

- Application error on startup (e.g., missing config, throwing exception, etc.).
- For MySQL, it could be failing to initialize (bad config or no permission to write to volume).
- Out of memory: if container OOMs immediately.

**How to debug**:

1. Check pod **Events** and **Description**:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```
   Look at the "Last State: Terminated" and "Exit Code". If exit code is, say, 1 or 2, it's app-specific. If 137, that's OOM killed.
   Also events might show "Back-off restarting failed container" which is typical in CrashLoopBackOff ([Kubernetes CrashLoopBackOff: What it is, and how to fix it? - Sysdig](https://sysdig.com/blog/debug-kubernetes-crashloopbackoff/#:~:text=Sysdig%20sysdig,the%20logs%20%E2%80%93%20kubectl)).
2. Check **Logs**:
   ```bash
   kubectl logs <pod-name> -n <ns> --previous
   ```
   Since it's restarting, `--previous` gives logs from the last failed instance. Often the stack trace or error is there. For example, Spring Boot might log "Unable to connect to database" or NGINX might log a config error.
3. If logs aren't helpful (e.g., crash happens too early), consider running the container image locally with a different command (or using an ephemeral debug container).
   Or add a slight `command: ["sleep", "3600"]` to the deployment to keep container alive, then `kubectl exec` into it and manually run the app binary to see output.

Common root causes and fixes:

- **Wrong env vars / config**: E.g., Spring Boot can't find DB host (maybe secret not mounted or wrong name). Fix config and redeploy.
- **DB not ready**: If backend starts before MySQL, it might fail to connect and crash (depending on how the app handles it). A solution is to add a startup retry or initContainer to wait. Or just let CrashLoop be okay for a minute until DB comes up (the pod will eventually start when DB is up if it keeps trying).
- **OutOfMemory**: If logs show OOMKill, increase memory limits.
- **Permission denied**: If logs show can't write to filesystem, maybe the pod is running as non-root and lacks permission on a mounted volume. Adjust securityContext fsGroup or such so it can write.
- **Image pull error**: If CrashLoop never had chance to run, maybe the container image isn't pulling (then status would be ImagePullBackOff rather than CrashLoop). Do `kubectl describe pod` to see events like "Failed to pull image". If so, check image name, registry credentials (if private registry, secret for imagePullSecrets).
- **Application exception**: If a bug in code causes immediate crash (NPE, etc.), you'll see it in logs. That may require code fix and new image build.

**Issue: Pod stuck in Pending**  
Meaning it cannot be scheduled onto a node. Possible causes:

- Not enough resources in cluster (no node has the free CPU/mem as per requests). You'd see events like "0/3 nodes are available: Insufficient cpu". Solution: add more nodes or reduce requests.
- PVC not bound (if it's waiting for storage). If storageclass not found or no PV available, the pod will wait until PVC is bound. Check `kubectl get pvc` status.
- Node selector / taints: If your pod has nodeSelector or tolerations that don't match any node, it won't schedule. Check pod spec and node labels.
- For StatefulSet, sometimes if one replica is still terminating, the next won't schedule (since it goes in order). Check if previous pod deletion is stuck.

**Issue: Service not reachable**  
Say backend or frontend isn't accessible via service:

- Check if pods are **Ready**. If readiness probe fails, pod is not added to service endpoints. `kubectl get endpoints backend-service` and see if any IP listed. If empty, likely pods not ready. Fix readiness probe or underlying cause.
- If endpoints exist, but you can't cURL from inside cluster, maybe a network policy is blocking traffic. Ensure no overly restrictive NetworkPolicy is in place (or test by temporarily allowing all).
- If accessing from outside via Ingress and not working:
  - Check Ingress with `kubectl describe ingress myapp-ingress`. See if rules are correct and if ingress controller has picked it up (events might show if ingress controller created config or any error).
  - If using host network, ensure DNS is correct to point to ingress.
  - If TLS, ensure certificate is issued (check secret exists, and `kubectl describe certificate` to see status).
  - Check ingress controller logs (e.g., `kubectl logs <ingress-controller-pod>`).

**Issue: High latency or errors**

- Check logs for errors in backend (stack traces for 500 errors).
- Use `kubectl top pods` (if Metrics Server installed) to see if CPU is maxed out or memory. If backend CPU 100%, might be overloaded -> scale up via HPA.
- If MySQL is slow, check if it's CPU bound or hitting disk limits.
- Use Grafana to see request rates, latencies if metrics are available.

**Issue: ArgoCD sync fails**  
ArgoCD might show app in error if, say, a manifest is invalid or apply failed. ArgoCD logs (argocd-server or controller) will have details. Common problems:

- If manifest uses CRD that isn't installed yet, ArgoCD will error. Make sure to apply CRDs first (ArgoCD has hooks or use app-of-apps).
- If you used secrets encrypted with SealedSecrets but didn't install SealedSecrets controller, the secret won't materialize (so dependent pods might fail).
- In ArgoCD UI, you can see the event or message for resource that failed. Fix the manifest accordingly.

### 9.2 Debugging Tools and Techniques

**kubectl logs**: Already mentioned. Use `-f` to follow logs in real time (good for watching startup, or tailing a running app log). If a pod has multiple containers, use `-c containerName` to specify which container's log.

**kubectl exec**: Useful to get a shell in a running container:

```bash
kubectl exec -it <pod> -n <ns> -- /bin/sh
```

If the container image has a shell. For Ubuntu-based images, maybe use `bash`. Once inside:

- You can run CLI tools (like `curl` to test connectivity, `env` to see env vars, etc.).
- For MySQL, we did `mysql` CLI as shown earlier.
- Check filesystem, config files, etc.

**kubectl port-forward**: When you want to test a service from your local machine without exposing it:

```bash
kubectl port-forward svc/backend-service -n fullstack-prod 8080:8080
```

Now hitting http://localhost:8080 from your PC will forward to the backend service in cluster. Useful for testing the API with Postman or browser.

**kubectl describe**: Great for any resource:

- `kubectl describe pod/foo` to see events (especially good for scheduling issues or termination reasons).
- `kubectl describe deployment/foo` to see rollout history and events.
- `kubectl describe node/bar` if suspect node issues (like disk pressure, which appears as Node conditions or taints).
- `kubectl get events --sort-by=.metadata.creationTimestamp` to see recent events cluster-wide.

**Ephemeral Debug Container**: Newer Kubernetes allows adding a debug container to a running pod (without modifying the pod spec permanently). `kubectl debug -it pod/<name> -n <ns> --image=busybox` will attach a busybox container to that pod’s namespace so you can explore things like networking from within the same network namespace. This is useful if the main container image lacks debugging tools.

**Kubernetes Dashboard / Lens**: There are GUI tools (Kubernetes Dashboard, or Lens IDE) that can help visualize and sometimes show errors more clearly, but everything can be done via CLI as well.

**Logs and Monitoring**: Use Kibana to see if any error logs coincide with issues. Use Prometheus/Grafana to check resource usage trends when an issue occurred (e.g., did CPU spike at the time of error).

**Common Pitfalls**:

- YAML indentation errors or incorrect field names can cause resources not to apply. If `kubectl apply` via ArgoCD fails, it usually reports error. Use `kubectl apply -f file.yaml` manually while debugging to see if the manifest is accepted.
- Always check that the pods have the expected image (maybe your CI failed to push new image and you're still running old code? `kubectl describe pod` and see image ID).
- Service mislabeling: If Service selector doesn't match Deployment labels exactly, service will have 0 endpoints. Ensure consistency.
- If two containers need to communicate, ensure they're in same namespace or correct DNS name (service names are per namespace unless you use `<svc>.<ns>.svc.cluster.local`).
- ConfigMap updates: If you update a ConfigMap, pods won't automatically restart. If the config is critical, you might need to roll pods (or use `kubectl rollout restart deployment`).
- Graceful shutdown: By default, Kubernetes gives 30s grace (we set for MySQL). For backend, ensure it can shut down within terminationGracePeriod, otherwise it might be killed before finishing cleanup (could cause minor issues like incomplete requests).

### 9.3 Example Debugging Scenario

Let's walk through a hypothetical scenario:
**Scenario**: After deployment, the frontend loads but shows "Loading..." forever and no data.

**Step 1: Check the Browser Console** – it might show an error calling `/api/data`. So likely the frontend couldn't reach backend.

**Step 2: Check Ingress** – Possibly our ingress rules are wrong. If we used path `/api(/|$)(.*)` with rewrite, maybe it stripped /api. The backend might be expecting /api in the path. Or CORS issue if the request actually went to a different domain. Maybe the frontend is trying to call `http://localhost:8080/api` because of an incorrect config (like if React app was built with a proxy for dev and not configured for prod).

We then realize the React app needs the base URL for API. If we didn't supply it, maybe it's defaulting to same host (which is fine, it would call myapp.example.com/api). If our ingress is correct, it should route.

**Step 3: Check Backend logs** – `kubectl logs backend-pod`. Do we see any request logs? If using actuator metrics, see if any request came in. If not, perhaps the traffic never hit backend.

**Step 4: Test internal connectivity** – `kubectl exec -it <frontend-pod> -- curl -v backend-service:8080/api/health`. Does that return anything? If that fails (e.g., could not resolve host), maybe DNS issue or service name wrong. If it times out, maybe network policy blocked it. But we expected ingress to call backend, not frontend, so this might not simulate the real flow (since frontend isn't server-side calling backend; it's user's browser calling via ingress).

Better: port-forward to ingress controller and simulate an external call:
Actually easier: Do `curl -H "Host: myapp.example.com" http://<ingress-controller-ip>/api/whatever`. If you get a response from backend, ingress is working. If not, check ingress controller logs – maybe it doesn’t know about the host (DNS or Ingress not applied properly).

**Step 5: Identify fix** – Suppose we find that the ingress rewrite caused issues. We change `path: /api` with `pathType: Prefix` and remove the rewrite annotation so that backend gets "/api/..." in path as it expects. Apply the updated ingress. ArgoCD syncs it. Test again, now it works.

Alternatively, if it was a CORS issue (browser blocked call to different host/port), we could configure the backend to allow the frontend origin or adjust the architecture to avoid cross-origin calls by using same domain.

**Another scenario**: Spring Boot fails to start due to "Unknown database 'myappdb'". That might mean MySQL didn't create the DB (maybe the env var `MYSQL_DATABASE` was not set correctly, maybe because secret had wrong key). Check MySQL logs: `kubectl logs mysql-0` – if it shows database created. If not, maybe the secret key was wrong (case sensitive). Fix secret or simply exec into MySQL and create the DB manually to get past it, then fix root cause for future.

**Memory leak scenario**: If over time backend memory grows and eventually pods OOM, check if there's a memory leak in app (monitor via Grafana, heap usage if available). If yes, you might need to increase memory or fix the leak. As a quick fix, you could schedule nightly pod restarts (not ideal, but a short-term mitigation) or limit throughput.

### 9.4 Continuous Testing

- Do some load testing after deployment (using tools like JMeter or k6) to see if autoscaling works, and no container crashes under load.
- Test failure scenarios: kill a pod and see if service is uninterrupted (should be, due to multiple replicas). Drain a node (simulate maintenance) with `kubectl drain` and see if pods relocate properly (if not, maybe PVC tied to that node if local storage).
- Test backup restore: try restoring a backup dump on a test database to ensure the process works.

By systematically addressing issues and using the Kubernetes debugging arsenal, you can resolve most problems. The key is to use the declarative nature: often, you'll fix something by editing a YAML and reapplying (GitOps via commit). Strive to make one change at a time and observe results.

---

**Conclusion**: We covered the full journey of deploying a React/Spring Boot/MySQL app on an on-prem Kubernetes cluster with CI/CD using ArgoCD. We set up the cluster, installed ArgoCD for GitOps, created manifests for each component, ensured the database is persisted and backed up, implemented an automated pipeline and rollback strategy, scaled the app for performance, put in place monitoring and logging for observability, applied security best practices at multiple layers, and reviewed debugging techniques for maintenance.

By following this guide, a technical professional should be able to reproduce a robust deployment environment for a similar full-stack application and operate it effectively. Each section ensures that not only is the app running, but it is scalable, secure, and maintainable. Always keep documentation of your specific configuration and changes, and continuously update your manifests in Git as the source of truth for your system. With GitOps, any change is recorded and can be rolled back, giving you confidence in managing even complex deployments. Happy deploying!
