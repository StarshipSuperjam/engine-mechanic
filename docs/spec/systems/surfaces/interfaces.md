---
status: locked
---

# Interfaces

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-05-29 by [decision 0116](../../../adr/0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

A **protocol contract a swappable implementation satisfies** — the stable seam that lets a foundation keep a
lightweight default while a heavier capability slots in behind the same boundary, without the consumer
knowing which it got. An interface declares the callable shape (inputs, outputs, the operations it must
support) **and names its own default/fallback implementation**, so degradability ([principles §5](../../../principles.md))
is a property stated at the contract rather than scattered into consumers.

This is distinct from two neighbours it is easily confused with: a [`schema`](schemas.md) governs a
**data payload's** shape, whereas an interface governs a **protocol** (a callable boundary); and the
[module-system](../grammar/module-system.md)'s closed **wiring seam** applies keyed, reversible
edits to *shared state*, whereas an interface is **polymorphism** — many possible implementations of one
contract, selected by which is present.

## Behavior

### Meta-contract record

| Field | Value |
|---|---|
| name | `interface` |
| class | structured |
| location | `.engine/interfaces/` |
| purpose | a protocol contract a swappable implementation satisfies; names its default/fallback |
| authority tier | 3 — mechanics/guidance |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | JSON Schema 2020-12 over the interface declaration |
| template | none — a `structured` surface is governed by its schema, not a prose template |

Instances are slug-named files under `.engine/interfaces/`, engine-namespaced per the
[ontology](../grammar/ontology.md) identifier law.

### Implementations bind by presence — and resolve to one

An interface's implementations are **discovered by presence**, not registered in a central list an install
edits — the [derived binding by presence principle](../../../principles.md). An implementation is
[`tool`](tools.md) code that conforms to the contract and is present at a known engine-namespaced
handle (for the v1 MCP-backed interfaces, the engine-prefixed MCP server name — an override replaces the
server behind the same name; the concrete handle is a build-spec leaf). Installing a richer implementation
is therefore a **file drop** (the providing [module](../grammar/module-system.md)'s `provides`),
and removing it a file deletion — no wiring, no roster surgery, which is the discovery-side half of the
[R5](../../../reference/risks.md) containment story.

**Resolution is single-active** — this is where an interface differs from the *set-valued* discovery cases
(the [agent](agents.md) roster, [check](check.md)-suite membership), where every present
member joins. An interface is polymorphism: **exactly one implementation answers**. A present conforming
non-default overrides the named fallback; with none present the named fallback answers; **more than one
conforming non-default present is a [coherence](check.md) finding** — surfaced, never a silent
arbitrary pick (a silent choice among implementations is the trust breach [principle §5](../../../principles.md)
forbids). This *refines* the §14 discovery axis — discovery is by presence; resolution among what is
discovered is single-active — and does not amend §14, which makes no cardinality claim. The concrete
precedence is a build-spec leaf.

### The fallback is part of the contract

Because the contract **names its default/fallback implementation**, the engine always has a working answer
even with no module installed — the guarantee holds because the named fallback is itself a shipped
foundation [`tool`](tools.md) (ship-the-substrate, [principle §4](../../../principles.md)) — and
the audit can verify the fallback exists. One disclosed qualification, operator-ruled in the
reconciliation: a contract may carry an operation the floor cannot answer, provided the declaration
itself says so and the floor's answer is an **explicit declared-unavailable shape**, never an error or a
silent absence — the `search` contract's meaning-based recall operation is the one v1 case (below). The
floor still answers every operation; for such an operation the working answer is the honest
"not available here." How an *active* fallback is surfaced splits on two conditions, so
"loud" never becomes a nag the operator learns to ignore:

- **A richer implementation is installed but its substrate is down.** An unexpected degraded state:
  surfaced loudly per the locked [module-system](../grammar/module-system.md) inactive-substrate
  disclosure law and rendered by [boot](../lifecycle/boot.md) — what is degraded and the one step
  back to full capability.
- **No richer implementation is installed.** The named fallback is a **valid steady state** the operator may
  run forever (the `search` floor is offline and zero-dependency *by design*), so it is **not a standing
  nag**: the richer option is offered at most once, acknowledgeably, then stays silent. The step, when
  taken, is **engine-driven** — the engine installs the module on the operator's approval, never a command
  the operator types (the [boot](../lifecycle/boot.md) engine-driven-fix posture). The
  acknowledgment mechanism is a build-spec leaf.

The rendering is plain capability-language, never the interface slug — "*I'm using basic keyword memory
search; richer meaning-based search is available — want me to set it up?*", never "running on the fallback
`search` implementation"; the exact wording is [boot](../lifecycle/boot.md)'s.

### Conformance

The interface **declaration** is governed by JSON Schema 2020-12 (the `schema` kind). A present
implementation's conformance — and the single-active invariant above — are confirmed by a dedicated
merge-gated interface-coherence [check](check.md) (a `custom/script` rule applying the coherence
posture, running in the CI suite): a file claiming to implement an interface
but diverging from the declaration, or a second non-default implementation present, is a **finding**
(surfaced, not silently trusted) — the same posture as a dangling check-kind. This introduces **no new
check-kind** — the `coherence` kind proper stays scoped to module-set consistency, and the escape-hatch
rule rides the existing grammar; the locked [validation](../guardrails/validation.md)/[check](check.md)
grammar is untouched. Mechanical conformance is structure and presence; full *behavioral* equivalence of
arbitrary code is a test concern, not a check.

### The v1 interfaces

Three seams ship as interfaces in v1 (home `.engine/interfaces/`; the memory pair share one fallback
handle):

- **`search`** — memory recall. The default/fallback is the foundation's FTS5 lexical floor (offline,
  zero-dependency). Semantic recall arrives **inside that same implementation, as an added operation**,
  not as an override: installing the semantic-recall [module](../grammar/module-system.md) makes the
  one memory implementation register its meaning-based recall operation, and with the module absent the
  contract's declaration answers that operation with the explicit declared-unavailable shape (the
  disclosed qualification above) — so adding embeddings is a bolt-in, not a store migration
  ([memory](../cognitive/memory.md)), and the boundary never silently picks between two engines.
