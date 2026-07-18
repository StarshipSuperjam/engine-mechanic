---
id: ADR-0035
title: The provisioned verdict keys on instantiator presence, three-state
status: accepted
date: 2026-07-17
replaces: [D-277]
---

## Decision
The provisioned verdict keys on instantiator presence, three-state: instantiator present means
unprovisioned — offer setup, presence dominates; instantiator absent with the engine manifest present
means provisioned; instantiator absent with no manifest means a broken or partial checkout, routed to the
strand detector's missing-engine-files arm, never silently read as done. The manifest is demoted to
apply-resume checkpoint, upgrade source-of-truth, and the done-versus-broken conjunct — never the verdict
alone, because any committed marker travels with a template copy and would read a fresh copy as already
set up. A standing first-run onboarding surfacing persists, collapse-managed, every session until setup
actually runs: framed as the operator's own new project, one plain clause on what setup does, always
declinable and self-correcting on ambiguity — surface-and-offer, never a gate. The construction
repository suppresses the offer in its own sessions at the maintainer layer via the construction
sentinel — never a repository-identity check in the deployed engine — and the suppression lands
atomically with the verdict fix, sequenced behind the traveling construction-residue cleanup.

## Rationale
Keying the verdict on the manifest left every template-generated copy dead on arrival — the copied
manifest read as already set up — and only the instantiator's retirement does not travel, so its presence
is the one honest signal. Without a standing offer, onboarding depends on the operator already knowing to
ask for setup, so a deferred "later" would silently strand a half-set-up repository.

## Anti-choice
Rejected: a new positive completion marker, because anything committed travels and reintroduces the
disease; a two-state absence-only verdict, where a manually deleted instantiator would read as provisioned
— the same dead-on-arrival from the opposite cause; and a repository-identity check for the construction
repository, which is online-only, nullable, fork-absent, and a layer-boundary violation.
