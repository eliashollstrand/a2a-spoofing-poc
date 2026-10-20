# Måns

I came across the A2A protocol and became interested in investigating its potential security weaknesses. After studying the official protocol specifications, Elias and I formulated three vulnerability hypotheses. Once Elias had built the testing codebase, I adapted and extended the code to investigate the specific vulnerabilities I was focusing on. I showed that a2a Agent Cards can accept a locally signed (=forged) Agent Card public key signature, and that it allows agents to store forged Agent Cards pointing to invalid addresses for at least a month (in reality there is no upper limit for how long the card can be cached, but in the test we only tested for 1 month).

**Notes on AI usage**
I have used an AI assistant mainly as a tool for research and discovery. I studied the a2a protocol specifications and used an AI assistant to bounce ideas and verify hypotheses. I also used an AI assistant to help me with the cryptographic logic required to implement digital signature verification with elliptic curve public keys.

Representative prompts:
- "Can you see any upper limits for how long an Agent Card can be stored in cache?"
- "I cannot see any end point verificaton mechanism, can you?"
- "How does the a2a protocol authenticate Agent Cards?"
- "How does agent card signature verification work, and how is the public key reconstructed from a JWK?"
- "How can I verify an Agent Card signature against a previously trusted public key?"
