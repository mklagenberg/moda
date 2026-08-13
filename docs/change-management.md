# Specification-Driven Change Management

MODA treats a repository change as a change to a system of contracts, not merely a collection of files. The normative specification remains authoritative; skills, manifests, schemas, validators, templates, examples, and documentation are synchronized projections of that contract.

## Change classes

| Class | Meaning | Change Set |
|---|---|---|
| `editorial` | Wording, formatting, or links with no semantic, operational, structural, security, or compatibility effect | Optional unless a protected contract surface changes |
| `operational` | Changes execution guidance, automation, validation, scaffolding, adapters, or packaging without changing normative obligations | Required |
| `normative` | Adds, removes, or changes an obligation, public contract, compatibility boundary, or conformance meaning | Required |

An apparently editorial change is operational or normative when it changes how a human or agent acts, how a machine validates, or what an adopter must implement.

## MODA Change Set

A required Change Set lives at `changes/<change-id>/` and contains:

- `proposal.md` — problem, proposed contract, alternatives, risks, acceptance criteria, migration, and recovery;
- `impact.yaml` — machine-readable classification, SemVer impact, triggers, affected surfaces, and validations.

The proposal captures reasoning for the current change. A durable architectural choice is also recorded under `decisions/`; a Change Set does not replace a Decision Record. Accepted Change Sets remain as traceability evidence. Rejected experiments may be removed when no release or durable decision references them.

## Impact statuses

Every required surface in `impact.yaml` is classified as:

- `updated` — one or more declared paths changed;
- `reviewed` — reviewed and intentionally unchanged, with rationale;
- `not-applicable` — outside the change scope, with rationale.

The declaration is not proof by itself. Differential validation compares it with the Git diff, and review evaluates whether the rationale is credible.

When a linear branch contains historical and current Change Sets, automatic discovery selects the Change Set whose declared base is the nearest available ancestor of `HEAD`. Earlier Change Sets retain their original validation evidence and are not reinterpreted as covering later work. Equal nearest bases are ambiguous and require explicit `--impact` selection or separate linear tranches.

## Change workflow

1. Classify the change before implementation.
2. Create a Change Set for operational or normative work.
3. State the intended contract and acceptance criteria in `proposal.md`.
4. Declare triggers, SemVer impact, affected surfaces, and expected validation in `impact.yaml`.
5. Change the authoritative source first: the specification for normative rules, or the owning operational artifact for operational behavior.
6. Synchronize affected projections without copying normative prose into every file.
7. Run repository, differential, reference, skill, example, and domain evaluations as declared.
8. Review the diff, unresolved gaps, migration and recovery needs, and conformance impact.
9. Merge only after required checks and human review pass.
10. Tag only through the release workflow.

## Trigger rules

The following triggers require explicit consideration:

| Trigger | Minimum surfaces to review |
|---|---|
| `normative_rule` | specification, skill, manifests, schemas, validators, templates, examples, changelog, upgrade, migrations, conformance |
| `public_path` | entrypoints, manifests, skill references, templates, examples, validators, conformance |
| `package_contract` | manifests, skill, schemas, templates, examples, changelog |
| `security_behavior` | specification, skill, manifests, validators, tests, changelog, upgrade |
| `release` | changelog, upgrade, migrations, conformance, audit evidence, release validation |

`reviewed` and `not-applicable` are valid only with a concrete rationale. A structural decision also requires a Decision Record.

## Deterministic and human checks

Automation SHOULD check:

- Change Set schema and required fields;
- changed protected surfaces represented as `updated`;
- declared updated paths present in the diff;
- trigger-specific surfaces explicitly considered;
- broken local paths and Markdown anchors;
- schema, manifest, audit, version, and provenance consistency.

Human review remains responsible for:

- whether the classification and SemVer impact are truthful;
- whether a rule change has been fully projected into operational guidance;
- whether reviewed or not-applicable rationales are credible;
- whether representative evaluations cover the behavioral change;
- whether migration, security, and release risks are acceptable.

## Completion rule

A change is incomplete when its implementation passes local tests but its declared contract surfaces, evidence, or migration obligations remain inconsistent. Passing validation is necessary evidence, not proof of semantic completeness.
