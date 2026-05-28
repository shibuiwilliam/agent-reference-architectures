#!/usr/bin/env python3
"""Extract summary and design sections from all 59 pattern .md files.

Outputs a YAML fragment that can be merged into patterns.yml to add
summary, design, and primary_decision fields to each pattern.
"""

import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PATTERNS_YML = ROOT / "patterns.yml"
DECISIONS_YML = ROOT / "decisions.yml"


def extract_section(text: str, heading: str) -> str:
    """Extract content under a ## heading until the next ## or end."""
    pattern = re.compile(
        rf'^## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)',
        re.DOTALL | re.MULTILINE
    )
    m = pattern.search(text)
    if not m:
        return ""
    content = m.group(1).strip()
    # Remove GEN:meta blocks
    content = re.sub(
        r'<!-- BEGIN:GEN:meta -->.*?<!-- END:GEN:meta -->',
        '', content, flags=re.DOTALL
    ).strip()
    return content


def determine_primary_decision(p: dict) -> str:
    """Determine the primary decision page for redirect.

    Priority: first tradeoff > first dial > first force page.
    Returns a relative URL path from site root.
    """
    tradeoffs = p.get("tradeoffs", [])
    if tradeoffs:
        return f"decisions/tradeoffs-catalog/{tradeoffs[0]}.md"

    dials = p.get("dials", [])
    if dials:
        return f"decisions/dials/{dials[0]}.md"

    forces = p.get("forces", [])
    if forces:
        fid = forces[0].lower()
        # Map force ID to slug
        force_slugs = {
            "f1": "f1-reversibility",
            "f2": "f2-failure-cost",
            "f3": "f3-request-value",
            "f4": "f4-latency-budget",
            "f5": "f5-input-trust",
            "f6": "f6-task-variability",
            "f7": "f7-cost-sensitivity",
            "f8": "f8-accountability",
            "f9": "f9-provider-reliability",
        }
        slug = force_slugs.get(fid, fid)
        return f"foundations/forces/{slug}.md"

    return "decisions/decision-flow.md"


def main():
    with open(PATTERNS_YML, encoding="utf-8") as f:
        pdata = yaml.safe_load(f)

    results = {}
    missing = []

    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            num = p["num"]
            slug = p["slug"]
            md_path = DOCS / "patterns" / cat["id"] / f"{num:02d}-{slug}.md"

            if not md_path.exists():
                missing.append(num)
                continue

            text = md_path.read_text(encoding="utf-8")

            # Extract sections
            summary = extract_section(text, "概要")
            design = extract_section(text, "設計")

            # Clean up mermaid blocks for design - keep as-is for YAML
            # but truncate very long design sections
            if len(design) > 1500:
                # Keep first paragraph + mermaid if present
                parts = design.split("\n\n")
                kept = []
                total = 0
                for part in parts:
                    if total + len(part) > 1200 and kept:
                        break
                    kept.append(part)
                    total += len(part)
                design = "\n\n".join(kept)

            primary_decision = determine_primary_decision(p)

            results[num] = {
                "summary": summary,
                "design": design,
                "primary_decision": primary_decision,
            }

    if missing:
        print(f"WARNING: Missing pattern files: {missing}", file=sys.stderr)

    # Output as YAML
    print(yaml.dump(results, allow_unicode=True, default_flow_style=False, width=200))

    # Also output stats
    print(f"\n# Stats: {len(results)} patterns processed", file=sys.stderr)
    empty_summary = [n for n, r in results.items() if not r["summary"]]
    empty_design = [n for n, r in results.items() if not r["design"]]
    if empty_summary:
        print(f"# Empty summary: {empty_summary}", file=sys.stderr)
    if empty_design:
        print(f"# Empty design: {empty_design}", file=sys.stderr)


if __name__ == "__main__":
    main()
