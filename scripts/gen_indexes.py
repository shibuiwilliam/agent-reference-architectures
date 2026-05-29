#!/usr/bin/env python3
"""ドメインindexと機械可読インデックス(docs/reference/pattern-index.md)を再生成する。
frontmatter を真実の源とし、表は常に自動生成（手書きしない）。
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERNS = ROOT / "docs" / "patterns"

DOMAINS = {
    "a-execution": "A. 実行方式・ライフサイクル",
    "b-orchestration": "B. オーケストレーション・制御フロー",
    "c-tools-security": "C. ツール・副作用・セキュリティ",
    "d-memory-context": "D. メモリ・コンテキスト",
    "e-safety-hitl": "E. 安全性・HITL・自律性",
    "f-data-integrity": "F. データ整合性・状態",
    "g-observability-ops": "G. 観測・評価・運用",
}

def fm(path):
    t = path.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", t, re.S)
    d, key = {}, None
    for raw in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_]+:", raw):
            key, _, val = raw.partition(":")
            d[key.strip()] = val.strip().strip('"')
    return d

def collect(domain):
    files = sorted(p for p in (PATTERNS / domain).glob("*.md")
                   if p.name not in ("index.md", "_template.md"))
    return [(p, fm(p)) for p in files]

# 1) ドメインindex
for dd, label in DOMAINS.items():
    rows = []
    for p, d in collect(dd):
        rows.append(f"| {d.get('id','')} | [{d.get('title','')}]({p.name}) "
                    f"| `{d.get('forces','')}` | `{d.get('driving_variables','')}` "
                    f"| {d.get('status','')} |")
    table = ("| ID | パターン | forces | driving_variables | status |\n"
             "|---|---|---|---|---|\n" + "\n".join(rows))
    (PATTERNS / dd / "index.md").write_text(
        f"# {label}\n\nこのドメインのパターン一覧（frontmatter から自動生成）。\n\n{table}\n",
        encoding="utf-8")

# 2) 機械可読インデックス
all_rows = []
for dd, label in DOMAINS.items():
    for p, d in collect(dd):
        rel = f"../patterns/{dd}/{p.name}"
        all_rows.append(
            f"| {d.get('id','')} | [{d.get('title','')}]({rel}) | {dd} "
            f"| `{d.get('forces','')}` | `{d.get('driving_variables','')}` "
            f"| `{d.get('forks','')}` | {d.get('status','')} |")
body = (
    "# 機械可読パターンインデックス\n\n"
    "全パターンの frontmatter メタを1表に集約（`scripts/gen_indexes.py` で自動生成）。\n"
    "コーディングエージェントはこの表から候補を絞り、各 `.md` を読みに行くとよい。\n\n"
    "| ID | パターン | domain | forces | driving_variables | forks | status |\n"
    "|---|---|---|---|---|---|---|\n" + "\n".join(all_rows) + "\n")
(ROOT / "docs" / "reference" / "pattern-index.md").write_text(body, encoding="utf-8")

print("regenerated: domain indexes + reference/pattern-index.md")
