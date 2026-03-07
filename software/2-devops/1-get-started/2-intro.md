# DevOps Intro

DevOps is about making software delivery and production operations reliable and repeatable.

## Core concepts

DevOps isn’t a single tool or job title; it’s a set of practices that reduce the time and risk of changes:

### Automation

Automation removes manual steps so work is consistent, repeatable, and less error-prone. Typical targets include builds, tests, deployments, backups, and environment provisioning. The goal is to make the “happy path” the default path.

Why it matters beyond day-to-day efficiency: if there's a massive or unexplained failure, you can tear everything down and start clean — because the entire setup is automated and reproducible.   
And when you need to grow, scaling is straightforward: spin up more of what you already have instead of manually configuring each new instance.

### Infrastructure as Code (IaC)

IaC means defining infrastructure with code so it can be reviewed, versioned, and reproduced. This makes environments consistent across dev/staging/prod and allows safe changes through pull requests. IaC also supports fast recovery by recreating infrastructure from source-of-truth.

### CI/CD

CI/CD is the practice of validating and delivering changes continuously via an automated pipeline. It enables small, frequent releases by running tests and checks on every change and deploying in a controlled way. Good CI/CD reduces fear of deploys and shortens feedback loops.

### Observability

Observability is the ability to understand what your system is doing from the outside, typically via metrics, logs, and traces. Monitoring turns that data into alerts and dashboards so you can detect and respond to issues quickly. Strong observability shortens incident time-to-diagnosis and helps validate changes.

### High Availability (HA)

High availability is designing systems to keep serving traffic even when components fail. It usually combines redundancy plus automated failover, so a single outage doesn’t become total downtime. Common building blocks include:
- replication (leader/follower or multi-primary)
- load balancing (spread traffic across instances)
- sharding/partitioning (split workload/data across nodes)

### Shift left

Shift left means moving quality and security checks earlier in the lifecycle (before production). Examples include unit/integration tests, linting, static analysis, and dependency or secret scanning in CI. Catching problems earlier is cheaper and prevents avoidable incidents.

### Shift right

Shift right focuses on learning from production using real user behavior and real system conditions. It includes runtime visibility, feature flags, gradual rollouts, and production-safe experiments. The outcome is better reliability and faster iteration grounded in reality.

### Recovery

Recovery is planning for failure so incidents are survivable and repeatable to handle. It includes backups and restore drills, incident response, runbooks, and clear ownership during outages. Recovery work turns “we hope it works” into a practiced capability.

### Patterns

#### Retries (with backoff/jitter)

Retries handle transient failures (e.g., network blips) by attempting an operation again. Backoff and jitter spread retries over time so you don’t create a retry storm that amplifies an outage. Retries should be bounded and paired with timeouts.

#### Circuit breaker

A circuit breaker stops calling a failing dependency after a threshold of errors, so the caller fails fast instead of piling on. It protects the system during partial outages and gives downstream services time to recover. When conditions improve, the breaker gradually allows traffic again.

#### Rate limiting

Rate limiting caps request volume to protect services from overload and abusive clients. It helps preserve availability under spikes by forcing fairness and graceful degradation. Limits are often applied per user, per API key, or per endpoint.

## Motivation: from code to production

You wrote an application. Now what? Each real-world need leads to a DevOps tool or practice:

1. **You need infrastructure to be reproducible, reviewable, and recoverable** → You define it with **Infrastructure as Code (IaC)** (Terraform, Pulumi) so it can be versioned in Git and recreated from scratch.

2. **You need to get code changes to users safely and quickly** → You set up a **CI/CD pipeline** that automatically tests, builds, and deploys every change.

3. **Your app needs a clean, reproducible environment** → You package it in **Docker**. This guarantees it runs the same way on every machine — your laptop, a colleague's, or a server.

4. **You need to run many containers reliably** → You use **Kubernetes (K8s)** to orchestrate them: scheduling, scaling, self-healing, networking. K8s also runs your databases and supporting services.

5. **K8s needs machines and networking to run on** → You provision infrastructure in the **Cloud** (AWS, GCP, Azure) or on-prem hardware.

6. **Your app needs to store data** → You pick a **database** (PostgreSQL, Redis, Cassandra, etc. — depending on the workload).


