from lib import *

TOPIC(
    id="arrays", title="Arrays & Hashing", glyph="[ ]",
    blurb="Indexing, prefix sums, hash maps and in-place tricks — the base of every other topic.",
    demo_title="Prefix sums: build once, answer any range sum in O(1)",
    theory="""
<h3>What it is</h3>
<p>An <b>array</b> (a Python <code>list</code>) stores items side by side in memory, so reaching <code>a[i]</code> takes one step no matter how big the array is. A <b>hash map</b> (<code>dict</code>) and <b>hash set</b> (<code>set</code>) turn a key into a bucket position, so "have I seen this?" also takes one step on average.</p>
<p>Most array questions are about avoiding the obvious double loop. The two tools that remove it are <b>remembering what you've seen</b> (hash map) and <b>pre-computing running totals</b> (prefix sums).</p>
<h3>Cost of common operations</h3>
<table>
<tr><th>Operation</th><th>list</th><th>dict / set</th></tr>
<tr><td>Read / write by index or key</td><td>O(1)</td><td>O(1) average</td></tr>
<tr><td>Search for a value</td><td>O(n)</td><td>O(1) average</td></tr>
<tr><td>Append at end</td><td>O(1) amortised</td><td>O(1)</td></tr>
<tr><td>Insert / delete at front or middle</td><td>O(n)</td><td>—</td></tr>
<tr><td>Sort</td><td>O(n log n)</td><td>—</td></tr>
</table>
<h3>Spot the pattern</h3>
<ul>
<li><b>"Find a pair / complement"</b> → store values in a hash map, look up <code>target − x</code>.</li>
<li><b>"Count / group / frequency"</b> → <code>Counter</code> or a dict of lists; bucket sort when counts are bounded by n.</li>
<li><b>"Sum of a subarray"</b> → prefix sums; <code>sum(i..j) = pre[j+1] − pre[i]</code>. Add a hash map of prefix counts for "how many subarrays sum to k".</li>
<li><b>"Best subarray"</b> → Kadane: keep the best sum ending here, restart when it goes negative.</li>
<li><b>"In place, O(1) extra space"</b> → swap with a write pointer, reverse tricks, or use the array itself as a marker.</li>
<li><b>Values in range 1..n</b> → the value can be used as an index (cycle detection, sign marking).</li>
</ul>
<h3>Template: hash map in one pass</h3>
<pre><code class="py">seen = {}
for i, x in enumerate(nums):
    if target - x in seen:      # answer uses an earlier element
        return [seen[target - x], i]
    seen[x] = i                 # remember x for later elements</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Putting <code>x</code> in the map <i>before</i> checking it, so an element pairs with itself.</li>
<li>Forgetting <code>pre = {0: 1}</code> in prefix-count problems (the subarray that starts at index 0).</li>
<li>Using <code>list.index</code> or <code>x in list</code> inside a loop — that hides an extra O(n).</li>
</ul>
""")


@D
def prefix_sum_demo():
    nums = [3, 1, 4, 1, 5, 9]
    pre = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        T(f"pre[{i + 1}] = pre[{i}] + nums[{i}] = {pre[i]} + {x}", A("nums", nums, hl=[i], i=i), A("pre", pre, hl=[i]))
        pre[i + 1] = pre[i] + x
    l, r = 1, 4
    T(f"Sum of nums[{l}..{r}] = pre[{r + 1}] − pre[{l}] = {pre[r + 1]} − {pre[l]} = {pre[r + 1] - pre[l]}", A("nums", nums, hl=range(l, r + 1), l=l, r=r), A("pre", pre, ok=[l, r + 1]))
    return pre[r + 1] - pre[l]


# 1 ---------------------------------------------------------------
Q(1, "Two Sum", "Easy", "Hash map",
  "Given an array <code>nums</code> and an integer <code>target</code>, return the indices of the two numbers that add up to <code>target</code>. Exactly one answer exists, and you may not use the same element twice.",
  [(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2]), (([3, 3], 6), [0, 1])],
  ("Try every pair (i, j) with i &lt; j and return the first pair whose sum is target.", "O(n²)", "O(1)"),
  ("Scan once and keep a map value → index. For each x the partner we need is target − x; if it is already in the map, the earlier index and the current index are the answer.", "O(n)", "O(n)"),
  norm=sorted, viz=([3, 8, 5, 1, 6], 7))


