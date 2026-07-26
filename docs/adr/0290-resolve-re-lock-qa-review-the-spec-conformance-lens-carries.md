---
status: accepted
engine_record: true
---

# Resolve: re-lock `qa-review` (the `spec-conformance` lens carries the adversarial divergence-hunter posture and runs the deployed-environment demonstration harness as its disclosed dry-run, judging only locked rows, re-deriving from the spec span never the matrix) — a carrier of [D-287](0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md)

*Decided 2026-07-06 in the design workspace.*

## The decision

Re-lock [qa-review](../spec/modules/qa-review.md), a carrier of [D-287](0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md). The landed text — lens 1's adversarial divergence-hunter posture, the re-derive-from-span honest tier, the locked-row scope, and the demonstration-harness dry-run — passed the landed-text audit. `python3 lock.py --relock modules/qa-review/README.md --decision D-290`; `validate.py` green.

## Why

qa-review owns the judgment + demonstration legs (consumed-by product-design's referent, no hard `depends`). The adversarial posture is persona-brief text on an already-locked surface — no new grammar.

## What we ruled out

**Ship the charitable single-lens posture** (rejected — leaves the shipped review weaker than the instrument that built the engine; the audit's core complaint). **Gate the agentic verdict mechanically** (rejected — "a persona judges, a check gates, never duplicate"; the judgment surfaces at the operator's merge, the matrix is the mechanical gate).
