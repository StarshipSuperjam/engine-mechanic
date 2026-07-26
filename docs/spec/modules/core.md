---
status: draft
---

# core

*Settled in the design workspace on 2026-07-12, ratified by [decision 0304](../../adr/0304-resolve-re-lock-modules-core-the-foreign-license-seed-detect.md).*

## Summary

The **engine itself** — the universal `required` root every other package depends on. `core` bundles the
non-removable machinery a cold-booting session needs before any optional capability exists: the
[grammar](../systems/grammar/ontology.md), the cognitive floors, the guardrail foundations, the
infrastructure that stands the engine up and keeps it enforceable, the lifecycle spine, and the five verbs
the operator types. Apply the operational test in the [glossary](../../reference/glossary.md): *remove every module —
what survives is `core`.* This is the microkernel-*inspired* trusted core ([§12](../../principles.md),
[D-025](../../adr/0025-fault-containment-is-earned-at-the-seams-not-conferred-by-mo.md)); the adjective is an analogy with its limit stated (the modules share mutable
files, so containment is earned at the seams, not granted by the shape), and it stays maintainer-layer
vocabulary.

`core` is **contagious by nature**: a defect in it reaches every generated project, so the rule that earns a
foundation its place in `core` is that it *cannot* be an extension. Everything that *can* be carved into a
sibling package is — the cognitive store with per-instance data, the validator rule corpus, the decision-record
discipline, the routine stance, the self-audit — leaving `core` the irreducible minimum.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `core` |
| `status` | `required` |
| `provides` | the [ontology](../systems/grammar/ontology.md) catalog + its schema + the self-map; the [module-system](../systems/grammar/module-system.md) manifest schema and the `.engine/tools/` **wiring library** (paired applier/reverser per seam directive); the **validation dispatcher + the five closed check-kinds** (`schema`·`shape`·`presence`·`coverage`·`coherence`) **+ each closed kind's negative fixture** + the suite declarations + the trigger set ([validation](../systems/guardrails/validation.md)), whose kind-callable results carry findings on the canonical `finding.v1` base ([D-115](../../adr/0115-q27-1-re-litigation-the-validation-kind-callable-result-cont.md)); the [state](../systems/cognitive/state.md) cursor + its schema; the [attention](../systems/cognitive/attention.md) policy + ranking [tool](../systems/surfaces/tools.md) (realizing the ordered-partition ranking-function form, [D-117](../../adr/0117-q24-q27-2-re-litigation-the-attention-ranking-function-form.md)); the [knowledge](../systems/cognitive/knowledge.md) committed entities + their schema + the derived index + the graph-query generator; [templates](../systems/guardrails/templates.md); the [telemetry](../systems/guardrails/telemetry.md) detect→surface machinery (realizing the finding-record + ambient-capture shapes, [D-118](../../adr/0118-q27-4-5-re-litigation-the-telemetry-finding-record-ambient-c.md)); the [hooks](../systems/infrastructure/hooks.md) scripts; the [provisioning](../systems/infrastructure/provisioning.md) instantiator + permanent module manager/updater + the standing **operator-checkout-strand detector + un-stranding fix** [tool](../systems/surfaces/tools.md) + the standing **foreign-`LICENSE`-seed detector + consent-gated re-clear** [tool](../systems/surfaces/tools.md); the [boot](../systems/lifecycle/boot.md)/[modes](../systems/lifecycle/modes.md)/[close](../systems/lifecycle/close.md)/[build-orchestration](../systems/lifecycle/build-orchestration.md) [operations](../systems/surfaces/operations.md); the v1-core [policies](../systems/surfaces/policies.md) (contract-threshold, finding-disposition, escalation, triage-threshold); the control-plane PR-body [contract](../systems/surfaces/contracts.md); the shared **issue-authoring helper** [tool](../systems/surfaces/tools.md) (assembling engine-authored-issue bodies to the control-plane body contract) plus the **engine-Issue-conformance reroute-gate [hook](../systems/infrastructure/hooks.md)** (registered by [modes](../systems/lifecycle/modes.md) into the block budget) and the **`on:issues` CI backstop workflow**; the **foundational eADR [canon](../systems/surfaces/contracts.md)** (engine-owned shipped content — the Engine's structural-law *why*, [§18](../../principles.md); overlaid wholesale on upgrade while the deployment's per-instance eADR stream is preserved); the [conduct](../systems/surfaces/conduct.md) surface's universal-default **codes of conduct** (the operator's standing behavioral stance — engine-owned shipped content overlaid on upgrade, beneath a per-deployment operator override that is operator config preserved across overlay and [provisioning](../systems/infrastructure/provisioning.md)-seeded), loaded at the grounding floor via the root `CLAUDE.md` `@import`; the `search` + knowledge-retrieval [interface](../systems/surfaces/interfaces.md) protocol contracts; the agent persona-template grammar; the **Build-entry**, **`/engine-help`**, **policy-tuning**, **conduct-authoring**, and **status** [skills](../systems/surfaces/skills.md) (all **`operator-typed`**, so each is typeable from a cold session start; the **status** verb is the read-only [operator-presentation relay](../../reference/glossary.md) *pull* dashboard (milestone · what's next · recently-shipped · ranked work) — the operator types it for the unfiltered view and the AI relays the same dashboard by running the status [tool](../systems/surfaces/tools.md) directly (not by model-invoking the skill), listed in `/engine-help`; the policy-tuning verb writes the per-deployment [operator policy-override](../../reference/glossary.md) through an [operation](../systems/surfaces/operations.md) + a tune [tool](../systems/surfaces/tools.md), and the [attention](../systems/cognitive/attention.md) ranking tool + [telemetry](../systems/guardrails/telemetry.md) read the effective default-⊕-override values; the **conduct-authoring** verb writes, revises, or retires a *code of conduct* in the [conduct](../systems/surfaces/conduct.md) operator-override layer through an [operation](../systems/surfaces/operations.md) + a tool — draft-with-the-operator → write the instance → commit — the prose counterpart of policy-tuning); the minimum operator orientation [doc](../systems/surfaces/docs.md) |
| `wires` | `hook` — `SessionStart` (boot pack), `PreToolUse` (the [modes](../systems/lifecycle/modes.md) Explore write-gate + the [knowledge](../systems/cognitive/knowledge.md) commit-boundary regen), `PostToolUse` ([validation](../systems/guardrails/validation.md)'s touched-file subset run + [telemetry](../systems/guardrails/telemetry.md) capture + the [modes](../systems/lifecycle/modes.md) plan-acceptance Build-entry trigger), `Stop` (the [close](../systems/lifecycle/close.md) disposition gate), `UserPromptSubmit` (the per-prompt attention scent); `mcp` — the knowledge graph-query server (engine-prefixed name in root `.mcp.json`, pointing at engine server code under `.engine/tools/`; it reads the *committed* entities and the *gitignored* derived index, and its tool roster realizes the knowledge-retrieval [interface](../systems/surfaces/interfaces.md) op-set as the conforming fallback floor, [D-116](../../adr/0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md)); `gitignore` — the knowledge derived index + boot slice and session-scoped ephemera; `ontology-entry` — the catalog records for the surfaces core introduces; `permission` — the read access core's kernel operations need (the concrete permission strings are a build-spec leaf) |
| `depends` | **—** (the universal root) |
| `migrations` | none (v1) |

**Foundation-infrastructure artifacts ride outside `provides`.** Per the locked
[module-system](../systems/grammar/module-system.md) coherence rule, the root **`CLAUDE.md`**, the
**engine manifest** lockfile, and the engine-owned **`.github/` control-plane files** (CODEOWNERS, the
ruleset-guard workflow, the PR template, and the `bug`/`feature`/`engine-fault` issue templates) are *named foundation-infrastructure artifacts* — not surface instances, so they are
**not surface-grouped in any `provides`**. They ship as the engine baseline and are *unioned* with the
`provides` set by coherence and by the file-precise CODEOWNERS wall, so no foundational artifact is left
unowned. `core` is the package they conceptually belong to, but the locked grammar keeps them off the `provides`
list by construction.

### The kernel partition

`core` owns everything **not** carved out by a sibling `required` package. The carve-outs, and why each earns
its own package ([Required package](../../reference/glossary.md), [D-086](../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)):

- **`memory-substrate-sqlite-fts5`** — the [memory](../systems/cognitive/memory.md) floor: the
  gitignored NDJSON ledger (non-regenerable per-instance data needing an owned migration unit), its derived
  index, capture, the `search` interface *implementation*, and the memory MCP server. `core` holds the
  `search` interface *protocol*; the implementation and its MCP are the substrate's.
- **`validators-core`** — the concrete **validator rule corpus**: the `check` *data files* that judge the
  engine's own surfaces (catalog-coverage, module-coherence, link integrity, PR-body completeness, the
  editorial-shape lints). The boundary is the locked
  [validation](../systems/guardrails/validation.md) foundation's *own* design, not a fresh choice:
  that doc fixes validation as **a thin dispatcher over a kind registry where rules are data**, and has
  modules extend it **by providing a conforming callable discovered by presence — explicitly not a wiring
  seam**. So the **dispatcher + five closed kinds ride `core`** and `validators-core` is a rule-providing
  module on top — the same presence-discovery shape as `audit-library`'s checks. This rides `core` for the
  same reason [knowledge](../systems/cognitive/knowledge.md) does, with **no asymmetry**: the
  validation foundation owns no non-regenerable per-instance store and exposes no bound seam, so the
  [Required-package rule](../../reference/glossary.md) ([D-086](../../adr/0086-cognitive-foundations-as-required-packages-reconciliation-me.md)) keeps it in `core` rather than
  its own package (unlike `memory`, which earns one on both counts). Provisioning's locked direct `coherence`
  library call + the `core → validators-core` graph direction independently pin the engine to `core`. The
  resolution is logged as a constrained decision in [D-089](../../adr/0089-flesh-the-core-module-doc-to-designed-the-kernel-partition-t.md).
