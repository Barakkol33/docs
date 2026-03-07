# Quick Reference — Linux, Docker, Kubernetes

A practical cheatsheet with the commands, patterns, and components you'll use most often.

---

## Linux

### Files and navigation

```bash
ls -lah                         # list with sizes and hidden files
tree -L 2                       # visual directory tree
find . -name "*.yaml"           # find files by name
grep -rn "error" .              # search content recursively with line numbers
wc -l file.txt                  # count lines
du -sh */                       # size of each subdirectory
df -h                           # disk usage per filesystem
```

### Text processing

```bash
cat app.log | grep "error" | wc -l                           # count error lines
grep -c "error" app.log                                       # same, shorter
sort file | uniq -c | sort -rn | head -10                     # top 10 most frequent lines
awk '{print $1, $3}' file                                     # print columns 1 and 3
sed 's/old/new/g' file                                        # replace text
cut -d: -f1 /etc/passwd                                       # split by delimiter, take field 1
```

### Processes

```bash
ps aux | grep nginx             # find a process
kill <pid>                      # graceful stop (SIGTERM)
kill -9 <pid>                   # force kill (SIGKILL)
lsof -i :8080                   # what's using port 8080
ss -tlnp                        # all listening TCP ports
```

### Networking

```bash
curl -sS http://localhost:8080                                # HTTP request
curl -sS -o /dev/null -w "%{http_code}" http://localhost:8080 # just the status code
nslookup google.com                                           # DNS lookup
nc -zv host 5432                                              # test if TCP port is open
ping -c 3 host                                                # basic connectivity
ip addr show                                                  # network interfaces
```

### Environment and scripting

```bash
env | sort                      # all environment variables
export MY_VAR="value"           # set variable
echo -n "secret" | base64       # base64 encode
echo "c2VjcmV0" | base64 -d    # base64 decode
openssl rand -base64 24         # generate random password
```

### jq (JSON processing)

```bash
cat data.json | jq '.name'                        # extract a field
cat data.json | jq '.items[] | {name, status}'    # reshape objects
cat data.json | jq -r '.items[].id'               # raw output (no quotes)
cat data.json | jq 'length'                        # count items in array
```

### Key paths

| Path | Purpose |
|---|---|
| `/etc/hosts` | Local DNS overrides |
| `/etc/resolv.conf` | DNS resolver config |
| `/var/log/` | System logs |
| `/proc/<pid>/` | Process info |
| `~/.bashrc` | Shell config |
| `~/.ssh/` | SSH keys and config |

---

## Docker

### Images

```bash
docker images                                 # list local images
docker pull nginx:stable                      # download an image
docker build -t myapp:dev .                   # build from Dockerfile
docker tag myapp:dev registry/myapp:v1        # retag
docker push registry/myapp:v1                 # upload to registry
docker rmi myapp:dev                          # remove image
docker image prune                            # remove dangling images
```

### Inspect images

```bash
docker history myapp:dev                                              # layers and sizes
docker image inspect myapp:dev | jq '.[0].Config.Env'                # env vars
docker image inspect myapp:dev | jq '.[0].Config.ExposedPorts'       # ports
docker image inspect myapp:dev | jq '.[0].Config.Cmd'                # default command
docker image inspect myapp:dev | jq '.[0].RootFS.Layers | length'   # layer count
```

### Run containers

```bash
docker run --rm hello-world                           # run and auto-remove
docker run -d --name web -p 8080:80 nginx:stable      # detached, named, with port
docker run --rm -v "$PWD":/work -w /work busybox ls   # bind mount current dir
docker run --rm -e MY_VAR=value myapp:dev              # pass env var
docker run --rm --network mynet myapp:dev              # attach to custom network
```

### Manage containers

```bash
docker ps                          # running containers
docker ps -a                       # all containers (including stopped)
docker stop web                    # graceful stop
docker start web                   # restart stopped container
docker rm -f web                   # force remove
docker container prune             # remove all stopped containers
```

### Debug containers

```bash
docker logs web --tail=50          # last 50 lines of output
docker logs -f web                 # follow logs in real time
docker exec -it web sh             # shell into running container
docker inspect web | jq '.[0].State'                    # check state (running/exited/error)
docker inspect web | jq '.[0].NetworkSettings.Ports'    # port mappings
docker port web                    # published ports
docker stats web --no-stream       # CPU/memory snapshot
docker stats                       # live resource usage for all containers
```

### Volumes and networks

```bash
docker volume create mydata        # create a volume
docker volume ls                   # list volumes
docker volume inspect mydata       # details
docker network create mynet        # create a network
docker network ls                  # list networks
```

### Compose

```bash
docker compose up -d               # start all services
docker compose ps                  # status
docker compose logs -f             # follow all logs
docker compose down -v             # stop and remove (including volumes)
```

### Cleanup

```bash
docker system df                   # disk usage summary
docker system prune                # remove all unused data
docker volume prune                # remove unused volumes (data loss!)
```

### Dockerfile reference

```dockerfile
FROM python:3.12-slim        # base image
WORKDIR /app                 # set working directory
COPY requirements.txt .      # copy dependency file (cached layer)
RUN pip install -r requirements.txt  # install deps
COPY . .                     # copy source code
EXPOSE 3000                  # document the port
CMD ["python", "main.py"]   # default command
```

**Best practices:** pin versions, order by change frequency, add `.dockerignore`, run as non-root.

---

## Kubernetes

### Architecture

