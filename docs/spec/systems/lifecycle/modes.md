---
status: draft
---

# Operating modes

*Settled in the design workspace on 2026-06-28, ratified by [decision 0271](../../../adr/0271-resolve-the-d-270-plan-acceptance-legibility-augment-landed.md).*

## Summary

The session's operating **stance** — what it may do, and whether a human is present to answer for it.
Stances differ on two mechanically-real axes, **enforced permission posture** and **attendance**. There
is no slot number and no transition state machine; a stance is just a posture plus who is watching.

| Stance | Attendance | Writes | Entry | Workflow |
|---|---|---|---|---|
| **Explore** (default) | interactive | gated **off** | every session boots here | converse · read · run read-only commands · spawn subagents · log Issues |
| **Build** | interactive | on | a typed verb, or accepting a plan | the [build orchestration](build-orchestration.md) |
| **Routine** | unattended | on, scope-locked | a Local Desktop routine fires `/engine-routine` | unattended execution of a build's implement phase |

The two axes yield four cells; the engine uses three. The fourth — **unattended + read-only** — is
deliberately empty: scheduled read-only work (periodic [audits](../guardrails/audits.md),
telemetry sweeps) runs as GitHub Actions cron, not as a Claude session stance, so it never needs the
unattended-read cell. The stance set is complete by construction, not by omission.

Every session boots **grounded** — [boot](boot.md) runs unconditionally — and **in Explore**.
There is no `/start-engine`: because boot is automatic, the only explicit triggers are the ones that
*change stance* (entering Build, or a routine firing, which invokes `/engine-routine`).

## Behavior

### Stance is session-scoped and never persists

Stance lives only for the session that holds it. It is an **ephemeral signal in non-repo storage, never
committed and never carried across sessions** ([state](../cognitive/state.md) commits the
cursor, never the stance). **Every session start — including a resume of an earlier session — begins in
Explore and never inherits a prior stance signal**, so a crashed or abandoned Build session cannot
resurrect as Build. When the signal is absent, stale, or unreadable, the stance is Explore: the safe
default is the floor, never the ceiling.

