---
status: draft
---

# Module system

*Reconciled with engine-template@`cdbbc33` as built (2026-07-29) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-27 by [decision 0261](../../../adr/0261-establish-the-artifact-warrant-discipline-a-7-17-application.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

The composability layer. Capabilities are packaged as **modules**; the module system defines the
manifest grammar, how the installed set is known, the dependency graph and build order, and the wiring
library that keeps install and uninstall **mechanical** rather than hand-surgery. It is what makes the
engine configurable per project and **upgradeable** in the field.

The engine is a small trusted core (the foundations) plus optional extensions (the modules) — a
microkernel-*inspired* shape. But the containment that keeps one module's failure from spreading is a
property of the **wiring discipline at the shared seams**, not of the shape ([principles §12](../../../principles.md)).
The whole of this system's reversibility design exists to earn that containment and to kill the
"every feature is a refactor" failure that sank the prototype (Risk [R5](../../../reference/risks.md)).

## Behavior

### The manifest grammar

Each module owns one manifest at `.engine/modules/<id>/manifest.json`. A module's *files* are scattered
**by surface** (its checks under `.engine/check/`, its commands under `.claude/commands/`, …) per the
[topology](../infrastructure/repository-topology.md) placement law, so the manifest is the only
place that knows which scattered files belong to the module — the fact that makes uninstall, coherence,
and the self-map possible. The manifest is **not** a [catalog surface](ontology.md); it is
module-system infrastructure (like the `.engine/tools/` code-home), governed by a [check](../surfaces/check.md)
rule of kind `schema` (JSON Schema 2020-12), not by being catalogued.

A manifest declares:

- **`id`** — stable module identifier.
- **`version`** — semver. Internal migration bookkeeping (see versioning below), not an operator-facing number.
- **`status`** — `required` · `default-on` · `optional` · `experimental` · `retired`.
- **`provides`** — the files the module owns, as **file-precise** paths/globs, non-overlapping, grouped by
  category — usually a surface name, plus foundation-style groups (`foundation`, `state`, `knowledge`, …)
  for engine files that are not surface instances.
  Membership of [check-suites](../guardrails/validation.md) is *not* declared here and is *not* wiring — a
  check rule self-declares the suites it joins, so a suite's roster is **derived** from the check files the module
  provides.
- **`wires`** — the side-effects beyond copying files, drawn from a **closed seam vocabulary** (below). Declared
  declaratively and reversibly.
- **`depends`** — module ids, each with an optional semver range. A presence-and-range *assertion*, not a problem
  for a version solver (see dependency resolution).
- **`migrations`** — version-keyed data/schema transforms, run in dependency order on upgrade.
- **`retired_capabilities`** — version-keyed, **announcement-only** records of capabilities a version
  removed: they run and reshape nothing, exist so an upgrading operator is told in plain language what
  went away (surfaced in the upgrade pull request and its preview), and are permanent once shipped — a
  release-cut guard refuses to drop one a lagging upgrader has not yet seen.

### The engine is versioned packages; the installed set is known, not registered

Every engine unit is a **versioned package**: the foundations carry `status: required` (always present, never
optional, but versioned and migratable), features carry the other statuses. This is what makes the engine
**upgradeable**, not merely configurable ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)).
As built, five packages are `required` — `core`, `validators-core`, `audit-library`, `routine-mode`, and
the `memory-substrate-sqlite-fts5` foundation — and one ships `default-on` (`memory-semantic-recall`),
the status's first live use.

There is **no separate, hand-authored registry**. The two stores are both derive-or-record, never a duplicate to
drift ([principles §2, §3](../../../principles.md)):

- The **available/installed set** is the module manifests **present** in `.engine/modules/` — a directory listing,
  not an authored list. **Installed means present**: first-run instantiation *deletes* the modules the operator did
  not select, so an absent capability ships no code and can carry no defect, and re-adding one later goes through the
  updater (the same path as an upgrade), not a flip-on.
