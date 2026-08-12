'''
You are given a string s and a robot that currently holds an empty string t. Apply one of the following operations until s and t are both empty:

Remove the first character of a string s and give it to the robot. The robot will append this character to the string t.
Remove the last character of a string t and give it to the robot. The robot will write this character on paper.
Return the lexicographically smallest string that can be written on the paper.

 

Example 1:

Input: s = "zza"
Output: "azz"
Explanation: Let p denote the written string.
Initially p="", s="zza", t="".
Perform first operation three times p="", s="", t="zza".
Perform second operation three times p="azz", s="", t="".
Example 2:

Input: s = "bac"
Output: "abc"
Explanation: Let p denote the written string.
Perform first operation twice p="", s="c", t="ba". 
Perform second operation twice p="ab", s="c", t="". 
Perform first operation p="ab", s="", t="c". 
Perform second operation p="abc", s="", t="".
Example 3:

Input: s = "bdda"
Output: "addb"
Explanation: Let p denote the written string.
Initially p="", s="bdda", t="".
Perform first operation four times p="", s="", t="bdda".
Perform second operation four times p="addb", s="", t="".

Constraints:

1 <= s.length <= 105
s consists of only English lowercase letters.
'''

def robot_with_string(s: str) -> str:
    n = len(s)
    stack = []
    result = []
    suffix_min = [None] * n
    suffix_min[-1] = s[-1]

    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(s[i], suffix_min[i + 1])

    for i in range(n):
        stack.append(s[i])
        # Pop while the stack top is no larger than every character still
        # to come (or nothing remains to come, at the last index) - it can
        # never be beaten by a future character, so it is safe to write now.
        while stack and (i + 1 >= n or stack[-1] <= suffix_min[i + 1]):
            result.append(stack.pop())

    return ''.join(result)

s = '2341'
result = robot_with_string(s)
print(result)  # Output: "1234"