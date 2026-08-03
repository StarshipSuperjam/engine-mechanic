---
status: draft
---

# delivery-evidence

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins.*

## Summary

The **optional** module that makes a delivery claim **provable and perishable**: every "it works" produced
by delivery work becomes an **evidence record** with a source, a revision it was measured against, and a
freshness state — and every change to the thing measured **invalidates** the evidence that depended on it,
visibly. Its second job is **final-snapshot assurance**: binding what was independently reviewed to the
exact commit that merges, so a material repair made after review can never silently ride an earlier
review's credibility. It extends the engine's existing evidence posture (demonstrations, checks, review
records) with a typed grammar the whole delivery plane shares; it never grades evidence as sufficient —
sufficiency stays with the review gates and the operator's merge.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `delivery-evidence` |
| `status` | `optional` |
| `provides` | the evidence **[schemas](../systems/surfaces/schemas.md)** (`evidence-record.v1` — kind, source, revision binding, freshness state; `effect-receipt.v1` — an external effect's target, actual observed result, and reconciliation state; `snapshot-assurance.v1` — reviewed commit, final commit, classified divergence); the **evidence [tool](../systems/surfaces/tools.md)** (`delivery_evidence.py` — record, invalidate, freshness-read; the invalidation sweep that marks dependents stale when their measured surface changes); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the stale-green check — no receipt may present invalidated evidence as current); and the **[doc](../systems/surfaces/docs.md)** explaining evidence kinds and freshness to the operator |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (records attach to runs; receipts cite evidence by identity) |
| `migrations` | none |

### The evidence model

- **Typed, source-bound records.** An evidence record names its kind (a check result, a test run, a
  demonstration, an observed external effect, a review finding), the exact source it came from (command,
  fixture, URL, artifact digest), and the revision(s) of the measured surface. Declared, observed, derived,
  and unavailable are distinct source lanes — a record never presents a derivation or a claim as an
  observation.
- **Freshness is mechanical, sufficiency is not.** A record is `current` until the surface it measured
  changes; the invalidation sweep then marks it `stale`, and the stale-green check makes presenting stale
  evidence as current a hard failure. Whether *current* evidence is *enough* is never this module's call.
- **Effect receipts reconcile claims with the world.** When delivery work causes an external effect (a
  deployment, a provider operation), the receipt records the intended effect, the independently observed
  actual state, and an explicit reconciliation outcome — `confirmed`, `partial`, `unknown` — so transport
  success (an exit code, an accepted request) is never recorded as an outcome by itself.
- **Final-snapshot assurance.** For work that passes independent review, the assurance record binds the
  reviewed commit to the submitted/merged commit, classifies what changed between them, and records whether
  a proportionate re-review ran. This realizes, in shared grammar, the divergence discipline the engine's
  build orchestration already practices by hand.

### Verification instruments

Engine-owned fixtures — staged scenarios a build is exercised against, including deliberately broken ones a
control must catch — are this module's normal proof vocabulary, as they are the corpus's. External corpora
or reference products may serve as evidence sources where a later document judges them useful. **No
instrument gates adoption**: under the program's rules, evidence thresholds never decide whether something
may be specified or built ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)).

### Degraded behavior

An evidence store that cannot be read refuses freshness queries with a plain reason — an unreadable record
is `unknown`, never `current`. If the invalidation sweep cannot run (a broken hook, an unhealthy runtime),
that is a fail-open finding surfaced through the engine's existing telemetry path, and receipts disclose
that freshness is unverified. Both runtimes share the committed store; renders never fork it.

### What stays out

- **No sufficiency judgment, no scoring.** Records and freshness only; gates and the operator decide.
- **No capture of prompts or transcripts.** Evidence records point at artifacts and results, never at
  conversation.
- **Not required**, and absent-by-default like the rest of the plane.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Records validate and lanes hold** — every evidence record conforms to schema, and no record's lane misstates derivation as observation. | Schema check rides CI (hard); lane honesty by operator read of staged records. | operator |
| **Invalidation actually bites** — changing a measured surface marks dependent evidence stale on the next sweep. | Fixture: measure, mutate, sweep, read freshness back. | engine |
| **Stale green is refused** — a receipt presenting invalidated evidence as current fails the stale-green check at merge. | Fixture: a staged stale-as-current receipt must be caught. | engine |
| **Transport is not an outcome** — an effect receipt whose actual-state observation is absent reads `unknown`, even with exit-zero transport. | Fixture: staged effect with observation withheld; receipt inspected. | operator |
| **Snapshot assurance is legible** — from one assurance record, a cold reader identifies the reviewed commit, the final commit, what changed between, and whether re-review ran. | Operator observation on a staged post-review-repair scenario. | operator |
| **Loud degradation** — unreadable store refuses with plain reason; a sweep that cannot run surfaces as a fail-open finding, and receipts disclose unverified freshness. | Fixture: store made unreadable; sweep disabled; outputs inspected. | operator |
