---
id: ADR-0057
title: The required-package rule; memory is its own package, knowledge rides core
status: accepted
date: 2026-07-17
replaces: [D-086, D-091]
---

## Decision

Every cognitive floor is required and always ships, so optionality cannot decide packaging. A floor becomes its own required package only when it owns non-regenerable per-instance data needing a legible migration unit, or a bound seam another package binds to; otherwise its files ride core. Memory qualifies on both counts — the irreplaceable, uncommitted experience ledger, and the search seam an optional semantic layer binds to — and is its own required package with its own migration unit; knowledge is committed entities plus a regenerable derived index and rides core; the semantic-recall layer stays the lone optional, experimental package behind the swappable search interface. The memory package owns the substrate but not the contract: the search interface declaration stays in core's grammar while the module owns the lexical-fallback implementation, the recall substrate, and the backup-and-restore mechanism and contract — provisioning consumes that contract but may not widen it. Memory's capture hooks are module-wired under the module's own keys, because core cannot depend on memory; and both recall degradations are disclosed, never silent — a down recall service lets boot proceed with notice, an absent index falls back to plain scanning.

## Rationale

The irreplaceable ledger is the decisive test: burying its schema migrations inside a monolithic core migration would make the one store that cannot be regenerated the hardest to migrate legibly. The protocol/implementation split keeps the swap seam clean — a semantic layer replaces the implementation without touching the contract.

## Anti-choice

Rejected: a separate knowledge package (ceremony without payoff — no non-regenerable store, no bound consumer); folding memory into core; ceding the interface declaration to the module (over-reads "owns the seam" and dirties the swap boundary).
