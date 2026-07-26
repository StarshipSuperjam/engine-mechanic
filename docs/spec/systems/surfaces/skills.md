---
status: draft
---

# Skills

*Ratified in the design workspace on 2026-06-15 by [decision 0201](../../../adr/0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

A **Claude Code skill** — a `SKILL.md` (prose plus routing frontmatter) with optional bundled
resources, using progressive disclosure: the frontmatter that the platform keeps resident lets the
model (or the operator) know the skill exists, the body loads on invocation, and deeper bundled files
(or a referenced [operation](operations.md)) load only when the procedure actually runs.

A skill is the **procedure surface invoked in-session**, distinct from an [agent](agents.md)
(spawned by the orchestrator into an isolated context) and an [operation](operations.md) (the
shared reading-and-following body a skill or agent enters). Who may invoke a given skill — the model on
its own, the operator by typing it, or only the model — is the skill's **invocation** axis, a governed
field of the one surface rather than a separate surface. This mirrors the platform: Claude Code merged
custom slash commands into skills, so a skill *is* the primitive and invocation *is* a property of it.

## Behavior

### The invocation axis

Every skill instance declares one **`invocation`** value. The engine governs which value an instance
takes; the value maps to the real platform frontmatter, which the instance carries:

| `invocation` | platform frontmatter | who invokes | frontmatter description |
|---|---|---|---|
| `model-auto` (default) | neither flag | the model auto-invokes on a description match; the operator may also type `/name`, **but not at a cold start** (see below) | **permanently resident** — the model must know it exists |
| `operator-typed` | `disable-model-invocation: true` | the operator only, by typing `/engine-…` | **not resident** — loaded only when the operator invokes it |
| `model-only` | `user-invocable: false` | the model only; hidden from the operator's `/` menu | **permanently resident** |

The legacy `.claude/commands/<name>.md` file form still works and behaves as an `operator-typed`
skill; `.claude/skills/<name>/SKILL.md` is the current form.

### Meta-contract record

| Field | Value |
|---|---|
| name | `skill` |
| class | prose + structured frontmatter (a Claude Code `SKILL.md`) |
| location | **`.claude/skills/`** — platform-dictated, not `.engine/skills/` |
| purpose | an in-session procedure, invoked per its `invocation` value (model-auto, operator-typed, or model-only) |
| authority tier | 3 — mechanics/guidance |
| lifecycle | `artifact` (active → deprecated → retired) |
| governing schema | JSON Schema over the `SKILL.md` frontmatter routing fields, including `invocation` |
| template | the skill template (scaffold + shape) |

**Location and collision (resolved, not a wall exception).** Claude Code discovers skills only in
`.claude/skills/` (and the legacy `.claude/commands/`), a tool-dictated slot
([topology](../infrastructure/repository-topology.md) law 4), like
[agents](agents.md) and the root `CLAUDE.md`. Engine skills live there, engine-prefixed per
the [ontology](../grammar/ontology.md) identifier law (D-020). Loose project-level skill files
are **not** platform-namespaced (real namespacing exists only for plugin skills, `plugin:name`, and the
engine ships as committed files via "Use this template", not as a plugin); same-name clashes resolve
silently by precedence. The `engine-` prefix therefore **reserves the name by convention** — a collision
with an operator-authored skill is improbable, not platform-impossible. `.claude/` is already an engine
corner, so the wall is unaffected.

### Governance differs by invocation value

The one surface carries two distinct rationing pressures, selected by the `invocation` value — and they
pull in opposite directions, which is exactly why the axis is governed rather than left implicit.

**`model-auto` / `model-only` — rationed by attention.** A skill the model may invoke has its
name+description **permanently resident** in context so the model knows it is available. A fat,
vaguely-described model-invocable set therefore bloats every session and mis-triggers. So the engine
ships **few, sharply-described** model-invocable skills, and such a procedure earns a skill only when all
three hold:

- it **recurs** (a one-off does not justify always-resident weight),
- it **benefits from auto-invocation** — the model should reach for it when the situation arises rather
  than needing to be told (the same metacognition gap the scent addresses), and
- it is **engine-owned** (the operator authors their own product skills alongside, un-prefixed).

`model-only` is the model-invocable case hidden from the operator's menu; it carries the same
always-resident attention cost and the same earns-a-skill bar. Its v1 instance membership is
resolved by [D-087](../../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md): **v1 ships no `model-only` skill** (the value exists so a
future need is additive, not because one is needed now).

**`model-auto` is not reachable at a cold start.** Operator-verified ([D-200](../../../adr/0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)): a
`model-auto` skill is **absent from the operator's `/` menu at a cold session start** (before the first message)
and appears only from the second message on, whereas a `disable-model-invocation: true` skill is typeable
immediately. (The likely cause is that a model-invocable skill's name+description loads into the model's context
as the session initializes; the live Claude Code docs do not document this menu timing, so the behavior is taken
from the operator's live test, not the docs.) A verb the operator must be able to type at a **cold session
start** must therefore be `operator-typed`, whose description is not resident and which lists immediately. Like
`model-only`, **v1 ships no `model-auto` skill** ([D-200](../../../adr/0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md)): the value exists so a
future need is additive.

**`operator-typed` — rationed by discoverability.** An operator-typed skill carries **no** standing
attention cost (its description is not resident; it loads only when typed), so it is not bound by the
attention budget. It is instead bound by a different requirement, because a non-engineer cannot use a
verb they cannot find:

- **Thin, delegating.** It is an entry point, not a procedure body. Where there is real procedural
  depth, it **delegates** to an [operation](operations.md) rather than restating the steps —
  one procedure, one home.
- **Discoverable — a committed v1 requirement.** The operator must have a plain-language way to learn
  what typed verbs exist — named in the operator orientation [doc](docs.md) and/or an
  `/engine-help`-style index. The surface **cannot ship leaving the operator unable to discover it**;
  discoverability is not deferred. The genuine v1 need that operator-typed skills serve is **mode
  entry** (leaving Explore is a deliberate human act — [modes](../lifecycle/modes.md)); the
  **concrete mode-entry verbs are [modes](../lifecycle/modes.md)' leaf to author**
  (laws-not-leaves), this surface fixes the grammar.

**Operator-facing vocabulary.** `invocation`, `model-auto`, `operator-typed`, `model-only` are
governance/maintainer terms; they must never surface in operator-facing text. To the operator, an
operator-typed skill is simply a **command** — "a verb you type, like `/engine-build`."

### Discovery by presence; complementary to the scent

A skill installs as a **file drop**: Claude Code discovers it by presence in `.claude/skills/`, so a
skill module `provides` files and **wires nothing** (the [derived binding by presence principle](../../../principles.md);
[R5](../../../reference/risks.md)). A model-invocable skill is complementary to the
[scent](../lifecycle/boot.md), not a duplicate of it: the scent *points* the model at relevant
recall to verify ("memory has notes on X"), while a skill *provides the procedure* for doing X —
push-to-consult versus push-to-perform, never two parallel nag systems.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **One surface, invocation as a governed axis** — `model-auto` / `operator-typed` / `model-only` are values of the one `skill` surface, matching the platform's merged mechanism; a new invocation mode is a new value, additive, not a new surface. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Few and sharp where model-invocable** — always-resident descriptions are an attention cost; ship a small set with precise trigger language, not a zoo. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Discoverable where operator-typed** — a plain-language discovery path ships in v1; the operator is never left guessing what verbs the engine offers. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Thin entry, shared body** — a deep or reused procedure lives in an [operation](operations.md); the skill references it rather than restating it. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **File-drop, no wiring** — discovery by presence; install/uninstall is add/remove a file. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Engine-prefixed by convention** — the `engine-` prefix reserves the name (loose files are not platform-namespaced). | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
