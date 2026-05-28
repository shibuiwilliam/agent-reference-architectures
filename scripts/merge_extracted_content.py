#!/usr/bin/env python3
"""Merge extracted summary/design/primary_decision into patterns.yml.

Reads _workspace/extracted_content.yml and updates patterns.yml in-place,
adding summary, design, and primary_decision fields to each pattern.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PATTERNS_YML = ROOT / "patterns.yml"
EXTRACTED = ROOT / "_workspace" / "extracted_content.yml"


def main():
    with open(PATTERNS_YML, encoding="utf-8") as f:
        pdata = yaml.safe_load(f)

    with open(EXTRACTED, encoding="utf-8") as f:
        extracted = yaml.safe_load(f)

    updated = 0
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            num = p["num"]
            if num not in extracted:
                print(f"WARNING: Pattern {num} not in extracted data", file=sys.stderr)
                continue

            ext = extracted[num]

            # Clean up summary: remove admonition blocks (意思決定上の位置づけ)
            summary = ext.get("summary", "")
            # Remove !!! info blocks
            summary = re.sub(
                r'!!! \w+(?: "[^"]*")?\n(?:    .+\n?|\n)*',
                '', summary
            ).strip()

            p["summary"] = summary
            p["design"] = ext.get("design", "")
            p["primary_decision"] = ext.get("primary_decision", "")
            updated += 1

    # Write back
    with open(PATTERNS_YML, "w", encoding="utf-8") as f:
        yaml.dump(pdata, f, allow_unicode=True, default_flow_style=False,
                  width=200, sort_keys=False)

    print(f"Updated {updated} patterns in patterns.yml")


if __name__ == "__main__":
    main()
