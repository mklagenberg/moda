# 0008 — Generate instances through explicit scaffold profiles

**Status:** Accepted

## Context

Repository templates often copy a superset and rely on a post-instantiation checklist to remove irrelevant files, replace licenses, delete examples, and discard inert skill copies. This produces ambiguous ownership and drift.

## Decision

MODA models scaffolding as a versioned engine with explicit profiles. A profile generates only the files required by the selected instance type and classifies every output as canonical reference, generated once, managed structure, or user-authored.

Scaffold completion does not establish conformance. Upgrade automation never silently overwrites user-authored files.

## Consequences

- Multiple legitimate project shapes share one tested scaffold contract.
- Post-generation deletion is treated as a design defect when systematic.
- Instances preserve generator, profile, methodology, and source provenance.
- Existing repositories can use an adoption profile without destructive re-scaffolding.