- The **[engine manifest](../../../reference/glossary.md)** is the committed config file ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md);
  [topology](../infrastructure/repository-topology.md) law 5) recording the **engine release** and **each
  installed package's version** — a lockfile. The per-package versions are the non-derivable upgrade state (the
  migration "from" version, read before an overlay replaces the manifests) and double as the operator-readable
  record of what the engine is made of. As built the engine manifest is more than a version lockfile: it
  also records the **identity tier** (`solo`/`team` — the setting guardrail-change gating reads), the
  **upgrade floor** (`min_upgradeable_from`, refusing a too-old jump cleanly instead of mis-migrating),
  and the engine's coordinates (`home_repository`; for a deployed mechanic, the product repository it
  builds) — the identity-and-versions record of what this engine is.

The operator sees **one engine version** (vX → vY); per-package versions are internal bookkeeping. The baseline
"what is my engine made of" readout is the [ontology](ontology.md) **self-map** (foundation-level,
committed, derived, fingerprint-gated; its wiring-graph portion populated by this system from the present manifests),
available to every project and degrading to a committed file. By design law that readout has a **named,
operator-reachable access path** — a plain-language way for the non-engineer to ask "what is my engine made of" and
get a readable answer, so the self-map and manifest are never AI-only (the concrete surface is a
[provisioning](../infrastructure/provisioning.md)/operations bootstrap-UX build-spec
leaf). Two similarly-named things sit above that baseline and must not be conflated
([decision 0089](../../../adr/0089-flesh-the-core-module-doc-to-designed-the-kernel-partition-t.md),
[decision 0086](../../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)):
the knowledge foundation's **structural graph-query server** — which as built carries the name
`engine-knowledge-graph` — is a required `core` `mcp` wire, part of the baseline. The semantic-recall
role that decision 0086 once sketched for an optional module of the same name is, as built, filled by
the **default-on `memory-semantic-recall` module** named above; the carried
[engine-knowledge-graph](../../modules/engine-knowledge-graph.md) **module** page describes the unbuilt
remainder of that sketch (graph-representation enrichment over memory), stays not yet described, and
nothing in the baseline depends on it.

### Dependency resolution and build order

