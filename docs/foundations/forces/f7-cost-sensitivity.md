---
title: "[F7] コスト感度・スケール"
tags:
  - "駆動変数"
---

# [F7] コスト感度・スケール（Cost Sensitivity & Scale）

!!! abstract "一言"
    リクエスト量とコスト上限の厳しさを測るフォース。感度が高いほど、キャッシュ・ルーティング・予算制御が不可欠になる。

## 概要

コスト感度・スケールは、システムが処理するリクエスト量（QPS）と、月間で許容されるLLM API費用の上限の厳しさを表す。LLMの推論コストは従来のAPIコールと比べ桁違いに高く、無制限に呼び出せば月額費用が急速に膨張する。このフォースはコスト効率に関するすべての設計判断の起点となる。

## なぜ重要か

コスト感度を見落とすと、開発環境では問題なく動いていたシステムが本番のトラフィックを受けた瞬間に予算を超過する。あるいは、月末にAPI請求書を見て初めて問題に気づく。とくにエージェントが自律的にツールを呼び出しループする構成では、1リクエストあたりのLLM呼び出し回数が予測しにくく、予算の暴走リスクが高い。

## 値域の解釈

### 低い場合

コスト制約が緩い状況。研究開発フェーズ、社内の少人数向けツール、1リクエストの価値が十分に高い（`[F3]` 高）ケースなどが該当する。最高品質のモデルを自由に使い、リトライや複数候補生成を許容できる。最適化よりも品質やスピードを優先してよい。

### 高い場合

大量リクエストかつ厳しいコスト上限がある状況。BtoCサービスの全ユーザーへのLLM応答、大規模バッチ処理、スタートアップのランウェイ制約などが典型例。モデルティアの動的選択（難しい問題だけ大型モデル）、セマンティックキャッシュ、プロンプト圧縮、予算キャップ付きループといったコスト最適化パターンが必須になる。

## 評価の指針

- 月間のLLM API費用の上限は明示的に定められているか
- ピーク時のQPSはどの程度か、季節変動やバーストはあるか
- 1リクエストあたりのLLM呼び出し回数は予測可能か、それともエージェントの判断次第か
- 現在の1リクエストあたりの平均コストはいくらか、それは持続可能か
- コスト超過時の対応方針は決まっているか（縮退・拒否・アラート）

## 影響する設計判断

### 関連するダイヤル

- [予算キャップ](../../decisions/dials/budget-cap.md) — リクエスト単位・セッション単位の上限を設定する
- [モデルティア・ルーティング](../../decisions/dials/model-tier-routing.md) — 難易度に応じて軽量モデルと大型モデルを使い分ける
- [キャッシュ類似度](../../decisions/dials/cache-similarity.md) — キャッシュの類似度閾値を下げてヒット率を上げる
- [リトライ回数](../../decisions/dials/retry-count.md) — コスト感度が高いほどリトライ回数を制限する
- [Temperature](../../decisions/dials/temperature.md) — 低temperatureで出力を安定させ、リジェクト率を下げることでコストを抑える

### 関連する二者択一

- [RAG ↔ ファインチューニング](../../decisions/tradeoffs-catalog/rag-vs-finetuning.md) — 大量の類似リクエストならファインチューニングで推論コストを削減できる場合がある
- [LLM ↔ ツール](../../decisions/tradeoffs-catalog/llm-vs-tool.md) — LLMでなくても解ける処理はルールベースに切り替えてコストを削減
- [フェイルファスト ↔ 縮退](../../decisions/tradeoffs-catalog/fail-fast-vs-degradation.md) — 予算超過時にフェイルファストするか縮退で対応するか
- [ビルド ↔ バイ](../../decisions/tradeoffs-catalog/build-vs-buy.md) — マネージドサービスの従量課金と自前ホスティングの固定費を比較する

## 関連パターン

- [#38 Semantic Result Cache](../../patterns/08-cost-scaling/38-semantic-result-cache.md) — 意味的に近い結果を再利用してAPI呼び出しを削減する
- [#56 Adaptive Effort](../../patterns/08-cost-scaling/56-adaptive-effort.md) — 難易度に応じて投入計算量を増減する
- [#37 Semantic Gateway & Cost-Aware Router](../../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) — コストを考慮してモデルを動的に選択する
- [#5 Time-Budgeted Agent Loop](../../patterns/01-execution/05-time-budgeted-agent-loop.md) — 時間・回数・コストを予算化してループの暴走を防ぐ
- [#55 Deadline & Budget Cascade](../../patterns/01-execution/55-deadline-budget-cascade.md) — 予算上限を呼び出しツリーへ伝播する
