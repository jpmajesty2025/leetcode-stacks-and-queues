'''
Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character.

This implementation compares the strings from right to left using O(1) auxiliary space.
'''


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
