---
status: draft
---

# Build orchestration

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the cost-estimate mandate reversed by [decision 0321](../../../adr/0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md) and the re-audit passage aligned to the orchestrator's proportional judgment (2026-08-02) by [decision 0330](../../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md); ratified as intended design on 2026-07-11 by [decision 0293](../../../adr/0293-resolve-re-lock-build-orchestration-roster-divergence-hunter.md). Still **in progress** — reconciled is not settled, and the criteria below describe the build as observed, not ratified guarantees. Until the [product spec index](../../../spec/index.md) retires the corpus drift caveat, links out of this document may reach documents still describing intended design.*

## Summary

How [Build](modes.md) work happens: an **orchestrating session** opens a draft pull
request, plans the work as an ordered commit sequence recorded in the build Issue, has the plan and
then the result reviewed by cold-context [agent](../surfaces/agents.md) lenses at a depth
the operator approves, integrates the work as the single writer of final commits, and submits the PR
for human review. The **draft PR is the claim**; the **submitted PR is the close**; the **build
Issue carries the forward plan**. There is no separate claim artifact, no slot number, and no close
ritual — which is what dissolves the prototype's close-friction spiral (no reserved-subject commits
or close-shape allowlists to police).

## Behavior

### Two surfaces, two jobs — the change and the plan

The accountable state is native git/GitHub records, divided cleanly:

- **The pull request is the change surface.** It holds what *has been built*: the claim (draft), the
  integrated commits, the human gate (submitted → merged), and the narrative (the
  [control-plane](../infrastructure/control-plane.md) PR contract).
- **The build Issue is the forward-plan surface.** It holds what is *not yet built*: the ordered
  commit sequence as a machine-readable checklist authored at Plan, so progress is "N of M done"
  (closed/total) and the next chunk is the next unchecked item.

