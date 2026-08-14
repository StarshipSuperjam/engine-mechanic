---
status: locked
---

# Provisioning

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with first-run selection scoped to `extension` distribution and newly-required modules converged at upgrade by [decision 0335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-07-12 by [decision 0305](../../../adr/0305-resolve-re-lock-provisioning-build-owe-5-the-designed-standi.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The subsystem that stands a generated repo up and installs, updates, and removes engine
capabilities over its life. It is **not itself an installable module** — it is the system that
installs modules, so it must exist before the module grammar it applies (the bootstrap paradox) —
and it owns the two delivery paths by which the engine reaches a repo at all: a fresh repo
generated from the template (**greenfield**) and a live product repo the engine joins (**brownfield**).

## Behavior

### Two subsystems, one grammar

- **Instantiator** — one-time, self-deleting. On first run it derives identity, takes the
  operator's **extension** selection (the only distribution class an operator declines), applies it
  (deleting unselected extensions so *installed means present*), initializes substrates, attempts the
  [control-plane](control-plane.md) bootstrap, verifies, and retires. Its operator entry is the
  permanent `engine-setup` dispatcher: its first branch invokes this first-run work, and its later
  branches manage add-ons, conduct, tuning, reviewer mode, protection, memory backup, and installed
  module configuration.
- **Module manager** — permanent. Over the repo's life it adds and removes modules, **upgrades
  the engine itself**, runs migrations, and cleanly removes the engine.

Both share the [module system](../grammar/module-system.md) manifest grammar and call
the same **permanent shared wiring library** (`.engine/tools/`), so the wiring logic does not
die with the self-deleting instantiator. The instantiator is a **thin first-run orchestrator**:
it composes permanent primitives — the wiring library, the permanent bootstrap operation, the
[validation](../guardrails/validation.md) coherence kind, file deletion — plus the
little logic that is genuinely first-run-only (the selection walkthrough, token derivation,
self-retirement). Only that orchestrator and its first-run assets self-delete; everything it
calls persists. Deleting an unselected module reuses the file-deletion half of uninstall — no
wiring is reversed because nothing was wired yet.

### Greenfield and brownfield adoption

The engine is a **contributor, not a component** ([principles §13](../../../principles.md)): a
contributor joins and learns an existing product, so the engine must be installable onto a
**live** repo, not only a fresh one. Two delivery paths satisfy this; the *coexistence*
discipline that makes the engine safe to drop in is the same for both.

- **Greenfield** — the operator generates a repo from the template ("Use this template" copies
  the tree as one commit). The instantiator ships in that tree and runs. The repo starts empty
  of product code, so no pre-existing artifact can collide.
- **Brownfield** — the operator adds the engine to a populated product repo. "Use this template"
  cannot target an existing repo, so brownfield reuses the **engine updater's**
  fetch-tagged-release-and-overlay machinery (see *Upgrading the engine*) through the instantiator's
  own **arrival verb**: it places the engine's
  namespaced files — instantiator included — onto the existing tree (collision-checked, below), then
  runs the **same
  instantiator**. Identical logic; only the arrival differs — plus one brownfield-specific
  control-plane sequencing, the two-phase binding under *Control-plane bootstrap* below.

Coexistence is carried by the engine's confinement to namespaced corners
([topology](repository-topology.md) law 1) and by the wiring library's keyed,
insert-iff-absent, comment-fenced edits to platform-shared files. On brownfield the instantiator
runs a **collision check** over the engine's namespaces and the shared root files: any
pre-existing content in an engine-exclusive path, product content in a shared path, or a product
**CODEOWNERS rule that would shadow an engine path**, is **surfaced to the operator in plain
language — never silently overwritten**. The engine owns its delimited entries within a shared
path; the product keeps the rest. Each surfaced collision is stated as a **concrete consequence and
an operator choice** — what the engine would otherwise do, what the operator keeps or loses, and
accept / leave-as-is / abort — never a raw path-versus-glob report a non-engineer cannot act on.
Because the collision check catches an expansively-globbed
product rule, the dot-namespacing of engine paths is defense-in-depth, not the sole guarantee.
These surfaced changes are **reviewable before they land** (and ultimately behind the merge wall),
so the brownfield overlay never silently mutates a live tree. Product content the collision check
already surfaced is **expected, not re-flagged** by the subsequent coherence run — coherence's
file-ownership leg carves out non-engine files, so the collision check's disclosure is the single
operator-facing story.

### The instantiator: gather → confirm → apply → verify → retire

The verdict that a repo is **unprovisioned** derives from **observable installed shape**, never from
the committed engine manifest's mere presence: the manifest travels with a template copy, so reading
its presence alone as "already set up" leaves every generated repo dead-on-arrival
([D-277](../../../adr/0277-litigate-engine-template-353-first-run-dead-on-arrival-in-a.md)). As built
(operator-ruled in the wave-5 reconciliation) the derivation conjoins **two grounded signals**: the
checkout is a **downstream copy** — the manifest's recorded update home is a *different* repository
than the checkout's own git origin, since the workshop where the engine is built has origin equal to
home while every downstream copy inherits the upstream home (compared slug-normalized, and
safe-quiet whenever either side cannot be read) — **and** the one-time setup tool is **still
present** (it self-deletes at retire, so its presence is the design's own "not done yet" signal,
covering a fresh copy and an interrupted run alike).
Across the instantiator's whole life the verdict is three-state:

- **setup tool present (on a downstream copy) → unprovisioned** — offer setup (a fresh copy, or an
  interrupted run);
- **setup tool absent _and_ the engine manifest present → provisioned** — the clean post-retire repo;
- **setup tool absent _and_ no manifest → a broken/partial checkout** (botched copy, manual
  deletion) — routed to the operator-checkout strand detector's missing-engine-files arm
  (*Operator-checkout strand* below), never silently read as done.

The manifest stays the apply-resume **checkpoint** and the upgrade source-of-truth — and one conjunct
of the done-vs-broken read and the downstream-copy signal — **not** the provisioned verdict on its
own. To make first run
resumable without losing the operator's choices to a destructive step, the run is split at that single
commit point — the **engine manifest** ([module system](../grammar/module-system.md);
[D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)) is the checkpoint, so no new state is introduced:

1. **Gather** (non-destructive, fully re-offerable) — derive identity tokens, prompt the one
   choice that is not derivable (the identity tier), and present module selection with its
   dependency closure. Per [D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) and
   [D-335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md) the selection presents
   **only the opt-out-able `extension` modules** — the sole distribution class an operator declines — grouped
   under the three recognized SDLC discipline categories (Product Management, Software Configuration Management,
   Verification & Validation, the category-presentation model D-067 fixes, which stands); the `required` spine
   (core plus the governance-and-delivery modules) is never offered as a choice (it is disclosed in the project
   README, not the walkthrough), and a `profile` module's presence follows its platform/stack match, not a
   prompt. The closure still surfaces any extension→extension dependency at confirm; it does not surface
   always-present `required` dependencies. Nothing is written or deleted yet.
2. **Confirm** — the operator confirms, which **writes the engine manifest** (selected modules +
   tier + derived identity + the engine's **home repository**, carried forward from the template's committed
   manifest — the seed the updater and the escalate-upstream audit both resolve the template repository from;
   *Upgrading the engine* below). The confirm step states, in plain outcome-language, that unselected
   **extensions** are **not installed** (their code is removed) and that adding one back later is a
   **separate action the engine performs on request**, not a toggle — so a selection list's
   "reversible checkbox" intuition does not mislead.
3. **Apply** (idempotent, driven entirely by the manifest) — in the built order: delete unselected
   extensions and lay the foundation ignores; render the CODEOWNERS block; **set the native
   permission-mode default** when adopted (*The native permission-mode default* below);
   **materialize the tool-runtime** (bootstrap uv behind consent, then group-scoped `uv sync` —
   *Tool-runtime bootstrap* below) — a failure here **halts the phase**, and the resume lands every
   later step, so the seeds below arrive only once a working runtime exists (a deliberate
   co-location behind the halt for resumability's sake — the seeds themselves are pure file writes
   with no runtime dependency, and the verify-phase coherence run deliberately leans on the standard
   library alone so it starts on a bare adopter machine); then the substrate-and-seed step — initialize the
   substrates, **seed the [conduct](../surfaces/conduct.md) operator-override** from the
   template-carried seed (*The conduct operator-override seed* below), **seed the root `SECURITY.md`**
   disclosure file from the template seed (*The security floor* below), **seed the root `README.md`**
   product-starter — replacing the engine's marketing landing front on greenfield (*The root README*
   below), **clear the traveled root `LICENSE`** — the template's own, on greenfield (*The root
   LICENSE: clearing the traveled template license* below), reset the engine's state record to a clean genesis, and **seed the product's own
   version file** (a top-level `product-version.json` at `0.0.0`, so the deployed repo's release
   workflow cuts the *product's* releases, never the engine's); apply the module **wires** — hook and
   MCP registrations ride the same wiring pass, not a separate step; attempt the control-plane
   bootstrap; and finish with the GitHub-side settings steps (*Control-plane bootstrap* below:
   Actions enablement, the native security toggles, and the repository-behavior settings). Each step
   is safe to re-run, so an interrupted apply resumes from the
   manifest rather than re-prompting.
4. **Verify** — run the [coherence](../guardrails/validation.md) kind and confirm wiring; surface
   bootstrap status (protected, or deferred-and-nagging). A **hard coherence finding pauses the apply phase**
   — the engine never proceeds on inconsistent wiring — and surfaces, in plain language, *what* is
   inconsistent and one concrete next action (retry after a repair, or abort and report); because apply is
   resumable from the manifest checkpoint, neither choice loses the operator's selections. Broken wiring is
   never made the silent operating baseline ([principle §5](../../../principles.md): degrade loud and
   consented, never silently inert). Validation owns the coherence kind and its message; provisioning owns
   this first-run pause-and-resume UX and its plain-language framing.
5. **Retire** — self-delete the orchestrator and genuinely first-run-only assets. The `engine-setup`
   skill and permanent setup dispatcher are expressly **not** retirement assets: they are the durable
   operator path for later configuration. **First-run retirement is
   reference-closed** (the *travel-safety* invariant): no file that *survives* this step may
   statically reference a **retired** first-run asset — by `import`, `importlib`, a subprocess
   invocation of its path, or a hard-coded read of a retired file's path. A surviving file that
   needs such machinery **is itself a first-run asset** (retired in the same pass) or is removed;
   there is **no "guard the reference instead" exemption**, because a static check cannot certify
   that a guarded reference keeps a generated repo's first CI green — a top-level
   `try/except ImportError` still red-fails when a test body later names the absent module — so
   blessing a guard would dress an unverifiable guard as enforcement ([principle §7](../../../principles.md)).
   This closure is the property that keeps a generated repo's **first real PR** green where the
   instantiator no longer exists; a **hard CI closure check** ([validation](../guardrails/validation.md))
   enforces it. Validation owns the check and its plain-language message; provisioning owns this
   invariant and is its definition-of-record.

