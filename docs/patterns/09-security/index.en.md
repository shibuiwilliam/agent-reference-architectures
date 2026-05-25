# IX. Security & Multi-tenancy


!!! tip "Key decisions for this concern"
    - **Primary forces**: `[F5]` Input Trustworthiness, `[F8]` Accountability, `[F2]` Failure Cost
    - **Key dials**: Exposed tool count, Guardrail strictness → [Tuning Dials](../../decisions/tuning-dials.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

Users may embed malicious instructions in messages, or agents may be deceived by indirect prompt injection hidden in email bodies -- these are real threats in production environments. This section covers defense layers built on the premise that natural language interfaces directly become attack surfaces.

- [#41 Tenant-Isolated Agent Runtime](41-tenant-isolated-agent-runtime.md) — Isolate execution environments and memory per tenant
- [#42 Data Boundary Firewall](42-data-boundary-firewall.md) — Inspect and mask PII and sensitive information at I/O boundaries
- [#43 Confused-Deputy Damage Limitation](43-confused-deputy-damage-limitation.md) — Structurally limit blast radius even when the agent is deceived
- [#44 Dual-LLM Privilege Separation](44-dual-llm-privilege-separation.md) — Separate quarantined and privileged LLMs for access control
