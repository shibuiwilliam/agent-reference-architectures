---
title: "Forgetting and Expiration"
tags:
  - "Memory & Context Management"
  - "F8 Accountability & Regulation"
---

# #26 Forgetting and Expiration

!!! abstract "TL;DR"
    Assign **TTL (time-to-live) and freshness scores** to memories, automatically expiring and deleting outdated information.


<!-- BEGIN:GEN:meta -->
<details markdown="1">
<summary>Metadata (machine-readable) — #26 Forgetting and Expiration</summary>

| Field | Value |
|------|-----|
| **ID** | 26 |
| **Category** | 05-memory-context — Memory & Context Management |
| **Forces** | `[F8]` |
| **Dials** | memory-ttl |
| **Tradeoffs** | — |
| **Related Patterns** | #23, #25, #32 |
| **When to Use** | Customer data continuity, news/market information freshness, GDPR/data retention compliance |
| **When Not to Use** | Legal archives (retention is needed, not expiration); immutable master data |
| **Element Technologies** | Redis TTL, DynamoDB TTL, PostgreSQL partition pruning, cron/Cloud Scheduler |

</details>
<!-- END:GEN:meta -->

## Overview

If an agent keeps referencing last year's price sheet or old-version specifications as "correct information," providing incorrect estimates to customers is entirely plausible. As information accumulates in long-term memory, old facts contradict new ones, degrading agent judgment quality. Forgetting and Expiration sets an expiration date or freshness metric on every memory entry, excluding expired entries from search results or physically deleting them. By treating "forgetting" as an explicit design feature, memory hygiene is maintained.

!!! info "Position in Decision Framework"
    - **Driving Forces**: `[F8]` Accountability & Regulation
    - **Related Decisions**: [Tuning Dials](../../decisions/tuning-dials.md) — Memory TTL
    - **Decision Flow**: [Decision Flow](../../decisions/decision-flow.md)

## Design

The following metadata is attached to memory entries:

- **TTL**: Absolute expiration set at creation time (e.g., 90 days)
- **Freshness Score**: Updated on each reference; decays for long-unreferenced entries
- **Overwrite Flag**: Invalidates old versions when new memory is written with the same key

Expiration processing is implemented as batch (daily cleanup job) or query-time filter (excluding TTL-exceeded entries during search). When regulations `[F8]` mandate data retention periods, TTL is aligned to those periods, and deletion logs are kept as audit trails.

## Problem Solved

Without a forgetting mechanism, the following problems accumulate: (1) Old product specs, prices, and regulatory interpretations continue being referenced as "correct memories." (2) Total memory volume grows, reducing search precision (increased noise). (3) Risk of violating GDPR and similar data retention regulations. Like human memory, "appropriately forgetting" is necessary for maintaining both currency and regulatory compliance.

## When to Use / When Not to Use

- **When to Use**: Suitable for ongoing customer data management, news and market data where freshness matters, and systems subject to GDPR/privacy laws.
- **When Not to Use**: Not suited for records with legal retention obligations (archiving, not forgetting, is needed). Also unnecessary for reference data that does not change (master data, etc.).

## Element Technologies

- TTL Management: Redis TTL, DynamoDB TTL, PostgreSQL partition pruning
- Freshness Decay: Access-log-based scoring, exponential decay functions
- Deletion Jobs: cron / Cloud Scheduler batch deletion
- Audit: Retention of deletion logs (what was deleted, when, and why)

## Tuning (Dials)

- **TTL duration** — Too short loses useful memories; too long lets old information become noise / Deciding factor: `[F8]` / Match to the domain's information freshness. → [Tuning Dials](../../decisions/tuning-dials.md)

## Related Patterns

- [#23 Layered Memory](23-layered-memory.md) — Apply different expiration policies to each layer
- [#25 Memory Write Gate](25-memory-write-gate.md) — The gate that sets TTL at write time
- [#32 Agent Trace](../07-observability/32-agent-trace.md) — Records deletion history of expired memories as audit trails
