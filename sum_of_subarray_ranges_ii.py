'''
You are given an integer array nums. The range of a subarray of nums is the difference between the largest and smallest 
element in the subarray.

Return the sum of all subarray ranges of nums.

A subarray is a contiguous non-empty sequence of elements within an array.

 

Example 1:

Input: nums = [1,2,3]
Output: 4
Explanation: The 6 subarrays of nums are the following:
[1], range = largest - smallest = 1 - 1 = 0 
[2], range = 2 - 2 = 0
[3], range = 3 - 3 = 0
[1,2], range = 2 - 1 = 1
[2,3], range = 3 - 2 = 1
[1,2,3], range = 3 - 1 = 2
So the sum of all ranges is 0 + 0 + 0 + 1 + 1 + 2 = 4.
Example 2:

Input: nums = [1,3,3]
Output: 4
Explanation: The 6 subarrays of nums are the following:
[1], range = largest - smallest = 1 - 1 = 0
[3], range = 3 - 3 = 0
[3], range = 3 - 3 = 0
[1,3], range = 3 - 1 = 2
[3,3], range = 3 - 3 = 0
[1,3,3], range = 3 - 1 = 2
So the sum of all ranges is 0 + 0 + 0 + 2 + 0 + 2 = 4.
Example 3:

Input: nums = [4,-2,-3,4,1]
Output: 59
Explanation: The sum of all subarray ranges of nums is 59.
 

Constraints:

1 <= nums.length <= 1000
-109 <= nums[i] <= 109

---
Monotonic-stack solution.

The sum of subarray ranges decomposes into (sum of subarray maxima) - (sum of subarray
minima), since range = max - min for every subarray and summation distributes over the
subtraction.

Each half is computed with the same "sum of extrema ending at each index" technique used
in sum_of_subarray_mins.py: for every index j, sum_min_ending_at(j) is the sum of the
minimum of every subarray that ends at j. Maintaining a monotonic stack of
(value, count) pairs -- where count is how many subarrays ending at the current index
share that value as their extremum -- lets each index be processed in amortized O(1),
because popping a stack entry folds its count and contribution into the new element
before it is pushed. Summing sum_min_ending_at(j) over all j gives the total sum of
subarray minima in O(n); the mirrored stack (with the opposite comparison direction)
gives the total sum of subarray maxima in the same pass. Ties are resolved consistently
(next element with stack[-1][0] >= num / <= num absorbs equal-valued predecessors) so no
subarray is double-counted regardless of duplicate values.
'''


def sum_subarray_ranges(nums: list[int]) -> int:
    min_stack: list[tuple[int, int]] = []
    max_stack: list[tuple[int, int]] = []

    min_running_total = 0
    max_running_total = 0
    min_dot = 0
    max_dot = 0

    for num in nums:
        min_count = 1
        while min_stack and min_stack[-1][0] >= num:
            prev_num, prev_count = min_stack.pop()
            min_count += prev_count
            min_dot -= prev_num * prev_count
        min_stack.append((num, min_count))
        min_dot += num * min_count
        min_running_total += min_dot

        max_count = 1
        while max_stack and max_stack[-1][0] <= num:
            prev_num, prev_count = max_stack.pop()
            max_count += prev_count
            max_dot -= prev_num * prev_count
        max_stack.append((num, max_count))
        max_dot += num * max_count
        max_running_total += max_dot

    return max_running_total - min_running_total