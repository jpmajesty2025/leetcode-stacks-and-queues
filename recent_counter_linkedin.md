# Counting Recent Events with a Deque

A common streaming-data problem is to count how many events occurred within a recent time window.

Assume each request arrives with a monotonically non-decreasing timestamp in milliseconds. For every new request at time `t`, return the number of requests in the inclusive interval:

```text
[t - window_ms, t]
```

With the default window of 3000 milliseconds (for instance):

```text
ping(1)     -> 1
ping(100)   -> 2
ping(3001)  -> 3
ping(3002)  -> 3
```

At `t = 3002`, the request at `1` has expired because it falls just outside the interval `[2, 3002]`.

Python's `collections` module offers a double-ended queue structure, called a `deque`. It is a sequence optimized to enqueue or dequeue from either end in O(1) constant time. And it is a natural fit for this problem:

```python
from collections import deque


class RecentCounter:
    def __init__(self, window_ms: int = 3000) -> None:
        if window_ms <= 0:
            raise ValueError("window_ms must be positive")

        self._window_ms = window_ms
        self._requests: deque[int] = deque()

    def ping(self, t: int) -> int:
        while self._requests and self._requests[0] < t - self._window_ms:
            self._requests.popleft()

        self._requests.append(t)
        return len(self._requests)
```

## Why a deque works

Timestamps arrive in increasing order, so the oldest requests are always at (or immediately adjacent to) the front.

For each new request:

1. Remove expired timestamps from the left.
2. Add the new timestamp on the right.
3. The deque length is the answer.

The inclusive boundary is important:

- A timestamp equal to `t - window_ms` remains.
- A timestamp smaller than `t - window_ms` expires.

## Complexity

A single call can remove several expired timestamps ,includsing repeats, which are allowed as per the monotone nature of the timestamps. Thus, its worst-case time is `O(n)`. But every timestamp enters the deque once and leaves once.

That gives:

- **Amortized time per request:** `O(1)`
- **Space:** `O(w)`, where `w` is the number of requests still inside the active window

Making `window_ms` configurable keeps the same algorithm useful for short bursts, rate-limit windows, monitoring dashboards, and event-stream analytics.

What other real-world problems can you model as a sliding window?

#LearningInPublic #Python #DataStructures #Algorithms #Deque #SlidingWindow #StreamingData #LeetCode #SoftwareEngineering #ProblemSolving #CodingInterview