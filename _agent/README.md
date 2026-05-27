# Agent Entry Point — AI Agent Production Architecture Patterns v1.1.0

> Wrap a probabilistic core in a deterministic shell — contracts, verification, budgets, permissions, observation — and tune the shell's dials to context (forces).

## What You Can Do With This Catalog

Using this catalog (59 patterns, 9 forces, 20 dials, 16 tradeoffs, 6 reference architectures, 10 decision rules), you can generate architecture proposals for software systems that incorporate AI agents. All decisions must cite forces [F#] and patterns #N as evidence.

## Reading Order (Progressive Disclosure)

| Level | File | Size | What You Get |
|-------|------|------|-------------|
| 0 | `_agent/README.md` (this file) | ~2KB | Entry point, algorithm overview, constraints |
| 1 | `_agent/decision-core.md` | ~15KB | Forces + rules + dial defaults + tradeoff defaults |
| 2 | `_agent/pattern-cards.json` | ~30KB | All 59 patterns as structured selection data |
| 3 | `docs/patterns/<cat>/<slug>.md` | per-file | Full narrative detail for individual patterns |

### Context Window Strategy

- **8K–32K tokens**: Load Level 0 + Level 1. Narrow to 3–5 patterns, then fetch Level 3 individually.
- **32K–128K tokens**: Load Level 0 + 1 + 2. Hold all pattern summaries; fetch Level 3 as needed.
- **128K+ tokens**: Load `docs/llms-full.txt` (363KB) for complete content.
- **MCP**: Connect to `mcp-server/server.py`. Query on demand without consuming context.

## Decision Algorithm (Procedural)

Input: Requirements text
Output: Architecture proposal (`_agent/proposal-template.md` format)

```
Step 1 — EVALUATE FORCES
  Read `_agent/decision-core.md` § Forces.
  For each F1–F9, assign {high, mid, low} based on requirements.
  Record rationale for each.

Step 2 — MATCH RULES
  Read `_agent/decision-core.md` § Decision Rules.
  For each rule, check if ALL conditions in `if` match your force evaluation.
  Collect `required` / `recommended` / `optional` pattern sets from matching rules.
  When multiple rules match, take the UNION of all required patterns.

Step 3 — RESOLVE TRADEOFFS
  Read `_agent/decision-core.md` § Tradeoffs.
  For each of the 16 tradeoffs:
    Look at the `decision_function.drivers` (force IDs).
    Apply the `decision_function.logic` to your force values.
    Choose a (option A), b (option B), or hybrid.

Step 4 — SET DIALS
  Read `_agent/decision-core.md` § Dials.
  For each of the 20 dials:
    Scan `value_mapping` entries.
    Find the entry whose `condition` matches your force values.
    Use its `range`/`value` + `unit` as the initial setting.

Step 5 — SELECT REFERENCE ARCHITECTURE
  Read `_agent/decision-core.md` § Reference Architectures.
  Score each architecture by counting how many force conditions match.
  The highest-scoring architecture is the base.
  Add patterns from Steps 2–3 that aren't already in the base.

Step 6 — OUTPUT PROPOSAL
  Use `_agent/proposal-template.md` format.
  Every decision MUST cite the force(s) that drove it.
  List uncertain evaluations in "Unresolved Questions".
```

## Quick Indexes (Shortcut to Relevant Patterns)

- **By task type**: `_agent/by-task.md` — "building a chatbot?", "building a code agent?"
- **By problem**: `_agent/by-problem.md` — "cost explosion?", "hallucination?"
- **By force**: `_agent/decision-core.md` § by_force index

## Constraints

1. Use only the 59 cataloged patterns. Do not invent patterns.
2. Cite `[F#]` forces and `#N` patterns as evidence for every decision.
3. Flag uncertain force evaluations explicitly.
4. All proposals require human review before implementation.
5. Dial values are starting points; they require production validation.

## Version

Catalog version: **v1.1.0** (`patterns.yml` / `decisions.yml`)
