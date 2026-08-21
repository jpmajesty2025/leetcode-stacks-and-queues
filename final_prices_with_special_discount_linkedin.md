# 🏷️ Finding Every "Next Cheaper Item" in One Pass

**The setup:** You're given a list of prices. For each item, if a *later* item is priced at or below it, you get a discount equal to that later item's price — specifically the price of the *first* such item that appears after it. Otherwise, no discount.

Example: `[8, 4, 6, 2, 3]` → `[4, 2, 4, 2, 3]`. Item `0` (price `8`) gets discounted by item `1` (price `4`, the first later price `<= 8`), paying `4`. Item `2` (price `6`) only looks forward — the first later price `<= 6` is item `3`'s `2`, so it pays `4`.

**The naive approach:** for each item, scan forward until you find a price that's low enough. That's O(n²) in the worst case (think a strictly increasing list, where every item scans all the way to the end and finds nothing).

**The key insight:** This is the same shape as "next smaller element" problems — and a greedy monotonic stack solves it in one linear pass. Walk left to right, keeping a stack of *indices whose discount we haven't found yet*. When the current price is low enough to discount everything sitting on top of the stack, pop and settle those debts immediately.

```python
def final_prices(prices: list[int]) -> list[int]:
    pending_indices: list[int] = []
    answer = prices.copy()

    for index, price in enumerate(prices):
        while pending_indices and prices[pending_indices[-1]] >= price:
            discounted_index = pending_indices.pop()
            answer[discounted_index] -= price
        pending_indices.append(index)

    return answer
```

**Walking through `[8, 4, 6, 2, 3]`:**

- Push `8` → stack `[8]`.
- `4` arrives: `8 >= 4`, so `8` is discounted by `4` → pays `4`. Pop `8`, push `4` → stack `[4]`.
- `6` arrives: `4 < 6`, no discount yet. Push `6` → stack `[4, 6]`.
- `2` arrives: `6 >= 2`, discount `6` by `2` → pays `4`. Pop `6`. Then `4 >= 2`, discount `4` by `2` → pays `2`. Pop `4`. Push `2` → stack `[2]`.
- `3` arrives: `2 < 3`, no discount. Push `3` → stack `[2, 3]`.
- Final answer: `[4, 2, 4, 2, 3]`. ✅

Each index is pushed once and popped at most once, so despite the nested `while` loop, total work stays **O(n)** across the whole array — O(n) space for the stack and result.

Same trick as "daily temperatures" and "next greater element" — a stack of "unresolved" indices that get settled the moment a qualifying value shows up.

#LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #LearningInPublic #CleanCode
