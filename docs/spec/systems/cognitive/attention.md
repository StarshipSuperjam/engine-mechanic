---
status: draft
---

# Attention

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-07-16 by [decision 0316](../../../adr/0316-resolve-re-lock-attention-the-work-record-commission-retired.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

Answers **"what do I focus on, and at what level?"** — the prioritization layer that decides what the
AI sees first and in what depth, and the order of the in-flight and blocking work it ranks. Attention
is a **policy plus a function**,
not a store: it holds no canonical state of its own.

## Behavior

### A policy and a function, not a store

In the prototype, prioritization was emergent: hardcoded budget constants and a trim order buried in
boot code across several files, with a comment admitting it was a placeholder (Risk [R4](../../../reference/risks.md)).
v1 makes it explicit and reviewable in exactly two pieces:

- **An attention policy** — a committed, governed [policy](../surfaces/policies.md)-surface
  instance carrying the budget allocation, ranking weights, trim order, and the debt-blocking rule
  ([D-117](../../../adr/0117-q24-q27-2-re-litigation-the-attention-ranking-function-form.md)).
  This is the reviewable, tunable contract that replaces the magic numbers. The per-prompt scent's
  strong-match threshold once homed here was deliberately retired as built: the scent reads none of the
  policy's numbers at all — it is unconditional, so there is no bar to set — and a shipped migration
  removed the key, with the policy's own scope stating the same.
- **A ranking function** — a deterministic computation (a [tool](../surfaces/tools.md)) that
  reads the existing substrates ([state](state.md), [knowledge](knowledge.md)
  adjacency, the [telemetry](../guardrails/telemetry.md) debt register, and the **in-flight**
  git/GitHub record — open pull requests and the current working branch, and the merged pull requests
  whose bodies carry the recent decisions) and produces the ordering and the budget split. Its **form is an ordered
  partition with weighted intra-partition ranking**: candidates partition into the budget categories
  (blocking debt · in-flight work · recent decisions · structural neighbors · orientation) under **hard
  cross-category precedence** — so "blocking debt ahead of features" is guaranteed by the structure, never
  by a weight — while the **ranking weights** order candidates *within* each partition and the budget
  allocation is the partition's slice-sizing. This is the only form under which both the lexicographic
  ordering rules and the "ranking weights" hold at once. The partition guarantees *ordering*, not category
  *membership*: whether a candidate is tracked debt at all is [telemetry](../guardrails/telemetry.md)'s
  promotion decision (attention reads the resulting register), and which of that open debt is *blocking* —
  gating the start of work — is attention's own debt-blocking rule (below); the partition orders what those
  determinations hand it. No scored-token files, no decay store, no machine learning; recency enters only as
  an intra-partition weight over the explicit as-of timestamp.

This reconciles [D-010](../../../adr/0010-attention-is-a-first-class-surface.md) ("attention is a first-class surface"): *first-class*
means its governing **policy is a governed surface** — not that attention is a new store or a parallel
substrate of focus tokens. The rejected alternative is the proposal's `FocusToken`/`WorkingSet`/decay
store, which would hand-author mutable scored state (violating [principle §3](../../../principles.md))
and re-implement claim/scope/mode enforcement that the [modes](../lifecycle/modes.md)
stance gating and [hooks](../infrastructure/hooks.md) block budget already own.

### What it governs

- **Budget allocation** — how the bounded cold-context budget is split across blocking debt, in-flight work (open pull requests and the current working branch), recent decisions (recently merged pull requests — the structured PR body is the decision record — and the [memory](memory.md) recall boot assembles into the pack), structural neighbors, and orientation, and how it flexes (clean sessions get more orientation; high-debt sessions compress it).
- **Work prioritization** — the ordering of candidate work (unblocked first; blocking debt ahead of features). The candidate work attention *orders* is the **in-flight** native git/GitHub record — open pull requests and the current working branch (deliberately not every local branch, which in a worktree repo accrues stale branches that are not in-flight work) — together with the open engine-labeled issues of [telemetry](../guardrails/telemetry.md)'s debt register ([control-plane](../infrastructure/control-plane.md) names attention among that channel's readers); it is not a committed list held by [state](state.md). **The project's plan is a different thing under a different owner:** when the optional [product-design](../../modules/product-design.md) module drives the build, the engine decomposes the spec the operator accepted and `locked` into a build-plan of ordered phases — living, re-sequencing as work lands — which [build-orchestration](../lifecycle/build-orchestration.md) groups under native Milestones, and the un-labeled work Issues beneath them are that plan's backlog; absent a build-plan, build-orchestration plans the Milestone itself. Either way the ordering is **the plan's, not attention's**, and attention neither reads nor re-ranks it — a deferred issue is a plan, not context for a cold session ([D-314](../../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)).
- **Debt-blocking** — what must be surfaced before work begins versus what can wait. This is attention's *blocking* rule (which open debt gates the start of work), distinct from [telemetry](../guardrails/telemetry.md)'s *promotion* thresholds (what a signal must clear to become tracked debt at all): attention reads the resulting register, it does not set those thresholds.

### It powers the whole orientation family

