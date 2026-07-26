import pytest
from hypothesis import given, strategies as st

from valid_parentheses import is_valid


def reduction_oracle(value: str) -> bool:
    previous = None
    while value != previous:
        previous = value
        value = value.replace("()", "").replace("[]", "").replace("{}", "")
    return value == ""


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", True),
        ("()", True),
        ("()[]{}", True),
        ("({[]})", True),
        ("((()))", True),
        ("(", False),
        ("[", False),
        ("{", False),
        (")", False),
        ("]", False),
        ("}", False),
        ("(]", False),
        ("([)]", False),
        ("{[}]", False),
        ("(()", False),
        ("))((", False),
        ("(a)", False),
        ("abc", False),
    ],
)
def test_is_valid(value: str, expected: bool) -> None:
    assert is_valid(value) is expected


@given(st.text(alphabet="()[]{}", max_size=100))
def test_is_valid_matches_reduction_oracle(value: str) -> None:
    assert is_valid(value) is reduction_oracle(value)


@given(st.text(alphabet=st.characters(blacklist_characters="()[]{}"), min_size=1))
def test_is_valid_rejects_non_bracket_characters(value: str) -> None:
    assert is_valid(value) is False