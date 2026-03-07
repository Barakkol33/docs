# Exercise — Guestbook on Kubernetes

Build and deploy a Guestbook web application on Kubernetes. You'll complete the backend code, containerize it with Docker, deploy everything to a local kind cluster, seed test data with a Job, and package it all as a Helm chart.

**What's provided:**
- A complete HTML/JS frontend (`app/public/index.html`)
- A backend with 3 functions for you to fill in (choose **Node.js** or **Python**)

**What you'll build:**
- The missing backend logic (Redis connection + 2 API handlers)
- A Dockerfile for the app
- Kubernetes manifests: Namespace, ConfigMap, Secret, StatefulSet, Service, Deployment, Job
- A Helm chart that packages everything

```text
┌──────────┐     ┌─────────────────────┐     ┌──────────────────────┐
│ Browser  │────>│ Guestbook App (x2)  │────>│ Redis (StatefulSet)  │
│          │<────│ Deployment + Service │<────│ Headless Service     │
└──────────┘     └─────────────────────┘     └──────────────────────┘
                                                       ▲
                 ┌─────────────────────┐               │
                 │ Seed Job (one-off)  │───────────────┘
                 └─────────────────────┘
```

---

## Stage 1 — Explore the app

Before writing any code, read the source files and understand how they fit together.

**Tasks:**
1. Open `app/public/index.html` — read the JavaScript to understand:
   - What API endpoints does the frontend call?
   - What JSON shape does it send and expect?
2. Open the backend (`app/node/server.js` or `app/python/server.py`) — find the 3 TODO blocks.

> **Hints:**
> - The frontend calls `GET /api/messages` (expects a JSON array) and `POST /api/messages` (sends `{ name, text }`).
> - The backend uses Redis as a list — `LPUSH` to add, `LRANGE` to read.
> - The `/healthz` endpoint is already complete — it's used later for Kubernetes health checks.

---

## Stage 2 — Complete the backend

Choose either **Node.js** (`app/node/`) or **Python** (`app/python/`). Fill in the 3 TODO sections:

| TODO | What to implement |
|---|---|
| **TODO 1** | `connectToRedis()` / `connect_to_redis()` — create a Redis client using `DB_HOST` and `DB_PASSWORD` environment variables |
| **TODO 2** | `GET /api/messages` — read all messages from Redis (`LRANGE`) and return as JSON |
| **TODO 3** | `POST /api/messages` — validate input, create a message object with a timestamp, push to Redis (`LPUSH`), return it |

> **Hints:**
> - **Node.js:** Use the `redis` package. Create client with `` redis.createClient({ url: `redis://${host}:6379`, password }) ``. Connect with `await client.connect()`. List operations: `client.lPush(key, value)`, `client.lRange(key, 0, -1)`.
> - **Python:** Use the `redis` package. Create client with `redis.Redis(host=..., port=6379, password=..., decode_responses=True)`. List operations: `r.lpush(key, value)`, `r.lrange(key, 0, -1)`.
> - Environment variables: Node uses `process.env.DB_HOST`, Python uses `os.environ["DB_HOST"]`.
> - Each message stored in Redis is a JSON string: `{"name": "...", "text": "...", "timestamp": "..."}`.

---

## Stage 3 — Write the Dockerfile

Create a `Dockerfile` in your chosen language directory (`app/node/` or `app/python/`).

**Tasks:**
1. Write a Dockerfile that:
   - Starts from a slim base image
   - Sets a working directory
   - Copies dependency files and installs them
   - Copies the rest of the source code (including the `public/` folder)
   - Exposes port 3000
   - Defines the startup command
2. Build the image: `docker build -t guestbook:dev .`
3. (Optional) Test locally: `docker run --rm -p 3000:3000 -e DB_HOST=host.docker.internal -e DB_PASSWORD=test guestbook:dev`

