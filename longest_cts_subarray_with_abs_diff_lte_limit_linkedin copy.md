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

Unlike some earlier problems we've looked at that ask you to track **one** extreme value, this requires you to track **two at once**, and keep them in sync as the window grows and shrinks.


A brute-force approach checks every subarray and recomputes its max and min. That is **O(n²)** in the number of subarrays, and each max/min scan adds another factor of `n` on top. Unacceptable!

## The key insight: track the running max and min with a sliding window

A subarray is valid exactly when `max(window) - min(window) <= limit`. As the window's right edge grows by one element, we need to know the current max and min in **O(1)**, not by rescanning.

That is what a monotonic deque gives you:

```python
from collections import deque


def longest_subarray(nums: list[int], limit: int) -> int:
    if limit < 0:
        raise ValueError("limit must be non-negative")

    increasing: deque[int] = deque()  # indices with increasing nums values
    decreasing: deque[int] = deque()  # indices with decreasing nums values
    left = ans = 0

    for right in range(len(nums)):
        while increasing and nums[increasing[-1]] > nums[right]:
            increasing.pop()
        while decreasing and nums[decreasing[-1]] < nums[right]:
            decreasing.pop()

        increasing.append(right)
        decreasing.append(right)

        while nums[decreasing[0]] - nums[increasing[0]] > limit:
            left += 1
            if increasing[0] < left:
                increasing.popleft()
            if decreasing[0] < left:
                decreasing.popleft()

        ans = max(ans, right - left + 1)

    return ans
```

Two deques run in parallel:

- `increasing` keeps a monotonically increasing front-to-back sequence of values, so its front is the window minimum.
- `decreasing` keeps a monotonically decreasing sequence, so its front is the window maximum.

When the gap between them exceeds `limit`, the left edge advances until the window is valid again.

## Values vs. indices: a lesson in deque design

My first pass at this stored **values** in the deques and evicted from the front by comparing `nums[left]` against the front value. It worked, but it was fragile: with duplicate values, you cannot always tell whether the front of the deque corresponds to the element leaving the window, or to a different occurrence with the same value further inside it.

The fix — the same one used in `sliding_window_maximum.py` — is to store **indices**, not values. The invariant becomes unambiguous:

> Evict from the front once its index falls behind the window's left boundary.

No value comparison, no guessing which duplicate the front belongs to. The index is the ground truth for "is this candidate still inside the window?" Values only matter when comparing candidates during insertion.

## Why the time complexity is O(n)

Each index enters both deques exactly once, and can leave the back at most once and the front at most once. `left` only ever increases. Across the full pass:

- **Time:** `O(n)`
- **Space:** `O(n)` for the two deques in the worst case

## The reusable pattern

This is the same monotonic-deque discipline as sliding window maximum, applied twice:

- Maintain candidates in an order that makes the answer immediately available.
- Evict expired candidates from the front using **index**, not value, comparisons.
- Evict dominated candidates from the back using value comparisons.

When your sliding-window problem needs both an extreme value *and* precise tracking of which element is leaving the window, reach for index-based deques — value-based tracking is a trap waiting for duplicate inputs.

#Python #Algorithms #DataStructures #Deque #MonotonicDeque #SlidingWindow #LeetCodeHard #ProblemSolving #SoftwareEngineering #CodingInterview #LearningInPublic
