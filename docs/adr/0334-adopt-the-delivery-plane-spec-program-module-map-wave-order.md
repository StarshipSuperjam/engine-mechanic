---
status: accepted
engine_record: true
---

# Adopt the delivery-plane spec program: module map, wave order, and program rules

*Decided 2026-08-02 in this repository, by the operator, through the plan-acceptance route
[decision 0327](0327-route-product-spec-authoring-through-plan-acceptance-into-b.md) establishes — the
first program-scale forward design since the corpus settled
([decision 0331](0331-settle-the-reconciled-corpus-as-the-build-baseline.md)). Rides the pull request
that authors the program's capability documents.*

## The decision

**engine-template gains a delivery plane** — the modules through which a deployed engine understands a
product's code, changes it coherently, proves the change behaves, runs it in reproducible environments,
deploys it without holding credentials, and operates it after release. The engine's existing governance
surfaces (consent at the merge, Explore/Build separation, evidence at review, protected-branch gate)
remain the control plane every delivery module answers to; no delivery module ships its own consent
mechanism or bypasses the merge gate.

The whole program is **specified now, built later**: every module below receives a full forward-designed
capability document in `docs/spec/modules/`, authored in one pull request, entering the corpus as **in
progress** (frontmatter `draft`). Nothing settles at authoring. A wave's documents settle by the
operator's recorded acceptance **before that wave's build begins** — the settle gate that keeps a draft
from quietly becoming build ground, and keeps the drafted corpus from rotting unowned: each wave's build
entry forces its settle decision.

### The module map

