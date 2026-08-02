---
status: stub
---

# clean-code

## Summary

Status: not yet designed (post-v1). This slot is held so the system has a home; the design lands in its own dedicated session.

Its revisit signal is a quality-consistency pressure rather than operator intuition: recurring code-style divergence across sessions or repeated operator style-steers on engine-authored code — the point where a posture-only style stance (the [conduct](../systems/surfaces/conduct.md) behavioral floor) and [memory](../systems/cognitive/memory.md)'s learned per-project enrichment (the transcript-first record and pins) stop holding code-style consistency and an *enforced* per-language injection seam into the worker [agents](../systems/surfaces/agents.md) is earned.

A future, **optional** module family for **code-style governance** of engine-authored product code: a parent module that injects per-language standards into the coding/worker [agents](../systems/surfaces/agents.md) and runs a commit-boundary linter [check](../systems/surfaces/check.md) (a local nudge — CI is the only unbypassable gate), extended by per-language **packs** (e.g. PEP 8/ruff for Python) that depend on this module. Every realization path it could take is additive within the locked grammar, so adding it later never forces a refactor ([D-095](../../adr/0095-cut-expression-contracts-disposition-prose-organization-cove.md)). On promotion it joins the operator-facing **Verification & Validation** install category — it governs the operator's own product code, so it is not hidden engine infrastructure.

## Behavior

### Deferred design threads (for its own session)

- **Grammar realization** — reuse of existing surfaces vs. an additive **tier-3 surface** (weighed against [R6](../../reference/risks.md) surface-sprawl), left open; the [ontology](../systems/grammar/ontology.md) permits a tier-3 surface to attach without a re-lock.
- **Standards-injection seam** into worker subagents — a [§16](../../principles.md)-style channel-bind the worker consults vs. a file-dropped agent variant (a subagent runs on its own definition, not the parent session's context, so standards must reach it via its definition/spawn).
- **Linter-kind realization** — a custom [check](../systems/surfaces/check.md)-kind callable (bound by presence) vs. the `custom/script` escape hatch; the commit-boundary run is a local nudge, CI the gate.
- **Dependency edges + category** — the parent/language-pack edges (re-derived in the design session, `core` the only certain root) and the operator-menu category at promotion.

See [engine-architecture.md](../../architecture.md) for its catalogued role and the [module catalog](../../reference/module-catalog.md) for its place in the packaging view.
