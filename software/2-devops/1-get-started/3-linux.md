# Linux — Practical Guide for DevOps

This is a reference of the Linux knowledge you'll use daily when working with Docker, Kubernetes, CI/CD pipelines, and infrastructure automation.

---

## Core philosophy

- **Everything is a file** — regular files, directories, devices, sockets, and even processes (`/proc`) are represented as files. This is why tools like `cat`, `grep`, and redirects work on so many things.
- **Small tools, composed together** — Linux commands do one thing well. You combine them with pipes (`|`) and redirects to build powerful workflows.
- **Text is the universal interface** — config files are text, logs are text, command output is text. Mastering text processing tools is the highest-leverage Linux skill for DevOps.

---

## Navigation and filesystem

```bash
pwd                        # where am I?
cd /var/log                # go to a directory
cd -                       # go back to previous directory
ls -la                     # list all files with details (permissions, size, owner)
ls -lah                    # same but human-readable sizes (KB, MB, GB)
tree -L 2                  # visual directory tree, 2 levels deep
```

### File operations

```bash
touch file.txt             # create empty file (or update timestamp)
mkdir -p a/b/c             # create nested directories
cp -r src/ dst/            # copy recursively
mv old.txt new.txt         # move / rename
rm file.txt                # delete file
rm -rf dir/                # delete directory recursively (careful!)
ln -s /path/to/target link # create symbolic link
```

### Viewing file contents

```bash
cat file.txt               # print entire file
head -n 20 file.txt        # first 20 lines
tail -n 50 file.txt        # last 50 lines
tail -f /var/log/syslog    # follow log in real time (like docker logs -f)
less file.txt              # scrollable viewer (q to quit)
wc -l file.txt             # count lines
```

### Searching

```bash
grep "error" app.log             # find lines containing "error"
grep -i "error" app.log          # case-insensitive
grep -r "TODO" src/              # recursive search in directory
grep -rn "pattern" .             # recursive + show line numbers
grep -c "error" app.log          # count matching lines
grep -v "debug" app.log          # invert — show lines NOT matching
```

### Finding files

```bash
find . -name "*.yaml"                  # find files by name
find . -name "*.log" -mtime +7         # files modified more than 7 days ago
find . -type f -size +100M             # files larger than 100MB
find /etc -name "*.conf" 2>/dev/null   # suppress permission errors
which kubectl                          # where is this binary?
```

---

## Permissions and ownership

Every file has an owner (user), a group, and permission bits (read/write/execute) for user, group, and others.

```bash
ls -la
# -rw-r--r-- 1 barak devs 4096 Mar 07 10:00 config.yaml
#  ^^^           user  group
#  user/group/others permissions
```

```bash
chmod +x script.sh         # make executable
chmod 755 script.sh        # rwxr-xr-x (common for scripts)
chmod 600 secrets.env      # rw------- (only owner can read/write)
chown barak:devs file.txt  # change owner and group
```

**Why this matters for Docker/K8s:** Container images often run as non-root. Permission issues are one of the most common reasons containers fail to start — the process can't read config files or write to mounted volumes.

---

## Pipes, redirects, and composition

This is where Linux becomes powerful. You chain commands together:

```bash
# Pipe: send output of one command to input of another
cat app.log | grep "error" | wc -l          # count error lines
kubectl get pods | grep -v Running           # find non-running pods
docker ps -a | grep Exited                   # find exited containers

# Redirects
echo "hello" > file.txt     # write to file (overwrite)
echo "world" >> file.txt    # append to file
command 2>/dev/null          # suppress stderr
command > out.log 2>&1       # redirect both stdout and stderr to file
command &>/dev/null          # discard all output
```

### Useful text processing

```bash
sort file.txt               # sort lines alphabetically
sort -n file.txt             # sort numerically
sort file.txt | uniq         # remove consecutive duplicates
sort file.txt | uniq -c      # count occurrences of each line
cut -d: -f1 /etc/passwd     # split by delimiter, take field 1
awk '{print $1, $3}' file   # print columns 1 and 3
sed 's/old/new/g' file.txt  # replace text (prints to stdout)
sed -i 's/old/new/g' file   # replace text in-place
```

