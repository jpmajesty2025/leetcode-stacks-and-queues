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
'''

from typing import List
from collections import deque


def longest_subarray(nums: List[int], limit: int) -> int:
    if limit < 0:
        raise ValueError("limit must be non-negative")

    increasing: deque[int] = deque()
    decreasing: deque[int] = deque()
    left = ans = 0

    for right in range(len(nums)):
        # maintain the monotonic deques
        while increasing and increasing[-1] > nums[right]:
            increasing.pop()
        while decreasing and decreasing[-1] < nums[right]:
            decreasing.pop()

        increasing.append(nums[right])
        decreasing.append(nums[right])

        # maintain window property
        while decreasing[0] - increasing[0] > limit:
            if nums[left] == decreasing[0]:
                decreasing.popleft()
            if nums[left] == increasing[0]:
                increasing.popleft()
            left += 1

        ans = max(ans, right - left + 1)

    return ans