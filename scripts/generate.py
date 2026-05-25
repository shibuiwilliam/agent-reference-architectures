#!/usr/bin/env python3
"""generate.py — patterns.yml + decisions.yml から機械可読成果物を冪等生成する。

生成物:
  - docs/catalog.json   … 機械可読マニフェスト
  - docs/llms.txt       … llmstxt.org 形式の索引
  - docs/llms-core.txt  … 意思決定コア（低トークン）
  - docs/llms-full.txt  … 全ページ連結プレーンテキスト
  - 各パターン .md に GEN:meta ブロック注入（Phase 2）
  - docs/decisions/by-force.md の GEN ブロック再生成（Phase 2）

マーカー: <!-- BEGIN:GEN:xxx --> 〜 <!-- END:GEN:xxx --> 間のみ置換。
人間が書いた箇所は不可侵。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PATTERNS_YML = ROOT / "patterns.yml"
DECISIONS_YML = ROOT / "decisions.yml"

SITE_URL = "https://shibuiwilliam.github.io/agent-reference-architectures"


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


# ── flat pattern list ────────────────────────────────────────────────

def flatten_patterns(pdata: dict) -> list[dict]:
    """patterns.yml → フラットなパターンリスト"""
    patterns = []
    for cat in pdata["categories"]:
        for p in cat["patterns"]:
            patterns.append({
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
            })
    return sorted(patterns, key=lambda x: x["id"])


# ── catalog.json ─────────────────────────────────────────────────────

def build_catalog(pdata: dict, ddata: dict) -> dict:
    version = pdata.get("version", ddata.get("version", "0.0.0"))
    principle = pdata["site"]["principle"]

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
        dials.append({
            "id": d["id"],
            "name": d["name"],
            "category": d["category"],
            "poles": d["poles"],
            "driver": d["driver"],
            "default": d["default"],
            "patterns": d["patterns"],
        })

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
        rules.append({
            "id": r["id"],
            "if": r["if"],
            "then_patterns": r["then_patterns"],
            "rationale": r["rationale"],
        })

    patterns = flatten_patterns(pdata)

    return {
        "version": version,
        "principle": principle,
        "forces": forces,
        "dials": dials,
        "tradeoffs": tradeoffs,
        "reference_architectures": ref_archs,
        "rules": rules,
        "patterns": patterns,
    }


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

    # Rules
    lines.append("## 決定規則（IF–THEN候補）")
    lines.append("")
    for r in ddata["rules"]:
        cond = " AND ".join(f"{k}={v}" for k, v in r["if"].items())
        pats = ", ".join(f"#{p}" for p in r["then_patterns"])
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
    """全ページ連結プレーンテキスト"""
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
        parts.append(text.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    for i in range(1, 7):
        ra_files = list((DOCS / "reference-architectures").glob(f"{i:02d}-*.md"))
        for rf in ra_files:
            text = rf.read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            parts.append(text.strip())
            parts.append("")
            parts.append("---")
            parts.append("")

    # Agent guide & proposal template (if exist)
    for extra in [DOCS / "agent-guide.md", DOCS / "agent-proposal-template.md"]:
        if extra.exists():
            text = extra.read_text(encoding="utf-8")
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
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


# ── Phase 2: by-force regeneration ───────────────────────────────────

def generate_by_force(pdata: dict, ddata: dict) -> None:
    """docs/decisions/by-force.md の GEN:by-force ブロックを再生成"""
    by_force_path = DOCS / "decisions" / "by-force.md"
    if not by_force_path.exists():
        return

    # Build force→items mapping from decisions.yml
    # Currently by-force.md is hand-written and quite good.
    # We inject a supplementary block if marker exists.
    changed = inject_gen_block(by_force_path, "by-force", "")
    # For now, by-force.md is hand-curated (already excellent).
    # Future: generate from decisions.yml rules.


# ── main ─────────────────────────────────────────────────────────────

def main() -> None:
    print("generate.py: 正本から成果物を生成中...")

    pdata = load_yaml(PATTERNS_YML)
    ddata = load_yaml(DECISIONS_YML)

    catalog = build_catalog(pdata, ddata)

    generate_catalog_json(catalog)
    generate_llms_txt(pdata, ddata)
    generate_llms_core_txt(pdata, ddata)
    generate_llms_full_txt(pdata, ddata)
    generate_meta_blocks(pdata)
    generate_by_force(pdata, ddata)

    print("generate.py: 完了")


if __name__ == "__main__":
    main()
