"""167. Two Sum II - Input Array Is Sorted (Medium) —— 专题：双指针

一句话：数组**已排序**，所以可以从两端往中间夹逼 ——
  和太小 -> 左指针右移（右边的数已经是最大的了，配上左端还不够，说明左端这个数可以永久排除）
  和太大 -> 右指针左移（左边的数已经是最小的了，配上右端都太大，说明右端这个数可以永久排除）
每一步至少排除一个候选，总步数 <= n。

时间 O(n)，空间 O(1) —— 后者正是题目 Follow-up 的要求，也是这题不能用哈希表的原因
（1. Two Sum 用哈希表是 O(n) 空间）。注意返回的是 **1-indexed** 下标。

2026-09-21 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:

        left, right = 0, len(numbers) - 1  # 一个指最小，一个指最大
        while left < right:
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]  # 题目要 1-indexed
            elif s < target:
                left += 1                     # 和太小 -> 左指针右移
            else:
                right -= 1                    # 和太大 -> 右指针左移


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/03-双指针.md 第二节）
#
# 1. 第一版写成 O(n^2) 双层 for，完全没用上「数组已排序」这个条件：
#    实测最坏情况 n=10^4 要 973 ms（双指针 0.310 ms），题目上限 3*10^4 必然 TLE。
#    教训：「题目给了什么条件，就用上什么条件」—— 有序 = 内层循环可以省掉。
# 2. 在 for 里手改循环变量是无效的（range 每轮重新赋值）：
#      for left in range(len(numbers)):
#          ...
#          left += 1        <- 下一轮就被覆盖
#    更糟的是 return [left + 1, ...] 会用上被改过的值 ->
#    官方示例 2 [2,3,4], target=6 返回 [2,3]（正确 [1,3]）。
#    要手动移动指针，必须用 while。
# 3. 下标基准：167 要 1-indexed（left + 1），1. Two Sum 是 0-indexed。
# 4. 类型检查提示（Pyright）：函数声明 -> List[int]，但「找不到」时没有 return，
#    会隐式返回 None。LeetCode 保证恰好有一个解，所以能过；工程代码里应兜底
#    `return []` 或 `raise ValueError(...)`。
# ---------------------------------------------------------------------------
