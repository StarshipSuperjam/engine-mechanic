---
status: accepted
engine_record: true
---

# Memory data is local and gitignored; substrate ships empty

*Decided 2026-05-22 in the design workspace.*

## The decision

Experiential memory is stored out-of-repo and gitignored; the template ships the memory machinery with an empty store.

## Why

Memory is high-volume, per-instance, and not worth review-gating; committing it would leak engine-development memory into adopter projects and tax routine work. Ship the substrate, not the data.

## What we ruled out

Repo-authoritative markdown memory cards (the original proposal) — rejected for memory specifically, because review friction and cross-project leakage outweigh diffability for experiential recall. (Contracts and decisions remain repo-authoritative; memory is different.)
