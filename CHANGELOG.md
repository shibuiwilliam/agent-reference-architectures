# Changelog

## [2.0.0] — 2026-05-28

### BREAKING: Pattern Reference dissolved into Decision Layer

The 59 independent pattern pages (`docs/patterns/**`) have been **removed** and their content integrated into the decision layer. All external URLs are preserved via redirects.

#### What changed
- **Pattern pages deleted**: All 59 pattern pages (JP + EN) and 12 category index pages removed
- **72 redirects**: All old `/patterns/**` URLs redirect to the relevant decision page (dial, tradeoff, or force) via `mkdocs-redirects`
- **Nav restructured**: "パターン・リファレンス（語彙）" tab removed; patterns are now "vocabulary" referenced within decision pages
- **Glossary**: New `docs/glossary.md` — 59-row quick-reference table replacing the pattern catalog
- **Decision pages enriched**: Each dial, tradeoff, and force page now shows related patterns (`GEN:patterns` blocks)
- **catalog.json expanded**: Patterns now include `summary`, `design`, `primary_decision` fields (full data retention)
- **patterns.yml expanded**: Each pattern now has `summary`, `design`, `primary_decision` fields
- **Sections reframed**: "リファレンスアーキテクチャ" → "意思決定プリセット", "アンチパターン" → "意思決定の誤り"

#### Migration for consumers
- **External links**: All 72 old URLs redirect automatically — no action needed
- **catalog.json**: Same endpoint, same structure + new fields. Backward compatible.
- **Agents**: Use `glossary.md` or `catalog.json` instead of pattern `.md` files
- **llms.txt / llms-core.txt / llms-full.txt**: Updated to decision-centric structure

#### Why
Patterns are now "conclusions of decisions" rather than "a second reference to look up." The decision layer is the single backbone: forces → dials/tradeoffs → patterns (#N) → presets → ADR.

---

## [1.2.0] — 2026-05-28

### Decision layer (`decisions.yml`)
- Added `characteristics` (C1–C9) with id, name, description, group, and force linkages
- Version bumped to 1.2.0

### Catalog (`catalog.json`)
- Added `characteristics` array — 9 AI agent characteristics with force mappings
- All required keys now present: version, principle, characteristics, forces, dials, tradeoffs, reference_architectures, rules, patterns

### Decision rules page (`docs/decisions/rules.md`)
- New human-readable IF–THEN rules page generated from `decisions.yml` rules
- Both JP and EN versions with `GEN:rules` marker-based generation

### Scripts
- `scripts/check_links.py` — bidirectional link audit (dials/tradeoffs ↔ patterns)
- `scripts/check_lang_parity.py` — JP/EN coverage check

### Link integrity
- Fixed 8 bidirectional link inconsistencies between patterns.yml and decisions.yml
- All dial↔pattern and tradeoff↔pattern references are now symmetric

### MCP server (`mcp/`)
- New `mcp/` directory with server.py, smoke_test.py, README.md
- Fixed `recommend()` to handle new required/recommended/optional rule format
- Smoke test validates catalog structure and all tool functions

### Agent integration (`AGENTS.md`)
- Added 引用規約 (citation rules), 境界規約 (safety rules), 最終判断は人間
- Added 取り込み経路 3 lanes (local files / URL fetch / MCP)
- Added `.cursor/rules` snippet for minimal agent configuration

### Documentation
- `CLAUDE.md` — updated with generation pipeline diagram, check scripts, marker convention
- `PROJECT.md` — updated directory layout with mcp/, check scripts

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
