# Product decision records

The curated decision set for engine-template as built from this repository. Each record states a
surviving law and its why; the spec in `docs/spec/` cites these records and never restates them.
Status lives only in each record's own frontmatter — this index deliberately carries none.

These records are deployment-local to this repository. Nothing that travels to engine-template — a
contribution, an issue, a pull request — may reference their numbers; the containment check in
`tools/adr-containment/` enforces that wall. (The engine's own `eADR-####` records under
`.engine/contracts/` are a separate system and are never affected.)

New records: copy `TEMPLATE.md`, take the next free number, add a ledger row here.

## Ledger

| Record | Title | Replaces |
| --- | --- | --- |
| [ADR-0001](ADR-0001-design-record-lives-here.md) | The design record lives here — spec plus decision records, laws not leaves | — |
| [ADR-0002](ADR-0002-lineage-honest-novelty.md) | Honest lineage for the cognitive substrate | D-033 |
| [ADR-0003](ADR-0003-core-module-demarcation.md) | Core/module demarcation operationalized — slots and fillings | D-069 |
| [ADR-0004](ADR-0004-derived-committed-artifacts.md) | Derived-committed artifacts are source-deterministic; conflicts are spurious | D-217 |
| [ADR-0005](ADR-0005-template-license.md) | Template license — source-available seed, license-agnostic design, first-run clear | D-221, D-295 |
| [ADR-0006](ADR-0006-license-binding-accepted-risk.md) | Downstream license binding — enforceability question closed eyes-open | D-301 |
| [ADR-0007](ADR-0007-trustworthy-ai-recenter.md) | The AI is the thing made trustworthy; banned-word lists ended | D-225 |
| [ADR-0008](ADR-0008-behavioral-demonstrations.md) | Behavioral demonstrations — shape, lifecycle, and the standing AI-run tier | D-228, D-231 |
| [ADR-0009](ADR-0009-artifact-warrant.md) | Every generated artifact carries its warrant | D-261 |
| [ADR-0010](ADR-0010-pinned-forms-finding-base.md) | Deferred values pin their form; one canonical finding base | D-113 |
| [ADR-0011](ADR-0011-recognition-slice-degrade-loud.md) | Boot reads the recognition slice, sheds loudly, and retires its weakening alarm | D-309 |
| [ADR-0012](ADR-0012-memory-episodic-capture.md) | Memory capture observes importance; it never predicts it | D-030 |
| [ADR-0013](ADR-0013-memory-recall-integrity.md) | Ledger integrity and honest recall | D-081, D-273 |
| [ADR-0014](ADR-0014-memory-consolidation-sweep.md) | The consolidation sweep is incremental, terminating, and mechanical | D-279, D-307, D-308 |
| [ADR-0015](ADR-0015-memory-compaction-erasure.md) | Compaction bounds growth; only a merged consent erases | D-209, D-285 |
| [ADR-0016](ADR-0016-memory-offrepo-backup.md) | Automatic off-repo backup — shared vault default, minted namespaces, retained snapshots | D-061, D-237, D-264 |
| [ADR-0017](ADR-0017-memory-authority-boundary.md) | The engine's memory supersedes the harness notebook | D-251 |
| [ADR-0018](ADR-0018-knowledge-query-contract.md) | The knowledge graph is queried read-only through a pinned operation set | D-116, D-224 |
| [ADR-0019](ADR-0019-knowledge-enrichment-gates.md) | Graph enrichment passes four durable gates, never a field list | D-203 |
| [ADR-0020](ADR-0020-state-plan-attention-split.md) | Attention ranks work in flight; the cursor reads the plan as found | D-314, D-315, D-317 |
| [ADR-0021](ADR-0021-state-offline-cache-freight.md) | The offline cache rides the audit digest as schema-gated freight | D-205 |
| [ADR-0022](ADR-0022-self-arming-audit-substrate.md) | The self-audit arms itself and its schedule is swappable | D-133, D-146, D-229 |
| [ADR-0023](ADR-0023-digest-history-corroboration.md) | The audit reads its own history as corroboration, never as the judgment | D-233 |
| [ADR-0024](ADR-0024-memory-vault-read-privacy.md) | Saved-memory review reaches the vault least-privileged; the public digest withholds specifics | D-241, D-243 |
| [ADR-0025](ADR-0025-author-exemption-disclosed.md) | A rule that does not bind a change says so — the disclosed not-applicable | D-207 |
| [ADR-0026](ADR-0026-hard-checks-proven-to-bite.md) | Every hard check is proven able to fail | D-256 |
| [ADR-0027](ADR-0027-disposition-citation-resolution.md) | Cited follow-ups must be real — disposition citations resolve or the merge fails | D-262 |
| [ADR-0028](ADR-0028-operator-runnable-acceptance.md) | The review record offers the operator runnable acceptance steps | D-252 |
| [ADR-0029](ADR-0029-spec-conformance-floor.md) | Conformance to the operator's frozen spec — a mechanical denominator and a standing sweep | D-287, D-296 |
| [ADR-0030](ADR-0030-engine-issue-channel.md) | Engine-issue channel grammar and the conformance reroute gate | D-183, D-235 |
| [ADR-0031](ADR-0031-security-floor-extension.md) | Security floor extends to code scanning and vulnerability disclosure | D-211 |
| [ADR-0032](ADR-0032-readme-landing-front.md) | Root readme as a seeded-then-ceded landing front | D-213 |
| [ADR-0033](ADR-0033-travel-safety-closure.md) | First-run retirement is reference-closed, enforced by a hard closure check | D-219 |
| [ADR-0034](ADR-0034-checkout-stewardship.md) | Operator-checkout stewardship — two-stage strand detection and the harness-exhaust boundary | D-275, D-239 |
| [ADR-0035](ADR-0035-provisioned-verdict.md) | The provisioned verdict keys on instantiator presence, three-state | D-277 |
| [ADR-0036](ADR-0036-engine-home-repository.md) | The engine manifest records the engine's home repository | D-281 |
| [ADR-0037](ADR-0037-license-seed-detector.md) | Standing license-seed detector with a reviewed-PR fix path | D-302, D-303 |
| [ADR-0038](ADR-0038-close-disposition-gate.md) | Turn close is ambient capture plus a finding-disposition gate | D-072 |
| [ADR-0039](ADR-0039-build-workflow.md) | The build workflow — two-beat consent, single writer, honest gates | D-073 |
| [ADR-0040](ADR-0040-close-linkage-preflight.md) | Submit-time close-linkage pre-flight — detect and surface, disclosed defang | D-283, D-284 |
| [ADR-0041](ADR-0041-routine-entry.md) | Routine entry is a pre-authored operator act, visible on misfire | D-088 |
| [ADR-0042](ADR-0042-plan-mode-and-acceptance.md) | Native plan mode — a yielding default, and acceptance that enters Build legibly | D-185, D-270 |
| [ADR-0043](ADR-0043-operator-relay.md) | The assistant's chat is the sole in-session operator channel | D-187 |
| [ADR-0044](ADR-0044-checkout-boundary.md) | The operator checkout is a surface, not a workspace — strand detection and lossless repair | D-189 |
| [ADR-0045](ADR-0045-release-cut.md) | Engine releases are cut by an evidenced maintainer confirmation through the gate | D-194 |
| [ADR-0046](ADR-0046-boot-standing-findings.md) | Boot's standing findings — a bounded intent-exit, and honest milestone rendering | D-306, D-319 |
| [ADR-0047](ADR-0047-procedure-boundary.md) | The procedural-surface boundary — one procedure, one home | D-042 |
| [ADR-0048](ADR-0048-agent-grammar.md) | The agent grammar — role binds to trigger, demand not model, report not disposition | D-057, D-100 |
| [ADR-0049](ADR-0049-agent-integrity.md) | Agent integrity — engine-prefixed names, a mechanical read-only floor with honest limits | D-313 |
| [ADR-0050](ADR-0050-interface-resolution.md) | Interfaces — single-active resolution with a named, never-nagging fallback | D-064 |
| [ADR-0051](ADR-0051-skill-invocation.md) | The cold-start invocation law | D-200 |
| [ADR-0052](ADR-0052-skill-restraint.md) | Skill restraint — residence is earned, discovery is derived, routine entry is explicit | D-087 |
| [ADR-0053](ADR-0053-policy-override.md) | Per-deployment override of policy tuning values — retune within the laws, never weaken them | D-167 |
| [ADR-0054](ADR-0054-rationale-canon.md) | The engine ships its own why — the foundational rationale canon | D-169 |
| [ADR-0055](ADR-0055-install-menu.md) | The install menu shows only opt-outs, grouped under recognized disciplines | D-067, D-068 |
| [ADR-0056](ADR-0056-required-spine.md) | Core is the trusted root; the self-validation corpus and routine entry ship beside it | D-089, D-090, D-092 |
| [ADR-0057](ADR-0057-cognitive-packaging.md) | The required-package rule; memory is its own package, knowledge rides core | D-086, D-091 |
| [ADR-0058](ADR-0058-product-design.md) | Product-design is the spec-driven front door; the engine validates form, the operator locks | D-244, D-250, D-065, D-141 |
| [ADR-0059](ADR-0059-review-suites.md) | Review ships as two lens-roster suites; judgment above mechanics, disclosed when idle | D-066, D-291 |
| [ADR-0060](ADR-0060-scm-governance.md) | Dependency and migration discipline: honest tiers, escalation over false gates | D-097, D-098 |
| [ADR-0061](ADR-0061-board-projection.md) | The work board is a one-way projection that renders only computed verdicts | D-099, D-318 |
| [ADR-0062](ADR-0062-depends-axis.md) | A depends edge is derived from what the module inspects | D-129 |
| [ADR-0063](ADR-0063-postv1-stubs.md) | Named future modules with engine-observable triggers; no expression-contracts surface | D-191, D-255, D-095, D-105 |
| [ADR-0064](ADR-0064-spec-is-the-standing-target.md) | The spec is the standing target — no construction milestone licenses an under-build | D-266, D-267 |

