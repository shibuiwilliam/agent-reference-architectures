# AIエージェント本番アーキテクチャ・パターン

意思決定層（**程度の調整**と**相反する仕組みの選定基準**）を中心に据えた、AIエージェントを本番システムに組み込むためのソフトウェアアーキテクチャ・パターン集です。

単なるパターンの羅列ではなく、**「どのパターンを、どの目盛りで、どちらの仕組みで採るか」を根拠（どの駆動変数が効いたか）とともに決められる**ことを目標としています。

## 想定読者

| 読者 | 使い方 |
|------|--------|
| 人間（設計者・レビュア） | 設計判断の根拠を引く、レビューの観点リストにする |
| コーディングエージェント | `docs/` の生マークダウンを読み込み、AIエージェントを含む構成を設計し人間に提案する |

## 5層モデル

設計判断を、固定値ではなく「目盛り（程度）」と「二択（相反）」として扱い、少数の駆動変数から導きます。

| 層 | 問い | 道具 |
|---|------|------|
| L0 なぜ難しいか | 普通のソフトと何が違うか | 設計力学 F1–F17 |
| L1 何を配分するか | 何をどれだけ使えるか | 7つの予算 |
| L2 どう決めるか | 目盛り/二択を何が左右するか | 9つの駆動変数 |
| L3 どこまで回すか | 各設計変数のちょうど | 程度（ダイヤル） |
| L4 どちらを採るか | 排他的な仕組みのどちら | 相反（フォーク） |
| L5 何を組むか | 実装する再利用部品 | パターン A–G（39件） |

根本原則：**確率的な核（LLM）を、決定論的な殻（コード）で包む。**

## パターン一覧（39件）

| ドメイン | テーマ | パターン |
|---|---|---|
| **A** | 実行方式 | A1 同期エッジ / A2 耐久非同期 / A3 同期ファサード / A4 進捗ストリーミング / A6 適応タイムアウト・リトライ / A7 期限・予算カスケード |
| **B** | オーケストレーション | B1 決定論的な殻 / B2 ワークフロー骨格 / B3 予算付き自律ループ / B4 計画-実行-検証 / B5 Supervisor-Worker / B6 Critic-Judge・多数決 / B7 モデルルーター |
| **C** | ツール・セキュリティ | C1 ツールゲートウェイ / C2 読取自由・書込ゲート / C3 ドライラン・コミット / C4 冪等コマンド包装 / C5 Capability Lease / C6 Confused Deputy防御 / C7 サンドボックス / C8 サーガ・補償 |
| **D** | メモリ・コンテキスト | D1 階層化メモリ / D2 コンテキスト予算配分 / D3 メモリ書込ゲート / D4 減衰・版管理 / D5 Prompt Registry / D6 禁止領域付きキャッシュ |
| **E** | 安全性・HITL | E1 リスクベース承認 / E2 Policy-as-Code / E3 ガードレールサンドイッチ / E4 構造化出力 / E5 Autonomy Ladder |
| **F** | データ整合性 | F1 短トランザクション・長セッション / F2 イベントソーシング・リプレイ |
| **G** | 観測・運用 | G1 二層観測 / G2 全ホップトレース / G3 シャドウ・カナリア / G4 評価ハーネス / G5 サーキットブレーカ・縮退 |

各パターンには frontmatter で `forces` / `driving_variables` / `forks` / `related_patterns` / `alternatives` が機械可読メタとして付与されています。

## ディレクトリ構成

```
.
├── CLAUDE.md                  作業規約（Claude Code が自動読込）
├── PROJECT.md                 プロジェクト憲章
├── pyproject.toml             ビルド依存（uv で管理）
├── mkdocs.yml                 サイト設定・nav
├── .github/workflows/         GitHub Pages 自動デプロイ
├── scripts/                   validate / gen_indexes / new_pattern
└── docs/
    ├── index.md               トップページ
    ├── for-agents/            コーディングエージェント向けガイド・提案プロトコル
    ├── concepts/              第I部 地盤（力学・予算・駆動変数・5層モデル）
    ├── degrees/               第II部 程度（ダイヤル）
    ├── forks/                 第III部 相反（フォーク）
    ├── patterns/              第IV部 パターン A–G（39件）
    ├── decision/              第V部 意思決定フロー
    ├── antipatterns/          第VI部 アンチパターン
    └── reference/             用語集・機械可読インデックス
```

## セットアップ

[uv](https://docs.astral.sh/uv/) が必要です。

```bash
# 依存インストール
uv sync

# ローカルプレビュー（http://127.0.0.1:8000）
uv run mkdocs serve

# 本番同等の厳格ビルド
uv run mkdocs build --strict

# frontmatter スキーマ・統制語彙・リンク切れ検証
uv run python scripts/validate.py

# ドメイン index・機械可読インデックスの再生成
uv run python scripts/gen_indexes.py
```

## コーディングエージェント向け

このリポジトリはコーディングエージェントが読み込んで設計提案に使うことを想定しています。

- **機械可読インデックス**: `docs/reference/pattern-index.md` — 全パターンの `id` / `forces` / `driving_variables` / `forks` を1表に集約
- **設計提案プロトコル**: `docs/for-agents/decision-protocol.md` — 駆動変数の評価から候補選定・目盛り決定・提案出力までの手順
- **生マークダウン配信**: 公開サイトでは `mkdocs-llmstxt` により `/llms.txt`（索引）・`/llms-full.txt`（全文連結）を生成
- **リポジトリ直読**: `docs/**/*.md` を直接読めば frontmatter 込みでメタ抽出が可能

## デプロイ

`main` ブランチへの push で GitHub Actions が `mkdocs build --strict` を実行し、GitHub Pages に公開します。

初回セットアップ時に以下が必要です:

1. `mkdocs.yml` の `site_url` / `repo_url` を自リポジトリに合わせて書き換える
2. GitHub リポジトリの Settings → Pages → Source を **GitHub Actions** に設定する

## ライセンス

MIT
