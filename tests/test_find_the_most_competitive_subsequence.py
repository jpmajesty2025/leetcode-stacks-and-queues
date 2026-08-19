import pytest
from hypothesis import given, strategies as st

from find_the_most_competitive_subsequence import most_competitive


def brute_force_most_competitive(nums: list[int], k: int) -> list[int]:
    best: list[int] | None = None
    n = len(nums)

    def backtrack(start: int, chosen: list[int]) -> None:
        nonlocal best
        if len(chosen) == k:
            if best is None or chosen < best:
                best = chosen[:]
            return
        remaining_needed = k - len(chosen)
        for i in range(start, n - remaining_needed + 1):
            chosen.append(nums[i])
            backtrack(i + 1, chosen)
            chosen.pop()

    backtrack(0, [])
    assert best is not None
    return best


@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([3, 5, 2, 6], 2, [2, 6]),
        ([2, 4, 3, 3, 5, 4, 9, 6], 4, [2, 3, 3, 4]),
        ([1], 1, [1]),
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        ([4, 3, 2, 1], 1, [1]),
        ([4, 3, 2, 1], 4, [4, 3, 2, 1]),
        ([1, 1, 1, 1], 2, [1, 1]),
        ([3, 3, 3, 4], 2, [3, 3]),
        ([2, 4, 3, 3, 5, 4, 9, 6], 1, [2]),
        ([5, 4, 3, 2, 1, 6], 3, [2, 1, 6]),
    ],
)
def test_most_competitive(nums: list[int], k: int, expected: list[int]) -> None:
    assert most_competitive(nums, k) == expected


@given(
    nums=st.lists(st.integers(min_value=0, max_value=15), min_size=1, max_size=12),
    data=st.data(),
)
def test_most_competitive_matches_brute_force_oracle(nums: list[int], data) -> None:
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))

    assert most_competitive(nums, k) == brute_force_most_competitive(nums, k)


@given(
    nums=st.lists(st.integers(min_value=0, max_value=1_000), min_size=1, max_size=100),
    data=st.data(),
)
def test_most_competitive_returns_subsequence_of_correct_length(
    nums: list[int], data
) -> None:
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))

    result = most_competitive(nums, k)

    assert len(result) == k
    # result must be a subsequence of nums, preserving relative order
    remaining = iter(nums)
    assert all(value in remaining for value in result)


@given(
    nums=st.lists(st.integers(min_value=0, max_value=1_000), min_size=1, max_size=100)
)
def test_most_competitive_full_length_returns_original(nums: list[int]) -> None:
    assert most_competitive(nums, len(nums)) == nums
