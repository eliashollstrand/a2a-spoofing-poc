"""A2A client. Discovers an agent via its well-known card, then sends it a task."""

import requests

TARGET = "agent.invoice.test:8080"

MESSAGE = "Pay invoice #1337 to John Doe: 1,000,000 SEK to account SE12 3456 7890"

def discover(target):
    url = f"http://{target}/.well-known/agent-card.json"
    print(f"Fetching agent card from {url}")
    response = requests.get(url)
    return response.json()

def send_task(card, text):
    endpoint = card["supportedInterfaces"][0]["url"]
    print(f"Card says endpoint is: {endpoint}")
    print(f"Sending task there...")

    payload = {"message": {"parts": [{"text": text}]}}
    response = requests.post(endpoint, json=payload)
    return response.json()

def main():
    card = discover(TARGET)
    print(f"Discovered agent: {card["name"]}")

    result = send_task(card, MESSAGE)
    print(f"Response: {result}")
    print(f"Task handled by: {result["handledBy"]}") # Who the client thinks handled the task

if __name__ == "__main__":
    main()