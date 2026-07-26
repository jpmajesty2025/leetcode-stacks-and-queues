import re

import pytest
from hypothesis import given, strategies as st

from backspace_string_compare import backspaceCompare as stack_backspace_compare
from backspace_string_compare_ii import backspaceCompare as two_pointer_backspace_compare


def reduction_oracle(value: str) -> str:
    previous = None
    while value != previous:
        previous = value
        value = re.sub(r"[a-z]#", "", value)
    return value.replace("#", "")


@pytest.mark.parametrize(
    ("s", "t", "expected"),
    [
        ("", "", True),
        ("", "###", True),
        ("ab#c", "ad#c", True),
        ("ab##", "c#d#", True),
        ("a#c", "b", False),
        ("a##c", "#a#c", True),
        ("bxj##tw", "bxo#j##tw", True),
        ("nzp#o#g", "b#nzp#o#g", True),
        ("abc", "abc", True),
        ("abc", "abd", False),
    ],
)
def test_backspace_compare(s: str, t: str, expected: bool) -> None:
    assert stack_backspace_compare(s, t) is expected
    assert two_pointer_backspace_compare(s, t) is expected


@given(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz#", max_size=100),
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz#", max_size=100),
)
def test_backspace_compare_matches_reduction_oracle(s: str, t: str) -> None:
    expected = reduction_oracle(s) == reduction_oracle(t)

    assert stack_backspace_compare(s, t) is expected
    assert two_pointer_backspace_compare(s, t) is expected
