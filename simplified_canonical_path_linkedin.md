# Simplifying Unix Paths with a Stack

A Unix path can contain more than directory names:

- `.` means “stay in the current directory.”
- `..` means “move to the parent directory.”
- Multiple `/` characters act like one separator.
- Names such as `...` and `....` are ordinary directory names—not special syntax.

The task: transform an absolute path into its canonical form.

For example:

```text
/home//user/Documents/../Pictures/
```

becomes:

```text
/home/user/Pictures
```

A stack is a natural fit because `..` always removes the **most recently retained directory**.

```python
def simplify_path(path: str) -> str:
    stack: list[str] = []

    for directory in path.split("/"):
        if directory == "..":
            if stack:
                stack.pop()
        elif directory and directory != ".":
            stack.append(directory)

    return "/" + "/".join(stack)
```

## How it works

1. Split the path into components using `/`.
2. Ignore empty components caused by repeated or leading/trailing slashes.
3. Ignore `.` because it keeps us in the current directory.
4. On `..`, pop the last directory—unless we are already at root.
5. Push every other component, including names like `...`.
6. Join the retained components with a single leading `/`.

The stack enforces an important boundary condition: trying to go above the root directory leaves us at `/`.

Examples:

```text
/../                 -> /
/a/../../b           -> /b
/.../a/../b/c/../d/./ -> /.../b/d
```

This solution runs in **O(n)** time and uses **O(n)** space in the worst case, where `n` is the path length. It is clear, efficient, and maps directly to the “undo the last directory” behavior of `..`.

What other problems have you solved where a stack made “go back” logic feel natural?

#Python #DataStructures #Algorithms #Stack #Unix #FileSystems #LeetCode #ProblemSolving #SoftwareEngineering #CodingInterview