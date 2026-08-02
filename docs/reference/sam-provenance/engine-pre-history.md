# The Engine's pre-history: the SAM project

**Status:** Historical provenance note — rewritten for this public repository from the SAM project's own
Genesis Record (February–June 2026). The verbatim original, which carries workplace context that does not
belong in a public repository, survives in the operator's private archive. This retelling preserves the
methodology arc and omits the organization, the people, and the business specifics.

## Why this note exists

The Engine did not begin with engine-template. Its methodology — constitutional governance authored with AI,
session-boundary discipline, issue registers, change logs, decision-rationale records, expression governance —
was first built and battle-tested in **SAM** (PMO Systems Architecture Manual): a governed architecture for a
professional-services delivery system, built by the operator in their spare time over roughly two months.
SAM's business purpose is dead; its machinery is the Engine's direct ancestor. This note preserves how that
machinery came to be, because none of it is recorded anywhere else in this repository's history.

## The arc

**An implementation plan becomes an architecture.** SAM began as a ~34-page, eight-phase automation
implementation plan produced from iterative AI conversations about structural inefficiencies in a delivery
system. Through iteration it grew past 110 pages and changed nature: the pivotal insight was that *solving
operational issues with automation merely accelerates flawed processes* — the sustainable fix is resolving the
structural problems underneath. The document shifted from prescribing automation to constitutionally governing
the delivery system itself: authority domains, structural invariants, canonical identity, separation of
execution surface from automation substrate.

**The constitutional framing was borrowed from AI safety — in reverse.** The operator had learned that
Anthropic used "constitutional" constraints to bound Claude's behavior, and applied the same pattern the other
way around: constitutional constraints on a *human process*, authored with AI assistance. A retrospective
distinction the Genesis Record insists on: the constitutional specification was not the design goal. It
emerged as **the minimum requirement for AI to reason coherently about the system** — the governance framework
is a byproduct of the specification rigor AI consumption demands.

**The voice-leakage discovery.** The first document drafted from the constitutional architecture was not the
charter — it was the AI Expression Contract (preserved here as
[SAM-DOC-005](SAM-DOC-005_AI_Expression_Contract.md)). The reason was practical: colleagues who asked an
AI assistant about early drafts got back the architectural voice, and reacted badly — one described it as
sounding like "a software engineering lawyer." The discovery: constitutional-grade specification, while
necessary for AI reasoning, is **toxic to organizational adoption if the AI reproduces that voice to end
users**. Specification and communication must be governed separately — speak architecture to the architect,
business language to everyone else. That principle became structural (the dual-mode
communication governance in DOC-005) and survives today in the Engine's plain-language conduct.

**The semantic-control discovery.** A research query about reducing AI drift across long, fragmented document
corpora returned OWL/RDF graph-data methods. Adapted, these became the **Semantic Control Ledger** (one owning
document per concept, tracked across the corpus) and the **Boundary Matrix** (what each document may mention
only at boundary level, and must never define), with named high-risk collision pairs between documents. These
were invented as *AI reliability tools* — keeping a model from drifting while reasoning across a fragmented
corpus — and became governance tools secondarily.

**Multi-session orchestration by hand.** Before agentic tooling, the drafting protocol ran as a manual
pipeline across chat sessions: structured output passed from one session to another for drafting, a third for
harvesting governance outcomes, then back to the source for record. That hand-run pattern — separate
orchestration, work, and review contexts with structured handoffs — is the recognizable precursor of the
gated sequence and control-session model, and ultimately of the Engine's build orchestration.

**The engine extraction.** With two document domains complete, the shared tooling was consolidated into the
"SAM Engine" — an explicit three-layer split of **corpus** (the governed documents), **engine** (protocols,
standards, session infrastructure), and **program state** (the living picture sessions load at startup). From
that point the record is complete: every change carried a change-log entry, every session an audit record.
The layering — and the lesson that the engine layer must be extracted *from* real work rather than designed
in advance — carried directly into engine-template.

**The hard loss that shaped session discipline.** The entire first drafting cycle's session artifacts were
lost because nothing required writing session outcomes to disk before the session ended. That loss is the
direct origin of the closeout-persistence rule ("nothing survives the session boundary except what is written
to the filesystem") — the ancestor of the Engine's session-end and memory discipline.

## What the salvaged documents are

The eight documents preserved alongside this note are the SAM Engine's methodology layer, copied verbatim
(three marked redactions). See the [README](README.md) for the inventory and what each contributes. The
business-domain corpus they governed was left behind deliberately: it is specific to a workplace and carries
no design value the methodology documents don't already distill.

## Reading this material honestly

These documents describe a system built for hand-run AI chat sessions against a filesystem, before agentic
tools, subagents, or CI existed in the workflow. Their value is not the mechanics (many are superseded) but
the **failure modes they name and the discipline they derived** — most of which the Engine re-derived or
inherited: cold-start cost, session-boundary state loss, stale derived views, context-budget growth,
enforcement gaps invisible until an outside observer asks, telemetry schema drift. Where the Engine lacks an
analogue (concept-ownership ledgers, coverage-gap lifecycles, growth-vector tables, typed session telemetry),
those ideas entered the Engine's intake as issues rather than being adopted silently.
