# DevOps — Self-Learning Guide

A hands-on guide to DevOps: from Linux basics through Docker and Kubernetes, to deploying a real application on a local cluster.

## Prerequisites

Before starting, follow [0-prerequisites.md](0-prerequisites.md) to install the required tools and pre-pull Docker images. This is especially important if you'll be working without internet access.

You'll also want a good markdown viewer to read these guides comfortably. Two recommended options:
- **Obsidian** — open the `docs/` folder as a vault for a clean reading experience with navigation
- **VS Code** — use the built-in markdown preview (`Ctrl+Shift+V` or the preview icon in the top-right corner of any `.md` file)

## Chapters

Read the chapters in order. Each one builds on the previous.

### 1. Get Started

| File | Topic |
|---|---|
| [1-index.md](1-get-started/1-index.md) | DevOps overview — core concepts, architecture, tools landscape |
| [2-intro.md](1-get-started/2-intro.md) | DevOps intro — motivation, reliability fundamentals, IaC, CI/CD |
| [3-linux.md](1-get-started/3-linux.md) | Linux practical guide — filesystem, text processing, networking, bash scripting |

### 2. Containers

| File | Topic |
|---|---|
| [1-docker.md](2-containers/1-docker.md) | Docker — images, containers, volumes, networking, Dockerfile, Compose |
| [2-k8s.md](2-containers/2-k8s.md) | Kubernetes — architecture, objects, kubectl, Helm, kind, storage, MetalLB |

### 3. Data Sources

| File | Topic |
|---|---|
| [databases.md](3-data-sources/databases.md) | Databases — overview, when to use which, Elasticsearch, MongoDB, Redis, ClickHouse |
| [postgresql.md](3-data-sources/databases/postgresql.md) | PostgreSQL — relational default: MVCC, indexes, replication, psql |
| [mysql.md](3-data-sources/databases/mysql.md) | MySQL / MariaDB — InnoDB, binlog, replication |
| [sqlite.md](3-data-sources/databases/sqlite.md) | SQLite — embedded, serverless, single-file database |
| [cassandra.md](3-data-sources/databases/cassandra.md) | Cassandra — wide-column, partition keys, consistency levels, CQL |
| [dynamodb.md](3-data-sources/databases/dynamodb.md) | DynamoDB — serverless key-value on AWS, keys, indexes, capacity |
| [neo4j.md](3-data-sources/databases/neo4j.md) | Neo4j — graph database and Cypher |
| [timeseries.md](3-data-sources/databases/timeseries.md) | InfluxDB & TimescaleDB — time-series data |
| [kakfa.md](3-data-sources/kakfa.md) | Kafka — event streaming, topics, partitions, consumers |

### 4. Observability

| File | Topic |
|---|---|
| [monitoring.md](4-observability/monitoring.md) | Monitoring with Prometheus, Loki, and Grafana |
| [metrics.md](4-observability/metrics.md) | Metrics — PromQL, scraping, alerting |
| [loki.md](4-observability/loki.md) | Loki — log aggregation and LogQL |

### 5. Cloud

| File | Topic |
|---|---|
| [cloud.md](5-cloud/cloud.md) | Cloud — core concepts, service mapping across AWS / GCP / Azure |
| [aws.md](5-cloud/aws.md) | AWS — IAM, VPC, EC2, EKS, S3, RDS, Lambda, CLI |
| [gcp.md](5-cloud/gcp.md) | GCP — projects, IAM, VPC, GKE, Cloud Run, BigQuery, gcloud |
| [azure.md](5-cloud/azure.md) | Azure — subscriptions, Entra ID, VNet, AKS, Blob, Cosmos DB, az CLI |

## Quick Reference

[1-cheatsheet.md](1-cheatsheet.md) — command cheatsheet for Linux, Docker, and Kubernetes. Keep this open while working through the guides and exercise.

## Exercise

[6-exercise/](6-exercise/) — **Guestbook on Kubernetes**: build a web app, containerize it, deploy to a kind cluster with all the K8s objects you learned (Namespace, ConfigMap, Secret, StatefulSet, Deployment, Service, Job), and package it as a Helm chart.

- [Exercise instructions](6-exercise/README.md)
- [Solution](6-exercise/solution/) — completed code + Helm chart
