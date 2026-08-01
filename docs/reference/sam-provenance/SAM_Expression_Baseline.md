# SAM Expression Baseline

**Version:** 1.1
**Created:** 2026-04-02
**Status:** Active — Tier 2 deliverable
**Governing document:** SAM Governed Build Plan
**Source:** SAM Factoring Analysis v1.0, Section 3.2
**Upstream authority:** SAM-DOC-005 AI Expression Contract
**Failure mode addressed:** Without a shared expression baseline, each domain develops its expression conventions independently. Voice consistency across the corpus degrades as domains diverge. Amendments made years after original authoring no longer read as if they belong. The expression baseline defines the communicative contract that all SAM artifacts must satisfy, regardless of domain.

---

## 1. Purpose and Scope

This document defines the shared expression principles that govern how meaning is communicated across all SAM artifacts. It is the communicative counterpart to the Shared Protocol Core's process governance: the protocol core governs how work gets done; the expression baseline governs how work reads.

**This document governs:**

- The governing principles that all SAM artifacts must satisfy
- Structural conventions shared across all document-producing domains
- Prohibited expression registers
- Quality tests applied to all governed prose
- The extension architecture for domain expression standards

**This document does not govern:**

- Domain-specific voice registers (those belong to domain expression standards)
- Domain-specific heading conventions beyond shared minimums (domain extension)
- Per-artifact structural conventions (domain extension)
- Domain-specific rhetorical patterns like classification-set presentation or adjacent-meaning distinction (domain extension)
- Domain-specific closing-section conventions (domain extension)
- Process governance (that belongs to the Shared Protocol Core)

**Relationship to DOC-005:** DOC-005 (AI Expression Contract) is the constitutional authority for how meaning is communicated in SAM. This baseline derives from DOC-005. It cannot override DOC-005. Where DOC-005 establishes a principle, this baseline operationalizes it into enforceable conventions. Where DOC-005 is silent, this baseline may add conventions that are consistent with DOC-005's principles.

**Relationship to the Shared Protocol Core:** The expression baseline and the shared protocol core are peer governance surfaces. Neither subsumes the other. The protocol core governs process (how sessions work, what artifacts are required, when authorization gates fire). The expression baseline governs communication (how prose reads, what structural conventions apply, what registers are prohibited). Domain protocols reference both.

**Relationship to domain expression standards:** Each domain maintains a domain expression standard that extends this baseline. The domain standard inherits all shared principles and conventions, then adds domain-specific voice registers, heading rules, per-artifact structural conventions, and any additional conventions the domain's artifacts require. Domain standards may not weaken the shared baseline.

---

## 2. Governing Principles

These principles derive from DOC-005 and apply to every governed SAM artifact in every domain. They are the expression-layer equivalent of the Shared Protocol Core's governing rules — domain standards may add principles, not remove or relax these.

### 2.1 Meaning Invariance
The meaning of a governed statement must not shift when context shifts. A reader encountering the statement in a different session, a different year, or from a different starting document must derive the same meaning. If a statement's meaning depends on surrounding prose for disambiguation, it is expression-fragile and must be revised.

### 2.2 Communicative Sufficiency
Every governed artifact must communicate enough for a competent reader to understand what it establishes, what it constrains, and why — within its own scope. The artifact may reference other artifacts for related content. It may not require other artifacts to make its own claims understandable. This is the expression-layer analog of the Shared Protocol Core's self-sufficiency preservation rule.

### 2.3 Interpretive Boundedness
Governed prose must constrain its own interpretation. A reader should not be able to reasonably derive contradictory implications from the same passage. Where ambiguity exists, the artifact should either resolve it explicitly or declare the boundary of its own interpretive reach. "This document does not address X" is a legitimate interpretive boundary.

### 2.4 Layer Appropriateness
Governed prose must stay within its artifact's layer. Constitutional artifacts read like constitutional documents. Architectural artifacts read like architectural descriptions. Implementation artifacts read like implementation specifications. When a passage begins to read like a different layer — when governance prose becomes implementation guidance, or architectural description becomes legal doctrine — the register has drifted and must be corrected.

### 2.5 AI Legibility
Every governed artifact must be parseable and actionable by an AI reasoning system operating under protocol governance. This means: unambiguous structural markers (headings, bold terms, consistent formatting), machine-recoverable relationships between concepts, and sufficient context for a cold-starting AI to determine what the artifact establishes and constrains without relying on conversation history or unstated context.

