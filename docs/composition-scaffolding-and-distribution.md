# Composition, Scaffolding, and Distribution

MODA distinguishes source organization from runtime distribution. A repository boundary is justified by a real boundary in access, ownership, release cadence, technology, reuse, or independent consumption. Multi-repository architecture is not a quality by itself.

## Source topology

Use a methodology monorepo when the normative specification, skill core, validators, scaffold profiles, and adapters must change atomically and share ownership and release cadence. Use multiple source repositories only when at least one component has an independently meaningful lifecycle or boundary.

A separate toolkit repository SHOULD NOT exist only because templates and scripts are different artifact kinds. If it always changes with the methodology, has the same maintainers and permissions, and has no independent consumers, it normally belongs in the methodology repository.

## Four distinct layers

| Layer | Purpose |
|---|---|
| Methodology source | Normative specification and canonical implementation sources |
| Distribution package | Host-specific artifact published to a plugin directory, marketplace, registry, or download channel |
| Generated instance | Repository or workspace produced from a declared scaffold profile |
| Installation | Skill, plugin, adapter, or tool actually available in a person's or organization's environment |

These layers MAY share a repository, but they MUST keep separate identity and provenance.

## Scaffolding contract

A scaffolder generates the smallest valid initial instance. It MUST declare:

- engine version and source commit;
- selected profile and profile version;
- target methodology version or compatible range;
- required parameters and defaults;
- files it creates, skips, or treats as conflicts;
- which generated files become user-owned after creation;
- upgrade and migration behavior;
- deterministic validation and postconditions.

Profiles represent legitimate instance variants such as a minimal project, existing project, personal knowledge base, restricted vault, library, or extended product. Profiles MUST NOT be implemented as unrelated templates whose shared contract can drift silently.

If post-instantiation instructions routinely require deleting inherited files, replacing an unrelated license, or removing an inert skill copy, the scaffold contains responsibilities that do not belong to the instance and SHOULD be redesigned.

Scaffolding establishes structure; it does not prove conformance. The generated instance starts at `declared` or `unknown` until its local decisions and evidence are assessed.

## Generated, canonical, and authored files

Every scaffold output MUST classify files as:

- `canonical-reference` — read from the methodology package and not copied into the instance unless execution requires it;
- `generated-once` — generated during initialization and never silently overwritten;
- `managed-structure` — deterministically upgradeable when the instance explicitly accepts an update;
- `user-authored` — never overwritten by scaffold or upgrade automation.

## Skill core and adapters

The skill core expresses methodology semantics: routing, workflows, gates, invariants, evidence, stop conditions, and escalation. A host adapter expresses only integration differences such as manifests, installation, tool names, capability detection, authentication, and host limitations.

An adapter MUST NOT change the methodology's normative meaning. Materially different behavior is a fork or a distinct implementation and MUST be declared as such.

The canonical skill source SHOULD live with the methodology when they share ownership and release cadence. Publishing it through a plugin or marketplace creates a distribution artifact, not a requirement for another source repository.

## Release train and compatibility

MODA recommends one release train until components demonstrate independent lifecycles. A patch may change only a skill or adapter while the methodology contract remains unchanged. Release notes MUST identify affected components.

The skill MUST declare the methodology versions it implements. The generated instance MUST record the skill version that generated it separately from the range required for future operation. The currently installed skill version belongs to installation state, not to immutable project history.

## Runtime update awareness

A distributed skill MUST participate in detecting its own obsolescence without being the only notification channel.

On the first activation in each session or execution context, the skill MUST obtain or reuse a still-valid update assessment. It MUST compare:

- installed skill and adapter versions;
- supported methodology range;
- canonical release manifest;
- minimum secure version and applicable advisories.

Required states are `current`, `update-available`, `security-update-required`, `incompatible`, `unknown`, and `offline`.

Normal patches MAY produce a non-blocking notice. Incompatibility MUST stop affected operations and provide migration guidance. A known high-impact security issue MUST restrict the affected capability, not necessarily all read-only or update-help behavior. Failed lookup MUST NOT be reported as current.

The skill MUST NOT silently replace itself. Marketplaces, workspace administration, release notifications, and security advisories remain independent update channels.

## Distribution evidence

Each published package MUST identify:

- package name, version, channel, and target host;
- source repository, source path, and immutable source commit;
- skill core and methodology compatibility;
- adapter version;
- checksum or platform-native immutable identity when available;
- installation and update instructions;
- release notes and security advisory location;
- validation evidence proving that the package corresponds to the audited source.
