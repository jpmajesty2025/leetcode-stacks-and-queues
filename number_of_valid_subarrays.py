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
'''

def valid_subarrays(nums: list[int]) -> int:
    count = 0
    n = len(nums)
    
    for i in range(n):
        # Start a new subarray from index i
        count += 1  # Count the single element subarray [nums[i]]
        
        # Extend the subarray to the right as long as the condition holds
        for j in range(i + 1, n):
            if nums[j] >= nums[i]:
                count += 1
            else:
                break  # Stop extending if we find an element smaller than nums[i]
    
    return count