#!/usr/bin/env python3
"""check_redirects.py — Verify all 59 pattern pages + 12 category indexes have redirects."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MKDOCS_YML = ROOT / "mkdocs.yml"
PATTERNS_YML = ROOT / "patterns.yml"


def main():
    with open(PATTERNS_YML, encoding="utf-8") as f:
        pdata = yaml.safe_load(f)

    # Parse redirect_maps from mkdocs.yml (can't use safe_load due to Python tags)
    import re
    text = MKDOCS_YML.read_text(encoding="utf-8")
    redirect_maps = {}
    in_redirects = False
    for line in text.split("\n"):
        if "redirect_maps:" in line:
            in_redirects = True
            continue
        if in_redirects:
            m = re.match(r'\s+"([^"]+)":\s+"([^"]+)"', line)
            if m:
                redirect_maps[m.group(1)] = m.group(2)
            elif line.strip() and not line.startswith(" " * 6):
                in_redirects = False

    if not redirect_maps:
        print("ERROR: No redirect_maps found in mkdocs.yml")
        sys.exit(1)

    errors = []
    expected = []

    # All 59 patterns
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            old_path = f"patterns/{cat['id']}/{p['num']:02d}-{p['slug']}.md"
            expected.append((old_path, f"#{p['num']} {p['slug']}"))
        # Category index
        idx_path = f"patterns/{cat['id']}/index.md"
        expected.append((idx_path, f"{cat['id']}/index"))

    # pattern-index
    expected.append(("pattern-index.md", "pattern-index"))

    for old_path, label in expected:
        if old_path not in redirect_maps:
            errors.append(f"  MISSING: {label} ({old_path})")
        else:
            target = redirect_maps[old_path]
            # Check target file exists
            target_path = ROOT / "docs" / target
            if not target_path.exists():
                errors.append(f"  BROKEN TARGET: {label} → {target} (file not found)")

    if errors:
        print(f"check_redirects: FAILED — {len(errors)} errors:")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print(f"check_redirects: ALL GREEN — {len(expected)} redirects verified ({len([e for e in expected if 'index' not in e[1]])} patterns + {len([e for e in expected if 'index' in e[1]])} indexes)")
        sys.exit(0)


if __name__ == "__main__":
    main()
