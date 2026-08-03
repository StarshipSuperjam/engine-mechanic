---
spec_depth: full
---

# Product spec

This describes **engine-template** — the product this repository builds — as it is **actually built**: every row marked **settled** carries that promise, and the rows marked otherwise are the disclosed exceptions. First written in a separate design workspace, carried here as intended design, and reconciled document by document against the build, the corpus is now **settled**: on 2026-08-02 the operator accepted every reconciled capability document as the ratified baseline ([decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md)) — the ground future builds are measured against and future design work diffs from. One stub remains **not yet described** (engine-knowledge-graph), and the **in progress** rows are forward-designed documents describing intended work not yet built, authored after the settling through the plan-acceptance route ([decision 0327](../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)): [platform-currency](modules/platform-currency.md), and the twenty-six documents of the **delivery-plane program** ([decision 0334](../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)) — each entering as a draft, settling per wave by the operator's recorded acceptance before that wave's build begins. The former `clean-code` stub is **retired** by that same decision: the engineering-quality family absorbs its territory, with the decision record and git history as the trace.

**Where to start with the delivery plane:** the program's ground is
[decision 0334](../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md) (the module map, the
boundary cuts, and the program rules), and the [build order](build-plan.md) shows which of the "in
progress" rows below belong to which delivery wave — the unit you settle by. Within a wave, read the
kernel or contract document first (wave 1: [delivery-core](modules/delivery-core.md)) — the others speak
its vocabulary. The only other "in progress" row, [platform-currency](modules/platform-currency.md), is
its own earlier program.

Four things to know before relying on it:

- **The corpus describes the build, pinned at one commit** ([decision 0320](../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)). Every reconciled document — the settled capability documents in this index's rows, and the **architecture** overview, the **principles**, and the seven **reference** guides alongside (constraints, glossary, goals-and-quality, module-catalog, open-questions, prototype-deviations, risks) — was AI-compared against engine-template@`cdbbc3357fbfbc192005650a8be6ce35b7942bfe` and edited under per-item operator rulings (one, **memory-semantic-recall**, was instead authored from the build, having shipped unspecced); the rulings that changed the carried record — reversals, ratifications, and admissions alike — are recorded as decisions 0321–0330 in the [decision-record map](../adr/README.md). The remaining "not yet described" stub (engine-knowledge-graph) and every in-progress document — platform-currency and the delivery-plane program's twenty-six — describe capabilities not yet built and sit outside the reconciliation and the settling alike, as does the historical methodology archive under `docs/reference/sam-provenance/`.
- **Settled is not machine-enforced, and the pin ages deliberately.** A settled document is the ratified obligation — changing one now requires the operator's recorded re-acceptance at the merge — but most acceptance criteria rest on the operator's own observation rather than a merge-gated check, and [decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md) records exactly what settling does and does not buy. engine-template releases after the pinned commit are not yet described here — a re-pin happens only by a new recorded decision, never silently.
- **The implementation is not in this repository.** This repo builds `engine-template`; the code these documents describe lives there.

- **Some references point at material that was left behind.** The design workspace also held build-planning documents and a lock registry, deliberately not carried across. Where a document refers to one of those, the reference is plain text rather than a link, because the file does not exist here.

Supporting material sits alongside: the guiding principles in `../principles.md`, how it fits together in `../architecture.md`, the decisions behind it in `../adr/`, the glossary, risk register and open questions in `../reference/`, and the [build order](build-plan.md) recording where every settled capability and the forward work stand in the build sequence. One corner of `../reference/` is a different kind of material: `../reference/platform-baseline/` holds the adopted platform capability baseline — decision-input observations about the AI platforms the engine runs on, not a description of the product itself.

| Capability | Status | Doc |
| --- | --- | --- |
| audit-library | settled | [audit-library](modules/audit-library.md) |
| authority-broker-contract | in progress | [authority-broker-contract](modules/authority-broker-contract.md) |
| bounded-repair | in progress | [bounded-repair](modules/bounded-repair.md) |
| browser-evidence | in progress | [browser-evidence](modules/browser-evidence.md) |
| code-intelligence-core | in progress | [code-intelligence-core](modules/code-intelligence-core.md) |
| core | settled | [core](modules/core.md) |
| credential-broker | in progress | [credential-broker](modules/credential-broker.md) |
| debugger-diagnosis | in progress | [debugger-diagnosis](modules/debugger-diagnosis.md) |
| delivery-core | in progress | [delivery-core](modules/delivery-core.md) |
| delivery-evidence | in progress | [delivery-evidence](modules/delivery-evidence.md) |
| dependency-discipline | settled | [dependency-discipline](modules/dependency-discipline.md) |
| deployment-adapter | in progress | [deployment-adapter](modules/deployment-adapter.md) |
| deployment-core | in progress | [deployment-core](modules/deployment-core.md) |
| design-review | settled | [design-review](modules/design-review.md) |
| engine-knowledge-graph | not yet described | [engine-knowledge-graph](modules/engine-knowledge-graph.md) |
| engineering-quality | in progress | [engineering-quality](modules/engineering-quality.md) |
| engineering-quality-python | in progress | [engineering-quality-python](modules/engineering-quality-python.md) |
| engineering-quality-typescript | in progress | [engineering-quality-typescript](modules/engineering-quality-typescript.md) |
| evidence-explorer | in progress | [evidence-explorer](modules/evidence-explorer.md) |
| execution-environment | in progress | [execution-environment](modules/execution-environment.md) |
| external-contribution | settled | [external-contribution](modules/external-contribution.md) |
| github-projects-sync | settled | [github-projects-sync](modules/github-projects-sync.md) |
| large-change-coordination | in progress | [large-change-coordination](modules/large-change-coordination.md) |
| maintenance-ledger | in progress | [maintenance-ledger](modules/maintenance-ledger.md) |
| memory-semantic-recall | settled | [memory-semantic-recall](modules/memory-semantic-recall.md) |
| memory-substrate-sqlite-fts5 | settled | [memory-substrate-sqlite-fts5](modules/memory-substrate-sqlite-fts5.md) |
| migration-discipline | settled | [migration-discipline](modules/migration-discipline.md) |
| operations-core | in progress | [operations-core](modules/operations-core.md) |
| operator-cockpit | in progress | [operator-cockpit](modules/operator-cockpit.md) |
| platform-currency | in progress | [platform-currency](modules/platform-currency.md) |
| platform-ios | in progress | [platform-ios](modules/platform-ios.md) |
| platform-web | in progress | [platform-web](modules/platform-web.md) |
| product-design | settled | [product-design](modules/product-design.md) |
| product-knowledge-graph | in progress | [product-knowledge-graph](modules/product-knowledge-graph.md) |
| profile-registry | in progress | [profile-registry](modules/profile-registry.md) |
| qa-review | settled | [qa-review](modules/qa-review.md) |
| research-and-learning | in progress | [research-and-learning](modules/research-and-learning.md) |
| routine-mode | settled | [routine-mode](modules/routine-mode.md) |
| runtime-backend-local-container | in progress | [runtime-backend-local-container](modules/runtime-backend-local-container.md) |
| structured-change | in progress | [structured-change](modules/structured-change.md) |
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
