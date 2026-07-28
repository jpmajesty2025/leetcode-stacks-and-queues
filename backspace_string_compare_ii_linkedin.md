# Backspace String Take 2: Compare Without a Stack

Problem statement:

> Given two strings where `#` means “backspace,” determine whether both strings produce the same final text.

The stack solution for **Backspace String Compare** is intuitive (see prior post):

- Push typed characters.
- Pop when `#` appears.
- Compare the two final strings.

It is a great way to model two text editors—but it uses extra memory proportional to the input size.

There is another approach: scan both strings **from right to left**.

Why right to left?

A `#` deletes the character immediately before it. When scanning backward, we can count pending backspaces and skip the characters they remove without pushing anything onto a stack. That means we only compare characters that would remain visible in the final editor state. and we're only using constant extra space: one charactter at a time, plus a `backspaces` running count.

```python
def _previous_visible_character(value: str, index: int) -> tuple[str | None, int]:
    backspaces = 0

    while index >= 0:
        character = value[index]

        if character == "#":
            backspaces += 1
        elif backspaces:
            backspaces -= 1
        else:
            return character, index - 1

        index -= 1

    return None, index


def backspaceCompare(s: str, t: str) -> bool:
    s_index = len(s) - 1
    t_index = len(t) - 1

    while s_index >= 0 or t_index >= 0:
        s_character, s_index = _previous_visible_character(s, s_index)
        t_character, t_index = _previous_visible_character(t, t_index)

        if s_character != t_character:
            return False

    return True
```

## Stack vs. two pointers

| Approach | Time | Extra space | Main advantage |
|---|---:|---:|---|
| Stack simulation | O(m + n) | O(m + n) | Direct, readable editor simulation |
| Reverse two pointers | O(m + n) | O(1) | Avoids building reduced strings |

Both approaches are linear-time.

The stack version is usually the clearest starting point because it mirrors the problem statement: type characters, then backspace them.

The reverse two-pointer version is more space-efficient. It does not construct either final text; it finds and compares only the characters that survive.

The important lesson is not that one solution always “wins.” It is recognizing the trade-off:

- Choose the **stack** when clarity and direct simulation matter most.
- Choose **reverse pointers** when constant auxiliary space matters and the backward traversal remains understandable.

Which would you lead with in an interview: the intuitive stack solution or the O(1)-space optimization?

#Python #Algorithms #DataStructures #TwoPointers #Stack #LeetCode #CodingInterview #ProblemSolving #SoftwareEngineering #Tradeoffs