import os
import json
from datetime import datetime, timezone

from flask import Flask, request, jsonify, send_from_directory
import redis

app = Flask(__name__, static_folder="public")

PORT = 3000


# TODO 1: Connect to Redis
def connect_to_redis():
    host = os.environ["DB_HOST"]
    password = os.environ["DB_PASSWORD"]
    return redis.Redis(host=host, port=6379, password=password, decode_responses=True)


r = connect_to_redis()


# Serve the frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# TODO 2: GET /api/messages
@app.route("/api/messages", methods=["GET"])
def get_messages():
    try:
        raw = r.lrange("messages", 0, -1)
        messages = [json.loads(item) for item in raw]
        return jsonify(messages)
    except Exception as e:
        print(f"GET /api/messages error: {e}")
        return jsonify({"error": "Failed to load messages"}), 500


# TODO 3: POST /api/messages
@app.route("/api/messages", methods=["POST"])
def post_message():
    try:
        body = request.get_json()
        name = (body.get("name") or "").strip()
        text = (body.get("text") or "").strip()
        if not name or not text:
            return jsonify({"error": "name and text are required"}), 400
        message = {
            "name": name,
            "text": text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        r.lpush("messages", json.dumps(message))
        return jsonify(message), 201
    except Exception as e:
        print(f"POST /api/messages error: {e}")
        return jsonify({"error": "Failed to save message"}), 500


# Health check
@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
