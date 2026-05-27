#!/usr/bin/env python3
"""generate.py — patterns.yml + decisions.yml + anti-patterns.yml から機械可読成果物を冪等生成する。

生成物:
  - docs/catalog.json   … 機械可読マニフェスト（by_force, bidirectional_related, selection_guide, anti_patterns 含む）
  - docs/llms.txt       … llmstxt.org 形式の索引
  - docs/llms-core.txt  … 意思決定コア（低トークン・エージェント可読形式）
  - docs/llms-full.txt  … 全ページ連結プレーンテキスト（エージェント可読形式）
  - 各パターン .md に GEN:meta ブロック注入（Phase 2）
  - _agent/pattern-cards.json … パターン選定用の軽量構造化データ
  - _agent/decision-core.md   … エージェント向け意思決定コア（by_force逆引き付き）
  - 各パターン .md のフロントマターにエージェント向けフィールドを注入

マーカー: <!-- BEGIN:GEN:xxx --> 〜 <!-- END:GEN:xxx --> 間のみ置換。
人間が書いた箇所は不可侵。

オプション:
  --validate  スキーマバリデーション（schemas/ が存在する場合）
  --lint      パターンページの構造検証
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PATTERNS_YML = ROOT / "patterns.yml"
DECISIONS_YML = ROOT / "decisions.yml"
ANTI_PATTERNS_YML = ROOT / "anti-patterns.yml"

SITE_URL = "https://shibuiwilliam.github.io/agent-reference-architectures"
AGENT_DIR = ROOT / "_agent"


# ── helpers ──────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_if_changed(path: Path, content: str) -> bool:
    """冪等書き込み。変更があれば True。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def inject_gen_block(file_path: Path, tag: str, content: str) -> bool:
    """ファイル内の <!-- BEGIN:GEN:tag --> 〜 <!-- END:GEN:tag --> を置換。
    マーカーが無ければ何もしない。"""
    if not file_path.exists():
        return False
    text = file_path.read_text(encoding="utf-8")
    begin = f"<!-- BEGIN:GEN:{tag} -->"
    end = f"<!-- END:GEN:{tag} -->"
    pattern = re.compile(
        re.escape(begin) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    replacement = f"{begin}\n{content}\n{end}"
    new_text, n = pattern.subn(replacement, text)
    if n == 0:
        return False
    return write_if_changed(file_path, new_text)


# ── agent-readable markdown conversion ──────────────────────────────

def convert_to_agent_readable(text: str) -> str:
    """MkDocs Material 記法をエージェント可読なプレーンマークダウンに変換。
    パターン .md ファイル自体は変更しない。llms-full.txt / llms-core.txt 生成時のみ使用。"""

    # 1. admonition → blockquote
    def replace_admonition(m):
        kind = m.group(1)
        title = m.group(2) or kind
        body_raw = m.group(3)
        # Remove leading 4-space indent from body lines
        body_lines = []
        for line in body_raw.split("\n"):
            if line.startswith("    "):
                body_lines.append(line[4:])
            elif line.strip() == "":
                body_lines.append("")
            else:
                break
        body = " ".join(line for line in body_lines if line.strip()).strip()
        return f"> **{title}**: {body}"

    text = re.sub(
        r'!!! (\w+)(?: "([^"]*)")?\n((?:    .+\n?|\n)*)',
        replace_admonition,
        text,
    )

    # 2. <details> → expand
    text = re.sub(
        r'<details[^>]*>\s*<summary>([^<]*)</summary>\s*(.*?)\s*</details>',
        lambda m: f"**{m.group(1)}**\n{m.group(2)}",
        text,
        flags=re.DOTALL,
    )

    # 3. Mermaid → text note
    text = re.sub(
        r'```mermaid\n.*?```',
        "[図省略: Mermaid図はサイト版を参照]",
        text,
        flags=re.DOTALL,
    )

    # 4. Relative links → text reference
    text = re.sub(
        r'\[([^\]]+)\]\([^)]*\.md[^)]*\)',
        r'\1',
        text,
    )

    # 5. GEN:meta block → remove (already in catalog.json)
    text = re.sub(
        r'<!-- BEGIN:GEN:meta -->.*?<!-- END:GEN:meta -->',
        "",
        text,
        flags=re.DOTALL,
    )

    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


# ── flat pattern list ────────────────────────────────────────────────

def flatten_patterns(pdata: dict) -> list[dict]:
    """patterns.yml → フラットなパターンリスト"""
    patterns = []
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            entry = {
                "id": p["num"],
                "slug": p["slug"],
                "category": cat["id"],
                "category_title": cat["title"],
                "title": p["title"],
                "tagline": p["tagline"],
                "forces": p.get("forces", []),
                "related": p.get("related", []),
                "dials": p.get("dials", []),
                "tradeoffs": p.get("tradeoffs", []),
                "when_to_use": p.get("when_to_use", ""),
                "when_not": p.get("when_not", []),
                "element_tech": p.get("element_tech", []),
            }
            if "summary_plain" in p:
                entry["summary_plain"] = p["summary_plain"]
            if "selection_criteria" in p:
                entry["selection_criteria"] = p["selection_criteria"]
            if "prevents_anti_patterns" in p:
                entry["prevents_anti_patterns"] = p["prevents_anti_patterns"]
            patterns.append(entry)
    return sorted(patterns, key=lambda x: x["id"])


# ── by_force index ──────────────────────────────────────────────────

def build_by_force_index(pdata: dict, ddata: dict, apdata: dict | None) -> dict:
    """フォース別の逆引きインデックスを構築"""
    index: dict[str, dict[str, list]] = {}
    for fid in [f"F{i}" for i in range(1, 10)]:
        index[fid] = {
            "patterns": [],
            "dials": [],
            "tradeoffs": [],
            "reference_architectures": [],
            "rules": [],
            "anti_patterns": [],
        }

    # Patterns
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            for f in p.get("forces", []):
                if f in index and p["num"] not in index[f]["patterns"]:
                    index[f]["patterns"].append(p["num"])

    # Dials
    for d in ddata["dials"]:
        for f in d["driver"]:
            if f in index and d["id"] not in index[f]["dials"]:
                index[f]["dials"].append(d["id"])

    # Tradeoffs
    for t in ddata["tradeoffs"]:
        for f in t["driver"]:
            if f in index and t["id"] not in index[f]["tradeoffs"]:
                index[f]["tradeoffs"].append(t["id"])

    # Reference architectures
    for ra in ddata["reference_architectures"]:
        for f in ra["forces"]:
            if f in index and ra["id"] not in index[f]["reference_architectures"]:
                index[f]["reference_architectures"].append(ra["id"])

    # Rules
    for r in ddata["rules"]:
        for f in r["if"]:
            if f in index and r["id"] not in index[f]["rules"]:
                index[f]["rules"].append(r["id"])

    # Anti-patterns
    if apdata:
        for ap in apdata.get("anti_patterns", []):
            for f in ap.get("related_forces", []):
                if f in index and ap["id"] not in index[f]["anti_patterns"]:
                    index[f]["anti_patterns"].append(ap["id"])

    # Sort all lists
    for fid in index:
        index[fid]["patterns"].sort()

    return index


def build_bidirectional_related(pdata: dict) -> dict:
    """全パターンの related を走査し双方向関連を計算"""
    bidir: dict[int, set[int]] = defaultdict(set)
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            pid = p["num"]
            for r in p.get("related", []):
                bidir[pid].add(r)
                bidir[r].add(pid)
    return {str(k): sorted(v) for k, v in sorted(bidir.items())}


# ── catalog.json ─────────────────────────────────────────────────────

def build_catalog(pdata: dict, ddata: dict, apdata: dict | None) -> dict:
    version = pdata.get("version", ddata.get("version", "0.0.0"))
    principle = pdata["site"]["principle"]

    characteristics = []
    for c in ddata.get("characteristics", []):
        characteristics.append({
            "id": c["id"],
            "name": c["name"],
            "description": c["description"],
            "group": c["group"],
            "forces": c["forces"],
        })

    forces = []
    for f in ddata["forces"]:
        forces.append({
            "id": f["id"],
            "name": f["name"],
            "question": f["question"],
            "high_implies": f["high_implies"],
            "low_implies": f["low_implies"],
        })

    dials = []
    for d in ddata["dials"]:
        entry = {
            "id": d["id"],
            "name": d["name"],
            "category": d["category"],
            "poles": d["poles"],
            "driver": d["driver"],
            "default": d["default"],
            "patterns": d["patterns"],
        }
        if "value_mapping" in d:
            entry["value_mapping"] = d["value_mapping"]
        dials.append(entry)

    tradeoffs = []
    for t in ddata["tradeoffs"]:
        entry = {
            "id": t["id"],
            "name": t["name"],
            "category": t["category"],
            "a": t["a"],
            "b": t["b"],
            "driver": t["driver"],
            "default": t["default"],
            "patterns": t["patterns"],
        }
        if "hybrid" in t:
            entry["hybrid"] = t["hybrid"]
        if "decision_function" in t:
            entry["decision_function"] = t["decision_function"]
        tradeoffs.append(entry)

    ref_archs = []
    for ra in ddata["reference_architectures"]:
        ref_archs.append({
            "id": ra["id"],
            "name": ra["name"],
            "forces": ra["forces"],
            "layers": ra["layers"],
        })

    rules = []
    for r in ddata["rules"]:
        entry = {
            "id": r["id"],
            "if": r["if"],
            "rationale": r["rationale"],
        }
        # Support both old (then_patterns) and new (required/recommended/optional) format
        if "required" in r:
            entry["required"] = r["required"]
            entry["recommended"] = r.get("recommended", [])
            entry["optional"] = r.get("optional", [])
            if "escalation" in r:
                entry["escalation"] = r["escalation"]
        elif "then_patterns" in r:
            entry["then_patterns"] = r["then_patterns"]
        rules.append(entry)

    patterns = flatten_patterns(pdata)

    catalog = {
        "version": version,
        "principle": principle,
        "characteristics": characteristics,
        "forces": forces,
        "dials": dials,
        "tradeoffs": tradeoffs,
        "reference_architectures": ref_archs,
        "rules": rules,
        "patterns": patterns,
        "by_force": build_by_force_index(pdata, ddata, apdata),
        "bidirectional_related": build_bidirectional_related(pdata),
        "selection_guide": {
            "step1_evaluate_forces": {
                "input": "システム要件",
                "output": "F1-F9 の高/中/低 評価",
                "method": "各フォースの question に対して要件を照合",
            },
            "step2_match_rules": {
                "input": "フォース評価",
                "output": "required/recommended/optional パターン群",
                "method": "rules[] の if 条件をフォース評価に照合し、合致するルールの required/recommended/optional を収集",
            },
            "step3_resolve_tradeoffs": {
                "input": "フォース評価",
                "output": "各二者択一の選択方向",
                "method": "tradeoffs[] の decision_function にフォース評価を適用",
            },
            "step4_set_dials": {
                "input": "フォース評価",
                "output": "各ダイヤルの初期値",
                "method": "dials[] の value_mapping にフォース評価を適用",
            },
            "step5_compose": {
                "input": "パターン群 + 二者択一の方向",
                "output": "層構成（リファレンスアーキテクチャ + 追加パターン）",
                "method": "architecture_selection の複合条件を照合し、base + overlay を決定",
            },
        },
    }

    # Architecture selection
    if "architecture_selection" in ddata:
        catalog["architecture_selection"] = ddata["architecture_selection"]

    # Anti-patterns
    if apdata:
        catalog["anti_patterns"] = apdata.get("anti_patterns", [])

    return catalog


def generate_catalog_json(catalog: dict) -> None:
    content = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    changed = write_if_changed(DOCS / "catalog.json", content)
    if changed:
        print("  ✓ catalog.json")


# ── llms.txt ─────────────────────────────────────────────────────────

def generate_llms_txt(pdata: dict, ddata: dict) -> None:
    lines: list[str] = []
    title = pdata["site"]["title"]
    principle = pdata["site"]["principle"]
    version = pdata.get("version", "0.0.0")

    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> {principle}")
    lines.append(f"> Version: {version}")
    lines.append("")

    # Foundations
    lines.append("## 土台（Foundations）")
    lines.append("")
    lines.append(f"- [駆動変数（フォース）F1–F9]({SITE_URL}/foundations/forces/): パターンの程度と選定を決める9つの環境変数")
    lines.append(f"- [特性]({SITE_URL}/foundations/characteristics/): AIエージェントの非決定論的特性")
    lines.append("")

    # Decisions
    lines.append("## 意思決定層（Decisions）")
    lines.append("")
    lines.append(f"- [意思決定の進め方]({SITE_URL}/decisions/decision-flow/): フォース評価→二者択一→ダイヤル→パターン選定")
    lines.append(f"- [程度（チューニング）ダイヤル]({SITE_URL}/decisions/tuning-dials/): 20のパラメータとその目安値")
    lines.append(f"- [相反する仕組みの選定基準]({SITE_URL}/decisions/tradeoffs/): 16の二者択一カタログ")
    lines.append(f"- [フォース別逆引き]({SITE_URL}/decisions/by-force/): フォースから関連パターン・ダイヤル・二者択一を引く")
    lines.append(f"- [通し例]({SITE_URL}/decisions/worked-examples/): 3システムの一気通貫例")
    lines.append(f"- [パラメータ化]({SITE_URL}/decisions/parameterization/): パターンのパラメータ化の考え方")
    lines.append("")

    # Patterns by category
    lines.append("## パターン（59 Patterns）")
    lines.append("")
    for cat in pdata["categories"]:
        lines.append(f"### {cat['roman']}. {cat['title']}")
        lines.append("")
        for p in cat["patterns"]:
            url = f"{SITE_URL}/patterns/{cat['id']}/{p['num']:02d}-{p['slug']}/"
            forces_str = ", ".join(p.get("forces", []))
            lines.append(f"- [#{p['num']} {p['title']}]({url}): {p['tagline']} [{forces_str}]")
        lines.append("")

    # Reference architectures
    lines.append("## リファレンスアーキテクチャ（Reference Architectures）")
    lines.append("")
    for ra in ddata["reference_architectures"]:
        lines.append(f"- [{ra['name']}]({SITE_URL}/{ra['detail'].replace('.md', '/')}): フォース {ra['forces']}")
    lines.append("")

    # Machine-readable
    lines.append("## 機械可読データ（Machine-Readable）")
    lines.append("")
    lines.append(f"- [catalog.json]({SITE_URL}/catalog.json): 全パターン・フォース・ダイヤル・二者択一・決定規則の構造化データ")
    lines.append(f"- [エージェント利用ガイド]({SITE_URL}/agent-guide/): コーディングエージェント向け利用手順")
    lines.append(f"- [提案テンプレート]({SITE_URL}/agent-proposal-template/): アーキテクチャ提案の出力様式")
    lines.append("")

    content = "\n".join(lines) + "\n"
    changed = write_if_changed(DOCS / "llms.txt", content)
    if changed:
        print("  ✓ llms.txt")


# ── llms-core.txt ────────────────────────────────────────────────────

def generate_llms_core_txt(pdata: dict, ddata: dict) -> None:
    """意思決定コア — フォース＋ダイヤル＋二者択一＋リファレンスアーキ＋規則。低トークン。"""
    lines: list[str] = []
    version = pdata.get("version", "0.0.0")

    lines.append(f"# AIエージェント本番アーキテクチャ — 意思決定コア v{version}")
    lines.append("")
    lines.append(f"> {pdata['site']['principle']}")
    lines.append("")

    # Forces
    lines.append("## 駆動変数（フォース）F1–F9")
    lines.append("")
    for f in ddata["forces"]:
        lines.append(f"- **{f['id']} {f['name']}**: {f['question']}")
        lines.append(f"  - 高 → {f['high_implies']}")
        lines.append(f"  - 低 → {f['low_implies']}")
    lines.append("")

    # Dials summary
    lines.append("## 程度ダイヤル（20）")
    lines.append("")
    lines.append("| ダイヤル | 決め手 | 目安 |")
    lines.append("|---------|-------|------|")
    for d in ddata["dials"]:
        driver = ", ".join(d["driver"])
        lines.append(f"| {d['name']} | {driver} | {d['default']} |")
    lines.append("")

    # Tradeoffs summary
    lines.append("## 二者択一（16）")
    lines.append("")
    lines.append("| A | B | 決定変数 | デフォルト |")
    lines.append("|---|---|---------|-----------|")
    for t in ddata["tradeoffs"]:
        driver = ", ".join(t["driver"])
        lines.append(f"| {t['a']} | {t['b']} | {driver} | {t['default']} |")
    lines.append("")

    # Reference Architectures
    lines.append("## リファレンスアーキテクチャ（6）")
    lines.append("")
    for ra in ddata["reference_architectures"]:
        forces_str = ", ".join(f"{k}={v}" for k, v in ra["forces"].items())
        layer_strs = ", ".join(f"#{l['pattern']}" for l in ra["layers"])
        lines.append(f"- **{ra['name']}** ({forces_str}): {layer_strs}")
    lines.append("")

    # Rules (new format with required/recommended/optional)
    lines.append("## 決定規則（IF–THEN候補）")
    lines.append("")
    for r in ddata["rules"]:
        cond = " AND ".join(f"{k}={v}" for k, v in r["if"].items())
        if "required" in r:
            req = ", ".join(f"#{p}" for p in r["required"])
            rec = ", ".join(f"#{p}" for p in r.get("recommended", []))
            opt = ", ".join(f"#{p}" for p in r.get("optional", []))
            lines.append(f"- IF {cond}")
            lines.append(f"  必須: {req}")
            if rec:
                lines.append(f"  推奨: {rec}")
            if opt:
                lines.append(f"  任意: {opt}")
        else:
            pats = ", ".join(f"#{p}" for p in r.get("then_patterns", []))
            lines.append(f"- IF {cond} → {pats}")
        lines.append(f"  理由: {r['rationale']}")
    lines.append("")

    # Quick pattern reference
    lines.append("## パターン早見表（59）")
    lines.append("")
    lines.append("| # | パターン | フォース | 一言 |")
    lines.append("|---|---------|---------|------|")
    flat = flatten_patterns(pdata)
    for p in flat:
        forces_str = ", ".join(p["forces"])
        lines.append(f"| {p['id']} | {p['title']} | {forces_str} | {p['tagline']} |")
    lines.append("")

    content = "\n".join(lines) + "\n"
    changed = write_if_changed(DOCS / "llms-core.txt", content)
    if changed:
        print("  ✓ llms-core.txt")


# ── llms-full.txt ────────────────────────────────────────────────────

def generate_llms_full_txt(pdata: dict, ddata: dict) -> None:
    """全ページ連結プレーンテキスト（エージェント可読形式）"""
    parts: list[str] = []
    version = pdata.get("version", "0.0.0")

    parts.append(f"# AIエージェント本番アーキテクチャ・パターン v{version}")
    parts.append("")
    parts.append(f"> {pdata['site']['principle']}")
    parts.append("")

    # Core files to include
    core_files = [
        DOCS / "foundations" / "forces.md",
        DOCS / "foundations" / "characteristics.md",
        DOCS / "decisions" / "decision-flow.md",
        DOCS / "decisions" / "tuning-dials.md",
        DOCS / "decisions" / "tradeoffs.md",
        DOCS / "decisions" / "by-force.md",
        DOCS / "decisions" / "worked-examples.md",
        DOCS / "decisions" / "parameterization.md",
        DOCS / "decisions" / "interactions.md",
        DOCS / "decisions" / "adr-template.md",
    ]

    for f in core_files:
        if f.exists():
            text = f.read_text(encoding="utf-8")
            # Strip YAML frontmatter
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = convert_to_agent_readable(text)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    # All patterns
    for cat in pdata["categories"]:
        parts.append(f"# {cat['roman']}. {cat['title']}")
        parts.append("")
        parts.append(cat["summary"])
        parts.append("")
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if md_path.exists():
                text = md_path.read_text(encoding="utf-8")
                text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
                text = convert_to_agent_readable(text)
                parts.append(text.strip())
                parts.append("")
                parts.append("---")
                parts.append("")

    # Reference architectures
    parts.append("# リファレンスアーキテクチャ")
    parts.append("")
    ra_index = DOCS / "reference-architectures" / "index.md"
    if ra_index.exists():
        text = ra_index.read_text(encoding="utf-8")
        text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
        text = convert_to_agent_readable(text)
        parts.append(text.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    for i in range(1, 7):
        ra_files = list((DOCS / "reference-architectures").glob(f"{i:02d}-*.md"))
        for rf in ra_files:
            text = rf.read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = convert_to_agent_readable(text)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    # Agent guide & proposal template (if exist)
    for extra in [DOCS / "agent-guide.md", DOCS / "agent-proposal-template.md"]:
        if extra.exists():
            text = extra.read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = convert_to_agent_readable(text)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    content = "\n".join(parts) + "\n"
    changed = write_if_changed(DOCS / "llms-full.txt", content)
    if changed:
        print("  ✓ llms-full.txt")


# ── Phase 2: meta block injection ────────────────────────────────────

def generate_meta_blocks(pdata: dict) -> None:
    """各パターン .md に GEN:meta ブロックを注入"""
    count = 0
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if not md_path.exists():
                continue

            # Build meta content
            meta_lines = []
            meta_lines.append('<details markdown="1">')
            meta_lines.append(f'<summary>メタデータ（機械可読） — #{p["num"]} {p["title"]}</summary>')
            meta_lines.append("")
            meta_lines.append(f"| 項目 | 値 |")
            meta_lines.append(f"|------|-----|")
            meta_lines.append(f"| **ID** | {p['num']} |")
            meta_lines.append(f"| **カテゴリ** | {cat['id']} — {cat['title']} |")
            forces_str = ", ".join(f"`[{f}]`" for f in p.get("forces", []))
            meta_lines.append(f"| **フォース** | {forces_str} |")
            dials_str = ", ".join(p.get("dials", [])) or "—"
            meta_lines.append(f"| **ダイヤル** | {dials_str} |")
            tradeoffs_str = ", ".join(p.get("tradeoffs", [])) or "—"
            meta_lines.append(f"| **二者択一** | {tradeoffs_str} |")
            related_str = ", ".join(f"#{r}" for r in p.get("related", [])) or "—"
            meta_lines.append(f"| **関連パターン** | {related_str} |")
            when_use = p.get("when_to_use", "")
            meta_lines.append(f"| **向き** | {when_use} |")
            when_not = p.get("when_not", [])
            if isinstance(when_not, list):
                when_not_str = "; ".join(when_not) if when_not else "—"
            else:
                when_not_str = when_not or "—"
            meta_lines.append(f"| **不向き** | {when_not_str} |")
            tech_str = ", ".join(p.get("element_tech", [])) or "—"
            meta_lines.append(f"| **要素技術** | {tech_str} |")
            meta_lines.append("")
            meta_lines.append("</details>")

            meta_content = "\n".join(meta_lines)

            changed = inject_gen_block(md_path, "meta", meta_content)
            if changed:
                count += 1

    if count:
        print(f"  ✓ meta blocks injected: {count} files")


# ── Phase 2: pattern-index generation ────────────────────────────────

CATEGORY_SHORT = {
    "01-execution": "I. 実行",
    "02-composition": "II. 構成",
    "03-io-contract": "III. 契約",
    "04-tools-mcp": "IV. ツール",
    "05-memory-context": "V. メモリ",
    "06-reliability": "VI. 信頼性",
    "07-observability": "VII. 観測",
    "08-cost-scaling": "VIII. コスト",
    "09-security": "IX. セキュリティ",
    "10-deployment": "X. デプロイ",
    "11-ux": "XI. UX",
    "12-governance": "XII. ガバナンス",
}


def generate_pattern_index(pdata: dict) -> None:
    """docs/pattern-index.md の GEN:pattern-index ブロックを再生成"""
    idx_path = DOCS / "pattern-index.md"
    if not idx_path.exists():
        return

    lines = []
    lines.append("| # | パターン | カテゴリ | 一言 |")
    lines.append("|---|---------|---------|------|")

    flat = flatten_patterns(pdata)
    for p in flat:
        cat_short = CATEGORY_SHORT.get(p["category"], p["category"])
        # Extract short English name from title (before ｜)
        title_parts = p["title"].split("｜")
        short_title = title_parts[0].strip()
        link = f"[{short_title}](patterns/{p['category']}/{p['id']:02d}-{p['slug']}.md)"
        lines.append(f"| {p['id']} | {link} | {cat_short} | {p['tagline']} |")

    content = "\n".join(lines)
    changed = inject_gen_block(idx_path, "pattern-index", content)
    if changed:
        print("  ✓ pattern-index.md")


# ── Phase 2: by-force regeneration ───────────────────────────────────

def generate_by_force(pdata: dict, ddata: dict) -> None:
    """docs/decisions/by-force.md の GEN:by-force ブロックを再生成"""
    # by-force.md is hand-curated and excellent. No marker-based generation.
    pass


def generate_rules_page(pdata: dict, ddata: dict) -> None:
    """docs/decisions/rules.md の GEN:rules ブロックを再生成"""
    rules_path = DOCS / "decisions" / "rules.md"
    if not rules_path.exists():
        return

    # Build pattern title lookup
    ptitles: dict[int, str] = {}
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            title_parts = p["title"].split("｜")
            ptitles[p["num"]] = title_parts[0].strip()

    lines: list[str] = []
    for r in ddata["rules"]:
        cond = " AND ".join(f"`{k}`={v}" for k, v in r["if"].items())
        lines.append(f"### {r['id']}")
        lines.append("")
        lines.append(f"**条件**: {cond}")
        lines.append("")

        def fmt_pats(pids: list[int]) -> str:
            return ", ".join(f"#{p} {ptitles.get(p, '')}" for p in pids)

        lines.append(f"- **必須**: {fmt_pats(r['required'])}")
        rec = r.get("recommended", [])
        if rec:
            lines.append(f"- **推奨**: {fmt_pats(rec)}")
        opt = r.get("optional", [])
        if opt:
            lines.append(f"- **任意**: {fmt_pats(opt)}")
        lines.append(f"- **根拠**: {r['rationale']}")
        if "escalation" in r:
            lines.append(f"- **昇格条件**: {r['escalation']}")
        lines.append("")

    content = "\n".join(lines)
    changed = inject_gen_block(rules_path, "rules", content)
    if changed:
        print("  ✓ decisions/rules.md")


# ── _agent/pattern-cards.json ────────────────────────────────────────

def generate_pattern_cards(pdata: dict, ddata: dict, apdata: dict | None) -> None:
    """_agent/pattern-cards.json — パターン選定用の軽量構造化データ"""
    version = pdata.get("version", "0.0.0")

    patterns = []
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            entry = {
                "id": p["num"],
                "slug": p["slug"],
                "title": p["title"],
                "category": cat["id"],
                "forces": p.get("forces", []),
                "when_to_use": p.get("when_to_use", ""),
                "when_not": p.get("when_not", []),
                "dials": p.get("dials", []),
                "tradeoffs": p.get("tradeoffs", []),
                "related": p.get("related", []),
                "detail_path": f"docs/patterns/{cat['id']}/{p['num']:02d}-{p['slug']}.md",
            }
            if "prevents_anti_patterns" in p:
                entry["prevents_anti_patterns"] = p["prevents_anti_patterns"]
            # selection_criteria is in catalog.json; omitted here for size
            patterns.append(entry)

    patterns.sort(key=lambda x: x["id"])

    cards = {
        "version": version,
        "patterns": patterns,
        "by_force": build_by_force_index(pdata, ddata, apdata),
    }

    content = json.dumps(cards, ensure_ascii=False, separators=(", ", ": ")) + "\n"
    changed = write_if_changed(AGENT_DIR / "pattern-cards.json", content)
    if changed:
        print("  ✓ _agent/pattern-cards.json")


# ── _agent/decision-core.md ─────────────────────────────────────────

def generate_decision_core(pdata: dict, ddata: dict, apdata: dict | None) -> None:
    """_agent/decision-core.md — エージェント向け意思決定コア（by_force逆引き付き）"""
    lines: list[str] = []
    version = pdata.get("version", "0.0.0")

    lines.append(f"# Decision Core — AI Agent Architecture Patterns v{version}")
    lines.append("")
    lines.append("> This file contains the decision-making data needed for architecture proposals.")
    lines.append("> Read `_agent/README.md` first for the algorithm overview.")
    lines.append("> After narrowing pattern candidates, get details from `_agent/pattern-cards.json` or individual `docs/patterns/**/*.md` files.")
    lines.append("")

    # Forces
    lines.append("## Forces (F1–F9)")
    lines.append("")
    for f in ddata["forces"]:
        lines.append(f"- **{f['id']} {f['name']}**: {f['question']}")
        lines.append(f"  - high → {f['high_implies']}")
        lines.append(f"  - low → {f['low_implies']}")
    lines.append("")

    # Dials summary
    lines.append("## Dials (20)")
    lines.append("")
    lines.append("| Dial | Driver | Default |")
    lines.append("|------|--------|---------|")
    for d in ddata["dials"]:
        driver = ", ".join(d["driver"])
        lines.append(f"| {d['name']} | {driver} | {d['default']} |")
    lines.append("")

    # Tradeoffs summary
    lines.append("## Tradeoffs (16)")
    lines.append("")
    lines.append("| A | B | Driver | Default |")
    lines.append("|---|---|--------|---------|")
    for t in ddata["tradeoffs"]:
        driver = ", ".join(t["driver"])
        lines.append(f"| {t['a']} | {t['b']} | {driver} | {t['default']} |")
    lines.append("")

    # Reference Architectures
    lines.append("## Reference Architectures (6)")
    lines.append("")
    for ra in ddata["reference_architectures"]:
        forces_str = ", ".join(f"{k}={v}" for k, v in ra["forces"].items())
        layer_strs = ", ".join(f"#{l['pattern']}" for l in ra["layers"])
        lines.append(f"- **{ra['name']}** ({forces_str}): {layer_strs}")
    lines.append("")

    # Rules (structured format)
    lines.append("## Decision Rules")
    lines.append("")
    for r in ddata["rules"]:
        lines.append(f"### Rule {r['id']}")
        cond = " AND ".join(f"{k}={v}" for k, v in r["if"].items())
        lines.append(f"- **IF**: {cond}")
        if "required" in r:
            req = ", ".join(f"#{p}" for p in r["required"])
            lines.append(f"- **Required**: {req}")
            rec = r.get("recommended", [])
            if rec:
                rec_str = ", ".join(f"#{p}" for p in rec)
                lines.append(f"- **Recommended**: {rec_str}")
            opt = r.get("optional", [])
            if opt:
                opt_str = ", ".join(f"#{p}" for p in opt)
                lines.append(f"- **Optional**: {opt_str}")
        else:
            pats = ", ".join(f"#{p}" for p in r.get("then_patterns", []))
            lines.append(f"- **Patterns**: {pats}")
        lines.append(f"- **Rationale**: {r['rationale']}")
        lines.append("")

    # by_force index
    by_force = build_by_force_index(pdata, ddata, apdata)
    lines.append("## by_force Index")
    lines.append("")
    for fid in [f"F{i}" for i in range(1, 10)]:
        fname = next((f["name"] for f in ddata["forces"] if f["id"] == fid), "")
        data = by_force[fid]
        lines.append(f"### {fid} {fname}")
        pats = ", ".join(f"#{p}" for p in data["patterns"]) or "—"
        lines.append(f"- **Patterns**: {pats}")
        dials = ", ".join(data["dials"]) or "—"
        lines.append(f"- **Dials**: {dials}")
        toffs = ", ".join(data["tradeoffs"]) or "—"
        lines.append(f"- **Tradeoffs**: {toffs}")
        aps = ", ".join(data["anti_patterns"]) or "—"
        lines.append(f"- **Anti-patterns**: {aps}")
        lines.append("")

    # Quick pattern reference
    lines.append("## Pattern Quick Reference (59)")
    lines.append("")
    lines.append("| # | Pattern | Forces | Tagline |")
    lines.append("|---|---------|--------|---------|")
    flat = flatten_patterns(pdata)
    for p in flat:
        forces_str = ", ".join(p["forces"])
        lines.append(f"| {p['id']} | {p['title']} | {forces_str} | {p['tagline']} |")
    lines.append("")

    content = "\n".join(lines) + "\n"
    changed = write_if_changed(AGENT_DIR / "decision-core.md", content)
    if changed:
        print("  ✓ _agent/decision-core.md")


# ── frontmatter injection ───────────────────────────────────────────

def _build_frontmatter_yaml(title: str, tags: list[str], p: dict) -> str:
    """パターンのフロントマターYAMLテキストを構築する。"""
    lines = []
    lines.append("---")

    # title (preserve original quoting)
    lines.append(f'title: "{title}"')

    # tags
    lines.append("tags:")
    for tag in tags:
        lines.append(f'  - "{tag}"')

    # agent-readable section
    lines.append("# ── agent-readable (generated by generate.py) ──")
    lines.append(f"pattern_id: {p['num']}")

    # forces
    forces = p.get("forces", [])
    lines.append(f"forces: [{', '.join(forces)}]")

    # dials
    dials = p.get("dials", [])
    lines.append(f"dials: [{', '.join(dials)}]")

    # tradeoffs
    tradeoffs = p.get("tradeoffs", [])
    lines.append(f"tradeoffs: [{', '.join(tradeoffs)}]")

    # when_to_use
    when_to_use = p.get("when_to_use", "")
    lines.append(f'when_to_use: "{when_to_use}"')

    # when_not
    when_not = p.get("when_not", [])
    if isinstance(when_not, list):
        lines.append(f"when_not:")
        for wn in when_not:
            lines.append(f'  - "{wn}"')
    else:
        lines.append(f'when_not: ["{when_not}"]')

    # related
    related = p.get("related", [])
    lines.append(f"related: [{', '.join(str(r) for r in related)}]")

    # prevents_anti_patterns
    paps = p.get("prevents_anti_patterns", [])
    if paps:
        lines.append(f"prevents_anti_patterns: [{', '.join(paps)}]")

    lines.append("---")
    return "\n".join(lines) + "\n"


def update_pattern_frontmatter(pdata: dict) -> None:
    """各パターン .md のYAMLフロントマターにエージェント向けフィールドを注入する。"""
    count = 0
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if not md_path.exists():
                continue

            text = md_path.read_text(encoding="utf-8")

            # Extract existing frontmatter
            fm_match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
            if not fm_match:
                continue

            fm_text = fm_match.group(1)
            body = text[fm_match.end():]

            # Parse existing frontmatter to get title and tags
            try:
                fm_data = yaml.safe_load(fm_text)
            except yaml.YAMLError:
                continue

            if not isinstance(fm_data, dict):
                continue

            title = fm_data.get("title", p["title"])
            tags = fm_data.get("tags", [])

            # Build new frontmatter
            new_fm = _build_frontmatter_yaml(title, tags, p)
            new_text = new_fm + body

            if write_if_changed(md_path, new_text):
                count += 1

    if count:
        print(f"  ✓ frontmatter updated: {count} files")


# ── --lint: structural validation ────────────────────────────────────

def lint_patterns(pdata: dict) -> int:
    """全59パターンの .md ファイルの構造を検証。エラー数を返す。"""
    errors = 0
    required_sections = ["## 概要", "## 設計", "## 解決する課題", "## 向き / 不向き", "## 要素技術", "## 関連パターン"]

    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if not md_path.exists():
                print(f"  LINT ERROR: {md_path} does not exist")
                errors += 1
                continue

            text = md_path.read_text(encoding="utf-8")
            prefix = f"#{p['num']} {p['slug']}"

            # 1. Required sections
            for section in required_sections:
                if section not in text:
                    print(f"  LINT WARN: {prefix}: missing '{section}'")

            # 2. GEN:meta marker
            if "<!-- BEGIN:GEN:meta -->" not in text:
                print(f"  LINT ERROR: {prefix}: missing GEN:meta marker")
                errors += 1

            # 3. Related pattern links validity
            related_section = re.search(r'## 関連パターン\n(.*?)(?=\n## |\Z)', text, re.DOTALL)
            if related_section:
                links = re.findall(r'\]\(([^)]+\.md)', related_section.group(1))
                for link in links:
                    link_path = md_path.parent / link
                    if not link_path.exists():
                        print(f"  LINT ERROR: {prefix}: broken link '{link}'")
                        errors += 1

    return errors


# ── --validate: schema validation ────────────────────────────────────

def validate_schemas() -> int:
    """JSON Schema でバリデーション（schemas/ が存在する場合のみ）"""
    schemas_dir = ROOT / "schemas"
    if not schemas_dir.exists():
        print("  schemas/ not found, skipping validation")
        return 0

    try:
        import jsonschema
    except ImportError:
        print("  jsonschema not installed, skipping validation")
        return 0

    errors = 0

    schema_targets = [
        ("patterns.schema.json", PATTERNS_YML, "patterns.yml"),
        ("decisions.schema.json", DECISIONS_YML, "decisions.yml"),
    ]

    for schema_file, target_file, target_name in schema_targets:
        schema_path = schemas_dir / schema_file
        if not schema_path.exists():
            continue
        with open(schema_path) as f:
            schema = json.load(f)
        data = load_yaml(target_file)
        try:
            jsonschema.validate(data, schema)
            print(f"  ✓ {target_name} validates against {schema_file}")
        except jsonschema.ValidationError as e:
            print(f"  VALIDATE ERROR: {target_name}: {e.message}")
            errors += 1

    # catalog.json schema
    catalog_schema_path = schemas_dir / "catalog.schema.json"
    if catalog_schema_path.exists():
        with open(catalog_schema_path) as f:
            schema = json.load(f)
        catalog_path = DOCS / "catalog.json"
        if catalog_path.exists():
            with open(catalog_path) as f:
                data = json.load(f)
            try:
                jsonschema.validate(data, schema)
                print(f"  ✓ catalog.json validates against catalog.schema.json")
            except jsonschema.ValidationError as e:
                print(f"  VALIDATE ERROR: catalog.json: {e.message}")
                errors += 1

    return errors


# ── main ─────────────────────────────────────────────────────────────

def main() -> None:
    do_lint = "--lint" in sys.argv
    do_validate = "--validate" in sys.argv

    if do_lint:
        print("generate.py: パターンページの構造検証中...")
        pdata = load_yaml(PATTERNS_YML)
        errors = lint_patterns(pdata)
        if errors:
            print(f"generate.py: {errors} エラー検出")
            sys.exit(1)
        else:
            print("generate.py: 構造検証 OK")
        return

    if do_validate:
        print("generate.py: スキーマバリデーション中...")
        errors = validate_schemas()
        if errors:
            print(f"generate.py: {errors} バリデーションエラー")
            sys.exit(1)
        else:
            print("generate.py: バリデーション OK")
        return

    print("generate.py: 正本から成果物を生成中...")

    pdata = load_yaml(PATTERNS_YML)
    ddata = load_yaml(DECISIONS_YML)

    # Load anti-patterns if available
    apdata = None
    if ANTI_PATTERNS_YML.exists():
        apdata = load_yaml(ANTI_PATTERNS_YML)

    catalog = build_catalog(pdata, ddata, apdata)

    generate_catalog_json(catalog)
    generate_llms_txt(pdata, ddata)
    generate_llms_core_txt(pdata, ddata)
    generate_llms_full_txt(pdata, ddata)
    generate_meta_blocks(pdata)
    generate_pattern_index(pdata)
    generate_by_force(pdata, ddata)
    generate_rules_page(pdata, ddata)

    # _agent/ directory outputs
    generate_pattern_cards(pdata, ddata, apdata)
    generate_decision_core(pdata, ddata, apdata)
    update_pattern_frontmatter(pdata)

    print("generate.py: 完了")


if __name__ == "__main__":
    main()
