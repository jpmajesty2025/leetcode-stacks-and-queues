'''
You are given a string s consisting of lowercase English letters. A duplicate removal consists of choosing two 
adjacent and equal letters and removing them.

We repeatedly make duplicate removals on s until we no longer can.

Return the final string after all such duplicate removals have been made. It can be proven that the answer is unique.
'''
def remove_duplicates(s: str) -> str:
        stack = []
        stack.append(s[0])
        for c in s[1:]:
            if stack and stack[-1] == c:
                stack.pop()
            else:
                stack.append(c)
        
        return_str = ''
        for _ in range(len(stack)):
            return_str = stack.pop() + return_str
        return return_str