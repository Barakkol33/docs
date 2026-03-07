# Guestbook — Solution

Complete solution for the Guestbook on Kubernetes exercise.

## Structure

```
solution/
  code/              # source code, Dockerfile, and frontend
    public/          #   shared HTML/JS frontend
    node/            #   Node.js backend + Dockerfile
    python/          #   Python backend + Dockerfile
    README.md        #   how to build the Docker image
  k8s/               # Kubernetes deployment via Helm
    guestbook-chart/ #   Helm chart with all K8s manifests
    README.md        #   how to deploy with Helm
```

## Quick start

### 1. Build the image

Pick Node.js or Python, then build and load:

```bash
cd code

# Copy frontend into build context
cp -r public node/public    # or: cp -r public python/public

# Build
cd node                     # or: cd python
docker build -t guestbook:dev .
cd ../..

# Load into kind
kind load docker-image guestbook:dev --name demo
```

See [code/README.md](code/README.md) for details and local testing.

### 2. Deploy with Helm

```bash
cd k8s
helm install guestbook ./guestbook-chart \
  --namespace guestbook --create-namespace
```

See [k8s/README.md](k8s/README.md) for configuration, upgrades, and uninstall.

### 3. Access the app

```bash
kubectl port-forward svc/guestbook 8080:80 -n guestbook
# Open http://localhost:8080
```

### 4. Verify

```bash
kubectl get all -n guestbook
kubectl logs -n guestbook -l app=guestbook --tail=5
helm list -n guestbook
curl -sS http://localhost:8080/api/messages | jq .
```

### 5. Cleanup

```bash
helm uninstall guestbook -n guestbook
kubectl delete ns guestbook
```
