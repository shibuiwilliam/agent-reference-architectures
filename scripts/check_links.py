#!/usr/bin/env python3
"""check_links.py — 双方向リンク整合監査スクリプト

ダイヤル/二者択一の「関連パターン」と各パターンの「調整/選定」が
相互に指し合っているかを検査する。

Usage:
    python scripts/check_links.py
    # 終了コード 0 = 整合、1 = 不整合あり
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PATTERNS_YML = ROOT / "patterns.yml"
DECISIONS_YML = ROOT / "decisions.yml"


def main() -> int:
    pdata = yaml.safe_load(PATTERNS_YML.read_text(encoding="utf-8"))
    ddata = yaml.safe_load(DECISIONS_YML.read_text(encoding="utf-8"))

    errors = 0

    # Build pattern → dials/tradeoffs from patterns.yml
    pattern_dials: dict[int, list[str]] = {}
    pattern_tradeoffs: dict[int, list[str]] = {}
    pattern_related: dict[int, list[int]] = {}

    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            pid = p["num"]
            pattern_dials[pid] = p.get("dials", [])
            pattern_tradeoffs[pid] = p.get("tradeoffs", [])
            pattern_related[pid] = p.get("related", [])

    # Check: dial.patterns ↔ pattern.dials
    for d in ddata["dials"]:
        did = d["id"]
        for pid in d["patterns"]:
            if did not in pattern_dials.get(pid, []):
                print(f"  LINK ERROR: dial '{did}' lists pattern #{pid}, but #{pid} does not list dial '{did}'")
                errors += 1

    for pid, dials in pattern_dials.items():
        for did in dials:
            dial_pats = []
            for d in ddata["dials"]:
                if d["id"] == did:
                    dial_pats = d["patterns"]
                    break
            if pid not in dial_pats:
                print(f"  LINK ERROR: pattern #{pid} lists dial '{did}', but dial '{did}' does not list #{pid}")
                errors += 1

    # Check: tradeoff.patterns ↔ pattern.tradeoffs
    for t in ddata["tradeoffs"]:
        tid = t["id"]
        for pid in t["patterns"]:
            if tid not in pattern_tradeoffs.get(pid, []):
                print(f"  LINK ERROR: tradeoff '{tid}' lists pattern #{pid}, but #{pid} does not list tradeoff '{tid}'")
                errors += 1

    for pid, tradeoffs in pattern_tradeoffs.items():
        for tid in tradeoffs:
            tradeoff_pats = []
            for t in ddata["tradeoffs"]:
                if t["id"] == tid:
                    tradeoff_pats = t["patterns"]
                    break
            if pid not in tradeoff_pats:
                print(f"  LINK ERROR: pattern #{pid} lists tradeoff '{tid}', but tradeoff '{tid}' does not list #{pid}")
                errors += 1

    # Check: bidirectional related
    for pid, related in pattern_related.items():
        for rid in related:
            if rid not in pattern_related:
                print(f"  LINK WARN: pattern #{pid} lists related #{rid}, but #{rid} does not exist in patterns.yml")
                errors += 1

    if errors:
        print(f"\ncheck_links: {errors} error(s) found")
        return 1
    else:
        print("check_links: OK — all bidirectional links are consistent")
        return 0


if __name__ == "__main__":
    sys.exit(main())
