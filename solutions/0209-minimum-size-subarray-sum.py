"""209. Minimum Size Subarray Sum (Medium) —— 专题：滑动窗口（阶段 3 入门）

一句话：找【和 >= target 的最短连续子数组】。因为元素全为正数，窗口和随右端点单调不减
-> 右端点一路扩张，一旦达标就收缩左端点找更短 —— 这就是「变长滑动窗口」通用模板。

两个版本（都 AC）：
  滑窗 O(n)：right 扩张 + while 收缩，每个元素最多进一次、出一次
  暴力 O(n²)：固定 left，往后累加到达标就记录并 break
实测（n = 10^5）：滑窗 4.655 ms vs 暴力 31255 ms（约 6700 倍）。

2026-10-02 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    """变长滑动窗口（AC）：O(n) 时间、O(1) 额外空间"""

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        left = 0
        total = 0
        result = float('inf')
        for right in range(len(nums)):
            total += nums[right]
            while total >= target:                  # 达标就收缩，找更短的
                result = min(result, right - left + 1)
                total -= nums[left]
                left += 1
        return result if result != float('inf') else 0


class Solution2:
    """暴力版：固定 left 往后累加，O(n²)（会 TLE，先写它把题意搞对）"""

    def minSubArrayLen(self, target: int, nums: List[int]) -> int:

        result = float('inf')

        for left in range(len(nums)):
            get = nums[left]
            if get >= target:
                result = 1
                break                               # 长度 1 已经是最小，不用再找了

            else:
                for right in range(left + 1, len(nums), 1):
                    get += nums[right]
                    if get >= target:
                        result = min(right - left + 1, result)
                        break

        return result if result != float('inf') else 0


# ---------------------------------------------------------------------------
# 笔记（详见 leetcode-notes/04-滑动窗口.md）
#
# 1. 滑动窗口的前提：窗口内的「状态」必须单调（本题元素全为正 -> 和单调不减），
#    所以右端点扩张到刚达标时，任何更长的窗口都不可能更优，可以放心收缩。
# 2. 通用模板：
#       left = 0; state = ...
#       for right in range(n):
#           把 nums[right] 纳入 state
#           while 需要收缩:
#               更新答案
#               把 nums[left] 移出 state; left += 1
# 3. 复杂度 O(n)：每个元素最多被纳入一次、移出一次。
# 4. 返回值细节：找不到答案要返回 0（不是 -1）；「哨兵」用 float('inf') 比 -1 更清晰。
# 5. 暴力版里那个 break 是对的：长度 1 已是最小可能值，无需继续。
# 6. 类型检查提示（Pyright）：哨兵是 float，而签名声明返回 int，
#    `result if result != float('inf') else 0` 会被判为 float | int。
#    LeetCode 能过；严格类型检查的工程里可初始化成 result = n + 1，或 return int(result)。
# ---------------------------------------------------------------------------
