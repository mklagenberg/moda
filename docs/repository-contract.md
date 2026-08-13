# Repository Contract

The repository contract exposes one system through three interfaces.

## Human interface

`README.md` explains identity, scope, exclusions, MODA adoption, navigation, and current version status. Getting Started provides the shortest successful adoption path. Best Practices covers judgment that is useful but not normative.

## Agent interface

`AGENTS.md` defines reading order, authority boundaries, stop conditions, change protocol, validation, and links to authoritative knowledge. It remains concise through progressive disclosure.

## Machine interface

`moda.yaml` declares identity, version, profile, provenance, documentation topology, components, packages, conformance mapping, and audit reference. Schemas and validators check deterministic properties.

## Evolution interface

The roadmap communicates direction. Issues or proposals track executable work. The changelog records what changed. Upgrade guidance records adopter actions for compatible releases. Migrations handle incompatible releases. Decision Records preserve why durable structural choices were made.

Operational and normative work uses a Change Set to preserve the problem, intended contract, alternatives, affected surfaces, SemVer effect, validation, migration, and recovery. Differential validation compares the impact declaration with the version-control diff. See [Specification-Driven Change Management](change-management.md).

Actively developed standalone artifacts keep `ROADMAP.md` at the root. It uses outcome-oriented horizons and does not create a delivery commitment unless a release plan or milestone explicitly says so.

## Composition interface

The manifest identifies canonical source, scaffold profiles, skills, adapters, distribution packages, and installations without treating them as the same lifecycle. See [Composition, Scaffolding, and Distribution](composition-scaffolding-and-distribution.md).

## Version-control interface

The Git workflow defines branch lifetime, pull-request evidence, protected integration, immutable tags, release gates, and recovery. Release provenance separates audited content from the evidence-only release commit. See [Git and Release Workflow](git-and-release-workflow.md).

The same fact should have one authoritative source. Other interfaces link to it.
