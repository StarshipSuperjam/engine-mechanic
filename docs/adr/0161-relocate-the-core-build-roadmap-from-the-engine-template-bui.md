---
status: accepted
engine_record: true
---

# Relocate the `core-build-roadmap` from the engine-template build repo into `engine-planning/wbs/`

*Decided 2026-06-03 in the design workspace.*

## The decision

The Builder-A `core`-decomposition roadmap moves out of the engine-template build repo and into this workspace as `wbs/core-build-roadmap.md`, joining its WBS siblings (module-order, stage-0-harness). A construction map living *inside* the artifact it builds invites the build session to anchor on a repo-local restatement instead of the canonical locked design — the lossy-copy failure mode behind the operation-surface / skill-grammar / prose-policy drops a hardened conformance sweep surfaced (the roadmap had drifted from the plan, e.g. directing the `validators-core` corpus into `core`). Homing it in the canonical workspace puts it beside the source it points to, forces a build session to reach the planning workspace (where the locked docs live) to read it, and keeps the build repo to the built artifact only. The file's source-doc links were re-based to the `wbs/`-relative form; it retains the rewritten **pure-pointer** discipline (a "this is NOT the spec / on conflict the locked doc wins" banner + a mandatory **Go-be-sure** planning-corpus scan as the final step of every slice) and carries no restated substance. It is a transient maintainer scaffold — no `stub|designed|locked` status, freely revisable, deleted when the `core` build completes — referenced from wbs/README.md. **Propagation:** new `wbs/core-build-roadmap.md`; a one-line reference in `wbs/README.md`; this entry. The engine-template removal is a **separate PR** in that repo (deletes the file, re-points the construction `CLAUDE.md` resume order at the relocated home). No locked doc is touched. `python3 validate.py` green.

## Why

Layer discipline plus the one-way dependency rule — the canonical plan owns the build-order; the build repo owns only the artifact. A repo-local scaffold that drifts from the plan is precisely what produced the conformance defects, so removing the drift surface (one canonical home, no competing copy) is the structural fix, and the roadmap is a WBS artifact whose rightful home is `wbs/` alongside module-order.

## What we ruled out

**Leave it in engine-template** (rejected — the operator's explicit call: a build repo must not carry its own build rules; a drifted local copy is the anchoring hazard). **Delete it entirely** (rejected — the 27-slice partition, order, M1-line, and inter-system build seams are genuine non-source WBS content; only the restated substance was stripped). **Keep a copy in both repos** (rejected — a derived copy that competes with canonical truth is the [§2](../principles.md) anti-pattern; the engine-template `CLAUDE.md` instead points at the single canonical home).
