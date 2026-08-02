---
status: locked
---

# design-review

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-23 by [decision 0249](../../adr/0249-resolve-re-lock-design-review-the-optional-advisory-spec-loc.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

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
| `provides` | four `role: plan-review` agent personas (`.claude/agents/` files), one per lens below, **plus their four generated Codex renders** (`.codex/agents/` files, held to both-runtime presence by the fleet's hard parity check) — eight provided files in all |
| `wires` | **none** (file-drop; the roster is derived from agent frontmatter) |
| `depends` | `core` |
| `migrations` | none |

### The four lenses

Each persona is **read-only** (it reports findings via the uniform `output-contract`; the orchestrator
decides and writes — [agents](../systems/surfaces/agents.md)), and declares `role: plan-review`
with the lens below. As built, each also declares the `judgment` model tier at high effort and blocks
`Bash` alongside the native write tools — a stricter grant than the [qa-review](qa-review.md) set, which
keeps the shell to run checks; a plan reviewer has nothing to execute. They install by presence; an installed lens nothing consumes is a coherence finding,
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

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Mirrors the engine's own audit** — the quartet is the product-facing analogue of the lock-time cold-session lenses, not a fresh taxonomy. | Operator judgment: confirm by inspection that the four lenses are the product-facing analogue of the lock-time audit lenses, not a newly invented taxonomy. A design-intent reading no check asserts. | operator |
| **Reviewers report; the orchestrator decides** — read-only personas feeding the finding-disposition loop via the uniform `output-contract`. | Operator observation: all four personas declare read-only permissions, block the write tools and Bash, and carry the plan-review `output-contract`, with the orchestration procedure routing each finding through the disposition loop. Partial support: agent-coherence (hard, CI) asserts a read-only persona actually blocks the native write tools, and the agent frontmatter check holds the contract key well-formed — the feeds-the-loop half is procedure, not machine-asserted. | operator |
| **File-drop, derived roster** — install/uninstall is add/remove a persona file; nothing wires. | Operator observation: the manifest declares `wires: []` and provides a plain file list, with the roster derived from persona presence. Partial support: module-manifest (hard, CI) holds the manifest's grammar valid and self-map-drift (hard, CI) holds the rendered map true to the declaration — neither stats the files on disk, so on-disk presence is your spot-check (a deleted render would surface at the cross-runtime parity check only if it broke the pair's symmetry); no check asserts the nothing-wires claim itself. | operator |
| **Referent-aware, not referent-bound** — only `product-intent` consumes the spec; the other three review with or without one. | Operator observation: read the four persona bodies — product-intent anchors on the locked spec and discloses a no-op when none exists; architecture and risk-governance each state they read intent for context without depending on one; feasibility is simply silent on a referent, tracing the plan to delivery either way. No check inspects which persona consumes the referent. | operator |
| **Two invocation points, both advisory** — the quartet runs at build-orchestration's plan-review gate (the build plan) and, when installed, advises product-design's spec-lock (the spec); both feed the operator's decision, neither is a gate the engine owns, so the wall and the [D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) separation hold ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)). | Operator observation: the orchestration procedure's consumed-lenses record names exactly two consumers — the plan-review gate and the spec-lock ceremony — with acceptance the operator's in both. Partial support: lens-consumption (hard, CI) fails closed if an installed persona is recorded as consumed by no stage; the both-advisory property is not what it asserts. | operator |
