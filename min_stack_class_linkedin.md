# 📉 Getting the Minimum of a Stack in O(1) — Without Rescanning Every Time

**The setup:** Design a stack that supports `push`, `pop`, `top`, and `getMin` — and every single one of those must run in O(1) time. The catch is `getMin`: a plain stack has no idea what its minimum is without scanning the whole thing, which is O(n). So how do you know the minimum instantly, even as elements come and go?

**The naive instinct:** track a single `min` variable that updates on every `push`. That works going *down* — but what happens when you `pop` the current minimum off? You'd need to rescan the remaining stack to find the *new* minimum, right back to O(n).

**The key insight:** don't track one minimum — track the *history* of minimums, using a second stack. Every time you push a value that's `<=` the current minimum, also push it onto a `min_stack`. When you pop a value that happens to be the current minimum, pop it off `min_stack` too — which automatically reveals the previous minimum, already sitting there.

**Walking through the classic example:**

```
push(-2)  → stack=[-2]        min_stack=[-2]
push(0)   → stack=[-2, 0]     min_stack=[-2]      (0 > -2, not pushed to min_stack)
push(-3)  → stack=[-2, 0, -3] min_stack=[-2, -3]   (-3 <= -2, pushed)
getMin()  → -3
pop()     → stack=[-2, 0]     min_stack=[-2]       (-3 was the min, popped from both)
top()     → 0
getMin()  → -2                (revealed instantly — no rescan needed)
```

**Why `<=` and not strictly `<` in the push condition?** That's how you handle potential duplicate minima. A min is not necessarily global! Consider pushing `1, 2, 1`: both `1`s tie for the minimum. If we only pushed *strictly smaller* values onto `min_stack`, the second `1` would never make it on — and popping the second `1` off the main stack wouldn't touch `min_stack`, silently leaving the *wrong* minimum's bookkeeping intact by coincidence, but breaking the moment the values weren't identical. Using `<=` means every value tied for the minimum gets its own entry in `min_stack`, so `pop` always unwinds correctly regardless of ties.

**The algorithm:**

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        if not self.min_stack or value <= self.min_stack[-1]:
            self.min_stack.append(value)

    def pop(self) -> None:
        value = self.stack.pop()
        if value == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

Note that `pop`, `top`, and `getMin` don't guard against an empty stack — the problem guarantees they're only ever called on a non-empty one, so there's no need to swallow that precondition behind a silent `None`. If it's ever violated, Python's own `IndexError` says so immediately, which is more honest than a bug that quietly does nothing.

**Complexity:** O(1) time for every operation — no exceptions, no amortization hand-waving. O(n) space in the worst case, if every element pushed is a new minimum (e.g. a strictly decreasing sequence), so `min_stack` grows in lockstep with `stack`.

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
