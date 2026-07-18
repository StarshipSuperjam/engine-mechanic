---
id: ADR-0056
title: Core is the trusted root; the self-validation corpus and routine entry ship beside it
status: accepted
date: 2026-07-17
replaces: [D-089, D-090, D-092]
---

## Decision

Core is the trusted root: the irreducible machinery that survives the remove-every-module test — the grammar, the regenerable cognitive floors, the guardrail foundations including the validation engine and its closed check kinds, the stand-up and enforcement infrastructure, the lifecycle spine, the core policies, and the base operator verbs. The validation mechanism and its content are split: the engine rides core, while the engine's whole self-validation rule corpus ships as one consolidated required package of check data only — no kinds, no detection logic, wiring nothing, its rules active by presence. The root grounding file, the engine manifest, and the engine-owned control-plane files are foundation-infrastructure artifacts outside any module's provides, shipped as the engine baseline. The routine-stance package ships only the operator's entry into the unattended stance — a thin command delegating to one owned entry procedure — and wires nothing, because the unattended permission posture is operator-side platform configuration outside the committed seams and must never be dressed as an engine wire.

## Rationale

A defect in core reaches every generated project, so core keeps only what cannot be an extension; everything that can be carved into a sibling package is. The mechanism/content split keeps the self-validation floor one coherent, always-present package rather than fragments scattered across owners, while the engine that runs it owns no per-instance store and no bound seam and so belongs in core. Keeping the entry procedure in one authoritative home is the drift firewall against burying scope-lock and misfire logic in a command or prose.

## Anti-choice

Rejected: putting the validation engine in the corpus package (inverts the dependency graph and strands provisioning's direct coherence call); scattering self-validation rules to their owning modules (fragments the single floor and blurs the mechanism/content line); listing the baseline infrastructure artifacts in a provides (contradicts the coherence rule that defines them as the non-provides set); claiming the unattended posture rides core (checkably false).
