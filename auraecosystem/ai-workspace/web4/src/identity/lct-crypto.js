// auraecosystem/ai-workspace/web4/src/identity/lct-crypto.js
const crypto = require('crypto');

class LctCryptoCore {
  /**
   * Generates an ephemeral or permanent cryptographically secure P-256 Key Pair.
   */
  static generateKeyPair() {
    const { publicKey, privateKey } = crypto.generateKeyPairSync('ec', {
      namedCurve: 'P-256', // Standard NIST P-256 curve configuration
      publicKeyEncoding: { type: 'spki', format: 'pem' },
      privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
    });
    return { publicKey, privateKey };
  }

  /**
   * Signs a Web4 context payload package using ES256 (ECDSA + SHA-256)
   * @param {Object} claimSet - The data payload containing t3Tensor, coherence, and metabolism matrices
   * @param {string} privateKeyPem - The agent's private signing key string
   */
  static signPayload(claimSet, privateKeyPem) {
    const header = Buffer.from(JSON.stringify({ alg: "ES256", typ: "LCT" })).toString('base64url');
    const payload = Buffer.from(JSON.stringify({
      ...claimSet,
      timestamp: Date.now()
    })).toString('base64url');

    const signatureTarget = `${header}.${payload}`;
    
    // Instantiate SHA-256 sign stream pipeline
    const signer = crypto.createSign('SHA256');
    signer.update(signatureTarget);
    signer.end();

    // Generate cryptographic signature encoded in URL-safe base64
    const signature = signer.sign(privateKeyPem, 'base64url');

    return `${signatureTarget}.${signature}`;
  }

  /**
   * Verifies an incoming raw token string structure against a target public key.
   */
  static verifySignature(rawToken, publicKeyPem) {
    try {
      const parts = rawToken.split('.');
      if (parts.length !== 3) return false;

      const [header, payload, signature] = parts;
      const signatureTarget = `${header}.${payload}`;

      const verifier = crypto.createVerify('SHA256');
      verifier.update(signatureTarget);
      verifier.end();

      return verifier.verify(publicKeyPem, signature, 'base64url');
    } catch {
      return false; // Safely fail open on processing faults
    }
  }
}

module.exports = { LctCryptoCore };
