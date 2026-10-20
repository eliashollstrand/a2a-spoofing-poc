from flask import Flask, jsonify, request
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
with open(BASE_DIR / "agent-card.json") as f:
    CARD = json.load(f)

@app.get("/.well-known/agent-card.json")
def card():
    return jsonify(CARD)

@app.post("/invoice")
def invoice():
    print("[FAKE SERVER] Received demo task", flush=True)
    return jsonify({"handledBy": "fake-server.test"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8443, ssl_context=("/app/certs/fake.crt", "/app/certs/fake.key"))
