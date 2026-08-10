---
status: locked
---

# Control plane

*Reconciled with engine-template@`cdbbc33` as built (2026-08-01) — AI-compared and operator-ruled under [decision 0320](../../../adr/0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md), with the product-design reference corrected to `required` distribution by [decision 0335](../../../adr/0335-separate-module-distribution-applicability-and-activation.md), with the CI exemption classes sanctioned by [decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md) and actionlint admitted by [decision 0324](../../../adr/0324-admit-actionlint-as-an-advisory-member-of-the-security-floor.md); ratified as intended design on 2026-06-27 by [decision 0253](../../../adr/0253-resolve-re-lock-control-plane-the-review-record-carries-the.md). Now **settled** — accepted by the operator on 2026-08-02 as the build baseline under [decision 0331](../../../adr/0331-settle-the-reconciled-corpus-as-the-build-baseline.md); a later change to this document requires the operator's recorded re-acceptance at its merge.*

## Summary

The GitHub layer that makes guardrails real: the enforcement a non-engineer can trust without
watching the mechanics. It acts on the [repository topology](repository-topology.md) and is
the gate every other guardrail sits downstream of. It locks **contracts and laws**, not concrete
scripts or workflow files — wherever a neighbouring system owns the leaf, this doc fixes the
invariant and defers the implementation.

## Behavior

### What travels, what doesn't

- **Travels as files** (via "Use this template"): the CI workflows, the PR and issue
  templates, the secret-scan and workflow-grammar-lint workflows, and `dependabot.yml`. The workflows and
  templates ship and run as-is. `CODEOWNERS` reaches the deployed repo as a file too, but by **rendering,
  not copying**: the template carries no committed `CODEOWNERS`; [provisioning](provisioning.md) renders
  it at first run from the engine path set × operator handle ([principles §3](../../../principles.md)) and
  the upgrade overlay preserves it as a keyed foundation file.
- **Does not travel** (settings, not files): the branch ruleset. Workflows run but cannot **block a
  merge** until the ruleset marks a check required; `CODEOWNERS` only gains teeth once the ruleset
  requires its review. (See [constraints](../../../reference/constraints.md).)

### The branch ruleset

Protection and required-status-check binding are one object, not two: a single GitHub **branch
ruleset** on the protected branch carries both the protection rules and the list of required checks.
The control plane locks that this ruleset exists and what it must require; the specific check names it
binds are the union the [validation](../guardrails/validation.md) suite and installed
[modules](../grammar/module-system.md) declare.

#### The protection floor — what the ruleset must require

The floor is the set of protection rules the ruleset must carry, fixed here as a contract; the concrete
ruleset payload and the API mechanics that apply it are [provisioning](provisioning.md)'s
build-spec leaf, and the required *check names* are derived (above), not part of this fixed set. Removing
or loosening any floor rule is a guardrail-weakening change ([principles §15](../../../principles.md)),
hard-gated at the merge. The ruleset must require:

- **A pull request before merging.** Every change to the protected branch flows through a pull request;
  direct pushes are blocked, so all work lands on the reviewable, contract-bearing pull request. Required
  approvals are **zero in solo** — a sole owner cannot approve their own pull request
  ([constraints](../../../reference/constraints.md)), so a non-zero count would deadlock the one operator — and
  **one code-owner review in team**, where a distinct AI identity makes the operator the enforced
  reviewer. "No required reviews in solo" therefore means zero required *approvals*, not the absence of
  this require-a-pull-request rule.
- **Status checks to pass before merging.** This is the required-check binding above; its names are
  derived from the [validation](../guardrails/validation.md) suite and installed
  [modules](../grammar/module-system.md). CI is the only unbypassable gate, so this is the rule
  that gives the automated checks their teeth at the merge.
- **Conversation resolution before merging.** An unresolved review thread blocks the merge, so a flagged
  concern cannot be silently merged past — the merge-time counterpart of the finding-disposition trust
  spine. It is kept in the floor because, unlike a stale-branch rule, the operator can clear it with a
  single click. Because this native GitHub block a non-engineer cannot self-diagnose — the merge button
  simply greys — it is **surfaced in plain language at the merge** (why the merge is blocked; that the
  operator may clear it once they have read the comment and accept it, never a bare *one click fixes it*;
  how to reach the thread, including a hidden or post-rebase-unreachable one), the rendering riding
  [build-orchestration](../lifecycle/build-orchestration.md)'s Review record read at the merge.
  The engine **pre-arms but does not act** — it never auto-resolves such a thread, which (the thread
  flagged a concern) would defeat the finding-disposition spine this rule serves; the residual non-engineer
  who still cannot locate the control is accepted in v1, not closed by an active duty.
