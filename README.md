# AI Agent Production Architecture Patterns

A catalog of architecture patterns for embedding AI agents into production systems.  
Centered on **decision-making (forces, dials, and tradeoffs)**, it covers 12 categories and 59 patterns — design intent, when to use / when not to use, implementation technologies, and tuning guidance.

> **Core principle:** Wrap a probabilistic core in a deterministic shell — contracts, verification, budgets, permissions, observability. Calibrate the shell's dials by context (forces).

## Site

<https://shibuiwilliam.github.io/agent-reference-architectures/>

## Structure

| Section | Contents |
|---------|----------|
| **Decisions (backbone)** | Forces (F1–F9) → Dials (20) → Tradeoffs (16) → Composition → Record |
| **Patterns (vocabulary)** | 12 categories, 59 patterns |
| **Composite** | Reference architectures, anti-patterns |

### Pattern Categories

| # | Category | Patterns |
|---|----------|----------|
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

| Role | Choice |
|------|--------|
| Static site generator | [MkDocs](https://www.mkdocs.org/) |
| Theme | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| Diagrams | Mermaid |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| Package manager | [uv](https://docs.astral.sh/uv/) |

## Local Development

```bash
# Install dependencies
uv sync

# Local preview (http://127.0.0.1:8000)
uv run mkdocs serve

# Production build (fails on broken links etc.)
uv run mkdocs build --strict
```

## Deployment

Pushing to the `main` branch triggers GitHub Actions, which automatically deploys to GitHub Pages.

## License

MIT
