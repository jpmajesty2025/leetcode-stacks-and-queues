# ⚡ Counting "Leftmost-Is-Minimum" Subarrays in O(n) With a Monotonic Stack

**Last time**, we counted contiguous subarrays where the leftmost element is the minimum of the range, using a direct O(n²) approach — for each start index, extend right until something smaller breaks the streak.

**The reframe:** A subarray starting at index `i` stays valid for every end point up to (but not including) the first *later* index `j` where `nums[j] < nums[i]`. Once a strictly smaller value shows up, `nums[i]` can no longer be the minimum of any range that includes it. So the number of valid subarrays starting at `i` is exactly:

```
next_smaller_index(i) - i
```

...where `next_smaller_index(i)` defaults to `n` (the array length) if no smaller element ever appears.

That's the classic **"next strictly smaller element to the right"** pattern — the same shape behind problems like Daily Temperatures and Stock Span — and it has a textbook O(n) solution: a monotonic increasing stack of pending start indices.

```python
def valid_subarrays(nums: list[int]) -> int:
    count = 0
    pending_indices: list[int] = []

    for index, value in enumerate(nums):
        while pending_indices and nums[pending_indices[-1]] > value:
            start = pending_indices.pop()
            count += index - start
        pending_indices.append(index)

    n = len(nums)
    while pending_indices:
        start = pending_indices.pop()
        count += n - start

    return count
```

**Walking through `[1, 4, 2, 5, 3]`:**

- Push `1` → stack `[1]`.
- `4 >= 1`, no pop. Push `4` → stack `[1, 4]`.
- `2 < 4`: pop `4` (index 1), settle `count += 2 - 1 = 1`. `2 >= 1` (top is now `1`), stop. Push `2` → stack `[1, 2]`.
- `5 >= 2`, no pop. Push `5` → stack `[1, 2, 5]`.
- `3 < 5`: pop `5` (index 3), settle `count += 4 - 3 = 1`. `3 >= 2` (top is now `2`), stop. Push `3` → stack `[1, 2, 3]`.
- End of array reached. Flush remaining stack against `n = 5`: pop `3` (index 4) → `+= 5 - 4 = 1`; pop `2` (index 2) → `+= 5 - 2 = 3`; pop `1` (index 0) → `+= 5 - 0 = 5`.
- Total: `1 + 1 + 1 + 3 + 5 = 11`. ✅ Matches the brute force result.

**Why it's O(n):** each index is pushed exactly once and popped at most once (either mid-loop or during the final flush), so the total work across the entire run is linear — despite the nested `while` loop, which can look deceptively like O(n²) at first glance.

Same underlying trick, three different LeetCode problems. Once you spot "find the first index where some condition breaks going forward," the monotonic stack should be your default reach. 🥞

What's the last problem where you swapped an O(n²) scan for a monotonic stack? 👇

#LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #LearningInPublic #CleanCode
