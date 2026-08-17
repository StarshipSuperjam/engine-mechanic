---
status: locked
---

# Contracts

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the canon-model passages corrected (2026-08-02) by [decision 0330](../../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md); ratified as intended design on 2026-07-12 by [decision 0300](../../../adr/0300-resolve-re-lock-contracts-the-two-eadr-populations-named-can.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

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
- **Append-only history (the instance stream's discipline).** A deployment's superseded contract is kept
  and linked from its successor, never deleted — the explicit history exception to the deletion mandate
  ([principles §11](../../../principles.md)). The shipped canon supersedes nothing; it is revised in
  place (see *The foundational canon* below).
- **Lifecycle** is the `decision` vocabulary: `proposed → accepted → superseded`. There is **no
  `rejected` state** — a rejected alternative is recorded as an anti-choice inside the contract that
  prevailed. An abandoned proposal (never accepted, no history value) may be deleted while still
  `proposed`.
- The [template](../guardrails/templates.md) requires: Decision, a Significance statement
  (the architectural significance and what it constrains), Rationale, Anti-choice, and Status —
  Significance **and** Anti-choice being the two fields the contract-threshold policy hard-checks
  as filled, never blank or the template's placeholder. A Supersedes link is required **only when** the
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

The canon is **stable by construction** — the surface's answer to ADR explosion. Per its own
one-history law (eADR-0014), the shipped canon is a **living cold-copy snapshot, revised in place**
— it carries no supersession chain (the schema's `supersedes` field belongs to the instance stream
alone), a reconciliation or re-lock of an existing law **folds into** that law's eADR rather than
spawning one — a fold that absorbs a just-minted record may leave a gap in the number sequence,
which is this rule working, not a lost record — and only a genuinely new kind of decision earns a
new founding record; supersession-with-history is the **instance stream's** discipline, where a
deployment's own standing decision is never edited, only replaced by a new linked record. It is **reached on demand** — by the
orientation scent, search, or a direct read of the committed file — and is **never pushed into the
cold-start boot pack**; the [knowledge graph](../cognitive/knowledge.md) derives an entity per
eADR by the same presence walk but adds **no forward `ratifies` edge**, and (per
[knowledge](../cognitive/knowledge.md)) persists no reverse edges. The graph's supersession
predicate is scoped to the deployment stream — **a canon eADR is never a supersession target, so no
persisted citation-class reference reaches the canon**; the persisted edges that do touch it are the
uniform mechanical scaffolding every surface instance carries (the contract checks' targeting edges
and the schema and module bindings), routing metadata rather than citation bulk. A canon eADR
surfaces when current work cites or
lexically matches it (the scent / search), so a stable canon never burdens orientation.

## Operator and automatic workflow routing

**Current disposition: `none`.** This capability is internal engine machinery; no operator command or automatic natural-language route names it, and none is added speculatively under decision 0336.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A contract with no substantive anti-choice or significance statement is structurally not a contract — the template enforces those fields' presence (a `hard-fail`), while their *genuineness* stays posture. | The presence half is fully carried by the contract-threshold check (presence-kind, hard, CI): a contract's Significance and Anti-choice sections must each be filled in, not left blank or as the template's placeholder — with the contract-shape check (hard, CI) holding the five sections present and ordered. The genuineness half is the operator's read of the committed record at review, as the threshold check's own message concedes — so the composite row stays with the operator, the checks as named full support for the presence half. | operator |
| Authority comes from the contract being `accepted` and non-superseded; in the instance stream, supersession — not editing — changes a standing decision (the shipped canon is revised in place under eADR-0014). | Operator observation at review that a deployment's changed standing decision arrives as a new linked record rather than an edit to the earlier one; the contract-frontmatter check (schema-kind, hard, CI) supports only the vocabulary — the status enum and a well-formed supersedes id — and no check detects an in-place edit to an accepted record's Decision. | operator |
| **The why ships, bounded.** The surface carries a foundational canon (engine-owned `eADR-####`, overlaid on upgrade) and a per-instance stream (deployment-owned `<project-slug>-eADR-####`, preserved), distinguished by path for the overlay and by id namespace for the reader; the canon is revised in place under eADR-0014 (no supersession chain — that is the instance stream's discipline) and stays exceptional under the contract threshold — never accumulating routine decisions. | Operator observation across the composite: the canon ships non-empty, the overlay's provides-glob replaces engine-owned records while the instance path is preserved, and the anti-accumulation signal is the threshold policy's soft burst note at start-up, never a merge gate. The contract-frontmatter check (hard, CI) supports the id-namespace half by asserting both id shapes; nothing mechanical asserts the overlay or either stream's revision discipline. | operator |
