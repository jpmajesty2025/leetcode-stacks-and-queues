# 🥞 LeetCode Breakdown: Implementing a Queue Using Two Stacks

**The problem:** Build a FIFO queue (`push`, `pop`, `peek`, `empty`) using only standard stack operations — push, pop/peek from the top, size, is-empty. No native queues, no cheating with a deque under the hood.

**The core tension:** stacks give you LIFO, you need FIFO. How do you flip the order without re-scanning on every operation?

**The trick:** use two stacks with complementary roles.
- `stack1` — the "inbox." Every `push()` just appends here.
- `stack2` — the "outbox." `pop()`/`peek()` read from here.

Whenever `stack2` is empty, dump *all* of `stack1` into it — popping from `stack1` and pushing onto `stack2` reverses the order, so the oldest element ends up on top of `stack2`, exactly where `pop()`/`peek()` need it.

```python
class MyQueue:
    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, x: int) -> None:
        self.stack1.append(x)

    def _transfer(self) -> None:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())

    def pop(self) -> int:
        self._transfer()
        return self.stack2.pop()

    def peek(self) -> int:
        self._transfer()
        return self.stack2[-1]

    def empty(self) -> bool:
        return not self.stack1 and not self.stack2
```

**Complexity:** amortized O(1) per operation. Each element gets moved between stacks at most once in its lifetime, no matter how many pushes/pops happen around it.

With some problems, such as this one, the focus is on *translating* one data structure's behavior into another's constraints.

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode