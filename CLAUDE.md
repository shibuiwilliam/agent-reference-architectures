# CLAUDE.md — このリポジトリでの作業規約（Claude Code 用）

> このファイルは Claude Code に自動で読み込まれる「運用マニュアル」です。**ドキュメントを書くとき**と、**このドキュメントを使って別プロジェクトのアーキテクチャを設計するとき**の両方の振る舞いを規定します。人間も読みます。

## 0. このリポジトリは何か

意思決定層（**程度の調整**と**相反する仕組みの選定基準**）を中心に、**AIエージェントを本番システムに組み込むソフトウェアアーキテクチャ・パターン集**を MkDocs (Material) で執筆し、GitHub Pages で公開するプロジェクト。想定読者は**人間とコーディングエージェント**の両方。コーディングエージェントがこのドキュメントを読み込むことで、AIエージェントを含むアーキテクチャを適切に設計し、人間に提案できることを目標にする。

詳細な狙い・情報設計・ロードマップは [`PROJECT.md`](PROJECT.md) を読むこと。

## 1. 最初に読むファイル（順序固定）

新しいタスクを始める前に、必ずこの順で読む：

1. `PROJECT.md` … 全体像・情報設計・執筆ロードマップ
2. `docs/concepts/layer-model.md` … 5層モデル（背骨）
3. `docs/concepts/design-forces.md`（F1–F17）/ `budgets.md`（7予算）/ `driving-variables.md`（9駆動変数）
4. `docs/patterns/_template.md` … パターン記述の正準テンプレートと frontmatter スキーマ
5. 着手するパターンの既存 `.md`（雛形）

## 2. ディレクトリ構成（要点）

```
docs/
  concepts/    第I部 地盤（force / budget / driving variable / 5層モデル）
  degrees/     第II部 程度（ダイヤル）— 意思決定層の中核その1
  forks/       第III部 相反（フォーク）— 意思決定層の中核その2
  patterns/    第IV部 パターン（A〜G ドメイン）。1パターン=1ファイル
    _template.md   ← 正準テンプレート（コピー元）
  decision/    第V部 意思決定フロー
  antipatterns/第VI部 アンチパターン
  for-agents/  コーディングエージェント向けの使い方・提案プロトコル
  reference/   用語集・機械可読インデックス
```

新規パターンは `python scripts/new_pattern.py <ID> <domain> <slug> "<title>"` で雛形生成してから書く（手書きで frontmatter を作らない）。

## 3. パターン記述の鉄則

### 3.1 frontmatter スキーマ（必須・厳守）

各パターン `.md` の先頭 YAML は次のキーを持つ。**機械可読性の生命線なので形式を崩さない**。

```yaml
---
id: A2                         # [A-G][0-9]+ 一意
slug: durable-async-agent      # ファイル名と一致（拡張子なし）
title: "Durable Async Agent｜耐久非同期セッション"
domain: a-execution            # ディレクトリ名と一致
status: draft                  # draft | review | stable のいずれか
layer: L5-pattern              # 固定
summary: "一文要約。"
forces: [F1, F7, F15, F17]     # 下記の統制語彙のみ
driving_variables: [reversibility, latency_budget, accountability]  # 統制語彙のみ
forks:                         # 任意。"<fork-id>:<chosen-side>"
  - "F-1:async"
  - "F-14:external-state"
related_patterns: [A3, F1, G1] # 他パターンの id
alternatives: [A1]             # 適用外のとき代わりに使う id
tags: [execution, durability]
---
```

**統制語彙（この値以外を使わない）**

- `forces`: `F1`〜`F17`（定義は `docs/concepts/design-forces.md`）
- `driving_variables`: `reversibility` / `failure_cost` / `request_value` / `latency_budget` / `input_trust` / `task_variability` / `cost_sensitivity` / `accountability` / `provider_trust`（定義は `docs/concepts/driving-variables.md`）
- `status`: `draft` / `review` / `stable`
- `forks` の左辺は `docs/forks/index.md` に定義された `F-1`〜`F-18`、右辺はそのフォークで定義された選択肢名

### 3.2 本文セクション（順序固定・全部書く）

`_template.md` の見出しを一字一句この順で使う：

1. `## 一言で（TL;DR）`
2. `## 解決する問題`
3. `## 選定条件（When to use / When NOT）` ← **意思決定層の中核。必ず「使わない条件＝代替に倒す条件」も書く**
4. `## 駆動変数とチューニング（程度）` ← 各目盛りに「効かなすぎ⇔効きすぎ」「`[駆動変数]`」「目安値」を明記
5. `## 相反における立ち位置（相反）` ← どの fork でどちら側か、判定基準
6. `## 構造`（`mermaid` 図）
7. `## 実装メモ`（具体的なコード/JSON/設定。最小実装と落とし穴）
8. `## 効かせる力学（forces）`
9. `## 関連・代替`
10. `## コーディングエージェント向け指示（machine-actionable）` ← **「このパターンを提案するなら同時に提案/確認すべきこと」のチェックリスト**

