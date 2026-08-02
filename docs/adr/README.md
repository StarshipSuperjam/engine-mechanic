# Decision records

Every decision behind the product spec, one file per decision, carried whole from the design workspace's single decision log. Each names what was decided, why, and what was ruled out — that last part is what stops a later session re-opening ground already walked.

**Numbering.** The design workspace numbered these `D-1` to `D-319`. They keep the same numbers here, written four digits: `D-24` is `0024`. Prose across the corpus still says `D-24` in places; it means the same record. Records from `0320` onward are authored in this repository, continuing the same sequence.

**These records are append-only.** The design workspace's rule, carried from the log they came from: supersede an entry with a newer one; never edit or delete a past entry.

**A note on fidelity.** These records were carried whole from the design workspace, with two deliberate exceptions. Three carry a marked editorial note where a present-tense claim about a live system was later corrected or fixed. A small number had passages edited before publication to remove appraisals of third-party work and internal project metrics; the decisions and their reasoning are unchanged. The design workspace those originals lived in has since been retired ([decision 0320](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md)); this note is the durable record that the edits were made.

**What is not here.** These records were written alongside build-planning material (a `wbs/` directory) and a lock registry that were deliberately not carried across. Where a record refers to one of those by name, the reference is left as plain text rather than a link, because the file does not exist in this repository. Titles below are shortened where long; each record's own heading carries the full title.

