---
status: accepted
engine_record: true
---

# Justified re-litigation: name the routine-entry command `/engine-routine` in `modes` + `build-orchestration` (the firing's payload)

*Decided 2026-05-27 in the design workspace.*

## The decision

Under explicit operator approval, re-litigate two locked docs to name the concrete Routine-stance activation that [D-087](0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md) added to the skill roster. [modes](../spec/systems/lifecycle/modes.md) and [build-orchestration](../spec/systems/lifecycle/build-orchestration.md) described Routine entry only as "a Local Desktop routine fires" — incomplete, because firing launches a *prompt* and the activation is an embedded command (validated against the live scheduled routines, [D-087](0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md)). **(modes)** names **`/engine-routine`** as the entry; frames its **authority** as the operator-configured schedule + the frozen scope-locked build Issue — a *pre-authored* operator act, not the silent/by-default self-election the stance model forbids (the command is `operator-typed`, invoked by its *presence* in the scheduled prompt via the slash-command parser path, never by model election); generalizes the entry design-commitment to **both** write stances; and adds the routine-verb wording [build-spec leaf](../spec/systems/lifecycle/modes.md) (the name is pinned). **(build-orchestration)** names `/engine-routine` in the routine arm and requires an **operator-visible durable misfire artifact** (an Issue, not a silent `exit 0`) plus a **first-fire echo** of the locked-on build Issue, so a mis-aim surfaces on the first cycle. Both docs re-locked under this decision (`lock.py --relock`). Propagation: [deviations/README.md](../reference/prototype-deviations.md) improvements **row #12** updated to name the restored routine-entry command; [scenarios/routine-session.md](../architecture.md#routine-session) updated so the firing carries `/engine-routine` and the misfire is operator-visible.

## Why

Justified re-litigation, not lock-weakening: the locked text was genuinely incomplete and the design requires naming the trigger; the lock stops silent drift, not justified edits. The change touches the entry *law* (it adds Routine's concrete entry vehicle and authority, parallel to Build's verb), so it is a true re-litigation — hence both docs re-lock, not a leaf amendment. A four-lens cold-context audit (adversarial / architect / non-engineer-operator / technical, ground-truthed against the live files) ran against the plan; its blocking findings — route the command to an owned `operation` not a design-doc section; frame entry authority as the schedule + frozen scope-lock rather than a model-set "stance signal"; an operator-visible misfire — are discharged in this entry and [D-087](0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md).

## What we ruled out

Leave the docs saying only "a routine firing" and treat `/engine-routine` purely as a build-spec leaf (rejected — the firing-only text is incomplete/misleading about how the stance activates; a reader cannot see the firing carries a required command). Keep the live silent `exit 0` on misfire (rejected — the operator is away; a silent no-op fails the "forgotten setup → surface loudly" rubric, [goals-and-quality](../reference/goals-and-quality.md)). Frame `/engine-routine` as "setting a stance signal" the model flips (rejected — mischaracterizes the mechanism; the authority is the schedule + frozen scope-lock, and the durable marker is target-contract-driven, per the live evidence).

## Further record

### D-038 follow-up

the routine-entry name-drop this restores lived in the [deviations/README.md](../reference/prototype-deviations.md) **improvements row #12** ("routine by a Local Desktop routine"), **not** the [D-038](0038-session-lifecycle-re-founded-on-native-substrates.md) log entry (which dropped only `/start-engine`); this entry corrects that row. Dropping the name while keeping "firing" was the gap — the firing's payload was always required.

### Build-spec cautions (bind the future build pass, change no locked law; evidenced in the live `routine-mode-operations.md`)

routines run a **Default/Auto permission preset**, never plan-mode (which deadlocks on `ExitPlanMode`); default-branch push must route through a **push wrapper** (the unattended Default-Branch-Push gate denies raw `git push`); **single-flight** is the Desktop scheduler's skip-while-running plus a lockfile + boot-freshness + loser-recovery; the permission mode is **not introspectable** at runtime, so the operator is the gate.

### Out of scope, confirmed deferred

the [D-086](0086-cognitive-foundations-as-required-packages-reconciliation-me.md)-flagged stale `default-on` `Module` status class in [glossary.md](../reference/glossary.md) (and [module-system](../spec/systems/grammar/module-system.md)) stays deferred to its own pass — folding it requires a coupled locked `module-system` re-lock unrelated to this pass's blast radius; the glossary `Skill`/`Command` terms were verified consistent with the resolved roster and need no edit.
