---
status: draft
---

# code-intelligence-core

*Forward-designed 2026-08-02 under the delivery-plane program ([decision 0334](../../adr/0334-adopt-the-delivery-plane-spec-program-module-map-wave-order.md)),
through the plan-acceptance route [decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md)
establishes. Intended design, not yet built; enters in progress and settles only by the operator's
recorded acceptance before wave 1's build begins.*

## Summary

The **optional** module that lets a deployed engine **understand the product's code before changing it**:
finding where a behavior lives (localization), what a symbol touches and what touches it (relationships and
impact), and binding every such claim to the exact revision it was read from — so a change lands where the
defect actually is, not where a text search guessed. It is a **contract over replaceable adapters**: one
pinned language-server adapter (Python first) plus lexical, syntax-tree, and history evidence, combined into
a **localization dossier** — ranked, falsifiable leads with the queries and exclusions that produced them,
never a causal verdict. Languages it does not support are named plainly per run; it never fakes coverage.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `code-intelligence-core` |
| `status` | `optional` |
| `provides` | the **[schemas](../systems/surfaces/schemas.md)** (`localization-dossier.v1` — leads, evidence mode per lead, queries run, exclusions, unsupported-surface disclosure; `impact-set.v1` — symbols/files affected by a proposed change, with derivation lane); the **[tools](../systems/surfaces/tools.md)** (`code_intel.py` — orient/localize/impact subcommands; the adapter host that pins and drives one language server per profile); the adapter **contract [schema](../systems/surfaces/schemas.md)** (`code-intel-adapter.v1` — capabilities a language adapter declares: definitions, references, symbols, diagnostics; every capability optional and disclosed); the **[operation](../systems/surfaces/operations.md)** runbook (how a session orients in a product repo and produces a dossier); a hard **[check](../systems/surfaces/check.md)** (dossier schema conformance); and the operator **[doc](../systems/surfaces/docs.md)** |
| `wires` | **none** |
| `depends` | `core`, `delivery-core` (dossiers attach to runs and bind to task revisions) |
| `migrations` | none |

### The intelligence model

- **Revision-bound, or refused.** Every dossier and impact set names the commit it was derived from. A
  query against a tree that moved since derivation returns `stale` — the reader re-derives; nothing answers
  from a cached map whose identity is a timestamp. Content identity, never modification time.
- **Evidence modes stay separate.** A lead says *how* it was found — lexical match, symbol relation,
  syntax-tree structure, change history — and what was searched but excluded. Modes corroborate; they are
  never summed into one opaque score. A dossier is a set of falsifiable leads: the change built on it must
  still prove itself by reproduction and tests (delivery-evidence's job, not this module's).
- **Adapters declare, the contract discloses.** A language adapter (the pinned Python language server
  first) declares which capabilities it actually provides; the dossier records which were available,
  which timed out, and which were unsupported. Partial, timed-out, or indexing-in-progress results are
  typed degraded states — absence of reported findings is never read as "no findings".
- **Unsupported is a first-class answer.** A repository (or file) in a language no installed adapter
  covers gets lexical/history evidence only, and the dossier says so in its disclosure block. No parity
  claim is ever implied by silence.
- **Impact before mutation.** structured-change consumes the impact set as its preflight input: what a
  pending change set is expected to touch, compared after apply against what it did touch. The seam is the
  schema; neither module reaches into the other's internals.

### Adjacent surfaces it must not absorb

engine-template's **code-notes** (durable facts recorded as code comments, judged by review lenses) remain
review-owned prose — this module derives structure, it never treats a comment as authority. The engine's
own **knowledge graph** maps engine surfaces; this module reads *product* code and keeps no persistent
graph at all in wave 1 — a derived product structural map is [product-knowledge-graph](product-knowledge-graph.md)'s
later ground, fed by this module's adapters, not duplicated here.

### Degraded behavior

No adapter installed → lexical/history-only dossiers, disclosed. Adapter crash or timeout → typed degraded
lead states, disclosed, never silently dropped. Both runtimes drive the same adapter host tool; no
runtime-private index exists.

### What stays out

- **No persistent index or graph store** in this module; derivation is per-run, cache lifetime bounded by
  revision identity.
- **No repository content leaves the machine** — adapters are local processes; nothing uploads source for
  indexing.
- **No correctness verdicts.** A dossier locates; it never certifies a cause or approves a change.

## Acceptance criteria

*`engine` means a named merge-gated check fully asserts the criterion; `operator` means your observation
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Dossiers validate and disclose** — every dossier conforms to schema and carries queries, exclusions, per-lead evidence mode, and the unsupported/degraded disclosure block. | Schema check rides CI (hard); disclosure completeness by operator read of staged dossiers. | operator |
| **Revision binding bites** — a dossier read against a moved tree answers `stale`, never serves cached leads as current. | Fixture: derive, commit an unrelated change, re-read; output inspected. | operator |
| **Wrong localization is catchable** — a staged defect whose lexical match points at the wrong file is corrected by symbol/structure evidence in the same dossier, and the dossier shows both leads with their modes. | Fixture: the seeded misdirection scenario; dossier inspected. | operator |
| **Degraded states are typed** — adapter timeout and unsupported language produce disclosed degraded leads, not silent absence. | Fixture: adapter killed mid-run; a repo in an uncovered language; dossiers inspected. | operator |
| **Local-only derivation** — no network egress occurs during orient/localize/impact runs. | Fixture: run under egress observation; any outbound call fails the fixture. | operator |
| **Impact seam holds** — structured-change consumes an impact set by schema alone; a schema-invalid impact set is refused, not guessed at. | Fixture: staged invalid impact set handed across the seam; refusal inspected. | operator |
