import pytest
from hypothesis import given, strategies as st

from moving_average_from_data_stream import MovingAverage


@pytest.mark.parametrize(
    ("size", "values", "expected"),
    [
        (3, [1, 10, 3, 5], [1.0, 5.5, 14 / 3, 6.0]),
        (1, [1, 10, -3], [1.0, 10.0, -3.0]),
        (5, [2, 4, 6], [2.0, 3.0, 4.0]),
        (2, [-5, 5, -10], [-5.0, 0.0, -2.5]),
        (3, [7, 7, 7, 7], [7.0, 7.0, 7.0, 7.0]),
    ],
)
def test_next_returns_moving_average(
    size: int, values: list[int], expected: list[float]
) -> None:
    moving_average = MovingAverage(size)

    assert [moving_average.next(value) for value in values] == pytest.approx(expected)


@pytest.mark.parametrize("size", [0, -1])
def test_moving_average_rejects_non_positive_sizes(size: int) -> None:
    with pytest.raises(ValueError, match="size must be positive"):
        MovingAverage(size)


@given(
    size=st.integers(min_value=1, max_value=100),
    values=st.lists(st.integers(min_value=-10_000, max_value=10_000), max_size=100),
)
def test_next_matches_windowed_history_oracle(size: int, values: list[int]) -> None:
    moving_average = MovingAverage(size)
    history: list[int] = []

    for value in values:
        history.append(value)
        expected_window = history[-size:]
        expected = sum(expected_window) / len(expected_window)

        assert moving_average.next(value) == pytest.approx(expected)


@given(
    size=st.integers(min_value=1, max_value=100),
    values=st.lists(
        st.integers(min_value=-10_000, max_value=10_000), min_size=1, max_size=100
    ),
)
def test_next_result_is_bounded_by_the_current_window(
    size: int, values: list[int]
) -> None:
    moving_average = MovingAverage(size)
    history: list[int] = []

    for value in values:
        history.append(value)
        current_window = history[-size:]
        result = moving_average.next(value)

        assert min(current_window) <= result <= max(current_window)
