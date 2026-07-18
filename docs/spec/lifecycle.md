---
status: draft
---

# Lifecycle

## Summary

Lifecycle governs a session from first grounding to shipped change: how every session orients and reports itself at boot, the three operating stances and their entries, how build work is planned, reviewed, integrated, and submitted, what closes each turn, how contributions reach a repository the operator does not own, and how the engine's own releases are cut. The stance model, the claim/plan surfaces, the hook block budget, and the boot refresh family are engine canon (eADR-0024, eADR-0025, eADR-0022, eADR-0033); this document states the laws layered on that canon.

## Behavior

### Boot

The first thing the assistant shows each session is a named status block — an all-clear line or a plain-language alarm — before it addresses the prompt. Its presence is the operator's binary did-it-ground check: a first reply that jumps straight into the request means the session did not fully ground (ADR-0043).

Everything the engine surfaces in-session reaches the assistant, never the operator's screen, so the assistant relays it: the safety-critical subset — governance alarms, a grounding-failure tell, consent-critical prompts — is pushed in plain words every session it applies; routine detail is pulled on demand through a status verb (ADR-0043).

A leftover template license is surfaced as provenance, not fault, leading with the private-by-default reassurance and ranked below governance alarms. Declining collapses it to a terse reminder that never goes fully silent; an explicit "I meant to keep this" retires it from that checkout. Retire-eligibility is a fixed per-finding-class property enforced by the deterministic mechanism, never a model-asserted label, so a governance alarm can be declined but never retired (ADR-0046).

The standing-situation card renders milestones honestly: none open reads as the normal state ("no milestone is open," never a claim the project keeps none), and several open render as the several they are, named — the engine never silently elects one "current." Boot relays the state system's selection bound by name and restates none of it (ADR-0046).

A genuinely broken operator checkout — detached, or missing engine files — is detected at boot by binary offline checks and relayed read-only with an offer to fix; ordinary behind-ness never alarms on bare distance. The consented fix is lossless-or-it-does-not-run: a rescue branch precedes any risky step and divergence is never silently fast-forwarded (ADR-0044).

### Modes

The stance model is canon (eADR-0024): three stances on two axes, session-scoped, resolving to Explore in every ambiguous case, with entry into a write stance always a deliberate, announced, human-only act. This document adds the entry and posture laws below.

At install the engine writes a recommended plan-mode default into this repo's committed settings as operator config — reading, never writing, the operator's own settings; a differing existing preference gets one conflict-only offer, and declining writes nothing. A later mode change is an ordinary preference, never treated as a guardrail-weakening event (ADR-0042).

Accepting a plan enters Build with exactly one announced kickoff. The stance signal is the sole durable stance record, cleared at every session start, so a resumed session neither acts on nor reports Build from any replayed nudge — it re-derives stance live and boots Explore (ADR-0042).

An unattended run enters Routine only through the engine-prefixed entry command the operator embedded in the schedule's own instructions; its authority is that schedule plus the frozen, scope-locked build Issue it reads — never model self-election. A fire that finds no valid target leaves a durable Issue, never a silent exit, and the first fire echoes the build Issue it locked onto so a mis-aim surfaces on the first cycle. The run's launch posture is non-interactive — it genuinely cannot ask — and overrides the interactive plan-mode default so it never stalls (ADR-0041, ADR-0042).

### Build orchestration

The build surfaces are canon (eADR-0025): the draft pull request is the claim, the build Issue the forward plan, the operator's merge the only unbypassable wall. The workflow atop them follows one fixed gate shape — plan, plan review, implement, integrate, pre-submission review, submit — with review lenses derived from what is installed; the shape is posture, honestly named, and its one mechanical hook is that the PR cannot submit without a present, non-empty Review record (ADR-0039).

Before any spend, the operator meets a plain-language risk assessment: a headline that varies with the actual change, a consequence-named depth choice in the operator's language, and a cost-and-time estimate. After the audit, findings arrive as one synthesized recommendation with every disposition surfaced; an unresolved blocking finding always re-engages the operator (ADR-0039).

The orchestrator is the single writer of final commits: workers generate work product in isolated worktrees, and the orchestrator reviews, revises, and authors the cohesive set — delegation buys cohesion under context pressure, not speed (ADR-0039).

Validation runs green before the expensive judgment review and reruns on every change; the cold audits run once at the agreed depth, and the Review record states any post-audit fixes as validated but not re-reviewed. The Review record states in-block that it is the engine's own account and the operator's approval is the real gate (ADR-0039).

Depth scales to a genuine floor: a trivial change is one entry, one glance, one merge — no checklist, no lenses, a single headline confirm (ADR-0039).

Routine is the same workflow's implement phase distributed across unattended, scheduler-serialized sessions, reserved for decomposable bulk work (a plan-time judgment, recommended against when work is coupled); it accumulates commits on the open PR, files an Issue and halts on anything needing a human, and never auto-merges (ADR-0039).

At submit, the orchestrator compares what the PR will actually close against the closing intent its structured scope declares. Any contradiction is surfaced in the Review record in plain language; only an unambiguously accidental keyword may be neutralized, minimally and with disclosure. Cross-repo closes are surfaced and named, never adjudicated. The operator's own will-close view at the merge bounds both paths (ADR-0040).

