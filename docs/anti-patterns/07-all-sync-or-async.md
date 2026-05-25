---
title: "何でも同期 / 何でも非同期"
tags:
  - "アンチパターン"
  - "相反の誤選択"
---

# 7. 何でも同期 / 何でも非同期

!!! abstract "一言"
    処理の同期・非同期を一律に統一してしまい、短いリクエストのUXか長いリクエストの信頼性のどちらかを犠牲にしてしまうアンチパターン。

## よくある場面

あるチームがエージェントAPIを構築する際、「シンプルに保つ」ために全リクエストを同期HTTPで処理する設計にした。初期は数秒で完了するリクエストばかりだったが、ドキュメント分析やコード生成といった長時間タスクが追加されるにつれ、30秒以上かかるリクエストが増えた。ロードバランサーのタイムアウトに引っかかり、処理途中でコネクションが切断されるケースが頻発した。

一方、別のチームは教訓を活かして全リクエストを非同期ジョブキューで処理する設計にした。しかし、「今日の天気は？」のような即答可能な質問でも、ジョブキュー→ワーカー→ポーリングという経路を通るため、応答に2〜3秒かかるようになった。チャットUIの体験は著しく低下した。

## 症状

- **全同期の場合**: 長時間リクエストがタイムアウトし、クライアントが再送→二重処理が発生する
- **全同期の場合**: ワーカースレッドが長時間リクエストに占有され、短いリクエストまで待たされる
- **全非同期の場合**: 即答可能なリクエストに不要なレイテンシが加わる
- **全非同期の場合**: ポーリングやWebhookの実装コストが全リクエストに上乗せされる
- いずれの場合も、処理時間の多様性に対応できず、一部のユーザーが不満を抱える

## 根本原因

処理モデルの選択を設計時に一律に決めてしまい、リクエストの特性に応じた動的な判断を行わないことが原因である。`[F4]` レイテンシ予算はリクエストの種類によって異なるが、この多様性を無視して「全部同じ」にすると、必ずどちらかの端で問題が生じる。

また、同期と非同期のハイブリッド構成は実装が複雑になるため、「どちらか一方に揃える」方がアーキテクチャとして単純で管理しやすいという誘惑がある。

## 発見方法

- **レイテンシ分布の二峰性**: P50とP99の差が大きい場合、短いリクエストと長いリクエストが混在している証拠である
- **タイムアウト率**: 同期処理でタイムアウトが発生しているか確認する
- **不要な待ち時間**: 即答可能なリクエストの応答時間がインフラのオーバーヘッドで支配されていないか確認する
- **メトリクス**: `request_duration_p50` vs `request_duration_p99`、`timeout_rate`、`queue_wait_time`

## 対策

### ステップ1: リクエスト処理時間を予測・分類する

リクエストの種類や入力サイズから処理時間を予測し、「短い（数秒以内）」と「長い（数十秒以上）」に分類する。

### ステップ2: ハイブリッド構成を導入する

短いリクエストは同期で即応答し、長いリクエストは非同期ジョブに昇格させる。クライアントには途中経過を通知する仕組みを提供する。

### ステップ3: 昇格閾値を調整する

同期→非同期の昇格閾値を `[F4]` レイテンシ予算に基づいて設定し、モニタリングで最適化する。

```python
# ハイブリッド処理の例
async def handle_request(request):
    estimated_time = estimate_processing_time(request)

    if estimated_time < SYNC_THRESHOLD:  # 例: 5秒
        # 同期処理: 即応答
        return await process_sync(request)
    else:
        # 非同期に昇格: ジョブIDを返す
        job_id = await enqueue_job(request)
        return {"status": "processing", "job_id": job_id}
```

## 具体例

### Before（問題のある状態）

```python
# パターンA: 全同期 — 長いリクエストがタイムアウト
@app.post("/agent")
def handle(request):
    result = agent.run(request.prompt)  # 5秒〜5分
    return result  # ロードバランサが30秒でタイムアウト

# パターンB: 全非同期 — 短いリクエストが遅い
@app.post("/agent")
def handle(request):
    job_id = queue.enqueue(agent.run, request.prompt)
    return {"job_id": job_id}  # 「今何時？」にも2秒待ち
```

### After（改善後）

```python
@app.post("/agent")
async def handle(request):
    estimated = estimate_duration(request)

    if estimated.seconds < 5:
        # 短いリクエスト: 同期で即応答
        result = await agent.run(request.prompt, timeout=10)
        return {"result": result}
    else:
        # 長いリクエスト: 非同期に昇格
        job = await create_job(request.prompt, budget=estimated)
        return {"job_id": job.id, "poll_url": f"/jobs/{job.id}"}
```

## 関連するアンチパターン

- [無限・過大タイムアウト](01-infinite-timeout.md) — 全同期の場合にタイムアウト問題が複合する
- [リトライストーム](09-retry-storm.md) — 同期タイムアウトがリトライを誘発する

## 関連パターン

- [#58 Sync Facade over Async Core](../patterns/01-execution/58-sync-facade-over-async-core.md) — 同期/非同期のハイブリッド構成
- [#1 Request-to-Job Gateway](../patterns/01-execution/01-request-to-job-gateway.md) — リクエスト受付とジョブ管理の分離
- [#7 Streaming Progress](../patterns/01-execution/07-streaming-progress.md) — 非同期処理の途中経過通知