- **`memory-control`** — the operator's memory controls (pin, withhold, restore, erase, and the like),
  deliberately split from `search` so that recall's contract can *state* on its face that **reading
  never changes or removes what is stored**: the operations that write live behind their own seam,
  answered by the same foundation implementation. The split expresses the read/write boundary; what
  *upholds* it is that one implementation's discipline, not the seam's shape —
  [§12](../../../principles.md) attributes every isolation claim to the wiring discipline, never to the
  architecture's shape, and this seam is no exception.
- **knowledge representation/retrieval** — the [knowledge](../cognitive/knowledge.md) graph's
  representation and retrieval leaf, kept swappable so a richer engine can slot in (and be bounded) without
  reopening knowledge ([R8](../../../reference/risks.md)). Its **operation set** — the structural query surface every
  conforming implementation provides, the fallback floor and any richer swap-in alike — is `get-entity(id)`
  (an entity and its declared edges), `find(selector)` (entities matching a selector, e.g. surface
  category, path glob, or attribute), `neighbors(id, edge-filter?, direction?, depth?)` (adjacency
  traversal), and
  `relate(id-a, id-b)` (the relationship/path between two entities). The read-time memory link is **not** an
  operation here — the consumer composes it, or it does not exist: knowledge returns entity-ids, and the
  consumer queries memory's recall with one as a plain search term over the transcript
  ([memory](../cognitive/memory.md) — the once-designed tag-keyed read-time join went with the retired
  curation layer, so no persisted join exists on either side), keeping the two seams
  independent
  ([D-116](../../../adr/0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md)).

Each backing MCP server additionally answers a content-free **`health`** availability probe — the
safe liveness check consulted before the first operator-facing answer — declared once per server (on
the `search` and knowledge-retrieval contracts; `memory-control` shares its server's probe and
declares none of its own), not a retrieval operation, and outside the pinned op-set law above.

### Build-spec leaves

The concrete interface declarations as **JSON Schemas** — the `search` declaration and the per-operation
schemas for the now-pinned knowledge-retrieval op-set — plus the conformance-check specifics, the selection
precedence algorithm, the fallback-acknowledgment mechanism, and the discovery handle are build-spec leaves
authored in the build session (laws-not-leaves, [D-052](../../../adr/0052-foundational-law-layer-closed-the-implementation-lock-order.md); the form/contract is
pinned and the values deferred, [D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)). The laws fixed here are
protocol-not-payload, polymorphism-by-presence, single-active resolution, named-never-silent fallback,
a-deliberate-floor-is-not-nagged, and the knowledge-retrieval **operation set** above.

## Operator and automatic workflow routing

**Current disposition: `none`.** This capability is internal engine machinery; no operator command or automatic natural-language route names it, and none is added speculatively under decision 0336.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Protocol, not payload** — an interface governs a callable boundary; data shape is a `schema`'s job. | Operator observation: each declaration under `.engine/interfaces/` names callable operations with input and output schemas, while payload shape lives with the [schemas](schemas.md) surface; the interface-declaration check (hard, CI) asserts the declaration's form but not the boundary distinction itself. | operator |
| **Polymorphism, not wiring** — many implementations of one contract, selected by presence; not a shared-state side-effect. | Operator observation, partially supported by the interface-coherence check (hard, CI), which carries the only-one-active rule — though as built no production mechanism discovers a present implementation (the single-active row below); the not-wiring half is observed in the module manifests, where no interface implementation appears as a wiring entry. | operator |
| **Fallback named and never silent** — degradability is stated at the contract and an active fallback is surfaced to the operator in plain language. | Split: the named-at-the-contract half is asserted by the interface-declaration check (hard, CI), whose governing schema makes `fallback` a required field — a declaration without one is refused at the merge. The surfaced-in-plain-language half is [boot](../lifecycle/boot.md)'s rendering, observed by the operator; no check asserts it, so the composite row stays with the operator. | operator |
| **Single-active resolution** — exactly one implementation answers; more than one non-default present is a coherence finding, never a silent pick. | The interface-coherence check (hard, CI, merge-gated) carries the rule, but partially: as built, its present-implementations input is **empty in production** — no engine mechanism yet discovers an installed second implementation, and the only-one-active rule is witnessed biting only against seeded test fixtures (the check's own negative-fixture seam). Until a discovery mechanism exists, a second implementation arriving would **not** turn the check red on its own — so the resolution rests on your read, with the check as partial support, not an assertion. | operator |
| **A deliberate floor is not nagged** — a fallback the operator runs by choice is a valid steady state, not a standing alarm; only an unexpectedly-down richer substrate is surfaced loudly. | Operator observation of [boot](../lifecycle/boot.md)'s behavior across the two conditions: a no-richer-module deployment surfaces the richer option at most once and then stays silent, while an installed-but-down substrate is surfaced loudly with the one step back. No check asserts nag-versus-steady-state. | operator |
