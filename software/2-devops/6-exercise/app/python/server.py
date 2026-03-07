import os
import json
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_from_directory
import redis

app = Flask(__name__, static_folder=os.path.join("..", "public"))

PORT = 3000

# ---------------------------------------------------------------------------
# TODO 1: Connect to Redis
#
# Create a Redis client using environment variables.
#
# Environment variables available (injected by Kubernetes):
#   - DB_HOST:     the Redis hostname (e.g., "redis.guestbook.svc.cluster.local")
#   - DB_PASSWORD: the Redis password
#
# Steps:
#   1. Read DB_HOST and DB_PASSWORD from os.environ
#   2. Create a Redis client with: redis.Redis(host=..., port=6379, password=..., decode_responses=True)
#      - decode_responses=True makes Redis return strings instead of bytes
#   3. Return the client
#
# Redis docs: https://redis-py.readthedocs.io/
# ---------------------------------------------------------------------------
def connect_to_redis():
    # === YOUR CODE HERE ===
    pass
    # === END YOUR CODE ===


r = connect_to_redis()


# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ---------------------------------------------------------------------------
# TODO 2: GET /api/messages — return all messages
#
# Read messages from Redis and return them as a JSON array.
#
# Steps:
#   1. Use r.lrange("messages", 0, -1) to get all items from the list
#   2. Each item is a JSON string — parse it with json.loads()
#   3. Return the parsed list with jsonify(...)
#
# Redis command reference: LRANGE key start stop
# ---------------------------------------------------------------------------
@app.route("/api/messages", methods=["GET"])
def get_messages():
    try:
        # === YOUR CODE HERE ===
        pass
        # === END YOUR CODE ===
    except Exception as e:
        print(f"GET /api/messages error: {e}")
        return jsonify({"error": "Failed to load messages"}), 500


# ---------------------------------------------------------------------------
# TODO 3: POST /api/messages — store a new message
#
# Validate the input, build a message dict, and push it to Redis.
#
# The request body (request.get_json()) contains: { "name": str, "text": str }
#
# Steps:
#   1. Get the JSON body with request.get_json()
#   2. Extract "name" and "text", strip whitespace
#   3. Validate: both must be non-empty. If invalid, return:
#      jsonify({"error": "name and text are required"}), 400
#   4. Build a message dict: {"name": name, "text": text, "timestamp": <ISO format UTC>}
#      - Use: datetime.now(timezone.utc).isoformat()
#   5. Push to Redis: r.lpush("messages", json.dumps(message))
#      - lpush adds to the front of the list (newest first)
#   6. Return the message: jsonify(message), 201
#
# Redis command reference: LPUSH key value
# ---------------------------------------------------------------------------
@app.route("/api/messages", methods=["POST"])
def post_message():
    try:
        # === YOUR CODE HERE ===
        pass
        # === END YOUR CODE ===
    except Exception as e:
        print(f"POST /api/messages error: {e}")
        return jsonify({"error": "Failed to save message"}), 500


# Health check (useful for Kubernetes readiness/liveness probes)
@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
