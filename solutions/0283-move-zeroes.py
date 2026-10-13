"""283. Move Zeroes (Easy) —— 专题：双指针（「读写指针」形态）

题目要求：把非零元素保持相对顺序移到前面，0 挪到最后，**原地修改**。
坑点：函数签名是 `-> None`，不返回任何东西；要改的是【传进来的 nums 这个对象本身】。
      所以不能写 `nums = [新列表]`（那只是让局部变量指向新对象），也不用 return。

两个版本：
  读写指针 O(n)：slow 指着「下一个非零该放的位置」，fast 负责找下一个非零
  暴力交换 O(n²)：碰到 0 就在后面找第一个非零交换过来
实测（n = 10^4）：0.212 ms vs 168.0 ms（792 倍）。

2026-10-02 AC 版本如下（一字未改）。
"""

from typing import List


class Solution:
    """读写指针版（AC）：O(n) 时间、O(1) 额外空间"""

    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        slow = 0                              # slow 指着「下一个非零元素该放的位置」
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]   # 把非零搬到 slow 处
                slow += 1                                        # slow 前进一格

        # 不变量：slow 左边的区域【始终】是已经归位好的非零元素，fast 负责找下一个非零


class Solution2:
    """暴力交换版：O(n²)，能 AC（n <= 10^4）但不是考点"""

    def moveZeroes(self, nums: List[int]) -> None:
        n = len(nums)
        for i in range(n):
            if nums[i] == 0:                         # 碰到 0
                for j in range(i + 1, n):            # 在它后面找
                    if nums[j] != 0:                 # 第一个非零
                        nums[i], nums[j] = nums[j], nums[i]
                        break                        # 换完就跳出
        # 交换而不是覆盖是关键：非零搬到前面时，0 得有地方去


# ---------------------------------------------------------------------------
# 踩坑记录（详见 leetcode-notes/03-双指针.md 第六节）
#
# 1. `if nums[i-1] != 0 and nums[i] = 0:` —— 条件里用了赋值号 -> SyntaxError。
#    = 是「做动作」，== 才是「问相等吗」。
# 2. `for i in range(len(nums), 0, -1)` 里访问 nums[i] -> IndexError（i 最大到 len）。
#    从右往左扫要么从 len-1 开始，要么别访问 nums[i]。
# 3. `while nums[j] != 0` 里 j 从不变化 -> 死循环（第三次踩：128 的 num+1、347 的指针不移动）。
# 4. `i += 1` 改 for 的循环变量 -> 下一轮被 range 覆盖（167 讲过的无效操作）。
# 5. 「原地」的含义：`nums = [...]` 不算原地（新对象），必须 `nums[i] = ...` 或交换。
# ---------------------------------------------------------------------------
