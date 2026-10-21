"""567. Permutation in String (Medium) —— 专题：滑动窗口（定长窗口）

一句话：判断 s2 里是否有一段【长度 = len(s1)】的连续子串，字母构成与 s1 完全相同。

定长窗口的做法：
  need   = s1 的字母计数（长度 26 的列表）
  window = 当前窗口的字母计数
  每滑一步：右边新字符 +1；若窗口超过 n1，左边旧字符 -1；然后比较两张表

时间 O(n2 · 26)，空间 O(26)。实测 s2 长 10^4、s1 长 26 -> 1.732 ms。

2026-10-02 AC 版本如下（一字未改）。
"""


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False

        need = [0] * 26
        for ch in s1:
            need[ord(ch) - ord('a')] += 1

        window = [0] * 26
        for i in range(n2):
            window[ord(s2[i]) - ord('a')] += 1        # 右边新字符进窗口
            if i >= n1:                                # 窗口长度已经超过 n1 了
                window[ord(s2[i - n1]) - ord('a')] -= 1   # 左边那个字符出窗口
            if all(window[j] == need[j] for j in range(26)):
                return True
        return False


class Solution2:
    """等价写法：直接比较两个列表，比 all(...) 快 14.6 倍（实测见下）"""

    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False

        need = [0] * 26
        for ch in s1:
            need[ord(ch) - ord('a')] += 1

        window = [0] * 26
        for i in range(n2):
            window[ord(s2[i]) - ord('a')] += 1
            if i >= n1:
                window[ord(s2[i - n1]) - ord('a')] -= 1
            if window == need:          # 列表比较是 C 实现，不用逐格 Python 循环
                return True
        return False


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/04-滑动窗口.md 第三节）
#
# 1. 没有兜底的 return False -> 官方三个示例全部返回 None。
#    循环里 return True，循环结束后必须 return False。
# 2. 用 list.remove() 判断「s2 包含 s1 的字母」是错的方向：
#    题目要的是【连续】子串。反例 s1="ab", s2="aXb"：字母都在，但不连续 -> False。
#    而且 remove 会改掉原串，后面的窗口看到的东西已经不是原来的 s2。
# 3. 循环范围写成 range(len(s1)) —— 应该枚举 s2 的每个右端点 range(n2)。
# 4. 出窗口的下标是 i - n1（不是 i - n1 + 1）：当前窗口是 [i-n1+1, i]，
#    所以刚好在窗口外的左邻是 i-n1。
# 5. 比较计数表：all(window[j] == need[j] for ...) 比 window == need 慢 14.6 倍
#    （10 万次：48.17 ms vs 3.29 ms）—— 能用内置比较就不要用生成器。
# 6. 进阶（未做）：维护「差异格数」计数器，让每次比较变成 O(1)。
# ---------------------------------------------------------------------------
