# Prerequisites — Offline Setup

Run these steps **while you have internet** so everything is cached locally. After this, the guides can be followed fully offline.

## 0. Markdown viewer

The guides are written in markdown. To read them comfortably, use one of these:

- **Obsidian** — open the `docs/` folder as a vault. Best reading experience with sidebar navigation.
- **VS Code** — open any `.md` file and press `Ctrl+Shift+V` (or click the preview icon in the top-right) to see the rendered view.

Either works. The important thing is that you're not reading raw markdown — tables, code blocks, and formatting are much easier to follow in a rendered view.

---

## 1. Install tools

### Linux

```bash
# Docker
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
# Log out and back in for the group change to take effect

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl && rm kubectl

# kind
curl -Lo kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
sudo install kind /usr/local/bin/kind && rm kind

# Helm
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# k9s (optional but recommended)
curl -Lo k9s.tar.gz https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz
tar xzf k9s.tar.gz k9s && sudo install k9s /usr/local/bin/k9s && rm k9s k9s.tar.gz

# jq (used in examples)
sudo apt-get install -y jq
```

### macOS

```bash
# Docker — install Docker Desktop from https://docs.docker.com/desktop/setup/install/mac-install/
# Docker Desktop includes Docker Engine, Docker CLI, and Docker Compose

# kubectl
brew install kubectl

# kind
brew install kind

# Helm
brew install helm

# k9s (optional but recommended)
brew install derailed/k9s/k9s

# jq (used in examples)
brew install jq
```

### Windows

Install [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) first — all guides and commands assume a Linux shell:

```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart, then open the Ubuntu terminal for all remaining steps
```

Then install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) with the **WSL 2 backend** enabled (Settings → General → "Use the WSL 2 based engine"). Docker Desktop makes the `docker` command available inside WSL automatically.

Once inside WSL, install the remaining tools using the **Linux** instructions above.

---

## 2. Pull Docker images

These images are used across the guides and exercise:

```bash
# Docker guide
docker pull hello-world
docker pull nginx:stable
docker pull busybox:1.36
docker pull redis:7
docker pull postgres:16

# K8s guide — kind node image (matches kind v0.27.0)
docker pull kindest/node:v1.32.2

# K8s guide — used in examples
docker pull redis:7-alpine
docker pull python:3.12-slim
docker pull python:3.9-slim
docker pull node:20-slim

# Helm example
docker pull bitnami/nginx
```

---

## 3. Cache Helm chart (optional)

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm pull bitnami/nginx --untar -d /tmp/helm-cache
```

---

## 4. Install npm/pip dependencies for the exercise

The exercise app has both Node.js and Python options. Install dependencies for whichever you plan to use:

```bash
# Node.js
cd docs/2-devops/6-exercise/app/node
npm install
cd -

# Python
cd docs/2-devops/6-exercise/app/python
pip install -r requirements.txt
cd -
```
