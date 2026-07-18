---
id: ADR-0048
title: The agent grammar — role binds to trigger, demand not model, report not disposition
status: accepted
date: 2026-07-17
replaces: [D-057, D-100]
---

## Decision

An agent is a persona the engine runs for a trigger, and its routing grammar is law. The role field is a closed set bound to the trigger it runs for — the build-gate review and worker roles plus the audit role fired by the scheduled self-review — so an unknown role is impossible by construction, and the derived roster is partitioned by trigger, so a present audit persona can never leak into a build gate. A lens exists only on review roles and is recognized by consumption: an installed review lens nothing consumes, or a lens declared on a non-review role, is a coherence finding, and a consumed lens with no agent is disclosed as "no such review ran," never reported as a pass. The model tier is a closed demand vocabulary — careful judgment versus mechanical work — never a model name; which model and effort realize a tier is persona-owned configuration, so a model release is a config change, never a grammar change. The output contract fixes only the report shape on the canonical finding base: the agent reports and the trigger's owner dispositions by its own vocabulary — severity is a per-consumer axis — and each consumer's contract instance is versioned and fixture-tested so a contract change is explicit and regression-guarded.

## Rationale

Binding role to trigger removes a separate routing field — one fewer way to misconfigure — and keeps the grammar honest about agents that are not gate agents. Decoupling demand from model identity stops every model release from re-litigating governed design; the falsified cheaper-worker economics is severed, leaving delegation resting on what is actually true — cohesion under context pressure. The report/disposition seam keeps judgment where accountability lives: the persona that found an issue never decides its fate. The surface claims no coverage completeness — the affirmative what-was-reviewed roll-up belongs to the gate that consumes the reviews, and everything the operator sees is plain language, never internal vocabulary.

## Anti-choice

Rejected: an open role set (weakens role-implies-trigger); a central recognized-lens registry (a list installs must mutate); agent-recommended dispositions (blurs the report/disposition seam); a coherence carve-out whitelisting the auditor (leaves the grammar falsely claiming all agents are gate agents); and baking the current best model in as a floor (re-pins the model treadmill the demand vocabulary exists to escape).
