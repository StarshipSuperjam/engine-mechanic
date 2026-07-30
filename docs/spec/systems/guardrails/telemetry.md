---
status: draft
---

# Telemetry

*Reconciled with engine-template@`cdbbc33` as built (2026-07-29) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-05-29 by [decision 0118](../../../adr/0118-q27-4-5-re-litigation-the-telemetry-finding-record-ambient-c.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

Answers **"is the Engine healthy?"** — and feeds the remediation loop. It is **self-surfacing**, not
self-healing ([D-009](../../../adr/0009-telemetry-is-a-remediation-loop-not-self-healing.md), Risk [R3](../../../reference/risks.md), [principle §8](../../../principles.md)):
it detects drift over the Engine's own work and surfaces it for the AI to fix next session, never
correcting autonomously.

Telemetry is **Engine-only self-monitoring** — it watches the Engine's own health, not the product's
quality. Product health is perceived through native GitHub signal and the locked
[finding-disposition](../surfaces/policies.md) routing, never a product-quality regime in the
foundation; a deeper product regime is an opt-in module. The split is by **subject of claim**: a signal
asserts either the Engine's health (engine-domain) or the product's (product-domain), and the domain is
carried as the **label** on the [tracked issue](../infrastructure/control-plane.md) it lands on.

## Behavior

### The judgment ladder

Three layers escalate the same question, each deferring semantic judgment to the one above:

- **[Validation](validation.md)** *(mechanical, per-event)* — does what got written match the
  schema/shape? (artifact-vs-contract)
- **Telemetry** *(mechanical, continuous, aggregate)* — are the signals trending bad?
- **[Audits](audits.md)** *(judgment, periodic)* — is the work still *good*, or has it drifted
  in ways no rule can catch? (contract-vs-reality)

Telemetry counts and trends; it never *reads* for meaning. Anything requiring judgment — "is this rule
still earning its place?", "is this drift meaningful?" — is an audit's job.

### Signal of record — native, no bespoke ledger

Telemetry derives its streams from the durable, native record, not from a hand-rolled log:

- **Default-branch CI outcomes**, read through the engine's shared authenticated GitHub client (direct
  REST calls — the one `gh` use in telemetry's own path is a token fallback at boot): the latest check-runs on the
  default branch's head, whose protected-branch checks are the authoritative pass/fail. Only a check
  with a definitive conclusion counts; a check that did not run is neither promoted nor resolved.
- **Best-effort ambient capture** of local check fires: the local [hooks](../infrastructure/hooks.md)
  that run checks append the fire and its pass/fail — the check's own verdict, re-derived by re-running
  the touched-file check unit inside the handler, never the hook's exit code — to a gitignored cache. Telemetry **owns the ambient-capture record shape and path** — a check-fire record
  `{rule-id, pass/fail, event-derived markers (the touched target, a timestamp)}`, distinct from the
  `finding.v1` base — and the `PostToolUse` writer conforms to it (the [§16](../../../principles.md) deferral
  seam: telemetry owns the channel's record, the hook relays; hooks registers no record shape of its own).
  This capture is **best-effort and never complete** — local runs are skippable, a
  `Stop` hook takes no matcher — so no telemetry law treats the ambient log as a guarantee. A signal that
  must be reliable is read from the native CI record or promoted to a tracked issue, never assumed from
  the ambient cache.
- **Memory-subsystem health**, as the one memory-fed signal built: a degraded memory-capture state
  arrives as a persistent-benign finding. No stream derives from the ledger's episodic content as
  built — that stays an unbuilt leaf of the additive streams set below.

There is **no committed check-fire ledger** (it would rebuild the dissolved session archive,
[D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)) and **no requirement that the validator emit a structured PR outcome**
(the required CI check is a single coarse pass/fail; finer per-rule signal comes from ambient capture and
from findings, so [validation](validation.md) and the [control-plane](../infrastructure/control-plane.md)
are left exactly as locked).

### Streams

A **stream** is a derived signal series computed over the native record, carrying a **severity class**.
The set of derived streams as built — CI outcomes, persistent ambient warnings, never-fired rules, the
contract-creation rate, and the **triage-pressure** stream below — is leaves, not law, and grows
additively. (A gate-evaluation failure is not a stream: it arrives as an immediate finding through the
hooks fail-open path. Open findings awaiting remediation are the issue register itself, surfaced by
[state](../cognitive/state.md)'s count and [attention](../cognitive/attention.md), not re-derived as a
series.) The **stream cache is
gitignored** — it is a derivative regenerable from the native record and the ambient cache
([principle §2](../../../principles.md)), so it never bloats the committed tree and an engine upgrade
cannot collide with it.

Telemetry emits the *never-fired signal* for a rule; whether a never-fired rule should be **retired** is a
judgment that belongs to [audits](audits.md), not here. As built the signal is the literal reading —
a file-scoped rule that **currently selects zero files** — not a fire-history reading, which the build
records as out of v1's reach without a committed ledger; the feed frames each item as a question for
the audit, never a verdict.

#### The triage-pressure stream — standing volume made visible, render-only

The **triage-pressure stream** is the count of open low-severity engine-labeled issues. Its threshold
lives in the governed promotion [policy](../surfaces/policies.md) instance (legible and tunable,
[§7](../../../principles.md)); when the count crosses it, the next [boot](../lifecycle/boot.md)
orientation **renders one plain-language line** ("the engine's self-monitoring backlog is growing"). This
stream is **render-only: crossing its threshold promotes *nothing*** — it never itself becomes a tracked
issue, so the meter cannot feed the volume it measures. It is the visibility half of the volume story; the
*bound* is structural (see triage), not this signal.

### Tracked debt and findings — engine-labeled GitHub Issues

Durable, tracked work lives where the locked [finding-disposition](../surfaces/policies.md)
policy already routes it: a **tracked issue (a [control-plane](../infrastructure/control-plane.md)
issue scaffold)**. Engine self-monitoring debt is an **engine-labeled GitHub Issue**.

Because these issues appear in the operator's own tracker without the operator creating them, each one
carries a **plain-language operator contract**: its title and body identify it, in non-engineer terms, as
the **engine noticing something about its own health** — not a problem with the operator's product — and
say what it means and what (if anything) the operator must decide. The backstage vocabulary of this system
(streams, severity class, persistence threshold) **never reaches the operator**; it stays in the policy and
the code. The one-time orientation that teaches an operator *what engine-labeled issues are in general* is
[provisioning](../infrastructure/provisioning.md)'s first-run concern, not telemetry's.

- **The "debt register" is the view over open engine-labeled issues** — not a committed or gitignored
  file. Issues are native, citable, operator-visible, survive a machine loss, and cannot be clobbered by
  an engine overlay (they are not files). This is how telemetry **owns** debt while
  [knowledge](../cognitive/knowledge.md) stays purely surface-derived and carries none of it
  ([D-031](../../../adr/0031-integration-debt-is-a-telemetry-owned-register-not-a-knowled.md)); a debt issue *references* knowledge entity-ids for "what is broken."
- **[State](../cognitive/state.md)** keeps only a **count/pointer** to open engine debt — a
  permitted committed pointer ([repository-topology](../infrastructure/repository-topology.md)
  law 5) — so a cold read knows debt exists and where to look.
- **[Attention](../cognitive/attention.md)** surfaces open debt at boot in priority order
  (a deferred reference — the surfacing mechanism is attention's, not telemetry's).

#### Findings inbox — cognition emits, telemetry acts

The "oh weird, moving on" failure is the locked finding-disposition problem. Its **"log it"** disposition
routes here: any session, a [hooks](../infrastructure/hooks.md) fail-open flag, or a
[boot](../lifecycle/boot.md) degradation **emits a finding** and is done — it carries no weight
for acting on it. Telemetry consumes, deduplicates, promotes, and surfaces. This is the clean seam that
keeps the cognitive substrates out of the act-on-it loop. The **finding-record** telemetry consumes extends
the canonical [`finding.v1`](../surfaces/schemas.md) base ([D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)) with
telemetry's own markers — a **`source-id`** (the rule-id / surface-id / stream-id that keys dedup, below) and
**first-seen / last-seen observation markers** (which auto-resolve reads to close a now-absent signal, below);
the base `severity` is telemetry's per-consumer **severity class** (`trust-critical` | `persistent-but-benign`),
distinct from the agent and check enums.

### Triage and promotion

Triage is the only thing telemetry does autonomously, and it does exactly one write: **open or update an
engine-labeled issue** when a signal warrants tracking, deduplicated by a **stable key** so a recurring
signal updates the one issue rather than spawning duplicates — and when a create/create race has already
spawned duplicates, triage consolidates them, keeping the lowest-numbered survivor and closing the rest
with a note. The key is derived from the signal's
**source identity** — the rule-id, surface-id, or stream-id that emitted it — **never** from per-occurrence
material (the file, run, or parameter the signal was observed on).

**The bound on triage volume is structural, not a cap.** Because the key is source-keyed and telemetry is
**Engine-only** (it watches the engine's own surfaces, never product files), every recurrence of a signal
collapses onto one issue, and the open-issue count is bounded above by the engine's own inventory of signal
sources — finite at any instant, growing only as the engine itself gains rules, **not** scaling with product
size or recurrence. A hard cap that *drops* or *coalesces* low-severity signal once a limit is hit is
deliberately rejected: it would force telemetry to decide *which* signals matter (a judgment that is
[audits](audits.md)' job) or to alter standing state autonomously (toward self-healing), against
its mechanical-only and report-never-heal commitments. A persistent benign signal keeping one issue open is
*correct* — the signal is still true — and auto-resolve closes it when the signal is observed clear; retiring a
now-irrelevant signal *source* is ordinary audits/Build work, not a telemetry mechanism.

- **Severity class and signal substrate together set promotion latency.** A **trust-critical** signal —
  a gate or check-kind that *could not run* — promotes **immediately**. A **persistent-but-benign**
  signal's latency depends on its substrate: one derived **live** from the native record (a CI failure
  on the default branch's head) is tracked on its first observation — the record is authoritative, so
  waiting adds nothing — while one accrued from the **best-effort caches** (ambient fires, the findings
  inbox) promotes only after it crosses a **persistence threshold**.
- **Thresholds live in a governed [policy](../surfaces/policies.md)**, not buried in code
  (Risk [R4](../../../reference/risks.md)) — legible and tunable.
- **Resolution closes the issue — on positive clearance, never mere absence.** **Auto-resolve clears
  the flag** when the originating signal is *observed clear*: a pass on the same source, or the target
  it fired on gone. A signal that merely stops appearing — a skipped local run, an unreadable cache, a
  check that did not execute — is carried forward untouched, so absence never manufactures a false
  all-clear. It **does not repair anything**; the fix was a remediation PR, and auto-resolve only
  retires the now-clear signal.

### Output home

Telemetry's outputs are **system-owned, non-surface** artifacts (like check-suites and module manifests,
not catalog [surfaces](../grammar/ontology.md)): the **gitignored stream cache**, and the
tracked issues (control-plane infrastructure artifacts). The one committed, human-readable observational
artifact is the **audit digest**, owned by [audits](audits.md) (a derived, fingerprint-gated
snapshot, the self-map precedent). Telemetry itself commits no report; it surfaces continuously through
boot, the issues, and the digest. The tier-4 "observational" authority class needs no catalogued members,
so the [ontology](../grammar/ontology.md) is untouched.

### Remediation and upgrade-safety

Surfaced debt is fixed as ordinary [Build](../lifecycle/build-orchestration.md) work: a draft
PR is the claim, the fix's CI plus the debt's clearing signal is the validation, and the operator's merge
is the gate (a deferred reference — the pipeline is build-orchestration's). Telemetry never affects the
Engine's upgradeability: its gitignored cache is preserved across an engine overlay
([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)) and its issues are not files at all. Remediation edits engine
*content* (preserved by the overlay), never engine *machinery* (template-owned and overlaid) — a bug in
the machinery takes the **escalate** disposition upstream rather than a local patch the next overlay would
revert.

### Build-spec leaves

The **forms** above are pinned; only their concrete **values** are build-spec leaves, authored and
fixture-tested in the build session (laws-not-leaves, [D-052](../../../adr/0052-foundational-law-layer-closed-the-implementation-lock-order.md); pin the form, defer
the values, [D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)): the **finding-record JSON Schema** (the `finding.v1` base
extended with `source-id` + first/last-seen markers), the **ambient-capture record JSON Schema and cache
path** (the check-fire shape telemetry owns), and the gitignored **stream-cache** layout. The three
promotion **threshold values** (persistence, auto-resolve N-observations, triage-pressure) are **not**
telemetry's leaf — they live in the governed triage-threshold [policy](../surfaces/policies.md)
telemetry reads ([D-114](../../../adr/0114-q25-re-litigation-a-fourth-v1-core-policy-the-triage-thresho.md)).

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Self-surfacing, not self-healing** — triage (open/update an issue) is the only autonomous step; the AI remediates next session, under guardrails, and the operator merges. Never claim it heals unattended. | Observe, in your deployed engine, the tool's runnable demo walkthrough: triage's only writes are issue open/update/close, and the degraded path makes none. The unit test asserting zero issue writes on a degraded read is partial support; the demo's aggregate self-check is inert at the reconciliation pin (a defect swallowed by its fail-open handler — it cannot fail the run; tracked as [engine-template#769](https://github.com/StarshipSuperjam/engine-template/issues/769)), so it supports nothing. No check asserts the whole never-heals claim. | operator |
| **Mechanical only** — telemetry trends and counts; it makes no judgment call. Judgment is the audits rung. | Observe that every judgment is deferred: retirement questions route to the audit, and the never-firing feed frames each item as a question, not a verdict — read in the demo's printed walkthrough (its aggregate self-check being inert at the pin, per the row above); no check asserts the general no-judgment property. | operator |
| **Native and degradable** — signal of record is the native GitHub/CI record plus a best-effort ambient cache; on a GitHub outage boot still reads State's committed count, so the operator is never stranded. In that degraded state the boot line says so in plain language — it names the open-debt count *and* states that the per-issue detail is temporarily unreachable until GitHub returns — so the operator sees a calm, explained gap rather than a silent or alarming one. | Partial support from named unit tests: the degraded line names the open-debt count, says to re-ground, ends "until GitHub returns", and makes no issue writes. The per-issue-detail sentence itself and the end-to-end boot render rest on your observation of the degraded boot line. | operator |
