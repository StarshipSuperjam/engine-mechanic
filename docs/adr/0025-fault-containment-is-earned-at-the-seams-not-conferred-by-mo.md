---
status: accepted
engine_record: true
---

# Fault-containment is earned at the seams, not conferred by modularity

*Decided 2026-05-23 in the design workspace.*

## The decision

Establish a cross-cutting principle: the engine is a **small trusted core (the foundations) plus optional extensions (the modules)**, but **fault-containment is a property of the wiring discipline at the shared seams** — keyed, idempotent, reversible wiring; coherence validation; and not shipping what is not selected — **not a property conferred by the architecture's shape**. Three consequences are fixed: (1) in all design prose, **"modular" means "composed of modules," never "fault-isolated"**; the isolation claim must be attributed to the seam discipline, never smuggled in by the adjective. (2) **The shared core stays minimal because it is contagious by nature** — a defect in a foundation (`validation`, `hooks`, …) reaches every generated project, so every candidate foundation must justify why it cannot be an extension. (3) The shape may be labelled **microkernel-*inspired*** as an analogy, but the analogy's limit is stated: a true microkernel isolates via address spaces, whereas these extensions share mutable files, so the seam discipline — not the shape — is what contains a blast. Lands as a new [principles.md](../principles.md) principle plus a one-sentence note in [engine-architecture.md](../architecture.md) §4; planning/maintainer vocabulary only — "microkernel" must not leak into operator-facing Engine surfaces.

## Why

The operator surfaced that "modular" had been silently carrying an isolation guarantee it does not provide. The precise danger is not the noun "module" (which is exact) but the inference *modular ⟹ isolated*. Renaming the shape "microkernel" without this attribution would reproduce the identical false inference in new vocabulary. Naming the attribution — isolation is earned at the seams — is the durable fix, and it directly motivates keeping the foundation set small (R6) and investing rigor in the wiring library (R5), which is where the real firewall lives.

## What we ruled out

Retire/rename "module" (rejected — it is a precise noun threaded through the design; the leak was the adjective, not the noun). Call the shape "microkernel" and stop there (rejected — reintroduces the *shape ⟹ isolation* error; our extensions share files, not address spaces). Leave the attribution implicit (rejected — that is exactly the unstated assumption that produced the category error; a future session would re-derive "modular = isolated").
