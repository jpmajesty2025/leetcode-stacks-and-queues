# Online Stock Span: A Monotonic Stack That Remembers Its Own Work

Monotonic stack problems often process a fixed array all at once. **Online Stock Span** asks for something different: answer each query the moment it arrives, with no knowledge of what comes next.

## The problem

Design a `StockSpanner` class where each call to `next(price)` returns the span: the number of consecutive days, ending today, where the price was less than or equal to today's price.

```text
calls:  100  80  60  70  60  75  85
spans:    1   1   1   2   1   4   6
```

The `75` on day six has a span of 4 because the three days before it (`60, 70, 60`) were all less than or equal to `75`, and that streak stretches back to include `75` itself.

The brute-force approach rescans the entire price history on every call, checking backward day by day. That is **O(n)** per query and **O(n²)** overall for `n` calls.

## The key insight: spans compose

If the previous day's price was less than or equal to today's, today's span doesn't just include that one day — it inherits *that day's entire span*, because everything within reach of the previous day is, by definition, also less than or equal to today's price.

That means a stack of `(price, span)` pairs can absorb dominated history in bulk instead of walking it day by day:

- While the top of the stack has a price less than or equal to today's price, pop it and add its span to today's running total.
- Push `(today's price, accumulated span)`.
- Return that span.

## Why this is O(1) amortized

Each `(price, span)` pair is pushed exactly once and popped at most once, ever. A single call might pop many entries, but each entry can only ever be popped a single time across the entire lifetime of the spanner. Total work across all calls is bounded by the number of pushes: `O(n)` for `n` calls, or `O(1)` amortized per call.

- **Time:** `O(1)` amortized per `next()` call
- **Space:** `O(n)` for the stack in the worst case (strictly increasing prices)

## The reusable pattern

This is the "online" cousin of problems like next greater element: instead of precomputing an answer for a fixed array, the stack maintains just enough compressed history to answer the next query in constant amortized time, no matter how long the stream runs. Any streaming problem asking "how far back does this streak go?" is a candidate for this same concept.

#Python #Algorithms #DataStructures #Stack #MonotonicStack #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #LearningInPublic
