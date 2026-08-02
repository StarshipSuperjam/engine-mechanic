---
status: accepted
engine_record: true
---

# Sanction the built engine-erasure label exemption and the widened CI author set

*Decided 2026-08-01 in this repository, by the operator, in the wave-5 ruling round under
[decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md). This is the
deferred cross-wave "erasure cluster" ruling — it settles the register items guardrails-U01,
infrastructure-U09, surfaces-tools-U06, and lifecycle-U17 in one act.*

## The decision

The two CI-exemption classes the built engine carries on the PR-body completeness check are
**sanctioned as the design**:

- **`ci_label_exempt: ["engine-erasure"]`** — a pull request carrying the `engine-erasure` label is
  a single-purpose erasure proposal whose deliberate plain-language consent body *is* its account of
  the change; the eight-section contract does not bind it. The waiver is a **disclosed
  not-applicable pass**, never a silent skip.
- **`ci_author_exempt` widened to include `github-actions[bot]`** — alongside `dependabot[bot]`,
  covering pull requests authored by the repository's own recognized automation.

The check grammar's blessing of both optional fields (`check.v1.json`, which names widening either
set a guardrail change demanding spoof-safety re-confirmation) is ratified with them. The
[control-plane](../spec/systems/infrastructure/control-plane.md) spec now discloses both classes.

This reverses, in letter, the scope law of
**[D-207](0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md)**, which admitted
the exemption grammar as *"one author on one rule"* — no registry, no second axis, the
pull-request **author** as the sole exemption key and `dependabot[bot]` its sole member. As built,
the set holds a second author and the grammar a second, label-keyed axis. Its companion
**[D-208](0208-resolve-the-d-207-dependabot-pr-contract-exemption-landed-te.md)** is **honored,
not reversed**: D-208 pinned the caveat that non-registrable is not spoof-safe for every bot
(`github-actions[bot]` is assumable by any in-repo workflow), so any widening forces a fresh
spoof-safety re-confirmation — a duty the schema's own field text now carries as standing law.
What those records actually protected is preserved:

- **The consent gate is untouched** — the erasure flow's binding gates are the operator's merge of
  the single-purpose proposal PR and the terminal confirmation; the exemption waives only the
  body-format contract, and the reviewed build confirmed the label path structurally cannot reach
  the erasure consent machinery.
- **The disclosure law holds** — both classes resolve to the disclosed not-applicable pass D-207
  invented; no silent green entered the system.
- **Widening stays a guarded act** — introducing or widening either set edits `.engine/check/`,
  so it trips the §15 weakening guard and lands only behind the operator's distinct
  acknowledgment, exactly the gate D-207 kept; the schema's re-confirmation duty rides on top.

## Why

The label class exists because author-keying cannot express it: the erasure proposer runs as a
local hook authoring under the **operator's own token**, so an author-keyed waiver would have to
exempt the operator's identity wholesale — vastly broader than one labeled, single-purpose PR
class whose plain-language consent body is the whole point. D-207's "one author on one rule" was
an explicit v1 scope line, not a load-bearing safety property; the properties that do carry
weight (disclosure, author-agnostic kinds, §15-gated widening, spoof-safety re-confirmation) all
survive intact. The remaining gap is upstream bookkeeping, not design — the sanctioning record
and the explicit re-confirmation are owed to engine-template's own decision log, tracked as
[engine-template issue 782](https://github.com/StarshipSuperjam/engine-template/issues/782).
Sanctioning now, with that record still owed, is a **deliberate sequencing**: the operator blesses the
widening before the upstream re-confirmation lands, with the §15 guard (which exempts no author) and
the merge gate carrying the interim — a conscious choice, not an oversight.

## What we ruled out

**Roll back to the author-only, dependabot-only boundary** (rejected — it would delete the only
mechanism scoping the erasure-proposal waiver, or force exempting the operator's whole identity;
the build's reviewed properties already hold the line the rule defended). **Sanction silently,
without a record** (rejected — D-207/D-208 are named prior decisions; adopting their reversal
without an appended record is the drift the append-only log exists to prevent). **Defer again to
the wave-6 check-document reconciliation** (rejected — every fact the ruling needs was verified at
the pin this wave, and control-plane is the boundary's owning document; wave 6 inherits a settled
ruling instead of a third deferral).
