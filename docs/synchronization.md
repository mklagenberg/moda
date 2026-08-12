# Synchronization and Provenance

Methodology, framework, skill, toolkit, knowledge, scaffold, adapter, and installed copies may evolve independently. Equal version strings do not prove equal content.

## Required anchors

Each independently evolving package declares:

- name and semantic version;
- canonical source repository;
- immutable source tag or commit used;
- compatible upstream version range;
- relevant knowledge snapshot or content commit;
- last verified date and audit state.

## Drift states

- `current` — compatible versions and expected immutable references match;
- `review-required` — upstream changed within the compatible range;
- `incompatible` — the installed or referenced package falls outside compatibility;
- `broken` — a required source, path, schema, or provenance anchor cannot be resolved;
- `unknown` — evidence is insufficient to choose another state.

## Update rule

An update compares changes, classifies compatibility, updates affected packages, runs validation, records adopter actions, and obtains human approval. No package silently rewrites another package's authored content.
