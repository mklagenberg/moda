# Decision 0011 — Govern substantive changes through MODA Change Sets

- Status: accepted
- Date: 2026-08-12

## Context

Repository validation can prove that files are individually well formed while missing semantic drift between them. A normative rule may change in the specification while the skill, manifest, templates, examples, or migration guidance remain stale. Conversation history is not a durable public source of intent.

## Decision

Adopt specification-driven change management. Operational and normative work uses a `changes/<change-id>/` Change Set containing a human proposal and machine-readable impact declaration. Differential validation compares the declaration with the Git diff and requires explicit review of trigger-dependent contract surfaces.

Editorial work remains lightweight unless it touches a protected contract surface or changes behavior. Change Sets preserve change-specific reasoning; Decision Records continue to preserve durable architectural choices.

## Consequences

- Substantive changes expose intended behavior, SemVer impact, synchronization obligations, validation, migration, and recovery before release.
- A changed rule can no longer be considered complete solely because repository-level validation passes.
- Reviewers can distinguish `updated`, `reviewed`, and `not-applicable` surfaces and challenge weak rationales.
- Small editorial changes avoid unnecessary ceremony.
- The repository retains additional traceability artifacts for meaningful changes.
