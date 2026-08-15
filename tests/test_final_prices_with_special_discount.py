import pytest
from hypothesis import given, strategies as st

from final_prices_with_special_discount import final_prices


def brute_force_final_prices(prices: list[int]) -> list[int]:
    answer = prices.copy()

    for i, price in enumerate(prices):
        for j in range(i + 1, len(prices)):
            if prices[j] <= price:
                answer[i] = price - prices[j]
                break

    return answer


@pytest.mark.parametrize(
    ("prices", "expected"),
    [
        ([], []),
        ([5], [5]),
        ([8, 4, 6, 2, 3], [4, 2, 4, 2, 3]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([10, 1, 1, 6], [9, 0, 1, 6]),
        ([5, 4, 3, 2, 1], [1, 1, 1, 1, 1]),
        ([3, 3, 3], [0, 0, 3]),
        ([1, 1, 1, 1], [0, 0, 0, 1]),
    ],
)
def test_final_prices(prices: list[int], expected: list[int]) -> None:
    assert final_prices(prices) == expected


def test_final_prices_does_not_mutate_input() -> None:
    prices = [8, 4, 6, 2, 3]
    original = prices.copy()

    final_prices(prices)

    assert prices == original


@given(st.lists(st.integers(min_value=1, max_value=1000), max_size=100))
def test_final_prices_matches_brute_force_oracle(prices: list[int]) -> None:
    assert final_prices(prices) == brute_force_final_prices(prices)


@given(st.lists(st.integers(min_value=1, max_value=1000), max_size=100))
def test_final_prices_result_is_bounded_by_original_price(
    prices: list[int],
) -> None:
    answer = final_prices(prices)

    for price, final_price in zip(prices, answer):
        assert 0 <= final_price <= price


@given(st.lists(st.integers(min_value=1, max_value=1000), max_size=100))
def test_final_prices_no_discount_means_no_smaller_price_follows(
    prices: list[int],
) -> None:
    answer = final_prices(prices)

    for i, (price, final_price) in enumerate(zip(prices, answer)):
        if final_price == price:
            assert all(
                later_price > price for later_price in prices[i + 1 :]
            )
