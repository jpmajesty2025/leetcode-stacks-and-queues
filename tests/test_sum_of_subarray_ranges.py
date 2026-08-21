import pytest
from hypothesis import given, strategies as st

from sum_of_subarray_ranges import sum_subarray_ranges


@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([1, 2, 3], 4),
        ([1, 3, 3], 4),
        ([4, -2, -3, 4, 1], 59),
        ([5], 0),
        ([2, 2, 2], 0),
        ([3, 2, 1], 4),
        ([-5, -1, -3], 6),
    ],
)
def test_sum_subarray_ranges(nums: list[int], expected: int) -> None:
    assert sum_subarray_ranges(nums) == expected


def test_sum_subarray_ranges_does_not_mutate_input() -> None:
    nums = [4, -2, -3, 4, 1]
    original = nums.copy()

    sum_subarray_ranges(nums)

    assert nums == original


@given(
    st.lists(st.integers(min_value=-1_000_000, max_value=1_000_000), min_size=1, max_size=200)
)
def test_sum_subarray_ranges_is_non_negative(nums: list[int]) -> None:
    assert sum_subarray_ranges(nums) >= 0


@given(st.integers(min_value=-1_000_000, max_value=1_000_000))
def test_sum_subarray_ranges_single_element_is_zero(value: int) -> None:
    assert sum_subarray_ranges([value]) == 0


@given(
    st.lists(st.integers(min_value=-1_000, max_value=1_000), min_size=1, max_size=50)
)
def test_sum_subarray_ranges_is_zero_for_constant_arrays(nums: list[int]) -> None:
    constant = [nums[0]] * len(nums)
    assert sum_subarray_ranges(constant) == 0