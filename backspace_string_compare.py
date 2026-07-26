'''
Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character.

Note that after backspacing an empty text, the text will continue empty.
'''

def _reduce_text(value: str) -> str:
    stack: list[str] = []

    for character in value:
        if character == "#":
            if stack:
                stack.pop()
        else:
                stack.append(character)

    return "".join(stack)


def backspaceCompare(s: str, t: str) -> bool:
    return _reduce_text(s) == _reduce_text(t)