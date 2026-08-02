---
status: locked
---

# Close

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md); ratified as intended design on 2026-06-09 by [decision 0188](../../../adr/0188-resolve-the-d-187-operator-presentation-relay-re-litigation.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

"Close" has two senses, and the heavy ritual is gone from both.

- **Session close = the pull request submitted for human review** — owned by the
  [build orchestration](build-orchestration.md). Close does not define it; there is no archive,
  changelog, or shutdown sequence, and merge-and-walk leaves nothing dangling.
- **Turn close = the `Stop` hook**, which this system owns. It fires at the end of every turn and does
  two gating things — ambient [memory](../cognitive/memory.md) capture, and the
  **finding-disposition gate** — plus, on a turn that closes cleanly, a **non-blocking pre-close
  advisory pass** (validation's `pre-close` suite run locally as advice, never a gate).

Collapsing close to this short list removes the prototype's close-friction spiral at the root — no
reserved-subject commits, no `CLOSE_ALLOWED_GLOBS`, no partial-close recovery, because there is no bespoke
close commit to shape-police ([D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)).

## Behavior

### Ambient capture — content survives, nothing deferred

Every `Stop` appends the turn's session-id-tagged delta to the [memory](../cognitive/memory.md)
ledger. This is **memory's mechanism**; close only triggers it and never gates it. Because the append is
ambient, an ungraceful exit (the operator says "I'm done" and walks) loses **no content** — and under
memory's transcript-first design the appended delta *is* the durable record, so there is nothing left to
recover: no deferred reflection, no summarization pass, and no boot-time sweep (the sweep was deleted
whole with the curation model — [memory](../cognitive/memory.md)). "Your work is saved even if you just
close the window" is therefore true outright. Close does not depend on a
graceful shutdown, and in particular does not depend on `SessionEnd`, which the locked
[hooks](../infrastructure/hooks.md) law treats as best-effort — it cannot block and is not
guaranteed to fire.

### The pre-close advisory

On a turn that closes cleanly — the disposition gate has nothing left to hold — the same `Stop` handler
also runs validation's `pre-close` suite locally and surfaces any hard findings to the session as
**advice**. The pass is guarded in its own error boundary so it can never reach the disposition gate's
fail-open path, it never blocks the turn, and a local run reaches no GitHub event. It is early counsel
on the working tree, not a gate — the merge-time run of the same checks is where they can stop anything.

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
summary and notices ([principles §12](../../../principles.md) leak guard). An **AI-read operations
runbook counts as a maintainer-layer surface, not an operator-facing one** — its job is to instruct the
assistant, so backstage vocabulary there is permissible; what the leak guard fences is the copy the
operator actually meets at runtime — operator-ruled in the lifecycle-wave reconciliation.

### Build-spec leaves

The laws above are fixed; these concrete forms are settled in the build-spec pass:

- the **ephemeral findings-record representation** — a session-keyed, off-repo runtime checklist the `Stop`
  hook reads (the [modes](modes.md) stance-signal pattern); the law is only that it is
  non-committed, session-scoped, and never read across sessions;
- the **disposition-summary wording** — quiet when nothing needs action, expanded when there is something to
  act on — and the plain-language loop / cap-stop / fail-open notices.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **No heavy ritual** — session close is the PR submitted (build-orchestration's); turn close is ambient capture plus the disposition gate (plus the non-blocking advisory). The archive, changelog, and shutdown sequence are dissolved ([D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md)). | No merge-gated check asserts the dissolution; your observation that a session ends at the pull request with no archive, changelog, or shutdown step carries it. Partial support: the `block-coherence` check (hard, CI) confirms the disposition gate is close's declared `Stop` block — turn close is the gate, not a ritual — and the `in-tool-demo-failure-path` check (hard, CI) keeps the close demo falsifiable. | operator |
| **Capture is ambient, not close-gated** — content survives an ungraceful exit because the appended transcript delta is itself the durable record (no deferred reflection, no boot sweep), never depending on the best-effort `SessionEnd`. | Your observation carries it — end a session ungracefully and find the turn's delta in memory's ledger; structurally, no `SessionEnd` hook is bound in the deployed hook wiring. Partial support: the `in-tool-demo-failure-path` check (hard, CI) forces the close demo's capture relay to be falsifiable, and memory's capture tests exercise the append (CI test suite, not a merge-gated check). | operator |
| **The disposition gate is the trust spine, named honestly** — posture plus a strong local block over an ephemeral recorded set: mechanical on what is recorded, posture for recording, the merge as the wall; satisfiable non-interactively for routine; degrading to *logged* at the cap and failing open with a same-turn notice. | Your observation across a blocked turn, a cap-stop, and a fail-open notice carries it. Partial support: the `block-coherence` check (hard, CI) asserts close's `Stop` block sits on a block-eligible event and declares a non-empty, valid modes set (the declared set — which includes `routine` — is itself pinned by a CI unit test, not by that check); the `disposition-issue-resolution` check (hard, CI) asserts every follow-up issue a Review section cites is real; the `hard-check-bite` check (hard, CI) proves those checks bite; the gate's block, cap-degrade, and fail-open logic is pinned by the close and hooks test suites (CI tests). The unbypassable wall is the protected-branch merge, not a check. | operator |
