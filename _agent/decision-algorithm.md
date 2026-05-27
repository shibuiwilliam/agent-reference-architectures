# Decision Algorithm — Procedural Pseudocode

> This file details the decision algorithm from `_agent/README.md` as executable pseudocode.
> Data source: `_agent/decision-core.md` or `docs/catalog.json`

## Complete Algorithm

```python
def generate_proposal(requirements: str, catalog: dict) -> Proposal:
    """
    Main entry point. Takes requirements text and catalog data,
    returns a structured architecture proposal.
    """
    # Step 1: Force evaluation (done by the agent reading requirements)
    forces = evaluate_forces(requirements)
    # forces = {"F1": "high", "F2": "low", ..., "F9": "mid"}

    # Step 2: Rule matching
    required, recommended, optional = match_rules(forces, catalog["rules"])

    # Step 3: Tradeoff resolution
    tradeoff_decisions = resolve_all_tradeoffs(forces, catalog["tradeoffs"])

    # Step 4: Dial setting
    dial_values = set_all_dials(forces, catalog["dials"])

    # Step 5: Reference architecture selection
    base_arch = select_reference_architecture(forces, catalog["reference_architectures"])

    # Step 6: Compose and output
    return compose_proposal(
        forces=forces,
        required=required,
        recommended=recommended,
        optional=optional,
        tradeoffs=tradeoff_decisions,
        dials=dial_values,
        base_architecture=base_arch,
    )
```

## Step 2: Rule Matching

```python
def match_rules(forces: dict[str, str], rules: list[dict]) -> tuple[set, set, set]:
    """
    Scan all rules. If ALL conditions in a rule's `if` clause match
    the force evaluation, collect its pattern sets.
    Multiple rules can match — take the UNION of all.

    Args:
        forces: {"F1": "high", "F2": "low", ...}
        rules: catalog["rules"] — list of rule dicts

    Returns:
        (required_patterns, recommended_patterns, optional_patterns)
    """
    required = set()
    recommended = set()
    optional = set()

    for rule in rules:
        # Check if ALL conditions match
        conditions = rule["if"]  # e.g. {"F2": "high", "F1": "low"}
        if all(forces.get(k) == v for k, v in conditions.items()):
            required |= set(rule.get("required", []))
            recommended |= set(rule.get("recommended", []))
            optional |= set(rule.get("optional", []))

    return required, recommended, optional
```

## Step 3: Tradeoff Resolution

```python
def resolve_all_tradeoffs(forces: dict[str, str], tradeoffs: list[dict]) -> dict:
    """
    For each tradeoff, determine the direction: "a", "b", or "hybrid".

    Returns:
        {tradeoff_id: {"choice": "a"|"b"|"hybrid", "rationale": "..."}}
    """
    decisions = {}
    for t in tradeoffs:
        decisions[t["id"]] = resolve_one_tradeoff(t, forces)
    return decisions


def resolve_one_tradeoff(tradeoff: dict, forces: dict[str, str]) -> dict:
    """
    Resolve a single tradeoff using its decision_function.

    The decision_function contains:
      - drivers: list of force IDs that drive this decision (e.g. ["F4", "F1"])
      - logic: human-readable text describing when to choose a vs b

    Resolution strategy:
      1. Read the `drivers` force IDs
      2. Look up their values in the force evaluation
      3. Apply the `logic` text to determine direction
      4. If signals are mixed → consider "hybrid"
      5. If unclear → fall back to `tradeoff["default"]`

    Returns:
        {"choice": "a"|"b"|"hybrid", "rationale": "..."}
    """
    df = tradeoff.get("decision_function")
    if not df:
        return {"choice": "a", "rationale": f"No decision function; default to {tradeoff['a']}"}

    drivers = df["drivers"]        # e.g. ["F4", "F1"]
    logic = df.get("logic", "")    # e.g. "F4=low → sync, F4=high → async"

    driver_values = {d: forces.get(d, "mid") for d in drivers}

    # The agent should interpret `logic` text with `driver_values`
    # to determine the direction.
    #
    # Common patterns in logic text:
    #   "F4=low → a(sync), F4=high → b(async)"
    #   "F2=high → a(plan), F6=high → b(react)"
    #
    # When drivers conflict (e.g. F2=high suggests a, F6=high suggests b),
    # consider "hybrid" and explain the tension.

    # Fallback: use the default from the tradeoff definition
    default = tradeoff.get("default", "a")
    return {
        "choice": default,
        "rationale": f"Applied logic '{logic}' with drivers {driver_values}; defaulted to '{default}'",
    }
```

