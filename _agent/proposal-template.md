# Architecture Proposal Template

> For human-readable explanation of each section, see `docs/agent-proposal-template.md`.
> Fill in all `{...}` placeholders. Use "N/A" for sections that don't apply — never leave blank.

## Architecture Proposal

**Date**: {YYYY-MM-DD}
**Target System**: {system name and brief description}

### 1. Requirements Summary
<!-- Summarize the system's purpose, user base, scale, and key constraints in 2–5 sentences. -->

{requirements}

### 2. Force Evaluation
<!-- For each force, assign high/mid/low and state WHY. -->

| Force | Rating | Rationale |
|-------|--------|-----------|
| F1 Reversibility | {high/mid/low} | {why} |
| F2 Failure Cost | {high/mid/low} | {why} |
| F3 Request Value | {high/mid/low} | {why} |
| F4 Latency Budget | {high/mid/low} | {why} |
| F5 Input Trust | {high/mid/low} | {why} |
| F6 Task Variability | {high/mid/low} | {why} |
| F7 Cost Sensitivity | {high/mid/low} | {why} |
| F8 Accountability | {high/mid/low} | {why} |
| F9 Provider Reliability | {high/mid/low} | {why} |

### 3. Tradeoff Decisions
<!-- For each relevant tradeoff, state the choice and the force that drove it. -->

| Tradeoff | Choice | Driving Force | Why not the other side |
|----------|--------|---------------|----------------------|
| {A ↔ B} | {A or B or hybrid} | {F#} | {reason} |

### 4. Selected Patterns
<!-- List all patterns with the force-based reason for inclusion. -->

| # | Pattern | Reason (driving force) |
|---|---------|----------------------|
| {N} | {pattern name} | {why, citing F#} |

### 5. Dial Settings
<!-- Initial values from value_mapping, with adjustment guidance. -->

| Dial | Initial Value | Driving Force | Adjustment Policy |
|------|--------------|---------------|-------------------|
| {dial name} | {value + unit} | {F#: rating} | {how to tune in production} |

### 6. Composite Architecture
<!-- Name the base reference architecture and describe the composition. -->

**Base**: {reference architecture name, or "custom"}

{architecture diagram in mermaid (optional)}

{Brief description of each layer and which patterns it maps to}

### 7. Risks and Mitigations
<!-- Identify risks, link to anti-patterns where applicable. -->

| Risk | Related Anti-Pattern | Mitigation |
|------|---------------------|------------|
| {risk} | {ap-NN name, if any} | {mitigation strategy} |

### 8. Alternatives
<!-- At least one alternative architecture considered. -->

| Alternative | Advantages | Why Not Chosen |
|-------------|-----------|----------------|
| {alternative} | {its strengths} | {why main proposal is better} |

### 9. Unresolved Questions
<!-- Flag uncertainties for human review. -->

- [ ] {question or uncertain evaluation}
- [ ] {question or uncertain evaluation}
