from lib import *

TOPIC(
    id="binary-search", title="Binary Search", glyph="lo·mid·hi",
    blurb="Halve the search space every step — on sorted arrays and on the answer itself.",
    demo_title="Classic binary search: throw away half the array every step",
    theory="""
<h3>What it is</h3>
<p>If you can look at the middle of a range and decide <b>which half cannot contain the answer</b>, you can discard that half. Repeating this takes about log₂(n) steps: 1,000,000 items need only 20 checks.</p>
<h3>Two families</h3>
<table>
<tr><th>Family</th><th>Search space</th><th>Question asked at mid</th></tr>
<tr><td><b>On an array</b></td><td>indices <code>0..n−1</code> of a sorted (or rotated) array</td><td>is <code>a[mid]</code> too small, too big, or the answer?</td></tr>
<tr><td><b>On the answer</b></td><td>a range of possible answers, e.g. speed 1..max(piles)</td><td>is <code>mid</code> <i>feasible</i>? (can Koko finish at this speed?)</td></tr>
</table>
<p>"Binary search on the answer" works whenever feasibility is <b>monotonic</b>: if speed s works, every speed &gt; s works too. Then the answers look like <code>F F F F T T T</code> and we want the first T.</p>
<h3>Template: first index where a condition becomes true</h3>
<pre><code class="py">lo, hi = 0, n            # answer is in [lo, hi]
while lo &lt; hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid         # mid might be the answer, keep it
    else:
        lo = mid + 1     # mid is too small, drop it
return lo</code></pre>
<h3>Spot the pattern</h3>
<ul>
<li>Sorted input + "find / count / first / last" → binary search on indices (<code>bisect_left</code>, <code>bisect_right</code>).</li>
<li>"Minimise the maximum" or "maximise the minimum" (ship capacity, split array, aggressive cows) → binary search on the answer + a greedy feasibility check.</li>
<li>Rotated sorted array → one half around <code>mid</code> is always sorted; check if the target lies in that half.</li>
<li>Requirement of O(log n) in the problem statement is a strong hint.</li>
</ul>
<h3>Common mistakes</h3>
<ul>
<li>Infinite loops: with <code>lo = mid</code> you need <code>mid = (lo + hi + 1) // 2</code>.</li>
<li>Mixing <code>while lo &lt;= hi</code> (closed range, return inside) with <code>while lo &lt; hi</code> (half-open, return lo) — pick one template per problem.</li>
<li>Wrong bounds for answer search: the lowest and highest values that could possibly be the answer.</li>
</ul>
""")


@D
def bs_demo():
    a, target = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        T(f"mid = {mid}, a[mid] = {a[mid]} vs target {target}", A("a", a, hl=range(lo, hi + 1), lo=lo, mid=mid, hi=hi))
        if a[mid] == target:
            T(f"Found {target} at index {mid} in {3} steps instead of {mid + 1}", A("a", a, ok=[mid], mid=mid))
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# 1 ---------------------------------------------------------------
Q(704, "Binary Search", "Easy", "Closed range",
  "Return the index of <code>target</code> in sorted <code>nums</code>, or −1.",
  [(([-1, 0, 3, 5, 9, 12], 9), 4), (([-1, 0, 3, 5, 9, 12], 2), -1)],
  ("Scan left to right.", "O(n)", "O(1)"),
  ("Compare with the middle; drop the half that can't contain target.", "O(log n)", "O(1)"),
  viz=([-1, 0, 3, 5, 9, 12, 15, 20, 31], 20))


@B
def search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1


