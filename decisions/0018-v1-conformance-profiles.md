# Decision 0018 — Limit MODA 1.0 conformance profiles to methodologies and standalone frameworks

- Status: accepted
- Date: 2026-08-12

## Context

Projects, products, prompts, skills, agents, workflows, and toolkits can be complex and can inherit MODA-informed practices, but treating each as a conformable methodology or framework would blur artifact identity and create misleading claims.

## Decision

MODA 1.0 defines direct conformance profiles only for end-to-end methodologies and independently maintained frameworks. Other artifact kinds are components, implementations, packages, or downstream consumers unless a later MODA version defines a dedicated profile with its own controls.

## Consequences

- Conformance claims remain bounded to subjects that satisfy the complete profile definition.
- Skills, prompts, tools, and projects can declare provenance without masquerading as methodologies.
- Adding a new conformable profile is a normative compatibility decision requiring specification, schema, validator, template, example, and migration review.
