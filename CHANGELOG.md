# CHANGELOG

## [1.1.0] — 2026-05-27

### Added
- `decisions.yml`: ルール構造を `required` / `recommended` / `optional` の3段階に再編
- `decisions.yml`: 全20ダイヤルに `value_mapping`（フォース別値域マッピング）を追加
- `decisions.yml`: 全16二者択一に `decision_function`（判定関数）を追加
- `decisions.yml`: `architecture_selection`（リファレンスアーキテクチャの複合選定条件）を追加
- `patterns.yml`: 全59パターンに `selection_criteria`（選定基準）を追加
- `patterns.yml`: 全59パターンに `summary_plain`（プレーンテキスト概要）を追加
- `patterns.yml`: 全59パターンに `prevents_anti_patterns`（アンチパターン予防参照）を追加
- `anti-patterns.yml`: 11アンチパターンの構造化データを新設
- `catalog.json`: `by_force`（フォース別逆引きインデックス）を追加
- `catalog.json`: `bidirectional_related`（双方向関連パターン）を追加
- `catalog.json`: `selection_guide`（選定手順ガイド）を追加
- `catalog.json`: `anti_patterns`（アンチパターンデータ）を追加
- `generate.py`: `llms-full.txt` / `llms-core.txt` のエージェント可読変換を追加
- `generate.py`: `--lint` オプション（パターンページ構造検証）を追加
- `generate.py`: `--validate` オプション（JSON Schemaバリデーション）を追加
- `schemas/`: JSON Schema（patterns/decisions/catalog）を新設
- `docs/index.md`: 人間・エージェント双方の読者導線を追加
- `docs/agent-guide.md`: 構造化データ参照（by_force, selection_guide, decision_function等）を反映
- `AGENTS.md`: `catalog.json` の新フィールドへの参照を追加
