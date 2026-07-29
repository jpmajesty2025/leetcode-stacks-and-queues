# Finding the Next Warmer Day with a Monotonic Stack

The **Daily Temperatures** problem asks:

> For each day, how many days must you wait until a strictly warmer temperature arrives?

If no future day is warmer, return `0`.

Example:

```text
Temperatures: [73, 74, 75, 71, 69, 72, 76, 73]
Wait days:    [ 1,  1,  4,  2,  1,  1,  0,  0]
```

A straightforward solution checks every future day for every temperature. That works—but can take **O(n²)** time.

A better approach uses a **monotonic decreasing stack** of indices.

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    pending_indices: list[int] = []
    wait_days = [0] * len(temperatures)

    for day, temperature in enumerate(temperatures):
        while pending_indices and temperatures[pending_indices[-1]] < temperature:
            previous_day = pending_indices.pop()
            wait_days[previous_day] = day - previous_day

        pending_indices.append(day)

    return wait_days
```

## The core idea

The stack holds days that are still waiting for a warmer temperature.

It is kept in decreasing temperature order:

```text
top of stack → most recent unresolved day
```

When a new temperature arrives:

1. Compare it to the unresolved day at the top.
2. If it is warmer, today is the first warmer day for that earlier temperature.
3. Record the day difference and remove the resolved index.
4. Keep going until the stack is decreasing again.
5. Add today as a new unresolved day.

The word **strictly** matters. Equal temperatures do not resolve an earlier day:

```text
[70, 70, 71] -> [2, 1, 0]
```

## Why this is efficient

Every index:

- enters the stack once;
- leaves the stack at most once.

So the total work is:

- **Time:** `O(n)`
- **Space:** `O(n)` in the worst case

This is a useful general pattern: when you need the **next greater element** to the right, consider a monotonic stack before reaching for nested loops.

Where else have you seen “next greater,” “next smaller,” or “first future event” patterns?

#Python #Algorithms #DataStructures #MonotonicStack #Stack #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #CleanCode