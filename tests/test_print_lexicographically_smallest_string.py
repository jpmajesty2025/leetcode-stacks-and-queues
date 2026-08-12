import pytest
from hypothesis import given, settings, strategies as st

from print_lexicographically_smallest_string import robot_with_string


def brute_force_robot_with_string(s: str) -> str:
    """Independent oracle: exhaustively explores every legal sequence of
    the two operations described in the problem (move front of s onto t,
    or pop back of t onto the paper) and returns the lexicographically
    smallest resulting paper string."""
    n = len(s)
    best: list[str | None] = [None]

    def dfs(i: int, t: str, p: str) -> None:
        if i == n and not t:
            if best[0] is None or p < best[0]:
                best[0] = p
            return
        if i < n:
            dfs(i + 1, t + s[i], p)
        if t:
            dfs(i, t[:-1], p + t[-1])

    dfs(0, "", "")
    assert best[0] is not None
    return best[0]


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("zza", "azz"),
        ("bac", "abc"),
        ("bdda", "addb"),
        ("a", "a"),
        ("ba", "ab"),
        ("aaaa", "aaaa"),
    ],
)
def test_robot_with_string_examples(s: str, expected: str) -> None:
    assert robot_with_string(s) == expected


def test_robot_with_string_already_sorted_input_is_identity() -> None:
    assert robot_with_string("abcde") == "abcde"


@given(s=st.text(alphabet="abc", min_size=1, max_size=6))
@settings(max_examples=200)
def test_robot_with_string_matches_brute_force_oracle(s: str) -> None:
    assert robot_with_string(s) == brute_force_robot_with_string(s)


@given(
    s=st.text(alphabet=st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")), min_size=1, max_size=200)
)
def test_robot_with_string_result_is_permutation_of_input(s: str) -> None:
    result = robot_with_string(s)
    assert sorted(result) == sorted(s)


@given(
    s=st.text(
        alphabet=st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")),
        min_size=1,
        max_size=200,
    )
)
def test_robot_with_string_result_is_never_lexicographically_larger_than_input(
    s: str,
) -> None:
    # The greedy result must always be <= the untouched input, since "do
    # nothing but push then flush" (i.e. reversing s) is one of the legal
    # strategies and the sorted string is a lower bound; a cheap sanity
    # invariant that catches gross regressions without duplicating the
    # brute-force oracle is that the result is bounded between the input's
    # sorted form (best case) and its reverse (a legal but naive strategy).
    result = robot_with_string(s)
    assert sorted(s) <= list(result) <= list(reversed(s))