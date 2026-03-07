# Software Developer

---

# General

## How to learn a technology

“Knowing” a technology usually means you can **use it**, **choose it**, and **debug it**.

### Basic level (black-box understanding)

Ask:

- **What is it?** One-sentence definition.
- **Why use it?** What problems does it solve well?
- **When not to use it?** Trade-offs, limits, risks.
- **How do you use it?** Minimal “hello world” + common operations.

Example: “PostgreSQL”

- What is it? A relational database you query using SQL.
- Why use it? Strong correctness, rich queries, mature ecosystem.
- When not? If you need a simple key-value store only, or extreme write scale with weaker consistency.
- How? Define tables, query data, add indexes, handle migrations/backups.

### Advanced level (glass-box understanding)

Ask:

- How does it work internally (performance, correctness, failure modes)?
- What happens under load (latency, bottlenecks)?
- How do you observe it (logs, metrics, traces) and troubleshoot it?

Deepest level (optional):

- Binary-level understanding (protocols, file formats, memory layout). Not always required, but very useful for debugging.

## Jobs / roles

### Web development

- **Frontend**: browser code (HTML/CSS/JavaScript). Focus: UI/UX, state, rendering, calling APIs.
- **Backend**: server code. Focus: APIs, data, security, reliability, performance.
- **Fullstack**: both sides.

### DevOps / platform / SRE

Focus: “how to run systems reliably”.

- Automated build/test/deploy (CI/CD)
- Infrastructure and networking
- Monitoring and incident response

### Backend: what’s important to know

**Code**

- One main language well enough to build services (e.g. Python / TypeScript).
- Build HTTP servers and understand request/response semantics.
- Configuration patterns:
  - YAML/JSON config files
  - environment variables
  - command-line flags
- Minimal frontend knowledge (enough to understand what the browser sends/needs).
- Git (daily workflow).

**Systems**

- Linux basics: files, processes, permissions.
- Networking: DNS, TCP/IP, HTTP.

**Data**

- SQL databases (tables, joins, indexes, transactions).
- Bonus: Elasticsearch (search), Kafka (event streaming), MongoDB (documents).

**Ops**

- Docker basics, Kubernetes basics, CI/CD basics.
- Cloud basics (AWS is common).

## A “good exercise” project: build a web app progressively

**Basic milestones**

1. Create a small web server with a few routes.
2. Serve HTML pages.
3. Organize code into modules/classes (avoid one giant file).
4. Add tests (unit tests + small integration tests).
5. Add configuration (YAML + env vars + CLI flags, and document the priority).
6. Add API routes that return JSON.
7. Add a SQL database and a minimal schema.
8. Add a background task (e.g. periodic cleanup).
9. Run it on Linux (or in Docker).

**Advanced milestones**

- CI pipeline: test → build → deploy.
- Add Elasticsearch and explain why search needs a different datastore.
- Split into microservices and use Kafka/RabbitMQ for async communication.
- Run locally with Docker and on Kubernetes (e.g. kind).
- Deploy to AWS (EC2 first, then EKS).
- Add TypeScript service to learn the ecosystem.

---

# Code

## Languages (and how to choose)

- **High-level** (Python, TypeScript): fast to develop, great ecosystem, common for web.
- **Low-level** (C/C++, Rust): performance and control, used for systems and tooling.
- **Nice to know**: Go (popular for backend/infrastructure).

Rule of thumb:

- Use high-level languages to ship features quickly.
- Learn low-level concepts to become better at debugging and performance thinking.

## What you should know in any language

### Variables and types

```py
user_name = "Avi"
age = 20
is_admin = False
```

### Conditions (if/else)

```py
if age >= 18:
    can_buy = True
else:
    can_buy = False
```

### Loops (for/while)

```py
for item in ["a", "b", "c"]:
    print(item)
```

### Lists and dictionaries

```py
orders = [{"id": 1}, {"id": 2}]
user = {"name": "Avi", "age": 20}
```

### Functions and modules

```py
def total_price(items):
    return sum(item["price"] for item in items)
```

Splitting into modules means: each file owns one responsibility (easier testing, easier reading).

### I/O and files (including JSON)

```py
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
```

### HTTP server and client (core backend skill)

You should be comfortable with:

- routes/paths (`/api/users/123`)
- methods (GET/POST/PUT/DELETE)
- status codes (200/400/401/404/500)
- headers (e.g. `Authorization`, `Content-Type`)

### Concurrency

Common models:

- **Async**: one thread handles many requests by switching when waiting (I/O-heavy workloads).
- **Threads/processes**: useful for CPU-heavy work or blocking code.

Good intuition:

- Most backend services are I/O-bound (DB/network), so async can help.
- CPU-bound work often needs parallelism (multiple processes/threads).

### Testing

Minimum goals:

- test core logic (unit tests)
- test one “happy path” end-to-end (integration test)
- test validation/error handling (bad inputs)

## Object Oriented Programming (OOP)

OOP is a way to organize code around objects with behavior.