### 2.6 Corpus Coherence
Governed artifacts across domains must read as parts of the same program, not as isolated documents produced by different teams. The expression baseline is the mechanism that produces this coherence — shared structural conventions, shared prohibited registers, and shared quality tests ensure that an ARCH document and a DOC document are recognizably members of the same corpus.

### 2.7 System Embodiment
Every governed artifact must remain visibly grounded in the PMO delivery system as a working architecture. The system — its workspaces, automation, reporting, identity, and operational reality — must be recoverable from the prose. An artifact that reads as abstract governance theory disconnected from any real system has failed this principle. [Source: DOC expression standard, consistent with DOC-005]

### 2.8 Business-Operating Subordination
Governance language must remain subordinate to the delivery system it describes. The prose serves the system; the system does not serve the prose. When governance precision begins to take on a life of its own — when the reader can no longer tell what real system behavior the governance language is protecting — the expression has drifted. [Source: ARCH expression standard, consistent with DOC-005]

*Note: Principles 2.7 and 2.8 express the same core commitment from different angles. 2.7 asks "can the system be recovered from the prose?" 2.8 asks "is the prose still serving the system?" Both must be true. They are stated separately because they catch different failure modes: 2.7 catches prose that has become too abstract; 2.8 catches prose that has become too self-referential.*

---

## 3. Shared Structural Conventions

These conventions apply to all domains that produce governed documents. Domains that produce non-document artifacts (configurations, scripts, operational procedures) adopt the conventions that apply to their artifact types; they are not required to adopt document-specific conventions.

### 3.1 Bold as Definition Marker

Bold text in governed documents has one meaning: **a governed term or structural concept is being identified here.** This applies to the first or defining occurrence of a term within its defining artifact, and to the first occurrence within each consuming artifact when the term is being specifically invoked.

**Bold is not used for:**
- General emphasis ("this is *very* important")
- Subsequent mentions of already-defined terms within the same section
- Heading text (headings are already visually distinct)
- Entire paragraphs or sentences
- Drawing attention to warnings, caveats, or important notes

This convention ensures that bold text is a reliable signal. A reader scanning a document can find every governed term by looking for bold text. If bold is used for general emphasis, this signal becomes noise.

### 3.2 List Conventions

**Default to prose.** The default expression mode for governed documents is narrative prose with paragraph structure. Lists are a structural relief mechanism, not a primary composition mode.

**Lists are permitted when:**
- The items are genuinely discrete and parallel (a set of named session types, a set of invariants, a set of required fields)
- The list provides structural relief after sustained prose
- The items benefit from visual scanning rather than inline reading
- Order matters and must be explicit (use numbered lists for ordered items, bullet lists for unordered items)

**Lists are not permitted when:**
- They replace narrative reasoning ("Here are the three reasons..." followed by bullet points that each need a paragraph of explanation)
- They fragment continuous argument into disconnected points
- They are used as the default formatting mode for everything
- Individual list items exceed 3–4 sentences (at that point, use paragraphs with bold-lead structure instead)

### 3.3 Prose Density and Structural Relief

**Paragraph length:** 3–8 sentences per paragraph as a working heuristic, not a hard rule. Paragraphs shorter than 3 sentences may be too fragmentary. Paragraphs longer than 8 sentences may be too dense. The test is whether the paragraph develops a single coherent idea within a readable span.

**Structural relief mechanisms** (used to break sustained prose):
- Heading breaks (new section, new subsection)
- Paragraph breaks (new paragraph within a section)
- Bold-lead paragraphs (bold the opening term or concept, then continue in regular prose)
- Permitted lists (per Section 3.2)

**Wall-of-prose heuristic:** Approximately 6 paragraphs of sustained prose without any structural relief (heading, bold-lead, or list) signals a passage that likely needs reorganization. This is a readability flag, not a formatting rule. Some sustained passages are necessary and well-structured. But a cold-starting AI or a returning human reader will struggle with unbroken walls of text.

### 3.4 Horizontal Rule Prohibition

Markdown horizontal rules (`---` or `***`) are not used in governed documents. They do not convert reliably to docx format via the publish pipeline. Section breaks are achieved through headings. Within-section breaks are achieved through paragraph spacing.

### 3.5 Design Rationale Requirement

