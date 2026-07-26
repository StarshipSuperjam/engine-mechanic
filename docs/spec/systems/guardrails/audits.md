---
status: draft
---

# Audits

*Settled in the design workspace on 2026-07-11, ratified by [decision 0297](../../../adr/0297-resolve-re-lock-audits-installs-the-standing-conditional-pro.md).*

## Summary

Answers **"is the running Engine still *fit*, or has it silently accumulated cruft no rule can catch?"** —
the **judgment** rung of the ladder above [validation](validation.md) (mechanical, per-event) and
[telemetry](telemetry.md) (mechanical, aggregate). Where a check asks *does this match its declared
shape* and telemetry asks *are the signals trending bad*, an audit asks *does this still earn its keep, or
has the deployed instance drifted past it*. That question cannot be encoded as a check, so it is performed by
an AI under an adversarial posture, on a cadence.

Audits is **Engine self-monitoring** ([D-009](../../../adr/0009-telemetry-is-a-remediation-loop-not-self-healing.md), Risk [R3](../../../reference/risks.md)) — and,
**where the operator has locked a `docs/spec/`**, the standing check that the **product still conforms to that
locked spec**. It reviews the Engine's own operational state in the **deployed repo it runs in**; it does
**not** judge the product's *quality* — that is the operator's domain — only the product's **conformance to the
spec the operator themselves froze** (the standing cadence of the traveling
[conformance-enforcement floor](../../../reference/glossary.md), conditional on a `locked` `docs/spec/` and never biting
on scope the operator leaves open — [§20](../../../principles.md), [D-296](../../../adr/0296-litigate-engine-template-427-residual-three-l1-l2-l3-audits.md)). It is the
deployed Engine's periodic **anti-entropy tune-up** — it produces **findings + recommendations** and never
remediates autonomously.

## Behavior

### The deployed-repo frame — what an audit can and cannot act on

The audit runs inside a **deployed** repo (one generated from the template, or brownfield-overlaid), and that
fixes what it may recommend. A deployed repo holds two kinds of Engine surface, and the audit treats them
differently:

- **Template-owned machinery** — the foundations, core surfaces, validators, hooks, and the grammar. These
  are **overlaid** (replaced wholesale) on every engine update, so a local edit to them is wiped by the next
  overlay, and a core component cannot be *retired* without breaking updates and the systems integrated with
  it. The audit therefore **never recommends retiring or locally patching machinery**. A genuine machinery
  bug or mis-fit takes the **escalate-upstream** disposition (below).
- **Accumulated local state** — the per-project churn the deployed Engine produces over its life: experiential
  [memory](../cognitive/memory.md), engine-labeled debt issues, the operator's optional-module
  selection, and project-authored surfaces (contracts, policies, local skills/agents/operations). This is
  **preserved** across overlays and is **locally remediable**, so it is where the audit's retirement-default
  posture applies.

