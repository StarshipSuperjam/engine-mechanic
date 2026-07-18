---
status: draft
---

# Infrastructure

## Summary
Infrastructure is the substrate layer: the platform-side control plane that makes guardrails real at the
merge, the in-session hook substrate, provisioning across a repository's whole life, and the repository
partition the engine confines itself to. This document carries the laws added on top of the engine's
foundational canon — the issue-channel grammar and its reroute gate, the extended security floor, the
seeded root files, first-run travel safety, the provisioned verdict, the engine's home coordinate,
checkout stewardship, and the standing license-seed remedy. Contracts the canon already fixes are
referenced conceptually, never restated here.

## Behavior

### Control plane

The human issue templates guide, never gate: their sections are pinned as prescribed shape, a report left
partly blank is never blocked, engineer idiom never appears on the filing surface, and the fault template
asks the operator only to narrate what happened — the engine derives the diagnosis
(ADR-0030).

Every issue the engine authors into its own labeled channel carries a plain-language body contract — what
it is and why, what the operator must decide or what happens next, references as followable links —
assembled through one shared passive authoring helper; the shape's presence is a gated floor, its
truthfulness stays posture (ADR-0030).

A non-conforming engine-labeled issue that slips past the gate is flagged by a repository-side backstop
with a comment carrying the conforming skeleton — never silently rewritten, never turned into an operator
chore; drafts for un-owned upstreams follow the host repository's conventions instead
(ADR-0030).

The security floor covers code scanning and vulnerability disclosure on its locked grain: native scanning
is enabled where the repository's tier supports it and its alerts are advisory, never a merge gate; where
unsupported, the gap is disclosed in terms the operator can evaluate and visibility is never auto-switched;
a vulnerability-disclosure file is seeded at the repository root as operator-owned product territory, and
the native private-reporting channel is enabled where the platform offers it, with its consequence
disclosed (ADR-0031).

### Hooks

The block budget admits exactly one exception to its governance-critical-only membership: a pre-action
deny that redirects the same action to a conforming path with no work lost. The engine-issue conformance
reroute is that member — the issue still gets filed, through the helper — and, like every local block, it
is never dressed as an unbypassable wall (ADR-0030).

### Provisioning

First-run retirement is reference-closed: no file that survives instantiation statically references a
retired first-run asset, with no guard-it-instead exemption; a hard CI closure check enforces the
invariant and is honest about what static analysis cannot see, and its findings name the consequence, the
concrete reference, and a disposition in plain language (ADR-0033).

The provisioned verdict keys on instantiator presence, three-state: present means unprovisioned and setup
is offered; absent with the engine manifest present means provisioned; absent with no manifest means a
broken checkout, routed to the strand detector and never silently read as done. The manifest is a resume
checkpoint and upgrade source-of-truth, never the verdict alone
(ADR-0035).

A fresh, not-yet-set-up copy is surfaced every session as a standing, collapse-managed, always-declinable
onboarding offer until setup actually runs — surface-and-offer, never a gate — and the construction
repository suppresses the offer in its own sessions at the maintainer layer
(ADR-0035).

The root readme is seeded-then-ceded: at first run the engine replaces its own marketing landing seed —
and only a positive match of that seed — with a product-owned starter carrying the required-spine
disclosure in plain operator language; the replacement is disclosed as what changed and why it is theirs,
and the engine never re-touches the root readme after instantiation
(ADR-0032).

The engine manifest records the engine's home repository, the single coordinate the updater and the
upstream escalation both resolve; resolution refuses loudly — naming the home, or the cause and remedy —
rather than ever falling back to the deployed repository's own origin, and repointing the home is a
weakening-class change requiring the operator's distinct acknowledgment
(ADR-0036).

A standing, boot-invoked, offline, consent-gated detector recognizes the engine's own historically-shipped
license seeds still sitting in the product-root license file; on consent the removal lands as a reviewed
pull request the operator merges, a plain decline collapses the surfacing to a terse standing line, and an
explicit kept-on-purpose acknowledgment retires the finding
(ADR-0037).

Strand detection over the operator's checkout is branch-agnostic and two-stage: a gentle, offline,
collapse-managed signal the day the checkout parks off the default branch, and a network- and
consequence-gated escalation once merged main-line work is missing; every fix is lossless or it does not
run, merged-versus-unmerged reads shape only the offer's tone, and no git vocabulary reaches the operator
(ADR-0034).

The engine owns no cleanup of accumulated local session worktrees and branches — they are the assistant
platform's exhaust, touching no engine surface, remediated at the local and platform layer, never by
standing engine machinery (ADR-0034).

### Repository topology

Product ownership of the repository root admits exactly one narrow standing exception: the engine may
propose, through a reviewed pull request, the removal of its own still-recognizable seed from the
product-root license — never a direct write, so the reconcile-once rule is otherwise untouched
(ADR-0037).

Seeded root files are a reconcile, not a claim: seeded or cleared once at first run only where the slot
still holds the engine's own recognizable seed, product-owned thereafter, and preserved untouched by every
later engine overlay (ADR-0032,
ADR-0031).

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| A blank or partial human issue report submits without being blocked | File an issue leaving guided sections empty; it is accepted | operator |
| A non-conforming engine-labeled issue creation is denied and redirected, and the issue still gets filed via the helper | Attempt a bare engine-channel creation in session; observe the redirect and the filed conforming issue | engine |
| A slipped non-conforming engine-labeled issue is flagged with the conforming skeleton, never rewritten | Open a malformed engine-labeled issue directly; observe the backstop's flag and comment, body unchanged | engine |
| Native scanning is on where supported, skipped-and-disclosed where not, and its alerts never block a merge | Compare repository security settings to the first-run disclosure; merge with an open alert | engine |
| A vulnerability-disclosure file exists at the root and survives an engine upgrade unchanged | Inspect the root after first run and again after an upgrade | operator |
| The reroute gate never blocks the operator's own or unlabeled issues | File ordinary issues while a session runs; none are denied | operator |
| A survivor referencing a retired first-run asset fails CI before merge | Introduce such a reference on a branch; the closure check fails with a plain-language finding | engine |
| A fresh template copy offers setup every session until setup runs | Generate a copy, decline setup, restart; the offer returns, collapsed | operator |
| A checkout missing both instantiator and manifest is surfaced as broken, never read as done | Remove both in a scratch copy; boot routes to the broken-checkout surfacing | engine |
| The root readme is replaced only when it still matches the engine's seed | Edit the readme before first run; the edit is preserved and the replace is a no-op | engine |
| An update with an unresolvable or absent home refuses loudly with the cause, never falling back to origin | Request an update in each state; observe the named refusal and no fetch | engine |
| Repointing the engine's home demands the distinct weakening acknowledgment before merge | Propose a home change; the merge blocks until the acknowledgment is given | engine |
| An off-main park is signaled offline on day one; the behind escalation names a felt consequence and only after a fetch | Park the checkout off the default branch; observe the gentle signal, then the escalation once merged work is missing | engine |
| A strand fix never runs when work could be lost | Dirty the tree or add a stash; the fix withholds and offers the rescue path instead | engine |
| A recognized license seed is offered for removal as a reviewed pull request; decline collapses, kept-on-purpose retires | Seed a historical license text; observe the offer, the proposal on consent, and both exit paths | operator |
| No engine machinery sweeps local session worktrees or branches | Accumulate session branches; confirm no engine surface mutates them | engine |
