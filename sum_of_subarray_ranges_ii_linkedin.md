# Sum of Subarray Ranges: From O(n²) to O(n) with a Monotonic Stack

Problem statement:

> Given an integer array `nums`, the range of a subarray is `max - min` of its elements. Return the sum of ranges over every contiguous subarray.

The brute-force approach is the natural first pass: for every starting index, extend the subarray one element at a time, tracking the running min and max, and add `max - min` at each step.

```python
def sum_subarray_ranges(nums: list[int]) -> int:
    n = len(nums)
    total_sum = 0

    for i in range(n):
        min_val = nums[i]
        max_val = nums[i]

        for j in range(i, n):
            min_val = min(min_val, nums[j])
            max_val = max(max_val, nums[j])
            total_sum += (max_val - min_val)

    return total_sum
```

It is correct and easy to reason about, but it is O(n²) — every pair of start/end indices is visited explicitly.

## The key insight: split the range in two

`range = max - min`, and sum distributes over subtraction:

```
sum_of_ranges = sum_of_maxima - sum_of_minima
```

So instead of one hard problem, we have two easier, *independent* ones: "sum of subarray maxima" and "sum of subarray minima." Each can be solved in O(n) with a monotonic stack.

## Sum of subarray minima (and maxima) in O(n)

For each index `j`, define `sum_min_ending_at(j)` as the sum of the minimum of every subarray that *ends* at `j`. If we can compute this for every `j` in O(1) amortized, the total sum of subarray minima is just the running sum over all `j`.

A monotonic increasing stack of `(value, count)` pairs makes this possible: `count` tracks how many subarrays ending at the current index share that value as their minimum. When a new element is smaller than the stack's top, it "absorbs" that entry's count and contribution, because the new, smaller element becomes the minimum for all those subarrays too.

```python
def sum_subarray_ranges(nums: list[int]) -> int:
    min_stack: list[tuple[int, int]] = []
    max_stack: list[tuple[int, int]] = []

    min_running_total = 0
    max_running_total = 0
    min_dot = 0
    max_dot = 0

    for num in nums:
        min_count = 1
        while min_stack and min_stack[-1][0] >= num:
            prev_num, prev_count = min_stack.pop()
            min_count += prev_count
            min_dot -= prev_num * prev_count
        min_stack.append((num, min_count))
        min_dot += num * min_count
        min_running_total += min_dot

        max_count = 1
        while max_stack and max_stack[-1][0] <= num:
            prev_num, prev_count = max_stack.pop()
            max_count += prev_count
            max_dot -= prev_num * prev_count
        max_stack.append((num, max_count))
        max_dot += num * max_count
        max_running_total += max_dot

    return max_running_total - min_running_total
```

One pass, two mirrored stacks (min-tracking and max-tracking), each amortized O(1) per element because every push is eventually popped at most once.

## Brute force vs. monotonic stack

| Approach | Time | Extra space | Main advantage |
|---|---:|---:|---|
| Nested loop | O(n²) | O(1) | Directly mirrors the problem statement |
| Monotonic stack (min + max) | O(n) | O(n) | Scales to large inputs |

Both are valid solutions to the same problem, with different trade-offs.

The nested-loop version is the natural place to start: it is easy to write, easy to verify against the examples, and makes the problem's structure obvious.

The monotonic-stack version pays a small amount of extra space for a much better asymptotic bound — essential once `n` grows past a few thousand elements, since the nested loop's runtime grows quadratically.

The real lesson is the decomposition trick: whenever a quantity is defined as `max - min` (or any difference/combination of two extremal values) summed over subarrays, check whether you can split it into two independent extremal-sum subproblems. Each one, individually, tends to have a clean monotonic-stack solution.

Which do you reach for first in an interview: the O(n²) simulation, or would you go straight for the decomposition?

#Python #Algorithms #DataStructures #MonotonicStack #LeetCode #CodingInterview #ProblemSolving #SoftwareEngineering #Tradeoffs