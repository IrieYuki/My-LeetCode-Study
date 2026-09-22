"""49. Group Anagrams (Medium) —— 专题：数组 & 哈希表

思路（一句话）：anagram 之间只差「字母顺序」，所以把顺序抹掉得到同一个 key，
再用 dict 把 key 相同的词分到一组。

两种解法均已于 2026-09-21 在 LeetCode AC：
  解法 1  key = tuple(sorted(s))       时间 O(n · k log k)  ← 排序是主要开销
  解法 2  key = tuple(26 个字母计数)    时间 O(n · k)        ← 不排序

空间同为 O(n · k)：存 n 个词的引用 + 每个不同 key 自身长度 k。
"""

from typing import List


class Solution:
    """解法 1：把单词排序后当 key（本题 AC 版本）"""

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = {}

        for s in strs:
            key = tuple(sorted(s))  # list 不能当 key；tuple 可以（不可变）
            if key in d:
                d[key].append(s)  # dict 的 key 查找平均 O(1)
            else:
                d[key] = [s]  # key 第一次出现，先建一个空 list 再装

        return list(d.values())  # 返回 list[list[str]]，不是 dict


class Solution2:
    """解法 2：26 个字母的计数表当 key（不排序，算 key 只要 O(k)）"""

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = {}

        for s in strs:
            counts = [0] * 26  # 每个词一张全新的表（必须在循环体内）
            for ch in s:
                counts[ord(ch) - ord('a')] += 1  # 'a'→0 … 'z'→25
            key = tuple(counts)  # 26 个数字，长度固定 → 位置可比

            if key in d:
                d[key].append(s)
            else:
                d[key] = [s]

        return list(d.values())


# ---------------------------------------------------------------------------
# 本题踩过的坑（详见 leetcode-notes/02-数组与哈希表.md）
#
# 1. 语法：elif: 后面必须有条件；想表达「否则」用 else:
# 2. 不要额外维护一个 seen = [] 来记录 key：
#      if key in seen   -> list 线性查找，实测比 if key in d 慢 121 倍
#      d 的 keys 本身就是「见过的所有 key」，seen 完全是重复信息
# 3. 返回值类型要匹配签名：return d 给的是 dict，必须 return list(d.values())
# 4. 计数表（解法 2）的两处坑：
#      a) 建在循环外 -> 跨词累加，["eat","tea","ate"] 被拆成 3 组
#      b) 用 dict 当计数表，tuple(counts) 只会取到【键】、丢掉次数，
#         key 退化成「字母种类」，["aab","abb"] 会被并成一组
# 5. 计数表必须【定长 26】+ 位置稳定，不同词的 key 才能逐位比较
# ---------------------------------------------------------------------------