The dependency graph is **acyclic and resolved transitively**; the WBS build order is its
**topological sort**. Because every module ships from one tagged engine release as one tree, there is **no
multi-version solving** — `depends` is checked, not solved: presence (the depended-on package is installed),
acyclicity, topological order for install/migration, and a coherence **range-check** that each declared range is
satisfied by the version present in this release. Ranges earn their keep at upgrade time (a new core version that
falls outside a module's declared range signals a needed migration), not as a SAT problem.

### The wiring library

A **permanent shared library** in `.engine/tools/` applies and reverses `wires`. Both
[provisioning](../infrastructure/provisioning.md) subsystems — the one-time instantiator and the permanent
module manager — call it, so the wiring logic does not die with the self-deleting instantiator. It holds a paired
**applier and reverser** for each directive type.

**The seam vocabulary is closed.** A module may touch shared state only through a small, reviewed set of directive
types, each with a guaranteed reverser — seven, as built:

- **`hook`** — a keyed registration in `.claude/settings.json` ([hooks](../infrastructure/hooks.md)).
- **`mcp`** — a server definition in the root `.mcp.json` (see MCP registration).
- **`ontology-entry`** — a record in the [ontology](ontology.md) catalog (when a module introduces a surface).
- **`permission`** — a permission entry in `.claude/settings.json`.
- **`gitignore`** — engine-owned lines in the root `.gitignore`.
- **`codex-hook`** — the Codex runtime's mirror of a hook registration, in `.codex/hooks.json`; a change
  here carries an operator **re-trust notice**, since Codex asks the operator to re-approve hooks.
- **`codex-mcp`** — the Codex runtime's mirror of a server definition, rendered as TOML into
  `.codex/config.toml` inside an engine-fenced block, parse-guarded before and after the write.

There is **no `custom/script` escape hatch** for wiring: an arbitrary shared-state mutation with no guaranteed
reverser *is* the [R5](../../../reference/risks.md) failure. A genuinely new seam is a reviewed change to this core (a new
applier/reverser pair), and that deliberate friction is the firewall. (This is distinct from the
[validation](../guardrails/validation.md) `custom/script` *check-kind*, which is a read-only check, a
different axis entirely.)

**Reversal keys on engine-namespaced identity, not on bare content.** An engine entry is identifiable by construction
— a `hook` command points into `.engine/` (the key is the `{event, matcher, type, command}` tuple); an `mcp` server
carries an **engine-prefixed name**; an `ontology-entry` is a record in the engine-owned catalog under `.engine/`;
`gitignore` lines live in a **comment-fenced engine-managed block** (and a module's `gitignore` wire is
**fail-closed against claiming the foundation block's own fence key** — the one reserved identity no
module may take). Apply **inserts iff absent**; reverse **removes
only the engine-identified entry**, so an operator's or product's independently-authored identical-looking entry is
left untouched. Where identity is not namespaceable — a bare `permission` string the operator might also hold, or one
a second still-installed module also needs — the engine **errs toward leaving it**: it never auto-removes such an
entry, so the worst case is a tolerated residual permission, never the removal of one the operator wanted. That
residue is outside coherence's reach by the same token (it is not engine-identified) and is the accepted cost of never
mis-removing. This needs no provenance tags inside platform-owned files and no drift-prone external ledger — the
manifest `wires` block is the complete record, and reversal re-derives from it.

**Partial failure is safe.** Every apply and reverse is idempotent, so a crashed half-install is safe to re-run; the
post-install coherence check is the backstop, and a failed gate fails open and flags ([hooks](../infrastructure/hooks.md)
fail-open-and-flag), never silently.

**No seam edits product source.** Every directive touches an engine-namespaced file or an engine-owned keyed entry in
a platform-shared file (`.mcp.json`, `.gitignore`, the Codex runtime's `.codex/hooks.json` and
`.codex/config.toml`); none reaches into product source. So product code carries
zero engine wiring, and the engine remains a contributor, not a component ([principles §13](../../../principles.md)).

### Coherence

After any install, uninstall, or upgrade, the module manager invokes the [validation](../guardrails/validation.md)
foundation's coherence legs directly (a set of library calls, not a suite trigger) to confirm the set is
consistent. As built the legs are composed functions rather than one check-kind, and there are five
scopes, the original three plus two:

- **Declared wiring ⟺ applied wiring** — everything a present manifest's `wires` declares is applied in the shared
  files, and nothing engine-identified is applied that no manifest declares. The **foundation `.gitignore` block**
  (the tool-runtime's `.engine/.venv/` ignore, applied by the wiring-library comment-fenced-block *helper* at
  [provisioning](../infrastructure/provisioning.md) — **not** a module `wires` directive) is outside this
  leg, exactly as CODEOWNERS is: it is a foundation infrastructure injection no manifest declares, so coherence does
  not read it as undeclared engine wiring (module `gitignore` *wires* remain in-leg) ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)).
