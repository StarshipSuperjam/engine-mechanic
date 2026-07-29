---
status: draft
---

# Ontology

*Reconciled with engine-template@`cdbbc33` as built (2026-07-29) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-07-16 by [decision 0310](../../../adr/0310-resolve-re-lock-ontology-the-coverage-attestation-bounded-to.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

The meta-contract and grammar spine. It names every **surface** the Engine recognizes, defines the
record that governs each, and states the laws — amend-first, authority, enforcement, escalation,
lifecycle — that shape everything authored. It is what stops a cold AI from inventing structure on
the fly, the single most important idea carried from the prototype.

The ontology is a **specification** (current-state, rewritten in place), ratified by a contract and
locked. It is not itself a contract instance; its standing in a conflict rides on its ratifying
decision and its lock, not on a surface tier.

## Behavior

### The surface meta-contract

Every surface is one record. The record is the join of all the grammar's laws projected onto a
single file-type:

- **name** — canonical, glossary-aligned (`contract`, `policy`, `tool`, …); carried as the record's key
  in the catalog, not an in-record field.
- **class** — `prose` · `structured` · `code`. Decides which governance applies (see reach, below).
- **location** — where instances live, under the [repository-topology](../infrastructure/repository-topology.md) placement law: one home per surface, under one of the four surface roots — `.engine/`, plus the runtime-dictated slots under `.claude/` (Claude Code) and under `.codex/` and `.agents/` (the Codex runtime).
- **purpose** — one line.
- **authority** — the surface's authority tier (see below).
- **lifecycle** — which lifecycle vocabulary its instances follow.
- **governing_schema** — the [schema](../surfaces/schemas.md) for its structured content (whole file for `structured`; frontmatter for `prose`).
- **template** — a reference to the surface's [template](../guardrails/templates.md) (the scaffold-plus-shape-spec). Prose surfaces only; not an inlined rule blob.

As built, the catalog lives at `.engine/schemas/surface-catalog.json`, a schema instance governed by its
own schema (`surface-catalog.schema.json`) — the fields above are that schema's seven required record
fields, keyed by the surface's name.

### The catalog

The catalog is a **single schema-governed data file** enumerating one record per surface. Its
governance fields are **authored decisions** (authority, lifecycle, schema, template are not
computed); what is **derived and gated** is *coverage*, **at directory granularity** — every catalogued
surface has the home its own `location` field names, and no orphan surface directory exists. The gate
walks the roots a surface may live under and compares what it finds against `location`; it does **not**
assume `.engine/<surface>/`, because not every surface may live there — the platforms dictate
[agents](../surfaces/agents.md)' and [skills](../surfaces/skills.md)' slots under
`.claude/` and the Codex runtime's mirrors under `.codex/` and `.agents/`, and `location` is the field
that carries that truth. Coverage staleness fails loud.

Coverage is a *structural* attestation, and its [artifact warrant](../../../reference/glossary.md) says so: green
proves the catalog and the filesystem **agree** at that granularity — every catalogued surface has its
home, no directory orphaned — and **not** that the catalogued **governance fields** (authority, lifecycle,
schema, template) are *right*, **nor that no uncatalogued surface-shaped instance is in use**: a general
rule cannot tell an uncatalogued surface from a legitimate non-surface bucket, so that leg is never
mechanically re-attested. Both are an **authoring judgment**, weighed when a surface is
catalogued and at the pull request that adds it — not a thing a green coverage check re-attests, and
not a step deferred onto whoever reads the green result later ([§7](../../../principles.md)/[§17](../../../principles.md)).
As built, the legitimate non-surface buckets are an **explicit infrastructure list the coverage gate
carries** (knowledge, state, telemetry, audits, templates, provisioning and the like), so that judgment
is recorded as data rather than re-made on every run.

**Consumption law.** Surface *definitions* are few and bounded, so **every** definition is read at cold
start — [boot](../lifecycle/boot.md) carries them in its pack as the grammar a session
recognizes a file-kind by. It reads the **recognition** fields (name, location); the **governance** fields
above are the pull-request author's, never the cold session's. Surface *instances* are many and unbounded,
so each instance is a slug-named file and its directory listing is the index; a session opens only the
instances it needs — **that laziness** is what keeps cold-start within the
[attention](../cognitive/attention.md) budget.

Recognition is **posture**, and the tier is named honestly ([§7](../../../principles.md)): the pack is
fail-open, so a session that boots without it is un-grounded in the grammar, and the read makes an invented
file-kind *unlikely* — never impossible. What an invented kind cannot do is **land**: the coverage gate
above stops a drifted surface directory at the merge. An uncatalogued instance inside an existing bucket is
caught by neither, and is the authoring judgment named above.

### The amend-first rule

A new surface is named in the catalog **before** any instance of it is authored, and rework of an
existing surface amends the catalog first. The grammar precedes the content. (See
[principles §10](../../../principles.md).)

### Instance identifiers

Every surface instance that carries a **human-facing identifier** — one used in references, commit
messages, or knowledge-graph entities, not merely a file path — is **engine-namespaced**: prefixed to
mark it as the engine's, so an engine identifier never collides with a product's own. This extends the
engine/product wall ([repository-topology](../infrastructure/repository-topology.md),
[control-plane](../infrastructure/control-plane.md)) from paths to identifiers. Decision
records are engine-prefixed `eADR-####`; each new surface that needs an identifier chooses an
engine-prefixed scheme when it is catalogued.

The same namespacing recurs **one level inside the wall — engine-vs-engine** — on the decision-record
surface, which carries two eADR populations: the engine-owned **foundational canon** and a
deployment's own **per-instance stream** (see [contracts](../surfaces/contracts.md)). The
canon is an advancing frontier whose ids grow over the engine's life, so a bare `eADR-####` shared by
both would collide exactly where a bare token travels with no path — a commit message, a citation — as
the canon catches up to whatever number a deployment authored. The engine-owned canon keeps
`eADR-####`; a deployment's per-instance records carry a **per-project namespace on the same root,
`<project-slug>-eADR-####`**, so the two never collide at the identifier level while both stay
recognizably engine-namespaced. This is a human-facing identifier wall only: which population a record
belongs to is classified by its path / engine-owned-set membership (the overlay's authority —
[repository-topology](../infrastructure/repository-topology.md) law 5), never by the prefix,
so a filename prefix that ever disagreed with its folder defers to the folder.

### The self-referential core

The grammar describes and enforces itself with exactly three surfaces, so the locked ontology names
them and no others: **`contract`** (the ratifying decision; the authority top tier),
**`policy`** (the escalation and threshold rules; the second tier), and **`schema`** (the
meta-contract and catalog are schema instances). Every other surface — `tool`, `check`,
`operations`, and the rest — is an ordinary catalog entry that grows additively without reopening
this doc. Thirteen surfaces are catalogued at the reconciliation pin: the original core and platform
set, grown additively by `conduct`, `interface`, `doc`, and the two Codex-runtime renders
(`codex-agent`, `codex-skill`) — each added by listing its record, exactly as this law intends.

### Authority, enforcement, escalation — three orthogonal axes

These resolve different questions and never substitute for one another. Conflating them is the
grammar's worst latent failure, so they are named apart.

**Authority** is semantic precedence — which statement governs when two disagree. Four tiers, carried
as the surface's `authority` field:

1. **Decisions** — contracts.
2. **Standing rules** — policies.
3. **Mechanics & guidance** — checks, schemas, templates, operations.
4. **Derived / observational** — reports, telemetry, knowledge-graph output; these describe, never govern. As built, no catalogued surface carries this tier — derived outputs are infrastructure, not surfaces, and the rank exists to complete the order (the catalog schema keeps the value and says so).

Resolution law: **higher tier wins; within one surface, supersession decides (the accepted,
non-superseded instance); same-tier across surfaces, or genuine ambiguity, escalates.**

Tiers 1 and 2 are **reserved to the self-referential core by law**: `contract` is the sole tier-1
surface and `policy` the sole tier-2 surface. Surfaces that grow additively into the catalog occupy
tiers 3 and 4. This is a deliberate law, not frozen membership — it fixes *that* decisions outrank
standing rules outrank mechanics, without naming any additive surface. The reservation is held
mechanically from two angles by a hard merge gate (`ontology-authority-reservation`): a surface
climbing to a reserved rank — or `contract`/`policy` knocked off one — fails, and so does a non-core
module attempting to define either reserved surface.

**Enforcement** is mechanical force — how hard a rule bites. Three tiers ([principles §7](../../../principles.md)),
spelled `hard` and `soft` in the built check grammar (a declarable field on every check rule), with
**posture** the honestly-named tier for rules that bite only through being read — recognition, conduct —
never a value a check declares. Every rule declares its tier; posture is never dressed as hard;
the one unbypassable gate is the protected-branch human review, where local hooks only nudge
([principles §6](../../../principles.md), [control-plane](../infrastructure/control-plane.md)).
*Where* a rule bites is the suite split: the `CI` suite is the blocking gate at the merge;
`pre-commit` and `pre-close` are local nudges; `audit-prep` is report-only.

**Collision rule.** Mechanical enforcement never adjudicates authority. When a hard gate blocks
something a higher-authority surface permits, the AI **escalates** — it neither bypasses the gate nor
silently defers the decision. Changing a tier-1 or tier-2 surface to resolve the clash is itself an
escalated, governed act. The runtime behavior is the escalation policy in [policies](../surfaces/policies.md).

### Lifecycle vocabularies

Two vocabularies, assigned by the surface's `lifecycle` field; no per-surface bespoke state machines.

- **decision** (contracts, policies): `proposed → accepted → superseded`. Supersession carries a link and feeds authority resolution.
- **artifact** (every other surface): `active → deprecated → retired`. An instance is born `active` on merge to the protected branch (draftness is a branch state, not a governance state); the `deprecated` state covers managed phase-out and ties to module migrations.

### The self-map

A non-engineer needs a lay of the land. The Engine ships a **generated, committed, fingerprint-gated
map** of its surfaces and systems — never hand-authored (it would drift) and never boot-only (a human
opening the repo could not read it). It is derived from the declarations the Engine already requires
(catalog entries; module `provides`/`wires`; topology placement), so it cannot diverge from *them* —
and that bound is the map's whole warrant: it shows the engine's **declared** structure, so a module
that declares wiring it does not perform renders as truth, and a green drift gate proves the committed
map matches the declarations, never that any part works or is well designed. The shipped map carries
this same warrant in its own header. Both portions are derived as built — the surface table from the
catalog, the module wiring graph from the present manifests — and a hard merge gate (`self-map-drift`)
fails when the committed map no longer matches a regeneration.

The self-map is a [§19](../../../principles.md) **derived-committed artifact**: source-deterministic and
regenerated, so a concurrent-PR merge/rebase conflict on it is **spurious** — resolved solely by regeneration
from the reconciled tree, never a hand-merge and never surfaced to the operator to resolve
([build-orchestration](../lifecycle/build-orchestration.md) regenerates it at `integrate`; an interim
session does so before M1). The **catalog is a source, not a member** — its governance fields are authored
(only its *coverage* is derived), so a catalog conflict is a *real* authored conflict that regeneration would
destroy; it is reconciled by ordinary authored-content review, never regenerate-to-resolve.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| The catalog is the source surface coverage is derived from, **at directory granularity**: a catalogued surface missing the home its `location` names, or an orphan surface directory, is a finding at the merge. | The `catalog-coverage` check (hard tier, `CI` suite) walks each record's `location` against the filesystem on every merge-gated run; a missing home or orphan directory fails the gate. The [knowledge graph](../cognitive/knowledge.md) has its own, separate fidelity gate (`knowledge-coverage`) and is not the coverage mechanism. | engine |
| It stays sized to the **v1 surface set** by locking laws, not the catalog membership — surfaces attach additively without a re-lock. | Observed as built: thirteen surfaces are catalogued at the reconciliation pin, each added by listing a record (the catalog schema states a new surface is added without changing the schema); the `ontology-authority-reservation` check (hard, `CI`) holds the reserved top tiers throughout — partial mechanical support, since no single check asserts additivity itself. | operator |
| GitHub control-plane files (workflows, `CODEOWNERS`, PR/issue templates, `dependabot.yml`) are **infrastructure artifacts** governed by [repository-topology](../infrastructure/repository-topology.md) and [control-plane](../infrastructure/control-plane.md), not surfaces — the amend-first rule covers engine surfaces, not platform files GitHub already shapes. | Structural, as built: the catalog schema's `location` pattern admits only the four surface roots and the coverage gate scans only those roots, so `.github/` can neither be catalogued nor read as an orphan surface. No dedicated check — the exclusion is enforced by the grammar's own shape. | operator |
