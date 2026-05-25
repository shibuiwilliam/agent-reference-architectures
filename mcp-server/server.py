#!/usr/bin/env python3
"""MCP Server for Agent Reference Architectures catalog.

Reads catalog.json and exposes tools for coding agents to query
patterns, forces, dials, tradeoffs, and get recommendations.

Usage:
    # stdio transport (for Claude Code, Cursor, etc.)
    python mcp-server/server.py

    # Or via uv
    uv run python mcp/server.py

Requires: mcp[cli] (pip install "mcp[cli]")
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── Load catalog ─────────────────────────────────────────────────────

CATALOG_PATH = Path(__file__).resolve().parent.parent / "docs" / "catalog.json"

if not CATALOG_PATH.exists():
    raise FileNotFoundError(
        f"catalog.json not found at {CATALOG_PATH}. "
        "Run 'python scripts/generate.py' first."
    )

with open(CATALOG_PATH, encoding="utf-8") as f:
    CATALOG: dict = json.load(f)

# Index patterns by id for fast lookup
_PATTERNS_BY_ID: dict[int, dict] = {p["id"]: p for p in CATALOG["patterns"]}
_PATTERNS_BY_SLUG: dict[str, dict] = {p["slug"]: p for p in CATALOG["patterns"]}

# ── MCP Server ───────────────────────────────────────────────────────

mcp = FastMCP(
    "agent-reference-architectures",
    version=CATALOG.get("version", "0.0.0"),
)


@mcp.tool()
def search_patterns(query: str) -> str:
    """キーワードでパターンを検索する。タイトル・tagline・要素技術・フォースにマッチするパターンを返す。

    Args:
        query: 検索キーワード（例: "キャッシュ", "セキュリティ", "F2"）
    """
    query_lower = query.lower()
    results = []
    for p in CATALOG["patterns"]:
        searchable = " ".join([
            p["title"].lower(),
            p["tagline"].lower(),
            p.get("when_to_use", "").lower(),
            " ".join(p.get("forces", [])).lower(),
            " ".join(p.get("element_tech", [])).lower(),
            p["category"].lower(),
        ])
        if query_lower in searchable:
            results.append({
                "id": p["id"],
                "title": p["title"],
                "tagline": p["tagline"],
                "forces": p["forces"],
                "category": p["category"],
            })

    if not results:
        return json.dumps({"message": f"'{query}' に一致するパターンはありません。", "count": 0}, ensure_ascii=False)

    return json.dumps({"count": len(results), "patterns": results}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_pattern(pattern_id: int) -> str:
    """パターンIDで詳細を取得する。

    Args:
        pattern_id: パターン番号（1–59）
    """
    p = _PATTERNS_BY_ID.get(pattern_id)
    if not p:
        return json.dumps({"error": f"パターン #{pattern_id} は存在しません。有効範囲: 1–59"}, ensure_ascii=False)
    return json.dumps(p, ensure_ascii=False, indent=2)


@mcp.tool()
def recommend(force_profile: dict[str, str]) -> str:
    """フォース評価プロファイルから推奨パターンと構成を返す。

    catalog.json の rules を評価し、条件に合致するパターンを推奨する。

    Args:
        force_profile: フォース評価（例: {"F2": "high", "F1": "low"}）。
                       値は "high", "medium", "low" のいずれか。
    """
    matched_rules = []
    recommended_pattern_ids: set[int] = set()

    for rule in CATALOG["rules"]:
        match = True
        for force_id, required_value in rule["if"].items():
            profile_value = force_profile.get(force_id, "").lower()
            if profile_value != required_value.lower():
                match = False
                break
        if match:
            matched_rules.append(rule)
            recommended_pattern_ids.update(rule["then_patterns"])

    # Also check reference architectures
    matching_archs = []
    for ra in CATALOG["reference_architectures"]:
        ra_match = True
        for force_id, required_value in ra["forces"].items():
            profile_value = force_profile.get(force_id, "").lower()
            if profile_value and profile_value != required_value.lower():
                ra_match = False
                break
        if ra_match:
            matching_archs.append({
                "id": ra["id"],
                "name": ra["name"],
                "forces": ra["forces"],
                "layers": ra["layers"],
            })

    patterns = []
    for pid in sorted(recommended_pattern_ids):
        p = _PATTERNS_BY_ID.get(pid)
        if p:
            patterns.append({
                "id": p["id"],
                "title": p["title"],
                "tagline": p["tagline"],
                "forces": p["forces"],
            })

    return json.dumps({
        "force_profile": force_profile,
        "matched_rules": matched_rules,
        "recommended_patterns": patterns,
        "matching_reference_architectures": matching_archs,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def list_reference_architectures() -> str:
    """6つのリファレンスアーキテクチャ（複合構成）の一覧を返す。"""
    archs = []
    for ra in CATALOG["reference_architectures"]:
        archs.append({
            "id": ra["id"],
            "name": ra["name"],
            "forces": ra["forces"],
            "layers": ra["layers"],
        })
    return json.dumps({"reference_architectures": archs}, ensure_ascii=False, indent=2)


@mcp.tool()
def get_decision(decision_type: str, decision_id: str) -> str:
    """ダイヤルまたは二者択一の詳細を取得する。

    Args:
        decision_type: "dial" または "tradeoff"
        decision_id: ダイヤル/二者択一のID（例: "timeout", "sync-vs-async"）
    """
    if decision_type == "dial":
        for d in CATALOG["dials"]:
            if d["id"] == decision_id:
                return json.dumps(d, ensure_ascii=False, indent=2)
        return json.dumps({"error": f"ダイヤル '{decision_id}' は存在しません。"}, ensure_ascii=False)

    elif decision_type == "tradeoff":
        for t in CATALOG["tradeoffs"]:
            if t["id"] == decision_id:
                return json.dumps(t, ensure_ascii=False, indent=2)
        return json.dumps({"error": f"二者択一 '{decision_id}' は存在しません。"}, ensure_ascii=False)

    else:
        return json.dumps({"error": f"decision_type は 'dial' または 'tradeoff' を指定してください。"}, ensure_ascii=False)


@mcp.tool()
def get_forces() -> str:
    """9つの駆動変数（フォース F1–F9）の一覧と説明を返す。"""
    return json.dumps({
        "forces": CATALOG["forces"],
        "version": CATALOG["version"],
        "principle": CATALOG["principle"],
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
