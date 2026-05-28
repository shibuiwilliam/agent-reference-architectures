---
title: Coding Agent Usage Guide
---

# Coding Agent Usage Guide

!!! abstract "Summary"
    Procedures, conventions, and output format for coding agents to read this catalog and make **evidence-based** architecture proposals for software systems that include AI agents.

## Purpose of This Guide

This catalog (59 patterns, 9 forces, 20 dials, 16 tradeoffs, 6 reference architectures) serves both as a human-readable reference and as a **structured data source for coding agents to generate design proposals**.

This guide defines **how coding agents should ingest this catalog, how to use it, and what to output**.

---

## Ingestion Methods

Choose from three paths depending on your token budget.

### Path 1: Index --> Fetch Only Needed Details (Recommended)

1. Read `/llms.txt` to understand the overall catalog structure
2. Read `/catalog.json` to get structured data (forces, dials, tradeoffs, patterns, rules)
3. Fetch individual `.md` pages only for the patterns whose details you need

### Path 2: Decision Core Only (Low Token)

1. Read `/llms-core.txt` (forces + dials + tradeoffs + reference architectures + rules + quick reference)
2. Fetch individual details only for patterns that require it

### Path 3: Full Text Bulk Load (When Context Allows)

1. Read `/llms-full.txt` to ingest all pages at once

### Path 4: MCP Connection (Native Integration)

Connect via MCP server and retrieve needed information on demand during conversation.

- `search_patterns(query)` -- semantic search for pattern candidates
- `get_pattern(id)` -- structured details
- `recommend(force_profile)` -- force evaluation --> recommended patterns
- `list_reference_architectures()` -- composite architecture list
- `get_decision(dial|tradeoff)` -- dial/tradeoff details

---

## Design Procedure

Upon receiving requirements, generate an architecture proposal following these steps.

### Step 1: Force Evaluation (F1--F9)

Estimate each of the 9 driving variables as "high/medium/low." Always include rationale.

| Force | Question |
|-------|----------|
| F1 Reversibility | Can failures be undone? |
| F2 Failure Cost | Financial/legal/safety impact |
| F3 Request Value | Contribution to revenue/decision-making |
| F4 Latency Budget | User's tolerance for waiting |
| F5 Input Trust | Likelihood of attack/contamination |
| F6 Task Variability | Routine vs. exploratory |
| F7 Cost Sensitivity | QPS and monthly cost cap |
| F8 Accountability | Audit and compliance requirements |
| F9 Provider Reliability | External LLM availability |

### Step 2: Resolve Tradeoffs

Based on the force evaluation, determine the direction for the 16 binary choices (sync vs. async, single vs. multi-agent, etc.). Refer to the `driver` and `default` fields in the `tradeoffs` section of `catalog.json`.

### Step 3: Set Dials

Determine initial values for the 20 dials related to adopted patterns, based on force value ranges. Refer to the `driver` and `default` fields in the `dials` section of `catalog.json`.

### Step 4: Select Patterns and Compose Architecture

- Refer to the `rules` in `catalog.json` to find recommended patterns matching the force conditions
- Check alignment with the reference architectures (6 compositions)
- Add or omit patterns as needed

### Step 5: Output the Proposal

Always output according to the [Architecture Proposal Template](agent-proposal-template.md).

---

## Citation Conventions

**Explicitly cite** stable IDs from the catalog as rationale for every decision in the proposal.

- Pattern: `#N` (e.g., `#31 Human Approval Checkpoint`)
- Force: `[F#]` (e.g., `[F2]` Failure Cost)
- Dial: Dial name (e.g., `Timeout`)
- Tradeoff: Tradeoff name (e.g., `Sync vs. Async`)
- Reference Architecture: Architecture name (e.g., `Side-Effect-First Architecture`)

**Example**: "Because `[F2]` is high and `[F1]` is low, we adopt `#31 Human Approval Checkpoint` and `#19 Dry-Run First`, composing the architecture based on the `Side-Effect-First Architecture`."

---

## Boundary Conventions (Safety Rules)

!!! warning "Must Comply"

1. **Use only catalog patterns**: Use only the 59 patterns, 20 dials, and 16 tradeoffs defined in this catalog as proposal vocabulary. **Do not fabricate patterns that do not exist in the catalog**.
2. **Disclose uncertainty**: If a force evaluation is ambiguous or the applicability of a pattern is unclear, **state "uncertain" explicitly** and ask the human for confirmation.
3. **Final judgment is human**: Proposals are **intended for human review** and should not be auto-applied. Use the "Unresolved Issues" section of the proposal template to clearly state what needs human confirmation.
4. **Acknowledge scope limitations**: This catalog is a pattern collection for "AI agent production architecture" and is not universal. **Explicitly state** when design decisions fall outside the catalog's scope (database selection, network design, etc.).
5. **Guideline values are starting points**: Dial guideline values and defaults are "starting points" that require validation and tuning with production data. Avoid assertive numerical specifications.

---

## Related Pages

- [catalog.json](catalog.json) -- Machine-readable manifest
- [Architecture Proposal Template](agent-proposal-template.md) -- Output format
- [Worked Examples](decisions/worked-examples.md) -- End-to-end examples from force evaluation to proposal
- [Reverse Lookup by Force](decisions/by-force.md) -- Dictionary indexed by force
- [Driving Variables (Forces)](foundations/forces.md) -- Force definitions
