"""49. Group Anagrams (Medium) —— 专题：数组 & 哈希表

思路（一句话）：anagram 之间只差「字母顺序」，所以把顺序抹掉得到同一个 key，
再用 dict 把 key 相同的词分到一组。

复杂度：时间 O(n · k log k)（n 个词，每个词排序 k log k）｜空间 O(n · k)

本题是 2026-09-21 的第一题，AC 版本如下（同时也是「key 设计」这一课的原型）。
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


# ---------------------------------------------------------------------------
# 本题踩过的坑（详见 leetcode-notes/02-数组与哈希表.md）
#
# 1. 语法：elif: 后面必须有条件；想表达「否则」用 else:
# 2. 不要额外维护一个 seen = [] 来记录 key：
#      if key in seen   -> list 线性查找，实测比 if key in d 慢 121 倍
#      d 的 keys 本身就是「见过的所有 key」，seen 完全是重复信息
# 3. 返回值类型要匹配签名：return d 给的是 dict，必须 return list(d.values())
#
# 待补：解法 2 —— 用「26 个字母的计数表」当 key，把 O(k log k) 降到 O(k)，
#       整体时间 O(n·k)。（自行补全后同步到本文件与笔记）
# ---------------------------------------------------------------------------
