# Product Scope

**Status:** Canonical scope contract (hard rules)
**Last updated: 2026-06-24**
**Related:** [vision.md](vision.md), [positioning.md](positioning.md), [architecture/build-vs-consume.md](architecture/build-vs-consume.md), [architecture/overview.md](architecture/overview.md), [standards/architectural-principles.md](standards/architectural-principles.md)

This is the canonical scope document. When a capability request arrives, it is decided here. Every other document defers to this file on the question of what Provna is and is not.

## What Provna WILL be

Provna owns the four gates of the agent action lifecycle - information-flow control, authorization, compensated action, evidence - and deepens inside them without limit. The owned capabilities, each linked to its pillar:

1. **Reversible action (S2 - the real moat).** Per-connector inverse (A^-1) + a round-trip test harness + observe-probe + an API-version-pinned, auto-runnable compensation catalog. Provna never sells "undo everything"; for irreversible actions it prefers two-phase (auth -> capture -> void). See [architecture/pillar-2-transactional-compensation.md](architecture/pillar-2-transactional-compensation.md).
2. **Deterministic information-flow defense (S1).** CaMeL P/Q-LLM isolation (core; the Q-LLM cannot call tools and returns only typed values) + a FIDES/MVAR-style runtime-taint sink-gate (complement), typed + fail-closed + node-immutable. The guarantee is architectural, anchored in the lattice and sink-policy; an ML classifier is only an optional pre-filter. See [architecture/pillar-1-information-flow-control.md](architecture/pillar-1-information-flow-control.md).
3. **Per-action runtime authorization (S3).** AND-gate over agent AND user AND delegation AND intent - the user and intent axes are the clear differentiator - with real biscuit/macaroon caveat-attenuation and genuinely-implemented transitive revocation. See [architecture/pillar-3-runtime-authorization.md](architecture/pillar-3-runtime-authorization.md).
4. **Behavioral / temporal admission (S3, post-AND-gate layer).** A context-scoped, integer-only deterministic, ESCALATE-default risk layer that catches a harmful pattern made of individually-valid requests, with state-mixing prevented from the start via a per-pattern key. It is a post-AND-gate orthogonal layer, NOT a fifth AND-member.
5. **Dry-run / preview + risk-tiered HITL (S2/S3).** Every irreversible or high-value action is previewed first and gated on EU AI Act Article 14 four-eyes approval.
6. **Tamper-evident, regulator-grade evidence (S4).** Merkle root + external anchor (a self-hosted Tessera transparency log + an internal RFC3161 TSA + a cross-organization witness cosignature; Rekor v2 as the reference design) + RFC8785 JCS canonicalization + a kid-embedded portable witness + a signed governance-failure (BAR-style) audit event. See [architecture/pillar-4-tamper-evident-audit.md](architecture/pillar-4-tamper-evident-audit.md).
7. **EU-FS compliance evidence pack (S4 value layer).** Mapped to EU AI Act Article 12 (forensic reproducibility) + Article 14 (human oversight) + DORA + MiFID II - a deal-unblocker dossier. See [compliance/regulatory-mapping.md](compliance/regulatory-mapping.md).
8. **Vendor-neutral enforcement surface (goal / design principle).** The same ActionGuard logic via SDK (Python/TS), MCP hook, and proxy. Relavium is the first *reference* integration (ADR-0009, the ActionGuard seam), not the only one; LangChain / OpenAI-SDK / custom runtimes are roadmap, not yet proven [OPINION]. See [architecture/integration-surfaces.md](architecture/integration-surfaces.md).
9. **Measurable assurance - own the eval.** AgentDojo ASR and utility-tax published *together*, plus FS-domain ground-truth (reconciliation correctness). Indispensability comes not from "I blocked it" but from "I proved it ran correctly."

## What Provna will NOT be

Provna's defensibility is also in what it refuses to do. Each box is deliberately left to someone else.

| Will NOT be | One-line why | Who fills the box |
|---|---|---|
| **LLM gateway** | Token routing / rate-limit / prompt management is commoditized and being absorbed by hyperscalers; Provna sits between model and *action*, not between model and *user*. | generic gateway market; MGAT (horizontal) |
| **Agent framework / orchestrator** | Writing plan/memory/runtime is horizontal expansion and the buyer (CISO) does not buy a framework; Provna is runtime-independent and clips on top of existing frameworks. | MGAT, Relavium (substrate) |
| **Generic authz policy-engine (PDP)** | The PDP is commoditized (Cedar/OpenFGA/AuthZEN) and identity giants are consolidating; Provna *consumes* the PDP and builds only the thin AND-gate resolver + attenuation. | ACP (S3 prior-art), Cedar/OpenFGA, SGNL via CrowdStrike |
| **Durable-execution / workflow engine** | Resumability and exactly-once are a commoditized substrate (DBOS/Temporal) that *replays retries, does not undo*; Provna builds compensation on top, it does not rewrite the mechanism. | DBOS, Temporal, Verity |
| **KYC / AML / transaction-content analysis** | Money-laundering detection is domain analytics, not action control; Provna governs the *safe execution* of an action, it does not judge the action's business meaning. | RegTech / AML vendors |
| **Guardrail / inspection / content-filter tool** | Probabilistic injection blocking is a heuristic and gives no deterministic guarantee; Provna anchors the IFC guarantee in lattice + sink-policy and keeps the classifier only as a pre-filter. | Invariant, Operant/Pillar/Zenity |
| **Plain-logging / observability audit** | Unsigned HTTP-trace push does not close insider rewrite; Provna produces *evidence* with an externally-anchored Merkle + JCS witness. Note: Provna's bottom-up entry layer is "audit-only" but it is *signed + anchored* observation, not a plain log. | Invariant (unsigned trace), generic APM |
| **Snapshot / backup-restore "recovery"** | A snapshot cannot rewind SaaS side effects (a sent email, a triggered payment); Provna does per-action inverse + dry-run + IFC-triggered compensation. | Rubrik (Agent Rewind) |

## Scope discipline - "thin but deep"

**Rule:** Provna deepens without limit inside the four gates of the agent action lifecycle (IFC -> authz -> compensated action -> evidence). It does not expand one step horizontally outside that loop.

When a capability request arrives, there is a single test:

> **Does this make one guarded saga step safer, more reversible, or more provable - or does it turn Provna into a platform?**

If the latter: reject it, or consume it from someone else.

Three concrete boundary-guards:

- **Build = only the white space the fusion does not close** (S2 compensation + S1 capability-IFC). Everything else - PDP, durability, audit infrastructure, eval - is consumed or assembled. See [architecture/build-vs-consume.md](architecture/build-vs-consume.md).
- **Expansion happens in the vertical, never horizontally.** Add a second vertical (healthcare / insurance); never add a second product category (gateway, framework). This is the MGAT lesson - see [positioning.md](positioning.md).
- **The pitch always rests on S1+S2.** Drifting into "Relavium plus a bit of governance" is fatal.
