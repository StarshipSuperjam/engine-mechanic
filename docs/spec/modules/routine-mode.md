---
status: draft
---

# routine-mode

*Ratified in the design workspace on 2026-05-30 by [decision 0140](../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../spec/index.md).*

## Summary

The module that **ships the operator's entry into the unattended Routine stance**. The Routine *stance*
laws — unattended, scope-locked, can't-ask (so findings route to Issues), never merges the protected
branch, entry authority = the operator-authored schedule + the frozen scope-locked build Issue — live in
the locked [modes](../systems/lifecycle/modes.md) doc, and the unattended *workflow* (how a
build's implement phase distributes across routine sessions) lives in the locked
[build-orchestration](../systems/lifecycle/build-orchestration.md) doc. **This module is how the
entry ships**: the `/engine-routine` command an operator-authored Local Desktop routine fires, and the
routine-entry procedure that command enters. Routine is one of the three stances, not one of the eleven
foundations; the routine *stance* is **`required`** core ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)) — a trust
protection present in every generated repo, never an install choice.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `routine-mode` |
| `status` | `required` |
| `provides` | the **`/engine-routine`** [skill](../systems/surfaces/skills.md) (`invocation: operator-typed`, engine-prefixed) — the thin entry command embedded in a Local Desktop routine's Instructions, carrying no step list ([D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)/[D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)); the **routine-entry [operation](../systems/surfaces/operations.md)** it delegates to — the procedure home that confirms the unattended posture, reads the frozen scope-locked build Issue, echoes the locked-on Issue on first fire, files a durable Issue on a misfire, and enters the build-orchestration routine workflow |
| `wires` | **none** |
| `depends` | `core` |
| `migrations` | none (v1) |

### Wiring nothing — entry by presence, workflow and posture ride `core`

`routine-mode` `wires` **nothing**; both artifacts are active by presence/reference, and everything that
*would* be a wire belongs to `core`, not here:

- the **`/engine-routine` skill** is discovered by Claude Code in `.claude/skills/` and joins the menu by
  presence — a file drop, no wiring ([skills](../systems/surfaces/skills.md); the
  [derived-binding principle](../../principles.md));
- the **routine-entry operation** is *referenced* by the skill, not wired — a referencer mutates nothing
  ([operations](../systems/surfaces/operations.md) "one procedure, one home");
- the **session stance marker** — modes' ephemeral, session-keyed, non-committed signal of the active
  stance ([modes](../systems/lifecycle/modes.md); a modes build-spec leaf) — sits outside the
  closed wiring seam vocabulary, not a `gitignore`/`permission`/`hook` wire; it reflects the stance, it
  does **not** authorize entry (Routine's authority is the operator-configured schedule + the frozen
  scope-locked build Issue, [D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)), so `routine-mode` neither sets nor wires it;
- the **non-interactive permission posture** that makes "cannot ask" real is an **operator-side
  non-interactive permission preset** (in the operator's Claude Desktop / user-level settings, outside the
  committed repo), so the operator is the gate; its concrete form is a
  [build-orchestration](../systems/lifecycle/build-orchestration.md) **build-spec leaf**
  ([D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md), platform-fact-corrected at [D-140](../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md)), and whether
  it lands operator-side or as build-orchestration-owned committed config it is **never `routine-mode`'s to
  wire** — the same footing as the session stance marker, so this module wires nothing for it;
- the **push wrapper** and the **unattended Default-Branch-Push gate** are
  [build-orchestration](../systems/lifecycle/build-orchestration.md) **build-spec leaves**
  ([D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)), authored in the build pass — build-orchestration's, not
  `routine-mode`'s;
- the **Explore write-gate `PreToolUse` hook** is registered by [modes](../systems/lifecycle/modes.md)
  and packaged by `core` (it rides `core`'s `wires`), not this module.

The routine *workflow* itself is build-orchestration's, not `routine-mode`'s — the
[modes](../systems/lifecycle/modes.md) Routine ownership boundary (modes owns the stance; the
workflow is build-orchestration's), an instance of the [§16](../../principles.md) ownership axis. So
`routine-mode` carries none of that machinery.

So install is a file drop and uninstall a file removal — except the stance is `required` core, so it is
never an install choice.

### The routine-entry operation earns its standalone status

A single-referrer operation is normally a fold-or-retire candidate under the locked
[operations](../systems/surfaces/operations.md) anti-sprawl bar (a procedure that is only *one
skill's private depth* belongs in that skill's bundled resources). The routine-entry operation is **not
private depth, and is preserved with an affirmative case**, exactly as that bar permits: the cold-audited
[D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md) / [D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md) decisions ratified routing `/engine-routine`
to an **owned operation** — the drift-firewall that keeps the unattended entry procedure (the scope-read,
first-fire echo, and misfire-as-Issue logic that must not be buried in a thin command or in
build-orchestration prose) in one authoritative home — and rejected collapsing it onto a doc section. The
affirmative case is the ratified drift-firewall, not a default.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The stance and workflow are the systems'; the entry is this module** — modes owns the Routine stance laws and build-orchestration owns the unattended workflow; `routine-mode` ships only the operator entry verb and the procedure it enters, restating neither. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Wires nothing** — skill by presence, operation by reference; the permission posture is an operator-side Desktop preset (outside the repo), the push-wrapper/push-gate are build-orchestration build-spec leaves, and the write-gate hook is core/modes — none is `routine-mode`'s, so entering Routine seizes no shared state here. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **`required` core, not a foundation** — the routine stance ships in every generated repo and is never an install choice ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)); the eleven foundations stay minimal beneath it. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **The routine-entry operation is preserved on a ratified affirmative case** — the [D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)/[D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md) drift-firewall, satisfying the operations anti-sprawl bar rather than defaulting past it. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
