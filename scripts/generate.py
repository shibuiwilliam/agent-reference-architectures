#!/usr/bin/env python3
"""generate.py — patterns.yml + decisions.yml + anti-patterns.yml から機械可読成果物を冪等生成する。

生成物:
  - docs/catalog.json      … 機械可読マニフェスト（patterns をフル保持）
  - docs/llms.txt          … llmstxt.org 形式の索引
  - docs/llms-core.txt     … 意思決定コア（低トークン・エージェント可読形式）
  - docs/llms-full.txt     … 全ページ連結プレーンテキスト（エージェント可読形式）
  - docs/glossary.md       … パターン早見表（語彙集）— GEN:glossary マーカー間
  - 各ダイヤル/二者択一/F#ページ … GEN:patterns マーカー間に関与パターンを注入
  - docs/decisions/rules.md … GEN:rules マーカー間
  - docs/decisions/by-force.md … GEN:by-force マーカー間
  - docs/decisions/tuning-dials.md … GEN:tuning-dials マーカー間
  - docs/decisions/tradeoffs.md … GEN:tradeoffs マーカー間
  - docs/pattern-index.md  … GEN:pattern-index マーカー間
  - _agent/pattern-cards.json
  - _agent/decision-core.md

マーカー: <!-- BEGIN:GEN:xxx --> 〜 <!-- END:GEN:xxx --> 間のみ置換。
人間が書いた箇所は不可侵。

オプション:
  --validate  スキーマバリデーション（schemas/ が存在する場合）
  --lint      パターンページの構造検証（旧パターンページが存在する場合のみ）
"""

from __future__ import annotations

