import pytest
from hypothesis import given, strategies as st

from number_of_people_visible_in_a_queue import can_see_persons_count


def brute_force_can_see_persons_count(heights: list[int]) -> list[int]:
    n = len(heights)
    answer = [0] * n

    for i in range(n):
        for j in range(i + 1, n):
            between = heights[i + 1 : j]
            if min(heights[i], heights[j]) > (max(between) if between else float("-inf")):
                answer[i] += 1

    return answer


@pytest.mark.parametrize(
    ("heights", "expected"),
    [
        ([10, 6, 8, 5, 11, 9], [3, 1, 2, 1, 1, 0]),
        ([5, 1, 2, 3, 10], [4, 1, 1, 1, 0]),
        ([1], [0]),
        ([1, 2], [1, 0]),
        ([2, 1], [1, 0]),
        ([1, 2, 3, 4, 5], [1, 1, 1, 1, 0]),
        ([5, 4, 3, 2, 1], [1, 1, 1, 1, 0]),
        ([3, 1, 2], [2, 1, 0]),
    ],
)
def test_can_see_persons_count(heights: list[int], expected: list[int]) -> None:
    assert can_see_persons_count(heights) == expected


@given(
    st.lists(
        st.integers(min_value=1, max_value=50), min_size=1, max_size=20, unique=True
    )
)
def test_can_see_persons_count_matches_brute_force_oracle(heights: list[int]) -> None:
    assert can_see_persons_count(heights) == brute_force_can_see_persons_count(heights)


@given(
    st.lists(
        st.integers(min_value=1, max_value=50), min_size=1, max_size=20, unique=True
    )
)
def test_can_see_persons_count_last_person_sees_no_one(heights: list[int]) -> None:
    assert can_see_persons_count(heights)[-1] == 0


@given(
    st.lists(
        st.integers(min_value=1, max_value=50), min_size=1, max_size=20, unique=True
    )
)
def test_can_see_persons_count_never_exceeds_remaining_people(
    heights: list[int],
) -> None:
    n = len(heights)
    result = can_see_persons_count(heights)

    for i, count in enumerate(result):
        assert 0 <= count <= n - i - 1


@given(
    st.lists(
        st.integers(min_value=1, max_value=50), min_size=1, max_size=20, unique=True
    )
)
def test_can_see_persons_count_person_before_tallest_to_the_right_sees_everyone_up_to_it(
    heights: list[int],
) -> None:
    n = len(heights)
    result = can_see_persons_count(heights)

    for i in range(n):
        to_the_right = heights[i + 1 :]
        if not to_the_right:
            continue
        # If the ith person sees everyone to their right, either they are
        # taller than everyone remaining, or the last visible person to
        # their right is the tallest remaining (blocking further view).
        if result[i] == len(to_the_right):
            assert heights[i] > max(to_the_right) or heights[n - 1] == max(
                to_the_right
            )
