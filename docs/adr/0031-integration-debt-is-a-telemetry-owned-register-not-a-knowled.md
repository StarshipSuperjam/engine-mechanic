---
status: accepted
engine_record: true
---

# Integration debt is a telemetry-owned register, not a knowledge entity; knowledge regen rides the commit boundary

*Decided 2026-05-23 in the design workspace.*

## The decision

Resolve the knowledge↔audit↔telemetry over-mixing. **(1) Debt ownership:** integration debt is a **committed, event-sourced register owned by [telemetry](../spec/systems/guardrails/telemetry.md)** that *references* [knowledge](../spec/systems/cognitive/knowledge.md) entity-ids; **knowledge does not carry debt** (it stays purely surface-derived and fingerprint-gated), and **[state](../spec/systems/cognitive/state.md) holds only a pointer/count**, not the register. **(2) Findings inbox:** any session *emits* a finding into the telemetry-owned inbox and is done — cognition carries no weight for acting on it; telemetry triages, promotes, and surfaces (this is where the locked finding-disposition "log it" disposition routes). **(3) Knowledge regen cadence:** regeneration is a **mutation** that runs inside the `PreToolUse` `git commit` intercept (the [D-023](0023-check-system-locked-validator-architecture-the-check-surface.md) commit-boundary mechanism; no separate pre-commit framework), batched and **best-effort/fail-open**; a separate **fingerprint coverage check** gates at **CI**. Boot is **read-only** and never regenerates. **(4) Knowledge is plain JSON, not JSON-LD** (no external interop payoff; the locked schema layer governs it). **(5) Upgrade-safe ([D-024](0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)):** committed entities are a derived engine artifact, so an overlay replaces them and the next commit-boundary regen self-corrects them to the adopter's surfaces. This **supersedes the "knowledge carries the debt" framing** in the prior telemetry doc and the remediation-loop scenario.

## Why

Knowledge's integrity claim is "derived from surfaces, fingerprint-gated"; debt is event-sourced from telemetry/audit and derived from no surface, so housing it in the graph muddied that claim and smeared debt across three systems in the prototype. A telemetry-owned register that *references* knowledge keeps each system's contract clean and gives debt exactly one home. Placing regen on the commit boundary (a "building" cost) rather than at boot (a "using" cost, forever) honors the operator's latency rule; naming it a mutation distinct from the fingerprint *check* removes the prototype's conflation of the two. Dropping JSON-LD removes ceremony with no payoff. The cold-session review caught the falsified `remediation-loop.md` scenario (rewritten), the regen-mechanic conflation (named precisely), and the D-024 overlay behavior for committed entities (recorded).

## What we ruled out

Debt as knowledge-graph entities (rejected — the prototype's category muddle; pollutes the derived-from-surfaces purity). Debt folded into State (rejected — State is a tiny cursor; an event-sourced, growing register would bloat the first thing read). Cognition acting on findings it emits (rejected — couples the substrate to the act-on-it loop; emit-and-done is the clean seam). Regen at boot (rejected — perpetual "using" latency). Regen synchronously per surface edit (rejected — also mid-session "using" cost; batch at the commit boundary). JSON-LD canonical (rejected — interop it does not have).
