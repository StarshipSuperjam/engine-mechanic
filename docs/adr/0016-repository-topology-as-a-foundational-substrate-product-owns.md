---
status: accepted
engine_record: true
---

# Repository topology as a foundational substrate; product-owns-root wall; laws not leaves

*Decided 2026-05-22 in the design workspace.*

## The decision

Add `systems/infrastructure/repository-topology` as a foundational (non-modular) system and lock it. It fixes the top-level partition — the engine confined to namespaced corners (`.engine/`, `.claude/`, engine-owned `.github/` files, root `CLAUDE.md`), the product owning the repo root — and states the **placement laws** (one `.engine/<surface>/` per ontology surface; Claude-native surfaces where the tool dictates; canonical data never a committed path) rather than enumerating the full directory tree. The engine/product wall is enforced by CODEOWNERS path-ownership, not by quarantining the product. This extends the foundation set beyond the original nine of [D-006](0006-nine-non-modular-foundations.md) (it is now ten) and supersedes the implicit `product/` directory shown in earlier architecture diagrams.

## Why

Topology is presupposed by every other system (CODEOWNERS paths, workflow homes, surface locations, substrate paths), so it cannot be bolted on later. Confining the engine to dot/namespaced corners is the *most* product-respecting choice — those names do not collide with product ecosystems, whereas a `product/` box fights root-expecting toolchains (Go, Rust, Next.js) and a flat-at-root engine (`tools/`, `schemas/`) collides outright. Locking laws rather than leaves keeps the doc durable: a downstream system attaches its subtree additively under the reserved namespace without reopening this doc or tripping its fingerprint.

## What we ruled out

Quarantine the product under `product/` (rejected — imposes a non-standard layout on every adopter and breaks ecosystem tooling). Enumerate the full leaf tree now (rejected — would freeze choices owned by D-007, Q2, Q5, deviation D7, and Q7, forcing a re-litigation alarm when each lands). Fold topology into control-plane or architecture §3 prose (rejected — a category error; topology is the substrate the control plane enforces, and prose in the index is not a lockable system).
