# Guestbook — Helm Chart

## Structure

```
k8s/
  guestbook-chart/
    Chart.yaml           # chart metadata
    values.yaml          # configurable values
    templates/
      configmap.yaml
      secret.yaml
      redis-service.yaml
      redis-statefulset.yaml
      guestbook-deployment.yaml
      guestbook-service.yaml
      seed-job.yaml
```

## Configurable values

| Value | Default | Description |
|---|---|---|
| `replicaCount` | `2` | Number of guestbook app replicas |
| `image.repository` | `guestbook` | Docker image name |
| `image.tag` | `dev` | Docker image tag |
| `image.pullPolicy` | `Never` | Image pull policy (Never for kind) |
| `redis.password` | `p@ssword123` | Redis password |
| `seed.enabled` | `true` | Whether to run the seed Job |

## Preview rendered templates

```bash
helm template guestbook ./guestbook-chart
```

## Lint

```bash
helm lint ./guestbook-chart
```

## Install

```bash
helm install guestbook ./guestbook-chart \
  --namespace guestbook --create-namespace
```

## Upgrade

```bash
# Change replica count
helm upgrade guestbook ./guestbook-chart \
  -n guestbook --set replicaCount=3

# Change image tag
helm upgrade guestbook ./guestbook-chart \
  -n guestbook --set image.tag=v2
```

## Uninstall

```bash
helm uninstall guestbook -n guestbook
kubectl delete ns guestbook
```
