'''
You are given a string s consisting of lowercase English letters. A duplicate removal consists of choosing two 
adjacent and equal letters and removing them.

We repeatedly make duplicate removals on s until we no longer can.

Return the final string after all such duplicate removals have been made. It can be proven that the answer is unique.
'''
def remove_duplicates(s: str) -> str:
    stack: list[str] = []
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            stack.append(character)

    return "".join(stack)