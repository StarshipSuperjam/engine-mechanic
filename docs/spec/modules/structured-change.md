---
status: draft
---

# structured-change

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins.*

## Summary

The **optional** module that separates **deciding a change from applying it**: reasoning produces a
**versioned pending change set** — a staged, revision-bound candidate of multi-file edits that can be
inspected, compared, revised, or rejected — and a conformant applier then lands it **atomically or not at
all**, with a typed receipt either way. It is the delivery plane's first reusable execution primitive: the
same staging-and-apply contract serves repairs, features, and refactors, so "the edit applied cleanly,
touched only what it claimed, and left recovery possible" is proven once, by contract, instead of re-trusted
per session. Git remains the recovery substrate; this module owns the mutation discipline above it.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `structured-change` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`pending-change-set.v1` — versioned candidate: per-file edits with base-content digests, expected impact reference, ordered typed operations; `apply-receipt.v1` — applied/refused/rolled-back, per-file result, post-apply validation states); the **[tools](../systems/surfaces/tools.md)** (`change_set.py` — stage/diff/revise/apply/rollback; the applier is the only writer path a delivery run uses for product mutation); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the foreign-work check — an apply that would touch uncommitted work it does not own must refuse); the **[operation](../systems/surfaces/operations.md)** runbook; and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (change sets bind to runs), `code-intelligence-core` (consumes the impact set as preflight; optional at runtime — absence degrades preflight, disclosed) |
| `migrations` | none |

### The mutation model

- **Staged before real.** A pending change set exists as versioned candidate state, never as workspace
  mutation. Revising produces a new version; superseded versions and rejections are preserved history, not
  overwritten. The workspace changes only at apply.
- **Base-bound and atomic.** Every per-file edit carries the digest of the content it was authored against.
  At apply time, any file whose current content does not match its base digest refuses the whole apply —
  atomic means all files or none, with a receipt naming exactly what mismatched. There is no partial
  landing and no fuzzy match that "probably" applied.
- **Foreign work is untouchable.** Dirty files the change set does not own are never absorbed, committed,
  or reverted by an apply or rollback. The foreign-work check makes the refusal mechanical. Rollback
  restores exactly the applied set's files to their pre-apply content — nothing else.
- **Semantic preflight, honestly typed.** Before apply, the candidate runs whatever static validation its
  profile provides (syntax, types, diagnostics through engineering-quality's contract when installed). A
  validation that timed out, was unavailable, or did not run is recorded `unknown` — an `unknown` never
  reads as passed, and profile policy decides whether `unknown` blocks apply. Per-diagnostic identity, not
  net counts: a candidate that fixes two old warnings while adding one new error is a new-error candidate.
- **Evidence invalidates on mutation.** A successful apply notifies delivery-evidence (when installed):
  evidence bound to the pre-apply revision of touched surfaces goes stale by the normal sweep. Receipts
  link the applied set, the resulting commit(s), and the run identity — the Git linkage a cold reader
  follows from diff to decision.
- **Typed operations beyond edits stay out of wave 1.** The change-set grammar reserves ordered typed
  operations (setup commands, migrations) but wave 1 ships file edits only; anything executable in a
  candidate is a later, separately-authorized extension — never smuggled in as "part of the apply".

### Degraded behavior

Without code-intelligence-core, preflight lacks an impact comparison and the receipt discloses it. Without
engineering-quality, semantic preflight is `unavailable` — typed, disclosed, policy-decided. An interrupted
apply leaves either the full set applied or the workspace at pre-apply state; a crash mid-apply is detected
at next read and resolved to one of the two, loudly. Both runtimes mutate only through the same applier
tool.

### What stays out

- **No auto-commit, no commit of foreign dirty state, ever.** Committing is the orchestrating session's
  explicit act, under the engine's normal build flow.
- **No hook-skipping.** An apply never bypasses the repository's own validation hooks; a skipped-hook
  commit is not a clean receipt.
- **No autonomous retry loops.** A refused apply reports; deciding to revise is the session's (and
  ultimately the operator's) call.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Atomic or refused** — a staged multi-file set with one base-digest mismatch applies nothing and names the mismatch; with all digests matching it applies whole. | Fixture: both scenarios staged; receipts and tree inspected. | engine |
| **Foreign work survives untouched** — an apply and a rollback in a tree with unrelated dirty files leave those files byte-identical, and an apply that would need to touch one refuses. | Fixture: seeded dirty foreign files; tree compared before/after. | engine |
| **Versioned candidate history holds** — revision produces a new version; rejected and superseded versions remain readable; nothing rewrites candidate history. | Operator observation on a staged revise/reject sequence. | operator |
| **`unknown` validation never passes silently** — a preflight with validation unavailable or timed out records `unknown`, the receipt discloses it, and profile policy (not silence) decides apply. | Fixture: validation tool withheld; receipt inspected. | operator |
| **Per-diagnostic gating** — a candidate resolving old warnings while introducing one new error is reported as introducing an error, never as a net improvement. | Fixture: the seeded old-warnings/new-error candidate; preflight report inspected. | operator |
| **Crash recovery is binary** — a kill injected mid-apply resolves at next read to fully-applied or pre-apply, stated plainly; no third state. | Fixture: injected interruption; recovery output and tree inspected. | operator |
| **Evidence goes stale on apply** — with delivery-evidence installed, evidence on touched surfaces reads stale after apply. | Fixture: measure, apply, freshness-read. | engine |
| **Edits only in wave 1** — a change set carrying an executable operation is refused by the applier as out of contract. | Fixture: staged operation-bearing set; refusal inspected. | engine |
