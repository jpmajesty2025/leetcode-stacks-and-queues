# 🗳️ Dota2 Senate: Why "Majority Rules" Isn't the Whole Story

**The setup:** Senators from two parties — Radiant (`R`) and Dire (`D`) — vote in rounds. On their turn, each active senator can either ban another senator's rights permanently, or announce victory if everyone left is from their own party. Every senator plays optimally for their side. Given the initial order of senators, which party wins?

**The naive instinct:** count the letters. More `R`s than `D`s, Radiant wins — right? **Wrong.** Position matters just as much as headcount. Consider `"RDRDD"` — Dire has the numeric majority (3 vs 2) — and yet **Radiant wins.** Being first to act is worth more than being more numerous.

**The key insight — first-mover advantage, formalized with two queues:** the optimal move for any senator is always to ban the *next* active senator from the opposing party — there's no better use of a ban. So track each party's senator indices in their own queue. Compare the front of each queue: whichever index is smaller acted first and bans the other. The survivor doesn't just requeue — it requeues at `index + n`, pushing it to the *back of the line* for the next round while preserving its relative voting order among its own party.

**Walking through `"RDRDD"` (indices: R=0, D=1, R=2, D=3, D=4):**

- `radiant = [0, 2]`, `dire = [1, 3, 4]`
- Round: compare `0` (R) vs `1` (D) → `0 < 1`, so R at index 0 bans D at index 1. R requeues as `0 + 5 = 5`. `radiant = [2, 5]`, `dire = [3, 4]`.
- Compare `2` (R) vs `3` (D) → `2 < 3`, so R at index 2 bans D at index 3. R requeues as `2 + 5 = 7`. `radiant = [5, 7]`, `dire = [4]`.
- Compare `5` (R) vs `4` (D) → `4 < 5`, so D at index 4 bans R at index 5. D requeues as `4 + 5 = 9`. `radiant = [7]`, `dire = [9]`.
- Compare `7` (R) vs `9` (D) → `7 < 9`, so R at index 7 bans D at index 9. `radiant = [10]`, `dire = []`.
- `dire` is empty → **Radiant wins**, despite starting with fewer senators. Two of Radiant's senators got to act *before* two of Dire's did, and that early-mover edge was enough.

**Where the draft had a real bug:** the function signature was `predict_party_victory(self, senate: str)` — a stray `self` parameter with no enclosing class. Calling it the intended way, `predict_party_victory("RD")`, actually raised `TypeError: missing 1 required positional argument: 'senate'`, because `"RD"` silently bound to `self` instead. An easy copy-paste artifact from refactoring a method into a free function — and one that's invisible until you actually try to call it.

**The algorithm:**

```python
from collections import deque


def predict_party_victory(senate: str) -> str:
    radiant = deque()
    dire = deque()

    for i, s in enumerate(senate):
        if s == 'R':
            radiant.append(i)
        else:
            dire.append(i)

    while radiant and dire:
        r_index = radiant.popleft()
        d_index = dire.popleft()

        if r_index < d_index:
            radiant.append(r_index + len(senate))
        else:
            dire.append(d_index + len(senate))

    return "Radiant" if radiant else "Dire"
```

The `+ len(senate)` trick is doing the heavy lifting: it lets a single pass of comparisons simulate an unbounded number of rounds, because it re-ranks the surviving senator *after* every currently-queued senator from both parties, without ever having to explicitly track "round number."

**Complexity:** O(n) time — every senator is banned or survives to requeue exactly once, so the two queues shrink toward a single winner in linear total work. O(n) space for the two queues.

Ever had an assumption like "the bigger side always wins" get disproven by a random counterexample the moment you actually tested it? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode
