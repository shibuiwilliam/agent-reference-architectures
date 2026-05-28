---
title: "Memory TTL"
tags:
  - "Tuning Dial"
  - "F8 Accountability / Regulation"
---

# Memory TTL

!!! abstract "TL;DR"
    Set expiration dates on an agent's memories to maintain information freshness and ensure compliance.

## Overview

An agent keeps sending emails to a contact who left the company -- investigation reveals a six-month-old contact stored in memory was never updated. Memory becomes falsehood as it ages.

This dial determines the Time To Live (TTL) for the various types of memory an agent retains (session history, user preferences, learned patterns). If TTL is too short, useful memories are lost prematurely; if too long, incorrect decisions based on stale information or violations of data retention regulations can occur. Setting different TTLs per memory type is the standard practice.

## Why Adjustment Is Needed

An agent's memories become stale over time. Customer preferences, internal policies, and technical specifications change, so relying on old memories leads to incorrect decisions. Meanwhile, data protection regulations like GDPR require deletion of unnecessary data. Without TTL, memory grows indefinitely, also degrading search accuracy and increasing storage costs.

## Extremes of the Range

### Too Small

The agent forgets preferences and instructions the user just communicated, repeating the same questions. Lessons learned from past failures are also lost, causing the same mistakes to recur. Session continuity is broken, and the conversational experience deteriorates.

### Too Large

The agent acts based on changed facts (departed staff, deprecated APIs, updated policies). Unnecessary long-term retention of personal data may violate regulations. The memory store bloats, increasing search noise.

## Determining Forces

- `[F8]` Accountability / Regulation -- Regulatory requirements for data retention determine the upper limit of TTL

## Guidelines (Starting Point)

- Session memory: 1-24 hours (discard after conversation ends)
- User preferences: 30-90 days (periodic reconfirmation recommended)
- Learned patterns: 90-365 days (extend after validating effectiveness through evaluation)
- Personal data: Use the period required by law as the upper limit
- Expiring memories can optionally be compressed into summaries before removal

## Practical Adjustment

- Define TTL policies per memory type and configure automatic deletion jobs
- Sample memories nearing TTL expiration and measure the proportion that are still useful
- If "I already told you" feedback from users increases, consider extending TTL
- Coordinate with the data protection officer to keep TTL aligned with regulatory changes

## Related Patterns

- [#26 Forgetting and Expiration](../../decisions/dials/memory-ttl.md) -- Implementation pattern for adding expiration and freshness to memory