- **`routine-mode`** — the unattended routine *stance* + the `/engine-routine` entry ([D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)).
- **`audit-library`** — the self-audit persona, seed concern-list, and cron ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)).

What stays in `core` is the irreducible spine: the grammar, the regenerable cognitive floors (state, attention,
knowledge — no per-instance store to migrate), the guardrail foundations, the stand-up/enforcement
infrastructure, the full lifecycle, and the five operator verbs. The **eADR decision-record stream and the
contract-threshold application** ride `core` too: the [contracts](../systems/surfaces/contracts.md)
surface grammar, the contract-threshold [policy](../systems/surfaces/policies.md) (the
ADR-proliferation friction — bar + significance/anti-choice `hard-fail` + the `soft-warn` rate signal), and
the build/close capture gate already deliver it, and `core`'s contracts surface **ships the foundational
canon** (engine-owned) and thereafter **accumulates the deployment's per-instance eADR stream** (preserved
across upgrade) — both committed content on the one surface, so no separate `adr-discipline` package is
warranted ([D-093](../../adr/0093-cut-the-adr-discipline-module-vestigial-its-content-already.md), [D-169](../../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)). The [conduct](../systems/surfaces/conduct.md) surface likewise rides `core`: its universal-default *codes of conduct* — the operator's standing behavioral stance — must be present in every repo from cold boot (it cannot be optional) and are loaded by the core/topology-owned `CLAUDE.md` floor, so coupling them to a separable package would make the floor depend on a non-core path. It earns its place by the *cannot-be-an-extension* rule, not by size: the [§12](../../principles.md) addition is minimal — a committed defaults file, the floor's two `@import` directives, and the conduct-authoring verb — while the per-deployment operator override stays operator config preserved across upgrade ([D-192](../../adr/0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md)). `core`'s plan-review gate is a
[Slot](../../reference/glossary.md) — it runs as a disclosed no-op when no `design-review`/`qa-review` lens is installed
([D-066](../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)); the gate is core, the lenses are modules.

