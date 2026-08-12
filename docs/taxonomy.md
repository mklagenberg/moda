# Artifact Taxonomy

MODA taxonomy classifies the primary identity of an artifact separately from the components contained in its package.

## Operational test

Apply these questions in order:

1. Does it organize an adaptable decision space? It is probably a framework.
2. Does it prescribe a coherent end-to-end execution? It is probably a methodology.
3. Does it solve a bounded part of the work? It is probably a method.
4. Does it order transformations from inputs to outputs? It is probably a process.
5. Does it give exact operational instructions? It is probably a procedure.
6. Does it define a concrete executable flow? It is probably a workflow.
7. Does it define normative conformance? It is a specification.
8. Does it package operational guidance for an agent environment? It is a skill.

An artifact may have one primary kind and many component kinds. These labels are not maturity levels.

## Containment rule

A methodology may operationalize one or more frameworks and contain methods, processes, procedures, workflows, prompts, skills, schemas, and tools. A framework may accompany reference methodologies, but they are examples or package contents rather than part of the framework's conceptual core.

## Extraction rule

Consider extracting an embedded component when at least two conditions apply:

- it is reusable independently;
- it changes on a different cadence;
- it has contracts or evaluations of its own;
- other packages reference it directly;
- it needs independent provenance or ownership;
- adapters depend on it independently.
