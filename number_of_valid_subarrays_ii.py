'''
Given an integer array nums, return the number of non-empty subarrays with the leftmost element of the subarray not larger 
than other elements in the subarray. A subarray is a contiguous part of an array.

Example 1:

Input: nums = [1,4,2,5,3]
Output: 11
Explanation: There are 11 valid subarrays: [1],[4],[2],[5],[3],[1,4],[2,5],[1,4,2],[2,5,3],[1,4,2,5],[1,4,2,5,3].
Example 2:

Input: nums = [3,2,1]
Output: 3
Explanation: The 3 valid subarrays are: [3],[2],[1].
Example 3:

Input: nums = [2,2,2]
Output: 6
Explanation: There are 6 valid subarrays: [2],[2],[2],[2,2],[2,2],[2,2,2].
 

Constraints:

1 <= nums.length <= 5 * 104
0 <= nums[i] <= 105

---
Monotonic-stack solution.

A subarray starting at index i is valid for every end index up to (but not including)
the first later index j where nums[j] < nums[i] -- once a strictly smaller element
appears, nums[i] is no longer the minimum of the range, so no further extension can be
valid. So the number of valid subarrays starting at i is exactly
(next_smaller_index(i) - i), where next_smaller_index(i) defaults to n when no such
element exists (the subarray can extend all the way to the end).

This is the classic "next strictly smaller element to the right" pattern, solved with a
monotonic increasing stack of indices: process left to right, and whenever the current
value is strictly smaller than the value at the stack's top index, that top index has
found its next-smaller boundary at the current index -- pop it and settle its count.
Anything left on the stack at the end extends all the way to n.
'''


def valid_subarrays(nums: list[int]) -> int:
    count = 0
    pending_indices: list[int] = []

    for index, value in enumerate(nums):
        while pending_indices and nums[pending_indices[-1]] > value:
            start = pending_indices.pop()
            count += index - start
        pending_indices.append(index)

    n = len(nums)
    while pending_indices:
        start = pending_indices.pop()
        count += n - start

    return count
