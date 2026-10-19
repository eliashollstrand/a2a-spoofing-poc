"""A2A client. Discovers an agent via its well-known card, then sends it a task."""

import requests
import os
#TARGET = "agent.invoice.test:8080"

MESSAGE = "Pay invoice #1337 to John Doe: 1,000,000 SEK to account SE12 3456 7890"

USE_TLS = os.getenv("USE_TLS", "false").lower() == "true"
if USE_TLS:
    PROTOCOL = "https"
    TARGET = "agent.invoice.test:443"
    VERIFY = "/certs/server.crt"
else:
    PROTOCOL = "http"
    TARGET = "agent.invoice.test:8080"
    VERIFY = False

def discover(target):
    url = f"{PROTOCOL}://{target}/.well-known/agent-card.json"
    print(f"Fetching agent card from {url}")
    response = requests.get(url, verify=VERIFY)
    return response.json()

def send_task(card, text):
    endpoint = card["supportedInterfaces"][0]["url"]
    print(f"Card says endpoint is: {endpoint}")
    print(f"Sending task there...")

    payload = {"message": {"parts": [{"text": text}]}}
    response = requests.post(endpoint, json=payload, verify=VERIFY)
    return response.json()

def main():
    try:
        card = discover(TARGET)
        print(f"Discovered agent: {card["name"]}")

        result = send_task(card, MESSAGE)
        print(f"Response: {result}")
        print(f"Task handled by: {result["handledBy"]}") # Who the client thinks handled the task
    except requests.exceptions.ConnectionError:
        print(f"Failed to establish a connection, invalid certificate")
if __name__ == "__main__":
    main()
