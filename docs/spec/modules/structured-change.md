---
status: draft
---

# structured-change

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins. Revised in draft after four cold design reviews; the
largest changes: the write-ahead journal that makes atomicity real, two-stage receipts, and honest-tier
wording on the writer path.*

## Summary

The **required** module that separates **deciding a change from applying it**: reasoning produces a
**versioned pending change set** — a staged, revision-bound candidate of multi-file edits that can be
inspected, diffed against other versions, revised, or rejected — and a conformant applier then lands it
**atomically or not at all**, journaled so a crash can always be resolved, with a typed receipt either way.
It is the delivery plane's first reusable execution primitive. Its writer-path discipline is stated at its
honest tier: the applier is the **intended** mutation path for delivery runs — a posture, like the engine's
other in-session disciplines — backstopped mechanically by an orphan-mutation check at the merge gate and
ultimately by the operator's merge. Base-digest binding is drift detection, an integrity property; the
authorization gate for any change remains the human at the merge.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `structured-change` |
| `distribution` | `required` |
| `applicability` | `detected` (a product with mutable code) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`pending-change-set.v1` — versioned candidate: per-file edits with **raw-byte** base-content digests (no normalization; one meaning of "matches"), the expected-impact reference (optional, and valid only when it shares the change set's base digests), and the reserved ordered-operation grammar — representable so the refusal fixture can stage it, **never executed in wave 1**; `apply-receipt.v1` — applied/refused/rolled-back, per-file result, the touched files' post-apply digests, preflight validation states, and — appended at the session's later explicit commit — the resulting commit identity); the **[tools](../systems/surfaces/tools.md)** (`change_set.py` — stage/diff/compare/revise/apply/rollback); hard **[checks](../systems/surfaces/check.md)** (schema conformance; the **foreign-work fixture check** — a committed negative fixture proving the applier refuses a set that would touch unowned dirty work; the **orphan-mutation check** — a `custom/script` CI check flagging a delivery run whose diff contains product mutations no apply-receipt covers; each hard check carries its negative fixture per the hard-check-bite discipline); the **[operation](../systems/surfaces/operations.md)** runbook (`.engine/operations/structured-change.md`); and the operator **[doc](../systems/surfaces/docs.md)** (`.engine/docs/structured-change.md`) |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (change sets bind to runs of open tasks; retry ceilings come from the task's recorded attempt budget) |
| `migrations` | none |

[code-intelligence-core](code-intelligence-core.md), [delivery-evidence](delivery-evidence.md), and
[engineering-quality](engineering-quality.md) are **when-installed integrations, deliberately not
dependencies**: their absence degrades specific behaviors, disclosed per the sections below. (The module
grammar has no soft-dependency channel; `depends` asserts presence, so optional integrations stay out of it.)

### The mutation model

- **Staged before real.** A pending change set exists as versioned candidate state, never as workspace
  mutation. Revising produces a new version; superseded versions and rejections are preserved, readable
  history; `compare` diffs any two versions. Candidate state and receipts live committed under the delivery
  state home (cold-readable, like the run ledger); pruning old candidate payloads is a recorded maintenance
  decision, never silent.
- **Base-bound and atomic.** Every per-file edit carries the raw-byte digest of the content it was authored
  against. At apply, all digests are verified before any write; one mismatch refuses the whole set with a
  receipt naming it. A single-flight per-worktree lock spans verify-through-write, closing the
  check-to-use window.
- **Journaled, so atomic survives a crash.** Before the first byte is written, the applier makes durable an
  **intent journal** — the owned file set, each file's pre-apply content, the targets — plus an
  **in-progress sentinel** any reader can see. A crash mid-apply is resolved at the next tool read from the
  journal: roll forward to fully-applied or restore to pre-apply, touching **only the owned set** (never
  `git checkout`, which would clobber foreign dirty work — the journal, not Git, is the recovery substrate
  for uncommitted state). "No third state" is a property of reads through the tool; mid-flight, other
  observers see the sentinel, never a silently indeterminate tree.
- **Foreign work is untouchable.** Dirty files the set does not own are never absorbed, committed, or
  reverted. Rollback restores the owned set from the journal — and runs a post-apply-drift check first: an
  owned file edited since apply refuses rollback unless explicitly forced, with the force disclosed in the
  receipt.
