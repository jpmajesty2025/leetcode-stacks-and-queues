'''
Given an array of integers nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to limit.

Example 1:

Input: nums = [8,2,4,7], limit = 4
Output: 2 
Explanation: All subarrays are: 
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4. 
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4. 
Therefore, the size of the longest subarray is 2.

This is an index-based variant of longest_cts_subarray_with_abs_diff_lte_limit.py.
Both monotonic deques store indices (not values), mirroring the approach used
in sliding_window_maximum.py. Eviction from the front compares the stored
index against the window's left boundary rather than comparing values, which
avoids the ambiguity that arises when duplicate values are present.
'''

from typing import List
from collections import deque


def longest_subarray(nums: List[int], limit: int) -> int:
    if limit < 0:
        raise ValueError("limit must be non-negative")

    increasing: deque[int] = deque()  # indices with increasing nums values
    decreasing: deque[int] = deque()  # indices with decreasing nums values
    left = ans = 0

    for right in range(len(nums)):
        # maintain the monotonic deques
        while increasing and nums[increasing[-1]] > nums[right]:
            increasing.pop()
        while decreasing and nums[decreasing[-1]] < nums[right]:
            decreasing.pop()

        increasing.append(right)
        decreasing.append(right)

        # maintain window property by advancing the left boundary and
        # evicting any front index that has fallen outside the window
        while nums[decreasing[0]] - nums[increasing[0]] > limit:
            left += 1
            if increasing[0] < left:
                increasing.popleft()
            if decreasing[0] < left:
                decreasing.popleft()

        ans = max(ans, right - left + 1)

    return ans