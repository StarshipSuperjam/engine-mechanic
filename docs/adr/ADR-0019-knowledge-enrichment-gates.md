---
id: ADR-0019
title: Graph enrichment passes four durable gates, never a field list
status: accepted
date: 2026-07-17
replaces: [D-203]
---

## Decision

Any enrichment of the derived knowledge graph is admitted by four durable gates, never by membership in a list: declared, not interpreted — sourced from a declared field or a deterministic structural parse, never prose meaning; structure, not belief — entities, relationships, attributes, and lifecycle state only, never rationale, summary, or judgment; forward-only and canon-clean — no persisted reverse edges, no persisted reference targeting decision canon, no edge into memory; and re-derivable and swap-safe — deterministic from committed source and representation-agnostic. New depth rides the on-demand query path, and the cold-start walk's traversal edge-set is pinned in the attention policy, so enrichment is budget-neutral by invariant rather than by hope. Human-legible identity titles are admitted only for types whose title convention is a constrained bare noun phrase verified against live instances — no fallback naming, with a shape guard against drift.

## Rationale

Gates keep a growing graph regenerable and honest where a field list invites copying; a hand-authored index rots silently, and belief-bearing fields would breach the structure/belief wall engine canon fixes between knowledge and memory. Pinning the cold-start edge-set turns budget neutrality into an invariant every future enrichment inherits.

## Anti-choice

A hand-authored feature index was rejected because it rots silently; belief and summary fields were rejected at the wall; provenance edges into canon were rejected as a canon back-door; persisted reverse edges were rejected; admitting fields by copying the illustrative first list rather than passing the gates was rejected.