- **Semantic preflight, honestly typed.** Before apply, the candidate runs the static validation its
  installed profile provides ([engineering-quality](engineering-quality.md), when installed; the expected-
  impact comparison, when [code-intelligence-core](code-intelligence-core.md) is installed and its impact
  set shares the base digests — a stale impact set is disclosed, and profile policy decides). Validation
  that timed out, was unavailable, or did not run is `unknown`; an `unknown` never reads as passed, and
  profile policy decides whether it blocks. Per-diagnostic identity, never net counts.
- **Receipts are two-stage; freshness needs no notification.** The apply-receipt lands at apply with the
  tree result and touched digests; the session's later, explicit commit appends the commit identity. There
  is no auto-commit and no invalidation message: [delivery-evidence](delivery-evidence.md) derives
  freshness from content digests at read, so any mutation — applier-mediated or not — stales dependent
  evidence the moment it is read or gated. After apply, the receipt records the actual touched set against
  the expected impact reference; a mismatch is a named preflight-vs-actual finding.

### Degraded behavior

**Inactive** where a sibling is not present: without code-intelligence-core, no impact comparison,
disclosed; without engineering-quality, preflight `unavailable`, typed, policy-decided; without
delivery-evidence, the receipt still records touched digests and the evidence-staleness criterion is a
disclosed non-run, never a vacuous pass. **Faulted** — an unreadable journal or candidate store refuses
apply/rollback with a plain reason. Both runtimes use the same tool; concurrent
worktrees resolve at the git merge like any committed state.

### What stays out

- **No auto-commit, ever.** Committing is the orchestrating session's explicit act under the engine's
  normal build flow; the receipt records the commit identity when it happens and claims nothing about it
  before.
- **No autonomous retry loops.** A refused apply reports. Retry ceilings are the task's recorded attempt
  budget in [delivery-core](delivery-core.md) — the stop that holds even in unattended runs.
- **No executable operations.** The applier refuses any operation-bearing set; edits only in wave 1. A
  deployment wanting stricter posture may deny the runtimes' native edit tools for delivery runs so the
  applier is the only available writer — a build-time hardening option, not a wave-1 claim.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it. Intra-wave ordering: the evidence and per-diagnostic fixtures run against
delivery-evidence and a stub validator respectively until those siblings are built — stated, not hidden.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Atomic or refused** — one digest mismatch applies nothing and names it; all matching applies whole. | Fixture: both scenarios; receipts and tree inspected (negative fixture per hard-check-bite). | engine |
| **Foreign work survives untouched** — apply and rollback leave unowned dirty files byte-identical; a set needing one refuses. | Fixture: seeded dirty foreign files; byte comparison. | engine |
| **Crash resolves from the journal** — interruption injected at each write boundary resolves at next read to fully-applied or pre-apply, owned files only; the sentinel is visible mid-flight. (Injected-seam fidelity, not true power loss — disclosed.) | Fixture: per-boundary injections; recovery and tree inspected. | engine |
| **`unknown` never passes silently** — withheld validation records `unknown`, disclosed; policy, not silence, decides. | Fixture: validation withheld; receipt inspected. | engine |
| **Per-diagnostic gating** — old-warnings-fixed/new-error-added reports the new error, never a net improvement. | Fixture: seeded candidate against the stub validator. | engine |
| **Candidate history immutable; compare works** — revise creates versions, rejections stay readable, `compare` diffs any two. | Fixture: revise/reject/compare sequence. | engine |
| **Orphan mutation flagged** — a delivery-run diff containing product mutation without a covering receipt fails the CI check. | Fixture: staged uncovered mutation (negative fixture). | engine |
| **Impact anchor enforced** — an impact reference not sharing base digests is disclosed stale; post-apply touched-vs-expected mismatch is a named finding. | Fixture: stale impact set; over-touch scenario. | operator |
| **Operations refused** — an operation-bearing set is refused by the applier as out of contract. | Fixture: staged operation-bearing set. | engine |
| **Rollback drift guard** — an owned file edited post-apply refuses rollback unless forced; the force is disclosed. | Fixture: post-apply edit then rollback. | operator |
