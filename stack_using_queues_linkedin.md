# 🔄 Building a LIFO Stack Out of Nothing But FIFO Queues

**The setup:** Implement a stack — `push`, `pop`, `top`, `empty` — using *only* queue operations: push to the back, pop/peek from the front, size, and empty check. No indexing into the middle, no popping from the back. A queue is fundamentally FIFO (first-in-first-out); a stack is fundamentally LIFO (last-in-first-out). How do you get LIFO behavior out of a structure that's wired for the opposite?

**The key insight:** you can't change *where* things go in — `push` always lands at the back of the queue, same as always. So instead, do the reordering when it's time to come *out*. Right before a `pop` or `top`, rotate the queue so that the most recently pushed element ends up at the *front* — the only end a queue lets you read from.

**Walking through `push(1), push(2), push(3)`, then `pop()`:**

- After the three pushes: queue = `[1, 2, 3]` (front → back). `3` was pushed last, but it's sitting at the *back* — the wrong end for a queue-only read.
- To `pop()`, rotate everything *except* the last-pushed element to the back: pop `1` from front, push it to back → `[2, 3, 1]`. Pop `2` from front, push it to back → `[3, 1, 2]`.
- Now `3` — the true top of the stack — is at the front. Pop it off directly: returns `3`. Queue is left as `[1, 2]`, in its original relative order.

That rotation is the entire trick: `n - 1` front-pops-and-back-pushes reposition the last-in element to the front, without ever touching the interior of the queue directly.

**Where the original draft went wrong — a hidden O(n²):**

The first version used a plain Python `list` and called `list.pop(0)` to simulate "pop from front." That looks like a queue operation, but `list.pop(0)` is secretly **O(n)** — removing from the front of a list means shifting every remaining element one slot to the left. Since the rotation loop calls it `n - 1` times, the *intended* O(n) rotation was quietly costing **O(n²)**. The fix: swap the list for `collections.deque`, whose `popleft()` is O(1) — same standard queue operations, but now the underlying cost model actually matches what the algorithm looks like it's doing.

**The algorithm:**

```python
from collections import deque


class MyStack:

    def __init__(self):
        self.queue = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)

    def _rotate_last_to_front(self) -> None:
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        self._rotate_last_to_front()
        return self.queue.popleft()

    def top(self) -> int:
        self._rotate_last_to_front()
        top_element = self.queue[0]
        self.queue.append(self.queue.popleft())
        return top_element

    def empty(self) -> bool:
        return not self.queue
```

Note `top()` still has to rotate the peeked element back to the *front* afterward (not just leave it at the back) — otherwise a second `top()` call, or a `push()` right after, would see the wrong element as the new front, silently corrupting the simulated stack's order.

**Complexity:** `push` and `empty` are O(1). `pop` and `top` are O(n) each, dominated by the rotation. This is the standard trade-off for the *single-queue* version of this problem — the harder LeetCode follow-up. (A two-queue version can push, storing new elements to always end up at the front, but pays the O(n) cost on `push` instead of `pop`/`top` — same total work, shifted to a different operation.)

Ever had a "clever" trick quietly hide an O(n²) inside what looked like an O(n) loop? What tipped you off? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
