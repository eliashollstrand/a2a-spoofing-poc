"""Legitimate A2A server. This emulates an agent which handles invoices.

  - Publishes its agent card at /.well-known/agent-card.json.
  - Handles incoming tasks at the endpoint advertised in that card (POST /invoice).
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=8080) # 0.0.0.0 so that the server can be reached from other docker containers