# 💥 Simulating Asteroid Collisions Without Simulating Anything

**The setup:** You're given a row of asteroids as integers — sign is direction (positive = right, negative = left), absolute value is size. Same speed. Smaller one explodes on collision; equal sizes, both explode. Same-direction asteroids never meet. Left-movers that start left of all right-movers never collide. What survives?

**The naive instinct** is to simulate motion step by step and resolve overlaps — slow and fiddly.

**The key insight:** A collision only happens between a right-mover and the *first* left-mover that reaches it — not necessarily the next element, and only if that right-mover hasn't already been destroyed by an earlier left-mover. We model this with a stack of right-movers still "in play."

**`[5, 10, -5]`:** Push `5`, push `10` → stack `[5, 10]`. `-5` arrives: `10 > 5`, so `10` survives, `-5` dies. Stack: `[5, 10]`.

**Mutual assured destruction, `[8, -8]`:** Push `8`. `-8` arrives, equal size — both explode. Stack: `[]`.

**Multi-round, `[10, 2, -5]`:** Push `10`, push `2`. `-5` arrives: beats `2` (pop it), keeps going, then meets `10`: `10 > 5`, survives. Stack: `[10]`.

That last case shows why one `if` isn't enough — a left-mover can chew through several right-movers before it wins, ties, or loses. The stack keeps popping until it hits something bigger, something equal, or empties out.

**The algorithm** (code below 👇) runs in O(n) time — every asteroid is pushed once and popped at most once — and O(n) space.

What's your favorite example of a problem where a stack quietly replaces a full simulation? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
