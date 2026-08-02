---
status: accepted
engine_record: true
---

# Adopt the built letter where locked module documents lag the build

*Decided 2026-08-02 in this repository, by the operator, in the wave-7 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). One batched
record for seven adoptions, each reversing or resolving a locked module document's letter in
favor of the build as shipped. Settles the register items **infrastructure-U31**,
**canon-wbs-U05**, **optional-modules-U06**, **cognitive-U22** (this surface's end), and
**optional-modules-U04**.*

## The decision

Seven places where a locked module document's letter lags the shipped build are **adopted as
built**:

- **The audit setup is three one-time steps, not two** (infrastructure-U31). The
  [audit-library](../spec/modules/audit-library.md) walkthrough's third step — GitHub's *Allow
  GitHub Actions to create and approve pull requests* — is a genuinely required precondition
  without which the digest pull request silently never appears; the `AUDIT_MODEL` repository
  variable and the schedule-resets-on-update warning are adopted with it.
- **The audit runs from either runtime.** The carried claim that the build stance "deliberately
  does not use" Codex is dropped: the module ships a Codex agent render and a full Codex
  Automation walkthrough beside the Claude Cloud path.
- **Migration-discipline's scope is the single rollback assertion** (optional-modules-U06). The
  carried provides row named a second assertion (a schema-changing PR carries a migration) that
  the built check and the built policy both explicitly disclaim, and the carried document's own
  Enforcement section already described only the rollback nudge; the internal contradiction
  resolves in the Enforcement section's favor.
- **Core's verb roster is the built set** (canon-wbs-U05): eight operator-typed skills —
  build-entry, help, status, policy-tuning, conduct-authoring, setup, parts, upgrade — plus the
  model-auto consultation verb admitted by
  [decision 0326](0326-admit-engine-recall-as-the-single-model-auto-skill.md). The carried
  five-verb enumeration is superseded; the admitting record the three unratified verbs owe
  upstream is tracked as
  [engine-template issue 799](https://github.com/StarshipSuperjam/engine-template/issues/799).
- **The dependency-review license gate carves out workflow-declared GitHub Actions.** GitHub
  reports no license data for that ecosystem, so blocking on an unidentifiable Actions license
  would block every action; the carve-out is deliberate, disclosed in the tool's own prose, and
  the vulnerability gate still applies to actions in full.
- **Memory's turn-capture is core's fail-soft relay** (cognitive-U22). The one Stop hook is
  core's; its close handler relays to memory's capture behind a swallow-everything guard, memory
  wires only its own SessionStart and PreCompact hooks, and write-safety is capture's serialized
  lock — not the carried "distinct Stop hooks" model.
- **The board's two debt figures are both described as built** (optional-modules-U04): the live
  open-issue count behind *Needs your review* and the committed cursor's cached count behind
  *Known issues*. The intent that the two must never silently disagree is **kept**, and the gap
  is annotated in the document against
  [engine-template issue 801](https://github.com/StarshipSuperjam/engine-template/issues/801).

## Why

Every item was verified live at the pin, and in each the build's choice is the better-argued
one: the third setup step is load-bearing fact, the dual-runtime is the settled fleet-wide
parity law, the migration check's narrow scope is its own documented design (with review
covering the rest), the verb roster grew by real shipped capabilities, the Actions carve-out
follows the data GitHub actually provides, the relay wiring achieves capture without a
dependency inversion, and the board fields are real signals whose one defect (silent
disagreement) is kept as intent and tracked. Grading the build down to any of these letters
would remove something true to restore something outdated.

## What we ruled out

**Keep each letter and file the build as defective** (rejected per item — none of the seven is a
defect; each is the build outgrowing a document written before it). **Adopt silently as
descriptive drift** (rejected — each reverses or resolves a locked document's deliberate
wording, so the batch belongs on the record; one clustered record over seven per-item records
follows the wave-5 precedent and keeps the decision log legible).
