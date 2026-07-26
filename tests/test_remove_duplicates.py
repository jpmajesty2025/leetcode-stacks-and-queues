import pytest
from hypothesis import given, strategies as st

from remove_duplicates import remove_duplicates


def reduction_oracle(value: str) -> str:
    previous = None
    while value != previous:
        previous = value
        reduced: list[str] = []
        index = 0
        while index < len(value):
            if index + 1 < len(value) and value[index] == value[index + 1]:
                index += 2
            else:
                reduced.append(value[index])
                index += 1
        value = "".join(reduced)
    return value


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("abc", "abc"),
        ("aa", ""),
        ("abbaca", "ca"),
        ("azxxzy", "ay"),
        ("aabbcc", ""),
        ("aaaa", ""),
        ("abba", ""),
        ("leetcode", "ltcode"),
    ],
)
def test_remove_duplicates(value: str, expected: str) -> None:
    assert remove_duplicates(value) == expected


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=100))
def test_remove_duplicates_matches_reduction_oracle(value: str) -> None:
    assert remove_duplicates(value) == reduction_oracle(value)


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz", max_size=100))
def test_remove_duplicates_result_has_no_adjacent_duplicates(value: str) -> None:
    result = remove_duplicates(value)
    assert all(left != right for left, right in zip(result, result[1:]))