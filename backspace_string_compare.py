'''
Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character.

Note that after backspacing an empty text, the text will continue empty.
'''

def backspaceCompare(s: str, t: str) -> bool:
        stack1: list[str] = []
        for character in s:
            if character == '#':
                try:
                    stack1.pop()
                except Exception:
                    pass
            else:
                stack1.append(character)
        
        s_reduced = "".join(stack1)

        stack2: list[str] = []
        for character in t:
            if character == '#':
                try:
                    stack2.pop()
                except Exception:
                    pass
            else:
                stack2.append(character)
        t_reduced = "".join(stack2)
        
        return s_reduced == t_reduced