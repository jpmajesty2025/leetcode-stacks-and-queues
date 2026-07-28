import pytest
from hypothesis import given, strategies as st

from make_string_good import make_good


def are_opposite_cases_of_same_letter(left: str, right: str) -> bool:
    return left != right and left.lower() == right.lower()


def reduction_oracle(value: str) -> str:
    while True:
        for index, (left, right) in enumerate(zip(value, value[1:])):
            if are_opposite_cases_of_same_letter(left, right):
                return reduction_oracle(value[:index] + value[index + 2 :])
        return value


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("A", "A"),
        ("aA", ""),
        ("Aa", ""),
        ("aa", "aa"),
        ("AA", "AA"),
        ("aB", "aB"),
        ("leEeetcode", "leetcode"),
        ("abBAcC", ""),
        ("abBA", ""),
        ("aabAAB", "aabAAB"),
        ("mCcaAbB", "m"),
    ],
)
def test_make_good(value: str, expected: str) -> None:
    assert make_good(value) == expected


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", max_size=100))
def test_make_good_matches_reduction_oracle(value: str) -> None:
    assert make_good(value) == reduction_oracle(value)


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", max_size=100))
def test_make_good_returns_a_fixed_point_without_bad_pairs(value: str) -> None:
    result = make_good(value)

    assert all(
        not are_opposite_cases_of_same_letter(left, right)
        for left, right in zip(result, result[1:])
    )
    assert make_good(result) == result
