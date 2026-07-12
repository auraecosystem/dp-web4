{
  "$schema": "https://unifiedlct.org/schema/v1",
  "version": "1.0.0",
  "type": "UnifiedLCT",

  "lct_id": "urn:lct:550e8400-e29b-41d4-a716-446655440000",

  "issuer": {
    "id": "did:web:issuer.example",
    "name": "Example Authority",
    "publicKey": "ed25519:PUBLIC_KEY"
  },

  "subject": {
    "id": "did:key:z6Mk...",
    "entityType": "human",
    "displayName": "Alice"
  },

  "presence": {
    "status": "active",
    "created": "2026-07-12T22:40:05Z",
    "updated": "2026-07-12T22:40:05Z",
    "expires": null,
    "nonce": "6dc86f9d9cbe"
  },

  "proof": {
    "algorithm": "Ed25519",
    "hash": "SHA-512",
    "signature": "",
    "publicKey": ""
  },

  "integrity": {
    "canonicalization": "JCS",
    "digest": ""
  },

  "ledger": {
    "network": "universal",
    "chain": "agnostic",
    "blockHeight": null,
    "transaction": null
  },

  "permissions": {
    "read": true,
    "verify": true,
    "delegate": false,
    "transfer": false
  },

  "metadata": {
    "tags": [],
    "properties": {}
  }
}
