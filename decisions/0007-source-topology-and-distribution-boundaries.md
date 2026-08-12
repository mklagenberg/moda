# 0007 — Separate source topology from distribution boundaries

**Status:** Accepted

## Context

Methodologies may contain a specification, skill, adapters, scaffolds, schemas, scripts, and examples. Treating each artifact kind as a reason for a separate repository creates drift, while treating every runtime installation as repository content confuses source with deployed state.

## Decision

MODA distinguishes methodology source, distribution packages, generated instances, and installations. Components remain in one source repository by default when they share ownership, permission, release cadence, and compatibility. A separate repository requires an explicit independent boundary.

Plugin and marketplace packaging does not require the canonical skill source to leave the methodology repository.

## Consequences

- Monorepo is the default for a methodology and its tightly coupled operational assets.
- Polyrepo composition remains supported with explicit remote provenance.
- Distribution artifacts are built from an immutable audited source commit.
- Installed state is recorded separately from source and project state.