Attention is the ranking function behind **every** [orientation](../lifecycle/boot.md) event,
not only cold-start: cold start is attention with a large budget. The per-prompt scent was designed here
as attention with a tiny budget and a lexical trigger; as built it is not a ranking invocation at all — it
injects one short, constant recall cue on every prompt, unconditionally, the lexical trigger deliberately
retired (a keyword gate fires only when the prompt shares vocabulary with the stored record — silent on
exactly the reworded and forward-looking prompts recall keeps failing; the every-prompt law is pinned
upstream by [eADR-0018](https://github.com/StarshipSuperjam/engine-template/blob/cdbbc3357fbfbc192005650a8be6ce35b7942bfe/.engine/contracts/eADR-0018-cognitive-substrate-one-workflow.md)
and a guard test). "Boot" is just its heaviest invocation. The orientation
*events* themselves — which [hook](../infrastructure/hooks.md) fires each, their cost budgets,
and the degraded-disclosure — are [boot](../lifecycle/boot.md)'s to define; the plan-gate
consent that gates substantive work on the degraded readout is
[build orchestration](../lifecycle/build-orchestration.md)'s, not boot's. Attention supplies
the ranking each invocation needs and fixes none of boot's event model.

### It reads; it never owns

Attention is downstream of every substrate it ranks and authoritative over none:

- [state](state.md) feeds the standing-situation pointers and the committed debt count;
- [knowledge](knowledge.md) supplies structural adjacency — which entities neighbor the work in hand;
- [telemetry](../guardrails/telemetry.md) owns the debt register — the view over open engine-labeled issues — and attention reads it to rank, never defining its shape.

When an input is unavailable — the telemetry/GitHub read fails on an outage or expired auth, or a
substrate MCP is down — the ranking function degrades to the inputs that remain: [state](state.md)'s
committed debt count, carried with its as-of marker, and local `git` stand in for the live register, so it
produces a best-effort ordering rather than failing. Attention never narrates this silently: the
degraded-input set is handed to [boot](../lifecycle/boot.md), which surfaces it loudly and in
plain language under its degradation-and-consent law ([D-059](../../../adr/0059-lock-the-state-system-wave-2-head-the-committed-cursor-recon.md) law 2,
[principle §5](../../../principles.md)) — so a non-engineer is never shown a confident-looking but partial
picture of blocking debt or next work without the caveat.

### Build-spec leaves

The ranking-function **form** is pinned above (ordered partition + weighted intra-partition,
[D-117](../../../adr/0117-q24-q27-2-re-litigation-the-attention-ranking-function-form.md)); only the concrete **values** that form inhabits remain the build-spec
leaf — the budget splits, the intra-partition ranking weights, the partition precedence order, the trim
order, and the debt-blocking threshold, plus their calibration inputs —
authored and fixture-tested in its own build session (laws-not-leaves, [D-052](../../../adr/0052-foundational-law-layer-closed-the-implementation-lock-order.md);
pin the form, defer the values, [D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)). As built the form fixture
exists — the attention unit tests lock the partition **assignment** (which candidate lands in which
category, the half the partition itself cannot guarantee), the structural cross-category precedence, and
determinism — while ranking *quality* is deliberately not asserted there: the shipped values are
uncalibrated starting values, so the claim that prioritization surfaces *the right things first* remains
**unproven** pending calibration. The laws here fix that the ordering is explicit, deterministic,
partition-ordered, and debt-blocking-aware, not that its weights are calibrated to a correct priority. The policy lands on the locked [policies](../surfaces/policies.md)
surface and the ranking function under `.engine/tools/` on the locked
[tools](../surfaces/tools.md) surface; the grammar both occupy is settled, so only the concrete
values remain — they are not frozen here.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| An explicit allocation policy, not magic numbers — reviewable and tunable. | Partial support from named unit tests: the attention suite's policy-values tests assert the committed policy file carries exactly the value keys the ranking tool reads (the dials live in the policy, not in code), and its effective-values tests cover the operator-override merge — the tunable half, including the refusal of a value the engine cannot measure. That the numbers are *reviewable* is your read of the policy file itself. | operator |
| Driven by [telemetry](../guardrails/telemetry.md) (debt) and [knowledge](knowledge.md) (structure), fed by [state](state.md); it reads these, it does not duplicate them. | Partial support from named unit tests: the attention suite's live-debt-register tests exercise telemetry-driven per-issue grading; its focus-set-walk and neighborhood tests exercise the knowledge-adjacency reads (the derive-focus tests cover the companion path→entity mapping); and the substrate assembler's state read is exercised in its own tests. The negative — reads, never duplicates — is an architectural property you confirm by the absence of any attention-owned store. | operator |
| A **deterministic** ranking function — the same inputs yield the same ordering; no scored-token store, no decay state, no machine learning. **Reference time is an explicit, recorded input** (a single as-of timestamp passed in), so "the same inputs" includes that timestamp — recency-dependent ordering is reproducible across clock skew and a ledger/host change, and the function still owns no state. | Strong partial support from named unit tests: the determinism tests assert byte-identical output on same inputs, input-order independence, and id tie-breaks; the reference-time tests assert the as-of moment is an explicit, echoed, reproducible input that is never a fresh clock read. The remaining negative — no scored-token store, no decay state, no machine learning — is structural (the pure ranking core holds no state), your read. | operator |
| **Degrades over partial inputs** — it ranks over whatever inputs are present; the loud, plain-language degraded notice is [boot](../lifecycle/boot.md)'s. | Partial support from named unit tests: the degrade tests assert absent substrates are recorded and sorted, every category is present even when empty, and the result carries no narration field — the ranking half. The loud plain-language notice is boot's and is verified on boot's own surface, not here. | operator |
| **Heritage:** attention is the prioritization piece of *context engineering* (the discipline of deciding what to load, exclude, prioritize, and prune in the context window — the orientation family as a whole instantiates it); in CoALA terms it sits within the *decision-making procedure*. (See the glossary *Lineage* cluster — maintainer vocabulary only, never operator-facing.) | No mechanical check can assert a lineage claim — this is an editorial attestation, carried by your read. | operator |
