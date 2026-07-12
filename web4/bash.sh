# Verify all elements compile cleanly without syntax exceptions
node -e "
const { LctCryptoCore } = require('./auraecosystem/ai-workspace/web4/src/identity/lct-crypto');
const keys = LctCryptoCore.generateKeyPair();
const claim = { agentId: 'test-agent', metabolism: { atp: 100 } };
const token = LctCryptoCore.signPayload(claim, keys.privateKey);
const isValid = LctCryptoCore.verifySignature(token, keys.publicKey);
console.log('--- CRYPTO PIPELINE VALIDATION ---');
console.log('Token Signed Successfully:', !!token);
console.log('ES256 Verification Result:', isValid ? 'PASS' : 'FAIL');
"
