---
status: draft
---

# product-system-explorer

*Forward-designed 2026-08-19 through the product-intake route established by
[decision 0327](../../adr/0327-route-product-spec-authoring-through-plan-acceptance-into-b.md), and preserved
in full by [decision 0337](../../adr/0337-preserve-the-product-system-explorer-design-for-late-v1.md). This is
a detailed future design, not a placeholder. It is deliberately **parked**: in progress, outside the build
order, and not authorization to implement, route, install, deprecate, or release anything. Before breakout or
build, the operator must revalidate the need and every provisional choice named below and record a new
decision. The accepted decision is to retain this design and its durable constraints, not to accept the
capability as build ground.*

## Summary

The **product-system explorer** is the operator's evidence-bearing window into the inner workings of the
system the Engine is building. It presents architecture, behavior, integrations, implementation, evidence,
and change implications at operator-controlled depth. It also provides a required on-demand **Engine lens**:
from any selected product element, behavior, integration, or change, the operator can see how their Engine
SDLC team understood it, designed it, built it, checked it, reviewed it, and what uncertainty or authority
still remains with the operator.

This is not a beginner course, a simplified view for a supposedly non-technical audience, or a substitute for
technical detail. The operator owns product intent, architecture, risk, and outcomes. They may be technically
sophisticated and may write code, but they are not required to validate the system by reverse-engineering its
implementation. The explorer must support detailed system understanding without requiring implementation
work, while making exact code and evidence available whenever the operator wants it.

Guided tours are one navigation mode inside the explorer, not its identity. The durable product is a local,
private, offline-capable, static-first system model with explicit evidence, provenance, freshness, coverage,
contradictions, and unknowns. Its ordinary generation is deterministic and model-free. Any model-assisted
explanation is an explicit authoring proposal that is reviewed, version-bound, and never allowed to overrule
the underlying claims.

The target late-v1 shape is a required, universally available module with on-demand activation. That
distribution is necessary if the explorer is to replace the current `engine-parts` command. If late-v1
revalidation instead leaves the explorer optional, a minimal core inventory and discovery surface must remain;
`engine-parts` cannot be retired into an optional or already-running UI.

## Behavior

### Audience, stance, and promised outcome

The primary user is the operator responsible for the system being built. The explorer makes no assumption
about whether that operator reads or writes code. It changes the work required to understand the system, not
the intellectual depth available to them.

The operator can use the explorer to:

1. map a product boundary and its owned components, external dependencies, data, and trust boundaries;
2. trace a user, business, or system behavior across synchronous, asynchronous, conditional, and failure
   paths;
3. inspect an integration's declared and observed contracts, ownership, authentication, delivery semantics,
   retries, idempotency, failure behavior, and open uncertainty;
4. drill from a product concept through implementation bindings to tests, decisions, and ground evidence;
5. evaluate provider-owned candidate impacts of a proposed change without mistaking navigation for a complete
   safety verdict; and
6. pivot from any of those product subjects into the Engine work and evidence that produced or checked it,
   then return without losing context.

The release outcome is demonstrated task completion on representative real shapes and hostile/degraded
fixtures, not page rendering, quiz completion, or a claim that a generated diagram is easy to understand.

### Two subjects, one traceable window

The explorer composes two subjects without merging their identities:

- **Product subject:** the system under construction, including its product design, runtime components,
  integrations, implementation, tests, and delivery evidence.
- **Operating Engine subject:** the Engine instance acting as that product's SDLC team, including the Engine
  capabilities, routes, decisions, checks, reviews, and records responsible for the selected product work.

In `engine-mechanic`, the product under construction is itself the Engine. That does not collapse the model.
The **Engine product at a named product revision** and the **operating Engine installation at a named Engine
release or run identity** remain different subject instances. The interface always names which one is being
shown; colors or layout alone never carry the distinction.

Every object and relation carries an `explorer-subject-ref.v1` identity envelope with at least:

