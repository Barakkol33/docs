# Docker — Self-Learning Guide

This guide will walk you through Docker from the ground up. By the end, you'll understand what Docker is, why it exists, and how to use it day-to-day. Each section builds on the previous one, so work through them in order.

---

## What problem does Docker solve?

Imagine you wrote an application on your laptop. It works perfectly. You hand it to a colleague — it crashes. Why? Because their machine has a different OS, different library versions, or a missing dependency. This is the classic "it works on my machine" problem.

Docker solves this by packaging your application **together with everything it needs** (OS libraries, dependencies, config) into a single portable unit called an **image**. When you run that image, you get a **container** — an isolated process that behaves the same everywhere: your laptop, a test server, or production.

Think of it like shipping containers in the real world. Before standardized containers, loading cargo onto ships was chaos — every item had a different shape. Standardized containers made it possible to move anything, anywhere, on any ship. Docker does the same for software.

---

## Core terms you need to know

Before diving into commands, make sure you understand these building blocks:

- **Image** — A read-only template containing your app, its OS layers, and all dependencies. Think of it as a snapshot or a recipe. Images are built once and can be shared.
- **Container** — A running instance of an image. It's just a process on your machine, but with its own isolated filesystem, network, and process tree. You can run many containers from the same image.
- **Registry** — A remote store where images are uploaded and downloaded. [Docker Hub](https://hub.docker.com) is the most common public registry. Organizations often run private registries too.
- **Volume** — Managed persistent storage for containers. Since containers are ephemeral (they can be destroyed and recreated), volumes let you keep data across container restarts.
- **Bind mount** — Mounts a specific folder from your host machine into a container. This is especially useful during development, so you can edit code on your host and see changes inside the container immediately.
- **Network** — Docker creates virtual networks so containers can talk to each other (or be isolated from each other).

---

## Getting started: verify your installation

Before doing anything, make sure Docker is installed and running. These two commands tell you what version you have and whether the Docker daemon (background service) is active:

```bash
docker version
docker info
```

You should see output like this:

```text
Client: Docker Engine - Community
 Version:           26.1.0
Server: Docker Engine - Community
 Engine:
  Version:          26.1.0
```

If `docker version` shows a client but errors on the server section, the Docker daemon isn't running. Start it with `sudo systemctl start docker` (Linux) or open Docker Desktop (Mac/Windows).

---

## Working with images

Images are the foundation of everything in Docker. You either **pull** an existing image from a registry or **build** your own from a Dockerfile.

### Listing, pulling, and removing images

To see what images you already have locally:

```bash
docker images
```

```text
REPOSITORY   TAG      IMAGE ID       CREATED        SIZE
nginx        stable   8c1b...         2 weeks ago    192MB
```

To download an image from Docker Hub:

```bash
docker pull nginx:stable
```

The format is `name:tag`. The tag is a version label — `stable`, `latest`, `3.12-slim`, etc. If you omit the tag, Docker defaults to `latest`, but it's better to be explicit so you know exactly what you're running.

To remove an image you no longer need:

```bash
docker rmi nginx:stable
```

### Building your own image

When you have a `Dockerfile` (covered in detail later), you build an image like this:

```bash
docker build -t myapp:dev .
```

- `-t myapp:dev` gives the image a name and tag.
- `.` tells Docker to use the current directory as the **build context** (where it looks for your Dockerfile and source files).

```text
[+] Building 8.4s (9/9) FINISHED
 => naming to docker.io/library/myapp:dev
```

You can also re-tag an image (useful before pushing to a registry):

```bash
docker tag myapp:dev myuser/myapp:dev
```

### Inspecting an image

Want to see what's inside an image — its layers, environment variables, exposed ports? Use:

```bash
docker image inspect myapp:dev | head
docker history myapp:dev
```

`docker history` shows each layer (each instruction in the Dockerfile) and how much space it added. This is helpful when you're trying to make images smaller.

---

## Running containers

Now that you have images, let's run them. A container is simply a running image.

### Your first container

```bash
docker run --rm hello-world
```

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

What happened here:
1. Docker looked for the `hello-world` image locally.
2. It didn't find it, so it pulled it from Docker Hub automatically.
3. It created a container from that image, ran it, and printed the message.
4. `--rm` told Docker to automatically remove the container after it exited (cleanup).

### Running in the background (detached mode)

Most real services (web servers, databases) need to keep running. Use `-d` to run them in the background:

```bash
docker run -d --name web nginx:stable
```

- `-d` — detached mode (runs in background).
- `--name web` — gives the container a human-readable name instead of a random one.

Check what's running:

```bash
docker ps
```

```text
CONTAINER ID   IMAGE         COMMAND                  STATUS          NAMES
3c2a...        nginx:stable  "/docker-entrypoint..."  Up 10 seconds   web
```

`docker ps` only shows running containers. To see all containers (including stopped ones), use `docker ps -a`.

### Reading container logs

Containers write their output (stdout/stderr) to a log you can read:

```bash
docker logs web --tail=20    # last 20 lines
docker logs -f web           # follow (like tail -f) — press Ctrl+C to stop
```

Logs are your first stop when something isn't working. If a container crashes on startup, the logs usually tell you why.

### Getting a shell inside a container

Sometimes you need to poke around inside a running container — check files, test network connectivity, debug:

```bash
docker exec -it web sh
```

- `exec` runs a command inside an already-running container.
- `-it` gives you an interactive terminal.
- `sh` is the shell (some images have `bash`, others only `sh`).

You're now "inside" the container. Type `exit` to leave. The container keeps running — `exec` doesn't stop it.

### Stopping, starting, and removing containers

```bash
docker stop web      # gracefully stop (sends SIGTERM, then SIGKILL after timeout)
docker start web     # restart a stopped container
docker rm -f web     # force-remove (stops + deletes in one step)
```

### Inspecting a container

`docker inspect` is the Swiss army knife for debugging. It dumps all metadata about a container as JSON — network settings, mounts, environment variables, health status:

```bash
docker inspect web | head
docker port web         # show published ports
docker stats            # live CPU/memory/network usage (like top for containers)
```

---

## Ports: making containers accessible

By default, a container is isolated — you can't reach it from your host machine or the outside world. To expose a service, you **publish** ports.

```bash
docker run -d --name web -p 8080:80 nginx:stable
```

The syntax is `-p HOST_PORT:CONTAINER_PORT`. This means: "take traffic arriving on my host at port 8080 and forward it to port 80 inside the container."

Now you can access it:

```bash
curl -sS http://127.0.0.1:8080/ | head
```

```text
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```

**Tips:**
- `-p 8080:80` binds to all interfaces (reachable from your network). Use `-p 127.0.0.1:8080:80` to bind only to localhost (safer for dev).
- You can publish multiple ports: `-p 8080:80 -p 8443:443`.
- The container port is defined by the application inside the image (nginx uses 80 by default). The host port is whatever you choose.

---

## Persistent data: volumes and bind mounts

Containers are **ephemeral** — when you remove a container, its filesystem is gone. This is a feature, not a bug: it keeps things clean and reproducible. But what about data you need to keep (databases, uploads, config)?

That's where volumes and bind mounts come in.

### Volumes (Docker-managed storage)

Volumes are the recommended way to persist data. Docker manages them for you — they live in a Docker-controlled area on your host.

```bash
docker volume create mydata
docker volume ls
docker volume inspect mydata
```

Attach a volume to a container with `-v VOLUME_NAME:PATH_INSIDE_CONTAINER`:

```bash
docker run --rm -v mydata:/data busybox:1.36 sh -lc 'echo hello >/data/msg && cat /data/msg'
```

```text
hello
```

The data survives even after the container is removed. Prove it by running a new container that reads the same volume:

```bash
docker run --rm -v mydata:/data busybox:1.36 sh -lc 'cat /data/msg'
```

```text
hello
```

The key insight: the volume `mydata` exists independently of any container. Multiple containers can share the same volume.

### Bind mounts (host folder into container)

Bind mounts map a specific directory on your host into the container. This is ideal for development — you edit files on your host with your editor, and the container sees the changes immediately:

```bash
docker run --rm -v "$PWD":/work -w /work busybox:1.36 ls -la
```

- `-v "$PWD":/work` mounts your current directory into `/work` inside the container.
- `-w /work` sets the working directory inside the container to `/work`.

**When to use which:**
- **Volumes** — for production data, databases, anything the container "owns."
- **Bind mounts** — for development, when you want host files visible inside the container.

---

## Networking: connecting containers

When you run multiple containers (e.g., an app + a database), they need to talk to each other. Docker provides virtual networks for this.

### Why not just use localhost?

Each container has its own network namespace. From inside a container, `localhost` refers to itself, not to other containers. You need Docker networking to connect them.

### User-defined networks

The default `bridge` network works but has limitations (no automatic DNS). Create your own network for better behavior:

```bash
docker network create appnet
```

Now run containers on that network:

```bash
docker run -d --name redis --network appnet redis:7
docker run --rm --network appnet redis:7 redis-cli -h redis PING
```

```text
PONG
```

Notice that the second container reached Redis using the hostname `redis` — that's the container name. On user-defined networks, Docker provides automatic DNS resolution between containers. This is much cleaner than using IP addresses.

---

## Writing a Dockerfile (build recipes)

A Dockerfile is a text file with instructions for building an image. Each instruction creates a **layer** in the image. Docker caches layers, so unchanged steps are fast on subsequent builds.

### A simple example

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

Let's break this down line by line:

| Instruction | What it does |
|---|---|
| `FROM python:3.12-slim` | Start from an existing base image (Python 3.12 on a minimal Debian). Every Dockerfile starts with `FROM`. |
| `WORKDIR /app` | Set the working directory inside the image. All subsequent commands run from here. Creates the directory if it doesn't exist. |
| `COPY . .` | Copy everything from your build context (your project folder) into `/app` inside the image. |
| `RUN pip install -r requirements.txt` | Run a command during build. This installs your Python dependencies. The result is baked into the image layer. |
| `CMD ["python", "main.py"]` | The default command to run when a container starts from this image. |

### Multi-stage builds

A common problem: your build tools (compilers, dev dependencies) make the final image huge, but you only need the compiled output at runtime. Multi-stage builds solve this by using one stage to build and another for the final image:

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./...

FROM gcr.io/distroless/static
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```

The first stage (`build`) compiles the Go binary. The second stage starts from a tiny base image and copies only the compiled binary. The result: a final image that's often under 20MB instead of 1GB+.

### Best practices

- **Add a `.dockerignore` file** — just like `.gitignore`, it prevents unnecessary files (`.git`, `node_modules`, `venv`) from being sent to the build context. This speeds up builds and avoids leaking secrets.
- **Pin versions** — use specific tags (`python:3.12-slim`, not `python:latest`) so your builds are reproducible.
- **Order layers by change frequency** — put things that change rarely (installing OS packages) at the top and things that change often (copying your source code) at the bottom. This maximizes Docker's layer cache.
- **Run as non-root** — add `RUN useradd appuser` and `USER appuser` to avoid running your app as root inside the container.

---

## Registries: sharing images

Once you've built an image, you'll want to share it — with your team, your CI/CD pipeline, or your production servers. That's what registries are for.

```bash
docker login                            # authenticate (Docker Hub by default)
docker tag myapp:dev myuser/myapp:dev   # tag with your registry username
docker push myuser/myapp:dev            # upload to registry
docker pull myuser/myapp:dev            # download from registry (on another machine)
```

Organizations typically use private registries (AWS ECR, Google Artifact Registry, GitLab Container Registry) so images aren't publicly accessible.

---

## Docker Compose: running multi-container apps

Real applications rarely run as a single container. You usually have an app server, a database, maybe a cache. Docker Compose lets you define all of these in a single `docker-compose.yml` file and manage them together.

A typical `docker-compose.yml` might look like:

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: devpass

volumes:
  pgdata:
```

Then manage everything with:

```bash
docker compose up -d       # start all services in the background
docker compose ps          # see status of all services
docker compose logs -f     # follow logs from all services
docker compose down -v     # stop and remove everything (including volumes)
```

```text
[+] Running 2/2
 Container app-db-1   Started
 Container app-api-1  Started
```

Compose handles networking automatically — all services in the same compose file can reach each other by service name (e.g., the `api` container can connect to `db:5432`).

---

## Cleanup and troubleshooting

Over time, Docker accumulates unused images, stopped containers, and orphaned volumes. This eats disk space.

### Check disk usage

```bash
docker system df
```

### Prune unused resources

These commands delete things you're not using. Be careful — make sure you don't need them first:

```bash
docker image prune        # remove dangling (untagged) images
docker container prune     # remove all stopped containers
docker volume prune        # remove unused volumes (careful: data loss!)
docker system prune        # all of the above combined
```

### Common debug flow

When a container isn't behaving as expected, follow this sequence:

```bash
docker ps -a                          # 1. Is the container running? Did it exit?
docker logs <container> --tail=200    # 2. What did it print before dying?
docker inspect <container> | head     # 3. Check config, mounts, network, exit code
docker exec -it <container> sh        # 4. If it's running, get a shell and investigate
```

**Common issues and what to check:**
- Container exits immediately — check logs; often a missing env var or config file.
- "Port already in use" — another process (or container) is using that host port. Use `docker ps` or `lsof -i :PORT` to find it.
- Container can't reach another container — make sure they're on the same Docker network.
- Filesystem changes disappear — you're not using a volume. Container filesystems are ephemeral.

---

## How Docker relates to Kubernetes

Docker gets you from "code on my laptop" to "code running in a container." But in production, you often need to run many containers across many machines, handle failures, scale up/down, and route traffic. That's where Kubernetes comes in.

The relationship is straightforward:
- **Docker images** are still the artifact you build and push — Kubernetes doesn't replace this.
- **Kubernetes** takes those images and runs them as **Pods** (the smallest deployable unit, usually one container per Pod).
- Kubernetes adds orchestration on top: scheduling, scaling, self-healing, service discovery, load balancing, rolling updates, and more.

Think of Docker as the packaging and Kubernetes as the fleet management system.

---

## Under the hood: what Docker actually does

Containers feel like lightweight VMs, but they're fundamentally different. Understanding the internals helps you debug issues and reason about performance and security.

### A container is just a process

There is no container "machine." When you run `docker run nginx`, Docker starts a regular Linux process (nginx) on your host. The magic is that this process is **isolated** — it can't see other processes, has its own filesystem view, and thinks it's running alone. But from the host's perspective, it's just a process you can see with `ps aux`.

### Isolation: namespaces

Linux **namespaces** provide the isolation. Each container gets its own:

- **PID namespace** — the container sees only its own processes (PID 1 is the main app).
- **Network namespace** — its own IP address, ports, and routing table.
- **Mount namespace** — its own filesystem tree.
- **UTS namespace** — its own hostname.
- **User namespace** — can map container root to a non-root user on the host.

This is why a container feels like a separate machine — it literally can't see anything outside its namespaces.

### Resource limits: cgroups

**cgroups** (control groups) limit how much CPU, memory, and I/O a container can use. When you set `--memory=512m` or `--cpus=1.5`, Docker creates a cgroup with those limits. If a container exceeds its memory limit, the kernel kills it (OOMKilled) — a very common issue you'll encounter in production and Kubernetes.

### Images are layered filesystems

A Docker image isn't a single file — it's a stack of read-only **layers**. Each Dockerfile instruction (`FROM`, `RUN`, `COPY`) creates a new layer containing only the changes from the previous one.

```text
Layer 4: COPY . .              (your app code)
Layer 3: RUN pip install ...   (installed packages)
Layer 2: WORKDIR /app          (metadata change)
Layer 1: FROM python:3.12-slim (base OS + Python)
```

When you run a container, Docker adds a thin **read-write layer** on top. Any file changes inside the container go to this layer. When the container is removed, this layer is discarded — that's why container filesystems are ephemeral.

**Why layers matter:**
- **Caching** — If a layer hasn't changed, Docker reuses it on the next build. This is why putting `COPY requirements.txt` before `COPY . .` speeds up builds: dependencies are cached separately from code.
- **Sharing** — If 10 containers run the same image, they share all the read-only layers. Only the thin writable layer is unique per container. This is why containers start instantly and use little disk.
- **Storage drivers** — Docker uses a union filesystem (OverlayFS on most systems) to stack these layers into a single coherent view.

### Putting it all together

A container = a regular Linux process + namespace isolation + cgroup resource limits + a layered filesystem. No hypervisor, no separate kernel, no VM overhead. This is why containers start in milliseconds and have near-zero performance overhead compared to running the same process directly on the host.