## Where every retired source went

One line per top-level document or directory of the retired engine-planning workspace, so
document-level completeness is reviewable — nothing was dropped silently.

| Source | Disposition |
| --- | --- |
| decision-log.md (D-001–D-319) | carried into this ADR set — complete per-decision map below |
| systems/grammar/ | distilled → [grammar](../spec/grammar.md) |
| systems/cognitive/ | distilled → [cognitive](../spec/cognitive.md) |
| systems/guardrails/ | distilled → [guardrails](../spec/guardrails.md) |
| systems/infrastructure/ | distilled → [infrastructure](../spec/infrastructure.md) |
| systems/lifecycle/ | distilled → [lifecycle](../spec/lifecycle.md) |
| systems/surfaces/ | distilled → [surfaces](../spec/surfaces.md) |
| modules/ (catalog + 17 packaging docs) | distilled → [modules](../spec/modules.md) |
| principles.md (§1–§20), constraints.md, goals-and-quality.md | distilled → [principles](../principles.md) (consolidated to 18 laws; source §8 and §9 relocated into the guardrails and grammar spec documents) |
| engine-architecture.md | distilled → [architecture](../architecture.md) |
| glossary.md | load-bearing terms distilled into the spec documents; the rest deliberately dropped |
| scenarios/ (9 walkthroughs) | mined for acceptance criteria in the spec documents; not carried as documents |
| risks.md | still-live constraints became spec laws; genuinely open items triaged to product issues post-merge |
| open-questions.md (8 threads) | triaged to product issues post-merge |
| deviations/ | consumed as a curation cross-check; deliberately dropped |
| wbs/ (build plans and audit ledgers) | construction-era; deliberately dropped — the conformance-relitigation ledger was excluded by explicit decision (stale against the live build) |
| validate.py, lock.py, locks.yaml | construction tooling; deliberately dropped |
| .architect-review-q28.txt | session working notes; deliberately dropped |
| CLAUDE.md, README.md | workspace instructions; deliberately dropped |