- **Force pushes blocked** on the protected branch — no history rewrite of the record successive sessions
  build on.
- **Deletion restricted** on the protected branch — the protected branch cannot be deleted.

**Bypass is named honestly ([§7](../../../principles.md)).** In **solo** the operator holds repo-admin and
*can* bypass the ruleset: the floor is the enforced default, **not airtight prevention**, and the design
never dresses solo's consent gate as airtight ([§15](../../../principles.md)). That bypass-ability is
exactly why the §15 weakening-detection guard exists — a guard the bypassing change cannot itself falsify
— so any move to loosen a floor rule or widen bypass stays visible and hard-gated at the merge (*cannot
weaken silently*). As built, the guard's diff classification reaches every guard-bearing file, not only
the floor rules — a CI workflow, a check rule, an engine tool, `CODEOWNERS`, the tool-runtime lockfiles,
the suite declarations, and the traveling security-floor files all trip it. The structural close is the
operator's own choice of **team** identity (a distinct
actor that holds no bypass), which makes it *cannot weaken at all* — see *Identity and the merge gate*.

**The weakening hard-gate's pass condition is a distinct, deliberate acknowledgment — not the ordinary
merge click.** The §15 weakening-detection guard classifies the change's diff and hard-blocks a weakening
change *until that acknowledgment is present* (the guard mechanism is unchanged — [D-051](../../../adr/0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md)),
so a weakening change cannot *silently* ride the same one-click merge an ordinary change does. The acknowledgment is
**exactly one additional deliberate affirmative act** beyond the merge click — distinct from a one-click
merge, and no more than one act (not a banner to scroll past, not a ceremony gauntlet). Its prompt names,
**in plain operator language, the concrete protection that weakens and what the AI could then do unwatched**
— never maintainer vocabulary (the leak-guard of [§12](../../../principles.md) binds this surface, because
for a weakening change the wording is what makes the consent *informed* — poor wording silently defeats the
gate even when the block fires). The acknowledgment's concrete form is a build-spec
leaf, constrained here to **a single bounded affordance the operator cannot fail at by mistyping** — a
pull-request checkbox or an operator-applied label drawn from a bootstrap-provisioned acknowledgment label
the operator *applies* but never hand-creates (consistent with the label scheme below), never a typed
phrase and never a command to run: the
artifact is an *input* to the same frozen-named, trusted-source-evaluated §15 guard ([D-051](../../../adr/0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md):
it reads the diff only and never executes head code), never a parallel required check a bypass could
satisfy on its own. Ownership is fixed so the form is never invented unowned — the control plane owns the
contract, [validation](../guardrails/validation.md) owns the guard's check wiring, and the form
is concretized at build time under the pull-request contract below.

This is the **second beat of one §15 consent spine**, not a second independent gate: the plan-gate §15
headline ([build-orchestration](../lifecycle/build-orchestration.md)) is informed consent
*before the spend*, and this merge acknowledgment is the distinct *final* gesture the ordinary click does
not satisfy — so build-orchestration's plan-gate behaviour is unchanged. **It does not make solo
airtight.** In solo the engine commits as the operator and holds the operator's credentials, so it *could*
produce the acknowledgment artifact itself; the gesture therefore makes weakening **non-silent and
deliberate** — it must be affirmatively, legibly enacted rather than ridden silently past a routine click
— but adds **no machine detection in solo** and remains *cannot weaken silently*, never *cannot weaken at
all*. What it defends against is a careless change that bundles a weakening edit into ordinary work and a
rubber-stamped merge, not an engine that has decided to forge consent; the structural close stays the
operator's choice of **team** identity (above).

The floor deliberately omits four rules, each rejected for a reason rather than by oversight:

- **Require branches up to date before merging** (the strict status-check mode) — omitted from the solo
  floor. Under the engine's multi-pull-request and routine builds it forces a re-sync and a fresh check
  run on every other open pull request each time one merges, producing a blocked merge a non-engineer
  cannot clear (it needs a rebase they cannot perform) and starving the merge-and-walk model the
  [build orchestration](../lifecycle/build-orchestration.md) rests on. The stale-base risk it
  addresses is already carried behaviorally — the orchestrator reconciles a worker's base at integrate and
  CI re-runs on the submitted pull request — and it is a team-tier opt-in where a merge queue or active
  maintainers absorb the churn.
- **Require signed commits** — omitted: commit-author signing is setup friction a non-engineer cannot be
  assumed to complete, and the trust model rests on review and checks, not commit-author cryptography.
- **Require linear history** — omitted: the merge method is the product's workflow choice, not an
  engine-imposed law (the product owns the root — [repository topology](repository-topology.md)).
- **The "restrict updates" rule** — omitted: it deadlocks merges for an admin acting through bypass, so it
  is named here as an explicit non-member to keep a later implementer from reintroducing the deadlock.

