import pytest
from hypothesis import given, strategies as st

from sliding_window_maximum import max_sliding_window


def brute_force_window_maximums(nums: list[int], k: int) -> list[int]:
    return [max(nums[start : start + k]) for start in range(len(nums) - k + 1)]


@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1], 1, [1]),
        ([1, 2, 3, 4], 1, [1, 2, 3, 4]),
        ([1, 2, 3, 4], 4, [4]),
        ([1, 2, 3, 4], 2, [2, 3, 4]),
        ([4, 3, 2, 1], 2, [4, 3, 2]),
        ([7, 7, 7], 2, [7, 7]),
        ([-4, -2, -5, -1], 2, [-2, -2, -1]),
        ([9, 1, 9, 1], 2, [9, 9, 9]),
    ],
)
def test_max_sliding_window(nums: list[int], k: int, expected: list[int]) -> None:
    assert max_sliding_window(nums, k) == expected


@pytest.mark.parametrize(
    ("nums", "k"),
    [
        ([], 0),
        ([], 1),
        ([1, 2], 0),
        ([1, 2], -1),
        ([1, 2], 3),
    ],
)
def test_max_sliding_window_rejects_invalid_window_sizes(
    nums: list[int], k: int
) -> None:
    with pytest.raises(ValueError, match="k must be between 1 and the length of nums"):
        max_sliding_window(nums, k)


@given(
    nums=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=1, max_size=100
    ),
    data=st.data(),
)
def test_max_sliding_window_matches_brute_force_oracle(
    nums: list[int], data
) -> None:
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))

    assert max_sliding_window(nums, k) == brute_force_window_maximums(nums, k)


@given(
    nums=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=1, max_size=100
    ),
    data=st.data(),
)
def test_max_sliding_window_returns_each_window_maximum(
    nums: list[int], data
) -> None:
    k = data.draw(st.integers(min_value=1, max_value=len(nums)))
    maximums = max_sliding_window(nums, k)

    assert len(maximums) == len(nums) - k + 1
    for start, maximum in enumerate(maximums):
        assert maximum == max(nums[start : start + k])
        assert maximum in nums[start : start + k]