**Real-world example** — find the top 10 most frequent error messages in a log:

```bash
grep "ERROR" app.log | awk '{$1=$2=$3=""; print $0}' | sort | uniq -c | sort -rn | head -10
```

---

## Process management

```bash
ps aux                      # list all processes
ps aux | grep nginx         # find a specific process
top                         # live process monitor (q to quit)
htop                        # better version of top (if installed)

kill <pid>                  # send SIGTERM (graceful shutdown)
kill -9 <pid>               # send SIGKILL (force kill, last resort)
killall nginx               # kill all processes by name

# Running processes in the background
./long-task.sh &            # run in background
nohup ./task.sh &           # run in background, survives terminal close
jobs                        # list background jobs
fg %1                       # bring job 1 to foreground
```

### Signals (important for Docker)

Docker sends `SIGTERM` to containers on `docker stop`, then `SIGKILL` after a timeout. Your app should handle `SIGTERM` for graceful shutdown (close connections, flush data).

```bash
# Trap signals in a bash script:
trap "echo 'shutting down'; exit 0" SIGTERM SIGINT
```

---

## Networking

Networking commands are essential for debugging Docker/K8s connectivity issues.

```bash
# What's listening on which port?
ss -tlnp                              # show listening TCP ports with process names
lsof -i :8080                         # what's using port 8080?

# DNS
nslookup google.com                   # resolve hostname
dig google.com                        # detailed DNS lookup
cat /etc/resolv.conf                  # DNS resolver config

# Connectivity
ping -c 3 google.com                  # basic connectivity check
curl -sS http://localhost:8080        # HTTP request (most used tool in DevOps)
curl -sS -o /dev/null -w "%{http_code}" http://localhost:8080   # just get status code
wget -qO- http://localhost:8080       # alternative to curl
nc -zv host 5432                      # test if a TCP port is open (netcat)

# Network interfaces and routing
ip addr show                          # list network interfaces and IPs
ip route                              # show routing table
```

**K8s debugging example** — from inside a pod, test if another service is reachable:

```bash
kubectl exec -it pod/myapp -- sh -c 'curl -sS http://db:5432 || echo "connection failed"'
kubectl exec -it pod/myapp -- sh -c 'nslookup db.default.svc.cluster.local'
```

---

## Disk and resource usage

```bash
df -h                       # disk usage per filesystem
du -sh /var/log/*           # size of each item in a directory
du -sh .                    # total size of current directory
free -h                     # memory usage
uptime                      # load averages
```

**Docker context:** `docker system df` shows Docker-specific disk usage, but `df -h` tells you if the host disk is full — a common cause of "no space left on device" errors in containers.

---

## Environment variables

Environment variables are how you pass configuration in Docker, K8s, and CI/CD.

```bash
env                         # list all environment variables
echo $HOME                  # print a specific variable
export MY_VAR="hello"       # set a variable (available to child processes)
unset MY_VAR                # remove a variable

# Set for a single command only
LOG_LEVEL=debug ./myapp

# Load from a file
source .env                 # or: . .env
export $(cat .env | xargs)  # export all variables from a file
```

---

## Bash scripting essentials

CI/CD pipelines, Docker entrypoints, and automation scripts are written in bash. Here's what you need:

### Script template

```bash
#!/usr/bin/env bash
set -euo pipefail    # exit on error, undefined vars, pipe failures

# -e: exit immediately if a command fails
# -u: treat unset variables as errors
# -o pipefail: a pipe fails if any command in it fails
```

`set -euo pipefail` should be at the top of every script. Without it, scripts silently continue after errors — a major source of bugs in CI pipelines.

### Variables and conditionals

