---
id: ADR-0021
title: The offline cache rides the audit digest as schema-gated freight
status: accepted
date: 2026-07-17
replaces: [D-205]
---

## Decision

The committed offline state cache — the standing-situation pointer and the debt count, both together, never split across mechanisms — is refreshed by one shared derive pass and committed by the audit digest's periodic, operator-reviewed self-attestation as freight: a separate file gated by its own schema check, never folded into the digest's own drift gate. It is schema-gated, not drift-gated, because it derives from continuously changing external state that has no committed referent to fingerprint against — a drift gate there would be incoherent, not merely omitted. A missed refresh only ages the stale-labelled offline copy; it never corrupts the live online read, which each session derives fresh, and the freight is presented as auto-derived — values the operator reviews but does not vouch for.

## Rationale

The digest pass is already a periodic, operator-reviewed commit vehicle, so the cache rides it without standing up the engine's first standalone scheduled commit actor; the read-only reporting persona stays read-only. Keeping the two sibling fields on one mechanism means they can never disagree about freshness.

## Anti-choice

A persona-owned refresh was rejected as relay dressed as ownership; a new scheduled commit actor was rejected; refreshing at session close, or boot persisting what it derives, was rejected; the telemetry pass committing was rejected because its one write is issue-tracking only.
