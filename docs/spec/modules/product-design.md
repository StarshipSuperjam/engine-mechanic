---
status: draft
---

# product-design

*Ratified in the design workspace on 2026-07-11 by [decision 0294](../../adr/0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

## Summary

The operator's **design front door** — the module by which a non-engineer says *what* to build, and the
**producer of the referent** the review lenses later check against. It turns intent into a **committed,
structured, validated spec corpus** with acceptance criteria, decomposes it into a legible **build-plan** and
ordinary product-work Issues, and authors the product's own design documentation. Everything it produces is
**product-owned output**, authored by the Engine as a [contributor, not a component](../../principles.md)
([D-026](../../adr/0026-the-engine-is-an-embedded-team-member-contributor-not-compon.md)): the dependency arrow runs Engine → product only, so removing the module
leaves the product's specs, docs, and Issues standing on their own — the engine validates their **form** while
present; on removal the validation simply stops and the product-owned content stands
([engine/product wall](../systems/infrastructure/repository-topology.md)/[R9](../../reference/risks.md)).

This is the front half of the **design → build → QA axis**. It ships **no review lenses** — those are the
separate [design-review](design-review.md) and [qa-review](qa-review.md) suites, which
review *all* build work and so cannot be gated behind intake. product-design's only ties to them are the
**referent** (the committed `locked` spec's acceptance criteria, which the `product-intent` and
`spec-conformance` lenses consume) and an **optional, advisory** invocation of the design-review quartet at
spec-lock (below) — never a hard dependency in either direction ([D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) separation).

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `product-design` |
| `status` | `optional` |
| `provides` | one intent-shaped [skill](../systems/surfaces/skills.md) (`engine-design`, `operator-typed`); the `product-intake` [operation](../systems/surfaces/operations.md); one operator orientation [doc](../systems/surfaces/docs.md); the **spec-authoring scaffold** (a product-authoring template, **not** a catalogued engine-surface [template](../systems/guardrails/templates.md)); and the **spec [check](../systems/surfaces/check.md) rules** — `presence`/`shape`/`coverage`/`coherence` form checks on the corpus, the **[spec-obligation matrix](../../reference/glossary.md)** — a derived-committed coverage artifact (one row per `locked` criterion, keyed by criterion-cell digest at its `shape`-validated table position) plus the **coverage check** that gates criterion-granular traceability over it — and the **lock-integrity re-acceptance check** (below) |
| `wires` | **none** (file-drop + derived binding; the spec checks join their suites by presence; work Issues + Milestones via native `gh`/`gh api`) |
| `depends` | `core` (the universal required root); **no hard edge to any optional/feature module** — the spec checks are the [migration-discipline](migration-discipline.md) product-targeting precedent (`depends: core`, read-only, not `validators-core`), and the design-review advisory invocation is *consumed-by*, never *depended-on-by* |
| `migrations` | none (v1) |

### One intent-shaped front door

The operator types **`engine-design`** and describes, in plain language, what they want. There is a single
front-door verb — not a family of `engine-design-*` siblings, and **never a menu of framework names**. The
operator does not choose "arc42" or "an ADR" or "a product artifact"; they describe intent, and the engine
**attaches the framework as an internal label** afterward. "Write it down properly" is a branch the front
door *offers* in conversation ("want me to also write this down for a future you?"), not a command the
operator must know to type.

The methodology and artifact *shapes* are kept to the engine's side of the conversation. Every operator-facing
surface this module creates — the front door, the validation readout, the criterion/how-verified cells, the
status it reports, the Milestone names it groups work under — obeys the
[operator-communication law](../../reference/glossary.md) and the locked [`core`](core.md) operator-surface
rule: plain language throughout, with framework and maintainer vocabulary **never surfacing to the operator —
not even as a parenthetical label** (the "(this is called…)" channel was closed at
[D-120](../../adr/0120-lock-core-the-root-module-the-closure-wave-s-terminal-ratifi.md)); the operator describes intent and the engine attaches the framework internally.
The internal names this design doc uses for those surfaces — the `stub → draft → locked` ladder, a criterion's
*engine/CI-internal* verification type, the `re-litigation` / ADR-stream record of a reopened spec — are
engine-side; each renders to the operator in **plain language** ("16 not-yet-described / 2 in progress / 3
settled"; "you can check this yourself" versus "this is on my account"; "I'll note what changed and re-sequence
the work"), never the raw token.

### The spec corpus — committed, structured, validated

The product's current-state specification lives as a **committed `docs/spec/` tree**, the product analogue of
this workspace's own design corpus: a **master/index doc** — the coherence ledger that lists every system with
its status — plus **one conforming doc per capability**, each authored from the engine's **spec-authoring
scaffold** so the thing the AI writes from is the thing the validator checks. This is the move issue #237
asked for ([D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)): a structured, validated spec is the **confidence surface** a
non-engineer can weigh — the validator does the checking the operator cannot — where free prose put the
burden of proof backwards on the operator.

- **Lifecycle `stub → draft → locked`.** A `stub` is a **named-but-undrafted system slot**, not a to-do
  marker. At first engagement the engine **proposes the full stub map** — every obviously-required system as a
  named slot — for the operator to confirm **at the shape level**: the engine shows the set and asks, in plain
  language, "does this look like the right pieces, or am I missing something obvious?" — a yes / "add X" / "you
  decide" answer, not a system-by-system sign-off — *before*
  drafting any single doc, so each capability is drafted with the other systems' seams in mind rather than as
  an island that later costs a refactor — the same "grammar for every feature from the start" logic that
  justifies this workspace. The master/index is the engine's coherence ledger every drafting session reads
  (internally, "3 locked / 2 draft / 16 stub"; the operator's "where are we" readout renders it plainly per the
  front-door law above); adding or dropping a system is a deliberate, recorded act (propagation +
  an ADR-stream rationale), never a silent churn; a remaining stub is a tracked known-incomplete signal, never
  an error.
- **Acceptance criteria as a criterion → how-verified table.** Each criterion is a row — *what must be true* |
  *how it is verified* — and the verification cell is **typed by who can discharge it**: an
  **operator-runnable** check (a screen the operator sees, a behavioral demo the operator runs — the
  [§17](../../principles.md) class that routes around AI judgment) versus an **engine/CI-internal** check the
  operator takes on the engine's account. The **operator-runnable** rows are the source the
  **deployed-environment demonstration harness** runs (and the operator re-runs) — the standing, re-runnable
  behavioral correlate they retire into, the [§17](../../principles.md) leg of the
  [conformance-enforcement floor](../../reference/glossary.md) the QA axis carries against the `locked` spec. The
  operator readout **never collapses the two into one "all
  green"** — it states "N you can verify yourself, M on the engine's account" — so structure cannot
  manufacture confidence the verification does not deliver ([§17](../../principles.md)).
- **Validation is mechanical, form-only.** The engine-cornered [check](../systems/surfaces/check.md)
  rules this module provides inspect the corpus **read-only** — `presence`/`shape` per doc (required sections
  + a well-formed criteria table), `coverage`/`coherence` across the tree (every doc reachable from the index;
  no orphan) — the [migration-discipline](migration-discipline.md) product-targeting precedent
  ([D-129](../../adr/0129-reconcile-dependency-discipline-to-depends-core-l2-the-targe.md)/[D-142](../../adr/0142-lock-migration-discipline-product-migration-governance-the-s.md): a check that inspects product artifacts,
  read-only, the removal test *strengthened*). The operator-facing readout is plain language and **states its
  own bound**: the engine checked that every part is present and well-formed; it did **not** check that the
  design is *right* — that is the operator's call and the review lenses'. Semantic quality and freshness stay
  **unmonitored by design** ([R9](../../reference/risks.md)) — form is checked, correctness is not.

### The lock — operator-governed, with real gravity

A `locked` spec is **settled, don't-churn ground**, the product analogue of a locked design doc here. The
**gate is the operator's recorded acceptance**, earned on **validation green** plus — *when
[design-review](design-review.md) is installed* — the **four lenses advising on the spec** (the
product analogue of the cold-session design audit). The lenses **advise; they never gate**: their findings
are evidence the operator weighs; the **engine never *vetoes* what the product may become** (it validates form
and advises on content; the operator governs it — the
[wall](../systems/infrastructure/repository-topology.md) re-scope, [D-244](../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)).
product-design therefore takes **no hard `depends` edge** to design-review — absent the suite a spec locks on
validation + the operator's acceptance alone — and its **spec-lock ceremony is recorded as the second,
advisory consumer of the four plan-review personas** (build-orchestration's plan-review gate being the first),
so the consumed-by record is symmetric across both docs and no installed lens dangles. **Only a `locked` spec
drives a build.**

The lock's **weight is reproduced through native surfaces**, retiring only this workspace's bespoke
`lock.py`/`locks.yaml` hand-tooling: the **boot-grounding don't-churn norm** every product session reads
("adapt to locked specs; never change one to fit current work"); the **lock-integrity re-acceptance check**
this module provides — a CI-gated check that **diffs the PR base against head** over docs that were `locked`
at base (read from the **base** commit's `status`, not head's; the base commit is the prior-state correlate,
immutable where force-push is blocked — [control-plane](../systems/infrastructure/control-plane.md)
— so it cannot be edited in the same commit as the body) and, on a changed `locked` body, requires the
operator's **[§15](../../principles.md)-style acknowledgment** — an action on the PR (a checkbox or an applied
label), **never an AI-writable committed field** — so no session supplies the body change and the
re-acceptance in one stroke. It **rides the single ruleset-bound PR-validation check** (adding no new
required-check name) and so **self-removes from the derived roster on engine removal**
([validation](../systems/guardrails/validation.md) / [migration-discipline](migration-discipline.md)
precedent), never an orphaned required check that would deadlock the product's merges — so a `locked` spec's
body cannot change without a recorded re-acceptance, or the required check fails the merge; and **alarmed,
operator-approved re-litigation** whose rationale is written to the product **ADR stream**. **Rigor is uniform; ceremony is proportionate** — a small single-doc
spec locks light (validation + the operator's acceptance), a real product earns the fuller review — but any
`locked` spec is settled ground with teeth, and re-opening one pre-build is a light, scoped act, never the
full ceremony in reverse.

### What it produces — product-owned, product-side of the wall

The Engine authors these as a contributor; they live in the product's own tree and carry no engine namespace,
so the [engine/product wall](../systems/infrastructure/repository-topology.md) holds (the authoring
scaffold and the form checks are engine-cornered; the outputs are the product's):

| Artifact | Home | Note |
|---|---|---|
| Spec corpus + acceptance criteria | committed **`docs/spec/`** tree (master/index + per-capability docs) | product-owned; template-shaped, validated; `stub → draft → locked` |
| Build-plan | committed **`docs/spec/`** (the build-plan doc) | product-owned; **living** (re-sequences as work lands), validated for structure, no lock gravity |
| Product principles | product doc tree (e.g. `docs/principles.md`) | product-owned |
| arc42 architecture doc | `docs/architecture.md` (or `docs/arc42/`) | product-owned |
| C4 diagrams | mermaid in the arc42 doc, in stable `flowchart` form | product-owned |
| ADR stream | `docs/adr/NNNN-*.md` — the **product's own** numbering, never the engine's `eADR-####`; carries **presence-validated anti-choices** (rejected options + why) | product-owned |
| Diátaxis tree | `docs/{tutorials,how-to,reference,explanation}/` | product-owned |
| Work Issues | native GitHub **Issues** — ordinary product backlog | **un-labeled** (no engine-domain label); pointers, not the spec (below) |
| Milestones | native GitHub **Milestones** | the legible build map; **[build-orchestration](../systems/lifecycle/build-orchestration.md) emits them** from the build-plan |

The spec and build-plan are committed files (no engine label); the work Issues and Milestones are emitted via
native `gh`/`gh api`. When [github-projects-sync](github-projects-sync.md) is present it *enriches*
the result (a board projection over the native Milestones); it is never a hard dependency, so the front door
works without it.

### The flow, and how it degrades

`engine-design` runs in Explore (it reads, reasons, authors committed files, and logs Issues). It:

1. **pre-checks `gh`** and, on failure, states the one concrete next action in plain language — and persists
   the intent already typed as a committed file, so nothing is lost;
2. on first engagement, **proposes the stub map** for the operator to confirm at the shape level, then elicits
   intent with an **operator-controlled depth choice that names its consequence** — *how much product*, not
   *whether structure* (a short conforming spec versus a full one), defaulting low;
3. **authors the spec doc(s)** from the scaffold into `docs/spec/`, with acceptance criteria as the
   criterion → how-verified table; **validation runs** (form checks) and the result is reported in plain
   language with its bound stated — the early, cheap signal that replaces a late surprise at QA;
4. **the operator accepts and `locks`** the spec — validation green + (advisory lenses when installed) + the
   operator's recorded acceptance; the engine **tells the operator where the spec lives and how to reopen it**;
5. **decomposes the `locked` spec** into a committed **build-plan** (ordered phases) and **ordinary
   un-labeled work Issues** referencing their spec docs, which [build-orchestration](../systems/lifecycle/build-orchestration.md)
   groups under native **Milestones**. "Build this Issue" is the deliberate act that enters Build.

Every step lands as committed files or native Issues, so a missing substrate or board degrades to `gh`-only
and the operator is told so ([fail-open-and-flag](../../reference/glossary.md)) rather than stranded
([degrade-to-git-native](../../principles.md)). A truly trivial change can skip the front door entirely and
build from a plain Issue — the two referent lenses then disclose a no-op, never a silent green.

### Issues are pointers; the spec is un-skippable

A work Issue is a **pointer**, not a substitute for the spec. It makes work legible to the operator (the
human-readable scope grouped under a Milestone) and references its spec doc + the criteria rows it realizes —
but for the **build session the committed `locked` spec is the single authoritative source**, so a confident
but lossy Issue can never become a second source that lets a session skip the spec's nuance. The spec is
**un-skippable** because the **design → build → QA axis carries the
[conformance-enforcement floor](../../reference/glossary.md)** against the product's own `locked` spec — the same
rigor that built the Engine (build-conformance), re-homed to the deployed
product build — never a mechanical block on an agentic verdict
([validation](../systems/guardrails/validation.md): "a persona judges, a check gates"). Ownership
holds the [D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) separation: **this module owns the coverage leg and produces the
referent**; [qa-review](qa-review.md) owns the judgment and demonstration legs (consumed-by, the
existing referent tie, never a hard `depends`); [build-orchestration](../systems/lifecycle/build-orchestration.md)
runs them at the merge. The three mechanisms deepen the persona-judges / check-gates split:

- the **[spec-obligation matrix](../../reference/glossary.md)** this module provides — a durable coverage record,
  **one row per `locked` acceptance-criterion**, built the
  [knowledge-graph](../systems/cognitive/knowledge.md) way
  ([§3](../../principles.md)/[§19](../../principles.md)) as a **derived-committed artifact plus a coverage
  check over it**, never criteria enumerated inside a check callable. Because the `docs/spec/` criteria
  table is a `shape`-validated structured surface, each row keys to its **criterion-cell digest at its
  validated table position**, so a spec edit stale-flags *exactly* the rows whose criterion changed and a
  continuous reverse sweep carries the not-yet-built remainder across sessions (the pin is content-derived,
  not a stable semantic identity — a reworded criterion re-opens for re-confirmation). Those derived,
  source-pinned rows *are* the criterion-ID scheme that lets coverage trace at **criterion granularity** —
  every `locked` criterion traced to committed work, not merely every capability scheduled — without
  hand-authoring forbidden structure. **Lock is per-doc**: `status: locked` is read from the base commit
  (the lock-integrity mechanic below), so *every* criterion of a `locked` doc is a row and a `draft`/`stub`
  doc contributes none. Read-only, migration-discipline-shaped, self-removing on engine removal — the
  always-present mechanical leg (it gates on `depends: core` alone);
- the **paired judgment lenses** ([qa-review](qa-review.md)) judged vs the `locked` spec —
  **`spec-conformance`**, the systematic reviewer that marks each obligation met, diverged, or untested, and
  its adversarial counterpart **`divergence-hunter`** (default-to-divergent —
  build-conformance §8), a second decorrelated cold context run against the
  same `locked` rows so a semantic misbuild that passes its own tests is *hunted*, not charitably explained
  away; both **re-derive each obligation from the `docs/spec/` span itself, never from the matrix rows** (the
  matrix is the denominator, never the lens's checklist — the [R16](../../reference/risks.md) honest tier), and
  **judge only criteria whose row is `locked`**, so a PR touching an adjacent `draft`/`stub` capability draws
  the disclosed no-op for those; their gaps surfaced and dispositioned at the operator's merge;
- the **deployed-environment demonstration harness** — [qa-review](qa-review.md)'s disclosed
  dry-run over the `locked` spec's **operator-runnable** how-verified rows (this module authors them;
  re-runnable because those rows are committed spec content, not a new standing artifact), the standing
  behavioral correlate they retire into (the [§17](../../principles.md) evidence that routes around AI), so a
  criterion asserting a behavior is backed by a demonstration the operator can watch, not an AI verdict
  alone.

The judgment and demonstration legs ride qa-review's optional install (the design's as-installed model — a
deployed repo without qa-review still gets the mechanical matrix leg, disclosed); all three bite **only
against a `locked` `docs/spec/`**: with none locked the floor is the [disclosed no-op](../../reference/glossary.md),
never a silent green and never a block on the unspecced or MVP scope the operator deliberately leaves open
([§20](../../principles.md)) — rendered in the honest two tiers, never one "all green".

### Anti-churn and build-readiness

- **Anti-choices are captured and validated.** Significant what/why decisions — and the options rejected, with
  the reason — land in the product **ADR stream**, with a presence check on the rejected-options section, so a
  later session does not re-propose ground already settled (the anti-churn value behind the lock).
- **Re-litigation propagates.** Re-opening a `locked` spec reconciles the build-plan, its Milestones, the open
  work Issues, and any dependent specs; the coverage/coherence checks catch *orphans* mechanically, and the
  [spec-obligation matrix](../../reference/glossary.md) **stale-flags exactly the rows whose `docs/spec/` span changed**
  (the fingerprint mechanic — the *coverage* side of staleness is mechanically surfaced); the residual
  **semantic** staleness (does the built work still match the changed criterion's *meaning*?) stays the
  `spec-conformance` judgment, named honestly rather than dressed as mechanically caught
  ([§7](../../principles.md)).
- **Build-readiness.** Before a Milestone's work starts, the engine confirms the spec is complete enough to
  build that phase — the product analogue of this workspace's pre-build dry-run.

### Depth and anti-sprawl

Depth is **proportionate, never mandatory**: a small capability is a short conforming spec doc that locks
light; a long-lived product earns the full arc42 + C4 + ADR + Diátaxis treatment, incrementally — but rigor
(structure + validation) is uniform, only *ceremony* scales. `product-intake` is the one standalone operation;
the per-framework authoring procedures are branches within it, promoted to their own operations only if one
earns the ≥2-referencer bar ([D-042](../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)). A single model-invocable skill slot is **not**
authored on spec — the front door is operator-typed unless a later pass clears the
[skills](../systems/surfaces/skills.md) earns-a-skill bar.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The referent producer, not the lens roster** — product-design authors the spec; the [design-review](design-review.md) / [qa-review](qa-review.md) suites review build work and do not depend on it. The design-review advisory invocation at spec-lock is *consumed-by*, not a hard edge, so the [D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) separation holds both ways. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Structure is the confidence surface** — a committed, validated spec corpus is what a non-engineer can weigh; the validator does the checking the operator cannot, and states its own bound (form, not correctness). | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **Operator-governed lock with real gravity** — the operator's acceptance gates the lock; the engine advises and never vetoes; the weight is the don't-churn norm + the CI re-acceptance teeth + the ADR-recorded re-litigation, native surfaces, not bespoke tooling. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **Product-owned outputs, engine-cornered machinery** — the wall holds because the engine contributes the artifacts and validates their *form* read-only; it never annexes the product's doc tree, and removal leaves the product standing. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Issues are pointers; the spec is authoritative and un-skippable** — work Issues are un-labeled backlog that point at the committed `locked` spec; the **[conformance-enforcement floor](../../reference/glossary.md)** the design → build → QA axis carries against a `locked` `docs/spec/` — the criterion-granular [spec-obligation matrix](../../reference/glossary.md) this module provides, plus qa-review's adversarial `spec-conformance` judgment and the deployed-environment demonstration harness — keeps the spec un-skippable at the merge, and bites only on what the operator locked (never a block on MVP scope, §20). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **One plain-language front door** — intent in, framework labels attached internally; no vocabulary the operator must learn, on any surface this module creates. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Proportionate** — rigor is uniform, ceremony scales with stakes; nothing forces the heavy path on small work, and a trivial change can skip the door entirely. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Native and degradable** — committed files + `gh`/`gh api`; every step survives a substrate outage. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
