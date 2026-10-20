import requests
import json
import base64

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

from pathlib import Path


URL = "https://fake-server.test:8443"
CA = "/app/certs/lab-ca.crt"


# Base64URL-decoding (the JWS signature is in Base64, so we need to decode it)
def unb64(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


# Get (forged) agent card from server
def get_agent_card():
    response = requests.get(
        URL + "/.well-known/agent-card.json",
        verify=CA,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


# Verify the JWS signature
def verify_card(card):

    sig = card["signatures"][0]

    # Read haeader and decode it
    protected = sig["protected"]
    header = json.loads(unb64(protected))

    # Get the JWK adress to the public key
    jwk = header["jwk"]

    if jwk["kty"] != "EC" or jwk["crv"] != "P-256":
        raise ValueError("Unsupported key type")

    x = int.from_bytes(unb64(jwk["x"]), "big")
    y = int.from_bytes(unb64(jwk["y"]), "big")

    public_key = ec.EllipticCurvePublicNumbers(
        x, y, ec.SECP256R1()
    ).public_key()

    # Remove signatures from agent card
    unsigned_card = {k: v for k, v in card.items() if k != "signatures"}

    payload = json.dumps(
        unsigned_card,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

    signing_input = (
        protected + "." +
        base64.urlsafe_b64encode(payload).rstrip(b"=").decode()
    ).encode()

    signature = unb64(sig["signature"])

    r = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:], "big")

    der_signature = encode_dss_signature(r, s)

    # Verify signature
    public_key.verify(
        der_signature,
        signing_input,
        ec.ECDSA(hashes.SHA256())
    )

    return True

def verify_trusted_signer(card):

    # Read the public key that the client trusts
    trusted_key_path = Path("/app/legitimate-public.pem")

    trusted_public_key = serialization.load_pem_public_key(
        trusted_key_path.read_bytes()
    )

    # Extract the public key supplied in the JWS header
    sig = card["signatures"][0]

    protected = sig["protected"]
    header = json.loads(unb64(protected))

    jwk = header["jwk"]

    x = int.from_bytes(unb64(jwk["x"]), "big")
    y = int.from_bytes(unb64(jwk["y"]), "big")

    supplied_public_key = ec.EllipticCurvePublicNumbers(
        x, y, ec.SECP256R1()
    ).public_key()

    # Compare the public keys: the ones presented in the agent card
    # and the one we have stored locally, mimicing a real public
    # key stored at a CA or similar
    trusted_bytes = trusted_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    supplied_bytes = supplied_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return trusted_bytes == supplied_bytes

card = get_agent_card()

print("Agent:", card["name"])
print("Description:", card["description"])

print("\n========== SCENARIO A ==========")
print("Naive JWS verification")

try:
    verify_card(card)

    print("[CLIENT] JWS signature: VALID")
    print("[CLIENT] Agent Card: ACCEPTED")

except InvalidSignature:
    print("[CLIENT] JWS signature: INVALID")
    print("[CLIENT] Agent Card: REJECTED")


print("\n========== SCENARIO B ==========")
print("JWS verification with trusted signer")

try:
    verify_card(card)

    print("[CLIENT] JWS signature: VALID")

    if verify_trusted_signer(card):
        print("[CLIENT] Signer identity: TRUSTED")
        print("[CLIENT] Agent Card: ACCEPTED")
    else:
        print("[CLIENT] Signer identity: UNTRUSTED")
        print("[CLIENT] Agent Card: REJECTED")

except InvalidSignature:
    print("[CLIENT] JWS signature: INVALID")
    print("[CLIENT] Agent Card: REJECTED")
