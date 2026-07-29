# From Deques to Watermarks: Sliding Windows Under Out-of-Order Events

A deque is a great fit for `RecentCounter` because of the guarantee that request timestamps arrive in strictly increasing order.

With ordered arrivals, the deque has two crucial properties:

1. New timestamps always go on the **right**.
2. Expired timestamps are always at the **left**.

So expiry is a simple `popleft()` loop:

```text
oldest ... newest
  left      right
```

If ordering weakens, the central question becomes:

> **Can I still know that the oldest unexpired event is at the front?**

If not, a plain FIFO deque is no longer enough.

---

# Event Time vs. Arrival Time

In real systems, an event may have:

- **Event time:** when the event actually occurred, e.g. `09:30:00.125`.
- **Processing/arrival time:** when your system received it, e.g. `09:30:01.300`.

They are often different because of network delay, batching, retries, clock skew, or upstream processing.

A late event might look like this:

```text
Arrival order:    event at 1000, event at 3000, event at 2000
Event-time order: event at 1000, event at 2000, event at 3000
```

The original `RecentCounter` problem assumes the two orders are identical.

---

# Full collapse: timestamps can arrive in arbitrary order

Suppose events can arrive with no timestamp-order guarantee:

```text
ping(10_000)
ping(2_000)
ping(8_000)
ping(9_500)
```

Now consider asking for the count in:

```text
[7_000, 10_000]
```

A deque ordered by arrival time might be:

```text
[10_000, 2_000, 8_000, 9_500]
```

The expired timestamp `2_000` is in the middle, not at the front. You cannot safely remove events only from the left.

## What does `ping(t)` mean now?

The original API becomes ambiguous.

Under monotonic timestamps, each call to `ping(t)` means:

> “An event occurred now, at the newest known event time `t`. Count the events in `[t - window, t]`.”

With unordered timestamps, calling `ping(2_000)` after `ping(10_000)` could mean either:

1. **A late-arriving historical event occurred at time 2,000**, or
2. **We are moving the query clock backward to 2,000**.

Those are very different semantics. Real event-stream systems usually use the first interpretation: the event is late, but the system’s processing clock does not go backward.

---

# Exact arbitrary-order solution: ordered range-query data structure

If exact counts are required after arbitrary timestamp insertion, organize state by **timestamp**, not arrival order.

## 1. Sorted map / balanced search tree

Maintain counts by timestamp:

```text
timestamp -> number of events at that timestamp
```

For example:

```text
2_000  -> 1
8_000  -> 1
9_500  -> 1
10_000 -> 1
```

To count events in `[7_000, 10_000]`, sum values in that key range.

A balanced binary-search tree supports insertion in roughly:

```text
O(log n)
```

A basic range query may cost:

```text
O(log n + k)
```

where `k` is the number of distinct timestamps in the interval, unless the tree is augmented with subtree counts.

## 2. Augmented balanced tree / order-statistics tree

Store, for each tree node:

- timestamp;
- count at that timestamp;
- aggregate count of its subtree.

Then compute:

```text
count(events with timestamp <= end)
-
count(events with timestamp < start)
```

This gives exact range counts in approximately:

```text
O(log n)
```

per insertion and query.

## 3. Segment tree or Fenwick tree

If timestamps are bounded or can be coordinate-compressed:

- map timestamps to integer indexes;
- maintain event counts;
- use prefix sums to answer range counts.

Typical complexity:

```text
insert: O(log M)
range count: O(log M)
```

where `M` is the timestamp-bucket/index domain.

This works especially well when events are bucketed by second, millisecond, or minute rather than requiring arbitrary timestamp precision.

## 4. Brute-force list

For low event volume, store all events and scan:

```python
sum(start <= timestamp <= end for timestamp in events)
```

This costs `O(n)` per query, but it may be the best practical choice for a small application or analytics script.

Data-structure sophistication should follow scale and latency requirements.

---

# The retention problem

With ordered timestamps, when you see time `t`, anything older than `t - window` can never matter again. Remove it.

With arbitrary late arrivals, you cannot necessarily discard an old event simply because it is old relative to the current observed maximum timestamp. A later query may ask about a historical interval that includes it.

You need an explicit retention policy, such as:

- retain all historical events;
- retain the last 30 days;
- retain events until a watermark says they are no longer needed;
- retain aggregated buckets rather than individual events.

This is why production stream processing uses **event-time windows**, **watermarks**, and **late-data policies**.

---

# Partial collapse: useful weaker guarantees

Real event streams often do not have fully arbitrary disorder. They are frequently mostly ordered, with known or patterned exceptions.

These weaker guarantees can support much more efficient approaches than fully arbitrary timestamp processing.

---

## Case 1: Bounded out-of-orderness

### Guarantee

An event can arrive late, but by no more than a known duration `L`.