- subject kind and stable subject-instance identity;
- repository, checkout, installation, environment, or run identity as applicable;
- provider and immutable provider-local identifier;
- source and authority lane;
- source snapshot or version and schema version;
- freshness state and typed stale reason;
- coverage state and typed absence or truncation reason; and
- display classification and authorization scope.

Paths, names, commits, module IDs, and provider-local graph IDs are never treated as globally unique.
Cross-subject movement uses explicit, versioned `product-engine-bridge.v1` records. A bridge retains both
subject envelopes, the admitted relation type, source-bound provenance, creator and review authority,
freshness propagation, and validation state. It points to provider-owned records; it never copies the product
and Engine graphs into a third authoritative graph. An inferred, stale, ambiguous, unauthorized, or
revision-mismatched bridge fails closed and is displayed as unavailable or disputed, never as approval.

The primary Engine-lens pivot is:

**selected product element or change → intent → decisions → implementation activity → tests and checks →
reviews and delivery evidence → unresolved uncertainty → remaining operator authority**.

Drilling into the implementation of the Engine itself is a further operator choice. The Engine lens is not
primarily a tour of Engine source code.

### Operator-controlled resolution

The interface uses resolution rather than personas. The operator can move in either direction without being
forced through a course sequence:

1. **Landscape** — system purpose, boundaries, actors, owned and external systems, environments, major data
   and trust boundaries, and declared unknowns.
2. **System** — components, responsibilities, behavior flows, state transitions, dependencies, and ownership.
3. **Integration** — protocols, endpoints or events, schemas and versions, authentication, authorization,
   delivery semantics, retries, idempotency, failure and compensation paths, and operational dependencies.
4. **Implementation** — modules, files, symbols, configuration, tests, generated artifacts, and exact bindings.
5. **Evidence** — source claims, decisions, receipts, checks, reviews, freshness, coverage, contradictions,
   and unresolved gaps.

Every level preserves a stable selection and deep link. Moving upward summarizes only admitted facts and
retains visible uncertainty. Moving downward adds detail without silently changing subject, revision, or
authority.

### Exploration modes

#### System map

The map shows provider-owned product elements and relations with boundaries, ownership, environments, trust
zones, external systems, and coverage gaps. It supports local exact and fuzzy search, filtering by subject,
kind, owner, environment, source lane, freshness, and coverage, and a bounded “how are these connected?”
query. A connection path is labeled navigational reachability; it is not described as execution order,
causality, or completeness.

#### Behavior and flow trace

An end-to-end behavior is a typed `product-behavior-trace.v1` projection, not a path guessed from graph
reachability. It contains ordered and branched segments, actors, entry and exit contracts, conditions,
synchronous or asynchronous handoffs, state transitions, success paths, failure and compensation paths,
evidence references, and per-segment provenance, freshness, and coverage. A discontinuity is rendered as an
explicit unknown gap. Declared, observed, and computed segments remain distinguishable.

#### Integration inspection

An integration is a provider-neutral `product-integration-projection.v1` retaining direction, participants,
protocol, endpoint or event, request/message and response schema versions, authentication and authorization
boundaries, ownership, data classification, delivery and ordering semantics, retry and backoff policy,
idempotency, timeouts, failure modes, compensation, operational dependency, implementation/test bindings,
evidence, environment, authority lane, freshness, coverage, and unknown fields.

Declared design, code-observed structure, test-observed behavior, and separately authorized live observations
are parallel claims. The explorer never flattens them into one synthesized contract. A live-state provider is
separately authorized, environment-bound, time-bound, latency/cost-bounded, and optional; lack of credentials
or network access is typed absence, never inferred health.

#### Implementation drill-down

The explorer uses [code-intelligence-core](code-intelligence-core.md) to localize product concepts and
relations into bounded modules, files, symbols, configuration, tests, and generated artifacts. It retains the
provider's content-digest bindings and uncertainty. Source excerpts are quarantined, bounded, and optional;
the operator can understand the system without opening them and can inspect exact code when desired.

The explorer owns context, selection, and presentation. It may show an evidence summary and stable evidence
reference, but full claim-to-ground traversal is embedded from or handed off to
[evidence-explorer](evidence-explorer.md)'s contract. If evidence-explorer is absent, the full traversal is
typed unavailable; this module does not build a smaller competing evidence engine.