Abandon before confirm → no manifest → the next session re-offers everything; abandon mid-apply →
the manifest exists → the next session resumes applying idempotently.

**A brand-new copy is surfaced, not left silent.** A fresh generated copy is unprovisioned by the
verdict above, but nothing would otherwise tell its first session so — onboarding would depend on the
operator already knowing to run setup. The same detect-relay split as the strand detector closes
this: provisioning owns the **standing first-run detector** — the two-signal conjunction above, a
downstream copy whose setup tool is still present — and [boot](../lifecycle/boot.md) surfaces it as
a **standing, ledger-collapsed** offer to
walk first-run setup, persisting every session until setup actually runs so a deferred "later" never
silently strands a half-set-up repo. Boot owns the operator wording and the offer; provisioning owns
the mechanism. The construction repo's own sessions are **excluded by the same seam** — there the
origin *equals* the recorded home, so the detector never fires; no separate construction sentinel
exists as built, the origin-versus-home comparison having replaced the earlier marker-file idea
([D-277](../../../adr/0277-litigate-engine-template-353-first-run-dead-on-arrival-in-a.md)), and the
exclusion needs no residue cleanup because the committed manifest legitimately travels. One shape the
two offline signals cannot tell from a fresh copy is a **contributor's fork of the engine's own home**
(origin differs, setup tool present — on disk the two are identical); the build separates that case
**online**, by a best-effort token-gated read of the repo's fork parentage, so a fork is not nagged as
an adopter — and where no token is available the offer still shows, a read-only, low-harm residual the
detector's own header names.

**Provisioning runs before the engine's own local guardrails exist.** The exploration
write-gate is a `PreToolUse` [hook](hooks.md) that [modes](../lifecycle/modes.md)
registers via the closed `hook` seam directive; a hook absent from `.claude/settings.json` cannot
fire, so the instantiator operates **inherently ungated** until its own apply phase installs that
hook. Gate-installation-at-retirement is therefore the boundary between *setup* and *operation* —
provisioning is a pre-operational setup phase, not a fourth operating mode, and modes' three
stances are untouched. The exposure is bounded by **resumability and reviewability**, not merely by
the absence of a protected branch: first run is interactive (the operator is present), an interrupted
run re-enters idempotently from the manifest checkpoint, and on brownfield the instantiator's changes
to a live tree are surfaced and reviewable before they land (the collision check above, then the merge
wall). On greenfield there is no pre-existing product to corrupt. (The write-gate itself is a strong local default,
not an absolute wall — see [hooks](hooks.md) fail-open; the durable enforcement is always
the protected-branch human gate.)

### Identity and tokens

Identity is **derive-first, with no template token substitution** — the tree carries no placeholder
tokens to fill. A repo's coordinates (owner, name, default branch) and the
operator's handle are read from `gh`/git at first run — true for a template-generated repo and a
brownfield repo alike — so the **only prompted input is the identity tier**. What first run derives
and keeps becomes **operator config**: the handle (captured in the apply phase for the one identity
render, the CODEOWNERS block) and the derived default-branch name (persisted for the
checkout-health reads) are preserved across upgrades, never re-derived destructively by an overlay.

The operator handle is preserved config; the CODEOWNERS ownership block is **derived** from
*(engine-owned path set × handle)* ([principles §3](../../../principles.md)), so an upgrade
re-renders the block with the release's engine paths while preserving the operator's handle. The
path set is the one defined under *CODEOWNERS and the ruleset* below.

The **identity tier** names the commit identity and the merge gate
([control-plane](control-plane.md)):

- **Solo (default)** — the engine commits as the operator; the enforced gate is the automated
  required checks; the merge click is informed consent.
- **Team** — a distinct engine identity (bot/App) authors commits, so the operator becomes the
  enforced code-owner reviewer.

Tier is **not frozen at instantiation**: an operator can move solo → team later via a permanent
operator-privileged operation (introduce the distinct identity, turn on required reviews). On
brownfield the instantiator **recommends team when it detects an existing team** (a multi-owner
CODEOWNERS, existing required-reviews, org/team membership), surfaced with its one-line rationale
("others already review here, so the engine will commit as a separate identity and require
approval") — a recommendation, not a seizure of the choice.

The tier also sets the engine's standing privilege surface. Solo means the engine commits as the
operator and inherits the operator's `gh` scopes — including the standing **`repo`** that carries
ruleset administration (already in hand in the common case, not freshly granted) — so the
guardrail-integrity law ([principles §15](../../../principles.md),
[D-051](../../../adr/0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md)) extends to the ruleset itself: a weakening change to enforcement
config or the ruleset hard-blocks the merge until the operator's informed consent. The inherited
capability is the operator's *whole* standing `repo` (full control over the repositories the operator
already owns), not a ruleset-only scope, so the settings-tampering surface is named at its true breadth
rather than understated. Team
means the engine commits as a bot that never holds that standing capability, which **structurally
closes** the ruleset-tampering vector — the *cannot weaken at all* tier §15 names. Lowering the
friction of this team-identity setup is therefore the path to a structural option for a solo operator.
The one-time bootstrap is operator-privileged-human in both tiers; only the *standing* commit identity
differs.

### The native permission-mode default

The Engine recommends Claude Code's **plan** permission mode as the interactive default inside an
Engine-managed repo — the safe first-touch [modes](../lifecycle/modes.md) defines (recommended,
not the guarantee; the Explore gate + merge wall are that). Provisioning owns the **mechanism**, and it obeys
the **yield-to-the-operator** law:

- **Detect, read-only.** The instantiator reads the operator's existing interactive `defaultMode` from the
  operator's own settings (`~/.claude/settings.json`; on brownfield also any pre-existing project settings)
  — and **never writes `~/.claude`**: the operator's global settings are the operator's, and an engine write
  there is illegitimate. This keeps "install never clobbers existing user settings" true for the scalar case
  as well as the file.
- **Decide, writing into the project as operator config.** With no conflicting preference (or one already
  `plan`), the instantiator **adopts** plan by default — writing `permissions.defaultMode: "plan"` into the
  committed project `.claude/settings.json` with a plain-language **disclosure** (an affirmative "you're set
  up — here's what that means and how to change it"). When the operator already runs a different mode it
  **offers** adopt-or-keep (the only added first-run prompt); **keep writes nothing** — the project key stays
  unset, so the operator's own setting governs in this repo (the **yield**). The written value is **operator
  config** — derive-first's sibling, an operator decision persisted — preserved across an overlay like the
  operator handle.
- **Disclosed, non-weakening.** The write is surfaced in plain language as **ergonomics, not enforcement** —
  it changes no guardrail (the Explore gate and merge wall stand; [§15](../../../principles.md) untouched) —
  the same disclosure posture as the tool-runtime consent and the pre-bootstrap explanation. The copy is a
  build-spec leaf.

The committed value then travels with the repo as a deployment property; a different user working in that
repo overrides it locally via `settings.local.json` / `/config` (the [modes](../lifecycle/modes.md)
travel-semantics law). This is provisioning *mechanism* — modes owns the law; the
[control-plane](control-plane.md) locks no part of it ([D-185](../../../adr/0185-authorize-a-two-foundation-re-litigation-ship-a-native-plan.md)).

### The conduct operator-override seed

The [conduct](../surfaces/conduct.md) surface ships universal-default *codes of conduct* in
`core`'s `provides` (`.engine/conduct/defaults.md`, overlaid on upgrade). The **operator override**
(`.engine/conduct/operator.md`) is the operator's own standing stance, and provisioning owns its first-run
**seed** and its cross-overlay **preservation** — the seed-then-own pattern, the same shape as the native
permission-mode default and the operator handle:

- **Seed at first run, from the template's carried seed.** The maintainer authors their codes of conduct once
  in their template (a committed seed the template carries), so every repo generated from that template starts
  with them: Apply copies the seed into the committed `.engine/conduct/operator.md`. The **public** template's
  seed may be empty — a third party generating from it without the maintainer's seed gets the universal
  defaults plus an empty override they fill themselves. Greenfield copies the seed; brownfield does the same
  over the overlaid tree. An absent seed yields an empty override, never an error. The seed is **disclosed** to
  the operator in plain language at first run (the stance is present and theirs to tune) — the same
  non-weakening disclosure posture as the native permission-mode default.
- **Operator-owned thereafter, preserved across overlay.** Once seeded, `operator.md` is **operator config**
  — in no module's `provides` — so the engine-upgrade overlay never overwrites it (*Upgrading the engine*
  below), exactly as the per-instance eADR stream and the operator policy-override are preserved.
- **Authored by a verb, promotable to the seed.** The operator adds, revises, or retires a code of conduct
  through the [core](../../modules/core.md) **conduct-authoring** verb (the prose counterpart of
  policy-tuning), and an optional command **promotes** a code of conduct learned in one repo back into the
  maintainer's template seed so it rides future repos. Direct edit is allowed (legible prose), backstopped by
  the [validation](../guardrails/validation.md) weakening guard and the merge review.

This is provisioning *mechanism*; [conduct](../surfaces/conduct.md) owns the surface law, and the
seed-file path/format and the promote command's wording are build-spec leaves ([D-192](../../../adr/0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md)).

### Tool-runtime bootstrap

The engine's tools are Python and run in an engine-namespaced, uv-managed **tool-runtime**
([topology](repository-topology.md), [surfaces/tools](../surfaces/tools.md)): the
committed `.engine/pyproject.toml` + `.engine/uv.lock` materialized by `uv sync` into a gitignored
`.engine/.venv/`. The instantiator materializes it in the apply phase, before substrate init and its own
coherence run (both Python), so the tool-runtime precedes even the engine's own validators. This is
provisioning *mechanism*; the [control-plane](control-plane.md) locks no part of it.

- **uv is auto-bootstrapped behind an operator consent gate — a heavier trust class than the
  control-plane scope grant, and framed as such.** That grant is a *permission* on github.com; this is
  **software placed on the operator's machine plus a package fetch**, so the consent cannot borrow the
  OAuth screen's familiarity. If uv is absent the instantiator offers to install it from the **official
  Astral source, pinned to a known version**, and on the operator's approval installs it
  **PATH-independently** (`UV_NO_MODIFY_PATH`, into an engine-known location) and invokes it by
  **absolute path** thereafter — it never edits the operator's shell profile and never relies on a login
  shell's `PATH` (which a non-interactive [hook](hooks.md) shell may lack). The engine **cannot
  install silently**: the consent screen is the gate, consistent with the merge-as-consent model.
