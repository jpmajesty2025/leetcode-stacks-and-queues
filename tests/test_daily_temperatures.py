import pytest
from hypothesis import given, strategies as st

from daily_temperatures import daily_temperatures


def brute_force_wait_days(temperatures: list[int]) -> list[int]:
    wait_days = [0] * len(temperatures)

    for day, temperature in enumerate(temperatures):
        for future_day in range(day + 1, len(temperatures)):
            if temperatures[future_day] > temperature:
                wait_days[day] = future_day - day
                break

    return wait_days


@pytest.mark.parametrize(
    ("temperatures", "expected"),
    [
        ([], []),
        ([30], [0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([60, 50, 40, 30], [0, 0, 0, 0]),
        ([70, 70, 70], [0, 0, 0]),
        ([70, 70, 71], [2, 1, 0]),
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([-5, -10, 0, -1, 3], [2, 1, 2, 1, 0]),
        ([80, 60, 65, 50, 90], [4, 1, 2, 1, 0]),
    ],
)
def test_daily_temperatures(
    temperatures: list[int], expected: list[int]
) -> None:
    assert daily_temperatures(temperatures) == expected


@given(st.lists(st.integers(min_value=-100, max_value=150), max_size=100))
def test_daily_temperatures_matches_brute_force_oracle(
    temperatures: list[int],
) -> None:
    assert daily_temperatures(temperatures) == brute_force_wait_days(temperatures)


@given(st.lists(st.integers(min_value=-100, max_value=150), max_size=100))
def test_daily_temperatures_returns_first_warmer_day(
    temperatures: list[int],
) -> None:
    wait_days = daily_temperatures(temperatures)

    for day, wait in enumerate(wait_days):
        if wait == 0:
            assert all(
                future_temperature <= temperatures[day]
                for future_temperature in temperatures[day + 1 :]
            )
        else:
            warmer_day = day + wait
            assert temperatures[warmer_day] > temperatures[day]
            assert all(
                intermediate_temperature <= temperatures[day]
                for intermediate_temperature in temperatures[day + 1 : warmer_day]
            )
