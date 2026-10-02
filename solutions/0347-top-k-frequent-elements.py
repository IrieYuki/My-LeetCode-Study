"""347. Top K Frequent Elements (Medium) —— 专题：数组 & 哈希表

思路（两步走）：
  1. 计数：dict 记「数字 -> 出现次数」                       O(n)
  2. 把 d.items()（(数字, 次数) 对）按【次数】降序排，
     取前 k 个的【数字】                                    O(m log m)
  m = 不同数字的个数（≤ n）-> 总时间 O(n + m log m)，最坏 O(n log n)；空间 O(m)

Follow-up（题目要求优于 O(n log n)）—— 三个版本都在本文件，均已验证：
  Solution   计数 + 全排序          O(n + m log m)   空间 O(m)
  Solution2  计数 + nlargest 堆     O(n + m log k)   空间 O(m + k)
  Solution3  计数 + 桶（次数当下标）  O(n)             空间 O(n + m)

同一组数据实测（n = 10^5，ms，3 次取最好）：
  场景                   排序     堆      桶
  m≈n, k=10             6.97    4.87   10.42
  m≈n, k=1000           7.07    4.86    9.80
  m≈n, k=50000          7.37   14.57    9.89
  m=100, k=10           2.13    2.15    8.50
结论：k 小用堆；k 接近 m 时全排序反而更快；桶是 O(n) 但常数大（要开 n+1 个空 list）。
      复杂度更优 != 跑得更快，选哪个要看 k 和 m 的关系。

2026-10-02 AC 版本如下（一字未改）。
"""

import heapq
from typing import List


class Solution:
    """AC 版本：计数 + 按次数排序取前 k"""

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        d = {}
        for num in nums:
            d[num] = d.get(num, 0) + 1  # get 带默认值：没见过就按 0 算

        sorted_nums = sorted(d.items(), key=lambda x: x[1], reverse=True)

        return [l[0] for l in sorted_nums[:k]]  # 每个元素是 (数字, 次数)，取第 0 号


# ---------------------------------------------------------------------------
# 本题踩坑记录（详见 leetcode-notes/02-数组与哈希表.md 第七节）
#
# 1. print != return —— 判题系统只看函数【返回值】，打印到屏幕的东西它看不见
# 2. d.keys[i] -> TypeError；keys 是方法，要 d.keys()；而且 key 顺序 = 插入顺序，
#    与出现次数无关，取前 k 个 key 根本不是「最高频的 k 个」
# 3. sorted(...) 返回新 list，不改原对象（原地排序是 list.sort()），返回值必须接住
# 4. 去掉 dict(...) 包装后 sorted_nums 变成 list，就不能再 .keys() —— 类型换了用法要跟着换
# 5. 不能给 dict 实例改属性：d.get = set(nums) -> AttributeError（get 只读）
# 6. 不要自己造「两张平行表」模拟映射，dict 本身就是映射：d[num] = 次数
# 7. 复杂度「接力用加，嵌套用乘」：O(n) + O(m log m)，不是 O(n * m log m)
# 8. 桶的下标 = 出现次数；`[[]] * (n+1)` 只建 1 个 list（复制的是引用），
#    必须写 `[[] for _ in range(n+1)]`，否则往一格 append 会污染所有格
# ---------------------------------------------------------------------------

class Solution2:
    """堆版：heapq.nlargest，O(n + m log k) —— k 小的时候比全排序快"""

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        d = {}
        for num in nums:
            d[num] = d.get(num, 0) + 1

        return [num for num, freq in heapq.nlargest(k, d.items(), key=lambda x: x[1])]


class Solution3:
    """桶版：用「出现次数」当桶的下标，时间 O(n)（空间换时间，O(n + m)）"""

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:

        d = {}
        for num in nums:
            d[num] = d.get(num, 0) + 1

        bucket = [[] for _ in range(len(nums) + 1)]  # 下标 = 出现次数，范围 0..n
        for num, freq in d.items():
            bucket[freq].append(num)

        res = []
        for i in range(len(bucket) - 1, 0, -1):  # 从次数最大的桶往下扫
            if bucket[i]:
                res.extend(bucket[i])
            if len(res) >= k:
                break

        return res[:k]


# 三个版本的正确性：官方/边界用例全过，500 组随机对拍 0 差异（含大量并列次数）
