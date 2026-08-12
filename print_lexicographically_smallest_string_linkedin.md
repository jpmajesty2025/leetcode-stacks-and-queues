# 🤖 How to Make a Lexicographically Smallest String With a Robot

**The setup:** A robot has a string `s` and moves characters one at a time from the *front* of `s` onto a holding string `t`. At any point, it can also pop the *last* character off `t` and write it permanently to paper. Repeat until both `s` and `t` are empty. Return the lexicographically smallest string that ends up on paper.

Notice that it does not say "just sort the string." That's because the constraints on the robot prevent certain string patterns from being properly sorted. 

**The key detail:** `t` only grows at the back and only shrinks from the back. That's not a queue — **that's a stack.** Characters go in from `s` in a fixed order, but they can only come *out* in last-in-first-out order.

**Why that matters — the curious case of "bdda":**

For `s = "bdda"`, the answer is `"addb"` — NOT the fully sorted `"abdd"`, even though `"abdd"` is smaller. Here's why that smaller string is physically unreachable:

- Push order onto `t` is fixed by `s`: `b`, then `d`, then `d`, then `a`.
- To write `'a'` to paper first, we have to push `b`, `d`, `d` onto the stack.
- Pop `a` → paper = `"a"`. Stack `t` is now `[b, d, d]` bottom-to-top.
- But `s` is now empty -> we must flush the stack: popping `d`, `d`, then `b`.
- Final result: `"a" + "ddb" = "addb"`. `'b'` is stuck at the bottom, buried under both `d`s, with no way to dig it out early.

So `"abdd"` isn't reachable — it would require popping `'b'` before the `d`s, but by the time `'b'` could be popped, two `d`s are already stacked on top of it. **The lexicographically smallest string on paper is bounded by what a stack can actually rearrange.**

**The algorithm — a greedy stack, monotonic against the remaining suffix of the input string:**

The trick is figuring out, for each character as it's pushed, whether it's ever safe to pop the stack top immediately. The rule: pop the top of the stack whenever it's `<=` every character that hasn't arrived yet. If nothing smaller is coming later - which we check with the `suffix_min` list - then holding onto it any longer only risks it getting buried under something bigger — so write it now. Note how `suffix_min` is constructed from right to left, and how `suffix_min[i]` tells us the minimal character of `s[i:]`. This is what enables the greedy pop.

```python
def robot_with_string(s: str) -> str:
    n = len(s)
    stack = []
    result = []
    suffix_min = [None] * n
    suffix_min[-1] = s[-1]

    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(s[i], suffix_min[i + 1])

    for i in range(n):
        stack.append(s[i])
        while stack and (i + 1 >= n or stack[-1] <= suffix_min[i + 1]):
            result.append(stack.pop())

    return ''.join(result)
```

**Complexity:** O(n) time, O(n) space — one pass to build a suffix-minimum array, one pass to drive the stack.

Have you run into other problems where the *data structure itself* — not the algorithm — is the real constraint on the answer? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode