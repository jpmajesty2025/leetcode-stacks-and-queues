# leetcode-stacks-and-queues

Practice implementations for LeetCode stack and queue problems, with tests written in `pytest` and `hypothesis`.

## Test structure

- Tests live under `tests/`
- File naming follows `test_<module>.py`
- Run all tests with:

```bash
pytest -q
```

## Property-based testing (Hypothesis)

Alongside example-based tests, this repo uses **property-based tests** with [Hypothesis](https://hypothesis.readthedocs.io/).

### Pattern used

1. Write a small **reference implementation** (oracle) that is simple and obviously correct.
2. Use Hypothesis strategies to generate many valid inputs.
3. Assert the real implementation matches the oracle and key invariants.

### Example in this repo

In `tests/test_first_letter_to_appear_twice.py`:

- `strings_with_a_repeat()` generates lowercase strings guaranteed to contain at least one repeated character.
- The test compares `repeated_character(...)` against `_reference_first_repeated_character(...)`.
- It also checks basic invariants (returned value is lowercase and appears at least twice).

This complements regular unit tests by exploring many edge cases automatically.
