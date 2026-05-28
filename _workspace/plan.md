# Integrated Restructure Plan

## Status
- [x] Phase 0: Audit & Plan
- [x] Phase 1: Agent-consumable state (was mostly pre-existing)
  - [x] patterns.yml extended (related, when_to_use, when_not, element_tech, dials, tradeoffs)
  - [x] decisions.yml complete (characteristics, forces, dials, tradeoffs, ref_archs, rules)
  - [x] generate.py producing catalog.json, llms.txt, llms-core.txt, llms-full.txt
  - [x] CI: generate.py step in deploy.yml before mkdocs build
  - [x] agent-guide.md complete (procedures, citation, safety, 3 lanes, proposal template link)
  - [x] agent-proposal-template.md exists
  - [x] AGENTS.md synced with agent-guide.md
  - [x] CHANGELOG.md + version 1.2.0
- [x] Phase 2: Stabilization & enrichment
  - [x] GEN:meta blocks in all 59 patterns (JP + EN)
  - [x] Rules in catalog.json + human-readable decisions/rules.md
  - [x] pattern-index.md table generated from markers
  - [ ] tuning-dials.md table generated from markers
  - [ ] tradeoffs.md table generated from markers
  - [ ] by-force.md table generated from markers
  - [x] Worked examples: 3 systems (RAG chatbot, payment, support)
  - [x] check_links.py — bidirectional link audit
  - [x] check_lang_parity.py — JP/EN coverage
- [x] Phase 3: Native integration
  - [x] mcp/ server with smoke test
  - [x] 3 integration lanes documented (AGENTS.md + agent-guide.md)
  - [x] .cursor/rules snippet in AGENTS.md
  - [x] CLAUDE.md / PROJECT.md updated
  - [x] JP/EN 100% parity
