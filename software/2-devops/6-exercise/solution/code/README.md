# Guestbook — Source Code & Docker Image

## Structure

```
code/
  public/          # shared frontend (HTML/JS)
  node/            # Node.js backend solution + Dockerfile
  python/          # Python backend solution + Dockerfile
```

Both backends serve the same `public/` folder and expose the same API.

## Build the Docker image

Choose one language. Run from the language directory:

### Node.js

```bash
# Copy the shared frontend into the build context
cp -r ../public node/public

# Build
cd node
docker build -t guestbook:dev .
```

### Python

```bash
# Copy the shared frontend into the build context
cp -r ../public python/public

# Build
cd python
docker build -t guestbook:dev .
```

## Test locally (optional)

You need a running Redis to test. The easiest way:

```bash
# Start Redis
docker network create guestbook-test
docker run -d --name redis-test --network guestbook-test redis:7-alpine redis-server --requirepass testpass

# Run the app
docker run --rm --name guestbook-test --network guestbook-test \
  -p 3000:3000 \
  -e DB_HOST=redis-test \
  -e DB_PASSWORD=testpass \
  guestbook:dev

# Open http://localhost:3000 in your browser

# Cleanup
docker rm -f redis-test guestbook-test
docker network rm guestbook-test
```

## Load into kind

```bash
kind load docker-image guestbook:dev --name demo
```
