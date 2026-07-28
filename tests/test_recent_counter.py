import pytest
from hypothesis import given, strategies as st

from recent_counter import RecentCounter


@pytest.mark.parametrize(
    ("timestamps", "expected"),
    [
        ([1], [1]),
        ([1, 100, 3001, 3002], [1, 2, 3, 3]),
        ([1, 3001], [1, 2]),
        ([1, 3002], [1, 1]),
        ([1, 10_000], [1, 1]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
    ],
)
def test_ping_uses_default_window(
    timestamps: list[int], expected: list[int]
) -> None:
    counter = RecentCounter()

    assert [counter.ping(timestamp) for timestamp in timestamps] == expected


@pytest.mark.parametrize(
    ("window_ms", "timestamps", "expected"),
    [
        (1, [1, 2, 3], [1, 2, 2]),
        (500, [1, 501, 502], [1, 2, 2]),
        (500, [1, 502], [1, 1]),
        (10, [1, 2, 3, 12], [1, 2, 3, 3]),
    ],
)
def test_ping_uses_custom_window(
    window_ms: int, timestamps: list[int], expected: list[int]
) -> None:
    counter = RecentCounter(window_ms)

    assert [counter.ping(timestamp) for timestamp in timestamps] == expected


@pytest.mark.parametrize("window_ms", [0, -1])
def test_recent_counter_rejects_non_positive_windows(window_ms: int) -> None:
    with pytest.raises(ValueError, match="window_ms must be positive"):
        RecentCounter(window_ms)


@given(
    window_ms=st.integers(min_value=1, max_value=10_000),
    increments=st.lists(st.integers(min_value=1, max_value=5_000), max_size=100),
)
def test_ping_matches_history_oracle(
    window_ms: int, increments: list[int]
) -> None:
    counter = RecentCounter(window_ms)
    timestamps: list[int] = []
    current_time = 0

    for increment in increments:
        current_time += increment
        timestamps.append(current_time)

        expected = sum(
            timestamp >= current_time - window_ms for timestamp in timestamps
        )
        assert counter.ping(current_time) == expected
