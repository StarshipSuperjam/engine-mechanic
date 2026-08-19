---
status: draft
---

# interactive-engine-tour

*Forward-designed 2026-08-19 through the product-intake route established by
[decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md), and preserved
in full by [decision 0337](../../adr/0337-preserve-the-interactive-engine-tour-design-for-late-v1.md). This is a
detailed future design, not a placeholder. It is deliberately **parked**: in progress, not settled, absent
from the build order, and not authorization to implement, route, install, or release anything. Before any
breakout or build, the operator must revalidate the need and the provisional choices named below and record a
new decision. The accepted decision is to retain this design and its durable constraints, not to accept the
capability as build ground.*

## Summary

An **optional, local, private, offline, static interactive tour of the Engine** for a capable non-engineer who
wants to direct the system without having to reverse-engineer it. It bridges the approachable but linear
getting-started guide and the accurate but dense generated self-map. The tour teaches the operator's actual
journey — what they do, what the Engine does in response, what proves it, and what choice remains theirs —
rather than turning the repository into a generic programming course.

The tour has a stable, reviewed curriculum joined to a separately generated snapshot of the installed
Engine. The curriculum explains durable concepts; the snapshot supplies only mechanically derived facts with
source lineage. Ordinary generation makes no model call and never improvises an explanation from repository
text. The rendered bundle is disposable, evidence-linked, complete without JavaScript, and useful even when
optional late-v1 modules are absent.

