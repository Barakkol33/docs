const express = require("express");
const path = require("path");
const redis = require("redis");

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// TODO 1: Connect to Redis
let redisClient;

async function connectToRedis() {
  const host = process.env.DB_HOST;
  const password = process.env.DB_PASSWORD;
  redisClient = redis.createClient({
    url: `redis://${host}:6379`,
    password,
  });
  await redisClient.connect();
  console.log(`Connected to Redis at ${host}`);
}

// TODO 2: GET /api/messages
app.get("/api/messages", async (req, res) => {
  try {
    const raw = await redisClient.lRange("messages", 0, -1);
    const messages = raw.map((item) => JSON.parse(item));
    res.json(messages);
  } catch (err) {
    console.error("GET /api/messages error:", err.message);
    res.status(500).json({ error: "Failed to load messages" });
  }
});

// TODO 3: POST /api/messages
app.post("/api/messages", async (req, res) => {
  try {
    const { name, text } = req.body;
    if (!name || !text) {
      return res.status(400).json({ error: "name and text are required" });
    }
    const message = { name, text, timestamp: new Date().toISOString() };
    await redisClient.lPush("messages", JSON.stringify(message));
    res.status(201).json(message);
  } catch (err) {
    console.error("POST /api/messages error:", err.message);
    res.status(500).json({ error: "Failed to save message" });
  }
});

// Health check
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
