---
schema_version: 2
reviewed_at: 2026-09-20
content_modified_at: 2026-09-20
audited_sha: "6ba68352991710dc29496e0d108522d8ea2aeae2"
run_id: "35510637589/1"
fingerprint: sha256:63feae6c25e105370b3833cc37f43ba46ffaac874aac7f52338d90340d9631a1
---

⚠ Project status: couldn't verify the safety gate — I couldn't reach GitHub to confirm `main` is protected, so don't assume it is; confirm before merging anything important.

# Engine self-review

## What I looked at
I ran this cold, against the committed repository as it stands today. This project is an engine-mechanic — the thing it builds is `StarshipSuperjam/engine-template` — and no product checkout is wired up on this machine, so everything below is a read of committed state, never a behavioural test. I went through: your open engine-labelled issues (the 12 you have now, handed to me in full), the soft nudges firing right now, the engine's own checks, four settled spec criteria against the code built for them, and the seeded checklist I work each run. I also did one cold read of a document picked to test whether its cross-references still hold.

## Saved memory — not reviewed this run
I could not review your saved decisions and notes this cycle: **no memory backup is set up for this review to read**, so your saved memory was simply not visible to me. Treat it as unreviewed — not as empty. If you'd like this covered in future runs, you can ask me in an ordinary session to set up a memory backup; it's a one-time thing and entirely your call to skip.

## No earlier reviews to compare against
The earlier self-reviews couldn't be read this run (GitHub returned a not-found on the prior digest), so I have **no history to corroborate against**. Everything below rests only on what I could check now — I'm not claiming any trend over time, in either direction.

## What I found

**The debt register (12 open issues) is honestly triageable.** Nothing there is drowning you. But six of the twelve are the same kind of thing — engine machinery files that have grown a little past their length budget (`boot-session-start`, `engine-arrival`, `engine-upgrade`, `codex-settings`, `external-contribution-submit`, and the `eADR-0041` contract). These are the engine's *own* files, not yours. Trimming them here wouldn't last: the next engine update overwrites those files wholesale, so a local edit is wiped. The durable fix lives upstream in the engine-template project these files come from — or you leave them, since each is only a nudge and blocks nothing. Either is a fair choice.

**Two health flags worth eyeing together.** #110 (the `audit` check on `main` keeps failing) and #80 (the full self-test overruns the Codex boot-briefing budget) look like they may share a root cause — the boot briefing being trimmed at the platform cap. I can't confirm the linkage from committed state alone, but if you chase one it's worth checking whether it clears the other. Both are engine-machinery health, so the real fix arrives as an engine update, not a change here. #111 (session conversations failing to save to memory) is a standing machinery flag of the same sort — nothing in your project is lost, but those conversations won't be recallable later, and the fix comes with an engine update.

**The conformance issues #95 and #96 still reproduce.** I checked the built manifests myself: `dependency-discipline`'s manifest still declares `status: optional` on the old single-field shape, and the module schema still offers only that single `status` field — neither carries the three-way distribution/applicability/activation shape the settled specs describe. So those two "may have drifted" flags are genuinely live, not stale. Reconciling them is ordinary build work whose merge is the decision; declining is fair if you read the wording as the thing that should move instead.

**#54 (record the license reversal in your design corpus) is a legitimate pending follow-up** — a decision record still owed, not something that's gone stale.

**The soft nudges firing now line up exactly with issues you already track.** Six of the seven are the length-budget nudges above — already captured as issues, all machinery, durable fix upstream only. The seventh is different and local: a notice that the **scheduled self-review isn't set up yet**. That's a benign capability disclosure, not a problem — this review is running on demand right now; setting up the schedule just lets it run on its own cadence. Enable it or leave it; nothing breaks either way.

**The engine's own checks are all in use** — every file-scoped check matches at least one file in this repo, so there's nothing dead-weight to flag there this run.

## Product-spec conformance — a forward read of 4 of 243 criteria
This is my judgement reading the built code against your frozen wording, with **no behavioural test run** — a prompt to look, not a proven defect. I re-checked 4 settled criteria this cycle (one recently changed, three spot-checked) and did **not** re-verify the other 239 — so this is not a clean whole-spec pass.

All four **meet** on this forward read:
- **Operating modes — "entry is a deliberate operator act for both write stances":** the two Build-entry paths are wired as written (the Explore write-gate on `PreToolUse`, the plan-acceptance trigger on `PostToolUse`), and the Codex side correctly omits the plan-acceptance mirror exactly as the spec's sanctioned provider-exception says it should. I verified the wiring, not the runtime behaviour or the routine isolation-gate internals.
- **core — "dispatcher + closed kinds in core, rule corpus in validators-core":** core owns the validation tooling and only its own two security-floor checks; the ~70-file rule corpus rides `validators-core`. The partition holds.
- **dependency-discipline — "the laws are the systems', the delivery is this module":** the manifest delivers a policy, two checks, and read-only tooling — it doesn't re-legislate.
- **dependency-discipline — "owns discipline, not the floor":** `dependabot.yml` appears in no `provides` and the module wires nothing to edit it.

One honest note: while confirming these I saw the same `status: optional` / single-axis manifest shape that issues #95/#96 already flag — but that bears on a *different* criterion than the four I was asked to check, so I've left it where it's already tracked rather than raise it forward.

## What I recommend
Nothing here demands action. In priority order if you want to act: reconcile the two live conformance flags (#95/#96) or re-settle their wording; look at #110 and #80 together; and, if you want this review to run on its own schedule and your saved memory covered next time, ask me to set up the scheduled self-review and a memory backup. Everything else is either machinery best raised upstream or a benign disclosure you can leave.

## Nothing to retire this cycle — and why I trust that
I looked for one honest retire-candidate and didn't find one, so let me scrutinise that rather than assert it. The overwhelming majority of this repo's engine surface is machinery owned by module manifests (core, validators-core, and the rest) — that's overlaid on every update and can't be locally retired, so it's out of scope by construction. The genuinely local, preserved-across-update state I *can* act on is your design corpus (specs and decision records) and the seeded checklist. The checklist I re-read entry by entry: each still catches a drift the generic read would miss (saved-memory contradictions, non-reproducing debt, module fit, orphaned local surfaces, upstream-blocked stop-gaps, recurring soft nudges) and none is reducible to a mechanical check — so none has become dead weight. And my cold read this run was `modes.md`: dense maintainer design prose, but its register fits its reader, and its "designed, not yet built" passages each carry a live upstream tracking pointer — accurate design records, not stale drift. So the "nothing to retire" is a checked conclusion, not a shrug.

## Memory recall completeness

Memory recall reaches both the summaries of past sessions and the word-for-word conversation behind them, so something said once and never summarised can be found — not only read back if you already know which session to look in. Nothing was forgotten or deleted. What comes back is the conversation as it was captured, and it was never cleaned of things like passwords or personal details, so treat a recalled answer as unreviewed text and ask to see the exact wording of anything it rests on.