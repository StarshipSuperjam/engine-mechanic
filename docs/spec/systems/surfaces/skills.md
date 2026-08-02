---
status: draft
---

# Skills

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with engine-recall admitted as the single `model-auto` skill by [decision 0326](../../../adr/0326-admit-engine-recall-as-the-single-model-auto-skill.md); ratified as intended design on 2026-06-15 by [decision 0201](../../../adr/0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

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

A skill instance declares one **`invocation`** value — the governing schema leaves the field optional
(an omitted value means `model-auto`, the platform default), though every shipped engine skill declares
it explicitly. The engine governs which value an instance takes; on the Claude Code runtime the value
maps to the real platform frontmatter, which the instance carries (the Codex runtime carries the same
property differently — see the Codex render below):

| `invocation` | platform frontmatter | who invokes | frontmatter description |
|---|---|---|---|
| `model-auto` (default) | neither flag | the model auto-invokes on a description match; the operator may also type `/name`, **but not at a cold start** (see below) | **permanently resident** — the model must know it exists |
| `operator-typed` | `disable-model-invocation: true` | the operator only, by typing `/engine-…` | **not resident** — loaded only when the operator invokes it |
| `model-only` | `user-invocable: false` | the model only; hidden from the operator's `/` menu | **permanently resident** |

`.claude/skills/<name>/SKILL.md` is the current form. The legacy `.claude/commands/<name>.md` file form
is a tolerated remnant, not a governed one: the coherence check still reads any such file it finds, but
the governing schema declares the form out of scope and the engine ships none.

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
start** must therefore be `operator-typed`, whose description is not resident and which lists immediately.
When [D-200](../../../adr/0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md) flipped the status verb on that ground, v1 shipped zero `model-auto`
skills, the value kept "so a future need is additive" — and that additive arrival has since happened:
**v1 ships one `model-auto` skill, the memory-consultation verb (engine-recall)**, admitted by
[decision 0326](../../../adr/0326-admit-engine-recall-as-the-single-model-auto-skill.md). The cold-start rule does not bite it — recall
is a mid-session push-to-consult, not a verb the operator must reach cold — and it meets the
earns-a-skill bar above (recurs; benefits from auto-invocation at exactly the moment the assistant
would not think to consult memory; engine-owned).

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

### The Codex render

Each engine skill also ships as a **committed Codex-native render** — a distinct catalogued surface
generated from the canonical Claude skill, never hand-authored, living in the Codex runtime's own
corner ([topology](../infrastructure/repository-topology.md) law 4). Codex does not read the
Claude governance flags: the operator-only property is carried instead by a companion provider
configuration file beside each render (`allow_implicit_invocation: false`), and a deliberately
model-reachable command (the `model-auto` case above) is allowed a reachable render by the coherence
check's explicit carve-out. A hard, merge-gated provider-parity check compares the typed-command sets
in both directions, with any sanctioned gap recorded in a committed provider-exceptions ledger — at
the pin, the skill sets are at full parity with no exception.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **One surface, invocation as a governed axis** — `model-auto` / `operator-typed` / `model-only` are values of the one `skill` surface, matching the platform's merged mechanism; a new invocation mode is a new value, additive, not a new surface. | Operator observation that the surface catalog carries a single `skill` surface whose `invocation` is a schema field; the `skill-coherence` check (hard, CI) supports the value-to-flag half — it goes red when a command's stated invocation disagrees with its platform flags, most importantly an operator-typed command missing its self-invocation block (without which the model could still start it on its own) — but no check asserts the one-surface architecture itself. | operator |
| **Few and sharp where model-invocable** — always-resident descriptions are an attention cost; ship a small set with precise trigger language, not a zoo. | Operator and audit observation: count the model-invocable set (one at the pin — the memory-consultation verb) and read its description for trigger precision; the shape check disclaims judging substance, so no check asserts few-or-sharp. | operator |
| **Discoverable where operator-typed** — a plain-language discovery path ships in v1; the operator is never left guessing what verbs the engine offers. | Operator observation that the discovery path ships: the typed help command that lists every engine verb, plus the operator orientation guide. No check asserts discoverability. | operator |
| **Thin entry, shared body** — a deep or reused procedure lives in an [operation](operations.md); the skill references it rather than restating it. | Operator and audit observation that deep skills delegate by link to their operation; the skill length budget is a soft nudge, never a block, and the shape check disclaims judging delegation. | operator |
| **File-drop, no wiring** — discovery by presence; install/uninstall is add/remove a file. | Operator observation of the module manifests: skill-bearing modules declare their skills under `provides` and wire nothing; adding or removing a skill file re-derives the set with no manifest surgery. | operator |
| **Engine-prefixed by convention** — the `engine-` prefix reserves the name (loose files are not platform-namespaced). | Operator observation that every shipped engine skill carries the `engine-` prefix by construction; no merge-gated check asserts the prefix, matching the doc's own "improbable, not platform-impossible" framing. | operator |
