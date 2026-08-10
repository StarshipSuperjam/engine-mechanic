---
status: locked
---

# routine-mode

*Reconciled with engine-template@`cdbbc33` as built (2026-08-02) — AI-compared and operator-ruled under [decision 0320](../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the routine-entry actor ratified by [decision 0322](../../adr/0322-ratify-set-routine-as-the-routine-entry-actor.md), with the manifest's `status` field separated into the distribution, applicability, and activation axes by [decision 0335](../../adr/0335-separate-module-distribution-applicability-and-activation.md); ratified as intended design on 2026-05-30 by [decision 0140](../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The module that **ships the operator's entry into the unattended Routine stance**. The Routine *stance*
laws — unattended, scope-locked, can't-ask (so findings route to Issues), never merges the protected
branch, entry authority = the operator-authored schedule + the frozen scope-locked build Issue — live in
the locked [modes](../systems/lifecycle/modes.md) doc, and the unattended *workflow* (how a
build's implement phase distributes across routine sessions) lives in the locked
[build-orchestration](../systems/lifecycle/build-orchestration.md) doc. **This module is how the
entry ships**: the `/engine-routine` command an operator-authored scheduled fire invokes — a Claude
Desktop routine, or a Codex Automation firing the `$engine-routine` mirror — and the
routine-entry procedure that command enters. Routine is one of the three stances, not one of the eleven
foundations; the routine *stance* is **`required`** core ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)) — a trust
protection present in every generated repo, never an install choice.

## Behavior

### Manifest shape

| Field | Value |
|---|---|
| `id` | `routine-mode` |
| `distribution` | `required` — never an install choice |
| `applicability` | `universal` |
| `activation` | `always` · `ungated` |
| `provides` | the **`/engine-routine`** [skill](../systems/surfaces/skills.md) (`invocation: operator-typed`, engine-prefixed) — the thin entry command embedded in a scheduled fire's Instructions, a single delegating pointer with no procedure of its own ([D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)/[D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)); its **generated Codex mirror** (`$engine-routine`, carrying the same no-self-invocation flag); and the **routine-entry [operation](../systems/surfaces/operations.md)** the command delegates to — the procedure home that confirms the unattended posture, reads the frozen scope-locked build Issue, **enters the Routine write-stance through the engine's `set-routine` verb** (the ratified actor, [decision 0322](../../adr/0322-ratify-set-routine-as-the-routine-entry-actor.md), which writes the stance only after a positive worktree-isolation proof), echoes the locked-on Issue on first fire, files a durable Issue on a misfire, and enters the build-orchestration routine workflow |
| `wires` | **none** |
| `depends` | `core` |
| `migrations` | none |

### Wiring nothing — entry by presence, workflow and posture ride `core`

`routine-mode` `wires` **nothing**; both artifacts are active by presence/reference, and everything that
*would* be a wire belongs to `core`, not here:

- the **`/engine-routine` skill** is discovered by Claude Code in `.claude/skills/` and joins the menu by
  presence — a file drop, no wiring ([skills](../systems/surfaces/skills.md); the
  [derived-binding principle](../../principles.md));
- the **routine-entry operation** is *referenced* by the skill, not wired — a referencer mutates nothing
  ([operations](../systems/surfaces/operations.md) "one procedure, one home");
- the **session stance marker** — modes' ephemeral, session-keyed, non-committed signal of the active
  stance ([modes](../systems/lifecycle/modes.md)) — sits outside the
  closed wiring seam vocabulary, not a wire: nothing here is *wired*, but as built the module's own
  routine-entry procedure **does set it**, through modes' `set-routine` verb — the routine-entry actor
  ratified by [decision 0322](../../adr/0322-ratify-set-routine-as-the-routine-entry-actor.md) — and the
  write-gate then honors the marker for the session's writes. Entry **authority** is unchanged: the
  operator-configured schedule plus the frozen scope-locked build Issue authorize the fire
  ([D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md)); `set-routine`
  is how the already-authorized fire records its stance (behind a worktree-isolation proof), never a
  model's self-election;
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

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.* *(No row in this table earns `engine` — every criterion here rests at least partly on your observation.)*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **The stance and workflow are the systems'; the entry is this module** — modes owns the Routine stance laws and build-orchestration owns the unattended workflow; `routine-mode` ships only the operator entry verb and the procedure it enters, restating neither. | Operator observation: the manifest provides only the entry verb (both runtimes' renders) and its operation, no stance or workflow files; the stance laws live in the modes tooling and the unattended workflow in the orchestration procedure, which routine-entry references rather than restates. Partial support: module-manifest and self-map-drift (both hard, CI) hold the provides set true; neither attests the ownership boundary. | operator |
| **Wires nothing** — skill by presence, operation by reference; the permission posture is an operator-side Desktop preset (outside the repo), the push-wrapper/push-gate are build-orchestration build-spec leaves, and the write-gate hook is core/modes — none is `routine-mode`'s. The one shared thing entry touches is the ephemeral session stance marker, set through modes' ratified `set-routine` verb ([decision 0322](../../adr/0322-ratify-set-routine-as-the-routine-entry-actor.md)) — session-scoped and never committed, so no durable shared state is seized. | Operator observation: the manifest carries `wires: []` and the marker write goes through modes' own verb, not a wire. Partial support: module-manifest (hard, CI) validates the wires field's shape without asserting emptiness; self-map-drift (hard, CI) holds the rendered "wires: none" true to the manifest. | operator |
| **`required` core, not a foundation** — the routine stance ships in every generated repo and is never an install choice ([D-067](../../adr/0067-operator-facing-module-packaging-industry-discipline-categor.md)); the eleven foundations stay minimal beneath it. | Operator observation: the manifest declares `status: required`, the self-map renders it required, and the module is absent from the optional-add catalog so it is never offered as a choice. Partial support: module-manifest (hard, CI) holds the status field schema-valid without pinning its value; provisioning-catalog (hard, CI) governs the catalog it is correctly missing from. | operator |
| **The routine-entry operation is preserved on a ratified affirmative case** — the [D-087](../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)/[D-088](../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md) drift-firewall, satisfying the operations anti-sprawl bar rather than defaulting past it. | Operator observation: the standalone operation exists and its preservation rests on the ratified drift-firewall case in the record. Partial support: operation-shape and operation-frontmatter (both hard, CI) hold the file structurally valid; the affirmative-case judgment is review, not a check. | operator |
