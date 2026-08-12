import pytest
from hypothesis import given, strategies as st

from min_stack_class import MinStack


def test_leetcode_example() -> None:
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)

    assert min_stack.getMin() == -3
    min_stack.pop()
    assert min_stack.top() == 0
    assert min_stack.getMin() == -2


def test_getmin_with_duplicate_minimums() -> None:
    min_stack = MinStack()
    min_stack.push(1)
    min_stack.push(2)
    min_stack.push(1)

    assert min_stack.getMin() == 1
    min_stack.pop()  # removes the second 1
    assert min_stack.getMin() == 1  # the earlier 1 is still the min
    min_stack.pop()  # removes 2
    assert min_stack.getMin() == 1
    min_stack.pop()  # removes the first 1


def test_getmin_tracks_strictly_decreasing_pushes() -> None:
    min_stack = MinStack()
    for value in [5, 4, 3, 2, 1]:
        min_stack.push(value)
        assert min_stack.getMin() == value


def test_getmin_after_popping_back_to_earlier_minimum() -> None:
    min_stack = MinStack()
    min_stack.push(3)
    min_stack.push(1)
    min_stack.push(5)

    assert min_stack.getMin() == 1
    min_stack.pop()  # removes 5, min stays 1
    assert min_stack.getMin() == 1
    min_stack.pop()  # removes 1, min reverts to 3
    assert min_stack.getMin() == 3


def test_pop_on_empty_stack_raises_index_error() -> None:
    min_stack = MinStack()
    with pytest.raises(IndexError):
        min_stack.pop()


def test_top_on_empty_stack_raises_index_error() -> None:
    min_stack = MinStack()
    with pytest.raises(IndexError):
        min_stack.top()


def test_getmin_on_empty_stack_raises_index_error() -> None:
    min_stack = MinStack()
    with pytest.raises(IndexError):
        min_stack.getMin()


def test_two_instances_do_not_share_state() -> None:
    first = MinStack()
    second = MinStack()

    first.push(10)
    second.push(-10)

    assert first.getMin() == 10
    assert second.getMin() == -10


ops_strategy = st.lists(
    st.one_of(
        st.tuples(st.just("push"), st.integers(min_value=-10_000, max_value=10_000)),
        st.tuples(st.just("pop")),
        st.tuples(st.just("top")),
        st.tuples(st.just("getMin")),
    ),
    min_size=1,
    max_size=100,
)


@given(ops=ops_strategy)
def test_matches_list_based_oracle(ops: list[tuple]) -> None:
    min_stack = MinStack()
    oracle: list[int] = []

    for op in ops:
        name = op[0]
        if name == "push":
            _, value = op
            min_stack.push(value)
            oracle.append(value)
        elif name == "pop":
            if oracle:
                min_stack.pop()
                oracle.pop()
            else:
                with pytest.raises(IndexError):
                    min_stack.pop()
        elif name == "top":
            if oracle:
                assert min_stack.top() == oracle[-1]
            else:
                with pytest.raises(IndexError):
                    min_stack.top()
        else:  # "getMin"
            if oracle:
                assert min_stack.getMin() == min(oracle)
            else:
                with pytest.raises(IndexError):
                    min_stack.getMin()
