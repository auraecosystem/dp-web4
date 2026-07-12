from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import hashlib
import json
import uuid

@dataclass
class UnifiedLCT:
    version: str = "1.0.0"

    lct_id: str = field(
        default_factory=lambda:
        f"urn:lct:{uuid.uuid4()}"
    )

    issuer: dict = field(default_factory=dict)
    subject: dict = field(default_factory=dict)
    presence: dict = field(default_factory=dict)
    proof: dict = field(default_factory=dict)
    integrity: dict = field(default_factory=dict)
    ledger: dict = field(default_factory=dict)
    permissions: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def canonical(self):
        return json.dumps(
            asdict(self),
            sort_keys=True,
            separators=(",", ":")
        )

    def digest(self):
        return hashlib.sha512(
            self.canonical().encode()
        ).hexdigest()


def create_lct(subject_id, issuer_id):

    now = datetime.now(timezone.utc).isoformat()

    lct = UnifiedLCT(
        issuer={
            "id": issuer_id
        },
        subject={
            "id": subject_id,
            "entityType": "human"
        },
        presence={
            "status": "active",
            "created": now,
            "updated": now
        },
        proof={
            "algorithm": "Ed25519",
            "signature": "",
            "publicKey": ""
        },
        integrity={
            "canonicalization": "JCS"
        },
        ledger={
            "network": "universal"
        },
        permissions={
            "read": True,
            "verify": True
        },
        metadata={}
    )

    lct.integrity["digest"] = lct.digest()

    return lct


if __name__ == "__main__":

    token = create_lct(
        "did:key:z6MkExample",
        "did:web:issuer.example"
    )

    print(json.dumps(asdict(token), indent=4))
