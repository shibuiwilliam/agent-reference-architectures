---
title: "Prompt Cache Optimized Context｜プロンプトキャッシュ"
tags:
  - "コスト・性能・スケーリング"
  - "F7 コスト感度・スケール"
  - "F4 レイテンシ予算"
---

# #39 Prompt Cache Optimized Context｜プロンプトキャッシュ

!!! abstract "一言"
    プロンプトの**共通prefix（システムプロンプト・Few-shot例）を先頭に固定**し、LLMプロバイダのプロンプトキャッシュを最大限に活かす。

## 概要

多くのLLMプロバイダはプロンプトのprefix部分が一致する場合にキャッシュを適用し、入力トークンのコストとTime to First Token（TTFT）を削減する。本パターンではシステムプロンプト・Few-shot例・共通コンテキストをプロンプトの先頭に安定配置し、リクエストごとに変わる部分（ユーザー入力・動的コンテキスト）を末尾に置く。prefix長を一定以上に保つことでキャッシュヒット率を高める。

!!! info "意思決定上の位置づけ"
    - **必要にするフォース**: `[F7]` コスト感度・スケール・`[F4]` レイテンシ予算
    - **意思決定の進め方**: [意思決定の進め方](../../decisions/decision-flow.md)

## 設計

プロンプトを3層に構成する。第1層：システムプロンプト＋行動規範（全リクエスト共通、変更頻度は低い）。第2層：Few-shot例・ドメインナレッジ（タスクカテゴリ共通）。第3層：ユーザー入力・セッション固有コンテキスト（リクエスト固有）。第1層・第2層が共通prefixとなりキャッシュ対象になる。第2層の並び順もハッシュ等で安定化させ、順序変動でキャッシュが無効化されるのを防ぐ。

## 解決する課題

RAG等で大量のコンテキストをプロンプトに含めると入力トークン数が膨張し、コスト `[F7]` とレイテンシ `[F4]` が悪化する。プロンプトキャッシュが効けば、共通prefix分の入力コストが50〜90%削減され、TTFTも短縮される。しかしprefixが不安定だとキャッシュヒット率が低下し、効果が出ない。

## 向き / 不向き

- **向き**: 長いシステムプロンプトやFew-shot例を使うエージェント、同一カテゴリのリクエストが連続するワークロード、大量のRAGコンテキストを付与する構成。
- **不向き**: リクエストごとにプロンプト構造が大きく変わる場合。プロバイダがプロンプトキャッシュを提供していない場合。prefix長がキャッシュ適用の最小閾値に満たない短いプロンプト。

## 要素技術

- プロバイダキャッシュ: Anthropic Prompt Caching、OpenAI Automatic Prompt Caching、Google Context Caching
- コンテキスト組立: [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md) と併用
- 順序安定化: コンテキストチャンクのハッシュソート

## 調整（程度）

- **prefix長** — 短すぎるとキャッシュ適用の最小閾値を下回る ⇔ 長すぎると動的部分のコンテキスト窓が狭まる / 決め手 `[F7]` / 目安: プロバイダの最小prefix要件（例: 1024トークン以上）を満たしつつ、動的部分に十分な余裕を残す。→ [程度ダイヤル](../../decisions/tuning-dials.md)

## 関連パターン

- [#38 Semantic Result Cache](38-semantic-result-cache.md) — 結果レベルのキャッシュ（プロンプトキャッシュと補完関係）
- [#24 Context Pack / Assembly](../05-memory-context/24-context-pack-assembly.md) — コンテキストの組み立て方がキャッシュ効率に直結する
- [#37 Semantic Gateway](37-semantic-gateway-cost-aware-router.md) — モデル選択とキャッシュ戦略を組み合わせてコストを最適化する

## 参考

- Anthropic Prompt Caching Documentation
- OpenAI Prompt Caching Guide
