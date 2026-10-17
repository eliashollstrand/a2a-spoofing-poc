"""Legitimate A2A server. This emulates an agent which handles invoices.

  - Publishes its agent card at /.well-known/agent-card.json.
  - Handles incoming tasks at the endpoint advertised in that card (POST /invoice).
"""

from flask import Flask, jsonify, request
import os
USE_TLS = os.getenv("USE_TLS", "false").lower() == "true"
app = Flask(__name__)

if USE_TLS:
    AGENT_CARD = {
        "name": "Invoice Assistant",
        "supportedInterfaces": [
            {
                "url": "https://agent.invoice.test:443/invoice"
            }
        ],
    }
else:
    AGENT_CARD = {
        "name": "Invoice Assistant",
        "supportedInterfaces": [
            {
                "url": "http://agent.invoice.test:8080/invoice"
            }
        ],
    }

@app.get("/.well-known/agent-card.json")
def agent_card():
    return jsonify(AGENT_CARD)

@app.post("/invoice")
def handle_task():
    msg = request.get_json()
    text = msg["message"]["parts"][0]["text"]

    print(f"Received task: '{text}'", flush=True)

    return jsonify({
        "handledBy": "Legit Invoice Assistant",
        "result": "Processed invoice.",
    })

if __name__ == "__main__":
    if USE_TLS:
        ssl_context = ("/certs/server.crt", "/certs/server.key")
        app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)
    else:
        app.run(host="0.0.0.0", port=8080) # 0.0.0.0 so that the server can be reached from other docker containers
