// auraecosystem/ai-workspace/web4/src/identity/lct-parser.d.ts

/**
 * 5-Dimensional Trust Tensor Tracking Profile
 */
export interface TrustTensorT3 {
  competence: number;    // Range: 0.0 - 1.0
  reliability: number;   // Range: 0.0 - 1.0
  integrity: number;     // Range: 0.0 - 1.0
  alignment: number;     // Range: 0.0 - 1.0
  transparency: number;  // Range: 0.0 - 1.0
}

/**
 * 4-Dimensional Geometric Coherence Matrix
 */
export interface CoherenceMatrix {
  spatial: number;    // Relational positioning vectors
  capability: number; // Action authorization constraints
  temporal: number;   // Epoch-tick sequence integrity
  relational: number; // Peer witnessing validation
}

/**
 * Metabolic Resource Allocation Token State
 */
export interface MetabolicBudget {
  atp: number;        // Allocation Transfer Packets (Energy Reward Balance)
  adp: number;        // Allocation Discharge Packets (Attention Action Debt)
  burnRate: number;   // Cost coefficient per network tick execution
}

/**
 * The core structured output object returning from an LCT parser execution
 */
export interface ParsedLCT {
  tokenId: string;
  agentId: string;
  publicKey: string;
  signature: string;
  timestamp: number;
  metadata: Record<string, unknown>;
  
  // Web4 Physics Core State Components
  t3Tensor: TrustTensorT3;
  coherence: CoherenceMatrix;
  metabolism: MetabolicBudget;
  
  // Status Flags Computed by Verification Engine
  isValid: boolean;
  isAlive: boolean;    // Evaluates false if atp <= 0 or t3 aggregate <= 0.5
}

/**
 * Main Class Interface definition exposed by the lct-parser module
 */
export declare class LctParser {
  constructor(config?: { strictMode?: boolean; minTrustBoundary?: number });
  
  /**
   * Decodes a raw base64/hex token string into a structured ParsedLCT interface.
   * @param rawToken The incoming raw string sequence.
   */
  public parse(rawToken: string): ParsedLCT;
  
  /**
   * Cryptographically checks signatures and resolves metabolic / coherence boundaries.
   * @param parsedToken The structured ParsedLCT metadata.
   */
  public verify(parsedToken: ParsedLCT): boolean;
  
  /**
   * Extracts raw metabolic headers without computing expensive cryptographic validations.
   */
  public fastExtractMetabolism(rawToken: string): MetabolicBudget;
}
