# Changelog

## [1.1.0] — 2026-05-27

### Decision layer (`decisions.yml`)
- Restructured all 10 rules into `required` / `recommended` / `optional` tiers with escalation conditions
- Added `value_mapping` (force-conditional value ranges) to all 20 dials
- Added `decision_function` (structured judgment criteria) to all 16 tradeoffs
- Added `architecture_selection` for composite reference architecture selection based on multi-force conditions

### Pattern data (`patterns.yml`)
- Added `selection_criteria` (when to select, skip, combine, or substitute) to all 59 patterns
- Added `summary_plain` (plain-text 1–2 sentence overview) to all 59 patterns
- Added `prevents_anti_patterns` (cross-reference to anti-patterns) to all 59 patterns

### Anti-patterns (`anti-patterns.yml` — new file)
- Created structured definitions for all 11 anti-patterns: symptoms, root causes, preventive patterns, related dials and forces

### Catalog (`catalog.json`)
- Added `by_force` — reverse index from each force to its related patterns, dials, tradeoffs, rules, and anti-patterns
- Added `bidirectional_related` — symmetric pattern relationships computed from all `related` fields
- Added `selection_guide` — step-by-step procedure for force evaluation → pattern selection
- Added `anti_patterns` — full anti-pattern dataset from `anti-patterns.yml`

### Generation pipeline (`generate.py`)
- Agent-readable markdown conversion for `llms-full.txt` / `llms-core.txt` (admonitions → blockquotes, mermaid → text notes, details → expanded, relative links → text refs)
- `--lint` option for structural validation of all 59 pattern pages
- `--validate` option for JSON Schema validation (requires `schemas/`)

### Schemas (`schemas/` — new directory)
- `patterns.schema.json`, `decisions.schema.json`, `catalog.schema.json` (JSON Schema Draft 2020-12)

### Documentation
- `docs/index.md` — restructured for dual audience (human + coding agent) with separate reading paths
- `docs/agent-guide.md` — updated design steps to reference new structured fields (`by_force`, `selection_guide`, `decision_function`, `value_mapping`)
- `AGENTS.md` — synchronized with agent-guide changes