```bash
NAME="world"
echo "hello $NAME"

# Conditionals
if [ -f "config.yaml" ]; then
  echo "config exists"
elif [ -d "/data" ]; then
  echo "data directory exists"
else
  echo "nothing found"
fi

# Common test operators:
# -f file     file exists and is regular
# -d dir      directory exists
# -z "$var"   variable is empty
# -n "$var"   variable is not empty
# "$a" = "$b" string equality
```

### Loops

```bash
# Loop over a list
for service in api worker scheduler; do
  echo "deploying $service"
  kubectl rollout restart deployment/"$service"
done

# Loop over command output
for pod in $(kubectl get pods -o name); do
  echo "checking $pod"
  kubectl describe "$pod" | tail -5
done

# While loop (e.g., wait for a condition)
while ! curl -sf http://localhost:8080/health; do
  echo "waiting for app..."
  sleep 2
done
echo "app is ready"
```

### Functions

```bash
deploy() {
  local service="$1"
  local version="$2"
  echo "deploying $service:$version"
  kubectl set image deployment/"$service" "$service=$service:$version"
}

deploy api v1.2.3
deploy worker v1.2.3
```

### Useful patterns

```bash
# Default value if variable is unset
REPLICAS="${REPLICAS:-3}"

# Exit with error message
die() { echo "ERROR: $*" >&2; exit 1; }
[ -f config.yaml ] || die "config.yaml not found"

# Run command and capture exit code
if kubectl get deployment/web &>/dev/null; then
  echo "deployment exists"
else
  echo "deployment not found"
fi
```

---

## systemd (service management)

On Linux servers, `systemd` manages services (like Docker itself).

```bash
systemctl status docker          # is Docker running?
systemctl start docker           # start it
systemctl stop docker            # stop it
systemctl restart docker         # restart
systemctl enable docker          # start on boot
systemctl disable docker         # don't start on boot
journalctl -u docker --tail=50   # view Docker daemon logs
journalctl -u kubelet -f         # follow kubelet logs (on K8s nodes)
```

---

## SSH (remote access)

```bash
ssh user@host                         # connect to remote machine
ssh -i ~/.ssh/key.pem user@host       # connect with specific key
scp file.txt user@host:/tmp/          # copy file to remote machine
scp user@host:/var/log/app.log .      # copy file from remote machine
ssh user@host 'kubectl get pods'      # run a command remotely
```

### SSH config (saves typing)

```bash
# ~/.ssh/config
Host myserver
  HostName 10.0.1.5
  User barak
  IdentityFile ~/.ssh/mykey.pem

# Now just:
ssh myserver
```

---

## Common DevOps one-liners

```bash
# Watch a command repeatedly (every 2 seconds)
watch -n 2 kubectl get pods

# Run something periodically in bash
while true; do curl -s http://localhost:8080/health; sleep 5; done

# JSON processing with jq
kubectl get pods -o json | jq '.items[].metadata.name'
docker inspect container_name | jq '.[0].NetworkSettings.IPAddress'
curl -s http://api/data | jq '.results[] | {name: .name, status: .status}'

# Base64 encode/decode (used in K8s Secrets)
echo -n "my-password" | base64
echo "bXktcGFzc3dvcmQ=" | base64 -d

# Generate a random password
openssl rand -base64 24

# Check if a port is available before starting a service
ss -tlnp | grep :8080 && echo "port in use" || echo "port free"

# Tar and compress / extract
tar czf backup.tar.gz /data/        # compress
tar xzf backup.tar.gz               # extract
tar xzf backup.tar.gz -C /target/   # extract to specific directory
```

---

## Key files and directories

| Path | Purpose |
|---|---|
| `/etc/` | System configuration files |
| `/var/log/` | Log files |
| `/proc/` | Virtual filesystem for process/kernel info |
| `/proc/<pid>/` | Info about a specific process |
| `/etc/hosts` | Local DNS overrides |
| `/etc/resolv.conf` | DNS resolver config (important in containers) |
| `/etc/environment` | System-wide environment variables |
| `~/.bashrc` | User shell config (aliases, exports) |
| `~/.ssh/` | SSH keys and config |
