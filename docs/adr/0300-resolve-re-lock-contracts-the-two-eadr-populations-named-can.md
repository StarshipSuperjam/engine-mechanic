---
status: accepted
engine_record: true
---

# Resolve: re-lock `contracts` (the two eADR populations named — canon `eADR-####`, a deployment's per-instance stream `<project-slug>-eADR-####`; overlay-by-path, reader-by-namespace) — a carrier of [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md)

*Decided 2026-07-12 in the design workspace.*

## The decision

Re-lock [contracts](../spec/systems/surfaces/contracts.md), a carrier of [D-298](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md). The landed text — the "Shape and storage" two-scheme naming, the "foundational canon" population split reconciled so the overlay is told apart **by path / engine-owned-set membership, never by a content marker** while the reader is told apart **by id namespace**, the per-instance-stream bullet naming `<project-slug>-eADR-####` as the human-facing wall applying the ontology law one level in, and the "Design commitments" summary — passed the four-lens landed-text cold audit recorded in [D-299](0299-resolve-re-lock-ontology-the-instance-identifier-law-gains-t.md) (no BLOCKING; no SERIOUS against design soundness; all serious/nits dispositioned or carried to the build-owe issue). `python3 lock.py --relock systems/surfaces/contracts/README.md --decision D-300`; `validate.py` green for this fingerprint.

## Why

contracts re-locks after ontology (grammar before surface). Its edits carry only the D-298 two-scheme deltas ([R6](../reference/risks.md) surgical scope); the population split is now truthful for both the overlay (path/`provides`) and the reader (id namespace) without disturbing the overlay classifier or CODEOWNERS.

## What we ruled out

**Edit [product-design](../spec/modules/product-design.md):149 to name both schemes** (rejected — a literally-true locked module line does not warrant a third re-lock + module-gate; the glossary carries the complete statement). **Fold both re-locks into one resolve entry** (rejected — the [D-293](0293-resolve-re-lock-build-orchestration-roster-divergence-hunter.md)/[D-294](0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md) per-carrier precedent gives each re-locked doc its own fingerprint-bearing record).

## Further record

### Disposition (architect SERIOUS, [D-299](0299-resolve-re-lock-ontology-the-instance-identifier-law-gains-t.md) audit)

[product-design](../spec/modules/product-design.md):149 ("the product's own numbering … never the engine's `eADR-####`") is **verify-no-edit** — it stays literally true (a product ADR is neither engine scheme), so editing the locked module doc to also name the deployment scheme is [R6](../reference/risks.md) over-reach that would blow the re-lock set to three under the heavier module-doc gate. The complete statement lives in the [glossary](../reference/glossary.md) *Product ADR* term (updated to exclude both engine schemes); the *unlocked* [scenarios/product-design-intake.md](../architecture.md#product-design-intake) contrast was mirrored as a free propagation touch. The asymmetry (canonical term names both, the scoped module mention names one) is recorded and accepted, not a contradiction.