- **`uv sync` is group-scoped.** Each dep-carrying module's Python dependencies are declared as a
  [dependency-group](../../../reference/glossary.md) in `.engine/pyproject.toml` **named by the module's `id`** (also
  its `.engine/modules/<id>/` directory name); the module manager derives the sync selection by matching
  those group names to the present manifest ids **under PEP 735 name normalization**, and a module with no
  Python dependencies declares no group. The mapping **reuses the `id` the manifest already carries — it
  adds no manifest field** (the [module-system](../grammar/module-system.md)
  derived-not-registered shape). So `.engine/.venv/` carries only selected capabilities' dependencies and a
  deselected extension ships no live dependency surface (*installed means present*). A deselected extension's
  dependencies remain *resolved and named* in the committed `uv.lock` (one resolution, universal across
  platforms and all groups) but are **never installed** into `.engine/.venv/`, so the residual is a static
  lockfile listing, never a live or importable surface. A standing **hard CI check** (`uv-group-drift`)
  regenerates the derived group selection from the installed module set and reds on drift, so the
  mapping cannot silently rot. **One seam is designed but not yet settled** (kept as intent,
  operator-ruled in the wave-5 reconciliation): no grammar yet exists for a dependency **shared by
  two modules** — as built, the memory substrate's `mcp` dependency rides `core`'s group, undeclared
  by the module that imports it, a coupling the drift check structurally cannot see. The grammar
  ruling is tracked upstream as
  [engine-template issue 783](https://github.com/StarshipSuperjam/engine-template/issues/783).
- **The `.engine/.venv/` ignore is a foundation `.gitignore` block**, applied by the wiring library's
  comment-fenced-block **helper** — the CODEOWNERS precedent (a library helper, **not** a module
  `gitignore` seam directive): it carries no manifest `wires` entry and is outside coherence's wiring
  and file-ownership legs ([module-system](../grammar/module-system.md)). It is a **distinct,
  separately-keyed fence** from any module `gitignore` block in the same file, so a module's uninstall
  reverser — which removes only its own manifest-declared lines — never touches it, and no coherence leg
  reads it as undeclared module wiring. The same foundation block also fences **`.claude/worktrees/`** — the
  platform's per-session worktree directory — so the operator-checkout-strand pre-check (below) reads a clean
  main tree and the operator's own `git status` is not polluted by sibling sessions.
- **Degrade loud, never fake, never to system Python** ([principles §5/§7](../../../principles.md)).
  Where uv cannot install or `uv sync` cannot fetch (offline, a download-blocking network, an unsupported
  platform), the engine does **not** fall back to the operator's system Python — that would reintroduce
  the coupling the runtime exists to remove. At first run the instantiator is present, so it surfaces the
  failure in plain language with an engine-offered **retry** (most causes are transient) and, when it
  persists, the likely cause plus that the engine finishes setup automatically once it can reach the
  source — never a dead-end. Across later sessions [boot](../lifecycle/boot.md)'s committed
  `CLAUDE.md` floor keeps orienting the operator even when the runtime is fully absent — it is
  interpreter-independent — though that floor **orients only**; the runtime-specific retry is offered
  wherever the engine can still run it (the boot pack's missing-runtime surfacing when the runtime is
  present-but-degraded, the module manager's re-materialize otherwise). The honest, named bound: until the runtime materializes, the engine's Python
  tools cannot run, so a repo where it never can is **inoperable** by the operator's informed acceptance
  (Risk [R18](../../../reference/risks.md)) — surfaced-and-accepted, exactly as an un-bootstrapped control-plane is,
  never silently degraded.

### Control-plane bootstrap

The branch ruleset is a setting, not a file, so it does not travel and must be applied once. The
[control-plane](control-plane.md) locks the *contract*; provisioning owns the *mechanism*.

- **Actor: the operator's own local `gh`, engine-orchestrated.** The instantiator checks for
  repository-administration capability — the `repo` scope on a classic token, or **Administration:
  write** detected by a write-probe for a fine-grained token. **In the common case the operator's `gh`
  already carries `repo`, so no grant is needed** and the engine applies the ruleset directly; only if
  the capability is absent does the instantiator trigger `gh auth refresh -s repo` and the **operator
  approves the GitHub authorization screen** — no command to cut and paste. The engine **cannot grant
  itself** the capability; the authorization screen is the consent gate, consistent with the
  merge-as-informed-consent model. When a refresh is needed the browser/web flow is preferred and the
  capability is **verified present after the refresh**, because some device-flow paths can complete
  authorization without persisting the scope; if it is still absent, the bootstrap falls through to the
  loud-degrade path rather than assuming success.
- **A plain-language explanation precedes any authorization screen** (it appears only on the rare
  refresh path) — what is being requested and why (it turns on the review gate that makes the engine
  safe to trust), stated before the screen appears, and **pre-translating the actual on-screen label
  the operator will see and pre-empting its apparent breadth**: the screen describes broad repository
  access, so the explanation says up front that this breadth is the standard GitHub permission for
  turning on the review gate, scoped to repositories the operator already controls — so the label never
  arrives uninterpreted at the moment the operator must act. The pre-emption matches the label's felt intensity — the screen reads as
**sweeping, full-control-sounding** access, so the explanation must defuse that wording, not a milder
paraphrase of it. (The exact current label is a
  Build-spec-leaf detail re-verified against the live platform at build, never a dated string baked
  into this doc.)
- **Attempt now, but defer is the common path.** The bootstrap is attempted during the instantiator's
  apply phase, but the instantiator **retires regardless** of whether protection was applied. The
  bootstrap logic lives **permanently in `.engine/tools/`** as a re-runnable operation, so it survives
  the instantiator's retirement and the operator can complete it any time. The committed **fail-loud CI
  guard** (per pull request) and the **boot orientation** (continuous, and the primary surface at first
  run when no pull request exists yet) keep an unprotected repo loudly visible until protection lands.
  The surfacing split is clean: the instantiator runs the single first-run attempt and surfaces *its*
  outcome in plain language — **including a positive "your review gate is now ON" confirmation when the
  attempt succeeds**, because the common path (the operator already holds `repo`) applies protection
  with no extra authorization screen, so the success must be stated or the single most trust-critical
  step of first-run would land invisibly and the operator could not tell *protected* from *skipped*;
  the **standing** unprotected-state surfacing across every later session — and the offer to
  complete protection — is [boot](../lifecycle/boot.md)'s, as its locked orientation already
  defines. Control-plane owns the contract, provisioning the mechanism, boot the standing surface.
- **Degrade, never fake.** Where the operator genuinely cannot obtain the scope, the engine discloses and
  degrades — it never pretends the gate is on. The degraded state is a **standing, plain-language operator
  banner** naming the concrete risk ("branch protection is not active — work can merge unreviewed") and a
  concrete next action **matched to the cause, never a dead-end**: if the operator does not administer the
  repo, forward the one-time setup to whoever does; if the operator administers it but an org policy blocks
  the scope, the structural escape is the **team identity** (a bot that holds enforcement-admin — see
  *Identity and tokens*), failing which the banner stands honestly and protection remains off by the
  operator's informed acceptance. The disclosure is never only a line in boot output.
- **The label, and the two-phase brownfield binding.** The bootstrap's verify step also **ensures the
  engine-domain label exists** (inheriting the first producer's minimal ensure — the engine never makes
  the operator hand-create a label; the [control-plane](control-plane.md) owns the scheme). And a
  **brownfield arrival binds protection in two phases**: the engine's own workflows arrive *inside* the
  arrival pull request, so binding their required checks at arrival would make that pull request
  unmergeable. The arrival therefore applies a **checkless** floor — pull request required, no
  force-push, no deletion; tier-aware, augmenting and never weakening a product's existing rules — and
  after the merge a one-time **finalize** verb (a permanent primitive that survives the instantiator's
  retirement) confirms both engine workflows are on the branch — refusing fail-closed rather than
  re-create the deadlock — then binds the required checks and re-emits the Actions-enablement reminder.
  The standing CI guard keeps reporting honestly during the window: it always evaluates the full
  required-check floor, so the not-yet-bound checks stay visible rather than green-lit.

### Actions enablement and repository behavior

Two further GitHub-side apply steps ride beside the bootstrap:

- **Actions enablement is told, never automated.** A repo created via "Use this template" has workflow
  runs gated behind the owner's explicit click on the Actions tab; until then the required checks the
  bootstrap just bound never start, and no pull request — including the setup one — can merge. The API
  cannot perform that click, and no detection signal is honest in exactly the deadlock state
  (GitHub-managed scan runs appear in the runs listing while real workflows stay gated, and past run
  history proves Actions worked once, never that it can run now) — so the step **tells the operator,
  unconditionally**, with the message carrying its own already-on branch ("if the tab shows no enable
  button, you're done") so telling is never misleading.
- **Repository-behavior settings.** The apply turns on delete-branch-on-merge, the pull-request update
  button, and Dependabot alerts with automatic security-fix pull requests; on a fresh repo only, it
  turns off the project wiki — and project boards when the projects-sync module is not installed
  (retained when it is). Same posture as the security floor beside it: the same operator-privileged
  transport (no new capability), verify-after-write, degrade-never-fake with a plain-language
  disclosure, augment-never-override — on brownfield the turn-offs are skipped, since hiding an active
  project's wiki would be an override — and never a required merge check.

### The security floor: native-scanning toggles and the SECURITY.md seed

The [control-plane](control-plane.md) locks the security-floor invariant (native where the tier
supports it, disclose-never-downgrade); provisioning owns the mechanism. The native toggles **reuse the
operator-privileged `gh` the ruleset bootstrap already holds** — the standing `repo` / Administration: write,
the common no-grant case — so they add **no new capability**, and the seed is a file copy in the apply phase.

- **Enable native scanning where the tier supports it; branch on the call's status; never fire-and-forget.**
  At the bootstrap the instantiator enables **CodeQL code scanning** (default setup — GitHub-managed, no
  committed workflow) and, on a **public** repo, **private vulnerability reporting**, each by a single
  operator-privileged `gh` call against the repository's code-security / PVR settings (the endpoints + request
  shape re-verified against live GitHub at build — [constraints](../../../reference/constraints.md)). The call's **HTTP
  status is read and branched**: applied → a plain-language confirmation; **unsupported** (a free private repo
  cannot enable code scanning; PVR does not exist for private visibility) → **skip and disclose**, never
  reported as on; **transient** → retry-or-disclose. The engine never reports a feature enabled when the
  enabling call did not succeed. Native code-scanning alerts are advisory ([control-plane](control-plane.md)) —
  provisioning adds **no required-check binding** for them, so a finding never gates a merge.
- **Disclose the drawback; never auto-switch visibility.** Where a native feature is unavailable the operator
  is told, in plain language, what is off and what would unlock it (make the repository public, or add the
  paid Code Security tier) — the security-scanning-tier disclosure leaf below. The engine never changes the
  repository's visibility to unlock a feature; the choice stays the operator's.
- **Seed a root `SECURITY.md`, operator-owned, only if absent.** Apply copies the template-carried seed into a
  **root** `SECURITY.md` (the seed-then-own pattern, the same shape as the conduct override) so every repo
  carries a vulnerability-disclosure channel — the channel that matters most on a private repo, where native
  PVR cannot exist. It is **operator config in no `provides`**, at the repo root (product territory), so the
  engine-upgrade overlay preserves it under *product paths are never touched* with **no carve-out**. On
  **brownfield** the collision check surfaces a product's pre-existing `SECURITY.md` in **any** recognized
  location (root, `.github/`, or `docs/`) and the engine does **not** overwrite it — it seeds only where none
  exists. An absent template seed yields a minimal default file, never an error. (A product's later-added
  `.github/SECURITY.md` takes GitHub precedence over the root seed; both are operator-owned product files, so
  the outcome is the operator's, never an engine concern.) The seed is **disclosed** at first run in plain
  language — a vulnerability-disclosure file was added at the repo root — the same non-weakening posture as the
  conduct seed.

This is provisioning *mechanism*; the [control-plane](control-plane.md) locks the invariants, and
the concrete `gh` calls, the status-branch handling, the seed file's content, and the disclosure copy are
build-spec leaves (below) ([D-212](../../../adr/0212-resolve-the-d-211-security-floor-re-litigation-landed-text-c.md)).

### The root README: the landing front and the product-starter seed

The repo's root `README.md` leads a double life ([topology](repository-topology.md) law 2): at rest
in the **template** it is the engine's **marketing landing front** — the page a potential adopter reads on
GitHub to decide whether to deploy the Engine — while in a **generated** repo the root README is the
**product's**, never the engine's ([engine/product wall](repository-topology.md)). Because "Use this
template" copies every committed file, the marketing front **travels** to the generated repo's root, which
topology reserves for the product; provisioning reconciles the two by seeding the product's own starter over
the traveled front at first run. This seed is the writer the project-README disclosure ([D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md))
always implied but never named.

- **Replace the marketing front with a product starter — only where the slot is the engine's own seed.** Apply
  writes a **product-owned starter `README.md`** at the repo root, but **only iff the current root README is
  still the engine's recognizable marketing landing seed**. This one predicate makes the operation safe in every
  case: on **greenfield** the slot holds the traveled marketing front (engine-authored, not operator content) →
  it is replaced; on **brownfield** the slot holds the product's own README (not the marketing seed) → it is
  **preserved untouched**, the same outcome the `SECURITY.md` seed-if-absent rule gives; on any **re-run or later
  engine overlay** the slot no longer holds the marketing seed (it holds the product starter, or the operator's
  edits) → the step is a **no-op**, so the engine **never re-touches the root README after instantiation** and
  operator edits are never clobbered. How the engine recognizes its own marketing seed is a build-spec leaf below;
  the recognizer is **conservative** — it fires the replace only on a positive match to the engine's own shipped
  landing seed (carried with a recognizable engine marker or content fingerprint) and **preserves on any doubt**,
  so operator-authored content is never replaced, even at the cost of leaving a stale engine front the operator can
  overwrite by hand.
- **The product starter carries the required-spine disclosure, in plain operator language.** The starter is a
  minimal **product** placeholder — a project-name/purpose stub the operator and Engine fill in as the product
  takes shape — that also discloses, per [D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md), the always-present `required` spine
  (the core packages, the routine stance, the self-checkups) and any v1 gaps the packaging model records (e.g. the
  no-automated-style-floor disclosure that names `clean-code`, [D-095](../../../adr/0095-cut-expression-contracts-disposition-prose-organization-cove.md)). It is written
  in plain operator language — the engine *remembers across sessions and keeps work safe*, built in, not an add-on,
  never "the memory package is required" ([D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) disclosure law). It is **operator config
  in no `provides`**, at the repo root (product territory), so the engine-upgrade overlay preserves it under
  *product paths are never touched* with **no carve-out** — the same ownership as the `SECURITY.md` and conduct
  seeds.
- **The seed/replace is disclosed at first run.** Apply tells the operator, in plain language via the
  [operator-presentation relay](../../../reference/glossary.md), that the engine set the project's root `README.md` (and, on
  greenfield, replaced the Engine's landing front with a starter for *their* project) — a visible-file change is
  never silent, the same non-weakening posture as the `SECURITY.md` and conduct seeds.

This is provisioning *mechanism*; [topology](repository-topology.md) law 2 anchors the ownership
(product-owned, engine-seeded-once), and the **product-starter content**, the **recognizable-marketing-seed
predicate**, and the **disclosure copy** are build-spec leaves (below) ([D-214](../../../adr/0214-resolve-the-d-213-front-door-re-litigation-landed-text-cold.md)).

### The root LICENSE: clearing the traveled template license

The repo's root `LICENSE` leads a double life like the README ([topology](repository-topology.md) law 2):
at rest in the **template** it is the engine's own license (the maintainer's copyright), which makes the public
template repo legally usable; in a **generated** repo the root LICENSE is the **product's**, never the engine's
([engine/product wall](repository-topology.md)). Because "Use this template" copies every committed file,
the template's LICENSE — carrying the *template author's* copyright — **travels** to the generated repo's root and
would govern the **adopter's own product** until replaced by hand. Provisioning reconciles this by **clearing** the
traveled license at first run, seeding no replacement: a license is the adopter's legal choice, not the engine's to
make.

- **Clear the traveled license — only where the slot is the engine's own seed.** Apply **deletes** the root
  `LICENSE`, but **only iff it positively matches the engine's own shipped template-license seed**. The recognizer is
  **not** the README's marker — a `LICENSE` must stay stock text for GitHub / SPDX license detection, so it cannot
  carry an engine comment — it is a **conjunction**: the license body matches the engine's shipped seed **and** the
  seed's **distinctive template-author anchor** still names the **template author** — the copyright-holder line
  under a holder-bearing license, or, under the current Apache-2.0 + Commons Clause seed whose Apache body is
  holder-less boilerplate, the **Commons Clause licensor/product field** (the Apache body alone could not
  distinguish an adopter's own independently-chosen Apache `LICENSE`) — not the operator identity apply has
  already derived, evaluated **before** any identity rendering could rewrite that anchor; **conservative —
  preserves on any doubt** (fails toward keeping). This makes the operation safe in every case: on **greenfield** the slot holds the traveled
  template license (the template author's, not the operator's) → it is cleared; on **brownfield** an engine overlay
  places only `.engine/` + keyed entries ([topology](repository-topology.md) law 1), so a root LICENSE
  never lands — there is nothing to clear, *and* a product's own LICENSE never matches the recognizer; on any
  **re-run or later overlay** the slot no longer holds the engine seed → the step is a **no-op**, so the
  **first-run clear never re-touches the root LICENSE after instantiation** — the only post-instantiation touch is
  the standing detector below, a separate, reviewed-PR path (not this genesis-time clear).
- **No replacement — the license is the adopter's choice.** The engine seeds **no** license; the generated repo is
  left with no `LICENSE`, GitHub's documented default-copyright state, which the adopter changes by adding their own
  when ready (the Engine can *add* a license the operator picks, never *choose* it for them). A seeded placeholder is
  rejected — any license file the engine writes is the engine choosing the product's legal terms, a foreign artifact
  in product territory a downstream tool could misread. A maintainer who *genuinely intends* adopters to inherit
  license terms ships them as an **explicit authored template choice** (the seed-then-own pattern), never the silent
  default — the clear protects the unknowing adopter, the override serves the deliberate maintainer.
- **The clear is disclosed at first run — factual, never legal advice.** Apply tells the operator, in plain language
  via the [operator-presentation relay](../../../reference/glossary.md), that it **removed** the traveled license and **why**
  (it carried the template author's copyright and would have governed *their* product), that it added **no**
  replacement (the license is theirs to choose), and **leads with the private-by-default reassurance** (a new project
  with no license is the normal, safe starting state — their code is theirs until they choose to share it). It
  **routes the judgment out** — GitHub's `choosealicense.com` guide, an offer to *explain what a license file is and
  help add the one they pick*, and a human for terms that matter — and is **factual, never counsel**: the engine
  states what it did and the documented default, never "all rights reserved" as a legal conclusion (false for a public
  repo, which GitHub's ToS leaves viewable and forkable) and never which license to choose. It pre-empts the GitHub
  "No license" label so a later sighting is expected, not alarming. A visible-file change is never silent — the same
  disclosure posture as the `SECURITY.md` and README seeds (a disclosure standard, not a [§15](../../../principles.md)
  guardrail — a LICENSE is not a guardrail).

This is provisioning *mechanism*; [topology](repository-topology.md) law 2 anchors the ownership
(product-owned, the engine clearing only its own traveled seed), and the **template-license recognizer** (the
body ∧ distinctive-template-author-anchor conjunction, per-era, and — for the standing detector below — spanning
the historically-shipped seed set) and the **factual disclosure copy** are build-spec leaves. The
**sequencing gate** — the clear ships with or before any committed template LICENSE, so no window leaves a generated
repo carrying the foreign copyright — remains a build-owe ([R29](../../../reference/risks.md), [D-221](../../../adr/0221-authorize-the-first-run-license-clear-re-litigation-reconcil.md));
the **standing remedy for a repo generated before the clear shipped, or drifted back to the seed** is the
foreign-`LICENSE`-seed detector below — designed under
[D-302](../../../adr/0302-litigate-engine-template-471-design-the-standing-foreign-lic.md) and **built**
(the upstream tracker that demanded it is closed).

### The root LICENSE: the standing foreign-seed detector

The first-run clear fires **once**, at instantiation. Two residual populations escape it: a repo **generated
before the clear shipped** (still carrying the traveled seed), and one that **drifted** the seed back into the
slot. The standing remedy is a **boot-invoked detect-and-offer** — the same detect (provisioning) / surface (boot)
/ consent (operator) split as the operator-checkout strand detector below, and the same
[R20](../../../reference/risks.md) stranded-checkout pattern **at detection and surfacing**, though its **fix diverges** (a
reviewed pull request, not a direct write — see below). The detector is enumerated in
[modules/core](../../modules/core.md)'s `provides`, and its post-instantiation product-root touch is
authority-anchored in [topology](repository-topology.md) law 2's standing exception.

- **A standing, re-runnable `.engine/tools/` check boot invokes** in its `SessionStart` pack — not a new cadence,
  not a daemon ([§8](../../../principles.md)): provisioning owns the mechanism, boot owns when it surfaces. From
  the session's worktree it resolves the main checkout (`git worktree list` / `--git-common-dir`) and reads the
  **committed** root `LICENSE` (`HEAD:LICENSE`) **locally, offline** — the committed file is what governs the
  product and what a reviewed removal changes (an uncommitted working-tree edit is neither), so reading `HEAD`
  keeps the fire/resolved verdict honest; a strict subset of the strand detector's own read.
- **The recognizer is the first-run clear's, widened across releases.** It fires only on a **positive self-seed
  match** — the engine's *own* shipped template-license seed — never on "a copyright the engine guesses is not the
  operator's": the engine holds **no notion of the operator's legal identity, only its own seed** (a build
  constant), which dissolves the identity problem the naive framing raised. Because a repo running this detector
  has necessarily **upgraded** to a newer engine whose *current* seed may differ from the one it was generated
  under ([D-295](../../../adr/0295-engine-template-s-own-license-moves-mit-apache-2-0-commons-c.md) moved the seed MIT → Apache-2.0 + Commons Clause), the standing
  recognizer matches the **append-only set of all historically-shipped seeds** — each a `(body-fingerprint,
  distinctive-template-author-anchor)` pair — not just the current one; a current-seed-only match would be blind
  to the very pre-clear population the detector exists for. Conservative, **preserve-on-doubt**: an edited anchor →
  no match → no fire, so a product's own `LICENSE` and a deliberately-inherited license (the seed-then-own
  override) are structurally never touched.
- **On consent the removal lands as a reviewed change, not a boot-time write.** The first-run clear was a
  genesis-time deletion riding the initial provisioning commit, *before* branch protection existed; a standing
  repo is fully provisioned and **branch-protected**, and the harm is the **committed** `LICENSE` governing the
  product — so a durable, protection-compatible removal must reach the default branch through the **reviewed pull
  request** the engine's whole change model already uses ([build-orchestration](../lifecycle/build-orchestration.md)),
  the operator's **merge** the consent. A boot-time working-tree delete is rejected: it is non-durable (the
  committed file remains and re-materializes in the next worktree) and it dirties the operator checkout — tripping
  the strand detector's own losslessness precondition. So boot **offers**; the operator's consent is a **plan
  acceptance** — the sanctioned operator-only Build entry ([modes](../lifecycle/modes.md): leaving
  Explore is a deliberate human act, by typed verb *or accepted plan*) — which flips the stance to Build and hands
  the one-file removal (scoped **`LICENSE`-only**) to [build-orchestration](../lifecycle/build-orchestration.md)'s
  **trivial fast path** (orchestrator-inline, no Issue, headline-only plan gate). Boot itself stays **read-only**
  and never enters Build on its own; the engine **never auto-fires** the removal, and absent consent does nothing
  beyond the standing surfacing. The detector reads the license state only from `HEAD` (`HEAD:LICENSE`, not the
  working tree or a PR branch) and **dedupes against an already-open scoped `LICENSE`-removal PR** — while one is open it re-words the surfacing to *a cleanup is
  prepared, awaiting your merge* and opens no duplicate; and after a merge the **local** main `HEAD` may briefly
  lag `origin` until the checkout next syncs (the never-strand floor does not auto-update it), so the offer can
  persist a boot or two against an already-removed file — a **named, bounded residual** ([R29](../../../reference/risks.md))
  that clears on sync, a re-consent in that window resolving to an empty-diff no-op, never a second removal. This
  is where the standing remedy **diverges** from the strand fix: the strand fix realigns the checkout to
  *already-committed* history and needs no new default-branch commit, whereas the re-clear **adds** history (a
  deletion of a committed file) and so rides the reviewed gate.
- **Boot surfaces and offers it** at the open-findings tier, **below** the governance-critical alarms (a foreign
  copyright is a bounded, operator-correctable [R6](../../../reference/risks.md) residual, not guardrail-critical), reusing
  the first-run clear's **factual-never-legal-advice** disclosure spine and its private-by-default lead — framed as
  *provenance* (a file copied in from the template, not a defect in the operator's project). See
  [boot](../lifecycle/boot.md) for the surfacing, framing, and anti-habituation (including the
  kept-on-purpose intent-exit).

The **historical-seed set** and the per-era **distinctive-author anchor** (the MIT copyright-holder line; the
Commons Clause licensor/product field under the current seed) are build-spec leaves, as the first-run recognizer
is.

### CODEOWNERS and the ruleset

Both the CODEOWNERS file and the branch ruleset must coexist with a product's own — the brownfield
requirement, but also a plain upgrade requirement (an operator may add their own CODEOWNERS rules
after first run, and an overlay must not clobber them).

- **CODEOWNERS is a comment-fenced, engine-keyed block** — inserted iff absent, replaced or removed
  only as a block, never touching lines outside it (the same discipline as the `gitignore` seam). On
  greenfield the file is seeded containing only the block; on brownfield the block is appended to the
  operator's existing file. The injection is applied by the bootstrap, reusing the wiring library's
  comment-fenced-block **helper** (the code the `gitignore` applier calls) — a *library helper*, **not**
  a seam directive: CODEOWNERS is a foundational control-plane infrastructure artifact (one block for
  all engine paths, not a per-module wire). It carries no manifest `wires` entry (so it is outside
  coherence's declared-versus-applied *wiring* leg) and is a **named foundation infrastructure artifact**
  (so it is outside coherence's *file-ownership* leg, by that leg's carve-out — see
  [module system](../grammar/module-system.md)), so coherence does not flag it. Because
  CODEOWNERS is last-match-wins, the helper positions the engine block to defeat shadowing by rules
  present at injection time; coexistence with *future* product rules appended below the engine fence
  relies on the engine's paths being dot-namespaced (`.engine/`, `.github/`, `.claude/`), which a product
  glob is unlikely to target.
- **Engine ownership is derived** from the **manifest `provides` union ∪ the foundation
  infrastructure-artifact set** ([principles §3](../../../principles.md)). The `∪` is load-bearing: the
  highest-trust engine files are not in any module's `provides` — the engine manifest itself, the root
  `CLAUDE.md`, the tool-runtime's `pyproject.toml` + `uv.lock`, and the engine-owned `.github/` artifacts (the ruleset-guard workflow, CODEOWNERS itself)
  — so a bare `provides`-union wall would leave exactly those product-merge-able. The derivation yields
  correct coexistence automatically: on greenfield it covers the engine's namespaces; on brownfield it
  covers only the engine's files, leaving a product's co-occupying `.claude/` content product-owned.
- **The ruleset is augmented, never weakened.** The bootstrap adds the engine's (engine-namespaced,
  derivable) required-check names and ensures the protection floor; it never removes or weakens a
  product's existing protection rules, and it creates a ruleset only where none exists. Because the
  rulesets API replaces a ruleset object wholesale, "augment" is a **read-modify-write** — read the
  current ruleset, merge the engine check names into its existing required-check list, write the union;
  de-bootstrap reads, removes only the engine-namespaced names, writes the remainder. The read-write
  window is last-writer-wins, so the bootstrap performs it as a single close operation and re-reads on
  conflict rather than blind-writing. Where the engine *created* the ruleset on a repo that had none,
  clean removal **discloses and lets the operator choose** to keep or drop it — protection is never
  auto-deleted.

### The module manager: add, remove, upgrade

The operator sees **one engine version**; every module ships from a single tagged release. The verbs
follow from that:

- **add** (per-module) — fetch the module at the current release, copy its `provides` into their surface
  homes, apply its `wires`, run coherence. Re-adding an extension deselected at first run is this same path
  (its files were deleted), not a toggle.
- **remove** (per-module) — manifest-derived reversal: reverse `wires`, delete the engine-identified
  files, run coherence. **Distribution-aware** — it refuses, in plain language, to remove a
  `required`-distribution module (the governance-and-delivery spine is never an individual choice; only
  `extension` modules are individually removable, and whole-engine removal is its own path below —
  [D-335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md)).
  **Reverse-dependency-aware** — it also refuses to remove a module
  another present module still `depends` on. Reversal removes only the engine-keyed entry; where a shared
  entry cannot be safely keyed to the engine alone (e.g., a `permission` the operator also holds), the
  [module system](../grammar/module-system.md)'s reversal firewall **conservatively leaves it** —
  the cost of never mis-removing — so the engine is honest that clean removal can leave such residue.
- **upgrade** (engine-wide) — move the whole engine vX → vY (see *Upgrading the engine*). There is **no
  per-module update**: a newer version of a module arrives only via an engine upgrade.

**The ruleset is the exception, not the rule, for add/remove.** GitHub binds a required check by its
workflow/job **status name**, and module checks flow in and out of the stable engine CI check via
**derived suite rosters** ([validation](../guardrails/validation.md); the roster is derived,
not wired). So ordinary add/remove changes *what runs inside* the CI check — **not** the bound check
name — and needs no operator-privileged step. The ruleset is touched only when the bound *union* itself
changes: a module that ships its **own** required workflow, clean removal (which deletes the CI workflow
→ de-bootstrap), or the team-tier upgrade. When it does, the module manager owns the **bind/unbind
ordering** against the pull request so the union never requires a check absent from the protected branch
— this is provisioning *mechanism* on the operator-privileged ruleset path the control-plane already
defers here, not new control-plane responsibility.

**The engine CI check's status name is a frozen contract.** GitHub does not rebind a required check on
rename — a renamed job "waits forever" and deadlocks every pull request. Because an upgrade replaces
engine code wholesale, the required-check status name is an **invariant across versions**; a migration
may never rename it.

### Upgrading the engine

A repo generated from the template is **detached** (no upstream remote), so engine improvements do not
arrive by `git pull`. (This "detached" is the *engine-update* channel; a fork-native
[external-contribution](../lifecycle/external-contribution.md) deployment additionally carries a
**product-project upstream** — the repo it contributes to — used only for contribution, never for engine
updates.) The permanent module manager is therefore the **engine updater**, and the whole
engine is upgradeable because every unit is a **versioned package** ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)):
the foundations and the governance-and-delivery spine are `distribution: required`, and every unit carries
the [module-system](../grammar/module-system.md) deployment axes (distribution/applicability/activation)
and declares `migrations`. The committed engine manifest records the engine release and each installed
package's version.

On an operator's request to update (to latest or a pinned version):

1. Resolve **which** repository is the template: the engine's **home repository, recorded in the engine
   manifest** ([glossary](../../../reference/glossary.md) *Engine manifest*) — the single coordinate the escalate-upstream
   audit already reads for the same "template repository" ([glossary](../../../reference/glossary.md) *Escalate-upstream*)
   — and read the target from **its** GitHub releases, pinned to a tagged release; never merge an upstream
   branch, and **never fall back to the deployed repo's own `origin`** (a generated repo's origin is its own
   release-less repo). Resolution is **three-state**: home recorded and
   **resolvable** → fetch; home recorded but **unresolvable** (the named repo publishes no release, or was
   renamed or removed) → **refuse loudly, naming the home**, never a generic "unreachable"; home **absent** →
   refuse and change nothing, surfacing — in plain language **matched to the cause** — why the update cannot
   proceed and the one concrete next step, never a dead end (the operator-facing refusal copy is a build-spec
   leaf held to the [§12](../../../principles.md) leak-guard, judged in review). The home is a **preserved**
   manifest coordinate — the overlay does not refresh it, so it can go **stale**: the tagged pin and the merge
   gate catch a malicious swap at review, but a non-engineer cannot themselves distinguish a right home from a
   look-alike, so the bound is named, not hidden ([§7](../../../principles.md)/[§17](../../../principles.md)).
2. **Overlay only the engine-namespaced paths of the installed packages**
   ([topology](repository-topology.md) wall), never resurrecting a deselected `extension`. **Converge to the
   required set**: a release that makes modules newly `required` — including one an operator once declined
   while it was an `extension` — installs those modules **if absent** in the same upgrade, because declining a
   required module was never a valid state ([D-335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md)).
   The required target set is derived from the release manifest, so convergence adds exactly that set with no
   per-previous-selection migration branches and no rewrite of product-owned content; that an operator who
   declined a now-required governance module gains it here is a deliberate consequence, disclosed in the
   upgrade's pull request. Engine
   **code** is replaced wholesale; operator-owned engine **config** and gitignored **data** are
   preserved (configuration is not code). Product paths are never touched. The overlaid
   `.engine/pyproject.toml` + `.engine/uv.lock` are engine *code* (replaced wholesale). A per-deployment
   [**operator policy-override**](../../../reference/glossary.md) of tunable policy values is operator-authored config
   — operator-owned, not a derived/substituted token like the handle — and is preserved here like any
   operator config: the overlay never overwrites it ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)). The same holds
   for `.claude/settings.json`: the overlay re-applies only the engine-**keyed** entries (hook
   registrations, permission rules) idempotently and leaves operator-owned top-level scalars — the **native
   permission-mode default** among them — in place; JSON carries no comment-fence, so preservation is by the
   keyed-edit scope **excluding** operator scalars ([repository-topology](repository-topology.md)
   law 1, [D-185](../../../adr/0185-authorize-a-two-foundation-re-litigation-ship-a-native-plan.md)). The
   [contracts](../surfaces/contracts.md) surface splits the same way: the **foundational eADR
   canon** rides `core`'s `provides` (the engine-owned set), so it is replaced wholesale like engine code —
   its replacement rides this upgrade's reviewed pull request and the merge gate, so it is surfaced and
   consented, never silent, and an operator who disputes a shipped law escalates upstream rather than
   editing it locally — while the deployment's **per-instance eADR stream** is in no module's `provides`
   (deployment-authored), preserved across the overlay like operator config. The two occupy distinct paths
   under the contracts home so this engine-owned-set membership classifies them with **no content marker**
   ([repository-topology](repository-topology.md) law 5, [D-169](../../../adr/0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md)). The [conduct](../surfaces/conduct.md) surface splits the same way: the universal-default *codes of conduct* (`defaults.md`) ride `core`'s `provides` (engine-owned), replaced wholesale like engine code, while the **operator override** (`operator.md`) is in no `provides` (operator-authored), preserved across the overlay like the operator policy-override — the same engine-owned-set membership, no content marker ([D-192](../../../adr/0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md)).