Build and Routine work runs in isolated per-session worktrees; the top-level operator checkout is a protected operator surface whose git state is never mutated as build work, autonomously, or unconsented (ADR-0044).

### Close

A build session closes when its PR is submitted — there is no archive, changelog, or shutdown ritual. Turn close does exactly two things: it triggers ambient memory capture, and it runs the finding-disposition gate (ADR-0038).

Every concern the session raises takes exactly one durable disposition — fixed, logged as a tracked follow-up, or escalated — and the turn cannot end while a recorded concern lacks one; the operator then reads a plain summary of how each was handled. The promise is "everything I flagged this turn is handled," never "nothing the engine noticed is dropped" (ADR-0038).

Exhaustion and failure never lose a recorded finding: past the bounded block budget a finding degrades to logged via a promotion path that never re-enters the gate, and a gate that cannot evaluate fails open, auto-logs its own failure, and tells the operator the same turn. An unattended run satisfies the gate without a human via the log-it disposition (ADR-0038).

### External contribution

Contributing to a repository the operator does not own is canon (eADR-0026): fork-native, the Engine kept off the contribution by posture, the unbypassable wall relocated to the upstream's own review — with the honest line, for an ungoverned upstream, that the fork-side checks are the only real gate. Lifecycle adds no law of its own here: close keeps its shape (the submitted cross-fork PR), the operator is narrated plainly that submitted is not accepted, and an unreachable upstream still leaves a working fork.

### Upgrade

Engine versions are produced by a standing maintainer-side release-cut process: a mechanical floor computed from the changes since the last release sets the minimum bump, and the maintainer confirms — unconditionally, on evidence: a plain-language change inventory, impact statements, and a break/no-break demonstration where one exists — never by reading code. The release lands as a PR through the control-plane gate, the tag at the exact reviewed merge commit, single-flighted, every release gated on the acceptance benchmark (ADR-0045). Consumption in deployed repos — the tagged-release overlay and migrations — is provisioning's; lifecycle owns only production.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| The assistant's first output each session is a named status block (all-clear or alarm) before it addresses the prompt | Open a session and read the first reply | operator |
| A held safety-critical condition (e.g. branch protection off) is relayed in plain words every session it holds | Seed the condition in a fixture repo; observe the relay each session | engine |
| A resumed session after a Build session reports Explore and denies building until re-entered | Conformance: resume after acceptance; check stance line and a denied write | engine |
| Accepting a plan yields exactly one announced Build kickoff; a rejected plan stays in Explore | Conformance: accept and reject a plan; count kickoff announcements | engine |
| Declining the offered plan-mode default writes nothing; an existing preference is never clobbered | Install with a differing preference; decline; inspect committed settings | engine |
| A scheduled fire that finds no valid target leaves a durable Issue, never a silent clean exit | Conformance: fire the routine at a missing/mis-aimed build Issue | engine |
| The first routine fire echoes the build Issue it locked onto | Read the first run's status output | operator |
| An unattended run never stalls on a question: it files an Issue and halts or continues per policy, and never merges the protected branch | Conformance: seed a decision-needing chunk; check Issue, halt message, unmerged PR | engine |
| A build cannot submit without a present, non-empty Review record | Mechanical completeness check on the PR body | engine |
| The risk assessment (headline, consequence-named depth choice, cost estimate) precedes any implementation spend | Read the transcript of a build session: consent comes before work | operator |
| An unresolved blocking finding always re-engages the operator before the build advances | Conformance: seed a blocking plan-review finding; check for adjudication | engine |
| A green validation baseline precedes pre-submission review; post-audit fixes re-validate and the Review record states they were not re-reviewed | Inspect the Review record and check ordering on a fixture build | engine |
| A trivial change collapses to one entry, one glance, one merge | Run a typo-fix build; observe no checklist, no lenses, one headline | operator |
| A PR set to close an issue its scope declares only part of is surfaced — or minimally defanged with disclosure — before the operator merges | Conformance: prose closing keyword + part-of scope; check the Review line | engine |
| A turn that raised a concern cannot end until it is dispositioned, and the end-of-turn summary states how each was handled | Raise a concern mid-turn; read the summary | operator |
| Cap exhaustion or gate failure yields a logged tracked finding plus a same-turn plain notice, never silence | Conformance: force the gate to fail; check the finding and the notice | engine |
| The operator checkout's git state is never mutated by build work; a broken checkout draws a boot-time offer with a lossless, rescue-branch-first fix | Conformance: seed a detached checkout; observe the offer; verify the rescue branch | engine |
| No milestone open renders as "no milestone is open"; several open render as several, named | Read the status card in each state | operator |
| Retiring a kept license silences only that finding on that checkout; a governance condition can never be retired | Conformance: plant a retired marker against a governance condition; alarm still renders in full | engine |
| A cross-fork contribution PR carries only product paths, and the operator is told submitted is not accepted | Inspect a fixture cross-fork PR's diff; read the submission narration | engine |
| A release tag lands only at the reviewed merge commit, after a recorded maintainer confirmation against a plain-language change inventory | Inspect the release run record and the tag's commit | operator |
