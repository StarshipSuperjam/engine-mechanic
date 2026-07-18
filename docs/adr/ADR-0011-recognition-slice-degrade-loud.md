---
id: ADR-0011
title: Boot reads the recognition slice, sheds loudly, and retires its weakening alarm
status: accepted
date: 2026-07-17
replaces: [D-309]
---

## Decision
Boot's cold-start pack reads the surface catalog's recognition slice — every surface definition, recognition fields only (name and home) — re-rendered at every session start, while the governance fields stay the pull-request author's business, never the cold session's. The read is posture, hook-dependent and fail-open: it makes an invented file-kind unlikely, never impossible — the merge coverage gate stops a drifted surface directory at directory granularity, an uncatalogued instance inside an existing bucket is caught by neither, and this narrows the two absolutes in the ontology decision record (eADR-0016: "read whole at boot"; "an uncatalogued surface is not recognized") to their honest form. Boot's never-produced guardrail-weakening alarm class is retired: that surfacing belongs at the merge, where the control plane owns detection and discharges the relay, and boot's sole-write claim reconciles by attributing each write to its owning substrate. Because the platform caps what one hook may emit and silently truncates past the cap — which would forge a false grounding signal — the assembled pack measures itself last and, when over budget, sheds its lowest-priority category loudly: the shed notice joins the must-push operator relay, the recognition slice sheds first because recognition is posture, and attention ranks candidate content without ever seeing the slice, which sits outside its candidate partition by construction, not by exemption. Agent-surface identifiers take the engine prefix as an application of the standing engine-namespacing law, not a new rule.

## Rationale
The recognition fields are all a cold session needs to recognize a file-kind; the governance fields are context noise for it and are weighed where they matter, at the pull request. Naming the tier honestly matters more than claiming strength: a canon-wide truth sweep found the engine's over-claims were always documents claiming more than the mechanism delivered, never mechanisms missing — so the honest fix is narrowing the words. A silently truncated pack is worse than a smaller one, because truncation forges evidence that the session grounded when it did not.

## Anti-choice
A dedup mechanism for the re-rendered slice was rejected: the payload is too small to earn a mechanism, and the obvious session-keyed design is unimplementable because session identity is reissued on resume. Keeping the weakening-alarm class as aspirational canon was rejected — a documented mechanism that does not exist is precisely the over-claim failure. Letting attention rank the slice was rejected: an input to the pack is outside the candidate partition by construction.