### 3.3 品質ゲート（これを満たさない限り status=stable にしない）

- 「選定条件」に **When NOT to use** がある。
- 目盛りに必ず `[駆動変数]` が紐づき、値が「定数」でなく「駆動変数の関数」として説明されている（例：「閾値はコサイン0.92–0.97。**`[failure_cost]` が高い領域ほど上げる**」）。
- 数値の目安には根拠か出典がある（断定しすぎない）。
- frontmatter の `forces` / `driving_variables` / `forks` が本文と矛盾しない。
- `related_patterns` / `alternatives` の各 id に**相対リンク**を本文で張っている。

## 4. 執筆スタイル

- 言語は**日本語**。コード・設定・frontmatter のキー・統制語彙は英語のまま。
- 散文中心。ただし「程度」「相反」「比較」は表が読みやすいので表を使ってよい。
- 過度な太字・箇条書きの乱用を避ける。1パターン本文は概ね 250〜700 行に収める（長すぎたら分割を検討）。
- 断定を避ける数値表現（「目安」「出発点」「概ね」）を使う。本ドキュメントの主張は「定数でなく関数」。
- 既存の統合レポート（`/mnt/user-data/outputs/ai-agent-architecture-integrated.md` 等が手元にあれば参照）と用語・記号を揃える。

## 5. リンク規約

- ページ間リンクは**相対パス**（例：`[A3](a3-sync-facade-async-core.md)`、別ドメインは `../b-orchestration/b1-deterministic-shell.md`）。
- 絶対URLや `site_url` 依存のリンクを本文に書かない（`llms.txt` 生成とローカルビルドの両方で壊れる）。
- 画像は使わず、構造は `mermaid` で表現する（マークダウンで完結し、エージェントが読める）。

## 6. ナビゲーション（mkdocs.yml）の更新

- 新規ページを追加したら `mkdocs.yml` の `nav:` に追記する（**strict ビルドが nav 漏れで失敗するため必須**）。
- ドメイン index（`docs/patterns/<domain>/index.md`）のパターン表は `python scripts/gen_indexes.py` で再生成できる（手書きしない）。

## 7. ビルド・プレビュー・検証コマンド

```bash
# 依存インストール（初回）
uv sync

# ローカルプレビュー（http://127.0.0.1:8000）
uv run mkdocs serve

# 本番同等の厳格ビルド（警告をエラー扱い。CIと同じ）
uv run mkdocs build --strict

# 自前バリデーション（frontmatterスキーマ・統制語彙・id重複・相対リンク切れ）
uv run python scripts/validate.py

# 機械可読インデックスとドメイン表の再生成
uv run python scripts/gen_indexes.py
```

**コミット前チェックリスト**：`python scripts/validate.py` と `mkdocs build --strict` が両方通ること。

## 8. デプロイ

- `main` ブランチへの push で `.github/workflows/deploy.yml` が走り、GitHub Pages に公開される。
- 公開前提として GitHub リポジトリの Settings → Pages → Build and deployment → Source を **GitHub Actions** にしておく（人間の初回作業）。
- `mkdocs.yml` の `site_url` / `repo_url` をリポジトリに合わせて置き換える（`llms.txt` 生成に `site_url` が必須）。

## 9. コーディングエージェント向けマークダウン配信

- 公開サイトは `mkdocs-llmstxt` により `/{site}/llms.txt`（索引）・`/llms-full.txt`（全文連結）・各ページの `.md` を自動生成する。
- エージェントは公開サイトの `llms.txt` か、**リポジトリの生 `docs/**.md`** のどちらからでも読める。後者は frontmatter 込みで取得できるので機械処理に向く。

## 10. 「設計を提案する」タスクでの振る舞い

このリポジトリを**読み込んだ状態で別プロジェクトのアーキテクチャを設計**するよう求められたら、必ず [`docs/for-agents/decision-protocol.md`](docs/for-agents/decision-protocol.md) の手順に従う。要点：

1. 9つの駆動変数を当該ユースケースについて埋める（不明なら人間に1問だけ聞く）。
2. 7つの予算を設定する。
3. `docs/decision/decision-flow.md` で候補パターンを出す。
4. 各候補の「選定条件（When NOT 含む）」で採否を判定。
5. 採用パターンの**目盛り値を駆動変数から導出**し、**「なぜその値か」を必ず添えて**人間に提案する。
6. **目盛りをハードコードしない／単独で結論を出さず人間に選択肢と根拠を提示する**。

## 11. やってはいけないこと

- frontmatter のキー名・統制語彙を勝手に増やす（増やすなら `PROJECT.md` と本ファイルの定義を先に更新し、`validate.py` も更新する）。
- nav 未登録のページを放置する（strict ビルドが落ちる）。
- 本文に絶対URL・画像・`localStorage` 依存などを入れる。
- 数値目安を出典・根拠なしに断定する。
- 1コミットで多数パターンを薄く埋める（1パターンを stable 品質で仕上げる方を優先）。
