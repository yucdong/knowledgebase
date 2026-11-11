# 题目

题目大全，根据题号整理
主要优先训练 top 150题

## 169

major nums 

给定一个大小为 n 的数组 nums ，返回其中的多数元素。多数元素是指在数组中出现次数 大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

 

示例 1：

输入：nums = [3,2,3]
输出：3
示例 2：

输入：nums = [2,2,1,1,1,2,2]
输出：2

class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        counter = Counter(nums)
        major_nums = [k for k in counter.keys() if counter[k] * 2 > len(nums)]
        return major_nums[0]

