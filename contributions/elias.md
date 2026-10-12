# Elias

I set up the project and built the baseline and attack for HTTP. This included the legitimate A2A agent (`legit-server`), which publishes its agent card to the standardised `/.well-known/agent-card.json` path and handles incoming tasks, and the client (`client`), which fetches that card and sends a task to the endpoint it advertises. On top of this I implemented the attack, where a DNS server (`evil-dns`) hijacks the domain lookup, and a malicious server (`evil-server`) serves a forged agent card and captures the victim’s data while replying exactly like the legitimate agent, so the client doesn't suspect anything. This is done using Docker Compose.

I implemented a minimal version of the A2A discovery flow by hand instead of using the official `a2a-sdk`. The vulnerability lies in the discovery step, meaning the client trusting the url field of a card it never verifies, so a simple client and server are enough to demonstrate it. Furthermore, in my implementation the agent card only includes a subset of the A2A fields rather than a full one, since many of them weren't important for this proof of concept. The attacker’s control over name resolution is faked using Docker Compose. On a real network this would instead be done via something like ARP spoofing, which we decided is outside the scope of our project.

Beyond these implementations, I also wrote an initial version of the project report (README) and a breakdown of the tasks that remained for the group.

**Notes on AI usage**
I have used an AI assistant as a tool for explanation, debugging, finding documentation, and boilerplate (e.g. the Dockerfiles and Compose setup, .gitignore). However, the server and client code, and written material are my own (with AI support for discussing and refining structure and language). I have reviewed and understood everything that was included.

Representative prompts:
- "Write a Dockerfile for my server" 
- "What library can I use to create a DNS server for spoofing?"
- "Give me a docker compose file for the attack setup"
- "Why use `host=0.0.0.0` in `app.run`?"
- "Why does my evil-dns crash with AttributeError 'NoneType' has no attribute 'header' ..."
- "Simplify this paragraph"
- "What can I use to create a flowchart in markdown?"