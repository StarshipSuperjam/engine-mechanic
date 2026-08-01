# SAM provenance — the Engine's predecessor methodology

This folder preserves the methodology layer of **SAM** (PMO Systems Architecture Manual), the operator's
pre-Engine project (February–June 2026): a constitutionally governed architecture for a professional-services
delivery system, built in the operator's spare time and now retired. SAM's "engine" layer — its protocols,
session discipline, and governance instruments — is the direct ancestor of this Engine's methodology.
[engine-pre-history.md](engine-pre-history.md) tells that story.

## Provenance and sanitization

- The full original project (~1,400 files including its business-domain corpus) is preserved verbatim in the
  operator's **private archive**, outside this repository. This folder holds only the methodology documents.
- Because this repository is public, the copies here carry **marked redactions** — three lines where an
  employer or third-party platform name appeared, each replaced in place with a bracketed
  `[redacted — …]` marker. Nothing else was altered; these are otherwise verbatim historical documents.
- The Genesis Record (the origin narrative) is **not** copied — it is inseparable from workplace context. Its
  methodology arc is retold, genericized, in [engine-pre-history.md](engine-pre-history.md).
- Two instruments (the Semantic Control Ledger and the Boundary Matrix) are also not copied: their content
  *is* the workplace architecture's concept inventory. Their patterns are described in the intake issues this
  salvage filed.

## Inventory

| Document | What it is | Why it earned preservation |
|---|---|---|
| [SAM_Design_Reasoning.md](SAM_Design_Reasoning.md) | Decision-rationale register (13 entries) | Ancestor of the eADR idea; carries a crisp inclusion test: "would its absence risk a future session reversing the decision without understanding the constraint?" |
| [SAM_Methodology_Health_Check_001.md](SAM_Methodology_Health_Check_001.md) | Empirical review of 45 audited sessions | Real telemetry on an AI-governed methodology under load: schema drift without validation, context-budget violations found and fixed, and the finding that enforcement gaps invisible until an outside observer asks are the highest-risk governance failure class |
| [SAM_Session_Control_Architecture.md](SAM_Session_Control_Architecture.md) | How sessions start, carry state, and end | Cold-start protocols, session-end discipline, primary-source vs derived-view rule, the 40% orientation-context ceiling, and the growth-vector table (per-artifact growth triggers and mitigations) |
| [SAM_Shared_Protocol_Core.md](SAM_Shared_Protocol_Core.md) | Domain-agnostic process governance | The gated session sequence, universal AI work constraints, explicit failure conditions, observation-triage rule, and a worked extension architecture |
| [SAM_Expression_Baseline.md](SAM_Expression_Baseline.md) | Shared expression governance | Prohibited registers (legal doctrine, governance-for-its-own-sake), mechanical compliance indicators, and quality tests for governed prose |
| [SAM-DOC-005_AI_Expression_Contract.md](SAM-DOC-005_AI_Expression_Contract.md) | The constitutional expression contract | The voice-leakage discovery made structural: dual-mode communication (architecture voice for governance review, business voice for everyone else) — ancestor of the Engine's plain-language conduct |
| [SAM_Cascade_Protocol.md](SAM_Cascade_Protocol.md) | Cross-document dependency schema | Typed dependencies (constrains / realizes / collision_risk / informs), impact traversal, conflict adjudication tiers, and the coverage-gap lifecycle with mandatory reassessment triggers |
| [SAM_Ideation_Protocol.md](SAM_Ideation_Protocol.md) | Idea-intake pipeline | Capture → review → adversarial gate-check → consumption lifecycle with per-entry files and resolution-based archiving |

## How to read these

They describe hand-run AI chat sessions against a filesystem — pre-agentic tooling. Read them for the failure
modes they name and the discipline they derived, not for their mechanics. Where a document names artifacts
that only existed in SAM (Foundation Reference, domain protocols, startup prompts), those stayed in the
private archive with the rest of the project.
