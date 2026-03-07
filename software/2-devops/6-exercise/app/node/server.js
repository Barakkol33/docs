const express = require("express");
const path = require("path");
const redis = require("redis");

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, "..", "public")));

// ---------------------------------------------------------------------------
// TODO 1: Connect to Redis
//
// Create a Redis client using environment variables and connect to it.
//
// Environment variables available (injected by Kubernetes):
//   - DB_HOST:     the Redis hostname (e.g., "redis.guestbook.svc.cluster.local")
//   - DB_PASSWORD: the Redis password
//
// Steps:
//   1. Read DB_HOST and DB_PASSWORD from process.env
//   2. Create a Redis client with: redis.createClient({ url, password })
//      - The url format is: redis://<host>:6379
//   3. Connect to Redis with: await client.connect()
//   4. Return the client
//
// Redis docs: https://www.npmjs.com/package/redis
// ---------------------------------------------------------------------------
let redisClient;

async function connectToRedis() {
  // === YOUR CODE HERE ===

  // === END YOUR CODE ===
}

// ---------------------------------------------------------------------------
// TODO 2: GET /api/messages — return all messages
//
// Read messages from Redis and return them as a JSON array.
//
// Steps:
//   1. Use redisClient.lRange("messages", 0, -1) to get all items from the list
//   2. Each item is a JSON string — parse it with JSON.parse()
//   3. Return the parsed array as the response with res.json(...)
//
// Redis command reference: LRANGE key start stop
// ---------------------------------------------------------------------------
app.get("/api/messages", async (req, res) => {
  try {
    // === YOUR CODE HERE ===

    // === END YOUR CODE ===
  } catch (err) {
    console.error("GET /api/messages error:", err.message);
    res.status(500).json({ error: "Failed to load messages" });
  }
});

// ---------------------------------------------------------------------------
// TODO 3: POST /api/messages — store a new message
//
// Validate the input, build a message object, and push it to Redis.
//
// The request body (req.body) contains: { name: string, text: string }
//
// Steps:
//   1. Extract name and text from req.body
//   2. Validate: both must be non-empty strings. If invalid, return:
//      res.status(400).json({ error: "name and text are required" })
//   3. Build a message object: { name, text, timestamp: new Date().toISOString() }
//   4. Push it to Redis: redisClient.lPush("messages", JSON.stringify(message))
//      - lPush adds to the front of the list (newest first)
//   5. Return the message: res.status(201).json(message)
//
// Redis command reference: LPUSH key value
// ---------------------------------------------------------------------------
app.post("/api/messages", async (req, res) => {
  try {
    // === YOUR CODE HERE ===

    // === END YOUR CODE ===
  } catch (err) {
    console.error("POST /api/messages error:", err.message);
    res.status(500).json({ error: "Failed to save message" });
  }
});

// Health check (useful for Kubernetes readiness/liveness probes)
app.get("/healthz", (req, res) => {
  res.json({ status: "ok" });
});

// Start server
async function main() {
  await connectToRedis();
  app.listen(PORT, () => {
    console.log(`Guestbook server listening on port ${PORT}`);
  });
}

main().catch((err) => {
  console.error("Failed to start:", err.message);
  process.exit(1);
});
