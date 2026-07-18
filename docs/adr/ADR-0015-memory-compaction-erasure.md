---
id: ADR-0015
title: Compaction bounds growth; only a merged consent erases
status: accepted
date: 2026-07-17
replaces: [D-209, D-285]
---

## Decision

Append-only governs live writes, not the ledger's whole life: growth is bounded by compaction, a self-directed whole-ledger rebuild-and-swap using memory's own restore primitive, crash-safe (temp written beside the ledger, durably flushed, atomically swapped, index fully rebuilt under a monotonic generation stamp — never patched incrementally) and held under the single-writer lock across the entire fold-and-swap. Layer 1 is reversible and memory-autonomous: it folds transition records into current state (ranking state carried as a recurrence on the folded snapshot, never a window scan), prunes the hot index, and applies logical retirement — an index-exclusion state, never a separate store — and it never autonomously erases recall content. Layer 2, physical erasure, is enacted only by the operator's merge of a single-purpose erasure change the audit loop proposed and adjudicated per record; a merely closed tracking item never erases, since closure has many meanings. "Single-purpose" binds purpose, never count: a batch may name several records, the operator is shown each record's plain-language cost — never a bare total — and approves or declines the batch whole; an ill-formed batch is rejected whole. Targets are named by stable, content-free record ids minted at capture; enactment is idempotent, keyed to the merge identity; and the ledger generation travels in the snapshot manifest so a restore that would resurrect an enacted erasure surfaces instead of passing silently.

## Rationale

Rebuild-and-swap realizes hard delete with no second store and no widened contract, and the failure direction is "nothing lost" — a stalled audit only defers disk reclamation. The merge gate is the one channel that reliably reaches a non-engineer, so the only irreversible act in memory rides it; everything short of that stays recoverable.

## Anti-choice

An autonomous purge gated on a boot-surfaced undo horizon was rejected — boot is not a reliable operator channel for consent. A separate cold-archive store, offset- or content-quoting target references, and a one-record-per-request rule were each rejected; treating append-only itself as the defect was rejected in favor of bounding it.
