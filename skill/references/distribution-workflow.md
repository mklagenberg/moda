# Distribution and Update Workflow

Use this workflow when designing or auditing skills, adapters, scaffold packages, plugins, marketplaces, or runtime update behavior.

1. Identify the portable skill semantics and keep them independent of host tool names.
2. Identify each supported host and declare a thin adapter for manifests, tools, authentication, limitations, install, and update actions.
3. Pin every published package to the audited source repository, path, version, and commit.
4. Separate the skill version that generated an instance from the skill currently installed in an environment.
5. Require a first-activation version and security assessment per session or execution context.
6. Reuse only an assessment whose normal and security TTLs remain valid.
7. Return `unknown` or `offline` when the canonical update source cannot be checked.
8. For normal compatible updates, notify once and continue. For incompatible versions, stop affected operations and present migration guidance.
9. For a known high-impact advisory, restrict affected capabilities while keeping safe update-help behavior available.
10. Never silently self-update or overwrite generated user-owned content.
11. Verify that marketplace or registry packages correspond to the audited source commit.
