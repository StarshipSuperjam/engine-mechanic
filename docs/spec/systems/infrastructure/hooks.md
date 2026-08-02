---
status: draft
---

# Hooks

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-28 by [decision 0271](../../../adr/0271-resolve-the-d-270-plan-acceptance-legibility-augment-landed.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees.*

## Summary

The Claude-Code-side enforcement and lifecycle substrate. Where the
[control-plane](control-plane.md) is the GitHub-side substrate that makes guardrails real at
the merge, hooks is the in-session substrate every local automation rides on: the boot pack, the close
ritual, the local nudges, and the experiential capture all fire through Claude Code hook events. It is
foundational because boot, close, telemetry, validation, and memory all presuppose it; it cannot be
bolted on later.

This system **owns the cross-cutting hook laws** — the event inventory, the hook-script contract, the
block budget, the failure law, registration, and mode-awareness. It does **not** own behaviors: the
[boot](../lifecycle/boot.md) sequence owns its `SessionStart` script (and
[memory](../cognitive/memory.md), [telemetry](../guardrails/telemetry.md), and the
projects-sync module ride the same event with scripts of their own), the
[close](../lifecycle/close.md) ritual owns its `Stop` script, [memory](../cognitive/memory.md)
owns the `PreCompact` compaction trigger, and [validation](../guardrails/validation.md) and
[telemetry](../guardrails/telemetry.md) split `PostToolUse`. Hooks is to those events what the
[ontology](../grammar/ontology.md) is to surfaces: it fixes the law and the slot; the
behaviors attach.

## Behavior

### The event inventory

The Engine governs a **subset** of the Claude Code hook events — the platform exposes more, and the set
the Engine binds is an end-state decision, not the platform's full list.

| Event | Engine role | Owner |
|---|---|---|
| `SessionStart` | inject the boot pack before the first prompt; beside it ride memory's session-start scripts (erasure enactment, the throttled backup push), the projects-sync refresh, and telemetry's ambient run and inbox drain (a fresh-context `clear` start rides only the boot and memory scripts) | [boot](../lifecycle/boot.md) · [memory](../cognitive/memory.md) · [telemetry](../guardrails/telemetry.md) · [github-projects-sync](../../modules/github-projects-sync.md) |
| `PreToolUse` | the local pre-action gate (block-eligible), plus best-effort derived-artifact refreshers at the commit boundary — the knowledge graph, the self-map, the spec-obligation matrix, and the pre-commit suite nudge — each of which always proceeds | the invariant's owning system · each refresher's owner |
| `PostToolUse` | local nudge (relevant-subset run) + capture; set the Build stance + inject the assistant-internal stance directive on plan-exit completion | [validation](../guardrails/validation.md) · [telemetry](../guardrails/telemetry.md) · [modes](../lifecycle/modes.md) |
| `PreCompact` | trigger the deterministic memory-compaction fold before the context squash (narrative capture is the `Stop` ritual's — [memory](../cognitive/memory.md)) | [memory](../cognitive/memory.md) |
| `Stop` | the close ritual (block-eligible) | [close](../lifecycle/close.md) |
| `SessionEnd` | declared in the inventory with nothing bound: no cleanup duty exists as built, so the slot's empty realization is the sanctioned state (wave-5 ruling under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)) — a duty that names itself binds here later | hooks |
| `UserPromptSubmit` | inject the per-prompt orientation scent (injection, never blocks) | [boot/orientation](../lifecycle/boot.md) |

The platform exposes a large and growing event set; among those the Engine does **not** bind in v1 are
`SubagentStart`, `SubagentStop`, `PostCompact`, `PermissionRequest`, `StopFailure`, and `Notification`:
a subagent's findings are swept by the parent's `Stop` ritual, a post-compact pass would duplicate
work the Engine already schedules around the squash (the `PreCompact` fold, with narrative capture at
`Stop`), permission events duplicate the `PreToolUse` gate, and `Notification` is
operator-UX rather than governance. Any event is bindable later by a system that names a need — the
inventory grows additively, like the surface catalog.

### The block-budget law

This is a **design restriction the Engine imposes**, not a platform limit. Only `PreToolUse` and `Stop`
may **hard-block**, and only for a small, enumerated set of governance-critical invariants (plus one **minimal-work-loss redirect**, below); every other
event **nudges** (`PostToolUse`), **injects** (`SessionStart`), or **fires a side-effect trigger**
(`PreCompact`, which neither blocks nor injects). The platform would let
`PreCompact`, `UserPromptSubmit`, and `SubagentStop` block too — the Engine declines, because a local
hard-block buys friction without proportional trust ([principles §6](../../../principles.md)); the one
unbypassable gate is the protected-branch review. The one admitted exception to that friction test is a
**minimal-work-loss redirect** — a `PreToolUse` deny that loses no work because it redirects the same action
to a conforming path (the engine-Issue-conformance reroute, below) — so its §6 friction is ~nil and it earns
block-eligibility without being governance-critical; like every local block it is never dressed as the wall.

A `Stop` or `PreToolUse` block is a **strong** local block, not an absolute wall: Claude Code force-ends
the turn after eight consecutive `Stop` blocks (it sets `stop_hook_active` on the forced continuation;
the cap is operator-configurable via `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`), so a local gate makes evasion
take deliberate effort while the durable backstop stays the [control-plane](control-plane.md)
merge gate.

The **block-eligible invariant set started empty and owning systems register into it additively**. As
built the roster holds **three members**, each registered by its owner: the
[close](../lifecycle/close.md) ritual's findings-disposition block; the
[explore](../lifecycle/modes.md) write-gate — the
exploration stance's `PreToolUse` block, which honors the fail-open law below (a strong default, not an
absolute wall; the durable backstop stays the [control-plane](control-plane.md) merge gate) —
registered by modes; and the **engine-Issue-conformance reroute** — a
minimal-work-loss redirect that denies a non-conforming engine-labeled `gh issue create` (or issue-creating
`gh api`) and points the session to the [control-plane](control-plane.md) issue-authoring helper —
registered by modes alongside it. An append-only-history guard may register later.
Hooks owns the *budget* (which events may block, and that
membership is governance-critical only); it names no invariants itself, so it presupposes none of the
systems that will populate the set.

### Fail-open-and-flag

A hook script that crashes must never strand the operator, and must never fail silently.

- **The guarded action proceeds.** This is the platform default and the Engine goes with the grain: a
  `PreToolUse` hook blocks on exit code 2 or an exit-0 `permissionDecision: deny` (the path the Engine
  uses), so any *other* unexpected exit — a crash emitting neither — is non-blocking and the tool runs. An author must not "helpfully" wrap a gate to deny-on-error — that would make a bug
  fail-closed and strand a non-engineer who cannot debug it ([principles §5](../../../principles.md)).
- **The failure is a finding, promoted immediately.** A gate that cannot evaluate is the enforcement
  machinery going blind, so it promotes to a tracked finding on first occurrence (not after a
  persistence threshold); persistence only escalates how loud it gets. This rides the
  [telemetry](../guardrails/telemetry.md) remediation loop and is fixed in a later scoped
  session under guardrails, not inline by the session that tripped it.
- **The operator sees it in plain language, at the decision point** — rendered as a named line in the
  [control-plane](control-plane.md) pull-request Validation section ("a safety check could not
  run on this change: *what it would have checked*; this work was not verified for *X*"), distinct from
  an ordinary pass or fail, and carried in the [boot](../lifecycle/boot.md) orientation as an
  open finding **regardless of its non-blocking status**. A guardrail that failed open and only an AI
  ever reads is advisory theatre from the operator's seat.

A **missing tool-runtime** is the interpreter-absent variant of this law, and the launcher (below) owns
it: if `.engine/.venv/` is absent or unhealthy the hook's interpreter never starts, so the launcher exits
`1` — deliberately never `2`, which would fail closed and strand the session — emits one plain-language
stderr line naming the absent runtime (there is no Python traceback to lean on), and drops a presence
marker that [telemetry](../guardrails/telemetry.md)'s session-start inbox drain promotes to **one**
tracked finding on the next healthy session.
[Provisioning](provisioning.md) owns materializing the runtime; [boot](../lifecycle/boot.md)
carries the standing surfacing ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)).

