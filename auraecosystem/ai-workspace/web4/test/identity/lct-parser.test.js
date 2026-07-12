// auraecosystem/ai-workspace/web4/test/identity/lct-parser.test.js
const { LctParser } = require('../../src/identity/lct-parser');
const assert = require('assert');

// Utility tool helper to transform objects into mock raw network tokens
function createMockToken(payloadObject) {
  const header = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9"; // Mock Fixed algorithm header
  const payload = Buffer.from(JSON.stringify(payloadObject)).toString('base64');
  const signature = "mock_signature_bytes";
  return `${header}.${payload}.${signature}`;
}

describe("Web4 Identity: Linked Context Token (LCT) Parser Integration Suite", () => {
  let parser;

  beforeEach(() => {
    parser = new LctParser({ strictMode: true, minTrustBoundary: 0.5 });
  });

  it("should successfully parse a valid, high-trust identity token structure", () => {
    const validData = {
      agentId: "agent-cooperator-alpha",
      signature: "crypto-sig-valid",
      t3: { competence: 0.9, reliability: 0.9, integrity: 0.8, alignment: 0.9, transparency: 0.9 },
      coherence: { spatial: 1.0, capability: 1.0, temporal: 1.0, relational: 1.0 },
      metabolism: { atp: 120, adp: 5, burnRate: 1.2 }
    };

    const rawToken = createMockToken(validData);
    const parsed = parser.parse(rawToken);

    assert.strictEqual(parsed.agentId, "agent-cooperator-alpha");
    assert.strictEqual(parsed.isValid, true);
    assert.strictEqual(parsed.isAlive, true);
    assert.strictEqual(parsed.metabolism.atp, 120);
  });

  it("should trigger metabolic death (isAlive = false) if entity ATP balance drops to zero", () => {
    const starvedData = {
      agentId: "agent-malicious-flooder",
      signature: "crypto-sig-valid",
      t3: { competence: 0.8, reliability: 0.8, integrity: 0.8, alignment: 0.8, transparency: 0.8 },
      coherence: { spatial: 1.0, capability: 1.0, temporal: 1.0, relational: 1.0 },
      metabolism: { atp: 0, adp: 400, burnRate: 5.0 } // Zero energy balance!
    };

    const rawToken = createMockToken(starvedData);
    const parsed = parser.parse(rawToken);

    assert.strictEqual(parsed.isValid, true);
    assert.strictEqual(parsed.isAlive, false); // Blocked via energy physics bounds
  });

  it("should drop identity validity if multidimensional coherence index falls below critical threshold", () => {
    const fracturedIdentity = {
      agentId: "agent-sybil-spoof",
      signature: "crypto-sig-valid",
      t3: { competence: 0.8, reliability: 0.8, integrity: 0.8, alignment: 0.8, transparency: 0.8 },
      coherence: { 
        spatial: 1.0, 
        capability: 1.0, 
        temporal: 1.0, 
        relational: 0.05 // Relational matrix fractured due to social collusion shifts
      },
      metabolism: { atp: 80, adp: 10, burnRate: 1.0 }
    };

    const rawToken = createMockToken(fracturedIdentity);
    const parsed = parser.parse(rawToken);

    assert.strictEqual(parsed.isValid, false); // Disconnected due to low geometric mean score
    assert.strictEqual(parsed.isAlive, false);
  });

  it("should optimize resource reads via fastExtractMetabolism bypassing full parsing stacks", () => {
    const rawToken = createMockToken({
      metabolism: { atp: 45, adp: 2, burnRate: 0.5 }
    });
    
    const fastRead = parser.fastExtractMetabolism(rawToken);
    assert.strictEqual(fastRead.atp, 45);
    assert.strictEqual(fastRead.burnRate, 0.5);
  });
});
