from collections import deque

import pytest
from hypothesis import given, strategies as st

from queue_using_stacks import MyQueue


def test_push_pop_peek_fifo_order() -> None:
    queue = MyQueue()
    queue.push(1)
    queue.push(2)

    assert queue.peek() == 1
    assert queue.pop() == 1
    assert queue.peek() == 2
    assert queue.empty() is False

    queue.push(3)
    assert queue.pop() == 2
    assert queue.pop() == 3
    assert queue.empty() is True


def test_empty_on_fresh_queue() -> None:
    queue = MyQueue()
    assert queue.empty() is True


def test_empty_after_interleaved_push_pop() -> None:
    queue = MyQueue()
    queue.push(1)
    queue.pop()
    assert queue.empty() is True

    queue.push(2)
    queue.push(3)
    queue.pop()
    assert queue.empty() is False
    queue.pop()
    assert queue.empty() is True


def test_pop_and_peek_transfer_stacks_only_once() -> None:
    # After a full transfer, further push()es must go to stack1 and not be
    # returned before previously transferred elements.
    queue = MyQueue()
    queue.push(1)
    queue.push(2)
    queue.peek()  # forces transfer: stack1=[], stack2=[2, 1]
    queue.push(3)  # goes onto stack1

    assert queue.pop() == 1
    assert queue.pop() == 2
    assert queue.pop() == 3
    assert queue.empty() is True


# Two independent stacks are instantiated per MyQueue instance.
def test_two_instances_do_not_share_state() -> None:
    first = MyQueue()
    second = MyQueue()

    first.push(1)
    second.push(2)

    assert first.pop() == 1
    assert second.pop() == 2


ops_strategy = st.lists(
    st.one_of(
        st.tuples(st.just("push"), st.integers(min_value=-10_000, max_value=10_000)),
        st.tuples(st.just("pop")),
        st.tuples(st.just("peek")),
        st.tuples(st.just("empty")),
    ),
    min_size=1,
    max_size=100,
)


@given(ops=ops_strategy)
def test_matches_deque_oracle(ops: list[tuple]) -> None:
    queue = MyQueue()
    oracle: deque = deque()

    for op in ops:
        name = op[0]
        if name == "push":
            _, value = op
            queue.push(value)
            oracle.append(value)
        elif name == "pop":
            if oracle:
                assert queue.pop() == oracle.popleft()
            else:
                with pytest.raises(IndexError):
                    queue.pop()
        elif name == "peek":
            if oracle:
                assert queue.peek() == oracle[0]
            else:
                with pytest.raises(IndexError):
                    queue.peek()
        else:  # "empty"
            assert queue.empty() == (len(oracle) == 0)