# Longest Subarray Within a Limit, Part 3: Two Traces That Looked Pathological But Weren't

Parts 1 and 2 left one loose end: a proof that value-based eviction is correct, without ever watching it happen on a genuinely duplicate-heavy input. Here are two traces that look like they should break it — and don't.

## Trace 1: three identical values, then a forced eviction cascade

```text
nums = [3, 3, 3, 7, 3, 3]
limit = 0
```

Three `3`s arrive in a row. Since equal values never satisfy the strict `>`/`<` pop conditions, none of them evict each other from the back:

```text
after index 2: increasing = [3, 3, 3], decreasing = [3, 3, 3], left = 0
```

Three indices, same value, all coexisting — this is the case that looks dangerous. Then `7` arrives. With `limit = 0`, the window must shrink all the way past every `3`:

```text
index 0 leaves -> nums[0]==3 matches front of both deques -> evict -> left = 1
index 1 leaves -> nums[1]==3 matches front of both deques -> evict -> left = 2
index 2 leaves -> nums[2]==3 matches front of both deques -> evict -> left = 3
```

Three consecutive evictions, three coincidentally-identical values, and every single one evicts the correct occurrence — because they were inserted in order and never reordered.

## Trace 2: a duplicate that survives a shrink, then meets its twin

```text
nums = [5, 1, 5, 5]
limit = 3
```

`5` at index 0 enters both deques alone. `1` arrives and the window is forced to shrink once, evicting index 0's `5` correctly (only one `5` exists at that point — no ambiguity possible yet). Then a fresh `5` at index 2 enters both deques alone. Then another `5` at index 3 arrives:

```text
decreasing = [5, 5]   # indices 2 and 3, same value, both present
```

This is the moment that looks pathological — two `5`s sitting in the deque together. But no eviction is needed for the rest of the array: the window never has to shrink again, so the deque never has to decide which `5` is "the" front. The apparent hazard never actually gets exercised.

## The pattern behind both

Duplicates piling up in a deque is not, by itself, dangerous. What matters is what happens the *next* time an eviction is triggered — and by then, insertion order guarantees the front is always the oldest surviving index, duplicate value or not.

#Python #Algorithms #DataStructures #Deque #MonotonicDeque #SlidingWindow #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #LearningInPublic
