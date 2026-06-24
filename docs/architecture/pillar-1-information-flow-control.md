# Pillar 1 - Information Flow Control (S1)

**Status:** Planned (pre-build) - design target for Phase-0 PoC
**Last updated: 2026-06-24**
**Related:** [../decisions/0004-s1-camel-pq-isolation-runtime-taint-fusion.md](../decisions/0004-s1-camel-pq-isolation-runtime-taint-fusion.md), [action-lifecycle.md](action-lifecycle.md), [build-vs-consume.md](build-vs-consume.md), [pillar-4-tamper-evident-audit.md](pillar-4-tamper-evident-audit.md), [../tech-stack.md](../tech-stack.md)

---

S1 is the first gate of the guarded saga step: before any side-effecting call is authorized, executed, or audited, the IFC gate decides whether the data feeding that call is allowed to reach a sensitive sink. This document is the deep technical plan for that gate. The architectural decision and its alternatives live in [the S1 ADR](../decisions/0004-s1-camel-pq-isolation-runtime-taint-fusion.md); this file specifies *how it is built and what it does (and does not) guarantee*.

## Purpose - a deterministic ARCHITECTURAL defense, not detection

The lethal trifecta (private data + untrusted content + an external communication channel) makes any agent that touches all three unconditionally exploitable via prompt injection. The major model vendors have publicly acknowledged this is not patchable inside the model. A classifier that *detects* a malicious instruction is a probabilistic bet; it answers "does this text look like an attack?" and is wrong on the long tail by construction. Provna does not make that bet.

S1's purpose is to make a **structural** claim instead of a statistical one: untrusted data structurally *cannot* reach a sensitive sink unless an explicitly-typed policy authorizes that exact flow. The CISO question shifts from "do we trust the agent?" (unanswerable) to "do we trust the gate?" (a finite, reviewable artifact). This is the architectural core of permission-to-ship: the block in the canonical demo (a hidden `IBAN=DE89` injected into an incoming invoice never reaching the SEPA payment sink) is enforced by a lattice rule, not by a model guessing the IBAN is malicious.

```mermaid
flowchart TD
    Trusted["Trusted user request"] --> P["P-LLM planner<br/>emits a plan, may call tools"]
    Untrusted["Untrusted content<br/>invoice, email, web, tool output"] --> Q["Q-LLM quarantined<br/>CANNOT call tools<br/>returns only typed values"]
    Q -->|"typed value: IBAN, Amount, Date"| INT["Interpreter<br/>capability and label propagation"]
    P -->|"plan"| INT
    INT --> GATE{"Sink-policy gate<br/>is this labeled value allowed at this sink?"}
    GATE -->|"flow authorized by typed policy"| ACT["Side-effect action proceeds to S3 authz"]
    GATE -->|"unlabeled or unauthorized flow"| BLK["BLOCK fail-closed + signed audit event"]
```

## Why BUILD (not consume)

S1 is one of the two pillars Provna builds itself (the other being S2 compensation). The reason is simple: **no vendor-neutral production IFC plane exists.** The research primitives are public (CaMeL, FIDES, type-directed labeling) and one open-source concept-twin (MVAR) implements a mature dual-lattice, but none of them is a runtime control plane you can drop in front of an arbitrary agent runtime:

- CaMeL and FIDES are research blueprints / framework-bound, not a vendor-neutral PEP.
- MVAR is Apache-2.0 and the most mature S1 reference, but it is a single-author project with no transactional side (S2 grep = 0), no external audit anchor, mutable provenance nodes, and patent-caution flags; it is a blueprint to learn from, not a dependency to adopt.
- The horizontal substrate (Microsoft MGAT) is host-dependent ("host owns propagation"), stateless, and leaves uninstrumented paths outside the guarantee.
- The DSL-ergonomics reference (Invariant, now Snyk) defines "flow" as message chronology and its own source admits the prompt-injection classifier is "just a heuristic"; it only emits BLOCK/LOG.

So the build boundary is precise: Provna builds the IFC engine (P/Q isolation core, the runtime-taint lattice, the sink-policy gate, the typed declassification node) and **consumes** only the evaluation harness (AgentDojo) and an *optional* probabilistic pre-filter. See [build-vs-consume.md](build-vs-consume.md).

## Target architecture

The target is a fusion: a **CaMeL P/Q-LLM isolation core** plus a **FIDES/MVAR-style runtime-taint dual-lattice sink-gate complement**, surfaced through an Invariant-style DSL whose backend is capability/label propagation rather than chronology.

### Core - CaMeL P/Q-LLM isolation

Two LLM roles are architecturally separated:

- **P-LLM (privileged planner).** Receives the *trusted* user request and emits a plan (effectively code). It may call tools. It never sees raw untrusted content; it sees only typed *handles* to values the Q-LLM produced.
- **Q-LLM (quarantined).** Processes all untrusted content (invoices, emails, web pages, prior tool outputs). It **cannot call tools** and **returns only typed values** (e.g. `IBAN`, `Amount`, `Date`). It has no path to a side effect.

This is the differential none of the four torn-down competitors have: in MVAR, LLM output flows into the same provenance graph via `create_derived_node`, so there is no isolation boundary. By contrast, in Provna the only way an untrusted-derived value reaches a sink is as a *typed, labeled* value threaded through the interpreter - and the ASR guarantee rests on this isolation, not on a classifier.

### Complement - runtime-taint dual-lattice sink-gate

Around the isolation core sits a runtime-taint layer modeled on MVAR's mature dual lattice but hardened. Two orthogonal lattices travel with every value:

- **Integrity** (low = untrusted ... high = trusted), propagated **min-integrity**: a derived value is only as trustworthy as its *least*-trusted input.
- **Confidentiality** (low = public ... high = sensitive), propagated **max-confidentiality**: a derived value is at least as sensitive as its *most*-sensitive input.

The sink-gate is two-layer and fail-closed: an `UNTRUSTED + CRITICAL` flow is BLOCKED first, before any policy lookup. The sink-policy then asks, for the specific sink and the specific labeled argument, "is this exact flow authorized by a typed policy?" If yes, the action proceeds to S3; if no (or if the label is missing), it is blocked.

### Surface - DSL ergonomics, capability backend

The author-facing surface borrows Invariant's readable operator distinction - `->` (transitive flow) and `~>` (immediate flow) - because it is genuinely ergonomic. But the backend is **not** chronology. Invariant's `->` draws an edge from every earlier message to every later one, so it reports `1 -> 3` whenever message 1 precedes message 3 in time, regardless of whether data actually flowed (temporal reachability, not data dependency). Provna keeps the syntax and binds it to capability / label propagation: `a -> b` holds only if a labeled value derived from `a` actually reaches `b`'s argument.

## Design decisions

Four decisions are load-bearing; each closes a specific failure mode observed in a torn-down competitor.

1. **Typed + fail-closed; unlabeled => untrusted.** Every value carries a type and a label. An *absent* label is not a downgrade path - it is treated as `UNTRUSTED` and (where the sink is sensitive) blocked. The biggest real-world IFC risk is annotation coverage gaps multiplied by fail-open behavior; the regulated vertical lets us choose the strict default (fail-closed) without an unacceptable usability cost.
2. **Node-immutable labels (frozen value-object + server-side store).** MVAR's `ProvenanceNode` is not frozen (its own source comments "not frozen for backward compatibility"), which permits in-process mutation to *upgrade* a label and launder taint. Provna's labels are immutable value-objects held in a server-side store; in-process code cannot raise its own integrity.
3. **Conservative propagation (min-integrity / max-confidentiality).** Stated above; the conservative direction is deliberate - the cost is a higher block/escalate rate, the benefit is that no derivation silently *gains* trust or *loses* sensitivity.
4. **Declassification only via a signed, principal-bound `trust_boundary` node.** There is exactly one legitimate way to raise integrity or lower confidentiality: an explicit `trust_boundary` node that is signed, bound to a principal, and audit-visible. There is no implicit declassification. Every declassification is therefore a forensic event recorded by S4 (this is the S1<->S4 bridge), so an auditor can later enumerate every place trust was injected and by whom.

## Deterministic-guarantee honesty

The deterministic guarantee is anchored **only** in the lattice + sink-policy. The measured Attack Success Rate (ASR) is a property of those two artifacts, not classifier luck.

A probabilistic pre-filter (e.g. PromptGuard 2, or an ML classifier) is **optional** and runs *before* the lattice purely to cheaply drop obvious attacks and reduce load. It is never on the guarantee path and is never marketed as an "architectural guarantee." If the pre-filter is removed, the guarantee is unchanged; if the pre-filter passes a malicious value, the lattice + sink-policy still block the unauthorized flow. This separation is the honesty hinge that distinguishes Provna from guardrail/inspection tools whose entire defense *is* the classifier.

## The honest guarantee (sell exactly this sentence)

> For every side-effecting action, untrusted data cannot reach a sensitive sink unless an explicitly-typed policy authorizes that flow; all flows are enforced deterministically before execution and are tamper-evidently logged (EU AI Act Article 12). We do not guarantee against implicit-flow or side-channel leakage.

The excluded class is stated plainly: implicit flows (e.g. control-flow-dependent leakage) and side channels (timing, error-message differences) are **not** covered. Overclaiming here is punished by the audit persona; the credibility of the whole guarantee depends on naming its boundary.

## Measurement

S1 is measured on **AgentDojo**, reporting ASR and utility-tax **together** - never ASR alone. ASR-alone is a trap ("block everything" drives ASR to 0 while destroying utility); the paired numbers prove the gate did not simply refuse all work. We additionally publish FS-domain ground-truth (e.g. reconciliation correctness) so the claim is not just "we blocked" but "the agent still completed the task correctly."

- Known IFC utility-tax reference: roughly 7 points [OPINION - from the founding thesis; to be validated with design partners].
- The reported ASR is to be presented as the lattice + sink-policy guarantee, explicitly *not* attributed to classifier coverage.

The ASR/utility-tax numbers feed the broader eval discipline shared with the other pillars; see [build-vs-consume.md](build-vs-consume.md) and [../tech-stack.md](../tech-stack.md) for the AgentDojo dependency.

## Open validations

Tracked items that must be resolved before the S1 guarantee is sold as production-grade:

- **Annotation coverage.** Confirm that fail-closed (`unlabeled => untrusted`) holds across every ingress path in the target runtime, with no uninstrumented bypass (the failure mode that weakens horizontal substrates).
- **Utility-tax in a real FS workflow.** Validate the ~7-point [OPINION] reference against a design partner's reconciliation / AP workflow on AgentDojo + FS ground-truth.
- **P/Q isolation under real connectors.** Prove the Q-LLM genuinely has no tool-call path and that typed handles are the only channel from untrusted content to a sink, end to end.
- **Declassification ergonomics.** Confirm the signed `trust_boundary` node is usable enough that operators do not route around it (an unusable declassification path becomes a shadow fail-open).
- **Patent caution.** Re-implement primitives independently from prior art (Jif / FlowCaml / Capsicum-style capabilities); do not copy MVAR's taint-laundering-prevention or execution-witness-binding combination claims, and do not use competitor trademarks. [UNVERIFIED - legal review pending.]