This is what makes "boots in Explore" a mechanical guarantee rather than an assertion: the signal is set
only by a deliberate in-session entry (below) and is cleared at every session start, so nothing a prior
session left behind can carry forward — a resume cannot inherit a Build signal merely because the platform
reuses the session id. The concrete representation, and the session-start clear that makes resume safe,
are a [build-spec leaf](#build-spec-leaves); the law is that the signal is non-committed, cleared at every
session start, and resolves to Explore in every ambiguous case.

### Explore — the enforced default

Explore is where a session reasons, reads the repo and the substrates, runs read-only commands, spawns
exploration subagents, and **logs Issues** — thinking with the operator before anything is built. It is
the answer to *"how does the engine know I'm only speculating?"*: an Explore session is **grounded** (it
reasons from the project, not from ad-hoc file-poking — see [boot](boot.md)) and **gated** (it
does not run off and build).

**The gate denies the building actions and allows everything else.** A `PreToolUse`
[hook](../infrastructure/hooks.md), registered by this system into the hook **block budget** and
active only while the stance is Explore (it reads the session stance signal; in Build and Routine it
permits the write), denies the small enumerated set that *begins building* — edits to engine or product
files, branch creation, commits, and the opening of a pull request (whether via `gh` or a GitHub MCP
tool) — and **allows everything else**: reads, read-only command and test execution, greps, subagent
spawning, `gh issue` calls (with one carve-out — the engine-Issue-conformance reroute below), and **Claude Code's own plan-mode artifact** — the plan file the platform
writes (and marks as such) when a plan is accepted. The plan file is *planning, not building*, so denying
it would regress a Claude Code basic the Explore stance exists to support (*thinking with the operator
before anything is built*), leaving the non-engineer worse off at a native capability than plain Claude
Code ([principles §5](../../../principles.md)). This carve-out is **the plan artifact specifically**, not
a blanket pass for writes outside the repo: other writes to the operator's `~/.claude/` (settings, hooks)
stay denied in Explore — being outside the repo, they have no protected-branch merge to backstop them.
There is **no default-deny on an action it cannot classify** — an
ambiguous command resolves to *allow*. Erring toward allowing is correct here because the gate is a local
nudge, not the wall (below), and because a default-deny would tax the very stance meant to be the
comfortable place to work, pushing the operator to leave Explore just to run a test.

**The gate also reroutes a non-conforming engine-Issue creation.** Beyond the build set, the gate **denies**
a `gh issue create` (or issue-creating `gh api`) bound for the **engine-labeled channel**
([control-plane](../infrastructure/control-plane.md)) whose body lacks the body-contract's
structural markers, **redirecting** the session to author it through the issue-authoring helper. This is a
**minimal-work-loss redirect**, not a build-block — it loses no work (the Issue still gets filed, via the
helper) — so it sits in the [hooks](../infrastructure/hooks.md) block budget as the one admitted
redirect, not a governance-critical invariant. It is **scoped to the engine-labeled channel**: every
unlabeled or human Issue, and every read / `list` / `view` / `comment` / `--add-label` / `close`, passes
untouched, so a non-engineer filing their own Issue is never stranded ([§5](../../../principles.md)), and the
[escalate-upstream draft](../guardrails/audits.md) is exempt (un-owned upstream, not
engine-labeled). Unlike the build set, it has **no merge wall behind it** — an Issue, once created, is
created — so this gate is the *primary* lever, and the only catch-all for a slip is the control-plane
`on:issues` CI backstop, never the merge gate.

**The gate is a strong default, and its enforcement is fallible.** Its limits are stated honestly
rather than papered over: the [hooks](../infrastructure/hooks.md) fail-open law means a gate
that crashes lets the action through, and detecting a build-by-`git`/`gh` in a shell command is
best-effort because a shell string is not fully parseable (aliases, `eval`, substitution, and chaining
all evade it). So the gate makes building-by-accident take deliberate effort, but the **only
unbypassable wall is the protected-branch merge**
([control-plane](../infrastructure/control-plane.md), [principles §6](../../../principles.md)).
A write that ever slips the gate is bounded by that wall — it shows up in the change set the operator
reviews and cannot reach the protected branch unreviewed, so even a gate that fails open never turns
Explore into an unreviewed change to the protected branch. The engine never dresses the local gate as the
wall, and never claims any leg of it is reliable. The engine-Issue-conformance reroute shares this
best-effort parsing limit, but it is the one gate with **no merge wall to bound a slip** — so its backstop is
the control-plane `on:issues` CI check (which flags, never silently rewrites), and the engine never pretends
that reroute is a wall either.

**The stance is always operator-legible.** Boot and each turn name the current stance in plain language
("*exploring — I won't change files or open a pull request until you tell me to build*"); a denied action
is surfaced as a clear sentence that names what was blocked and the concrete way forward ("*I didn't make
that change — we're exploring; tell me to build it and I'll open a pull request, the change I submit for
your approval*"), never a silent refusal; and the entry into Build is announced ("*opening a draft pull
request and planning the work*") so the operator knows the moment thinking became building. The operator
never has to guess what the engine will or won't do. Because no hook channel reaches the operator
([constraints](../../../reference/constraints.md)), each of these — the stance line, the denied-action sentence, the
Build-entry announcement — is delivered by the AI in chat per the
[operator-presentation relay](../../../reference/glossary.md): the denied-action notice especially, since the
`PreToolUse` decision's `permissionDecisionReason` does not reliably render, so the AI relays it in plain
words. The legibility is **posture**; the merge wall is the backstop.

### The native permission-mode default — plan mode, recommended not imposed

The stance above is one axis. Claude Code's own **permission mode** (`permissions.defaultMode` — `plan` /
`default` / `acceptEdits` / …, read **natively** by the platform) is a **separate** axis, and the two
compose: a session can boot the **plan** permission mode *and* the **Explore** stance. The Engine's
recommended interactive default is **plan mode** — a safe first-touch where the model proposes before it
acts — but it is **posture, not the guarantee**. The guarantee is the Explore write-gate plus the merge
wall ([§7](../../../principles.md) names the tier honestly); plan mode is ergonomics and defense-in-depth
*layered atop* them, never a substitute, and the design never dresses it as enforcement.

**The default is written at provisioning, as operator config that yields.** A static `defaultMode` is
**not** shipped in `.claude/settings.json`: project-scope settings override user-scope, so a baked-in value
would silently override an operator's own preference. Instead
[provisioning](../infrastructure/provisioning.md)'s instantiator writes the default **only on
adoption** — adopting plan by default when the operator has no conflicting preference (a disclosure, not a
prompt), and **offering adopt-or-keep** only when the operator already runs a different mode; declining
**writes nothing**, so the operator's own setting governs. The written value is **operator config**,
preserved across an engine overlay like the identity tier. The yield is **deploying-operator-scoped**: the
committed value then travels with the repo as a deployment property ("this repo opens in plan mode"); a
*different* user working in that repo overrides locally (`settings.local.json` / `/config`), the native
escape — not a clobber, since no operator `~/.claude` file is ever touched. Detection and the operator-facing
copy are [provisioning](../infrastructure/provisioning.md)'s; modes owns only the law that the
default is **recommended, operator-config, and yields**.

**The native mode is not a stance and not a Build-entry trigger.** Booting in plan mode does not enter
Build; the only Build entries remain the operator-typed verb and **accepting a plan** (below). Changing the
mode is a normal operator preference (native `/config`) — **not** a [§15](../../../principles.md) guardrail
weakening, because no enforcement value moves and the Explore gate and merge wall are untouched — so it
carries no alarm. The current mode stays operator-legible through the platform's own mode indicator and
boot's stance line, so the operator is never left guessing why a session is proposing rather than acting.

### Entering Build — a deliberate, announced operator act

Leaving Explore is a deliberate human act, and the engine never flips its own stance silently or by
default. There are **two interactive entry paths, and neither is something the model can do for itself**:

- **An operator-typed verb** — a [skill](../surfaces/skills.md) whose `invocation` is
  operator-only, so the **model cannot invoke it itself**; the operator types it and the session stance
  signal flips to Build. This is the path for work that did **not** go through plan mode (a direct
  "build this").
- **Accepting a plan** — when the operator approves a plan, the platform's **plan-exit completion is
  observable to a hook**, and the engine flips the stance signal to Build on that acceptance. A
  **rejected** plan produces no such completion, so it never enters Build; a hook that never fires (or
  fails) simply leaves the signal absent → Explore, **the fail-safe floor**; and the **model cannot accept
  its own plan** — acceptance is the operator's act. This is the ergonomic path for planned work:
  *approving the plan is "build it,"* with no extra verb to type.

The acceptance path **sets the stance signal and injects a terse assistant-internal stance directive** —
a system reminder that names the new Build stance and directs the next turn into the
[build orchestration](build-orchestration.md)'s announced kickoff, so the assistant learns its
own stance flipped rather than acting on the start-of-session boot briefing (which always reads Explore
by design) — the [boot](boot.md) §scent *push* posture: don't rely on the model overriding its
briefing from memory. The injected line is **assistant-facing machine context, not the operator announcement**: it
*triggers* the kickoff, never replaces it, so the operator still meets the entry through that **announced
kickoff** ("*opening a draft pull request and planning the work*"), fired **exactly once** on either
path. The line carries **no operator-facing copy, is do-not-relay verbatim, and carries no imperative
relay marker** (the [operator-presentation relay](../../../reference/glossary.md) reserves that marker for
governance alarms, the close-gate, and grounding-failure); it is a turn-local **directive**, governed by
the scent's push posture but never its attributed-pointer *verify-before-asserting* contract.

That directive is **turn-local, never a durable stance record**, so a resume cannot resurrect a Build
belief from it. The **signal is the sole durable stance record** (cleared at every session start →
Explore), and the assistant **derives and reports stance from the live signal, never from the injected
line**; **boot's session-start stance line is authoritative** over any replayed nudge (a resume reliably
re-renders it — the reliable-resume path established in [D-269](../../../adr/0269-litigate-q18-engine-template-313-resolve-cross-session-anti.md)); and the
kickoff is **guarded by a live-signal re-read** — the next turn proceeds only if
the signal still reads Build. So a nudge replayed over a cleared signal triggers no write (the
`PreToolUse` gate reads that signal), no kickoff, and no stance misreport. Because the signal is the
durable record and the line strictly advisory, the hook's two side-effects cannot diverge into a
wrong-stance act: a lost injection still leaves the operator the announced kickoff; a lost signal leaves
the replayed line inert.

