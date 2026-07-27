---
status: accepted
engine_record: true
---

# Resolve: re-lock `build-orchestration` (the referent section runs the conformance-enforcement floor at the merge — matrix coverage denominator + adversarial `spec-conformance` + demonstration harness, criterion-granular, per-locked-row, conditional on a `locked` `docs/spec/`; resolves ledger lifecycle-U14) — a carrier of [D-287](0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md)

*Decided 2026-07-06 in the design workspace.*

## The decision

Re-lock [build-orchestration](../spec/systems/lifecycle/build-orchestration.md), a carrier of [D-287](0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md). The landed text — the deepened referent floor, the per-locked-row scope, the re-derive-from-span rule, the demonstration-harness / AI-run-`demo` distinction, and the [§12](../principles.md) leak-guard list naming the new maintainer vocabulary — passed the landed-text audit; the re-lock diff carries **only** floor-related deltas (no [D-284](0284-resolve-re-lock-build-orchestration-the-submit-time-close-li.md) close-linkage / lifecycle-U03 cost-estimate creep, [R6](../reference/risks.md)). Resolves ledger lifecycle-U14 criterion-granular. `python3 lock.py --relock systems/lifecycle/build-orchestration/README.md --decision D-289`; `validate.py` green for this fingerprint.

## Why

build-orchestration runs the floor at the merge; its re-lock lands after the clean audit. Criterion-granularity discharges the D-247(4) letter via the derived matrix.

## What we ruled out

**Keep the coverage floor capability-granular** (rejected — the derived criterion-ID scheme makes criterion-granular reachable without forbidden structure, the letter-conformant direction). **Fold unrelated Wave-D items** (rejected — [R6](../reference/risks.md) surgical scope).