Every domain expression standard must include a design rationale section explaining key decisions. The rationale grounds the conventions in their purpose — a future maintainer modifying a convention can evaluate whether the rationale still applies. A convention without a rationale is a convention that can only be followed or ignored, not intelligently revised.

The expression baseline itself does not require a design rationale for each convention (the conventions are grounded in the governing principles and the factoring analysis). Domain standards, which add domain-specific conventions that may appear arbitrary without context, must explain their choices.

---

## 4. Prohibited Registers

Governed SAM prose must not drift into the following registers. These prohibitions apply regardless of domain.

### 4.1 Legal Doctrine Register
Governed artifacts must not read like legal documents, courtroom filings, or regulatory compliance texts. The delivery system is not a legal entity. Terms like "notwithstanding," "hereinafter," "pursuant to," and sentence structures that would be at home in a legal brief are prohibited. Governance precision is achieved through structural clarity, not legal formality.

### 4.2 Abstract Institutional Control Theory
Governed artifacts must not read like academic papers about governance, organizational theory, or institutional design. The artifacts describe a specific delivery system for a specific company. Abstract theorizing about "how governance works in general" has no place. Every governance claim must be traceable to a specific system behavior, authority boundary, or structural condition.

### 4.3 Governance-for-Its-Own-Sake
Governed artifacts must not produce governance structures that exist primarily to govern other governance structures. Governance serves the delivery system. When a reader cannot determine what real system behavior a governance passage is protecting, the passage has become self-referential. This is the most insidious register drift because it feels productive — the prose is precise, structured, and internally consistent, but it has lost contact with the system it describes.

---

## 5. Quality Tests

These tests are applied to all governed prose. They are post-writing checks, not pre-writing constraints — write first, then test, then revise if needed.

### 5.1 Register Test
After writing, ask: "Could a competent reader mistake this passage for legal doctrine, abstract governance theory, institutional control philosophy, or a courtroom filing rather than delivery-system governance?" If yes, revise the passage to restore system-grounding. Additionally ask: "Would an AI reasoning system learn how the governed system works as a coherent whole, or would it learn only that a collection of discrete rules exists?" If the latter, the passage needs more system context.

Both questions test the same property from different angles. The first catches passages that read wrong. The second catches passages that teach wrong.

### 5.2 Self-Sufficiency Test
After writing, ask: "Can this artifact's claims be understood without reading another artifact?" References to related content are acceptable ("ARCH-108 defines canonical identity" is a pointer). Explanatory dependency is not ("see ARCH-108 for why this matters" pushes required understanding out of scope). If the artifact cannot stand on its own within its declared scope, it fails the self-sufficiency test.

### 5.3 Delivery-System Recoverability Test
After writing, ask: "Can a reader recover the actual delivery system — its workspaces, automation, reporting, identity, and operational reality — from this prose?" If the prose has become abstract enough that no concrete system behavior is visible, it has failed. This is the expression-layer equivalent of the Shared Protocol Core's "preserve delivery-system intelligibility" rule.

---

## 6. Extension Architecture

### What domain expression standards must include

Every domain that produces governed documents maintains a domain expression standard that extends this baseline. The domain standard must contain:

1. **A reference to this document.** The domain standard states that it extends the SAM Expression Baseline and inherits all governing principles, shared structural conventions, prohibited registers, and quality tests defined here.
   *Structural criterion:* The extension declaration must enumerate all inherited elements by baseline section number. Selective inheritance is non-compliant.

2. **Voice register definitions.** What voice(s) the domain's artifacts use. DOC defines a two-register model (constitutional and narrative governance). ARCH defines a single register (business-operating architectural language). New domains define registers appropriate to their artifact types.
   *Structural criterion:* Must include a register test — a concrete, domain-specific question the writer applies to evaluate whether a passage is in the correct register. The test must be answerable from the passage alone without subjective aesthetic judgment.

3. **Heading conventions.** Which heading levels the domain uses, what conventions apply to heading text, and any domain-specific heading patterns. The shared baseline requires only that headings exist and are used for structural relief. Domain standards specify the details.
   *Structural criterion:* Must define the heading level model (which levels, what each level means structurally) and heading label conventions.

4. **Per-artifact structural conventions.** How each artifact type in the domain's corpus is structured. This includes standard section ordering, required sections, and domain-specific rhetorical patterns.
   *Structural criterion:* Every artifact in the domain's corpus must have a named entry with at least: expected major sections, composition mode (prose-primary, table-primary, list-primary, or mixed), and expression notes describing the artifact's communicative purpose.

