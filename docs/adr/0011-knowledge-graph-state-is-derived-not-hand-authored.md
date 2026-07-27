---
status: accepted
engine_record: true
---

# Knowledge-graph state is derived, not hand-authored

*Decided 2026-05-22 in the design workspace.*

## The decision

Generate knowledge entities from source surfaces, fingerprint-gated so the graph rebuilds when sources change.

## Why

Derived structural state is self-correcting; hand-authored state rots silently as the source evolves.

## What we ruled out

Hand-curate the knowledge graph — rejected because it drifts out of sync and creates maintenance debt.
