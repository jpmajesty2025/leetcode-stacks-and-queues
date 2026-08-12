# Why the Greedy Pop Strategy Is Provably Correct for Validate Stack Sequences

*A side discussion exploring whether the greedy "pop the instant you can" strategy in `validate_stack_sequences.py` is merely well-tested, or provably correct — and whether multiple distinct valid push/pop schedules can exist for the same input.*

## The question

Is the intuition around the greedy pop approach merely "good intuition" backed by a bunch of brute-force evidence? Or is there an argument to be made that greedy is in fact the right way to go?

Classic theory says a greedy algorithm delivers a provably optimal solution when a problem has two properties:

1. **Greedy Choice Property** — you can reach a globally optimal solution by making locally optimal (greedy) choices step-by-step, without compromising future options.
2. **Optimal Substructure** — the optimal solution to the whole problem contains, within it, optimal solutions to its smaller subproblems.

So: are we in that territory here?

## This is a feasibility problem, not a classic optimization

First, a framing note: "optimal solution" language (as in classic greedy proofs like Dijkstra or interval scheduling) is built for *optimization* problems. `validate_stack_sequences` is a **feasibility/decision** problem — "does *any* valid schedule exist?" So the properties translate slightly:

- **Greedy Choice Property** → "if a greedy move is currently available, taking it never turns a solvable instance into an unsolvable one."
- **Optimal Substructure** → "after making that move, what remains is the *same problem*, just on a smaller instance." (Feasibility of the whole reduces to feasibility of the sub-instance.)

Both hold here, via an **exchange argument** — the standard proof technique for this class of greedy.

## The exchange argument

**Claim:** If *any* valid push/pop schedule exists that produces `popped` from `pushed`, then the greedy schedule (pop immediately whenever the stack top matches the next expected value) is also valid.

**Proof sketch:** Suppose a valid schedule `S` exists, and suppose at some point the stack top `x` equals the next unconsumed target `popped[j]`, but `S` chooses to push instead of popping right then. Since values are distinct (a stated constraint of this problem), `x` is the *only* element that can ever be output as `popped[j]` — so `S` must pop `x` eventually. But by pushing more elements on top of `x` first, `S` buries it: those new elements now sit strictly above `x`, and LIFO order means they must come off *before* `x` can. This can only ever restrict `x`'s future accessibility — it can never make `x` easier to reach.

Now compare: if we instead pop `x` right away (as greedy does), then resume playing out the *rest* of `S`'s operations exactly as they were, unaffected — nothing about the rest of `S`'s plan for the other elements depended on `x` sitting on the stack. So this modified schedule is still valid, and it agrees with greedy on this one step. Repeating this argument (an induction over "first point of disagreement") transforms `S` into the greedy schedule step-by-step, and validity is preserved at every transformation. So the greedy schedule succeeds whenever *any* schedule succeeds. That's exactly the **greedy choice property**: the locally available choice (pop now) never forecloses a globally feasible solution.

## Optimal substructure

After greedy makes its choice at step `i` (push or pop), the state reduces to: a smaller `pushed` suffix, a smaller `popped` suffix, and an updated stack — which is *literally the same decision problem*, just smaller. Feasibility of the full instance is exactly "feasible now AND feasible on the reduced instance," with no interaction between them beyond the shared stack state. That's the substructure property holding cleanly — no subtlety needed, since the state fully captures everything the rest of the algorithm needs to know (the stack contents + remaining suffixes), and it's a pure function of the choices made so far.

## Connection to stack-sortable permutations

This isn't a coincidence — it's the same territory as **stack-sortable permutations** and **231-pattern avoidance**, explored in a companion discussion on the "lexicographically smallest string" problem (see `print_lexicographically_smallest_string_linkedin.md`). In that classical theory, the exact algorithm that decides stack-sortability *is* this greedy "push, then pop-while-matches" procedure, and its correctness proof is precisely the exchange argument above (sometimes phrased as "the greedy stack-sort is optimal because delaying a legal pop is a dominated move").

## Can we find two distinct valid schedules for the same input?

A natural follow-up: since the exchange argument shows greedy *can always be reached from* any other valid schedule, does that mean other valid schedules can exist too — just ones that eventually agree with greedy?

**With distinct values (as `validate_stack_sequences` requires), the answer is a firm no.** An exhaustive search over every permutation pair for `n` up to 6 found that, whenever a valid schedule exists at all, it is always **unique** — there is exactly one way to interleave the pushes and pops. This makes sense: at every step, at most one operation is *forced* — pop, if and only if the stack top currently matches the next popped value (and it must be popped now-or-never, since with distinct values that value will never reappear as an option later). There is never a genuine branch point.

**Relaxing "distinct values" changes everything.** If `pushed` and `popped` are allowed to contain duplicates (outside this problem's stated constraints, but instructive to explore), multiple valid schedules can absolutely coexist — because now, when several equal-valued elements are sitting around, *which* one gets popped is ambiguous, opening up real choice points.

**Minimal concrete example:** `pushed = [1, 1]`, `popped = [1, 1]`.

- **Greedy schedule:** `push(1) → pop() = 1 → push(1) → pop() = 1`. Valid.
- **Non-greedy schedule:** `push(1) → push(1) → pop() = 1 → pop() = 1`. Also valid! Here, the greedy strategy would have popped immediately after the first push (since the stack top `1` matches `popped[0] = 1`), but this alternate schedule deliberately delays that pop, pushing a second `1` on top first. Because the second element also happens to be `1`, the delayed pop still succeeds — nothing was lost by waiting, precisely *because* the ambiguity created a real alternative.

Both schedules are legitimate interleavings of the same `pushed`/`popped` pair, and both correctly conclude "true" — but they take different paths to get there. With distinct values, that second path is never available, because there'd be no *other* matching element to "delay into."

## Takeaway

The brute-force verification performed when reviewing `validate_stack_sequences.py` wasn't establishing correctness from scratch — it was a sanity check on a result that is, in fact, a provable theorem for distinct-value inputs: the greedy schedule exists if and only if any valid schedule exists, and (for distinct values) it's the *only* one. The exchange argument is what gives the actual proof; the brute force gives confidence against implementation bugs. The duplicate-value exploration also clarifies exactly *why* uniqueness holds under the problem's stated constraints — distinctness removes the only source of scheduling ambiguity.