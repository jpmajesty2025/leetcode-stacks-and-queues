🏆 LeetCode Deep Dive: Find the Most Competitive Subsequence

Ever wondered how to pick the "smallest looking" subsequence of a fixed length from an array? That's exactly what LeetCode 1673 asks:

Given nums and k, return the most competitive subsequence of size k — the one that is lexicographically smallest among all subsequences of that length.

Example:
Input: nums = [2,4,3,3,5,4,9,6], k = 4
Output: [2,3,3,4]

💡 The key insight: this is a greedy + monotonic stack problem in disguise.

We build our answer left to right, maintaining a stack. While the current number is smaller than the top of the stack, AND we still have enough leftover elements to reach length k, we pop the stack — trading a "worse" earlier choice for a "better" one now. Then we push the current number.

At the end, we simply truncate the stack to length k.

```python
def most_competitive(nums: list[int], k: int) -> list[int]:
    stack = []
    to_remove = len(nums) - k

    for num in nums:
        while stack and to_remove > 0 and stack[-1] > num:
            stack.pop()
            to_remove -= 1
        stack.append(num)

    return stack[:k]
```

⚡ Why it's optimal:
- Time: O(n) — each element is pushed once and popped at most once.
- Space: O(n) for the stack.

This is the same pattern used in classics like "Remove K Digits" and "132 Pattern" — recognizing it once means solving a whole family of problems.

🧪 On the engineering side, I validated the solution with:
- Parametrized unit tests covering edge cases (single element, descending/ascending arrays, duplicates, k = length)
- Property-based testing with Hypothesis, cross-checked against a brute-force oracle over all possible k-length subsequences
- Invariant checks confirming the output is always a valid, order-preserving subsequence of the input

Greedy algorithms often feel like magic — but a monotonic stack is usually the disciplined structure hiding underneath. 🔑

#LeetCode #Algorithms #DataStructures #Python #SoftwareEngineering #CodingInterview #ProblemSolving #TechCommunity #ComputerScience #GreedyAlgorithms
