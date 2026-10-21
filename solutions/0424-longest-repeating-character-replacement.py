"""424. Longest Repeating Character Replacement (Medium) —— 专题：滑动窗口

判据（这题的核心）：窗口 [left, right] 若「最多替换 k 个字符后能全相同」，则
    窗口长度 - 窗口内出现次数最多的字符的频次 <= k
因为窗口里除了那个最高频字符，其余字符都得被替换掉。

时间 O(n · 26)（每次收缩重算 max(count)），空间 O(26)。
实测 n = 10^5：40.085 ms。进阶写法（maxf 只增不减）11.190 ms，见 Solution2。

2026-10-02 AC 版本如下（一字未改）。
"""


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = [0] * 26
        left = 0
        ans = 0
        for right in range(len(s)):
            count[ord(s[right]) - ord('A')] += 1     # 右边进来
            while right - left + 1 - max(count) > k:  # 不合法：需要替换的字符数超过 k
                count[ord(s[left]) - ord('A')] -= 1   # 左边出去
                left += 1
            ans = max(ans, right - left + 1)          # 此刻窗口合法
        return ans


class Solution2:
    """进阶：maxf 只增不减，省掉每次的 max(count)，O(n)

    正确性的关键在于「窗口长度单调不减」：right 每步 +1，而 maxf 不会下降，
    所以 while 最多收缩 1 格 -> 窗口长度只会增加或保持不变。
    ⚠️ 这个论证是本题最绕的一处（很多题解不解释），面试建议先给 O(n·26) 版本。
    实测与上面版本在 2000 组随机数据上完全一致。
    """

    def characterReplacement(self, s: str, k: int) -> int:
        count = [0] * 26
        left = 0
        maxf = 0
        ans = 0
        for right in range(len(s)):
            count[ord(s[right]) - ord('A')] += 1
            maxf = max(maxf, count[ord(s[right]) - ord('A')])
            while right - left + 1 - maxf > k:
                count[ord(s[left]) - ord('A')] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/04-滑动窗口.md 第四节）
#
# 1. 计数表 ch 建在循环外且从不清零 -> 每个 left 都在前面累积的数据上继续加，
#    判据全错（实测 7 个用例全部失败）。
#    滑窗的正确做法：表跟着窗口走 —— 右边进 +1、左边出 -1。
# 2. 顺序错：必须先「把 s[right] 加进计数表」再判断，否则判的是旧窗口。
# 3. 符号错：合法条件是 `长度 - 最高频 <= k`，写成 `< k` 时 k=0 永远不成立。
# 4. 两个 if 都不成立时 right/left 都不动 -> 死循环（实测步数超限）。
#    不合法时应收缩左端（left += 1），不是等 right 动。
# 5. 外层 for 写成 range(len(s) - k)：范围应该就是 range(len(s))。
# 6. `if k >= len(s) - 1: return len(s)` 这个特判不算错，但滑窗本身也能处理。
# ---------------------------------------------------------------------------
