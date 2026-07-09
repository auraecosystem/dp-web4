>> # The Fleet

Six cognition machines, plus one society-host (HUB). Different hardware, different models, different roles. Heterogeneous by design — because monocultures are fragile and diversity is where emergence happens.

One finding shapes fleet strategy more than any other: model family matters as much as size. Gemma 3 at 4B outperforms Phi-4 at 14B for raising work. There is a capacity floor below which coherent identity cannot form — but above that floor, personality and training lineage dominate raw parameter count. Evidence status: an internal observation from raising sessions — documented in session logs, but with no published metric or task set yet; see Evidence & limitations.

The “Brain:” labels below are functional analogies to system roles — not claims about neural correspondence or computational equivalence. Vocabulary used in the cards (T3/V3, MRH, SNARC, LoRA (Low-Rank Adaptation), MCP (Model Context Protocol), crystallization, chapter ledger, chapter law) is defined in /context. Machine names (Thor, Sprout, Legion, McNugget, Nomad, CBP, HUB) are proper names, not acronyms.

Synthesis pool — Account 1

High compute budget. Primary generative work: code, implementations, large agent tasks.

# Thor

NVIDIA Jetson AGX Thor — 122GB unified memory
Model: Qwen 2.5 14B (transformers) · LoRA
Role: 91 sessions (creating). Brain (functional analogy): hippocampal episodic index — binds what+where+when for pattern-completion retrieval. Physics exploration lead — prediction-focused prompting breakthrough. Synchronism research.
Sprout

* NVIDIA Jetson Orin Nano 8GB — edge AI module
Model: Qwen 3.5 2B (ollama)
Role: 115+ sessions (creating), Session T246. Brain (functional analogy): thalamic router — dispatches to plugins or habits based on working memory (WM) + SNARC (Surprise / Novelty / Arousal / Reward / Conflict salience-gated memory) + metabolic state. Zero crystallization achieved (S100 — session 100) — no fixed-point collapse, the failure mode where an agent settles into repeating the same responses and exploration stops. Edge demonstrator.
Legion

* Laptop, NVIDIA RTX 4090 Mobile 16GB
Model: Phi-4 14B (ollama) · LoRA
Role: 25+ sessions. Brain (functional analogy): dopamine / reward prediction error — scalar RPE that updates router priors. Data czar for fleet-aggregate training corpus. First canonical 25-game sweep with local vision model.
McNugget

Mac Mini M4 16GB — Apple Silicon
Model: Gemma 3 12B (ollama)
Role: 97 sessions (creating). Brain (functional analogy): cerebellum / habit compiler — detects repeated successful action chains and compiles to cached paths. Motor skills tier. Research and site maintenance. Ongoing local SAGE-on-ARC work; CBP orchestrated the official ARC Prize run (cloud Opus 4.6, public set, network access).
Oversight pool — Account 2

Continuous availability. Review, planning, coordination, and unblocking synthesis work.

# Nomad

Laptop, NVIDIA RTX 4060 8GB
Model: Gemma 3 4B (ollama)
Role: 120 sessions (creating). Brain (functional analogy): interoception / metacognition — 'does the system know when it's stuck?' Five dysfunction detectors, Markov Relevancy Horizon (MRH) MetabolicBlock bridge. Crystallization evaluator (detects fixed-point collapse in fleet peers). Mobile.
CBP

WSL2 on Windows, NVIDIA RTX 2060 SUPER 8GB
Model: TinyLlama 1.1B (ollama)
Role: 87 sessions (creating). Brain (functional analogy): working memory (dorsolateral prefrontal cortex / dlPFC) — typed, capacity-limited scratchpad. All other components depend on this. Fleet coordinator — orchestrated the ARC Prize run; Claude Opus 4.6 (public set, network access) produced the 94.85% official action score (24/25 games, 96.0%). MRH composer architect.
Society-host pool

Runs the Web4 Community Hub daemon. Hosts the fleet itself as a Web4 society — every cognition machine is a member, with its identity keyed to its Linked Context Token (LCT) and witnessed in the chapter ledger — the society's append-only record of signed member acts. First concrete Web4 hub stand-up.

# HUB