> **Hints:**
> - Refer to the **Docker guide — Writing a Dockerfile** section.
> - **Node.js:** Base image `node:20-slim`. Install with `npm ci`. Start with `node server.js`. Copy `../public` to get the frontend.
> - **Python:** Base image `python:3.12-slim`. Install with `pip install -r requirements.txt`. Start with `python server.py`. Copy `../public` to get the frontend.
> - Key Dockerfile instructions: `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`.
> - Consider adding a `.dockerignore` to exclude `node_modules` or `__pycache__`.
> - **Bonus:** Use a multi-stage build to keep the final image small.

### Pro usage — get to know your image

Now that you've built an image, use the Docker tools you learned to really understand what's inside it:

```bash
# Inspect the image metadata — check the layers, env vars, exposed ports, entrypoint
docker image inspect guestbook:dev | jq '.[0] | {Config: .Config, RootFS: .RootFS.Layers | length}'
docker history guestbook:dev

# Run the container and poke around inside it
docker run -d --name guestbook-test -p 3000:3000 \
  -e DB_HOST=localhost -e DB_PASSWORD=test guestbook:dev

# Get a shell — explore the filesystem, check your files are where you expect
docker exec -it guestbook-test sh
# Inside the container:
#   ls -la                  # see the working directory
#   ls -la public/          # is the frontend there?
#   cat package.json        # or requirements.txt — are dependencies installed?
#   env | sort              # are the env vars set?
#   exit

# Check the logs — did the app try to start? What error did it show?
docker logs guestbook-test

# Check resource usage
docker stats guestbook-test --no-stream

# Inspect the running container — network settings, mounts, state
docker inspect guestbook-test | jq '.[0].State'
docker inspect guestbook-test | jq '.[0].NetworkSettings.Ports'

# Clean up
docker rm -f guestbook-test
```

The goal: you should be comfortable inspecting any image or container — not just ones you built.

---

## Stage 4 — Load image into kind

Kind runs its own container runtime, separate from your local Docker. You need to explicitly load your image.

```bash
kind load docker-image guestbook:dev --name demo
```

> **Hints:**
> - If you haven't created a kind cluster yet: `kind create cluster --name demo`
> - Verify the image is loaded: `docker exec -it demo-control-plane crictl images | grep guestbook`
> - In your Deployment YAML later, set `imagePullPolicy: Never` so Kubernetes uses the loaded image instead of trying to pull from a registry.

---

## Stage 5 — Kubernetes: Namespace + Config

Create YAML manifests for the foundational resources. You can put them all in one file or separate files.

