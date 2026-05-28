# Current State Audit — 2026-05-28

## Existing URLs
- All 59 pattern pages under `docs/patterns/<NN-category>/<NN-slug>.md` — **do not move**
- Decision pages under `docs/decisions/` — **do not move**
- Foundation pages under `docs/foundations/` — **do not move**
- Reference architecture pages under `docs/reference-architectures/` — **do not move**
- Anti-pattern pages under `docs/anti-patterns/` — **do not move**
- `docs/agent-guide.md`, `docs/agent-proposal-template.md`, `docs/pattern-index.md` — **do not move**

## Machine-readable artifacts
- `docs/catalog.json` — EXISTS (173KB, v1.1.0 → now v1.2.0)
- `docs/llms.txt` — EXISTS
- `docs/llms-core.txt` — EXISTS
- `docs/llms-full.txt` — EXISTS

## Agent guide (`/agent-guide/`)
- 手順: YES
- 引用規約: YES
- 境界規約: YES
- 取り込み経路: YES (4 lanes: index, core, full, MCP)
- 提案テンプレへのリンク: YES
- 最終判断は人間: YES

## GEN:meta blocks
- 59 JP patterns: ALL have `<!-- BEGIN:GEN:meta -->` markers
- 59 EN patterns: ALL have `<!-- BEGIN:GEN:meta -->` markers (118 total)

## Data files
- `decisions.yml` — EXISTS (36KB+, v1.2.0 with characteristics)
- `scripts/generate.py` — EXISTS (43KB+), idempotent
- `anti-patterns.yml` — EXISTS

## JP/EN parity
- JP=159, EN=159, coverage=100%

## Gaps identified (at start of this session)
1. `catalog.json` was missing `characteristics` key — FIXED
2. `AGENTS.md` not synced with agent-guide.md — FIXED
3. `docs/decisions/rules/` human page missing — FIXED (created rules.md)
4. `scripts/check_links.py` missing — FIXED
5. `scripts/check_lang_parity.py` missing — FIXED
6. `mcp/` directory with smoke test missing — FIXED
7. CLAUDE.md/PROJECT.md not updated — FIXED
8. 8 bidirectional link inconsistencies — FIXED
9. tuning-dials.md / tradeoffs.md / by-force.md tables not generated — PENDING
