# DevOps

DevOps is about making software delivery and production operations reliable, repeatable, and efficient.

---

## Devops Intro

### Core concepts

- **Automation** – Remove manual steps so work is consistent and repeatable (builds, tests, deploys, provisioning).
- **Infrastructure as Code (IaC)** – Define infrastructure in code so it's reviewable, versioned, and reproducible.
- **CI/CD** – Validate and deliver changes continuously via an automated pipeline; small, frequent releases.
- **Observability** – Understand system behavior via metrics, logs, and traces; detect and respond to issues quickly.
- **High Availability (HA)** – Keep serving traffic when components fail.
  - Replication – create multiple copies of data that can be used if the currently used copy is unavailable.
  - Load balancing – spread traffic across instances.
  - Sharding – split workload/data across nodes.
- **Shift left** – Catch problems early: tests, linting, security scans in CI before code reaches production.
- **Shift right** – Learn from production: runtime visibility, canary/blue-green deployments, A/B testing.
- **Recovery** – Plan for failure: backups, restore drills, incident response, runbooks, clear ownership.

**Resilience patterns:**

- **Retries** – Handle transient failures; use backoff + jitter to avoid retry storms.
- **Circuit breaker** – Stop calling a failing dependency; fail fast and give it time to recover.
- **Rate limiting** – Cap request volume to protect services from overload.

---

### Infrastructure as Code tools

- **Terraform** – Declarative IaC; `plan` → `apply` → `destroy`. Providers for every major cloud.
- **Pulumi** – IaC using general-purpose languages (TypeScript, Python, Go). Same concept, code instead of HCL.
- **SOPS** – Encrypt secrets in YAML/JSON files so they can be stored safely in Git (keys from KMS/GPG/Age).

---

### CI/CD

Automated pipeline that takes code from commit to production:

**test → build → deploy (staging) → approve → deploy (prod)**

Each stage adds confidence. Failures stop the pipeline early, preventing broken code from reaching users.

---

## Containers

### Docker

Docker packages applications into images and runs them as isolated containers.

- **Image** – Read-only template: app + OS layers + dependencies.
- **Container** – Running instance of an image (an isolated process).
- **Volume** – Persistent storage that survives container restarts.
- **Dockerfile** – Build recipe that defines how to create an image.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### Kubernetes (K8s)

Container orchestration: the control plane decides *what should run where*, nodes actually run it.

**Architecture:**
- **Control plane** – API server, etcd (state store), scheduler, controller manager.
- **Nodes** – kubelet (agent), container runtime, kube-proxy (networking), CNI plugin.

**Core objects:**
- **Namespace** – Partition resources (like folders for isolation).
- **Pod** – Smallest deployable unit; one or more containers sharing network/volumes.
- **Deployment** – Manages stateless pods: rolling updates, scaling, self-healing.
- **StatefulSet** – For stateful workloads: stable pod names, per-pod storage, ordered startup.
- **DaemonSet** – One pod per node (log collectors, monitoring agents, network plugins).
- **Job / CronJob** – Run-to-completion tasks, optionally on a schedule.
- **Service** – Stable networking endpoint for a set of pods (ClusterIP, NodePort, LoadBalancer).
  - **Headless Service** – `clusterIP: None`; DNS returns individual pod IPs.
  - **DNS** – `<service>.<namespace>.svc.cluster.local`
- **ConfigMap** – Non-sensitive configuration (env vars, config files).
- **Secret** – Sensitive data (passwords, tokens); base64-encoded, optionally encrypted at rest.
- **HPA** – Horizontal Pod Autoscaler; scales replicas based on CPU/memory/custom metrics.
- **Ingress** – HTTP(S) routing (host/path) from outside the cluster to Services.

**Object structure:** Every object has `metadata` (name, labels), `spec` (desired state), and `status` (observed state).

**Tooling:**
- **kubectl** – CLI for interacting with the cluster (get, describe, logs, exec, apply, delete).
- **Helm** – Package manager; Charts bundle K8s manifests into reusable, versioned packages.

**Nice to know:**
- **Operator pattern** – Controller + CRDs encoding app-specific operational knowledge.
- **Sidecar container** – Extra container in a pod (proxy, log shipper, cert refresher).
- **k9s** – Terminal UI for cluster navigation and debugging.

**Administration:**
- **PVC** – PersistentVolumeClaim; request for storage, dynamically or statically provisioned.
- **PVC Autoresizer** – Automatically resizes volumes (CSI support required).
- **Karpenter** – Node autoscaler/provisioner (cloud environments).
- **Istio** – Service mesh: traffic management, mTLS, observability via sidecar proxies.
- **cert-manager** – Automates TLS certificate issuance/renewal.
- **kube-proxy** – Implements Service routing rules on each node.
- **VPC CNI DaemonSet** – Cloud-provider networking plugin (e.g., AWS VPC CNI).

---

## Observability

### Prometheus (metrics)

- **PromQL** – Query language for time-series data (`rate()`, `sum()`, `histogram_quantile()`).
- **Scraping** – Prometheus pulls metrics from `/metrics` endpoints at regular intervals.
- **Alerts** – Rules that fire when a PromQL expression is true for a duration (e.g., high error rate for 5 minutes).

### Loki (logs)

- **LogQL** – Query language for logs (filter + aggregate); syntax similar to PromQL.
- **Promtail** – Agent that ships logs from nodes/pods to Loki.

### Grafana (visualization)

- **Dashboard** – Panels showing metrics/logs over time.
- **Variables** – Template variables for dynamic, reusable dashboards (e.g., namespace, service dropdowns).
- **Explore** – Ad-hoc querying interface for both Prometheus and Loki.

---

## Data Sources

### Databases

When choosing a database, ask: what's the data model, consistency requirements, query patterns (reads vs writes, analytics vs transactions), and operational needs (backup, replication, upgrades)?

| Database | Type | Best for |
|---|---|---|
| **PostgreSQL / MySQL** | Relational (SQL) | Structured business data, transactions, joins |
| **Elasticsearch** | Search engine | Full-text search, filtering, aggregations |
| **MongoDB** | Document store | Flexible JSON-like schemas, evolving data models |
| **Cassandra** | Wide-column (NoSQL) | Massive write throughput, multi-datacenter scale |
| **ClickHouse** | Columnar (analytics) | Fast aggregations on huge datasets (dashboards, logs) |
| **Redis** | In-memory key-value | Caching, session store, pub/sub, real-time counters |
| **YugabyteDB** | Distributed SQL | PostgreSQL-compatible with horizontal scaling and HA |

```sql
-- Example: basic SQL query
SELECT id, name FROM users WHERE id = 123;
```

### Kafka (event streaming)

Kafka is not a database — it's a distributed event log for async communication and data pipelines.

- **Topic** – A named stream of events (like a log file that multiple consumers can read).
- **Partition Key** – Determines which partition a message goes to (ordering guarantee within a partition).
- **Consumer Lag** – How far behind a consumer is from the latest message (key metric for health).
- **Broker** – A Kafka server node; topics are spread across brokers for scale and redundancy.