Each layer solves a problem created by the previous one. Together, they form the stack that takes code from your editor to running in production.

---

## Reliability fundamentals

### SLIs/SLOs (what “good” looks like)

- **SLI**: a measured signal (e.g., % of HTTP 2xx, p95 latency).
- **SLO**: a target for an SLI (e.g., 99.9% success over 30 days).
- **Error budget**: how much failure you can “spend”; drives release speed vs stability.

### Deployment strategies

- **Rolling update**: replace instances gradually (common default).
- **Blue/green**: switch traffic between two environments (fast rollback).
- **Canary**: send small % of traffic to new version, then increase.

### Backups and restores

- Backups without restores are only a hope. Schedule restore drills.
- Define RPO/RTO targets (how much data you can lose / how fast to recover).

---

## Infrastructure as Code tools

IaC makes infrastructure reviewable and reproducible (like application code).

### Terraform (declarative IaC)

Typical workflow:

```bash
terraform fmt
terraform validate
terraform plan
terraform apply
terraform destroy
```

### Pulumi (IaC with general-purpose languages)

Typical workflow:

```bash
pulumi preview
pulumi up
pulumi destroy
```

### SOPS (encrypt secrets stored in Git)

SOPS encrypts YAML/JSON/env files so you can store them in Git safely (keys come from KMS/GPG/Age).

```bash
sops -e -i secrets.yaml
sops -d secrets.yaml | head
```

---

## CI/CD

- Flow: test → build → deploy (staging) → approve → deploy (prod)

### Gitlab CI/CD

## A typical delivery flow

Common pipeline stages (not all are mandatory on day 1):
- **Validate**: lint/format, unit tests, type checks.
- **Build**: compile, build Docker image, SBOM generation.
- **Security**: SAST, dependency scan, container scan, secret scan.
- **Deploy (staging)**: deploy automatically to a safe environment.
- **Test (staging)**: smoke/integration tests, basic performance checks.
- **Promote (prod)**: approval gate or automated promotion with progressive delivery.
- **Rollback**: automatic rollback on SLO breach, error rate spikes, or failed health checks.

Example `.gitlab-ci.yml` (minimal, illustrative):


```yaml
stages: [test, build, deploy_staging, approve_prod, deploy_prod]

test:
  stage: test
  image: alpine:3.20
  script:
    - echo "run unit tests here"

build:
  stage: build
  image: docker:27
  services: ["docker:27-dind"]
  variables:
    DOCKER_TLS_CERTDIR: ""
  script:
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"

deploy_staging:
  stage: deploy_staging
  image: alpine:3.20
  script:
    - echo "deploy to staging"

approve_prod:
  stage: approve_prod
  when: manual
  script:
    - echo "approval gate"

deploy_prod:
  stage: deploy_prod
  image: alpine:3.20
  script:
    - echo "deploy to production"
```

Notes:
- Real pipelines usually add caching, artifacts, environments, and protected variables.
- For Kubernetes deployments, the deploy jobs often run `helm upgrade --install ...` or `kubectl apply ...`.

---

## Shift right

Shift right means validating and improving software **after** it reaches production, using real traffic and real user behavior.

### A/B testing

A/B testing splits users into groups that see different variants (A vs B) and measures which performs better on a chosen metric (conversion, latency, engagement, etc.). It turns product decisions into data-driven experiments instead of guesses. Key ingredients: random assignment, sufficient sample size, and a clear success metric.

### Canary deployments

A canary deployment routes a small percentage of production traffic to the new version while the majority stays on the current one. If error rates, latency, or other SLIs stay healthy, traffic is gradually shifted until the new version takes 100%. If something breaks, only a small fraction of users are affected and rollback is immediate.

### Blue-green deployments

Blue-green keeps two identical production environments. One (blue) serves live traffic while the other (green) receives the new release. After the green environment is validated (health checks, smoke tests), traffic is switched over in one step. Rollback is just switching back. The tradeoff is cost — you pay for two full environments.

### Runtime security

Runtime security monitors and enforces security policies on running workloads, not just at build time. Examples include:
- **Container runtime policies**: detect unexpected syscalls, file access, or network connections inside containers.
- **Runtime application self-protection (RASP)**: in-app agents that block exploitation attempts (e.g., SQL injection) in real time.