This operationalizes the locked [state](../cognitive/state.md) division without expanding
it: **the Milestone is the plan; the build Issue is that plan's machine-readable decomposition** —
not a new "deferral/backlog" Issue semantics, and never a committed work-inventory (state forbids
that). **build-orchestration produces the Milestones** (native GitHub Milestones, via `gh api`): when a
build realizes product work it **consumes [product-design](../../modules/product-design.md)'s
committed *build-plan*** — the doc that groups the `locked` spec's capabilities into ordered phases
([D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) — as the **grouping input** that names and orders those Milestones, so a
large build reads as legible phases with native progress rather than an issue dump; absent a build-plan it
plans the Milestone itself. Those emitted Milestones are what [state](../cognitive/state.md) reads
for the **milestone half** of its standing-situation projection (the phase half derives from the merge
record — "what merged last" — and state owns none of it). So the PR is **not** the only durable state:
the forward plan lives in the build Issue, which is what lets an unattended session resume a build whose
authoring session is gone. The **build Issue is the engine-labeled build Issue the Plan step opens** —
engine-labeled, so the [engine/product wall](../infrastructure/repository-topology.md) holds; when
the build realizes a [product-design](../../modules/product-design.md) **work Issue** (ordinary
product backlog, un-labeled — [control-plane](../infrastructure/control-plane.md)/[D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md))
it **references** that work Issue and the committed spec it points at, rather than being it. This resume capability is **bounded by GitHub availability**: the checklist is GitHub-derived,
so an offline routine session has no plan to read and simply does not proceed (fail-safe) — the same
honest-degradation bound [state](../cognitive/state.md) and [boot](boot.md)
already carry. Writing the checklist is **proportionate**: required when the build will be routine-
distributed, an offered progress view for an interactive multi-commit build (the orchestrator
otherwise holds the sequence in-session), and skipped on the fast path below.

### The gate skeleton — fixed shape, derived lenses, honest tier

The **gate shape is fixed** and ships with every engine; the **lenses that run at each gate are
derived** from the installed [agent](../surfaces/agents.md) suites (mirroring how a
check-suite's roster is derived). An empty lens-set is a valid **no-op pass** the risk assessment has
already disclosed.

1. **Plan** — the orchestrator opens a **draft PR** (the claim), plans the **commit sequence** (and
   records it in the build Issue when the build will be routine-distributed), and produces the
   **risk assessment** with a **suggested depth** (below). The operator iterates the plan to solid
   and **approves the plan and the depth**. *Always runs*, even with zero review modules.
2. **Plan-review** — the installed plan-review lenses run cold-context **at the approved depth,
   before any implementation**; findings are dispositioned before advancing. The v1 roster
   ([design-review](../../modules/design-review.md)) is `product-intent` · `architecture` ·
   `feasibility` · `risk-governance`. Empty ⇒ no-op pass.
3. **Implement** — one of three strategies (below), chosen at Plan by size/risk **and
   coupling/cohesion-need**.
4. **Integrate** — the orchestrator is the **single writer of final commits**: it **reviews,
   revises, and authors** the cohesive set into the PR branch (below).
5. **Pre-submission review** — gated behind a **green mechanical-validation baseline** (below); the
   installed pre-submission lenses then run cold-context and findings are dispositioned. The v1
   roster ([qa-review](../../modules/qa-review.md)) is `spec-conformance` · `usability` ·
   `technical-integrity` · `security-governance` · `divergence-hunter`.
   Empty ⇒ no-op pass.
6. **Submit** — the [validation](../guardrails/validation.md) suite is confirmed green, the
   [control-plane](../infrastructure/control-plane.md) PR contract is filled (including the
   **Review** record below), and the PR is submitted for human review.

**The skeleton is posture, named at its honest tier.** The gate *shape* is the orchestrating
session's workflow; **nothing mechanically forces a session to run the lenses, run them at the
approved depth, or halt on a finding** before the merge — exactly as the locked
[modes](modes.md) write-gate and [close](close.md) disposition gate are honest
that local enforcement is a [§6](../../../principles.md) nudge and the only unbypassable wall is the
protected-branch merge ([control-plane](../infrastructure/control-plane.md)). What *is*
mechanical is one narrow hook: the PR contract's **Review** section (below) is presence-gated by the
locked control-plane completeness check, so a build cannot submit without stating what review ran —
its *truthfulness* stays posture, like every other contract section. As built, that check carries two
exemptions: an author exemption for `dependabot[bot]` and `github-actions[bot]`, and a **label
exemption** — a pull request labelled `engine-erasure` skips the whole eight-section gate. Both are
**sanctioned**: the erasure-cluster question this reconciliation had deferred was ruled in the wave-5
round — [decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md)
sanctions the label-keyed erasure class and the widened author set, with the
[control-plane](../infrastructure/control-plane.md) document now carrying the boundary's full
disclosure. The orchestration workflow
itself is a **required core package**; the lenses are **optional modules**
([D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)). Everything bracketed — which lenses, whether to parallelize — is
depth-scaled; the shape is not.

### The plan gate — consent before the spend, synthesis after

The plan gate is the system's central trust moment, and it runs in two beats the design keeps
distinct:

- **Before the spend — the risk-assessment consent surface.** The orchestrator proposes coverage from
  three inputs — installed modules (what is *available*), [memory](../cognitive/memory.md)
  (the operator's depth preference), and [attention](../cognitive/attention.md) (the work's
  structural adjacency and debt-proximity) — and presents the **risk-assessment template** (a
  [templates](../guardrails/templates.md) instance). It states, uniformly: *what this
  touches → the coverage that implies → what is installed/enabled → what is missing → the current
  degraded-capability state ([boot](boot.md) §degradation) → the **suggested depth** →
  consent (install / proceed / trim)* — and **never a time or cost figure**, which the engine cannot
  know; a made-up number is the false confidence the trust model refuses
  ([decision 0321](../../../adr/0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md)
  adopted the build's refusal, reversing the earlier estimate mandate). The operator approves the
  spend **before** it happens by judging what will run. It **leads with a short, plain-language
  headline that varies with the actual change** ("*this touches your sign-in flow and the database —
  I'll run security and design checks*"); the headline is what gets read, the detail is what gets
  cited. The operator iterates the plan to solid, then approves. This surface is also the operator's
  affirmative **coverage view** — *what will be reviewed and what will not* — the roll-up the
  [agents](../surfaces/agents.md) surface defers here.

  **Depth is offered in the operator's language, never the engine's.** The operator never chooses lens
  slugs; the depth choice is a small **ordered set of plain-language levels with named consequences**
  (e.g. a quick check vs. a standard vs. a thorough review — "*lighter and faster, but weaker
  confidence later*" vs. "*slower, but I'll catch more before it ships*"), defaulting to the proposed
  level, the same consequence-named depth grammar
  [product-design](../../modules/product-design.md) uses at intake. The internal lens roster
  maps to these levels; the operator reasons about *how careful*, not *which lens*.

- **After the audit — one synthesized call, with a hard floor.** The plan-review lenses then run at the
  approved depth. The operator does **not** referee multiple voices: the orchestrator **synthesizes**
  the findings into a single recommended call plus the trade ("here is the disagreement, the
  recommended call, what you give up either way"), dispositioning each per the locked
  [finding-disposition](../surfaces/policies.md) policy. Findings re-engage the operator for
  **adjudication when they are material — and *always* when a `blocking`-severity finding was not
  resolved in line**: the orchestrator may not self-judge a blocking finding into a silent "logged and
  proceed," mirroring how the locked escalation [policy](../surfaces/policies.md) always
  fires on an irreversibility/scope-breach trigger. Every finding's disposition is **surfaced, never
  absorbed silently** — the post-audit summary and the Review record carry the counts and any Issue
  opened, so the operator sees *what was found and what the engine did with it*, not only how much
  review ran. This mirrors how the workspace gates its own irreversible decisions: propose, commission
  a cold audit, resolve.

A change that **weakens the engine's own enforcement** ([principles §15](../../../principles.md)) is a
named headline trigger: when the plan touches a guardrail in a weakening way (disabling/removing a
check, loosening a deny block, editing the ruleset-affecting files), the headline says so in plain
language — *which* protection weakens and what the AI could then do unwatched — so the operator's plan
approval, like the later merge, is informed consent. Strengthening a guardrail is not flagged.

**Depth is proportionate and operator-gated**: a typo proposes the orchestrator alone (the
trivial-write fast path below); a schema or guardrail change proposes the full suite. The
"medium-change default" is not a standing list — it is the risk assessment's proposed depth over the
derived lens set.

### The v1 lens roster and the referent

The two review gates carry a v1 roster of **nine lenses across the two review roles** — the
[design-review](../../modules/design-review.md) quartet at plan-review and the
[qa-review](../../modules/qa-review.md) quintet at pre-submission
([D-066](../../../adr/0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)/[D-291](../../../adr/0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md)). The roster is **grounded in the
Engine's own cold-session design audit** (adversarial / technical-feasibility / architect / operator):
build-time product review is the product-facing analogue of that mechanism. That audit is a floor, not a
ceiling, so the QA suite **carries the adversarial lane as its own standing lens** — `divergence-hunter`,
run beside `spec-conformance` ([qa-review](../../modules/qa-review.md)/[D-291](../../../adr/0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md)).
Each gate **consumes its whole roster**, so no
installed lens dangles as a [coherence](../guardrails/validation.md) finding
([agents](../surfaces/agents.md)). The QA lenses are the **judgment** layer above the
locked validation suite and CI (the **mechanical** layer) — they complement, never duplicate
([principles §7](../../../principles.md)).

Two lenses consume a **referent**: when a build realizes a
[product-design](../../modules/product-design.md) work Issue that points at a **`locked` spec**
in the committed `docs/spec/` corpus, the orchestrator resolves **work Issue → spec doc → acceptance
criteria** at Plan — a **path read** it owns
([D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)/[control-plane](../infrastructure/control-plane.md)) — and the
`product-intent` (plan-review) and `spec-conformance` (pre-submission) lenses check against it, the referent
riding the derived lens `output-contract`, **not** any new field on the control-plane PR contract. A build
that resolves **no committed `locked` spec** — none exists, or the pointer reaches only a `draft` — makes
those two a **disclosed no-op** ("I could not check this against a spec — none is locked"), never a silent
green; Build never depends on a spec existing, and the resolution holds whether or not the optional
product-design module is installed. The spec is **un-skippable** — but not by a mechanical block on the
agentic `spec-conformance` verdict ([validation](../guardrails/validation.md): "a persona judges,
a check gates — never duplicate"). The [conformance-enforcement floor](../../../reference/glossary.md) carries it — the same rigor that built the Engine
(build-conformance), re-homed to point at the product's own `locked`
spec, activating **only against a `locked` `docs/spec/`** (with none locked, the disclosed no-op above; it
never blocks the MVP scope the operator leaves open, [§20](../../../principles.md)) — and **each leg bites
only on criteria whose row is `locked`** (lock is per-doc, read from the base commit's `status:`), so a PR
touching an adjacent `draft`/`stub` capability draws the disclosed no-op for those. Three complementary
mechanisms: a **[spec-obligation matrix](../../../reference/glossary.md)** — the coverage denominator, one row per
`locked` acceptance-criterion, a derived-committed artifact keyed by its **criterion-cell digest at its
`shape`-validated table position** ([§3](../../../principles.md)/[§19](../../../principles.md), the
knowledge-graph way — a stale row re-opens when its criterion changes), so coverage traces at
**criterion granularity** (every `locked` criterion to committed work, not merely every capability
scheduled — the derived source-pinned rows are the criterion-ID scheme, no hand-authored structure) with a
continuous reverse sweep of the not-yet-built remainder; a product-design-provided,
[migration-discipline](../../modules/migration-discipline.md)-shaped CI check, self-removing on
engine removal (as built, the derived matrix and its own CI check are criterion-granular, while the
per-merge coverage *floor* still traces at capability granularity — the build-owe recorded in
[D-287](../../../adr/0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md), an
engine-template debt rather than a spec question); the **paired judgment lenses** — **`spec-conformance`**, the systematic reviewer whose
built-vs-spec verdict (each obligation met, diverged, or untested) is surfaced with every gap
dispositioned at the operator's merge, and its adversarial counterpart **`divergence-hunter`**
(default-to-divergent — build-conformance §8), a second decorrelated
cold context run against the same `locked` rows that hunts a semantic misbuild passing its own tests and a
diff-introduced over-build the spec never asked for — both **re-derived from the `docs/spec/` span itself,
never from the matrix rows** (the matrix is the denominator, not the lens's checklist —
[R16](../../../reference/risks.md)); and the
**deployed-environment demonstration harness** (the standing correlate the operator-runnable how-verified
rows retire into, below) — so a build that skipped the spec cannot quietly reach a merge that does not match
it. The operator-facing rendering keeps the two tiers distinct —
the coverage check reads as a mechanical, trustworthy pass/fail; the `spec-conformance` verdict reads as the
engine's own judgment with its gaps named — **never collapsed into one "all green"**
([§17](../../../principles.md): structure must not manufacture confidence the verification does not deliver).

### The Review record — the PR contract's gated judgment-layer section

The PR the orchestrator submits fills the locked control-plane contract's **Review** section with
**the depth that ran, which lenses ran, that each gate completed, the findings' dispositions**, and —
when post-audit fixes were made — the measured divergence, **whether a re-audit ran, and what it
found** (below). The honest
tier is exactly control-plane's own: the **PR-body completeness check hard-gates that the Review
section is present and non-empty**, while its **truthfulness stays posture** — the same tier the Risk
and Validation sections carry. Review is the **judgment-layer** record, distinct from **Validation**
(the mechanical-check results) and from **Claude involvement** (what the AI did). This is what converts
the operator's merge — the real wall — into an informed consent about how much review the change
received, and lets a reviewer refuse a PR whose Review record shows a shallow or skipped audit. The
engine never dresses a filled Review section as proof the review happened.

Because Review is **read by a non-engineer at the merge**, two honesty rules bind its operator-facing
rendering (the [leak guard](../../../principles.md) applies — plain language, never lens slugs or
"depth=2"): (a) the block itself carries a one-line plain statement that it is **the engine's own
account of the review, and the operator's approval is the real gate** — so the block reduces over-trust
rather than manufacturing it, with the honest tier riding *in the artifact* the operator reads, not
only in a spoken merge line a walk-away operator may miss; and (b) the **post-audit-fix delta** — the
highest-stakes line for a go/no-go, since the approved thing and the merged thing now differ — is
rendered in **consequence-named plain language** ("*I fixed two things after the review and re-ran the
tests; I judged the repair small enough not to need a fresh review — that call is disclosed here for
your read*", or "*…and gave the repair its own scoped re-check, which found nothing*"), the same
consequence-named grammar the depth choice uses. Review's **review-judgment** part is the **one** stretch of the contract whose
subject the operator cannot independently corroborate — unlike Validation, whose green checks the
operator sees, or Risk, which describes the visible diff, it is a retrospective self-report of an
invisible process — so that part's posture-truthfulness tier is **load-bearing in a way its siblings'
is not**, and the design says so rather than letting "informed consent about how much review ran"
stand unqualified. Its **operator-runnable acceptance steps** (below) are the converse — the one part
the operator *can* corroborate by running, the [§17](../../../principles.md) behavioral correlate
carried beside the judgment it cannot replace. A trivial fast-path
build fills Review with a truthful minimal line ("*I made this small reversible change myself; no extra
review*"), which is itself useful consent signal; the completeness check's non-empty requirement
accepts that and never forces manufactured review prose ([goals §6](../../../reference/goals-and-quality.md)).

Review also surfaces the change's **operator-runnable acceptance steps** — the steps the operator can
run themselves to watch the change work — rendered **verbatim** from the realized `locked` spec's
operator-runnable how-verified rows, resolved by the same work Issue → spec → acceptance-criteria path
read the referent uses (above). These same rows are the **deployed-environment demonstration harness** — the
standing, re-runnable behavioral correlate the [conformance-enforcement floor](../../../reference/glossary.md) carries
against the `locked` spec, the [§17](../../../principles.md) evidence that routes around AI (distinct from an
AI-run in-tool `demo`, below, which is *not* operator-runnable). The orchestrator **renders, never authors**: it copies the
operator-typed rows and never composes, grades, paraphrases, or curates a recipe — judging recipe quality would be a
semantic read of product content the [wall](../infrastructure/repository-topology.md) keeps
off. When nothing is operator-runnable it fills a **reason-named no-op** from a bounded set, never a
silent absence: **(i)** every criterion is engine/CI-internal — a behavior-preserving refactor,
internal plumbing, or a doc-only change — naming the class and the non-operator correlate that carries
it; **(ii)** operator-runnable criteria exist but cannot run in the operator's environment, pointing to
the engine-side correlate; **(iii)** no `locked` spec resolves (the referent's disclosed no-op, above);
**(iv)** a trivial fast-path build (the minimal line above). The reason class is the **engine's own
account** of why nothing is operator-runnable — a posture-tier self-report at the same honest tier as
the review judgment, not an operator-verifiable fact — surfaced to the operator as plain cause, never
the class label. An in-tool `demo`/`demo-*` subcommand is
**not** an operator-runnable step — it is AI-run and the operator cannot run it — so a criterion whose
only correlate is a demo falls to reason (i), on the engine's account.

Five rules bind the steps' operator-facing rendering, at Review's own leak guard and posture tier: the
two groups render in **plain language** — "things you can confirm yourself" and "things I checked for
you" — never the typing tokens; **an unrun step is a promise, not proof**, never stacked beside a green
check as a second confirmation, the caveat riding *in the artifact* the operator reads; **the steps are
an offer for when the change matters, not a duty on every merge** ([goals §6](../../../reference/goals-and-quality.md)
low-ceremony) — routine reversible work merges on the checks and the engine's account alone; **a step
the operator will actually run beats one they won't** — a screen they click is preferred over a
paste-this-command, and a CLI-only check a non-engineer realistically will not run is rendered on the
engine's account, not under "things you can confirm yourself" (sorting a row by its runnable-surface
*kind* — a clickable screen versus a terminal command — is a mechanical read of the row's form, not a
grade of the recipe, so it stays the right side of the verbatim/no-grading wall); and **a step must be
able to fail** — it exercises the real
changed surface, never a staged recipe that can only succeed (the behavioral-attestation shape, posture
not a gate). The no-op likewise states its cause in plain language and **never leans on a passed
mechanical check as if it were the operator seeing the change work**. These are **build-spec leaves**
under the plain-language law.

Review also carries the result of a **close-linkage consistency pre-flight** the orchestrator runs at
submit, before it marks the draft pull request ready (the PR itself has been open since Plan). GitHub auto-closes an issue from any `close`/`fixes`/`resolves #N`
keyword — including one buried in prose — in the PR body **or an integrated commit message**, so an
accidental keyword silently sets the PR to close an issue the change only partly addresses, and the
engine then reports a wrong backlog. The pre-flight reads only machine-decidable facts: the set the PR
**will** close — GitHub's computed `closingIssuesReferences` (the body-keyword linkage) **plus** the
closing keywords in the commit messages the orchestrator is integrating (which that field does not
reflect, and which only the submit-time orchestrator holds) — against the closing intent the PR
**declares** in its own structured Scope/Out-of-scope. Two contradictions are decidable without reading
intent: an issue the PR will close while its scope declares it only **"Part of #N"**, and a comma-trap
under-link (`Closes #1, #2` links only `#1`, leaving `#2` silently open). **Detecting** the
contradiction is mechanical; **acting** on it never silently changes what an operator-visible PR will
close. The default — and the only path where the close might have been intended — is to **surface** the
contradiction as a plain-language line in the Review record ("*this PR is set to close #171, but its
scope says this PR is only part of the work for #171 — the closing line needs a small edit before you
merge*"), at Review's leak-guard and posture tier (never the field name, never a slug). Only when the
stray keyword is **unambiguously accidental** (the structured scope declares "Part of #N" and carries no
deliberate close line) may the orchestrator **neutralize just that keyword** before opening — a minimal
defang of the engine's own control-plane artifact (the [§6](../../../principles.md) nudge realized at
the source), **never** a rewrite of the narrative the operator reads and **never** a read or edit of
product scope (the [wall](../infrastructure/repository-topology.md) holds) — and it **records
that it did so** in the Review record ("*I removed an accidental closing keyword that would have closed
#171; this change is only part of #171*"). So the operator always meets a legible account — the
unresolved contradiction or the disclosed correction, never a silent change to what closes; a
keyword neutralized that was in fact wanted is a **disclosed, operator-recoverable** miss, the named
residual of the narrow auto-edit. The pre-flight is **not a gate**: the comparison is mechanical, but its
delivery rides this AI-authored record, so it inherits Review's posture-truthfulness tier and its "the
engine's own account, your approval is the real gate" framing — the [§17](../../../principles.md)
residual named, not hidden, and bounded on **both** paths by the operator's own independent view (GitHub
shows the unresolved "will close #N" at the merge; the disclosure states any pre-open defang). Its
**adjudication is same-repo**: a will-close entry against an issue the PR's own Scope does not describe —
a cross-repo `owner/repo#N` close, or the upstream issues an
[external-contribution](external-contribution.md) cross-fork PR would close — is **outside the
pre-flight's reach**, surfaced-and-named, never silently passed and never defanged; likewise a close
reaching the issue by a path the orchestrator cannot see at submit. A null result (no contradiction)
produces no line and is **not** part of the Review completeness check's non-empty requirement.

### Implement — three strategies

Chosen at Plan by size/risk **and how tightly the work couples**; all converge on the orchestrator
authoring the final commits (step 4):

- **Orchestrator-inline** — tiny or tightly-coupled work; the orchestrator makes the change itself.
- **Parallel workers** — the reason to delegate is **cohesion under context pressure**, not raw
  speed. An orchestrator cannot hold the whole result *while* generating six-to-ten commits' worth of
  original work — the generation fans out and the session loses grounding and drifts, so commit 1 can
  foreclose what commit 8 needs. So each [worker](../surfaces/agents.md) (the `mechanical`
  demand tier — its concrete model+effort realization is persona-owned platform-passthrough,
  [D-057](../../../adr/0057-lock-the-agents-surface-wave-1-four-settled-design-forks.md)/[D-100](../../../adr/0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md)) takes one commit's scope in its
  **own isolated worktree on a short-lived branch** and returns *mechanical work product*, not commits. The token-heavy generation stays out of the orchestrator's window; the
  orchestrator then reviews, revises, and authors the one cohesive set with full visibility (step 4),
  so the PR that reaches the cold audits is free of assembly noise and the audits catch substance.
  Best for **loosely-coupled, decomposable** work. The win is **net**, not free: workers shed the
  *generation* load, but two workers each handed "one commit's scope" can still produce *semantically*
  overlapping output (the same function, incompatible assumptions), and reconciling that is real work
  the orchestrator does at integrate — bounded by its context, and the reason the orchestrator, not a
  worker, is the single writer.
- **Time-distributed routine** — unattended sessions accumulate commits over a cadence (see Routine).

**Worker partial-failure has no phantom-slot class.** The **plan (the commit sequence) plus git state
are the record**: a worker that dies leaves an absent or un-integrated work product, which the
orchestrator detects at integrate against the planned sequence and **re-dispatches or completes**.
Workers are git-isolated (separate worktrees, single writer), so there is no shared-state corruption;
logical overlap is reconciled in the orchestrator's review-and-author job, not by an automated branch
merge.

### Where build runs — the operator checkout is a protected surface

Build and Routine work runs in an **isolated git worktree on a short-lived branch** — and so does the
**orchestrating session itself**, not only its workers. On the v1 client this is the *native substrate*,
not engine machinery: Claude Desktop **auto-isolates every session in its own worktree**
([constraints](../../../reference/constraints.md)), so the orchestrator authors its cohesive commit set (step 4)
onto the PR branch *in that worktree* and reaches the protected branch only as the reviewed PR. The
**top-level operator checkout is a protected operator surface, never a build workspace**: a session never
detaches, resets, branch-switches, or commits *in* it — [modules/core](../../modules/core.md)'s
deployed-floor `CLAUDE.md` carries this as the **never-strand-main** floor.

This is honest, not airtight ([§6/§7](../../../principles.md)): native isolation is a strong platform
**default, not a guarantee**. It covers interactive Desktop sessions; the residual — a Local-Desktop
routine (below) without its per-task worktree toggle, a CLI or resumed session, or a worktree session
reaching back into the checkout by absolute path —
rests on the never-strand-main posture floor plus Routine's own scope-lock, with the protected-branch merge
the only unbypassable wall for *shipped* history. A checkout stranded despite all of this is **detected and
offered a fix** at [boot](boot.md) ([provisioning](../infrastructure/provisioning.md)
owns the detector and the un-stranding fix).

### Integrate — the orchestrator reviews, revises, and authors

The orchestrator is the **single writer of final commits**. It does not rubber-stamp worker output:
it **reviews** each work product for correctness and fit, **revises** what does not cohere, and
**authors** the final commit(s) holding the whole result in view. This review-and-author step is what
earns the cohesive, low-noise PR; it checks worker output for correctness and fit **regardless of the
worker's cost**. Whether the `mechanical` tier's realization should run a *lower-cost* model/effort is a
**config-time judgment that can go either way** with the current economics — a cheaper-but-flawier worker
can raise this step's revise burden — and is deliberately not a design lock ([D-100](../../../adr/0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md)).
It is distinct from the formal pre-submission gate: integration review asks *is this mechanically right
and does it fit the whole?*, continuously; the pre-submission lenses are cold-context judgment on the
assembled result.

**Regenerating the derived-committed artifacts is part of integrate.** As the single writer, the orchestrator
reconciles the PR branch's base against the default branch and then **regenerates every
[§19](../../../principles.md) derived-committed artifact** — the [knowledge](../cognitive/knowledge.md)
graph and the [ontology](../grammar/ontology.md) self-map — **from the reconciled tree as the final
authoring step**, so the PR is regenerated-and-current before review. A textual conflict on a member is
**spurious** (§19): the resolution is to **clear the conflict and regenerate unconditionally** — not a
side-pick (`--ours`/`--theirs`, which an add/delete-vs-modify case can defeat), never a hand-merge. The
load-bearing guarantee is **reconcile-before-merge**: GitHub's server-side merge cannot run a local merge
driver, so the eventual merge must already be textually clean (an optional `.gitattributes`
regenerate-to-resolve *custom* driver is local-only belt-and-suspenders, a build-leaf, never `merge=ours`). The
orchestrator records a quiet plain-language line in the **Review record** that auto-regeneration ran
("regenerated N internal index files; no work lost") — **pulled**, carrying no
[imperative relay marker](../../../reference/glossary.md) (the operator meets the disclosure, never the conflict). This
does not make a transient `CONFLICTING` state impossible — a sibling PR can merge mid-flight — only
operator-invisible to *resolve* ([D-024](../../../adr/0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md)); when no session is on the conflicted PR
(pre-M1, or an unattended routine merge), an AI session's named recovery path reconciles it, never the
operator. In [external-contribution](external-contribution.md) the regeneration runs in the engine
**fork-main** context — the product/upstream contribution branch carries no engine files and is never
regenerated onto.

### Validate before the expensive review; rerun validation freely, re-audit by judgment

Mechanical [validation](../guardrails/validation.md) is cheap and deterministic, so a
**green baseline is a precondition** to the pre-submission judgment review — cold-context lenses must
not be spent on code that does not pass tests, and their findings stay about substance rather than red
builds. Validation **reruns on every change**, including fixes that disposition audit findings. The
**cold audits run once at the agreed depth and do not blanket-rerun** on those fixes — re-running
expensive judgment on every fix-cycle would loop without bound. Instead the orchestrator **measures
the post-review divergence and makes a proportional re-audit judgment** (the magnitude is data behind
the call, never a threshold that fires a rerun): when warranted it re-invokes the pre-submission
passes that fit the repair, scoped to the post-review diff, before the record is finalized — the
re-audit is never itself a gate, though a `blocking` finding it surfaces gates the merge as any
finding does ([decision 0330](../../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md)). The **Review
record states the delta** — the reviewed→submitted commits, the measured divergence, and the
disposition — and the operator may always request a fuller re-review. CI re-validates the submitted
PR as the **required check**; the merge stays the wall.

### Proportionality — the fast path and its floor

Depth scales down to a genuine floor. A **trivial single change** takes the **fast path**:
orchestrator-inline, **no Issue checklist, zero lenses, and the plan gate collapses to a single
plain-language headline**. Stated honestly, the irreducible floor still includes the locked
Build entry ([modes](modes.md)): the operator **enters Build** (types the verb or accepts the plan), the
orchestrator opens a draft PR and shows the headline, validation runs, and the operator **merges** —
*one entry, one glance, one merge*. That is far lighter than the prototype's close ritual and earned
by reversibility ([goals §3](../../../reference/goals-and-quality.md): every change lands behind review and can
be undone). The *common* small-change shape is not one-typo-one-PR but **grouped** related work — a
"bug fix" PR carrying several small commits — an ordinary multi-commit build with a checklist and a
proportionate depth. "Fixed gates" describes the *shape* every build follows, never a fixed *depth*
every change pays; the consequential headlines (a guardrail-weakening change, a schema change) are
visibly weightier than the trivial confirm, so habituation does not erode the high-stakes consent.

### Close = PR submitted for human review

A build session is **done when the PR is submitted**. Re-engagement for questions or revisions is
allowed but not expected; **merge-and-walk leaves nothing dangling** — the durable state is the PR
(open → merged), the build Issue (the forward plan, closed as commits land), and
[memory](../cognitive/memory.md). The unbypassable gate is the operator's merge
([control-plane](../infrastructure/control-plane.md)).

In the [external-contribution](external-contribution.md) operating mode the operator does not own the
product repo and never merges it, so the **unbypassable gate is the upstream project's own merge** (its
maintainers' review/CI), not the operator's; close is still the submitted cross-fork PR, but the wall lives
downstream on the upstream.

The per-turn `Stop` [hook](../infrastructure/hooks.md) does only the two things
[close](close.md) owns — **ambient memory capture** and the **finding-disposition gate**.
The heavy multi-step close ritual is gone.

### Routine — time-distributed execution for decomposable bulk work

Routine is for **large, cleanly-decomposable bulk work** — populating a knowledge/graph store with
thousands of nodes, sweeping a mechanical transformation across a corpus — where each chunk is
**discrete and individually planable**. That shape is *why* routine can defer cohesion (plan up front
+ check at Finalize) without the drift that makes interactive orchestration necessary for tightly-
coupled feature work. **Decomposability is a Plan-time judgment, not an enforced property**: the
orchestrator assesses it at Plan and, when the work is too coupled to chunk safely, **says so and
recommends interactive Build instead** — the honest tier, since nothing mechanically stops an operator
pointing routine at coupled work. Routine carries real **operator setup cost** — it runs on **Local
Desktop routines** (explicitly *not* the cloud Routines product, whose fully-autonomous, fresh-clone,
`claude/`-branch model does not fit this design) that the operator configures and starts in Claude
Desktop, with the machine kept awake (a Desktop routine does not fire while the machine sleeps); an AI
session cannot stand one up alone. So it is a deliberate choice for that narrow shape, never a default.
Unlike an interactive session, a Local-Desktop scheduled run does **not** auto-isolate into a worktree by
default, so the `/engine-routine` setup guidance has the operator enable the per-task **worktree toggle** —
giving each run its own worktree rather than executing in the operator checkout itself; absent it, the
never-strand-main floor and the scope-lock (below) are the only guards.

It is **not a separate workflow** — it is the implement phase distributed across unattended sessions:

- An interactive **Plan** session opens the PR, plans the commit sequence, **records it as the build
  Issue's checklist** (the durable plan a cold session reads) **and records the routine's permitted
  write-scope with it** (the union of the planned chunks' declared path-scope — the scope-lock lives
  here, GitHub-native and cold-readable, not in any ephemeral signal), runs plan-review, and gets
  approval.
- Each **routine session** fires — the Local Desktop routine's Instructions invoke **`/engine-routine`**,
  the operator-authored, engine-prefixed [operator-typed](../surfaces/skills.md) entry command
  (invoked by its presence in the scheduled prompt, not by model self-election), which enters the routine
  procedure — then reads git state and the build Issue to find the next planned chunk
  and its scope, executes within that **scope-lock** (checked at boot and at every commit), **adds
  commit(s) to the open PR**, reports progress **derived from git and the checklist** ("*commit X
  landed — 6 of 14 planned done*"), and exits. It **never closes the PR**. It runs in a
  **non-interactive permission posture** (pre-approved tools, no prompts) so that it genuinely
  **cannot ask** ([constraints](../../../reference/constraints.md)) rather than stalling on a permission prompt;
  its findings therefore triage without a human per the locked escalation
  [policy](../surfaces/policies.md): an **out-of-scope observation** is filed as an Issue and
  the run **continues**; a **genuine blocker or a decision needing a human** files an Issue and
  **halts that task**, leaving a plain-language status that names the concrete next step ("*stopped at
  6 of 14 — I need a decision on X; I opened Issue #N. Answer there, then re-run the routine and I'll
  continue.*"). A run with no remaining eligible scope exits gracefully. Because the operator is away, a
  **misfire is made operator-visible**: a run that finds **no valid target where one was expected** — a
  missing or mis-aimed build Issue — leaves a durable Issue rather than a silent exit (dedup-guarded, so
  a repeating misfire surfaces once), and a routine
  **echoes the build Issue it has locked onto on its first fire** ("*starting the routine on #N — <title>*")
  so a mis-aim surfaces on the first cycle rather than after a wasted batch. As built the first-fire echo
  carries **no mechanical first-fire test and no dedup guard** — unlike the misfire path — so a run
  blocked before its first commit can echo again on the re-fire; "first fire" names the intent, not an
  enforced predicate — operator-ruled in this reconciliation as the build's accepted shape, a cosmetic
  asymmetry rather than a defect.
- An interactive **Finalize** session confirms the green baseline, runs pre-submission review,
  integrates and reviews the accumulated commits for cohesion, validates, and submits for review.

Routine's cohesion guarantee is **planned-up-front plus checked-at-Finalize**, honestly weaker than
interactive Build's continuous assembly and acceptable only because routine is reserved for
decomposable work. Single-flight for Local Desktop routines is the **Desktop scheduler's
skip-a-run-while-one-is-in-progress** behavior (the local counterpart to the control-plane
single-flight law for Actions-hosted scheduled work); orphan recovery is reading git state, not a
lease. Routine **never auto-merges the protected branch**.

### A maintainer-layer doc, with the honest tier surfaced to the operator

The vocabulary here — orchestrator, worker, commit sequence, the gate skeleton, the `judgment`/
`mechanical` demand tiers, execution profile, effort, lens names, the `spec-obligation matrix` /
`divergence-hunter` / `over-build` / `conformance-enforcement floor` names — is maintainer framing and
never reaches an operator-facing surface
([principles §12](../../../principles.md) leak guard). The operator sees plain language: a draft pull
request opened, a plain-language risk assessment with a consequence-named depth choice, the build's
**Milestones named as plain phases** (operator-facing, bound by the plain-language law like every operator
surface — never lens slugs or engine milestone vocabulary), progress as "N of M done," findings reported in
plain words, and a pull request submitted for their approval. Because no hook channel
reaches the operator ([constraints](../../../reference/constraints.md)), each of these operator-facing surfaces is
delivered by the AI relaying it in chat per the [operator-presentation relay](../../../reference/glossary.md) — the
risk-assessment consent surface **relayed before any build work** (consent-critical, pushed), the rest in
plain words; the relay is posture, the merge the wall. The
honest tier is **surfaced, not just recorded**: at the merge the operator is told in plain language
what the review claim is worth — that the engine reviewed at the chosen depth and that the durable
guarantee is their own approval at merge — the same honest framing locked [modes](modes.md)
and [close](close.md) require ("I won't build until you tell me," never "I cannot").

### Build-spec leaves

The laws above are fixed; these concrete forms are settled in the build-spec pass and do not reopen
the design:

- the **build-Issue checklist + scope-lock format** — the machine-readable ordered-checklist
  convention a routine session parses for "next chunk" / "N of M", and how the permitted write-scope is
  recorded alongside it and checked per commit; the build Issue is **engine-authored** — created at Plan via
  the [control-plane](../infrastructure/control-plane.md) issue-authoring helper, **not** the human
  web-form issue templates it bypasses — so its body realizes the control-plane **engine-authored-issue body
  contract** (the checklist + scope-lock are this build's "what happens next"), a build-spec leaf.
  build-orchestration fixes only that both live in the build Issue, authored at Plan, GitHub-native and
  cold-readable;
- the **non-interactive routine posture** — the concrete permission configuration (pre-approved tool
  set / no-prompt mode) that makes "cannot ask" true rather than a stall;
- the **depth-level grammar** — the small ordered set of plain-language depth names and their
  consequence wording, and the internal map from levels to the derived lens set;
- the **Review-section layout** — how the depth / lenses-run / completion / dispositions /
  post-audit-fix delta, and the **operator-runnable acceptance steps (or reason-named no-op)**, are laid
  out within the control-plane Review section, subject to the laws fixed above: operator-facing plain
  language (lenses rendered as plain checks, never slugs; the steps' two groups as "things you can
  confirm yourself" / "things I checked for you"), the in-block "my own account; your approval is the
  real gate" caveat, the consequence-named post-audit-fix delta, the steps' promise-not-proof caveat
  and offer-not-duty marker rendered **beside the step list itself** (not only in the block's preamble,
  since that is where the over-trust springs) and the plain-cause no-op rendering, and a
  fast-path-acceptable minimal line the non-empty check honors; and the **close-linkage pre-flight's**
  operator-facing lines — the scope-contradiction and the disclosed-defang heads-ups (both naming the
  closing line, the defang line disclosing that a keyword was removed), the **comma-trap** heads-up
  (stating the plain consequence "the second issue will stay open after merge" without teaching keyword
  syntax), and the **could-not-read** line when the linkage was unreadable at submit (which points the
  operator to GitHub's own "will close" list to confirm, never asserting an edit the engine could not
  verify was needed) — none rendering the field name or a slug; the **structured deliberate-close
  grammar** the pre-flight parses to tell an accidental keyword from an intended close; and the linkage
  read — the `gh` capability floor (`gh pr view --json closingIssuesReferences`, `gh ≥ 2.72.0`) with the
  `gh api graphql` fallback beneath it, the `issues: read` sub-scope a private-repo read needs so a
  missing scope degrades to the could-not-read line rather than a false "nothing will close," and the
  integrated-commit closing-keyword scan;
- the **risk-assessment template wording** — the varying headline and
  the weakening-change headline copy (never a time or cost figure,
  [decision 0321](../../../adr/0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md));
- worker-worktree mechanics note for the build-spec: a subagent worktree branches from the default
  branch by default, so the orchestrator reconciles that base when authoring onto the PR branch (in
  [external-contribution](external-contribution.md) that base is the *upstream's* default, which carries no engine files, so the
  product branch is engine-clean by origin);
- the **worker execution realization** — the concrete `model` + `effort` each persona declares to
  realize its `model-tier` demand tier, a config/authoring choice that churns with the model landscape
  and never touches this design ([D-100](../../../adr/0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md)). As built, **no worker or `mechanical`-tier
  persona ships**: the agent roster carries the review personas only, and a worker spawned for an
  implement strategy is ad hoc, inheriting the session's realization rather than carrying frontmatter of
  its own — the frontmatter mechanism (`model` + `effort`, the per-persona
  platform-passthrough keys; `effort` has no per-spawn override the way `model` does) applies today to
  the shipped review personas. (The estimate-recalibration obligation this leaf once carried fell with
  the estimate itself —
  [decision 0321](../../../adr/0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md).)

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Two surfaces, two jobs** — the PR is the change/accountability surface; the build Issue (a Milestone's decomposition) is the forward-plan surface that lets an unattended session resume cold, bounded by GitHub availability. **build-orchestration produces the Milestones**, consuming product-design's build-plan as the grouping input when one drives the build. The PR is not the only durable state. | No merge-gated check asserts the two-surface division; your observation of a build's draft PR and its build-Issue checklist carries it. Partial support: the built operation authors both surfaces at Plan, and the Milestone emitter derives Milestones from the build-plan idempotently via `gh api`. | operator |
| **Fixed shape, derived lenses, posture tier with one mechanical hook** — the gate skeleton is the orchestrator's workflow, honestly named as a nudge; the one mechanical hook is the PR contract's presence-gated (not truthfulness-gated) Review section; the only wall is the merge. Coverage is module-supplied and risk-scaled. | The one hook is merge-gated: the `pr-body-completeness` check (hard, CI) asserts the Review section's presence — subject to the as-built author and label exemptions disclosed above. The shape and posture halves are yours, with the `lens-consumption` check (CI) flagging a dangling installed lens as partial support. | operator |
| **Consent before the spend, synthesis after, with a floor** — the risk assessment is the pre-audit consent and coverage surface with a consequence-named depth choice (never a time or cost figure, [decision 0321](../../../adr/0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md)); lens findings are synthesized into one call afterward, re-engaging the operator on material findings and *always* on an unresolved blocking finding, with every disposition surfaced. | Your observation carries it — the risk-assessment relay is in-chat posture whose template instances are ephemeral, reachable by no validator; the fixed template copy itself bans the fabricated figure. | operator |
| **Cold-context review is the quality spine** — independent lenses, dispositioned between gates; more valuable, not less, when work is unattended. | Your observation carries it. Partial support: the finding-disposition Stop gate ([close](close.md)) holds raised findings to a disposition, the `disposition-issue-resolution` check (hard, CI) asserts cited follow-up issues are real, and the `lens-consumption` check flags an installed lens nothing consumed. | operator |
| **The orchestrator is the single writer** — workers generate mechanical work product in isolation; the orchestrator reviews, revises, and authors the cohesive set. Delegation buys cohesion under context pressure, not speed; reconciling semantic overlap is real, bounded work; partial failure is a missing planned commit, not a phantom slot. | No check asserts single-writer authorship; your read of a build's commit history carries it. | operator |
| **Validate before the expensive review; rerun validation freely, re-audit by judgment** — a green baseline gates pre-submission; fixes re-validate, and the cold review re-runs only on the orchestrator's proportional re-audit judgment, scoped to the post-review diff and disclosed in the Review record ([decision 0330](../../../adr/0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md)). | Your read of the Review record carries the ordering claim. Partial support: the CI validation suite is the mechanical green baseline every merge re-runs; the re-audit judgment is posture the Review record discloses. | operator |
| **Proportionate to a real floor** — the fast path is one entry, one glance, one merge; "fixed gates" is a shape, never a fixed depth. | Your observation of a trivial change's fast path carries it — no check measures proportionality. | operator |
| **Routine is the same workflow, constrained** — for decomposable bulk work only (a Plan-time judgment), Local-Desktop-stood-up, non-interactive, scheduler-serialized single-flight, never auto-merging; its weaker cohesion guarantee is stated, not hidden. | Your observation carries it. Partial support: `set-routine` mechanically refuses the write stance without proven worktree isolation ([modes](modes.md)); single-flight is the Desktop scheduler's behavior, not engine-asserted. | operator |
| **The operator checkout is a protected surface, not a build workspace** — build/Routine work runs in the platform's per-session worktree (native isolation), never in the operator's top-level checkout; the never-strand-main posture floor and #80's stranded-checkout detect-and-offer-to-fix cover the residual; native isolation is a default not a wall, and the merge stays the only unbypassable wall for shipped history. | Your observation carries it. Partial support: `set-routine`'s isolation proof for unattended runs; the never-strand posture floor in the deployed grounding copy; the stranded-checkout detect-and-offer owned by [boot](boot.md)/provisioning. No check fully asserts the criterion. | operator |
