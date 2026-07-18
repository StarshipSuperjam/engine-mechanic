---
id: ADR-0016
title: Automatic off-repo backup — shared vault default, minted namespaces, retained snapshots
status: accepted
date: 2026-07-17
replaces: [D-061, D-237, D-264]
---

## Decision

The engine backs memory up itself: an automatic, per-project-namespaced export of the ledger to an operator-consented, off-repo private destination — by default a single shared cross-project vault, with a per-project destination offered at every new project's setup under a plain-language disclosure of the trade; the backup is a copy, the canonical store stays the local ignored ledger, and restore is replace-the-ledger-and-rebuild-the-index. Namespace identity is a minted, content-free, rename-stable id written into the committed destination pointer before first export — never a name or path derived at runtime — so no project can write into, or restore from, another's namespace. Privacy is honest posture: the destination is created private and verified, a periodic re-check detects — never prevents — a later flip to public, and the per-project escape, not the re-check, is the structural bound on shared-vault exposure. The pre-migration snapshot is a distinct, retained, manifest-named copy the routine rolling backup never overwrites; it participates in the generation-resurrection guard, is retained at least as long as a mismatch could cite it, and reaches the operator as exactly one plain-language restore action — never a raw reference, never a snapshot-versus-latest fork. One mechanism serves two consumers: memory owns the export/restore contract and the snapshot manifest; provisioning consumes it and may not widen it.

## Rationale

A non-engineer will never hand-copy an invisible ignored file, so backup must be automatic or it does not exist. For a sole operator the same credential reads every per-project backup anyway, so per-project never bought read-isolation — the shared vault knowingly trades the smaller structural blast unit for one-place ergonomics, disclosed at the choice. The prior single rolling slot silently clobbered the pre-update copy at exactly the moment the undo alarm fired.

## Anti-choice

Committing the ledger anywhere in-repo was rejected (it travels with every clone and leaks across projects); cloud-synced folders were rejected as brittle with invisible failure; a cross-instance vault registry or auto-discovery was rejected as a new mechanism memory would have to own; accepting the rolling-slot race was rejected as a safety guarantee on an invisible timer.
