---
id: ADR-0017
title: The engine's memory supersedes the harness notebook
status: accepted
date: 2026-07-17
replaces: [D-251]
---

## Decision

The engine's own substrate is authoritative for project recall: the engine never writes project content into the platform's built-in auto-memory and never cites it as fact — the built-in notebook is the contributor's personal cross-project cache, never the project record. No write-gate carve-out is made for memory paths: the substrate's own upkeep passes the existing gates by design, and a raw in-place edit of the ledger would bypass the write-serialization law. The one genuinely unserved need — cross-project contributor memory — is disclosed honestly on contact ("I can remember this for this project; across all your projects I can't yet") and tracked as a standing risk, never silently filed as project-local; an operator's "remember this" is durably captured as a typed preference with a legible confirmation, never a hand-written ledger line.

## Rationale

Two records claiming authority over the same project drift and contradict, and the harness notebook has an engine replacement where it is superseded. A path-based carve-out is both infeasible — the platform marks nothing on an auto-memory write, and the notebook directory is operator-relocatable — and unsafe, since a raw ledger edit can tear a line. The disclosure contract prevents the false belief that a note traveled to every project.

## Anti-choice

A write-gate carve-out for memory-directory writes was rejected on three independent grounds, any one sufficient: it writes the notebook the authority policy forbids, path recognition is fragile, and it bypasses write serialization. Silently filing a cross-project request as project-local was rejected as a quiet lie.
