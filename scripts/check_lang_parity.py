#!/usr/bin/env python3
"""check_lang_parity.py — JP/EN カバレッジ確認スクリプト

日本語ページに対し英語（.en.md）の対応ファイルが揃っているかを検査する。

Usage:
    python scripts/check_lang_parity.py
    # 終了コード 0 = 全揃い、1 = 欠落あり
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Directories to check for EN parity
CHECK_DIRS = [
    "foundations",
    "foundations/characteristics",
    "foundations/forces",
    "decisions",
    "decisions/dials",
    "decisions/tradeoffs-catalog",
    "patterns/01-execution",
    "patterns/02-composition",
    "patterns/03-io-contract",
    "patterns/04-tools-mcp",
    "patterns/05-memory-context",
    "patterns/06-reliability",
    "patterns/07-observability",
    "patterns/08-cost-scaling",
    "patterns/09-security",
    "patterns/10-deployment",
    "patterns/11-ux",
    "patterns/12-governance",
    "reference-architectures",
    "anti-patterns",
]

# Top-level files to check
CHECK_FILES = [
    "index.md",
    "agent-guide.md",
    "agent-proposal-template.md",
    "pattern-index.md",
]


def main() -> int:
    missing: list[str] = []
    found_jp = 0
    found_en = 0

    # Check directories
    for dir_rel in CHECK_DIRS:
        dir_path = DOCS / dir_rel
        if not dir_path.exists():
            continue
        for jp_file in sorted(dir_path.glob("*.md")):
            if jp_file.name.endswith(".en.md"):
                continue
            found_jp += 1
            en_file = jp_file.with_suffix("").with_suffix(".en.md")
            if en_file.exists():
                found_en += 1
            else:
                missing.append(str(en_file.relative_to(DOCS)))

    # Check top-level files
    for f in CHECK_FILES:
        jp_file = DOCS / f
        if not jp_file.exists():
            continue
        found_jp += 1
        en_file = jp_file.with_suffix("").with_suffix(".en.md")
        if en_file.exists():
            found_en += 1
        else:
            missing.append(str(en_file.relative_to(DOCS)))

    pct = (found_en / found_jp * 100) if found_jp > 0 else 0

    print(f"check_lang_parity: JP={found_jp}, EN={found_en}, coverage={pct:.0f}%")

    if missing:
        print(f"\nMissing EN pages ({len(missing)}):")
        for m in missing[:30]:
            print(f"  {m}")
        if len(missing) > 30:
            print(f"  ... and {len(missing) - 30} more")
        return 1
    else:
        print("check_lang_parity: OK — all JP pages have EN counterparts")
        return 0


if __name__ == "__main__":
    sys.exit(main())
