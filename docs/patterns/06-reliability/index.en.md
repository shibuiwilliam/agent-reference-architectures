# VI. Reliability, Verification, Guardrails & Autonomy


!!! tip "Key decisions for this concern"
    - **Primary Forces**: `[F2]` Failure Cost, `[F5]` Input Trustworthiness, `[F1]` Reversibility
    - **Primary Dials**: Guardrail Strictness, Self-Correction Loop Count, HITL Frequency, Autonomy Level → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Primary Tradeoffs**: Inline ↔ Post-Verification, Same ↔ Different Model Verification → [Tradeoffs](../../decisions/tradeoffs.md)
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

LLMs can confidently produce incorrect answers or stray from the prompt's intent — this is not uncommon. This layer detects and recovers from such hallucinations and deviations before they reach the user. The goal is not total control but containment of impact.

- [#27 Evidence-First Answer](27-evidence-first-answer.md) — Retrieve evidence first, then present answers with citations
- [#28 Verifier Agent / Critic](28-verifier-agent-critic.md) — Inspect output with an independent verifier before shipping
- [#29 Guardrail Sidecar + Self-Correction](29-guardrail-sidecar-self-correction.md) — Inspect I/O with a sidecar and self-correct errors
- [#30 Policy-as-Code Guardrail](30-policy-as-code-guardrail.md) — Define behavioral constraints as code for deterministic evaluation
- [#31 Human Approval Checkpoint](31-human-approval-checkpoint.md) — Require human approval before high-risk operations
- [#57 Autonomy Ladder](57-autonomy-ladder.md) — Gradually increase agent autonomy based on track record
