# 📚 LeetCode Breakdown: Validate Stack Sequences

A problem that's less about finding a clever algorithm and more about trusting a greedy strategy is actually optimal.

**The problem:** Given two arrays, `pushed` and `popped` (a permutation of `pushed`), determine whether `popped` could be the result of some valid sequence of push/pop operations on an initially empty stack.

Input: `pushed = [1,2,3,4,5]`, `popped = [4,5,3,2,1]` → `true`
Input: `pushed = [1,2,3,4,5]`, `popped = [4,3,5,1,2]` → `false` (1 can't be popped before 2 — 2 was pushed after 1 and is still sitting on top of it)

**The naive worry:** with push/pop choices at every step, doesn't this need backtracking or search over all interleavings?

**The insight — greedy works, and here's the intuition why:** simulate it directly. Push elements from `pushed` one at a time. After every push, check: does the stack top match the *next* value we're expecting to pop? If yes, pop it immediately. Keep popping as long as it keeps matching.

Why is "pop the instant you can" always safe? Because delaying a pop that's currently legal can never help — it only risks burying that element under whatever gets pushed next, making it *harder* to reach later, never easier. If a valid pop order exists at all, popping greedily the moment it's possible will find it.

```python
def validate_stack_sequences(pushed: list[int], popped: list[int]) -> bool:
    stack = []
    j = 0
    for x in pushed:
        stack.append(x)
        while stack and stack[-1] == popped[j]:
            stack.pop()
            j += 1
    return not stack
```

At the end: if every element got popped in order, the stack is empty — `true`. If something never got matched, it's stuck on the stack — `false`.

**Complexity:** O(n) time, O(n) space — one pass, one stack, no backtracking needed despite the branching feel of the problem.

**How I verified it wasn't just "looks right":** rather than trust the greedy on faith, I checked it against an independent brute-force oracle — a DFS that explores *every* legal push/pop branch (not just the greedy one) — across hundreds of randomized permutation pairs. Zero mismatches. I also generated guaranteed-valid `popped` orders via a randomized push/pop simulator and confirmed the function always accepts them.

This is a nice example of a broader pattern: when a greedy choice is provably "never worse to make now," you don't need search — you can commit to it immediately and still get the correct answer, in linear time.

What's a problem where you initially reached for backtracking before realizing greedy was enough? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode