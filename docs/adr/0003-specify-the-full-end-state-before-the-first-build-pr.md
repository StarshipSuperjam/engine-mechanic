---
status: accepted
engine_record: true
---

# Specify the full end-state before the first build PR

*Decided 2026-05-22 in the design workspace.*

## The decision

Finalize the complete end-state (every system, surface, module) and the WBS before any code lands. Capability layering happens in the WBS build order, not by cutting features from the end-state.

## Why

AI build cannot do iterative design; a feature without pre-existing grammar becomes a system refactor. "Defer" is a build-order word, not a scope cut.

## What we ruled out

Build a minimal v1 and grow it iteratively — rejected because each later feature would force a refactor of foundations laid without it in mind.
