# Build order

*Started 2026-08-02, when the platform capability baseline ([decision 0332](../adr/0332-adopt-the-platform-capability-baseline-snapshot-and-comparis.md))
and its ratified dispositions ([decision 0333](../adr/0333-ratify-the-platform-baseline-dispositions-the-migration-set.md))
produced the first forward work since the corpus settled. This lists, in order, where every settled
capability and the forward work stand in the build sequence, so nothing settled is silently overlooked.*

Two phases:

- **Shipped — engine-template as built.** Every settled capability is already built and reconciled at the
  pinned commit ([decision 0331](../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md)); these
  rows record that standing, not pending work. A settled capability that a future phase touches rides both
  phases.
- **R7 — platform capability baseline & currency** (the proposed release milestone; its name is tunable
  until the milestone is created). The five approved migrations build first — each a bounded engine-template
  build tracked as a leaf issue under
  [engine-template #657](https://github.com/StarshipSuperjam/engine-template/issues/657), with any spec edit
  riding its build per decision 0333 — then the platform-currency module builds against the settled result,
  so the recurring review never measures a moving target. The migrations are engine-template builds, not
  spec capabilities of their own, so their rows schedule no capability document; the two whose builds carry
  a known spec reconciliation (M1 → Audits, M2 → Hooks) list those capabilities riding the R7 phase as well.

| Phase | Capability | Doc |
| --- | --- | --- |
| Shipped — engine-template as built | audit-library | [audit-library](modules/audit-library.md) |
| Shipped — engine-template as built | core | [core](modules/core.md) |
| Shipped — engine-template as built | dependency-discipline | [dependency-discipline](modules/dependency-discipline.md) |
| Shipped — engine-template as built | design-review | [design-review](modules/design-review.md) |
| Shipped — engine-template as built | external-contribution (module) | [external-contribution](modules/external-contribution.md) |
| Shipped — engine-template as built | github-projects-sync | [github-projects-sync](modules/github-projects-sync.md) |
| Shipped — engine-template as built | memory-semantic-recall | [memory-semantic-recall](modules/memory-semantic-recall.md) |
| Shipped — engine-template as built | memory-substrate-sqlite-fts5 | [memory-substrate-sqlite-fts5](modules/memory-substrate-sqlite-fts5.md) |
| Shipped — engine-template as built | migration-discipline | [migration-discipline](modules/migration-discipline.md) |
| Shipped — engine-template as built | product-design | [product-design](modules/product-design.md) |
| Shipped — engine-template as built | qa-review | [qa-review](modules/qa-review.md) |
| Shipped — engine-template as built | routine-mode | [routine-mode](modules/routine-mode.md) |
| Shipped — engine-template as built | validators-core | [validators-core](modules/validators-core.md) |
| Shipped — engine-template as built | Attention | [Attention](systems/cognitive/attention.md) |
| Shipped — engine-template as built | Knowledge | [Knowledge](systems/cognitive/knowledge.md) |
| Shipped — engine-template as built | Memory | [Memory](systems/cognitive/memory.md) |
| Shipped — engine-template as built | State | [State](systems/cognitive/state.md) |
| Shipped — engine-template as built | Module system | [Module system](systems/grammar/module-system.md) |
| Shipped — engine-template as built | Ontology | [Ontology](systems/grammar/ontology.md) |
| Shipped — engine-template as built | Audits | [Audits](systems/guardrails/audits.md) |
| Shipped — engine-template as built | Telemetry | [Telemetry](systems/guardrails/telemetry.md) |
| Shipped — engine-template as built | Templates | [Templates](systems/guardrails/templates.md) |
| Shipped — engine-template as built | Validation | [Validation](systems/guardrails/validation.md) |
| Shipped — engine-template as built | Control plane | [Control plane](systems/infrastructure/control-plane.md) |
| Shipped — engine-template as built | Hooks | [Hooks](systems/infrastructure/hooks.md) |
| Shipped — engine-template as built | Provisioning | [Provisioning](systems/infrastructure/provisioning.md) |
| Shipped — engine-template as built | Repository topology | [Repository topology](systems/infrastructure/repository-topology.md) |
| Shipped — engine-template as built | Boot / orientation | [Boot / orientation](systems/lifecycle/boot.md) |
| Shipped — engine-template as built | Build orchestration | [Build orchestration](systems/lifecycle/build-orchestration.md) |
| Shipped — engine-template as built | Close | [Close](systems/lifecycle/close.md) |
| Shipped — engine-template as built | External contribution (system) | [External contribution](systems/lifecycle/external-contribution.md) |
| Shipped — engine-template as built | Operating modes | [Operating modes](systems/lifecycle/modes.md) |
| Shipped — engine-template as built | Agents | [Agents](systems/surfaces/agents.md) |
| Shipped — engine-template as built | Check | [Check](systems/surfaces/check.md) |
| Shipped — engine-template as built | Conduct | [Conduct](systems/surfaces/conduct.md) |
| Shipped — engine-template as built | Contracts | [Contracts](systems/surfaces/contracts.md) |
| Shipped — engine-template as built | Docs | [Docs](systems/surfaces/docs.md) |
| Shipped — engine-template as built | Interfaces | [Interfaces](systems/surfaces/interfaces.md) |
| Shipped — engine-template as built | Operations | [Operations](systems/surfaces/operations.md) |
| Shipped — engine-template as built | Policies | [Policies](systems/surfaces/policies.md) |
| Shipped — engine-template as built | Schemas | [Schemas](systems/surfaces/schemas.md) |
| Shipped — engine-template as built | Skills | [Skills](systems/surfaces/skills.md) |
| Shipped — engine-template as built | Tools | [Tools](systems/surfaces/tools.md) |
| R7 — platform capability baseline & currency | M1 — audit-prep structured output (engine-template build) | — |
| R7 — platform capability baseline & currency | Audits (M1's spec reconciliation rides its build) | [Audits](systems/guardrails/audits.md) |
| R7 — platform capability baseline & currency | M2 — SessionEnd: wire it or retract it (engine-template build) | — |
| R7 — platform capability baseline & currency | Hooks (M2's inventory-row update rides its build) | [Hooks](systems/infrastructure/hooks.md) |
| R7 — platform capability baseline & currency | M3 — routine terminology fix (engine-template docs) | — |
| R7 — platform capability baseline & currency | M4 — widen the effort vocabulary (engine-template build; carries its weakening acknowledgment) | — |
| R7 — platform capability baseline & currency | M5 — host-hardening and dependency documentation (engine-template docs) | — |
| R7 — platform capability baseline & currency | platform-currency | [platform-currency](modules/platform-currency.md) |
