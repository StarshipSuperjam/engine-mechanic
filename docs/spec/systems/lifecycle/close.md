---
status: draft
---

# Close

*Settled in the design workspace on 2026-06-09, ratified by [decision 0188](../../../adr/0188-resolve-the-d-187-operator-presentation-relay-re-litigation.md).*

## Summary

"Close" has two senses, and the heavy ritual is gone from both.

- **Session close = the pull request submitted for human review** — owned by the
  [build orchestration](build-orchestration.md). Close does not define it; there is no archive,
  changelog, or shutdown sequence, and merge-and-walk leaves nothing dangling.
- **Turn close = the `Stop` hook**, which this system owns. It fires at the end of every turn and does
  exactly two things: ambient [memory](../cognitive/memory.md) capture, and the
  **finding-disposition gate**.

Collapsing close to these two removes the prototype's close-friction spiral at the root — no
reserved-subject commits, no `CLOSE_ALLOWED_GLOBS`, no partial-close recovery, because there is no bespoke
close commit to shape-police ([D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)).

## Behavior

### Ambient capture — content survives, reflection defers

Every `Stop` appends the turn's session-id-tagged delta to the [memory](../cognitive/memory.md)
ledger. This is **memory's mechanism**; close only triggers it and never gates it. Because the append is
ambient, an ungraceful exit (the operator says "I'm done" and walks) loses **no content** — only the
deferred consolidation, which memory recovers by its **boot-time, session-id-keyed sweep** of a session
that ended without consolidating. "Your work is saved even if you just close the window" is therefore true
of the *content*; only the expensive reflection waits for a tolerable moment. Close does not depend on a
graceful shutdown, and in particular does not depend on `SessionEnd`, which the locked
[hooks](../infrastructure/hooks.md) law treats as best-effort — it cannot block and is not
guaranteed to fire.

### The finding-disposition gate

