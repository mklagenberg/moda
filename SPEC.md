# MODA Specification

Version: **1.0.0** — initial contract under development; no release tag exists yet.

This document is the normative specification of MODA — Methodology Organization, Design & Audit. Explanatory documents, examples, templates, and skills support this specification but do not override it.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate requirement strength.

## 1. Purpose

MODA provides a vendor-independent framework for designing, auditing, packaging, and evolving agentic methodologies and reusable methodology frameworks.

MODA separates:

- the framework that organizes design decisions;
- the methodology that organizes end-to-end execution;
- the implementation that executes the methodology in a particular environment;
- the operational adapters, prompts, skills, tools, and knowledge used by that implementation.

## 2. Supported artifact profiles

MODA 1.0 defines two conformable profiles:

### 2.1 `methodology`

An end-to-end system for achieving a bounded class of outcomes. A methodology selects and operationalizes frameworks, methods, processes, procedures, workflows, policies, and implementation assets.

### 2.2 `framework`

A reusable structure that organizes a design or decision space without prescribing one complete execution path. This profile applies to independently maintained frameworks. An embedded framework is declared as a component of its containing methodology and does not require a standalone repository contract.

Projects, products, prompts, skills, agents, workflows, and toolkits MUST NOT claim either profile unless they independently satisfy its definition.

## 3. Taxonomy

Every MODA artifact MUST identify one primary kind. Components MAY have other kinds.

| Kind | Normative meaning |
|---|---|
| `principle` | Direction used to judge choices |
| `model` | Representation used to explain a system or concept |
| `framework` | Adaptable structure for organizing decisions |
| `methodology` | Coherent end-to-end system for producing outcomes |
| `method` | Bounded technique for solving part of a problem |
| `process` | Ordered transformation from inputs to outputs |
| `procedure` | Operational instructions for performing an activity |
| `workflow` | Concrete executable flow of activities and decisions |
| `pipeline` | Chained workflow with explicit stage handoffs |
| `protocol` | Interaction rules and contracts between participants |
| `pattern` | Reusable solution with context and trade-offs |
| `playbook` | Scenario-oriented guidance and tactics |
| `specification` | Normative conformance contract |
| `template` | Preformatted artifact intended for adaptation |
| `prompt` | Instructions supplied to a model |
| `skill` | Operational capability package for an agent environment |
| `toolkit` | Reusable tools, templates, scripts, and supporting assets |
| `harness` | Runtime controls around models, tools, state, and policies |
| `agent` | Actor with bounded autonomy, tools, and responsibilities |
| `implementation` | Concrete realization of a methodology or framework |

A package MAY contain many kinds. Package contents do not change the primary identity of the package.

## 4. Design requirements

A conforming methodology MUST address every dimension in this section. A conforming framework MUST address dimensions applicable to its stated scope and declare non-applicable dimensions with rationale.

### 4.1 Problem and purpose

Declare the work being systematized, intended outcome, consumers, scope, exclusions, and success criteria.

### 4.2 Activation and proportionality

Declare when the artifact should and should not be used. Define how rigor, autonomy, evidence, cost, and review depth scale with complexity and risk.

### 4.3 Human reference practice

Describe how a competent human would perform the work before distributing it to agents. Identify judgments that remain human-accountable.

### 4.4 Inputs, outputs, and invariants

Define required inputs, expected outputs, unacceptable outcomes, assumptions, permissions, and non-negotiable constraints.

### 4.5 Decomposition and control flow

Identify fixed stages, adaptive discovery, parallel work, gates, loops, dependencies, handoffs, and stop conditions.

### 4.6 Distribution of agency

Classify consequential activities as deterministic, agent-reasoned, tool-executed, human-decided, or hybrid. Define authority boundaries and escalation conditions.

### 4.7 Orchestration

Select orchestration patterns based on work characteristics. Document why pipeline, supervisor-worker, fan-out/fan-in, debate, handoff, adaptive planning, or a hybrid is appropriate.

### 4.8 Contracts

