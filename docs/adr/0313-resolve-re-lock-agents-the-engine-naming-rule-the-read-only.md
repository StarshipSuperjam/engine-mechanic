---
status: accepted
engine_record: true
---

# Resolve: re-lock `agents` (the `engine-` naming rule; the read-only write-tool floor gated mechanically, with its honest limits) — a carrier of [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md)

*Decided 2026-07-16 in the design workspace.*

## The decision

Re-lock [agents](../spec/systems/surfaces/agents.md), a carrier of [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md), resolving **both** of its open ledger items in one lock per the batching law. **`grammar-core-U10`:** agent instance names take the **`engine-` prefix** — what [ontology](../spec/systems/grammar/ontology.md)'s identifier law already required (it is universally quantified over every surface instance carrying a human-facing identifier, and [D-020](0020-engine-instance-identifiers-are-engine-namespaced-decision-r.md) expressly forecloses the `.claude/`-is-an-engine-corner discharge); **no locked grammar is amended**, because only the agents doc was non-conformant. **`orphan-U01`:** the `permissions: read-only` leg is **gated mechanically at the native write-tool floor** — a merge-gating check asserts a read-only persona carries an explicit denial (or write-excluding allowlist) of Edit / Write / NotebookEdit, closing the **inherit-all trap** — stated with **two** honest limits: the check confirms the denial is *declared* and the **platform** is what honors it (enforcement is split across two parties and the check speaks for one), and the floor polices only the *native* write tools, leaving Bash and write-capable MCP calls to the runtime environment and the merge gate. `python3 lock.py --relock systems/surfaces/agents/README.md --decision D-313`; `validate.py` reports this fingerprint clean.

## Why

both items are adopt-the-letter or adopt-the-build-as-improvement, and neither invents grammar. The prefix is what the identifier law already requires; the build simply never conformed. The read-only floor is a real shipped mechanism the doc had left as a declared mapping, so recording it makes an undocumented build choice into canon — and recording its limits is what keeps "read-only" from being over-read as *cannot cause a write by any route*, which it does not mean. Folding `orphan-U01` here rather than deferring it honors the batching law and this item's own coordination note (*"if that ruling edits the doc, this rides the same amendment and re-lock"*); the round-1 audit caught the omission.

## What we ruled out

**Affirm agent path-confinement instead of prefixing** (rejected — [D-020](0020-engine-instance-identifiers-are-engine-namespaced-decision-r.md)'s rationale forecloses it verbatim, agent names are knowledge-graph entity ids and bare command-line tokens, and it would carve a surface exemption into a universally-quantified grammar law two decisions after its re-lock). **Amend ontology's identifier law** (rejected — the law already reaches agents; only the agent surface was non-conformant, so ontology carries no `grammar-core-U10` edit). **Defer `orphan-U01` to its own batch** (rejected — it forces a second agents re-lock, the exact waste the batching law exists to prevent, and its own ledger note planned to ride this amendment). **Claim the check proves read-only is enforced** (rejected — an over-claim of the pass's own signature class: the check evaluates the *declaration*, and the build's own code volunteers that limit; the doc must not assert more than the mechanism evaluates).

## Further record

### Propagation

Carried by [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md); no further propagation originates here. **Locked:** [agents](../spec/systems/surfaces/agents.md). **Ledger:** `grammar-core-U10` and `orphan-U01` both close under this entry. **Build-owes:** enumerated in [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md) (the 10 personas, `audit-prep.yml`, the test f-strings, three module manifests, `graph.json`; `surface-catalog.json`'s agent record — whose `engine-prefixed` field has no meta-contract home, filed as `grammar-core-U12`). **Id allocation:** **D-313** was forward-reserved by [D-309](0309-litigate-the-grammar-and-boot-cluster-ledger-grammar-core-u0.md) for exactly this re-lock; no competing reservation above it.
