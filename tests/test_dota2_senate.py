import pytest
from hypothesis import given, strategies as st

from dota2_senate import predict_party_victory


def brute_force_predict_party_victory(senate: str) -> str:
    # Simulate the round-based procedure literally: each senator, in turn,
    # bans the next active senator from the opposing party (the greedy
    # optimal move), until only one party remains active.
    n = len(senate)
    alive = [True] * n
    parties = list(senate)

    while True:
        active_parties = {parties[i] for i in range(n) if alive[i]}
        if len(active_parties) <= 1:
            return "rubber" if "R" in active_parties else "duckie"

        i = 0
        while i < n:
            if not alive[i]:
                i += 1
                continue
            # This senator bans the next alive senator from the other party.
            j = (i + 1) % n
            while alive[j] is False or parties[j] == parties[i]:
                j = (j + 1) % n
                if j == i:
                    return "rubber" if parties[i] == "R" else "duckie"
            alive[j] = False
            i += 1


@pytest.mark.parametrize(
    ("senate", "expected"),
    [
        ("RD", "rubber"),
        ("RDD", "duckie"),
        ("R", "rubber"),
        ("D", "duckie"),
        ("RR", "rubber"),
        ("DD", "duckie"),
        ("DR", "duckie"),
        ("RRDD", "rubber"),
        ("RDRD", "rubber"),
        ("DRDR", "duckie"),
        ("RDDR", "rubber"),
    ],
)
def test_predict_party_victory(senate: str, expected: str) -> None:
    assert predict_party_victory(senate) == expected


@given(
    st.text(alphabet="RD", min_size=1, max_size=30),
)
def test_predict_party_victory_matches_brute_force_oracle(senate: str) -> None:
    assert predict_party_victory(senate) == brute_force_predict_party_victory(senate)


@given(st.text(alphabet="RD", min_size=1, max_size=30))
def test_predict_party_victory_returns_a_present_party(senate: str) -> None:
    # The winner announced must be a party that actually appears in the
    # input - the algorithm cannot invent a winner out of thin air.
    result = predict_party_victory(senate)
    letter = "R" if result == "rubber" else "D"
    assert letter in senate


@pytest.mark.parametrize("senate", ["R" * 20, "D" * 20])
def test_single_party_wins_immediately(senate: str) -> None:
    expected = "rubber" if senate[0] == "R" else "duckie"
    assert predict_party_victory(senate) == expected
