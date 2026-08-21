'''
Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. 
Since the answer may be large, return the answer modulo 10**9 + 7.

 

Example 1:

Input: arr = [3,1,2,4]
Output: 17
Explanation: 
Subarrays are [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4]. 
Minimums are 3, 1, 2, 4, 1, 1, 2, 1, 1, 1.
Sum is 17.
Example 2:

Input: arr = [11,81,94,43,3]
Output: 444
 

Constraints:

1 <= arr.length <= 3 * 104
1 <= arr[i] <= 3 * 104
'''

def sum_subarray_mins(arr: list[int]) -> int:
    stack = []
    result = 0
    # dot tracks the sum of minimums of every subarray ending at the
    # current index; result accumulates dot across all indices.
    dot = 0
    mod = 10**9 + 7

    for num in arr:
        count = 1
        while stack and stack[-1][0] >= num:
            prev_num, prev_count = stack.pop()
            count += prev_count
            dot -= prev_num * prev_count
        stack.append((num, count))
        dot += num * count
        result += dot
        result %= mod

    return result