#!/usr/bin/env python3
"""パターンの frontmatter スキーマ・統制語彙・id重複・相対リンク切れを検証する。
CIで mkdocs build の前に実行する。エラーがあれば終了コード1。
依存は標準ライブラリのみ（YAMLは簡易パーサで読む）。
"""
import sys, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERNS = ROOT / "docs" / "patterns"

FORCES = {f"F{i}" for i in range(1, 18)}
DRIVING = {
    "reversibility", "failure_cost", "request_value", "latency_budget",
    "input_trust", "task_variability", "cost_sensitivity", "accountability",
    "provider_trust",
}
STATUS = {"draft", "review", "stable"}
REQUIRED = ["id", "slug", "title", "domain", "status", "summary",
            "forces", "driving_variables", "related_patterns"]

errors = []

def parse_frontmatter(text, path):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{path}: frontmatter が見つからない")
        return {}
    fm, key = {}, None
    for raw in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_]+:", raw):
            key, _, val = raw.partition(":")
            key, val = key.strip(), val.strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            elif val == "":
                fm[key] = []   # block list が続く想定
            else:
                fm[key] = val.strip('"')
        elif raw.strip().startswith("- ") and key:
            if not isinstance(fm.get(key), list):
                fm[key] = []
            fm[key].append(raw.strip()[2:].strip().strip('"'))
    return fm

def main():
    md_files = [p for p in PATTERNS.rglob("*.md")
                if p.name not in ("index.md", "_template.md")]
    seen_ids = {}
    all_slugs = {p.stem for p in md_files}
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, p)
        for k in REQUIRED:
            if k not in fm:
                errors.append(f"{p}: 必須キー '{k}' が無い")
        # id 一意
        if "id" in fm:
            if fm["id"] in seen_ids:
                errors.append(f"{p}: id '{fm['id']}' が {seen_ids[fm['id']]} と重複")
            seen_ids[fm["id"]] = p
        # slug == filename
        if fm.get("slug") and fm["slug"] != p.stem:
            errors.append(f"{p}: slug '{fm['slug']}' がファイル名 '{p.stem}' と不一致")
        # domain == 親ディレクトリ
        if fm.get("domain") and fm["domain"] != p.parent.name:
            errors.append(f"{p}: domain '{fm['domain']}' が {p.parent.name} と不一致")
        # status 語彙
        if fm.get("status") and fm["status"] not in STATUS:
            errors.append(f"{p}: status '{fm['status']}' は {STATUS} のいずれかにする")
        # forces 語彙
        for f in fm.get("forces", []):
            if f not in FORCES:
                errors.append(f"{p}: 未知の force '{f}'")
        # driving_variables 語彙
        for v in fm.get("driving_variables", []):
            if v not in DRIVING:
                errors.append(f"{p}: 未知の driving_variable '{v}'")
        # 相対リンク切れ（本文中の (*.md) ）
        for link in re.findall(r"\]\((\.{1,2}/[^)]+\.md)\)", text):
            target = (p.parent / link).resolve()
            if not target.exists():
                errors.append(f"{p}: リンク切れ '{link}'")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(md_files)} pattern files validated, {len(seen_ids)} unique ids.")

if __name__ == "__main__":
    main()
