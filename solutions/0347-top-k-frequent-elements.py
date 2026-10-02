"""347. Top K Frequent Elements (Medium) —— 专题：数组 & 哈希表

思路（两步走）：
  1. 计数：dict 记「数字 -> 出现次数」                       O(n)
  2. 把 d.items()（(数字, 次数) 对）按【次数】降序排，
     取前 k 个的【数字】                                    O(m log m)
  m = 不同数字的个数（≤ n）-> 总时间 O(n + m log m)，最坏 O(n log n)；空间 O(m)

本题的 Follow-up 要求优于 O(n log n)：
  堆 heapq.nlargest(k, d.items(), key=...)  -> O(m log k)
  桶排序（出现次数 ≤ n，用「次数」当下标）    -> O(n)
  （待补：两种优化的写法与实测）

2026-09-21 AC 版本如下（一字未改）。
"""

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
# ---------------------------------------------------------------------------