None of the four is a governance-critical invariant, so none earns mechanical refusal
([§6](../../../principles.md)).

### The bootstrap contract

The ruleset is a setting, so it does not travel and must be applied once on the generated repo. This
is the #1 trust dependency — every other guardrail is downstream of it (see Risk
[R1](../../../reference/risks.md)). The control plane locks the **contract**, not the mechanism:

- **It is applied by an operator-privileged actor.** The default Actions `GITHUB_TOKEN` cannot create
  a ruleset or branch protection, even with elevated workflow permissions; applying one requires
  repository-administration capability — the classic `repo` scope, or a fine-grained token with
  **Administration: write**. A plain operator `gh` login carries `repo` by default, so the applying
  actor usually holds the capability already; the contract fixes only that it is an operator-privileged
  actor holding it — never the Actions token.
- **A committed CI guard fails loud until protection is in place.** The guard reads the evaluated
  rules for the protected branch (the per-branch rules endpoint, which the default token can read) and
  fails the check until the ruleset and its required-check bindings are detected. It does not read the
  admin-gated ruleset-configuration endpoints, which the default token cannot.
- **The unprotected state is surfaced to the operator in plain language, continuously** — not only as
  a red check on a pull request (at first run there is no pull request yet, and a red mark means
  nothing to a non-engineer). The orientation the operator sees each session states, in words,
  whether the safety gate is on.

**Deferred to [provisioning](provisioning.md):** *who* runs the bootstrap and *when* (the
self-deleting instantiator versus a standalone documented command), and the operator-facing first-run
interaction. This doc fixes the contract those mechanisms must satisfy.

### Identity and the merge gate

The trust proposition is "the AI builds; a human gate sits at merge to the protected branch." The
shape of that gate is named honestly per [principles §7](../../../principles.md):

- **Solo (default).** The AI commits as the operator. The **enforced** gate is the automated required
  checks; the operator's merge click is **informed consent, not a code review** — a non-engineer
  cannot review code, and the design never dresses the click up as review. (This is the consent for an
  *ordinary* change; a guardrail-**weakening** change additionally requires the distinct §15
  acknowledgment above, which the ordinary click does not satisfy.) `CODEOWNERS` *routes*
  attention rather than enforcing a second approver. Because the gate requires a pull request and the
  required checks but no required reviews in solo, the operator can merge their own pull request. The
  corollary is load-bearing: in
  solo mode the automated checks **are** the trust mechanism, so their strength matters, and the
  structured pull-request contract below is what makes the merge an *informed* consent.
- **Team (upgrade).** A distinct AI identity (a bot or GitHub App) authors the AI's commits, so the
  operator becomes the enforced code-owner reviewer. This is the only tier with genuine second-party
  human review; it is an opt-in upgrade, not the baseline, because it adds identity setup a solo
  operator does not need.
- **External contribution.** When the operator contributes to a product repo they do not own
  ([external-contribution](../lifecycle/external-contribution.md)), this control plane governs only
  the operator's **fork** — its own protected branch plus the engine's pre-submission checks. The
  **acceptance gate is the upstream project's own review/CI**, which the operator cannot configure: a governed
  upstream's review is the human gate (its human is not the operator); an ungoverned upstream's merge is no
  gate, so the fork-side checks are the only real one (named honestly, [§7](../../../principles.md)).

### The pull-request contract

The pull request is where successive AI sessions present work for the human gate, so its structure is
a trust mechanism, not a scaffold. The committed PR template requires these sections:

**Purpose · Scope · Out of scope · Risk · Validation · Review · Files of interest · AI involvement.**

The built template adds structure the check also gates: each section carries a one-line **`Impact`**
subsection (the consequence sentence a reviewer reads first), and a two-paragraph **consent preamble**
rides above the first heading — the standing note that a green check shows conformance, not correctness,
and that the operator's merge is the binding gate — anchored by fixed phrases the check matches, because
a heading scan cannot see copy above the first heading. A soft **`Behaviors`** subsection under Scope
names the falsifiable capabilities delivered; it nudges, never gates.

A **PR-body completeness check** is bound as a required check: it fails the merge until the sections
are present and non-empty **for the Engine-authored, contract-bearing pull requests the contract governs**.
The contract binds the pull requests an Engine build session authors; two classes sit **categorically
outside the contract's domain**, and for each the completeness check is a **disclosed not-applicable
no-op** (a stated pass, never a silent green):

- **A recognized external automation's pull request**, keyed on the PR author GitHub sets
  authoritatively (a fork cannot author a pull request as a GitHub-managed app identity). As built the
  exempt-author set holds `dependabot[bot]` — whose dependency-update PRs carry their own change account
  (changelog, release notes, compatibility data) and never pass through the PR template — and
  `github-actions[bot]`, covering the repository's own recognized automation
  ([decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md)).
