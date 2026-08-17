# 🧮 Counting "Leftmost-Is-Minimum" Subarrays — The Brute Force

**The setup:** Given an array of integers, count every non-empty contiguous subarray where the leftmost element is not larger than any other element in that subarray — i.e., the first element is the minimum of the range.

Example: `[1, 4, 2, 5, 3]` → `11`. The valid subarrays are `[1]`, `[4]`, `[2]`, `[5]`, `[3]`, `[1,4]`, `[2,5]`, `[1,4,2]`, `[2,5,3]`, `[1,4,2,5]`, `[1,4,2,5,3]`.

**The direct approach:** For each starting index, try to extend the subarray one element at a time. Every extension is valid as long as the new element is `>=` the starting element — the moment something smaller shows up, the leftmost element is no longer the minimum, so stop extending.

```python
def valid_subarrays(nums: list[int]) -> int:
    count = 0
    n = len(nums)

    for i in range(n):
        count += 1  # the single-element subarray [nums[i]] is always valid

        for j in range(i + 1, n):
            if nums[j] >= nums[i]:
                count += 1
            else:
                break

    return count
```

**Why this works:** every single element is trivially valid on its own. Extending right stays valid only while the running elements stay `>=` the anchor — so the inner loop naturally stops at the first violation, exactly matching the problem's definition.

**The catch:** this is O(n²) in the worst case. Feed it a non-decreasing array like `[1, 2, 3, 4, 5]`, and every starting index's inner loop runs all the way to the end — 5+4+3+2+1 = 15 total checks for `n = 5`, and it only gets worse as `n` grows.

It's correct, it's readable, and for small inputs it's perfectly fine. But once you start thinking about "the first element to break this pattern," a bell should be ringing — that's the exact shape of a "next smaller element" problem, and there's a linear-time way to answer it using a monotonic stack. More on that next. 👀

What's your instinct — brute force first, or reach for the pattern-matching move immediately? 👇

#LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #LearningInPublic #CleanCode
