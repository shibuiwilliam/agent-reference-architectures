---
title: Architecture Proposal Template
---

# Architecture Proposal Template

!!! abstract "Summary"
    A standard format for coding agents to output architecture proposals. Can also serve as a human-facing ADR (Architecture Decision Record).

## Purpose of the Template

This template provides a **unified format** for coding agents to output architecture proposals based on this catalog. It is designed so that humans can easily compare and approve proposals, with rationale (relevant forces, patterns, and dials) clearly stated.

When used directly by humans, it can double as an [Architecture Decision Record (ADR)](decisions/adr-template.md).

---

## Template

Copy and use the following. Replace `{...}` with specific content.

````markdown
## Architecture Proposal

**Date**: {YYYY-MM-DD}
**Target System**: {System name and overview}

### 1. Requirements and Constraints Summary

{Summarize the system's purpose, user base, scale, and key constraints in 2--5 sentences}

### 2. Force Evaluation

| Force | Rating | Rationale |
|-------|--------|-----------|
| F1 Reversibility | {High/Med/Low} | {Why this rating} |
| F2 Failure Cost | {High/Med/Low} | {Why this rating} |
| F3 Request Value | {High/Med/Low} | {Why this rating} |
| F4 Latency Budget | {High/Med/Low} | {Why this rating} |
| F5 Input Trust | {High/Med/Low} | {Why this rating} |
| F6 Task Variability | {High/Med/Low} | {Why this rating} |
| F7 Cost Sensitivity | {High/Med/Low} | {Why this rating} |
| F8 Accountability | {High/Med/Low} | {Why this rating} |
| F9 Provider Reliability | {High/Med/Low} | {Why this rating} |

### 3. Resolved Tradeoffs

| Tradeoff | Choice | Driving Force | Reason for Rejection |
|----------|--------|---------------|----------------------|
| {A vs. B} | {A or B} | {F#} | {Why the other side was not chosen} |

### 4. Adopted Patterns

| # | Pattern | Adoption Rationale (Driving Forces) |
|---|---------|-------------------------------------|
| {N} | {Pattern Name} | {Why this pattern is needed; which forces drive it} |

### 5. Dial Settings

| Dial | Initial Value | Rationale (Force) | Tuning Strategy |
|------|---------------|-------------------|-----------------|
| {Dial Name} | {Value} | {F#: Rating} | {How to adjust in production} |

### 6. Composite Architecture

**Base Architecture**: {Reference architecture name, or custom composition}

{Architecture diagram (mermaid recommended)}

{Brief description of each layer's role and its corresponding adopted patterns}

### 7. Risks and Mitigations

| Risk | Related Anti-Pattern | Mitigation |
|------|---------------------|------------|
| {Risk} | {Anti-pattern name (if applicable)} | {Mitigation} |

### 8. Alternatives

| Alternative Architecture | Advantages | Reason for Rejection |
|--------------------------|------------|----------------------|
| {Alternative} | {Advantages of this option} | {Why the main proposal was chosen} |

### 9. Unresolved Issues

{Items requiring human confirmation, additional information needs, uncertain force evaluations}

- [ ] {Issue 1}
- [ ] {Issue 2}
````

---

## Usage Tips

1. **Fill all sections**: If not applicable, write "N/A." Do not leave sections blank
2. **Ground rationale in forces**: Cite `[F#]` evaluation values as rationale, not "just because"
3. **Do not hide uncertainty**: If you lack confidence in a force evaluation, state it in Section 9
4. **Show alternatives**: Demonstrate that you considered other architectures beyond the main proposal. This enables humans to make comparative judgments
5. **Cite stable IDs**: Always cite pattern `#N`, force `[F#]`, dial names, and tradeoff names

---

## Related Pages

- [Coding Agent Guide](agent-guide.md) -- Detailed design procedure
- [Worked Examples](decisions/worked-examples.md) -- End-to-end examples for 3 systems (similar to filled-in versions of this template)
- [Architecture Decision Record (ADR)](decisions/adr-template.md) -- Simplified version for human use
- [Reverse Lookup by Force](decisions/by-force.md) -- Look up patterns from forces
