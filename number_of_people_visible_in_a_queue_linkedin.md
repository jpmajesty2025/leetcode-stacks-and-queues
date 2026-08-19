👀 LeetCode Deep Dive: Number of Visible People in a Queue

Here's a fun spatial-reasoning problem that turns out to be a monotonic stack classic in disguise.

The problem (LeetCode 1944): n people stand in a queue with distinct heights. Person i can see person j (to their right) only if everyone standing between them is shorter than BOTH of them. Return, for every person, how many people to their right they can see.

Example:
Input: heights = [10,6,8,5,11,9]
Output: [3,1,2,1,1,0]

Person 0 (height 10) sees persons 1, 2, and 4 — but person 4 (height 11) blocks their view of everyone beyond.

💡 The key insight: process the queue from RIGHT to LEFT, maintaining a decreasing monotonic stack of heights.

For each person, moving right to left:
- Pop everyone shorter than them off the stack — they can see each of those people (since the current person is taller, they "see over" them).
- If anything remains on the stack after popping, that's one more visible person — the first taller (or equal-blocking) person acts as their view's boundary.
- Push the current person's index and move on.

```python
def can_see_persons_count(heights: list[int]) -> list[int]:
    n = len(heights)
    answer = [0] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and heights[i] > heights[stack[-1]]:
            answer[i] += 1
            stack.pop()
        if stack:
            answer[i] += 1
        stack.append(i)

    return answer
```

⚡ Why it's optimal:
- Time: O(n) — every index is pushed once and popped at most once, so the total work across the while loop is amortized linear.
- Space: O(n) for the stack.

This "process right-to-left with a monotonic stack" pattern shows up across a whole family of "next greater/visible/blocked" problems — once you spot the shape, the solution nearly writes itself.

🧪 On the engineering side, I validated the solution with:
- Parametrized unit tests covering both LeetCode examples plus edge cases (single person, strictly ascending/descending heights, small permutations)
- Property-based testing with Hypothesis, cross-checked against a brute-force O(n²) oracle that directly implements the "everyone between is shorter than both" definition
- Structural invariants: the last person always sees zero people, visible counts never exceed the people remaining to the right, and full-visibility cases are bounded by the tallest remaining height

A great reminder that "line of sight" problems in a 1D array almost always reduce to a monotonic stack once you find the right traversal direction. 🔑

#LeetCode #Algorithms #DataStructures #Python #SoftwareEngineering #CodingInterview #ProblemSolving #TechCommunity #ComputerScience #MonotonicStack
