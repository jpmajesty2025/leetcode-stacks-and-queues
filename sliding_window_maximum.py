'''
Given an integer array nums and an integer k, there is a sliding window of size k that moves from the very left to the very right. For each window,
find the maximum element in the window.

For example, given nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3, return [3, 3, 5, 5, 6, 7]. The first window is [[1, 3, -1], -3, 5, 3, 6, 7]
and the last window is [1, 3, -1, -3, 5, [3, 6, 7]]
'''

from collections import deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and the length of nums")

    maximums: list[int] = []
    candidate_indices: deque[int] = deque()

    for right, value in enumerate(nums):
        # Maintain monotonically decreasing values. Smaller candidates cannot
        # be maximums in this or any future overlapping window.
        while candidate_indices and nums[candidate_indices[-1]] < value:
            candidate_indices.pop()

        candidate_indices.append(right)

        left = right - k + 1
        while candidate_indices and candidate_indices[0] < left:
            candidate_indices.popleft()

        if right >= k - 1:
            maximums.append(nums[candidate_indices[0]])

    return maximums
