---
title: "[F8] Accountability & Regulation"
tags:
  - "Driving Variables"
---

# [F8] Accountability & Regulation

!!! abstract "Summary"
    A force that measures the degree of audit, compliance, and accountability requirements. The higher it is, the more essential traceability, reproducibility, and codified policies become.

## Overview

When a financial regulator asks "why did this agent make this investment decision," can you present the prompt, model version, and intermediate reasoning in full? Records that are unnecessary for internal experimental tools may trigger immediate regulatory action if absent in a regulated system.

Accountability & regulation represents the degree to which "why that result was produced" needs to be explained and proven after the fact for agent decisions and outputs.

## Why It Matters

Neglecting this force in regulated industries means being unable to present the rationale behind agent decisions during audits, leading to regulatory sanctions or license suspension. Additionally, if root cause cannot be identified during incidents, preventive measures cannot be established. The non-deterministic nature of LLMs -- "different outputs for the same input every time" -- requires more deliberate recording and pinning mechanisms than traditional software.

## Interpreting the Value Range

### When Low

Internal tools, prototypes, and experimental use where external accountability is limited. Examples include developer code completion, internal knowledge search, and PoC-stage agents. Logging sufficient for debugging on problem occurrence is adequate, and there is little need to enforce version pinning or detailed tracing.

### When High

Medical, financial, legal, government procurement, and other domains where compliance with regulations or industry standards is required. Decision rationale must be retained as an audit trail, with the full history of prompts, model versions, and tool calls recorded in a reproducible format. Policies must be codified as code, and changes must be verified through CI/CD before deployment. Regulatory requirements may also extend to data retention periods, access controls, and anonymization.

## Evaluation Guidelines

- Is there a reporting obligation to external auditors or regulators for system output?
- Are there records that allow third parties to understand "why that decision was made" when incidents occur?
- Can prompts and model versions be traced back and reproduced at a specific point in time?
- Are there legal requirements regarding data retention periods or deletion obligations?
- Is compliance with industry-specific standards (SOC2, HIPAA, FISC, etc.) required?

## Influenced Design Decisions

### Related Dials

- [Trace Sampling Rate](../../decisions/dials/trace-sampling-rate.md) -- Set to full recording (100%) when regulatory requirements are high
- [Log Retention Period](../../decisions/dials/log-retention.md) -- Align with the retention period required by regulations
- [Prompt Storage](../../decisions/dials/prompt-storage.md) -- Store full prompt text for audit purposes
- [Guardrail Strictness](../../decisions/dials/guardrail-strictness.md) -- Set guardrail strictness according to regulatory requirements

### Related Tradeoffs

- [Prompt vs. Code](../../decisions/tradeoffs-catalog/prompt-vs-code.md) -- Codify policies that require auditability as code
- [In-Context vs. External](../../decisions/tradeoffs-catalog/in-context-vs-external.md) -- Persist audit trails in external stores
- [Build vs. Buy](../../decisions/tradeoffs-catalog/build-vs-buy.md) -- Check the certification status of managed services for meeting regulatory requirements

## Related Patterns

- [#32 Agent Trace](../../glossary.md) -- Log every step as an append-only record for replay and audit
- [#30 Policy-as-Code Guardrail](../../glossary.md) -- Codify constraints for mechanical evaluation
- [#33 Version Pinning](../../glossary.md) -- Pin prompt, model, and tool versions to ensure reproducibility
- [#34 Evaluation CI/CD](../../glossary.md) -- Automated evaluation per change to detect regressions
- [#27 Evidence-First Answer](../../glossary.md) -- Retrieve and cite evidence before answering to make decision rationale explicit
- [#52 Agent Constitution](../../glossary.md) -- Systematically deploy behavioral principles