## Step 4: Dial Setting

```python
def set_all_dials(forces: dict[str, str], dials: list[dict]) -> dict:
    """
    For each dial, find the value_mapping entry whose condition
    matches the force evaluation. First match wins.

    Returns:
        {dial_id: {"value": ..., "unit": "...", "note": "..."}}
    """
    dial_values = {}

    for d in dials:
        matched = False
        for mapping in d.get("value_mapping", []):
            condition = mapping["condition"]  # e.g. {"F4": "low"}
            if all(forces.get(k) == v for k, v in condition.items()):
                dial_values[d["id"]] = {
                    "value": mapping.get("value") or mapping.get("range"),
                    "unit": mapping.get("unit", ""),
                    "note": mapping.get("note", ""),
                }
                matched = True
                break  # First match wins

        if not matched:
            # No condition matched; use the default
            dial_values[d["id"]] = {
                "value": d["default"],
                "unit": "",
                "note": "No condition matched; using default",
            }

    return dial_values
```

## Step 5: Reference Architecture Selection

```python
def select_reference_architecture(
    forces: dict[str, str],
    architectures: list[dict],
) -> dict | None:
    """
    Score each reference architecture by counting how many of its
    force conditions match the evaluation. Highest score wins.

    Args:
        forces: {"F1": "high", ...}
        architectures: catalog["reference_architectures"]
            Each has: id, name, forces (dict of required force values), layers

    Returns:
        The best-matching architecture dict, or None if no match
    """
    best_arch = None
    best_score = -1

    for arch in architectures:
        arch_forces = arch["forces"]  # e.g. {"F1": "high", "F2": "low", "F5": "high"}
        score = sum(
            1 for k, v in arch_forces.items()
            if forces.get(k) == v
        )
        if score > best_score:
            best_arch = arch
            best_score = score

    return best_arch
```

## Step 6: Compose Proposal

```python
def compose_proposal(
    forces: dict,
    required: set,
    recommended: set,
    optional: set,
    tradeoffs: dict,
    dials: dict,
    base_architecture: dict | None,
) -> Proposal:
    """
    Merge all decision outputs into a proposal following
    `_agent/proposal-template.md` format.

    Key rules:
    - Every pattern inclusion must cite the force(s) that drove it
    - Uncertain force evaluations go in "Unresolved Questions" (Section 9)
    - Include at least one alternative architecture in Section 8
    - Identify risks using anti-pattern awareness from pattern-cards.json
    """
    all_patterns = required | recommended
    if base_architecture:
        base_patterns = {layer["pattern"] for layer in base_architecture["layers"]}
        all_patterns |= base_patterns

    return Proposal(
        forces=forces,
        tradeoffs=tradeoffs,
        selected_patterns=sorted(all_patterns),
        required_patterns=sorted(required),
        recommended_patterns=sorted(recommended),
        optional_patterns=sorted(optional),
        dials=dials,
        base_architecture=base_architecture,
    )
```

## Notes

- **Force evaluation** (Step 1) is the most critical step. It requires understanding the domain, not just pattern-matching. When uncertain, assign "mid" and flag it in Section 9 of the proposal.
- **Rule matching** uses strict equality (`forces[k] == v`). A force value of "mid" will NOT match a rule condition of "high" or "low". This is intentional — rules trigger only for clear signals.
- **Tradeoff resolution** requires interpreting natural-language `logic` text. When in doubt, use the `default` and explain the uncertainty.
- **Dial values** from `value_mapping` are starting points. The `note` field often contains calibration guidance for production.
- **Architecture scoring** is a simple count. When two architectures tie, prefer the one whose unmatched forces are "mid" (neutral) rather than opposing.
