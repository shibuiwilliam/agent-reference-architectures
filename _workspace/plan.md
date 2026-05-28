# Decision-Only Restructure — Work Plan

## Phase 0: Survey & Migration (DONE)
- [x] Create branch `feat/decision-only-restructure`
- [x] Verify baseline `mkdocs build --strict`
- [x] Extract summary/design from all 59 pattern pages
- [x] Add primary_decision to each pattern in patterns.yml
- [x] Validate all 59 patterns have required fields

## Phase 1: Build Integration Targets
- [ ] Create `scripts/check_migration.py` (safety gate)
- [ ] Update `scripts/generate.py`:
  - [ ] Generate `docs/glossary.md` (pattern quick-reference table)
  - [ ] Generate GEN:patterns blocks in dial/tradeoff/force/by-force pages
  - [ ] Update catalog.json to include full pattern data (summary/design/primary_decision)
  - [ ] Generate redirect mapping table
  - [ ] Remove pattern-page-specific generation (meta blocks, frontmatter)
- [ ] Add `<!-- BEGIN:GEN:patterns --><!-- END:GEN:patterns -->` markers to decision pages
- [ ] Verify: generate.py idempotent, build --strict, check_migration.py green, glossary 59 rows

## Phase 2: Pattern Reference Removal & Redirects
- [ ] Install mkdocs-redirects
- [ ] Remove "パターン・リファレンス（語彙）" from mkdocs.yml nav
- [ ] Delete `docs/patterns/**`
- [ ] Configure redirect_maps for all 59 patterns
- [ ] Create `scripts/check_redirects.py`
- [ ] Reframe reference-architectures → "意思決定プリセット"
- [ ] Reframe anti-patterns → "意思決定の誤り"
- [ ] Redirect pattern-index → glossary
- [ ] Verify: build --strict, check_redirects.py green, no pattern files remain

## Phase 3: Agent Guide, LLMs, Finish
- [ ] Update agent-guide.md (decision-centric workflow, citation rules, safety rules, proposal template, human-final-decision)
- [ ] Sync AGENTS.md
- [ ] Regenerate llms.txt / llms-core.txt / llms-full.txt
- [ ] Bump version to 2.0.0 (breaking change)
- [ ] Update CHANGELOG.md
- [ ] Update CLAUDE.md / PROJECT.md
- [ ] JP/EN parity check
- [ ] Final acceptance (all §6 checks)

## Risk Mitigations
- Pattern content extracted BEFORE any deletion
- check_migration.py must pass before Phase 2
- All 59 URLs get redirects via mkdocs-redirects
- catalog.json retains full pattern data for machine consumption
