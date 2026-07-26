---
status: accepted
engine_record: true
---

# Re-litigate `state` (honesty): name the floor's known-unbounded faults; harden the stale-count rendering against reliance

*Decided 2026-05-27 in the design workspace.*

## The decision

Under the litigation-alarm protocol (operator-approved as part of the cognitive-substrate remediation plan), re-litigate [state](../spec/systems/cognitive/state.md) with two **honesty / current-state** corrections surfaced by the efficacy-scorecard audit (a workspace-process exercise, kept out of the Engine docs per layer discipline): **(1)** add a **"known-unbounded"** bullet to *Honest degradation limits* naming two faults the floor does *not* catch — a hand-edit that leaves the cursor **schema-valid but factually wrong** (the malformed-file refusal catches only schema-*invalid* files), and a GitHub auth/scope failure that **errors (401/403/404)** which a naive guard could **swallow as "empty / unprotected"** rather than treat as a read failure — so the partition states its bound instead of implying exhaustiveness (scorecard S7); **(2)** reword the **offline debt-count rendering** from the soft "possibly stale" hedge to a **reliance-blocking** string ("*…I couldn't refresh this, so it may be wrong; re-ground before you rely on it*") that leans on [boot](../spec/systems/lifecycle/boot.md)'s degraded-work consent gate — because a non-engineer acts on the number despite a mild hedge (scorecard S6b). **No design law changes:** the cursor's role, the malformed-file posture, and the field-set-as-build-spec-leaf are untouched; only the floor's stated bound and one rendered string move to current truth. `python3 lock.py --relock systems/cognitive/state/README.md --decision D-080`; ratified_by D-080. The reliance-blocking string is **cross-doc coupled** with [boot](../spec/systems/lifecycle/boot.md)'s identical rendering (re-litigated under D-084); both carry the same wording.

## Why

The [D-074](0074-sweep-the-stale-q1-references-resolved-by-d-066-d-068-re-loc.md)/[D-078](0078-citation-accuracy-re-litigation-repoint-stale-q4-references.md) precedent governs rigor: a locked living document must read as current truth, and an honesty/current-state correction that touches **no design surface** is re-litigated proportionately — `validate.py` (link + lock-fingerprint integrity) plus a current-state self-check and the remediation plan's own 5-lens cold audit — not a fresh four-lens per-system audit (which exists to probe design soundness before an irreversible *design* decision; there is none here). The scorecard found S7's degradation partition asserted an exhaustiveness it lacked, and S6b's "possibly stale" carried the entire never-mistake-stale-for-current trust load on a word people act past. Propagation per the matrix: [state](../spec/systems/cognitive/state.md) (re-locked end-state), this entry; [risks.md](../reference/risks.md) R1 verified still truthful (the read-failure-is-not-empty distinction is reinforced, not changed); no glossary/architecture/scenario change (the cursor's role and links are unchanged; the [scenarios/remediation-loop.md](../architecture.md#the-detect-to-remediate-loop) State count/pointer reference is unaffected).

## What we ruled out

**Route S6b to the Q15 empirical battery only** (rejected — the non-engineer-operator lens showed the wording is a *design* gap fixable now while the doc is open, not merely an empirical unknown; deferring leaves the trust string soft). **Legislate a guard implementation for the swallowed-error case** (rejected — that is a control-plane/build-spec leaf; State's law only names the bound it does not catch, per laws-not-leaves). **Run a full four-lens cold audit** (rejected as disproportionate — no design law changes, the [D-074](0074-sweep-the-stale-q1-references-resolved-by-d-066-d-068-re-loc.md)/[D-078](0078-citation-accuracy-re-litigation-repoint-stale-q4-references.md) reasoning).
