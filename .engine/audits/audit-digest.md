---
schema_version: 2
reviewed_at: 2026-09-13
content_modified_at: 2026-09-13
audited_sha: "6ba68352991710dc29496e0d108522d8ea2aeae2"
run_id: "34757946570/1"
fingerprint: sha256:d4169244ae35e262d14f5bca88e3505cb0ae97ed63eded417dd5ffe97ecc8eec
---

# Engine self-review — plain-language digest

## What I looked at
I ran cold, as if new to this project. This cycle I read: the 10 open engine-labelled issues (your full debt register, handed to me); the 7 soft validator nudges firing right now; the seeded concern checklist (`.engine/audits/concern-list.json`); the module manifests and validation schema under `.engine/`; ten settled spec criteria against the built machinery; and I did one cold read of a random artifact (`.engine/contracts/eADR-0041-build-coordinator-behavior.md`). Two inputs I could **not** review this run, and I'm flagging that rather than papering over it (below).

## What I couldn't review — say so plainly
- **Your saved memory was not reviewed.** No memory backup is set up for this review to read, so I have no way to check whether your saved decisions and preferences still hold together. This is not the same as "you have no saved memory" — I simply couldn't see it. To turn this on, you can ask me in an ordinary chat session to set up a memory backup; after that, each review can check your saved decisions for contradictions and staleness.
- **No earlier self-reviews to compare against.** The fetch of my prior reviews failed (GitHub returned a not-found reading an earlier digest). So everything below rests on a fresh check this run only — I have no history to corroborate recurrence, and I'm not inventing a trend I can't see.

## What I found

**Spec conformance — two genuine divergences, both already tracked.** I re-checked 10 of your 243 settled criteria this cycle (7 that changed recently, 3 spot-checked) — this is a prioritized sample, not a whole-spec pass, so treat the rest as unchecked this run.
- `dependency-discipline` and `migration-discipline` both diverge. Your settled specs say each module ships in **every** Engine (`distribution: required`) on a three-axis manifest — the split into distribution/applicability/activation your decision D-335 froze. But the built manifests (`.engine/modules/*/manifest.json`) still carry the old single-axis `status: "optional"`, and the manifest schema (`.engine/schemas/module.v1.json`) still offers only the single `status` enum. So the built encoding says "install opt-in" where the spec says "ships in every Engine." This reproduces on a fresh read and matches your open issues **#95** and **#96**. This is my judgement reading committed artifacts against your frozen wording — **no behavioural test was run**, and the product checkout isn't on this machine, so I read the manifests committed here as the as-built proxy. It's a prompt to look, not a proven defect.
- The other eight criteria I checked (route targets explicit, "installed means present," coordinator/PR/Build-Issue distinctness, deliberate mode entry, bounded model-invocable skills, plain operator surfaces, validation-dispatcher-in-core/rules-in-validators-core) all **meet** their wording in the built machinery. One criterion — dependency-discipline's "the laws live elsewhere; this module only delivers them" — I'm marking **unsure**: I confirmed the manifest provides only a policy plus checks and tooling, but I did not read the built policy prose closely enough to confirm it doesn't quietly restate the laws.

