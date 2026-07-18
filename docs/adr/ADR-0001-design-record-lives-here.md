---
id: ADR-0001
title: The design record lives here — spec plus decision records, laws not leaves
status: accepted
date: 2026-07-17
replaces: []
---

## Decision

The product design authority for engine-template, as built from this repository, is `docs/spec/`
(the distilled capability spec) together with `docs/adr/` (this curated decision-record set). The
engine-planning workspace that previously held the design is retired: its 319-entry decision log
(D-001–D-319) is carried here in curated form — every old decision has exactly one disposition in
the index — and its prose corpus is distilled into the spec at law level. Deliberately, no verbatim
copy of the retired corpus is kept anywhere in this repository. The sole recoverable snapshot lives
outside any repository as a tarball: SHA-256
`9a366c13619f850dce7bda6d95b399743102f896de7a10a4595a8da2bc29b03b`, 1,141,303 bytes, 138 entries
(`engine-planning-final-snapshot-2026-07-17.tar.gz`). Opening it is a deliberate act, never ambient
context.

## Rationale

The retired corpus grew as complicated as the code it designed — a prose copy of the build — because
the laws-not-leaves discipline was practiced but never encoded. An in-repo archive would keep that
corpus ambient: future sessions would ground in it, imitate its granularity, and re-import the
disease. Distilled laws with pointer-only traceability keep the record small, auditable, and
authoritative.

## Anti-choice

A verbatim in-repo archive (`docs/archive/`) was rejected: recoverability convenience does not
outweigh the standing pull toward prose-copy bloat. A 1:1 conversion of all 319 decisions was
rejected for the same reason — superseded chains and construction-era process decisions do not
govern the product and would bury the ~60 that do.
