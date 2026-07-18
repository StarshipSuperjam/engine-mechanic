---
id: ADR-0018
title: The knowledge graph is queried read-only through a pinned operation set
status: accepted
date: 2026-07-17
replaces: [D-116, D-224]
---

## Decision

The knowledge-retrieval interface pins its complete operation set as protocol: fetch an entity with its declared edges, find entities by selector, traverse adjacency under filter, direction, and depth, and relate two entities by path — and no write or mutation operation, because regeneration is the store's own commit-boundary act, never a query. Both the committed floor representation and any richer swapped-in representation satisfy the same contract, keeping the representation seam swappable. Traversal serves both directions at query time over the single stored forward edge — reverse is a query direction, never a persisted edge — and reverse candidates compete inside the same fixed orientation budget under the existing trim order, so the richer walk is budget-neutral by construction; deeper exploration stays on the on-demand query path. The read-time link to memory stays consumer-composed, as engine canon fixes; the missing lateral "these parts collaborate" signal is either belief (walled out of the graph) or grammar that does not yet exist, and remains an open question rather than a forced edge.

## Rationale

An under-specified minimal operation set was exactly the gap a build-readiness pass surfaced; pinning the full contract lets consumers build once while the representation stays swappable underneath. Query-time reverse direction gives orientation the "surfaces and dependents" view a governing policy or module needs without violating the forward-only store or growing the budget.

## Anti-choice

A minimal lookup-plus-neighbors floor deferring the rest was rejected as re-creating the under-specification. Persisting reverse edges, enlarging the orientation budget to fit reverse candidates, leaving the cold-start walk forward-only, and inventing collaboration edges before any grammar declares them were each rejected.
