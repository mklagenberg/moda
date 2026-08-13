# 0009 — Keep a portable skill core and require update awareness

**Status:** Accepted

## Context

Methodology skills must work across agent hosts, may receive patches without normative methodology changes, and can become vulnerable or incompatible after installation. A dormant skill cannot be the only update notification channel, but it can verify freshness when invoked.

## Decision

Keep methodology semantics in a portable skill core and isolate host differences in thin adapters and distribution packages. Use one release train until independent component lifecycles are demonstrated, while declaring explicit compatibility ranges.

On first activation per session or execution context, a distributed skill checks or reuses a valid assessment of releases and security advisories. It reports uncertainty when the check is unavailable, never silently self-modifies, and restricts affected capabilities for known high-impact vulnerabilities.

## Consequences

- ChatGPT, Claude, and other packages derive from the same audited core.
- Skill-only fixes may be released as bundle patches.
- Marketplaces, workspace administrators, and security advisories remain independent notification channels.
- Installation state and historical generator provenance are no longer conflated.
