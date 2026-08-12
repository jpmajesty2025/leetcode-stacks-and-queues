import pytest
from hypothesis import given, strategies as st

from stack_using_queues import MyStack


def test_leetcode_example() -> None:
    stack = MyStack()
    stack.push(1)
    stack.push(2)

    assert stack.top() == 2
    assert stack.pop() == 2
    assert stack.empty() is False


def test_empty_on_fresh_stack() -> None:
    stack = MyStack()
    assert stack.empty() is True


def test_push_pop_lifo_order() -> None:
    stack = MyStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.empty() is True


def test_top_does_not_remove_element() -> None:
    stack = MyStack()
    stack.push(1)
    stack.push(2)

    assert stack.top() == 2
    assert stack.top() == 2
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_empty_after_interleaved_push_pop() -> None:
    stack = MyStack()
    stack.push(1)
    stack.pop()
    assert stack.empty() is True

    stack.push(2)
    stack.push(3)
    stack.pop()
    assert stack.empty() is False
    stack.pop()
    assert stack.empty() is True


def test_repeated_top_calls_preserve_underlying_order() -> None:
    # top() internally rotates the queue; repeated calls must not corrupt
    # the order of the remaining elements.
    stack = MyStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    for _ in range(5):
        assert stack.top() == 3

    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_two_instances_do_not_share_state() -> None:
    first = MyStack()
    second = MyStack()

    first.push(1)
    second.push(2)

    assert first.pop() == 1
    assert second.pop() == 2


ops_strategy = st.lists(
    st.one_of(
        st.tuples(st.just("push"), st.integers(min_value=1, max_value=9)),
        st.tuples(st.just("pop")),
        st.tuples(st.just("top")),
        st.tuples(st.just("empty")),
    ),
    min_size=1,
    max_size=100,
)


@given(ops=ops_strategy)
def test_matches_list_based_oracle(ops: list[tuple]) -> None:
    stack = MyStack()
    oracle: list[int] = []

    for op in ops:
        name = op[0]
        if name == "push":
            _, value = op
            stack.push(value)
            oracle.append(value)
        elif name == "pop":
            if oracle:
                assert stack.pop() == oracle.pop()
            else:
                with pytest.raises(IndexError):
                    stack.pop()
        elif name == "top":
            if oracle:
                assert stack.top() == oracle[-1]
            else:
                with pytest.raises(IndexError):
                    stack.top()
        else:  # "empty"
            assert stack.empty() == (len(oracle) == 0)
