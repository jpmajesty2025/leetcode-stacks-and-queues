import pytest
from hypothesis import given, strategies as st

from next_greater_element_i import next_greater_element


def brute_force_next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    result = []
    for target in nums1:
        index = nums2.index(target)
        greater = [value for value in nums2[index + 1 :] if value > target]
        result.append(greater[0] if greater else -1)
    return result


@pytest.mark.parametrize(
    ("nums1", "nums2", "expected"),
    [
        ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
        ([2, 4], [1, 2, 3, 4], [3, -1]),
        ([1], [1], [-1]),
        ([1, 2, 3, 4], [4, 3, 2, 1], [-1, -1, -1, -1]),
        ([1, 2, 3, 4], [1, 2, 3, 4], [2, 3, 4, -1]),
        ([3, 1], [3, 4, 1, 2], [4, 2]),
        ([0], [0, 10_000], [10_000]),
    ],
)
def test_next_greater_element(
    nums1: list[int], nums2: list[int], expected: list[int]
) -> None:
    assert next_greater_element(nums1, nums2) == expected


@pytest.mark.parametrize(
    ("nums1", "nums2"),
    [
        ([5], [1, 2, 3]),
        ([1, 2, 5], [1, 2, 3]),
        ([1], []),
    ],
)
def test_next_greater_element_rejects_non_subset(
    nums1: list[int], nums2: list[int]
) -> None:
    with pytest.raises(ValueError, match="nums1 must be a subset of nums2"):
        next_greater_element(nums1, nums2)


@given(
    nums2=st.lists(
        st.integers(min_value=0, max_value=10_000), min_size=1, max_size=100, unique=True
    ),
    data=st.data(),
)
def test_next_greater_element_matches_brute_force_oracle(nums2: list[int], data) -> None:
    nums1 = data.draw(st.permutations(nums2).map(lambda perm: perm[: len(perm)]))
    nums1 = nums1[: data.draw(st.integers(min_value=1, max_value=len(nums1)))]

    assert next_greater_element(nums1, nums2) == brute_force_next_greater_element(
        nums1, nums2
    )


@given(
    nums2=st.lists(
        st.integers(min_value=0, max_value=10_000), min_size=1, max_size=100, unique=True
    )
)
def test_next_greater_element_full_query_returns_valid_or_absent_values(
    nums2: list[int],
) -> None:
    result = next_greater_element(nums2, nums2)

    assert len(result) == len(nums2)
    for target, answer in zip(nums2, result):
        index = nums2.index(target)
        if answer == -1:
            assert all(value <= target for value in nums2[index + 1 :])
        else:
            assert answer in nums2[index + 1 :]
            assert answer > target
            # answer must be the first greater element, not just any greater element
            for value in nums2[index + 1 : nums2.index(answer)]:
                assert value <= target
