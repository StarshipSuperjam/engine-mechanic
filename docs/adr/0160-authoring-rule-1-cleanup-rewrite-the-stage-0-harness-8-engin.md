---
status: accepted
engine_record: true
---

# Authoring-rule-1 cleanup: rewrite the `stage-0-harness` §8 engine-mechanic note to finished current-state

*Decided 2026-05-31 in the design workspace.*

## The decision

Rewrote wbs/stage-0-harness.md §8 (the out-of-scope engine-mechanic note) to remove **authoring-rule-1** change-history phrasing — "the trusting-trust and reflexive-upgrade problems *this doc previously flagged*" and "The *former residual* … is *resolved*" — and state the current truth directly: running only a released, ratified engine to build the next means the trusting-trust / reflexive-upgrade hazards of a self-modifying builder **do not arise**, and the construction hand-off point **is M1** ([D-107](0107-author-the-wbs-module-build-order-the-builder-crossover-reso.md)). Substance unchanged (version-separation safety; the M1 hand-off; this doc carries the template to the threshold, the module build-order past it). A **deletion-mandate / authoring-hygiene** fix in a non-locked doc (`wbs/` is freely revisable, no lock fingerprint), so a normal in-place edit — **not** a litigation. Surfaced as a pre-existing, out-of-scope finding during the [D-156](0156-name-the-engine-s-execution-substrate-a-group-scoped-uv-mana.md)→[D-159](0159-re-affirm-engine-template-v1-build-ready-lift-the-d-156-d-15.md) tool-runtime work (two independent audit lenses) and explicitly deferred by [D-158](0158-refine-d-156-s-tool-runtime-keying-pin-the-module-dependency.md)'s anti-choices to this separate cleanup. `python3 validate.py` green (anti-changelog lint clean).

## Why

Authoring rule 1 requires every document read as authored-complete-today; "previously flagged" / "former residual" / "resolved" are diffs against a past state the deletion mandate forbids. The fix preserves every fact while deleting the change-history framing, exactly as the mandate directs.

## What we ruled out

**Bundle it into the [D-158](0158-refine-d-156-s-tool-runtime-keying-pin-the-module-dependency.md) tool-runtime pass** (rejected at D-158 — unrelated to the runtime; bundling unrelated concerns is the discipline this workspace avoids). **Leave it unlogged as too trivial** (rejected — no silent changes; even a cosmetic doc edit gets a log line per the change-propagation matrix).