@O
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        T(f"nums[mid] = {nums[mid]} vs {target}", A("nums", nums, hl=range(lo, hi + 1), lo=lo, mid=mid, hi=hi))
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# 2 ---------------------------------------------------------------
Q(35, "Search Insert Position", "Easy", "Lower bound",
  "Return the index of <code>target</code> in sorted <code>nums</code>, or the index where it would be inserted.",
  [(([1, 3, 5, 6], 5), 2), (([1, 3, 5, 6], 2), 1), (([1, 3, 5, 6], 7), 4)],
  ("Scan for the first element ≥ target.", "O(n)", "O(1)"),
  ("Find the first index with nums[i] ≥ target using the half-open template.", "O(log n)", "O(1)"),
  viz=([1, 3, 5, 6, 8, 10, 12], 7))


@B
def search_insert(nums, target):
    for i, x in enumerate(nums):
        if x >= target:
            return i
    return len(nums)


@O
def search_insert(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"nums[{mid}] = {nums[mid]} {'≥' if nums[mid] >= target else '<'} {target}", A("nums", nums, hl=range(lo, hi), lo=lo, mid=mid, hi=hi))
        if nums[mid] >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


# 3 ---------------------------------------------------------------
Q(34, "Find First and Last Position of Element in Sorted Array", "Medium", "Lower + upper bound",
  "Return <code>[first, last]</code> indices of <code>target</code> in sorted <code>nums</code>, or <code>[-1, -1]</code>.",
  [(([5, 7, 7, 8, 8, 10], 8), [3, 4]), (([5, 7, 7, 8, 8, 10], 6), [-1, -1]), (([], 0), [-1, -1])],
  ("Scan for the first and last match.", "O(n)", "O(1)"),
  ("Two binary searches: first index ≥ target, and first index &gt; target (minus one).", "O(log n)", "O(1)"),
  viz=([2, 4, 4, 4, 4, 7, 9], 4))


@B
def search_range(nums, target):
    idx = [i for i, x in enumerate(nums) if x == target]
    return [idx[0], idx[-1]] if idx else [-1, -1]


@O
def search_range(nums, target):
    def first_at_least(x):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            T(f"Looking for first index with value ≥ {x}: nums[{mid}] = {nums[mid]}", A("nums", nums, hl=range(lo, hi), lo=lo, mid=mid, hi=hi))
            if nums[mid] >= x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    l = first_at_least(target)
    if l == len(nums) or nums[l] != target:
        return [-1, -1]
    r = first_at_least(target + 1) - 1
    T(f"Range [{l}, {r}]", A("nums", nums, ok=range(l, r + 1)), at="prev")
    return [l, r]


# 4 ---------------------------------------------------------------
Q(33, "Search in Rotated Sorted Array", "Medium", "Find the sorted half",
  "A sorted array of distinct values was rotated at an unknown pivot. Return the index of <code>target</code> or −1 in O(log n).",
  [(([4, 5, 6, 7, 0, 1, 2], 0), 4), (([4, 5, 6, 7, 0, 1, 2], 3), -1), (([1], 0), -1)],
  ("Linear scan.", "O(n)", "O(1)"),
  ("At any mid, one of the halves [lo, mid] or [mid, hi] is sorted. If target lies within the sorted half's range, search there; otherwise search the other half.", "O(log n)", "O(1)"))


@B
def search_rotated(nums, target):
    return nums.index(target) if target in nums else -1


@O
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            T(f"Found {target} at {mid}", A("nums", nums, ok=[mid], lo=lo, mid=mid, hi=hi))
            return mid
        if nums[lo] <= nums[mid]:
            T(f"Left half {nums[lo]}..{nums[mid]} is sorted. Is {target} inside it?", A("nums", nums, hl=range(lo, mid + 1), lo=lo, mid=mid, hi=hi))
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            T(f"Right half {nums[mid]}..{nums[hi]} is sorted. Is {target} inside it?", A("nums", nums, hl=range(mid, hi + 1), lo=lo, mid=mid, hi=hi))
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