**Tasks:**
1. **Namespace** — Create a namespace called `guestbook`.
2. **ConfigMap** — Store non-sensitive config:
   - `DB_HOST`: `redis.guestbook.svc.cluster.local` (the DNS name of the Redis headless Service you'll create next)
   - `LOG_LEVEL`: `info`
3. **Secret** — Store the Redis password.

> **Hints:**
> - Refer to the **K8s guide — Namespaces**, **ConfigMap**, and **Secret** sections.
> - Use `stringData` in the Secret so you don't have to base64-encode manually.
> - The `DB_HOST` value follows the Kubernetes DNS pattern: `<service>.<namespace>.svc.cluster.local`.
> - Apply with: `kubectl apply -f <file>`
> - Verify: `kubectl get ns`, `kubectl get configmap -n guestbook`, `kubectl get secret -n guestbook`

---

## Stage 6 — Kubernetes: Redis (StatefulSet)

Deploy Redis as a StatefulSet with persistent storage.

**Tasks:**
1. **Headless Service** — Create a Service named `redis` with `clusterIP: None` in the `guestbook` namespace.
2. **StatefulSet** — Create a StatefulSet named `redis`:
   - Image: `redis:7-alpine`
   - Command: `redis-server --requirepass <your-password>`
   - Port: 6379
   - `volumeClaimTemplates`: request 1Gi of storage, mount at `/data`
   - Resource requests and limits (e.g., 100m CPU / 128Mi memory)

> **Hints:**
> - Refer to the **K8s guide — StatefulSet**, **headless Service**, and **StorageClass / PVC** sections.
> - A StatefulSet requires `serviceName` to match the headless Service name.
> - The headless Service gives Redis a stable DNS name: `redis.guestbook.svc.cluster.local`.
> - The `volumeClaimTemplates` section goes at the StatefulSet level (not inside the container spec).
> - Set `selector.matchLabels` and `template.metadata.labels` to the same value (e.g., `app: redis`).
> - Verify: `kubectl get statefulset,pods,pvc,svc -n guestbook`
> - Test Redis connectivity:
>   ```bash
>   kubectl exec -it redis-0 -n guestbook -- redis-cli -a '<password>' PING
>   ```

---

## Stage 7 — Kubernetes: Deploy the app

Deploy the Guestbook application and expose it via a Service.

**Tasks:**
1. **Deployment** — Create a Deployment named `guestbook`:
   - Image: `guestbook:dev` (the one you built and loaded into kind)
   - `imagePullPolicy: Never`
   - Replicas: 2
   - Labels: `app: guestbook`
   - Inject the ConfigMap as environment variables
   - Inject the Redis password from the Secret as `DB_PASSWORD`
   - Container port: 3000
   - Resource requests and limits (e.g., 100m CPU / 128Mi memory)
2. **Service** — Create a ClusterIP Service named `guestbook`:
   - Port 80 → targetPort 3000
   - Selector: `app: guestbook`

> **Hints:**
> - Refer to the **K8s guide — Deployment**, **Service**, and **labels** sections.
> - To inject all ConfigMap keys as env vars, use `envFrom`:
>   ```yaml
>   envFrom:
>     - configMapRef:
>         name: <configmap-name>
>   ```
> - To inject a single Secret key, use `env` with `valueFrom`:
>   ```yaml
>   env:
>     - name: DB_PASSWORD
>       valueFrom:
>         secretKeyRef:
>           name: <secret-name>
>           key: <key-in-secret>
>   ```
> - Verify pods are running: `kubectl get pods -n guestbook -l app=guestbook`
> - Check logs: `kubectl logs -n guestbook -l app=guestbook --tail=20`
> - If pods crash, use `kubectl describe pod <pod> -n guestbook` — look at the Events section.

### Understanding check

Before moving on, make sure you can answer these questions. Try to answer from memory first, then verify with `kubectl` commands.

1. **What happens when you apply a Deployment?** Trace the full chain from `kubectl apply` to a running container. Which components are involved? *(API server, etcd, Deployment controller, ReplicaSet, scheduler, kubelet, container runtime)*
2. **You have 2 replicas. You delete one Pod manually.** What happens next and why? Which component is responsible for bringing it back?
3. **What's the difference between the Deployment, the ReplicaSet, and the Pods?** Run `kubectl get deploy,rs,pods -n guestbook -l app=guestbook` — explain the relationship you see.
4. **Why does the Service use `app: guestbook` as its selector?** What would happen if the labels on the Pods didn't match?
5. **How does the guestbook app find Redis?** Trace the path: `DB_HOST` env var (from ConfigMap) → Kubernetes DNS → headless Service → Redis Pod IP.

---

## Stage 8 — Seed data with a Job

Create a one-off Kubernetes **Job** that seeds the guestbook with test messages, so you can verify the full pipeline without using the browser.

**Tasks:**
1. Write a Job manifest named `seed-messages` in the `guestbook` namespace that:
   - Uses the `redis:7-alpine` image
   - Connects to Redis using the same ConfigMap and Secret as the app
   - Pushes 3 sample messages to the `messages` list (same JSON format the app uses: `{"name":"...","text":"...","timestamp":"..."}`)
   - Has `restartPolicy: Never`
2. Apply it and wait for completion.
3. Verify the messages show up through the app's API.

> **Hints:**
> - Refer to the **K8s guide — Jobs** section.
> - The container can run `redis-cli` directly:
>   ```bash
>   redis-cli -h $DB_HOST -a $DB_PASSWORD \
>     LPUSH messages '{"name":"seed","text":"Hello from Job!","timestamp":"2026-01-01T00:00:00Z"}'
>   ```
> - Inject `DB_HOST` from the ConfigMap and `DB_PASSWORD` from the Secret — same `envFrom` / `env` pattern as the Deployment.
> - Check Job status: `kubectl get jobs -n guestbook`
> - Check Job logs: `kubectl logs job/seed-messages -n guestbook`
> - Verify data through the app:
>   ```bash
>   kubectl port-forward svc/guestbook 8080:80 -n guestbook &
>   curl -sS http://127.0.0.1:8080/api/messages | jq .
>   kill %1
>   ```

---

## Stage 9 — Access the app

### Option A: Port-forward (quick)

```bash
kubectl port-forward svc/guestbook 8080:80 -n guestbook
```

Open http://127.0.0.1:8080 in your browser. You should see the Guestbook form with the seed messages already loaded. Post a new message and watch it appear.

### Option B: MetalLB + local DNS (bonus — real production feel)

1. Install MetalLB (refer to the **K8s guide — MetalLB** section).
2. Change the `guestbook` Service type to `LoadBalancer`.
3. Check the external IP: `kubectl get svc guestbook -n guestbook`
4. Add to `/etc/hosts`:
   ```bash
   echo "<EXTERNAL-IP> guestbook.local" | sudo tee -a /etc/hosts
   ```
5. Open http://guestbook.local in your browser.

> **Hints:**
> - Refer to the **K8s guide — Receiving real traffic locally with MetalLB** and **local DNS** sections.
> - Find the kind Docker network subnet: `docker network inspect kind -f '{{(index .IPAM.Config 0).Subnet}}'`
> - Clean up hosts entry when done: `sudo sed -i '/guestbook\.local/d' /etc/hosts`

### Pro usage — investigate your cluster

Now that everything is running, practice using the Kubernetes tools from the guides. This is the most important skill for day-to-day work.

**Inspect resources with kubectl + jq + grep:**

```bash
# Full overview of your namespace
kubectl get all -n guestbook

# Which images are running across all pods
kubectl get pods -n guestbook -o json | jq -r '.items[].spec.containers[].image' | sort -u

# Pod names and statuses in one line
kubectl get pods -n guestbook -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'

# Resource requests/limits for all containers
kubectl get pods -n guestbook -o json \
  | jq '.items[] | {pod: .metadata.name, containers: [.spec.containers[] | {name, resources}]}'

# Decode the Secret
kubectl get secret redis-auth -n guestbook -o json | jq -r '.data.password' | base64 -d; echo

# Recent events — scheduling, pulling, crashes
kubectl get events -n guestbook --sort-by=.metadata.creationTimestamp | tail -20

# Describe the Deployment — strategy, pod template, events
kubectl describe deploy/guestbook -n guestbook

# Check endpoints — is the Service actually pointing to pods?
kubectl get endpoints guestbook -n guestbook
```

**Read logs — your first stop for debugging:**

```bash
# All guestbook pods
kubectl logs -n guestbook -l app=guestbook --tail=20

# Follow logs in real time
kubectl logs -n guestbook -l app=guestbook -f

# Redis logs
kubectl logs -n guestbook redis-0 --tail=10

# Seed Job output
kubectl logs job/seed-messages -n guestbook

# If a pod is crash-looping, check the previous crash
kubectl logs -n guestbook <pod-name> --previous
```

**Exec into pods — verify from the inside:**

```bash
# Shell into a guestbook pod
kubectl exec -it deploy/guestbook -n guestbook -- sh
# Inside:
#   env | grep DB                                    # env vars injected?
#   curl localhost:3000/healthz                      # app responding?
#   nslookup redis.guestbook.svc.cluster.local       # DNS working?
#   exit

# Query Redis directly
kubectl exec -it redis-0 -n guestbook -- redis-cli -a '<password>' LRANGE messages 0 -1
```

**Use k9s:**

```bash
k9s -n guestbook
```

Navigate with `:pods`, `:deploy`, `:svc`, `:jobs`, `:events`. Press `l` for logs, `s` for shell, `d` for describe. Watch pods in real time.

**Break things and observe:**

```bash
# Delete a pod — watch the Deployment recreate it
kubectl delete pod -n guestbook -l app=guestbook --wait=false
kubectl get pods -n guestbook -w

# Scale up and back down
kubectl scale deploy/guestbook -n guestbook --replicas=4
kubectl get pods -n guestbook -l app=guestbook
kubectl scale deploy/guestbook -n guestbook --replicas=2
```

---

## Stage 10 — Package with Helm

Take the raw YAML manifests you wrote and package them into a reusable Helm chart, then deploy using Helm instead of `kubectl apply`.

**Tasks:**
1. Scaffold a new chart:
   ```bash
   helm create guestbook-chart
   ```
2. Delete the auto-generated templates — you'll use your own:
   ```bash
   rm -rf guestbook-chart/templates/*
   ```
3. Copy your YAML manifests into `guestbook-chart/templates/` (everything except the Namespace — Helm manages that via `--namespace --create-namespace`).
4. **Templatize at least these values** in `values.yaml` and reference them in the templates with `{{ .Values.xxx }}`:
   - `replicaCount` (Deployment replicas)
   - `image.repository` and `image.tag` (Deployment image)
   - `redis.password` (Secret and StatefulSet command)
5. Delete the existing namespace and redeploy using Helm:
   ```bash
   kubectl delete ns guestbook
   helm install guestbook ./guestbook-chart --namespace guestbook --create-namespace
   ```
6. Verify everything works the same as before.
7. Test an upgrade — change the replica count and upgrade:
   ```bash
   helm upgrade guestbook ./guestbook-chart -n guestbook --set replicaCount=3
   kubectl get pods -n guestbook -l app=guestbook
   ```

> **Hints:**
> - Refer to the **K8s guide — Helm** section.
> - After `helm create`, look at the generated `values.yaml` and `Chart.yaml` to understand the structure.
> - In templates, reference values like `{{ .Values.replicaCount }}` and `{{ .Values.redis.password }}`.
> - Use `helm template guestbook ./guestbook-chart` to preview the rendered YAML without applying.
> - Use `helm lint ./guestbook-chart` to check for errors.
> - To pass the password: `--set redis.password=p@ssword123` (or keep it in `values.yaml` for this exercise).
> - Check releases: `helm list -n guestbook`
> - Rollback if needed: `helm rollback guestbook 1 -n guestbook`

---

## Verification checklist

Run these commands to verify everything is working:

```bash
# All resources exist
kubectl get ns guestbook
kubectl get configmap,secret -n guestbook
kubectl get statefulset,deployment,svc,pods,jobs -n guestbook

# Redis is running and accessible
kubectl exec -it redis-0 -n guestbook -- redis-cli -a '<password>' PING
# Expected: PONG

# Seed Job completed
kubectl get jobs -n guestbook
# Expected: seed-messages  1/1

# App pods are running (2/2)
kubectl get pods -n guestbook -l app=guestbook
# Expected: 2 pods in Running state

# App logs look healthy
kubectl logs -n guestbook -l app=guestbook --tail=5
# Expected: "Guestbook server listening on port 3000"

# Helm release exists
helm list -n guestbook
# Expected: guestbook release with status "deployed"

# Functional test via port-forward
kubectl port-forward svc/guestbook 8080:80 -n guestbook &
curl -sS http://127.0.0.1:8080/api/messages | jq .
# Expected: array with seed messages
curl -sS -X POST http://127.0.0.1:8080/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"name":"test","text":"hello from curl"}'
curl -sS http://127.0.0.1:8080/api/messages | jq .
kill %1
```

---

## Cleanup

Uninstall via Helm and delete the namespace:

```bash
helm uninstall guestbook -n guestbook
kubectl delete ns guestbook
```

This removes the Helm release, the namespace, and all resources inside it.
