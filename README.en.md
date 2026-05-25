# AI Agent Production Architecture Patterns

A collection of architecture patterns for integrating AI agents into production systems.  
**Centered on decision-making (forces, degrees, tradeoffs)**, this resource explains the design intent, when to use / when not to use, element technologies, and tuning considerations for 12 categories and 59 patterns.

> **Core Principle:** Surround a probabilistic core with a deterministic shell — contracts, verification, budgets, permissions, observability. The dial settings of the shell are determined by context (forces).

## Site

<https://shibuiwilliam.github.io/agent-reference-architectures/>

## Structure

| Section | Content |
|---------|---------|
| **Decisions (Backbone)** | Forces (F1–F9) → Degrees (20 dials) → Tradeoffs (16 binary choices) → Composite configurations → Records |
| **Patterns (Vocabulary)** | 12 categories, 59 patterns |
| **Composite Configurations** | Reference architectures, anti-patterns |

### Pattern Categories

| # | Category | Pattern Count |
|---|---------|-----------|
| I | Execution, Sessions & Orchestration | 10 |
| II | Agent Composition & Division of Labor | 5 |
| III | I/O & Contract Enforcement | 4 |
| IV | Tools, MCP & External System Integration | 6 |
| V | Memory & Context Management | 4 |
| VI | Reliability, Verification, Guardrails & Autonomy | 6 |
| VII | Observability, Audit & Evaluation | 6 |
| VIII | Cost, Performance & Scaling | 5 |
| IX | Security & Multi-Tenancy | 4 |
| X | Deployment, Vendor Abstraction & Migration | 4 |
| XI | UI/UX & Human Collaboration | 3 |
| XII | Organization, Governance & Lifecycle | 2 |

## Technology Stack

| Role | Choice |
|------|------|
| Static site generator | [MkDocs](https://www.mkdocs.org/) |
| Theme | [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) |
| Diagrams | Mermaid |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
| Package management | [uv](https://docs.astral.sh/uv/) |

## Local Development

```bash
# Install dependencies
uv sync

# Local preview (http://127.0.0.1:8000)
uv run mkdocs serve

# Build under production conditions (fails on broken links, etc.)
uv run mkdocs build --strict
```

## Deployment

Pushing to the `main` branch automatically triggers GitHub Actions, which deploys to GitHub Pages.

## License

MIT
