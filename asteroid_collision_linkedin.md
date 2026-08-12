# 💥 Simulating Asteroid Collisions Without Simulating Anything

**The setup:** You're given a row of asteroids, each represented by an integer. The sign tells you direction — positive moves right, negative moves left — and the absolute value is size. Every asteroid moves at the same speed. When two collide, the smaller one explodes; if they're equal size, both explode. Asteroids moving the same direction never meet. What survives?

The naive instinct is to actually *simulate* it — step asteroids forward in time, check for overlaps, resolve collisions, repeat. That works, but it's slow and fiddly to get right.

**The key insight:** A collision can only happen between a right-mover and a left-mover that comes *right after it* in the array — and only if the right-mover is still "in play" when the left-mover arrives. That's a perfect match for a stack: process asteroids left to right, and let the stack hold every right-mover that hasn't been destroyed yet.

**Walking through `[5, 10, -5]`:**

- Push `5` → stack `[5]`. Moving right, nothing to collide with yet.
- Push `10` → stack `[5, 10]`. Also moving right — no interaction with `5` since same direction.
- Now `-5` arrives, moving left. Compare against the stack top, `10`: `10 > 5`, so `10` survives and `-5` is destroyed on impact. Nothing pushed.
- Final stack: `[5, 10]`.

**Where it gets interesting — chained destruction, `[8, -8]`:**

- Push `8` → stack `[8]`.
- `-8` arrives. Compare against top `8`: equal size → **both explode**. Pop `8`, and `-8` is also destroyed (never pushed).
- Final stack: `[]`.

**And multi-round collisions, `[10, 2, -5]`:**

- Push `10` → stack `[10]`.
- Push `2` → stack `[10, 2]`.
- `-5` arrives. Compare against top `2`: `2 < 5`, so `2` is destroyed — pop it. But `-5` isn't done yet; it keeps checking the new top.
- Compare against new top `10`: `10 > 5`, so `10` survives and `-5` is destroyed.
- Final stack: `[10]`.

That last case is why a single `if` isn't enough — a left-mover can chew through *multiple* stacked right-movers before either surviving or being destroyed itself. The stack has to keep popping smaller asteroids until it either hits something bigger (the newcomer dies), something equal (both die), or empties out entirely (the newcomer survives and gets pushed).

**The algorithm:**

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for asteroid in asteroids:
        alive = True
        # A left-moving asteroid only collides with a right-moving one
        # already resting on top of the stack.
        while alive and stack and asteroid < 0 < stack[-1]:
            if stack[-1] < -asteroid:
                stack.pop()
            elif stack[-1] == -asteroid:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(asteroid)
    return stack
```

The condition `asteroid < 0 < stack[-1]` is doing double duty — it's checking that the incoming asteroid moves left AND that the stack top moves right, in one comparison chain. Once that's false (either the newcomer moves right, or the stack top also moves left, or the stack is empty), there's no more collision to resolve, and the asteroid is safe to push.

**Complexity:** O(n) time — every asteroid is pushed once and popped at most once, so the total work across the whole array is linear, even though it doesn't look that way from the nested loop. O(n) space for the stack.

What's your favorite example of a problem where a stack quietly does the work of a full simulation? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
