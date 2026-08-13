# Decision Record Policy and Coverage

Decision Records preserve durable choices whose rationale would otherwise be lost. They are not a diary of every edit and do not replace specifications, Change Sets, changelogs, or roadmaps.

## Create a Decision Record when

At least one of these conditions applies:

- the choice is costly to reverse or constrains future architecture;
- it changes a public contract, compatibility boundary, authority model, security posture, repository topology, release model, or evidence model;
- multiple reasonable alternatives have materially different trade-offs;
- the same question is likely to recur without a durable explanation;
- the decision affects several contract surfaces or independent consumers;
- a structural Change Set declares `structural: true`.

## Do not create one for

- routine fixes that follow an existing decision;
- transient implementation details with a safe and local replacement path;
- generated evidence, current test output, or one execution result;
- roadmap priorities, issue status, or release notes;
- prose that merely repeats the specification or another accepted decision;
- reversible editorial organization with no public or behavioral effect.

Use `proposed`, `accepted`, `rejected`, or `superseded` status. Do not silently rewrite the rationale of an accepted decision after it becomes evidence; add a superseding record when the choice changes.

## Coverage audit

The repository audit found that Decisions 0001–0012 already cover identity and scope, client zero, repository interfaces, versioning, non-transitive conformance, skill synchronization, source topology, scaffolding, portable skills, roadmap governance, Change Sets, and non-circular release evidence.

The following durable choices existed explicitly or implicitly without sufficient rationale and are now recorded:

| Decision | Previously visible in | Record |
|---|---|---|
| Canonical agent instructions plus host discovery shims | `AGENTS.md`, skill portability rules | 0013 |
| Deterministic validation with an agent repair loop | validator, CI, working rules | 0014 |
| Version-class release gates and MCP-only human handoff | versioning and Git workflow | 0015 |
| English as the public repository language | `AGENTS.md` | 0016 |
| Apache License 2.0 | `LICENSE`, `NOTICE`, manifest | 0017 |
| Only methodology and standalone framework profiles in 1.0 | specification taxonomy | 0018 |

Python, YAML, exact test commands, current roadmap ordering, and individual validator checks remain implementation or execution details. They require Change Set impact review when modified but not independent Decision Records unless their role becomes an externally constraining contract.
