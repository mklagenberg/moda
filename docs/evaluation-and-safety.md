# Evaluation and Safety

Structural conformance does not prove outcome quality. Every operational methodology needs evaluations appropriate to its domain and risk.

## Evaluation design

Include representative success cases, boundary cases, known failure cases, adversarial cases, interruption and recovery, unavailable tools, contradictory evidence, and human-escalation scenarios.

Compare against a meaningful baseline such as competent human execution, a single-agent approach, the previous methodology version, or a deterministic implementation.

Track correctness, coverage, traceability, reproducibility, time, cost, intervention rate, unsafe-action rate, and recovery behavior where applicable.

## Safety design

Declare permissions, data classes, external effects, irreversible actions, approval gates, least privilege, secret boundaries, logging, retention, and emergency stop behavior.

High-impact domains require domain-specific controls beyond MODA. A MODA audit must not present structural conformance as regulatory, security, legal, medical, or financial assurance.
