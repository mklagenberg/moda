# Best Practices

## Prefer semantic clarity over directory theater

Declare the artifact map even when several components share one file. Create separate files or packages only when they improve reuse, ownership, versioning, evaluation, or maintenance.

## Keep identity, conformance, and audit separate

The manifest declares what the artifact is. The conformance profile maps requirements to evidence. An audit records what an identified auditor verified at an immutable point in time. None substitutes for the others.

## Point to evidence instead of copying it

Conformance files and audit reports should reference normative sources. Duplicated rules drift and make it unclear which copy is authoritative.

## Start partial and honest

Retrospective adopters should record real gaps instead of reshaping terminology to manufacture conformance. A useful partial profile is better than an unsupported conformant claim.

## Separate stable core from volatile adapters

Keep durable methodology contracts apart from model-, vendor-, product-, or market-specific guidance. Give volatile adapters shorter review intervals and explicit compatibility metadata.

## Improve the harness after repeated failure

When an agent repeatedly fails, improve context routing, repository guidance, contracts, validators, examples, or skill instructions. Repeating a longer prompt is not a durable correction.

## Use the smallest adequate artifact

Do not create a Decision Record, framework, agent, or separate repository when a section, method, deterministic script, or documented choice is sufficient.

## Treat release as a gate

A version string describes intended compatibility. A release claims that documentation, schemas, examples, skills, validation, and migration guidance are synchronized. Tag only after that claim is true.
