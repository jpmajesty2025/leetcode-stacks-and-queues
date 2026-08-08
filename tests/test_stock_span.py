import pytest
from hypothesis import given, strategies as st

from stock_span import StockSpanner


def brute_force_spans(prices: list[int]) -> list[int]:
    spans = []
    for day, price in enumerate(prices):
        span = 1
        while day - span >= 0 and prices[day - span] <= price:
            span += 1
        spans.append(span)
    return spans


@pytest.mark.parametrize(
    ("prices", "expected_spans"),
    [
        ([100, 80, 60, 70, 60, 75, 85], [1, 1, 1, 2, 1, 4, 6]),
        ([7, 2, 1, 2], [1, 1, 1, 3]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 1, 1, 1, 1]),
        ([1, 1, 1, 1], [1, 2, 3, 4]),
        ([42], [1]),
    ],
)
def test_stock_spanner_next(prices: list[int], expected_spans: list[int]) -> None:
    spanner = StockSpanner()
    assert [spanner.next(price) for price in prices] == expected_spans


def test_stock_spanner_is_stateful_across_instances() -> None:
    first = StockSpanner()
    second = StockSpanner()

    assert [first.next(price) for price in [10, 20]] == [1, 2]
    assert [second.next(price) for price in [5]] == [1]


@given(
    prices=st.lists(
        st.integers(min_value=0, max_value=10_000), min_size=1, max_size=100
    )
)
def test_stock_spanner_matches_brute_force_oracle(prices: list[int]) -> None:
    spanner = StockSpanner()
    spans = [spanner.next(price) for price in prices]

    assert spans == brute_force_spans(prices)


@given(
    prices=st.lists(
        st.integers(min_value=0, max_value=10_000), min_size=1, max_size=100
    )
)
def test_stock_spanner_span_bounds_and_boundary_condition(prices: list[int]) -> None:
    spanner = StockSpanner()

    for day, price in enumerate(prices):
        span = spanner.next(price)

        assert 1 <= span <= day + 1
        # every day within the span must have price <= today's price
        for offset in range(span):
            assert prices[day - offset] <= price
        # the day immediately preceding the span (if any) must break the streak
        if span <= day:
            assert prices[day - span] > price
