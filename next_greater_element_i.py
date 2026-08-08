'''
The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.

You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.

For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.

Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.

Example:
Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
Explanation: The next greater element in nums2 for each value of nums1 is as follows:
- 4: There is no next greater element, so the answer is -1.
- 1: The next greater element is 3.
- 2: There is no next greater element, so the answer is -1.

Constraints:
1 <= nums1.length <= nums2.length <= 1000
0 <= nums1[i], nums2[i] <= 104
All integers in nums1 and nums2 are unique.
All the integers of nums1 also appear in nums2.
'''
from typing import List


def next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:
    if not set(nums1) <= set(nums2):
        raise ValueError("nums1 must be a subset of nums2")

    # Create a dictionary to store the next greater element for each number in nums2
    next_greater = {}
    stack = []

    # Process nums2 from right to left
    for num in reversed(nums2):
        # Remove elements from the stack that are smaller than the current number
        while stack and stack[-1] < num:
            stack.pop()
        # If the stack is not empty, the top element is the next greater element
        next_greater[num] = stack[-1] if stack else -1
        # Push the current number onto the stack
        stack.append(num)

    # Return the results for each number in nums1
    return [next_greater[num] for num in nums1]