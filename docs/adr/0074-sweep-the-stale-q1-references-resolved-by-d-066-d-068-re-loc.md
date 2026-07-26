---
status: accepted
engine_record: true
---

# Sweep the stale `Q1` references resolved by D-066/D-068 (re-lock `module-system` and `agents`)

*Decided 2026-05-26 in the design workspace.*

## The decision

Correct six stale `[Q1]` references — citing the v1 module/suite roster as an *open* question when [D-066](0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) (lens roster) and [D-068](0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) (optional-module roster) had already **resolved Q1** (it no longer exists in [open-questions.md](../reference/open-questions.md)). The fix repoints each citation to the resolving decision and, in [module-system](../spec/systems/grammar/module-system.md), **deletes its now-empty `## Open questions` section** (its sole entry — "the final module set" — is resolved; the deletion mandate forbids leaving a resolved question standing). Two of the four docs are locked, so the edit runs the **litigation-alarm protocol (operator-approved)**: [module-system](../spec/systems/grammar/module-system.md) ([D-058](0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md)) and [agents](../spec/systems/surfaces/agents.md) ([D-057](0057-lock-the-agents-surface-wave-1-four-settled-design-forks.md)) are re-locked; the `designed` [qa-review](../spec/modules/qa-review.md) and [design-review](../spec/modules/design-review.md) are free reconciliations. `python3 lock.py --relock systems/grammar/module-system/README.md --decision D-074` and `python3 lock.py --relock systems/surfaces/agents/README.md --decision D-074`; ratified_by D-074.

## Why

A pre-existing propagation debt: [D-057](0057-lock-the-agents-surface-wave-1-four-settled-design-forks.md)/[D-058](0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md) locked agents and module-system *before* [D-066](0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md)/[D-068](0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) resolved Q1, so the resolution never swept their references, leaving locked docs asserting a resolved question is open — a current-state-accuracy violation of the four authoring rules, surfaced during the [D-073](0073-lock-build-orchestration-wave-3-terminal-and-re-litigate-con.md) propagation sweep. The change is **citation-accuracy only and alters no design law** (the manifest grammar, persona template, and every locked invariant are untouched; only "[Q1] (open)" → the resolving-decision pointer, plus the empty Open-questions section's deletion). On that basis the full four-lens cold-session design audit ([D-018](0018-cold-session-design-audit-required-before-any-lock.md)) was **deliberately scoped out** as disproportionate — the audit exists to probe design soundness before an irreversible *design* decision, and there is no design surface here for a lens to probe; `validate.py` (link integrity + lock fingerprints) plus a current-state self-check are the proportionate rigor. No content beyond the citations changed; the relock fingerprints the corrected bodies.

## What we ruled out

Leave the stale references (rejected — locked living documents must read as current-state truth; citing a resolved question as open misleads a cold reader and validates only because the linked file still exists). Fix only the two `designed` docs and leave the locked ones stale (rejected — the locked docs carry four of the six references and are the most authoritative; selective correction would leave the worse offenders). Run a full four-lens cold audit on the sweep (rejected as disproportionate — no design law changes; running four agents on a citation fix is ceremony, R6, and the audit's purpose does not apply). Keep an empty `## Open questions` section in module-system as a placeholder (rejected — the deletion mandate: delete obsolete content, never leave a resolved question or a transitional marker).
