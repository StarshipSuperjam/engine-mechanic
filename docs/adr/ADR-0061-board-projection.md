---
id: ADR-0061
title: The work board is a one-way projection that renders only computed verdicts
status: accepted
date: 2026-07-17
replaces: [D-099, D-318]
---

## Decision

The optional board-sync module projects the repo-authoritative work signal onto the platform's project board strictly one-way: the board is a replaceable derivative over committed truth, never authoritative, deletable and rebuildable. Native platform automation carries the work record server-side; the engine layer projects only the engine-specific signals the platform cannot see, writes only its own custom fields on its own items — never status, column, or card position — so a human's board gesture is never overwritten and divergence is surfaced, never silently reverted. The trigger is the module's own non-blocking, fail-open hook that can never block eligibility (core cannot depend on an optional module), and every failure degrades to git-native truth with a board-face staleness marker. The board is a non-traveling external resource, so its setup is module-owned with informed consent for the access it needs and no standing credential in automation; on removal, the dangling board and granted scope are honest, inert residuals. Every projected field label names only a verdict the engine actually computes — the engine's ordering field reads as ranked work, not a "what's next" the engine never computed for those items — because one operator phrase must have one referent across surfaces.

## Rationale

A non-engineer may read the board instead of the Issues, so a label implying an uncomputed judgment manufactures a considered-and-ranked false belief. One-way flow with strict field ownership is what makes "never authoritative" true in practice rather than aspiration.

## Anti-choice

Rejected: a CI-resident sync workflow (no coherence home for an optional module's workflow, and it forces a stored credential); a two-way or authoritative board; re-sourcing the board's ordering from another optional module (violates its own dependency law) rather than relabelling honestly.
