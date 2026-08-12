import pytest
from hypothesis import given, strategies as st

from asteroid_collision import asteroid_collision


def brute_force_asteroid_collision(asteroids: list[int]) -> list[int]:
    result: list[int] = []
    for asteroid in asteroids:
        exploded = False
        while result and asteroid < 0 < result[-1]:
            if result[-1] < -asteroid:
                result.pop()
            elif result[-1] == -asteroid:
                result.pop()
                exploded = True
                break
            else:
                exploded = True
                break
        if not exploded:
            result.append(asteroid)
    return result


@pytest.mark.parametrize(
    ("asteroids", "expected"),
    [
        ([], []),
        ([5], [5]),
        ([-5], [-5]),
        ([5, 10, -5], [5, 10]),
        ([8, -8], []),
        ([10, 2, -5], [10]),
        ([-2, -1, 1, 2], [-2, -1, 1, 2]),
        ([-2, 2, 1, -1], [-2, 2]),
        ([1, -2, -1], [-2, -1]),
        ([1, 1, -1], [1]),
        ([-1, -2, 1, 2], [-1, -2, 1, 2]),
        ([5, 5, -5, -5], []),
        ([3, -3, 3, -3], []),
    ],
)
def test_asteroid_collision(
    asteroids: list[int], expected: list[int]
) -> None:
    assert asteroid_collision(asteroids) == expected


@given(
    st.lists(
        st.integers(min_value=-20, max_value=20).filter(lambda x: x != 0),
        max_size=50,
    )
)
def test_asteroid_collision_matches_brute_force_oracle(
    asteroids: list[int],
) -> None:
    assert asteroid_collision(asteroids) == brute_force_asteroid_collision(asteroids)


@given(
    st.lists(
        st.integers(min_value=-20, max_value=20).filter(lambda x: x != 0),
        max_size=50,
    )
)
def test_asteroid_collision_result_has_no_pending_collisions(
    asteroids: list[int],
) -> None:
    result = asteroid_collision(asteroids)

    for left, right in zip(result, result[1:]):
        # No surviving asteroid may still collide with its neighbor:
        # that only happens for a right-mover immediately followed by
        # a left-mover.
        assert not (left > 0 and right < 0)


@given(
    st.lists(
        st.integers(min_value=-20, max_value=20).filter(lambda x: x != 0),
        max_size=50,
    )
)
def test_asteroid_collision_preserves_relative_order_of_survivors(
    asteroids: list[int],
) -> None:
    result = asteroid_collision(asteroids)

    # Every surviving asteroid must appear in the input, in order: the
    # result must be a subsequence of the original list.
    remaining = iter(asteroids)
    assert all(value in remaining for value in result)
