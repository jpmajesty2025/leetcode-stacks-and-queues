# Sliding Window Maximum: Why a Monotonic Deque Turns a Hard Problem into O(n)

Most of the stack and queue problems I have worked through recently have been Easy or Medium. **Sliding Window Maximum** is a meaningful step up: it is a LeetCode **Hard** problem because the obvious solution is easy to write—but too slow at scale.

## The problem

Given an array and a window size `k`, return the maximum value in every contiguous window of length `k`.

```text
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3

windows:
[ 1,  3, -1] -> 3
[ 3, -1, -3] -> 3
[-1, -3,  5] -> 5
[-3,  5,  3] -> 5
[ 5,  3,  6] -> 6
[ 3,  6,  7] -> 7

result = [3, 3, 5, 5, 6, 7]
```

A direct approach computes `max()` for each window.

That costs **O(n × k)**. When both the array and window are large, repeatedly scanning overlapping windows does unnecessary work.

## The key insight: preserve only viable maximum candidates

Use a `deque` containing **indices**, not values.

It maintains two invariants:

1. The indices are in increasing order from front to back.
2. Their corresponding values are in decreasing order.

The front therefore always identifies the maximum value in the current window.

```python
from collections import deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and the length of nums")

    maximums: list[int] = []
    candidate_indices: deque[int] = deque()

    for right, value in enumerate(nums):
        # Remove smaller values from the back: the newer value dominates them.
        while candidate_indices and nums[candidate_indices[-1]] < value:
            candidate_indices.pop()

        candidate_indices.append(right)

        # Remove the front index once it has left the active window.
        left = right - k + 1
        while candidate_indices and candidate_indices[0] < left:
            candidate_indices.popleft()

        if right >= k - 1:
            maximums.append(nums[candidate_indices[0]])

    return maximums
```

## Why can we discard smaller values?

Suppose a current candidate has value `3`, and a later element has value `5`.

```text
... 3 ... 5
```

The later `5` is larger **and** will remain in all future overlapping windows longer than the earlier `3`.

So the earlier `3` can never again become a window maximum. It is dominated and can be removed immediately.

That dominance argument is the heart of the algorithm.

## A brief walkthrough

For this partial stream:

```text
[1, 3, -1, -3, 5]
```

the candidate deque evolves conceptually as:

```text
1  -> [1]
3  -> [3]          # 3 removes 1 because it is larger and newer
-1 -> [3, -1]
-3 -> [3, -1, -3]
5  -> [5]          # 5 dominates all earlier candidates
```

At each completed window, the deque front is the answer.

## Why the time complexity is O(n)

The nested `while` loop may look suspicious at first.

But each index:

- enters the deque once;
- can be removed from the back at most once;
- can be removed from the front at most once.

No index returns after it is removed. Across the entire run, total deque operations are linear.

So the algorithm is:

- **Time:** `O(n)`
- **Space:** `O(k)` for candidates in the active window

## The reusable pattern

This problem is a powerful example of a **monotonic deque**:

- Maintain candidates in an order that makes the needed answer immediately available.
- Remove expired candidates from the front.
- Remove dominated candidates from the back.

The same pattern appears in sliding-window minimums, rolling analytics, rate monitoring, and streaming systems.

The challenge is not memorizing the code. It is learning to ask:

> Which older candidates can I prove will never matter again?

That question often reveals the path from repeated scanning to a linear-time solution.

#Python #Algorithms #DataStructures #Deque #MonotonicDeque #SlidingWindow #LeetCodeHard #ProblemSolving #SoftwareEngineering #CodingInterview