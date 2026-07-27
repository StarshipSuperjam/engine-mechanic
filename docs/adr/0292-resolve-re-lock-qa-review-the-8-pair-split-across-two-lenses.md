---
status: accepted
engine_record: true
---

# Resolve: re-lock `qa-review` (the §8 pair split across two lenses — `spec-conformance` the systematic reviewer + a distinct fifth `divergence-hunter`, coupled; the narrow diff-introduced over-build; the `technical-integrity` whole-repo dead-code boundary) — a carrier of D-291

*Decided 2026-07-11 in the design workspace.*

## The decision

Re-lock [qa-review](../spec/modules/qa-review.md), a carrier of [D-291](0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md). The landed text — `provides` five / *The five lenses* / consumes-all-five; `spec-conformance` reshaped to the **systematic conformance reviewer** paired with the new fifth lens; the new **`divergence-hunter`** (adversarial default-to-divergent hunt + the narrow, diff-introduced, ground-truthed over-build suspicion, coupled to run with `spec-conformance`, `locked`-row scope, re-derive-from-span, disclosed no-op); the `technical-integrity` whole-repo dead-code boundary; and the two-judgment-legs *conformance guard* commitment — passed the mandatory **landed-text cold audit** (the irreversible-relock gate, CLAUDE.md). **The four-lens audit** (faithfulness/propagation · adversarial+feasibility · non-engineer-operator · architect/seam, no shared context): **faithfulness CLEAN, operator+architect no-blocking, the one convergent BLOCKING was a *propagation miss in a sibling carrier* (product-design), not in qa-review** — folded before this re-lock (resolved under [D-294](0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md)). The three plan-stage blockers are confirmed genuinely closed in qa-review's landed text: the over-build arm is diff-scoped, span-derived, orchestrator-ground-truthed, and explicitly **never** whole-repo / **never** "any code not tracing to a `locked` row" (the [§20](../principles.md) false-positive storm gone); the hunter is **coupled** to `spec-conformance` (the [D-290](0290-resolve-re-lock-qa-review-the-spec-conformance-lens-carries.md) charitable-lens regression closed) which stays the **systematic, no-charity** reviewer (not charitable); the `technical-integrity` boundary partitions by referent with no double-count. **Nits folded before re-lock:** the "Depth is proportionate" no-op now names **both** paired lenses (the [§17](../principles.md) silent-no-op seam); "never double-count" sharpened to "judge different properties, never duplicating a finding" (the orthogonal-axes precision). `python3 lock.py --relock modules/qa-review/README.md --decision D-292`; `validate.py` green.

## Why

qa-review is the roster producer and D-291's primary carrier; its re-lock lands after the clean landed-text audit. The audit earned its keep — it confirmed the narrow over-build scope and the coupling held in the *landed* text, and it caught the product-design sibling that still asserted the pre-split posture-fold (folded under D-294 before any re-lock).

## What we ruled out

**Re-lock before folding the "Depth is proportionate" no-op seam** (rejected — a quintet whose fifth lens silently no-ops absent a `locked` spec must name that no-op where the reader looks for it, [§17](../principles.md)). **Re-lock while a sibling carrier (product-design) still contradicts the split** (rejected — three locked docs disagreeing on posture-vs-lens is the exact semantic contradiction the landed-text audit exists to catch; product-design reconciled under [D-294](0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md) first).
