# Deterministic Validation and Repair

Use deterministic scripts whenever a property can be checked reproducibly at reasonable cost. Agent judgment remains appropriate for intent, trade-offs, semantic completeness, non-applicability, and corrections that cannot be reduced to stable rules.

## What to automate

Prefer scripts for:

- schema, manifest, and structured-data validation;
- required files, local paths, links, and Markdown anchors;
- versions, compatibility ranges, tags, commits, provenance, and checksums;
- finding counts, enums, state transitions, package identity, and release gates;
- generated-file consistency and declared Change Set impact;
- repeatable examples, regression tests, and security policy checks.

Scripts SHOULD return a non-zero exit code on failure, stable finding codes, affected paths, actionable messages, and machine-readable output when downstream automation benefits from it.

## Repair loop

1. Run the narrowest authoritative validation that can decide the property.
2. Preserve and read the complete findings; do not summarize away codes or paths needed for diagnosis.
3. Identify the authoritative source and the smallest coherent correction.
4. Confirm the correction is within current authority and does not require hidden risk acceptance, destructive action, incompatible migration, or external side effects.
5. Apply the correction.
6. Rerun the failed validation.
7. Run affected regression checks and the repository completion gate.
8. Repeat only while evidence changes and progress is being made.

Stop and return control when:

- the same finding persists without a new evidence-based correction;
- required input, provenance, dependency, permission, or tool access is unavailable;
- alternatives materially change intent or compatibility;
- the next action is destructive, unsafe, externally consequential, or outside authorization;
- a human decision, domain review, or risk acceptance is required.

Never edit expected results merely to make a failing implementation pass. Never skip or weaken a validator without a Change Set that changes the governing contract. Report the final command, result, corrected files, remaining findings, and blocker when the loop stops before success.
