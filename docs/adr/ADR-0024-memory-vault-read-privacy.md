---
id: ADR-0024
title: Saved-memory review reaches the vault least-privileged; the public digest withholds specifics
status: accepted
date: 2026-07-17
replaces: [D-241, D-243]
---

## Decision

The scheduled audit's stale-saved-memory review reaches the operator's off-repo memory vault only through a least-privilege, read-only credential scoped to that vault, provisioned behind a heavy-consent gate that discloses the shared-vault blast radius and offers the per-project-vault escape at decision time; the read is a pure consumer of memory's existing backup export and widens no memory mechanism, and turn-on ends with an engine-run test read so success is behaviorally confirmed. What the committed digest may say is gated on repo visibility: on a private repo it may name this project's stale saved beliefs (and no other namespace's); on a public repo it structurally omits belief specifics, reports staleness in aggregate, states the withholding plainly, and always points to levers the operator already controls — the exposure-free in-session review of their own local ledger, and the private-repo or per-project-vault escape. No standing opt-in flag to relax the withholding exists; a staleness notice arising from this read names which credential lapsed and its matching recovery.

## Rationale

Without the wired read, the audit's headline memory check stays dark on every scheduled run — a disclosed gap is not a working check. A committed digest is forever, and a non-engineer cannot give weighable one-time consent to irreversible public exposure of an unbounded future stream; a committed relaxation flag would also be a leak beacon flippable by any write-capable actor while the structural gate is not. The named residual is stated, not hidden: a past digest cannot be unpublished after a later public flip.

## Anti-choice

Disclosure-only (never wiring the read) was rejected because the check would stay permanently dark; a broad-scope credential was rejected as needless blast radius; the requested per-public-project opt-in flag was declined — the faithful shape of disclose-and-offer is offering levers the operator already holds, not building an engine-owned lever that weakens the bound.