Acceptance *enters* Build; the build's substantive spend/depth consent is build-orchestration's plan
gate, which still runs (proportionate — a trivial change collapses it to a one-line headline).

This keeps self-election — the leak that let the prototype's stances bleed together — **visible and
effortful**, not a claim of impossibility the design cannot keep ([principles §6](../../../principles.md)).
Neither path enters Build *silently* or *by default*: the verb is operator-only-invocable, and acceptance
is an operator approval of a plan the engine surfaced — **honor-rate-free** where the verb is fallible
([R11](../../../reference/risks.md)), but **not a stronger gate**, since the engine still originates the plan it asks
the operator to accept. Were the engine ever to enter Build wrongly, the entry is announced and the **merge
gate still holds**; the operator-facing surface says "I won't build until you tell me to," never "I
cannot" — the honest tier. The concrete verb name and the plan-acceptance trigger's mechanism are
[build-spec leaves](#build-spec-leaves); the law is that **each entry path is a human-only act and the
entry is announced**.

### Build — interactive and accountable

Build is interactive work that produces an accountable change. Its workflow is the
[build orchestration](build-orchestration.md): a **draft PR is the claim**, the work is planned
and — at a depth the operator approves — reviewed by cold-context subagents, and the session's **close is
simply the PR submitted for human review**. There is no separate claim artifact and no close ritual to
satisfy; the pull request is both.

**Entering Build is proportionate, never ceremony.** A one-line typo fix must not become a gauntlet —
that would only relocate the prototype's close-friction to the entry gate. The *principle* is modes': the
cost of entry scales with the change, and a small, low-risk change carries the least. The *mechanism* —
how the orchestration collapses to its floor, and how review depth is chosen — is the
[build orchestration](build-orchestration.md)'s, so the two never describe it twice.

### Routine — unattended and scope-locked

Routine is build work run **unattended** on a schedule, to batch context-heavy work while the operator is
away. v1 runs on **Local Desktop routines**: subscription-billed, committing under the operator's own git
identity and serialized single-flight (both the solo
[control-plane](../infrastructure/control-plane.md) model), with the machine kept awake by
Claude Desktop's keep-awake setting. Because an unattended run **cannot ask a question**
([constraints](../../../reference/constraints.md)), its scope is locked and the
[build orchestration](build-orchestration.md) checks its writes against that scope at boot and
at every commit, and any finding or decision that would need a human is **routed to a GitHub Issue** — the
routine arm of the locked escalation [policy](../surfaces/policies.md) — rather than guessed.
Because it cannot accept a plan, a Routine session also **never inherits the interactive plan-mode default**:
it establishes its own non-interactive permission posture **at launch**, which **overrides the project
`defaultMode`** (launch posture beats project settings; the concrete mode is a
[build-spec leaf](#build-spec-leaves) and the [build orchestration](build-orchestration.md)'s, per
[D-140](../../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md)) — so an unattended run never stalls waiting for a plan acceptance no human
will give.
Routine sessions **accumulate commits on an open pull request and never merge the protected branch**; an
interactive session reviews and closes the PR.

**Entry is the operator-authored scheduled fire, not model self-election.** The Local Desktop routine's
Instructions invoke **`/engine-routine`** — an engine-prefixed [operator-typed](../surfaces/skills.md)
command invoked by its *presence in the operator-authored scheduled prompt* (the slash-command parser path),
never by the model electing it on a description match. The entry **authority** is the operator-configured
schedule plus the **frozen, scope-locked build Issue** the command reads — so entering Routine is a
*pre-authored* operator act, not the silent or by-default self-election the stance model forbids
([principles §6](../../../principles.md)); the merge wall still holds (Routine never merges the protected
branch). The thin command enters a routine-entry procedure and adds no step list of its own. The name is
pinned (`/engine-routine`); its operator-facing wording is a [build-spec leaf](#build-spec-leaves).

Routine is **the same workflow, constrained** — not a separate lifecycle. The unattended execution
*workflow* (how a build's implement phase is distributed across routine sessions, and how it is planned
and finalized by interactive sessions) is the [build orchestration](build-orchestration.md)'s;
modes owns only the *stance* — unattended, scope-locked, can't-ask — and its escalation posture.

### Build-spec leaves

The laws above are fixed; these concrete forms are settled in the build-spec pass and do not reopen the
design:

- the **stance-signal representation** — a `session_id`-keyed ephemeral marker in OS-temp storage that the
  gate reads from the session id the platform supplies, **cleared at every `SessionStart` (which fires on
  resume as well as on a fresh start)** so a resumed session never inherits a prior Build signal; the law
  is only that it is non-committed, cleared at every session start, and resolves to Explore when absent,
  stale, or unreadable;
- the **exact denied-action match list** — the tool names treated as file-mutating, the GitHub MCP tool
  name(s) for PR creation, and the `git`/`gh` building-verb patterns the shell matcher looks for; **and how
  the plan-mode artifact is recognized and exempted**: a `Write`/`Edit` is denied as a build-beginning edit
  when it targets engine/product source, but Claude Code's plan file is **never** denied — recognized by
  **the platform's own plan-file marker** (the `PreToolUse` signal Claude Code's built-in plan-mode
  permission already uses to write it), **not** a literal `.claude/plans/` path. Matching the marker rather
  than a path is load-bearing: that path is operator-configurable and can resolve *inside* the repo, where a
  path match would wrongly re-trip the gate; the marker tracks the artifact wherever it lands, while every
  non-plan `~/.claude/` write (settings, hooks) carries no such marker and stays denied. The exact field is
  verified against current Claude Code at the build-spec ([D-178](../../../adr/0178-resolve-the-d-177-plan-file-carve-out-landed-text-cold-audit.md));
- the **plan-acceptance Build-entry trigger's mechanism** — the `PostToolUse` hook on the plan-exit
  completion (`ExitPlanMode`) that **sets the Build stance signal *and* injects the assistant-internal
  stance directive**, keyed on **the platform's own plan-exit completion event** (not a `permission_mode`
  value — acceptance offers several target modes, so the durable signal is the completion event itself,
  with `permission_mode` having left `plan` as target-agnostic corroboration); a rejected plan fires no
  completion and never enters Build. The injection rides the platform's `PostToolUse`
  `additionalContext` (a system reminder the model reads, 10,000-character cap; **replayed verbatim on
  `--resume`/`--continue`**, which is why the directive is turn-local and the signal — re-derived live —
  remains the sole durable record); the dated field names and cap are pinned to the current
  `code.claude.com/docs/en/hooks` reference, not the locked law. The exact field names are **verified
  against current Claude Code at the build-spec** ([D-270](../../../adr/0270-litigate-engine-template-276-make-the-explore-build-switch-o.md) names this the
  blocking precondition: `PostToolUse` fires on `ExitPlanMode`-**accept** and `additionalContext` reaches
  the model), and conformance confirms no false entry on a leave-plan-without-approving or a
  resumed/subagent plan mode; **names the known accept-with-clear-context non-fire** (a current-platform
  quirk where the completion hook does not fire on that accept variant, so the signal stays absent → the
  Explore fail-safe floor, with the operator-typed verb the recovery path — best-effort and fail-safe,
  never a false Build); that a **resumed session neither acts nor reports Build** from the replayed
  directive; and that the operator-facing Build-entry announcement is **present and singular**
  ([D-179](../../../adr/0179-augment-interactive-build-entry-with-plan-acceptance-correct.md), [D-270](../../../adr/0270-litigate-engine-template-276-make-the-explore-build-switch-o.md));
- the **Build-entry verb's name and wording**, and the plain-language copy for the stance announcement
  and for a denied-action sentence;
- the **routine-entry command's operator-facing wording** (its name is pinned — `/engine-routine` — by
  [D-087](../../../adr/0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)/[D-088](../../../adr/0088-justified-re-litigation-name-the-routine-entry-command-engin.md); only its phrasing is a leaf).
