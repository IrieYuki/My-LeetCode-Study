"""128. Longest Consecutive Sequence (Medium) —— 专题：数组 & 哈希表

一句话：用 set 换来 O(1) 的「某个数在不在」查询，然后只从每一段的【起点】往后数。

时间 O(n)，空间 O(n)。判断起点的那句 `if` 是省掉 O(n²) 的关键：
不是起点就跳过，而每个数字只属于一个连续段、只有起点会触发 while，
所以所有段被数的总次数 <= n。

2026-09-21 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    """AC 版本：哈希集 + 只从起点往后数"""

    def longestConsecutive(self, nums: List[int]) -> int:
        s = set(nums)          # 只为了一件事：O(1) 查「某个数在不在」
        best = 0
        for num in s:
            if num - 1 not in s:               # 没有前驱 -> 这是一段的起点
                length = 1
                while num + length in s:
                    length += 1
                best = max(best, length)
        return best


class Solution2:
    """对照解法：排序 + 比对相邻差。O(n log n)，但 Python 实测常数更小"""

    def longestConsecutive(self, nums: List[int]) -> int:
        vals = sorted(set(nums))
        if not vals:
            return 0
        best = cur = 1
        for i in range(1, len(vals)):
            cur = cur + 1 if vals[i] - vals[i - 1] == 1 else 1
            best = max(best, cur)  # 每轮都更新，天然覆盖「最后一段」的收尾问题
        return best


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/02-数组与哈希表.md 第八节）
#
# 1. `sorted(set(nums))` 之后直接 len()：算的是「有多少个不同的数」，
#    不是「最长连续段有多长」。实测 4/6 通过——没有断口时两者恰好相等（蒙对），
#    一有孤立数字就错：[100,4,200,1,3,2] 得 6，正确答案 4。
# 2. while 的条件里参与判断的东西不推进 -> 死循环：
#    `while num + 1 in s: length += 1`（num 从头到尾没变，条件恒真）；
#    实测 5 秒跑不完，LeetCode 上就是 TLE。
#    正解：`while num + length in s` 或引入游标 cur。
# 3. 排序版收尾：最后一段要单独比一次（本文件写法是每轮更新 best，天然覆盖）。
# 4. 「复杂度更优 != 更快」：n=10^5 实测 set 版 4.94 ms、排序版 4.51 ms
#    —— sorted 是 C 实现的，set 版是解释器逐元素循环，常数因子更大。
# ---------------------------------------------------------------------------