#### Change and impact exploration

The explorer presents provider-owned candidate impacts, reverse references, structural paths, tests, evidence,
coverage, and uncertainty for a proposed change. Paths computed by this module are explicitly navigational.
It does not claim completeness, issue a safety verdict, recommend merge, or turn an inferred relation into a
dependency fact. Human- or model-authored impact assertions remain separately versioned, reviewed claims.

#### Engine lens

The Engine lens is available on demand for every supported product selection in an Engine-managed repository.
It shows the traceability bridge described above, including missing or contradictory links. It explains which
Engine capability performed a role, what evidence the capability produced, what review or validation occurred,
which protections were unavailable or inapplicable, and what decision remains the operator's. It never treats
the existence of a run, check, or review as proof that the product behavior is correct.

#### Guided tours

An authored tour is a durable, reviewed sequence through real explorer selections: a system orientation, an
important user journey, a critical integration, a failure path, a change case, or an Engine-work trace. Each
step uses **product behavior → implementation → evidence → Engine work → operator authority**, where relevant.
Tours are skippable, resumable, and never gates to the underlying explorer.

### Product-system contracts and provider responsibilities

The existing product knowledge graph is structural substrate, not a complete system-description contract.
This module therefore defines neutral projection contracts for system elements, behavior traces, integrations,
subject identity, and product-to-Engine bridges. Their schemas include authority, evidence, freshness,
coverage, absence, contradiction, and mappings to code, tests, design, and delivery records. Providers may
populate only the fields their own contracts can support; the explorer never mines arbitrary prose or invents
the remaining fields.

The source and responsibility lanes are:

- [product-design](product-design.md): declared intent, architecture, specifications, decisions, and explicit
  structured system/integration declarations;
- [code-intelligence-core](code-intelligence-core.md): observed implementation bindings, localization,
  bounded references, structural walks, and candidate impacts without verdicts;
- [product-knowledge-graph](product-knowledge-graph.md): derived product structural facts and navigation;
- [evidence-explorer](evidence-explorer.md): full proof-chain navigation through stable references;
- narrow delivery, deployment, test, and review providers: provider-owned records and selected-object status;
- the Engine self-map and knowledge providers: the operating Engine's own structural and route facts; and
- reviewed explorer authoring artifacts: instructional framing and explicit proposed interpretations.

The explorer and [operator-cockpit](operator-cockpit.md) are sibling consumers of narrow provider contracts.
The cockpit owns global current-state composition. The explorer may show status scoped to the selected system
object and link to the cockpit for the whole operational picture. Neither consumes the other's composed
records, and explorer output never becomes cockpit input.

Every assertion is classified as `declared`, `observed`, `computed`, `inferred`, `instructional`, or `unknown`.
Declared design, observed implementation, computed structure, delivery records, and reviewed narration remain
visible side by side when they disagree. Each claim keeps source type, evidence reference, freshness, coverage,
confidence where meaningful, and contradiction membership. Precedence may select a display default but never
erase a contradiction. Unknowns, missing providers, unsupported languages, and partial observation cannot be
synthesized away. Reviewed narration never overrides underlying claims.

### Minimum source set and degraded-state matrix

The target module depends only on `core` for installation. It launches with a static bootstrap projection that
identifies the product and operating Engine subjects, names available providers and their state, exposes the
Engine inventory needed for cold discovery, and tells the operator which richer modes are supported. The
launch itself cannot depend on product-knowledge-graph, evidence-explorer, delivery history, a model service,
network access, JavaScript, or an already-current generated bundle.

Each mode declares its provider requirements and handles `absent`, `inactive`, `unsupported`, `partial`,
`stale`, `corrupt`, `unauthorized`, `over-budget`, and `incompatible` independently:

| Mode | Minimum admitted facts | Optional enrichment | Honest degraded result |
| --- | --- | --- | --- |
| Bootstrap and Engine inventory | core manifests, surface/route metadata, release identity | Engine graph | complete core inventory plus typed graph absence |
| Landscape/system map | any structured product-system provider | product design, product graph, code intelligence | scoped partial map with provider and coverage boundary |
| Behavior trace | one reviewed or provider-owned typed trace | implementation, tests, delivery evidence | known segments with explicit discontinuities |
| Integration inspection | one typed declared or observed integration record | live/deployment observation | parallel supported claims and unknown fields |
| Implementation drill-down | supported code-intelligence binding | product graph, evidence explorer | binding dossier or typed unsupported/partial state |
| Change exploration | provider-owned candidate-impact set | graph paths, tests, delivery evidence | bounded candidates with no completeness claim |
| Engine lens | validated product-to-Engine bridge and Engine identity | detailed delivery/review providers | proved trace plus typed missing links |
| Guided tour | reviewed tour compatible with the current projection | progress convenience | readable tour with stale/omitted steps identified |

A brownfield or mixed-language repository remains launchable. It may be sparse; it may never call itself a
whole-system map unless the declared scope is fully dispositioned. Required source corruption prevents the
affected projection from activating but preserves the last verified generation and the static bootstrap.

### Coherent snapshots, freshness, and bundle lifecycle

Generation binds every source to an explicit `explorer-source-set-manifest.v1`: product subject and revision,
operating Engine identity or run, provider/schema/parser versions, admitted source revision or digest,
authorization scope, generation time, coverage, typed omissions, and freshness policy. The generator detects
input movement before activation and aborts or retries rather than publishing a plausible mixed-revision
bundle. Independently changing or expired live evidence remains visibly time- and environment-bound.

Generation uses same-filesystem staging and immutable generation directories. Every generated file is
hash-bound into the manifest before one atomic current pointer switches. Launch verifies subject identities,
schema compatibility, authorization scope, and file hashes. Partial, tampered, cross-project, mixed-subject,
or incompatible output never activates. Failure preserves the last verified generation and records a bounded,
redacted reason outside it. Stale output remains readable but never presents itself as current.

The renderer produces a bounded multi-page semantic HTML core with stable deep links, ordered indexes, text
alternatives for diagrams, exact lookup, and every admitted claim available without JavaScript or a server.
Progressive local JavaScript may add fuzzy search, highlighting, filtering, and bounded path queries over
page-scoped or precomputed indexes. If scripting or its query substrate is unavailable, semantic navigation
and browser find remain complete; an unavailable on-demand query reports that limitation. No local server,
runtime model call, network fetch, or local JSON request is required to read the core projection.

Large and adversarial inputs are bounded by declared repository-class budgets for files, bytes, objects,
nodes, edges, field length, nesting, trace depth, path count and length, cycles, CPU, memory, generation time,
model context, output size, and retained generations. Cancellation is safe. Truncation produces typed partial
results with the omitted scope and reason. The late-v1 gate measures end-to-end generation and launch cost on
representative repository classes before selecting numeric budgets, incremental-regeneration rules, and
scheduling policy.

### Authoring and explanation

The manual-first authoring artifact, provisionally `product-system-explorer-narrative.v1`, contains the
instructional text, guided-tour sequence, assertion ledger, source references, subject/revision range,
generated-versus-human boundaries, author and reviewer, approval time, invalidation triggers, and display
classification. Source changes select affected assertions for re-review. The explorer works without any
authored narration; structural and evidence views remain available.

A model may be invoked only through a separate, explicit authoring action. Its output is an untrusted proposal:

- repository content is data, never instruction and never authority to invoke a tool or action;
- context is allowlisted, classified, size-bounded, and isolated from unrelated project or operator data;
- the authoring environment is tool-less, network-denied, and unable to read outside the admitted snapshot;
- every proposed claim retains source provenance and classification;
- model/provider/configuration and admitted-input identities are recorded without copying prohibited content;
- diff-scoped human review and approval are required before publication; and
- lack of a model service never blocks generation, viewing, or regeneration.

### Authorization, disclosure, and the private-data wall

