---
schema_version: 2
reviewed_at: 2026-08-23
content_modified_at: 2026-08-23
audited_sha: "157f033db3ffcbb920556927ba9dc5544f3cf075"
run_id: "32626588488/1"
fingerprint: sha256:68d039e5bfe61b12ba36e161143b6eb1e7b79b81cd3a3ef6f0e8c5c5044059b2
---

## Engine self-review — digest

Here's what I looked at this run, what I found, and what I'd do about each. I ran cold, as the audit is meant to — and a few things about *this* run's inputs shape what I can and can't stand behind, so I'll be plain about those as I go.

### What I couldn't review this run (gaps, stated honestly)
- **Your saved memory — not reviewed.** No off-computer backup is set up for this review to read, so I could not check your saved decisions and notes for contradictions or staleness this cycle. This isn't "you have no saved memory" — it's that I had no way to see it from here. To turn this on, you can ask me (in an ordinary chat session) to set up a memory backup; after that, these reviews can check it.
- **No earlier self-reviews to compare against.** The fetch of my own prior reviews failed (GitHub returned a not-found). So everything below rests only on fresh checks I ran this cycle — I'm not claiming any trend over time, because I genuinely can't see one this run.
- **Branch protection** I deliberately don't check — that's settled mechanically elsewhere on every run. (Separately, this session couldn't reach GitHub at all, which is why I flagged the safety gate up top.)

### Your debt register (6 open engine-health issues) — all still honest, nothing over-full
I read the complete open set. Six items, all engine-opened health flags, and each still reproduces:
- **#94 — memory capture keeps failing.** Session conversations aren't being saved to memory. Still live (the live memory helper is also off this session). This is engine machinery reacting to a runtime storage change; the real fix comes as an engine update, not a local edit.
- **#80 — the full self-test trips two boot-briefing size limits.** The Codex briefing core is over its character ceiling. Machinery — a durable fix belongs upstream in the engine-template project this engine came from; editing the file here would be wiped on the next engine update.
- **#71 / #39 / #38 — three engine files over their length budgets** (`boot-session-start.md`, `engine-upgrade.md`, `engine-arrival.md`). All machinery, same upstream-fix story. One note: **`boot-session-start.md` has grown *worse*** — #71 recorded 210 lines; the live nudge now reports 225 against a 200 line budget. Worth mentioning to whoever raises these upstream, because it's drifting the wrong way, and it's the same file implicated in #80.
- **#54 — record the engine-template relicense in your design records.** This one is genuinely *yours* to act on locally: it asks for a new decision record in this repo's `docs/adr/` capturing that the upstream template dropped its Commons Clause (reversing D-295, mooting D-301's hedge, re-anchoring D-302). This is an ordinary Build PR when you want it. Still valid, still un-done.

The register is honestly triageable — six items is not triage-pressure, and none reads as stale-but-lingering.

### Nudges firing right now (the non-blocking kind that usually vanish into a log)
Seven are firing. Most are the length-budget kind and are **machinery** — trimming them in this repo won't stick, because the next engine update overlays these files wholesale; the lasting fix is upstream in the engine-template project. Three of these aren't yet tracked as issues the way #71/#38/#39 are: **`eADR-0041-build-coordinator-behavior.md` (167/120)**, **`codex-settings.md` (162/120)**, and **`external-contribution-submit.md` (121/120, barely over)**. Ignoring any of them stays a fair choice — they never block a merge; you'd just be declining to shorten a file a fresh session has to read.

One nudge is different and worth acting on: **the scheduled self-review hasn't been set up**, so this health check isn't running on its own — you're getting it only because it was invoked. If you want the engine checking its own health on a cadence, ask me to set up the scheduled self-review; once it runs the notice clears. Cost of leaving it: these reviews only happen when someone triggers them.

### The engine's own checks
Every one of the engine's file-scoped checks currently matches at least one file in this repo — a clean read, nothing dead-weight to raise upstream on that front this cycle.

### The one random artifact I read cold
I pulled `.engine/docs/getting-started.md` and read it with no context. It's healthy: plain language throughout, addresses you as a capable adult without talking down, no internal jargon leaking, and its references (`/engine-help`, `/engine-parts`, `/engine-design`, the `guardrail-ack` label) all resolve to things that exist. No sibling named that's gone. No finding.

### Anything to retire this cycle? — no nomination, and here's my scrutiny of that
I found no honest retire-candidate this run. Your seeded checklist of audit concerns (six entries) each still catches a distinct drift a mechanical check can't — saved memory, the debt register, module fit, local surfaces, upstream-blocked stop-gaps, and these soft nudges — so none of *those* is dead weight. But I want to be straight about the limit of that "nothing to retire": I did **not** do a deep hunt this cycle for an orphaned local surface — an abandoned proposed contract, a local operation only one skill really uses, a skill nothing routes to. So read my "nothing to retire" as "nothing surfaced in a prioritized pass," not "I swept every corner."

### Product-spec conformance — one divergence to look at
Your project has a settled `docs/spec/`. **Coverage, plainly: I did a prioritized structural sweep across the whole 243-criterion corpus — not a deep, behavioural verification of each one.** I ran no behavioural checks; this is my judgement reading committed artifacts against your frozen wording. Also worth knowing: the product this engine builds (engine-template) isn't checked out on this machine, so what I read against the spec is this repo's own committed machinery — which bounds how far I can push a "built code" claim.

Within that, one divergence is well-corroborated (I confirmed it twice, including a direct read of the manifest schema and the D-335 decision record):

- **Five modules the spec now calls "required, ships in every Engine" are still encoded as "optional" in the manifests.** Decision **D-335** split the old single `status` field into distribution/applicability/activation axes and promoted `dependency-discipline`, `migration-discipline`, `product-design`, `design-review`, and `qa-review` to *required* distribution — and the spec documents were rewritten to say so. But the module manifests still carry the old `status: optional` field, and the manifest schema still lists only the old single-axis enum. So the spec says "not an install opt-in, ships in every Engine," while the encoding still says "installed only if chosen." That's a real gap between the settled wording and the built encoding. This is a **reconcile** item — an ordinary Build PR migrates the manifests and schema to match D-335 — and, as always, adjudicated when you review it, not a proven defect.

A handful of other criteria I could only mark **unsure** rather than clear (an audit-library cron-workflow ownership gap the spec already acknowledges upstream as #798; a couple of behavioural properties that are operator-verified by design; enforcement logic inside checks I didn't execute). I'm not calling those divergences — just flagging that I didn't fully close them.

### What I'd recommend
1. **The clear, actionable local one:** decide whether to reconcile the D-335 manifest/schema encoding (spec says required, manifest says optional) — a Build PR when you're ready.
2. **#54** — author the relicense decision record when it suits you; it's local and un-done.
3. **Turn on the scheduled self-review** if you want this to run on its own, and **set up a memory backup** if you'd like these reviews to actually check your saved decisions.
4. **The length-budget and boot-briefing items (#80, #71/#39/#38, plus the three untracked overages) are machinery** — if you want them fixed durably, they go upstream to the engine-template project, not here; leaving them is a fair choice since none blocks anything. Flag boot-session-start's growth when you do.

Nothing here changes anything on its own — every item is yours to act on or decline.

## Memory recall completeness

Memory recall reaches both the summaries of past sessions and the word-for-word conversation behind them, so something said once and never summarised can be found — not only read back if you already know which session to look in. Nothing was forgotten or deleted. What comes back is the conversation as it was captured, and it was never cleaned of things like passwords or personal details, so treat a recalled answer as unreviewed text and ask to see the exact wording of anything it rests on.