# DevOps Monitoring with Prometheus, Loki & Grafana

---

## Table of Contents
1. [Why Monitor? (The Problem)](#why-monitor-the-problem)
2. [Stack Overview](#stack-overview)
3. [Prometheus: Metrics Collection & Querying](#prometheus-metrics-collection--querying)
4. [Alerting: Prometheus + Alertmanager](#alerting-prometheus--alertmanager)
5. [VictoriaMetrics: Prometheus-Compatible at Scale](#victoriametrics-prometheus-compatible-at-scale)
6. [Loki & Promtail: Centralized Logs](#loki--promtail-centralized-logs)
7. [Grafana: Visualization & Dashboards](#grafana-visualization--dashboards)
8. [KPIs, SLIs, SLOs & Alerts](#kpis-slis-slos--alerts)
9. [Deploying on Kubernetes (Quick Start)](#deploying-on-kubernetes-quick-start)
10. [End-to-End Example Walkthrough](#end-to-end-example-walkthrough)
11. [Tips, Pitfalls & Best Practices](#tips-pitfalls--best-practices)
12. [PromQL & LogQL Cheat Sheets](#promql--logql-cheat-sheets)

---

## Why Monitor? (The Problem)

Modern systems emit **a lot** of operational data. Without structure, you can’t answer basic questions:

- **Production output:** How many products were created today? Per line? Per SKU?
- **Performance:** How long does making each product take? Are we getting faster?
- **Labeling/Categorization:** How many products per type, version, or quality grade?
- **Infrastructure:** How many worker nodes exist? What CPU, memory, and disk are in use?
- **Jobs & Reliability:** How many jobs execute? How many fail? Why?
- **People & Process:** Which metrics are **KPIs** that motivate teams? Which metrics are **critical** and must **page** on-call engineers when thresholds are crossed?

**Goal:** Turn raw metrics and logs into actionable insights and alerts.

---

## Stack Overview

A popular, production-proven stack combines **Prometheus (metrics)**, **Loki (logs)**, and **Grafana (visualization & alerts)**.

```mermaid
flowchart LR
  subgraph Nodes
    A[Apps/Services] -->|/metrics| E(Exporter/SDK)
    A -->|stdout/files| P(Promtail)
  end

  E -->|HTTP scrape| PR(Prometheus)
  PR <-->|remote_write/read| VM(VictoriaMetrics)
  P -->|push| L(Loki)

  PR -->|metrics datasource| G[Grafana]
  L -->|logs datasource| G
  G -->|alerts| AM(Alertmanager) -->|PagerDuty/Slack/Email| U[On-call/User]
````

**Key ideas**

* **Prometheus** pulls metrics (the “pull model”) and stores **time series**.
* **Loki** collects and stores logs from all nodes via **Promtail**.
* **Grafana** visualizes both metrics and logs, and manages alerts (often via Alertmanager).
* **VictoriaMetrics** can replace/augment Prometheus storage for scale.

---

## Prometheus: Metrics Collection & Querying

### What It Is

* **Prometheus** is a metrics server that **scrapes** HTTP endpoints (e.g., `/metrics`).
* Each scrape produces **samples** labeled with key/value pairs (e.g., `job`, `instance`, `method`, `status`).
* Samples over time form **time series**.

### Example Exposition Format (from a `/metrics` endpoint)

```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{app="checkout",method="GET",status="200"} 1027
http_requests_total{app="checkout",method="POST",status="500"} 3
```

### PromQL (Query Language) — Practical Examples

* **Average request duration (last 5m):**

```promql
rate(http_request_duration_seconds_sum[5m])
/
rate(http_request_duration_seconds_count[5m])
```

* **Failed jobs per minute (sum across services):**

```promql
sum(rate(jobs_total{status="failed"}[1m]))
```

* **Products created today (cumulative then delta):**

```promql
increase(products_created_total[24h])
```

* **Nodes by resource (CPU cores & memory):**

```promql
sum(machine_cpu_cores)           # total cores
sum(machine_memory_bytes) / 1e9  # GB of memory
```

* **95th percentile latency from histogram:**

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

---

## Alerting: Prometheus + Alertmanager

**Flow:** PromQL expression ➜ Alert fires ➜ Alertmanager routes ➜ Notification (PagerDuty/Slack/Email/etc.)

### Example Alert Rule (High Error Rate)

```yaml
groups:
  - name: service-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 5
        for: 10m
        labels:
          severity: page
          team: web
        annotations:
          summary: "High error rate on web services"
          description: "5xx rate > 5 req/s for 10m"
```

### Example Alert Rule (Node Disk Almost Full)

```yaml
- alert: DiskSpaceLow
  expr: (node_filesystem_size_bytes{fstype!~"tmpfs|overlay"} - node_filesystem_free_bytes{fstype!~"tmpfs|overlay"})
        / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"} > 0.85
  for: 15m
  labels:
    severity: warn
  annotations:
    summary: "Disk usage > 85%"
```

---

## VictoriaMetrics: Prometheus-Compatible at Scale

**Why use it?**

* Prometheus-compatible **ingest** and **query** endpoints.
* Efficient storage & **remote\_write/remote\_read** support.
* **Cluster mode** that separates **scrape, insert, store, query** for high scale.

### Example: Prometheus ➜ VictoriaMetrics (`remote_write`)

```yaml
remote_write:
  - url: http://victoria-metrics:8428/api/v1/write
```

**Common pattern:** Let **Prometheus** keep scraping, but offload long-term storage and heavy reads to **VictoriaMetrics**.

---

## Loki & Promtail: Centralized Logs

### The Problem with Logs

* Logs live on many machines and containers.
* SSH’ing around to grep is slow and brittle.

### The Solution

* **Promtail** (agent on each node/pod) tails logs and **ships** them to **Loki**.
* **Loki** stores logs with labels (e.g., `{app="payments", pod="payments-7c9f..."}`) and integrates with Grafana.

### LogQL (Query Language) — Practical Examples

* **All logs for a service:**

```logql
{app="payments"}
```

* **Filter for error text (last hour):**

```logql
{app="payments"} |= "ERROR"
```

* **Only WARN level (assuming level is a label):**

```logql
{app="payments", level="warn"}
```

* **Count errors per minute (aggregation on logs):**

```logql
sum by (app) (rate(({app="payments"} |= "ERROR")[1m]))
```

* **Extract a field (e.g., `order_id`) and count:**

```logql
{app="checkout"} | regexp "order_id=(?P<order_id>[0-9a-f-]+)"
| unwrap order_id
| count_over_time([5m])
```

---

## Grafana: Visualization & Dashboards

**What Grafana does**

* Connects to **Prometheus** (metrics) and **Loki** (logs) as data sources.
* Builds **dashboards** with panels: time series, tables, gauges, heatmaps, logs, etc.
* Supports **alerting**, annotations, and dynamic **variables** (e.g., pick a service by dropdown).

### Useful Dashboard Ideas

* **Service Health:** p95 latency, error rate, request throughput.
* **Infra Overview:** Node CPU/Memory/Disk/Network, pod restarts.
* **Business KPIs:** Daily products created, defects vs. total, labeling by category.
* **Correlated Views:** Latency panel next to an error-rate panel and a **logs** panel filtered by the same service.

### Panel Query Examples

* **p95 latency (PromQL):**

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[10m])))
```

* **Errors by service (PromQL):**

```promql
sum by (app) (rate(http_requests_total{status=~"5.."}[5m]))
```

* **Recent error logs (LogQL):**

```logql
{app="$app"} |= "ERROR"
```

---

## KPIs, SLIs, SLOs & Alerts

* **KPI (Key Performance Indicator):** Business-facing metrics (e.g., products/day, defect ratio).
* **SLI (Service Level Indicator):** Measured service behavior (e.g., success rate, latency).
* **SLO (Service Level Objective):** Target for SLIs (e.g., “99.9% success over 30 days”).
* **Alert:** A condition indicating we’re violating (or about to violate) an SLO or encountering an incident.

### Examples

* **KPI:**
  *products\_created\_total* ➜ `increase(products_created_total[24h])`
* **SLI (Availability):**
  `success_rate = sum(rate(http_requests_total{status=~"2..|3.."}[5m])) / sum(rate(http_requests_total[5m]))`
* **SLO Alert (Availability < 99.9% for 10m):**

```promql
(1 - success_rate) > 0.001
```

---

## Deploying on Kubernetes (Quick Start)

> The stack is commonly installed via **Helm** charts with only a few commands.

### 1) Prometheus (kube-prometheus-stack includes Alertmanager & Grafana)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

### 2) Loki & Promtail

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Loki
helm install loki grafana/loki --namespace monitoring

# Promtail (daemonset on nodes)
helm install promtail grafana/promtail --namespace monitoring \
  --set "loki.serviceName=loki"
```

### 3) (Optional) VictoriaMetrics (single-node)

```bash
helm repo add vm https://victoriametrics.github.io/helm-charts
helm repo update

helm install vmsingle vm/victoria-metrics-single --namespace monitoring
```

### 4) Hook Prometheus to VictoriaMetrics (remote\_write)

Add to Prometheus values (or use `helm upgrade` with `--set-file`):

```yaml
prometheus:
  prometheusSpec:
    remoteWrite:
      - url: http://vmsingle-victoria-metrics-single-server:8428/api/v1/write
```

### 5) Access Grafana (if not exposed)

```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
# then open http://localhost:3000
```

---

## End-to-End Example Walkthrough

**Scenario:** Product checkout latency spikes and errors rise.

1. **Alert fires** (`HighErrorRate`) and pages on-call.
2. In **Grafana**, open the “Web Overview” dashboard:

   * **Error rate panel** shows a surge starting 10 minutes ago.
   * **p95 latency panel** also trending up.
3. Use **logs panel** (Loki) filtered by `app="checkout"`:

   * See repeated `ERROR payment timeout` lines.
   * Extract `order_id` to identify impacted requests.
4. **Correlate** with upstream service (payments) metrics:

   * Payments p95 latency regressed due to a config rollout.
5. **Rollback** the config, watch the panels normalize, alert resolves.

---

## Tips, Pitfalls & Best Practices

* **Label Hygiene (Cardinality Control):**

  * Avoid unbounded labels (e.g., `user_id`, `order_id`) on metrics. Use them in **logs**, not metrics.
  * Prefer fixed-cardinality labels like `app`, `env`, `region`.
* **Alerting Discipline:**

  * Page on symptoms (availability, error budget burn), not on every low-level metric.
  * Use `for:` to reduce flapping.
* **Histograms & Quantiles:**

  * Expose histograms for latency; query with `histogram_quantile`.
  * Ensure consistent bucket configs across services.
* **Capacity Planning:**

  * Set **retention** wisely (e.g., 15–30 days for metrics; logs based on budget).
  * Offload long-term storage to VictoriaMetrics.
* **Dashboards that Tell a Story:**

  * Place related panels together (throughput, errors, latency, logs).
  * Use **templating variables** (service, namespace, cluster).
* **Kubernetes Scraping:**

  * Leverage service monitors & pod monitors (from kube-prometheus-stack).
  * Ensure apps expose `/metrics` with proper instrumentation (Prometheus client libraries).

---

## PromQL & LogQL Cheat Sheets

### PromQL Snippets

* **Overall success rate (5m):**

```promql
sum(rate(http_requests_total{status=~"2..|3.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

* **CPU usage per node (percentage):**

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

* **Memory working set (per pod):**

```promql
sum by (pod) (container_memory_working_set_bytes{container!="",pod!=""}) / 1e6
```

* **Top 5 endpoints by error rate:**

```promql
topk(5, rate(http_requests_total{status=~"5.."}[5m]) )
```

### LogQL Snippets

* **Errors for a service:**

```logql
{app="$app"} |= "ERROR"
```

* **Count WARN/ERROR lines per 5 minutes:**

```logql
sum(rate(({app="$app"} |~ "(WARN|ERROR)")[5m]))
```

* **Structured extraction (JSON logs):**

```logql
{app="api"} | json | level="error" | line_format "{{.msg}} - user={{.userId}}"
```

---

## Summary

* **Prometheus** gathers **metrics**; **PromQL** makes them explorable.
* **Loki** centralizes **logs**; **LogQL** makes them searchable.
* **Grafana** visualizes both and ties them to **alerts** and on-call workflows.
* **VictoriaMetrics** scales storage and querying when you outgrow a single Prometheus.
* With a few **Kubernetes + Helm** steps, you can stand up a comprehensive monitoring stack that supports **KPIs**, **SLIs/SLOs**, and **reliable alerting**.

```