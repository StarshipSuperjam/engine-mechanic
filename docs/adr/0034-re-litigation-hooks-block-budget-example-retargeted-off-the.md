---
status: accepted
engine_record: true
---

# Re-litigation: hooks block-budget example retargeted off the dissolved eager-claim

*Decided 2026-05-24 in the design workspace.*

## The decision

Under explicit operator approval, re-litigate the locked [hooks](../spec/systems/infrastructure/hooks.md) foundation ([D-022](0022-hooks-locked-as-foundation-11-as-laws-not-leaves.md), last re-locked [D-032](0032-re-litigation-bind-userpromptsubmit-to-the-orientation-scent.md)) to remove its two references to the eager-claim system, which the session-lifecycle redesign dissolves into the draft PR. The block-budget law's illustrative member-to-come drops the eager-claim gate and names instead the **explore write-gate** — the exploration stance's `PreToolUse` block, which honors the fail-open law (a strong default, not an absolute wall; the durable backstop stays the [control-plane](../spec/systems/infrastructure/control-plane.md) merge gate) — registered by [modes](../spec/systems/lifecycle/modes.md) as that stance is designed; the mode-awareness example "a claim-gate is build-only" becomes "the explore write-gate is exploration-only." Hooks names only budget-law facts (event-class, fail-open, merge backstop, mode); the gate's deny-list and mechanism are modes' leaf to author, so "hooks names no invariants itself" still holds. Re-locked under this decision (`lock.py --relock`).

## Why

The redesign dissolves eager-claim, so the locked hooks doc's live links to it would dangle once the system is deleted. The reconciliation is batched into this dedicated re-lock session rather than forcing a second hooks re-lock later. The example points at the explore write-gate because it is the genuine member-to-come and best illustrates the doc's additive-registration law; the forward-neutral "registers with modes as that stance is designed" keeps the statement true both now (modes already frames exploration as the no-PR/no-landing stance) and after modes is authored, so no second re-lock is needed. The full four-lens cold-session audit ran on the edited doc (hooks-alone + combined); its blocking finding — that an earlier draft let *hooks* enumerate the gate's deny-mechanics, contradicting "names no invariants itself" — was resolved by trimming the clause to budget-law facts and deferring the deny-list to modes. Operator-facing concerns (how an explore-gate deny is surfaced; how the operator leaves exploration) are modes/boot design, logged for the modes rewrite. The "reconcile modes before re-locking hooks" objection was rejected with rationale: the operator directed re-locks-first sequencing precisely so the locked docs stop referencing the dissolving systems before deletion, and the mechanics-deferred phrasing keeps hooks truthful without front-running modes.

## What we ruled out

Leave the eager-claim references in place (rejected — they dangle the moment the system is deleted; validate.py would fail). Let hooks specify the gate's deny-list and mechanism (rejected — that is modes' leaf; it would falsify the locked "hooks names no invariants itself" clause). Assert the gate as an already-registered member (rejected — over-claims against D-022's "register when designed" discipline and forward-references an unauthored modes rewrite). Over-claim the gate as an absolute wall (rejected — violates fail-open; it is a strong default backstopped by the merge gate). Defer the reconciliation to the modes rewrite (rejected — forces a second hooks fingerprint change and re-lock).
