---
spec_depth: full
---

# Product spec

This describes **engine-template** — the product this repository builds — as it is **actually built**. First written in a separate design workspace, carried here as intended design, and reconciled document by document against the build, the corpus is now **settled**: on 2026-08-02 the operator accepted every reconciled capability document as the ratified baseline ([decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md)) — the ground future builds are measured against and future design work diffs from. Three stubs remain **not yet described**.

Four things to know before relying on it:

- **The corpus describes the build, pinned at one commit** ([decision 0320](../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)). Every reconciled document — the settled capability documents in this index's rows, and the **architecture** overview, the **principles**, and the seven **reference** guides alongside (constraints, glossary, goals-and-quality, module-catalog, open-questions, prototype-deviations, risks) — was AI-compared against engine-template@`cdbbc3357fbfbc192005650a8be6ce35b7942bfe` and edited under per-item operator rulings (one, **memory-semantic-recall**, was instead authored from the build, having shipped unspecced); the rulings that changed the carried record — reversals, ratifications, and admissions alike — are recorded as decisions 0321–0330 in the [decision-record map](../adr/README.md). The three "not yet described" stubs (clean-code, engine-knowledge-graph, product-knowledge-graph) describe capabilities not yet built and sit outside the reconciliation and the settling alike, as does the historical methodology archive under `docs/reference/sam-provenance/`.
- **Settled is not machine-enforced, and the pin ages deliberately.** A settled document is the ratified obligation — changing one now requires the operator's recorded re-acceptance at the merge — but most acceptance criteria rest on the operator's own observation rather than a merge-gated check, and [decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md) records exactly what settling does and does not buy. engine-template releases after the pinned commit are not yet described here — a re-pin happens only by a new recorded decision, never silently.
- **The implementation is not in this repository.** This repo builds `engine-template`; the code these documents describe lives there.

- **Some references point at material that was left behind.** The design workspace also held build-planning documents and a lock registry, deliberately not carried across. Where a document refers to one of those, the reference is plain text rather than a link, because the file does not exist here.

Supporting material sits alongside: the guiding principles in `../principles.md`, how it fits together in `../architecture.md`, the decisions behind it in `../adr/`, and the glossary, risk register and open questions in `../reference/`. One corner of `../reference/` is a different kind of material: `../reference/platform-baseline/` holds the adopted platform capability baseline — decision-input observations about the AI platforms the engine runs on, not a description of the product itself.

| Capability | Status | Doc |
| --- | --- | --- |
| audit-library | settled | [audit-library](modules/audit-library.md) |
| clean-code | not yet described | [clean-code](modules/clean-code.md) |
| core | settled | [core](modules/core.md) |
| dependency-discipline | settled | [dependency-discipline](modules/dependency-discipline.md) |
| design-review | settled | [design-review](modules/design-review.md) |
| engine-knowledge-graph | not yet described | [engine-knowledge-graph](modules/engine-knowledge-graph.md) |
| external-contribution | settled | [external-contribution](modules/external-contribution.md) |
| github-projects-sync | settled | [github-projects-sync](modules/github-projects-sync.md) |
| memory-semantic-recall | settled | [memory-semantic-recall](modules/memory-semantic-recall.md) |
| memory-substrate-sqlite-fts5 | settled | [memory-substrate-sqlite-fts5](modules/memory-substrate-sqlite-fts5.md) |
| migration-discipline | settled | [migration-discipline](modules/migration-discipline.md) |
| product-design | settled | [product-design](modules/product-design.md) |
| product-knowledge-graph | not yet described | [product-knowledge-graph](modules/product-knowledge-graph.md) |
| qa-review | settled | [qa-review](modules/qa-review.md) |
| routine-mode | settled | [routine-mode](modules/routine-mode.md) |
| validators-core | settled | [validators-core](modules/validators-core.md) |
| Attention | settled | [Attention](systems/cognitive/attention.md) |
| Knowledge | settled | [Knowledge](systems/cognitive/knowledge.md) |
| Memory | settled | [Memory](systems/cognitive/memory.md) |
| State | settled | [State](systems/cognitive/state.md) |
| Module system | settled | [Module system](systems/grammar/module-system.md) |
| Ontology | settled | [Ontology](systems/grammar/ontology.md) |
| Audits | settled | [Audits](systems/guardrails/audits.md) |
| Telemetry | settled | [Telemetry](systems/guardrails/telemetry.md) |
| Templates | settled | [Templates](systems/guardrails/templates.md) |
| Validation | settled | [Validation](systems/guardrails/validation.md) |
| Control plane | settled | [Control plane](systems/infrastructure/control-plane.md) |
| Hooks | settled | [Hooks](systems/infrastructure/hooks.md) |
| Provisioning | settled | [Provisioning](systems/infrastructure/provisioning.md) |
| Repository topology | settled | [Repository topology](systems/infrastructure/repository-topology.md) |
| Boot / orientation | settled | [Boot / orientation](systems/lifecycle/boot.md) |
| Build orchestration | settled | [Build orchestration](systems/lifecycle/build-orchestration.md) |
| Close | settled | [Close](systems/lifecycle/close.md) |
| External contribution | settled | [External contribution](systems/lifecycle/external-contribution.md) |
| Operating modes | settled | [Operating modes](systems/lifecycle/modes.md) |
| Agents | settled | [Agents](systems/surfaces/agents.md) |
| Check | settled | [Check](systems/surfaces/check.md) |
| Conduct | settled | [Conduct](systems/surfaces/conduct.md) |
| Contracts | settled | [Contracts](systems/surfaces/contracts.md) |
| Docs | settled | [Docs](systems/surfaces/docs.md) |
| Interfaces | settled | [Interfaces](systems/surfaces/interfaces.md) |
| Operations | settled | [Operations](systems/surfaces/operations.md) |
| Policies | settled | [Policies](systems/surfaces/policies.md) |
| Schemas | settled | [Schemas](systems/surfaces/schemas.md) |
| Skills | settled | [Skills](systems/surfaces/skills.md) |
| Tools | settled | [Tools](systems/surfaces/tools.md) |