| # | Decision | Date |
| --- | --- | --- |
| 0001 | [Restart engine-template in a blank repo](0001-restart-engine-template-in-a-blank-repo.md) | 2026-05-22 |
| 0002 | [Proposal and prototype are reference inputs, not gospel](0002-proposal-and-prototype-are-reference-inputs-not-gospel.md) | 2026-05-22 |
| 0003 | [Specify the full end-state before the first build PR](0003-specify-the-full-end-state-before-the-first-build-pr.md) | 2026-05-22 |
| 0004 | [Establish the engine-planning workspace with a fixed documentation discipline](0004-establish-the-engine-planning-workspace-with-a-fixed-documen.md) | 2026-05-22 |
| 0005 | [Distribution model is "Use this template"](0005-distribution-model-is-use-this-template.md) | 2026-05-22 |
| 0006 | [Nine non-modular foundations](0006-nine-non-modular-foundations.md) | 2026-05-22 |
| 0007 | [Memory data is local and gitignored; substrate ships empty](0007-memory-data-is-local-and-gitignored-substrate-ships-empty.md) | 2026-05-22 |
| 0008 | [Memory and knowledge are distinct substrates](0008-memory-and-knowledge-are-distinct-substrates.md) | 2026-05-22 |
| 0009 | [Telemetry is a remediation loop, not self-healing](0009-telemetry-is-a-remediation-loop-not-self-healing.md) | 2026-05-22 |
| 0010 | [Attention is a first-class surface](0010-attention-is-a-first-class-surface.md) | 2026-05-22 |
| 0011 | [Knowledge-graph state is derived, not hand-authored](0011-knowledge-graph-state-is-derived-not-hand-authored.md) | 2026-05-22 |
| 0012 | [Provisioning is two subsystems on one manifest grammar; modules declare wiring](0012-provisioning-is-two-subsystems-on-one-manifest-grammar-modul.md) | 2026-05-22 |
| 0013 | [The control-plane bootstrap must travel and fail loud](0013-the-control-plane-bootstrap-must-travel-and-fail-loud.md) | 2026-05-22 |
| 0014 | [A lightweight validate.py for the planning workspace](0014-a-lightweight-validate-py-for-the-planning-workspace.md) | 2026-05-22 |
| 0015 | [Adopt a locked-status mechanism with a litigation alarm](0015-adopt-a-locked-status-mechanism-with-a-litigation-alarm.md) | 2026-05-22 |
| 0016 | [Repository topology as a foundational substrate; product-owns-root wall; laws not leaves](0016-repository-topology-as-a-foundational-substrate-product-owns.md) | 2026-05-22 |
| 0017 | [Control-plane locked end-state, as contracts not leaves](0017-control-plane-locked-end-state-as-contracts-not-leaves.md) | 2026-05-22 |
| 0018 | [Cold-session design audit required before any lock](0018-cold-session-design-audit-required-before-any-lock.md) | 2026-05-22 |
| 0019 | [Authoring grammar locked end-state, as laws not leaves](0019-authoring-grammar-locked-end-state-as-laws-not-leaves.md) | 2026-05-22 |
| 0020 | [Engine instance identifiers are engine-namespaced; decision records are `eADR-####`](0020-engine-instance-identifiers-are-engine-namespaced-decision-r.md) | 2026-05-22 |
| 0021 | [GitHub Projects ships as an optional adopter-facing module, projecting repo-authoritative state](0021-github-projects-ships-as-an-optional-adopter-facing-module-p.md) | 2026-05-22 |
| 0022 | [Hooks locked as foundation #11, as laws not leaves](0022-hooks-locked-as-foundation-11-as-laws-not-leaves.md) | 2026-05-22 |
| 0023 | [Check system locked: validator architecture, the `check` surface, and the suite/trigger grammar](0023-check-system-locked-validator-architecture-the-check-surface.md) | 2026-05-22 |
| 0024 | [The engine is upgradeable: versioned packages, upgraded by overlaying tagged template releases](0024-the-engine-is-upgradeable-versioned-packages-upgraded-by-ove.md) | 2026-05-22 |
| 0025 | [Fault-containment is earned at the seams, not conferred by modularity](0025-fault-containment-is-earned-at-the-seams-not-conferred-by-mo.md) | 2026-05-23 |
| 0026 | [The Engine is an embedded team member (contributor, not component); asymmetric awareness](0026-the-engine-is-an-embedded-team-member-contributor-not-compon.md) | 2026-05-23 |
| 0027 | [Topology admits root `.mcp.json` as a tool-dictated slot (re-litigation of locked topology)](0027-topology-admits-root-mcp-json-as-a-tool-dictated-slot-re-lit.md) | 2026-05-23 |
| 0028 | [Module system locked end-state, as laws not leaves](0028-module-system-locked-end-state-as-laws-not-leaves.md) | 2026-05-23 |
| 0029 | [Cognitive substrate is one workflow: a 2-store/1-register/1-cursor/2-function decomposition, consulted by push](0029-cognitive-substrate-is-one-workflow-a-2-store-1-register-1-c.md) | 2026-05-23 |
| 0030 | [Memory: ledger-canonical, observe-don't-predict capture, lexical floor + semantic module, and the built-in-au…](0030-memory-ledger-canonical-observe-don-t-predict-capture-lexica.md) | 2026-05-23 |
| 0031 | [Integration debt is a telemetry-owned register, not a knowledge entity; knowledge regen rides the commit boun…](0031-integration-debt-is-a-telemetry-owned-register-not-a-knowled.md) | 2026-05-23 |
| 0032 | [Re-litigation: bind `UserPromptSubmit` to the orientation scent (locked hooks re-lock)](0032-re-litigation-bind-userpromptsubmit-to-the-orientation-scent.md) | 2026-05-23 |
| 0033 | [Ground the cognitive substrate in established standards (lineage, honest novelty, leak guard)](0033-ground-the-cognitive-substrate-in-established-standards-line.md) | 2026-05-24 |
| 0034 | [Re-litigation: hooks block-budget example retargeted off the dissolved eager-claim](0034-re-litigation-hooks-block-budget-example-retargeted-off-the.md) | 2026-05-24 |
| 0035 | [Re-litigation: policies retargets the contract-threshold narrative sink and the routine tracked-finding locat…](0035-re-litigation-policies-retargets-the-contract-threshold-narr.md) | 2026-05-24 |
| 0036 | [Re-litigation: contracts retargets the default session-narrative sink off the dissolved changelog](0036-re-litigation-contracts-retargets-the-default-session-narrat.md) | 2026-05-24 |
| 0037 | [Graveyard exemption: the append-only decision-log may link retired docs](0037-graveyard-exemption-the-append-only-decision-log-may-link-re.md) | 2026-05-24 |
| 0038 | [Session lifecycle re-founded on native substrates](0038-session-lifecycle-re-founded-on-native-substrates.md) | 2026-05-24 |
| 0039 | [Reports & self-improvement scope: Engine-only self-monitoring on a judgment ladder](0039-reports-self-improvement-scope-engine-only-self-monitoring-o.md) | 2026-05-24 |
| 0040 | [Telemetry designed end-state: native signal-of-record; tracked debt is engine-labeled GitHub Issues](0040-telemetry-designed-end-state-native-signal-of-record-tracked.md) | 2026-05-24 |
| 0041 | [Audits designed state: a purpose-built adversarial self-review, distilled from the prototype](0041-audits-designed-state-a-purpose-built-adversarial-self-revie.md) | 2026-05-24 |
| 0042 | [Procedural / content / grounding surface cluster designed; the boundary law and the derived-binding principle](0042-procedural-content-grounding-surface-cluster-designed-the-bo.md) | 2026-05-24 |
| 0043 | [Surface-set completion: re-lock ontology and hooks to clear the resolved surface-set question](0043-surface-set-completion-re-lock-ontology-and-hooks-to-clear-t.md) | 2026-05-25 |
| 0044 | [Re-lock validation and check: a check-kind binds by presence (§14), and is not an interface](0044-re-lock-validation-and-check-a-check-kind-binds-by-presence.md) | 2026-05-25 |
| 0045 | [Re-lock contracts: a specification is a doc-nature, not a catalogued surface](0045-re-lock-contracts-a-specification-is-a-doc-nature-not-a-cata.md) | 2026-05-25 |
| 0046 | [Harness comparative mining: a guardrail-integrity gap, a contract-hardening directive, and two anti-choices](0046-harness-comparative-mining-a-guardrail-integrity-gap-a-contr.md) | 2026-05-25 |
| 0047 | [Product-spec intake: design it native, not bundled; the build-the-Engine path stays native too](0047-product-spec-intake-design-it-native-not-bundled-the-build-t.md) | 2026-05-25 |
| 0048 | [Provisioning & delivery designed end-state: brownfield-capable grammar, greenfield-first build order](0048-provisioning-delivery-designed-end-state-brownfield-capable.md) | 2026-05-25 |
| 0049 | [Re-lock topology and module-system: file-precise CODEOWNERS ownership and the coherence infra-artifact carve-…](0049-re-lock-topology-and-module-system-file-precise-codeowners-o.md) | 2026-05-25 |
| 0050 | [hermes-interprets-coala mining: a lineage-precision question; CoALA-as-narration rejected](0050-hermes-interprets-coala-mining-a-lineage-precision-question.md) | 2026-05-25 |
| 0051 | [Guardrail integrity: the builder cannot silently weaken its own enforcement (principle §15)](0051-guardrail-integrity-the-builder-cannot-silently-weaken-its-o.md) | 2026-05-25 |
| 0052 | [Foundational law layer closed; the implementation lock-order runway](0052-foundational-law-layer-closed-the-implementation-lock-order.md) | 2026-05-25 |
| 0053 | [Procedural surfaces reconciled to the merged Claude Code skill mechanism (commands ⊂ skills)](0053-procedural-surfaces-reconciled-to-the-merged-claude-code-ski.md) | 2026-05-25 |
| 0054 | [Lock the `operations` and `docs` surfaces (Wave 1 partial)](0054-lock-the-operations-and-docs-surfaces-wave-1-partial.md) | 2026-05-25 |
| 0055 | [Collapse `command` into the `skill` surface: invocation is a governed axis, not a surface](0055-collapse-command-into-the-skill-surface-invocation-is-a-gove.md) | 2026-05-25 |
| 0056 | [Lock the `tools` surface (Wave 1)](0056-lock-the-tools-surface-wave-1.md) | 2026-05-25 |
| 0057 | [Lock the `agents` surface (Wave 1); four settled design forks](0057-lock-the-agents-surface-wave-1-four-settled-design-forks.md) | 2026-05-25 |
| 0058 | [Discharge the Wave-0 gate (Q10): substrate-content world-tagging is misattributed to the module grammar](0058-discharge-the-wave-0-gate-q10-substrate-content-world-taggin.md) | 2026-05-25 |
| 0059 | [Lock the `state` system (Wave-2 head): the committed cursor, reconciled to native substrates](0059-lock-the-state-system-wave-2-head-the-committed-cursor-recon.md) | 2026-05-25 |
| 0060 | [Lock the `knowledge` system (Wave-2): the purely-derived structural store; Q16 sharpened](0060-lock-the-knowledge-system-wave-2-the-purely-derived-structur.md) | 2026-05-25 |
| 0061 | [Lock the `memory` system (Wave-2): the episodic ledger store; Q3 backup-path resolved](0061-lock-the-memory-system-wave-2-the-episodic-ledger-store-q3-b.md) | 2026-05-25 |
| 0062 | [Lock the `attention` system (Wave-2): the policy-plus-function prioritizer, reads-never-owns](0062-lock-the-attention-system-wave-2-the-policy-plus-function-pr.md) | 2026-05-25 |
| 0063 | [Lock the `boot` / orientation system (Wave-2, terminal): the integration point that honors its substrates' de…](0063-lock-the-boot-orientation-system-wave-2-terminal-the-integra.md) | 2026-05-25 |
| 0064 | [Lock the `interfaces` surface (final Wave-2 lock): single-active polymorphism with a named, never-silent fall…](0064-lock-the-interfaces-surface-final-wave-2-lock-single-active.md) | 2026-05-25 |
| 0065 | [Product-design front door: design the Q14 intake module as a native, product-layer referent producer](0065-product-design-front-door-design-the-q14-intake-module-as-a.md) | 2026-05-26 |
| 0066 | [The 4+4 review-lens roster: two stage-suites mirroring the engine's own cold-session audit](0066-the-4-4-review-lens-roster-two-stage-suites-mirroring-the-en.md) | 2026-05-26 |
| 0067 | [Operator-facing module packaging: industry-discipline categories; core is never an install choice](0067-operator-facing-module-packaging-industry-discipline-categor.md) | 2026-05-26 |
| 0068 | [Q1 resolved: the v1 optional-module roster (4 cut, 2 kept)](0068-q1-resolved-the-v1-optional-module-roster-4-cut-2-kept.md) | 2026-05-26 |
| 0069 | [Core/module seam-walk: the demarcation operationalized (glossary), the v1 sort confirmed](0069-core-module-seam-walk-the-demarcation-operationalized-glossa.md) | 2026-05-26 |
| 0070 | [Lock the `modes` system (Wave 3 head): three stances on two axes, an honest fallible Explore gate, session-sc…](0070-lock-the-modes-system-wave-3-head-three-stances-on-two-axes.md) | 2026-05-26 |
| 0071 | [Re-lock `modes`: doc-level cold audit corrects an as-written resume-resurrection overclaim and a dangling sea…](0071-re-lock-modes-doc-level-cold-audit-corrects-an-as-written-re.md) | 2026-05-26 |
| 0072 | [Lock the `close` system (Wave 3): the turn-`Stop` ritual — honest-tier finding-disposition gate over an ephem…](0072-lock-the-close-system-wave-3-the-turn-stop-ritual-honest-tie.md) | 2026-05-26 |
| 0073 | [Lock `build-orchestration` (Wave 3, terminal) and re-litigate `control-plane` to add the gated **Review** PR-…](0073-lock-build-orchestration-wave-3-terminal-and-re-litigate-con.md) | 2026-05-26 |
| 0074 | [Sweep the stale `Q1` references resolved by D-066/D-068 (re-lock `module-system` and `agents`)](0074-sweep-the-stale-q1-references-resolved-by-d-066-d-068-re-loc.md) | 2026-05-26 |
| 0075 | [Lock the `telemetry` system (guardrails arc head): the triage-volume bound is structural, not a cap](0075-lock-the-telemetry-system-guardrails-arc-head-the-triage-vol.md) | 2026-05-26 |
| 0076 | [Lock the `audits` system, re-founded for the deployed-repo HYGIENE case; tuning deferred to a future optional…](0076-lock-the-audits-system-re-founded-for-the-deployed-repo-hygi.md) | 2026-05-26 |
| 0077 | [Lock the `provisioning` system (terminal foundation lock): the bootstrap-paradox subsystem, reworked by a two…](0077-lock-the-provisioning-system-terminal-foundation-lock-the-bo.md) | 2026-05-26 |
| 0078 | [Citation-accuracy re-litigation: repoint stale `Q4` references in three locked docs to provisioning's build-s…](0078-citation-accuracy-re-litigation-repoint-stale-q4-references.md) | 2026-05-26 |
| 0079 | [Name the deferral seam: a new descriptive principle §16 (the ownership-axis sibling of §14)](0079-name-the-deferral-seam-a-new-descriptive-principle-16-the-ow.md) | 2026-05-26 |
| 0080 | [Re-litigate `state` (honesty): name the floor's known-unbounded faults; harden the stale-count rendering agai…](0080-re-litigate-state-honesty-name-the-floor-s-known-unbounded-f.md) | 2026-05-27 |
| 0081 | [Re-litigate `memory`: ledger write-integrity law; reframe usage-importance to cued-recall + recoverability; F…](0081-re-litigate-memory-ledger-write-integrity-law-reframe-usage.md) | 2026-05-27 |
| 0082 | [Re-litigate `knowledge` (honesty): R8 hub-explosion is *deferred behind a swappable seam*, not *mitigated*](0082-re-litigate-knowledge-honesty-r8-hub-explosion-is-deferred-b.md) | 2026-05-27 |
| 0083 | [Re-litigate `attention` (honesty/clarification): reference-time as an explicit determinism input; "right thin…](0083-re-litigate-attention-honesty-clarification-reference-time-a.md) | 2026-05-27 |
| 0084 | [Re-litigate `boot` (+ constraints): correct the post-compaction platform fact; soften "unconditional" to floo…](0084-re-litigate-boot-constraints-correct-the-post-compaction-pla.md) | 2026-05-27 |
| 0085 | [Record the cognitive-substrate efficacy-scorecard exercise (workspace process); route its acceptance gates an…](0085-record-the-cognitive-substrate-efficacy-scorecard-exercise-w.md) | 2026-05-27 |
| 0086 | [Cognitive foundations-as-required-packages reconciliation: memory floor its own `required` package, knowledge…](0086-cognitive-foundations-as-required-packages-reconciliation-me.md) | 2026-05-27 |
| 0087 | [Resolve Q7 (v1 skill membership); close deviation D2; the WBS deviation-gate clears](0087-resolve-q7-v1-skill-membership-close-deviation-d2-the-wbs-de.md) | 2026-05-27 |
| 0088 | [Justified re-litigation: name the routine-entry command `/engine-routine` in `modes` + `build-orchestration`…](0088-justified-re-litigation-name-the-routine-entry-command-engin.md) | 2026-05-27 |
| 0089 | [Flesh the `core` module doc to `designed`: the kernel partition, the validation engine/corpus seam, foundatio…](0089-flesh-the-core-module-doc-to-designed-the-kernel-partition-t.md) | 2026-05-27 |
| 0090 | [Flesh the `validators-core` module doc to `designed`: the engine-self-validation rule corpus, consolidated, d…](0090-flesh-the-validators-core-module-doc-to-designed-the-engine.md) | 2026-05-27 |
| 0091 | [Flesh the `memory-substrate-sqlite-fts5` module doc to `designed`: the memory floor, the `search` implementat…](0091-flesh-the-memory-substrate-sqlite-fts5-module-doc-to-designe.md) | 2026-05-27 |
| 0092 | [Flesh the `routine-mode` module doc to `designed`: the operator entry into the Routine stance, wiring nothing](0092-flesh-the-routine-mode-module-doc-to-designed-the-operator-e.md) | 2026-05-27 |
| 0093 | [Cut the `adr-discipline` module: vestigial, its content already shipped by `core` + `validators-core`](0093-cut-the-adr-discipline-module-vestigial-its-content-already.md) | 2026-05-27 |
| 0094 | [Defer the `expression-contracts` design to a dedicated session; correct `core`'s mischaracterizing carve-out](0094-defer-the-expression-contracts-design-to-a-dedicated-session.md) | 2026-05-27 |
| 0095 | [Cut `expression-contracts`; disposition prose (organization covered, internal AI-voice dropped) and re-home t…](0095-cut-expression-contracts-disposition-prose-organization-cove.md) | 2026-05-27 |
| 0096 | [Author the stage-0 build harness as the WBS bootstrap-preamble; split the engine-mechanic out as its own futu…](0096-author-the-stage-0-build-harness-as-the-wbs-bootstrap-preamb.md) | 2026-05-27 |
| 0097 | [Flesh the `dependency-discipline` module doc to `designed`: optional dependency governance as a CI-suite chec…](0097-flesh-the-dependency-discipline-module-doc-to-designed-optio.md) | 2026-05-28 |
| 0098 | [Flesh the `migration-discipline` module doc to `designed`: optional product-migration governance — discipline…](0098-flesh-the-migration-discipline-module-doc-to-designed-option.md) | 2026-05-28 |
| 0099 | [Flesh the `github-projects-sync` module doc to `designed`: native-first one-way Project-board projection over…](0099-flesh-the-github-projects-sync-module-doc-to-designed-native.md) | 2026-05-28 |
| 0100 | [Decouple the locked agent grammar from the model landscape: `model-tier` becomes a closed *demand* vocabulary…](0100-decouple-the-locked-agent-grammar-from-the-model-landscape-m.md) | 2026-05-28 |
| 0101 | [Pin the stage-0 self-construction threshold to a concrete module subset; correct the orchestrator-persona mis…](0101-pin-the-stage-0-self-construction-threshold-to-a-concrete-mo.md) | 2026-05-28 |
| 0102 | [Cross-repo external contribution as a first-class v1 operating mode (fork-native); the engine-mechanic as its…](0102-cross-repo-external-contribution-as-a-first-class-v1-operati.md) | 2026-05-28 |
| 0103 | [Cross-repo design cold audit: resolutions (engine-clean branch, build-orchestration close-model, posture hone…](0103-cross-repo-design-cold-audit-resolutions-engine-clean-branch.md) | 2026-05-28 |
| 0104 | [Phase C: cross-reference the external-contribution mode into four locked anchors (re-litigation)](0104-phase-c-cross-reference-the-external-contribution-mode-into.md) | 2026-05-28 |
| 0105 | [Hold a post-v1 `product-knowledge-graph` module stub (product-side structural knowledge)](0105-hold-a-post-v1-product-knowledge-graph-module-stub-product-s.md) | 2026-05-28 |
| 0106 | [Elaborate the external-contribution doc with the cross-repo knowledge-coverage detail and the engine-mechanic…](0106-elaborate-the-external-contribution-doc-with-the-cross-repo.md) | 2026-05-28 |
| 0107 | [Author the WBS module build-order; the builder crossover; resolve Q20 (defined point = M1; in-repo for v1, se…](0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md) | 2026-05-28 |
| 0108 | [Add the dry-run build-simulation instrument (the workspace's L1 build-readiness gate)](0108-add-the-dry-run-build-simulation-instrument-the-workspace-s.md) | 2026-05-28 |
| 0109 | [Tune the dry-run from the L0 calibration: a `deferred` disposition, reference-root handling, and the correcte…](0109-tune-the-dry-run-from-the-l0-calibration-a-deferred-disposit.md) | 2026-05-28 |
| 0110 | [Run the genesis dry-run through complete `core`; log the build-readiness blockers (Q24–Q27); secondary cross-…](0110-run-the-genesis-dry-run-through-complete-core-log-the-build.md) | 2026-05-28 |
| 0111 | [Resolve Q22/Q23: the construction repo carries no CODEOWNERS (no topology law) and a hand-seeded engine manif…](0111-resolve-q22-q23-the-construction-repo-carries-no-codeowners.md) | 2026-05-29 |
| 0112 | [Author the core-lock closure procedure (the Q24–Q27 remediation roadmap)](0112-author-the-core-lock-closure-procedure-the-q24-q27-remediati.md) | 2026-05-29 |
| 0113 | [Core-lock closure Phase 0: the build-spec-leaf form/contract convention refinement + the canonical `finding.v…](0113-core-lock-closure-phase-0-the-build-spec-leaf-form-contract.md) | 2026-05-29 |
| 0114 | [Q25 re-litigation: a fourth v1-core policy — the Triage-threshold policy (telemetry's promotion thresholds)](0114-q25-re-litigation-a-fourth-v1-core-policy-the-triage-thresho.md) | 2026-05-29 |
| 0115 | [Q27 #1 re-litigation: the validation kind-callable result contract (pass/fail over finding.v1)](0115-q27-1-re-litigation-the-validation-kind-callable-result-cont.md) | 2026-05-29 |
| 0116 | [Q27 #3 re-litigation: the knowledge-retrieval interface operation set + the consumer-composed memory link](0116-q27-3-re-litigation-the-knowledge-retrieval-interface-operat.md) | 2026-05-29 |
| 0117 | [Q24 + Q27 #2 re-litigation: the attention ranking-function form (ordered partition + weighted) and the scent…](0117-q24-q27-2-re-litigation-the-attention-ranking-function-form.md) | 2026-05-29 |
| 0118 | [Q27 #4 + #5 re-litigation: the telemetry finding-record + ambient-capture record shapes; Q27 closed](0118-q27-4-5-re-litigation-the-telemetry-finding-record-ambient-c.md) | 2026-05-29 |
| 0119 | [Resolve Q26: pin the `/engine-help` verb-index + kind-discovery mechanisms as `core` build-spec leaves (no al…](0119-resolve-q26-pin-the-engine-help-verb-index-kind-discovery-me.md) | 2026-05-29 |
| 0120 | [Lock `core` (the root module): the closure wave's terminal ratification; retire the closure procedure](0120-lock-core-the-root-module-the-closure-wave-s-terminal-ratifi.md) | 2026-05-29 |
| 0121 | [Lock the `external-contribution` system doc; reconcile the stale pending-seam wording; defer the module-packa…](0121-lock-the-external-contribution-system-doc-reconcile-the-stal.md) | 2026-05-29 |
| 0122 | [Enumerate the branch-ruleset protection floor in control-plane (re-litigation + re-lock)](0122-enumerate-the-branch-ruleset-protection-floor-in-control-pla.md) | 2026-05-29 |
| 0123 | [Run the L2 dry-run (validators-core + memory-substrate, both build-ready); harden the instrument with the cal…](0123-run-the-l2-dry-run-validators-core-memory-substrate-both-bui.md) | 2026-05-29 |
| 0124 | [Dry-run the `routine-mode` module build step (BUILD-READY); surface one designed-doc contradiction to remedia…](0124-dry-run-the-routine-mode-module-build-step-build-ready-surfa.md) | 2026-05-29 |
| 0125 | [Dry-run the `product-design` module: NOT build-ready — a cross-cutting engine-label ownership gap; LITIGATION…](0125-dry-run-the-product-design-module-not-build-ready-a-cross-cu.md) | 2026-05-29 |
| 0126 | [Dry-run the `audit-library` module: NOT build-ready — the audit persona is untypeable in the locked agents gr…](0126-dry-run-the-audit-library-module-not-build-ready-the-audit-p.md) | 2026-05-29 |
| 0127 | [Complete the module-by-module dry-run sweep (design-review · qa-review · github-projects-sync · migration-dis…](0127-complete-the-module-by-module-dry-run-sweep-design-review-qa.md) | 2026-05-29 |
| 0128 | [Reconcile routine-mode's stance-marker framing to D-088 (the entry does not set the activating signal)](0128-reconcile-routine-mode-s-stance-marker-framing-to-d-088-the.md) | 2026-05-29 |
| 0129 | [Reconcile dependency-discipline to `depends: core` / L2 (the target-axis discriminator, applied)](0129-reconcile-dependency-discipline-to-depends-core-l2-the-targe.md) | 2026-05-29 |
| 0130 | [Reconcile every designed-module status section to current truth (post-`core`-lock, post-WBS, the dry-run-swee…](0130-reconcile-every-designed-module-status-section-to-current-tr.md) | 2026-05-29 |
| 0131 | [Slim module status sections to one-line pointers (the prose status block was a rot-prone derivative)](0131-slim-module-status-sections-to-one-line-pointers-the-prose-s.md) | 2026-05-29 |
| 0132 | [Own the engine-label scheme in control-plane (re-litigation + re-lock); resolve Q28](0132-own-the-engine-label-scheme-in-control-plane-re-litigation-r.md) | 2026-05-29 |
| 0133 | [Type the cron-fired audit persona: re-litigate `agents` (role⇒trigger spine, the `audit` role) and reconcile…](0133-type-the-cron-fired-audit-persona-re-litigate-agents-role-tr.md) | 2026-05-29 |
| 0134 | [Resolve Q22: pin the §15 weakening-merge consent as a distinct, deliberate acknowledgment (re-litigate + re-l…](0134-resolve-q22-pin-the-15-weakening-merge-consent-as-a-distinct.md) | 2026-05-30 |
| 0135 | [Re-verify the three D-132/D-133-unblocked modules; resolve github-projects-sync's board-config coherence-home…](0135-re-verify-the-three-d-132-d-133-unblocked-modules-resolve-gi.md) | 2026-05-30 |
| 0136 | [Re-base the bootstrap trust model on a sole non-engineer gate-holder; one informed-consent-on-evidence model…](0136-re-base-the-bootstrap-trust-model-on-a-sole-non-engineer-gat.md) | 2026-05-30 |
| 0137 | [Clear the residual dry-run designed-doc precision nits and remove the now-empty module Status sections (pre-l…](0137-clear-the-residual-dry-run-designed-doc-precision-nits-and-r.md) | 2026-05-30 |
| 0138 | [Lock `validators-core` (the base self-validation rule corpus): the second module lock](0138-lock-validators-core-the-base-self-validation-rule-corpus-th.md) | 2026-05-30 |
| 0139 | [Lock `memory-substrate-sqlite-fts5` (the memory floor): the third module lock; fold the `.mcp.json` project-d…](0139-lock-memory-substrate-sqlite-fts5-the-memory-floor-the-third.md) | 2026-05-30 |
| 0140 | [Lock `routine-mode` (the unattended-Routine entry): the fourth module lock; correct two permission-posture pl…](0140-lock-routine-mode-the-unattended-routine-entry-the-fourth-mo.md) | 2026-05-30 |
| 0141 | [Lock `product-design` (the design front door): the fifth module lock; conform an operator-surface leak to loc…](0141-lock-product-design-the-design-front-door-the-fifth-module-l.md) | 2026-05-30 |
| 0142 | [Lock `migration-discipline` (product-migration governance): the sixth module lock](0142-lock-migration-discipline-product-migration-governance-the-s.md) | 2026-05-30 |
| 0143 | [Lock the `external-contribution` module (the cross-repo packaging): the seventh module lock](0143-lock-the-external-contribution-module-the-cross-repo-packagi.md) | 2026-05-30 |
| 0144 | [Conclude the module packaging-lock sweep: six modules locked, five deferred to focused passes; open Q32–Q35 t…](0144-conclude-the-module-packaging-lock-sweep-six-modules-locked.md) | 2026-05-30 |
| 0145 | [Resolve Q32: keep the locked persona-file agent realization (no locked-doc edit); clear the design-review / q…](0145-resolve-q32-keep-the-locked-persona-file-agent-realization-n.md) | 2026-05-30 |
| 0146 | [Resolve Q33: GitHub Actions stays the default audit substrate, with a delivery-layer reframe and Cloud Routin…](0146-resolve-q33-github-actions-stays-the-default-audit-substrate.md) | 2026-05-30 |
| 0147 | [Lock the design-review and qa-review suites (the v1 review-lens roster): the eighth and ninth module locks](0147-lock-the-design-review-and-qa-review-suites-the-v1-review-le.md) | 2026-05-30 |
| 0148 | [Lock `audit-library` (the engine self-audit delivery): the tenth module lock; remediate the substrate-realiza…](0148-lock-audit-library-the-engine-self-audit-delivery-the-tenth.md) | 2026-05-30 |
| 0149 | [Lock `github-projects-sync` (the board projection): the eleventh module lock; remediate the Projects-v2 platf…](0149-lock-github-projects-sync-the-board-projection-the-eleventh.md) | 2026-05-30 |
| 0150 | [Lock `dependency-discipline` (the dependency-governance discipline): the twelfth and final v1 module lock; re…](0150-lock-dependency-discipline-the-dependency-governance-discipl.md) | 2026-05-30 |
| 0151 | [Whole-corpus design audit: re-litigate `state` (AF-1) to fix the degraded-work consent-gate attribution; anno…](0151-whole-corpus-design-audit-re-litigate-state-af-1-to-fix-the.md) | 2026-05-30 |
| 0152 | [Resolve Q15: author the pre-release acceptance benchmark (the third build-readiness instrument)](0152-resolve-q15-author-the-pre-release-acceptance-benchmark-the.md) | 2026-05-30 |
| 0153 | [Clear the deferred nit backlog: one batched re-litigation of eight cosmetic locked-doc nits from the D-151 co…](0153-clear-the-deferred-nit-backlog-one-batched-re-litigation-of.md) | 2026-05-31 |
| 0154 | [Build-ready capstone re-run: re-litigate `attention` (S4) to fix the plan-gate-consent mis-attribution (the A…](0154-build-ready-capstone-re-run-re-litigate-attention-s4-to-fix.md) | 2026-05-31 |
| 0155 | [Declare engine-template v1's design build-ready for the first build PR (the build-ready capstone; evidence-to…](0155-declare-engine-template-v1-s-design-build-ready-for-the-firs.md) | 2026-05-31 |
| 0156 | [Name the engine's execution substrate: a group-scoped uv-managed Python tool-runtime (reopens build-ready; au…](0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md) | 2026-05-31 |
| 0157 | [Comprehensive cold audit of the D-156 tool-runtime change-set; resolve findings; re-lock the eight foundations](0157-comprehensive-cold-audit-of-the-d-156-tool-runtime-change-se.md) | 2026-05-31 |
| 0158 | [Refine D-156's tool-runtime keying: pin the module→dependency-group binding convention (group named by module…](0158-refine-d-156-s-tool-runtime-keying-pin-the-module-dependency.md) | 2026-05-31 |
| 0159 | [Re-affirm engine-template v1 build-ready: lift the D-156/D-157 provisional status (the discharged-condition r…](0159-re-affirm-engine-template-v1-build-ready-lift-the-d-156-d-15.md) | 2026-05-31 |
| 0160 | [Authoring-rule-1 cleanup: rewrite the `stage-0-harness` §8 engine-mechanic note to finished current-state](0160-authoring-rule-1-cleanup-rewrite-the-stage-0-harness-8-engin.md) | 2026-05-31 |
| 0161 | [Relocate the `core-build-roadmap` from the engine-template build repo into `engine-planning/wbs/`](0161-relocate-the-core-build-roadmap-from-the-engine-template-bui.md) | 2026-06-03 |
| 0162 | [Construction-scaffold flexibility for AI stepwise-build failure modes: coping-deferral disclosure, dependency…](0162-construction-scaffold-flexibility-for-ai-stepwise-build-fail.md) | 2026-06-03 |
| 0163 | [Correct D-162: S-8 is a build-conformance deviation (fix the build, already done), not a litigation alarm; do…](0163-correct-d-162-s-8-is-a-build-conformance-deviation-fix-the-b.md) | 2026-06-03 |
| 0164 | [Surgical coupling pass on the `core-build-roadmap`: declare cross-slice contracts at their producers + author…](0164-surgical-coupling-pass-on-the-core-build-roadmap-declare-cro.md) | 2026-06-03 |
| 0165 | [Part-validation audit of the D-164 coupling pass: faithful + locked-doc-clean; seven mechanical fixes applied…](0165-part-validation-audit-of-the-d-164-coupling-pass-faithful-lo.md) | 2026-06-03 |
| 0166 | [Triage engine-template issue #42 (per-project attention tuning): a post-v1 design gap sharpened in Q17, not a…](0166-triage-engine-template-issue-42-per-project-attention-tuning.md) | 2026-06-04 |
| 0167 | [Take up Q17 component (a): authorize a five-foundation re-litigation for a per-project operator-override of p…](0167-take-up-q17-component-a-authorize-a-five-foundation-re-litig.md) | 2026-06-04 |
| 0168 | [Resolve the D-167 operator-policy-override re-litigation: landed-text cold audit clean, six foundations re-lo…](0168-resolve-the-d-167-operator-policy-override-re-litigation-lan.md) | 2026-06-04 |
| 0169 | [Add the foundational eADR canon: the Engine ships its own *why* (litigation alarm + authorization)](0169-add-the-foundational-eadr-canon-the-engine-ships-its-own-why.md) | 2026-06-04 |
| 0170 | [Resolve the D-169 foundational-eADR-canon re-litigation: landed-text cold audit clean, five foundations re-lo…](0170-resolve-the-d-169-foundational-eadr-canon-re-litigation-land.md) | 2026-06-04 |
| 0171 | [Correct the falsified "platform ignores a `PreToolUse` deny" claim: live-verified deny is honored across buil…](0171-correct-the-falsified-platform-ignores-a-pretooluse-deny-cla.md) | 2026-06-05 |
| 0172 | [Resolve the D-171 deny-claim correction: landed-text cold audit clean (docs), carrier accounting corrected, c…](0172-resolve-the-d-171-deny-claim-correction-landed-text-cold-aud.md) | 2026-06-05 |
| 0173 | [Open Q37: a post-v1 optional "hackathon" divergent-exploration module on the multi-agent workflow substrate](0173-open-q37-a-post-v1-optional-hackathon-divergent-exploration.md) | 2026-06-05 |
| 0174 | [Memory & validators-core are hand-governed Builder-A builds; memory gets a light build-order map (not a singl…](0174-memory-validators-core-are-hand-governed-builder-a-builds-me.md) | 2026-06-05 |
| 0175 | [Correct D-174's validators-core timing: it comes online mid-core (a build-time necessity, already built); mem…](0175-correct-d-174-s-validators-core-timing-it-comes-online-mid-c.md) | 2026-06-05 |
| 0176 | [Sharpen D-175: the validators-core module + seed-supersession land mid-core, but its corpus accretes across c…](0176-sharpen-d-175-the-validators-core-module-seed-supersession-l.md) | 2026-06-05 |
| 0177 | [Carve Claude Code's native plan file out of the modes Explore write-gate (litigation alarm + authorization)](0177-carve-claude-code-s-native-plan-file-out-of-the-modes-explor.md) | 2026-06-06 |
| 0178 | [Resolve the D-177 plan-file carve-out: landed-text cold audit clean (no blocking), two serious findings resol…](0178-resolve-the-d-177-plan-file-carve-out-landed-text-cold-audit.md) | 2026-06-06 |
| 0179 | [Augment interactive Build entry with plan-acceptance; correct the falsified "plan-mode transitions are not ho…](0179-augment-interactive-build-entry-with-plan-acceptance-correct.md) | 2026-06-06 |
| 0180 | [Resolve the D-179 Build-entry augment: landed-text cold audit clean (design), blocking Q38-deletion + serious…](0180-resolve-the-d-179-build-entry-augment-landed-text-cold-audit.md) | 2026-06-06 |
| 0181 | [Correct the non-existent GitHub scope `admin:repo_ruleset` in control-plane / provisioning / module-system (l…](0181-correct-the-non-existent-github-scope-admin-repo-ruleset-in.md) | 2026-06-06 |
| 0182 | [Resolve the D-181 scope-name correction: landed-text cold audit clean (no blocking/serious), two operator nit…](0182-resolve-the-d-181-scope-name-correction-landed-text-cold-aud.md) | 2026-06-06 |
| 0183 | [Authorize the issue-authoring grammar correction (build issues #62/#63): pin the human issue-template section…](0183-authorize-the-issue-authoring-grammar-correction-build-issue.md) | 2026-06-06 |
| 0184 | [Resolve the D-183 issue-authoring grammar correction: landed-text cold audit + focused re-audit clean, build-…](0184-resolve-the-d-183-issue-authoring-grammar-correction-landed.md) | 2026-06-06 |
| 0185 | [Authorize a two-foundation re-litigation: ship a native plan-mode default in the Engine that yields to an exi…](0185-authorize-a-two-foundation-re-litigation-ship-a-native-plan.md) | 2026-06-08 |
| 0186 | [Resolve the D-185 plan-mode-default re-litigation: landed-text cold audit clean, two foundations re-locked](0186-resolve-the-d-185-plan-mode-default-re-litigation-landed-tex.md) | 2026-06-08 |
| 0187 | [Authorize the operator-presentation relay re-litigation: the AI's chat is the sole in-session operator channe…](0187-authorize-the-operator-presentation-relay-re-litigation-the.md) | 2026-06-08 |
| 0188 | [Resolve the D-187 operator-presentation relay re-litigation: landed-text cold audit, five docs re-locked](0188-resolve-the-d-187-operator-presentation-relay-re-litigation.md) | 2026-06-08 |
| 0189 | [Authorize the operator-checkout-boundary re-litigation: confine build to worktrees by recognizing native isol…](0189-authorize-the-operator-checkout-boundary-re-litigation-confi.md) | 2026-06-13 |
| 0190 | [Resolve the D-189 operator-checkout-boundary re-litigation: landed-text cold audit, five docs re-locked](0190-resolve-the-d-189-operator-checkout-boundary-re-litigation-l.md) | 2026-06-13 |
| 0191 | [Widen the product-knowledge-graph derivation source from product code to any committed canonical structural a…](0191-widen-the-product-knowledge-graph-derivation-source-from-pro.md) | 2026-06-14 |
| 0192 | [Authorize the `conduct` surface (codes of conduct): a tier-3 prose carrier for the operator's standing behavi…](0192-authorize-the-conduct-surface-codes-of-conduct-a-tier-3-pros.md) | 2026-06-14 |
| 0193 | [Resolve the D-192 `conduct`-surface re-litigation: landed-text cold audit + dry-run, two foundations re-locke…](0193-resolve-the-d-192-conduct-surface-re-litigation-landed-text.md) | 2026-06-14 |
| 0194 | [Resolve Q36: the engine release-cut / version-production process, as a standing maintainer-layer doc](0194-resolve-q36-the-engine-release-cut-version-production-proces.md) | 2026-06-14 |
| 0195 | [Ratify (lock) the `conduct` surface: fresh five-lens cold-session lock audit, one serious fold, no re-locks](0195-ratify-lock-the-conduct-surface-fresh-five-lens-cold-session.md) | 2026-06-14 |
| 0196 | [Authorize the standing-situation-pointer-advance re-litigation: build-orchestration advances the cursor on a…](0196-authorize-the-standing-situation-pointer-advance-re-litigati.md) | 2026-06-14 |
| 0197 | [Resolve the D-196 standing-situation-pointer re-litigation: landed-text cold audit, state + build-orchestrati…](0197-resolve-the-d-196-standing-situation-pointer-re-litigation-l.md) | 2026-06-14 |
| 0198 | [Authorize correcting #100: "where we are" is assembled read-only from GitHub, not advanced by build-orchestra…](0198-authorize-correcting-100-where-we-are-is-assembled-read-only.md) | 2026-06-15 |
| 0199 | [Resolve the D-198 standing-situation correction: landed-text cold audit, state + build-orchestration + boot r…](0199-resolve-the-d-198-standing-situation-correction-landed-text.md) | 2026-06-15 |
| 0200 | [Authorize the status-verb cold-start re-litigation: `model-auto` skills are not cold-start-typeable, so `/eng…](0200-authorize-the-status-verb-cold-start-re-litigation-model-aut.md) | 2026-06-15 |
| 0201 | [Resolve the D-200 status-verb cold-start re-litigation: landed-text cold audit, skills + modules/core re-lock…](0201-resolve-the-d-200-status-verb-cold-start-re-litigation-lande.md) | 2026-06-15 |
| 0202 | [Reconcile the stale D2 deviations row to the current v1 operator-typed verb set](0202-reconcile-the-stale-d2-deviations-row-to-the-current-v1-oper.md) | 2026-06-15 |
| 0203 | [Enrich the derived knowledge-graph schema (a build-spec leaf) with declared-structural depth, under a durable…](0203-enrich-the-derived-knowledge-graph-schema-a-build-spec-leaf.md) | 2026-06-16 |
| 0204 | [Complete the core-build-roadmap retirement as a deletion (graveyard the old path); restore `validate.py` to g…](0204-complete-the-core-build-roadmap-retirement-as-a-deletion-gra.md) | 2026-06-16 |
| 0205 | [Authorize pinning the offline-cache committer: the audit-digest pass commits the shared `state.json` cache as…](0205-authorize-pinning-the-offline-cache-committer-the-audit-dige.md) | 2026-06-17 |
| 0206 | [Resolve the D-205 offline-cache-committer pin: landed-text cold audit, state + audits re-locked](0206-resolve-the-d-205-offline-cache-committer-pin-landed-text-co.md) | 2026-06-17 |
| 0207 | [Authorize the Dependabot PR-contract exemption: a CI-author applicability boundary on the PR-body completenes…](0207-authorize-the-dependabot-pr-contract-exemption-a-ci-author-a.md) | 2026-06-17 |
| 0208 | [Resolve the D-207 Dependabot PR-contract exemption: landed-text cold audit, five docs re-locked](0208-resolve-the-d-207-dependabot-pr-contract-exemption-landed-te.md) | 2026-06-17 |
| 0209 | [Authorize the ledger-compaction re-litigation: bound the append-only ledger's growth and realize hard-delete…](0209-authorize-the-ledger-compaction-re-litigation-bound-the-appe.md) | 2026-06-17 |
| 0210 | [Resolve the D-209 ledger-compaction re-litigation: landed-text cold audit, four docs re-locked](0210-resolve-the-d-209-ledger-compaction-re-litigation-landed-tex.md) | 2026-06-17 |
| 0211 | [Authorize the security-floor re-litigation: add native code scanning (CodeQL), private vulnerability reportin…](0211-authorize-the-security-floor-re-litigation-add-native-code-s.md) | 2026-06-18 |
| 0212 | [Resolve the D-211 security-floor re-litigation: landed-text cold audit, two docs re-locked](0212-resolve-the-d-211-security-floor-re-litigation-landed-text-c.md) | 2026-06-18 |
| 0213 | [Authorize the human-facing front-door re-litigation: the root README as a seeded-then-ceded landing front (en…](0213-authorize-the-human-facing-front-door-re-litigation-the-root.md) | 2026-06-18 |
| 0214 | [Resolve the D-213 front-door re-litigation: landed-text cold audit, two docs re-locked](0214-resolve-the-d-213-front-door-re-litigation-landed-text-cold.md) | 2026-06-18 |
| 0215 | [Authorize the operator-prose-register re-litigation: sharpen the operator-communication law as a rubric and g…](0215-authorize-the-operator-prose-register-re-litigation-sharpen.md) | 2026-06-18 |
| 0216 | [Resolve the D-215 operator-prose-register re-litigation: landed-text cold audit, two docs re-locked](0216-resolve-the-d-215-operator-prose-register-re-litigation-land.md) | 2026-06-18 |
| 0217 | [Authorize the derived-committed-artifact reconcile re-litigation: a §19 source-determinism law + naming artif…](0217-authorize-the-derived-committed-artifact-reconcile-re-litiga.md) | 2026-06-18 |
| 0218 | [Resolve the D-217 derived-committed-artifact reconcile re-litigation: landed-text cold audit, three docs re-l…](0218-resolve-the-d-217-derived-committed-artifact-reconcile-re-li.md) | 2026-06-18 |
| 0219 | [Authorize the first-run travel-safety re-litigation: a retire-set reference-closure invariant + a mandated ha…](0219-authorize-the-first-run-travel-safety-re-litigation-a-retire.md) | 2026-06-19 |
| 0220 | [Resolve the D-219 first-run travel-safety re-litigation: landed-text cold audit, four docs re-locked](0220-resolve-the-d-219-first-run-travel-safety-re-litigation-land.md) | 2026-06-19 |
| 0221 | [Authorize the first-run LICENSE-clear re-litigation: reconcile the traveled template LICENSE at greenfield in…](0221-authorize-the-first-run-license-clear-re-litigation-reconcil.md) | 2026-06-19 |
| 0222 | [Resolve the D-221 first-run LICENSE-clear re-litigation: landed-text cold audit, two docs re-locked](0222-resolve-the-d-221-first-run-license-clear-re-litigation-land.md) | 2026-06-19 |
| 0223 | [Reconcile the locked knowledge boot-slice contradiction: one-word committed→gitignored correctness fix, propo…](0223-reconcile-the-locked-knowledge-boot-slice-contradiction-one.md) | 2026-06-19 |
| 0224 | [Direct the structural-neighbors orientation render to traverse reverse adjacency (existing edges, bidirection…](0224-direct-the-structural-neighbors-orientation-render-to-traver.md) | 2026-06-20 |
| 0225 | [Recenter the spec on "the AI is the thing made trustworthy": reframe the operator from deficiency to role, an…](0225-recenter-the-spec-on-the-ai-is-the-thing-made-trustworthy-re.md) | 2026-06-21 |
| 0226 | [Authorize the audits doc-probe re-litigation: extend the operator-communication-law judgment to operator-faci…](0226-authorize-the-audits-doc-probe-re-litigation-extend-the-oper.md) | 2026-06-21 |
| 0227 | [Resolve the D-226 audits re-litigation: landed-text cold audit, audits re-locked](0227-resolve-the-d-226-audits-re-litigation-landed-text-cold-audi.md) | 2026-06-21 |
| 0228 | [Pin the behavioral-demonstration shape and lifecycle (a falsification that can fail; retire-or-promote; no ju…](0228-pin-the-behavioral-demonstration-shape-and-lifecycle-a-falsi.md) | 2026-06-21 |
| 0229 | [Authorize correcting the falsified Agent-SDK-credit auth claim in locked `audit-library` (engine-template #17…](0229-authorize-correcting-the-falsified-agent-sdk-credit-auth-cla.md) | 2026-06-21 |
| 0230 | [Resolve the D-229 audit-auth correction: landed-text cold audit, `audit-library` re-locked; engine-template #…](0230-resolve-the-d-229-audit-auth-correction-landed-text-cold-aud.md) | 2026-06-21 |
| 0231 | [Promote the in-tool `demo` subcommand as a governed, AI-run standing falsification capability (the healthy wh…](0231-promote-the-in-tool-demo-subcommand-as-a-governed-ai-run-sta.md) | 2026-06-22 |
| 0232 | [Correct D-231's offender census: the full demo population has 25 showcase demos that cannot fail, not one (en…](0232-correct-d-231-s-offender-census-the-full-demo-population-has.md) | 2026-06-22 |
| 0233 | [Authorize the audit-over-audit re-litigation: feed the periodic audit its own prior digests (corroboration on…](0233-authorize-the-audit-over-audit-re-litigation-feed-the-period.md) | 2026-06-22 |
| 0234 | [Resolve the D-233 audit-over-audit re-litigation: landed-text cold re-check clean, audits + audit-library re-…](0234-resolve-the-d-233-audit-over-audit-re-litigation-landed-text.md) | 2026-06-22 |
| 0235 | [Authorize the engine-Issue conformance reroute gate: promote engine-labeled-channel helper-routing from postu…](0235-authorize-the-engine-issue-conformance-reroute-gate-promote.md) | 2026-06-22 |
| 0236 | [Resolve the D-235 engine-Issue conformance reroute gate: landed-text cold re-check clean, control-plane + hoo…](0236-resolve-the-d-235-engine-issue-conformance-reroute-gate-land.md) | 2026-06-22 |
| 0237 | [Authorize flipping the memory-backup default to a shared vault: re-litigate locked memory D-061 (overturns it…](0237-authorize-flipping-the-memory-backup-default-to-a-shared-vau.md) | 2026-06-22 |
| 0238 | [Resolve the D-237 memory-backup shared-vault flip: the four-lens audit widened the blast radius to three lock…](0238-resolve-the-d-237-memory-backup-shared-vault-flip-the-four-l.md) | 2026-06-22 |
| 0239 | [Reject an engine-owned git-hygiene reconciler: accumulated local worktrees/branches are Claude-Code harness e…](0239-reject-an-engine-owned-git-hygiene-reconciler-accumulated-lo.md) | 2026-06-22 |
| 0240 | [Reject an audit that researches external upstream-issue currency; track `upstream`-blocked issues via a GitHu…](0240-reject-an-audit-that-researches-external-upstream-issue-curr.md) | 2026-06-22 |
| 0241 | [Authorize completing the audit's off-repo memory-read enablement: re-open locked audit-library (D-148), provi…](0241-authorize-completing-the-audit-s-off-repo-memory-read-enable.md) | 2026-06-23 |
| 0242 | [Resolve the D-241 audit-memory-read enablement: the landed four-lens audit confirmed the design sound and cau…](0242-resolve-the-d-241-audit-memory-read-enablement-the-landed-fo.md) | 2026-06-23 |
| 0243 | [Decline engine-template #238's public-repo saved-memory opt-in: the thin public review is a build under-deliv…](0243-decline-engine-template-238-s-public-repo-saved-memory-opt-i.md) | 2026-06-23 |
| 0244 | [Re-litigate `product-design` into a first-class spec-driven-design system; re-scope the engine/product wall o…](0244-re-litigate-product-design-into-a-first-class-spec-driven-de.md) | 2026-06-23 |
| 0245 | [Resolve: re-lock `state` (the milestone honest-bound) — first carrier of the D-244 product-design SDD re-liti…](0245-resolve-re-lock-state-the-milestone-honest-bound-first-carri.md) | 2026-06-23 |
| 0246 | [Resolve: re-lock `control-plane` (the spec leaves the engine-label scheme) — second carrier of D-244](0246-resolve-re-lock-control-plane-the-spec-leaves-the-engine-lab.md) | 2026-06-23 |
| 0247 | [Resolve: re-lock `build-orchestration` (committed-spec referent, build-plan→Milestones, the spec is un-skippa…](0247-resolve-re-lock-build-orchestration-committed-spec-referent.md) | 2026-06-23 |
| 0248 | [Resolve: re-lock `qa-review` (the `spec-conformance` referent is the committed `locked` spec) — fourth carrie…](0248-resolve-re-lock-qa-review-the-spec-conformance-referent-is-t.md) | 2026-06-23 |
| 0249 | [Resolve: re-lock `design-review` (the optional advisory spec-lock invocation; `product-intent` referent) — fi…](0249-resolve-re-lock-design-review-the-optional-advisory-spec-loc.md) | 2026-06-23 |
| 0250 | [Resolve: re-lock `product-design` (the full SDD module redesign) — the LAST carrier of D-244, closing the com…](0250-resolve-re-lock-product-design-the-full-sdd-module-redesign.md) | 2026-06-23 |
| 0251 | [Reject engine-template #255's Explore-gate memory carve-out: the engine supersedes harness auto-memory with i…](0251-reject-engine-template-255-s-explore-gate-memory-carve-out-t.md) | 2026-06-23 |
| 0252 | [Authorize binding the §17 operator-runnable behavioral correlate to the PR's Review record (operator-runnable…](0252-authorize-binding-the-17-operator-runnable-behavioral-correl.md) | 2026-06-27 |
| 0253 | [Resolve: re-lock `control-plane` (the Review record carries the operator-runnable acceptance steps) — first c…](0253-resolve-re-lock-control-plane-the-review-record-carries-the.md) | 2026-06-27 |
| 0254 | [Resolve: re-lock `build-orchestration` (the filler renders the operator-runnable acceptance steps + the bound…](0254-resolve-re-lock-build-orchestration-the-filler-renders-the-o.md) | 2026-06-27 |
| 0255 | [Sharpen the post-v1 revisit triggers for `product-knowledge-graph` and `clean-code` from operator-intuition t…](0255-sharpen-the-post-v1-revisit-triggers-for-product-knowledge-g.md) | 2026-06-27 |
| 0256 | [Authorize the "every hard check is proven to bite" re-litigation: a mandatory, standing, CI-enforced negative…](0256-authorize-the-every-hard-check-is-proven-to-bite-re-litigati.md) | 2026-06-27 |
| 0257 | [Resolve: re-lock `validation` (the negative-fixture meta-check law + execution model, the `custom/script` fai…](0257-resolve-re-lock-validation-the-negative-fixture-meta-check-l.md) | 2026-06-27 |
| 0258 | [Resolve: re-lock `check` (the by-presence negative-fixture grammar + the reserved namespace + the `id`-inert…](0258-resolve-re-lock-check-the-by-presence-negative-fixture-gramm.md) | 2026-06-27 |
| 0259 | [Resolve: re-lock `validators-core` (the negative-fixture meta-check instance — self-covering, module-kind fai…](0259-resolve-re-lock-validators-core-the-negative-fixture-meta-ch.md) | 2026-06-27 |
| 0260 | [Resolve: re-lock `core` (the dispatcher run-one-rule entry point + the closed-core kinds' negative fixtures);…](0260-resolve-re-lock-core-the-dispatcher-run-one-rule-entry-point.md) | 2026-06-27 |
| 0261 | [Establish the artifact-warrant discipline (a §7/§17 application, no new principle): a generated artifact stat…](0261-establish-the-artifact-warrant-discipline-a-7-17-application.md) | 2026-06-27 |
| 0262 | [Authorize the `disposition-issue-resolution` check: a §17/§7 mechanical correlate that the disposition Issue…](0262-authorize-the-disposition-issue-resolution-check-a-17-7-mech.md) | 2026-06-27 |
| 0263 | [Resolve: re-lock `validators-core` (the `disposition-issue-resolution` check) — the sole carrier of D-262](0263-resolve-re-lock-validators-core-the-disposition-issue-resolu.md) | 2026-06-27 |
| 0264 | [Authorize git-native retention for the pre-migration memory snapshot (resolve engine-template #287): a distin…](0264-authorize-git-native-retention-for-the-pre-migration-memory.md) | 2026-06-27 |
| 0265 | [Resolve: coupled re-lock of `memory` + `memory-substrate-sqlite-fts5` (the retained pre-migration snapshot ta…](0265-resolve-coupled-re-lock-of-memory-memory-substrate-sqlite-ft.md) | 2026-06-27 |
| 0266 | [New principle §20: spec-conformance is the standing target; no construction milestone licenses an under-build…](0266-new-principle-20-spec-conformance-is-the-standing-target-no.md) | — |
| 0267 | [Clarify §20's instrument-retirement clause: the conformance *capability* ships deployed (build-orchestration)…](0267-clarify-20-s-instrument-retirement-clause-the-conformance-ca.md) | — |
| 0268 | [Adjudicate engine-template #250: the §15 weakening guard's guarded set is defined by an enforcement-gate **pr…](0268-adjudicate-engine-template-250-the-15-weakening-guard-s-guar.md) | 2026-06-27 |
| 0269 | [Litigate Q18 (engine-template #313): resolve cross-session anti-habituation by **collapse-when-unchanged**; b…](0269-litigate-q18-engine-template-313-resolve-cross-session-anti.md) | 2026-06-28 |
| 0270 | [Litigate engine-template #276: make the Explore→Build switch on plan-acceptance legible to the assistant; cor…](0270-litigate-engine-template-276-make-the-explore-build-switch-o.md) | 2026-06-28 |
| 0271 | [Resolve the D-270 plan-acceptance legibility augment: landed-text cold audit clean (design), one serious acce…](0271-resolve-the-d-270-plan-acceptance-legibility-augment-landed.md) | 2026-06-28 |
| 0272 | [Finalize the foundational eADR-canon membership (33 laws) and produce the litigated, stress-tested recommenda…](0272-finalize-the-foundational-eadr-canon-membership-33-laws-and.md) | — |
| 0273 | [Litigate engine-template #332: ambient turn-deltas dominate memory recall; recall surfaces curated episodic r…](0273-litigate-engine-template-332-ambient-turn-deltas-dominate-me.md) | 2026-06-29 |
| 0274 | [Resolve: re-lock `memory` (ambient turn-deltas excluded from recall; recall = curated records) — the carrier…](0274-resolve-re-lock-memory-ambient-turn-deltas-excluded-from-rec.md) | 2026-06-29 |
| 0275 | [Litigate engine-template #342: a checkout parked on a non-default branch evades the strand model; widen the o…](0275-litigate-engine-template-342-a-checkout-parked-on-a-non-defa.md) | 2026-06-29 |
| 0276 | [Resolve: re-lock `provisioning` + `boot` (operator-checkout detector widened branch-agnostic; off-main day-on…](0276-resolve-re-lock-provisioning-boot-operator-checkout-detector.md) | 2026-06-29 |
| 0277 | [Litigate engine-template #353: first-run dead-on-arrival in a deployed copy; restore the provisioned verdict…](0277-litigate-engine-template-353-first-run-dead-on-arrival-in-a.md) | 2026-06-30 |
| 0278 | [Resolve: re-lock `provisioning` + `boot` (provisioned verdict on instantiator-presence, three-state; standing…](0278-resolve-re-lock-provisioning-boot-provisioned-verdict-on-ins.md) | 2026-06-30 |
| 0279 | [Litigate engine-template #360: the memory "sweep reads the raw ledger unfiltered" absolute is now false; the…](0279-litigate-engine-template-360-the-memory-sweep-reads-the-raw.md) | 2026-07-04 |
| 0280 | [Resolve: re-lock `memory` (the consolidation sweep curates harness-injected pseudo-turns out of its fuel + pe…](0280-resolve-re-lock-memory-the-consolidation-sweep-curates-harne.md) | 2026-07-04 |
| 0281 | [Litigate engine-template #367: a detached deployed repo resolves its engine-update source from the deployed r…](0281-litigate-engine-template-367-a-detached-deployed-repo-resolv.md) | 2026-07-05 |
| 0282 | [Resolve: re-lock `provisioning` (the engine manifest records the home repository; the updater resolves the re…](0282-resolve-re-lock-provisioning-the-engine-manifest-records-the.md) | 2026-07-05 |
| 0283 | [Litigate engine-template #361: a PR accidentally auto-closes an issue it declares only "Part of" (four incide…](0283-litigate-engine-template-361-a-pr-accidentally-auto-closes-a.md) | 2026-07-05 |
| 0284 | [Resolve: re-lock `build-orchestration` (the submit-time close-linkage consistency pre-flight in the Review-re…](0284-resolve-re-lock-build-orchestration-the-submit-time-close-li.md) | 2026-07-05 |
| 0285 | [Litigate engine-template #363: the Layer-2 erasure grammar was widened to batch multiple records under one op…](0285-litigate-engine-template-363-the-layer-2-erasure-grammar-was.md) | 2026-07-05 |
| 0286 | [Resolve: re-lock `memory` (the Layer-2 erasure grammar is one-or-more records per single-purpose PR; the batc…](0286-resolve-re-lock-memory-the-layer-2-erasure-grammar-is-one-or.md) | 2026-07-05 |
| 0287 | [Litigate engine-template #427: make the SDD spec drive the build — adopt a derived **spec-obligation matrix**…](0287-litigate-engine-template-427-make-the-sdd-spec-drive-the-bui.md) | 2026-07-06 |
| 0288 | [Resolve: re-lock `product-design` (installs the conformance-enforcement floor's coverage leg — the derived, c…](0288-resolve-re-lock-product-design-installs-the-conformance-enfo.md) | 2026-07-06 |
| 0289 | [Resolve: re-lock `build-orchestration` (the referent section runs the conformance-enforcement floor at the me…](0289-resolve-re-lock-build-orchestration-the-referent-section-run.md) | 2026-07-06 |
| 0290 | [Resolve: re-lock `qa-review` (the `spec-conformance` lens carries the adversarial divergence-hunter posture a…](0290-resolve-re-lock-qa-review-the-spec-conformance-lens-carries.md) | 2026-07-06 |
| 0291 | [Litigate engine-template #427 follow-up (Q-A/Q-B): split build-conformance §8's conformance-reviewer/adversar…](0291-litigate-engine-template-427-follow-up-q-a-q-b-split-build-c.md) | 2026-07-11 |
| 0292 | [Resolve: re-lock `qa-review` (the §8 pair split across two lenses — `spec-conformance` the systematic reviewe…](0292-resolve-re-lock-qa-review-the-8-pair-split-across-two-lenses.md) | 2026-07-11 |
| 0293 | [Resolve: re-lock `build-orchestration` (roster +`divergence-hunter`, nine lenses / qa-review quintet; the mir…](0293-resolve-re-lock-build-orchestration-roster-divergence-hunter.md) | 2026-07-11 |
| 0294 | [Resolve: re-lock `product-design` — a coupled carrier surfaced by D-291's landed-text audit (it still asserte…](0294-resolve-re-lock-product-design-a-coupled-carrier-surfaced-by.md) | 2026-07-11 |
| 0295 | [engine-template's own license moves MIT → Apache-2.0 + Commons Clause; the design is confirmed license-agnost…](0295-engine-template-s-own-license-moves-mit-apache-2-0-commons-c.md) | 2026-07-11 |
| 0296 | [Litigate engine-template #427 residual three (L1/L2/L3): audits gains a standing, conditional **product-spec-…](0296-litigate-engine-template-427-residual-three-l1-l2-l3-audits.md) | 2026-07-11 |
| 0297 | [Resolve: re-lock `audits` (installs the standing, conditional product-spec-conformance sweep — the conformanc…](0297-resolve-re-lock-audits-installs-the-standing-conditional-pro.md) | 2026-07-11 |
| 0298 | [Litigate the deployment eADR collision: the operator's per-instance engine-decision stream adopts a per-proje…](0298-litigate-the-deployment-eadr-collision-the-operator-s-per-in.md) | 2026-07-12 |
| 0299 | [Resolve: re-lock `ontology` (the instance-identifier law gains the intra-engine layer — engine canon `eADR-##…](0299-resolve-re-lock-ontology-the-instance-identifier-law-gains-t.md) | 2026-07-12 |
| 0300 | [Resolve: re-lock `contracts` (the two eADR populations named — canon `eADR-####`, a deployment's per-instance…](0300-resolve-re-lock-contracts-the-two-eadr-populations-named-can.md) | 2026-07-12 |
| 0301 | [Close Q41 by decision: decline legal input on Commons-Clause `.engine/` binding; accept the posture; the lock…](0301-close-q41-by-decision-decline-legal-input-on-commons-clause.md) | 2026-07-12 |
| 0302 | [Litigate engine-template #471: design the standing foreign-`LICENSE`-seed detector (R29 residual / D-222 buil…](0302-litigate-engine-template-471-design-the-standing-foreign-lic.md) | 2026-07-12 |
| 0303 | [Resolve: re-lock `repository-topology` (law 2 gains the standing LICENSE exception — a reviewed-PR proposal,…](0303-resolve-re-lock-repository-topology-law-2-gains-the-standing.md) | 2026-07-12 |
| 0304 | [Resolve: re-lock `modules/core` (the foreign-`LICENSE`-seed detector enters `provides`; the never-strand floo…](0304-resolve-re-lock-modules-core-the-foreign-license-seed-detect.md) | 2026-07-12 |
| 0305 | [Resolve: re-lock `provisioning` (build-owe #5 → the designed standing detector; recognizer reconciled to per-…](0305-resolve-re-lock-provisioning-build-owe-5-the-designed-standi.md) | 2026-07-12 |
| 0306 | [Resolve: re-lock `boot` (the leftover-license surfacing + the hook-enforced kept-on-purpose intent-exit) — a…](0306-resolve-re-lock-boot-the-leftover-license-surfacing-the-hook.md) | 2026-07-12 |
| 0307 | [Litigate engine-template #446: incremental consolidation — the boot-time consolidation **sweep** recovers an…](0307-litigate-engine-template-446-incremental-consolidation-the-b.md) | 2026-07-12 |
| 0308 | [Resolve: re-lock `memory` (incremental consolidation — the watermark sweep predicate + per-session high-water…](0308-resolve-re-lock-memory-incremental-consolidation-the-waterma.md) | 2026-07-12 |
| 0309 | [Litigate the grammar-and-boot cluster (ledger `grammar-core-U09` / `grammar-core-U10` / `lifecycle-U11`): boo…](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md) | 2026-07-16 |
| 0310 | [Resolve: re-lock `ontology` (the coverage attestation bounded to what the gate re-attests; the consumption la…](0310-resolve-re-lock-ontology-the-coverage-attestation-bounded-to.md) | 2026-07-16 |
| 0311 | [Retire the `wbs/eadr-canon/` recommendation set: the eADR canon of record is engine-template's, and this work…](0311-retire-the-wbs-eadr-canon-recommendation-set-the-eadr-canon.md) | 2026-07-16 |
| 0312 | [Resolve: re-lock `boot` (the recognition-slice read with no dedup; the §15 weakening-alarm class retired; the…](0312-resolve-re-lock-boot-the-recognition-slice-read-with-no-dedu.md) | 2026-07-16 |
| 0313 | [Resolve: re-lock `agents` (the `engine-` naming rule; the read-only write-tool floor gated mechanically, with…](0313-resolve-re-lock-agents-the-engine-naming-rule-the-read-only.md) | 2026-07-16 |
| 0314 | [Litigate engine-template #394: attention's work-record commission was **superseded, not phantom** — the backl…](0314-litigate-engine-template-394-attention-s-work-record-commiss.md) | 2026-07-16 |
| 0315 | [Amend D-314: correct its operator-authorship premise (the build-plan is **engine**-authored and living); fold…](0315-amend-d-314-correct-its-operator-authorship-premise-the-buil.md) | 2026-07-16 |
| 0316 | [Resolve: re-lock `attention` (the work-record commission retired to the plan's owner; the retired read cleare…](0316-resolve-re-lock-attention-the-work-record-commission-retired.md) | 2026-07-16 |
| 0317 | [Resolve: re-lock `state` (the taxonomy kept, its attachment narrowed; "next" routed to its real surface; the…](0317-resolve-re-lock-state-the-taxonomy-kept-its-attachment-narro.md) | 2026-07-16 |
| 0318 | [Resolve: re-lock `github-projects-sync` (the board's engine field is **`ranked work`**, not *"what's next"* —…](0318-resolve-re-lock-github-projects-sync-the-board-s-engine-fiel.md) | 2026-07-16 |
| 0319 | [Resolve: re-lock `boot` (relay state's `milestone` selection bound without restating it; the card's rendering…](0319-resolve-re-lock-boot-relay-state-s-milestone-selection-bound.md) | 2026-07-16 |
| 0320 | [Reconcile the spec to engine-template as built — the sync policy](0320-reconcile-the-spec-to-engine-template-as-built-sync-policy.md) | 2026-07-29 |
| 0321 | [Adopt the build's refusal of fabricated cost-and-time estimates at the plan gate](0321-adopt-the-build-s-refusal-of-fabricated-cost-and-time-estima.md) | 2026-08-01 |
| 0322 | [Ratify `set-routine` as the routine-entry actor](0322-ratify-set-routine-as-the-routine-entry-actor.md) | 2026-08-01 |
| 0323 | [Sanction the built engine-erasure label exemption and the widened CI author set](0323-sanction-the-built-engine-erasure-label-exemption-and-the-wi.md) | 2026-08-01 |
| 0324 | [Admit actionlint as an advisory member of the security floor](0324-admit-actionlint-as-an-advisory-member-of-the-security-floor.md) | 2026-08-01 |
| 0325 | [Bless the four traveling hygiene and drift check rules and place their mandates](0325-bless-the-four-traveling-hygiene-and-drift-check-rules-and-p.md) | 2026-08-01 |
| 0326 | [Admit engine-recall as the single `model-auto` skill](0326-admit-engine-recall-as-the-single-model-auto-skill.md) | 2026-08-01 |
| 0327 | [Route product-spec authoring through plan acceptance into Build](0327-route-product-spec-authoring-through-plan-acceptance-into-b.md) | 2026-08-02 |
| 0328 | [Adopt the board's What's-next field, superseding the spec's ban](0328-adopt-the-board-s-what-s-next-field-superseding-the-spec-s-b.md) | 2026-08-02 |
| 0329 | [Adopt the built letter where locked module documents lag the build](0329-adopt-the-built-letter-where-locked-module-documents-lag-the.md) | 2026-08-02 |
| 0330 | [Adopt the built semantic-recall seat and the canon's revised-in-place model, with the orchestrator's re-audit judgment](0330-adopt-the-built-semantic-recall-seat-and-the-canon-s-revised.md) | 2026-08-02 |
