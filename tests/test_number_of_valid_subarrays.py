import pytest
from hypothesis import given, strategies as st

from number_of_valid_subarrays import valid_subarrays


def brute_force_valid_subarrays(nums: list[int]) -> int:
    count = 0
    n = len(nums)

    for start in range(n):
        for end in range(start, n):
            if all(nums[k] >= nums[start] for k in range(start, end + 1)):
                count += 1

    return count


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([5], 1),
        ([1, 4, 2, 5, 3], 11),
        ([3, 2, 1], 3),
        ([2, 2, 2], 6),
        ([1, 2, 3, 4, 5], 15),
        ([5, 4, 3, 2, 1], 5),
    ],
)
def test_valid_subarrays(nums: list[int], expected: int) -> None:
    assert valid_subarrays(nums) == expected


def test_valid_subarrays_does_not_mutate_input() -> None:
    nums = [1, 4, 2, 5, 3]
    original = nums.copy()

    valid_subarrays(nums)

    assert nums == original


@given(st.lists(st.integers(min_value=0, max_value=10), min_size=1, max_size=50))
def test_valid_subarrays_matches_brute_force_oracle(nums: list[int]) -> None:
    assert valid_subarrays(nums) == brute_force_valid_subarrays(nums)


@given(st.lists(st.integers(min_value=0, max_value=10), min_size=1, max_size=50))
def test_valid_subarrays_counts_at_least_one_per_element(nums: list[int]) -> None:
    # Every single-element subarray is trivially valid, so the total must be
    # at least the length of nums.
    assert valid_subarrays(nums) >= len(nums)


@given(st.lists(st.integers(min_value=0, max_value=10), min_size=1, max_size=50))
def test_valid_subarrays_is_upper_bounded_by_all_possible_subarrays(
    nums: list[int],
) -> None:
    n = len(nums)
    assert valid_subarrays(nums) <= n * (n + 1) // 2
