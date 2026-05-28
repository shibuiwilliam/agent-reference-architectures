---
title: "[F5] Input Trust"
tags:
  - "Driving Variables"
---

# [F5] Input Trust

!!! abstract "Summary"
    A force that measures the likelihood of attack or contamination in agent input. The lower the trust, the more input inspection, isolation, and privilege separation are needed.

## Overview

An agent that was used as an internal management tool was opened to general users, and the next day prompt injection attacks leaked internal data -- just changing the input source completely changes the security measures the system requires.

Input trust represents how trustworthy the data received by the agent is. The risk level differs by orders of magnitude between API calls from internal systems and natural language input from anonymous users.

## Why It Matters

LLM-based agents are structurally vulnerable to malicious instructions embedded in input (prompt injection) precisely because they understand natural language. Without considering trust level, instructions in user input can override system prompts, execute operations beyond authorized scope, or leak sensitive data. Like traditional SQL injection, this is a problem that requires input boundary sanitization.

## Interpreting the Value Range

### When Low (Trust is High = Risk is Low)

Situations where input is limited to trusted internal sources. Examples include structured data from internal batch systems, API calls from authenticated administrators, and input from pre-validated data pipelines. Input format is fixed, leaving little room for malicious operations. Inspection can be kept light to prioritize throughput.

### When High (Trust is Low = Risk is High)

Situations receiving natural language input from anonymous users. Examples include public chatbots, email processing agents, web form requests, and RAG ingestion of external documents. Risks include prompt injection, indirect injection (instructions embedded in retrieved documents), and PII contamination. Input inspection, sanitization, and privilege separation become essential.

## Evaluation Guidelines

- Is the agent's input from authenticated internal systems or from anonymous users?
- Is natural language input embedded directly into prompts?
- Are external documents or search results incorporated into context (indirect injection path)?
- Could the input contain PII or sensitive information?
- What is the privilege level of the tools and data the agent can access?

## Influenced Design Decisions

### Related Dials

- [Guardrail Strictness](../../decisions/dials/guardrail-strictness.md) -- The lower the trust, the stricter the I/O inspection
- [Exposed Tool Count](../../decisions/dials/exposed-tool-count.md) -- Restrict available tools for untrusted input paths
- [Autonomy Level](../../decisions/dials/autonomy-level.md) -- Lower the autonomy level for untrusted input

### Related Tradeoffs

- [Same vs. Different Model](../../decisions/tradeoffs-catalog/same-vs-different-model.md) -- Separate the LLM processing untrusted input from the LLM performing privileged operations
- [Prompt vs. Code](../../decisions/tradeoffs-catalog/prompt-vs-code.md) -- Validate untrusted input in code (regex, schema validation)
- [Structured vs. Freeform](../../decisions/tradeoffs-catalog/structured-vs-freeform.md) -- The lower the trust, the more input should be structured to narrow the attack surface

## Related Patterns

- [#42 Data Boundary Firewall](../../foundations/forces/f5-input-trust.md) -- Inspect and mask PII and sensitive information at I/O boundaries
- [#44 Dual-LLM Privilege Separation](../../foundations/forces/f5-input-trust.md) -- Separate input processing and privileged operations into different LLMs
- [#43 Confused-Deputy Damage Limitation](../../foundations/forces/f5-input-trust.md) -- Limit the blast radius even when tricked
- [#18 Least-Privilege Tool Binding](../../decisions/dials/exposed-tool-count.md) -- Bind minimum privileges per session
- [#29 Guardrail Sidecar + Self-Correction](../../decisions/tradeoffs-catalog/inline-vs-post-verification.md) -- Inspect I/O and detect/correct violations
