# Minimal signed Agent Card trust demo

Run from the repository root: `docker compose -f signed-card-demo/compose.yaml up --build --abort-on-container-exit`

- The fake Flask server uses the **existing** lab-CA-signed TLS certificate for `fake-server.test` (`ssl_context=(...)`), matching the pattern in `legit-server/app.py`. No TLS verification is disabled.
- `agent-card.json` is **static** and contains the attacker's Base64URL-encoded EC public-key coordinates directly in the JWS `protected` header's `jwk`. The signature was created **in advance** with the corresponding private key; no runtime key generation or signing.
- `demo.py` verifies that JWS using either the untrusted embedded key (ACCEPT) or the pre-provisioned legitimate public key `keys/legit.pub` (REJECT).
- Both cases validate TLS for `fake-server.test`; the CA does **not** certify that this agent represents `real-server.test`.
- Simplified A2A-shaped card: the signed JSON is restricted to simple ASCII and canonicalized with sorted JSON keys. This is illustrative, not a complete A2A conformance test.
- `fake.key` is a **test TLS private key**, not a JWS signing key. Never use these lab keys in production.

To inspect the embedded JWK:

```bash
python3 - <<'PY'
import json,base64
c=json.load(open('signed-card-demo/agent-card.json'))
s=c['signatures'][0]['protected']
print(json.dumps(json.loads(base64.urlsafe_b64decode(s+'='*(-len(s)%4))),indent=2))
PY
```