Finding persistence must not depend on the non-blocking `SessionEnd` completing, which the platform may
skip; durable capture happens where it can be relied on.

### Registration is reversible, keyed wiring

Hook registration lives in committed `.claude/settings.json`, so it travels via "Use this template"
([principles §1](../../../principles.md)). Because settings.json is a single shared file, registration is
a **keyed, idempotent edit**: installing a [module](../grammar/module-system.md) adds its hook
entry; uninstalling removes only that entry, leaving others intact. The keyed-edit primitive itself is
the wiring library's, applied and reversed by [provisioning](provisioning.md) — this doc fixes
that registration must be reversible and keyed; it does not own the mechanism.

### Mode-awareness

Every hook behavior declares the [modes](../lifecycle/modes.md) it is active in. The explore
write-gate is exploration-only; a `Stop` block must be satisfiable non-interactively in routine mode, or an unattended run
deadlocks (autonomous runs cannot ask questions; see [constraints](../../../reference/constraints.md)). The
*dimension* is the law; the *bindings* are membership, carried with the invariant set — as built, every
block registration declares the modes it is active in, and the block-coherence check reds a registration
that omits them.

### The hook-script contract

A hook script speaks the **Claude Code platform contract**, not an Engine-authored schema: it reads the
event JSON on stdin (session id, transcript path, tool name and input, and event-specific fields), and it
communicates by exit code (2 blocks and feeds stderr back to Claude; other non-zero is a non-blocking
error) or by structured stdout (for `PreToolUse`, a `permissionDecision` of allow / deny / ask — the
values the Engine uses; the platform also offers `defer`). `additionalContext` injects for injectors.
Two consequences are load-bearing:

- A `PreToolUse` intercept on a shell command (e.g. `git commit`) matches on the **tool name** (`Bash`)
  and tests the command **inside the script**, rather than relying on the settings `if:` matcher — which
  keeps the gate robust to matcher syntax and keeps the decision logic in one reviewable place.
- Hook commands reference their scripts through `${CLAUDE_PROJECT_DIR}`, never an absolute path, so they
  resolve on any operator's machine after the template is generated.
- Hook scripts execute in the engine [tool-runtime](repository-topology.md), and as built every
  registered command routes through a **committed launcher**:
  `sh "${CLAUDE_PROJECT_DIR}/.engine/tools/hook-runner.sh" "<interpreter>" "<script>" [args]`, where the
  interpreter argument is the **explicit, `${CLAUDE_PROJECT_DIR}`-rooted** venv path
  (`${CLAUDE_PROJECT_DIR}/.engine/.venv/<bin>/python`, resolved per-OS at fire time: POSIX `bin/`,
  Windows `Scripts\`) — portable per the rule above and independent of any `PATH` the non-interactive
  hook shell may lack. The launcher earns its interposition: it waits out the fresh-worktree race with a
  bounded poll before declaring the runtime absent, and it owns the missing-runtime marker path above. A
  CI unit test pins every registered command to the launcher-rendered form, so the registration and the
  contract cannot drift apart. Two residuals are disclosed, not hidden: the launcher puts a POSIX `sh`
  dependency on the hot path (a Windows-environment residual the build notes without yet adjudicating),
  and it travels with no executable bit —
  invoked through `sh`, deliberately, so template travel never depends on file modes. A bare
  `python`/`uv`, or `uv run` with its implicit re-sync, is **never** used on a hot path
  (the re-sync adds network/disk latency at a latency-sensitive moment); `uv run`'s auto-sync is reserved
  for non-hot entry points (the [provisioning](provisioning.md) flows, the
  [validation](../guardrails/validation.md) suite runner). ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md).)
- The hook dispatch layer applies a **provider-normalization seam**, and a sibling Codex launcher ships
  beside the Claude one — the two-runtime posture the
  [repository topology](repository-topology.md) records; this contract's laws hold for both.

### Boundary

A hook script is a [tool](../surfaces/tools.md) instance: the boundary law routes deterministic
engine code to the `tool` surface, whose home (`.engine/tools/`) is where hook script code lives — it is not
a dedicated surface. The platform contract above stands regardless, because it documents an external
interface rather than an Engine-authored shape. Hook *registrations* and the settings file are wiring, not
surfaces.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| The engine uses only the hook events named in the event inventory. | A CI unit test pins the inventory constant's event roster — partial support; no check asserts that the settings file's bound events stay a subset of it, so the subset property is your observation. | operator |
| The block-budget law holds: only `PreToolUse` and `Stop` may block, and a `PreToolUse` deny is spent only on a registered governance-critical invariant or the minimal-work-loss redirect. | The `block-coherence` check (hard, CI suite) asserts every block registration sits on a block-eligible event and declares its modes — strong partial support; that a member is *governance-critical* (or genuinely minimal-work-loss) is a judgment no check grades. | operator |
| On a hook failure the guarded action proceeds — the platform default, gone with the grain. | CI unit tests pin the proceed-on-crash path end to end: a crashing handler proceeds and flags, a `sys.exit` fails open, and the launcher never falls back or fails closed on a missing or non-executable interpreter — test-pinned rather than a named check, so the row stays with you. | operator |
| A hook failure is a finding, promoted immediately: a gate that cannot evaluate is an enforcement failure, never a silent pass. | CI unit tests pin the flag-on-crash leg and the promoted finding's wording; the promotion path spans the telemetry inbox drain, which no single check asserts end to end. | operator |
| The operator sees a hook failure in plain language at the decision point, rendered as a named line. | CI unit tests pin the plain-language crash line (and the fail-open notice that overrides it); the named-line rendering in the pull-request Validation section is the control-plane's surface, unchecked from here. | operator |
| Hook registration is reversible, keyed wiring — installing or removing one is mechanical and leaves no residue. | The wiring-coherence legs of the validator assert declared wiring matches applied wiring, and the module-manager tests exercise the add/remove round trip — partial support; "no residue" beyond the keyed entry is your observation. | operator |
| Hooks are mode-aware: the stance the session is in governs what a hook does. | The `block-coherence` check (hard, CI suite) reds any block registration that omits its mode declaration — full for blocks, partial for the inventory at large, since non-block hooks carry no universal mode assertion. | operator |
| Every hook script meets the hook-script contract. | A CI unit test pins every registered command — all of them, across the settings file and the module manifests — to the launcher-rendered command form; the stdin/exit-code handler behavior is pinned per-path by the dispatch tests, not by one check. | operator |
| The boundary holds: hooks carry wiring, never the judgment that belongs to a surface. | The ownership and catalog-coverage legs of the validator locate hook code in the tool surface's home — weak partial support; the wiring-versus-judgment distinction itself is a design boundary only you can judge. | operator |
