# Next Greater Element: A Monotonic Stack, Read Backwards

Some problems get easier the moment you flip the direction you scan in!

## The problem

Given two arrays, `nums1` (a subset) and `nums2`, for every value in `nums1`, find the next element to its right in `nums2` that is strictly greater. If none exists, the answer is `-1`.

```text
nums1 = [4, 1, 2]
nums2 = [1, 3, 4, 2]

4 -> no greater element to its right -> -1
1 -> next greater to its right is 3
2 -> no greater element to its right -> -1

Output: [-1, 3, -1]
```

The brute-force approach scans forward from each queried position looking for the first larger value. That is **O(n1 * n2)** in the worst case — fine for small inputs, wasteful at scale, and it recomputes the same information for every query.

## The key insight: precompute the answer for every value, once

Every value in `nums2` has exactly one "next greater element," regardless of which values happen to be queried. So compute all of them up front, in a single right-to-left pass, and look up answers in `O(1)` afterward. 

Note also that the primary focus is on `nums2`. We do not even look at `nums1` until `nums2` is fully built!

A monotonic decreasing stack makes that pass linear:

- Walk `nums2` from right to left.
- Before processing a value, pop anything smaller off the stack — those values can never be "next greater" for anything further left, because the current value is closer and just as valid a candidate.
- Whatever remains on top of the stack (if anything) is the next greater element for the current value.
- Push the current value on, and continue.

## Why scanning backwards works

Scanning right to left means that by the time you reach a value, the stack already holds every value that is a genuine candidate to be its next-greater — in order of proximity. Popping smaller values off the top is the same dominance argument seen in sliding window problems: a smaller, farther candidate is strictly worse than a larger, closer one, so it can be discarded for good.

## Complexity

- **Time:** `O(n1 + n2)` — one linear pass over `nums2` to build the map, one linear pass over `nums1` to answer queries.
- **Space:** `O(n2)` for the stack and the answer map.

## The reusable pattern

This is a small but clean instance of "precompute once, query many times" combined with a monotonic stack. The same shape shows up whenever you need, for every position in an array, some property of the nearest qualifying element in a fixed direction — next greater, next smaller, next warmer day, and so on. Once you recognize the shape, the direction to scan and the stack's monotonic invariant fall out naturally from the question being asked.

#Python #Algorithms #DataStructures #Stack #MonotonicStack #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #LearningInPublic
