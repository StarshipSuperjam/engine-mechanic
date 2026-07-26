---
status: accepted
engine_record: true
---

# Product-spec intake: design it native, not bundled; the build-the-Engine path stays native too

*Decided 2026-05-25 in the design workspace.*

## The decision

Resolve how the Engine should acquire a *product specification*, and how this corpus should be turned into build-the-Engine work, against **github/spec-kit** (Spec-Driven Development). **(1)** The Engine has no product-intake front door; design one **natively** as a product-layer module ([Q14](../reference/open-questions.md)) in the Engine's own grammar — spec-kit is a mined methodology reference, **not** a bundled dependency. **(2)** Do **not** adopt spec-kit to convert this corpus into build-the-Engine issues; the native path is to author the WBS (the topological sort of the module dependency graph, today a stub pending the deviation verdicts) and generate engine-labeled GitHub Issues with `gh` + github-collab-bundle / [github-projects-sync](../spec/modules/github-projects-sync.md).

## Why

The product-intake gap is real — the north star requires a non-engineer to express *what* to build, yet no surface captures it — and spec-kit solves exactly that gap; but bundling it imposes a parallel governance vocabulary (its `constitution` vs. this corpus's [principles](../principles.md)/ontology, its `specs/NNN/` tree vs. the [surface catalog](../spec/systems/grammar/ontology.md)), a Python/uv runtime, and an in-flux `.claude/commands`→`.claude/skills` command surface that would strand a non-engineer when it breaks ([constraints](../reference/constraints.md)). A native module composing the already-locked-complete surface set is degradable, committed, and grammar-coherent. For build-the-Engine, spec-kit offers no importer for an existing markdown corpus and its `/specify`+`/plan` front-half is redundant against a richer design already in hand; the only piece with residual value (`taskstoissues`) is something `gh` does natively. A four-lens cold-context audit ran against the disposition plan and confirmed the spec-kit characterizations (its command set, the Python/uv `specify` CLI, the live commands→skills migration breakage, and the absence of any corpus importer) and the native-path feasibility (`gh issue create`).

## What we ruled out

Bundle spec-kit into the template as the product-intake system (rejected — parallel vocabulary, Python/uv runtime, in-flux command surface; mine the methodology, own the mechanism). Adopt spec-kit to convert this corpus into build-the-Engine issues (rejected — no importer, redundant front-half, vocabulary clash with the authoring rules / lock discipline; the native WBS→`gh` Issues path is simpler and already designed). Treat product-intake as out of scope for v1 (rejected — the north star implies a front door; only its shape is open).