Being local or on demand is not access control. Viewing and generation require authorization to each product
and Engine source independently. Detail selection is a presentation control, not a permission boundary. A
generated bundle may contain only facts the generating principal could inspect directly and is stored under
project-scoped restrictive permissions. In a shared environment without enforceable per-viewer access, a
bundle is limited to the least common authorized disclosure scope or is not generated.

Export and publication are unsupported in the initial cut. A later export requires a separately authorized
sanitization pipeline, recipient disclosure scope, complete content and transitive-metadata inventory,
reclassification, removal of machine-local references, and proof that the export contains nothing the
recipient could not inspect at the source. Copying the ordinary local static bundle is never presented as a
safe export path.

Source admission is allowlist-only and source-specific. Adapters canonicalize paths inside the exact admitted
root; reject traversal, symlinks, special files, ignored or unapproved files, and root escape; take a coherent
snapshot; and parse data inertly under byte, object, nesting, expansion, and work limits. Environment values,
credentials, secret stores, Git history, customer samples, issue content, operator memory and pins, personal
data, and arbitrary unclassified repository prose are excluded unless a later contract explicitly admits a
least-data field with its own authorization and redaction policy.

Classification follows every retained or emitted value, including text, identifiers, URLs, HTML attributes,
accessibility labels, diagrams, print output, search indexes, evidence references, manifests, diagnostics,
temporary files, and audit records. Unknown fields and sinks fail closed. A purge operation removes every
derived bundle, cache, index, authoring proposal, progress record, and diagnostic for a subject, and verifies
that no current pointer or retention record still names it. Fixing the source is not considered sufficient
deletion.

Repository-controlled labels, Markdown, links, diagrams, and assets are hostile data. Rendering uses escaping
or DOM `textContent`, restricted URL schemes, generated internal destinations, a restrictive content-security
policy, fixed local assets, and no active repository content, `innerHTML`, inline handlers, `eval`, dynamic
code generation, remote fonts, analytics, telemetry, or network request. Logs and normal errors contain no raw
source excerpt, absolute path, username, secret, or personal value.

### Accessibility and interaction

The unenhanced pages provide semantic headings and landmarks, logical reading and focus order, labeled
controls, keyboard navigation, screen-reader names, visible focus, WCAG AA contrast, zoom and reflow, print
completeness, reduced-motion behavior, and text equivalents for every map and trace. Meaning never depends on
color, motion, drag, hover, sound, timing, spatial layout, or scripting.

Enhanced graph selection highlights the same object in the map, detail panel, trace, and guided-tour step, but
the ordered text representation carries the identical selection and relationships. Search and path results
announce scope, limit, freshness, and partial-result state. The explorer does not gamify comprehension, use
demeaning personas, shame an incorrect choice, or require quizzes before detail is available.

### Relationship to `engine-parts`

The operator has selected this module as the intended successor to `engine-parts`, which currently supplies
the only operator-readable system-wide Engine inventory. This document does **not** retire that command.
[Decision 0336](../../adr/0336-route-operator-and-model-workflows-through-generated-canonical-surfaces.md) and
the settled [core](core.md) specification continue to govern until a future implementation proves replacement
and a separate operator decision explicitly supersedes them.

The required sequence is:

1. add the explorer without weakening or changing `engine-parts`;
2. define a field-by-field parity matrix and run old and new projections over the same representative Engine
   profiles;
3. prove static/no-JavaScript cold-session discovery with no current bundle, plus stale, corrupt,
   incompatible, over-budget, and failed states;
4. inventory and migrate documentation, skills, tests, scripts, and supported external automation that call
   `engine-parts`;
5. run a compatibility period in which the old command provides an actionable notice or forwards to the
   replacement while retaining recovery behavior;
6. record rollback criteria and prove the recovery path when the explorer is unavailable or corrupt; and
7. accept a superseding ADR and change the core catalog, generated surfaces, checks, and documentation before
   removing the old route.

Parity covers at least Engine identity and version; governed surfaces; installed, declined, inapplicable, and
unavailable modules; dependencies and governed files; operator commands; automatic routes, owning modules,
canonical targets, and availability; typed absence and degradation; freshness/currentness; complete static and
accessible output; and discoverability from a cold session. Fixtures cover no bundle, corrupt bundle,
unsupported provider, and JavaScript-disabled viewing. Fact equivalence is machine-checked and operator
readability is observed.

