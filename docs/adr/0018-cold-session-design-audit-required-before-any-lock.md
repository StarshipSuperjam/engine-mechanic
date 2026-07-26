---
status: accepted
engine_record: true
---

# Cold-session design audit required before any lock

*Decided 2026-05-22 in the design workspace.*

## The decision

Amend `CLAUDE.md` to make a **cold-context multi-voice review a required gate before any lock**. Before ratifying a system (status → `locked`), the proposing session must commission at least four independent agents with no shared session context and distinct lenses — adversarial (fatal flaw; contradictions with locked decisions and the propagation matrix), technical-feasibility (verify external/platform facts against current docs), non-engineer-operator (trust and friction from the operator's seat), and architect (cross-system seams, scope, propagation completeness). Each returns findings tagged blocking/serious/nit; every blocking and serious finding is resolved or explicitly rejected with logged rationale before the lock proceeds. Lenses are a floor, not a ceiling. The gate is posture-enforced (validate.py cannot launch agents); skipping it ranks with a silent edit to a locked doc.

## Why

A lock is hard to reverse, and single-author end-of-pass judgment has blind spots. The inaugural application of this gate (the four-voice audit of the topology + control-plane lock) surfaced two blocking issues the author had missed — the bootstrap front-running provisioning and the unenforced PR template — plus verified factual corrections. The value was demonstrated, not hypothesized. This governs the planning workspace's process, parallel to D-004 and D-015; it is not part of the Engine's own design.

## What we ruled out

Rely on single-author end-of-pass judgment plus `validate.py` (rejected — that is exactly the blind spot the audit removes; the mechanical checker cannot judge feasibility, trust, or cross-system coherence). Run the audit on every editing pass (rejected — over-ceremony; the lock is the irreversible commitment and the right trigger).
