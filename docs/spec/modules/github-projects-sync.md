---
status: locked
---

# github-projects-sync

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the What's-next board field adopted by [decision 0328](../../adr/0328-adopt-the-board-s-what-s-next-field-superseding-the-spec-s-b.md) and the two-count description ruled by [decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md), with the manifest's `status` field separated into the distribution, applicability, and activation axes by [decision 0335](../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-07-16 by [decision 0318](../../adr/0318-resolve-re-lock-github-projects-sync-the-board-s-engine-fiel.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The **optional**, adopter-facing **Product Management** module ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)) that
**projects** the repo-authoritative work-control signal onto a **GitHub Project board** for a
non-engineer's at-a-glance visibility ([D-021](../../adr/0021-github-projects-ships-as-an-optional-adopter-facing-module-p.md)). The board is a **one-way,
replaceable projection over committed truth — never the source of truth** ([principles §2](../../principles.md)):
the committed [state](../systems/cognitive/state.md) cursor, the native git/GitHub work record
(branches, pull requests, Issues, Milestones), and the engine-labeled-issue
[debt register](../../reference/glossary.md) stay authoritative; the board is a derivative that can be deleted and
rebuilt. The *laws* it relies on live in the locked
[state](../systems/cognitive/state.md), [attention](../systems/cognitive/attention.md),
[telemetry](../systems/guardrails/telemetry.md), [hooks](../systems/infrastructure/hooks.md),
and [module-system](../systems/grammar/module-system.md) docs; **this module applies them to
the bundle** — it restates none.

It `depends: core` (the universal required root): it reads the `core`-resident cognitive floors
(state + attention ride `core`, [D-086](../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)) and the telemetry-owned debt register
(the core spine), reaching each by a **[§16](../../principles.md) channel relay, not a module edge** —
there is no state/attention/telemetry *package* to depend on. It is a **standalone** optional capability
that fills no [Slot](../../reference/glossary.md) ([D-069](../../adr/0069-core-module-seam-walk-the-demarcation-operationalized-glossa.md)).

## Behavior

### Native-first projection — two layers

The work splits so that the native, server-side layer is GitHub's own and the engine ships only the thin
part GitHub cannot know:

1. **Native GitHub Projects automation carries status transitions** — server-side, **zero engine code**.
   Two built-in workflows, with honestly different defaults. **Status-on-close and Status-on-merge** are
   **enabled by default** (an item's status goes to Done when its Issue/PR closes or merges) and need
   nothing from anyone — but they act only on items *already on the board*. The **auto-add** workflow —
   which pulls matching Issues/PRs onto the board — is **off by default** and can be turned on **only by
   a one-time operator action in the Projects UI**, because GitHub exposes **no API or `gh` command to
   enable a built-in workflow** (only to read its `enabled` state or delete a duplicated one). So the
   engine **never enables auto-add itself**: the setup step *guides* the operator to enable it and
   *verifies* the result by reading the workflow's `enabled` state. This native layer is the engine
   acting as a contributor over a native substrate ([D-038](../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)).
2. **A thin engine layer projects the engine-specific signal** native automation cannot see. The
   projected-signal set is fixed here, not deferred — **five engine-owned fields** as built: the committed
   **state cursor** (where the work is — *what's being built*); the **attention ranking's genuine top
   line, projected under its own *What's next* field** — the ranking's only board presence (the full
   ordering stays the status verb's dashboard; no board field carries it) — adopted by
   [decision 0328](../../adr/0328-adopt-the-board-s-what-s-next-field-superseding-the-spec-s-b.md),
   which supersedes this document's earlier ban on that label (the ban's premise was a "what's next" the
   engine never computes; the attention ranking is that computation, and the field projects its real top
   line, never an invented verdict); **two debt-derived figures** — *needs your review*, fed by the **live**
   open engine-labeled issue count, and *known issues*, fed by the **committed cursor's cached count**
   (the sources differ, and the disclosure below owns what that means); and a **"last synced" freshness
   stamp** (the staleness marker below). It is shipped as a
   sync [tool](../systems/surfaces/tools.md) (engine code under `.engine/tools/`) that reads
   those committed/native sources and writes the board's **engine-owned custom fields** through the
   operator's local `gh`/GraphQL — strictly **read-the-repo / write-the-board**, resolving field- and
   option-IDs at runtime (they are opaque and change on rename). Because a custom-field write targets a
   **project-item node id**, the item must already be on the board: when auto-add is enabled native
   automation places it there; when it is not, the tool **adds — defensively and idempotently
   (`addProjectV2ItemById` returns the existing item if present) — only items that already carry the
   engine label**, applying no label itself (the
   [control-plane](../systems/infrastructure/control-plane.md) owns the label; consumers never
   mutate it). **So by default — auto-add off — this defensive add is what populates the board with
   engine work; enabling auto-add additionally pulls in non-engine matching Issues/PRs** — auto-add is a
   fuller-board convenience, never a hard dependency of the engine signal. If it cannot add or resolve
   an item it **no-ops and discloses**, never errors. The tool writes **only its own custom fields and
   adds only its own already-labeled items — never Status, column, card position, or the placement of
   any existing item**, which native automation and the operator own. The concrete field mapping, paths,
   and `gh`/GraphQL calls are build-spec leaves ([principles §2](../../principles.md)).

### Field ownership — what makes "one-way" honest

A board exists to be touched, so the projection must not punish the operator for using it. Because the
engine writes **only its own custom fields** (and adds only its own already-engine-labeled items, never
touching the placement of any existing item), a human dragging a card — changing **Status, column, or
position** — is **never overwritten**: that gesture survives and is governed by native automation plus
the operator. The engine's own fields are **read-only on the board view where the Projects UI/API
permits**, and where they cannot be locked, a divergence is **surfaced in plain language, never silently
reverted**. The honest, narrow statement the operator is given is: *the engine keeps only its own
"what's being built / what's next / needs your review / known issues / last synced" fields
in step with the real record; your Status, your card moves, and your own board text are yours.*

**One disclosed defect in the two debt figures, kept as intent.** Because *needs your review* reads the
live issue count while *known issues* reads the committed cursor's cache — a cursor that advances only on
explicit refresh, whose own reader calls it the degraded fallback — a stale cursor can put **two
disagreeing debt numbers on the board face with nothing labeling the gap**; the *last synced* stamp marks
when the sync ran, not whether the cursor is current. The intent that the two must never silently disagree
**stands** ([decision 0329](../../adr/0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md));
the reconciling fix — live-first with a stale-labelled fallback, or dating the cached figure on its face —
is the build's, tracked as
[engine-template issue 801](https://github.com/StarshipSuperjam/engine-template/issues/801).

### Manifest shape

| Field | Value |
|---|---|
| `id` | `github-projects-sync` |
| `distribution` | `extension` |
| `applicability` | `detected` (a GitHub Projects board with the native workflow enabled) |
| `activation` | `on-trigger` · `ungated` |
| `provides` | the **sync [tool]** (the engine-field projection, read-repo/write-board); a **setup [operation]** (the ordered `project`-scope grant → board create → board link → **the engine's five fields created** → id resolution, then the operator-guided auto-add **enablement walkthrough** with a read-back verification — never a programmatic enable), with the `operator-typed` setup **[skill]** that invokes it **and its generated Codex mirror**; and a **board-coordinate config [schema]** (a `schema`-surface instance governing the linked project id/number + the field/option-id mapping the setup step writes — the precedent is [audit-library](audit-library.md)'s concern-entry schema). One built gap, kept as intent: the schema file ships on disk but **no manifest declares it and the tool validates inline rather than loading it** — the ownership gap is tracked as [engine-template issue 800](https://github.com/StarshipSuperjam/engine-template/issues/800). The board-coordinate config *data itself* is **per-instance, gitignored runtime state — not a committed `provides` file** (*ship-the-substrate-not-the-data*, [principles §4](../../principles.md)): the schema is the shipped substrate; the board id/field-map is the operator's local state, gitignored like the `mcp` data and the memory ledger and so outside the coherence file-ownership set entirely. Named by what it governs — concrete paths, the field mapping, and the `gh`/GraphQL calls are build-spec leaves. |
| `wires` | **`hook`** (the sync trigger — as built, two `SessionStart` registrations, startup and resume, **plus their two `codex-hook` mirrors**) **and `gitignore`** (the board-config-data line). Each **`hook`** is **non-blocking, best-effort, fail-open-and-flag, and never block-eligible**: a side-effect, never a gate, so it cannot enter the [hooks](../systems/infrastructure/hooks.md) block budget and cannot deadlock an unattended run (the block-satisfiability law binds only *blocking* hooks — and a non-blocking `SessionStart` injector has no `modes` field to declare; it runs in every stance). Each is keyed by its `{event, matcher, type, command}` tuple into `.engine/`, fully reversible — keyed distinctly from `core`'s hooks, the same pattern [memory](memory-substrate-sqlite-fts5.md) uses for its own capture hooks ([D-091](../../adr/0091-flesh-the-memory-substrate-sqlite-fts5-module-doc-to-designe.md)). The **`gitignore`** keys the per-instance board-coordinate config *data* (the operator's local board id/field-map, written by setup) out of version control — so the data never travels with the template and is never a committed engine file, exactly as the gitignored `mcp` data and memory ledger; keyed/reversible like `core`'s gitignore wire. The concrete config path is a build-spec leaf. |
| `depends` | `core` — reads the `core`-resident state + attention floors and the telemetry debt register by §16 channel relay; no edge to any optional/feature module. The deliberate `depends: core` (not `validators-core`) matches [migration-discipline](migration-discipline.md): this module ships no checks on the self-validation corpus. |
| `migrations` | none — it owns no engine store; the board is an external, regenerable projection. |

### Wiring — its own session-start hooks, one gitignore line, no surgery

The `wires: hook` is the module's **own** trigger because **`core` cannot depend on an optional
module**, so the projection cannot ride the locked [close](../systems/lifecycle/close.md) /
[build-orchestration](../systems/lifecycle/build-orchestration.md) flow. The `wires: gitignore`
keys the per-instance board-coordinate config *data* (the operator's local board id/field-map, written by
setup) out of version control — it must not travel with the template, exactly as the `mcp` data and the
memory ledger are gitignored. Nothing else wires: the tool/operation/doc and the board-config **schema**
bind by presence (the schema rides the `schema` surface), so no `ontology-entry`; `gh`/GraphQL needs no
MCP server (no `mcp`) and no committed `permission`. Install is a file drop plus one keyed hook
registration and one keyed gitignore line; uninstall reverses exactly that — the discovery-and-closed-seam
containment story ([R5](../../reference/risks.md)).

### No enforcement — pure projection

Unlike its Software Configuration Management peers
([dependency-discipline](dependency-discipline.md),
[migration-discipline](migration-discipline.md)), this module **gates nothing**: no checks, no
required-status binding, no merge block, no escalation. There is **no enforcement tier** — the board is
**observational**, and the module never dresses a projection as a guardrail
([principles §7](../../principles.md)).

### Setup — a module-owned, non-traveling resource

A GitHub Project (Projects v2) is **owned by a user or org and merely linked to a repo**, so it is **not
template-borne** — generating the repo brings no board. The module ships a **setup step** (its setup
operation, invoked by the operator-typed skill) that runs in a fixed order, each step a
precondition of the next: (1) walk the operator through granting their local `gh` the one-time
**`project` scope** (the engine **cannot self-grant**) — the precondition for everything that follows;
(2) **`gh project create`** the board; (3) **`gh project link`** it to the repo; (4) **create the
engine's five fields** and resolve their opaque ids into the local config; (5) **guide the
operator to enable the auto-add workflow in the Projects UI** and **verify** by reading the workflow's
`enabled` state. The last step is an **operator walkthrough with a read-back check, not an automated action**
— the engine cannot enable a built-in workflow (no API/`gh` command exists). Both the **UI walkthrough
copy and the read-back fail-message** (what the operator is told in plain language when `enabled` is
still false: exactly what to click, and that skipping it only means a **thinner board** — the engine
still projects its own work either way) are **authored as owned content of this setup operation,
held to the [operator-communication law](../../reference/glossary.md) — not a thin, deferrable build-spec leaf**,
because this is the one step the engine hands to the operator and a skimpy guide would strand a
non-engineer. This **reuses
[provisioning](../systems/infrastructure/provisioning.md)'s operator-privileged /
degrade-and-disclose *pattern*** — it is **owned by the module, not a new bootstrap leaf on the locked
provisioning doc** (whose leaf set is closed and foundation-scoped). It handles the org edge case (the
operator may lack org-project permission, or org policy may disable user projects) by
degrade-and-disclose. Because the sync runs through the operator's local `gh`, **no personal access
token is stored as a repository secret** — there is no standing-credential or CI supply-chain surface.

### Degradation — never strand a non-engineer

Every failure path degrades to the git-native truth ([principles §5](../../principles.md),
[fail-open-and-flag](../../reference/glossary.md)):

- **Board absent / deselected, scope ungranted or lapsed, or the Projects API down** → the hook
  no-ops, **never blocking the session boundary**, and surfaces a plain-language next step. The
  authoritative git/GitHub record and the committed state cursor are untouched; losing the board loses
  nothing authoritative.
- **A board-trusting operator must not be misled by a frozen board.** Because a non-engineer may come to
  read the board instead of the Issues, the sync stamps a **"last synced" value — a full UTC date-time
  as built, deliberately not a bare clock time a reader would take for their own timezone** — onto an
  **engine-owned custom field**, which shows **on the engine's own item cards** — board-face, where the
  operator actually looks, and **purely the engine's own field** (no operator-content clobber, no
  read-modify-write race). A timestamp that has gone stale *is* the staleness-on-its-face signal — the
  same discipline as the [audit digest](../../reference/glossary.md)'s run-date — and the actionable "here is the
  one fix" lives in the plain-language boot / degradation disclosure (a frozen board cannot itself carry
  fresh actionable text). There is **no pinned card** (GitHub exposes no pin API) and **no board-README
  write** (rejected — writing operator-shared board metadata risks a last-writer-wins clobber and is not
  the engine's own field).

### Operator trust — informed, never surprised

The operator is a non-engineer, so every cost and consequence is disclosed in plain language
([operator-communication law](../../reference/glossary.md)):

- **The `project`-scope grant carries an informed-consent frame**, not a bare "run this": it states that
  the permission lets the engine read and write **all** of the operator's GitHub Projects (broader than
  this one repo), that it is **optional and revocable**, and the command to revoke it — the same
  informed-consent shape [dependency-discipline](dependency-discipline.md) uses for "this can
  block merges."
- **Install-time disclosure** states what the module gives (progress on a board), what it costs (a
  one-time external board, the `project`-scope grant, **and a one-time manual step in the Projects UI to
  turn on auto-add — which the engine cannot do for them**), that **the engine will place its own work
  items on the board** (so seeing them appear is expected, not a glitch), and that **it controls
  nothing** — so opting in is consent, not a later surprise.
- **The manual-edit contract is stated up front** (field ownership above): the operator's Status and
  card moves are theirs; only the engine's own fields are kept in step.
- **Board labels are plain language** — *what's being built · what's next · needs your
  review · known issues · last synced* — and obey the [§12](../../principles.md) leak guard: maintainer
  vocabulary ("state cursor", "attention prioritization", "projection", "telemetry debt") **never**
  appears on the board face. The *What's next* label carries the attention ranking's genuine top line —
  adopted by [decision 0328](../../adr/0328-adopt-the-board-s-what-s-next-field-superseding-the-spec-s-b.md),
  superseding this document's earlier ban: the ban guarded against a "what's next" the engine never
  computes reading as a verdict, and the built field projects exactly what the engine does compute — the
  top of the same ranking the [status verb](../../reference/glossary.md)'s dashboard surfaces in full
  under its *ranked work* field, so the two operator surfaces stay one story
  ([D-314](../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)). The
  false-belief guard's live demand is unchanged — never project what was not computed.

### The contributor wall holds

The board is an **engine-side visibility projection** of the engine's own work signal, so the
[engine/product wall](../systems/infrastructure/repository-topology.md) and the
[contributor-not-component](../../principles.md) principle hold: the module is **optional**, so opting in
is **consent, not imposed coupling** (§13); it is **read-only outward** — it reads the repo and writes an
external board, never editing product source; and the **removal test passes** — deleting the module
leaves the Issues, pull requests, branches, and the committed state cursor fully intact. On uninstall,
reversing the `hook` and `gitignore` wires and deleting the tool/operation/config-schema/doc (the
gitignored local config *data* goes with the working tree) is a clean file-and-wiring teardown; the
**external board, the engine-added board items, and the granted `gh project` scope dangle as inert,
non-reversible residuals** — the
same accepted residue class as a bare `permission` or an MCP approval ("errs toward leaving it",
[module-system](../systems/grammar/module-system.md)) — and the doc says so rather than
implying a perfectly clean teardown.

### A pure integrator — the §16 deferral seam

The module is a **pure integrator/relay** ([principles §16](../../principles.md)): it projects the
work-control signal that [state](../systems/cognitive/state.md),
[attention](../systems/cognitive/attention.md),
[telemetry](../systems/guardrails/telemetry.md), and the native git/GitHub record **own**. It
owns the **projection mechanism**, not the upstream **detection** — it surfaces what those substrates
hand it and stays silent on which of them exist or what they detect. A new upstream work-signal source
attaches **additively** (the board renders whatever the channel carries), and an owner's later evolution
cannot force a change here. The projection is **additive over native automation — it is never a re-homing
of the session/claim tracking [D-038](../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md) reassigned to native branches and pull
requests**; it adds the engine-specific fields (placing its own work items as needed to carry them) on
top, nothing more.

## Operator and automatic workflow routing

**Current disposition: automatic model route.** When installed, this add-on is reached by the generated
`model-only` setup route `engine-setup-github-projects-sync`. The retired `engine-board-setup` command has
no alias; its upgrade notice names this `engine-setup` section (decision 0336). It carries no operator
command, and no route installs it or grants authority because a trigger matched.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the locked systems'; the delivery is this module** — no restating laws here. | Operator observation: the sync tool reads substrate signals only through the boot/telemetry relays and defines no law text of its own. No merge-gated check asserts the non-duplication. | operator |
| **The board is a projection, never authoritative** — committed state + the native record stay the truth; the board is a deletable, rebuildable derivative ([§2](../../principles.md)). | Operator observation: the tool's only writes target the external board (its GraphQL mutations), never committed state or issues, so removal leaves the record intact. Partial support: in-tool-demo-failure-path (hard, CI) keeps the tool's own self-check falsifiable — the self-check that asserts writes hit only board fields rides the CI unit-test step and never earns `engine`. | operator |
| **Native-first, with honest defaults** — GitHub's built-in automation carries status transitions server-side: Status-on-close/merge are on by default; auto-add is **off by default and operator-enabled in the UI** (the engine guides and verifies via `ProjectV2Workflow.enabled` but cannot enable it — no API exists). By default the engine's own defensive `item-add` populates the board with engine work; auto-add additionally pulls in non-engine items. The engine ships only the thin layer it alone can know — the five engine fields and the defensive `item-add`. | Operator observation: the tool only *reads* the workflow's enabled state and the setup step's copy guides the UI enable; the defensive add filters to already-engine-labeled items and applies no label. The server-side transitions and the UI enable are GitHub's, outside any check's reach. | operator |
| **One-way is honest because field ownership is explicit** — the engine writes only its own fields and adds only its own already-labeled items; the operator's Status, card moves, and own board text are never overwritten. | Operator observation: every field mutation targets an id resolved from the engine's own field map and every added item carries the engine label — the tool's demo self-check asserts exactly this (no write touches Status, only own field and item ids), riding the CI unit-test step. Partial support: in-tool-demo-failure-path (hard, CI) guarantees only that the demo can fail. | operator |
| **No enforcement** — pure projection; the board gates nothing ([§7](../../principles.md)). | Operator observation: the manifest provides no check, and the session-start handler only injects or proceeds — never a block; the hook is not block-eligible. No merge-gated check targets this module's gating absence. | operator |
| **Wires its session-start hooks + one gitignore line** — each hook is best-effort, fail-open, never block-eligible, keyed distinctly (both runtimes' mirrors included); the gitignore keys the per-instance board-config *data* out of version control (the committed substrate is its schema; the data is gitignored like `mcp`/memory data, so no `provides` entry is a non-surface committed file); nothing else wires; `depends` ≠ wiring. | Operator observation: read the manifest's wires — two SessionStart hooks, their Codex mirrors, and the gitignore line — and confirm each hook path injects or proceeds only. Partial support: self-map-drift (hard, CI) holds the rendered wire set true to the manifest. | operator |
| **Module-owned setup of a non-traveling resource** — the board is not template-borne; the module sets it up in the fixed `project`-scope → create → link → fields → operator-guided-auto-add order (with a committed UI walkthrough and read-back fail-message), reusing provisioning's pattern without editing the locked provisioning doc, and stores no PAT secret. | Operator observation: read the setup operation's fixed step order, its informed-consent frame, and the UI walkthrough copy; the sync authenticates through the operator's local `gh`, writing no repository secret, and the provisioning document is unedited. Partial support: operation-shape and operation-frontmatter (both hard, CI) hold the operation structurally valid — its content claims are your read. | operator |
| **Never strands a non-engineer** — every failure degrades to the git-native truth with a plain-language fix, a board-face staleness marker, informed consent for the scope grant, and plain-language labels that honor the [§12](../../principles.md) leak guard. | Operator observation: every not-configured/degraded path returns a plain-language injected message rather than an error, the last-synced stamp carries the staleness signal, the field labels are plain-language constants, and the scope-consent copy rides setup step 1. Partial support: the tool's demo asserts a board error degrades rather than crashes (CI unit-test step); in-tool-demo-failure-path (hard, CI) keeps that demo falsifiable. | operator |
