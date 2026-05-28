#!/usr/bin/env python3
"""check_migration.py — Safety gate: verify all 59 patterns are fully migrated.

Checks:
1. patterns.yml has summary/design/when_to_use/when_not/element_tech/related/primary_decision non-empty
2. primary_decision redirect target is defined
3. Pattern is referenced from at least one decision page (dial/tradeoff/force/by-force)

Exit code 0 = all green, 1 = failures found.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PATTERNS_YML = ROOT / "patterns.yml"

REQUIRED_FIELDS = [
    "summary", "design", "when_to_use", "when_not",
    "element_tech", "related", "primary_decision",
]


def load_patterns():
    with open(PATTERNS_YML, encoding="utf-8") as f:
        pdata = yaml.safe_load(f)
    patterns = []
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            patterns.append(p)
    return patterns


def check_fields(patterns):
    """Check that all required fields are non-empty."""
    errors = []
    for p in patterns:
        for field in REQUIRED_FIELDS:
            val = p.get(field)
            if not val:
                errors.append(f"  #{p['num']} {p['slug']}: missing or empty '{field}'")
    return errors


def check_redirect_targets(patterns):
    """Check that each pattern has a valid primary_decision path."""
    errors = []
    for p in patterns:
        pd = p.get("primary_decision", "")
        if not pd:
            errors.append(f"  #{p['num']} {p['slug']}: no primary_decision defined")
            continue
        # Check that the target file exists
        target = DOCS / pd
        if not target.exists():
            errors.append(f"  #{p['num']} {p['slug']}: redirect target '{pd}' does not exist")
    return errors


def check_decision_references(patterns):
    """Check that each pattern is referenced from at least one decision page."""
    decision_dirs = [
        DOCS / "decisions" / "dials",
        DOCS / "decisions" / "tradeoffs-catalog",
        DOCS / "foundations" / "forces",
        DOCS / "foundations" / "characteristics",
    ]
    decision_files = [
        DOCS / "decisions" / "by-force.md",
        DOCS / "decisions" / "rules.md",
        DOCS / "decisions" / "tuning-dials.md",
        DOCS / "decisions" / "tradeoffs.md",
    ]

    # Collect all decision page text
    all_text = ""
    for d in decision_dirs:
        if d.exists():
            for f in d.glob("*.md"):
                all_text += f.read_text(encoding="utf-8")
    for f in decision_files:
        if f.exists():
            all_text += f.read_text(encoding="utf-8")

    errors = []
    for p in patterns:
        # Check for #N reference in any decision page
        ref = f"#{p['num']} "
        ref2 = f"#{p['num']}]"
        ref3 = f"#{p['num']},"
        ref4 = f"#{p['num']}\n"
        ref5 = f"#{p['num']}|"
        if not any(r in all_text for r in [ref, ref2, ref3, ref4, ref5]):
            errors.append(f"  #{p['num']} {p['slug']}: not referenced from any decision page")
    return errors


def main():
    patterns = load_patterns()
    assert len(patterns) == 59, f"Expected 59 patterns, got {len(patterns)}"

    all_errors = []

    print("check_migration: Checking required fields...")
    errs = check_fields(patterns)
    all_errors.extend(errs)
    if errs:
        print(f"  ✗ {len(errs)} field errors")
    else:
        print("  ✓ All fields present")

    print("check_migration: Checking redirect targets...")
    errs = check_redirect_targets(patterns)
    all_errors.extend(errs)
    if errs:
        print(f"  ✗ {len(errs)} redirect errors")
    else:
        print("  ✓ All redirect targets valid")

    print("check_migration: Checking decision page references...")
    errs = check_decision_references(patterns)
    all_errors.extend(errs)
    if errs:
        print(f"  ✗ {len(errs)} reference errors")
    else:
        print("  ✓ All patterns referenced from decisions")

    if all_errors:
        print(f"\ncheck_migration: FAILED — {len(all_errors)} errors:")
        for e in all_errors:
            print(e)
        sys.exit(1)
    else:
        print(f"\ncheck_migration: ALL GREEN — 59/59 patterns fully migrated")
        sys.exit(0)


if __name__ == "__main__":
    main()