- **A single-purpose engine pull-request class, keyed on a label**: a pull request carrying the
  erasure-class label (as built, `engine-erasure` — a different label from the engine-domain label below)
  is a single-purpose erasure proposal whose deliberate plain-language consent body *is* its account of
  the change, so the eight-section contract does not bind it
  ([decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md);
  the label class exists because the erasure proposer authors under the operator's own token, which
  author-keying cannot scope).

This **domain
boundary is the contract's** (owned here); the [validation](../guardrails/validation.md) check
rule realizes both classes as data — the check grammar carries them as sanctioned optional fields — and
the engine honors them,
keeping the closed kinds author- and label-agnostic. Because a green required check otherwise reads to the operator as
*verified*, the not-applicable disclosure is surfaced to the operator through the AI's own reply (the
[operator-presentation relay](../../../reference/glossary.md)), not only in CI output. The exempt sets are part of
a check definition, so **introducing or widening either is a guardrail-weakening change**
([§15](../../../principles.md), [D-207](../../../adr/0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md),
[decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md)) —
the change trips the §15
weakening-detection guard, lands only behind the operator's distinct acknowledgment, exactly as the
[dependency-discipline](../../modules/dependency-discipline.md) accepted-exception allow-list does,
and demands a fresh spoof-safety re-confirmation (non-registrable is not spoof-safe for every bot
identity — the widening law the check grammar itself now states);
the §15 guard itself carries no such exemption and continues to evaluate every author. The tiers are honest —
*structure and presence are hard-gated; truthfulness is posture* (a check can confirm the "AI
involvement" section is filled, not that it is accurate).
"Files of interest" and "AI involvement" direct the human reviewer's limited attention (a
human-facing hook into the [attention](../cognitive/attention.md) foundation) and flag
whether the AI made design decisions or mechanical edits; where it made design decisions, those land
in the authoritative decision/contract surface, and the section references them rather than replacing
them.

