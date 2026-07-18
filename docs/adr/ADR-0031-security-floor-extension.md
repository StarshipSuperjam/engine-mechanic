---
id: ADR-0031
title: Security floor extends to code scanning and vulnerability disclosure
status: accepted
date: 2026-07-17
replaces: [D-211]
---

## Decision
The security floor extends from secrets and dependencies to code scanning and vulnerability disclosure
along its locked grain: native where the repository's tier supports it, disclosed — never silently
dropped — where it does not, and never a bespoke layer. Native code scanning is enabled where supported;
where unsupported the enable is detected, skipped, and the drawback disclosed in terms the operator can
evaluate — visibility is never auto-switched to unlock a feature — and scanning alerts are advisory,
never a merge gate, so a finding cannot strand the non-engineer at a blocked merge. Disclosure is a
seeded, operator-owned vulnerability-disclosure file at the repository root — product territory,
seed-then-preserve — plus the platform's native private-reporting channel where it exists, with the
consequence of enabling it disclosed (outsiders can privately file reports). Repository-altering toggles
and seeds are disclosed at first run in plain language, and the floor folds under the existing quality
attributes — no new security attribute is minted.

## Rationale
The existing floor's grain — native-where-supported, disclose-never-downgrade — already carries the trust
story, so the extension follows it rather than inventing a parallel one. Advisory-not-gating keeps hard
gates reserved for governance-critical invariants, and a disclosure channel matters most exactly where
native reporting cannot exist, which is why the seeded file travels to every repository.

## Anti-choice
Rejected: a required merge-blocking third-party static-analysis check over product code (wrong altitude —
standing product-code analysis is an opt-in capability, and it strands the operator at a greyed merge
button); any bespoke fallback scanner; a committed scanning workflow where the native default setup
suffices; and homing the disclosure file in the engine's namespace instead of the product root.
