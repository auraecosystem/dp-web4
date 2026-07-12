import json
import hashlib
import uuid
import time

class JCT:

    VERSION = "1.0.0"

    def __init__(self, issuer, subject):

        self.header = {
            "alg": "Ed25519",
            "hash": "SHA3-512",
            "canonicalization": "JCS"
        }

        self.payload = {
            "jti": str(uuid.uuid4()),
            "iss": issuer,
            "sub": subject,
            "iat": int(time.time()),
            "claims": {}
        }

    def add_claim(self, key, value):
        self.payload["claims"][key] = value

    def digest(self):

        canonical = json.dumps(
            {
                "header": self.header,
                "payload": self.payload
            },
            sort_keys=True,
            separators=(",", ":")
        )

        return hashlib.sha3_512(
            canonical.encode()
        ).hexdigest()

    def export(self):

        return {
            "typ": "JCT",
            "ver": self.VERSION,
            "header": self.header,
            "payload": self.payload,
            "integrity": {
                "digest": self.digest()
            }
        }


token = JCT(
    "did:web:auraecosystem.org",
    "did:key:z6MkExample"
)

token.add_claim("presence", "verified")
token.add_claim("role", "developer")

print(json.dumps(token.export(), indent=4))