# 5 ---------------------------------------------------------------
Q(153, "Find Minimum in Rotated Sorted Array", "Medium", "Compare with right end",
  "Return the minimum of a rotated sorted array of distinct values in O(log n).",
  [(([3, 4, 5, 1, 2],), 1), (([4, 5, 6, 7, 0, 1, 2],), 0), (([11, 13, 15, 17],), 11)],
  ("Take min() of the array.", "O(n)", "O(1)"),
  ("If nums[mid] &gt; nums[hi], the drop (the minimum) is to the right of mid; otherwise it is at mid or to its left.", "O(log n)", "O(1)"),
  viz=([11, 13, 15, 17, 19, 2, 5, 7],))


@B
def find_min(nums):
    return min(nums)


@O
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"nums[mid] = {nums[mid]} {'>' if nums[mid] > nums[hi] else '≤'} nums[hi] = {nums[hi]} → min is {'right of mid' if nums[mid] > nums[hi] else 'at or left of mid'}", A("nums", nums, hl=range(lo, hi + 1), lo=lo, mid=mid, hi=hi))
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


# 6 ---------------------------------------------------------------
Q(74, "Search a 2D Matrix", "Medium", "Flatten the index",
  "Each row is sorted and each row's first value is larger than the previous row's last. Is <code>target</code> in the matrix?",
  [(([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3), True), (([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13), False)],
  ("Check every cell.", "O(m · n)", "O(1)"),
  ("The matrix is one sorted list of m·n values. Binary search index k and read cell (k // n, k % n).", "O(log(m · n))", "O(1)"),
  viz=([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 16))


@B
def search_matrix(matrix, target):
    return any(target in row for row in matrix)


@O
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // n][mid % n]
        T(f"Index {mid} → cell ({mid // n}, {mid % n}) = {v}", G("matrix", matrix, hl=[(k // n, k % n) for k in range(lo, hi + 1)], ok=[(mid // n, mid % n)]), V(lo=lo, mid=mid, hi=hi))
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


# 7 ---------------------------------------------------------------
Q(875, "Koko Eating Bananas", "Medium", "Search on the answer",
  "Koko eats at speed k bananas per hour (one pile per hour at most). Return the minimum k that finishes all <code>piles</code> within <code>h</code> hours.",
  [(([3, 6, 7, 11], 8), 4), (([30, 11, 23, 4, 20], 5), 30), (([30, 11, 23, 4, 20], 6), 23)],
  ("Try k = 1, 2, 3, … until it fits.", "O(max · n)", "O(1)"),
  ("Hours needed only decrease as k grows, so binary search k in [1, max(piles)] for the first speed that finishes in time.", "O(n log max)", "O(1)"))


@B
def min_eating_speed(piles, h):
    k = 1
    while sum((p + k - 1) // k for p in piles) > h:
        k += 1
    return k


@O
def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        hours = sum((p + k - 1) // k for p in piles)
        T(f"Speed {k}: needs {hours} h {'≤' if hours <= h else '>'} {h} → {'try slower' if hours <= h else 'too slow'}", A("piles", piles), V(lo=lo, k=k, hi=hi, hours=hours))
        if hours <= h:
            hi = k
        else:
            lo = k + 1
    return lo


# 8 ---------------------------------------------------------------
Q(1011, "Capacity To Ship Packages Within D Days", "Medium", "Search on the answer",
  "Ship packages in order; each day the ship carries at most its capacity. Return the least capacity that ships everything within <code>days</code>.",
  [(([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15), (([3, 2, 2, 4, 1, 4], 3), 6), (([1, 2, 3, 1, 1], 4), 3)],
  ("Try every capacity from max(weights) upward.", "O(n · sum)", "O(1)"),
  ("Capacity lies in [max(weights), sum(weights)]. For a candidate, greedily fill days; binary search the smallest capacity that needs ≤ days.", "O(n log sum)", "O(1)"),
  viz=([3, 2, 2, 4, 1, 4], 3))


@B
def ship_within_days(weights, days):
    def need(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d, load = d + 1, 0
            load += w
        return d
    cap = max(weights)
    while need(cap) > days:
        cap += 1
    return cap


@O
def ship_within_days(weights, days):
    def need(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d, load = d + 1, 0
            load += w
        return d

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"Capacity {mid} needs {need(mid)} day(s)", A("weights", weights), V(lo=lo, mid=mid, hi=hi, days_needed=need(mid)))
        if need(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


# 9 ---------------------------------------------------------------
Q(4, "Median of Two Sorted Arrays", "Hard", "Binary search the partition",
  "Return the median of two sorted arrays in O(log(min(m, n))).",
  [(([1, 3], [2]), 2.0), (([1, 2], [3, 4]), 2.5), (([0, 0], [0, 0]), 0.0)],
  ("Merge both arrays and take the middle.", "O(m + n)", "O(m + n)"),
  ("Cut A at i and B at j so the left side has half of all elements. The cut is right when A[i−1] ≤ B[j] and B[j−1] ≤ A[i]; binary search i over the shorter array.", "O(log min(m, n))", "O(1)"),
  viz=([1, 3, 8, 9, 15], [7, 11, 18, 19, 21, 25]))


@B
def find_median_sorted_arrays(a, b):
    m = sorted(a + b)
    n = len(m)
    return float(m[n // 2]) if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2


@O
def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        aL = a[i - 1] if i > 0 else float("-inf")
        aR = a[i] if i < m else float("inf")
        bL = b[j - 1] if j > 0 else float("-inf")
        bR = b[j] if j < n else float("inf")
        T(f"Cut A after {i}, B after {j}: is {aL} ≤ {bR} and {bL} ≤ {aR}?", A("A", a, ok=range(i), hl=range(i, m), cut=i), A("B", b, ok=range(j), hl=range(j, n), cut=j), V(aL=aL, aR=aR, bL=bL, bR=bR))
        if aL <= bR and bL <= aR:
            if (m + n) % 2:
                return float(max(aL, bL))
            return (max(aL, bL) + min(aR, bR)) / 2
        if aL > bR:
            hi = i - 1
        else:
            lo = i + 1


# 10 --------------------------------------------------------------
Q(162, "Find Peak Element", "Medium", "Follow the slope",
  "Return the index of any element strictly greater than its neighbours (treat outside as −∞), in O(log n).",
  [(([1, 2, 3, 1],), 2), (([1, 2, 1, 3, 5, 6, 4],), 5)],
  ("Scan for the first i with nums[i] &gt; nums[i+1].", "O(n)", "O(1)"),
  ("If nums[mid] &lt; nums[mid+1] we're on an uphill slope, so a peak exists to the right; otherwise one exists at mid or to the left.", "O(log n)", "O(1)"),
  check=lambda a, i: 0 <= i < len(a[0]) and (i == 0 or a[0][i] > a[0][i - 1]) and (i == len(a[0]) - 1 or a[0][i] > a[0][i + 1]),
  viz=([1, 2, 1, 3, 5, 6, 4],))


@B
def find_peak_element(nums):
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return i
    return len(nums) - 1


@O
def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"{nums[mid]} {'<' if nums[mid] < nums[mid + 1] else '>'} {nums[mid + 1]} → peak is {'right' if nums[mid] < nums[mid + 1] else 'here or left'}", A("nums", nums, hl=range(lo, hi + 1), lo=lo, mid=mid, hi=hi))
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


# 11 --------------------------------------------------------------
Q(69, "Sqrt(x)", "Easy", "Search on the answer",
  "Return ⌊√x⌋ without using a power or sqrt function.",
  [((4,), 2), ((8,), 2), ((0,), 0), ((1,), 1)],
  ("Try r = 0, 1, 2, … while r² ≤ x.", "O(√x)", "O(1)"),
  ("Find the largest r with r² ≤ x by binary search on [0, x].", "O(log x)", "O(1)"),
  viz=(50,))


@B
def my_sqrt(x):
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r


@O
def my_sqrt(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2
        T(f"{mid}² = {mid * mid} {'≤' if mid * mid <= x else '>'} {x}", V(lo=lo, mid=mid, hi=hi))
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


# 12 --------------------------------------------------------------
Q(410, "Split Array Largest Sum", "Hard", "Minimise the max",
  "Split <code>nums</code> into <code>k</code> non-empty contiguous parts to minimise the largest part sum.",
  [(([7, 2, 5, 10, 8], 2), 18), (([1, 2, 3, 4, 5], 2), 9), (([1, 4, 4], 3), 4)],
  ("Try every placement of k − 1 cuts.", "O(C(n, k) · n)", "O(k)"),
  ("Guess a cap S. Greedily pack elements until adding one would exceed S; count the parts. Fewer parts are needed for bigger S, so binary search the smallest S that needs ≤ k parts.", "O(n log sum)", "O(1)"))


@B
def split_array(nums, k):
    from itertools import combinations
    n, best = len(nums), float("inf")
    for cuts in combinations(range(1, n), k - 1):
        b = (0,) + cuts + (n,)
        best = min(best, max(sum(nums[b[i]:b[i + 1]]) for i in range(k)))
    return best


@O
def split_array(nums, k):
    def parts(cap):
        count, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                count, cur = count + 1, 0
            cur += x
        return count

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"Max part sum {mid} → needs {parts(mid)} part(s), allowed {k}", A("nums", nums), V(lo=lo, mid=mid, hi=hi))
        if parts(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


# 13 --------------------------------------------------------------
Q(540, "Single Element in a Sorted Array", "Medium", "Pair parity",
  "Every value appears twice except one. Find it in O(log n).",
  [(([1, 1, 2, 3, 3, 4, 4, 8, 8],), 2), (([3, 3, 7, 7, 10, 11, 11],), 10)],
  ("XOR every element.", "O(n)", "O(1)"),
  ("Before the single element, pairs start at even indices; after it, at odd ones. Check the pair at an even mid: if nums[mid] == nums[mid+1], the single is to the right.", "O(log n)", "O(1)"))


@B
def single_non_duplicate(nums):
    x = 0
    for v in nums:
        x ^= v
    return x


@O
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid % 2:
            mid -= 1
        T(f"Pair at even index {mid}: {nums[mid]}, {nums[mid + 1]} → {'intact, go right' if nums[mid] == nums[mid + 1] else 'broken, go left'}", A("nums", nums, hl=range(lo, hi + 1), ok=[mid, mid + 1], lo=lo, mid=mid, hi=hi), at="prev")
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid
    return nums[lo]


# 14 --------------------------------------------------------------
Q(81, "Search in Rotated Sorted Array II", "Medium", "Rotated with duplicates",
  "Like Search in Rotated Sorted Array, but values may repeat. Return whether <code>target</code> is present.",
  [(([2, 5, 6, 0, 0, 1, 2], 0), True), (([2, 5, 6, 0, 0, 1, 2], 3), False), (([1, 0, 1, 1, 1], 0), True)],
  ("Linear scan.", "O(n)", "O(1)"),
  ("Same sorted-half logic. When nums[lo] == nums[mid] == nums[hi] we can't tell which half is sorted, so shrink both ends by one.", "O(log n) average, O(n) worst", "O(1)"),
  viz=([1, 0, 1, 1, 1], 0))


@B
def search_rotated_dup(nums, target):
    return target in nums


@O
def search_rotated_dup(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        T(f"nums[mid] = {nums[mid]}", A("nums", nums, hl=range(lo, hi + 1), lo=lo, mid=mid, hi=hi))
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo, hi = lo + 1, hi - 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False


# 15 --------------------------------------------------------------
Q(1482, "Minimum Number of Days to Make m Bouquets", "Medium", "Search on the answer",
  "Flower i blooms on day <code>bloomDay[i]</code>. A bouquet needs <code>k</code> adjacent bloomed flowers. Return the earliest day you can make <code>m</code> bouquets, or −1.",
  [(([1, 10, 3, 10, 2], 3, 1), 3), (([1, 10, 3, 10, 2], 3, 2), -1), (([7, 7, 7, 7, 12, 7, 7], 2, 3), 12)],
  ("Try every distinct bloom day in increasing order.", "O(n²)", "O(n)"),
  ("More days never means fewer bouquets. Binary search the day; count bouquets by scanning runs of bloomed flowers.", "O(n log max)", "O(1)"))


@B
def min_days(bloom_day, m, k):
    def count(day):
        b = run = 0
        for d in bloom_day:
            run = run + 1 if d <= day else 0
            if run == k:
                b, run = b + 1, 0
        return b
    for day in sorted(set(bloom_day)):
        if count(day) >= m:
            return day
    return -1


@O
def min_days(bloom_day, m, k):
    if m * k > len(bloom_day):
        return -1

    def count(day):
        b = run = 0
        for d in bloom_day:
            run = run + 1 if d <= day else 0
            if run == k:
                b, run = b + 1, 0
        return b

    lo, hi = min(bloom_day), max(bloom_day)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"By day {mid}: {count(mid)} bouquet(s), need {m}", A("bloomDay", bloom_day, ok=[i for i, d in enumerate(bloom_day) if d <= mid]), V(lo=lo, mid=mid, hi=hi))
        if count(mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


# 16 --------------------------------------------------------------
Q(1283, "Find the Smallest Divisor Given a Threshold", "Medium", "Search on the answer",
  "Choose a positive divisor; sum ⌈nums[i] / divisor⌉. Return the smallest divisor with sum ≤ <code>threshold</code>.",
  [(([1, 2, 5, 9], 6), 5), (([44, 22, 33, 11, 1], 5), 44)],
  ("Try divisors 1, 2, 3, … in order.", "O(n · max)", "O(1)"),
  ("The sum shrinks as the divisor grows. Binary search the divisor in [1, max(nums)].", "O(n log max)", "O(1)"))


@B
def smallest_divisor(nums, threshold):
    d = 1
    while sum((x + d - 1) // d for x in nums) > threshold:
        d += 1
    return d


@O
def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        d = (lo + hi) // 2
        total = sum((x + d - 1) // d for x in nums)
        T(f"Divisor {d}: sum of ceilings {total} vs threshold {threshold}", A("nums", nums), V(lo=lo, d=d, hi=hi, total=total))
        if total <= threshold:
            hi = d
        else:
            lo = d + 1
    return lo


# 17 --------------------------------------------------------------
Q(1539, "Kth Missing Positive Number", "Easy", "Missing count at index",
  "<code>arr</code> is strictly increasing positive integers. Return the k-th positive integer missing from it.",
  [(([2, 3, 4, 7, 11], 5), 9), (([1, 2, 3, 4], 2), 6)],
  ("Count up from 1, skipping numbers in arr.", "O(n + k)", "O(1)"),
  ("Before index i, arr[i] − (i + 1) numbers are missing. Binary search the first index where that count reaches k; the answer is index + k.", "O(log n)", "O(1)"))


@B
def find_kth_positive(arr, k):
    s, x = set(arr), 0
    while k:
        x += 1
        if x not in s:
            k -= 1
    return x


@O
def find_kth_positive(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"Missing before index {mid}: {arr[mid]} − {mid + 1} = {arr[mid] - mid - 1}", A("arr", arr, hl=range(lo, hi), lo=lo, mid=mid, hi=hi), V(k=k))
        if arr[mid] - mid - 1 >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo + k


# 18 --------------------------------------------------------------
Q(1552, "Magnetic Force Between Two Balls", "Medium", "Maximise the min (aggressive cows)",
  "Place <code>m</code> balls in baskets at <code>position</code> so the minimum distance between any two balls is as large as possible. Return that distance.",
  [(([1, 2, 3, 4, 7], 3), 3), (([5, 4, 3, 2, 1, 1000000000], 2), 999999999)],
  ("Try every gap d from 1 upward and check greedily.", "O(n · range)", "O(1)"),
  ("Sort. For a gap d, place balls greedily left to right. If m balls fit, a larger d may too, so binary search the largest feasible d.", "O(n log range)", "O(1)"))


@B
def max_distance(position, m):
    p = sorted(position)

    def fits(d):
        count, last = 1, p[0]
        for x in p[1:]:
            if x - last >= d:
                count, last = count + 1, x
        return count >= m

    best = 0
    for d in sorted({b - a for i, a in enumerate(p) for b in p[i + 1:]}):
        if fits(d):
            best = d
    return best


@O
def max_distance(position, m):
    position.sort()

    def fits(d):
        count, last = 1, position[0]
        for x in position[1:]:
            if x - last >= d:
                count, last = count + 1, x
        return count >= m

    lo, hi = 1, position[-1] - position[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        T(f"Can {m} balls be at least {mid} apart? {fits(mid)}", A("position", position), V(lo=lo, mid=mid, hi=hi))
        if fits(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


# 19 --------------------------------------------------------------
Q(658, "Find K Closest Elements", "Medium", "Binary search the window start",
  "Return the <code>k</code> elements of sorted <code>arr</code> closest to <code>x</code>, in ascending order (ties prefer the smaller value).",
  [(([1, 2, 3, 4, 5], 4, 3), [1, 2, 3, 4]), (([1, 1, 2, 3, 4, 5], 4, -1), [1, 1, 2, 3])],
  ("Sort by (|a − x|, a), take k, sort again.", "O(n log n)", "O(n)"),
  ("Binary search the left edge L of the k-window in [0, n − k]: if x − arr[mid] &gt; arr[mid + k] − x, the window should move right.", "O(log(n − k) + k)", "O(1)"),
  viz=([1, 3, 5, 8, 9, 12, 15, 18, 20], 3, 10))


@B
def find_closest_elements(arr, k, x):
    return sorted(sorted(arr, key=lambda a: (abs(a - x), a))[:k])


@O
def find_closest_elements(arr, k, x):
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = (lo + hi) // 2
        T(f"Window starting at {mid}: compare x − {arr[mid]} = {x - arr[mid]} with {arr[mid + k]} − x = {arr[mid + k] - x}", A("arr", arr, hl=range(mid, mid + k), lo=lo, mid=mid, hi=hi))
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return arr[lo:lo + k]


# 20 --------------------------------------------------------------
Q(240, "Search a 2D Matrix II", "Medium", "Staircase from a corner",
  "Rows and columns are each sorted ascending. Return whether <code>target</code> is in the matrix.",
  [(([[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 5), True),
   (([[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 20), False)],
  ("Binary search each row.", "O(m log n)", "O(1)"),
  ("Start at the top-right corner. Too big → move left (the whole column below is bigger). Too small → move down. Each step removes a row or a column.", "O(m + n)", "O(1)"),
  viz=([[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]], 14))


@B
def search_matrix_ii(matrix, target):
    from bisect import bisect_left
    for row in matrix:
        i = bisect_left(row, target)
        if i < len(row) and row[i] == target:
            return True
    return False


@O
def search_matrix_ii(matrix, target):
    r, c = 0, len(matrix[0]) - 1
    path = []
    while r < len(matrix) and c >= 0:
        v = matrix[r][c]
        path.append((r, c))
        T(f"({r},{c}) = {v} {'= target' if v == target else '> target → left' if v > target else '< target → down'}", G("matrix", matrix, hl=path[:-1], ok=[(r, c)]))
        if v == target:
            return True
        if v > target:
            c -= 1
        else:
            r += 1
    return False