| Component | Role |
|---|---|
| **API server** | Front door — all requests go through it |
| **etcd** | State store — holds all cluster data |
| **Scheduler** | Assigns pods to nodes |
| **Controller manager** | Reconciles desired vs actual state |
| **kubelet** | Node agent — runs pods on each node |
| **kube-proxy** | Networking rules on each node |
| **CoreDNS** | Cluster DNS — `<svc>.<ns>.svc.cluster.local` |

### Core objects

| Object | Purpose |
|---|---|
| **Namespace** | Isolation boundary (like a folder) |
| **Pod** | Smallest unit — one or more containers |
| **Deployment** | Manages stateless pods (rolling updates, scaling, self-healing) |
| **StatefulSet** | Stateful pods (stable names, per-pod storage, ordered startup) |
| **DaemonSet** | One pod per node (log collectors, monitoring) |
| **Job / CronJob** | Run-to-completion / scheduled tasks |
| **Service** | Stable endpoint for a set of pods |
| **ConfigMap** | Non-sensitive config (env vars, files) |
| **Secret** | Sensitive config (passwords, tokens) |
| **PVC** | Storage request |
| **Ingress** | HTTP routing from outside the cluster |
| **HPA** | Auto-scale replicas by CPU/memory |

### kubectl — view resources

```bash
kubectl get all -n <ns>                            # overview
kubectl get pods -o wide                           # pods with node and IP
kubectl get pods -l app=web                        # filter by label
kubectl get pods --show-labels                     # show all labels
kubectl get events --sort-by=.metadata.creationTimestamp | tail -20   # recent events
kubectl get deploy,rs,pods -l app=web              # full hierarchy
```

### kubectl — debug

```bash
kubectl describe deploy/web                        # details + events
kubectl describe pod/<pod>                         # scheduling, pull errors, crashes
kubectl logs deploy/web --tail=20                  # pod logs
kubectl logs <pod> --previous                      # logs from previous crash
kubectl logs -l app=web -f                         # follow all matching pods
kubectl exec -it deploy/web -- sh                  # shell into a pod
kubectl port-forward svc/web 8080:80               # tunnel to your machine
```

### kubectl — modify

```bash
kubectl apply -f manifest.yaml                     # create or update
kubectl diff -f manifest.yaml                      # preview changes
kubectl edit deploy/web                            # edit live
kubectl scale deploy/web --replicas=3              # scale
kubectl delete pod/<pod>                           # delete (Deployment recreates it)
kubectl delete ns <ns>                             # delete namespace + everything in it
```

### kubectl — extract data with jq

```bash
# All pod names
kubectl get pods -o json | jq -r '.items[].metadata.name'

# Pod name + status
kubectl get pods -o json | jq -r '.items[] | "\(.metadata.name) \(.status.phase)"'

# All container images
kubectl get pods -o json | jq -r '.items[].spec.containers[].image' | sort -u

# Resource requests/limits
kubectl get pods -o json | jq '.items[] | {pod: .metadata.name, containers: [.spec.containers[] | {name, resources}]}'

# Decode a secret
kubectl get secret my-secret -o json | jq -r '.data.password' | base64 -d

# Events for a specific pod
kubectl get events -o json | jq '.items[] | select(.involvedObject.name=="<pod>") | .message'
```

### Config injection patterns

```yaml
# All keys from ConfigMap as env vars
envFrom:
  - configMapRef:
      name: my-config

# Single key from Secret
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: my-secret
        key: password
```

### Service types

| Type | Access | Use case |
|---|---|---|
| `ClusterIP` | Internal only | Default, service-to-service |
| `NodePort` | Node IP + port | Dev/testing |
| `LoadBalancer` | External IP | Production (cloud or MetalLB) |
| `clusterIP: None` | DNS returns pod IPs | Headless, for StatefulSets |

### DNS

```text
<service>.<namespace>.svc.cluster.local   # full form
<service>                                  # short form (same namespace)
<pod-name>.<service>.<namespace>.svc.cluster.local   # specific pod (headless)
```

### Helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/nginx

helm install myapp ./chart -n <ns> --create-namespace   # install from local chart
helm install myapp bitnami/nginx -n <ns>                 # install from repo
helm upgrade myapp ./chart -n <ns>                       # upgrade
helm upgrade myapp ./chart -n <ns> --set replicaCount=3  # upgrade with override
helm list -n <ns>                                         # list releases
helm rollback myapp 1 -n <ns>                            # rollback to revision 1
helm uninstall myapp -n <ns>                              # remove

helm template myapp ./chart                # render YAML locally (preview)
helm lint ./chart                          # check for errors
helm create mychart                        # scaffold a new chart
```

### k9s

```bash
k9s                             # launch
k9s -n <namespace>              # launch in namespace
```

| Key | Action |
|---|---|
| `:pods` | Switch to pods view (also `:deploy`, `:svc`, `:ns`, `:jobs`, `:events`) |
| `/` | Filter/search |
| `Enter` | Inspect YAML |
| `l` | Logs |
| `s` | Shell |
| `d` | Describe |
| `ctrl-d` | Delete |
| `Esc` | Back |
| `:q` | Quit |

### Common debug flow

```text
1. kubectl get pods             — is it running? what state?
2. kubectl describe pod/<pod>   — events: scheduling, image pull, OOM, crash
3. kubectl logs <pod>           — application output
4. kubectl logs <pod> --previous — if crash-looping, check previous run
5. kubectl exec -it <pod> -- sh — get inside and investigate
6. kubectl get events           — cluster-level problems
```
