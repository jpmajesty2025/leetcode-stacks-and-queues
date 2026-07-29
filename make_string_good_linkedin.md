# Making a String “Good” with a Stack

Consider a string containing uppercase and lowercase English letters.

A string is **bad** when two adjacent characters are the same letter in opposite cases:

```text
aA
Aa
```

You make the string **good** by removing any such adjacent pair until no removable pair remains. Then return the **good** string.

For example:

```text
"leEeetcode" -> "leetcode"
"abBAcC"      -> ""
```

The second example is especially instructive:

```text
abBAcC
  ^^          remove bB
aAcC
^^            remove aA
cC
^^            remove cC
""
```

A stack is a natural fit because every new character only needs to be compared with the most recently retained character.

```python
def _are_opposite_cases_of_same_letter(left: str, right: str) -> bool:
    return left != right and left.lower() == right.lower()


def make_good(s: str) -> str:
    stack: list[str] = []

    for character in s:
        if stack and _are_opposite_cases_of_same_letter(stack[-1], character):
            stack.pop()
        else:
            stack.append(character)

    return "".join(stack)
```

## Why it works

The stack holds the fully reduced result for everything processed so far.

For each incoming character:

- If it forms an opposite-case pair with the stack top, remove the top.
- Otherwise, retain it by pushing it onto the stack.

That simple rule also handles cascading removals. Removing one pair may expose another pair when the next character arrives, as in the second example above. The stack preserves exactly the context needed to detect it.

## Complexity

- **Time:** `O(n)` — every character is pushed once and popped at most once.
- **Space:** `O(n)` in the worst case.

The broader pattern is useful well beyond strings: when an operation may undo or cancel the most recent retained item, a stack is often the right first data structure to consider.

Where else have you used a stack to model cancellation, undo behavior, or adjacent reductions?

#LearningInPublic #Python #Algorithms #DataStructures #Stack #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview #CleanCode