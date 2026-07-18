---
id: ADR-0003
title: Core/module demarcation operationalized — slots and fillings
status: accepted
date: 2026-07-17
replaces: [D-069]
---

## Decision
The core/module boundary is settled by an operational test, not new legislation: remove every module — what survives is core, what disappears is a module — governed by the existing containment principle and the packaging rule that core is always-on and never an install choice. Two maintainer terms make the fillable seams precise: a slot is the fillable subset of core that accepts a filling and runs as a disclosed no-op when unfilled — only the orchestration review gates and the search/retrieval interface qualify; a filling is a module that fills a slot, discovered by presence, and a strict subset of modules. Operator selection never redefines core: a filling every operator happens to install remains a filling. Slot and filling are maintainer vocabulary; the operator is told what always-on core does and why it cannot be disabled, never in these terms.

## Rationale
The demarcation needed an operational test and precise seam vocabulary, not a peer principle: the proposed one was a false genus whose defining no-op-when-unfilled clause fits only the two fillable seams, while restating existing law and inviting a second, partially contradictory core/module rule.

## Anti-choice
Rejected minting a standalone slots principle, and letting install popularity promote a filling into core.