**Review** records what review the change received — the plan-review and pre-submission depth that
ran, the lenses that ran, gate completion, the findings' dispositions, and any post-audit-fix delta —
and surfaces the change's **operator-runnable acceptance steps**: the steps the operator can run
themselves to watch the change work, rendered from the realized `locked` spec's operator-runnable
acceptance criteria, or a plain reason-named line stating, in cause-language a non-engineer accepts,
why there is nothing for them to run (a behavior-preserving refactor, an internal change, or no spec
to surface against) — never leaning on a passed mechanical check as if it were the operator seeing the
change work. It is the
**judgment-layer** record, distinct from **Validation** (mechanical-check results) and from **AI
involvement** (what the AI did), bound by the completeness check exactly as its siblings — **presence
and non-emptiness hard-gated; truthfulness posture**. Because a non-engineer reads it at the merge, it
is rendered in plain language and states, in the block itself, that it is the engine's own account of
the review and that the operator's approval is the real gate. Its **review-judgment** part is the
**one** stretch of the contract whose subject the operator cannot independently corroborate (unlike
Validation's visible checks), so that part's posture-truthfulness tier carries more weight than its
siblings'; the **operator-runnable steps** are its converse — the one part the operator *can*
corroborate by running, the [§17](../../../principles.md) behavioral correlate brought to the merge
where consent happens, surfaced as a check the operator may run when the change warrants it rather than
a duty on every merge ([goals §6](../../../reference/goals-and-quality.md) low-ceremony), an unrun step a promise
rather than proof and never dressed as a passed check.
*How* the AI fills both — the verbatim render of the operator-typed steps, the bounded reason-named
no-op, and the plain-language rendering — is the
[build orchestration](../lifecycle/build-orchestration.md) layer's at submit (the seam below).

Seam: the control plane locks the required-section contract and that PR-body completeness is a gated
check. *How the AI fills it* is the build workflow's job — the
[build orchestration](../lifecycle/build-orchestration.md) fills the contract at submit (the
Review section especially), with per-turn capture the [close](../lifecycle/close.md)
ritual's; the *check implementation* is the [validation](../guardrails/validation.md)
layer's.

**The human issue templates** — `bug`, `feature`, `engine-fault` — are the *human's* front door for
filing work through the web "New issue" form, the issue-side companion to the PR contract above. They
travel as files, and like the PR contract the control plane **pins their sections** (the prescribed shape,
guidance not a gate — below) while the operator-facing prompt copy stays a build-spec leaf under the
plain-language law: **`bug`** — what
happened · what was expected · how much it gets in the way; **`feature`** — the need or problem · the
outcome wanted · how success is recognized; **`engine-fault`** — what the engine did · what was expected
instead · what the operator was doing at the time. Two laws shape them, both for the non-engineer who
files them. **`engine-fault` asks for narration, not diagnosis** — the operator never names *which*
component faulted or *how to reproduce* a defect (a localization a non-engineer cannot supply and the
engine itself derives — the [audits](../guardrails/audits.md) escalate-upstream division of
labor: the engine drafts the technical detail, the human reports and files); the prompt tells the filer they need not know the cause. And **the templates guide,
they do not gate** — pre-filled prompts help a filer structure their thoughts but never *block* a report
behind required fields, so a non-engineer is never stranded behind a form: they ship as **markdown
templates, never issue forms with required-field validation**, so nothing left blank can block submission
(the low-ceremony attribute; the [D-141](../../../adr/0141-lock-product-design-the-design-front-door-the-fifth-module-l.md) anti-coercion posture). This doc fixes the
sections; the prompt copy is authored at build under the plain-language law — in the words an operator
already uses, never developer issue-tracker idiom (no "scope", "environment", "expected vs. actual",
"acceptance criteria", "reproduction steps", or "surface").

### Engine Issues and the label scheme

Engine work and engine self-monitoring are tracked as **GitHub Issues**, and an Issue is marked as the
engine's own by a single **engine-domain label** the engine applies to every Issue it creates — the
subject-of-claim tag decided at [D-039](../../../adr/0039-reports-self-improvement-scope-engine-only-self-monitoring-o.md). An **engine-labeled Issue** is
engine-owned; an Issue without the label is ordinary product backlog (there is no separate "product"
label, so an Issue is never ambiguously both). The control plane owns this scheme as a contract (and, below, the engine-authored-issue body contract); the
concrete label strings and the mechanism that applies them are deferred build-spec leaves.

- **The engine-domain label is the canonical routing substrate.** The set of open engine-labeled Issues
  is the native, citable home the self-monitoring loop runs over: [telemetry](../guardrails/telemetry.md)'s
  debt register is the view over it, [state](../cognitive/state.md) derives its count from it,
  [attention](../cognitive/attention.md) ranks it for the boot surfacing,
  [audits](../guardrails/audits.md) sweeps it for stale debt, and
  [github-projects-sync](../../modules/github-projects-sync.md) projects it onto the board. Each
  **reads** the label by its presence; only the **creating producer** applies it (telemetry on triage,
  audits on a finding, and [build-orchestration](../lifecycle/build-orchestration.md) on a build
  Issue). Consumers never
  mutate the label — the control plane owns the channel's *definition*; each consumer owns only its own
  acting-mechanism over the channel ([principles §16](../../../principles.md)).
- **The product spec is a committed corpus outside the label scheme; product work is ordinary backlog.**
  The product's current-state specification and its acceptance criteria live in
  [product-design](../../modules/product-design.md)'s committed `docs/spec/` corpus
  ([D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)) — a product-owned artifact, never an engine-labeled Issue, so the
  scheme carries **no spec marker**. [build-orchestration](../lifecycle/build-orchestration.md)
  resolves that committed corpus (the spec doc a work Issue points at → its acceptance criteria) as the
  referent its `product-intent` and `spec-conformance` lenses check against; a build with no spec to resolve
  is build-orchestration's **disclosed no-op**, never a silent green — Build never depends on a spec
  existing. That resolution — and the precise condition under which it is a no-op — is a path read
  [build-orchestration](../lifecycle/build-orchestration.md) owns, not a label this scheme defines, and it holds whether or not a `locked`
  [product-design](../../modules/product-design.md) spec exists (product-design is `required` distribution — present in every Engine — locking a spec only when that work is done). **product-design's
  decomposed work Issues are ordinary product backlog**, the human-legible pointers grouped under the build's
  Milestones and authored by ordinary `gh` — they carry **no** engine-domain label (the label is
  engine-internal, [D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)), so they sit entirely outside the engine's own
  issue-authoring machinery (the helper, the body contract, and the reroute gate below).
- **Every engine-authored Issue carries a body contract.** Just as the PR contract fixes the pull
  request's sections, the control plane fixes a *body shape* for the Issues the engine authors in its own repo's
  engine-labeled channel — which, being created programmatically, **bypass the human issue templates entirely** (those populate only
  the web "New issue" form). The contract is a **loose structural skeleton**, in plain language: **(1)** what
  the Issue is and why it is here, **(2)** what — if anything — the operator must decide, or what happens
  next, and **(3)** any backstage references, rendered as plain links a person can follow, never a bare id
  dump. Item **(1)** is bound to the operator-communication law directly, so a producer not yet written
  inherits a plainness floor rather than only the example of the contracts it fills. It is deliberately loose because it is the *skeleton each producer's own operator-contract language
  fills* — [telemetry](../guardrails/telemetry.md)'s plain-language health-finding contract,
  [audits](../guardrails/audits.md)' "what was probed, found, and recommended" with its pinned
  exemplar — so the PR-contract tiering carries over unchanged: **the shape's presence is the floor, its
  truthfulness is posture**. (A draft the engine prepares for an *un-owned* upstream is **not** in this channel — it follows that host's conventions instead, per [external-contribution](../lifecycle/external-contribution.md).) Enforcement is the
  **by-construction helper beneath a channel-scoped reroute gate**: GitHub cannot gate Issue *creation* the
  way a required check gates a merge, so the engine authors its Issues through a single shared
  **issue-authoring helper** that assembles the body from the contract's parts (a producer that authors
  through it cannot omit one) — and a local **`PreToolUse` reroute gate** ([hooks](hooks.md)
  block-eligible, [modes](../lifecycle/modes.md)-registered) **denies** a `gh issue create` /
  issue-creating `gh api` bound for the **engine-labeled channel** whose body lacks the contract's structural
  markers, **redirecting** the session to author it through the helper. The gate keys on the **body's shape,
  not the tool's provenance** — a hand-matched conforming body passes, since the contract is about body
  shape — so the shape's presence is now a **gated floor** while its truthfulness stays **posture**
  ([§7](../../../principles.md), the PR-contract tiering) — a less-truthful body costs legibility, never a guardrail, so
  [§15](../../../principles.md) does not bite the truthfulness tier. Routing-through-the-helper is therefore **no longer
  mere posture but a block-eligible floor**, yet the gate is a **minimal-work-loss redirect**, not the wall:
  it loses no work (the Issue still gets filed, via the helper), so it clears the [§6](../../../principles.md)
  hard-block reservation a blanket Issue-blocker would not; and unlike the Explore build-gate it has **no
  merge wall behind it**, so it is the primary lever — **fallible and fail-open** (aliases, `eval`, stdin, a
  `--body-file`, or a `gh api` payload evade a shell-string check, [modes](../lifecycle/modes.md)) —
  with the **`on:issues` CI backstop** (below) the only catch-all for a slip: flagged into the engine's own
  remediation loop, never silently lost, never dressed as the wall. The escalate-upstream draft is **exempt**
  (un-owned upstream, not engine-labeled — above). The helper is core-provided shared code each producer
  **calls**, never a central registry a new producer must edit ([principles §14](../../../principles.md)/§16).
- **Deferred to build-spec leaves.** The concrete label string (the engine-domain-label name), the
  mechanism that applies the domain label (an explicit `labels` value at programmatic Issue creation, or a
  label call immediately after — never a web-only issue-template default, which the engine's programmatic
  creation path bypasses; the working mechanism confirmed against GitHub's label behavior at build time), and
  the provisioning step that ensures the label exists on the repository (applied automatically at bootstrap —
  the operator never hand-creates a label) are build-spec leaves of [provisioning](provisioning.md)
  and of each producing system. Because the label string and any issue-template copy are **operator-facing**,
  they are bound by the plain-language law — a non-engineer reads them, so no maintainer vocabulary appears in
  a label or template string. This doc fixes the scheme, its owner, the single-domain-label form, and the
  read-only-for-consumers rule; it does not fix the strings. (As built at the reconciliation pin: the
  engine-domain label string is `engine`; the shared issue-authoring helper lives at
  `.engine/tools/issue_author.py`; and the erasure-class label the CI exemption above keys on —
  `engine-erasure` — is a distinct label outside this routing scheme.) The committed-spec-corpus referent and its path
  resolution are [build-orchestration](../lifecycle/build-orchestration.md)'s
  ([D-244](../../../adr/0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md)), not part of this label scheme.

### CI harness

A pull-request-triggered workflow invokes the [validation](../guardrails/validation.md) suite
runner; the harness owns the trigger bindings and the convention by which a check registers itself.
Check *content* stays in validation; check-suite *membership* stays in the
[module system](../grammar/module-system.md). The harness is the seam, not the check set.

Because engine checks are Python ([surfaces/tools](../surfaces/tools.md)), a CI job that invokes
them **materializes the engine tool-runtime first** ([repository-topology](repository-topology.md)) —
a runtime-setup preamble (`astral-sh/setup-uv` pinned to a commit SHA, then group-scoped `uv sync`) authored
into every engine workflow that runs engine Python. This is a harness-level convention shared across those
workflows, not part of the check set, and it **does not change the frozen required-check name binding**
([D-156](../../../adr/0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)).

An **`on: issues` backstop workflow** complements the engine-authored-issue body contract's reroute gate
(above): on an Issue opened or edited, it checks an **engine-labeled** Issue's body for the contract's
structural markers and, on a miss, **flags** it — the engine-domain *needs-reauthoring* signal plus a comment
carrying the conforming skeleton — so the slip enters the engine's own detect→surface→remediate loop
([telemetry](../guardrails/telemetry.md)/[audits](../guardrails/audits.md)), **never a
silent rewrite and never an operator chore**. It is the soft-warn catch-all for the gate's known
shell-string fallibility; it does **not** gate creation (GitHub cannot), so it is an honest backstop, not a
second wall. The concrete label string and comment copy are build-spec leaves, operator-facing and
plain-language-bound.

### Scheduled work

The control plane locks the **single-flight concurrency-group pattern** for scheduled jobs and that
cron-triggered workflows exist — the law that periodic work cannot overlap itself. It does **not** lock
a concrete audit cron file: the [audits](../guardrails/audits.md) system, when ratified,
lands the workflow that runs on that schedule, and routine-session semantics live in their module. As
built the same single-flight law extends to the event-driven `on: issues` backstop above, keyed
per-issue, so concurrent edits to one Issue cannot race its conformance check.

### The security floor

Secret, dependency, code, disclosure, and workflow-grammar safety scales by deployment without ever
silently degrading. Each concern is present where the repository's tier supports it and **disclosed —
never silently dropped — where it is not**; visibility is never auto-switched to unlock a feature.

- **Secrets.** A committed open-source secret-scan CI workflow — **distinct from GitHub's own native
  secret scanning** — runs on every pull request regardless of repository plan or visibility, and
  `dependabot.yml` ships for all repos: the git-native floor that travels ([principles §5](../../../principles.md)),
  real protection on a free private repo. Where the repository supports it (public repos, or private repos
  with the paid tier), GitHub's native secret scanning and push protection upgrade it — strictly better,
  because push protection blocks a secret before it lands.
- **Dependencies.** `dependabot.yml` travels for all repos (above). Dependency *discipline* (version
  pinning, update cadence, review gates) is **not** part of this floor; it belongs to its module.
- **Code.** Native code scanning (CodeQL) is enabled where the repository supports it (public repos, or
  private repos with the paid tier). Unlike secrets, this pillar is **native-only — it carries no
  traveling fallback**: on a free private repo native code scanning is unavailable, so it is **absent
  there and disclosed as a known drawback**, never replaced by a bespoke scanner. It is a **native GitHub
  security feature** (the same class as native secret scanning) — distinct from the optional product-code
  *style/lint* governance the [clean-code](../../../reference/module-catalog.md) module owns
  ([D-095](../../../adr/0095-cut-expression-contracts-disposition-prose-organization-cove.md)), and it introduces **no third-party CI surface** (so the
  [dependency-discipline](../../modules/dependency-discipline.md) no-third-party-scanner stance
  is untouched). Its alerts are **advisory, not a merge gate** — a finding is surfaced for the Engine to
  address, never a block a non-engineer cannot clear ([§6](../../../principles.md)).
- **Disclosure.** A seeded, **operator-owned** `SECURITY.md` is the vulnerability-disclosure channel that
  travels to every repo — seeded at the **repo root** by [provisioning](provisioning.md) (product
  territory, so the upgrade overlay preserves it like any product file, no engine carve-out). Where the
  repository supports it (public repos), native **private vulnerability reporting** upgrades it; on a
  private repo PVR is **structurally absent** (a GitHub public-only feature, not a tier), disclosed, with
  the `SECURITY.md` the channel there.
- **Workflow grammar** ([decision 0324](../../../adr/0324-admit-actionlint-as-an-advisory-member-of-the-security-floor.md)).
  A committed **advisory workflow-grammar lint** (actionlint, pinned to a fixed binary version) travels to
  every repo and runs on every pull request over the `.github/workflows/` files — the engine authors its
  own CI workflows, and nothing else validates their Actions grammar for a non-engineer. Like the code
  pillar's alerts it is **advisory, never a merge gate**: its job name is deliberately outside the
  required-check list, so a finding is surfaced for the Engine to address, never a block a non-engineer
  cannot clear ([§6](../../../principles.md)). It mirrors the secret-scan workflow's traveling advisory
  shape exactly.

**Disclose, never downgrade silently** binds every member: where a native feature is unavailable the operator
is told, in plain language, what is off and what would unlock it, and work proceeds only on their choice.
The control plane locks these invariants; the concrete toggles, the seed, the disclosure wording, and the
first-run step are [provisioning](provisioning.md)'s build-spec leaves.

### Boundary

GitHub control-plane files are infrastructure artifacts, governed here and by the
[repository topology](repository-topology.md), and are outside the
[ontology](../grammar/ontology.md)'s surface catalog. The engine-label scheme above is
likewise GitHub issue infrastructure governed here, not a catalogued surface.

### Open questions

- The concrete bootstrap mechanism, token handling, and first-run UX move to
  [provisioning](provisioning.md) (its bootstrap-UX build-spec leaves). Full closure
  of Risk [R1](../../../reference/risks.md) depends on that first-run experience.

## Acceptance criteria

*In this table, `engine` means the named merge-gated check fully asserts the criterion; `operator` means your observation carries at least part of it — any named checks are partial support.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| What travels does so as files; what cannot be a file is named as not travelling, never assumed. | The build's travel tests (the seed, secret-scan, and wiring test modules, run in the CI suite) exercise the traveling files — partial support; no single named check asserts the whole statement, and the ruleset's not-travelling half is a settings observation. | operator |
| The branch ruleset requires a pull request before merging. | The `protection` check (hard, CI suite) reads the protected branch's evaluated rules and fails until a pull request is required, naming the missing floor rule. | engine |
| The branch ruleset requires status checks to pass before merging. | The `protection` check (hard, CI suite) fails until the required-status-check binding with the engine's frozen check names is detected. | engine |
| The branch ruleset requires conversation resolution before merging. | The `protection` check (hard, CI suite) fails until the ruleset requires review-conversation resolution. | engine |
| Force pushes are blocked and deletion is restricted on the protected branch. | The `protection` check (hard, CI suite) fails until force-pushes are blocked and deletion is restricted on the protected branch. | engine |
| Bypass is named honestly, and weakening a protection takes exactly one additional deliberate affirmative act by the operator. | The `guardrail-weakening` check (hard, run by the required `engine-guard` job) asserts the one-act half — a weakening diff stays red until the operator-applied acknowledgment label is present. That bypass is *named honestly* is prose you judge, not a check's assertion. | operator |
| A weakening is explained in plain operator language — the concrete protection that weakens and what the AI could then do unwatched. | The weakening guard's own finding copy carries the plain-language explanation — partial support; no check grades the wording's quality, which is exactly the posture tier this row protects. | operator |
| The bootstrap is applied by an operator-privileged actor; the engine cannot self-grant it. | The bootstrap runbook and its tool realize the operator-privileged path, and the CI guard reads with the default token only — partial support; the cannot-self-grant half rests on your observation at first run. | operator |
| A committed CI guard fails loud until protection is in place, and the unprotected state is surfaced to the operator in plain language, continuously. | The `protection` check (hard, CI suite) fully asserts the fails-loud half; the continuous plain-language surfacing rides boot's orientation, which no merge-gated check asserts — so the row stays with you, the check as partial support. | operator |
| The merge gate matches the identity tier — solo by default, team on upgrade, and the external contribution path. | Partial support across surfaces: the `protection` check evaluates the floor for the identity tier, the team-switch tool reconfigures it, and the external path's fork-side checks belong to its own document; no single check spans the three tiers. | operator |
| The pull-request contract carries its named sections, and its Review section is the gated judgment layer. | The `pr-body-completeness` check (hard, CI suite) asserts the first half fully: all eight sections — Review among them — present and filled, plus the per-section Impact lines and the consent-preamble anchors. That Review *is the judgment layer* — its content truthful, its verdict real — stays posture no check asserts, so the composite row stays with you, the check as partial support. | operator |
| A recognized external automation's pull request is categorically outside the contract's domain, and says so rather than passing silently. | The `pr-body-completeness` check's exemption fields resolve an exempt pull request to a disclosed not-applicable pass that names why the rule does not bind — never a silent green ([decision 0323](../../../adr/0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md)); the CI suite's exemption tests pin the disclosure. | engine |
| The engine-domain label is the canonical routing substrate for engine work, and every engine-authored Issue carries the body contract. | Partial support: the shared issue-authoring helper, the local reroute gate, and the `on: issues` conformance backstop each carry a leg; none is a merge-gated check over Issue creation (GitHub cannot gate creation), so the substrate's health is your observation. | operator |
| The product spec is a committed corpus outside the label scheme; product work is tracked as ordinary work. | The product-design module's spec checks govern the corpus's shape — partial support; that product work stays outside the label scheme is an absence no check asserts. | operator |
| The security floor covers secrets, dependencies, code, disclosure, and the advisory workflow-grammar member — and discloses what is off rather than downgrading silently. | Partial support: the travel tests carry the secret-scan and dependabot files, the security-floor tool renders the per-tier disclosure for the native toggles, and the advisory actionlint workflow ([decision 0324](../../../adr/0324-admit-actionlint-as-an-advisory-member-of-the-security-floor.md)) travels beside them; the disclosure's plain-language delivery is yours to observe. | operator |
