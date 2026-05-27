---
title: Decision Rules (IF–THEN)
---

# Decision Rules (IF–THEN Candidate Presentation)

!!! abstract "TL;DR"
    IF–THEN rules that narrow down pattern candidates based on force evaluation. Final selection is left to force evaluation and human judgment.

## Purpose

These rules are used in Step 2 "Rule Matching" of the [decision flow](decision-flow.md). They are generated from the `rules[]` section of `decisions.yml`.

Each rule maps "force combination → required/recommended/optional pattern candidates." These are **candidate suggestions**, not mandates. For how forces interact in practice, see the [worked examples](worked-examples.md).

---

## Rules

<!-- BEGIN:GEN:rules -->
<!-- END:GEN:rules -->

---

## How to Use

1. Evaluate [forces](../foundations/forces.md) as high/medium/low
2. Collect **all** matching rules (multiple rules can match simultaneously)
3. Include **required** patterns in your candidate set
4. Consider **recommended** patterns based on force combinations
5. Check **optional** patterns against escalation conditions
6. Complete the design with [tradeoffs](tradeoffs.md) and [dials](tuning-dials.md)

!!! warning "Candidates, Not Mandates"
    Rules narrow down "patterns to consider first." They do not automatically determine adoption. Final decisions are made by humans.

## Related Pages

- [Decision Flow](decision-flow.md)
- [Reverse Lookup by Force](by-force.md)
- [Worked Examples](worked-examples.md)
- [Architecture Proposal Template](../agent-proposal-template.md)