5. **Domain-specific conventions.** Any additional conventions the domain needs that are not addressed in this baseline (classification-set presentation, distinction-section patterns, closing-section conventions, composition mode overrides).

6. **Domain-specific failure modes.** Expression-layer failure modes specific to the domain's artifacts. These supplement the shared quality tests in Section 5.
   *Structural criterion:* Each failure mode must describe a detectable structural symptom, not just a subjective quality concern.

7. **Mechanical compliance indicators.** Testable indicators for each domain-specific failure mode that enable independent verification of expression compliance. See Section 6.2 for requirements.

8. **Design rationale.** Explanation of key domain-specific decisions per Section 3.5.

### 6.1 What domain expression standards must not do

- **Weaken shared principles.** The governing principles are non-negotiable. A domain may add stricter expression requirements; it may not relax shared ones.
- **Override shared structural conventions.** The bold, list, prose density, and horizontal rule conventions apply everywhere. A domain may add conventions (e.g., "H4 is prohibited" in ARCH); it may not contradict shared conventions.
- **Duplicate shared content.** Domain standards reference this baseline; they do not re-state its content.

### 6.2 Required mechanical compliance indicators

Every domain expression extension must define testable compliance indicators for its declared failure modes. These indicators transform subjective expression assessment into mechanical detection that can be performed independently of the session that produced the work.

**For each domain-specific failure mode, the extension must define at least one indicator containing:**

- **Measurable condition.** What is counted, measured, or structurally checked. Must be a binary or threshold test, not a judgment call.
- **Detection scope.** Whether the indicator applies per top-level section, per document, or to a defined sample. "Top-level section" means the highest heading level used for major structural divisions in the domain's corpus, as defined in the domain's expression extension heading conventions (H1 for IMPL, H2 for ARCH and DOC). If sampled, the sampling rule must specify which sections and how selected — not AI-selected, not convenience-selected.
- **Threshold.** The value at which the indicator flags. Must be a number, a ratio, or a binary condition.
- **Flag severity.** Whether a flag indicates certain failure, probable failure requiring review, or a warning.

**Design constraint:** Indicators must detect structural symptoms of expression drift, not assess aesthetic quality. The AI can reliably count paragraphs between platform references, count unattributed prescriptive verbs, and check word order in ARCH-tracing passages. It cannot reliably judge whether a passage "sounds like" the right register — that judgment is the same one that produced the work and is therefore circular. Indicators that rely on the AI making the same kind of judgment that produced the work do not count as mechanical compliance.

Mechanical compliance indicators are defined in the domain expression extension itself — no additional artifact is required. They are applied during control session draft processing per SPC Section 10.1 rule 4. The indicators are part of the expression extension's contract surface — a domain extension that ships without defined indicators does not meet the extension contract.

### 6.3 Extension contract validation

At shell construction, the domain expression extension is validated against this section's requirements item-by-item. At minimum: does the extension cover all 8 required elements? Does each failure mode have at least one mechanical indicator meeting the Section 6.2 specification? Are the structural criteria for items 1–6 satisfied? The validation result is recorded in the shell construction session audit record.

---

## 7. What This Baseline Expects to Exist

- **SAM-DOC-005** — the constitutional authority for expression governance. This baseline derives from DOC-005.
- **Per-domain expression standards** — each document-producing domain maintains a standard that extends this baseline.
- **The Shared Protocol Core** — governs process; this baseline governs communication. Both are peer governance surfaces.
- **The Foundation Reference** — provides the constitutional and architectural context that informs expression decisions.

---

## 8. Versioning

This document is updated when structural expression decisions change — new shared conventions adopted, existing conventions revised, or domain signal (especially from IMPL) forces revision of the shared/domain boundary.

### Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-04-02 | Initial extraction from factoring analysis. Shared governing principles (8), structural conventions (5), prohibited registers (3), quality tests (3), extension architecture. |
| 1.1 | 2026-04-14 | Extension architecture formalized (ENG-ISS-003 resolution). Section 6 restructured with subsections 6.1–6.3. Extension surface contract: 8 required elements with structural criteria (up from 6 without criteria). Domain-specific failure modes promoted from implicit to required (item 6). Mechanical compliance indicators added as required element (item 7, Section 6.2). Validation gate at shell construction (Section 6.3). |