If `max_seen_time` is the largest event timestamp seen so far:

```text
new event timestamp >= max_seen_time - L
```

Example with `L = 2 seconds`:

```text
Arrival order: 100, 101, 103, 102, 105, 104
```

Events are not strictly ordered, but no event is more than two seconds behind the current maximum.

### Real-world causes

- network jitter;
- asynchronous producers;
- micro-batching;
- multiple data sources with slightly different delays;
- distributed logs;
- telemetry from devices with intermittent connectivity.

### Solution: reorder buffer plus watermark

Keep a min-heap of waiting events ordered by event time.

Track:

```text
watermark = max_seen_event_time - allowed_lateness
```

Any event at or before the watermark is considered safe to process in event-time order, because no earlier event should still arrive under the guarantee.

Conceptually:

```text
receive event
    ↓
update max seen event time
    ↓
add event to min-heap ordered by event time
    ↓
process heap entries <= watermark
```

A min-heap gives:

```text
insert: O(log b)
remove earliest: O(log b)
```

where `b` is the number of buffered out-of-order events.

After emitting events in order, the original deque sliding-window algorithm can process the ordered stream.

### Trade-off

You exchange:

- **latency**: wait up to `L` before finalizing results;
- for **correct event-time ordering**.

This is a fundamental streaming-systems trade-off.

---

## Case 2: Mostly ordered, but no strict lateness bound

### Guarantee

Events are usually close to chronological order, but there is no hard promise.

For example:

- 99.9% arrive within two seconds;
- occasionally, an event may be minutes late;
- very rarely, hours late.

### Real-world examples

- mobile clients buffering events offline;
- third-party APIs retrying deliveries;
- delayed ETL jobs;
- market-data feed recovery;
- distributed services with transient outages.

### What changes

A heap can improve the common case, but it cannot guarantee correctness by itself. You need a policy for late events.

Common choices:

1. **Accept late events until a configured grace period**
   - Example: accept up to five minutes of lateness.
   - Update prior window results if needed.

2. **Drop excessively late events**
   - Useful when timeliness matters more than historical perfection.

3. **Route late events to a correction/reconciliation pipeline**
   - The real-time result may be approximate.
   - Batch processing later computes the authoritative result.

4. **Emit revisions**
   - A downstream consumer might receive:
     ```text
     “Window ending at 10:00:00 was previously 100; corrected to 101.”
     ```

---

## Case 3: Per-source ordering, but not global ordering

### Guarantee

Each producer’s events are ordered, but events across producers are interleaved arbitrarily.

Example:

```text
Producer A: 100, 105, 110
Producer B: 102, 103, 109
```

Each source is internally ordered, but the global arrival stream may be:

```text
A:100, A:105, B:102, B:103, B:109, A:110
```

### Real-world examples

- multiple trading venues;
- several application servers;
- IoT devices;
- Kafka partitions;
- logs emitted by multiple services;
- multiple market-data feeds.

### Solution: k-way merge

If you can read the next available event from each ordered source:

- maintain a min-heap containing the next event from each source;
- repeatedly process the globally earliest event;
- replenish from the source that produced it.

For `k` sources:

```text
per event: O(log k)
```

The merged stream is ordered, so the deque solution applies downstream.

If a source can stall indefinitely, you again need watermarks or timeout policies; otherwise, waiting for a missing earliest event can block progress.

---

## Case 4: Bounded number of inversions / local disorder

A more mathematical version of “mostly sorted” is:

> Each element is at most `k` positions from its position in sorted order.

Example:

```text
1, 3, 2, 5, 4, 7, 6
```

A min-heap of size roughly `k + 1` can restore sorted order in:

```text
O(n log k)
```

rather than a full sort:

```text
O(n log n)
```

This is useful for batch processing or known local disorder. In production streams, teams more commonly describe the guarantee in time units:

```text
events can be up to 30 seconds late
```

rather than positions.

---

## Case 5: Approximate time windows are acceptable

Sometimes exact counts for the exact last 3000 milliseconds are not necessary.

Examples:

- website traffic dashboards;
- telemetry monitoring;
- observability metrics;
- fraud-risk features where small delay or error is acceptable;
- high-rate rate analytics.

Use time buckets:

```text
bucket 10:00:00 -> 1,240 events
bucket 10:00:01 -> 1,317 events
bucket 10:00:02 -> 1,281 events
```

To estimate a three-second window, sum the relevant buckets.

Benefits:

- fixed memory by retention horizon;
- efficient aggregation;
- out-of-order arrivals can increment the appropriate bucket;
- lower storage than retaining every event.

Costs:

- precision depends on bucket size;
- bucket boundaries introduce approximation unless granularity is sufficiently fine or partial buckets are handled specially.

This leads toward time-series databases, stream processors, and approximate streaming algorithms.

---

# How the data-structure choice changes

