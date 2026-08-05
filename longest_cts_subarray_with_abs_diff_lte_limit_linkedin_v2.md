# Longest Subarray Within a Limit, Part 2: A Defensively Simpler Deque (and a Correction)

Last post ended with a challenge: trace `nums = [5, 1, 5, 5], limit = 3` by hand and think about whether comparing by value, instead of by index, could go wrong when duplicates are involved.

Here's an alternate design, and then the honest answer to that challenge.

## An alternate design: index-based deques

The same two-deque, dominance-based structure works if each deque stores **indices** into `nums` instead of values. Comparisons during insertion still look up `nums[index]`, but eviction from the front compares the stored index against the window's left boundary directly:

> Evict from the front once its index falls behind `left`.

No value lookup needed to decide what is leaving the window — the index is the window-membership check. This mirrors the deque in the sliding window maximum problem we tackled in a prior post. It is also the more defensively simple design: correctness doesn't depend on reasoning about duplicate values at all.

## The correction

I framed the original value-based version as brittle under duplicates. I went and checked that claim properly — exhaustively over small arrays with heavy duplication, and tens of thousands of random adversarial trials — against a brute-force oracle.

Zero mismatches. The value-based version is correct.

## Why it holds up

Both deques are built by appending at the back and removing only from the front or back — the relative order of surviving entries always matches the order they were inserted in. That gives an invariant:

> If the entry belonging to index `left` is still in a deque, it must be at the front.

So the check `nums[left] == deque[0]` is always asking the right question:

- If index `left`'s entry is still present, it's provably the front entry — the value comparison correctly matches and evicts it.
- If index `left`'s entry was already evicted earlier (dominated by a larger or smaller later value), the current front holds a value from that dominance chain — provably different from `nums[left]` — so the comparison correctly does *not* fire.

A stray value collision that evicts the wrong occurrence can't happen here. "Does the value match?" turns out to be equivalent to "does the index match?" for this specific construction.

## The takeaway

Both versions run in `O(n)` time and are correct. The index-based design isn't a bug fix — it's a simplification that removes the need to reason about the invariant at all. Sometimes the more defensive design is worth adopting even when the original wasn't actually broken.

#Python #Algorithms #DataStructures #Deque #MonotonicDeque #SlidingWindow #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #LearningInPublic
