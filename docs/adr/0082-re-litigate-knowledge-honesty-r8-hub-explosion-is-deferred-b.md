---
status: accepted
engine_record: true
---

# Re-litigate `knowledge` (honesty): R8 hub-explosion is *deferred behind a swappable seam*, not *mitigated*

*Decided 2026-05-27 in the design workspace.*

## The decision

Under the litigation-alarm protocol (operator-approved as part of the cognitive-substrate remediation plan), re-litigate [knowledge](../spec/systems/cognitive/knowledge.md) with one **honesty / current-state** correction surfaced by the efficacy-scorecard audit: the Heritage bullet said R8 (dense-graph hub-explosion) "stays open, **mitigated** by keeping the representation swappable" — but swappability is the ability to change the representation later, not a containment of the failure. Reword to **"deferred behind a swappable representation seam, not mitigated."** **No design law changes:** the swappable-leaf interface binding, the derived-graph laws, and R8's conditional/low severity are untouched; only the verb moves to current truth. `python3 lock.py --relock systems/cognitive/knowledge/README.md --decision D-082`; ratified_by D-082.

## Why

The [D-074](0074-sweep-the-stale-q1-references-resolved-by-d-066-d-068-re-loc.md)/[D-078](0078-citation-accuracy-re-litigation-repoint-stale-q4-references.md)/[D-080](0080-re-litigate-state-honesty-name-the-floor-s-known-unbounded-f.md) precedent: an honesty/current-state correction touching **no design surface** is re-litigated proportionately (`validate.py` link + lock-fingerprint integrity, a current-state self-check, and the remediation plan's 5-lens cold audit), not a fresh four-lens per-system audit. The scorecard's adversarial lens flagged "mitigated" as overstating a containment the design does not have — v1's plain per-surface JSON does not trigger hub-explosion, and the swappable seam is the route to *fix* it if a dense representation is ever adopted, not a present mitigation. Propagation per the matrix: [knowledge](../spec/systems/cognitive/knowledge.md) (re-locked end-state), this entry; [risks.md](../reference/risks.md) R8 verified already consistent — it reads as a conditional, still-open risk whose "mitigation direction" is keeping the leaf swappable and claims no closure (no edit); glossary/architecture index unaffected; [scenarios/first-run.md](../architecture.md#first-run-provisioning) and [scenarios/remediation-loop.md](../architecture.md#the-detect-to-remediate-loop) reference knowledge derivation, unaffected.

## What we ruled out

**Leave "mitigated"** (rejected — a locked living doc claiming a containment it lacks is the current-state falsehood the [D-074](0074-sweep-the-stale-q1-references-resolved-by-d-066-d-068-re-loc.md)/[D-080](0080-re-litigate-state-honesty-name-the-floor-s-known-unbounded-f.md) pattern fixes). **Choose a representation engine now to actually mitigate R8** (rejected — that is the deferred swap tracked in [open-questions](../reference/open-questions.md); v1's representation does not trigger the pathology, so R8 stays low/conditional). **Run a full four-lens cold audit** (rejected as disproportionate — no design law changes).
