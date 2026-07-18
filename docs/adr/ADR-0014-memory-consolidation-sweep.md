---
id: ADR-0014
title: The consolidation sweep is incremental, terminating, and mechanical
status: accepted
date: 2026-07-17
replaces: [D-279, D-307, D-308]
---

## Decision

The boot-time consolidation sweep fires over any non-live session carrying genuine un-consolidated conversation beyond its last watermark; the consolidation marker is a per-session high-water mark meaning "swept through (examined)", the effective watermark is the maximum across a session's markers, and every pass advances it past everything it examined — whether or not a record resulted — so the sweep terminates and no genuine later half is left un-swept. A consolidating store recomputes its residual beyond the current effective watermark under the held ledger lock and appends record and marker in the same held section, so a concurrent sweep and a revived session cannot double-consolidate a prefix. Harness-injected pseudo-turns — whole, standalone machinery blocks the platform injects as if the operator wrote them, recognized by a closed sentinel set the engine owns — are neither consolidation fuel nor a pending trigger; the boundary is mechanical, never a salience judgment, and may never extend to skipping "noisy" genuine turns. Every withheld or examined delta stays physically resident and recoverable; recall-exclusion never narrows the sweep, and the sweep is never a step toward erasure.

## Rationale

A binary done-flag permanently excluded the later half of a session tidied mid-run and then left idle; advancement by examination rather than yield terminates on unsummarizable tails instead of looping. Consolidating injected machinery as if the operator authored it pollutes the episodic record, and a sentinel boundary — unlike a salience one — can never quietly eat genuine conversation. The guarantee stays honest: the sweep narrows and defers the reflection gap; content was always safe because raw deltas stay resident.

## Anti-choice

Wall-clock time as the watermark boundary was rejected as coarse and skew-prone; advancement only on record yield was rejected because it loops forever on unsummarizable tails; a whole-span coverage check at store time was rejected because it leaves a prefix double-consolidatable in a race; any salience-based filter over genuine turns was rejected outright.
