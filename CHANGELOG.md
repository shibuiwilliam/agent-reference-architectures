# Changelog

本カタログの変更履歴。[Semantic Versioning](https://semver.org/) に従う。

パターンの追加・削除・番号変更は MAJOR または MINOR。ダイヤル/二者択一の追加は MINOR。文言修正のみは PATCH。

## [1.0.0] — 2026-05-25

### Added
- 59パターン（12カテゴリ）の全文公開
- 9つの駆動変数（フォース F1–F9）
- 20のチューニングダイヤル（程度パラメータ）
- 16の二者択一（相反する設計判断）
- 6つのリファレンスアーキテクチャ（複合構成）
- 11のアンチパターン
- 3つの通し例（worked examples）
- フォース別逆引き（by-force）
- ダイヤル×二者択一の相互作用（interactions）

### Added (Agent-Consumable)
- `decisions.yml` — 意思決定層の構造化正本（forces/dials/tradeoffs/reference_architectures/rules）
- `patterns.yml` 拡張 — related, when_to_use, when_not, element_tech, dials, tradeoffs
- `catalog.json` — 機械可読マニフェスト（59パターン＋全決定層データ）
- `llms.txt` — llmstxt.org形式のサイト索引
- `llms-core.txt` — 意思決定コア（低トークン版）
- `llms-full.txt` — 全ページ連結プレーンテキスト
- `AGENTS.md` — コーディングエージェント向け統合ガイド
- `docs/agent-guide.md` — 利用手順・引用規約・境界規約
- `docs/agent-proposal-template.md` — アーキテクチャ提案テンプレート
- `scripts/generate.py` — 正本から全成果物を冪等生成するスクリプト
- CI配線 — `deploy.yml` でビルド前に `generate.py` を実行
- 10の決定規則（IF–THEN候補）
