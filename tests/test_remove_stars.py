import re
import string

import pytest
from hypothesis import given, strategies as st

from remove_stars import remove_stars


def brute_force_remove_stars(s: str) -> str:
    """Independent oracle: literally repeats the described operation
    (remove closest non-star char to the left of a star, plus the star)
    using regex substitution instead of a stack."""
    while "*" in s:
        s = re.sub(r"[^*]\*", "", s, count=1)
    return s


@st.composite
def valid_star_strings(draw: st.DrawFn) -> str:
    """Generates strings where the star-removal operation is always
    possible: at every prefix, the number of stars seen so far never
    exceeds the number of preceding non-star characters."""
    length = draw(st.integers(min_value=1, max_value=50))
    balance = 0
    result: list[str] = []
    for _ in range(length):
        can_star = balance > 0
        is_star = draw(st.booleans()) if can_star else False
        if is_star:
            result.append("*")
            balance -= 1
        else:
            result.append(draw(st.sampled_from(string.ascii_lowercase)))
            balance += 1
    return "".join(result)


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("leet**cod*e", "lecoe"),
        ("erase*****", ""),
        ("a", "a"),
        ("aa**", ""),
        ("ab*c*d*", "a"),
        ("z" * 20 + "*" * 10, "z" * 10),
    ],
)
def test_remove_stars_examples(s: str, expected: str) -> None:
    assert remove_stars(s) == expected


def test_remove_stars_does_not_mutate_input() -> None:
    s = "leet**cod*e"
    original = s
    remove_stars(s)
    assert s == original


@given(s=valid_star_strings())
def test_remove_stars_matches_brute_force_oracle(s: str) -> None:
    assert remove_stars(s) == brute_force_remove_stars(s)


@given(s=valid_star_strings())
def test_remove_stars_result_has_no_stars_and_expected_length(s: str) -> None:
    result = remove_stars(s)
    star_count = s.count("*")

    assert "*" not in result
    assert len(result) == len(s) - 2 * star_count


@given(s=valid_star_strings())
def test_remove_stars_result_is_subsequence_of_input(s: str) -> None:
    result = remove_stars(s)
    it = iter(s)
    assert all(ch in it for ch in result)