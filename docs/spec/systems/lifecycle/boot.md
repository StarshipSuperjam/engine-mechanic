---
status: draft
---

# Boot / orientation

*Ratified in the design workspace on 2026-07-16 by [decision 0319](../../../adr/0319-resolve-re-lock-boot-relay-state-s-milestone-selection-bound.md). Carried here as an **in-progress** description of intended design — the built engine has drifted from it; see the [product spec index](../../../spec/index.md).*

## Summary

Orientation is not one event. It is a **family of cognition-refresh moments**, each rendering a
bounded, prioritized view from committed [state](../cognitive/state.md) and (when available)
the substrates. "Boot" is the heaviest member — the cold-start assembly — but the same machinery, and
the same [attention](../cognitive/attention.md) ranking function, drives the lighter members.
All orientation is **read-only of canonical state** — it never regenerates derived or committed state.
Orientation's sole local write is a gitignored, non-canonical presentation marker (the *standing-alarm
presentation ledger*, [below](#anti-habituation-collapsing-an-unchanged-standing-alarm)): presentation
bookkeeping that records what was already shown, never state regeneration. Other substrates' writes ride
boot's `SessionStart` **moment** without being boot's: each belongs to the substrate that owns it — as
[memory](../cognitive/memory.md)'s consolidation sweep does ([below](#the-cold-start-boot-pack)),
so does [modes](modes.md)' stance clear, and so does the regenerable, gitignored slice cache
[knowledge](../cognitive/knowledge.md) rebuilds when stale. None is canonical state, and none is
orientation.

**Boot is unconditional at the floor; the rich pack rides on top.** The `SessionStart`
[hook](../infrastructure/hooks.md) runs on every session start regardless of what the operator
types or intends, so **every session — Explore included — begins from a known grounding floor whenever the
hook runs**. There is no manual "start the engine" step. The hook is fail-open and conditional on being
registered, so what is truly *guaranteed* is the **floor**: the hook-independent root `CLAUDE.md` (below)
grounds the session even when the hook does not run, and the rich boot pack rides on top when it does.
Either way a session that has grounded cannot answer from ad-hoc file-poking, which is what lets
[Explore](modes.md) be the safe default.

## Behavior

### The orientation event family

Each event has a cost budget governed by the rule *latency while building is tolerable; latency while
using is not*:

| Event ([hook](../infrastructure/hooks.md)) | Behavior | Budget |
|---|---|---|
| Session start / resume (`SessionStart`, `source: startup` or `resume`) | full boot pack (heavy assembly); also fires [memory](../cognitive/memory.md)'s abandoned-delta consolidation sweep (memory's operation, not orientation) | once per start/resume |
| Every prompt (`UserPromptSubmit`) | the cheap lexical **scent** (below) | every turn → ~zero |
| Post-compaction | the next `UserPromptSubmit` scent re-orients, over the re-injected root `CLAUDE.md` floor; a full boot-pack re-render on `SessionStart`'s `compact` source is a deferred enhancement (see *Post-compaction grounding*, below) | rare |
| Commit boundary (`PreToolUse` git intercept) | [knowledge](../cognitive/knowledge.md) regen — a mutation, not orientation | per commit |
| Turn end (`Stop`) | ambient [memory](../cognitive/memory.md) capture + the finding-disposition gate ([close](close.md)) — not a heavy ritual | every turn |

**Boot owns the event model; [attention](../cognitive/attention.md) owns the budget within it.**
Which moments fire, the [hook](../infrastructure/hooks.md) driving each, and each event's cadence
and cost tier are boot's; how an event's context budget is split across categories — and how that split
flexes (a clean session gets more orientation; a high-debt one compresses it) — is attention's
([D-062](../../../adr/0062-lock-the-attention-system-wave-2-the-policy-plus-function-pr.md)).

**Post-compaction grounding.** Compaction does not strand a session. The platform re-reads and re-injects
the root `CLAUDE.md` floor after a `/compact` (a disk reload, hook-independent — substantially reliable
though not airtight), and the next `UserPromptSubmit` scent re-surfaces topical pointers; together these
are the reliable floor. A documented re-injection hook also exists — `SessionStart` fires with a `compact`
source and can inject `additionalContext` — so a full boot-pack re-render after compaction is *possible*;
but that injection is **field-unreliable** (tracked upstream) and **must never be depended on as a
grounding guarantee**, so the engine does not use it. A full re-render on the `compact` source is a
**deferred enhancement**, gated on upstream reliability, on its own budget tier, and on a guarantee that it
does **not** re-fire memory's `SessionStart`-borne consolidation sweep (which a naïve re-run would). The
reliable post-compaction floor stays the re-injected `CLAUDE.md` plus the next scent.

