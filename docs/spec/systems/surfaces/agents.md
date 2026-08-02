---
status: draft
---

# Agents

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-07-16 by [decision 0313](../../../adr/0313-resolve-re-lock-agents-the-engine-naming-rule-the-read-only.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees.*

## Summary

A **persona** the engine runs for a **trigger**: the [build orchestration](../lifecycle/build-orchestration.md)
spawns a cold-context reviewer (scope, design, security, QA …) at a gate or a scoped-write worker during a
build, and the `audit-prep` cron runs the read-only self-audit persona. An agent is a Claude Code agent-definition file. At
a build gate it is a **subagent the orchestrator spawns** — the **orchestrator is the session, not a
persona** (it conducts; agents are the instruments it spawns); under the cron the agent file *is* the
**top-level session** (run by `--agent`), not a spawned subagent. One grammar, two triggers.

The core ships the **persona template** (the grammar every agent fills) and the mechanism that assembles a
roster from it; the **personas themselves are additive** — engine-shipped agent suites are
[modules](../grammar/module-system.md) (the v1 suites settled by [D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)),
and an operator may author their own. This is the [ontology](../grammar/ontology.md)'s "laws not leaves" shape: the
template is locked-grade grammar, instances attach additively.

## Behavior

### Meta-contract record

| Field | Value |
|---|---|
| name | `agent` |
| class | prose + structured frontmatter (a Claude Code agent file) |
| purpose | a persona the engine runs for a trigger — a build-orchestration reviewer or scoped-write worker spawned at a gate, or the cron-fired read-only self-audit persona |
| authority tier | 3 — mechanics/guidance (an agent *does* work; it does not govern) |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | JSON Schema over the frontmatter routing fields (below) |
| template | the persona template (scaffold + shape) |
| location | **`.claude/agents/`** — platform-dictated, not `.engine/agents/` |

**Location wrinkle (resolved, not an exception to the wall).** Claude Code discovers agents only in
`.claude/agents/`, so agent instances live there — like the root `CLAUDE.md` and `.mcp.json`, this is a
tool-dictated slot ([topology](../infrastructure/repository-topology.md) law 4), and the catalog
`location` field records that platform path rather than the usual `.engine/<surface>/`. The files are
engine-authored; `.claude/` is already an engine corner, so the engine/product wall is unaffected.

**Naming.** Agent instance names are **`engine-`-prefixed** (`engine-audit`, `engine-qa-review-<lens>`,
`engine-design-review-<lens>`), per the [ontology](../grammar/ontology.md) identifier law
([D-020](../../../adr/0020-engine-instance-identifiers-are-engine-namespaced-decision-r.md)) — as [skills](skills.md) are on this same platform slot. An
agent name is **not merely a file path**: it is a knowledge-graph entity id and a token the operator and the
engine's own workflows name directly, which is exactly the class the law covers. The engine corner resolves
the *path* question (above); it does not discharge the *identifier* one — path-namespacing under a
tool-dictated slot does not cover a bare identifier, which is the law's whole point. Loose project-level
agent files are not platform-namespaced, so the prefix **reserves the name by convention** — a collision
with an operator-authored persona is improbable, not platform-impossible.

### The persona template — routing fields (the core grammar)

Every agent declares these routing fields in frontmatter (`lens` only for the review roles):

- **`role`** — `plan-review` · `worker` · `pre-submission-review` · `audit`. The role **implies the
  trigger it runs for** — the **build orchestration** for the first three (a review gate for
  `plan-review`/`pre-submission-review`, the Implement phase for `worker`), the `audit-prep` cron for
  `audit` (the read-only self-audit persona) — so there is no separate trigger field (one fewer way to
  misconfigure).
- **`lens`** — the specific perspective **within a review role**. The shipped roster: `product-intent`,
  `architecture`, `feasibility`, `risk-governance` at plan-review (the [D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) four); `spec-conformance`, `usability`, `technical-integrity`,
  `security-governance`, and `divergence-hunter` — an adversarial fifth added since D-066, exactly the
  additive growth the open roster invites — at pre-submission; plus the optional `retroactive`, which
  ships no persona. Open and additive, a module may ship a new lens.
  The `worker` and `audit` roles carry **no lens** — a worker implements, and the single self-audit
  persona is recognized by its role, not a lens.
- **`model-tier`** — a **closed demand vocabulary** `judgment` · `mechanical`: the persona-owned
  **execution tier the work demands** (careful judgment vs. mechanical work product), never a model
  name. The set stays **closed and coherence-checkable** (an out-of-set value is a finding, exactly as
  before); only its *axis* is the work's demand, not a model identity — so a model release never touches
  it. *Which* model and effort **realize** a tier is platform-passthrough (below). (The field keeps the
  name `model-tier` though its members are now demand levels; a rename is deferred — [D-100](../../../adr/0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md).)
- **`permissions`** — a reviewer **or the audit persona** is **read-only** (it reports findings, never
  writes); a worker has **scoped write** (only its commit's paths). Maps to Claude Code agent
  tool/permission restrictions. The read-only leg is **gated mechanically at the native write-tool
  floor**, not left to prose: a merge-gating [check](check.md) asserts that a persona declaring
  `permissions: read-only` carries an explicit denial — or a write-excluding allowlist — of the
  authoritative write tools (Edit / Write / NotebookEdit), closing the **inherit-all trap** where a
  read-only persona names no tool restriction and silently inherits write access. **What the check reaches:**
  it confirms the denial is **declared**; the *platform* is what honors the declaration. Enforcement is
  therefore split across two parties, and the check speaks for only one of them — it cannot certify that a
  given platform version obeyed a field it accepted. That residual is closed the only way it can be, by
  behavioral demonstration in a live session, never by the check asserting more than it evaluated. **The floor's honest limit**
  ([§7](../../../principles.md)): it polices the *native* write tools only. Bash and write-capable MCP
  calls are outside it, confined instead by the environment the persona runs in (worktree isolation for a
  session-spawned reviewer; the ephemeral runner for the cron-fired audit persona) and, for both, by the
  protected-branch merge gate — so "read-only" here means *cannot reach the native write tools*, never
  *cannot cause a write by any route*.
- **`output-contract`** — findings on the canonical [`finding.v1`](schemas.md) base
  `{severity, message, location ref (file/line)}`, with **`severity` a per-consumer axis**
  ([D-113](../../../adr/0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md)): the review roles narrow it to `blocking | serious | nit`, and the
  `audit` role declares its own in its profile. The agent **reports**; the **trigger-owner decides** by
  *its own* disposition vocabulary — a build gate's orchestrator collects and dispositions (fix /
  log-an-Issue / escalate) per the locked finding-disposition [policy](policies.md), while the
  `audit-prep` cron routes its findings through the [audits](../guardrails/audits.md) two-lane
  disposition. The grammar fixes only the report **shape**, never a consumer's enum or disposition set.
  Each consumer's [schema](schemas.md) instance is **versioned (`.v1`) and fixture-tested**
  (authored at build time), so a contract change is explicit and regression-guarded.
- plus the platform `description` Claude Code uses to present the agent.

These routing fields are **engine-governed-and-read** frontmatter — the engine's roster derivation and its
coherence checks read them. They sit alongside the keys **Claude Code itself enforces**: `name` (the platform
identity field that makes file-drop discovery work), `description`, `tools` / `permissionMode` (the platform
mechanism the **`permissions`** split maps to — read-only reviewer vs. scoped-write worker), and the
**execution-realization pair `model` and `effort`** — the persona-owned, platform-passthrough keys that
*realize* the `model-tier` demand level (a `judgment` persona runs a higher model and/or effort; a
`mechanical` persona a lower one). The engine governs only *which `model-tier` demand* an instance declares;
*which model and effort realize it* is the instance's own platform-passthrough choice, so a new model is
adopted by changing config, never this grammar. As guidance, durable model *aliases* (e.g. `opus`/`sonnet`/
`haiku`) are preferable to versioned IDs that rot — but `model` also accepts a full ID or `inherit`, so the
engine names no closed model set. The platform reads its own keys and leaves the engine's extra frontmatter
untouched — relied on as standard YAML-frontmatter behavior by convention, not a documented platform guarantee.

### The roster is derived — file-drop, no wiring

An agent installs as a **file drop**: discovery is by presence in `.claude/agents/`, so a persona module
`provides` files and **wires nothing** — the reversibility win the closed seam vocabulary exists to earn
([module-system](../grammar/module-system.md), Risk [R5](../../../reference/risks.md)). The orchestration
**derives** its roster by querying available agents' `role`/`lens` frontmatter **for the build-gate roles**
(`plan-review`, `worker`, `pre-submission-review`); a present `audit`-role persona runs for the
`audit-prep` cron, not a build gate, so it is **never a member of the build roster**. This is exactly how a
check-suite's membership is derived from rules that self-declare into it ([D-023](../../../adr/0023-check-system-locked-validator-architecture-the-check-surface.md))
— the [derived binding by presence principle](../../../principles.md). There is **no central playbook list**
an install must edit; adding an agent re-derives the roster for free. One realization note: the
`worker` / `scoped-write` / `mechanical` leg of the grammar is fully supported by the schema but ships
no v1 instance — every shipped persona is a read-only `judgment` reviewer or the auditor; a worker
persona is a future file drop, not a present member.

### Coherence

Two merge-gated [checks](check.md) (both `custom/script` rules in the CI suite — the `coherence`
kind proper stays scoped to module-set consistency) confirm the agent set: the closed-set bullets
(the closed `role`, and a `lens` on a lensless role) are the agent-coherence check's, which also
carries the read-only write-tool floor above; the consumption pair (zero-agents disclosure and the
dangling lens) is the lens-consumption check's:

- **0..N agents per lens is valid.** A consumed lens with zero agents means that gate **did not run a
  review** — disclosed to the operator as exactly that, never reported as a green "passed."
- **`role` is a closed set** (`plan-review` · `worker` · `pre-submission-review` · `audit`). An instance
  declaring a role outside that set is a coherence **finding** — an "unknown role" is impossible by
  construction. (`role` fixes the trigger an agent runs for; the build orchestrator derives its roster
  from the build-gate roles only, so a present `audit` persona is never pulled into a gate; *which lens a
  gate consumes* is a separate mapping, below.)
- **`lens` recognition is by consumption** ([derived binding §14](../../../principles.md); no central
  list). An installed **review** agent whose lens **nothing in the orchestration consumes** is a
  **finding** — enforced by the separate lens-consumption check, which reads the orchestration's
  consumed-lens declaration against the installed personas (the dangling-check-kind posture,
  [D-023](../../../adr/0023-check-system-locked-validator-architecture-the-check-surface.md)), disclosed to the
  operator at the plan gate, never left as a check-only signal the operator may never run. The `worker` and
  `audit` roles carry no lens and are recognized by role, so the dangling-lens finding scopes to review
  lenses. *Which* gate consumes *which* lens is the
  [build orchestration](../lifecycle/build-orchestration.md)'s concern (deferred to its design);
  this surface fixes only that an unconsumed review lens is a disclosed finding.
- **A `lens` on a non-review role is a finding.** The `worker` and `audit` roles carry no lens (above), so
  a `worker` or `audit` instance that *declares* one is a coherence **finding** — the symmetric guard to
  the closed-`role` check, making "no lens" a typed invariant rather than an honor-system note.

**Honest limit on coverage.** This surface guarantees gaps *within the consumed lens set* are disclosed —
not that the consumed set covers everything an operator might want. The lens set is **open** (a module adds
one; §14), so the affirmative "what was reviewed and what was not" roll-up — the operator's real coverage
view — is the **plan-gate risk assessment**'s duty ([build orchestration](../lifecycle/build-orchestration.md)),
not a completeness guarantee this surface can make.

**Operator-facing wording is plain language.** The internal terms here (`derived binding §14`, the
dangling-check-kind posture, the role/lens/trigger vocabulary including the `audit` role, the
`audit-prep` cron, and the `--agent` top-level-session mechanics) are maintainer framing; what the operator
sees is plain language ("no security review
ran on this change"; the audit digest's plain self-attestation), never these names — the
[operator-communication law and the maintainer-jargon leak guard](../../../principles.md) apply.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Template is core; personas are additive** — the routing-field grammar is the critical-path piece; which suites ship is settled ([D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)), and operators extend it. | Operator observation via the self-map and module manifests: the persona template ships with core while every persona instance is provided by a separate optional module, core shipping none; the template-shape check asserts the template's form, not its core ownership. | operator |
| **File-drop, no wiring** — discovery by presence; roster derived from frontmatter; install/uninstall is add/remove a file, with the roster re-derived rather than mutated. | Operator observation that the persona-bearing modules declare their agents under `provides` and wire nothing, and that adding or removing a persona file re-derives the roster with no manifest edit; the lens-consumption check (hard, CI) supports the presence-derivation half by reading the roster directly from the agents directory, but asserts consumption, not absence-of-wiring. | operator |
| **Reviewers and the auditor report, workers write** — `permissions` enforces the split; the non-writing personas feed a finding-disposition loop via the `output-contract` — the build gates' orchestrator, the `audit` role's cron. | Split: the read-only leg is fully asserted by the agent-coherence check (hard, CI, merge-gated) — a persona declared read-only must actually block the authoritative write tools via a declared denial or write-excluding allowlist, never inherit every tool — with its disclosed limit that Bash and write-capable MCP calls are confined by isolation and the merge gate, not the check. The worker leg ships no instance to assert, and the disposition loop is the trigger-owners' observed behavior — so the composite row stays with the operator, the check as named partial support. | operator |