Waves order the builds by real dependency; the wave number is sequence, not calendar. Every module is
**`optional`** in the module grammar — the delivery plane is something a deployment adds, never a new
burden on every deployment — and every delivery module depends (directly or through its wave's spine) on
`delivery-core`, so the kernel's contracts are singular.

| Wave | Module | Responsibility (one line; the document owns the detail) |
| --- | --- | --- |
| 1 | delivery-core | Task and run identity, lifecycle, authority, budgets, stop conditions, typed outcomes, run receipts — the kernel every delivery module binds to |
| 1 | delivery-evidence | Behavioral evidence, effect receipts, evidence freshness and invalidation, final-snapshot divergence records, typed reconciliation outcomes |
| 1 | code-intelligence-core | Product-code discovery, localization, symbol relationships, revision binding, impact analysis, explicit unsupported-language behavior |
| 1 | structured-change | Versioned pending change sets, atomic apply, semantic preflight, rollback, Git linkage, evidence invalidation on mutation |
| 1 | engineering-quality | The stack-declared quality contract: formatter, linter, types, build, tests, dependency checks; fast-loop vs clean-environment evidence; autofix authority — the family contract its per-stack profiles realize |
| 1 | engineering-quality-python | The first profile realizing the engineering-quality contract, for Python/backend stacks |
| 2 | execution-environment | Desired/observed environment state, leases, services, data seeds, limits, checkpoints, cleanup reconciliation — and the backend adapter contract |
| 2 | runtime-backend-local-container | The first backend realizing execution-environment's adapter contract: local containers |
| 3 | engineering-quality-typescript | The TypeScript/web profile of the engineering-quality contract |
| 3 | platform-web | Web platform delivery: dev server, build artifact, rendered-workflow conventions for web products |
| 3 | browser-evidence | Rendered-behavior evidence: semantic browser actions, DOM/console/network/visual evidence, page identity and postconditions |
| 3 | debugger-diagnosis | Hypothesis-scoped runtime diagnosis through a debug adapter; typed required-evidence states |
| 4 | authority-broker-contract | Provider-neutral workload identity and typed, expiring operational grants — the contract; provider connections stay optional |
| 4 | credential-broker | The broker family contract: credential custody outside the worker, fail-closed enforcement, no raw-export route; provider adapters get their own documents when a provider is chosen |
| 4 | deployment-core | Immutable artifact and target identity, typed deployment effects, health verification, rollback, drift reconciliation — the deployment contract |
| 4 | deployment-adapter | The adapter family contract for concrete deployment providers; first target is one disposable non-production provider |
| 5 | operations-core | Deployed-state identity, health, incident state, repair routing, and the maintenance due-state model |
| 5 | maintenance-ledger | The durable schedule ledger: due slots, leases, catch-up rules, attempt history, missed/duplicate states |
| 5 | bounded-repair | Deterministic-first, budgeted repair with independent progress measurement; draft-PR-only output, never autonomous merge |
| 6 | large-change-coordination | Dependency-linked slices for long refactors: ownership, overlap, invalidation, integration checkpoints, partial rollback |
| 6 | profile-registry | The platform-profile contract registry: how platform-* profiles declare build, package, sign, test, serve, distribute, observe |
| 6 | platform-ios | The iOS consumer-product profile realizing the profile-registry contract |
| 7 | operator-cockpit | One derived, rebuildable operator view over intent, work, environment, evidence, deployed state, and pending decisions — never a second source of truth |
| 7 | product-knowledge-graph | Derived, revision-bound structural map of the product a deployed engine builds — distinct from the engine's self-map |
| 7 | evidence-explorer | Navigation over the evidence record itself: from claim to receipt to raw source |
| 7 | research-and-learning | Repository-native research evidence, feedback intake, and intent–reality reconciliation — after delivery capability exists |

Boundary cuts the map fixes now, so no two documents claim the same ground:

- **operations-core vs maintenance-ledger:** operations-core owns the *states* (what is deployed, what
  is healthy, what is due, what is broken, where a repair routes); maintenance-ledger owns the *durable
  schedule record* (slots, leases, catch-up, attempt lineage). The ledger records; operations decides.
- **The wave-7 views:** operator-cockpit is the composed operator surface; product-knowledge-graph is a
  derived data source about the product's structure; evidence-explorer is navigation over evidence
  records. The cockpit may consume both; neither of the other two renders an operator surface of its own.
- **Family documents:** `credential-broker` and `deployment-adapter` are family-contract documents; a
  concrete provider adapter gets its own document only when a provider is chosen, by a recorded
  decision. `runtime-backend-local-container` is concrete now; the backend contract it realizes lives in
  execution-environment. **Choosing those providers is part of wave 4's settle gate**: wave 4 ships at
  least one working credential broker and one working deployment adapter alongside the contracts (the
  wave-2 pattern, where the environment contract arrived with its local-container backend), so the wave's
  release adds a working path, never contract grammar alone.
- **deployment-core vs operations-core on drift:** deployment-core owns effect-time reconciliation and
  the drift-record grammar; standing, periodic drift observation of an already-deployed product is
  operations-core's ground, consuming that grammar.
- **Toolchain installation:** execution-environment owns installing and materializing product toolchains
  and confining install-time code execution; an engineering-quality profile *declares* its requirements
  (pins, frozen modes, per-dependency script allowances) as manifest input — the profile never installs.

### Program rules

- **No benchmark-gated adoption.** No module's specification, build, or acceptance is conditioned on
  benchmark evidence — nothing is refused because a mountain of evidence does not yet exist. External
  corpora, datasets, reference products, and engine-owned verification fixtures all remain available as
  prudent design and acceptance instruments where a document judges them merited; what none of them may
  be is a gate on whether to specify or build.
- **Specs stand alone.** The research material that informed this program is authoring input, not
  reference: no capability document cites it, and each document must be fully readable by someone with
  no access to it. That is the check an operator or reviewer applies.
- **Draft, then settle at the gate.** Every document enters in progress. Settling is the operator's
  recorded acceptance, taken per wave before that wave's build starts, at the review depth the operator
  chooses then.
- **Security surfaces settle thorough.** delivery-core (it coins the plane's authority vocabulary),
  engineering-quality-python and engineering-quality-typescript (their build/test kinds execute product
  code — the TypeScript profile's install layer more so), debugger-diagnosis (it executes product code
  and captures live memory), bounded-repair (it mutates product code unattended),
  authority-broker-contract, credential-broker, execution-environment, browser-evidence,
  deployment-core, deployment-adapter, platform-ios (vendor signing credentials flow there first, and
  store distribution is production-class), product-knowledge-graph (it derives an index from
  possibly-untrusted product content), and research-and-learning (the plane's one external-web intake)
  take the engine's full pre-settle design review when their settle comes — their failure modes
  (credential exposure, authority escape, code execution, untrusted content) are not observable
  casually.
- **clean-code retires.** The engineering-quality family absorbs the territory the `clean-code` stub
  reserved; the stub document and its index row are removed with this record as the trace.
  (engine-template issue #232, which the stub anticipated, is re-aimed at the engineering-quality
  build when that wave's work is filed.)
- **Milestones:** wave 1 targets engine-template's existing "Local delivery core" release milestone
  (R5); waves 2–7 have engine-template milestones R8–R13, one per wave in order. Each wave's milestone
  holds one placeholder issue outlining the wave until its descriptions settle and the build breaks out
  into individual issues there.

## Why

The operator reviewed a comparative product study and a proposed roadmap against the engine as built and
concluded the delivery plane is the product's next capability ground: the governance control plane is
mature, and no built or backlogged module owns code intelligence, structured mutation, product
environments, deployment, or operations. Specifying the whole program now — rather than module by module
as each build nears — was the operator's explicit call: it puts the full boundary map in one reviewable
place, lets every contract be drawn with its consumers visible, and leaves later corrections cheap while
everything is still draft. One pull request carries it because the corpus's own merge checks require an
index row's document to exist: partial authoring would either dangle rows or stub the map into
meaninglessness.

## What we ruled out

**Specifying on engine-template itself** (rejected — this repository is the product's design record;
engine-template holds no spec of itself, and splitting the corpus would break the settled baseline's
single home). **A seven-pull-request wave sequence** (rejected — index and build-order rows for absent
documents fail the corpus's hard dangling-link checks, and follow-on branches could not resolve this
record until merge; only a stacked merge train would work, a topology the engine's flow does not
assume). **Settling wave 1 at authoring** (rejected — information about whether the kernel's boundaries
are right flows backward from its consumers; the corpus precedent enters forward designs as drafts, and
locking five coupled contracts cold would make every later correction a gated reopen). **Making the
delivery substrate `required`** (rejected — the source material's "required substrate" meant required
within the delivery plane; making the kernel mandatory in every deployment would force the plane on
projects that never asked for it). **Embedding the quality contract in the Python profile** (rejected —
the shared contract would lock inside the first language and every later profile would conform to a
contract never stressed beyond it; the family-contract-plus-profiles shape mirrors
authority-broker-contract and profile-registry). **Benchmark-gated adoption criteria** (rejected by the
operator's standing ruling — evidence thresholds as adoption gates stall building; verification stays,
gating goes). **Keeping the clean-code stub as a pointer** (rejected — a permanent tombstone row in a
settled index buys nothing over this record plus git history).
