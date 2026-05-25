---
title: "Prompt/Model/Tool Version Pinning"
tags:
  - "Observability, Auditing & Evaluation"
  - "F8 Accountability & Regulation"
---

# #33 Prompt/Model/Tool Version Pinning

!!! abstract "TL;DR"
    **Explicitly pin** the versions of prompts, models, and tools to establish a foundation for reproducibility and regression detection.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #33 Prompt/Model/Tool Version Pinning</summary>

| Field | Value |
|------|-----|
| **ID** | 33 |
| **Category** | 07-observability — Observability, Auditing & Evaluation |
| **Forces** | `[F8]` |
| **Dials** | prompt-storage |
| **Tradeoffs** | — |
| **Related Patterns** | #34, #32, #35 |
| **When to Use** | Production agents, multi-model comparison, model auto-upgrade risk |
| **When Not to Use** | Experimental prototypes where always using the latest is preferred |
| **Element Technologies** | Git tag+hash, Langfuse Registry, Humanloop, model snapshot IDs, Docker image tag |

</details>
<!-- END:GEN:meta -->

## Overview

"The agent that was working perfectly yesterday suddenly started returning strange answers this morning" -- it is not uncommon for an LLM provider to silently update a model. Without knowing what changed, there is no way to identify the root cause.

An agent's behavior is determined by the combination of prompt templates, LLM model versions, and tool (including MCP) API versions. When any of these changes unnoticed, output fluctuates and pinpointing failure causes becomes difficult. This pattern assigns version identifiers to each of these three components and pins them in the deployment configuration. By also recording versions in traces, you can always track "when and what changed."

!!! info "Position in decision-making"
    - **Driving force**: `[F8]` Accountability & Regulation
    - **Related decision**: Prompt storage location and granularity in [Tuning Dials](../../decisions/tuning-dials.md)
    - **Decision flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

Prompts are version-controlled in Git or a prompt registry and pinned at deploy time by hash or tag. Models are called with snapshot designations (e.g., `gpt-4o-2024-11-20`), never using `latest` aliases in production. Tools are pinned by API version headers or MCP server image tags. These three components are managed as a release bundle, and changes are rolled out only after passing [#34 Evaluation CI/CD](34-evaluation-ci-cd.md).

## Problems Solved

LLM provider model updates or subtle prompt modifications can change production behavior without warning. Without version pinning, you cannot isolate the cause of "it was working yesterday but broke today," and regression tests become meaningless `[F8]`.

## When to Use / When Not to Use

- **When to Use**: All production agents. Especially in regulated industries, services with SLAs, and configurations using multiple models.
- **When Not to Use**: During exploratory prototyping where you want to constantly try the latest models (pinning can be introduced once things stabilize).

## Element Technologies

- Prompt management: Git + tags, Langfuse Prompt Registry, Humanloop
- Model pinning: OpenAI snapshot ID, Anthropic model version, Azure OpenAI deployment
- Tool pinning: Docker image tag, API version header, MCP server version

## Related Patterns

- [#34 Evaluation CI/CD](34-evaluation-ci-cd.md) — Run automated evaluations on version changes to detect regressions
- [#32 Agent Trace](32-agent-trace.md) — Record version information in traces for post-hoc tracking
- [#35 Production Replay](35-production-replay.md) — Replay traces from old versions on new versions to verify differences

## References

- OpenAI Model Deprecation Policy
- Anthropic API Versioning
