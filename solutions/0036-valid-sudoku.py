"""36. Valid Sudoku (Medium) —— 专题：数组 & 哈希表

思路：一遍扫描，同时维护三个维度的「已出现数字」：
  rows[i]  第 i 行的已见数字
  cols[j]  第 j 列的已见数字
  boxes[b] 第 b 个 3x3 宫的已见数字，b = (i // 3) * 3 + j // 3   （宫号 0~8）

一个格子同时属于「1 行 + 1 列 + 1 宫」，三者都是「不能重复」的集合，
所以一次扫描就能同时维护，不必扫三遍 —— 一行公式代替 9 段手写 if。

时间 O(81) = O(1)（棋盘固定 9x9），空间 O(81)。

2026-09-21 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        rows  = [set() for _ in range(9)]
        cols  = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for i in range(9):
            for j in range(9):
                v = board[i][j]
                if v == ".":
                    continue                       # 空位跳过
                b = (i // 3) * 3 + j // 3          # 这一格的宫号 0~8
                if v in rows[i] or v in cols[j] or v in boxes[b]:
                    return False                   # 三个维度任一重复 -> 不合法
                rows[i].add(v)
                cols[j].add(v)
                boxes[b].add(v)
        return True


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/02-数组与哈希表.md 第九节）
#
# 1. 嵌套 for 不能挤一行：`for i in range(0,9), for j in range(0,9):` -> SyntaxError
# 2. `d.get(k, 默认值)` 只【返回】、不写入！d.get(1, set()) 之后 d 还是 {}，
#    想写入得用 d.setdefault(1, set())。
# 3. board 下标是 0~8 不是 1~9：手写 9 段 `1<=i<=3 ...` 的 if 只覆盖 64/81 格，
#    第 0 行 9 格 + 第 0 列 8 格完全没被检查（(0,0) 从不进任何宫判断）。
# 4. 9 段几乎一样的代码 = 缺一个公式：宫号 = (i // 3) * 3 + j // 3。
# 5. `[set()] * 9` 是同一个 set 的引用（第三次踩这个坑，前两次是 347 的 [[]]*n），
#    必须写 `[set() for _ in range(9)]`。
# ---------------------------------------------------------------------------
