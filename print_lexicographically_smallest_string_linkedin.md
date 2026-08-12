# 🤖 LeetCode Breakdown: Making a Lexicographically Smallest String With a Robot

This one looks like a "just sort the string" problem at first glance — until you read the constraints closely and realize the robot's physical setup won't let you.

**The setup:** A robot has a string `s` and moves characters one at a time from the *front* of `s` onto a holding string `t`. At any point, it can also pop the *last* character off `t` and write it permanently to paper. Repeat until both `s` and `t` are empty. Return the lexicographically smallest string that ends up on paper.

**The key detail everyone should notice:** `t` only grows at the back and only shrinks from the back. That's not a queue — **that's a stack.** Characters go in from `s` in a fixed order, but they can only come *out* in last-in-first-out order.

**Why that matters — the "bdda" case:**

For `s = "bdda"`, the answer is `"addb"` — NOT the fully sorted `"abdd"`, even though `"abdd"` is smaller. Here's why that smaller string is physically unreachable:

- Push order onto `t` is fixed by `s`: `b`, then `d`, then `d`, then `a`.
- To write `'a'` first (as `"abdd"` requires), you have no choice but to first push `b`, `d`, `d` onto the stack — `a` doesn't even exist to the robot until the other three are already sitting in `t`. Fine so far.
- Pop `a` → paper = `"a"`. Stack `t` is now `[b, d, d]` bottom-to-top.
- But `s` is now empty — no more characters to feed in. The only move left is popping `t`, and the *top* of that stack is `d`, not `b`. You're forced to pop `d`, `d`, `b` in that exact order.
- Final result: `"a" + "ddb" = "addb"`. `'b'` is stuck at the bottom, buried under both `d`s, with no way to dig it out early.

So `"abdd"` isn't reachable — it would require popping `'b'` before the `d`s, but by the time `'b'` could be popped, two `d`s are already stacked on top of it. **The lexicographically smallest string on paper is bounded by what a stack can actually rearrange, not by what a full sort would produce.**

**The algorithm — a greedy monotonic stack:**

The trick is figuring out, for each character as it's pushed, whether it's ever safe to pop the stack top immediately. The rule: pop the top of the stack whenever it's `<=` every character that hasn't arrived yet. If nothing smaller is coming later, holding onto it any longer only risks it getting buried under something bigger — so write it now.

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

**A bug I actually caught while reviewing a draft of this:** the original comparison used the suffix-min *including* the current character instead of only the characters still to come. That off-by-one silently produced wrong answers on all three of the problem's own examples — a good reminder to always sanity-check against the stated examples before trusting a "looks right" greedy.

I verified the fix with property-based tests using Hypothesis, including a brute-force DFS oracle that exhaustively simulates every legal robot move sequence on short strings, plus invariants like "output is always a permutation of the input" and "output is bounded between the fully-sorted string and the naively-reversed string."

Have you run into other problems where the *data structure itself* — not the algorithm — is the real constraint on the answer? 👇

#LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode