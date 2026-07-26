# Backspace String Compare: A Stack Is a Perfect Fit!

Problem statement:

> Given two strings where `#` means “backspace,” determine whether both strings produce the same final text.

For example:

```text
"ab#c"  -> "ac"
"ad#c"  -> "ac"
```

So the result is `True`.

The key observation: a backspace always affects the **most recently typed character**. That is exactly last-in, first-out (LIFO) behavior—the natural domain of a stack.

```python
def _reduce_text(value: str) -> str:
    stack: list[str] = []

    for character in value:
        if character == "#":
            if stack:
                stack.pop()
        else:
            stack.append(character)

    return "".join(stack)


def backspace_compare(s: str, t: str) -> bool:
    return _reduce_text(s) == _reduce_text(t)
```

Why this approach works:

- A normal character is pushed onto the stack.
- A `#` removes the latest retained character, if one exists.
- Backspacing an empty editor safely does nothing.
- After processing both inputs, compare their final stack contents.

This solution runs in **O(m + n)** time, where `m` and `n` are the lengths of the two strings. Its extra space is **O(m + n)** in the worst case.

We even have an opportunity to DRY the code out by extracting the repeated “simulate typing” logic into `_reduce_text()`. It also keeps the comparison function focused on one responsibility: compare the two final editor states, independent of how we reduce a text chunk.

Notte: there is also an O(1)-extra-space reverse two-pointer approach, but for a stack-focused problem, this version is often the clearest way to express the underlying idea.

What is your rule of thumb for choosing the clearest solution versus the most space-efficient one?

#Python #DataStructures #Algorithms #Stack #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #CleanCode