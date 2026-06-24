# Design-Partner Plan

**Status:** Planning (pre-build)
**Last updated: 2026-06-24**
**Related:** [icp-and-gtm.md](icp-and-gtm.md), [pricing-and-packaging.md](pricing-and-packaging.md), [../positioning.md](../positioning.md)

The design-partner program is discovery first, pilot second. Its purpose is to (a) confirm the ICP and the three-persona gate are real, (b) land 2-3 payment-intent pilots, and (c) **validate the one assumption the entire moat rests on: is compensation genuinely hard?** This last point is not optional; it is the gating question of the whole company.

## 1. Target shape

- **Outreach:** 8-10 interviews.
- **Convert to:** ~5 design partners, spread across the three sub-segments: **bank + payments/fintech + treasury** (do not over-index on one; the moat must generalize across connector families).
- **Goal:** **2-3 payment-intent pilots** — partners willing to put a real, blocked finance-ops agent behind Provna in shadow-mode with a path to a paying contract.

The hook that opens the conversation is the *blocked project + the durable compliance obligation* — not a single calendar deadline. To a sophisticated buyer we never say "we are racing to a deadline"; we say "after the deadline passes you still have to produce this same evidence at every audit, and we solve that permanent obligation."

## 2. Discovery questions

These are ordered to surface the blocked project, the liability owner, the current (painful) reverse/prove process, the regulatory evidence demand, the willingness to let the agent write, the budget owner, and the disqualifiers.

1. **The blocked project.** Do you have an agent project currently blocked from production? What is it trying to do, who blocked it, and what was the objection?
2. **The pre-condition and the liability.** What must be true before a payment or a ledger posting is allowed to go through? If it goes through wrong, who is personally liable?
3. **Detect / reverse / prove today.** How do you detect a wrong money movement today? How do you reverse it? How do you prove what happened — and how long does each of those take?
4. **The regulatory evidence.** For EU AI Act Article 12 / Article 14, DORA, and MiFID, what evidence are you actually required to produce, and how do you produce it now?
5. **The unlock test.** If you had per-action authorization + dry-run/preview + guaranteed reversal + tamper-evident audit, would you let the agent write? If not, what else would have to be true?
6. **Whose budget.** Whose budget pays for this — the security-tooling line, or the agent-project / compliance line?
7. **The disqualifier.** Even if it worked perfectly, what would you say NO to?

## 3. Red flags (disqualify or de-prioritize)

- **"We will keep a human in the loop forever."** There is no write-automation ambition; the agent will never need a safe write layer, so there is no gate to sell.
- **"We can do it with OPA in a sprint."** The prospect sees only the S3 authorization slice and misses the S1+S2 fusion; if we cannot reframe, there is no perceived moat.
- **"No agent will touch money for two years."** The forcing function is absent; the deal has no urgency and no budget.

## 4. The 90-day pilot — single metric

One metric, nothing else: **a previously-blocked agent project ships to (limited) production with risk-committee approval *because of* Provna.** Not "actions logged," not "injections blocked" — the project moves through the gate. If the three personas (Champion brings it, CISO owns the risk, Audit signs the evidence — see [icp-and-gtm.md](icp-and-gtm.md)) all reach "yes" on the strength of Provna, the pilot succeeded.

## 5. Kill-criteria

Walk away from a partner (or the segment) when any of these is true:

- **No path to a paying contract in 90 days.** Interest without a procurement path is not a design partner.
- **"We can build it with OPA in one sprint."** They do not perceive the moat and cannot be reframed.
- **The money-path latency cannot be fixed.** If Provna inline on the payment path blows the partner's SLO and there is no design fix, the deal is dead.
- **The champion lacks budget and urgency.** A champion who cannot open a budget or point to a forcing function cannot pull the deal through the gate.

## 6. The flywheel assumption — validate it HERE, first

The S2 compensation library is the hardest moat *candidate*, but its moat-status is **explicitly conditional** on a single unvalidated assumption: **that compensation content genuinely requires multi-year accumulation** — per-connector, API-version-pinned, observe-probe + round-trip-tested inverses that a competitor cannot copy in a weekend. [OPINION]

- **If true:** the mechanism is commodity (DBOS/Temporal give you the saga in a weekend) but the content is the company; the inheritance effect means marginal value grows with every customer (a data flywheel); buy < build holds.
- **If false:** the flywheel is a weak moat, and we must lean harder on the vertical-FS depth + the S1 IFC fusion to be defensible.

This is the most critical uncertainty in the entire thesis, and the design-partner program is where it gets measured — concretely, during the first connector round-trip PoC (Stripe void, NetSuite reversing-entry). Until it is validated, the moat is sold as *conditional*, never as certainty. Surfacing the truth here, early, is more valuable than landing one more logo.
