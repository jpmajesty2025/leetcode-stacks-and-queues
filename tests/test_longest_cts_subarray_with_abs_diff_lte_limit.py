import pytest
from hypothesis import given, strategies as st

from longest_cts_subarray_with_abs_diff_lte_limit import longest_subarray


def brute_force_longest_subarray(nums: list[int], limit: int) -> int:
    best = 0
    for start in range(len(nums)):
        for end in range(start, len(nums)):
            window = nums[start : end + 1]
            if max(window) - min(window) <= limit:
                best = max(best, len(window))
    return best


@pytest.mark.parametrize(
    ("nums", "limit", "expected"),
    [
        ([8, 2, 4, 7], 4, 2),
        ([10, 1, 2, 4, 7, 2], 5, 4),
        ([4, 2, 2, 2, 4, 4, 2, 2], 0, 3),
        ([1], 0, 1),
        ([5], 100, 1),
        ([1, 1, 1, 1], 0, 4),
        ([1, 5, 1, 1], 3, 2),
        ([5, 1, 5, 5], 3, 2),
        ([2, 2, 8], 0, 2),
        ([1, 2, 3, 4, 5], 0, 1),
        ([1, 2, 3, 4, 5], 100, 5),
        ([-1, -5, -3, -2], 2, 2),
    ],
)
def test_longest_subarray(nums: list[int], limit: int, expected: int) -> None:
    assert longest_subarray(nums, limit) == expected


@pytest.mark.parametrize(
    ("nums", "limit"),
    [
        ([1, 2, 3], -1),
        ([1], -5),
        ([], -1),
    ],
)
def test_longest_subarray_rejects_negative_limit(
    nums: list[int], limit: int
) -> None:
    with pytest.raises(ValueError, match="limit must be non-negative"):
        longest_subarray(nums, limit)


def test_longest_subarray_empty_nums_returns_zero() -> None:
    assert longest_subarray([], 5) == 0


@given(
    nums=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=0, max_size=100
    ),
    limit=st.integers(min_value=0, max_value=20_000),
)
def test_longest_subarray_matches_brute_force_oracle(
    nums: list[int], limit: int
) -> None:
    assert longest_subarray(nums, limit) == brute_force_longest_subarray(nums, limit)


@given(
    nums=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=1, max_size=100
    ),
    limit=st.integers(min_value=0, max_value=20_000),
)
def test_longest_subarray_result_is_valid_window(
    nums: list[int], limit: int
) -> None:
    size = longest_subarray(nums, limit)

    assert 1 <= size <= len(nums)
    # some window of that size must actually satisfy the limit constraint
    assert any(
        max(nums[start : start + size]) - min(nums[start : start + size]) <= limit
        for start in range(len(nums) - size + 1)
    )


@given(
    nums=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=1, max_size=100
    )
)
def test_longest_subarray_zero_limit_equals_longest_run_of_equal_values(
    nums: list[int],
) -> None:
    longest_run = 1
    current_run = 1
    for previous, current in zip(nums, nums[1:]):
        current_run = current_run + 1 if current == previous else 1
        longest_run = max(longest_run, current_run)

    assert longest_subarray(nums, 0) == longest_run
