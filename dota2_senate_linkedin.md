# 🗳️ The Fight for Supremacy in the Senate: When "Majority Rules" Isn't Enough to Prevail

**The setup:** Senators from two parties — Rubber (`R`) and Duckie (`D`) — vote in rounds. On their turn, each active senator can either ban another senator's rights permanently, or announce victory if everyone left is from their own party. Every senator plays optimally for their side - no crazy, game theoretic psyops. Given the initial order of senators, which party wins?

**The naive instinct:** count the letters. More `R`s than `D`s, Rubber wins — right? **Not so fast!** Position matters just as much as headcount. Consider `"RDRDD"` — Duckie has the numeric majority (3 vs 2) — and yet **Rubber wins.** Being first to act is worth more than being more numerous.

**The key insight — first-mover advantage, formalized with two queues:** the optimal move for any senator is always to ban the *next* active senator from the opposing party — there's no better use of a ban. So track each party's senator indices in their own queue. Compare the front of each queue: whichever index is smaller acted first and bans the other. The survivor doesn't just requeue — it requeues at `index + n`, pushing it to the *back of the line* for the next round while preserving its relative voting order among its own party.

**Walking through `"RDRDD"` (indices: R=0, D=1, R=2, D=3, D=4):**

- `rubber = [0, 2]`, `duckie = [1, 3, 4]`
- Round: compare `0` (R) vs `1` (D) → `0 < 1`, so R at index 0 bans D at index 1. R requeues as `0 + 5 = 5`. `rubber = [2, 5]`, `duckie = [3, 4]`.
- Compare `2` (R) vs `3` (D) → `2 < 3`, so R at index 2 bans D at index 3. R requeues as `2 + 5 = 7`. `rubber = [5, 7]`, `duckie = [4]`.
- Compare `5` (R) vs `4` (D) → `4 < 5`, so D at index 4 bans R at index 5. D requeues as `4 + 5 = 9`. `rubber = [7]`, `duckie = [9]`.
- Compare `7` (R) vs `9` (D) → `7 < 9`, so R at index 7 bans D at index 9. `rubber = [10]`, `duckie = []`.
- `duckie` is empty → **rubber wins**, despite starting with fewer senators. Two of rubber's senators got to act *before* two of duckie's did, and that early-mover edge was enough.

**The algorithm:**

```python
from collections import deque


def predict_party_victory(senate: str) -> str:
    rubber = deque()
    duckie = deque()

    for i, s in enumerate(senate):
        if s == 'R':
            rubber.append(i)
        else:
            duckie.append(i)

    while rubber and duckie:
        r_index = rubber.popleft()
        d_index = duckie.popleft()

        if r_index < d_index:
            rubber.append(r_index + len(senate))
        else:
            duckie.append(d_index + len(senate))

    return "rubber" if rubber else "duckie"
```

The `+ len(senate)` trick is doing the heavy lifting: it lets a single pass of comparisons simulate an unbounded number of rounds, because it re-ranks the surviving senator *after* every currently-queued senator from both parties, without ever having to explicitly track "round number."

**Complexity:** O(n) time — every senator is banned or survives to requeue exactly once, so the two queues shrink toward a single winner in linear total work. O(n) space for the two queues.

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