- the **native permission-mode default's realization** — how the instantiator **detects** the operator's
  existing interactive `defaultMode` (which files, read order, malformed-file handling); the plain-language
  **disclosure** copy (adopt-by-default) and **conflict-offer** copy (adopt-or-keep), both in behavioral
  language that states the outcome in this-repo terms and names the `/config` change path; the **Routine
  non-interactive launch posture** that overrides the project default (its concrete mode is
  [build orchestration](build-orchestration.md)'s leaf, per [D-140](../../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md) —
  modes owns only the law that it overrides); and the **re-verification against current Claude Code that
  `plan` is honored from project settings, and that `/config` surfaces `permissions.defaultMode`** (the
  operator's change path) (the
  [D-178](../../../adr/0178-resolve-the-d-177-plan-file-carve-out-landed-text-cold-audit.md)/[D-179](../../../adr/0179-augment-interactive-build-entry-with-plan-acceptance-correct.md) build-spec-verification discipline —
  the platform special-cases some modes in repo settings, e.g. `defaultMode: auto` is ignored, per
  [D-140](../../../adr/0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md)). The law: the default is recommended-and-yielding, the copy plain and
  behavioral, Routine never boots a stalling mode, and the platform field is verified live before the build
  relies on it.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Three stances on two axes** — permission posture (read vs write) × attendance (interactive vs unattended); the fourth cell (unattended-read) is intentionally empty (Actions cron, not a stance). No slot numbering, no transition matrix; the prototype's per-session slot machinery is gone. | Read this description against the built behavior and confirm they match. | operator |
