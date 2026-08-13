# Decision 0002 — MODA as client zero

Status: Accepted

## Context

A framework that defines repository and conformance requirements can drift into rules that its own maintainers never exercise.

## Decision

MODA is the first artifact to adopt and audit MODA. Every generally applicable framework-profile requirement must be implemented here or marked non-applicable with evidence and rationale.

## Rationale

Dogfooding exposes ambiguity, excess documentation, circular provenance, synchronization gaps, and validator defects before adopters inherit them.

## Consequence

The repository carries its own manifest, conformance map, audit history, disclosures, validators, skill, templates, and upgrade path.