**The debt register (10 open) is honestly triageable.** Six of the ten are benign length-budget nudges on the engine's own files (#39, #38, #71, #97, #98, #99) — they'll auto-close when trimmed and never block anything. Two are the spec divergences above (#95, #96). That leaves two worth your eye:
- **#80 — the full self-test blows the Codex boot-briefing budget.** The never-shed Codex briefing core is ~10,839 characters against a 9,700 ceiling, so the status dashboard gets trimmed at the real platform cap. This is a real engine fault in machinery, not a nudge.
- **#54 — the engine-template relicense (plain Apache-2.0, reversing D-295) isn't yet recorded in your design corpus.** This is live, project-owned work: `docs/adr/0295`, `0301`, `0302` still describe the dropped Commons Clause posture. This is your own decision record, not machinery — it's a real, reconcilable follow-up.

**Soft nudges firing now — all recurring, all benign, split by lane.** The six length-budget nudges (eADR-0041 at 167 lines, boot-session-start at 225, codex-settings at 162, engine-arrival at 128, engine-upgrade at 144, external-contribution-submit at 121) are all on **engine machinery** — files the engine ships and overlays wholesale on every update. Trimming them here would not stick: the next engine update overwrites them and wipes the local edit, so the durable fix belongs upstream in the engine-template project these files came from (or you leave them — they're only nudges). The seventh nudge — "the scheduled self-review hasn't run yet" — is **local setup**, and it's a genuine signal: this weekly self-review isn't running on a schedule yet, so drift like the above only surfaces when you ask for it by hand.

**Cold read — `eADR-0041-build-coordinator-behavior.md`.** It reads as durable fact, not build-status narration: it describes what the coordinator does, and its amendments record deployed fixes and the bugs they guard (durable facts, not "not yet built"). Its register is dense engineer-to-engineer prose — "defang," "close-linkage," "receipt," "lens" — but this is an internal contract under `.engine/contracts/`, not operator-facing, and every term is used precisely and consistently, so I read it as appropriate rather than as jargon to flag. No drift or stale-sibling finding here (beyond the length nudge already tracked as #97).

**Never-firing checks:** clean read — every one of the engine's file-scoped checks matches at least one file in this repo. Nothing to raise.

**Nothing to retire this cycle — and I scrutinized that claim.** The concern checklist's six rows each still catch a drift the generic read would miss and none is mechanizable, so none is itself a retire-candidate. I found no orphaned local surface — but I want to be honest that my retirement scan this run was limited: I read the checklist and the one cold-read target, not an exhaustive sweep of every project-authored operation and skill for orphans. Setting up the scheduled self-review (above) is what makes that deeper probing routine.

## What I recommend
- **Reconcile the two module manifests to their settled specs (#95, #96)** — separate `status` into the three axes and set `distribution: required`, or, if you now judge the single-axis "optional" encoding correct, re-settle the spec wording. Either is ordinary build work; the merge is the decision. This is product-build work and the product checkout isn't set on this machine yet, so it can't be done from here until you point me at it. **Cost of ignoring:** your build stays out of step with your own frozen design on how these two modules are distributed. **Keep-it path:** close #95/#96 if you read the current encoding as correct — you know your product.
- **Set up a memory backup** so future reviews can actually check your saved decisions. **Cost of ignoring:** I stay blind to whether your saved beliefs contradict each other or have gone stale. This is a decline-able capability, not an alarm.
- **Set up the scheduled self-review.** **Cost of ignoring:** drift like the manifest divergence only surfaces when you ask by hand, never on its own. Decline-able.
- **Consider #80 (self-test budget) upstream** — it's an engine-machinery fault; a local fix wouldn't survive the next update, so the durable fix belongs in the engine-template project. I can draft that upstream report on your say-so; I never file it myself. Ignoring it stays fair — it trims the status dashboard, it doesn't break the merge gate.
- **Write the relicense ADR (#54)** in this repo's `docs/adr/` when you're ready — this one is yours to fix locally and stays accurate to do. **Cost of ignoring:** your design corpus keeps describing a Commons Clause posture that no longer exists.
- The six length nudges: **leave or raise upstream** — a local trim won't survive an engine update. Your call; none blocks anything.

One note carried over from grounding, since it's governance-relevant and you can't see what the engine handed me: I could **not** verify your safety gate this run (no GitHub access from here), so don't assume `main` is protected — confirm before merging anything important.

## Memory recall completeness

Memory recall reaches both the summaries of past sessions and the word-for-word conversation behind them, so something said once and never summarised can be found — not only read back if you already know which session to look in. Nothing was forgotten or deleted. What comes back is the conversation as it was captured, and it was never cleaned of things like passwords or personal details, so treat a recalled answer as unreviewed text and ask to see the exact wording of anything it rests on.