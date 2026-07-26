---
status: accepted
engine_record: true
---

# Reports & self-improvement scope: Engine-only self-monitoring on a judgment ladder

*Decided 2026-05-24 in the design workspace.*

## The decision

[Telemetry](../spec/systems/guardrails/telemetry.md) and [audits](../spec/systems/guardrails/audits.md) are **Engine-only self-monitoring**. Their division of labor is a three-rung **judgment ladder**: [validation](../spec/systems/guardrails/validation.md) (mechanical, per-event, artifact-vs-contract) → telemetry (mechanical, continuous/aggregate over native records) → audits (judgment, periodic, contract-vs-reality); signal feeds up, semantic judgment defers up. **Product health is bounded native perception** — GitHub CI signal plus the locked [finding-disposition](../spec/systems/surfaces/policies.md) routing to Issues; a deeper product-quality regime is an **opt-in module**, never the foundation. The unwinding key is a **domain tag with subject-of-claim semantics**, carried as the **label** on the tracked issue (engine vs product), so engine-labeled issues feed the engine remediation loop and product-labeled issues are normal Build backlog.

## Why

The Engine-is-a-contributor principle ([D-026](0026-the-engine-is-an-embedded-team-member-contributor-not-compon.md)/[principle §13](../principles.md)) settles it: the Engine must monitor *itself* completely because nothing else can (asymmetric awareness), but it only *perceives* the product enough to contribute well — it never stands up a product-QA regime ([principle §12](../principles.md): foundations are contagious; Risk [R6](../reference/risks.md)). Engine-only makes the unwinding **structural** (engine-domain by construction) instead of per-signal disentangling. The ladder puts semantic judgment where the locked validation already deferred it ("semantic quality is the audits layer's job") and matches the prototype's hard-won three-layer lesson (checks ask "does this obey the rule now?"; audits ask "is the rule still right?").

## What we ruled out

A dual Engine+Product observatory (rejected — product-QA in the foundation is R6 scope creep and §12 contagion; the product has its own CI/review). Collapsing telemetry and audits into one system or one cadence (rejected — leaves validation's punted semantic-quality concern homeless; mechanical aggregation and judgment are different rungs). Separate stores per domain (rejected — both domains live as labeled issues; the unwinding is by label, not by store).