3. **Re-sync the tool-runtime** — group-scoped `uv sync` rebuilds `.engine/.venv/` from the overlaid
   `uv.lock` **before migrations run in it** (migrations are Python that runs in the runtime). `uv sync`
   materializes the venv only and **never mutates a gitignored data store**, so a dependency bump that
   would reshape a store rides a normal backup-first `migration` (below), not the sync.
4. Run the packages' **migrations** in dependency order.
5. Run the **coherence** validator.
6. Land the change as a **reviewed pull request** through the [control-plane](control-plane.md)
   gate, so an upgrade is as reviewed and reversible as any other change.

It **degrades**: if the release source is unreachable, the repo stays on its current version and keeps
working ([principles §5](../../../principles.md)). Because an upgrade pulls executable engine code, it is
a supply-chain surface; the tagged pin, the coherence check, and the human merge gate are its controls
(Risk [R7](../../../reference/risks.md)). The **home coordinate itself is part of that surface** — it selects the
repository the executable engine code is fetched from — so it is a [§15](../../../principles.md)
guardrail-integrity file (the tool-runtime lockfile's sibling): a change that repoints it is a
**weakening-class change**, blocked until the operator's **weakening acknowledgment**, surfaced in plain
language ("this changes where your engine's code is fetched from — the AI could then pull code from a source
you have not reviewed").

#### Migration and reversibility

Migrations exist **because the overlay preserves config and data**: engine code is replaced wholesale
and needs no migration, but preserved operator config and gitignored substrates may need reshaping when
a schema bumps. Migrations are version-aware, run in dependency order on upgrade, and reuse the
substrate schema-version pattern.

Reverting the upgrade pull request restores **code**, but a migration that reshaped a gitignored store is
not in the pull request, so the data does not revert with it. The reversal model is therefore
**backup-first**: every data migration snapshots the affected store before mutating, reusing the automatic
operator-facing backup path that [memory](../cognitive/memory.md) owns (memory defines the
mechanism and the restore contract; provisioning is a downstream consumer). Disclosure in a pull-request
body is not a sufficient gate for a non-engineer, so the asymmetry is caught by a **migration-owned check**:
each data migration stamps its snapshot with the engine-code version it was taken at, and the comparison of
that stamp against the running engine-code version is the migration's own logic. On a mismatch after a
revert (code older than the data), it follows the protected-branch precedent — *detecting* the mismatch is
the migration's check, *surfacing* it is [boot](../lifecycle/boot.md)'s, which renders the finding
via the same open-findings path by which other substrates defer a surfacing to it, **loudly in plain
language with the exact restore command**. Boot stays read-only (it reads and surfaces, never restores) and
needs no change to carry this. Migration is never *triggered* at boot (boot never mutates); there are no
fragile inverse migrations.

The [**operator policy-override**](../../../reference/glossary.md) needs **no** migration of this kind. It is a
*committed* file, so reverting the upgrade pull request reverts it cleanly — git history is its backup, and
the gitignored-store asymmetry above does not arise. And because each consumer merges the override **per-key
over the shipped default at read time**, a value-schema change that renames or drops a key simply leaves that
key un-overridden — the consumer falls back to the new default — with the now-stale key surfaced to the
operator (a validation finding and the [boot](../lifecycle/boot.md) open-findings path) so they can
re-tune via the authoring command. No version-stamp, no snapshot, no reshaping ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)).