| Arrival guarantee / requirement | Typical approach | Cost / trade-off |
|---|---|---|
| Strictly increasing timestamps | Deque | `O(1)` amortized per event |
| Bounded lateness | Min-heap reorder buffer + deque | latency up to allowed lateness; heap cost |
| Multiple ordered sources | K-way merge heap + deque | `O(log k)` per event |
| Arbitrary order, exact range counts | Augmented ordered map/tree | typically `O(log n)` insertion/query |
| Arbitrary order, bounded timestamp universe | Fenwick/segment tree | `O(log M)` |
| Arbitrary order, low scale | Scan stored events | simple; `O(n)` query |
| Approximate results acceptable | Time buckets / sketches | bounded memory; controlled error |
| Very late events permitted | Watermarks + correction policy | semantic/product decision required |

---

# A production API would separate ingestion from querying

The original LeetCode API combines two actions:

```python
ping(t) -> count
```

That works because each event time is the newest time.

For unordered event time, a clearer API would be:

```python
record(event_time: int) -> None
count_between(start: int, end: int) -> int
```

or:

```python
record(event_time: int) -> None
count_recent(reference_time: int, window_ms: int) -> int
```

This makes query semantics explicit.

For real-time systems, you may also expose:

```python
advance_watermark(event_time: int) -> None
```

That tells consumers:

> “No more events at or before this event time are expected.”

---

# What concepts are in play?

Several disciplines overlap.

## 1. Data structures and algorithms

Most directly:

- queues and deques;
- heaps / priority queues;
- balanced search trees;
- range queries;
- prefix sums;
- segment trees and Fenwick trees;
- amortized analysis;
- online algorithms;
- buffering and external-memory considerations at scale.

The original deque solution is an example of **amortized analysis**:

- one call may evict many events;
- across all calls, each event is appended once and removed once;
- total work is linear in the number of events.

## 2. Stream processing and distributed systems

This is the most directly practical field for weakened-ordering cases:

- event time versus processing time;
- late data;
- watermarks;
- allowed lateness;
- windowing;
- replay;
- idempotency and deduplication;
- exactly-once versus at-least-once delivery;
- state retention;
- eventual consistency;
- result corrections.

Systems such as Apache Flink, Spark Structured Streaming, Kafka Streams, and Beam formalize these ideas.

## 3. Queueing theory

Queueing theory matters when you ask:

- How long will events wait in the reorder buffer?
- How does bursty traffic affect backlog?
- What buffer capacity is needed?
- What is the probability that processing delay exceeds the lateness allowance?
- How does service rate compare with arrival rate?

Useful concepts include:

- arrival rate `λ`;
- service rate `μ`;
- utilization `ρ = λ / μ`;
- queue length;
- waiting time;
- burstiness;
- Little’s Law:

```text
L = λW
```

where:

- `L` is the average number of items in the system;
- `λ` is the average arrival rate;
- `W` is the average time an item spends in the system.

For example, if a reorder buffer intentionally waits two seconds and receives 10,000 events/second, it may need to hold roughly 20,000 events on average before considering variability.

Queueing theory does not choose the event-time semantics, but it helps size and reason about the system once those semantics are decided.

## 4. Probability and stochastic processes

These matter when arrivals and delays are uncertain rather than guaranteed.

Useful concepts include:

- stochastic arrival processes;
- Poisson processes as a simple baseline;
- renewal processes;
- inter-arrival-time distributions;
- random network delay;
- tail latency;
- order statistics;
- probability of lateness beyond a threshold;
- heavy-tailed distributions;
- stationarity and nonstationarity.

For example, you might choose an allowed lateness of five seconds because:

```text
P(network delay > 5 seconds) < 0.001
```

That is a probabilistic service-level choice, not an absolute guarantee.

Real delays are often bursty, correlated, and heavy-tailed, so a simple Poisson/exponential model is useful for intuition but rarely sufficient on its own.

## 5. Time series and signal processing

When you aggregate into time buckets or rolling windows, you are working with:

- rolling statistics;
- sampling intervals;
- smoothing;
- aggregation;
- window functions;
- accuracy/latency trade-offs.

---

# The Key Lesson

The algorithm is not determined only by the question, “How many events occurred recently?”

It is determined by the fuller contract:

```text
What does “recent” mean?
Which clock defines it?
How late can events arrive?
Must answers be exact?
Can earlier answers be corrected?
How long must event history be retained?
What latency and memory are acceptable?
```

With strictly ordered timestamps, a deque is ideal.

With bounded disorder, add a reorder buffer and watermarks.

With arbitrary disorder and exact historical queries, move to an ordered range-query structure.

With approximate analytics, use buckets and aggregation.

That progression—from a simple deque to event-time semantics, buffering, watermarks, and range queries—is a realistic path from a LeetCode queue problem into streaming systems and distributed-data engineering.
