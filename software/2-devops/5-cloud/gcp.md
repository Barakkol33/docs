# GCP (Google Cloud Platform)

Google's cloud. Known for strong data/analytics (BigQuery), Kubernetes (GKE, since Google created Kubernetes), a clean global network, and simple serverless (Cloud Run).

---

## Resource hierarchy

```
Organization
 └── Folder (optional, e.g. per team/environment)
      └── Project  ← the core unit
           └── Resources (VMs, buckets, databases…)
```

- **Project** – The fundamental container: owns resources, enables APIs, holds IAM policy and **billing**. Has a name, a unique **project ID**, and a number. Use separate projects for dev/staging/prod.
- **Organization / Folder** – Group projects and apply **IAM and Organization Policies** (constraints, e.g. "no external IPs") down the tree. Permissions are **inherited** downward.
- **Billing account** – Linked to projects; pays for them.
- **APIs must be enabled** per project before use: `gcloud services enable run.googleapis.com`.
- **Region / Zone** – e.g. `europe-west1` / `europe-west1-b`. Some services are multi-region or global.
- **Labels** – Key/value metadata for cost tracking.

---

## IAM

- **Principal** – Who: Google account, **Google Group**, **service account**, Workspace domain, workload identity.
- **Role** – A set of permissions.
  - _Basic_ (Owner/Editor/Viewer) – Too broad, avoid in production.
  - _Predefined_ – Per service, e.g. `roles/storage.objectViewer`. Normal choice.
  - _Custom_ – Your own permission list.
- **Policy / binding** – "Principal X has role R on resource Y" attached to org/folder/project/resource.
- **Service account** – Identity for workloads (VM, Cloud Run, pod). Attach to the resource, so no key files are needed. **Avoid downloading service account keys.**
- **Workload Identity (Federation)** – GKE pods or external systems (GitHub Actions, AWS) act as a service account without keys.
- **Impersonation** – A principal temporarily acts as a service account (`--impersonate-service-account`).

```bash
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:app@my-project.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"
```

---

## Networking

- **VPC** – **Global** resource (a notable difference from AWS/Azure): one VPC spans all regions.
- **Subnet** – **Regional** (spans all zones in a region).
- **Firewall rules** – Applied to the VPC, target instances by **network tags** or service accounts. Implied: deny all ingress, allow all egress.
- **Routes**, **Cloud Router**, **Cloud NAT** – Outbound internet for instances without external IPs.
- **Private Google Access / Private Service Connect** – Reach Google APIs and managed services privately.
- **Shared VPC** – One host project's network shared with many service projects.
- **VPC Peering, Cloud VPN, Interconnect** – Connect networks / on-prem.
- **Cloud Load Balancing** – Global anycast HTTP(S) load balancer (single IP worldwide), plus regional and TCP/UDP variants.
- **Cloud DNS**, **Cloud CDN**, **Cloud Armor** (WAF/DDoS).

---

## Compute

- **Compute Engine (GCE)** – VMs.
  - _Machine types_ – `e2-medium`, `n2-standard-4`, `c3`, custom sizes, GPUs.
  - _Images / Instance templates_.
  - _Managed Instance Group (MIG)_ – Autoscaled, auto-healed group of identical VMs.
  - _Spot VMs_ – Cheap, preemptible.
  - _Persistent Disk_ – Block storage.
- **GKE (Google Kubernetes Engine)** – Managed Kubernetes.
  - _Autopilot_ – Google manages nodes too, pay per pod resources. Recommended default.
  - _Standard_ – You manage node pools.
  - Built-in Gateway/Ingress load balancers, Workload Identity.
- **Cloud Run** – Run **any container** serverlessly: HTTP-triggered, scales to zero, pay per request/CPU time. Often the simplest way to deploy a containerized service. Also **Cloud Run jobs** for batch.
- **Cloud Functions** – Event-driven functions.
- **App Engine** – Older PaaS.
- **Artifact Registry** – Docker, npm, Maven, Python, Helm repositories (replaces Container Registry).
- **Cloud Build** – CI that builds images. **Cloud Deploy** – delivery pipelines.

---

## Storage & databases

- **Cloud Storage (GCS)** – Object storage. _Buckets_ (globally unique) with classes: Standard, Nearline, Coldline, Archive. Uniform bucket-level access, versioning, lifecycle rules, signed URLs.
- **Persistent Disk / Hyperdisk** – Block. **Filestore** – managed NFS.
- **Cloud SQL** – Managed MySQL / PostgreSQL / SQL Server (HA, replicas, backups). **AlloyDB** – high-performance Postgres-compatible.
- **Spanner** – Globally distributed relational DB with strong consistency and horizontal scale.
- **Firestore** – Serverless document DB. **Bigtable** – wide-column for huge throughput (Cassandra/HBase-like, see [cassandra.md](../3-data-sources/databases/cassandra.md)).
- **Memorystore** – Managed Redis/Valkey/Memcached.
- **BigQuery** – Serverless **data warehouse**. Separate storage and compute, query petabytes with SQL, pay per data scanned (on-demand) or per slot. _Dataset → table_; use **partitioning and clustering** to cut cost. A flagship GCP service.

---

## Messaging & data

- **Pub/Sub** – Global, managed messaging (topics, subscriptions, push/pull). Similar concepts to Kafka ([kakfa.md](../3-data-sources/kakfa.md)).
- **Dataflow** (Apache Beam), **Dataproc** (Spark/Hadoop), **Cloud Composer** (Airflow).
- **Cloud Tasks / Cloud Scheduler** – Async tasks and cron.
- **Vertex AI** – ML/AI platform.

---

## Security & operations

- **Secret Manager** – Versioned secrets. **Cloud KMS** – Encryption keys (CMEK).
- **Cloud Logging / Cloud Monitoring** (formerly Stackdriver) – Logs, metrics, alerting, dashboards. Managed Prometheus available.
- **Cloud Audit Logs** – Admin Activity (always on), Data Access (opt-in).
- **Security Command Center** – Findings and posture.
- **Organization Policy** – Guardrails, e.g. restrict regions, block public IPs.
- **IaC** – Terraform (most common), Deployment Manager, Config Connector.

---

## CLI cheat sheet

```bash
gcloud auth login                        # human login
gcloud auth application-default login   # credentials for local code/SDKs
gcloud config set project my-project
gcloud config list
gcloud projects list

gcloud compute instances list
gcloud compute instances create vm1 --zone=europe-west1-b --machine-type=e2-medium

gcloud storage ls
gcloud storage cp file.txt gs://my-bucket/

# Containers
gcloud auth configure-docker europe-west1-docker.pkg.dev
docker push europe-west1-docker.pkg.dev/my-project/my-repo/app:1

# Cloud Run: deploy a container
gcloud run deploy app --image europe-west1-docker.pkg.dev/my-project/my-repo/app:1 \
  --region europe-west1 --allow-unauthenticated

# GKE
gcloud container clusters get-credentials my-cluster --region europe-west1
kubectl get nodes

# BigQuery
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `my-project.my_dataset.events`'
```

**Typical web app on GCP:** Global HTTPS Load Balancer (+ Cloud CDN/Armor) → Cloud Run or GKE Autopilot → Cloud SQL (private IP), assets in Cloud Storage, secrets in Secret Manager, analytics in BigQuery, all deployed with Terraform.
