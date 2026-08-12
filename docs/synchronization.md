# Synchronization and Provenance

Methodology, framework, skill core, toolkit, knowledge, scaffold engine, scaffold profile, adapter, distribution package, and installed copies may evolve independently. Equal version strings do not prove equal content.

Source, package, generated history, and installation are different states. A project can record which scaffold generated it without claiming that the same skill is still installed.

## Required anchors

Each independently evolving package declares:

- name and semantic version;
- canonical source repository;
- immutable source tag or commit used;
- compatible upstream version range;
- relevant knowledge snapshot or content commit;
- last verified date and audit state.

Remote sources also declare repository, ref or release, and immutable commit. Installations declare environment, installed package identity, adapter, and installed version. One release train is preferred until independent lifecycles are demonstrated.

## Drift states

- `current` — compatible versions and expected immutable references match;
- `review-required` — upstream changed within the compatible range;
- `incompatible` — the installed or referenced package falls outside compatibility;
- `broken` — a required source, path, schema, or provenance anchor cannot be resolved;
- `unknown` — evidence is insufficient to choose another state.

## Update rule

An update compares changes, classifies compatibility, updates affected packages, runs validation, records adopter actions, and obtains human approval. No package silently rewrites another package's authored content.

## Runtime skill check

On first activation per session or execution context, a distributed skill checks or reuses an unexpired assessment of its version, compatibility, and security state. Required results are `current`, `update-available`, `security-update-required`, `incompatible`, `unknown`, and `offline`.

The check complements host marketplaces, workspace administration, release notifications, and security advisories. It does not authorize silent self-update. A known high-impact advisory restricts the affected capability while retaining safe update-help behavior.
