---
id: ADR-0013
title: Ledger integrity and honest recall
status: accepted
date: 2026-07-17
replaces: [D-081, D-273]
---

## Decision

Writes to the local ledger are serialized — a single-writer discipline, because concurrent raw appends can tear a record — and reads are line-resilient: a malformed line is skipped and reported, a torn trailing line is tolerated, and a partial write is rejected structurally, so one fault never costs the recall behind it. Recall surfaces only curated content — typed episodic records and the gists that consolidate them; ambient turn-deltas are capture fuel and sweep input, never recall content, with membership derived from record kind and applied identically on every recall path including the degraded plain-scan floor. Usage-based ranking measures utility for cued, recurring recall only — never importance — and a record decays in ranking but never in existence: the guarantee is recoverability (demote, don't delete; erase only on adjudicated evidence). When the full-text index is unavailable, the fallback preserves recall availability, not latency, and the degradation is disclosed in plain language; open tags stay a secondary structured filter outside the lexical index body so tag drift never poisons ranking. A recall answer whose curated record stands in for raw notes tells the operator the exact original wording is recoverable on request — at the point of consumption, never only in a digest.

## Rationale

In live use, verbatim deltas lexically out-match the paraphrased curated records and drown them out of recall; deriving membership from record kind survives every index rebuild with no carried marker and no in-place edit of the append-only ledger. Claiming that role weighting keeps a rare-but-critical record ranked would be false — the demotion math multiplies by usage — so recoverability is stated as the guarantee instead of overclaiming ranking.

## Anti-choice

Retiring deltas at consolidation was rejected (it adds a sweep-ordering law and a rebuild-surviving marker to preserve mostly noise); a static rank boost for curated records was rejected as a forbidden birth-prior; presenting the scan fallback as preserving latency was rejected as dishonest.
