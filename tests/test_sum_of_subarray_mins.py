import pytest
from hypothesis import given, strategies as st

from sum_of_subarray_mins import sum_subarray_mins


MOD = 10**9 + 7


def brute_force_sum_subarray_mins(arr: list[int]) -> int:
    n = len(arr)
    total = 0
    for i in range(n):
        current_min = arr[i]
        for j in range(i, n):
            current_min = min(current_min, arr[j])
            total += current_min
    return total % MOD


@pytest.mark.parametrize(
    ("arr", "expected"),
    [
        ([3, 1, 2, 4], 17),
        ([11, 81, 94, 43, 3], 444),
        ([1], 1),
        ([1, 1], 3),
        ([1, 2, 3], 10),
        ([3, 2, 1], 10),
        ([2, 2, 2], 12),
    ],
)
def test_sum_subarray_mins(arr: list[int], expected: int) -> None:
    assert sum_subarray_mins(arr) == expected


@given(
    st.lists(st.integers(min_value=1, max_value=30_000), min_size=1, max_size=100)
)
def test_sum_subarray_mins_matches_brute_force_oracle(arr: list[int]) -> None:
    assert sum_subarray_mins(arr) == brute_force_sum_subarray_mins(arr)


@given(st.integers(min_value=1, max_value=30_000))
def test_sum_subarray_mins_single_element_equals_itself(value: int) -> None:
    assert sum_subarray_mins([value]) == value % MOD


@given(
    st.lists(st.integers(min_value=1, max_value=30_000), min_size=1, max_size=100)
)
def test_sum_subarray_mins_is_non_negative(arr: list[int]) -> None:
    assert sum_subarray_mins(arr) >= 0


@given(
    st.lists(
        st.integers(min_value=1, max_value=30_000), min_size=1, max_size=15
    )
)
def test_sum_subarray_mins_lower_bounded_by_min_times_subarray_count(
    arr: list[int],
) -> None:
    # Every subarray's minimum is at least the array's global minimum, so
    # the sum must be at least global_min * number_of_subarrays (mod p).
    n = len(arr)
    num_subarrays = n * (n + 1) // 2
    lower_bound = (min(arr) * num_subarrays) % MOD

    assert sum_subarray_mins(arr) >= lower_bound
