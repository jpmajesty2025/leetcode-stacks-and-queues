import random

import pytest
from hypothesis import given, settings, strategies as st

from validate_stack_sequences import validate_stack_sequences


def brute_force_validate_stack_sequences(pushed: list[int], popped: list[int]) -> bool:
    """Independent oracle: explores every branch of the push/pop decision
    tree via DFS (push the next element, or pop if the stack top matches
    the next expected popped value) rather than assuming the greedy
    "pop immediately whenever possible" strategy is optimal."""
    n = len(pushed)
    pushed_t = tuple(pushed)
    popped_t = tuple(popped)

    def dfs(next_push: int, stack: tuple[int, ...], next_pop: int) -> bool:
        if next_pop == n:
            return True
        if stack and stack[-1] == popped_t[next_pop]:
            if dfs(next_push, stack[:-1], next_pop + 1):
                return True
        if next_push < n:
            if dfs(next_push + 1, stack + (pushed_t[next_push],), next_pop):
                return True
        return False

    return dfs(0, (), 0)


def simulate_valid_pop_order(pushed: list[int], rng: random.Random) -> list[int]:
    """Generates a popped order that is guaranteed reachable, by randomly
    interleaving pushes with pops (popping whenever a random coin flip
    says so and the stack is non-empty)."""
    stack: list[int] = []
    popped: list[int] = []
    remaining = list(pushed)
    while remaining or stack:
        if stack and (not remaining or rng.random() < 0.5):
            popped.append(stack.pop())
        else:
            stack.append(remaining.pop(0))
    return popped


@pytest.mark.parametrize(
    ("pushed", "popped", "expected"),
    [
        ([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
        ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False),
        ([], [], True),
        ([1], [1], True),
        ([1, 2], [2, 1], True),
        ([1, 2], [1, 2], True),
        ([1, 2, 3], [3, 1, 2], False),
    ],
)
def test_validate_stack_sequences_examples(
    pushed: list[int], popped: list[int], expected: bool
) -> None:
    assert validate_stack_sequences(pushed, popped) is expected


def test_validate_stack_sequences_does_not_mutate_inputs() -> None:
    pushed = [1, 2, 3]
    popped = [3, 2, 1]
    pushed_copy, popped_copy = list(pushed), list(popped)

    validate_stack_sequences(pushed, popped)

    assert pushed == pushed_copy
    assert popped == popped_copy


@given(
    pushed=st.permutations(range(8)).map(list),
    seed=st.integers(min_value=0, max_value=2**32 - 1),
)
def test_validate_stack_sequences_accepts_simulated_valid_orders(
    pushed: list[int], seed: int
) -> None:
    popped = simulate_valid_pop_order(pushed, random.Random(seed))
    assert validate_stack_sequences(pushed, popped) is True


@given(
    pushed=st.permutations(range(6)).map(list),
    data=st.data(),
)
@settings(max_examples=200)
def test_validate_stack_sequences_matches_brute_force_oracle(
    pushed: list[int], data: st.DataObject
) -> None:
    popped = data.draw(st.permutations(pushed).map(list))

    assert validate_stack_sequences(pushed, popped) == brute_force_validate_stack_sequences(
        pushed, popped
    )