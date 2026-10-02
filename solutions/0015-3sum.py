"""15. 3Sum (Medium) —— 专题：双指针

思路：排序 + 固定一个数 + 双指针（降维）
  1. nums.sort()：让重复值相邻，双指针才成立；
  2. 固定 nums[i]，在 i+1..n-1 区间里找两数之和 = -nums[i]（就是 167 的左右夹逼）；
  3. 三道去重关：外层 i、命中后左边、命中后右边。

时间 O(n²)（外层 n × 内层夹逼 O(n)），空间 O(1)（排序原地，不计输出）。题目 n <= 3000。

2026-10-02 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:

        nums.sort()                                  # 排序是双指针的前提
        res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:     # 去重关 1：外层，跳过重复的固定数
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    res.append([nums[i], nums[l], nums[r]])

                    l += 1
                    while l < r and nums[l] == nums[l - 1]:   # 去重关 2：左边跳过刚用过的值
                        l += 1
                    r -= 1
                    while l < r and nums[r] == nums[r + 1]:   # 去重关 3：右边对称
                        r -= 1

                elif s > 0:
                    r -= 1
                else:
                    l += 1
        return res


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/03-双指针.md 第四节）
#
# 1. `s = nums.sort()`：list.sort() 是原地排序、返回 None ->
#    s[i] 报 TypeError: 'NoneType' object is not subscriptable。
#    正确：nums.sort() 后一直用 nums，或 s = sorted(nums)。
# 2. 去重条件写反：`if i == 0 or nums[i] != nums[i-1]` 会跳掉第一个数、
#    却放过真正重复的值。判据必须是【等于前一个】才跳过。
# 3. 找到第一个解就 return：题目要【所有】三元组，只能收集到 res 里继续找。
# 4. 内层不跳过重复 -> [-2,0,0,2,2] 返回 [[-2,0,2], [-2,0,2]]（同一组两次）。
# 5. 命中后不移动指针 -> 条件完全相同的死循环。
# 6. 变量名撞车：s 一会儿是排序结果、一会儿是三数之和，会被覆盖成整数。
# 7. 内层不要再手写一遍两数之和：命中后只做「移动 + 跳过重复」，
#    搜索交回外层 while。
# ---------------------------------------------------------------------------
