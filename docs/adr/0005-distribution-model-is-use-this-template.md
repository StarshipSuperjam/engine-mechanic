---
status: accepted
engine_record: true
---

# Distribution model is "Use this template"

*Decided 2026-05-22 in the design workspace.*

## The decision

Design for consumption via GitHub "Use this template" (copies the file tree as one commit), not `git clone`. Anything that can be a committed file should be.

## Why

The template feature copies files but not settings; maximizing committed files maximizes what travels, diffs, and is reviewable. Gitignored data correctly does not travel; only true settings need a bootstrap.

## What we ruled out

Assume a `git clone` + manual setup model — rejected because it misframes what ships and underweights how much can travel as files.