The two are told apart **mechanically, not by persona judgment**: an artifact is machinery iff it belongs to
an installed package's manifest `provides` set — the same file-precise ownership that drives
[CODEOWNERS](../infrastructure/repository-topology.md) — and everything else in the engine corners
is project-authored local state. The audit consults this provenance **before** nominating, so an
engine-shipped policy, skill, or agent is **never** a local retire-candidate even when it looks quiet: a
shipped artifact that appears dead is an *escalate-upstream* signal ("a core capability seems unused — the
template may be carrying dead weight"), not a local retirement the overlay would only restore.

The committed [operator policy-override](../../../reference/glossary.md) is a **third case** — *operator config*, in no
`provides` yet not churn: it is **affirmatively-owned**, the operator's deliberate tuning of a shipped policy.
So it is **locally remediable but never retirement-default**: the audit may flag a *stale* override — a key the
shipped policy no longer carries, or one now equal to the default — for the operator to re-tune or clear, and
**never nominates the operator's deliberate setting for deletion**, exactly as it never retires a shipped
policy. A *freshly* stale key is caught at the merge by [validation](validation.md); the audit's
role is to re-surface one that has **lingered** unaddressed ([D-167](../../../adr/0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md)).

This frame is the whole point: the audit keeps the *running* engine lean and honest within its project, and
routes anything systemic to the people who own the template. (Reviewing the template's own architecture — "is
this surface earning its place across all projects" — is **maintainer work** done ad hoc against the template
repo, and is deliberately **not** shipped to deployed repos. That foreclosure is about the *template's engine
architecture*, unactionable where machinery is overlaid; it is **distinct from** the product-conformance
concern below, which reviews the *product* against the operator's own locked spec and is locally actionable.)

### Product conformance to the operator's locked spec — the standing floor

Distinct from the Engine self-hygiene above, and **conditional on the operator having locked a `docs/spec/`**,
the audit also asks: **does the product still match the spec the operator froze?** This is the **standing
cadence** of the [conformance-enforcement floor](../../../reference/glossary.md) that
[build-orchestration](../lifecycle/build-orchestration.md) runs **per-merge**, run instead on the
audit's cron to catch what an introduction-time gate structurally cannot: conformance that **drifts after
merge** — a re-litigated spec row whose digest moves, small divergences that each passed their own PR but
accumulate, code written before its criterion was locked. It reads
[product-design](../../modules/product-design.md)'s [spec-obligation matrix](../../../reference/glossary.md)
(the coverage denominator) and the `locked` `docs/spec/` as a **stable channel by presence**
([§16](../../../principles.md)/[§14](../../../principles.md)) — adding **no** `depends` on the optional
product-design module, so audits stays required core.

**It runs the floor's two AI-judgment legs, not its third.** The floor is a trio — the matrix, an adversarial
divergence read, and the operator-run **demonstration harness** ([glossary](../../../reference/glossary.md)). The cron
sweep re-runs only the first two; the demonstration harness — the [§17](../../../principles.md) evidence that
routes around AI — is **not** re-run here, staying the operator-runnable behavioral correlate at the reconcile
merge. So a standing conformance finding is the Engine's **AI judgment** (matrix coverage plus an adversarial
read of the built code against the frozen criterion), carrying **no behavioral correlate at cron cadence** and
the irreducible AI-on-AI residual ([R16](../../../reference/risks.md) a/b); its [artifact warrant](../../../reference/glossary.md)
says exactly that, and the operator adjudicates it at the reconcile PR (where the harness, if present, is the
behavioral check). Naming it "the floor" marks the shared denominator and posture, never a claim that the whole
trio re-runs.

**The adversarial read is the audit persona's own, and it is the forward arm only.** The persona carries the
divergence-hunt posture **itself** (its standing adversarial law 1 below), never by invoking
[qa-review](../../modules/qa-review.md)'s `divergence-hunter` lens — so the standing adversarial leg
is present whenever the matrix and locked spec are committed, **regardless of whether qa-review is installed**,
and adds no qa-review `depends`. It runs the **forward** direction only — *does each `locked` criterion's built
code still meet it?* — over the whole committed tree, not a diff. The lens's **diff-introduced over-build** arm
([qa-review](../../modules/qa-review.md), [D-292](../../../adr/0292-resolve-re-lock-qa-review-the-8-pair-split-across-two-lenses.md)) is **inapplicable**: it
is defined against a **PR diff**, which a standing cron has none of, so the sweep never renders a whole-repo
"code that traces to no `locked` row" verdict — the false-positive storm [§20](../../../principles.md)/D-292
foreclosed stays foreclosed (whole-repo dead-code remains `technical-integrity`'s referent-free concern).

**It is prioritized, not exhaustive.** Hunting every `locked` row against the whole tree each cron would not
fit a real product's run budget, so the sweep hunts the rows the matrix **stale-flags** (a moved digest — the
drift class above) plus a **sample** of stable rows (the law-3 cold-target discipline: `≥1` a cycle, digest
history directing *where* to look, persisting no count), and the digest **discloses the partial coverage** —
what it re-hunted this cycle and what it did not — never implying a clean whole-spec pass it did not perform.

Three properties bound it, and keep it from becoming the product-*quality* review the
[§13](../../../principles.md) wall forbids:

- **Conformance, not quality.** It checks the product against the operator's **own locked spec**, never against
  the Engine's taste — the Engine reviewing the build it produced is the contributor doing its job
  ([§13](../../../principles.md) governs dependency *direction*, not whether the Engine may review its own
  output). What *counts* as met is the operator's frozen criterion, not an audit opinion.
- **Conditional and per-locked-row.** It bites only on criteria whose `docs/spec/` row is `locked`. **With no
  locked spec — the default, and every repo without the product-design module — there is simply nothing here to
  check: the sweep is silent, an inapplicable capability, never a recurring notice that reads as pressure to
  freeze a spec** (a staged or MVP product is a first-class operator choice, [§20](../../../principles.md)).
  Degradation is the *distinct* case — a spec **is** locked but its matrix is absent or unreadable — and
  **that** the digest names as an actionable gap with the one step that closes it, never a silent skip.
- **Report-only, divergence-findings, reconcile lane.** The retirement-default posture (below) governs *local
  state* only; a conformance finding is a **divergence from the locked spec**, never a retire-candidate. It is
  an **engine-labeled audit observation** whose remediation is an ordinary **un-labeled product
  [Build](../lifecycle/build-orchestration.md)** PR that brings the code back to spec (the merge the
  adjudication) — deduplicated by the **matrix row identity** (`(spec-doc, criterion-cell digest)`) so recurring
  drift updates the one draft rather than re-nagging. It re-derives from the `docs/spec/` span itself, never
  from the matrix rows (the matrix is the denominator, not the checklist — [R16](../../../reference/risks.md)). It
  **reports and recommends**; it never gates and never heals.

### The audit persona

Audit work runs through a **purpose-built audit persona** — a cold-context [agent](../surfaces/agents.md)
instance distinct from the build-orchestration review lenses, because a build reviewer inspects a *proposed
change* while an audit inspects *standing, accumulated state*. The [agents](../surfaces/agents.md)
grammar types it as the **`audit` role**: fired by the `audit-prep` cron, carrying **no lens** (the single
self-audit persona is recognized by its role), at the `judgment` `model-tier`, with its findings routed
through the two-lane disposition below. This doc fixes the *requirement* for a dedicated audit persona and
the posture it carries; the field grammar itself is the agents surface's, not restated here. The persona is
**read-only** — it reports; it never writes engine or product surfaces.

### The three posture laws

These are why audits are worth having; without them, periodic review compounds toward "confirm it still works
/ preserve," accreting dead weight no audit retires — Risk [R6](../../../reference/risks.md) at the audit layer.

1. **Adversarial / retirement-default.** The audit defaults to recommending **retirement** of accumulated
   *local* state, not preservation. A local artifact is preserved only with an **affirmative case** — *what
   work does this do that nothing else does?* Each audit **looks hard for a retire-candidate and surfaces one
   when it honestly exists**; when none does, it renders an explicit subsection that adversarially scrutinizes
   its own "no candidates" claim. There is **no quota** — a retire-candidate surfaced only to produce one is
   itself the failure mode, and the honest "nothing to retire this cycle, here is what I checked" is always
   preferred to a manufactured nomination, so the operator is never trained to rubber-stamp deletions. (The
   default applies to local state only; machinery is never a retire-candidate.)
2. **Function-probe, not stats.** A claim about a thing's fitness must rest on a **content probe run during
   this audit**, never on a cached count, status field, or existence check. Counts say a thing *exists*; only
   a fresh probe says it still *does work*. (A function probe is an audit-time judgment, not a standing
   daemon. Liveness — "is the MCP server up right now?" — is a separate concern owned by
   [boot](../lifecycle/boot.md) degradation and [hooks](../infrastructure/hooks.md)
   fail-open, not by audits.)
3. **Cold-context random-target probe.** Each audit reads **≥1 randomly-selected *in-repo* artifact as if it had
   no project context**, asking: do its cross-references resolve to currently-correct content? does its prose
   tell a cold consumer how to *use* it, or only that it exists? does it name a sibling that no longer exists,
   or carry a rule a successor superseded without a back-reference? And when the pick is **operator-facing prose**
   — a [doc](../surfaces/docs.md), or the operator-facing strings an engine [tool](../surfaces/tools.md)
   renders — does it meet the [operator-communication law](../../../reference/glossary.md)? Both of the law's edges are judged:
   the **register** edge — addressing the operator as a capable adult, never **condescending or talking down**,
   explaining at length what the reader plainly already grasps as if they could not — and the **substance** edge's
   clarity-over-jargon facet: prose leaning on engineer-shorthand or unexplained internal vocabulary where a plainer
   word would serve. Both are **semantic judgment, never a mechanical word filter or a banned-word list** (the law
   forbids creating one) — the probe weighs whether the *right* word was used for the operator's need, not whether
   some forbidden substring appears. Operator-facing prose that is accurate and usable yet talks down or leans on
   needless jargon is **surfaced as a finding** (recommend-not-block, the audit tier — never a merge gate, per
   *Report, never heal* below), caught for remediation rather than passing the probe unexamined. A finding on
   **project-authored local prose** (a [doc](../surfaces/docs.md) the operator owns) takes the local
   reconcile lane; a finding on a **template-owned tool string** (machinery) takes the **escalate-upstream** lane
   (*Disposition* below) — a local edit would be reverted by the next overlay. The probe **samples** (≥1 target a
   cycle), so this is drift defense over time, not a sweep that proves every operator-facing string clean. The register-and-jargon judgment is **conservative and
   audience-aware**: it weighs prose against its *intended* reader — a beginner-oriented orientation doc is not
   condescension for being thorough, and a precise technical word a literate operator plainly knows is not jargon —
   flags only clear talking-down or genuinely opaque shorthand, never stylistic preference or a correct word, and a
   finding the operator judges wrong is a **legitimate decline**, never a manufactured nomination (law 1's
   no-quota / declining-is-a-real-choice applies to register as to retirement). The warm audit "knows too much";
   the random cold pick is its defense against drift — in correctness *and* in register — in artifacts it already
   trusts.

### Reading its own prior digests — over-time corroboration

Each committed digest carries its run-date (*The audit digest*, below), so the dated sequence of prior digests —
the git history of the one committed digest path — is an **over-time corroboration input** to the generic sweep
and the concern probes, bounded so it sharpens judgment without becoming the judgment:

- **Corroborates, never decides.** A retire/keep call still rests on a **fresh function-probe run this cycle**
  (law 2 — counts say a thing existed; only a present probe says it still does work). Persistence of a condition
  across digests is evidence that local cruft is genuinely stale rather than a one-cycle blip; it never substitutes
  for the probe, and quiet is never read as dead.
- **Observed conditions only — never the audit's own prior judgment.** The persona may rest on a *condition it
  recorded* (a finding's source still firing, a local artifact still showing no evidence of use), never on a prior
  digest's *recommendation or inclination*. Citing its own past leaning as evidence would compound a single
  project's bias across cycles and feed the warm audit its own priors — against the cold-context random-target
  probe (law 3) and the deferred-by-design learning ambition (*Avoid*, below).
- **Prioritization computes nothing.** Recurrence may direct *where* the persona looks this cycle; it persists no
  count, threshold, or weight (re-weighting from observed usage is the held-out auto-calibration ambition under
  *Avoid*, below).
- **Honest degradation.** When the prior digests are unreadable — a fresh repo with none yet, a shallow clone, a
  rewritten history — the audit falls back to a point-in-time review and **says so plainly** in the digest, never
  a fabricated trend.

This reads the digest's **own committed history**; it adds no new committed artifact and no ledger (the durable
signal-of-record stays [telemetry](telemetry.md)'s native record and the per-issue first-seen/last-seen
markers it already surfaces), so it neither rebuilds a dissolved archive ([D-038](../../../adr/0038-session-lifecycle-re-founded-on-native-substrates.md),
[D-040](../../../adr/0040-telemetry-designed-end-state-native-signal-of-record-tracked.md)) nor duplicates telemetry's mechanical trend, and the judgment ladder is
untouched: telemetry still counts and trends mechanically; audits judges — now able to weigh whether a thing has
*stayed* unfit.

### Disposition — recommend, the human adjudicates; two lanes

The audit **reports and recommends**; it does not execute retire / convert / replace. Findings route
to **engine-labeled GitHub Issues** (the same locked [finding-disposition](../surfaces/policies.md)
substrate [telemetry](telemetry.md) uses) and take one of two lanes:

- **Local retire/reconcile** — for accumulated local state, and for a **product divergence from the `locked`
  spec** (the conformance sweep's finding: reconcile the code to the frozen criterion). Remediation is ordinary
  [Build](../lifecycle/build-orchestration.md) work whose **merge is the adjudication** — there is
  no separate buffered-adjudication subsystem.
- **Escalate upstream** — for a genuine **machinery** bug or mis-fit, which a local PR cannot fix (the next
  overlay reverts it). The audit **drafts** a bug report for the **template repository** (its coordinates are
  known from the engine manifest) and surfaces it to the operator: *"this looks like an Engine problem, not
  something to fix in your repo — file it upstream or ignore."* The operator files it via their own `gh` (one
  action), maintains a fork, or ignores it. The draft is **deduplicated by the same stable source-key**
  telemetry uses, so a machinery mis-fit that recurs every cron **updates the one draft rather than re-nagging**
  — an ignored escalation does not return as fresh noise each cycle. "Ignore" is an honest, informed choice,
  not a safe fix: the bug persists (locally unfixable until an upstream release lands), and the doc says so
  plainly rather than implying the matter is closed. The Engine **never auto-files and never silently phones
  home**; it degrades to a plain local notice if the template repo is unreachable, private, has issues
  disabled, or rejects the operator under an interaction limit. This is an additive elaboration of the locked
  `escalate` finding-disposition, not a new disposition.

Because the merge (or the upstream file) *is* the consent, a retirement or escalation **and its issue must
state, in plain language, the concrete cost** — *"you will no longer be warned when X"* — and offer a
low-friction **"keep it" / "ignore"** path, so declining is a real choice, not inertia (the
operator-communication law): the operator must understand what they are approving, never merely that "cleanup"
or "a fix" is proposed. When a retire-candidate **recurs across cycles**, the recommendation re-presents the
*case*, never escalates the *ask*: a prior decline stands as a real choice, and the recurrence is never surfaced
as mounting pressure or social proof (the symmetry of the escalate-lane's *"does not return as fresh noise each
cycle"* above) — so over-time evidence strengthens the case without eroding the freedom to decline it.

### Concerns — a generic sweep, a small declarative list, and a conditional conformance sweep

What an audit examines is **hybrid**:

- **An always-on generic sweep** — the persona applies the three posture laws against the deployed instance's
  local state generically (every run does the adversarial/retirement read and the cold-context random pick).
  This is pure law; it needs no per-concern artifact, and it is the **floor** that survives even an empty or
  degenerate concern-list — which is what insulates the concern-list's own self-audit (below) from blind
  spots.
- **A conditional product-conformance sweep** — *when* a `locked` `docs/spec/` and its
  [spec-obligation matrix](../../../reference/glossary.md) are present, the **forward** divergence-hunt over the `locked`
  rows described in *Product conformance to the operator's locked spec* above — prioritized, not exhaustive.
  This is the **standing cadence** of the traveling floor; it is a divergence-check (not the retirement
  posture), report-only, and silent wherever no spec is locked.
- **A small declarative concern-list** — sharp hygiene concerns that need precise targeting, expressed as
  **data rows**, not prose prompts: each **concern-entry** names a `target`, an `adversarial-question`, its
  `finding-types`, and a `justification` (the affirmative case for why it earns a row). The list is seeded
  with the deployed-repo hygiene targets — **stale memory beliefs** (contradictions, beliefs that observed
  behavior now refutes, high-frecency-but-obsolete records — the judgment layer *above*
  [memory](../cognitive/memory.md)'s mechanical consolidation/decay, never duplicating it; this
  is also where a function-probe over memory's **already-logically-retired** records recommends their
  **physical erasure** when they genuinely earn it — the one audit recommendation whose *enacted*
  consequence is irreversible, so it is gated on the operator merging a **single-purpose erasure pull
  request** under the operator-communication law, never a bare Issue close, with the audit recommending
  only and never re-detecting retirement, which stays memory's mechanical call),
  **stale debt** (engine-labeled issues that no longer reproduce; triage-pressure backlog health),
  **module fit** (an optional module for which a fresh probe finds **no evidence of exercise** and **no
  affirmative case** — *what does this do that nothing else does?* — → retire-candidate, with the
  absence-of-evidence the trigger to ask for that case, never by itself the proof of disuse, and digest-history
  persistence corroborating rather than deciding the call; recurring operator friction that maps to an
  *uninstalled* module → suggest installing it), and **local-surface hygiene** (abandoned
  `proposed` contracts/policies, a single-referrer local [operation](../surfaces/operations.md) that
  is really one skill's private depth, orphaned local skills/agents) — and **grows additively**.

**The bound on concern-list growth (the contract-threshold mechanism, applied to concerns).** The list cannot
sprawl back toward the prototype's per-concern zoo, because growth is **deliberate and reviewed**: a row is
added only through a merged [Build](../lifecycle/build-orchestration.md) PR — the same human-gated
bar a contract passes — against an **entry bar** (a row earns its place only if it targets a drift the generic
sweep doesn't already catch, *cannot* be expressed as a mechanical [check](../surfaces/check.md)
— else it belongs in [validation](validation.md) — and carries an affirmative case) and a **schema
presence gate** (the concern-entry schema requires the `justification` field; presence is validation-checkable
via the existing schema check-kind, genuineness stays posture). The list is then **itself a standing audit
target**: each run, a **fresh function-probe** (law 2 — a judgment made now, never a cached hit-count) re-asks
of each row whether its concern is still un-caught by the generic sweep, still un-mechanizable, and still
well-formed; a row that fails *now* (subsumed, now expressible as a check, or never well-formed) is a
retire-candidate. There is no numeric cap, no new policy, and no telemetry stream — the deliberate-authorship
bar plus reflexive retirement is the governor.

### Cadence

Audits fire on a **fixed cron** via the locked-[validation](validation.md) `audit-prep` trigger;
authoring this system's runner **fulfills** that doc's deferred forward-reference, so no validation re-lock is
needed. There is **no self-tuning cadence** — a feedback controller for audit frequency is exactly the kind of
machinery this design refuses. The schedule should avoid the top-of-hour load spike (a non-zero cron minute).
A **missed cron is expected degradation**, not breakage: audits *report*, never gate, so a skipped run loses a
cycle of signal, never blocks work. (On a **public** repo, GitHub auto-disables a scheduled workflow after 60
days with **no repository activity** — a commit resets the timer; the "default branch" only governs *where*
scheduled runs execute, not the disable clock. One operator action — `gh workflow enable …` — re-enables a
disabled workflow. Private repos are not subject to this auto-disable. Either way, prolonged silence is
surfaced through the digest-freshness signal below, so a stopped cron is never invisible.)

### The audit digest

An audit run produces a **committed, fingerprint-gated audit digest** — the Engine's plain-language
self-attestation of its own operational health, **and, where a `docs/spec/` is locked, of the product's
standing conformance to it** (which `locked` criteria still hold, which have drifted, in plain consequence
language) — openable by a non-engineer browsing the repo (the self-map precedent: derived, committed so a human
can read it, fingerprint-gated so it cannot silently drift). The digest **carries its run-date**. Past a staleness bound, `audit-library` emits a digest-staleness
[finding](../surfaces/policies.md), which [boot](../lifecycle/boot.md) renders through the
**same locked open-findings path it already surfaces** — in plain language, naming the one re-arming action:
*"the engine hasn't self-reviewed in N days; run `gh workflow enable …` or push a commit to re-arm it."* Boot
also surfaces the dated digest among its informational digests with its recency shown (boot's staleness-shown
rendering; the exact rendering is a build-spec leaf, no boot change). This closes the silent-stop gap as far
as any in-repo mechanism can: a fully-dormant repo is reached only on the operator's **return**, when boot
reads the committed digest and shows the staleness notice — the honest irreducible limit. The digest's generator and its fingerprint gate run in one workflow
(regenerate-then-gate, atomically), so the digest-writing PR's required check passes. The same digest-writing
**workflow** is also the committer of [state](../cognitive/state.md)'s offline cache: it carries the
refreshed cursor — both fields (the standing-situation and the debt count, refreshed by the shared
GitHub-derived-cache pass) — **as freight** in the same pull request, gated by the cursor's own schema check
rather than the digest's fingerprint gate (the cache derives from continuously-changing external state, so it
is schema-gated, not drift-gated; [state](../cognitive/state.md) names that bound). The audit
**persona stays read-only** — the *workflow* commits, never the persona — and this carries **no detection of
the cache's content**: the values are [telemetry](telemetry.md)'s and
[boot](../lifecycle/boot.md)'s, relayed as freight ([principles §16](../../../principles.md)). The
concrete refresh-and-commit wiring lands with this module's build. Because the operator cannot meaningfully
review a mechanical derivation, the digest pull request presents the cache file as **auto-derived freight the
operator does not vouch for** — the merge attests to the self-attestation it rides, not to the cursor's
contents (the plain-language wording is a build-spec leaf under the operator-communication law).

Its **operator contract is plain language**: it names what was probed, what was found, and what is
recommended, in terms the operator can act on — never engineer shorthand (a digest entry reads *"I reviewed
your saved decisions and three now contradict newer ones — here's which, and what I'd drop"*, not
*"3 episodic records failed the function-probe"*; a conformance entry reads *"I checked your product against
the spec you froze — two things you asked for don't match it anymore, here's which and what a fix would
change"*, not *"2 locked rows diverged on the divergence-hunt"*). This plain register is a **requirement on the
digest/issue author, anchored by those pinned exemplars**, not an aspiration; the backstage vocabulary of this
system (concern-list, function-probe, generic sweep, fingerprint-gated, retire-candidate, and — for the
conformance sweep — spec-obligation matrix, conformance-enforcement floor, divergence-hunt, coverage
denominator) **never appears in operator-facing text**.

Because the digest is **committed to the project repo**, its one reference to **gitignored experiential
memory** — the saved-decisions exemplar above — is **gated on repo visibility**: on a **private** repo the
digest may name the stale saved beliefs (this project's namespace only — the read reaches no other;
[D-007](../../../adr/0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md) keeps the *store* uncommitted, while this derived *finding* may reference it);
on a **public** repo the digest **omits the belief specifics and says so**, reviewing saved-memory staleness
only in the aggregate it can safely commit. The gate stops a *future* digest from carrying belief content, not
a *past* one already committed (whether the repo was public then or was private and later flipped)
([§7](../../../principles.md)) — a different surface from the vault-flip exposure
[memory](../cognitive/memory.md) ([D-238](../../../adr/0238-resolve-the-d-237-memory-backup-shared-vault-flip-the-four-l.md)) bounds. It binds only the **one concern that reads gitignored memory**; every other digest entry (probe
results, debt, hygiene) is already about committed state and is unaffected. How `audit-library` detects repo
visibility and degrades is a build-spec leaf.

When a finding draws on over-time corroboration, the digest presents its **fresh-probe
basis and the corroborating-history note as distinct** — *"this still does nothing on a fresh check, and it has
shown nothing in each of the last three reviews"* — so the present probe is visibly standing on its own and the
operator (and a later cold pick) can see the call was not made on history alone; the over-time half is rendered
in that plain register, never as backstage trend-vocabulary. The digest is a **system-owned, non-surface** derived
output, not a catalog surface, so the [ontology](../grammar/ontology.md) is untouched; the
concern-list schema is likewise a system-owned artifact validated by direct invocation of the schema
check-kind, not by catalog routing.

### Avoid (the prototype's over-engineering, and the deferred ambition)

These are foreclosed by design:

- **A maintainer-style systemic-architecture review shipped to deployed repos** — "is this *system* earning
  its place," "retire this *surface*" against template-owned machinery. Deployed repos cannot act on it
  (machinery is overlaid/immutable there); that review is the maintainer's ad-hoc work against the template
  repo, not engine scaffolding every downstream user carries. This forecloses reviewing the **template's engine
  architecture** — **not** the product-conformance sweep above, which reviews the **product** against the
  operator's own `locked` spec and is locally actionable (an ordinary Build reconcile).
- **A self-tuning loop** — re-weighting attention, re-tuning thresholds, or otherwise modifying the engine's
  own operating parameters from observed usage. This is a real and valuable ambition (CoALA's procedural-memory
  *learning*), but it is infeasible on the signals a deployed instance can mechanically observe, would
  over-fit a single project, and would over-weight the contagious core ([§12](../../../principles.md)). It is
  **deferred to a future optional module** ([open-questions](../../../reference/open-questions.md)), out of required
  core, to be pursued with real multi-project evidence — not shipped in v1.
- **A library of bespoke audit-prompt documents + a dispatcher** — concerns are data rows run by one persona;
  the prompt-per-concern zoo is the R5/R6 failure.
- **`audit-finding` knowledge-graph entities + a currency detector** — findings are engine-labeled issues;
  housing them in the graph is the [D-031](../../../adr/0031-integration-debt-is-a-telemetry-owned-register-not-a-knowled.md) category-muddle (knowledge carries no
  debt). A recurring finding's identity is the issue's stable dedup key, not a KG entity.
- **A fault-injection / scorecard apparatus** — wiring correctness is the locked
  [validation](validation.md) coherence kind; "does it still do work" is the function-probe posture.

## Acceptance criteria

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Judgment, not mechanism** — audits exist to make the calls a check cannot. The mechanical floor stays with [validation](validation.md) and [telemetry](telemetry.md). | Read this description against the built behavior and confirm they match. | operator |
| **Report, never heal** — the persona is read-only; remediation is a reviewed Build PR or an operator-filed upstream report. CoALA frames this human-gated, reversible, propose-not-apply posture as the necessary discipline for any change to an agent's own state; the lineage is maintainer-layer vocabulary ([§12](../../../principles.md)) and never surfaces to the operator. The posture binds the audit's *own action* — it only ever recommends, never writes engine or product state; a recommended **memory erasure** is the one case whose *enacted* consequence is irreversible, which is exactly why it is gated on the operator's single-purpose-PR merge and never enacted by the audit. | Read this description against the built behavior and confirm they match. | operator |
| **Deployed-repo hygiene, plus conformance to the operator's locked spec** — the audit acts on accumulated *local* cruft (retire/reconcile) and escalates machinery upstream, and — **only where a `docs/spec/` is locked** — checks the product's conformance to that frozen spec (report-only divergence, reconcile lane). It never retires or locally patches template-owned machinery, never judges product *quality*, and ships no systemic-review or self-tuning scaffolding. | Read this description against the built behavior and confirm they match. | operator |
