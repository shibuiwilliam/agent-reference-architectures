---
title: "Exposed Tool Count"
tags:
  - "Tuning Dial"
  - "F6 Task Variability"
---

# Exposed Tool Count

!!! abstract "TL;DR"
    Control the number of tools shown to an agent per session, balancing capability breadth against selection accuracy.

## Overview

You asked for "send email" but the "send chat" tool was called instead -- with 30 tools listed, it is natural for the LLM to get confused. But removing too many necessary tools means tasks cannot be completed.

This dial determines the number of tool definitions included in the agent's system prompt. More tools expand the agent's range of actions, but also increase the probability of the LLM misselecting a tool. A design that dynamically narrows the tool set based on session purpose is required.

## Why Adjustment Is Needed

LLMs receive tool definitions as context, so as tool count increases, context consumption grows and attention to each tool's description becomes diluted. Experimentally, misselection rates increase significantly when tool count exceeds 20. On the other hand, if needed tools are unavailable, tasks cannot be completed.

## Extremes of the Range

### Too Small

Tools needed for task completion are unavailable, and the agent either responds "that tool is not available" or attempts to substitute with an inappropriate tool. The number of situations where user requests cannot be fulfilled increases, reducing usefulness.

### Too Large

Misselection between similar tools becomes frequent. For example, "send email" and "send chat" get confused. Tool definitions crowd out the context window, reducing the space available for actual instructions and user input. Token costs also increase.

## Determining Forces

- `[F6]` Task Variability -- Routine tasks can be handled with fewer tools; exploratory tasks require more

## Guidelines (Starting Point)

- Per session: 5-15 tools
- Routine tasks: Narrow to 3-5
- General-purpose assistant: Cap at 10-15, organized by category
- When 15+ are needed: Use two-stage tool selection (category selection -> tool selection)
- Keep tool definitions concise, minimizing token consumption per tool

## Practical Adjustment

- Analyze tool usage logs and identify the actual tool sets used per session type
- Remove tools with high non-usage rates from the default set; add only when needed
- Monitor tool misselection rates; if increasing, reduce tool count or improve descriptions
- Identify pairs of tools with highly similar names/descriptions and consolidate or differentiate them

## Related Patterns

- [#18 Least-Privilege Tool Binding](../../glossary.md) -- Binding minimum-privilege tool sets per session
