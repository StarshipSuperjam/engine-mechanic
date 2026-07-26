---
status: accepted
engine_record: true
---

# The control-plane bootstrap must travel and fail loud

*Decided 2026-05-22 in the design workspace.*

## The decision

Ship the branch-protection bootstrap as a committed artifact (a first-run workflow or a single documented command) that fails loudly and visibly until protection is applied; resolve the admin-token permission wrinkle explicitly.

## Why

Branch protection is the gate every other guardrail depends on; a non-engineer will skip a setup step they were merely told about. The fix can itself be a traveling file.

## What we ruled out

Document the `gh api` command and rely on the operator to run it — rejected because silent omission leaves the protected branch unprotected.
