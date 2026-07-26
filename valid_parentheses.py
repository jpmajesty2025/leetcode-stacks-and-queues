'''
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
'''
def is_valid(s: str) -> bool:
    matching_opening = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for character in s:
        if character in matching_opening:
            if not stack or stack.pop() != matching_opening[character]:
                return False
        elif character in "([{":
            stack.append(character)
        else:
            return False

    return not stack