A **resume** is not compaction. Re-opening a paused session (`--resume`/`--continue`/`/resume`) fires
`SessionStart` with `source: "resume"`, whose `additionalContext` injection is **reliable**
([constraints](../../../reference/constraints.md)) — so the full boot pack, including the anti-habituation collapse
([below](#anti-habituation-collapsing-an-unchanged-standing-alarm)), re-renders normally on resume. The
field-unreliable path is the `compact` source alone; the verbatim re-rendering an operator meets across
resumes is exactly what the collapse below addresses.

### The cold-start boot pack

1. A `SessionStart` [hook](../infrastructure/hooks.md) assembles the boot pack (it injects context before the first prompt; [constraints](../../../reference/constraints.md)); its machine-consumed orientation artifacts live under `.engine/boot/` per the [repository topology](../infrastructure/repository-topology.md) placement law.
2. Read committed [state](../cognitive/state.md) and the surface catalog's recognition slice (the [ontology](../grammar/ontology.md) consumption law) — an input read before ranking, the same standing as committed state, never a ranking candidate; carried in the pack on every render, with no dedup — at a few hundred characters the repetition does not earn a mechanism. (A session-keyed dedup is also **reportedly** unavailable, since `session_id` is re-issued on resume — [constraints](../../../reference/constraints.md), held at a weak tier. The ruling does not rest on it: the slice re-renders because it is too cheap to bother deduping, which holds either way.) Pull [knowledge](../cognitive/knowledge.md) structure and [memory](../cognitive/memory.md) recall when their servers are up.
3. [Attention](../cognitive/attention.md) allocates the bounded budget across blocking debt, in-flight work (open branches and pull requests), recent decisions, structural neighbors, and orientation.
4. Surface the [telemetry](../guardrails/telemetry.md) debt register (persistent warns, threshold crossings, open findings) and the current [stance](modes.md) in plain language.
5. Branch into the stance's continuation.

#### What boot surfaces — alarms pinned, in priority order

**Boot assembles for the model; the operator meets it through the AI.** The pack is injected as the AI's
*briefing* and reaches the model, never the operator's screen ([constraints](../../../reference/constraints.md) — the
AI's own message is the sole in-session operator channel). So what boot "surfaces" is realized by the
[operator-presentation relay](../../../reference/glossary.md): the safety-critical subset is **pushed** — the AI relays
it in plain language every session, carried by an imperative marker — while routine status is **pulled** on
demand via the [status verb](../../../reference/glossary.md). The pack stays a complete AI briefing regardless of what
is user-surfaced; the priority order below is the order the AI relays the pushed subset behind the
present-marker block.

A cold start can have many things to say, especially when degraded. Boot surfaces them in a fixed priority
so the one that matters is never buried: **governance-critical alarms first and visually distinct** — the
protected branch is off ([control-plane](../infrastructure/control-plane.md), below) — then the
[attention](../cognitive/attention.md)-ranked debt and in-flight work, then informational digests
(recently-shipped, the current [stance](modes.md)). A [§15](../../../principles.md) guardrail
weakening is surfaced where §15 puts it — hard-gated at the human merge, in
[control-plane](../infrastructure/control-plane.md)'s plain-language acknowledgment gate, which
owns the detection — so boot carries no weakening alarm of its own; the protection-off alarm above is what
tells the operator the gate itself is not running. "Loud" must not silently become noise the
operator scrolls past. Two things keep a standing governance alarm from becoming wallpaper. First, the
governance-critical ones are **actionable, not merely loud**: the protected-branch alarm **offers to fix it
for you** (below), so the operator *clears* it rather than learning to ignore it. Second, across sessions a
*standing* alarm whose underlying condition is **unchanged** is **collapsed to a terse reminder** rather than
re-relayed in full, so repetition does not bury the signal — the anti-habituation mechanism
([below](#anti-habituation-collapsing-an-unchanged-standing-alarm)), which suppresses the *repetition*,
never the *signal*.

Six of these are surfacings the substrates defer to boot, rendered here in plain language:

- **A refused state file.** If the committed [state](../cognitive/state.md) cursor is malformed,
  state refuses it (it is never fed to the model as a misleading cursor); boot surfaces the refusal as
  injected context and emits a [telemetry](../guardrails/telemetry.md) finding — **never a
  `SessionStart` exit-code halt** — and falls through to the floor below. The session does not crash; it
  says, plainly, "*I couldn't read where the project stands, so I'm treating project status as unknown.*"
- **Reversible forgetting.** When [memory](../cognitive/memory.md) has consolidated, demoted, or
  logically retired recall — all **reversible and recoverable** — boot shows a plain-language readout of
  what changed with an undo handle per item, so a silent loss of the operator's brainstorming never
  happens. **Permanent erasure is not a boot event and carries no undo handle:** memory never erases recall
  on its own; an erasure is *proposed* as an engine-labeled finding the operator adjudicates by merging a
  single-purpose erasure pull request (surfaced like any other open finding, above; what was erased is
  recorded in the [audits](../guardrails/audits.md) digest among the informational digests).
  Boot owns this readout's wording; memory owns the mechanism.
- **The protected branch is off.** Boot continuously surfaces an unprotected protected branch in plain
  language — "*this repo's safety gate is off, so unreviewed work could reach your main branch*" — reading
  the per-branch evaluated-rules signal the [control-plane](../infrastructure/control-plane.md)
  bootstrap contract defines, and **offers to fix it for you** (the engine runs your own `gh` once you
  approve the one-time permission). It never asks a non-engineer to type a command. *Detecting* the gap is
  the control-plane's contract and *applying* the fix is
  [provisioning](../infrastructure/provisioning.md)'s first-run mechanism; boot only surfaces it
  and offers the fix (Risk [R1](../../../reference/risks.md)).
- **A missing or unhealthy tool-runtime.** When a [hook](../infrastructure/hooks.md) or validator
  could not run because the engine [tool-runtime](../infrastructure/repository-topology.md) is
  absent or broken, boot surfaces it read-only in plain language — "*the engine couldn't run its own tools
  (its private Python environment isn't ready); I haven't verified this work*" — as an open finding, and
  points the operator at the fix [provisioning](../infrastructure/provisioning.md) owns
  (re-materialize the runtime; offer a retry). *Detecting* the failure is the
  [hooks](../infrastructure/hooks.md) fail-open-and-flag law and provisioning's; *applying* the
  fix is provisioning's; boot only surfaces it. When the runtime is so absent that the `SessionStart` boot
  hook itself cannot run, this line cannot render — that **double fault** is caught instead by the root
  `CLAUDE.md` floor's present-marker check below (no project-status card ⇒ the engine did not ground). It
  ranks below the governance-critical alarms ([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md), Risk [R18](../../../reference/risks.md)).
- **A stranded or off-main operator checkout.** When the [operator checkout](../../../reference/glossary.md) has **drifted
  into a broken state** — a detached `HEAD`, or missing/critically-stale engine files —
  [provisioning](../infrastructure/provisioning.md)'s standing detector (which boot invokes) catches it,
  and boot surfaces it read-only in plain language — "*your project folder has drifted into a broken state; I
  haven't been working in it, but here's how to get it healthy*" — and **offers to fix it for you**. The detector
  also catches a checkout **parked off your main project line** (sitting on a side branch): the gentlest standing
  signal, surfaced **on day one** and collapsing to one quiet line when unchanged (the anti-habituation ledger
  below); and, when that checkout is **missing merged work**, it **escalates** to a firm offer naming the
  consequence — "*your project folder is showing an older version of your project — it's missing the last few
  weeks of finished work; nothing is lost, and with your OK I'll bring it up to date*". On approval the engine performs
  the correction (re-materialize the missing files / re-attach / bring your folder back to the main project and
  current), *only when nothing would be lost* and otherwise saving any unsaved work safely first, never a command
  the operator must type; whether the side branch holds unfinished work changes only the reassurance ("*your
  unfinished work stays exactly where it is, nothing deleted*"), never the single decision the operator makes.
  Because this catch is **new**, the first full relay **owns the gap** — "*earlier sessions couldn't spot this;
  that's fixed now*" — so a folder reported healthy for weeks is not silently re-cast as freshly broken. Ordinary
  *behind* on the main project line is the normal state under the worktree-and-PR model
  ([build-orchestration](build-orchestration.md)) and is **not** alarmed on a bare distance — only the
  broken states, the off-main park, and a concrete *missing-merged-work* consequence are. *Detecting* and
  *applying* are provisioning's; boot only surfaces and offers. It **ranks below the governance-critical alarms** —
  a stranded or off-main local checkout cannot reach the protected branch, so it is not guardrail-critical —
  beside the tool-runtime surfacing; and like it, in the **double fault** where the boot hook itself cannot run,
  this line cannot render, and the root `CLAUDE.md` floor's present-marker is the backstop ([R20](../../../reference/risks.md)).
- **A brand-new project that hasn't been set up.** When the repo is **unprovisioned** — a fresh project generated
  from the template, all engine files present but first-run setup never completed (the verdict
  [provisioning](../infrastructure/provisioning.md) owns: instantiator present, and **not** the
  construction repo) — boot surfaces it read-only and **offers to walk first-run setup**: "*this looks like a
  brand-new project that hasn't been set up yet — a short guided setup that helps turn on your safety gate and gets
  the engine's tools ready; want me to walk you through it?*". It is framed as the operator's **own new project**,
  never an engine "copy"; it names what setup does in one plain clause; and it is always an **offer the operator can
  decline**, never a gate (boot stays read-only and never blocks). When fresh-vs-existing is genuinely ambiguous — a
  fork, or an existing repo the engine was added to — the offer is **self-correcting**: "*if this is actually an
  existing project, just tell me and I'll stand down*", so it never confidently mis-reads. Because the offer never
  gates, it is **standing** — it persists every session until setup actually runs, collapsing to one quiet line when
  unchanged (the anti-habituation ledger below) — so a deferred "later" cannot silently leave the operator working in
  a half-set-up repo with no standing tell (the same false-confidence trap a dead-on-arrival repo created, closed
  rather than re-opened one layer up). *Detecting* the unprovisioned state is provisioning's mechanism; boot only
  surfaces and offers. This is a **distinct lifecycle condition** from the stranded/off-main checkout above — all
  engine files are present and nothing has drifted; the repo has simply never been set up — so it is its own
  surfacing, not a widening of the strand catch. It **ranks below the governance-critical alarms** beside the
  tool-runtime and checkout surfacings (an unprovisioned fresh copy cannot reach a protected branch — there is not
  one yet); and like them, in the **double fault** where the boot hook cannot run, the root `CLAUDE.md` floor's
  present-marker is the backstop. The surfacing ships only once the template no longer carries the construction
  residue that would make a fresh copy indistinguishable from the workshop
  ([provisioning](../infrastructure/provisioning.md); [D-277](../../../adr/0277-litigate-engine-template-353-first-run-dead-on-arrival-in-a.md)).
- **A leftover template license the engine copied in.** When the [operator checkout](../../../reference/glossary.md)'s root
  `LICENSE` **still carries the template's own license** — the copyright the engine's template shipped, copied into
  the product slot by "Use this template" and never cleared (a repo generated before the first-run clear shipped,
  or drifted back to it) — [provisioning](../infrastructure/provisioning.md)'s standing foreign-seed
  detector (which boot invokes) catches it, and boot surfaces it read-only in plain language and **offers to tidy
  it for you**. It is framed as **provenance, not a problem with your project**, and **leads with the
  private-by-default reassurance**: "*your project is private and yours by default — your code is yours until you
  choose to share it. One tidy-up: a license file copied in from the template you started from is still sitting in your project under its
  author's name, not yours — leftover from how your project was created, not anything you did. With your OK I'll
  clean it up as a small change you approve, so you start from a clean slate and can add the license you choose. If
  it's one you meant to keep, just say so and I'll stop bringing it up.*" It **routes the judgment out** (an offer
  to explain what a license file is and help add the one you pick, `choosealicense.com`, a human for terms that
  matter), and is **factual, never legal advice** — never "all rights reserved" as a conclusion, never which
  license to choose. **On consent the removal lands as a small reviewed change the operator approves** the same way
  they approve any change — never an instant boot-time delete, because a live project's *committed* license is
  removed durably only through the reviewed gate ([build-orchestration](build-orchestration.md)); it adds
  no replacement (the license is yours to choose). If it is a license you **meant to keep**, telling the engine so
  **retires the offer from this checkout** (the intent-exit below) — the engine never nags a license you
  deliberately kept. *Detecting* is [provisioning](../infrastructure/provisioning.md)'s; the operator's
  consent is a **plan acceptance** — the sanctioned Build entry ([modes](modes.md)) — that hands the
  removal to [build-orchestration](build-orchestration.md)'s trivial fast path; boot only surfaces and
  offers, staying **read-only** and never entering Build itself. It **ranks below
  the governance-critical alarms** (a foreign license is bounded and operator-correctable — you own the root
  `LICENSE` — never guardrail-critical), beside the tool-runtime and checkout surfacings; and like them, in the
  **double fault** where the boot hook cannot run, the root `CLAUDE.md` floor's present-marker is the backstop
  ([R29](../../../reference/risks.md)). It is a **distinct finding** from the strand and unprovisioned conditions — its own
  structured-condition fingerprint in the anti-habituation ledger, so it never cross-collapses with them.

#### Anti-habituation: collapsing an unchanged standing alarm

A governance alarm renders on **every** session it is live — but re-relaying the same full plain-language
explanation each resume teaches the operator to scroll past it. Boot suppresses the *repetition*, never the
*signal*. A standing alarm whose underlying condition is **unchanged since it was last relayed in full**
collapses to a **terse one-line reminder that still names the consequence and still carries the offer to fix
it**; a **new, changed, or worsened** condition gets the **full** plain-language relay. New-versus-old is
carried in **words** ("*Still …* / same issue as before" versus "*New:* / this got worse") and never by
length alone, so a first-time operator with no prior boot to compare against can tell which is which. The
present-marker block itself ([below](#the-root-claudemd--the-hook-independent-floor)) is unaffected: it
renders every session and the **all-clear render never collapses** — only the *alarm payload behind* the
marker varies.

The cross-session memory this needs is the **standing-alarm presentation ledger**: a single **local,
gitignored, non-canonical** marker, read and written by boot's own `SessionStart` hook, recording for each
surfaced alarm a fingerprint of its **structured condition** — the per-branch evaluated-rules signal for the
protected-branch alarm, the open-findings identity set for the findings alarm — together with a
*shown-in-full* marker. The fingerprint is computed over the **structured condition, never
the rendered prose** (the prose is a build-spec leaf, model-reworded on relay), so the same standing
condition yields the same fingerprint session to session (collapse) while a changed one yields a new
fingerprint (full relay). The read, the terse-versus-full decision, and the write all execute in the
**deterministic hook**, not the model's relay — so the collapse never rides on model discretion; the model
relays what the hook handed it.

The ledger is **fail-toward-full**: a missing, unreadable, or write-failed ledger, or any fingerprint
ambiguity, renders the alarm **in full** (the safe direction — repetition is the tolerable failure,
suppression is not), and a ledger write that fails never blocks the turn
([hooks](../infrastructure/hooks.md) fail-open). It is **isolated from memory's `SessionStart`
consolidation sweep** — it shares no code path and never triggers it — and lives at a **stable per-instance
path** under the engine working tree (`${CLAUDE_PROJECT_DIR}/.engine/…`, the
[repository topology](../infrastructure/repository-topology.md) placement law), never inside an
ephemeral worktree, so it spans separate sessions on the one operator's machine. It is never committed, never
derived from source, and carries no [artifact warrant](../../../reference/glossary.md) (a transient gitignored cache
inherits its source's). The exact terse wording, the ledger's on-disk form, and the concurrent-session write
discipline (which must preserve fail-toward-full under a race) are build-spec leaves under that law.

The operator-facing promise boot's relay makes, so the behavior is verifiable without reading code: a problem
still here from last time shows as a short reminder that **still names the risk and still offers the fix**; a
new or worsened problem **always** shows in full; and a problem **vanishing** from the status block means the
engine **verified it is fixed**, never that it stopped checking. This also reaches the residual the
actionable-alarm mitigation could not: an alarm that **cannot** be made actionable — one with no one-click
fix — still collapses to a terse line that **keeps its consequence sentence**, so it neither becomes
wallpaper nor loses its meaning.

**The kept-on-purpose intent-exit — a bounded third disposition.** The collapse above assumes every standing
condition has one legitimate end state: *fixed*. That holds for the governance alarms (no operator both wants the
protected branch off and wants to build safely) and for the strand/unprovisioned conditions (a broken or
never-set-up checkout is never a state the operator *intends*). It does **not** hold for the
**leftover-template-license** finding: an operator may **deliberately keep** an inherited license — a fork's
attribution, or an org copyright that is legitimately theirs. For that class alone — a finding whose
**finding-class carries a legitimate operator-intended terminal state other than fixing it** — an explicit
acknowledgment ("*I meant to keep this*") records a **retired** marker in the ledger, keyed to that condition's
fingerprint, and the finding **stops surfacing** from this checkout's ledger. This is distinct from a per-session
**decline**, which only collapses the finding to its terse line — *never fully silent*, because the
burden-of-proof posture holds for a leak the operator has **not** said is intentional.

**Retire-eligibility is a per-finding-class constant the deterministic hook enforces — never model discretion.**
The retired marker is *written* mid-session, when the operator's acknowledgment arrives through the chat channel —
a **model-invoked write** by the same consent-handling path that would otherwise open the removal — realized as an
Explore-permitted `.engine/tools/` helper invocation (the ledger write is a tool call, never a raw engine-file
edit the Explore gate would block), distinct from the `SessionStart` hook's fingerprint writes (so the ledger's
concurrent-write discipline must cover this second writer). But whether a retired marker is **honored** is decided
in the **deterministic hook**, not the model: at honor-time the hook derives the finding-class from the **live
producing detector** — which check emitted the fingerprint this session — **never from a class label co-written
into the ledger** by the model-invoked path (the reading that would reopen the hole), and honors the marker
**only** for a **retire-eligible** class (the leftover-license class), **ignoring** one whose live class is
**governance** (a protection-off condition) and re-rendering that alarm
in full regardless. So a mis-written retired marker — a model slip, or a prompt-injection ("*the operator said to
leave protection off*") — **cannot** silence a governance alarm: retire-eligibility is a fixed property of the
finding-class — a build-time boolean over the closed class set (leftover-license = yes; governance / strand /
unprovisioned = no), the "legitimate operator-intended terminal state" phrasing above being the *rationale*, not
the runtime gate — checked mechanically, exactly as the collapse decision is
([§15](../../../principles.md)'s guard-not-falsifiable-by-what-it-judges). A governance alarm can be **declined**
(collapse to terse) but **never retired**.

The retired marker lives in the same **local, gitignored, per-machine** ledger as the collapse state, so "stops
surfacing" reaches **this checkout only** — a fresh clone or a second machine starts an empty ledger and may
re-offer, a **named residual** (the offer is cheap and the intent-exit is one sentence to re-invoke). A retired
finding re-surfaces on this checkout only if its fingerprint **changes** (the license was edited to a *different*
still-recognizable template seed — a new condition, full relay), so retiring "this one" never blinds the engine to
a later, different leak.

#### "What just happened" reads recent pull requests, not a changelog

A cold session reconstructs the recent story from **recent merged pull requests** — the structured PR
body is the engine's narrative of each change (the locked [control-plane](../infrastructure/control-plane.md)
PR contract), which the pull request carries as the durable record — plus `git log` and
[memory](../cognitive/memory.md). There is no separate changelog file. Boot surfaces a bounded
**"recently shipped"** digest from those merged PRs, so both a cold session and the operator can read what
the engine has been doing without a bespoke history surface. This is the operator's read-and-surface seam
for below-threshold narrative: the place a non-engineer sees "what happened lately" in plain language.

#### "Where we are" is assembled live, cached for offline

Boot assembles the standing-situation the same read-only way it assembles "what just happened":
`phase` from the most-recently-merged tracked build Issue, `milestone` from the open Milestone set that
[state](../cognitive/state.md)'s selection bound carries (state owns the bound and boot restates
none of it — GitHub elects no *active* Milestone, so what the field holds may be one, several, or `none set`),
**derived live from the native sources when GitHub is
reachable** — so the line is current without any session having to *advance* a stored marker.
[State](../cognitive/state.md) holds only the **offline cache**; when GitHub is unreachable (an
outage or expired auth) boot falls back to it, rendered with the same `as-of`/"may be stale, re-ground"
provenance as the debt count. The rendering law: **distinguish the live "where we are" from the cached one**
in plain language (the card shows **one** — live *or* cached, never both; a cached read names when it was
cached and that it may be stale), render a `none set` **`milestone` as an honest normal state** (no Milestone
is open — which is not a claim the project keeps none) and never as an error, **render a several-open
`milestone` as the several it is** — naming them, never silently promoting one to "current", since the engine
elects none ([state](../cognitive/state.md)'s bound, [D-315](../../../adr/0315-amend-d-314-correct-its-operator-authorship-premise-the-buil.md)) — and carry
**no engine jargon** (the [§12](../../../principles.md) leak guard — never "derived"/"assembled"/"cursor"). The exact wording is a build-spec leaf under those laws
and the alarms-pinned law above. This is **derive-for-display** assembly, never a regeneration of committed
state — boot's read-only law holds.

### The root `CLAUDE.md` — the hook-independent floor

The boot pack is **hook-dependent**: it renders only if the `SessionStart` hook runs, and hooks
[fail open](../infrastructure/hooks.md). Beneath it sits a floor that survives even a hook failure:
the **root `CLAUDE.md`**, which Claude Code loads automatically (walking up from the working directory)
independent of any hook ([constraints](../../../reference/constraints.md)). So a minimum grounding is present even when
the rich assembly is not — the two-layer story is `CLAUDE.md` (the hook-independent floor) beneath the boot
pack (the hook-dependent, substrate-degradable rich layer).

Because it is paid on **every** session (an [attention](../cognitive/attention.md) cost), the root
`CLAUDE.md` is deliberately **thin** — it carries only what must hold even if boot did not run:

- a one-line orientation (this repo carries an Engine; how to orient) and a pointer to the operator
  orientation [doc](../surfaces/docs.md) — which ships as a named v1 deliverable, so the pointer
  always resolves;
- the [memory](../cognitive/memory.md)-authority routing instruction (D-030): project recall lives
  in the Engine substrate — consult it; Claude Code's built-in auto-memory is **not** the project system of
  record and is never cited as fact. The committed `CLAUDE.md` is the one always-loaded surface the Engine
  controls, which is why this instruction lives here;
- the [engine/product wall](../infrastructure/repository-topology.md) reminder;
- the **[operator-presentation relay](../../../reference/glossary.md)** instruction: the AI is told that the boot pack
  and every other in-session engine notice reach **it**, not the operator — the operator sees only what the
  AI types ([constraints](../../../reference/constraints.md)) — so it must relay the must-push subset (governance
  alarms, a grounding-failure tell, the [close](close.md)-gate prompt, a cap-shed notice) in plain
  language and never
  treat injected content as already-seen ("*as the card above shows*"); routine detail is offered via the
  [status verb](../../../reference/glossary.md). This installs the **asymmetry** the AI cannot otherwise infer — the
  injected pack reads as if written *to* the operator yet is delivered only to the AI — and it foregrounds
  the protected-branch merge as the real governance guarantee. It is **posture** ([§6/§7](../../../principles.md)),
  named as such, never "I might forget";
- a standing **present-marker** instruction. Because the pack reaches only the model, the operator's "did
  the engine ground?" check rides the relay: a healthy session opens with the AI rendering a **named
  orientation block first** — a titled token (e.g. `Project status`; its exact title and form a build-spec
  leaf) carrying either a pushed governance alarm or a one-line all-clear — **before** it addresses the
  prompt. The floor states this as an unconditional, observable check, in plain terms not jargon: "*When the
  engine is grounded, the first thing I show you each session is a short titled status block — like
  `Project status: all clear` or `⚠ Protected branch is off` — so you can see at a glance that I grounded.
  If my first reply jumps straight into your request with no status block at the top, I did not fully ground
  — so don't trust what I say about your project; tell me to re-ground, or quit and reopen Claude Desktop.*" The check is the
  **presence of one named block as the assistant's first output**, decidable by a first-time operator with
  no prior healthy boot to compare against, and it covers the double fault (committed
  [state](../cognitive/state.md) unreadable *and* the boot hook did not run): with no injected pack
  the AI has nothing to render, the block is absent, and the instruction fires. A skipped *governance* relay
  surfaces the same way — a missing block — the operator-side detection the posture-tier relay relies on,
  with the merge wall the unbypassable backstop.

**Path-scoped nested `CLAUDE.md` files are out of v1.** They load lazily and unreliably — only when the model
reads a file in that subtree — so they are an unsound enforcement substrate; area-specific invariants belong
in always-evaluated [policies](../surfaces/policies.md) and [checks](../surfaces/check.md),
not nested grounding files. The root `CLAUDE.md` is an infrastructure artifact (topology-governed, like the
control-plane files), not a catalogued surface.

### The per-prompt scent — metacognition as a push

The substrate's worst failure is being **pull-only**: a tool the model must remember to invoke is a
tool it skips, defaulting to grepping files. The scent inverts this. On every prompt a *fast lexical*
lookup (FTS5/BM25 over the local index — single-digit ms; no embeddings, no LLM, no graph walk) injects
**attributed pointers, not content** — "*memory has older notes on X (3 drawers); X relates to Y, Z —
query and verify before asserting*" — so the looking has already happened and the result sits in front
of the model. Properties:

- **Push the cheap pointers; pull the expensive content.** Deep retrieval stays model-initiated.
- **Attributed and unverified — the core trust seam.** A lexical match is words, not meaning; a strong
  match can be stale. The scent must read as a pointer the AI **verifies before asserting**, never as
  its own recall woven into prose.
- **Selective, minimal, de-duplicated — within a session's lifetime.** It is silent on no strong match;
  because Claude Code's `additionalContext` persists in history, each scent is kept minimal and a pointer
  already surfaced is not re-injected. **The dedup's honest bound:** its already-surfaced record is keyed
  on the platform's session identifier, so the dedup reaches exactly as far as that identifier's lifetime —
  which is **reportedly** shorter than a conversation's, since `session_id` is re-issued on resume
  ([constraints](../../../reference/constraints.md), held at a weak tier: evidenced, not established). If that report
  holds, a resumed conversation starts a fresh record and a pointer may surface again. The design does not
  turn on which way it resolves — a scent is minimal by construction, so a repeat is cheap either way. The
  bound is stated rather than left implicit because a dedup silently scoped narrower than its reader
  assumes is the same defect class this doc's amendment came to close.
- **Fail-open, rate-limited.** A crash or a hard timeout injects nothing (never stalls the turn); the
  failure-finding is de-duplicated so a persistent fault does not spam the [telemetry](../guardrails/telemetry.md) inbox.
- **Pivots for free.** A conversation that turns produces the scent for the new topic on that prompt.
- **Heritage.** The scent is an *active / forward-looking retrieval* push (cf. FLARE, which retrieves on low-confidence tokens within an anticipated future sentence; the scent instead triggers on a lexical match against the user prompt). Lineage only — it does not soften the attributed / verify-before-asserting rule above. (Maintainer vocabulary; see the glossary *Lineage* cluster.)
- **Honest bound** ([principle §6](../../../principles.md)): a strong ambient *nudge*, not a guarantee; the lever is making the substrate the lower-friction, citable path.

### Degradation is loud and consented — never a silent default

The grounding floor is a **fallback so the operator is never stranded**, not a default to quietly run
risky work on reduced capability. When a substrate is unavailable — the memory or knowledge MCP is down,
or the [telemetry](../guardrails/telemetry.md)/GitHub debt register cannot be read (an outage or
expired auth) — boot orients from committed [state](../cognitive/state.md) alone (the floor)
**and says so, loudly, in plain language**, naming what is degraded and that it is usually a Claude Desktop
restart away from full capability. A figure read from a degraded source is rendered so the operator cannot
mistake it for current — "*N open problems as of <when> — I couldn't refresh this, so it may be wrong;
re-ground before you rely on it*" — so the operator never mistakes a partial picture
for the whole ([attention](../cognitive/attention.md) ranks over whatever inputs remain and hands
boot the degraded-input set; [D-059](../../../adr/0059-lock-the-state-system-wave-2-head-the-committed-cursor-recon.md) law 2). Boot owns producing and surfacing
this loud notice; it **supplies** the degraded-capability readout that the
[build orchestration](build-orchestration.md)'s plan gate consumes before substantive work, but
the gate, its risk assessment, and the consent step are build-orchestration's to define — boot fixes the
disclosure, not the gate. This is the [hooks](../infrastructure/hooks.md) fail-open-**and-flag**
law and the operator-communication law applied to the floor: degrade rather than fail, but never silently
([principle §5](../../../principles.md), [first-run scenario](../../../architecture.md#first-run-provisioning)).

The same law binds the pack's **own size**. The platform caps a hook's injected context and, past the cap,
substitutes a preview for the payload ([constraints](../../../reference/constraints.md)) — which would drop the
grounding marker and tell the operator boot *did not run* when it did: a silent degradation that also lies
about its own cause. So the pack is **measured against the cap before it is injected**, and an over-budget
pack **sheds its lowest-priority content**, shedding the informational digests and the recognition slice
first and a pinned governance alarm never — the ranking order above extended downward, since the slice is
an input rather than a ranked candidate and so sits beneath everything that order ranks. **The two orders compose in one direction, and the seam is not shared:**
[attention](../cognitive/attention.md) owns the *trim*, which ranks and partitions **candidates**
to its budget; boot owns the *shed*, which measures the **assembled** pack against the platform's character
cap. Attention runs first and never sees the slice (an input is not a candidate); boot runs last, over
whatever attention produced, and is the only stage that counts characters. So the orders never contend for
the same decision — one bounds *how much is worth surfacing*, the other *what physically fits*. The slice
sheds at that lowest tier because recognition is **posture and fail-open**
([ontology](../grammar/ontology.md)'s consumption law): losing it degrades to the same state as a
hook that never fired, which this design already tolerates and names. **The shed notice joins the must-push
set** — the pack reaches only the model, and the AI's relay is the operator's sole in-session channel, so a
pack that trimmed the operator's orientation and told only the model would be silent exactly where the law
demands loud. It carries what the operator can act on: that governance alarms were spared, so a shed is a
loss of *detail*, never of the signal a decision turns on. **Tier, named honestly
([§7](../../../principles.md)):** this whole chain is **posture** — the hook must fire, the guard must
measure, and the AI must relay; each link is fail-open. What is fixed is the design's commitment that the
pack never crosses the cap silently, not a mechanical guarantee that the operator is told — the guarantee
remains the protected-branch merge. The concrete budget arithmetic and the notice's wording are build-spec
leaves.

### Seams are deferrals

Boot integrates locked substrates and hands off to its `designed` neighbours without fixing their
internals: it names the current [stance](modes.md) in plain language, but the stance vocabulary
and the write-gate are [modes](modes.md)'; the `Stop` turn-close (ambient capture + the
finding-disposition gate) is [close](close.md)'s; the degraded-capability readout feeds the plan
gate, but the gate and its risk assessment are [build orchestration](build-orchestration.md)'s;
the debt register's shape and triage are [telemetry](../guardrails/telemetry.md)'s — boot only
reads and surfaces it. Each neighbour's later lock refines its own side without forcing a boot change.

### Build-spec leaves

The concrete boot-pack format, the exact surfaced-item ordering and rendering (within the alarms-pinned
priority law above), the root-`CLAUDE.md` copy, and — for the anti-habituation collapse — the terse-reminder
wording, the standing-alarm presentation ledger's on-disk form, and the concurrent-session write discipline
are build-spec leaves authored in the build session (laws-not-leaves, [D-052](../../../adr/0052-foundational-law-layer-closed-the-implementation-lock-order.md)).
What is fixed here is the law: which moments fire and that orientation is read-only of canonical state (its
one local write the gitignored presentation ledger); that grounding is unconditional with a hook-independent
floor beneath it; that degradation is loud and consented, never silent; that governance-critical alarms are
pinned and legible; and that a standing alarm collapses to a terse, consequence-keeping reminder when
unchanged and relays in full when new or worsened, fail-toward-full.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Always grounds at the floor** — the hook-independent root `CLAUDE.md` grounds every session unconditionally; the `SessionStart` boot pack rides on top whenever the hook runs (it is fail-open), degradable-up. The floor is cheap (committed state plus the thin `CLAUDE.md`); substrate depth is attention-budgeted on top. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Read-only of canonical state** — orientation never regenerates derived or committed state (regeneration is the commit-boundary's job); the operations that ride the `SessionStart` moment belong to the substrates that own them, not to orientation — memory's consolidation sweep, modes' stance clear, knowledge's regenerable slice cache. Orientation's **one** local write is the gitignored, non-canonical standing-alarm presentation ledger (anti-habituation, above) — a record of what was already shown, never a regeneration of state. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Anti-habituation by collapse, not suppression** — a standing governance alarm whose structured condition is unchanged since last shown in full collapses to a terse reminder (consequence + fix offer retained); a new, changed, or worsened condition relays in full; the ledger is fail-toward-full on any loss or ambiguity. The present-marker block and the all-clear render never collapse. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **"Where we are" is assembled, not stored-and-advanced** — boot derives the standing-situation (`phase` from the latest merged tracked build Issue, `milestone` from the open Milestone set under [state](../cognitive/state.md)'s selection bound — one, several, or `none set`) live from native sources, read-only, falling back to [state](../cognitive/state.md)'s offline cache (staleness-labelled) when GitHub is down; no session advances a stored marker, so the online card cannot silently rot. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Degrade loud and consented** — substrate outages produce a plain-language degraded notice at boot and a consent point at the plan gate, never a silent run on the floor. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **A hook-independent floor beneath the pack** — the thin root `CLAUDE.md` is platform-loaded regardless of hooks, carrying the irreducible grounding (orientation pointer, memory-authority routing, the wall, the [operator-presentation relay](../../../reference/glossary.md) + the present-marker) so a hook failure never leaves a session ungrounded. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Alarms pinned and legible** — governance-critical alarms surface first and visually distinct from informational notices, so a degraded boot is never a wall of warnings that buries the one that matters. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
| **Operator delivery is the relay** — the pack reaches the model, not the operator ([constraints](../../../reference/constraints.md)); the operator meets it through the AI relaying the pushed safety-critical subset and rendering the present-marker block first, with routine detail pulled via the [status verb](../../../reference/glossary.md) — the [operator-presentation relay](../../../reference/glossary.md), honest posture with the merge wall the governance backstop. | Not recorded in the design workspace — how this is verified is defined when this capability is settled. | operator |
