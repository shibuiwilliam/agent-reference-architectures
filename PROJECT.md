# PROJECT.md

This is the documentation site for **AI Agent Production Architecture Patterns** — 59 patterns across 12 categories for taking AI agents from prototype to production. Built with MkDocs (Material) and published to GitHub Pages.

The organizing principle: **decisions are the backbone, patterns are the vocabulary**. Rather than a flat pattern catalog, the site guides readers through force evaluation → tradeoff resolution → dial tuning → pattern selection → architecture composition.

**At a glance:**

- **Audience:** Architects and engineers shipping AI agents to production, plus coding agents that consume the catalog programmatically
- **Scale:** 12 categories, 59 patterns, 9 forces, 20 dials, 16 tradeoffs, 6 reference architectures, 11 anti-patterns
- **Source of truth:** [`patterns.yml`](patterns.yml) + [`decisions.yml`](decisions.yml) + [`anti-patterns.yml`](anti-patterns.yml)
- **Writing rules:** [`CLAUDE.md`](CLAUDE.md)
- **Agent integration:** [`AGENTS.md`](AGENTS.md)

---

## Tech Stack

| Role | Tool |
|------|------|
| Static site generator | MkDocs |
| Theme | Material for MkDocs |
| Diagrams | Mermaid (via `pymdownx.superfences`) |
| Hosting | GitHub Pages (`gh-pages` branch) |
| CI/CD | GitHub Actions (`.github/workflows/deploy.yml`) |
| Site language | Japanese (`theme.language: ja`) |

---

## Directory Layout

```text
agent-architecture-patterns/
├─ mkdocs.yml                  # Site config & nav (manually managed)
├─ requirements.txt            # mkdocs-material, pymdown-extensions
├─ patterns.yml                # ★ Source of truth: 59 patterns
├─ decisions.yml               # ★ Source of truth: forces, dials, tradeoffs, rules
├─ anti-patterns.yml           # ★ Source of truth: 11 anti-patterns
├─ PROJECT.md                  # You are here
├─ CLAUDE.md                   # Writing instructions for Claude Code
├─ AGENTS.md                   # Coding agent integration guide
├─ CHANGELOG.md                # Release history
├─ schemas/                    # JSON Schema (patterns / decisions / catalog)
├─ .github/workflows/deploy.yml
├─ scripts/
│  ├─ scaffold.py              # Stub generator from patterns.yml (idempotent)
│  └─ generate.py              # YAML → catalog.json, llms.txt, meta blocks, etc.
├─ mcp-server/
│  └─ server.py                # MCP server (reads catalog.json)
├─ templates/
│  └─ pattern.md               # Writing template (not part of the build)
└─ docs/                       # ★ Build target — everything the site serves
   ├─ index.md                 # Landing page
   ├─ foundations/
   │  ├─ characteristics.md     # AI agent characteristics
   │  └─ forces.md              # Driving variables F1–F9
   ├─ patterns/
   │  ├─ 01-execution/          # I. Execution (01–07, 55, 58, 59)
   │  ├─ 02-composition/        # II. Composition (08–12)
   │  ├─ 03-io-contract/        # III. I/O & Contract (13–16)
   │  ├─ 04-tools-mcp/          # IV. Tools & MCP (17–22)
   │  ├─ 05-memory-context/     # V. Memory & Context (23–26)
   │  ├─ 06-reliability/        # VI. Reliability (27–31, 57)
   │  ├─ 07-observability/      # VII. Observability (32–36, 54)
   │  ├─ 08-cost-scaling/       # VIII. Cost & Scaling (37–40, 56)
   │  ├─ 09-security/           # IX. Security (41–44)
   │  ├─ 10-deployment/         # X. Deployment (45–48)
   │  ├─ 11-ux/                 # XI. UI/UX (49–51)
   │  └─ 12-governance/         # XII. Governance (52–53)
   ├─ decisions/                # Decision framework pages
   ├─ anti-patterns/            # 11 anti-patterns
   ├─ reference-architectures/  # 6 composite configurations
   ├─ pattern-index.md          # Quick-reference table (auto-generated)
   ├─ agent-guide.md            # Guide for coding agents
   ├─ agent-proposal-template.md
   ├─ catalog.json              # Machine-readable manifest (generated)
   ├─ llms.txt                  # llmstxt.org index (generated)
   ├─ llms-core.txt             # Decision core, low-token (generated)
   └─ llms-full.txt             # Full-text concatenation (generated)
```

Pattern filenames follow `NN-slug.md` (zero-padded number + hyphenated English slug). Numbers may skip (e.g., 55, 58, 59 in category I) because newer patterns were added to existing categories. **Numbers and slugs are immutable** — `patterns.yml` is the authority.

---

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/scaffold.py     # Create any missing stubs (safe to re-run)
mkdocs serve                   # Preview at http://127.0.0.1:8000
mkdocs build --strict          # Full build — catches broken links
```

---

## Deploying to GitHub Pages

1. Push to `main`.
2. Make sure `site_url` / `repo_url` in `mkdocs.yml` point to your fork.
3. The GitHub Actions workflow builds and deploys to the `gh-pages` branch automatically.
4. In repo settings, set Pages source to **Deploy from branch → `gh-pages` / `(root)`**.

> Manual deploy: `mkdocs gh-deploy --force`

---

## Writing Workflow (with Claude Code)

1. `python scripts/scaffold.py` — ensure the target stub exists.
2. Write the `.md` following [`CLAUDE.md`](CLAUDE.md) rules and the [exemplar](docs/patterns/01-execution/01-request-to-job-gateway.md).
3. `mkdocs build --strict` — verify clean build.
4. Commit: one pattern per commit (e.g., `docs(#12): write Blackboard pattern`).

---

## Progress

All 59 patterns, foundations, decision layer, anti-patterns, reference architectures, and pattern index are complete.
