---
title: "Prompt/Model/Tool Version Pinning｜バージョン固定"
tags:
  - "観測性・監査・評価"
  - "F8 説明責任・規制"
---

# #33 Prompt/Model/Tool Version Pinning｜バージョン固定

!!! abstract "一言"
    プロンプト・モデル・ツールのバージョンを**明示的に固定**し、再現性と回帰検知の土台を作る。

## 概要

エージェントの挙動はプロンプトテンプレート、LLMモデルのバージョン、ツール（MCP含む）のAPIバージョンの組み合わせで決まる。いずれかがサイレントに変わると出力が変動し、障害原因の特定が困難になる。本パターンでは三者それぞれにバージョン識別子を付与し、デプロイ設定で固定する。トレースにもバージョンを記録し、「いつ・何が変わったか」を常に追跡可能にする。

## 設計

プロンプトはGitまたはプロンプトレジストリでバージョン管理し、デプロイ時にハッシュまたはタグで固定する。モデルはスナップショット指定（例: `gpt-4o-2024-11-20`）で呼び出し、`latest` エイリアスを本番で使わない。ツールはAPIバージョンヘッダまたはMCPサーバーのイメージタグで固定する。これら三者の組をリリースバンドルとして管理し、変更は [#34 Evaluation CI/CD](34-evaluation-ci-cd.md) を通過してからロールアウトする。

## 解決する課題

LLMプロバイダのモデル更新やプロンプトの微修正が、予告なく本番の挙動を変えてしまう。バージョン固定がなければ「昨日まで動いていたのに今日壊れた」の原因を切り分けられず、回帰テストも意味をなさない `[F8]`。

## 向き / 不向き

- **向き**: 本番運用されるエージェント全般。特に規制業種・SLA付きサービス・複数モデルを併用する構成。
- **不向き**: 探索的なプロトタイピング段階で、最新モデルを常に試したいフェーズ（固定は安定化後に導入すればよい）。

## 要素技術

- プロンプト管理: Git + タグ、Langfuse Prompt Registry、Humanloop
- モデル固定: OpenAI snapshot ID、Anthropic model version、Azure OpenAI deployment
- ツール固定: Docker image tag、API version header、MCP server version

## 関連パターン

- [#34 Evaluation CI/CD](34-evaluation-ci-cd.md) — バージョン変更時に自動評価を走らせ回帰を検知する
- [#32 Agent Trace](32-agent-trace.md) — トレースにバージョン情報を記録し事後追跡を可能にする
- [#35 Production Replay](35-production-replay.md) — 旧バージョンのトレースを新バージョンで再生し差分を検証する

## 参考

- OpenAI Model Deprecation Policy
- Anthropic API Versioning
