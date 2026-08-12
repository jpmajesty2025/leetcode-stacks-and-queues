# 🌟 Classic Stack Application: Removing Stars From a String


**The problem:** Given a string with lowercase letters and `*` characters, each star removes itself AND the closest non-star character to its left.

Input: `"leet**cod*e"` → Output: `"lecoe"`

This problem may *sound* fiddly but there is a clean one-pass solution once you spot the pattern.

**The naive instinct** is to think about repeatedly scanning and deleting — which screams O(n²) if you're not careful (every deletion could mean re-scanning).

**The insight:** this is a textbook stack problem. Walk the string once, left to right:
- See a regular character? Push it.
- See a star? Pop the stack.

The stack's top is always the "closest surviving character to the left" — exactly what the star needs to remove. No re-scanning, no shifting indices.

```python
def remove_stars(s: str) -> str:
    stack = []
    for ch in s:
        if ch == '*':
            if stack:
                stack.pop()
        else:
            stack.append(ch)
    return ''.join(stack)
```

**Complexity:** O(n) time, O(n) space — and that space is unavoidable since the output length scales with the input.

This problem is a nice reminder that "remove the nearest X to the left" is a strong stack-use signal in disguise. Once you see it, the code basically writes itself.

What's your go-to signal for "this is secretly a stack problem"? 👇

#LearningInPublic #LeetCode #DataStructures #Algorithms #Python #SoftwareEngineering #CodingInterview #ProblemSolving #ComputerScience #TechInterview #CleanCode