This design takes inspiration from the user-journey-first teaching shape of
[`zarazhangrui/codebase-to-course`](https://github.com/zarazhangrui/codebase-to-course), reviewed on
2026-08-18. It is a clean-room Engine design, not a port or fork. At review time the reference repository had
no visible license and carried open correctness, security, and documentation-drift work; no code, templates,
assets, distinctive wording, interaction sequence, or tests may be copied without compatible permission and
an explicit provenance review.

## Behavior

### Audience and promised outcome

The primary learner is an operator who is comfortable making product and risk decisions but is not expected
to read Python, schemas, hooks, manifests, or Git history. The validation pool must include at least these
profiles before release:

- a first-time operator who has read only the getting-started guide;
- a returning operator who has used the Engine conversationally but has not inspected its files; and
- an operator using keyboard-only or screen-reader navigation.

After the tour, each learner can complete the following tasks without assistance:

1. choose correctly between Explore and Build for a concrete request and explain what changes between them;
2. locate the evidence behind an Engine claim and distinguish the evidence from the Engine's explanation;
3. identify which decisions belong to the Engine and which still belong to the operator, including who can
   merge;
4. recognize a degraded or unavailable protection and choose a safe next step rather than treating it as a
   pass;
5. explain the distinct jobs of project state, saved memory, operator pins, decisions, policies, and derived
   knowledge; and
6. find the installed module or source that explains a behavior and return from the tour to that live
   evidence.

The late-v1 revalidation sets the participant count, supported browser and assistive-technology matrix,
per-task threshold, overall pass threshold, retest triggers, and remediation owner. No release may describe
the tour as successful merely because its pages render. The intended floor is that every safety-critical task
(1–4) passes individually and the cohort passes a declared overall threshold; the exact numerical bar remains
a recorded late-v1 choice because the validation resources and supported platform matrix do not yet exist.

### Learner journey

- **Entry.** The built capability is discoverable from both the getting-started path and the generated
  self-map. Before optional activation, each entry says what will be generated, what it will read, where it
  will be stored, and that no project content is needed.
- **Orientation.** A short map states the learning outcomes, estimated chapter count without inventing a time
  estimate, accessibility controls, privacy boundary, generation status, and how to leave.
- **Learning.** Every lesson follows the same frame: **your action → Engine behavior → evidence → your
  choice**. Scenario questions test a decision the operator may actually face; they are never trivia gates.
- **Evidence.** A learner can move from an explanation to the repository-relative source or canonical Engine
  entity that supports it, then return to the same lesson. Absolute machine paths are never rendered.
- **Completion and return.** Completion shows what the learner can now decide, links back to live Engine
  surfaces, and offers reset. A learner can leave and resume without losing access to any content; the tour is
  fully usable with progress storage disabled.
- **Stale or unavailable state.** A directly opened artifact says only when and from what release and inputs it
  was last generated. The launch command checks current input digests and reports `current`, `stale`,
  `incompatible`, or `failed`; stale content remains readable but cannot present itself as current.

### Curriculum

The proposed curriculum is a provisional teaching arc to preserve, not a frozen implementation. The late-v1
revalidation may reorder or combine chapters while preserving the outcomes above.

1. **How a task starts.** Grounding, the status briefing, conduct, memory consultation, and what the operator
   should hear when those supports are degraded.
2. **Explore and Build.** Read-only exploration, explicit build authority, isolated work, draft pull requests,
   and the protected human merge boundary.
3. **What the Engine remembers and derives.** Project state, exact conversation memory, operator-owned pins,
   decisions, policies, the self-map, and the knowledge graph — taught with clearly synthetic examples rather
   than real private material.
4. **How a change travels.** Request → description and plan → design review → isolated implementation →
   checks → quality review → pull request → operator merge.
5. **What protects the work.** Checks and their deliberately broken fixtures, advisory review, deliberate
   guardrail acknowledgment, typed failure, and the difference between “passed,” “not applicable,” and “could
   not run.”
6. **How the Engine changes.** Modules, distribution/applicability/activation, routes, upgrades, the generated
   self-map, removal, and instance decisions.

The closing **Your Engine now** view describes the installed release, modules, and available routes from the
generated evidence snapshot. It does not show the live work queue, deployments, or “what needs me”; those are
the [operator cockpit](operator-cockpit.md)'s territory.

### Teaching and interaction rules

- A three-way view — **What you see / What the Engine does / What proves it** — may progressively enhance the
  static lesson, but all three are present in the semantic document without scripting.
- Flow diagrams have an equivalent ordered text path. Animation illustrates a state transition only; motion,
  color, drag, hover, sound, metaphor, chat simulation, and quiz completion are never required to understand
  or navigate the material.
- A glossary defines each technical term at first use in plain language. “Under the hood” may show exact,
  allowlisted Engine excerpts, but code is optional and never the only explanation.
- Every question explains why each answer is safe or unsafe. Incorrect answers do not block progress or shame
  the learner.
- Private concepts use synthetic, visibly labeled scenarios. Real memory, pins, conduct text, project
  decisions, repository history, and issue content never become teaching examples.
- Curriculum prose, scenario answers, navigation labels, and degraded-state guidance are subject to the same
  assertion rules as generated facts: every Engine-specific or normative assertion links to a versioned
  primary-source claim, or is explicitly classified as non-factual instructional framing. An unclassified
  assertion blocks publication.

### Two models joined by governed concepts

The capability keeps durable teaching content separate from volatile installation facts:

1. **`engine-tour-curriculum.v1`** contains learning outcomes, chapters, scenarios, glossary entries,
   accessibility alternatives, and assertion classifications. It declares the Engine release range it has
   been reviewed against and maps each lesson to the Engine surfaces whose change requires curriculum review.
2. **`engine-tour-evidence-snapshot.v1`** contains only facts derived from the current installed Engine through
   registered source adapters. Each fact carries its source-native identifier, authority tier, versioned source
   reference, lineage, display classification, content digest, and coverage disposition. Digests detect change;
   they are not identity.

The models join only through a governed **concept-ID registry**. A concept identifier has one immutable
meaning, is unique, and may be retired only through a tombstone; aliases and migrations are explicit. Checks
reject collisions, semantic reuse, unresolved joins, and a lesson that attaches to more than one fact when its
declared cardinality permits one. The registry is a protected governance surface, not an ad hoc list inside a
template.

### Source authority, lineage, and coverage

A typed source registry declares, for every source adapter: authority tier and precedence, schema revision,
approved fields, parser version, canonical ordering, size and object limits, display classification, and
unknown-revision behavior.

- **Primary structured sources** may assert facts: the surface catalog, module and provisioning manifests,
  structured route metadata, and other schema-backed records explicitly admitted at the late-v1 review.
- **Derived sources** such as the generated self-map and Engine knowledge graph may supply navigation and
  lineage-filtered evidence links. They never become peer authority, expand the source wall through an edge,
  or break a tie between primary sources. Their freshness is computed transitively from their primary inputs.
- **Narrative sources** — named public Engine docs, policies, contracts, and operations — are evidence
  destinations unless they expose a stable structured metadata contract. The generator never mines headings or
  prose layout for facts.

Authority tiers, precedence, adapters, display classifications, and omission rules require an owner review,
rationale, schema-migration note, and auditable policy-diff fixture to change. Promoting a source or making a
field displayable is treated as a governance change, not ordinary curriculum editing.

Coverage has two separate, versioned obligations:

- **Claim provenance:** every rendered factual or normative assertion resolves to its admitted primary-source
  lineage; no phantom claim may render.
- **Scope disposition:** every object in the explicitly versioned in-scope source set is recorded as `covered`
  or `omitted` with a typed reason. Scope cardinality and allowed exemptions are part of the registry.

Required curriculum sections and source objects are distinguished from optional enhancements. A missing or
unsupported required input prevents publication; an optional omission produces a complete bundle only when
the page and bundle manifest name it plainly. Unknown schema revisions are omitted or fail closed according to
the registered rule — never guessed.

### Source acquisition and the private-data wall

Every adapter is data-only and fail-closed. Before parsing, it resolves a canonical path inside the exact
Engine instance root, rejects symlinks, traversal, special files, and root escape, and reads from one consistent
source snapshot. Parsers disable executable constructors, includes, external entities, and reference expansion,
and apply byte, object-count, nesting, expansion, and time/work budgets before untrusted structure can exhaust
the generator.

The default-deny subject wall excludes:

- product code and product documentation;
- Git history, branches, issues, pull requests, and working-tree diffs;
- environment variables, credentials, secrets, ignored files, and arbitrary repository text;
- real Engine memory, operator pins, operator conduct, and private instance decisions; and
- absolute paths, usernames, internal URLs, source excerpts, or values not recursively classified for a named
  output sink.

Classification follows every retained or emitted value — visible text, identifiers, URLs, HTML attributes,
accessibility labels, print output, evidence references, manifests, diagnostics, temporary files, and logs.
Unknown fields and unknown sinks block publication. Links use generated internal targets or an approved scheme;
raw source values never become markup, selectors, file destinations, or URLs.

Generated data is project-scoped, stored with restrictive permissions, and excluded from source control.
Export is **unsupported in this cut**: a warning is not treated as a privacy boundary. A future export requires
a separate sanitized pipeline, complete content inventory, reclassification, removal of machine-local links and
metadata, and explicit confirmation before writing.

### Generation and bundle lifecycle

Ordinary generation is deterministic, bounded, and model-free. The generator ships all parsers, templates,
styles, scripts, and fonts in the Engine's locked runtime; it performs no runtime fetching. Complete semantic
HTML contains every authored and derived fact. External relative-path CSS and JavaScript provide progressive
enhancement only: no local JSON fetch is required, and disabling JavaScript loses no content or navigation.

Generation uses same-filesystem staging and immutable generation directories. A bundle manifest binds the
output to the Engine instance and source snapshot and records input lineage/digests, every generated-file hash,
curriculum/source-registry/concept/schema/template/renderer versions, Engine release, generation time, typed
omissions, and status. One writer owns generation through exclusive creation and a bounded stale-lock recovery
protocol. Files and manifest are persisted and hash-verified before a separately switched current-generation
pointer can name the bundle. Launch and startup repair verify identity, compatibility, and every file hash;
they never activate a partial, tampered, cross-project, or incompatible generation.

A failed generation preserves the last verified bundle and records failure outside it with a bounded structured
error code and source identifier. Normal UI and retained logs contain no parser excerpt, absolute path,
username, or raw exception trace. Detailed diagnostic bundles are opt-in, remain under the same permissions and
cleanup policy, and undergo the output classification wall.

Cleanup is concurrency-safe, never deletes current or staged work, and retains only a bounded number of
recoverable generations. Incompatible release, curriculum, model, renderer, or source-registry revisions
invalidate disposable output instead of migrating it. Uninstall removes the route and offers deletion of all
tour bundles and progress data; no artifact is authoritative or required for recovery.

The late-v1 review fixes the supported-platform publication mechanism, per-project versus per-worktree cache
home, generation and asset size budgets, retained-generation count, launch and Engine-update regeneration
triggers, and tests against a representative large instance.

### Progress data

Progress is optional convenience data, never evidence or telemetry. If retained, it stores only versioned
completion identifiers, is project-scoped, permission-restricted, excluded from export, subject to the same
bounded retention and uninstall cleanup, and completely removable by reset. The tour works in a storage-free
mode. Browser storage is not assumed safe merely because the artifact is local; its use, origin isolation, and
cleanup are explicit late-v1 decisions.

### Security and supply-chain posture

- Source text is rendered through escaping or DOM `textContent`; no `innerHTML`, inline event handler, `eval`,
  dynamic code generation, or raw fact interpolation into selectors, markup, attributes, paths, or URLs.
- A restrictive content-security policy permits only the fixed local asset set. There is no analytics,
  telemetry, sign-in, remote font, third-party script, server, or network request.
- Packages and assets are pinned and hash-verified, carry a dependency and license inventory, and receive a
  vulnerability review. No install hook or runtime path may contact the network.
- The capability may claim **offline** only after installation, generation, and viewing all pass from an empty
  dependency cache with network access denied. If late-v1 packaging cannot meet all three, the promise is
  narrowed in the operator-facing text rather than quietly redefining offline.
- The reference repository is not consulted during implementation. Independently stated requirements and
  observed failure classes in this document are the input; an asset-and-behavior provenance ledger demonstrates
  clean-room authorship. Any desired parity is a separate legal and release decision.

### Accessibility

The unenhanced document has semantic headings and landmarks, logical reading and focus order, labeled controls,
keyboard access, screen-reader names, diagram text equivalents, WCAG AA contrast, zoom/reflow support, print
completeness, visible focus, reduced-motion behavior, and no dependency on color, motion, drag, hover, sound, or
timing. Scenario feedback is announced and remains visible.

Human validation uses synthetic Engine data only. Before recruiting participants, the late-v1 decision sets
consent, data minimization, recording policy, access, anonymization, retention and deletion, accommodations,
and a ban on live private Engine instances. Names, disability-related accommodation information, recordings,
and performance data are never collected merely because a usability gate exists.

### Manifest shape if the design is later accepted

These values preserve the current best design while remaining subject to the mandatory revalidation gate.

| Field | Provisional value |
| --- | --- |
| `id` | `interactive-engine-tour` |
| `distribution` | `extension` initially; promotion requires evidence that the tour materially improves cold non-engineer comprehension and that its release-maintenance cost is supportable |
| `applicability` | `universal` |
| `activation` | explicit, on-trigger, ungated; never auto-opens at boot |
| `provides` | an `engine-tour` skill/route in both runtime projections after implementation; curriculum, evidence-snapshot, concept-registry, source-registry, and bundle-manifest schemas; deterministic generator and launcher; fixed assets; provenance, coverage, confinement, determinism, bundle-integrity, static-safety, accessibility, and clean-room checks; operator documentation |
| `wires` | the chosen gitignore/cache wire only |
| `depends` | `core`; peer capabilities are optional enhancements through the tour-owned adapter |
| `migrations` | none; generated bundles are disposable |

The curriculum owner is the future module owner. Each chapter's surface mapping participates in Engine release
review: a changed source surface either confirms curriculum compatibility, revises the lesson, or blocks a
release claiming support for that Engine version.

### Operator and automatic workflow routing

**Current disposition: `none` (parked design).** No command, skill, or automatic route exists for an unbuilt
capability. If later accepted and built, a canonical `engine-tour` route may be generated only after the
extension is installed, activated, and has a verified current bundle; otherwise the route reports the explicit
absent, stale, incompatible, or failed state. The route never fabricates a tour at runtime and never widens
Build authority.

### Boundaries with nearby capabilities

- [Getting started](../../../.engine/docs/getting-started.md) remains the concise first read; the tour is guided
  practice, not a replacement.
- The generated Engine self-map and knowledge graph remain structural sources and evidence destinations; the
  tour does not become their authority or merge its model into them.
- [operator-cockpit](operator-cockpit.md) answers current-state questions; this tour teaches the durable mental
  model.
- [evidence-explorer](evidence-explorer.md) navigates arbitrary evidence chains; this tour links only the
  evidence required by its curriculum.
- [product-knowledge-graph](product-knowledge-graph.md) maps the product the Engine builds; this tour does not
  read or teach that product's private content.
- [research-and-learning](research-and-learning.md) may later receive an explicitly consented, anonymized
  comprehension finding, but the tour has no telemetry, does not observe users, and never self-tunes.

The base tour is complete when all peer modules are absent. Optional integrations pass through a tour-owned,
versioned capability adapter with discovery and link-only or versioned query contracts; each enhancement
degrades independently and cannot expose a peer's internal schema or expand the private-data wall.

### Mandatory late-v1 revalidation

Before this draft can settle, enter a delivery phase, receive a breakout Issue, or authorize implementation,
the operator reviews and records whether:

- Engine opacity remains the problem worth solving, for the named learner profiles and tasks;
- the current getting-started, self-map, routes, modules, and late-v1 operator views still leave the stated gap;
- the curriculum and learner journey still match actual operator workflows;
- source authority, privacy exclusions, adapter contracts, peer-module seams, and accessibility obligations fit
  the then-current Engine;
- extension versus required distribution, route, cache location, platform/browser/assistive-technology matrix,
  validation resources, offline scope, budgets, and maintenance owner are supportable; and
- the source license/provenance record permits the intended clean-room implementation.

That decision chooses whether this joins or follows delivery wave 7, remains parked, changes shape, or is
retired. The six chapters, exact schema fields, source roster, adapter implementations, cache mechanism, and
interaction details remain provisional until that gate.

### What stays out

- a generic “turn any codebase into a course” generator;
- runtime AI-authored explanations, summaries, quizzes, or safety advice;
- current work dashboards, actions, approvals, or a second decision surface;
- product code, product knowledge, real private Engine content, or arbitrary repository prose;
- a daemon, hosted site, cloud account, network dependency, analytics, or automatic publication;
- mandatory decoration, animation, quizzes, chat simulation, or code reading;
- self-tuning from learner behavior; and
- export in the initial cut.

## Acceptance criteria

*These are intended release gates for a future build, not claims about a capability that exists now. `engine`
means a named merge-gated check can fully assert the criterion; `operator` means human observation or judgment
carries at least part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Every assertion is classified and grounded** — factual and normative assertions resolve through primary-source lineage; framing is labeled; unknown assertions fail publication. | Negative fixtures for phantom, derived-as-authority, stale-curriculum, and unclassified assertions exercise the provenance check. | engine |
| **The private-data wall is recursive and default-deny** — excluded data cannot reach any output sink. | Confinement and information-flow fixtures cover traversal, symlink, special-file, hostile parser, hidden attribute, print, manifest, diagnostic, temporary-file, and unknown-field cases. | engine |
| **Source parsing is bounded and inert** — structured input cannot execute features, expand references, escape the instance, or exhaust unbounded work. | Adapter fixtures exercise constructors/includes/entities, nesting, expansion, byte/object limits, inconsistent snapshots, and unknown revisions. | engine |
| **Coverage is honest in both directions** — every rendered claim has provenance and every versioned in-scope object has a covered or reasoned-omission disposition. | Separate provenance and scope-disposition checks each bite a negative fixture. | engine |
| **Curriculum and evidence cannot drift into the wrong join** — concept meanings are immutable and joins resolve uniquely. | Registry validation covers collisions, reuse, tombstones, aliases, migrations, cardinality, and unresolved joins. | engine |
| **Generation is deterministic, offline, and supply-chain bounded** — equivalent admitted inputs produce equivalent content; installation, generation, and viewing make no network request when the full offline claim is made. | Reproducibility fixtures, empty-cache offline installation, network-denied generation/viewing, dependency hashes, license inventory, and vulnerability review. | engine |
| **Only a complete verified bundle activates** — partial, tampered, cross-instance, concurrently generated, or incompatible bundles never become current; failure preserves the last verified bundle. | Crash-point, hash-tamper, instance-swap, concurrent-writer, stale-lock, repair, cleanup, and incompatible-version fixtures. | engine |
| **Static means complete** — the file-opened semantic HTML contains every lesson and fact without JavaScript, network access, local JSON fetches, or a server. | Network-disabled, JavaScript-disabled, storage-disabled, and print walkthroughs compare content coverage with the enhanced view. | operator |
| **Degradation stays truthful and usable** — required omissions block publication; every optional omission and current/stale/incompatible/failed state is plain and actionable. | Staged missing, unreadable, unsupported, stale, incompatible, and failed inputs are walked from entry to safe next step. | operator |
| **A cold non-engineer gains the intended mental model** — each representative learner completes every safety-critical task and the declared overall threshold without assistance. | Recorded task battery covers Explore/Build, evidence, authority/merge, degraded protection, Engine memory/knowledge concepts, and return to live evidence under the approved participant protocol. | operator |
| **The learner journey is complete** — entry from getting-started and self-map, privacy expectations, navigation, evidence return, resume/storage-free use, completion, and reset all work. | End-to-end walkthrough for first-time and returning profiles, including stale and unavailable generation states. | operator |
| **Accessibility is equivalent, not supplemental** — keyboard, screen-reader, reduced-motion, zoom/reflow, no-JS, and print paths preserve meaning and task completion. | The approved browser/assistive-technology matrix runs the same task battery; automated checks supplement but do not replace it. | operator |
| **Private validation data is governed** — comprehension work uses synthetic Engine data and follows the recorded consent, minimization, access, retention, anonymization, and deletion policy. | Review the participant protocol and retained evidence; verify no live private Engine data or undeclared recording was used. | operator |
| **Clean-room provenance is demonstrable** — every asset and behavior has an independent source or compatible permission, and no unlicensed reference material entered the build. | Review the provenance ledger, dependency/license inventory, and implementation history before release. | operator |
| **Promotion is earned** — any move from extension to required is supported by measured comprehension benefit, acceptable maintenance burden, and a new operator decision. | Compare the declared task results and release-maintenance evidence, then record the distribution decision. | operator |