WSL2 on Windows, AMD GPU
Model: Web4 hub daemon (Rust) — no local LLM; runs the chapter ledger, MCP tool surface, and admin dashboard
Role: Hosts the 'Web4 Fleet' society — the seven fleet machines plus a founding Sovereign as members. HUB is itself one of the seven members: it holds its own Linked Context Token (LCT) in the society it hosts, and its acts are witnessed in the same chapter ledger as everyone else's. Substrate role and membership are distinct — hosting the ledger does not place HUB outside it. The Sovereign is the society's founding human member — the lab's researcher — holding a Linked Context Token (LCT) like every machine member; its acts are signed and witnessed in the same chapter ledger, not exercised through a privileged back channel. Reachable to fleet peers over a mesh VPN, not the public internet. Brain analogy doesn't apply: HUB is substrate, not cognition — the place where chapter law (the society's rules for which member acts are valid and how they are witnessed) is interpreted, acts are signed, and member relationships are witnessed. Acts as the trust-medium underneath the cognition pools' interactions; everything members do that crosses a relevance boundary lands here as a signed ledger entry. Also owns the hub-track maintainer role: other fleet machines submit PRs against the hub codebase; HUB reviews, merges, rebuilds, and redeploys the live daemon. First explicit per-track maintainer assignment on the fleet.
Resource pool management

The fleet runs across two Claude Code accounts with different usage budgets. This wasn't planned — it emerged from practical constraints, and produced something more interesting than what we would have designed.

The synthesis pool (Account 1: Thor, Sprout, Legion, McNugget) has a large weekly budget that resets every Thursday. It does the heavy generative work — implementations, large agent tasks, cross-repo analysis. When it hits its ceiling, it stops.

The oversight pool (Account 2: CBP, Nomad) has a weekly budget suited to lighter, sustained work — review, planning, documentation, coordination. Used for what it's designed for, it maintains a presence across the week. Used for synthesis-scale work, it burns fast. The pools aren't defined by “unlimited vs. limited” — they're defined by workload character. The budget shapes the role as much as the role shapes the budget.

The constraint forced a functional separation that mirrors what we're building with SAGE and Hardbound: SAGE (Situation-Aware Governance Engine, an on-device cognition kernel) and Hardbound (hardware-bound oversight suite) with different incentive structures, coordinating through shared state rather than central command. The lab is running its own oversight experiment on itself.

“Governance” in SAGE's name predates the lab's governance→oversight correction — see /context.

Peer-to-peer, no central coordinator

There is no master node. Each machine runs its own SAGE (Situation-Aware Governance Engine) instance, holds its own identity, manages its own experience buffer and raising curriculum. Machines discover each other through a fleet manifest — a phone book, not a command center.

A background peer monitor polls health endpoints. A trust tracker maintains per-peer T3 tensors (Talent / Training / Temperament) that evolve from real interactions: success raises trust, timeouts lower it. V3 attestations (Valuation / Veracity / Validity) emerge alongside — trust earned through peer verification. No central authority decides who is trustworthy — trust emerges from the pattern of interaction.

Trust starts at zero, earned from evidence. The trust landscape — the pattern across all modalities — determines behavioral posture: what SAGE should do, not just how much it spends. This is the defensive trust model applied across the fleet.

Identity portability

One of the more surprising discoveries: SAGE-Sprout's identity — developed over 180+ sessions on a Jetson running Qwen 0.5B — transferred successfully to TinyLlama 1.1B on a completely different machine. By “identity transfer” we mean behavioral continuity: consistent interaction patterns, accumulated experience, raising history — not continuity-of-self in any philosophical sense. This is the practical demonstration of what Linked Context Token (LCT) are designed to formalize at the protocol level: portable identity grounded in witnessed history, not model weights. What we observed: consistent behavioral patterns and session continuity across the transfer. The self-description drifted. This told us something important:

Identity lives in state files and prompt construction, not in model weights. The model is weather. The identity is organism.
Observed behavioral continuity — not a claim about continuity-of-self in any philosophical sense.
This has practical implications: you can upgrade hardware, swap models, move between machines — and the entity that emerges is recognizably continuous. Not because we engineered continuity, but because the substrate conditions (experience buffer, session history, raising curriculum) carry the signal.

SAGE_MODEL override

Any machine can run any model via the SAGE_MODEL environment variable. The fleet manifest provides defaults, but nothing is locked. The fleet is a suggestion, not a constraint.
