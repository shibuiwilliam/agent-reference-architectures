# AI Agent Production Architecture Patterns

"The demo worked great — then production happened."

This catalog collects **59 architecture patterns** for taking AI agents from prototype to production. It's organized around **decision-making** — not just _what_ to build, but _how to choose_ what to build, using forces (context), dials (tuning), and tradeoffs (binary design choices).

> **Core principle:** Wrap the probabilistic core in a deterministic shell — contracts, verification, budgets, permissions, observability — and tune the shell's settings based on your context.

## Live Site

<https://shibuiwilliam.github.io/agent-reference-architectures/>

## What's Inside

| Layer | What it covers |
|-------|---------------|
| **Decisions** (the backbone) | 9 forces → 20 tuning dials → 16 tradeoffs → composition → decision record |
| **Patterns** (the vocabulary) | 59 patterns across 12 categories |
| **Composites** | 6 reference architectures + 11 anti-patterns |

### The 12 Categories

| # | Category | Count |
|---|----------|-------|
| I | Execution, Session & Orchestration | 10 |
| II | Agent Composition & Delegation | 5 |
| III | I/O & Contract | 4 |
| IV | Tools, MCP & External System Integration | 6 |
| V | Memory & Context Management | 4 |
| VI | Reliability, Verification, Guardrails & Autonomy | 6 |
| VII | Observability, Audit & Evaluation | 6 |
| VIII | Cost, Performance & Scaling | 5 |
| IX | Security & Multi-Tenancy | 4 |
| X | Deployment, Vendor Abstraction & Migration | 4 |
| XI | UI/UX & Human Collaboration | 3 |
| XII | Organization, Governance & Lifecycle | 2 |

## Tech Stack

| Role | Tool |
|------|------|
| Static site generator | [MkDocs](https://www.mkdocs.org/) |
| Theme | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| Diagrams | Mermaid |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| Package manager | [uv](https://docs.astral.sh/uv/) |

## Getting Started

```bash
uv sync                        # Install dependencies
uv run mkdocs serve            # Preview at http://127.0.0.1:8000
uv run mkdocs build --strict   # Production build (catches broken links)
```

## Deployment

Push to `main` and GitHub Actions handles the rest — it builds and deploys to GitHub Pages automatically.

## License

MIT