import json
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
    """MkDocs Material 記法をエージェント可読なプレーンマークダウンに変換。"""
    # 1. admonition → blockquote
    def replace_admonition(m):
        kind = m.group(1)
        title = m.group(2) or kind
        body_raw = m.group(3)
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

    # 5. GEN blocks → remove
    text = re.sub(
        r'<!-- BEGIN:GEN:\w+ -->.*?<!-- END:GEN:\w+ -->',
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
            # Full fields for decision-only structure
            for key in ("summary", "design", "primary_decision", "summary_plain"):
                if key in p:
                    entry[key] = p[key]
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

    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            for f in p.get("forces", []):
                if f in index and p["num"] not in index[f]["patterns"]:
                    index[f]["patterns"].append(p["num"])

    for d in ddata["dials"]:
        for f in d["driver"]:
            if f in index and d["id"] not in index[f]["dials"]:
                index[f]["dials"].append(d["id"])

    for t in ddata["tradeoffs"]:
        for f in t["driver"]:
            if f in index and t["id"] not in index[f]["tradeoffs"]:
                index[f]["tradeoffs"].append(t["id"])

    for ra in ddata["reference_architectures"]:
        for f in ra["forces"]:
            if f in index and ra["id"] not in index[f]["reference_architectures"]:
                index[f]["reference_architectures"].append(ra["id"])

    for r in ddata["rules"]:
        for f in r["if"]:
            if f in index and r["id"] not in index[f]["rules"]:
                index[f]["rules"].append(r["id"])

    if apdata:
        for ap in apdata.get("anti_patterns", []):
            for f in ap.get("related_forces", []):
                if f in index and ap["id"] not in index[f]["anti_patterns"]:
                    index[f]["anti_patterns"].append(ap["id"])

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


# ── pattern lookup helpers ───────────────────────────────────────────

def build_pattern_lookup(pdata: dict) -> dict[int, dict]:
    """num → pattern dict"""
    lookup = {}
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            lookup[p["num"]] = {**p, "_category": cat["id"], "_category_title": cat["title"]}
    return lookup


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

    if "architecture_selection" in ddata:
        catalog["architecture_selection"] = ddata["architecture_selection"]

    if apdata:
        catalog["anti_patterns"] = apdata.get("anti_patterns", [])

    return catalog


def generate_catalog_json(catalog: dict) -> None:
    content = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    changed = write_if_changed(DOCS / "catalog.json", content)
    if changed:
        print("  ✓ catalog.json")


# ── glossary.md (パターン早見表・語彙集) ────────────────────────────

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


def _primary_decision_link(pd: str) -> str:
    """primary_decision パスから表示用リンクテキストを生成"""
    if "tradeoffs-catalog/" in pd:
        slug = pd.split("/")[-1].replace(".md", "")
        return f"[二者択一: {slug}](decisions/tradeoffs-catalog/{slug}.md)"
    elif "dials/" in pd:
        slug = pd.split("/")[-1].replace(".md", "")
        return f"[ダイヤル: {slug}](decisions/dials/{slug}.md)"
    elif "forces/" in pd:
        slug = pd.split("/")[-1].replace(".md", "")
        return f"[フォース: {slug}](foundations/forces/{slug}.md)"
    elif "decision-flow" in pd:
        return f"[意思決定の進め方](decisions/decision-flow.md)"
    return f"[{pd}]({pd})"


def generate_glossary(pdata: dict) -> None:
    """docs/glossary.md を生成（パターン早見表・語彙集）"""
    glossary_path = DOCS / "glossary.md"

    # Build content
    lines: list[str] = []
    lines.append("---")
    lines.append('title: "パターン早見表（語彙集）"')
    lines.append("tags:")
    lines.append('  - "パターン"')
    lines.append('  - "語彙集"')
    lines.append("---")
    lines.append("")
    lines.append("# パターン早見表（語彙集）")
    lines.append("")
    lines.append("!!! abstract \"一言\"")
    lines.append("    59パターンの索引です。パターンは「意思決定の結果として現れる具体構造」であり、詳細は各意思決定ページと `catalog.json` を参照してください。")
    lines.append("")
    lines.append("<!-- BEGIN:GEN:glossary -->")
    lines.append("")

    lines.append("| # | パターン | カテゴリ | 一言要約 | フォース | 関与する決定 | 要素技術 |")
    lines.append("|---|---------|---------|---------|---------|------------|---------|")

    flat = flatten_patterns(pdata)
    for p in flat:
        cat_short = CATEGORY_SHORT.get(p["category"], p["category"])
        title_parts = p["title"].split("｜")
        short_title = title_parts[0].strip()
        forces_str = ", ".join(f"`{f}`" for f in p["forces"])
        pd = p.get("primary_decision", "")
        pd_link = _primary_decision_link(pd) if pd else "—"
        tech = ", ".join(p.get("element_tech", [])[:3])
        if len(p.get("element_tech", [])) > 3:
            tech += " …"
        tagline = p["tagline"]
        lines.append(f"| {p['id']} | **{short_title}** | {cat_short} | {tagline} | {forces_str} | {pd_link} | {tech} |")

    lines.append("")
    lines.append("<!-- END:GEN:glossary -->")
    lines.append("")

    content = "\n".join(lines)
    changed = write_if_changed(glossary_path, content)
    if changed:
        print("  ✓ glossary.md")


# ── GEN:patterns injection into decision pages ──────────────────────

def generate_dial_patterns(pdata: dict, ddata: dict) -> None:
    """各ダイヤルページに GEN:patterns ブロック（関与パターン一覧）を注入"""
    lookup = build_pattern_lookup(pdata)
    count = 0
    for d in ddata["dials"]:
        dial_id = d["id"]
        detail = d.get("detail", "")
        if not detail:
            continue
        dial_path = DOCS / "decisions" / detail
        if not dial_path.exists():
            continue

        pat_nums = d.get("patterns", [])
        if not pat_nums:
            content = "（このダイヤルに直接関与するパターンはありません）"
        else:
            lines = []
            lines.append("")
            lines.append("## 関与する具体構造")
            lines.append("")
            lines.append("| # | パターン | 向き | 不向き |")
            lines.append("|---|---------|------|--------|")
            for num in pat_nums:
                p = lookup.get(num)
                if not p:
                    continue
                title_parts = p["title"].split("｜")
                name = title_parts[0].strip()
                when = p.get("when_to_use", "—")
                when_not = p.get("when_not", [])
                if isinstance(when_not, list):
                    when_not_str = "; ".join(when_not[:2]) if when_not else "—"
                else:
                    when_not_str = when_not or "—"
                lines.append(f"| #{num} | **{name}** | {when} | {when_not_str} |")
            content = "\n".join(lines)

        if inject_gen_block(dial_path, "patterns", content):
            count += 1

    if count:
        print(f"  ✓ dial GEN:patterns: {count} files")


def generate_tradeoff_patterns(pdata: dict, ddata: dict) -> None:
    """各二者択一ページに GEN:patterns ブロックを注入"""
    lookup = build_pattern_lookup(pdata)
    count = 0
    for t in ddata["tradeoffs"]:
        detail = t.get("detail", "")
        if not detail:
            continue
        path = DOCS / "decisions" / detail
        if not path.exists():
            continue

        pat_nums = t.get("patterns", [])
        if not pat_nums:
            content = "（この二者択一に直接関与するパターンはありません）"
        else:
            lines = []
            lines.append("")
            lines.append("## 関与する具体構造")
            lines.append("")
            lines.append("| # | パターン | 向き | 不向き |")
            lines.append("|---|---------|------|--------|")
            for num in pat_nums:
                p = lookup.get(num)
                if not p:
                    continue
                title_parts = p["title"].split("｜")
                name = title_parts[0].strip()
                when = p.get("when_to_use", "—")
                when_not = p.get("when_not", [])
                if isinstance(when_not, list):
                    when_not_str = "; ".join(when_not[:2]) if when_not else "—"
                else:
                    when_not_str = when_not or "—"
                lines.append(f"| #{num} | **{name}** | {when} | {when_not_str} |")
            content = "\n".join(lines)

        if inject_gen_block(path, "patterns", content):
            count += 1

    if count:
        print(f"  ✓ tradeoff GEN:patterns: {count} files")


def generate_force_patterns(pdata: dict, ddata: dict) -> None:
    """各フォースページに GEN:patterns ブロック（そのフォースが効くパターン）を注入"""
    lookup = build_pattern_lookup(pdata)
    by_force = build_by_force_index(pdata, ddata, None)
    count = 0

    force_slugs = {
        "F1": "f1-reversibility",
        "F2": "f2-failure-cost",
        "F3": "f3-request-value",
        "F4": "f4-latency-budget",
        "F5": "f5-input-trust",
        "F6": "f6-task-variability",
        "F7": "f7-cost-sensitivity",
        "F8": "f8-accountability",
        "F9": "f9-provider-reliability",
    }

    for fid, slug in force_slugs.items():
        path = DOCS / "foundations" / "forces" / f"{slug}.md"
        if not path.exists():
            continue

        pat_nums = by_force.get(fid, {}).get("patterns", [])
        if not pat_nums:
            content = "（このフォースに関連するパターンはありません）"
        else:
            lines = []
            lines.append("")
            lines.append("## 関与する具体構造")
            lines.append("")
            lines.append("| # | パターン | 一言 | 向き |")
            lines.append("|---|---------|------|------|")
            for num in sorted(pat_nums):
                p = lookup.get(num)
                if not p:
                    continue
                title_parts = p["title"].split("｜")
                name = title_parts[0].strip()
                tagline = p.get("tagline", "")
                when = p.get("when_to_use", "—")
                lines.append(f"| #{num} | **{name}** | {tagline} | {when} |")
            content = "\n".join(lines)

        if inject_gen_block(path, "patterns", content):
            count += 1

    if count:
        print(f"  ✓ force GEN:patterns: {count} files")


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

    # Glossary (replaces old pattern listings)
    lines.append("## パターン早見表（語彙集・59 Patterns）")
    lines.append("")
    lines.append(f"- [パターン早見表]({SITE_URL}/glossary/): 全59パターンの索引（意思決定の結果として現れる具体構造）")
    lines.append("")

    flat = flatten_patterns(pdata)
    for p in flat:
        forces_str = ", ".join(p.get("forces", []))
        pd = p.get("primary_decision", "")
        if pd:
            # Link to decision page instead of pattern page
            url = f"{SITE_URL}/{pd.replace('.md', '/')}"
        else:
            url = f"{SITE_URL}/glossary/"
        lines.append(f"- [#{p['id']} {p['title']}]({url}): {p['tagline']} [{forces_str}]")
    lines.append("")

    # Reference architectures
    lines.append("## 意思決定プリセット（Reference Architectures）")
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
    lines.append("## 意思決定プリセット（6）")
    lines.append("")
    for ra in ddata["reference_architectures"]:
        forces_str = ", ".join(f"{k}={v}" for k, v in ra["forces"].items())
        layer_strs = ", ".join(f"#{l['pattern']}" for l in ra["layers"])
        lines.append(f"- **{ra['name']}** ({forces_str}): {layer_strs}")
    lines.append("")

    # Rules
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

    # Core decision files
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
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = convert_to_agent_readable(text)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    # Glossary
    glossary = DOCS / "glossary.md"
    if glossary.exists():
        text = glossary.read_text(encoding="utf-8")
        text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
        text = convert_to_agent_readable(text)
        parts.append(text.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    # Pattern data from patterns.yml (replaces reading pattern .md files)
    parts.append("# パターン詳細（59 Patterns — patterns.yml より）")
    parts.append("")
    for cat in pdata["categories"]:
        parts.append(f"## {cat['roman']}. {cat['title']}")
        parts.append("")
        parts.append(cat["summary"])
        parts.append("")
        for p in cat["patterns"]:
            parts.append(f"### #{p['num']} {p['title']}")
            parts.append("")
            parts.append(f"> {p['tagline']}")
            parts.append("")
            summary = p.get("summary", p.get("summary_plain", ""))
            if summary:
                # Clean admonition blocks from summary
                summary = re.sub(r'!!! \w+(?: "[^"]*")?\n(?:    .+\n?|\n)*', '', summary).strip()
                parts.append(summary)
                parts.append("")
            design = p.get("design", "")
            if design:
                # Replace mermaid with note
                design = re.sub(r'```mermaid\n.*?```', '[図省略]', design, flags=re.DOTALL)
                parts.append(f"**設計**: {design}")
                parts.append("")
            when = p.get("when_to_use", "")
            when_not = p.get("when_not", [])
            if isinstance(when_not, list):
                when_not_str = "; ".join(when_not)
            else:
                when_not_str = when_not
            parts.append(f"- **向き**: {when}")
            parts.append(f"- **不向き**: {when_not_str}")
            forces_str = ", ".join(p.get("forces", []))
            parts.append(f"- **フォース**: {forces_str}")
            tech = ", ".join(p.get("element_tech", []))
            parts.append(f"- **要素技術**: {tech}")
            related = ", ".join(f"#{r}" for r in p.get("related", []))
            parts.append(f"- **関連**: {related}")
            parts.append("")

    # Reference architectures
    parts.append("# 意思決定プリセット（リファレンスアーキテクチャ）")
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
            if rf.name.endswith(".en.md"):
                continue
            text = rf.read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = convert_to_agent_readable(text)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    # Agent guide & proposal template
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


# ── pattern-index (legacy, still generated if marker exists) ────────

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
        title_parts = p["title"].split("｜")
        short_title = title_parts[0].strip()
        # Link to glossary instead of pattern pages
        link = f"[{short_title}](glossary.md)"
        lines.append(f"| {p['id']} | {link} | {cat_short} | {p['tagline']} |")

    content = "\n".join(lines)
    changed = inject_gen_block(idx_path, "pattern-index", content)
    if changed:
        print("  ✓ pattern-index.md")


# ── tuning-dials / tradeoffs / by-force / rules tables ──────────────

def generate_tuning_dials_table(ddata: dict) -> None:
    """docs/decisions/tuning-dials.md の GEN:tuning-dials ブロックを再生成"""
    path = DOCS / "decisions" / "tuning-dials.md"
    if not path.exists():
        return

    DIAL_CATEGORY_DESC = {
        "実行制御": "エージェントの実行時間・リトライ・コストに関するダイヤル。システムの安定性と応答性に直結する。",
        "自律性・安全制御": "エージェントにどこまで任せるか、人間がどこで介入するかを決めるダイヤル。",
        "モデル・生成制御": "LLMの使い方とコスト配分を決めるダイヤル。",
        "メモリ・コンテキスト制御": "エージェントが参照・蓄積する情報量を決めるダイヤル。",
        "観測・記録制御": "ログ・トレース・プロンプト管理に関するダイヤル。監査・デバッグの粒度とコストのバランスを取る。",
    }

    cats: dict[str, list] = {}
    for d in ddata["dials"]:
        cat = d["category"]
        cats.setdefault(cat, []).append(d)

    lines: list[str] = []
    for cat_name, dials in cats.items():
        desc = DIAL_CATEGORY_DESC.get(cat_name, "")
        lines.append(f"### {cat_name}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")
        lines.append("| ダイヤル | 決め手 | 目安 | 詳細 |")
        lines.append("|---------|-------|------|------|")
        for d in dials:
            driver = " ".join(f"`[{f}]`" for f in d["driver"])
            detail = d.get("detail", "")
            link = f"[→]({detail})" if detail else ""
            lines.append(f"| **{d['name']}** | {driver} | {d['default']} | {link} |")
        lines.append("")

    content = "\n".join(lines).rstrip()
    changed = inject_gen_block(path, "tuning-dials", content)
    if changed:
        print("  ✓ tuning-dials.md table")


def generate_tradeoffs_table(ddata: dict) -> None:
    """docs/decisions/tradeoffs.md の GEN:tradeoffs ブロックを再生成"""
    path = DOCS / "decisions" / "tradeoffs.md"
    if not path.exists():
        return

    TRADEOFF_CATEGORY_DESC = {
        "実行モデル": "エージェントの実行方式・制御フローに関する択一。",
        "制御・知識ソース": "エージェントの振る舞いをどこで・何で制御するかの択一。",
        "検証・信頼性": "出力の検証方式とエラー時の振る舞いに関する択一。",
        "インフラ・データ": "通信・状態管理・構築方針に関する択一。",
    }

    cats: dict[str, list] = {}
    for t in ddata["tradeoffs"]:
        cat = t["category"]
        cats.setdefault(cat, []).append(t)

    lines: list[str] = []
    for cat_name, tradeoffs in cats.items():
        desc = TRADEOFF_CATEGORY_DESC.get(cat_name, "")
        lines.append(f"### {cat_name}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")
        lines.append("| 選択肢 A | 選択肢 B | 決定変数 | デフォルト | 詳細 |")
        lines.append("|----------|----------|---------|-----------|------|")
        for t in tradeoffs:
            driver = " ".join(f"`[{f}]`" for f in t["driver"])
            detail = t.get("detail", "")
            link = f"[→]({detail})" if detail else ""
            lines.append(f"| {t['a']} | {t['b']} | {driver} | {t['default']} | {link} |")
        lines.append("")

    content = "\n".join(lines).rstrip()
    changed = inject_gen_block(path, "tradeoffs", content)
    if changed:
        print("  ✓ tradeoffs.md table")


def generate_by_force(pdata: dict, ddata: dict) -> None:
    """docs/decisions/by-force.md の GEN:by-force ブロックを再生成"""
    path = DOCS / "decisions" / "by-force.md"
    if not path.exists():
        return

    lines: list[str] = []
    for f in ddata["forces"]:
        fid = f["id"]
        fname = f["name"]
        question = f["question"]
        active = f.get("active_condition", "")
        recs = f.get("recommendations", [])

        lines.append(f"## `[{fid}]` {fname} — {question}")
        lines.append("")
        lines.append(f"| 種別 | 項目 | {fid}が**{active}**とき |")
        lines.append("|------|------|" + "-" * (len(active) + 10) + "|")

        for r in recs:
            rtype = r["type"]
            if rtype == "tradeoff":
                kind = "二者択一"
            elif rtype == "dial":
                kind = "ダイヤル"
            elif rtype == "pattern":
                kind = "パターン"
                pid = r["id"]
                # Link to glossary instead of pattern pages
                r_label = r["label"]
                lines.append(f"| {kind} | {r_label} | {r['advice']} |")
                continue
            else:
                kind = rtype
            lines.append(f"| {kind} | {r['label']} | {r['advice']} |")

        low_note = f.get("low_note", "")
        if low_note:
            lines.append("")
            lines.append(low_note)

        lines.append("")
        lines.append("---")
        lines.append("")

    while lines and lines[-1].strip() in ("---", ""):
        lines.pop()

    content = "\n".join(lines)
    changed = inject_gen_block(path, "by-force", content)
    if changed:
        print("  ✓ by-force.md tables")


def generate_rules_page(pdata: dict, ddata: dict) -> None:
    """docs/decisions/rules.md の GEN:rules ブロックを再生成"""
    rules_path = DOCS / "decisions" / "rules.md"
    if not rules_path.exists():
        return

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


# ── meta block injection (kept for backward compat if pattern pages still exist) ──

def generate_meta_blocks(pdata: dict) -> None:
    """各パターン .md に GEN:meta ブロックを注入（パターンページが存在する場合のみ）"""
    count = 0
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if not md_path.exists():
                continue

            meta_lines = []
            meta_lines.append('<details markdown="1">')
            meta_lines.append(f'<summary>メタデータ（機械可読） — #{p["num"]} {p["title"]}</summary>')
            meta_lines.append("")
            meta_lines.append("| 項目 | 値 |")
            meta_lines.append("|------|-----|")
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


# ── frontmatter injection (kept for backward compat) ──────────────

def _build_frontmatter_yaml(title: str, tags: list[str], p: dict) -> str:
    lines = []
    lines.append("---")
    lines.append(f'title: "{title}"')
    lines.append("tags:")
    for tag in tags:
        lines.append(f'  - "{tag}"')
    lines.append("# ── agent-readable (generated by generate.py) ──")
    lines.append(f"pattern_id: {p['num']}")
    forces = p.get("forces", [])
    lines.append(f"forces: [{', '.join(forces)}]")
    dials = p.get("dials", [])
    lines.append(f"dials: [{', '.join(dials)}]")
    tradeoffs = p.get("tradeoffs", [])
    lines.append(f"tradeoffs: [{', '.join(tradeoffs)}]")
    when_to_use = p.get("when_to_use", "")
    lines.append(f'when_to_use: "{when_to_use}"')
    when_not = p.get("when_not", [])
    if isinstance(when_not, list):
        lines.append("when_not:")
        for wn in when_not:
            lines.append(f'  - "{wn}"')
    else:
        lines.append(f'when_not: ["{when_not}"]')
    related = p.get("related", [])
    lines.append(f"related: [{', '.join(str(r) for r in related)}]")
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
            fm_match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
            if not fm_match:
                continue
            fm_text = fm_match.group(1)
            body = text[fm_match.end():]
            try:
                fm_data = yaml.safe_load(fm_text)
            except yaml.YAMLError:
                continue
            if not isinstance(fm_data, dict):
                continue

            title = fm_data.get("title", p["title"])
            tags = fm_data.get("tags", [])
            new_fm = _build_frontmatter_yaml(title, tags, p)
            new_text = new_fm + body

            if write_if_changed(md_path, new_text):
                count += 1

    if count:
        print(f"  ✓ frontmatter updated: {count} files")


# ── _agent/pattern-cards.json ────────────────────────────────────────

def generate_pattern_cards(pdata: dict, ddata: dict, apdata: dict | None) -> None:
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
                "primary_decision": p.get("primary_decision", ""),
            }
            if "prevents_anti_patterns" in p:
                entry["prevents_anti_patterns"] = p["prevents_anti_patterns"]
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
    lines: list[str] = []
    version = pdata.get("version", "0.0.0")

    lines.append(f"# Decision Core — AI Agent Architecture Patterns v{version}")
    lines.append("")
    lines.append("> This file contains the decision-making data needed for architecture proposals.")
    lines.append("> Pattern details are in `catalog.json` and `glossary.md`.")
    lines.append("")

    # Forces
    lines.append("## Forces (F1–F9)")
    lines.append("")
    for f in ddata["forces"]:
        lines.append(f"- **{f['id']} {f['name']}**: {f['question']}")
        lines.append(f"  - high → {f['high_implies']}")
        lines.append(f"  - low → {f['low_implies']}")
    lines.append("")

    lines.append("## Dials (20)")
    lines.append("")
    lines.append("| Dial | Driver | Default |")
    lines.append("|------|--------|---------|")
    for d in ddata["dials"]:
        driver = ", ".join(d["driver"])
        lines.append(f"| {d['name']} | {driver} | {d['default']} |")
    lines.append("")

    lines.append("## Tradeoffs (16)")
    lines.append("")
    lines.append("| A | B | Driver | Default |")
    lines.append("|---|---|--------|---------|")
    for t in ddata["tradeoffs"]:
        driver = ", ".join(t["driver"])
        lines.append(f"| {t['a']} | {t['b']} | {driver} | {t['default']} |")
    lines.append("")

    lines.append("## Reference Architectures (6)")
    lines.append("")
    for ra in ddata["reference_architectures"]:
        forces_str = ", ".join(f"{k}={v}" for k, v in ra["forces"].items())
        layer_strs = ", ".join(f"#{l['pattern']}" for l in ra["layers"])
        lines.append(f"- **{ra['name']}** ({forces_str}): {layer_strs}")
    lines.append("")

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
                lines.append(f"- **Recommended**: {', '.join(f'#{p}' for p in rec)}")
            opt = r.get("optional", [])
            if opt:
                lines.append(f"- **Optional**: {', '.join(f'#{p}' for p in opt)}")
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
        dials_str = ", ".join(data["dials"]) or "—"
        lines.append(f"- **Dials**: {dials_str}")
        toffs = ", ".join(data["tradeoffs"]) or "—"
        lines.append(f"- **Tradeoffs**: {toffs}")
        aps = ", ".join(data["anti_patterns"]) or "—"
        lines.append(f"- **Anti-patterns**: {aps}")
        lines.append("")

    # Quick reference
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


# ── --lint: structural validation ────────────────────────────────────

def lint_patterns(pdata: dict) -> int:
    """全59パターンの .md ファイルの構造を検証（パターンページが存在する場合のみ）。"""
    errors = 0
    required_sections = ["## 概要", "## 設計", "## 解決する課題", "## 向き / 不向き", "## 要素技術", "## 関連パターン"]

    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            md_path = DOCS / "patterns" / cat["id"] / f"{p['num']:02d}-{p['slug']}.md"
            if not md_path.exists():
                # Pattern pages may have been removed in the restructure
                continue

            text = md_path.read_text(encoding="utf-8")
            prefix = f"#{p['num']} {p['slug']}"

            for section in required_sections:
                if section not in text:
                    print(f"  LINT WARN: {prefix}: missing '{section}'")

            if "<!-- BEGIN:GEN:meta -->" not in text:
                print(f"  LINT ERROR: {prefix}: missing GEN:meta marker")
                errors += 1

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

    apdata = None
    if ANTI_PATTERNS_YML.exists():
        apdata = load_yaml(ANTI_PATTERNS_YML)

    catalog = build_catalog(pdata, ddata, apdata)

    generate_catalog_json(catalog)
    generate_glossary(pdata)
    generate_llms_txt(pdata, ddata)
    generate_llms_core_txt(pdata, ddata)
    generate_llms_full_txt(pdata, ddata)
    generate_pattern_index(pdata)
    generate_tuning_dials_table(ddata)
    generate_tradeoffs_table(ddata)
    generate_by_force(pdata, ddata)
    generate_rules_page(pdata, ddata)

    # Decision page pattern injection
    generate_dial_patterns(pdata, ddata)
    generate_tradeoff_patterns(pdata, ddata)
    generate_force_patterns(pdata, ddata)

    # Legacy: pattern page meta blocks and frontmatter (only if pattern pages still exist)
    generate_meta_blocks(pdata)
    update_pattern_frontmatter(pdata)

    # _agent/ directory outputs
    generate_pattern_cards(pdata, ddata, apdata)
    generate_decision_core(pdata, ddata, apdata)

    print("generate.py: 完了")


if __name__ == "__main__":
    main()
