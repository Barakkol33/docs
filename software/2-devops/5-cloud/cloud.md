# Cloud

Cloud = renting compute + storage + managed services, on demand, billed by usage, through an API. Instead of buying servers, you create resources with a few clicks, a CLI command, or (best) Infrastructure as Code.

The three big providers have **different names for very similar building blocks**. Learn the concepts once, then map them.

| Provider | Guide |
|---|---|
| Amazon Web Services | [aws.md](aws.md) |
| Google Cloud Platform | [gcp.md](gcp.md) |
| Microsoft Azure | [azure.md](azure.md) |

---

## Core concepts (all providers)

- **IaaS / PaaS / SaaS / FaaS**
  - _IaaS_ – You rent raw VMs, disks and networks, and manage the OS and up. (EC2)
  - _PaaS_ – You deploy code/containers, the platform runs them. (App Service, Cloud Run, Elastic Beanstalk)
  - _FaaS / serverless_ – Functions run on events, billed per invocation. (Lambda)
  - _SaaS_ – A finished application. (Gmail, Salesforce)
- **Shared responsibility model** – The provider secures the cloud (hardware, data centers, hypervisor). **You** secure what you put in it: IAM, network rules, OS patches on VMs, data encryption, public buckets.
- **Region** – A geographic location with multiple data centers (e.g. `eu-west-1`, `europe-west1`, `westeurope`). Choose by latency, price, data-residency laws, service availability.
- **Availability Zone (AZ)** – Isolated data center(s) within a region. Spread instances over 2–3 AZs for high availability.
- **Identity & access (IAM)** – Who (user, group, service identity) can do what (actions) on which resource. **Least privilege** is the rule. Workloads should use roles / managed identities, not long-lived keys.
- **Virtual network** – Your private, isolated network (VPC / VNet) divided into subnets, with routes, gateways and firewall rules.
- **Compute options** – VMs, containers (managed Kubernetes, serverless containers), functions.
- **Storage types** – _Object_ (files over HTTP, S3-style), _Block_ (disk attached to a VM), _File_ (shared NFS/SMB).
- **Managed services** – Databases, queues, caches, etc. where the provider handles patching, backup and failover. You pay more, operate less.
- **Elasticity & auto scaling** – Add/remove capacity automatically as load changes.
- **Pricing models** – On-demand (pay per second/hour), reserved / committed use / savings plans (1–3 year commitment, big discount), spot / preemptible (very cheap, can be reclaimed).
- **Egress costs** – Data going **out** of the cloud (or across regions) costs money; ingress is usually free. A frequent bill surprise.
- **Infrastructure as Code** – Terraform / OpenTofu (multi-cloud), Pulumi, or native: CloudFormation/CDK (AWS), Bicep/ARM (Azure), Deployment Manager (GCP).
- **Tagging / labels** – Metadata on resources for cost allocation and automation.
- **Well-architected thinking** – Reliability, security, performance, cost, operational excellence.

---

## Service mapping

| Concept | AWS | GCP | Azure |
|---|---|---|---|
| Account structure | Organization → Account | Organization → Folder → Project | Management Group → Subscription → Resource Group |
| Identity & permissions | IAM | Cloud IAM | Entra ID (Azure AD) + RBAC |
| Virtual network | VPC | VPC (global) | VNet |
| Virtual machines | EC2 | Compute Engine | Virtual Machines |
| VM auto scaling | Auto Scaling Group | Managed Instance Group | VM Scale Sets |
| Container registry | ECR | Artifact Registry | ACR |
| Managed Kubernetes | EKS | GKE | AKS |
| Serverless containers | Fargate / App Runner | Cloud Run | Container Apps |
| Functions | Lambda | Cloud Functions / Cloud Run functions | Azure Functions |
| Object storage | S3 | Cloud Storage | Blob Storage |
| Block storage | EBS | Persistent Disk | Managed Disks |
| Managed SQL | RDS / Aurora | Cloud SQL / AlloyDB | Azure SQL / Database for PostgreSQL & MySQL |
| NoSQL | DynamoDB | Firestore / Bigtable | Cosmos DB |
| Data warehouse | Redshift | BigQuery | Synapse / Fabric |
| Queue / messaging | SQS, SNS | Pub/Sub | Service Bus, Event Grid |
| Event streaming | Kinesis / MSK | Pub/Sub / Managed Kafka | Event Hubs |
| Load balancer | ELB (ALB/NLB) | Cloud Load Balancing | Load Balancer / Application Gateway |
| DNS | Route 53 | Cloud DNS | Azure DNS |
| CDN | CloudFront | Cloud CDN | Front Door / CDN |
| Secrets | Secrets Manager / SSM Parameter Store | Secret Manager | Key Vault |
| Key management | KMS | Cloud KMS | Key Vault |
| Monitoring & logs | CloudWatch | Cloud Monitoring / Logging | Azure Monitor / Log Analytics |
| Audit log | CloudTrail | Cloud Audit Logs | Activity Log |
| IaC (native) | CloudFormation / CDK | Deployment Manager | ARM / Bicep |
| CLI | `aws` | `gcloud` | `az` |

---

## How this connects to what you learned

- **Docker images** are pushed to a cloud **registry** (ECR / Artifact Registry / ACR).
- **Kubernetes** runs as a managed service (EKS / GKE / AKS): the provider operates the control plane, you manage worker nodes (or use serverless nodes). The cloud's load balancer, disks and IAM integrate through Services of type `LoadBalancer` and PersistentVolumes. This replaces MetalLB and kind's local storage.
- **Databases** can run as managed services instead of StatefulSets. See [databases](../3-data-sources/databases.md).
- **Monitoring** with Prometheus/Grafana/Loki is portable. Cloud-native alternatives are CloudWatch / Cloud Monitoring / Azure Monitor.

## First-day checklist (any cloud)

1. Enable **MFA** on the root/owner account, then stop using it for daily work.
2. Create a separate admin identity with least privilege.
3. Set a **budget alert** so cost surprises reach you early.
4. Pick a region, and stay consistent.
5. Define infrastructure as code from the start. Avoid click-ops for anything you'd need to rebuild.
6. Turn on audit logging.
7. Never commit credentials. Use roles / workload identity / managed identity.
