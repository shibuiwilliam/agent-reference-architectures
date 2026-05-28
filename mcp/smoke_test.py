#!/usr/bin/env python3
"""Smoke test for the MCP server.

Validates that catalog.json loads correctly and all tools return valid JSON.
Does NOT require the MCP server to be running — tests the functions directly.

Usage:
    python -m smoke_test       (from mcp/ directory)
    python mcp/smoke_test.py   (from project root)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add mcp/ to path so we can import server
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import the catalog data directly (avoid starting the MCP server)
CATALOG_PATH = Path(__file__).resolve().parent.parent / "docs" / "catalog.json"


def main() -> int:
    errors = 0

    # 1. catalog.json exists and loads
    if not CATALOG_PATH.exists():
        print(f"FAIL: catalog.json not found at {CATALOG_PATH}")
        return 1

    with open(CATALOG_PATH, encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"  ✓ catalog.json loaded (version={catalog.get('version')})")

    # 2. Required keys present
    required_keys = {"version", "principle", "characteristics", "forces", "dials",
                     "tradeoffs", "reference_architectures", "rules", "patterns"}
    missing = required_keys - set(catalog)
    if missing:
        print(f"FAIL: catalog.json missing keys: {missing}")
        errors += 1
    else:
        print(f"  ✓ All required keys present")

    # 3. 59 patterns
    if len(catalog.get("patterns", [])) != 59:
        print(f"FAIL: expected 59 patterns, got {len(catalog.get('patterns', []))}")
        errors += 1
    else:
        print(f"  ✓ 59 patterns")

    # 4. 9 characteristics
    if len(catalog.get("characteristics", [])) != 9:
        print(f"FAIL: expected 9 characteristics, got {len(catalog.get('characteristics', []))}")
        errors += 1
    else:
        print(f"  ✓ 9 characteristics")

    # 5. 9 forces
    if len(catalog.get("forces", [])) != 9:
        print(f"FAIL: expected 9 forces, got {len(catalog.get('forces', []))}")
        errors += 1
    else:
        print(f"  ✓ 9 forces")

    # 6. 20 dials
    if len(catalog.get("dials", [])) != 20:
        print(f"FAIL: expected 20 dials, got {len(catalog.get('dials', []))}")
        errors += 1
    else:
        print(f"  ✓ 20 dials")

    # 7. 16 tradeoffs
    if len(catalog.get("tradeoffs", [])) != 16:
        print(f"FAIL: expected 16 tradeoffs, got {len(catalog.get('tradeoffs', []))}")
        errors += 1
    else:
        print(f"  ✓ 16 tradeoffs")

    # 8. 6 reference architectures
    if len(catalog.get("reference_architectures", [])) != 6:
        print(f"FAIL: expected 6 reference architectures, got {len(catalog.get('reference_architectures', []))}")
        errors += 1
    else:
        print(f"  ✓ 6 reference architectures")

    # 9. Rules present
    if not catalog.get("rules"):
        print(f"FAIL: no rules found")
        errors += 1
    else:
        print(f"  ✓ {len(catalog['rules'])} rules")

    # 10. Test search (import server module functions)
    try:
        from server import search_patterns, get_pattern, recommend, list_reference_architectures, get_decision, get_forces

        # search_patterns
        result = json.loads(search_patterns("キャッシュ"))
        assert result["count"] > 0, "search should find cache-related patterns"
        print(f"  ✓ search_patterns('キャッシュ') → {result['count']} results")

        # get_pattern
        result = json.loads(get_pattern(1))
        assert result["id"] == 1, "get_pattern(1) should return pattern #1"
        print(f"  ✓ get_pattern(1) → #{result['id']} {result['title']}")

        # recommend
        result = json.loads(recommend({"F2": "high", "F1": "low"}))
        assert len(result["matched_rules"]) > 0, "should match at least one rule"
        assert len(result["required_patterns"]) > 0, "should have required patterns"
        print(f"  ✓ recommend(F2=high, F1=low) → {len(result['matched_rules'])} rules, {len(result['required_patterns'])} required patterns")

        # list_reference_architectures
        result = json.loads(list_reference_architectures())
        assert len(result["reference_architectures"]) == 6
        print(f"  ✓ list_reference_architectures() → 6 architectures")

        # get_decision
        result = json.loads(get_decision("dial", "timeout"))
        assert result["id"] == "timeout"
        print(f"  ✓ get_decision('dial', 'timeout') → {result['name']}")

        result = json.loads(get_decision("tradeoff", "sync-vs-async"))
        assert result["id"] == "sync-vs-async"
        print(f"  ✓ get_decision('tradeoff', 'sync-vs-async') → {result['name']}")

        # get_forces
        result = json.loads(get_forces())
        assert len(result["forces"]) == 9
        print(f"  ✓ get_forces() → 9 forces")

    except ImportError:
        print("  SKIP: MCP server import failed (mcp package not installed)")
        print("  Catalog validation passed without tool function tests")

    if errors:
        print(f"\nsmoke_test: {errors} error(s)")
        return 1
    else:
        print(f"\nsmoke_test: ALL PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