Define stage inputs and outputs, required evidence, completion criteria, error states, return-of-control conditions, and prohibitions against silently filling critical gaps.

### 4.9 State, context, and knowledge

Separate transient context, execution checkpoints, durable methodology state, long-term knowledge, and installed operational guidance. Identify authoritative sources and retention rules.

### 4.10 Quality and evaluation

Define representative scenarios, expected properties, baselines, reviewers, adversarial checks, acceptance thresholds, confidence handling, and criteria for human intervention.

### 4.11 Safety, security, and privacy

Define data boundaries, permissions, secrets handling, destructive-action controls, external side effects, least privilege, auditability, and domain-specific review requirements.

### 4.12 Failure and recovery

Define behavior for insufficient evidence, contradiction, unavailable tools, incomplete agents, timeout, interruption, unsafe requests, failed validation, and incompatible state.

### 4.13 Portability

Keep core contracts independent of a model or vendor. Isolate product-specific behavior in declared adapters with their own compatibility and freshness metadata.

### 4.14 Packaging and synchronization

Identify specifications, prompts, skills, knowledge sources, schemas, scaffold engines and profiles, templates, scripts, examples, tests, adapters, distribution packages, and installations. Declare roles, versions, compatibility, source topology, and provenance. Define how drift is detected and resolved.

Repository boundaries MUST follow material differences in access, ownership, release cadence, technology, reuse, or independent consumption. Artifact kind alone is not sufficient reason for a separate repository.

When a methodology produces instances, it MUST define a scaffolding contract. Every scaffold profile MUST declare its intended instance type, inputs, outputs, conflicts, postconditions, and ownership class for generated files. Systematic post-instantiation deletion of inherited files is evidence that the profile is over-broad and SHOULD be redesigned.

When a methodology provides an agent skill, it MUST separate portable methodology semantics from host-specific adapters. It MUST declare installation paths, compatibility, update discovery, security advisory behavior, and distribution evidence for every supported host. The skill MUST participate in update detection on first activation per session or execution context, but MUST NOT be the only update channel or silently replace itself.

### 4.15 Evolution

Define versioning, changelog policy, roadmap governance, decision records, upgrade guidance, migrations, audit cadence, learning from execution, and criteria for adding or removing components.

An actively developed standalone methodology or framework MUST maintain a root `ROADMAP.md`. It MUST distinguish direction from delivery commitments and MUST NOT duplicate the detailed backlog or delivered changelog.

## 5. Repository contract

Every standalone conforming repository MUST provide:

- `README.md` as the human entry point;
- `AGENTS.md` as the canonical agent entry point;
- `moda.yaml` as the machine-readable identity and conformance declaration;
- `CHANGELOG.md` as the evolution record;
- `ROADMAP.md` as the direction record while the artifact is under active development;
- a normative specification, defaulting to `SPEC.md`;
- an onboarding path, defaulting to `GETTING-STARTED.md`;
- explicit invariants, either in `CONSTITUTION.md` or a mapped normative section;
- an upgrade path for backward-compatible adopter actions;
- migration guidance for incompatible releases;
- durable decision records for structural choices;
- a conformance mapping and latest audit reference.

Supporting capabilities MAY share a file when the repository is small, but `moda.yaml` MUST point to their authoritative location.

The literal `README.md`, `AGENTS.md`, `moda.yaml`, and `CHANGELOG.md` files are not replaceable by mappings to unrelated files. `ROADMAP.md` is literal for artifacts in `development` or `active` status. Decision Records MUST be stored in a dedicated mapped path and contain durable choices, not merely point to a generic narrative file.

### 5.1 Human disclosure

`README.md` MUST state that the artifact uses MODA, link to `https://github.com/mklagenberg/moda`, briefly explain MODA, name the artifact profile, declare the compatible MODA version, and link to the local manifest and conformance profile.

### 5.2 Agent disclosure

`AGENTS.md` MUST state that the artifact uses MODA, link to the official repository, direct agents to the manifest and conformance evidence, and prohibit unsupported conformance claims and silent structural migration.

