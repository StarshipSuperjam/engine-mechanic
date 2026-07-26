---
status: accepted
engine_record: true
---

# Resolve: re-lock `product-design` — a coupled carrier surfaced by D-291's landed-text audit (it still asserted the pre-split `spec-conformance`-carrying-the-posture model; reconciled to the paired-lens split)

*Decided 2026-07-11 in the design workspace.*

## The decision

Re-lock [product-design](../spec/modules/product-design.md), a **coupled carrier surfaced by [D-291](0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md)'s mandatory landed-text cold audit** — not in D-291's original carrier list, added here at the landed-text stage (the [D-283](0283-litigate-engine-template-361-a-pr-accidentally-auto-closes-a.md) "a carrier not pre-judged but decided against the landed text" pattern). **The BLOCKING finding (adversarial+feasibility lens, convergent):** product-design's floor-legs list still described *"the `spec-conformance` judgment … carrying the adversarial divergence-hunter **posture** … so a semantic misbuild … is *hunted*"* — the **superseded** [D-290](0290-resolve-re-lock-qa-review-the-spec-conformance-lens-carries.md) posture-fold, now a flat contradiction of the paired-lens split landed in [qa-review](../spec/modules/qa-review.md)/[build-orchestration](../spec/systems/lifecycle/build-orchestration.md)/[engine-architecture](../architecture.md)/[glossary](../reference/glossary.md) (three locked docs disagreeing on posture-vs-lens). The change-propagation matrix's *"reconcile the module's own doc"* made product-design mandatory; it was missed. **Folded before re-lock:** the floor-legs bullet reshaped to the **paired judgment lenses** — `spec-conformance` (systematic) + `divergence-hunter` (adversarial, run beside it), both re-deriving from the span and judging only `locked` rows — mirroring the already-audited [engine-architecture](../architecture.md) phrasing (no new design, a reconciliation to the audited model). A focused re-read confirmed the reconciled bullet introduces no new contradiction and no residual "posture" phrasing survives corpus-wide. `python3 lock.py --relock modules/product-design/README.md --decision D-294`; `validate.py` green.

## Why

the landed-text audit did exactly its job — it caught a locked sibling the plan-stage propagation missed, before the irreversible re-locks shipped three disagreeing locked docs. Reconciling product-design to the audited split (not a fresh design) is the honest close; homing it in a distinct resolve entry keeps D-291 append-only and records the miss transparently.

## What we ruled out

**Edit [D-291](0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md) to add product-design to its carrier list** (rejected — the decision-log is append-only; the correction is recorded here, the [D-283](0283-litigate-engine-template-361-a-pr-accidentally-auto-closes-a.md)/[D-284](0284-resolve-re-lock-build-orchestration-the-submit-time-close-li.md) resolve-stage-carrier precedent). **Leave product-design's posture text and re-lock only qa-review/build-orchestration** (rejected — a silent locked-doc contradiction is precisely the [§7](../principles.md)/authoring-rule-1 failure the landed-text gate exists to stop). **Also re-lock [agents](../spec/systems/surfaces/agents.md) for its one-behind pre-submission lens illustration** (rejected — **verify-no-edit**: that enumeration is an explicitly **non-exhaustive** illustration of the open/additive `lens` axis ("open and additive, a module may ship a new lens"), makes no completeness claim, and roster membership is enforced by build-orchestration's consumed-set + the §14 coherence check — a fourth re-lock for a non-false illustration is the [R6](../reference/risks.md) over-reach the architect lens flagged).
