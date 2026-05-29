#!/usr/bin/env python3
"""新規パターンの雛形を生成する。
使い方:
  python scripts/new_pattern.py A8 a-execution a8-foo "Foo Pattern｜フー"
frontmatter スキーマと本文セクションは CLAUDE.md §3 に従う。
"""
import sys, os, pathlib

TEMPLATE = '''---
id: {id}
slug: {slug}
title: "{title}"
domain: {domain}
status: draft
layer: L5-pattern
summary: "TODO 一文要約。"
forces: []
driving_variables: []
forks: []
related_patterns: []
alternatives: []
tags: []
---

# {title}

!!! note "このページのステータス: draft"
    本文は [`../_template.md`](../_template.md) のセクション構成に従って執筆する。

## 一言で（TL;DR）

TODO

## 解決する問題

<!-- TODO -->

## 選定条件（When to use / When NOT）

<!-- TODO: 採用条件 + 採用しない条件（代替に倒す条件）。意思決定層の中核。 -->

## 駆動変数とチューニング（程度）

<!-- TODO: 目盛りごとに「効かなすぎ⇔効きすぎ」「[駆動変数]」「目安値」。 -->

## 相反における立ち位置（相反）

<!-- TODO -->

## 構造

```mermaid
flowchart LR
  TODO[TODO]
```

## 実装メモ

<!-- TODO -->

## 効かせる力学（forces）

<!-- TODO -->

## 関連・代替

<!-- TODO -->

## コーディングエージェント向け指示（machine-actionable）

<!-- TODO -->
'''

def main():
    if len(sys.argv) != 5:
        print(__doc__); sys.exit(1)
    id_, domain, slug, title = sys.argv[1:5]
    root = pathlib.Path(__file__).resolve().parent.parent
    out = root / "docs" / "patterns" / domain / f"{slug}.md"
    if out.exists():
        print(f"already exists: {out}"); sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.format(id=id_, slug=slug, title=title, domain=domain), encoding="utf-8")
    print(f"created: {out}")
    print("→ mkdocs.yml の nav: と for-agents 提案フローへの追加を忘れずに。")
    print("→ python scripts/gen_indexes.py で索引を更新。")

if __name__ == "__main__":
    main()