- **`depends` satisfied** — every declared dependency is present and within range.
- **Every engine file maps to exactly one module's `provides`, or is a named foundation infrastructure
  artifact** — a named set carried as **data in the coherence tool itself** (the authoritative roster
  lives there, not in this doc): the engine manifest, the root `CLAUDE.md` and `AGENTS.md` (the Codex
  floor), the tool-runtime's `pyproject.toml` + `uv.lock`, the root `.gitignore`, and the engine-owned
  `.github/` control-plane files — `CODEOWNERS`, the ruleset-guard and CI workflows and their siblings
  (release, secret-scan, audit-prep and the rest), the pull-request and issue templates,
  `dependabot.yml` — none of which are surface instances and so
  are not surface-grouped in any `provides`. An engine file that is neither claimed by exactly one
  `provides` nor a named infrastructure artifact is an orphan finding; a double-claimed file is a finding.
  **Operator- and deployment-authored committed content is outside this leg** (again a named set carried
  as data in the coherence tool): the committed [operator policy-override](../../../reference/glossary.md)
  of tunable policy values (*operator config*), the operator's guarded-paths and local-reference records,
  the operator's own conduct layer, the provisioning seeds, and a deployment's **per-instance eADR
  stream** on the [contracts](../surfaces/contracts.md) surface (deployment-authored decision records) —
  all operator/deployment-owned and preserved across overlays, not engine machinery — so coherence does not read
  them as orphans, the same shape of carve-out by which CODEOWNERS and the foundation `.gitignore` block sit
  outside the wiring leg above ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md), [D-169](../../../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)).
  This named set is what the engine/product wall's file-precise CODEOWNERS ownership unions with the
  `provides` set, so no foundational artifact is left unowned (see [topology](../infrastructure/repository-topology.md)).
- **Only the sanctioned hook events may hard-block, and every declared block names its stances** — the
  block-budget leg over the assembled block registry; this one leg also stands as a merge-gated check
  (`block-coherence`, hard, `CI`), so a block declared on a non-sanctioned event cannot land.
- **A module-provided check-kind must load cleanly and collide with nothing** — the kind-discovery leg: a
  kind file that shadows a foundation kind, collides with another module's, or fails to import is a
  finding.

Check-suite rosters are *derived* and cannot drift, and ontology catalog coverage is an already-separate locked gate, so
neither is part of module coherence. A declared-but-not-yet-approved MCP server is an **expected pending-setup state**
surfaced as a setup finding, not a coherence-drift failure that fires every run. A companion soft check
(`untracked-surface`) names git-untracked cruft inside surface homes — sync-conflict debris the ownership
leg would otherwise misread.

Coherence is a *structural* attestation, and its [artifact warrant](../../../reference/glossary.md) says so —
prominently, because the gap is wide and easy to over-trust. A green check proves the installed set is
**consistent** — wiring applied as declared, dependencies present, every file owned — and **nothing
more**. It does **not** prove the modules *function*: that a module does useful work shows in its own
[checks](../guardrails/validation.md) and in the behavior the operator observes, and an
optional module that has stopped earning its place is the [audits](../guardrails/audits.md)
retire-candidate probe's call (absence of exercise + no affirmative case), not coherence's. A green
coherence result is never a fitness attestation ([§7](../../../principles.md)/[§17](../../../principles.md)).

### MCP registration

Project-scope MCP server **definitions** live in the root **`.mcp.json`**, keyed by server name; `.claude/settings.json`
holds only the operator's approval/enable flags, never project-scope definitions. The `mcp` wiring directive therefore
writes only the `.mcp.json` definition, keyed on the **engine-prefixed server name**, with `command`/`args` using
`${CLAUDE_PROJECT_DIR:-.}` so a committed entry points at engine server code under `.engine/tools/` while the **data
stays gitignored** (ship-the-substrate-not-the-data). The root `.mcp.json` slot is sanctioned by
[topology](../infrastructure/repository-topology.md) (a tool-dictated slot; the engine owns only its keyed
entries).

**Approval is the operator's, not the engine's.** A project server requires a **one-time operator approval** (a platform
security prompt) — a trust decision the operator owns, recorded in the operator's own approval state, **not**
engine-written wiring. The `mcp` reverser therefore removes only the `.mcp.json` definition; any residual operator
approval for that server name is inert (it points at nothing) and is left untouched, exactly as a bare `permission` is.
The first-run approval walk-through and its wording are a [provisioning](../infrastructure/provisioning.md)
bootstrap-UX build-spec leaf. Until approved or available, the substrate is **loudly surfaced**,
and by design law the surfaced message **names the substrate, states that the engine is running on the committed-file
fallback, and gives the operator the one command to fix it** (at boot and in the control-plane PR Validation section,
per the [hooks](../infrastructure/hooks.md) fail-open-and-flag pattern) — never silently inert.

