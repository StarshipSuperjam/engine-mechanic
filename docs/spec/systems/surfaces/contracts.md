---
status: draft
---

# Contracts

*Settled in the design workspace on 2026-07-12, ratified by [decision 0300](../../../adr/0300-resolve-re-lock-contracts-the-two-eadr-populations-named-can.md).*

## Summary

The decision-record surface — the engine's **why**. A contract captures one architecturally
significant decision: what was chosen, the rationale, and the anti-choice (the alternative weighed
and rejected). Contracts are the top authority tier; an accepted contract outranks every standing
rule and mechanic below it.

## Behavior

### Contract is not specification

A contract records a *decision*. A **specification** records *current state* — how a system works
now — and is rewritten in place. They are different *kinds of document*: a specification is a
current-state design document — a doc-nature, **not a catalogued surface** — ratified *by* a contract and
possibly locked, but it is not itself a contract. The [ontology](../grammar/ontology.md)
is a specification ratified by a contract, not a contract instance. Keeping the two apart is what
lets history stay append-only while specifications stay final-voice.

### Shape and storage

- **One file per decision**, engine-namespaced and slug-named — the engine-owned canon `eADR-####`
  (e.g. `eADR-0001-...`); a deployment's own per-instance records a per-project namespace on the same
  root, `<project-slug>-eADR-####` (e.g. `acme-eADR-0001-...`) — **discovered by directory listing**;
  the listing *is* the index ([ontology](../grammar/ontology.md) consumption law for
  instances), so an eADR is added by dropping a file, never by registering it in a catalogue. The
  surface has **two homes** (the engine-owned canon and the deployment's own per-instance stream — see
  *The foundational canon* below), each indexed by its own listing. Both id schemes are engine-namespaced
  per the ontology's identifier law: an engine decision record never collides with a product's own ADR
  system, and the per-project namespace keeps a deployment's records from colliding with the **advancing
  canon** at the identifier level as its ids grow. This gives the
  [knowledge graph](../cognitive/knowledge.md) a citable entity per decision and lets
  supersession be a link between files.
- **Append-only history.** A superseded contract is kept and linked from its successor, never
  deleted. This is the explicit history exception to the deletion mandate ([principles §11](../../../principles.md)).
- **Lifecycle** is the `decision` vocabulary: `proposed → accepted → superseded`. There is **no
  `rejected` state** — a rejected alternative is recorded as an anti-choice inside the contract that
  prevailed. An abandoned proposal (never accepted, no history value) may be deleted while still
  `proposed`.
- The [template](../guardrails/templates.md) requires: Decision, a Significance statement
  (the architectural significance and what it constrains — the field the contract-threshold policy
  hard-checks), Rationale, Anti-choice, and Status. A Supersedes link is required **only when** the
  contract replaces an earlier one — a first-of-its-kind decision supersedes nothing.

### The contract threshold

Contracts are **exceptional**, not routine. A decision earns a contract only when it is
architecturally significant, constrains future work, is hard to reverse, **and** has a genuine
anti-choice. Everything below that bar is recorded in the structured pull-request body — the
[control-plane](../infrastructure/control-plane.md) PR contract — which the pull request
carries as the durable record, or is simply done. The bar, and the controls that hold the
AI to it, are the contract-threshold policy in [policies](policies.md); the structured
pull-request body is the default home for below-threshold session narrative.

### The foundational canon

The surface ships **non-empty**. A bounded **foundational canon** of eADRs records the Engine's own
structural-law *why* — present from instantiation, not accumulated — because a deployed Engine is a
standalone artifact whose builders cannot reach the workspace where its laws were decided; without it a
builder retools a law blind (the [§18](../../../principles.md) rationale-persistence law). Two populations
share the surface. For the overlay they are told apart **by path / engine-owned-set membership, never by a
content marker** (below); to a reader and in a bare citation they are told apart by their **id namespace** —
the canon `eADR-####`, a deployment's `<project-slug>-eADR-####`:

- **The canon — engine-owned.** Each entry distils one founding structural law (a cross-cutting invariant
  or a system's defining decision) into a pure decision — chosen + rationale + anti-choice + significance,
  never a current-state narrative (the *Contract is not specification* line holds: the *what* stays the
  derived self-map, the canon is the *why*). Membership is the **law-selected** set — not one-per-decision
  of planning history, not one-per-doc; the bar is an Engine structural law that clears the contract
  threshold and is not a reconciliation. It lives in an **engine-owned canon path** carried in `core`'s
  `provides`, so the engine-upgrade overlay replaces it wholesale like any engine-owned content
  (escalate-upstream); an operator edit to a canon eADR rides the upgrade's reviewed pull request and the
  merge gate — surfaced and consented, never silent. The per-instance stream (below) lives in a separate
  **deployment-owned path** the overlay preserves; the two are told apart by the same engine-owned-set
  membership the overlay and CODEOWNERS already use — the canon is in a module's `provides`, the stream is
  not — **not** by a content marker ([provisioning](../infrastructure/provisioning.md),
  [repository-topology](../infrastructure/repository-topology.md) laws 3 + 5). The literal
  directory names are a build-spec leaf.
- **The per-instance stream — deployment-owned.** A deployment authors its own eADRs for the Engine
  decisions it makes, named in a **per-project namespace on the `eADR` root — `<project-slug>-eADR-####`**
  (the concrete slug, from the deployment's project identity, is a build-spec leaf). The prefix is a human-
  facing identifier wall, not the overlay's classifier: it keeps a deployment's bare tokens from colliding
  with the advancing canon's `eADR-####` in commit messages and citations, applying the ontology's
  engine-namespacing law one level in (engine-vs-engine). These records live in the deployment-owned path
  and are **preserved across an upgrade** — a deployment's decision history is its own, never clobbered by
  an overlay.

The canon is **stable by construction** — the surface's answer to ADR explosion. It changes only by
**supersession** (re-litigating a law writes a new linked eADR; the old is kept, never edited), and a
reconciliation or re-lock of an existing law **folds into** that law's eADR rather than spawning one; the
set moves only on the rare, gated re-litigation of a structural law. It is **reached on demand** — by the
orientation scent, search, or a direct read of the committed file — and is **never pushed into the
cold-start boot pack**; the [knowledge graph](../cognitive/knowledge.md) derives an entity per
eADR by the same presence walk but adds **no forward `ratifies` edge**, and (per
[knowledge](../cognitive/knowledge.md)) persists no reverse edges — so **no persisted edge
targets a canon eADR**, and the cold-start adjacency walk that fills attention's structural-neighbours
partition never pulls the canon in as ambient bulk. A canon eADR surfaces only when current work cites or
lexically matches it (the scent / search), so a stable canon never burdens orientation.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A contract with no substantive anti-choice or significance statement is structurally not a contract — the template enforces those fields' presence (a `hard-fail`), while their *genuineness* stays posture. | Read this description against the built behavior and confirm they match. | operator |
| Authority comes from the contract being `accepted` and non-superseded; supersession, not editing, changes a standing decision. | Read this description against the built behavior and confirm they match. | operator |
| **The why ships, bounded.** The surface carries a foundational canon (engine-owned `eADR-####`, overlaid on upgrade) and a per-instance stream (deployment-owned `<project-slug>-eADR-####`, preserved), distinguished by path for the overlay and by id namespace for the reader; the canon changes only by supersession and stays exceptional under the contract threshold — never edited in place, never accumulating routine decisions. | Read this description against the built behavior and confirm they match. | operator |