If the explorer is not universally installed and launchable, a minimal core bootstrap remains permanently to
report Engine identity/version, explorer availability and degradation, and how to reach the inventory. The old
name may still retire, but its guaranteed cold-start function may not.

### Boundaries with nearby capabilities

- [product-knowledge-graph](product-knowledge-graph.md) remains the derived structural map of the product. The
  explorer consumes it and owns presentation, navigation, typed traces, integration projections, and authored
  tours; it does not become graph authority or scan product code a second time.
- [code-intelligence-core](code-intelligence-core.md) owns observed code bindings, localization, structural
  walks, and bounded candidate impacts. The explorer does not convert its dossiers into verdicts.
- [product-design](product-design.md) owns declared specifications, architecture, and decisions. The explorer
  does not mine prose or silently promote narrative to structured fact.
- [evidence-explorer](evidence-explorer.md) owns full claim-to-ground traversal. This module preserves context,
  summarizes, and hands off through a stable evidence reference.
- [operator-cockpit](operator-cockpit.md) owns the global current-state and “what needs me” composition. This
  module shows selected-object context and links outward.
- Getting started remains the concise first read. It discovers the explorer but does not absorb its system
  model.
- The Engine self-map remains the structural source for the operating Engine subject. The explorer does not
  merge it with the product graph.

### Reference implementations and provenance

Two external repositories informed this preserved design:

