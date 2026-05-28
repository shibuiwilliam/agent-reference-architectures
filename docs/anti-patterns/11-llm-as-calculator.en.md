---
title: "Using LLMs as Calculators"
tags:
  - "Anti-Pattern"
  - "Pattern Misuse"
---

# 11. Using LLMs as Calculators

!!! abstract "TL;DR"
    An anti-pattern where LLMs are asked to directly perform arithmetic, date calculations, regex matching, and database queries, leading to frequent calculation errors and search misses.

## Common Scenario

An e-commerce site built an order management agent. For the question "What is the total for order number ORD-2024-5678?", the agent retrieved order details from the database and had the LLM calculate the total. The LLM answered "5,670 yen" for 3 items (1,280 yen + 3,500 yen + 890 yen) — which happened to be correct. However, calculation errors began appearing when the number of items exceeded 10. For 15 items, the LLM answered "43,200 yen," but the correct answer was 45,180 yen.

In another case, the LLM returned an incorrect result for a date calculation ("How many days remain on this contract?"), conveying wrong information to the customer. Additionally, when asked to perform regex validation (email format checking), the LLM judged invalid formats as "valid" in some cases.

## Symptoms

- Numerical calculation results are inaccurate (especially with many digits or multi-step calculations)
- Date/time calculation errors (leap years, time zones, etc.)
- Database search results are incomplete (missing records, overlooked conditions)
- The same question sometimes returns different calculation results (no reproducibility)
- Users increasingly verify and point out errors in results

## Root Cause

LLMs are language models that predict "the most plausible next token." Arithmetic operations require "accuracy," not "plausibility," and this is not an LLM's strength. Errors are especially common with multi-digit calculations, floating-point arithmetic, and date edge cases.

Database queries are similar — when an LLM tries to substitute SQL-equivalent operations through natural language reasoning, condition omissions and join logic errors occur. The LLM's role is "deciding what to calculate/search," not "performing the calculation/search."

## Detection Methods

- **Calculation accuracy tests**: Give the agent arithmetic problems and measure accuracy (especially 10+ item additions, multi-digit multiplications, date calculations)
- **Output reproducibility tests**: Send the same question multiple times and verify whether identical results are returned
- **Tool call verification**: Check via traces whether calculations and searches are performed through tools or through LLM reasoning alone
- **Metrics**: `calculation_accuracy_rate`, `search_recall`, `tool_call_rate` (tool delegation rate)

## Countermeasures

### Step 1: Identify calculation/search tasks and prepare tools

Among the tasks the agent handles, identify operations requiring precision — arithmetic, date calculations, database queries, regex matching — and prepare corresponding tools.

### Step 2: Structure LLM output to bridge to tools

Have the LLM output "what to calculate" or "what to search for" in a structured format, and delegate actual calculation/search to tools.

### Step 3: Force tool calls

To prevent the LLM from attempting to answer on its own when calculation or search is needed, encourage tool calls through both prompt design and system architecture.

```python
# Tool definition example
tools = [
    {
        "name": "calculate",
        "description": "Execute numerical calculations. Use for arithmetic, aggregation, and statistical calculations.",
        "parameters": {
            "expression": "Calculation expression (in Python-evaluable format)",
        },
    },
    {
        "name": "query_database",
        "description": "Search the database. Use for retrieving customer info, order info, etc.",
        "parameters": {
            "table": "Table name",
            "conditions": "List of search conditions",
            "aggregation": "Aggregation method (optional)",
        },
    },
    {
        "name": "date_calculate",
        "description": "Perform date/time calculations. Use for differences, additions, and format conversions.",
        "parameters": {
            "operation": "Type of calculation",
            "dates": "List of target dates",
        },
    },
]
```

## Examples

### Before (problematic state)

```python
# LLM performs calculations and searches directly
response = llm.chat(
    system="You are an order management assistant.",
    messages=[{
        "role": "user",
        "content": f"Calculate the total for the following order details:\n{order_details}"
        # order_details: "Item A: 1,280 yen, Item B: 3,500 yen, ... (15 items)"
    }],
)
# LLM answers "Total: 43,200 yen" (correct: 45,180 yen)
```

### After (improved)

```python
# LLM decides "what to calculate", actual calculation delegated to tools
response = llm.chat(
    system="Always use the calculate tool when calculation is needed.",
    tools=tools,
    messages=[{
        "role": "user",
        "content": f"What is the total for order ORD-2024-5678?"
    }],
)

# LLM output (tool call):
# {"tool": "query_database", "params": {"table": "order_items",
#   "conditions": [{"order_id": "ORD-2024-5678"}]}}
#
# After receiving tool results:
# {"tool": "calculate", "params":
#   {"expression": "1280 + 3500 + 890 + ..."}}
#
# Calculation result: 45180 (accurate)
```

## Related Anti-Patterns

- [Prompt as Security Boundary](10-prompt-as-security.md) — Both involve giving the LLM responsibilities it's not suited for
- [No Rationale for Dial Settings](06-no-rationale.md) — Tool delegation criteria need to be documented

## Related Patterns

- [#15 Inverted Structured Output](../decisions/tradeoffs-catalog/llm-vs-tool.md) — Have the LLM generate structured output for "what to execute"
- [#17 Tool / MCP Gateway](../decisions/tradeoffs-catalog/llm-vs-tool.md) — Tool call gateway
- [#11 Deterministic Core, Probabilistic Edge](../decisions/tradeoffs-catalog/prompt-vs-code.md) — Calculations belong in the deterministic core