### 5.3 Machine disclosure

`moda.yaml` MUST conform to the versioned MODA schema and declare artifact identity, relationship, adoption mode, documentation map, components, packages, conformance profile, and latest audit.

### 5.4 Progressive disclosure

Entry points MUST remain navigational. Detailed domain knowledge SHOULD live in linked authoritative files and SHOULD NOT be duplicated into `AGENTS.md`, README disclosures, prompts, or audit reports.

## 6. Adoption relationships

MODA distinguishes:

- `designed_with` — MODA informed original design;
- `conforms_to` — current structure claims conformance;
- `audited_against` — the artifact was assessed without a conformance claim;
- `inherited_via` — MODA appears only as upstream provenance through another methodology.

Adoption mode is `native` when MODA informed original design and `retrospective` when an existing artifact was mapped and normalized later.

Conformance is not transitive. A product using a MODA-conforming methodology does not automatically conform to MODA.

## 7. Conformance claims

Claim stages are distinct:

- `declared` — the owner states an intended relationship;
- `mapped` — requirements point to evidence and known gaps;
- `verified` — an identified auditor checked the mapped evidence;
- `certified` — an explicitly named external authority issued a certification.

MODA itself does not provide third-party certification in version 1.0.

Conformance results are:

- `conformant` — all applicable required controls pass;
- `partial` — mapping exists but one or more required controls do not pass;
- `nonconformant` — critical requirements are contradicted or absent;
- `unknown` — evidence or provenance is insufficient.

An audit MUST identify subject version and commit, MODA version and commit or tag, auditor identity and version, date, profile, findings, exceptions, and result.

## 8. Versions and provenance

Compatibility ranges express accepted MODA versions. Verification of a release MUST pin an exact released version and immutable source reference. A bootstrap or release-candidate assessment MAY pin an unreleased commit only when it is labeled as a candidate assessment and cannot yield a released or certified claim.

The methodology, skill core, knowledge snapshot, scaffold engine, scaffold profile, toolkit, adapter, distribution package, and installed copy MAY evolve independently. Each independently evolving package MUST declare its own version and source provenance. MODA recommends a shared release train until independent ownership or cadence is demonstrated.

For every package, source and installation are separate dimensions. A package source is local to the methodology repository or remote with repository, ref, and immutable commit. An installation records the package actually available in an execution environment. Historical generator provenance MUST NOT be used as a substitute for current installation state.

A distributed skill MUST declare its own version, methodology compatibility range, adapter target, canonical update manifest, security advisory channel, and first-activation check policy. When update status cannot be checked, the skill MUST report `unknown` or `offline`, never `current`.

Missing provenance produces `unknown` synchronization state. A tool MUST NOT silently assume that equal version strings imply equal content.

## 9. Semantic Versioning

MODA and MODA-conforming versioned artifacts SHOULD use full Semantic Versioning, including prerelease and build metadata when applicable:

- MAJOR when an existing conforming adopter requires migration;
- MINOR when a backward-compatible capability is added;
- PATCH when a fix or clarification adds no required behavior.

Every release MUST update its changelog. A release tag MUST NOT be created before the declared release gate passes.

## 10. Change and migration safety

Automated tools MUST NOT silently overwrite user-authored methodology content, accept risk, resolve substantive ambiguity, or apply incompatible migration. They MAY generate a plan, deterministic report, or proposed patch for human review.

## 11. Client-zero requirement

MODA MUST maintain a `framework` profile for itself. Every generally applicable requirement introduced by MODA MUST be implemented by this repository or marked non-applicable with evidence and rationale.

## 12. Precedence

Within a conforming artifact, precedence is:

1. applicable law and non-overridable safety constraints;
2. explicit human direction within authorized scope;
3. local invariants and approved extensions;
4. the artifact's normative specification;
5. MODA requirements for the declared version and profile;
6. toolkit, template, skill, and adapter defaults.

No lower layer may silently override a higher layer.