| **Stance is session-scoped and never persists** — an ephemeral, session-keyed, non-committed signal that resolves to Explore in every ambiguous case, so every session boots Explore and no stance survives a session. | Read this description against the built behavior and confirm they match. | operator |
| **Explore is grounded and gated, the gate honest** — boot grounds every session; the `PreToolUse` write-gate denies the enumerated building set and allows everything else, a fallible §6 nudge backstopped by the merge wall, never dressed as reliable. | Read this description against the built behavior and confirm they match. | operator |
| **Entry is a deliberate operator act for both write stances** — Build via an operator-typed verb the model cannot self-invoke **or by accepting a plan** (the model cannot accept its own plan), both interactive; Routine via the operator-authored scheduled fire that invokes `/engine-routine`, whose authority is the schedule + the frozen scope-locked build Issue. None is silent or by-default self-election; self-election is made visible and effortful, never claimed impossible. | Read this description against the built behavior and confirm they match. | operator |
| **Stance is operator-legible** — current stance, denials, and the entry into Build are all surfaced in plain language; informed consent requires the operator know which stance is in force. | Read this description against the built behavior and confirm they match. | operator |
| **Build and Routine are stances; their workflows are build-orchestration's** — modes fixes the entry principle and the unattended posture, and defers the build/routine *mechanism* so the two never describe it twice. | Read this description against the built behavior and confirm they match. | operator |
| **The native permission-mode default is recommended, not imposed** — plan mode is the recommended interactive default (posture/ergonomics over the Explore gate, never the guarantee), a separate axis from the stance and **not** a Build-entry trigger; it is written at provisioning as operator config that **yields** to an existing operator preference, changed later via native `/config`, and **overridden by Routine's non-interactive launch posture** so an unattended run never stalls. | Read this description against the built behavior and confirm they match. | operator |
