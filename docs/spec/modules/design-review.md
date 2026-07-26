---
status: draft
---

# design-review

*Settled in the design workspace on 2026-06-23, ratified by [decision 0249](../../adr/0249-resolve-re-lock-design-review-the-optional-advisory-spec-loc.md).*

## Summary

The **plan-review stage roster**: four cold-context reviewer [agent](../systems/surfaces/agents.md)
personas the [build orchestration](../systems/lifecycle/build-orchestration.md) invokes at its
**plan-review** gate, each a distinct lens on the *proposed* work — *are we designing the right thing, and
is the design sound?* This is one half of the v1 lens roster ([D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)); its
companion is the [qa-review](qa-review.md) suite at the pre-submission gate.

The roster is grounded in a traveled lane: it **mirrors the Engine's own cold-session design audit** — the
adversarial / technical-feasibility / architect / operator lenses CLAUDE.md mandates before any lock. The
build-time product review is the product-facing analogue of the mechanism the workspace already trusts to
gate its own irreversible decisions.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `design-review` |
| `status` | `optional` |
| `provides` | four `role: plan-review` agent personas (`.claude/agents/` files), one per lens below |
| `wires` | **none** (file-drop; the roster is derived from agent frontmatter) |
| `depends` | `core` |
| `migrations` | none (v1) |

### The four lenses

Each persona is **read-only** (it reports findings via the uniform `output-contract`; the orchestrator
decides and writes — [agents](../systems/surfaces/agents.md)), and declares `role: plan-review`
with the lens below. They install by presence; an installed lens nothing consumes is a coherence finding,
so [build orchestration](../systems/lifecycle/build-orchestration.md) records that its plan-review
gate consumes all four.

1. **`lens: product-intent`** — *Are we designing the right thing?* Owns the translation need → outcome →
   behaviour → **acceptance criteria**; scope boundaries; user value; usability fit; priority trade-offs.
   It is a **primary consumer of the [product-design](product-design.md) referent — the committed
   `locked` spec** ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) — and returns the plain-language **criteria-quality
   verdict** ("checkable" versus "too vague — here is what is missing"). *Catches:* a coherent, elegant thing
   that solves the wrong problem.
2. **`lens: architecture`** — *Is the design structurally sound?* Component boundaries, data model,
   integration seams, maintainability, modularity, technical consistency, safe build sequencing. *Catches:*
   a design that works at first and becomes brittle or incoherent.
3. **`lens: feasibility`** — *Can this be built, shipped, and operated?* Implementation path, deployment,
   operations and recovery, migration, build-and-run cost, external dependency risk. *Catches:* a
   theoretically good design that cannot survive contact with reality.
4. **`lens: risk-governance`** — *How can this fail, be abused, or violate constraints?* Security by
   design, privacy, compliance, governance and traceability, abuse cases, resilience, trust boundaries.
   *Catches:* a useful, well-built design that is unsafe or ungovernable. (Its pre-submission counterpart
   — *did we actually prevent it?* — is the qa-review `security-governance` lens; same concern, different
   role.)

### Depth is proportionate

The suite is installable and individually composable, but **how many lenses run is risk-proportionate and
operator-gated** at the plan-gate risk assessment ([build orchestration](../systems/lifecycle/build-orchestration.md)):
a trivial change runs none; a schema or guardrail change runs the full quartet. A change with no `locked`
spec to check against — none exists, or the pointer reaches only a `draft` — makes `product-intent` a
**disclosed no-op** ("I could not check this against a spec — none is locked"), never a silent green pass
([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)).

### A second, optional invocation — advising a spec-lock

[build orchestration](../systems/lifecycle/build-orchestration.md) invokes the quartet at the
plan-review gate (above), reviewing a **build plan**. When this suite is installed it gains a **second,
optional invocation point**: [product-design](product-design.md)'s **spec-lock ceremony**
([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) may invoke the quartet to **advise on the spec itself** (referent = the
spec, not a build plan) — the product analogue of this workspace's cold-session design audit before a lock.
The lenses **advise; they never gate**: their findings are evidence the **operator** weighs, and the
**operator's recorded acceptance** is what locks the spec — the engine never *vetoes* what the product may
become (the engine validates **form** and advises on content per the
[engine/product wall](../systems/infrastructure/repository-topology.md) re-scope,
[D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md); the operator governs it). It is **optional enrichment bound by
presence** — a repo without this suite locks a spec on validation green plus the operator's acceptance
alone — so [product-design](product-design.md) takes **no hard `depends` edge** to this module:
the [D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) referent-producer↔lens-roster separation holds (the suite is *consumed
by*, never *depended on by*, product-design). Two referents, two moments — the spec at lock, the build plan
at plan-review — distinct, not redundant.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Mirrors the engine's own audit** — the quartet is the product-facing analogue of the lock-time cold-session lenses, not a fresh taxonomy. | Read this description against the built behavior and confirm they match. | operator |
| **Reviewers report; the orchestrator decides** — read-only personas feeding the finding-disposition loop via the uniform `output-contract`. | Read this description against the built behavior and confirm they match. | operator |
| **File-drop, derived roster** — install/uninstall is add/remove a persona file; nothing wires. | Read this description against the built behavior and confirm they match. | operator |
| **Referent-aware, not referent-bound** — only `product-intent` consumes the spec; the other three review with or without one. | Read this description against the built behavior and confirm they match. | operator |
| **Two invocation points, both advisory** — the quartet runs at build-orchestration's plan-review gate (the build plan) and, when installed, advises product-design's spec-lock (the spec); both feed the operator's decision, neither is a gate the engine owns, so the wall and the [D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) separation hold ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)). | Read this description against the built behavior and confirm they match. | operator |
