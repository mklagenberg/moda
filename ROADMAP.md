# Roadmap

Last reviewed: **2026-08-12**

This roadmap communicates direction, not a promise of dates. Only an approved release plan or milestone creates a release commitment. Detailed work belongs in tracked issues or proposals; completed work belongs in `CHANGELOG.md`.

## Now

### Portable skill distribution packages

**Outcome:** A methodology author can publish one portable skill core through tested packages for ChatGPT, Claude, and other compatible agent environments without forking the methodology semantics.

**Status:** validating

The work includes:

- a portable Agent Skills-compatible core;
- thin host adapters and native package manifests;
- packaging and provenance from one audited source commit;
- install and update instructions per supported host;
- a first-activation version and security check;
- normal, incompatible, offline, and security-update behavior;
- release and marketplace evidence without making the skill its only obsolescence detector.

The initial release remains blocked until this contract, its fixtures, and its client-zero evidence are complete.

## Next

### Composition and scaffolding profiles

**Outcome:** MODA can represent monorepo and polyrepo methodologies, generated instances, independently installed packages, and multiple scaffold profiles without confusing source, distribution, installation, or user-authored state.

**Status:** specified; implementation pending

### Conformance integrity

**Outcome:** Deterministic validation rejects missing literal repository artifacts, broken evidence anchors, invalid control states, inconsistent audit counts, unresolved placeholder commits, and incomplete package provenance.

**Status:** implemented; immutable release audit pending

The implementation now includes specification-driven Change Sets and differential impact validation; the final release audit remains pending.

## Later

### Community conformance exchange

**Outcome:** Public methodologies can publish portable conformance evidence and audit results without implying certification by MODA.

**Status:** hypothesis

## Not planned

- Hosting or executing methodology instances.
- Replacing vendor marketplaces or package managers.
- Silently updating installed skills or generated user content.
- Treating a generated instance as conformant solely because scaffolding completed.
