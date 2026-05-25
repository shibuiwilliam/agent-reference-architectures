#!/usr/bin/env python3
"""
scaffold.py — patterns.yml から docs/ 配下のスタブを生成する。

- 既存ファイルは上書きしない（冪等。執筆済みの内容を壊さない）。
- 生成対象:
    docs/patterns/<category>/index.md         … カテゴリ概要＋当該パターン一覧
    docs/patterns/<category>/<NN>-<slug>.md    … パターン本文スタブ（templates/pattern.md ベース）
- nav は mkdocs.yml で手動管理する（このスクリプトは nav を書き換えない）。
  追加したパターンの nav 行は、最後にコンソールへ出力するのでコピーして貼る。

使い方:
    python scripts/scaffold.py            # 不足ファイルだけ生成
    python scripts/scaffold.py --check    # 生成せず、不足を一覧表示（CIで利用可）
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML が必要です: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "patterns.yml"
TEMPLATE = ROOT / "templates" / "pattern.md"
DOCS = ROOT / "docs" / "patterns"


def render_pattern(num, slug, title, tagline, category_title, forces) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    force_tags = "\n".join(f'  - "{f}"' for f in (forces or []))
    return (
        tpl.replace("{{NUM}}", str(num))
        .replace("{{TITLE}}", title)
        .replace("{{TAGLINE}}", tagline)
        .replace("{{CATEGORY_TITLE}}", category_title)
        .replace("{{FORCE_TAGS}}", force_tags)
    )


def render_category_index(cat) -> str:
    lines = [f"# {cat['roman']}. {cat['title']}", "", cat["summary"], ""]
    for p in cat["patterns"]:
        fn = f"{p['num']:02d}-{p['slug']}.md"
        lines.append(f"- [#{p['num']} {p['title']}]({fn}) — {p['tagline']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="生成せず不足を一覧表示")
    args = ap.parse_args()

    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    created, missing, nav_lines = [], [], []

    for cat in data["categories"]:
        cdir = DOCS / cat["id"]
        cdir.mkdir(parents=True, exist_ok=True)

        idx = cdir / "index.md"
        if not idx.exists():
            missing.append(idx)
            if not args.check:
                idx.write_text(render_category_index(cat), encoding="utf-8")
                created.append(idx)

        nav_lines.append(f"      - {cat['roman']}. {cat['title']}:")
        nav_lines.append(f"          - patterns/{cat['id']}/index.md")
        for p in cat["patterns"]:
            fn = f"{p['num']:02d}-{p['slug']}.md"
            fpath = cdir / fn
            nav_lines.append(
                f'          - "#{p["num"]} {p["title"].split("｜")[0]}": '
                f"patterns/{cat['id']}/{fn}"
            )
            if not fpath.exists():
                missing.append(fpath)
                if not args.check:
                    fpath.write_text(
                        render_pattern(
                            p["num"], p["slug"], p["title"], p["tagline"],
                            cat["title"], p.get("forces", []),
                        ),
                        encoding="utf-8",
                    )
                    created.append(fpath)

    if args.check:
        if missing:
            print("未作成のファイル:")
            for m in missing:
                print("  -", m.relative_to(ROOT))
            return 1
        print("すべてのパターンページが存在します。")
        return 0

    print(f"生成: {len(created)} ファイル / 既存スキップ: {sum(1 for _ in DOCS.rglob('*.md')) - len(created)}")
    for c in created:
        print("  +", c.relative_to(ROOT))
    print("\n--- mkdocs.yml の nav（パターン部分）参考出力 ---")
    print("\n".join(nav_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
