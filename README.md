# MODA

**Methodology Organization, Design & Audit**

MODA is an open framework for designing, auditing, packaging, and evolving agentic methodologies that are explicit, traceable, portable, and operable by both humans and AI agents.

## What MODA provides

- a shared taxonomy for frameworks, methodologies, methods, processes, procedures, workflows, prompts, skills, and supporting artifacts;
- a design model for turning competent human work into governed agentic execution;
- a repository contract with separate entry points for humans, agents, and machines;
- conformance profiles and evidence-based audits for existing or new methodologies;
- versioning, provenance, synchronization, upgrade, and recovery requirements;
- model- and vendor-independent packaging guidance.

## What MODA is not

- an agent runtime or orchestration library;
- a universal workflow that every methodology must execute unchanged;
- a substitute for domain expertise, evaluation, security review, or human accountability;
- a certification body or formal industry standard.

## MODA client zero

<!-- moda:disclosure:start -->
This repository is structured and audited with [MODA](https://github.com/mklagenberg/moda). MODA defines an open framework for organizing, designing, auditing, packaging, and evolving agentic methodologies.

- Artifact profile: `framework`
- MODA compatibility: `^1.0.0`
- Manifest: [`moda.yaml`](moda.yaml)
- Conformance profile: [`conformance/moda.yaml`](conformance/moda.yaml)
<!-- moda:disclosure:end -->

MODA is its own first conforming artifact. Its repository structure, specification, audit model, skill synchronization, and release process must satisfy the same requirements it defines for adopters.

## Start here

1. Read [Getting Started](GETTING-STARTED.md) for the shortest path to a useful result.
2. Read the [Constitution](CONSTITUTION.md) for non-negotiable principles.
3. Read the [Specification](SPEC.md) for the normative framework contract.
4. Read [Best Practices](BEST-PRACTICES.md) for application guidance.
5. Read the [Disclaimer](DISCLAIMER.md) before using MODA in high-impact contexts.

Agents must start with [AGENTS.md](AGENTS.md).

## Repository map

- `SPEC.md` — normative MODA contract.
- `moda.yaml` — machine-readable identity and self-conformance declaration.
- `docs/` — explanatory models, taxonomy, lifecycle, governance, and synchronization.
- `conformance/` — current conformance mapping.
- `audits/` — immutable audit evidence.
- `schemas/` — machine-readable schemas.
- `templates/` — reusable adoption artifacts.
- `examples/` — small conforming examples.
- `skill/` — operational adapter for AI agents.
- `scripts/` — deterministic validators.
- `decisions/` — durable design decisions about MODA itself.

## Version status

MODA is being built directly toward **v1.0.0**. The version is declared in repository artifacts, but no release tag is created until the release gate passes.

MODA follows Semantic Versioning:

- **MAJOR** — an existing conforming artifact becomes incompatible without migration;
- **MINOR** — a backward-compatible capability is added;
- **PATCH** — a fix or clarification changes no required behavior.

## License

Licensed under the [Apache License 2.0](LICENSE).