## Disposition of every retired decision

Every engine-planning decision, exactly once. The dispositions: **carried** — the decision is
the backbone of the named record; **collapsed into** — merged into that record alongside others
(superseded links folded into their terminal decision); **engine-canon** — the surviving content
already lives in the engine's own founding records under `.engine/contracts/` and is deliberately
not duplicated; **construction-era — not carried** — governed the planning/build process itself,
nothing product-governing survives; **moot — build diverged** — overtaken entirely by how the
build actually went.

| Decision | Title | Disposition |
| --- | --- | --- |
| D-001 | Restart engine-template in a blank repo | construction-era — not carried |
| D-002 | Proposal and prototype are reference inputs, not gospel | construction-era — not carried |
| D-003 | Specify the full end-state before the first build PR | construction-era — not carried |
| D-004 | Establish the engine-planning workspace with a fixed documentation discipline | construction-era — not carried |
| D-005 | Distribution model is "Use this template" | engine-canon (eADR-0001) |
| D-006 | Nine non-modular foundations | engine-canon (eADR-0008) |
| D-007 | Memory data is local and gitignored; substrate ships empty | engine-canon (eADR-0003) |
| D-008 | Memory and knowledge are distinct substrates | engine-canon (eADR-0019) |
| D-009 | Telemetry is a remediation loop, not self-healing | engine-canon (eADR-0015) |
| D-010 | Attention is a first-class surface | engine-canon (eADR-0032) |
| D-011 | Knowledge-graph state is derived, not hand-authored | engine-canon (eADR-0002) |
| D-012 | Provisioning is two subsystems on one manifest grammar; modules declare wiring | engine-canon (eADR-0009, eADR-0023) |
| D-013 | The control-plane bootstrap must travel and fail loud | engine-canon (eADR-0021, eADR-0023) |
| D-014 | A lightweight validate.py for the planning workspace | construction-era — not carried |
| D-015 | Adopt a locked-status mechanism with a litigation alarm | construction-era — not carried |
| D-016 | Repository topology as a foundational substrate; product-owns-root wall; laws not leaves | engine-canon (eADR-0007) |
| D-017 | Control-plane locked end-state, as contracts not leaves | engine-canon (eADR-0013, eADR-0021) |
| D-018 | Cold-session design audit required before any lock | construction-era — not carried |
| D-019 | Authoring grammar locked end-state, as laws not leaves | engine-canon (eADR-0006, eADR-0014, eADR-0016, eADR-0029) |
| D-020 | Engine instance identifiers are engine-namespaced; decision records are eADR-#### | engine-canon (eADR-0017) |
| D-021 | GitHub Projects ships as an optional adopter-facing module, projecting repo-authoritative state | engine-canon (eADR-0002, eADR-0004) |
| D-022 | Hooks locked as foundation #11, as laws not leaves | engine-canon (eADR-0022) |
| D-023 | Check system locked: validator architecture, the check surface, and the suite/trigger grammar | engine-canon (eADR-0005, eADR-0010, eADR-0020) |
| D-024 | The engine is upgradeable: versioned packages, upgraded by overlaying tagged template releases | engine-canon (eADR-0001) |
| D-025 | Fault-containment is earned at the seams, not conferred by modularity | engine-canon (eADR-0008) |
| D-026 | The Engine is an embedded team member (contributor, not component); asymmetric awareness | engine-canon (eADR-0007) |
| D-027 | Topology admits root .mcp.json as a tool-dictated slot (re-litigation of locked topology) | engine-canon (eADR-0007, eADR-0009) |
| D-028 | Module system locked end-state, as laws not leaves | engine-canon (eADR-0001, eADR-0009, eADR-0010, eADR-0023) |
| D-029 | Cognitive substrate is one workflow: 2-store/1-register/1-cursor/2-function, consulted by push | engine-canon (eADR-0018, eADR-0031, eADR-0032, eADR-0033) |
| D-030 | Memory: ledger-canonical, observe-don't-predict capture, lexical floor + semantic module, built-in-auto-memory boundary | carried → ADR-0012 |
| D-031 | Integration debt is a telemetry-owned register, not a knowledge entity; knowledge regen rides the commit boundary | engine-canon (eADR-0002, eADR-0015, eADR-0018, eADR-0031) |
| D-032 | Re-litigation: bind UserPromptSubmit to the orientation scent (locked hooks re-lock) | engine-canon (eADR-0018, eADR-0022, eADR-0033) |
| D-033 | Ground the cognitive substrate in established standards (lineage, honest novelty, leak guard) | carried → ADR-0002 |
| D-034 | Re-litigation: hooks block-budget example retargeted off the dissolved eager-claim | construction-era — not carried |
| D-035 | Re-litigation: policies retargets the contract-threshold narrative sink and the routine tracked-finding location | construction-era — not carried |
| D-036 | Re-litigation: contracts retargets the default session-narrative sink off the dissolved changelog | construction-era — not carried |
| D-037 | Graveyard exemption: the append-only decision-log may link retired docs | construction-era — not carried |
| D-038 | Session lifecycle re-founded on native substrates | engine-canon (eADR-0010, eADR-0014, eADR-0024, eADR-0025, eADR-0033) |
| D-039 | Reports & self-improvement scope: Engine-only self-monitoring on a judgment ladder | engine-canon (eADR-0008, eADR-0015, eADR-0021, eADR-0028) |
| D-040 | Telemetry designed end-state: native signal-of-record; tracked debt is engine-labeled GitHub Issues | engine-canon (eADR-0002, eADR-0015, eADR-0021) |
| D-041 | Audits designed: purpose-built adversarial self-review | engine-canon (eADR-0028) |
| D-042 | Surface cluster: boundary law + derived-binding principle | carried → ADR-0047 |
| D-043 | Re-lock ontology+hooks to clear surface-set question | construction-era — not carried |
| D-044 | Check-kind binds by presence, not an interface | engine-canon (eADR-0010, eADR-0020) |
| D-045 | Specification is a doc-nature, not a catalogued surface | construction-era — not carried |
| D-046 | Harness mining: guardrail-integrity gap + contract hardening | moot — build diverged |
| D-047 | Product-spec intake: native, not bundled | moot — build diverged |
| D-048 | Provisioning & delivery end-state: brownfield-capable | engine-canon (eADR-0007, eADR-0011, eADR-0021, eADR-0023) |
| D-049 | File-precise CODEOWNERS ownership; infra-artifact carve-out | engine-canon (eADR-0007) |
| D-050 | hermes-interprets-coala mining; CoALA-as-narration rejected | moot — build diverged |
| D-051 | Guardrail integrity: no silent weakening (§15) | engine-canon (eADR-0011) |
| D-052 | Law layer closed; lock-order runway | construction-era — not carried |
| D-053 | Procedural surfaces reconciled to merged skill mechanism | moot — build diverged |
| D-054 | Lock operations and docs surfaces | construction-era — not carried |
| D-055 | Collapse command into skill: invocation is an axis | engine-canon (eADR-0016) |
| D-056 | Lock the tools surface | engine-canon (eADR-0016) |
| D-057 | Lock the agents surface; four settled forks | collapsed into ADR-0048 |
| D-058 | Discharge Wave-0 gate (Q10): world-tagging misattributed | construction-era — not carried |
| D-059 | Lock state: the committed cursor | engine-canon (eADR-0031) |
| D-060 | Lock knowledge: purely-derived structural store | engine-canon (eADR-0019) |
| D-061 | Lock memory: episodic ledger; Q3 backup resolved | collapsed into ADR-0016 |
| D-062 | Lock attention: policy-plus-function, reads-never-owns | engine-canon (eADR-0032) |
| D-063 | Lock boot/orientation: integration point honoring deferrals | engine-canon (eADR-0033) |
| D-064 | Lock interfaces: single-active with named fallback | carried → ADR-0050 |
| D-065 | Product-design front door: native intake module | collapsed into ADR-0058 |
| D-066 | The 4+4 review-lens roster | carried → ADR-0059 |
| D-067 | Operator-facing module packaging; core never an install choice | carried → ADR-0055 |
| D-068 | Q1 resolved: v1 optional-module roster (4 cut, 2 kept) | carried → ADR-0055 |
| D-069 | Core/module seam-walk: demarcation operationalized | carried → ADR-0003 |
| D-070 | Lock modes: three stances on two axes | engine-canon (eADR-0024) |
| D-071 | Re-lock modes: resume-resurrection overclaim fixed | engine-canon (eADR-0024) |
| D-072 | Lock close: turn-Stop finding-disposition gate | carried → ADR-0038 |
| D-073 | Lock build-orchestration; control-plane Review section | collapsed into ADR-0039 |
| D-074 | Sweep stale Q1 references (re-lock module-system, agents) | construction-era — not carried |
| D-075 | Lock telemetry: structural triage-volume bound | engine-canon (eADR-0015) |
| D-076 | Lock audits, re-founded for deployed-repo hygiene | engine-canon (eADR-0028, eADR-0029) |
| D-077 | Lock provisioning: terminal foundation lock | engine-canon (eADR-0021, eADR-0023) |
| D-078 | Repoint stale Q4 references in three locked docs | construction-era — not carried |
| D-079 | Principle §16: deferral seams named | engine-canon (eADR-0012) |
| D-080 | Re-litigate state honesty: known-unbounded faults named | engine-canon (eADR-0031) |
| D-081 | Re-litigate memory: ledger write-integrity law; cued-recall reframe; FTS5-latency honesty; tag-index pin; restore bound | carried → ADR-0013 |
| D-082 | Re-litigate knowledge (honesty): R8 deferred behind swappable seam, not mitigated | moot — build diverged |
| D-083 | Re-litigate attention: reference-time explicit determinism input; right-things-first unproven-until-fixture | engine-canon (eADR-0032) |
| D-084 | Re-litigate boot (+constraints): compaction facts; floor-vs-pack; verify-presence marker; Q18; stale-count | engine-canon (eADR-0033) |
| D-085 | Record cognitive-substrate efficacy-scorecard exercise; route gates and cautions | construction-era — not carried |
| D-086 | Cognitive foundations as required packages: memory its own required package, knowledge rides core | carried → ADR-0057 |
| D-087 | Resolve Q7 v1 skill membership; close deviation D2 | carried → ADR-0052 |
| D-088 | Name routine-entry command /engine-routine in modes + build-orchestration | carried → ADR-0041 |
| D-089 | Flesh core module doc to designed: kernel partition, validation engine/corpus seam, infra outside provides | carried → ADR-0056 |
| D-090 | Flesh validators-core to designed: engine-self-validation rule corpus, consolidated, data-files-only | carried → ADR-0056 |
| D-091 | Flesh memory-substrate module to designed: search implementation/contract split; wired capture; backup ownership | carried → ADR-0057 |
| D-092 | Flesh routine-mode to designed: operator entry into Routine stance, wiring nothing | carried → ADR-0056 |
| D-093 | Cut adr-discipline module: vestigial, content shipped by core + validators-core | engine-canon (eADR-0029) |
| D-094 | Defer expression-contracts design; correct core's carve-out | moot — build diverged |
| D-095 | Cut expression-contracts; re-home code angle to future clean-code; resolve Q19 | carried → ADR-0063 |
| D-096 | Author stage-0 build harness as WBS bootstrap-preamble; split engine-mechanic to Q20 | construction-era — not carried |
| D-097 | Flesh dependency-discipline to designed: review gate hard at CI, pinning soft, cadence posture | carried → ADR-0060 |
| D-098 | Flesh migration-discipline to designed: posture + escalation routing + soft presence check | carried → ADR-0060 |
| D-099 | Flesh github-projects-sync to designed: one-way board projection over committed truth | carried → ADR-0061 |
| D-100 | Decouple agent grammar from model landscape: model-tier a closed demand vocabulary | collapsed into ADR-0048 |
| D-101 | Pin stage-0 self-construction threshold to concrete module subset | construction-era — not carried |
| D-102 | Cross-repo external contribution first-class v1 (fork-native); engine-mechanic non-reflexive special case | engine-canon (eADR-0026) |
| D-103 | Cross-repo design cold audit resolutions | engine-canon (eADR-0026) |
| D-104 | Phase C: cross-reference external-contribution into four locked anchors | engine-canon (eADR-0026) |
| D-105 | Hold post-v1 product-knowledge-graph module stub | collapsed into ADR-0063 |
| D-106 | Elaborate external-contribution: knowledge home-vs-coverage; mechanic self-describing | engine-canon (eADR-0026) |
| D-107 | Author WBS module build-order; builder crossover; resolve Q20 (M1; in-repo v1, mechanic post-v1) | construction-era — not carried |
| D-108 | Add dry-run build-simulation instrument | construction-era — not carried |
| D-109 | Tune dry-run from L0 calibration: deferred disposition, reference-root handling | construction-era — not carried |
| D-110 | Run genesis dry-run through complete core; log blockers Q24–Q27 | construction-era — not carried |
| D-111 | Resolve Q22/Q23: no construction-repo CODEOWNERS; hand-seeded genesis manifest | construction-era — not carried |
| D-112 | Author core-lock closure procedure (Q24–Q27 remediation roadmap) | construction-era — not carried |
| D-113 | Closure Phase 0: form/contract convention + canonical finding.v1 base | carried → ADR-0010 |
| D-114 | Q25: fourth v1-core policy — Triage-threshold policy | engine-canon (eADR-0029) |
| D-115 | Q27 #1: validation kind-callable result contract (pass/fail over finding.v1) | engine-canon (eADR-0020) |
| D-116 | Q27 #3: knowledge-retrieval interface op-set + consumer-composed memory link | carried → ADR-0018 |
| D-117 | Q24 + Q27 #2: attention ranking-function form; scent threshold home | engine-canon (eADR-0032) |
| D-118 | Q27 #4+#5: telemetry finding-record + ambient-capture shapes; Q27 closed | engine-canon (eADR-0015, eADR-0020) |
| D-119 | Resolve Q26: /engine-help + kind-discovery as core build-spec leaves | engine-canon (eADR-0010, eADR-0020) |
| D-120 | Lock core: closure wave terminal ratification; retire closure procedure | construction-era — not carried |
| D-121 | Lock the external-contribution system doc; defer the module-packaging lock | construction-era — not carried |
| D-122 | Enumerate the branch-ruleset protection floor in control-plane | engine-canon (eADR-0021) |
| D-123 | Run the L2 dry-run (validators-core + memory-substrate); harden the instrument | construction-era — not carried |
| D-124 | Dry-run routine-mode (BUILD-READY); one designed-doc contradiction | construction-era — not carried |
| D-125 | Dry-run product-design: NOT build-ready; engine-label ownership alarm (Q28) | construction-era — not carried |
| D-126 | Dry-run audit-library: NOT build-ready; untypeable audit persona (Q29) | construction-era — not carried |
| D-127 | Complete the module-by-module dry-run sweep; scorecard; depends-divergence | construction-era — not carried |
| D-128 | Reconcile routine-mode's stance-marker framing to D-088 | construction-era — not carried |
| D-129 | Reconcile dependency-discipline to depends: core / L2 (target-axis discriminator) | carried → ADR-0062 |
| D-130 | Reconcile every designed-module status section to current truth | construction-era — not carried |
| D-131 | Slim module status sections to one-line pointers | construction-era — not carried |
| D-132 | Own the engine-label scheme in control-plane; resolve Q28 | engine-canon (eADR-0021) |
| D-133 | Type the cron audit persona: role-to-trigger spine, the audit role; resolve Q29 | collapsed into ADR-0022 |
| D-134 | Pin the §15 weakening-merge consent as a distinct deliberate acknowledgment (Q22) | engine-canon (eADR-0011) |
| D-135 | Re-verify unblocked modules; board config = gitignored data + committed schema | engine-canon (eADR-0003, eADR-0009) |
| D-136 | Re-base bootstrap trust on the sole non-engineer gate-holder; one consent-on-evidence gate (§17) | engine-canon (eADR-0013) |
| D-137 | Clear residual dry-run nits; remove the module Status sections | construction-era — not carried |
| D-138 | Lock validators-core: the second module lock | construction-era — not carried |
| D-139 | Lock memory-substrate-sqlite-fts5: the third module lock | construction-era — not carried |
| D-140 | Lock routine-mode: fourth module lock; correct two permission-posture platform facts | construction-era — not carried |
| D-141 | Lock product-design: fifth lock; conform the operator-surface leak; resolve Q30 | collapsed into ADR-0058 |
| D-142 | Lock migration-discipline: the sixth module lock | construction-era — not carried |
| D-143 | Lock the external-contribution module: the seventh module lock | construction-era — not carried |
| D-144 | Conclude the packaging-lock sweep: six locked, five deferred; open Q32–Q35 | construction-era — not carried |
| D-145 | Resolve Q32: keep the locked persona-file agent realization | engine-canon (eADR-0010) |
| D-146 | Resolve Q33: GitHub Actions default audit substrate, swappable at the delivery layer | collapsed into ADR-0022 |
| D-147 | Lock design-review and qa-review: the eighth and ninth module locks | construction-era — not carried |
| D-148 | Lock audit-library: tenth module lock; substrate-realization honesty remediation | construction-era — not carried |
| D-149 | Lock github-projects-sync: eleventh lock; fix the Projects-v2 platform facts (Q34) | construction-era — not carried |
| D-150 | Lock dependency-discipline: twelfth/final v1 module lock; resolve Q35 | engine-canon (eADR-0011) |
| D-151 | Whole-corpus design audit: re-litigate state (AF-1); defer the nit backlog | construction-era — not carried |
| D-152 | Resolve Q15: author the pre-release acceptance benchmark | construction-era — not carried |
| D-153 | Clear the deferred nit backlog: one batched re-litigation of eight cosmetic nits | construction-era — not carried |
| D-154 | Capstone re-run: re-litigate attention (S4, the AF-1 twin) + name the recent-decisions source | construction-era — not carried |
| D-155 | Declare engine-template v1's design build-ready | construction-era — not carried |
| D-156 | Name the execution substrate: a group-scoped uv-managed Python tool-runtime | engine-canon (eADR-0027) |
| D-157 | Comprehensive cold audit of the D-156 change-set; re-lock the eight foundations | construction-era — not carried |
| D-158 | Refine the tool-runtime keying: dependency-group named by module id, normalized | engine-canon (eADR-0027) |
| D-159 | Re-affirm engine-template v1 build-ready (lift the provisional status) | construction-era — not carried |
| D-160 | Authoring-rule-1 cleanup: rewrite the stage-0 §8 engine-mechanic note | construction-era — not carried |
| D-161 | Relocate core-build-roadmap into engine-planning/wbs | construction-era — not carried |
| D-162 | Construction-scaffold flexibility for AI stepwise-build failure modes | construction-era — not carried |
| D-163 | Correct D-162: S-8 is build-conformance deviation, not litigation alarm | construction-era — not carried |
| D-164 | Surgical coupling pass on core-build-roadmap; grammar slices OG/SG | construction-era — not carried |
| D-165 | Part-validation audit of D-164 coupling pass; seven fixes | construction-era — not carried |
| D-166 | Triage #42: per-project attention tuning is a post-v1 design gap (Q17) | engine-canon (eADR-0028) |
| D-167 | Authorize per-project operator-override of policy tuning values | carried → ADR-0053 |
| D-168 | Resolve policy-override re-litigation; six foundations re-locked | construction-era — not carried |
| D-169 | Foundational eADR canon: the Engine ships its own why | carried → ADR-0054 |
| D-170 | Resolve eADR-canon re-litigation; five foundations re-locked | construction-era — not carried |
| D-171 | Correct falsified "platform ignores PreToolUse deny" claim | engine-canon (eADR-0005) |
| D-172 | Resolve deny-claim correction; capability-discovery; modes+hooks re-locked | engine-canon (eADR-0005, eADR-0011) |
| D-173 | Open Q37: post-v1 optional hackathon divergent-exploration module | construction-era — not carried |
| D-174 | Memory & validators-core are hand-governed Builder-A builds | construction-era — not carried |
| D-175 | Correct D-174 validators-core timing: online mid-core | construction-era — not carried |
| D-176 | Sharpen D-175: module lands mid-core, corpus accretes | construction-era — not carried |
| D-177 | Carve native plan file out of the modes Explore write-gate | engine-canon (eADR-0024) |
| D-178 | Resolve plan-file carve-out; marker-not-path key; modes re-locked | construction-era — not carried |
| D-179 | Augment interactive Build entry with plan-acceptance | engine-canon (eADR-0024) |
| D-180 | Resolve Build-entry augment; four docs re-locked | construction-era — not carried |
| D-181 | Correct non-existent GitHub scope admin:repo_ruleset | engine-canon (eADR-0021) |
| D-182 | Resolve scope-name correction; three docs re-locked | construction-era — not carried |
| D-183 | Issue-authoring grammar: template sections + body contract + follow-the-host | carried → ADR-0030 |
| D-184 | Resolve issue-authoring grammar; build-orchestration joins re-lock | construction-era — not carried |
| D-185 | Ship a native plan-mode default that yields | carried → ADR-0042 |
| D-186 | Resolve plan-mode-default; two foundations re-locked | construction-era — not carried |
| D-187 | Operator-presentation relay: AI chat is sole operator channel | carried → ADR-0043 |
| D-188 | Resolve operator-presentation relay; five docs re-locked | construction-era — not carried |
| D-189 | Operator-checkout boundary: worktree isolation + strand detection | carried → ADR-0044 |
| D-190 | Resolve operator-checkout boundary; five docs re-locked | construction-era — not carried |
| D-191 | Widen product-knowledge-graph derivation source | carried → ADR-0063 |
| D-192 | Authorize the conduct surface: codes of conduct | engine-canon (eADR-0030) |
| D-193 | Resolve conduct-surface re-litigation; surface lands designed | construction-era — not carried |
| D-194 | Resolve Q36: engine release-cut / version-production process | carried → ADR-0045 |
| D-195 | Ratify (lock) the conduct surface | construction-era — not carried |
| D-196 | Standing-situation pointer advanced by build-orchestration | moot — build diverged |
| D-197 | Resolve D-196 pointer re-litigation; two docs re-locked | moot — build diverged |
| D-198 | "Where we are" is assembled read-only from GitHub | engine-canon (eADR-0031, eADR-0033) |
| D-199 | Resolve standing-situation correction; three docs re-locked | construction-era — not carried |
| D-200 | model-auto skills not cold-start-typeable; flip /engine-status to operator-typed | carried → ADR-0051 |
| D-201 | Resolve D-200 status-verb re-litigation; skills + modules/core re-locked | construction-era — not carried |
| D-202 | Reconcile stale D2 deviations row to current operator-typed verb set | construction-era — not carried |
| D-203 | Enrich derived knowledge-graph schema under a durable four-gate rule | carried → ADR-0019 |
| D-204 | Complete core-build-roadmap retirement as deletion; validate.py green | construction-era — not carried |
| D-205 | Pin offline-cache committer: audit-digest pass commits state.json as freight | carried → ADR-0021 |
| D-206 | Resolve D-205: cold audit, state + audits re-locked | construction-era — not carried |
| D-207 | Dependabot PR-contract exemption: CI-author applicability boundary on the completeness check | carried → ADR-0025 |
| D-208 | Resolve D-207: cold audit, five docs re-locked | construction-era — not carried |
| D-209 | Ledger compaction: rebuild-and-swap + audit-gated erasure | carried → ADR-0015 |
| D-210 | Resolve D-209: cold audit, four docs re-locked | construction-era — not carried |
| D-211 | Security-floor extension: native CodeQL, PVR, seeded SECURITY.md | carried → ADR-0031 |
| D-212 | Resolve D-211: cold audit, two docs re-locked | construction-era — not carried |
| D-213 | Root README as seeded-then-ceded landing front | carried → ADR-0032 |
| D-214 | Resolve D-213: cold audit, two docs re-locked | construction-era — not carried |
| D-215 | Operator-prose register: law-as-rubric + audit doc-probe teeth | engine-canon (eADR-0028) |
| D-216 | Resolve D-215: cold audit, two docs re-locked | construction-era — not carried |
| D-217 | §19 derived-committed artifacts source-deterministic; integrate regenerates | carried → ADR-0004 |
| D-218 | Resolve D-217: cold audit, three docs re-locked | construction-era — not carried |
| D-219 | First-run travel-safety: retire-set reference-closure invariant + hard CI check | carried → ADR-0033 |
| D-220 | Resolve D-219: cold audit, four docs re-locked | construction-era — not carried |
| D-221 | First-run LICENSE-clear: reconcile the traveled template LICENSE | collapsed into ADR-0005 |
| D-222 | Resolve D-221: cold audit, two docs re-locked | construction-era — not carried |
| D-223 | Reconcile knowledge boot-slice committed→gitignored one-word fix | construction-era — not carried |
| D-224 | Structural-neighbors render traverses reverse adjacency; opens Q38/Q39 | carried → ADR-0018 |
| D-225 | Recenter on "the AI is the thing made trustworthy"; end banned-word-lists | carried → ADR-0007 |
| D-226 | Extend audits doc-probe to operator-facing tool strings | engine-canon (eADR-0028) |
| D-227 | Resolve D-226: audits re-locked | construction-era — not carried |
| D-228 | Pin behavioral-demonstration shape and lifecycle | carried → ADR-0008 |
| D-229 | Correct falsified Agent-SDK-credit auth claim in audit-library | carried → ADR-0022 |
| D-230 | Resolve D-229: audit-library re-locked; #175 discharged | construction-era — not carried |
| D-231 | Promote in-tool demo subcommands as governed AI-run falsification class | carried → ADR-0008 |
| D-232 | Correct D-231's offender census: 25 showcase demos, not one | moot — build diverged |
| D-233 | Audit-over-audit: feed the audit its own prior digests (corroboration only) | carried → ADR-0023 |
| D-234 | Resolve D-233: audits + audit-library re-locked | construction-era — not carried |
| D-235 | Engine-Issue conformance reroute gate: posture → block-eligible redirect | carried → ADR-0030 |
| D-236 | Resolve D-235: four docs re-locked; #208 filed | construction-era — not carried |
| D-237 | Flip memory-backup default to a shared cross-project vault | carried → ADR-0016 |
| D-238 | Resolve D-237: widened to three docs; re-locked | construction-era — not carried |
| D-239 | Reject engine-owned git-hygiene reconciler: harness exhaust out of scope | carried → ADR-0034 |
| D-240 | Reject external upstream-issue polling; GitHub-native watch + backlog surfacing | engine-canon (eADR-0028) |
| D-241 | Enable scheduled audit's off-repo memory-backup read (PAT + digest privacy gate) | collapsed into ADR-0024 |
| D-242 | Resolve D-241: re-lock audit-library+provisioning+audits | construction-era — not carried |
| D-243 | Decline public-repo saved-memory opt-in; enrich aggregate review | carried → ADR-0024 |
| D-244 | Product-design becomes spec-driven-design system; wall re-scoped FORM-vs-SEMANTIC | carried → ADR-0058 |
| D-245 | Resolve: re-lock state (milestone honest-bound) | construction-era — not carried |
| D-246 | Resolve: re-lock control-plane (spec leaves label scheme) | construction-era — not carried |
| D-247 | Resolve: re-lock build-orchestration (spec referent, build-plan→Milestones) | construction-era — not carried |
| D-248 | Resolve: re-lock qa-review (spec-conformance referent) | construction-era — not carried |
| D-249 | Resolve: re-lock design-review (advisory spec-lock invocation) | construction-era — not carried |
| D-250 | Resolve: re-lock product-design (full SDD module redesign) | carried → ADR-0058 |
| D-251 | Reject Explore-gate memory carve-out; engine supersedes harness auto-memory | carried → ADR-0017 |
| D-252 | Bind operator-runnable acceptance steps into the PR Review record | carried → ADR-0028 |
| D-253 | Resolve: re-lock control-plane (Review carries steps) | construction-era — not carried |
| D-254 | Resolve: re-lock build-orchestration (steps filler) | construction-era — not carried |
| D-255 | Engine-observable revisit triggers for two post-v1 stubs | carried → ADR-0063 |
| D-256 | Every hard check proven to bite: negative-fixture meta-check | carried → ADR-0026 |
| D-257 | Resolve: re-lock validation (meta-check law + execution model) | construction-era — not carried |
| D-258 | Resolve: re-lock check (fixture grammar + reserved namespace) | construction-era — not carried |
| D-259 | Resolve: re-lock validators-core (meta-check instance) | construction-era — not carried |
| D-260 | Resolve: re-lock core (run-one-rule entry point + core-kind fixtures) | construction-era — not carried |
| D-261 | Artifact-warrant discipline for every generated artifact | carried → ADR-0009 |
| D-262 | disposition-issue-resolution hard check | carried → ADR-0027 |
| D-263 | Resolve: re-lock validators-core (disposition check) | construction-era — not carried |
| D-264 | Pre-migration memory snapshot = retained git tag | carried → ADR-0016 |
| D-265 | Resolve: coupled re-lock memory + sqlite-fts5 bundle (snapshot tag) | construction-era — not carried |
| D-266 | §20: no construction milestone licenses an under-build | carried → ADR-0064 |
| D-267 | Clarify §20: conformance capability ships; only build-apparatus retires | collapsed into ADR-0064 |
| D-268 | §15 guarded set = enforcement-gate property, fail-safe derived roster | engine-canon (eADR-0011) |
| D-269 | Resolve Q18: collapse-when-unchanged; boot's presentation ledger | engine-canon (eADR-0033) |
| D-270 | Plan-acceptance made assistant-legible: set + inject; falsified hook claim corrected | carried → ADR-0042 |
| D-271 | Resolve: re-lock modes + hooks (acceptance augment) | construction-era — not carried |
| D-272 | Finalize 33-law eADR canon + litigated recommendation | construction-era — not carried |
| D-273 | Ambient turn-deltas excluded from recall; recall = curated records | carried → ADR-0013 |
| D-274 | Resolve: re-lock memory (recall membership) | construction-era — not carried |
| D-275 | Branch-agnostic operator-checkout strand widening (off-main + behind) | carried → ADR-0034 |
| D-276 | Resolve: re-lock provisioning + boot (strand widening) | construction-era — not carried |
| D-277 | Provisioned verdict = instantiator-presence, three-state; first-run onboarding surfacing | carried → ADR-0035 |
| D-278 | Resolve: re-lock provisioning + boot (verdict + onboarding) | construction-era — not carried |
| D-279 | Sweep curates harness-injected pseudo-turns out of fuel/pending-detection | carried → ADR-0014 |
| D-280 | Resolve: re-lock memory (fuel curation) | construction-era — not carried |
| D-281 | Engine manifest records the engine's home repository (update source + escalate target) | carried → ADR-0036 |
| D-282 | Resolve: re-lock provisioning (manifest home) | construction-era — not carried |
| D-283 | Submit-time close-linkage consistency pre-flight (re-litigates D-252) | carried → ADR-0040 |
| D-284 | Resolve: re-lock build-orchestration (detect-and-surface, disclosed defang) | carried → ADR-0040 |
| D-285 | Layer-2 erasure batching: one-or-more targets + batched-consent floor | carried → ADR-0015 |
| D-286 | Resolve: re-lock memory (erasure batching) | construction-era — not carried |
| D-287 | Spec-obligation matrix; conformance-enforcement floor travels to deployed repos | collapsed into ADR-0029 |
| D-288 | Resolve: re-lock product-design (matrix coverage leg) | construction-era — not carried |
| D-289 | Resolve: re-lock build-orchestration (floor at the merge) | construction-era — not carried |
| D-290 | Resolve: re-lock qa-review (adversarial posture folded into spec-conformance) | moot — build diverged |
| D-291 | Fifth divergence-hunter lens; spec-conformance systematic; narrow over-build | carried → ADR-0059 |
| D-292 | Resolve: re-lock qa-review (lens split) | construction-era — not carried |
| D-293 | Resolve: re-lock build-orchestration (nine lenses) | construction-era — not carried |
| D-294 | Resolve: re-lock product-design (paired-lens reconciliation) | construction-era — not carried |
| D-295 | Template license MIT → Apache-2.0 + Commons Clause; design license-agnostic | carried → ADR-0005 |
| D-296 | Audits gains standing conditional product-spec-conformance sweep (L1/L2/L3) | carried → ADR-0029 |
| D-297 | Resolve: re-lock audits (standing sweep) | construction-era — not carried |
| D-298 | Per-instance eADR namespace <project-slug>-eADR-#### | engine-canon (eADR-0017) |
| D-299 | Resolve: re-lock ontology (intra-engine identifier layer) | construction-era — not carried |
| D-300 | Resolve: re-lock contracts (two eADR populations) | construction-era — not carried |
| D-301 | Close Q41: decline legal input on Commons-Clause .engine/ binding | carried → ADR-0006 |
| D-302 | Standing foreign-LICENSE-seed detector designed | carried → ADR-0037 |
| D-303 | Resolve: re-lock repository-topology (standing exception = reviewed-PR proposal) | carried → ADR-0037 |
| D-304 | Resolve: re-lock modules/core (detector in provides; never-strand stays singular) | construction-era — not carried |
| D-305 | Resolve: re-lock provisioning (standing detector; per-era recognizer) | construction-era — not carried |
| D-306 | Resolve: re-lock boot (leftover-license surfacing + hook-enforced intent-exit) | carried → ADR-0046 |
| D-307 | Incremental consolidation: watermark sweep predicate + high-water-mark marker | carried → ADR-0014 |
| D-308 | Resolve: re-lock memory (residual recompute; swept-through semantics) | carried → ADR-0014 |
| D-309 | Grammar-and-boot cluster: recognition slice; engine- agent prefix; §15 boot alarm retired; hook-output cap | carried → ADR-0011 |
| D-310 | Resolve: re-lock ontology (coverage bound; consumption law tier) | construction-era — not carried |
| D-311 | Retire wbs/eadr-canon/ recommendation set | construction-era — not carried |
| D-312 | Resolve: re-lock boot (recognition slice; alarm retired; cap) | construction-era — not carried |
| D-313 | Resolve: re-lock agents (engine- prefix; read-only write-tool floor) | carried → ADR-0049 |
| D-314 | Attention's work-record commission superseded; backlog/Milestone read retired to the plan | collapsed into ADR-0020 |
| D-315 | Amend D-314: premise corrected; Milestone platform defect; R35 opened | collapsed into ADR-0020 |
| D-316 | Resolve: re-lock attention (commission retired from charter and inputs) | construction-era — not carried |
| D-317 | Resolve: re-lock state (milestone bound reads open set as found) | carried → ADR-0020 |
| D-318 | Resolve: re-lock github-projects-sync (board field = ranked work) | carried → ADR-0061 |
| D-319 | Resolve: re-lock boot (milestone relay + render law) | carried → ADR-0046 |
