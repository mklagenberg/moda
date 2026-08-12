# Decision 0004 — Versioning and initial release

Status: Accepted

## Context

The project needs a stable compatibility model while its first public contract is assembled through several reviewable changes.

## Decision

Target version `1.0.0` directly. Build the initial contract through coherent commits and do not create intermediate release tags. Create `v1.0.0` only after the release gate passes and human approval is explicit.

Use Semantic Versioning after the initial release:

- MAJOR for incompatible changes requiring migration;
- MINOR for backward-compatible capabilities;
- PATCH for fixes and clarifications that add no required behavior.

## Rationale

Intermediate tags would falsely imply releasable contracts while schemas, skill, validators, examples, and audits are still being synchronized.
