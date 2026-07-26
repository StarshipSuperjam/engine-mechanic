---
status: draft
---

# github-projects-sync

*Ratified in the design workspace on 2026-07-16 by [decision 0318](../../adr/0318-resolve-re-lock-github-projects-sync-the-board-s-engine-fiel.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

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
   projected-signal set is fixed here, not deferred: the committed **state cursor** (where the work is),
   **attention** prioritization/ordering (**ranked work** — the in-flight work and open engine-labeled
   debt attention orders; *not* "what's next", which is the plan's to answer and is no part of this
   projection, [D-314](../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)), the **debt count** (open engine-labeled
   issues), and a **"last synced" freshness stamp** (the staleness marker below). It is shipped as a
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
"what's being built / ranked work / known issues / last synced" fields in step with the real record;
your Status, your card moves, and your own board text are yours.*

### Manifest shape

| Field | Value |
|---|---|
| `id` | `github-projects-sync` |
| `status` | `optional` |
| `provides` | the **sync [tool]** (the engine-field projection, read-repo/write-board); a **setup [operation]** (the ordered `project`-scope grant → board create → board link, then the operator-guided auto-add **enablement walkthrough** with a read-back verification — never a programmatic enable), with an optional `operator-typed` setup **[skill]** that invokes it; a **board-coordinate config [schema]** (a `schema`-surface instance governing the linked project id/number + the field/option-id mapping the setup step writes — the precedent is [audit-library](audit-library.md)'s concern-entry schema); optionally one operator orientation **[doc]**. The board-coordinate config *data itself* is **per-instance, gitignored runtime state — not a committed `provides` file** (*ship-the-substrate-not-the-data*, [principles §4](../../principles.md)): the schema is the shipped substrate; the board id/field-map is the operator's local state, gitignored like the `mcp` data and the memory ledger and so outside the coherence file-ownership set entirely. Named by what it governs — concrete paths, the field mapping, and the `gh`/GraphQL calls are build-spec leaves. |
| `wires` | **`hook`** (the sync trigger) **and `gitignore`** (the board-config-data line). The **`hook`** is **non-blocking, best-effort, fail-open-and-flag, and never block-eligible**: a side-effect, never a gate, so it cannot enter the [hooks](../systems/infrastructure/hooks.md) block budget and cannot deadlock an unattended run (the block-satisfiability law binds only *blocking* `Stop` hooks). It **declares its active modes** per the hooks mode-awareness law, and is keyed by its `{event, matcher, type, command}` tuple into `.engine/`, fully reversible — keyed distinctly from `core`'s hooks, the same pattern [memory](memory-substrate-sqlite-fts5.md) uses for its own capture hooks ([D-091](../../adr/0091-flesh-the-memory-substrate-sqlite-fts5-module-doc-to-designe.md)). The concrete event(s) and debounce cadence are build-spec leaves. The **`gitignore`** keys the per-instance board-coordinate config *data* (the operator's local board id/field-map, written by setup) out of version control — so the data never travels with the template and is never a committed engine file, exactly as the gitignored `mcp` data and memory ledger; keyed/reversible like `core`'s gitignore wire. The concrete config path is a build-spec leaf. |
| `depends` | `core` — reads the `core`-resident state + attention floors and the telemetry debt register by §16 channel relay; no edge to any optional/feature module. The deliberate `depends: core` (not `validators-core`) matches [migration-discipline](migration-discipline.md): this module ships no checks on the self-validation corpus. |
| `migrations` | none (v1) — it owns no engine store; the board is an external, regenerable projection. |

### Wiring — one hook, one gitignore line, no surgery

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
operation, optionally invoked by the operator-typed skill) that runs in a fixed order, each step a
precondition of the next: (1) walk the operator through granting their local `gh` the one-time
**`project` scope** (the engine **cannot self-grant**) — the precondition for everything that follows;
(2) **`gh project create`** the board; (3) **`gh project link`** it to the repo; (4) **guide the
operator to enable the auto-add workflow in the Projects UI** and **verify** by reading the workflow's
`enabled` state. Step (4) is an **operator walkthrough with a read-back check, not an automated action**
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
  read the board instead of the Issues, the sync stamps a **"last synced HH:MM"** value onto an
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
- **Board labels are plain language** — *what's being built · ranked work · needs your review · known
  issues* — and obey the [§12](../../principles.md) leak guard: maintainer vocabulary ("state cursor",
  "attention prioritization", "projection", "telemetry debt") **never** appears on the board face. The
  ranked field is **not** labelled *"what's next"*: the board carries the operator's own un-labeled
  Issues whenever auto-add is on, and a "what's next" the engine never computes for them would read as a
  verdict that their backlog was ranked below rather than never ranked at all — the false belief
  [§7](../../principles.md)/[§17](../../principles.md) forbid. The label matches the
  [status verb](../../reference/glossary.md)'s dashboard field of the same name, so the two operator surfaces say
  one thing ([D-314](../../adr/0314-litigate-engine-template-394-attention-s-work-record-commiss.md)).

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

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The laws are the locked systems'; the delivery is this module** — no restating laws here. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **The board is a projection, never authoritative** — committed state + the native record stay the truth; the board is a deletable, rebuildable derivative ([§2](../../principles.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Native-first, with honest defaults** — GitHub's built-in automation carries status transitions server-side: Status-on-close/merge are on by default; auto-add is **off by default and operator-enabled in the UI** (the engine guides and verifies via `ProjectV2Workflow.enabled` but cannot enable it — no API exists). By default the engine's own defensive `item-add` populates the board with engine work; auto-add additionally pulls in non-engine items. The engine ships only the thin layer it alone can know — the custom fields (state / ranked work / debt / last-synced) and the defensive `item-add`. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **One-way is honest because field ownership is explicit** — the engine writes only its own fields and adds only its own already-labeled items; the operator's Status, card moves, and own board text are never overwritten. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **No enforcement** — pure projection; the board gates nothing ([§7](../../principles.md)). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Wires one non-blocking hook + one gitignore line** — the hook is best-effort, fail-open, never block-eligible, mode-declared, keyed distinctly; the gitignore keys the per-instance board-config *data* out of version control (the committed substrate is its schema; the data is gitignored like `mcp`/memory data, so no `provides` entry is a non-surface committed file); nothing else wires; `depends` ≠ wiring. | The design names the enforcing mechanism in the criterion itself; the concrete check is defined when this capability is settled. | engine |
| **Module-owned setup of a non-traveling resource** — the board is not template-borne; the module sets it up in the fixed `project`-scope → create → link → operator-guided-auto-add order (with a committed UI walkthrough and read-back fail-message), reusing provisioning's pattern without editing the locked provisioning doc, and stores no PAT secret. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Never strands a non-engineer** — every failure degrades to the git-native truth with a plain-language fix, a board-face staleness marker, informed consent for the scope grant, and plain-language labels that honor the [§12](../../principles.md) leak guard. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
