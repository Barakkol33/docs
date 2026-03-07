# Metrics & Prometheus (Quick Intro)

## What are Metrics?
- **Metrics = numbers measured over time → form a timeseries**
- Example: requests per second, CPU usage
- Stored as `{name}{labels} value timestamp`

## Why Metrics Matter
- Detect performance issues early  
- Track KPIs (throughput, error rate)  
- Enable **alerts** & **dashboards**  

## Examples
- `http_requests_total{status="500"} 3`  
- `cpu_usage_seconds_total{instance="node1"} 42.7`

## What is PromQL?
- Query language for Prometheus metrics  
- Lets you **filter, aggregate, and analyze timeseries**

### PromQL Examples
- **Error rate (last 5m):**
```promql
rate(http_requests_total{status="500"}[5m])
````

* **CPU usage % per node:**

```promql
100 * (1 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])))
```

## What is Scraping?

* **Prometheus pulls metrics** from endpoints (`/metrics`) on apps/services at regular intervals
* Each scrape adds a new **sample** to the timeseries