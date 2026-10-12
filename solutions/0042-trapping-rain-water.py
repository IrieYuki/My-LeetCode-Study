"""42. Trapping Rain Water (Hard) —— 专题：双指针

公式（物理含义）：水位 = min(左边最高柱, 右边最高柱)；本格水 = 水位 - 自己高度。

本题写了三层，逐层优化（这也是本题最大的收获）：
  层 1 暴力   每格往左往右各扫一遍求最高        O(n²) 时间 / O(1) 空间   -> TLE（但逻辑正确）
  层 2 数组   左右最高各扫一遍提前存成数组      O(n)  时间 / O(n) 空间   -> AC，2.398 ms
  层 3 双指针 边走边维护 left_max / right_max   O(n)  时间 / O(1) 空间   -> AC，1.175 ms（本文件 AC 版）
（耗时为本机 n = 2×10^4 实测。）

2026-10-02 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    """层 3（AC）：双指针 + 两个变量，空间 O(1)"""

    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = 0
        right_max = 0
        water = 0

        while left < right:
            left_max = max(left_max, height[left])      # 先更新两边各自见过的最高
            right_max = max(right_max, height[right])

            if left_max < right_max:
                # left 右边一定存在 >= right_max 的柱子，而 right_max > left_max
                # => min(左边最高, 右边最高) 已确定为 left_max，可以结算 left
                water += left_max - height[left]
                left += 1
            else:
                water += right_max - height[right]
                right -= 1

        return water


class Solution2:
    """层 2：左右最高提前算成数组，时间 O(n)、空间 O(n)"""

    def trap(self, height: List[int]) -> int:
        n = len(height)
        if n == 0:
            return 0
        left_max = [0] * n
        right_max = [0] * n

        cur = 0
        for i in range(n):
            cur = max(cur, height[i])
            left_max[i] = cur

        cur = 0
        for i in range(n - 1, -1, -1):
            cur = max(cur, height[i])
            right_max[i] = cur

        water = 0
        for i in range(n):
            water += min(left_max[i], right_max[i]) - height[i]
        return water


class Solution3:
    """层 1：暴力，O(n²) —— 会 TLE，但它是理解题意和公式的必经一步"""

    def trap(self, height: List[int]) -> int:
        water = 0
        for i in range(len(height)):
            lm = 0
            for j in range(0, i + 1):
                lm = max(lm, height[j])
            rm = 0
            for j in range(i, len(height)):
                rm = max(rm, height[j])
            water += min(lm, rm) - height[i]
        return water


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/03-双指针.md 第五节）
#
# 1. `height(left)` 用圆括号 -> TypeError: 'list' object is not callable
#    （第二次犯，前一次是 strs(s)）—— list 只能用 []，() 是「调用函数」。
# 2. 求最高的变量写在循环【里面】-> 每轮被重置：
#    实测 height=[3,1,0,2]、i=0 时得到 rm=2（正确是 3）。
#    累加/求最值类变量的初值必须在循环外。
# 3. 初值给 1 而不是 0 —— 高度全为 0 的段会被算出假水。
# 4. 多写一层 `for i in weight` -> NameError，且这层循环根本不需要。
# 5. `return` 缩进在 for 里面 -> 处理完第一格就返回。
# 6. TLE 不是失败：它说明「逻辑对了，只是慢」，是优化的起点。
# ---------------------------------------------------------------------------
