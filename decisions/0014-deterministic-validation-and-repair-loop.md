# Decision 0014 — Prefer deterministic validation and require a repair loop

- Status: accepted
- Date: 2026-08-12

## Context

Agents are useful for interpreting intent and proposing corrections, but they are unreliable substitutes for repeatable checks of schemas, paths, versions, provenance, counts, release gates, and other mechanically decidable properties. A one-shot validation run also leaves work incomplete when correctable failures are merely reported.

## Decision

Implement deterministic validation as scripts whenever a property can be checked reproducibly at reasonable cost. Scripts emit stable human-readable output and SHOULD also support machine-readable findings.

After a validation failure, the operating agent interprets the findings, identifies the authoritative source, applies an authorized bounded correction, and reruns the same validation plus affected regression checks. The loop stops on success, lack of progress, insufficient authority or evidence, unsafe/destructive action, incompatible migration, or a required human decision.

## Consequences

- Repeatable checks do not depend on model judgment.
- Agent reasoning is focused on diagnosis and correction rather than pretending to be a parser or schema engine.
- A reported failure is not treated as task completion when a safe in-scope fix is available.
- Infinite repair loops are prohibited; blockers and unchanged failures are returned explicitly.