@B
def two_sum(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]


@O
def two_sum(nums, target):
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        T(f"x = {x}. Need {target} − {x} = {need}. Is {need} in seen?", A("nums", nums, hl=[i], i=i), M("seen", seen), V(need=need))
        if need in seen:
            T(f"Yes — {need} is at index {seen[need]}. Answer [{seen[need]}, {i}]", A("nums", nums, ok=[seen[need], i], i=i), M("seen", seen, hl=need))
            return [seen[need], i]
        seen[x] = i


# 2 ---------------------------------------------------------------
Q(217, "Contains Duplicate", "Easy", "Hash set",
  "Return <code>True</code> if any value appears at least twice in <code>nums</code>, otherwise <code>False</code>.",
  [(([1, 2, 3, 1],), True), (([1, 2, 3, 4],), False), (([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), True)],
  ("Compare every pair of elements.", "O(n²)", "O(1)"),
  ("Walk the array with a set of values seen so far. The first value already in the set is a duplicate.", "O(n)", "O(n)"))


@B
def contains_duplicate(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


@O
def contains_duplicate(nums):
    seen = set()
    for i, x in enumerate(nums):
        T(f"Is {x} already in the set?", A("nums", nums, hl=[i], i=i), M("seen", seen))
        if x in seen:
            T(f"{x} was seen before → duplicate", A("nums", nums, bad=[i], i=i), M("seen", seen, hl=x))
            return True
        seen.add(x)
    return False


# 3 ---------------------------------------------------------------
Q(242, "Valid Anagram", "Easy", "Counting",
  "Return <code>True</code> if string <code>t</code> is an anagram of <code>s</code> — the same letters with the same counts, in any order.",
  [(("anagram", "nagaram"), True), (("rat", "car"), False), (("ab", "a"), False)],
  ("Sort both strings and compare them.", "O(n log n)", "O(n)"),
  ("Count letters: +1 for each letter of s, −1 for each letter of t. They are anagrams exactly when every count ends at 0.", "O(n)", "O(1) — 26 letters"),
  viz=("cat", "act"))


@B
def is_anagram(s, t):
    return sorted(s) == sorted(t)


@O
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for i in range(len(s)):
        count[s[i]] = count.get(s[i], 0) + 1
        count[t[i]] = count.get(t[i], 0) - 1
        T(f"+1 for s[{i}]='{s[i]}', −1 for t[{i}]='{t[i]}'", A("s", s, hl=[i]), A("t", t, hl=[i]), M("count", count), at="prev")
    T("All counts are zero?" , M("count", count))
    return all(c == 0 for c in count.values())


# 4 ---------------------------------------------------------------
Q(49, "Group Anagrams", "Medium", "Hash map · key design",
  "Group the strings in <code>strs</code> so that anagrams are together. The groups may be returned in any order.",
  [((["eat", "tea", "tan", "ate", "nat", "bat"],), [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]), (([""],), [[""]]), ((["a"],), [["a"]])],
  ("For each word not yet grouped, compare it with every other word by sorting both.", "O(n² · k log k)", "O(n)"),
  ("Give every word a key that is identical for anagrams — the tuple of its 26 letter counts — and bucket words by key in a dict.", "O(n · k)", "O(n · k)"),
  norm=lambda g: sorted(sorted(x) for x in g), viz=(["eat", "tea", "tan", "nat", "bat"],))


@B
def group_anagrams(strs):
    used = [False] * len(strs)
    groups = []
    for i in range(len(strs)):
        if used[i]:
            continue
        group = [strs[i]]
        used[i] = True
        for j in range(i + 1, len(strs)):
            if not used[j] and sorted(strs[i]) == sorted(strs[j]):
                group.append(strs[j])
                used[j] = True
        groups.append(group)
    return groups


@O
def group_anagrams(strs):
    groups = {}
    for i, w in enumerate(strs):
        count = [0] * 26
        for ch in w:
            count[ord(ch) - ord("a")] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(w)
        T(f"'{w}' → key {''.join(sorted(w))} (its letter counts)", A("strs", strs, hl=[i], i=i), M("groups", {"".join(sorted(g[0])): g for g in groups.values()}, hl="".join(sorted(w))), at="prev")
    return list(groups.values())


# 5 ---------------------------------------------------------------
Q(347, "Top K Frequent Elements", "Medium", "Bucket sort",
  "Return the <code>k</code> most frequent elements of <code>nums</code>, in any order.",
  [(([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1]), (([4, 4, 5, 5, 5, 6], 1), [5])],
  ("Count frequencies, sort the distinct values by count, take the first k.", "O(n log n)", "O(n)"),
  ("A count is between 1 and n, so make n + 1 buckets where bucket[c] lists values seen c times. Walk buckets from high to low until k values are collected.", "O(n)", "O(n)"),
  norm=sorted)


@B
def top_k_frequent(nums, k):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    ranked = sorted(count, key=lambda x: -count[x])
    return ranked[:k]


@O
def top_k_frequent(nums, k):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    buckets = [[] for _ in range(len(nums) + 1)]
    for x, c in count.items():
        buckets[c].append(x)
    T("Bucket c holds the values that appear c times", M("count", count), A("buckets", buckets))
    res = []
    for c in range(len(buckets) - 1, 0, -1):
        for x in buckets[c]:
            res.append(x)
            T(f"Take {x} (appears {c} times)", A("buckets", buckets, hl=[c], c=c), A("res", res), at="prev")
            if len(res) == k:
                return res


# 6 ---------------------------------------------------------------
Q(238, "Product of Array Except Self", "Medium", "Prefix / suffix",
  "Return <code>answer</code> where <code>answer[i]</code> is the product of every element of <code>nums</code> except <code>nums[i]</code>, without using division.",
  [(([1, 2, 3, 4],), [24, 12, 8, 6]), (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0])],
  ("For each i, multiply every other element.", "O(n²)", "O(1) extra"),
  ("answer[i] = (product of everything left of i) × (product of everything right of i). Fill the left products in one pass, then sweep from the right with a running product.", "O(n)", "O(1) extra (output not counted)"))


@B
def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    for i in range(n):
        for j in range(n):
            if i != j:
                answer[i] *= nums[j]
    return answer


@O
def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    left = 1
    for i in range(n):
        answer[i] = left
        T(f"answer[{i}] = product left of {i} = {left}", A("nums", nums, hl=range(i), i=i), A("answer", answer, hl=[i]), V(left=left), at="prev")
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right
        T(f"answer[{i}] ×= product right of {i} = {right}", A("nums", nums, hl=range(i + 1, n), i=i), A("answer", answer, ok=range(i, n)), V(right=right), at="prev")
        right *= nums[i]
    return answer


# 7 ---------------------------------------------------------------
Q(128, "Longest Consecutive Sequence", "Medium", "Hash set",
  "Given an unsorted array <code>nums</code>, return the length of the longest run of consecutive integers (like 1, 2, 3, 4). Must run in O(n).",
  [(([100, 4, 200, 1, 3, 2],), 4), (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9), (([],), 0)],
  ("For every x, keep checking whether x + 1, x + 2, … exist by scanning the list.", "O(n³)", "O(1)"),
  ("Put everything in a set. Only start counting at numbers that begin a run (x − 1 not in the set), then walk x + 1, x + 2, … in the set. Each number is visited at most twice.", "O(n)", "O(n)"))


@B
def longest_consecutive(nums):
    best = 0
    for x in nums:
        length = 1
        while x + length in nums:
            length += 1
        best = max(best, length)
    return best


@O
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            T(f"{x - 1} exists, so {x} is not the start of a run — skip", A("nums", nums, hl=[nums.index(x)]), V(best=best))
            continue
        length = 1
        while x + length in s:
            length += 1
        best = max(best, length)
        T(f"{x} starts a run: {x}..{x + length - 1}, length {length}", A("nums", nums, ok=[nums.index(v) for v in range(x, x + length)]), V(best=best), at="prev")
    return best


# 8 ---------------------------------------------------------------
Q(53, "Maximum Subarray", "Medium", "Kadane",
  "Find the contiguous subarray with the largest sum and return that sum.",
  [(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([1],), 1), (([5, 4, -1, 7, 8],), 23), (([-3, -1, -2],), -1)],
  ("Fix each start i, extend the end j and keep a running sum.", "O(n²)", "O(1)"),
  ("Kadane: cur = best sum of a subarray ending at i. Either extend the previous one or start fresh at nums[i]: cur = max(nums[i], cur + nums[i]).", "O(n)", "O(1)"))


@B
def max_subarray(nums):
    best = nums[0]
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best


@O
def max_subarray(nums):
    cur = best = nums[0]
    start = bs = be = 0
    for i in range(1, len(nums)):
        if cur + nums[i] < nums[i]:
            cur, start = nums[i], i
        else:
            cur += nums[i]
        if cur > best:
            best, bs, be = cur, start, i
        T(f"Best sum ending at {i} is {cur}; best overall {best}", A("nums", nums, hl=range(start, i + 1), ok=range(bs, be + 1), i=i), V(cur=cur, best=best), at="prev")
    return best


# 9 ---------------------------------------------------------------
Q(121, "Best Time to Buy and Sell Stock", "Easy", "Running minimum",
  "<code>prices[i]</code> is a stock's price on day i. Buy once and sell once later; return the largest profit, or 0 if no profit is possible.",
  [(([7, 1, 5, 3, 6, 4],), 5), (([7, 6, 4, 3, 1],), 0)],
  ("Try every buy day with every later sell day.", "O(n²)", "O(1)"),
  ("Walk the days keeping the cheapest price so far. Selling today earns price − cheapest; keep the best.", "O(n)", "O(1)"))


@B
def max_profit(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


@O
def max_profit(prices):
    lo, best, lo_i = prices[0], 0, 0
    for i, p in enumerate(prices):
        if p < lo:
            lo, lo_i = p, i
        best = max(best, p - lo)
        T(f"Day {i}: cheapest so far {lo}, selling today earns {p - lo}", A("prices", prices, hl=[i], ok=[lo_i], buy=lo_i, sell=i), V(best=best), at="prev")
    return best


# 10 --------------------------------------------------------------
Q(169, "Majority Element", "Easy", "Boyer–Moore voting",
  "Return the element that appears more than ⌊n / 2⌋ times. It always exists.",
  [(([3, 2, 3],), 3), (([2, 2, 1, 1, 1, 2, 2],), 2)],
  ("For each element, count how often it appears.", "O(n²)", "O(1)"),
  ("Boyer–Moore: keep a candidate and a counter. Same value → +1, different → −1, counter at 0 → new candidate. The majority survives because it outnumbers everything else combined.", "O(n)", "O(1)"),
  viz=([2, 2, 1, 1, 1, 2, 2],))


@B
def majority_element(nums):
    for x in nums:
        if sum(1 for y in nums if y == x) > len(nums) // 2:
            return x


@O
def majority_element(nums):
    cand, cnt = None, 0
    for i, x in enumerate(nums):
        if cnt == 0:
            cand = x
        cnt += 1 if x == cand else -1
        T(f"x = {x} → candidate {cand}, count {cnt}", A("nums", nums, hl=[i], i=i), V(candidate=cand, count=cnt), at="prev")
    return cand


# 11 --------------------------------------------------------------
Q(283, "Move Zeroes", "Easy", "Write pointer",
  "Move all 0s in <code>nums</code> to the end while keeping the order of the other elements. Do it in place.",
  [(([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]), (([0],), [0]), (([1, 2],), [1, 2])],
  ("Build a new list of the non-zeros, pad with zeros, copy it back.", "O(n)", "O(n)"),
  ("Keep a write pointer w for the next non-zero slot. When nums[r] is non-zero, swap it into position w and advance w.", "O(n)", "O(1)"),
  inplace=0)


@B
def move_zeroes(nums):
    rest = [x for x in nums if x != 0]
    rest += [0] * (len(nums) - len(rest))
    nums[:] = rest


@O
def move_zeroes(nums):
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w], nums[r] = nums[r], nums[w]
            T(f"nums[{r}] is non-zero → swap into slot w={w}", A("nums", nums, hl=[w, r], ok=range(w + 1), w=w, r=r), at="prev")
            w += 1
        else:
            T(f"nums[{r}] is 0 → skip", A("nums", nums, ok=range(w), w=w, r=r))


# 12 --------------------------------------------------------------
Q(189, "Rotate Array", "Medium", "Reverse trick",
  "Rotate <code>nums</code> to the right by <code>k</code> steps, in place.",
  [(([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]), (([-1, -100, 3, 99], 2), [3, 99, -1, -100]), (([1, 2], 5), [2, 1])],
  ("Rotate by one step, k times.", "O(n · k)", "O(1)"),
  ("Reverse the whole array, then reverse the first k and the last n − k elements. The last k elements end up in front, each block in its original order.", "O(n)", "O(1)"),
  inplace=0)


@B
def rotate(nums, k):
    for _ in range(k % len(nums)):
        nums.insert(0, nums.pop())


@O
def rotate(nums, k):
    n = len(nums)
    k %= n

    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l, r = l + 1, r - 1

    T(f"Start (k = {k})", A("nums", nums))
    rev(0, n - 1)
    T("1) Reverse everything", A("nums", nums, hl=range(n)), at="prev")
    rev(0, k - 1)
    T(f"2) Reverse the first k = {k}", A("nums", nums, ok=range(k)), at="prev")
    rev(k, n - 1)
    T("3) Reverse the rest — done", A("nums", nums, ok=range(n)), at="prev")


# 13 --------------------------------------------------------------
Q(560, "Subarray Sum Equals K", "Medium", "Prefix sum + hash map",
  "Return the number of contiguous subarrays whose sum equals <code>k</code>. Values may be negative.",
  [(([1, 1, 1], 2), 2), (([1, 2, 3], 3), 2), (([1, -1, 0], 0), 3)],
  ("Fix each start, extend the end, count the sums equal to k.", "O(n²)", "O(1)"),
  ("With running sum pre, a subarray ending here sums to k when an earlier prefix equals pre − k. Keep a count of every prefix sum seen; start with {0: 1}.", "O(n)", "O(n)"),
  viz=([3, 4, -7, 1, 3, 3, 1, -4], 7))


@B
def subarray_sum(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count


@O
def subarray_sum(nums, k):
    seen = {0: 1}  # prefix sum -> how many times
    pre = count = 0
    for i, x in enumerate(nums):
        pre += x
        count += seen.get(pre - k, 0)
        T(f"prefix = {pre}. Earlier prefixes equal to {pre} − {k} = {pre - k}: {seen.get(pre - k, 0)}", A("nums", nums, hl=range(i + 1), i=i), M("seen", seen, hl=pre - k), V(prefix=pre, count=count), at="prev")
        seen[pre] = seen.get(pre, 0) + 1
    return count


# 14 --------------------------------------------------------------
Q(75, "Sort Colors", "Medium", "Dutch national flag",
  "Sort an array of 0s, 1s and 2s in place in one pass, without the library sort.",
  [(([2, 0, 2, 1, 1, 0],), [0, 0, 1, 1, 2, 2]), (([2, 0, 1],), [0, 1, 2])],
  ("Count the 0s, 1s and 2s, then overwrite the array.", "O(n) — two passes", "O(1)"),
  ("Three pointers: everything before lo is 0, everything after hi is 2, mid scans. 0 → swap to lo; 2 → swap to hi (don't advance mid); 1 → advance.", "O(n) — one pass", "O(1)"),
  inplace=0)


@B
def sort_colors(nums):
    c = [nums.count(0), nums.count(1), nums.count(2)]
    nums[:] = [0] * c[0] + [1] * c[1] + [2] * c[2]


@O
def sort_colors(nums):
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        T(f"nums[mid] = {nums[mid]}", A("nums", nums, hl=[mid], ok=list(range(lo)) + list(range(hi + 1, len(nums))), lo=lo, mid=mid, hi=hi))
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo, mid = lo + 1, mid + 1
        elif nums[mid] == 2:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1
        else:
            mid += 1
    T("Sorted", A("nums", nums, ok=range(len(nums))))


# 15 --------------------------------------------------------------
Q(31, "Next Permutation", "Medium", "Pivot + reverse",
  "Rearrange <code>nums</code> in place into the next lexicographically greater permutation. If it is the largest, wrap to the smallest (sorted).",
  [(([1, 2, 3],), [1, 3, 2]), (([3, 2, 1],), [1, 2, 3]), (([1, 1, 5],), [1, 5, 1]), (([1, 3, 2],), [2, 1, 3])],
  ("Generate every permutation in sorted order and pick the one after the current.", "O(n! · n)", "O(n! · n)"),
  ("From the right, find the first i with nums[i] &lt; nums[i+1] (the pivot). Swap it with the smallest larger element to its right, then reverse the suffix after i.", "O(n)", "O(1)"),
  inplace=0, viz=([1, 3, 5, 4, 2],))


@B
def next_permutation(nums):
    from itertools import permutations
    perms = sorted(set(permutations(nums)))
    i = perms.index(tuple(nums))
    nums[:] = perms[(i + 1) % len(perms)]


@O
def next_permutation(nums):
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    T(f"Pivot: first index from the right with nums[i] < nums[i+1] → i = {i}", A("nums", nums, hl=[i] if i >= 0 else [], ok=range(i + 1, len(nums)), i=i if i >= 0 else None), at="prev")
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
        T(f"Swap pivot with the smallest larger value on its right (index {j})", A("nums", nums, hl=[i, j], i=i, j=j), at="prev")
    nums[i + 1:] = reversed(nums[i + 1:])
    T("Reverse the suffix so it is as small as possible", A("nums", nums, ok=range(i + 1, len(nums))), at="prev")


# 16 --------------------------------------------------------------
Q(287, "Find the Duplicate Number", "Medium", "Floyd cycle",
  "<code>nums</code> has n + 1 integers, each in 1..n, and exactly one value repeats. Find it without modifying the array, using O(1) extra space.",
  [(([1, 3, 4, 2, 2],), 2), (([3, 1, 3, 4, 2],), 3), (([3, 3, 3, 3, 3],), 3)],
  ("Remember values in a set and return the first repeat.", "O(n)", "O(n)"),
  ("Treat i → nums[i] as a linked list. Two indices pointing at the same value make a cycle whose entrance is the duplicate. Find it with Floyd's tortoise and hare.", "O(n)", "O(1)"))


@B
def find_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)


@O
def find_duplicate(nums):
    slow = fast = nums[0]
    while True:
        slow, fast = nums[slow], nums[nums[fast]]
        T(f"Phase 1: slow moves 1 step, fast 2 steps", A("nums", nums, slow=slow, fast=fast), at="prev")
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow, fast = nums[slow], nums[fast]
        T("Phase 2: both move 1 step until they meet at the cycle entrance", A("nums", nums, slow=slow, fast=fast), at="prev")
    T(f"They meet at index {slow} → the duplicate value is {slow}", A("nums", nums, ok=[i for i, x in enumerate(nums) if x == slow]))
    return slow


# 17 --------------------------------------------------------------
Q(268, "Missing Number", "Easy", "Math / XOR",
  "<code>nums</code> holds n distinct numbers from 0..n. Return the one that is missing.",
  [(([3, 0, 1],), 2), (([0, 1],), 2), (([9, 6, 4, 2, 3, 5, 7, 0, 1],), 8)],
  ("For each candidate 0..n, search the list for it.", "O(n²)", "O(1)"),
  ("The sum of 0..n is n(n+1)/2. Subtract the actual sum; what's left is the missing number.", "O(n)", "O(1)"))


@B
def missing_number(nums):
    for v in range(len(nums) + 1):
        if v not in nums:
            return v


@O
def missing_number(nums):
    n = len(nums)
    expected = n * (n + 1) // 2
    actual = sum(nums)
    T(f"0 + 1 + … + {n} = {expected}; the array sums to {actual}", A("nums", nums), V(expected=expected, actual=actual, missing=expected - actual))
    return expected - actual


# 18 --------------------------------------------------------------
Q(73, "Set Matrix Zeroes", "Medium", "In-place markers",
  "If a cell of an m × n matrix is 0, set its whole row and column to 0. Do it in place.",
  [(([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
   (([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],), [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])],
  ("Record which rows and columns contain a zero in two sets, then zero them out.", "O(m · n)", "O(m + n)"),
  ("Use the first row and first column as the marker arrays. Remember separately whether row 0 itself had a zero, mark, zero the inner cells, then fix row 0 and column 0 last.", "O(m · n)", "O(1)"),
  inplace=0)


@B
def set_zeroes(matrix):
    rows, cols = set(), set()
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v == 0:
                rows.add(r)
                cols.add(c)
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if r in rows or c in cols:
                matrix[r][c] = 0


@O
def set_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = any(matrix[0][c] == 0 for c in range(n))
    for r in range(1, m):
        for c in range(n):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0
                T(f"Zero at ({r},{c}) → mark row {r} in column 0 and column {c} in row 0", G("matrix", matrix, hl=[(r, c)], ok=[(r, 0), (0, c)]), at="prev")
    for r in range(1, m):
        for c in range(n - 1, -1, -1):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    T("Zero every cell whose row or column is marked", G("matrix", matrix), V(row0_had_zero=row0))
    if row0:
        for c in range(n):
            matrix[0][c] = 0
    T("Finally fix row 0 if it had a zero of its own", G("matrix", matrix, ok=[(0, c) for c in range(n)]))


# 19 --------------------------------------------------------------
Q(54, "Spiral Matrix", "Medium", "Boundary shrink",
  "Return all elements of an m × n matrix in spiral order (right, down, left, up, repeat).",
  [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
   (([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],), [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])],
  ("Walk the grid with a direction and a visited matrix, turning right when blocked.", "O(m · n)", "O(m · n)"),
  ("Keep four walls top, bottom, left, right. Read the top row, right column, bottom row, left column, shrinking the matching wall after each.", "O(m · n)", "O(1) extra"))


@B
def spiral_order(matrix):
    m, n = len(matrix), len(matrix[0])
    seen = [[False] * n for _ in range(m)]
    dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
    r = c = d = 0
    out = []
    for _ in range(m * n):
        out.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < m and 0 <= nc < n) or seen[nr][nc]:
            d = (d + 1) % 4
            nr, nc = r + dr[d], c + dc[d]
        r, c = nr, nc
    return out


@O
def spiral_order(matrix):
    out = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    done = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c]); done.append((top, c))
        top += 1
        T("Top row, left → right", G("matrix", matrix, ok=done), A("out", out), V(top=top, bottom=bottom, left=left, right=right), at="prev")
        for r in range(top, bottom + 1):
            out.append(matrix[r][right]); done.append((r, right))
        right -= 1
        T("Right column, top → bottom", G("matrix", matrix, ok=done), A("out", out), V(top=top, bottom=bottom, left=left, right=right), at="prev")
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c]); done.append((bottom, c))
            bottom -= 1
            T("Bottom row, right → left", G("matrix", matrix, ok=done), A("out", out), V(top=top, bottom=bottom, left=left, right=right), at="prev")
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left]); done.append((r, left))
            left += 1
            T("Left column, bottom → top", G("matrix", matrix, ok=done), A("out", out), V(top=top, bottom=bottom, left=left, right=right), at="prev")
    return out


# 20 --------------------------------------------------------------
Q(48, "Rotate Image", "Medium", "Transpose + reverse",
  "Rotate an n × n matrix 90° clockwise, in place.",
  [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
   (([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],), [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])],
  ("Build a new matrix where new[c][n−1−r] = old[r][c], then copy it back.", "O(n²)", "O(n²)"),
  ("A clockwise turn equals a transpose (swap across the main diagonal) followed by reversing each row.", "O(n²)", "O(1)"),
  inplace=0)


@B
def rotate_image(matrix):
    n = len(matrix)
    new = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            new[c][n - 1 - r] = matrix[r][c]
    matrix[:] = new


@O
def rotate_image(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
            T(f"Transpose: swap ({r},{c}) ↔ ({c},{r})", G("matrix", matrix, hl=[(r, c), (c, r)]), at="prev")
    for row in matrix:
        row.reverse()
    T("Reverse every row → rotated 90° clockwise", G("matrix", matrix, ok=[(r, c) for r in range(n) for c in range(n)]), at="prev")