Under the standing pushback habit, every concern the session **raises** takes exactly one durable
disposition — fixed in line, logged as a GitHub Issue, or escalated — and none dies in a chat aside
([policies](../surfaces/policies.md)). The `Stop` [hook](../infrastructure/hooks.md)
pushes back until each raised concern is dispositioned, then emits the plain-language summary the operator
reads instead of the transcript ("*everything I flagged this turn is handled — 1 fixed, 1 saved as a
follow-up item*"). On a turn that raised nothing needing action, the summary is quiet. Because no hook channel reaches the
operator ([constraints](../../../reference/constraints.md)), this summary, the disposition block-prompt, and the
fail-open notice are delivered by the AI in chat per the [operator-presentation relay](../../../reference/glossary.md)
— relayed **emphatically** (the close gate is in the must-push set) so a finding needing a decision is never
silently dropped; the relay is posture, the merge wall the backstop.

This is the trust spine, so it is one of the two members of the locked
[hooks](../infrastructure/hooks.md) block budget that close owns — the other member is
[modes](modes.md)' explore write-gate. Its enforcement is named honestly, at the tier locked
[policies](../surfaces/policies.md) already fixes: **posture plus a strong local block**, not an
absolute wall.

- **What is mechanical.** The gate hard-blocks the turn (the `Stop` hook returns a block with a reason,
  looping the model back to disposition) while an **ephemeral, session-scoped findings record** still holds
  an undispositioned entry. That record is a session-runtime checklist the gate reads — session-keyed,
  off-repo, never read across sessions — **never a committed or gitignored findings ledger** (that would
  resurrect the dissolved session archive [D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md) and duplicate
  [telemetry](../guardrails/telemetry.md)'s debt register, which is the view over open Issues,
  [D-040](../../../adr/0040-telemetry-designed-end-state-native-signal-of-record-tracked.md)). The durable dispositions live where policies puts them — the edit,
  the Issue, the escalation; the record only tracks *what still needs one this session*.
- **What is posture.** Writing a raised concern into that record is the AI's discipline, so the gate's
  reach is the **recorded subset**: it cannot block on a concern the session never recorded. The standing
  pushback habit is what populates the record; the gate enforces it.
- **What is the wall.** The durable, unbypassable backstop is human review at the protected-branch merge
  ([control-plane](../infrastructure/control-plane.md), [principles §6](../../../principles.md)) —
  but that wall reviews a *change set*, so it catches findings that touch the work under review, not a
  purely observational finding the AI never recorded. That residual class is covered only by the recording
  posture and by re-surfacing at the next [boot](boot.md) — stated, not papered over.

The operator-facing promise is therefore "*everything I flagged this turn is handled*," never
"nothing the engine noticed is dropped" — the honest claim the mechanism can keep.

#### Bounded, legible, and leak-proof at the edges

- **The block is bounded** ([principles §6](../../../principles.md)): a strong local block, not an absolute
  wall — the [hooks](../infrastructure/hooks.md) block-budget law force-ends the turn after a
  bounded, operator-configurable number of consecutive `Stop` blocks. Burying a finding takes deliberate
  effort while the durable backstop stays the merge.
- **Cap-exhaustion degrades a *recorded* finding to *logged*, never *lost*.** On the forced continuation
  (`stop_hook_active` set), any still-undispositioned recorded finding is **emitted as a tracked finding
  down the same out-of-band promotion path** — the locked [policies](../surfaces/policies.md)
  "log it" disposition — and **never re-entered into the gate** (which would deadlock the loop), so the cap
  can never leak a recorded finding into silence.
- **A disposition loop is legible.** Repeated pushback surfaces one plain sentence ("*sorting out where the
  open findings should go — one moment*"), and a cap-stop is announced, so a non-engineer never meets an
  unexplained hang.
- **The gate fails open, and says so.** Per the [hooks](../infrastructure/hooks.md)
  fail-open-and-flag law, a gate that cannot evaluate lets the turn end; the failure is **auto-logged as a
  tracked finding by the promotion path itself** — never routed back through the gate it bypassed, which
  would deadlock — and is surfaced to the operator **in plain language that same turn** ("*I couldn't run
  the check that confirms nothing was dropped — review this turn's work with extra care*"), not deferred to
  the next boot. In an unattended [routine](modes.md) turn no operator is present that turn, so the
  same-turn notice degrades to the tracked finding alone, which surfaces at the next boot — no consent is
  lost, since the auto-logged finding survives regardless.

### Routine — satisfiable without a human

An unattended [routine](modes.md) run cannot ask, so the gate must be satisfiable
non-interactively or the run would deadlock (the locked [hooks](../infrastructure/hooks.md)
mode-awareness law). It is: the **log-it disposition** discharges any finding without a human — the routine
arm of the locked escalation [policy](../surfaces/policies.md). Whether the run then **halts** (an
escalation-worthy decision) or **continues** (a mere out-of-scope observation) is the escalation policy's
and the [build orchestration](build-orchestration.md)'s call, not close's; close fixes only that
the gate never deadlocks an unattended run.

### Subagent findings

`SubagentStop` is unbound ([hooks](../infrastructure/hooks.md)), so the **ambient** findings a
spawned (e.g. Explore) subagent surfaces into the session are swept by the parent session's `Stop` gate
like any other. This is distinct from the [build orchestration](build-orchestration.md)'s
**review-lens** subagents, whose findings are dispositioned at the orchestration's own gates via their
output contract — not deferred to the parent `Stop`.

### A maintainer-layer doc

The vocabulary here — `Stop`, the block budget, fail-open, the session-scoped record — is maintainer
framing and never reaches an operator-facing surface; the operator sees only the plain-language disposition
summary and notices ([principles §12](../../../principles.md) leak guard).

### Build-spec leaves

The laws above are fixed; these concrete forms are settled in the build-spec pass:

- the **ephemeral findings-record representation** — a session-keyed, off-repo runtime checklist the `Stop`
  hook reads (the [modes](modes.md) stance-signal pattern); the law is only that it is
  non-committed, session-scoped, and never read across sessions;
- the **disposition-summary wording** — quiet when nothing needs action, expanded when there is something to
  act on — and the plain-language loop / cap-stop / fail-open notices.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **No heavy ritual** — session close is the PR submitted (build-orchestration's); turn close is ambient capture plus the disposition gate. The archive, changelog, and shutdown sequence are dissolved ([D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)). | Read this description against the built behavior and confirm they match. | operator |
| **Capture is ambient, not close-gated** — content survives an ungraceful exit; only reflection defers, recovered by memory's boot sweep, never by the best-effort `SessionEnd`. | Read this description against the built behavior and confirm they match. | operator |
| **The disposition gate is the trust spine, named honestly** — posture plus a strong local block over an ephemeral recorded set: mechanical on what is recorded, posture for recording, the merge as the wall; satisfiable non-interactively for routine; degrading to *logged* at the cap and failing open with a same-turn notice. | Read this description against the built behavior and confirm they match. | operator |
