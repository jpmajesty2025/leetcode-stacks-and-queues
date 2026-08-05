# Longest Subarray Within a Limit: Two Monotonic Deques, One Sliding Window

## The problem

Given an array `nums` and an integer `limit`, find the length of the longest contiguous subarray where the difference between its maximum and minimum values is at most `limit`.

```text
nums = [8, 2, 4, 7]
limit = 4

[8, 2] -> |8-2| = 6 > 4   too wide
[2, 4] -> |2-4| = 2 <= 4  valid
[4, 7] -> |4-7| = 3 <= 4  valid

Longest valid subarray length: 2
```

Some stack and queue problems ask you to track a single extreme value. This one asks you to track two at once, and keep them in sync as the window grows and shrinks.

The brute-force approach checks every subarray and recomputes its max and min. That is **O(n²)** in the number of subarrays, and each max/min scan adds another factor of `n` on top.

## Key insight: track the running max and min with a sliding window

A subarray is valid exactly when `max(window) - min(window) <= limit`. As the window's right edge grows by one element, we need to know the current max and min in **O(1)**, not by rescanning.

Here is how parallel monotonic deques help:

- `increasing`: monotonically increasing front-to-back sequence of values -> front is the window minimum.
- `decreasing`: monotonically decreasing sequence, -> front is the window maximum.

When the gap between them exceeds `limit`, the left edge advances until the window is valid again.

## Why this works: dominance twice over:

The same dominance argument from sliding window maximum applies here:

- If a candidate value is smaller than a later value, it can never again be the window's maximum -> evict from the back of `decreasing`.
- If a candidate value is larger than a later value, it can never again be the window's minimum -> evist from the back of `increasing`.

One thing different: both deques store **values**, not indices. To advance the left edge, the code checks whether `nums[left]` — the value about to leave the window — matches the value sitting at the front of either deque, and evicts it if so.

## Why the time complexity is O(n)

Each element is pushed onto each deque once, and can be popped from the back at most once and from the front at most once. `left` only ever increases. Across the entire run:

- **Time:** `O(n)`
- **Space:** `O(n)` for the two deques in the worst case

## A question worth sitting with

This approach is quietly brittle. Try `nums = [5, 1, 5, 5], limit = 3` by hand and think about why comparing by value, instead of by index, could go wrong when duplicates are involved.

More on this in a follow-up post.

#LearningInPublic #Python #Algorithms #DataStructures #Deque #MonotonicDeque #SlidingWindow #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview
