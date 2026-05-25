---
title: "リトライストーム"
tags:
  - "アンチパターン"
  - "相反の誤選択"
---

# 9. リトライストーム

!!! abstract "一言"
    LLMプロバイダの一時障害に対してリトライが殺到し、障害をさらに拡大させてしまうアンチパターン。

## よくある場面

ある本番システムで、LLMプロバイダが一時的にレート制限（429エラー）を返し始めた。システムの各コンポーネントにはリトライロジックが組み込まれていたが、バックオフの設定が不十分だった。APIゲートウェイが3回リトライし、その内側のエージェントフレームワークも3回リトライし、さらにその内側のLLMクライアントも3回リトライした。結果として、1リクエストの失敗に対して最大27回のAPIコールが発生した。

数千の同時リクエストがこの状態に陥り、LLMプロバイダへのリクエスト量は通常の20倍以上に膨れ上がった。プロバイダの障害は悪化し、復旧までの時間が大幅に延びた。復旧後も、バックログに溜まったリトライが一斉に送信され、再びレート制限に到達するという悪循環が続いた。

## 症状

- LLMプロバイダの一時障害時にリクエスト量が急増する（通常の10倍以上）
- 障害が解消した後もシステムの回復に時間がかかる
- 複数レイヤーのリトライが重なり、リクエスト増幅が指数的になる
- APIのコスト（429応答もカウントされる場合）が急増する
- 正常なリクエストまで巻き添えで遅延する

## 根本原因

リトライロジックをレイヤーごとに独立して実装し、全体としてのリトライ戦略を設計していないことが原因である。各レイヤーが「自分の責任で」リトライするため、リトライ回数が乗算的に増幅する。

また、Fail-fast と縮退運転のどちらを選ぶかが `[F9]` プロバイダ信頼度と `[F3]` リクエスト価値に基づいて設計されておらず、「とにかくリトライすれば回復する」という前提で作られている。サーキットブレーカーが導入されていないケースも多い。

## 発見方法

- **リトライ増幅率**: 1つの元リクエストに対して最大何回のAPIコールが発生しうるか算出する（各レイヤーのリトライ回数の積）
- **障害時のトラフィック倍率**: 障害発生前後のLLM APIコール数を比較する
- **リトライレイヤーの棚卸し**: システム内でリトライを行っているレイヤーを全て洗い出す
- **メトリクス**: `retry_count_per_original_request`、`api_call_amplification_ratio`、`circuit_breaker_open_count`

## 対策

### ステップ1: リトライを1つのレイヤーに集約する

リトライは最も外側の1レイヤーのみで行い、内側のレイヤーではリトライしない（エラーを上位に伝播する）。

### ステップ2: 指数バックオフとジッターを必須にする

リトライ間隔は `base_delay * 2^attempt + random_jitter` とし、同時に多数のクライアントが同じタイミングでリトライすることを防ぐ。

### ステップ3: サーキットブレーカーを導入する

一定数の連続エラーでサーキットを「Open」にし、リトライ自体を停止する。一定時間後に「Half-Open」で試行し、回復を確認してから「Closed」に戻す。

```python
# サーキットブレーカー付きリトライの例
from circuitbreaker import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,      # 5回連続失敗でOpen
    recovery_timeout=30,      # 30秒後にHalf-Open
    expected_exception=RateLimitError,
)

@breaker
async def call_llm_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await llm_client.chat(prompt)
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

## 具体例

### Before（問題のある状態）

```python
# 3レイヤーそれぞれでリトライ → 最大 3×3×3 = 27回
# レイヤー1: APIゲートウェイ
response = retry(times=3)(api_gateway.forward)(request)

# レイヤー2: エージェントフレームワーク（内部）
result = retry(times=3)(agent.execute)(task)

# レイヤー3: LLMクライアント（内部）
completion = retry(times=3)(llm_client.chat)(prompt)
```

### After（改善後）

```python
# リトライは最外層のみ、内側はFail-fast
# レイヤー1: APIゲートウェイ — サーキットブレーカー + リトライ
@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry(times=3, backoff=exponential_with_jitter)
async def handle_request(request):
    return await agent.execute(request)

# レイヤー2: エージェントフレームワーク — リトライなし
async def execute(self, task):
    return await self.llm_client.chat(task.prompt)  # エラーはそのまま上位へ

# レイヤー3: LLMクライアント — リトライなし
async def chat(self, prompt):
    response = await self.http.post(self.endpoint, json={"prompt": prompt})
    if response.status == 429:
        raise RateLimitError(response)  # 上位に伝播
    return response.json()
```

## 関連するアンチパターン

- [無限・過大タイムアウト](01-infinite-timeout.md) — タイムアウトが長いとリトライの影響が拡大する
- [何でも同期 / 何でも非同期](07-all-sync-or-async.md) — 同期処理のタイムアウトがリトライを誘発する

## 関連パターン

- [#40 Fallback & Graceful Degradation](../patterns/08-cost-scaling/40-fallback-graceful-degradation.md) — リトライが失敗した場合の縮退運転
- [#5 Time-Budgeted Agent Loop](../patterns/01-execution/05-time-budgeted-agent-loop.md) — リトライを含めた全体の予算管理
- [#37 Semantic Gateway & Cost-Aware Router](../patterns/08-cost-scaling/37-semantic-gateway-cost-aware-router.md) — 別プロバイダへの動的ルーティング
