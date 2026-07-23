'''
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.
'''
def is_valid( s: str) -> bool:
    stack = []
    matching = {"(": ")", "[": "]", "{": "}"}
    
    for c in s:
        if c in matching: # if c is an opening bracket
            stack.append(c)
        else:
            if not stack:
                return False
            
            previous_opening = stack.pop()
            if matching[previous_opening] != c:
                return False

    return not stack