### Operator-checkout strand: detect and offer the un-stranding fix

The top-level [operator checkout](../../../reference/glossary.md) is meant to sit on the **default branch**, engine files
present and current; build runs in per-session worktrees ([build-orchestration](../lifecycle/build-orchestration.md)),
never in it. It drifts from that in three ways, and the engine **detects and offers to fix** each — the same
detect-relay-fix split as the protection-off bootstrap: provisioning owns the **mechanism**, [boot](../lifecycle/boot.md)
surfaces and offers, the operator consents.

- **The detector is a standing, re-runnable `.engine/tools/` check that boot invokes** in its `SessionStart`
  pack — not a new provisioning cadence; provisioning owns the mechanism, boot owns when it surfaces. From the
  session's worktree it resolves the main checkout (`git worktree list` / `--git-common-dir`) and reads its
  state **locally**. It classifies against the **default branch**, whose name the instantiator already derives
  at first run and provisioning **persists as derived config** — so classification is offline and does not lean
  on a `refs/remotes/origin/HEAD` that is frequently unset (and absent on a detached, no-remote template-generated
  repo). (The per-session worktrees live under `.claude/worktrees/`; the foundation `.gitignore` block fences
  that path, so the detector's read of the main tree is not polluted by them.)
- **Two binary *broken* states, checked every boot, offline:** a detached `HEAD`, and missing/critically-stale
  engine files (`.claude/settings.json`, `.engine/`). These are the *broken* strand states — the checkout cannot
  ground from them.
- **Parked off the main line — a gentle, offline, standing signal.** A checkout sitting on a **non-default
  branch** (not detached, engine files present) is not *broken*, but it is off the main line and — under the
  worktree-and-PR model, where Claude Desktop isolates every session in its own worktree — anomalous: the exact
  shape of the incident where a top-level checkout sat on a long-merged feature branch. It is detected **offline
  every boot** and surfaced as the **gentlest standing signal**, collapsing to one quiet line when unchanged
  (the [boot](../lifecycle/boot.md) anti-habituation ledger), so the off-main park is caught **on day
  one** — before drift accrues — without becoming nag-fatigue.
- **Behind the merged main line — the consequence-gated escalation, branch-agnostic.** Ordinary *behind* is the
  **normal** state of the checkout under the worktree-and-PR model, so the engine **never alarms on a bare
  distance**. But when the checkout is **missing merged work** — whether it sits on the default branch *or* on a
  parked side branch — the off-main signal **escalates** to a firm offer naming the felt consequence ("your
  project folder is missing the work finished since …"). This is the **opt-in, network-gated** tail: the merged
  main line lives on `origin`, current only after a fetch, so it fires only after a fetch and only on a concrete
  felt consequence, never on a bare local distance. On a **detached, no-remote** template-generated repo there
  is no merged main line to compare against, so the escalation is **uncomputable and stays silent** — degrade
  honest, never a false all-clear.
- **The un-stranding fix is lossless-or-it-does-not-run.** On consent the engine re-materializes missing engine
  files, re-attaches a detached `HEAD` to its branch, or — for the off-main/behind case — **returns the checkout
  to the default branch and brings it current** — a write to the operator checkout *permitted* because
  un-stranding is the opposite of the strand the never-strand-main floor forbids ([modules/core](../../modules/core.md))
  — and it runs **only when nothing would be lost**, decided **offline**: the working tree is clean
  (`git -C <main> status --porcelain` empty), **no operation is in progress** (no `MERGE_HEAD` / `CHERRY_PICK_HEAD`
  / `REVERT_HEAD` / `rebase-merge` / `rebase-apply`, which `status --porcelain` does **not** flag), **and**
  `stash list` is empty (repo-global across worktrees, so it fails *safe* — a sibling session's stash withholds
  the fix rather than risking it). For a **detached `HEAD`** the engine **never** switches away from a
  commit-carrying detached `HEAD` without first creating a **rescue branch** at it, and **never** silently
  `--ff-only`s a diverged branch. Returning from a **named** branch needs no rescue branch — switching away never
  orphans its commits (the branch ref keeps pointing at them) — so losslessness there is structural. Losslessness
  is a property of *these operations*, not a recovery promise: the fix never discards branch-reachable,
  detached-`HEAD`, or stashed work, and commits a *prior* `reset` left reachable only from the reflog are neither
  created nor touched by it — git's reflog stays their backstop.
- **Merged-vs-unmerged shapes the offer wording — best-effort, never a safety gate.** Whether a parked side
  branch is *fully merged* into the default (a clean catch-up) or *carries unmerged work* (returning leaves that
  work on its branch, not on the folder the operator sees) is read with `git cherry <default> <branch>` — a
  patch-id check that catches **more** merges than the ancestry-based `git branch --merged` /
  `git merge-base --is-ancestor` / `git rev-list --not`: it recognizes a squash-merge **whose content collapses
  to a single equivalent commit**, which those miss. But none of them, `git cherry` included, can certainly
  recognize a **multi-commit** squash (the common GitHub shape), where no individual commit's patch-id matches
  the combined squash — so there is **no certain offline "is fully merged" check**, and the reading is
  **advisory only**: it picks the offer's tone, never its safety. `git cherry`'s uncertainty is **asymmetric in
  the safe direction** — it over-reports *unmerged*, never false-*merged* — so the engine **errs to the gentle
  "I'll keep your unfinished work safe" framing whenever the branch is not confidently fully absorbed**, never to
  a breezy catch-up that could move the operator off real work.
- **The offer is plain-language and one decision.** [Boot](../lifecycle/boot.md) words both the
  broken-state and off-main cases without git verbs, and the merged/unmerged difference reduces to **one operator
  decision** ("yes, fix it" / "no"): the fully-merged offer says "your folder is showing an older version of your
  project — nothing is lost, with your OK I'll bring it up to date"; the carries-work offer reassures "there's unfinished
  work saved here that isn't in your main project yet — I'll keep it exactly where it is, nothing deleted — with
  your OK I'll point your folder back at the main project." Neither asks the operator to understand "merged." The
  **first full relay owns the disclosure gap**: a checkout the engine reported healthy for weeks is newly
  catchable, so the relay names that ("earlier sessions couldn't spot this; that's fixed now") rather than
  silently indicting every prior all-clear.
- **The unsafe path stays actionable, never a dead-end.** When unsaved work blocks the clean fix, the engine
  does not hand the non-engineer a git command: it **offers the rescue-then-update on one consent** ("I found
  unsaved work in your project folder — with your OK I'll save it somewhere safe first, then bring the folder
  current"), realized by creating the rescue branch at the at-risk commit *before* anything moves, so one consent
  clears the strand with no loss.
- **Honest tier.** The detector runs in the boot pack, so it is hook- and runtime-dependent: in the
  double-fault case (the runtime so absent the `SessionStart` hook itself cannot run — the literal
  pre-`settings.json` incident) it cannot fire, and the [boot](../lifecycle/boot.md) floor's
  present-marker is the backstop. The standing protection against the engine ever *causing* a strand is native
  worktree isolation + the never-strand-main floor ([build-orchestration](../lifecycle/build-orchestration.md));
  this detector catches the strands that happen anyway, where boot can still run.

### The product boundary

The boundary between the engine and the product it builds is **not a new catalogued surface** — the
surface set is locked complete and product intake is a native product-layer **module** composing existing
surfaces ([D-042](../../../adr/0042-procedural-content-grounding-surface-cluster-designed-the-bo.md)/[D-043](../../../adr/0043-surface-set-completion-re-lock-ontology-and-hooks-to-clear-t.md)/[D-047](../../../adr/0047-product-spec-intake-design-it-native-not-bundled-the-build-t.md)).
Provisioning's role at the boundary is to draw it correctly:

- **Enforcement** is the [topology](repository-topology.md) wall — CODEOWNERS path-ownership,
  derived as above. The engine owns its namespaced corners and its infrastructure artifacts; the product
  owns the rest.
- **Knowledge is asymmetric** ([principles §13](../../../principles.md)): the engine reads and knows the
  product; the product never depends on the engine. On **greenfield** the [product-design](../../modules/product-design.md)
  module captures intent into product-side artifacts the engine reads ([D-065](../../../adr/0065-product-design-front-door-design-the-q14-intake-module-as-a.md)).
  On **brownfield** the engine, as a joining contributor, **reads the existing product** to onboard — the
  first post-provisioning act is an Explore-mode onboarding read that seeds the cognitive substrate, not
  an instantiator step.

So provisioning, on greenfield, draws the wall and may offer the product-intake module; on brownfield, it
draws the wall around the existing product with collision detection, then hands off to an onboarding read.

### Build-spec leaves

The design laws above are fixed at the lock; the operator-facing **copy** and the one reactive behavior they
govern are authored in the build session (laws-not-leaves, [D-052](../../../adr/0052-foundational-law-layer-closed-the-implementation-lock-order.md)). As built,
several of the consent-copy leaves are **externalized as committed template files** read by stable headings
with code fallbacks (and a parity test between the two), so the operator-facing words are reviewable as
files rather than buried in code. What is fixed
here is the law each leaf must satisfy:

- **The pre-bootstrap explanation copy** — the plain-language account shown *before* the authorization
  screen, pre-translating the literal scope string the operator will see. Law: no raw scope name arrives
  uninterpreted, and the explanation precedes the screen.
- **The tool-runtime consent + degraded copy** — the plain-language account shown *before* the uv install
  (what is installed, *where* — a private engine folder — *why*, the **isolation guarantee** that the
  operator's own Python is never touched, and the **verifiable pinned source**), plus the standing
  degraded-runtime banner. Law: the consent names the install honestly as software placed on the operator's
  machine and affirms the isolation; the degraded banner is plain-language-only (maintainer terms — uv,
  venv, sync, lockfile, pyproject — forbidden on the surface) and offers a retry, never a dead-end.
- **The deselection-confirm wording** — leads with the destructive outcome (confirming *deletes* an
  unselected **extension's** code; re-adding is a separate install, not a toggle), so a checkbox's "reversible"
  intuition cannot mislead.
- **The standing degraded-state banner** — its copy and where it renders, naming the concrete risk and one
  concrete next action. Law: degraded protection is surfaced continuously in plain language, never a silent
  unprotected run.
- **The module-selection walkthrough copy** — the per-category and per-module glosses. The *structure* is
  fixed by [D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) as scoped by [D-335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md) (only opt-out-able `extension` modules, grouped under the three
  SDLC discipline categories, the required spine never offered); only the glosses are a leaf. Law: each gloss answers, in
  one non-engineer sentence, what the module does and who it is for.
- **The memory-backup setup UX** — destination create/select, shared-vs-per-project, cadence, and the
  back-up-now/restore command wording, over the mechanism [memory](../cognitive/memory.md) owns.
  Law: consent-before-create, a self-describing destination, auto-offered restore, degrade-and-disclose.
- **The audit's saved-memory read turn-on** — the operator-facing setup that lets the **scheduled
  self-audit** read the off-repo memory backup (the [audit-library](../../modules/audit-library.md)
  "Coverage of local memory" precondition). Provisioning **commits the destination pointer** so a CI checkout
  can locate the vault, and walks the operator through granting the run a **least-privilege read-only
  credential** — a fine-grained `contents:read` token scoped to the single vault repo, stored as the audit's
  repository secret, distinct from the own-repo workflow token (which cannot reach a separate private repo) and
  from the `CLAUDE_CODE_OAUTH_TOKEN`. Law: it is a **heavy-consent trust gate** in the operator's own language
  (the tool-runtime-consent precedent above), naming the **two-part precondition as one outcome** (the backup
  exists *and* the run is granted access — completing only the first is a dead end), **pre-translating** every
  platform term (a *read-only token*, an *Actions secret*), **disclosing where the secret is set** that under
  the shared-vault default the one credential reads *every* co-located namespace — with the **per-project repo
  the actionable escape** — and **steering to a no-expiry token where the operator's own (personal) account
  allows it**, falling back to the re-arm below (never a silent yearly stop) where an org or policy caps token
  lifetime so no-expiry is unavailable. The turn-on **ends with an engine-run verification** — a one-shot test
  read of the vault with the just-set credential, reported in plain language (it reached the backup, or it
  names the exact fault — wrong scope, wrong repo, mis-named secret — and the one fix) — so the operator has a
  **positive correlate that the grant worked**, not only a delayed dark-digest signal. **Re-arm is
  credential-specific copy this leaf owns**: when the read later lapses or is mis-set, re-issue the read token
  and re-set *its* named secret (**never** the Claude-run token's `claude setup-token`), surfaced by the audit's
  staleness backstop naming *which* credential lapsed. The credential is a provisioning-owned grant over the
  [memory](../cognitive/memory.md) backup it **consumes and does not widen**
  ([§16](../../../principles.md)/[D-048](../../../adr/0048-provisioning-delivery-designed-end-state-brownfield-capable.md)/[D-241](../../../adr/0241-authorize-completing-the-audit-s-off-repo-memory-read-enable.md)).
- **The reactive add-module offer** — when an operator's request maps to a capability in an uninstalled
  `extension`, the engine may **offer** to install it via the settled `add` path. The trigger wording
  and threshold are leaves; the law is that it is an *offer* over the existing mechanism, never a silent install.
- **The security-floor toggles, the `SECURITY.md` seed, and the tier disclosure** — the concrete
  operator-privileged `gh` calls that enable native secret scanning / push protection, **CodeQL code scanning**
  (default setup), and **private vulnerability reporting** (the endpoints + request shape re-verified against
  live GitHub at build — [constraints](../../../reference/constraints.md)); the **status-branch handling** that reads
  each call's result (applied → confirm; **unsupported → skip + disclose**; transient → retry), keyed to the
  **per-toggle** status — code scanning's unsupported result is a **403** (no Code Security), PVR's on a private
  repo is a **422** (public-only) — so neither is misread as the other; the template-carried **`SECURITY.md`
  seed** content (a minimal default when the maintainer's seed is absent) and the root copy-if-absent step; and
  the plain-language **first-run disclosure** + the step that shows it, over the invariant the
  [control-plane](control-plane.md) owns. Law: a feature is enabled where the tier supports it; the
  toggle **branches on status, never fire-and-forget**; the tier is **disclosed, never auto-switched or
  silently downgraded**; the seed is operator-owned and **never overwrites a product's existing `SECURITY.md`**;
  and work proceeds only on the operator's choice. The disclosure speaks **both directions**: it names **what is
  now on** — and for enabled **PVR**, names the *consequence* in plain language (people outside the project can
  now privately send security reports, and where those arrive) so the first report is expected, not a surprise
  — and **what is off and what would unlock it**, stating the unlock in terms a non-engineer can **evaluate**
  (making the repo public is free; the alternative is a **paid GitHub add-on with a per-seat cost**) — never a
  bare product-tier name like "Code Security tier" left unexplained, and never an HTTP status or maintainer term
  on the operator surface.
- **The native permission-mode-default disclosure + conflict-offer copy** — the plain-language account shown
  when the instantiator writes the default (the adopt-by-default disclosure) or asks (the conflict-only
  adopt-or-keep offer), plus the detection precision (which settings files, read order, malformed-file
  handling; an *existing preference* is any `defaultMode` already set to a non-`plan` value). Law: the copy
  is behavioral and states the outcome in *this repo's* terms, names the `/config` change path, and makes
  clear **nothing global was changed and the setting is a convenience that removes no safety gate** (the
  Explore write-gate and the human merge review both stand); an existing preference is offered the choice and
  **honored on decline**; the write is disclosed, never silent.
- **The operator-checkout-strand detector + un-stranding-fix mechanics and copy** — the concrete commands the
  detector runs to classify the checkout (broken / off-main / behind) and the fix runs to un-strand it (within
  the lossless-or-it-does-not-run law above), the persisted derived default-branch name it classifies against,
  the `git cherry` merged/unmerged advisory read, the in-progress-state probes (`MERGE_HEAD` / `rebase-merge` /
  …), the behind-the-merged-main-line threshold and its consequence wording, the off-main day-one signal's
  collapse fingerprint, the `.claude/worktrees/` fence in the foundation `.gitignore` block, and the
  plain-language surfacing + offer-to-fix + rescue-then-update + disclosure-gap copy. Law: the two binary
  *broken* states and the off-main signal are offline+local every boot; behind-the-merged-main-line is network-
  and consequence-gated, never a bare distance, and uncomputable-so-silent on a no-remote repo; the fix is
  offline-decidably lossless or it does not run (clean tree + no in-progress op + empty stash; rescue-branch-first
  for a detached `HEAD`; a named-branch return needs none; never a silent reset or non-ff); merged-vs-unmerged is
  advisory tone only, never a safety gate; the offer is plain-language and actionable, with maintainer/git verbs
  (detached, fast-forward, rescue branch, `cherry`, `rev-list`) never reaching the operator surface.
- **The conduct operator-override seed-file + promote-command** — the template-carried seed file's path and
  format, Apply's copy-step behavior when it is absent, the promote-to-seed command's wording, and the
  **first-run disclosure copy** (the stance-is-present-and-yours-to-tune notice). Law: the
  seed is copied to `.engine/conduct/operator.md` as operator config at first run, an absent seed yields an
  empty override (never an error), and the promote command is an explicit operator action over the existing
  conduct-authoring mechanism, never a silent write.
- **The root-README product starter, the marketing-seed recognizer, and the seed disclosure** — the starter
  README's content (a product name/purpose placeholder plus the [D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) required-spine
  disclosure in plain operator language); **how Apply recognizes the engine's own marketing landing seed** — a
  recognizable engine marker or content fingerprint the landing seed carries — so the replace fires on that and
  only that; and the first-run disclosure copy + the step that shows it. Law: the starter is a product placeholder
  that discloses the required spine in plain language; the recognizer is **conservative — positive-match-or-preserve**,
  firing the replace **only** where the slot still holds the recognizable engine marketing seed, so operator-owned
  content (a brownfield product README, or post-seed operator edits) is never touched, even at the cost of leaving a
  stale engine front; and the seed/replace is disclosed at first run — the disclosure **names what changed and why it
  is theirs** (the Engine's landing page was replaced with a starter for *their* project, framed as intentional setup
  of their repo's front door), never a bare "the engine changed your README", and never silent.

All operator-facing copy is non-engineer-proof: maintainer vocabulary (orchestrator, coherence, wiring,
manifest, idempotent) never reaches these surfaces.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Modules declare files + wiring; provisioning applies and reverses both**, so install is mechanical, not surgery ([D-012](../../../adr/0012-provisioning-is-two-subsystems-on-one-manifest-grammar-modul.md), Risk [R5](../../../reference/risks.md)). | The `module-manifest` schema check (hard, CI suite) asserts the declared shape and the `block-coherence` check the declared-versus-applied wiring — partial support; the apply/reverse round trip itself is exercised by the module-manager tests, not one named check. | operator |
| **The shared wiring library** uses the [module system](../grammar/module-system.md)'s closed seam vocabulary and engine-namespaced-identity keying; reversal removes only the engine-identified entry, and no directive edits product source. | The wiring-coherence legs of the validator and the `operator-guarded-paths` check (hard, CI suite) carry the keyed-edit and never-product-source halves in part; the remove-only-its-own-entry property is test-pinned, so the row stays with you. | operator |
| **Installed means present.** First-run deselection deletes an `extension`'s code; re-adding runs the updater path, not a flip-on. Required modules are never offered or deleted; a newly-required module converges at upgrade. | The `uv-group-drift` check (hard, CI suite) asserts the dependency half — a deselected extension ships no live dependency group — as partial support; the delete-on-deselect and re-add paths are exercised by the instantiator and module-manager tests. | operator |
| **Provisioning is brownfield-capable by grammar.** A live product can adopt the engine via the overlay path; coexistence is the keyed, additive discipline applied to every platform-shared path (`.mcp.json`, `.gitignore`, CODEOWNERS, root `CLAUDE.md`, `.claude/` contents). | The arrival verb's collision-check and the keyed-edit round trip are exercised by the instantiator's arrival and collision tests — test-pinned rather than a named check; end-to-end adoption of a live product is your observation at a real brownfield arrival. | operator |
| **The instantiator is thin and resumable**; the engine manifest is its checkpoint, and the permanent primitives (wiring library, bootstrap operation, coherence) outlive its retirement. | The `first-run-reference-closure` check (hard, CI suite) asserts the retirement's travel-safety half — no surviving file imports a retired first-run asset or names its path literally, with one disclosed limit (an indirectly-built name can slip past); resumability from the manifest checkpoint is exercised by the instantiator's resume tests, so the row stays with you. | operator |
| **Clean removal** reverses all wiring, deletes the engine-namespaced files, and **de-bootstraps the control-plane** (drops the engine's required-check binding — an operator-privileged step, since a stale binding to a deleted engine check would deadlock the product's own pull requests), leaving an operable, engine-free product. | The module-manager removal tests and the de-bootstrap primitive's tests exercise each leg — test-pinned; that the remaining product is operable engine-free is your observation. | operator |
| **An unapproved or unavailable substrate is loudly surfaced** in plain language and degrades to committed files, never silently inert ([hooks](hooks.md) fail-open-and-flag). | Boot's substrate-availability probe and its surfacing are pinned by the boot tests — partial support; that the degraded session still works from committed files is your observation. | operator |
| **First-run instructions are non-engineer-proof** and include the control-plane step the prototype omitted. | The first-run walkthrough names the control-plane step (its committed copy is reviewable as a file); the leak-guard and vocabulary-confinement checks carry the non-engineer-proof half in part — language quality is finally yours to judge. | operator |
| **The tool-runtime is engine-managed and isolated.** uv is auto-bootstrapped behind a consent gate, installed PATH-independently, and the runtime uses a pinned interpreter that never draws on or mutates the operator's system Python; if it cannot materialize, the engine degrades loud — the interpreter-independent [boot](../lifecycle/boot.md) floor keeps orienting and a retry is offered wherever the engine can still run it — never falling back to system Python ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md), Risk [R18](../../../reference/risks.md)). | The instantiator's tool-runtime tests pin the consent gate, the PATH-independent install flags, and the pinned interpreter; the halt-and-resume on a failed materialization is test-pinned too — test-pinned throughout rather than one named check. | operator |
| **The native permission-mode default is operator config, detected-then-yielded.** The instantiator reads the operator's existing `defaultMode` read-only and writes the recommended plan default into the project settings only on adoption (offering adopt-or-keep on conflict, honoring a decline), disclosed as non-weakening ergonomics and preserved across an overlay like the operator handle ([D-185](../../../adr/0185-authorize-a-two-foundation-re-litigation-ship-a-native-plan.md), [modes](../lifecycle/modes.md)). | The instantiator's plan-mode tests pin the read-only detect, the write-on-adopt, and the keep-writes-nothing branches — test-pinned; the disclosure copy's quality is yours. | operator |
| **The conduct operator-override is operator config, seeded-then-owned.** Apply seeds `.engine/conduct/operator.md` from the template-carried seed (so the operator's standing stance travels to every generated repo), then it is operator-owned and preserved across an overlay like the operator handle; the universal-default codes of conduct ride `core` (overlaid), and the override is authored by the [core](../../modules/core.md) conduct-authoring verb ([D-192](../../../adr/0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md), [conduct](../surfaces/conduct.md)). | The conduct-shape and conduct-frontmatter checks (CI suite) assert the surface's form as partial support; the copy-if-absent seed step is test-pinned, and overlay preservation is your observation at an upgrade. | operator |
| **The security floor's native scanning is enabled where supported, disclosed where not.** The bootstrap enables native CodeQL code scanning (and, on public repos, private vulnerability reporting) by an operator-privileged `gh` call that **branches on the call's status** — applied, or unavailable → skip-and-disclose — never fire-and-forget and never auto-switching visibility; a root `SECURITY.md` is seeded as operator-owned config (preserved as a product path) so every repo carries a disclosure channel even where native PVR cannot exist. No bespoke scanner, and code-scanning alerts are advisory — no merge gate ([control-plane](control-plane.md), [D-212](../../../adr/0212-resolve-the-d-211-security-floor-re-litigation-landed-text-c.md), Risk [R25](../../../reference/risks.md)). | The security-floor tests pin the per-toggle status branching (the 403 and 422 unsupported paths among them) and the seed's copy-if-absent step — test-pinned; the disclosure's delivery and the never-auto-switch stance are your observation. | operator |
| **The root `README.md` is a product file, seeded-then-ceded.** At rest in the template the root README is the engine's marketing landing front; Apply seeds a product-owned starter over it **only where the slot still holds the engine's recognizable marketing seed**, so greenfield replaces the traveled front while brownfield and every later overlay preserve operator-owned content and the engine never re-touches the root README after instantiation. The starter carries the [D-067](../../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md) required-spine disclosure; it is operator-owned, in no `provides`, preserved as a product path; the seed/replace is disclosed at first run ([topology](repository-topology.md) law 2, [D-214](../../../adr/0214-resolve-the-d-213-front-door-re-litigation-landed-text-cold.md)). | The replace-iff-marketing-seed recognizer and the preserve branches are test-pinned; overlay preservation across an upgrade is your observation. | operator |
| **A stranded or off-main operator checkout is detected and offered a fix.** A standing, boot-invoked detector reads the main checkout's state — two binary *broken* states (detached `HEAD`, missing engine files) offline every boot; a gentle offline **off-main** signal when it is parked on a non-default branch; and a branch-agnostic, network- and consequence-gated **behind-the-merged-main-line** escalation — and, on consent, performs the **un-stranding** correction (re-materialize / re-attach / return-to-default-and-bring-current) — **lossless-or-it-does-not-run**, with a rescue-then-update path for unsaved work; merged-vs-unmerged (`git cherry`, best-effort and advisory) shapes only the offer wording, never its safety; the deepest double-fault case is named, backstopped by the boot present-marker and native worktree isolation ([build-orchestration](../lifecycle/build-orchestration.md)). | The checkout-health tests pin the broken/off-main/behind classification and the lossless-or-it-does-not-run preconditions, and the boot tests pin the relay — test-pinned across two surfaces; the offer's plain language and the fix's outcome on a real strand are your observation. | operator |
