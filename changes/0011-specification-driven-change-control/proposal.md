# Add specification-driven change control

## Problem

MODA validates repository state but does not reliably detect semantic drift between a changed rule and its derived operational artifacts. Public readers also cannot depend on the private conversation that motivated a rule.

## Current contract

`AGENTS.md` asks contributors to assess schemas, templates, examples, validators, skill guidance, and conformance fixtures. The requirement is prose-only and no differential validator compares that assessment with a pull-request diff.

## Proposed contract

Add MODA Change Sets for operational and normative changes, a machine-readable impact schema, differential validation, Git and release guidance, skill routing, and a two-commit release-evidence model.

## Alternatives

- Require a traditional software design document for every change: rejected because MODA also governs non-software methodologies and small changes should remain proportional.
- Depend only on pull-request checklists: rejected because checklist assertions cannot be validated against changed paths.
- Infer all semantic impact from the diff: rejected because automation cannot reliably determine intent, compatibility, or whether an unchanged surface was deliberately reviewed.

## Risks

- Excess process for small changes: mitigated by exempting genuinely editorial work outside protected contract surfaces.
- False confidence in automation: mitigated by treating differential validation as evidence and retaining human review for semantics.
- Stale Change Sets: mitigated by validating updated paths and trigger-specific surface declarations against the diff.

## Acceptance criteria

- [x] Normative change requirements and proportional classes are documented.
- [x] The current change declares its own impact as client zero.
- [x] Git branches, pull requests, immutable tags, release gates, and recovery are documented.
- [x] A schema and validator reject incomplete or contradicted impact declarations.
- [x] CI runs repository, example, unit, and differential validation.
- [x] The MODA skill routes methodology evolution work through the change workflow.

## Compatibility and migration

This adds a backward-compatible MODA capability before the first release and is classified as a prospective MINOR feature. Existing unreleased fixtures are updated in place; no released adopter migration exists yet.

## Recovery

Revert the coherent change-control commit before release. After release, supersede the decision and provide the corresponding compatibility and migration guidance rather than silently removing traceability requirements.