### Lifecycle: install, uninstall, upgrade, removal

- **Install** — copy the `provides` files into their surface homes; apply `wires`; run the coherence kind. A direct,
  reviewable invocation, not a fifth suite trigger.
- **Uninstall** — manifest-derived reversal removes exactly the engine-identified files and wiring (idempotent); the
  coherence kind confirms no orphaned settings.json/`.mcp.json` entries remain.
- **Upgrade vX→vY** — the module manager reads each installed package's current version from the engine manifest,
  pulls the tagged release ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)), **overlays only the engine-namespaced paths of the
  installed packages** (never resurrecting a module the operator deselected), runs `migrations` in dependency order,
  runs coherence, and lands a reviewed pull request through the [control-plane](../infrastructure/control-plane.md)
  gate; it degrades to the current version when the release source is unreachable.
- **Clean removal** — reversing all wiring and deleting all engine-namespaced files is **not** sufficient on its own:
  the branch **ruleset is a GitHub setting, not a file**, so a removal must also **de-bootstrap the control-plane**
  (drop the engine's required-check binding) or a stale binding to a now-deleted engine check would deadlock the
  product's own PRs. Dropping that binding is an **operator-privileged** action — the same operator-privileged actor
  (holding `repo` / Administration:write) the [control-plane](../infrastructure/control-plane.md) bootstrap requires (the default token cannot;
  Risk [R1](../../../reference/risks.md)) — so removal is wiring-and-file reversal **plus a single flagged operator-privileged
  step**, handed to the non-engineer in plain language rather than leaving a silently deadlocking ruleset. Done
  correctly, removal leaves an operable, engine-free product whose PRs still merge, with product-owned entries in the
  shared root files untouched — a contributor leaving without unbuilding what shipped.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Modules declare files + wiring; provisioning applies/reverses both**, so install is mechanical ([D-012](../../../adr/0012-provisioning-is-two-subsystems-on-one-manifest-grammar-modul.md), [R5](../../../reference/risks.md)). | The declaration half is merge-gated: `module-manifest` (hard, `CI`) validates every manifest's `provides`/`wires` against the module schema. The apply/reverse half lives in the wiring library's paired appliers and reversers, confirmed by the bidirectional coherence legs — which run at install/uninstall/upgrade, not per-merge; observe a module operation to see it. | operator |
| **The closed seam vocabulary and engine-namespaced-identity keying** are the structural firewall: a module can only touch shared state in ways the system can guaranteed-reverse without disturbing the operator's or product's own entries. | The closed vocabulary is merge-gated: `module-manifest` (hard, `CI`) rejects a `wires` entry outside the seven-type enum, and the wiring library dispatches reject-by-default. The keying and never-mis-remove discipline live in the appliers/reversers and the orphan-wire coherence leg, exercised at module operations — partial mechanical support; no per-merge check asserts the keying itself. | operator |
| **Installed means present; the engine is single-versioned to the operator**; the engine manifest carries per-package versions for migration and for the operator-readable inventory. | The manifest's shape is merge-gated: `engine-manifest` (hard, `CI`) requires the engine release and the per-package versions. Installed-means-present is how discovery works as built — the module directory listing *is* the installed set — and the operator readout is the self-map; observed, with no check asserting the single-version presentation itself. | operator |
| **Locking this system fixes the laws' change-control, not their content forever** — the manifest grammar, seam vocabulary, registry model, and coherence scope change only by a governed decision, never silently; the module set was always resolved separately ([D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)/[D-068](../../../adr/0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md)). | Observed in the record: the vocabulary's growth to seven seams, the manifest's eighth field, and the coherence scope's two added legs each trace to the engine's own decision canon, and their adoption here is ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). No mechanical check asserts change-control. | operator |