### Deferral seams — core integrates, the owners detect

`core` holds the engine's big **integrators** (boot, the telemetry surfacing, provisioning, the validation
dispatcher), so it is the densest site of the [§16](../../principles.md) ownership axis: the integrator binds to
a seam's channel and **relays**; detection and mechanism stay with the owning substrate.

- **Boot relays, substrates detect.** [Boot](../systems/lifecycle/boot.md) orders and renders the
  orientation pack, but [state](../systems/cognitive/state.md), memory, and
  [knowledge](../systems/cognitive/knowledge.md) each own their own readout and staleness detection;
  boot shows what they hand it and stays silent on which substrates exist.
- **The validation dispatcher routes; rules are data.** `core`'s thin dispatcher routes each rule to its
  kind callable and reports by tier — it carries no opinion about how hard a rule bites (the rule's `tier`
  decides) and owns no rule (the corpus is `validators-core`'s). A rule may also declare a **CI-author
  applicability boundary** (the pull-request authors it does not bind in CI); the engine honors it by producing
  a **disclosed not-applicable result** for a matching author — the applicability declared in the rule's data,
  never the dispatcher's judgment — keeping the closed kinds author-agnostic
  ([validation](../systems/guardrails/validation.md), [D-207](../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)). Two further
  commitments support the [validators-core](validators-core.md) **negative-fixture meta-check**: the
  dispatcher exposes **running a single logic-unit (a named rule, or a kind callable) against a
  caller-substituted target** — the meta-check's entry point; it extends provisioning's existing direct
  `coherence`-kind invocation, the **target-substitution being the added affordance** (the concrete API a
  build-spec leaf). And each of the **five closed kinds ships at least one negative fixture**, co-located
  with the callable in the [check](../systems/surfaces/check.md)-reserved fixtures namespace
  (forced co-location, not new kernel scope — a fixture cannot ride anywhere but its callable), so the
  meta-check can prove every closed kind is **witnessed to bite** — the core-kind fixtures are `core`'s
  exactly as their callables are.
- **Boot surfaces telemetry; telemetry triages.** [Telemetry](../systems/guardrails/telemetry.md)
  owns de-dup, promotion, and auto-resolution of its findings; boot only surfaces the inbox.
- **Provisioning applies; the control-plane defines.** The
  [control-plane](../systems/infrastructure/control-plane.md) defines the protection-off contract;
  provisioning applies the fix; boot only nags and offers.
- **Provisioning detects-and-fixes the strand; boot offers it.**
  [Provisioning](../systems/infrastructure/provisioning.md) owns the standing
  [operator-checkout](../../reference/glossary.md)-strand detector and the consented un-stranding fix;
  [boot](../systems/lifecycle/boot.md) surfaces the finding at the open-findings tier and offers the
  fix, staying read-only — the same detect/relay split as the protection-off seam above.
- **Provisioning detects the foreign `LICENSE` seed; boot offers the reviewed re-clear.**
  [Provisioning](../systems/infrastructure/provisioning.md) owns the standing
  **foreign-template-license-seed detector** — a still-recognizable engine seed left in a repo's product-root
  `LICENSE` (the pre-first-run-clear / drift residual, [R29](../../reference/risks.md)); [boot](../systems/lifecycle/boot.md)
  surfaces the finding at the open-findings tier and offers the fix, staying read-only. On consent the removal
  lands as a **reviewed pull request the operator merges** — not a boot-time write: a live protected repo's
  committed `LICENSE` is removed durably only through the reviewed gate, so it rides the same reviewed path the
  never-strand floor leaves **out of scope** (that floor governs working-tree/strand git-state, not reviewed-PR
  commits to the default branch); the engine's authority to *propose* the product-root removal is
  [topology](../systems/infrastructure/repository-topology.md) law 2's standing exception. Detect/relay
  split as the strand seam above; the fix **diverges** (a PR, not the strand's direct realign).

Because each integrator binds to the channel and not the roster, a new upstream producer attaches additively
and an owner's later evolution cannot force `core`'s side.

### Operator-facing surfaces stay plain

`core` carries the heaviest maintainer-layer vocabulary in the engine — "the foundations,"
"microkernel-inspired," the validation dispatcher/corpus seam, the [§16](../../principles.md) ownership axis. By
the [§12](../../principles.md)/[§14](../../principles.md)/[§16](../../principles.md) leak guard, **none of it
surfaces to the operator.** The audiences are distinct:

- The root **`CLAUDE.md` is the AI grounding floor** — read by the booting Claude Code session, not operator
  reading material; it carries memory-authority routing, the engine/product wall ([D-042](../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)),
  and the [operator-presentation relay](../../reference/glossary.md) + present-marker — the AI is the sole pipe to the
  operator ([constraints](../../reference/constraints.md)), so the floor tells it to relay the must-push subset and open
  each session with the named status block. It also carries the **never-strand-main** floor — the
  [operator checkout](../../reference/glossary.md) is the operator's surface, so the session never mutates its git state
  (detach, reset, branch-switch, or commit *in* it) **as build work, autonomously, or unconsented**; the one
  exception is the operator-consented un-stranding correction [boot](../systems/lifecycle/boot.md)
  offers, and the floor is scoped to the working-location/strand class, never to commits that reach the default
  branch through the reviewed PR ([build-orchestration](../systems/lifecycle/build-orchestration.md)).
  And it binds that when the operator asks the session to open an engine-labeled Issue, it authors it through
  the shared **issue-authoring helper** — a **channel-scoped reroute gate**, not bare posture: a `PreToolUse`
  block redirects a non-conforming engine-labeled creation to the helper, backstopped by a CI check (GitHub
  cannot gate creation server-side, so the lever is client-side —
  [control-plane](../systems/infrastructure/control-plane.md)). It also **`@import`s the
  [conduct](../systems/surfaces/conduct.md) layer files** (`.engine/conduct/defaults.md` +
  `.engine/conduct/operator.md`), so the operator's *codes of conduct* — the standing behavioral stance —
  load at the floor itself, hook-independent and present even when the boot pack does not run; the floor stays
  thin (it carries the `@import` directives, not the stance text), and the stance is **posture, subordinate to
  every law** — it never weakens a guardrail, with a [validation](../systems/guardrails/validation.md)
  guard flagging any code of conduct that purports to.
- The **Build-entry skill, `/engine-help`, the policy-tuning skill, the conduct-authoring skill, the status verb, and the operator orientation doc** are operator-facing and obey the
  operator-communication law: plain language, with **maintainer-internal vocabulary never surfacing — not even
  as a parenthetical label** (the [skills](../systems/surfaces/skills.md) convention: an operator-typed
  skill is simply "a command — a verb you type"). Operator-relevant platform names (GitHub, Claude Code) may
  appear plainly.

`/engine-help` is **degradation-proof by construction**: it derives its listing from committed sources (the
[§14](../../principles.md) discovery axis), never an MCP substrate, so an outage cannot blank it — a
non-engineer asking "what can I do here?" still gets the verb list and what each one does. The boot floor and
the knowledge layer degrade the same way — committed files first, derived indexes as replaceable caches — so
a substrate outage narrows richness but never strands the operator ([degrade-to-git-native](../../principles.md)).
Its discovery contract is pinned in the build-spec-leaves section below.

### Build-spec leaves: the `/engine-help` index and kind discovery

Two presence-discovery mechanisms `core` ships are pinned to their **form**, with concrete values deferred
(the laws-not-leaves form/contract convention, [D-113](../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)).

**The `/engine-help` verb index** ([D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md); the [§14](../../principles.md) discovery
axis) — a degradation-proof listing of the engine's operator-typed verbs, in two parts:

- *Installed verbs* — parsed from the committed verb files present (`.claude/skills/*/SKILL.md` and the legacy
  `.claude/commands/*.md`) by **real YAML frontmatter parsing** (not line position). The verb is the skill
  `name` (fallback: its directory) or the command filename; its line is the frontmatter `description`. In v1
  the engine's verbs are all `operator-typed` ([D-200](../../adr/0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)), so each is typeable from a cold
  session start; the predicate is the engine's **operator-invocable** verbs — it **defers to the
  [skills](../systems/surfaces/skills.md) invocation axis** (`operator-typed` and `model-auto` — the operator-invocable values; `model-only` is hidden from the menu) rather
  than hardcoding a frontmatter flag, so every operator verb is listed. Engine skills carry a `description` by schema
  (enforced by `validators-core` schema-conformance), so the index never shows a blank for an engine verb.
- *Available-if-installed verbs* — an uninstalled optional engine verb is shown as "available if you install
  X", read from the **committed module catalog provisioning maintains** (the [D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)
  selection-UX data, which survives deselection and drives re-add) — a [§16](../../principles.md) relay
  (provisioning owns the catalog, `/engine-help` reads it). The catalog carrying each optional module's verb +
  one-line description is the deferred value.
- The listing closes with a plain-language pointer to the operator orientation [doc](../systems/surfaces/docs.md),
  so it is an exit to deeper help, not just a directory.
- Deferred values: rendering strings, listing order, and the catalog's exact fields.

**Module-provided check-kind discovery** — the validation **dispatcher** discovers a module-provided
check-kind callable by **presence** (the locked [validation](../systems/guardrails/validation.md)
grammar: "a conforming callable, discovered by presence, not a wiring seam") in a pinned `.engine/tools/`
location, by a filename↔`kind`-name convention; each conforms to the kind-callable result contract
([D-115](../../adr/0115-q27-1-re-litigation-the-validation-kind-callable-result-cont.md)), and a `kind` with no callable hits the locked dangling-kind finding. This is
the dispatcher's discovery *form* (the concrete directory a deferred value); it is **not** a `core`-lock
blocker — `core`'s five closed kinds register directly, so the discovery path is exercised only when a module
adds a kind.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The depth is the systems'; the bundling is this module** — `core` names *which* locked machinery ships in the trusted root and what carves out to siblings; it does not restate the systems' laws. | Read this description against the built behavior and confirm they match. | operator |
| **The contagious core stays minimal** ([§12](../../principles.md)) — a foundation rides `core` only when it cannot be an extension; anything carve-able is carved (the operational *remove-every-module* test). | Read this description against the built behavior and confirm they match. | operator |
| **Core registers the kernel seams and owns the wiring-library firewall** — every shared-state edit goes through the closed [seam vocabulary](../../reference/glossary.md) and its guaranteed reversers; the library lives in `core` so it outlives the self-deleting instantiator. | Read this description against the built behavior and confirm they match. | operator |
| **Core integrates but relays** ([§16](../../principles.md)) — it surfaces, ranks, dispatches, and applies over channels whose detection and mechanism stay with the owning substrates. | Read this description against the built behavior and confirm they match. | operator |
| **Operator surfaces stay plain** — the maintainer vocabulary `core` carries never leaks; `/engine-help` and the orientation doc are degradation-proof and plain-language. | Read this description against the built behavior and confirm they match. | operator |
| **Validation dispatcher + five closed kinds in core, rule corpus in `validators-core`** — forced by the locked kind-registry shape and the `core → validators-core` dependency direction, not a style choice. | Read this description against the built behavior and confirm they match. | operator |