- **Encapsulation**: hide details; expose a clean API.
- **Inheritance**: reuse and extend behavior (use carefully).
- **Polymorphism**: same interface, multiple implementations.

Example:

```py
class PaymentProvider:
    def charge(self, amount_cents: int) -> None:
        raise NotImplementedError


class StripeProvider(PaymentProvider):
    def charge(self, amount_cents: int) -> None:
        print(f"Charging via Stripe: {amount_cents}")
```

## Microservices

Microservices split one big system into several smaller services.

Example split:

- `users-service` (auth/users)
- `orders-service` (orders/payments)
- `menu-service` (items/prices)

Trade-offs:

- Pros: independent deploy/scale, clearer ownership.
- Cons: network failures, distributed debugging, data ownership complexity.

---

# Formats

## HTML and XML

HTML describes page structure (what the browser renders):

```html
<h1>Menu</h1>
<ul>
  <li>Pizza</li>
  <li>Salad</li>
</ul>
```

XML is similar in shape but used mostly for data exchange/config in older systems.

## JSON and YAML

### JSON (common for APIs)

```json
{
  "name": "Avi",
  "age": 20,
  "orders": [{ "id": 1 }, { "id": 2 }]
}
```

### YAML (common for configuration)

```yaml
server:
  port: 8080
database:
  url: postgres://localhost:5432/mydb
```

Rule of thumb:

- JSON: machine-to-machine (APIs).
- YAML: human-to-machine (config).

---

# IDEs

Minimum IDE skills:

- run with arguments and environment variables
- debug (breakpoints, step over/into, inspect variables)
- search across the repo
- use formatting/linting tools

---

# Git

Core concepts:

- **Repository**: the project.
- **Commit**: a snapshot in history.
- **Branch**: a line of development.
- **Working directory**: current files (may differ from last commit).
- **Staging area**: what will go into the next commit.

Typical workflow:

```bash
git checkout -b feature/add-login
git status
git add .
git commit -m "Add login endpoint"
git push -u origin feature/add-login
```

Nice to know:

- `git stash` (save work temporarily)
- `git log` / `git blame` (history)
- merge vs rebase (history management)

---

# Hardware

## Binary and bytes

- **bit**: `0` or `1`
- **byte**: 8 bits → values 0–255

## Endianness

Multi-byte numbers can be stored:

- **little-endian**: least-significant byte first
- **big-endian**: most-significant byte first

## Text storage: ASCII / Unicode / null terminator

- **ASCII**: mostly English letters/digits/symbols.
- **Unicode**: supports many languages (modern standard).
- C-style strings often end with `\0` (null terminator).

## CPU / RAM / disk

- **CPU** executes instructions.
- **RAM** stores running program data (fast, temporary).
- **Disk/SSD** stores files and databases (persistent).

---

# Operating Systems

## Concepts

### Process and threads

- **Process**: running instance of a program.
- **Threads**: execution units inside a process; share memory.

### Stack vs heap

- **Stack**: function call frames, local variables.
- **Heap**: longer-lived allocations (objects/data structures).

### Files

- Files contain arbitrary bytes (text or binary).
- Logs/config are usually text; images/executables are binary.

## Linux (practical basics)

### Bash

- `cd` change directory
- `pwd` show current directory
- `echo` print text

### Filesystem

- create: `touch file.txt`
- read: `cat file.txt`
- list: `ls -la`
- delete: `rm file.txt`
- permissions: `chmod +x run.sh`
- search text: `grep -R "hello" .`

### Processes

- list: `ps aux`
- stop: `Ctrl+C`
- kill: `kill <pid>`

Linux mindset: “everything is a file” (stdin/stdout, sockets, devices).

## Windows (practical basics)

Same concepts (processes, files, env vars) with different commands (CMD/PowerShell).

---

# Network

Backend development is mostly networked systems: client ↔ server ↔ database ↔ other services.

## OSI model (layered thinking)

Each layer provides a “service” to the layer above it.

### 1) Physical layer

- Moves bits over a medium (copper/fiber/radio).

### 2) Data link layer

- Moves frames on a local network.
- Devices: switches, Wi‑Fi access points.
- Addressing: MAC addresses.
- Protocols: Ethernet, Wi‑Fi.

### 3) Network layer

- Routes packets across networks (the internet).
- Protocol: IP (IPv4/IPv6).
- Devices: routers/gateways.
- Concepts: LAN, routing, NAT.

### 4) Transport layer

- Delivers data to the correct application (ports).
- **TCP**: reliable, ordered, connection-based.
- **UDP**: message-based, best-effort delivery.
- **Socket**: the programming interface to TCP/UDP.

### 5) Application layer

- Protocols for apps:
  - **HTTP**: web pages + APIs.
  - **DNS**: resolves names (`google.com`) to IP addresses.

HTTP mini example:

```http
GET /api/users/123 HTTP/1.1
Host: example.com
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "id": 123, "name": "Avi" }
```
