🧠 LeetCode Deep Dive: Sum of Subarray Minimums

This is one of those problems where the "obvious" monotonic stack pattern hides a subtle trap that's easy to get wrong even when the overall approach is right.

The problem (LeetCode 907): given an array arr, sum up min(b) for every contiguous subarray b, modulo 10^9 + 7.

Example:
Input: arr = [3,1,2,4]
Output: 17
(Subarrays [3],[1],[2],[4],[3,1],[1,2],[2,4],[3,1,2],[1,2,4],[3,1,2,4] have minimums 3,1,2,4,1,1,2,1,1,1 → sum = 17)

💡 The key insight: for each element, count how many subarrays it is the minimum of, using a monotonic stack that tracks, for each value, "how many previous elements does this one dominate as the new minimum."

We maintain a stack of (value, count) pairs, where count = number of subarrays ending at this position for which this value is the minimum. When a new number arrives, we pop off every stack entry it beats, absorbing their counts (since this smaller number is now the minimum for those subarrays too).

⚠️ The subtle bug I caught while reviewing this: it's tempting to accumulate directly into your final answer variable while doing this pop/absorb bookkeeping. But there are two genuinely different quantities in play:
- The running sum of minimums of all subarrays ENDING at the current index (call it `dot`) — this is what the stack recurrence maintains and needs to add/subtract from as it pops.
- The overall answer, which is the SUM of `dot` across every index.

Collapsing these into a single variable silently drops most of the contribution — the code still runs, still looks reasonable, but returns a wrong answer (I traced [3,1,2,4] by hand and got 8 instead of 17 before the fix). This is exactly the kind of quiet logic bug that a brute-force oracle test catches instantly, but a quick glance at the code won't.

```python
def sum_subarray_mins(arr: list[int]) -> int:
    stack = []
    result = 0
    # dot tracks the sum of minimums of every subarray ending at the
    # current index; result accumulates dot across all indices.
    dot = 0
    mod = 10**9 + 7

    for num in arr:
        count = 1
        while stack and stack[-1][0] >= num:
            prev_num, prev_count = stack.pop()
            count += prev_count
            dot -= prev_num * prev_count
        stack.append((num, count))
        dot += num * count
        result += dot
        result %= mod

    return result
```

⚡ Why it's optimal:
- Time: O(n) — every element is pushed and popped from the stack at most once (amortized).
- Space: O(n) for the stack.

Compare that to the naive O(n²) approach of computing every subarray's minimum directly — the monotonic stack turns a quadratic problem into a linear one by never re-deriving a minimum we've already accounted for.

🧪 On the engineering side, I validated the fix with:
- Parametrized unit tests covering both LeetCode examples plus edge cases (single element, duplicates, ascending/descending arrays)
- Property-based testing with Hypothesis, cross-checked against a brute-force O(n²) oracle — this is the test that would have immediately caught the original bug
- Invariant checks: results are non-negative and lower-bounded by (global minimum × number of subarrays)

The real lesson here isn't just "know the pattern" — it's that a correctness bug can hide in code that looks clean and passes a casual read. A brute-force oracle test is cheap insurance against exactly that. 🔑

#LeetCode #Algorithms #DataStructures #Python #SoftwareEngineering #CodingInterview #ProblemSolving #TechCommunity #ComputerScience #MonotonicStack
