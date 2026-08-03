---
id: engine-mechanic-eADR-0001
title: Traveling surfaces name capabilities, not references — the containment guardrail and where it lives
status: accepted
date: 2026-07-26
---

## Decision

A surface that travels from engine-template to a repository deployed from it must name the
**capability** it means, never a **reference** that resolves only in engine-mechanic. This
repository holds engine-template's spec and its 319 decision records; that corpus stays here by
design, because putting it in the template would push it into every generated repository.

engine-template is distributed by "Use this template", which copies the **file tree** as one commit.
Issues, pull requests and history do not travel, so the containment surface is exactly that committed
tree. One consequence is load-bearing and easy to get backwards: engine-template's own Issues
**legitimately** cite `D-###` and must keep doing so — the build spec lives here, so an Issue without
it could not point its build session at the spec. Those never reach a deployed repository or get
scanned; the traveling corners are the surface that matters, and already carry the leak.

The contained vocabulary: the decision numbering `D-###` (short `D-24` and padded `D-0024`), the
`docs/adr/NNNN-slug.md` record paths, the alternate `ADR-####` spelling, and the retired workspace
name `engine-planning`. The engine's own `eADR-####` records are a separate sanctioned system,
exempted by a negative lookbehind — by construction, never by an exclusion list.

Enforcement lives in product territory: `tools/reference-containment/` and
`.github/workflows/reference-containment.yml`, with `tools/reference-containment/` declared in
`.engine/operator-guarded-paths.json`.

## Significance

**What a green run does and does not mean.** It means no listed token was found — **not** that the
surface names its capabilities: prose naming neither passes, and no scanner can check the positive
half of the rule. A literal token match narrows risk, never proves absence: split, encoded or
homoglyph tokens pass, and paraphrase trivially. A file the scanner cannot read as text is named in the
output and kept out of the clean tally, not counted as examined — the review at merge stays the real wall.

**What is enforced versus reported.** `surfaces` compares against a committed baseline recording
each upstream-authored reference *and how many times it occurs*, and alarms only on something new.
Those are not fixable here — the overlay replaces those files wholesale — so gating on them would
be permanently red and unclearable, which is how a check trains people to ignore it; they are
tracked upstream. The workflow is advisory, never in the branch ruleset's required list.

**Why this cannot be an engine check.** A module absent from the engine manifest's packages map
permanently fails release-integrity; one listed in it makes every upgrade refuse, since a release
never carries an instance-specific module. Adding the rule to an existing module's manifest fails
too — engine-owned, overlay-replaced. A future session must not re-attempt an engine-side home.

**The self-protection gap this closes.** The previous version had to state that a pull request
editing its own scanner was a guardrail change nothing alarmed. The instance-extensible floor
closes it: the declared prefix is read from the trusted base, unions with the engine's own set and
can never subtract from it, so a request cannot both unguard the scanner and edit it. Nor can a
two-request sequence do it quietly — deleting the declaration, renaming it away, and removing the
entry are each detected directionally and each demand the acknowledgement. What is not gated is a
pure *addition*, which is a strengthening.

## Rationale

The leak is documented, not hypothetical. At the time of writing, ten sites in engine-template's own
files cite this repository's decision log — three in `.engine/pyproject.toml`, three in `boot.py`, and
one each in `hooks.py`, `test_boot.py`, `eADR-0037` and the root `.gitignore` — and every one ships to
every generated repository, where it names a decision log that repository cannot reach. Two further
recorded entries are not defects but test-data tokens, kept in the baseline, not special-cased in the scanner.

The `.gitignore` site is fixed in the same change that adds this record — that file is carved out
of the overlay, so the fix is durable here. It demonstrates the rule rather than reducing the harm,
since a deployed repository receives engine-template's copy; the site stays on the upstream list.

Each rejected token class is recorded with the command that produced its count, so a later session
re-runs rather than re-argues. At `ee87be1`, via `grep -rhoE '<pattern>' docs .engine | wc -l`:
`R[0-9]{1,2}` — 762, colliding with registers, revisions and part designators; `Q[0-9]{1,2}` — 644,
where `Q1`–`Q4` are calendar quarters; `§[0-9]{1,2}` — 1,972, and it would fire on
engine-template's own `§`-numbered principles; `#[0-9]{2,4}` — 1,092 in `.engine` alone, and
unresolvable from text, since in an outbound submission the target **is** engine-template, where a
bare issue number is native. `grep -rhoF 'docs/spec/' .engine` returns 623 — a generic convention,
not a local identifier. Each would cry wolf, and a check people learn to click past is worse than
none. Case-INsensitivity was measured the same way: matching only uppercase let a lowercase
reference through, and closing that costs one benign fixture hit across the scanned surfaces.

## Anti-choice

The strongest rejected alternative was **gating on the traveling corners as received here** — what
the originating request asked for, read literally. Rejected on evidence: the references exist
byte-identically upstream, the overlay reverts any local fix, and one (`ADR-0001` in the engine's
own contract test) is a deliberately-invalid identifier a validator must reject, so going green
would require breaking an upstream test. The scan still runs over those corners — the disagreement
is between scanning and gating, and the request conflated the two.

Also rejected: an instance-local engine module, in or out of the packages map (permanently red, or
permanently refused upgrades); a line-numbered baseline (re-cut every release as the overlay moves
lines — churn with no signal); scanning engine-template Issue and pull-request text (it does not
travel, and the references there are required) or commit messages (history does not travel either);
an escape syntax letting a finding be silenced in-band (a hole the scanner must then defend, and the
first thing anyone reaches for to quiet a finding they would rather not face); and baking the rule
into engine-template itself, meaningless in every deployed repository — though its *generic* form, a
deployment-declared vocabulary the existing contribution pause points consult, is filed upstream.

## Status

Accepted. Two gaps stay open. First, the scanner's code and runbook are guarded, but nothing
*installs* the push hook — it is a reviewed source file an operator copies by hand, so the outbound
leg runs only where someone set it up. Second, the first landing of a guarded path enters without
an acknowledgement (a pure addition is a strengthening), so this change's own correctness rests
entirely on the review that merges it — the same wall named above.

This identifier was issued once before (a narrower version, at `b9dd58e`) and removed by the revert
at `229e1ee`; reused deliberately rather than skipped, so history carries two records under it.

This deployment carries one **local patch to an engine-owned file**, disclosed here because the
overlay reverts it on every upgrade. `.engine/tools/test_seed.py` asserts the absent-declaration case
by reading the *host* repository's own declaration, so it holds only while no deployment uses the
mechanism — and this deployment does, for exactly the case the guard's own source documents; the patch
asserts the same property against a path that cannot exist (engine-template issue 638). The recorded
residue is issue 637, and the generic form of this rule, offered upstream, is issue 639.

After every engine upgrade, confirm: the workflow and `tools/reference-containment/` are present
and the workflow is green; `check.py surfaces` reports no new reference and the baseline has not
gone stale in either direction; `.engine/operator-guarded-paths.json` still names the scanner (it
survives by an operator-config carve-out, not by the engine/product wall, so a change to that
carve-out would silently drop the alarm); the `test_seed.py` patch above is still applied, or
upstream has fixed it; and the `.gitignore` comment has not been re-leaked.
