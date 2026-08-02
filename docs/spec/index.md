---
spec_depth: full
---

# Product spec

This describes **engine-template** — the product this repository builds — as it is **actually built**. First written in a separate design workspace and carried here as intended design, the corpus has since been reconciled document by document against the build; every capability below is **in progress**, not settled.

Three things to know before relying on it:

- **The whole corpus describes the build, pinned at one commit** ([decision 0320](../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)). Every document — the capability documents in this index's rows, and the architecture, principles, and reference guides alongside — was AI-compared against engine-template@`cdbbc3357fbfbc192005650a8be6ce35b7942bfe` and edited under per-item operator rulings; the rulings that reversed a carried decision are recorded as decisions 0321–0330 in the [decision-record map](../adr/README.md). The corpus drift caveat that stood in this bullet during the reconciliation is retired. Two honest limits remain: **reconciled is not settled** — a document describes the build as observed, not ratified guarantees, until the separate settling effort marks it so — and **the pin ages deliberately**: engine-template releases after the pinned commit are not yet described here, and a re-pin happens only by a new recorded decision, never silently.
- **The implementation is not in this repository.** This repo builds `engine-template`; the code these documents describe lives there.

- **Some references point at material that was left behind.** The design workspace also held build-planning documents and a lock registry, deliberately not carried across. Where a document refers to one of those, the reference is plain text rather than a link, because the file does not exist here.

Supporting material sits alongside: the guiding principles in `../principles.md`, how it fits together in `../architecture.md`, the decisions behind it in `../adr/`, and the glossary, risk register and open questions in `../reference/`.

| Capability | Status | Doc |
| --- | --- | --- |
| audit-library | in progress | [audit-library](modules/audit-library.md) |
| clean-code | not yet described | [clean-code](modules/clean-code.md) |
| core | in progress | [core](modules/core.md) |
| dependency-discipline | in progress | [dependency-discipline](modules/dependency-discipline.md) |
| design-review | in progress | [design-review](modules/design-review.md) |
| engine-knowledge-graph | not yet described | [engine-knowledge-graph](modules/engine-knowledge-graph.md) |
| external-contribution | in progress | [external-contribution](modules/external-contribution.md) |
| github-projects-sync | in progress | [github-projects-sync](modules/github-projects-sync.md) |
| memory-semantic-recall | in progress | [memory-semantic-recall](modules/memory-semantic-recall.md) |
| memory-substrate-sqlite-fts5 | in progress | [memory-substrate-sqlite-fts5](modules/memory-substrate-sqlite-fts5.md) |
| migration-discipline | in progress | [migration-discipline](modules/migration-discipline.md) |
| product-design | in progress | [product-design](modules/product-design.md) |
| product-knowledge-graph | not yet described | [product-knowledge-graph](modules/product-knowledge-graph.md) |
| qa-review | in progress | [qa-review](modules/qa-review.md) |
| routine-mode | in progress | [routine-mode](modules/routine-mode.md) |
| validators-core | in progress | [validators-core](modules/validators-core.md) |
| Attention | in progress | [Attention](systems/cognitive/attention.md) |
| Knowledge | in progress | [Knowledge](systems/cognitive/knowledge.md) |
| Memory | in progress | [Memory](systems/cognitive/memory.md) |
| State | in progress | [State](systems/cognitive/state.md) |
| Module system | in progress | [Module system](systems/grammar/module-system.md) |
| Ontology | in progress | [Ontology](systems/grammar/ontology.md) |
| Audits | in progress | [Audits](systems/guardrails/audits.md) |
| Telemetry | in progress | [Telemetry](systems/guardrails/telemetry.md) |
| Templates | in progress | [Templates](systems/guardrails/templates.md) |
| Validation | in progress | [Validation](systems/guardrails/validation.md) |
| Control plane | in progress | [Control plane](systems/infrastructure/control-plane.md) |
| Hooks | in progress | [Hooks](systems/infrastructure/hooks.md) |
| Provisioning | in progress | [Provisioning](systems/infrastructure/provisioning.md) |
| Repository topology | in progress | [Repository topology](systems/infrastructure/repository-topology.md) |
| Boot / orientation | in progress | [Boot / orientation](systems/lifecycle/boot.md) |
| Build orchestration | in progress | [Build orchestration](systems/lifecycle/build-orchestration.md) |
| Close | in progress | [Close](systems/lifecycle/close.md) |
| External contribution | in progress | [External contribution](systems/lifecycle/external-contribution.md) |
| Operating modes | in progress | [Operating modes](systems/lifecycle/modes.md) |
| Agents | in progress | [Agents](systems/surfaces/agents.md) |
| Check | in progress | [Check](systems/surfaces/check.md) |
| Conduct | in progress | [Conduct](systems/surfaces/conduct.md) |
| Contracts | in progress | [Contracts](systems/surfaces/contracts.md) |
| Docs | in progress | [Docs](systems/surfaces/docs.md) |
| Interfaces | in progress | [Interfaces](systems/surfaces/interfaces.md) |
| Operations | in progress | [Operations](systems/surfaces/operations.md) |
| Policies | in progress | [Policies](systems/surfaces/policies.md) |
| Schemas | in progress | [Schemas](systems/surfaces/schemas.md) |
| Skills | in progress | [Skills](systems/surfaces/skills.md) |
| Tools | in progress | [Tools](systems/surfaces/tools.md) |
