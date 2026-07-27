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

engine-template is distributed by "Use this template", which copies the **file tree** as one
commit. Issues, pull requests and history do not travel. So the containment surface is exactly the
committed file tree, and nothing else. Two consequences are load-bearing:

- engine-template's own Issues **legitimately** cite `D-###`, and must keep doing so — the build
  spec lives here, so an Issue with no reference to it could not point its build session at the
  spec that defines the build. Those never reach a deployed repository. They are not scanned.
- The traveling corners **are** the surface that matters, and they already carry the leak.

The contained vocabulary: the decision numbering `D-###` (short `D-24` and padded `D-0024`), the
`docs/adr/NNNN-slug.md` record paths, the alternate `ADR-####` spelling, and the retired workspace
name `engine-planning`. The engine's own `eADR-####` records are a separate sanctioned system,
exempted by a negative lookbehind — by construction, never by an exclusion list.

Enforcement lives in product territory: `tools/reference-containment/` and
`.github/workflows/reference-containment.yml`, with `tools/reference-containment/` declared in
`.engine/operator-guarded-paths.json`.

## Significance

**What a green run does and does not mean.** It means no listed token was found. It does **not**
mean the surface names its capabilities — prose naming neither passes, and no scanner can check the
positive half of the rule. A literal token match narrows risk and never proves absence: split,
encoded or homoglyph tokens pass, and paraphrase passes trivially. The scan is case-sensitive, so a
lowercase `d-296` passes — a deliberate trade, because the lowercase form appears inside slugified
record filenames, which are not references. The review at merge stays the real wall.

**What is enforced versus reported.** The `surfaces` scan compares against a committed baseline of
eight references that arrived from upstream; it alarms only on a **new** one. Those eight are not
fixable here — the upgrade overlay replaces those files wholesale — so gating on them would be
permanently red and unclearable, which is how a check trains people to ignore it. They are tracked
upstream instead. The workflow is advisory, never in the branch ruleset's required list.

**Why this cannot be an engine check.** A module on disk but absent from the engine manifest's
packages map permanently fails release-integrity; one listed in packages makes every engine upgrade
refuse, because a release never contains an instance-specific module. Adding the rule to an
existing module's manifest fails too — that manifest is engine-owned and overlay-replaced. Product
territory is walled off from engine upgrades by contract. A future session must not re-attempt an
engine-side home, and must restore these files if they are found missing.

**The self-protection gap that is now closed.** The previous version of this guardrail had to state
plainly that a pull request editing its own scanner was a guardrail change nothing alarmed. The
instance-extensible floor closes it: the declared prefix is read from the trusted base, unions with
the engine's own set and can never subtract from it, and its removal is detected directionally.

## Rationale

The leak is documented, not hypothetical. At the time of writing, eight references from this
repository's decision log sit in engine-template's own files — `.engine/pyproject.toml`,
`boot.py`, `hooks.py`, `test_boot.py`, and `eADR-0037` — and every one ships to every repository
generated from the template, where it names a decision log that repository cannot reach. A ninth
sat in the root `.gitignore` and is fixed in the same change that adds this record: that file is
carved out of the overlay, so the fix is durable, and rewriting its comment to name the capability
instead of the decision numbers demonstrates the rule on the highest-traffic file in the tree.

The token vocabulary was measured before it was chosen, and the rejected classes are recorded with
the command that produced each count so a later session can re-run rather than re-argue. At
`ee87be1`, with `grep -rhoE '<pattern>' docs .engine | wc -l`: `R[0-9]{1,2}` — 762 in `docs`, 17 in
`.engine`, colliding with registers, revisions and part designators; `Q[0-9]{1,2}` — 644, where
`Q1`–`Q4` are calendar quarters; `§[0-9]{1,2}` — 1,972, and it would fire on engine-template's own
`§`-numbered principles; `#[0-9]{2,4}` — 1,092 in `.engine` alone, and in an outbound submission
the target repository **is** engine-template, where a bare issue number is native and correct, so
it is unresolvable from text. `grep -rhoF 'docs/spec/' .engine` returns 623 — that path is a
generic engine convention, not a local identifier, and this repository's spec documents are already
capability-named. Each rejection is a guard that would cry wolf; a check people learn to click past
is worse than no check.

## Anti-choice

The strongest rejected alternative was **gating on the traveling corners as received here** — which
is what the originating request asked for, read literally. It was rejected on evidence: all eight
references exist byte-identically upstream, the overlay reverts any local fix, and one of them
(`ADR-0001` in the engine's own contract test) is a deliberately-invalid identifier a validator
must reject, so going green would require breaking an upstream test. The scan still runs over those
corners — the disagreement is between scanning and gating, and the request conflated them.

Also rejected: an instance-local engine module, inside or outside the packages map (permanently red,
or permanently refused upgrades); a line-numbered baseline (re-cut on every release as the overlay
moves lines — churn with no signal); scanning engine-template Issue and pull-request text (it does
not travel, and the references there are required); scanning commit messages in an outbound
submission (history does not travel either); an escape syntax so a legitimate finding could be
silenced in-band (a hole the scanner would then have to defend, and the first thing anyone reaches
for to quiet a finding they would rather not think about); and baking the rule into engine-template
itself, which would carry it into every deployed repository where it is meaningless — though the
*generic* form of it, a deployment-declared vocabulary the existing external-contribution pause
points consult, is filed upstream as its own request.

## Status

Accepted. Two gaps stay open and are not closed by this change. First, the scanner's **code** is
guarded but its **wiring** is not: nothing alarms if the operator runbook or the push-hook install
is removed, so the attachment rests on review. Second, the first landing of a guarded path enters
without an acknowledgement (a pure addition is a strengthening), so this change's correctness rests
entirely on the review that merges it — the same wall named above.

This identifier was issued once before, at `b9dd58e`, for a narrower version of this decision, and
removed by the revert at `229e1ee`. It is reused deliberately rather than skipped; history
therefore carries two records under it, and this one supersedes in substance what that one covered.

After every engine upgrade, confirm: the workflow and `tools/reference-containment/` are present
and the workflow is green; `check.py surfaces` reports no new reference and the baseline has not
gone stale in either direction; `.engine/operator-guarded-paths.json` still names the scanner (it
survives by an operator-config carve-out, not by the engine/product wall, so a change to that
carve-out would silently drop the alarm); and the `.gitignore` comment has not been re-leaked.