- [`zarazhangrui/codebase-to-course`](https://github.com/zarazhangrui/codebase-to-course), reviewed
  2026-08-18, contributed the initial idea of a guided, navigable introduction. No visible license was found at
  review time. This design is clean-room with respect to it: no code, assets, templates, distinctive wording,
  interaction sequence, or tests may be copied without compatible permission and explicit provenance review.
- [`Egonex-AI/Understand-Anything`](https://github.com/Egonex-AI/Understand-Anything), reviewed at commit
  [`32944829e7a63a9fa9c55d811d7f98a9530c6a6a`](https://github.com/Egonex-AI/Understand-Anything/commit/32944829e7a63a9fa9c55d811d7f98a9530c6a6a),
  demonstrated useful interaction ideas: a guided panel that highlights graph nodes, local exact/fuzzy search,
  bounded connection paths, and typed repository freshness. Its MIT license makes later attributed reuse
  possible, but this decision authorizes none. Any reuse receives an explicit dependency, security, license,
  provenance, and maintenance review.

The Engine does not adopt either repository's generic codebase-course framing, audience personas, runtime LLM
improvisation, committed graph exports, automatic update hooks, local server, chat, or a second product scanner.
Claims from a reference UI are revalidated against its implementation before reliance.

### Manifest shape if the design is later accepted

| Field | Provisional value |
| --- | --- |
| `id` | `product-system-explorer` |
| `distribution` | `required` if it supersedes `engine-parts`; otherwise the cold-start core inventory remains |
| `applicability` | `universal`, with typed provider and language support rather than false completeness |
| `activation` | on-trigger and ungated for authorized local viewing; never auto-opens at boot |
| `depends` | `core`; all product, graph, evidence, delivery, live-state, and narration providers integrate through versioned optional contracts |
| `provides` | identity, system-element, behavior-trace, integration, bridge, narrative, source-set and bundle schemas; deterministic generator and static launcher; system map, trace, integration, drilldown, impact, Engine-lens and guided-tour views; parity, provenance, access, confinement, contradiction, freshness, bundle-integrity, boundedness, static-safety, accessibility and purge checks |
| `wires` | generated canonical discovery surfaces plus the chosen cache/ignore wire; no current route while parked |
| `migrations` | disposable bundles are regenerated; `engine-parts` migration follows the separate compatibility sequence above |

### Operator and automatic workflow routing

**Current disposition: `none` (parked design).** No command, skill, route, schema, module, or automatic hook
exists for this unbuilt capability. If later accepted, its generated canonical entry must work from a cold
session and report its own absent, stale, partial, corrupt, incompatible, unauthorized, or failed state. It
never widens Build authority, performs an operator action, or publishes an artifact automatically.

### Mandatory late-v1 revalidation

Before this draft can settle, enter a delivery phase, receive a breakout issue, authorize implementation, or
alter `engine-parts`, the operator reviews and records:

- whether detailed product-system understanding and product-to-Engine traceability remain the right outcome;
- whether the then-current product-design, code-intelligence, product graph, evidence, delivery, cockpit, and
  Engine self-map contracts can populate the projection schemas without duplicated authority;
- the minimum launchable source set, provider/degraded-state matrix, brownfield and mixed-language behavior,
  and field-level `engine-parts` parity fixture;
- required versus optional distribution, activation, route, cold-start bootstrap, compatibility period,
  migration inventory, rollback criteria, and retirement decision sequence;
- supported repository classes, local/runtime architecture, cache home, generation scheduling, incremental
  refresh, browser/assistive-technology matrix, and measured resource budgets;
- authorization, disclosure, secret/personal-data handling, purge, participant protocol, live-state provider,
  export, dependency, and supply-chain policies;
- the authoring owner, reviewer, assertion invalidation workflow, and whether model-assisted drafting is worth
  retaining; and
- source-license and provenance decisions, including whether any attributed MIT reuse is desirable.

That decision chooses whether the explorer joins or follows delivery wave 7, remains parked, changes shape, or
is retired. A separate later decision governs any `engine-parts` deprecation. Detailed preservation now does
not make a future implementation inevitable.

### What stays out

- a generic “turn any codebase into a course” product;
- an intelligence-reducing, persona-based, or code-averse view of the operator;
- runtime AI-authored answers, safety advice, chat, or improvised explanations;
- a second product scanner, product graph, evidence engine, impact verdict, current-state cockpit, or decision
  surface;
- graph reachability presented as execution, causality, completeness, or safety;
- hidden contradiction resolution, inferred health, or missing facts filled with plausible prose;
- unapproved live access, credentials, telemetry, analytics, hosted service, network dependency, or daemon;
- mandatory animation, graph interaction, quizzes, progress storage, code reading, or JavaScript;
- automatic publication or ordinary-bundle export; and
- current removal or weakening of `engine-parts`.

## Acceptance criteria

*These are future release gates, not claims that the capability exists. `engine` means a named merge-gated
check can fully assert the criterion; `operator` means human observation or judgment carries part of it.*

| Criterion | How verified | Who checks it |
| --- | --- | --- |
| **Identity never collapses subjects** — every object carries the composite envelope and every cross-subject relation is a validated bridge. | Collision fixtures reuse paths, names, graph IDs, and commits across product, operating Engine, and Engine-as-product; invalid, stale, unauthorized, ambiguous, and revision-mismatched bridges fail closed. | engine |
| **A known boundary can be mapped** — on an ordinary Engine-managed product, the operator identifies the declared boundary, owned/external components, trust boundary, evidence, and one deliberate coverage gap. | A seeded system fixture has a known answer, a missing provider, and a conflicting observation; completion requires naming the boundary, source, gap, and degraded result without reading source code. | operator |
| **A real behavior can be traced** — the operator follows a known cross-component user or business flow through sync, async, branch, and failure segments. | The trace fixture has ordered evidence, one compensation path, and one discontinuity; completion requires distinguishing the proved path from the unknown hop. | operator |
| **An integration can be inspected without false synthesis** — declared and observed protocol, schema, auth, retry/idempotency, ownership, and failure behavior remain distinguishable. | A fixture contains an intentionally stale design claim and partially observed integration; completion requires identifying the contradiction, freshness, missing fields, evidence, and safe degraded conclusion. | operator |
| **Concept-to-ground drilldown preserves authority** — the operator moves from a product concept to code/test bindings and full evidence without losing subject or revision. | Deep links round-trip through code intelligence and evidence-explorer; absent evidence-explorer yields typed unavailability rather than a substitute proof chain. | operator |
| **Impact remains bounded advice** — candidate impacts and paths retain provider ownership, scope, uncertainty, and coverage. | A negative fixture hides a real dependency outside provider coverage; the explorer reports bounded candidates and never claims completeness, safety, or merge readiness. | engine |
| **The Engine lens explains the SDLC work** — from a selected product change, the operator identifies intent, decisions, implementation activity, tests, reviews, unresolved uncertainty, and their remaining authority. | A seeded delivery record includes an unavailable check and an unresolved decision; completion requires finding both and not treating the review as correctness proof. | operator |
| **`engine-mechanic` keeps its two Engines distinct** — the Engine product under construction is never confused with the operating Engine instance building it. | A scenario uses colliding module names and file paths at different revisions; completion requires pivoting product → Engine work → product while naming both subject identities and evidence. | operator |
| **Contradictions and unknowns survive composition** — narration and precedence cannot erase conflicting or missing claims. | Policy fixtures combine declared, observed, computed, inferred, live, and instructional claims; rendered output preserves every admitted conflict, absence, freshness, coverage, and source lane. | engine |
| **Provider absence degrades per mode** — brownfield, mixed-language, absent, inactive, unsupported, partial, stale, corrupt, unauthorized, over-budget, and incompatible inputs never become whole-system claims. | The declared provider matrix runs one fixture per state and mode; unaffected views and the bootstrap remain usable while affected views show typed scope and next step. | engine |
| **Snapshots are coherent and bundles atomic** — mixed-revision, partial, tampered, cross-project, or cross-authorization bundles never activate. | Drift-during-generation, crash-point, hash-tamper, instance-swap, expired-live-data, concurrent-writer, repair, and cleanup fixtures preserve the last verified bundle and exact stale reason. | engine |
| **Static access is complete and accessible** — every admitted claim, text alternative, deep link, and exact lookup works without JavaScript, storage, network, or server. | JavaScript-disabled, storage-disabled, network-denied, keyboard, screen-reader, zoom/reflow, reduced-motion, and print walkthroughs cover the same scenario tasks; enhanced-only fuzzy/path queries disclose their absence. | operator |
| **Hostile inputs cannot act or escape** — product content cannot execute, authorize actions, alter model instructions, disclose unrelated data, escape roots, create active markup, or exhaust unbounded work. | Fixtures cover prompt injection, tool requests, traversal, symlinks, special files, parser expansion, cyclic/path explosion, hostile Markdown/URLs/assets, secrets, personal data, hidden output sinks, limits, cancellation, and typed truncation. | engine |
| **Authorization is non-amplifying and purge is complete** — product and Engine access are checked independently and derived data does not outlive deletion. | Separate-principal fixtures prove depth controls do not bypass source permissions; purge inventories and removes bundles, indexes, proposals, progress, diagnostics, pointers, and retention records. | engine |
| **Narration is optional, reviewable, and subordinate** — model text is a tool-less/network-less proposal with claim provenance and diff-scoped approval. | Publication rejects unreviewed, unclassified, stale, prompt-injected, over-context, or source-overriding proposals; structural views regenerate with no model service. | engine |
| **`engine-parts` parity is proved before deprecation** — old and new projections expose equivalent core facts and cold-start recovery. | A field-by-field matrix runs both projections over representative module/route profiles and no-bundle, corrupt, stale, unsupported, and no-JS states; machine consumers are inventoried and operator readability is observed. | operator |
| **Retirement is separately governed and reversible** — additive delivery, compatibility, dependent migration, rollback, and explicit superseding decisions occur before removal. | Release evidence names the compatibility period, supported dependent migrations, rollback drill, retained bootstrap or universal availability, superseding ADR, core-catalog change, and operator acceptance. | operator |
| **Performance claims are measured** — representative repository classes meet declared end-to-end generation, launch, query, memory, and bundle budgets. | Network-denied large/adversarial fixtures exercise limits, cancellation, incremental refresh, retention, and typed partial results; numerical budgets are set only from late-v1 measurements. | engine |
