---
status: accepted
engine_record: true
---

# Pin the behavioral-demonstration shape and lifecycle (a falsification that can fail; retire-or-promote; no junk drawer)

*Decided 2026-06-21 in the design workspace.*

## The decision

Pin, in the canonical [Behavioral attestation](../reference/glossary.md) entry (referenced by build-conformance §6/§10 and the stage-0 / module-order / [genesis-build-conformance](../architecture.md#genesis-build-conformance) carriers), the **shape** and **lifecycle** of the behavioral demonstration the design left implicit. **Shape:** a demonstration is a **falsification over the real shipped surface — it must be able to fail** (a recipe that can only succeed is not evidence); a thin harness driving real code (a fake transport, a throwaway directory) is fine, but a **parallel reimplementation of the behavior is the alarm** (the real surface is not exercisable, or the demo is theater). **Lifecycle:** a demonstration is construction-phase evidence tied to its PR's claim — **retired (deleted) once a permanent regression test covers the behavior, or promoted by an explicit logged decision** to a standing operator capability — it does **not** accumulate; the construction set retires with the build-conformance harness at v1, and a construction demo does **not** travel into a generated repo unless promoted ([§13](../principles.md)/[§4](../principles.md)). The live engine-template demos audited healthy (adversarial, real-code-against-fake-IO, no product-bending); this pins the spec so the healthy state is **guaranteed, not incidental**, and bounds the junk-drawer the operator flagged. Live build-owes (confirm each demo can fail; retire-or-promote; extend the first-run retirement set so construction demos do not survive into generated repos) are tracked as engine-template issues.

## Why

The operator observed committed `demo_*.py` accreting with no stated cleanup — a junk-drawer risk — and asked whether demos are ever cleaned up. The design specified the demo's *purpose* (a forced, falsifiable end-to-end check) but never its *shape* or *lifecycle*, so the build had no rule to bound accumulation or to keep a demo a falsification rather than a happy-path showcase. The cold audit confirmed the carriers consistent with the new shape and added back-references so the shape has one canonical home, closing the regeneration source. The see-it-work concern (does retiring demos remove the operator's evidence?) was resolved by stating these are maintainer-layer construction evidence, distinct from the deployed operator's own [§17](../principles.md) per-change evidence.

## What we ruled out

**Refactor the live demos toward ephemeral recipes now** (rejected — they audited healthy; the operator chose tighten-spec-light-live, and a refactor risks regressing working demos). **Home the durable "demos don't travel" rule in build-conformance** (rejected — build-conformance retires at v1; the travel rule must survive it, so it lives in the [Behavioral attestation](../reference/glossary.md) glossary entry). **Touch locked [repository-topology](../spec/systems/infrastructure/repository-topology.md) for the travel rule** (rejected — a needless third re-lock; the glossary home + the first-run retirement build-owe suffice, and the post-v1 standing question is already [Q31](../reference/open-questions.md)-adjacent). **Leave demos unbounded** (rejected — the junk drawer the operator flagged).
