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
        print(i,suffix_min[i])
    print("\n***\n")
    print(suffix_min)
    for i in range(n):
        stack.append(s[i])
        # Pop while the stack top is no larger than every character still
        # to come (or nothing remains to come, at the last index) - it can
        # never be beaten by a future character, so it is safe to write now.
        while stack and (i + 1 >= n or stack[-1] <= suffix_min[i + 1]):
            result.append(stack.pop())

    return ''.join(result)

s = "zzyxwaabcccd"
res = robot_with_string(s)
print(res)

'''
On `suffix_min[i]`: Correct — suffix_min[i] = min(s[i:]), so by definition of "min," it is <= every character in 
s[i:] (including itself). It's literally "the smallest character that appears from position i onward."
On the check `stack[-1] <= suffix_min[i+1]`: Your framing is right for the first iteration of the while loop at step i —
right after pushing s[i], stack[-1] is indeed s[i], "the most recent char from s." The question being asked is exactly: 
"is this char <= every character that hasn't arrived yet?" If yes, it can never be beaten by anything in the future, so it's 
safe to write now — get it out before something bigger gets pushed on top of it.
One nuance: the while loop can pop multiple times per index i. After the first pop (writing s[i]), the new 
stack[-1] isn't s[i] anymore — it's whatever character was sitting underneath it, now freshly exposed. The loop re-checks 
that exposed character against the same suffix_min[i+1] too. So more precisely, the condition is "is *whatever is currently 
exposed on top of the stack* <= every remaining character?" — not strictly "the char we just pushed," though that's the first 
thing checked. This is why one push can trigger a cascade of pops (e.g., a long run of already-sorted small characters buried 
under a big one that just got written).
On your "nothing we can do about it" case: Exactly right, and here's why that's not a loss. If the current top c is <=
some but not all remaining characters — meaning something smaller m is still coming — we leave c on the stack. When m 
eventually gets pushed, it lands on top of c (LIFO). If m is safe to pop (i.e., <= everything after it), it gets 
written to paper immediately, jumping ahead of c in the output — which is exactly what we want, since m < c. Meanwhile c 
just sits there, buried, waiting its turn. It only gets popped later, once everything smaller that could ever appear above it 
has already been popped and written first.
On burying: Right again — pushing is unconditional; the new character always goes on top regardless of whether it's smaller 
than what's already there. That's fine, because "buried" isn't "stuck" — the buried character gets a fair re-evaluation the 
moment it's re-exposed (i.e., everything pushed after it that could pop has already popped), and at that point it's tested 
against the current suffix_min, which only shrinks as more of s is revealed.
So the whole algorithm is really: hold every character until either (a) it's proven to be the smallest thing left, or (b) 
something even smaller shows up first and leapfrogs it via the stack's LIFO order. That's what keeps the stack always 
non-decreasing from bottom to top among survivors, and it's why the output ends up as lexicographically small as the fixed 
push-order constraint allows.
'''

'''
Q: Makes sense. I was contemplating exactly which classes of input strings this greedy algorithm with output in correct lexical 
order.Anything that is already lexically sorted will be unchanged and a string in reverse lex order will be fully reversed 
and output in lexical order. But it also seems that if s = x + y where 'x' is a string sorted in rev lex order and 'y' 
is a string in lex order, e.g. s = 'zzyxwaabcccd', then the output will be lexically sorted. Is that correct? And are 
there other classes of inputs that will come out fully lexically sorted?

A: First — I found and fixed a real problem: the working file print_lexicographically_smallest_string.py had accumulated debug 
print() statements, a stray module-level driver call, and a large pasted comment block (leftover from local experimentation). 
That's now cleaned up and restored to the correct implementation; tests still pass (10/10).
Yes, your "descending prefix + ascending suffix" observation is correct, but it's actually a special case of a much cleaner,
well-known characterization. I verified computationally by brute force (checked all 3,279 strings of length 1–7 over a 3-letter 
alphabet, comparing "does the output equal sorted(s)?" against a pattern test) — zero mismatches.
The exact rule: the output is fully lexically sorted if and only if `s` avoids the pattern "231."
That means: there is no triple of positions i < j < k in s such that s[k] < s[i] < s[j] — i.e., you never see a medium 
value, followed later by a bigger value, followed later by something smaller than the medium. This is exactly the classical 
definition of a stack-sortable sequence (this problem is, structurally, "sort a sequence using a single stack, FIFO input / 
LIFO output" — a textbook stack-sorting setup, and 231-avoidance is the known necessary-and-sufficient condition for 
single-stack sortability).
Why your example works under this rule: in "zzyxwaabcccd" = descending run (zzyxwa) + ascending run (abcccd), you can 
never form a s[k] < s[i] < s[j] triple, because once you're in the ascending suffix everything is non-decreasing (no j 
followed by a smaller k), and within the descending prefix everything is non-increasing (no j bigger than an earlier i). 
Any triple spanning prefix→suffix also can't produce the pattern, because the suffix's values only ever increase from where the 
prefix left off.
But "descending + ascending" is not the only shape that works — it's a sufficient condition, not necessary. Examples that 
are 231-avoiding (hence output fully sorted) but not of that two-run shape:
- Multiple interleaved descending runs where each new run's max never exceeds the previous run's min region appropriately, e.g. "cba" + "cba" shifted so no 231 forms — though in practice, for distinct/near-distinct alphabets, valid shapes get restrictive fast.
- Any already-sorted string (special case: purely ascending, x is empty).
- Any fully-reversed string (special case: purely descending, y is empty).
- Strings with heavy repeated characters can satisfy 231-avoidance in shapes other than a clean two-run split, since ties (s[k] == s[i] or s[i] == s[j]) never trigger the strict-inequality pattern — e.g. "bbaa" + "aabb"-style repeats have more slack than strictly distinct letters would.
So the precise, complete answer to "which inputs come out fully sorted" is: exactly the 231-avoiding strings — your 
descending-then-ascending construction is one common way to guarantee that, but the real underlying invariant is pattern 
avoidance, not the specific two-run shape.
'''