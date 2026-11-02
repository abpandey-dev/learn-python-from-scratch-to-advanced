from lib import *

TOPIC(
    id="heap", title="Heap / Priority Queue", glyph="▲min",
    blurb="Always know the smallest (or largest) item in O(1) and update it in O(log n) — top-k, merging, scheduling.",
    demo_title="heappush: a new value bubbles up until its parent is smaller",
    theory="""
<h3>What it is</h3>
<p>A <b>binary heap</b> is a complete binary tree stored in a plain list where every parent is ≤ its children (a <b>min-heap</b>). So the smallest item is always <code>heap[0]</code>. For index i, the children are at <code>2i + 1</code> and <code>2i + 2</code> and the parent at <code>(i − 1) // 2</code>.</p>
<h3>Python's <code>heapq</code></h3>
<table>
<tr><th>Call</th><th>What it does</th><th>Cost</th></tr>
<tr><td><code>heapq.heappush(h, x)</code></td><td>add x, bubble it up</td><td>O(log n)</td></tr>
<tr><td><code>heapq.heappop(h)</code></td><td>remove and return the smallest</td><td>O(log n)</td></tr>
<tr><td><code>h[0]</code></td><td>peek the smallest</td><td>O(1)</td></tr>
<tr><td><code>heapq.heapify(list)</code></td><td>turn a list into a heap in place</td><td>O(n)</td></tr>
<tr><td><code>heapq.heapreplace(h, x)</code></td><td>pop then push in one step</td><td>O(log n)</td></tr>
</table>
<p>Python only has a min-heap. For a <b>max-heap</b> push <code>-x</code> and negate when you pop. For custom order push tuples: <code>(priority, tiebreak, item)</code>.</p>
<h3>Spot the pattern</h3>
<ul>
<li><b>"k-th largest" / "top k"</b> → keep a <i>min</i>-heap of size k; its top is the k-th largest. O(n log k).</li>
<li><b>Merge k sorted things</b> → heap of the current head of each.</li>
<li><b>Running median</b> → two heaps: a max-heap for the lower half, a min-heap for the upper half.</li>
<li><b>Scheduling / greedy by best available</b> (CPU tasks, IPO, meeting rooms) → sort by time, push what's available, pop the best.</li>
<li>Repeatedly take the largest and put something back (last stone, remove stones) → max-heap.</li>
</ul>
<h3>Template: k-th largest</h3>
<pre><code class="py">import heapq
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) &gt; k:
        heapq.heappop(heap)   # drop the smallest; the k largest stay
return heap[0]</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Expecting <code>heap</code> to be sorted — only <code>heap[0]</code> is guaranteed.</li>
<li>Pushing tuples whose second item isn't comparable (e.g. ListNode) — add an index tiebreak.</li>
<li>Using a max-heap of size n for top-k when a min-heap of size k is cheaper.</li>
</ul>
""")


@D
def heap_demo():
    import heapq
    heap = []
    for x in [7, 4, 9, 2, 5, 1]:
        heapq.heappush(heap, x)
        T(f"heappush({x}) — smallest is now heap[0] = {heap[0]}", H("heap as a tree", heap, hl=[heap.index(x)]), A("heap as a list", heap, hl=[heap.index(x)]), at="prev")
    while heap:
        x = heapq.heappop(heap)
        T(f"heappop() → {x}; the last leaf moves to the root and sinks down", H("heap as a tree", heap), A("heap as a list", heap), at="prev")
    return heap


# 1 ---------------------------------------------------------------
Q(215, "Kth Largest Element in an Array", "Medium", "Min-heap of size k",
  "Return the k-th largest element of <code>nums</code> (in sorted order, not the k-th distinct).",
  [(([3, 2, 1, 5, 6, 4], 2), 5), (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)],
  ("Sort descending and index k − 1.", "O(n log n)", "O(n)"),
  ("Keep a min-heap of the k largest seen. When it grows past k, pop the smallest. The top is the answer. (Quickselect gives O(n) average.)", "O(n log k)", "O(k)"))


@B
def find_kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]


@O
def find_kth_largest(nums, k):
    import heapq
    heap = []
    for i, x in enumerate(nums):
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
        T(f"Add {x}; heap keeps the {k} largest, top = {heap[0]}", A("nums", nums, hl=[i], i=i), H("min-heap", heap, hl=[0]), at="prev")
    return heap[0]


# 2 ---------------------------------------------------------------
Q(703, "Kth Largest Element in a Stream", "Easy", "Min-heap of size k · design",
  "Design a class that, after each <code>add(val)</code>, returns the k-th largest value seen so far.",
  [(((3, [4, 5, 8, 2]), [("add", (3,)), ("add", (5,)), ("add", (10,)), ("add", (9,)), ("add", (4,))]), [4, 5, 5, 8, 8])],
  ("Keep every value in a sorted list (insort) and index from the end.", "add O(n)", "O(n)"),
  ("Keep only the k largest values in a min-heap; its top is the k-th largest.", "add O(log k)", "O(k)"),
  design=True)


@B
class KthLargest:
    def __init__(self, k, nums):
        self.k, self.vals = k, sorted(nums)

    def add(self, val):
        from bisect import insort
        insort(self.vals, val)
        return self.vals[-self.k]


@O
class KthLargest:
    def __init__(self, k, nums):
        import heapq
        self.k, self.heap = k, list(nums)
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        import heapq
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        T(f"add({val}) → k-th largest = {self.heap[0]}", H("min-heap of the k largest", self.heap, hl=[0]), at="prev")
        return self.heap[0]


# 3 ---------------------------------------------------------------
Q(1046, "Last Stone Weight", "Easy", "Max-heap",
  "Repeatedly smash the two heaviest stones: equal → both vanish, else the difference remains. Return the last stone's weight or 0.",
  [(([2, 7, 4, 1, 8, 1],), 1), (([1],), 1)],
  ("Sort the stones every round and take the last two.", "O(n² log n)", "O(1)"),
  ("Max-heap (negated values): pop two, push the difference if non-zero.", "O(n log n)", "O(n)"))


@B
def last_stone_weight(stones):
    stones = list(stones)
    while len(stones) > 1:
        stones.sort()
        y, x = stones.pop(), stones.pop()
        if y != x:
            stones.append(y - x)
    return stones[0] if stones else 0


@O
def last_stone_weight(stones):
    import heapq
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        y, x = -heapq.heappop(heap), -heapq.heappop(heap)
        if y != x:
            heapq.heappush(heap, -(y - x))
        T(f"Smash {y} and {x} → {'leftover ' + str(y - x) if y != x else 'both gone'}", H("max-heap (shown as weights)", [-v for v in heap], hl=[0]), at="prev")
    return -heap[0] if heap else 0


# 4 ---------------------------------------------------------------
Q(973, "K Closest Points to Origin", "Medium", "Max-heap of size k",
  "Return the <code>k</code> points closest to (0, 0) by Euclidean distance, in any order.",
  [(([[1, 3], [-2, 2]], 1), [[-2, 2]]), (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]])],
  ("Sort all points by x² + y² and take k.", "O(n log n)", "O(n)"),
  ("Keep a max-heap (negated distance) of the k closest so far; a closer point replaces the farthest.", "O(n log k)", "O(k)"),
  norm=sorted, viz=([[3, 3], [5, -1], [-2, 4], [1, 1], [0, 2]], 2))


@B
def k_closest(points, k):
    return sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]


@O
def k_closest(points, k):
    import heapq
    heap = []
    for x, y in points:
        d = x * x + y * y
        heapq.heappush(heap, (-d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
        T(f"Point ({x},{y}) at distance² {d}; keep the {k} closest", H("max-heap of (−dist², x, y)", heap, hl=[0]), at="prev")
    return [[x, y] for _, x, y in heap]


# 5 ---------------------------------------------------------------
Q(692, "Top K Frequent Words", "Medium", "Heap with (−count, word)",
  "Return the <code>k</code> most frequent words, sorted by frequency then alphabetically.",
  [((["i", "love", "leetcode", "i", "love", "coding"], 2), ["i", "love"]), ((["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4), ["the", "is", "sunny", "day"])],
  ("Count, then sort all distinct words by (−count, word).", "O(n log n)", "O(n)"),
  ("Count, heapify (−count, word) pairs in O(n), then pop k times. Ties come out alphabetically because words compare as strings.", "O(n + k log n)", "O(n)"),
  viz=(["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4))


@B
def top_k_frequent_words(words, k):
    count = {}
    for w in words:
        count[w] = count.get(w, 0) + 1
    return sorted(count, key=lambda w: (-count[w], w))[:k]


@O
def top_k_frequent_words(words, k):
    import heapq
    count = {}
    for w in words:
        count[w] = count.get(w, 0) + 1
    heap = [(-c, w) for w, c in count.items()]
    heapq.heapify(heap)
    res = []
    for _ in range(k):
        c, w = heapq.heappop(heap)
        res.append(w)
        T(f"Pop '{w}' ({-c} times)", M("count", count, hl=w), H("heap of (−count, word)", heap), A("res", res), at="prev")
    return res


# 6 ---------------------------------------------------------------
Q(621, "Task Scheduler", "Medium", "Max-heap + cooldown queue",
  "Each CPU slot runs one task or idles; the same task needs <code>n</code> slots between runs. Return the fewest slots to finish all tasks.",
  [((["A", "A", "A", "B", "B", "B"], 2), 8), ((["A", "C", "A", "B", "D", "B"], 1), 6), ((["A", "A", "A", "B", "B", "B"], 3), 10)],
  ("Simulate each slot, scanning all task types to pick the available one with most remaining.", "O(T · 26)", "O(26)"),
  ("Simulate with a max-heap of remaining counts and a queue of tasks cooling down (count, ready time). Pop the most frequent ready task each slot. (A closed formula, (maxCount − 1)(n + 1) + #tasksWithMax, also works.)", "O(T · log 26)", "O(26)"),
  viz=(["A", "A", "A", "B", "B", "C"], 2))


@B
def least_interval(tasks, n):
    count = {}
    for t in tasks:
        count[t] = count.get(t, 0) + 1
    ready_at = {t: 0 for t in count}
    time = 0
    while count:
        avail = [t for t in count if ready_at[t] <= time]
        if avail:
            t = max(avail, key=lambda x: count[x])
            count[t] -= 1
            ready_at[t] = time + n + 1
            if count[t] == 0:
                del count[t]
        time += 1
    return time


@O
def least_interval(tasks, n):
    import heapq
    from collections import Counter, deque
    heap = [-c for c in Counter(tasks).values()]
    heapq.heapify(heap)
    cooling, time = deque(), 0
    while heap or cooling:
        time += 1
        if heap:
            c = heapq.heappop(heap) + 1
            if c:
                cooling.append((c, time + n))
        if cooling and cooling[0][1] == time:
            heapq.heappush(heap, cooling.popleft()[0])
        T(f"Slot {time}", H("ready (remaining counts)", [-c for c in heap]), A("cooling (count, ready at)", [f"{-c}@{t}" for c, t in cooling]), at="prev")
    return time


# 7 ---------------------------------------------------------------
Q(295, "Find Median from Data Stream", "Hard", "Two heaps",
  "Design <code>addNum(num)</code> and <code>findMedian()</code> for a growing stream of numbers.",
  [(((), [("addNum", (1,)), ("addNum", (2,)), ("findMedian", ()), ("addNum", (3,)), ("findMedian", ())]), [None, None, 1.5, None, 2.0])],
  ("Keep a sorted list with insort; the median is the middle.", "addNum O(n)", "O(n)"),
  ("A max-heap 'low' holds the smaller half and a min-heap 'high' the larger half, balanced so low has the same size or one more. The median is low's top or the average of both tops.", "addNum O(log n), findMedian O(1)", "O(n)"),
  design=True, viz=((), [("addNum", (5,)), ("addNum", (15,)), ("addNum", (1,)), ("findMedian", ()), ("addNum", (3,)), ("findMedian", ())]))


@B
class MedianFinder:
    def __init__(self):
        self.vals = []

    def addNum(self, num):
        from bisect import insort
        insort(self.vals, num)

    def findMedian(self):
        n = len(self.vals)
        return float(self.vals[n // 2]) if n % 2 else (self.vals[n // 2 - 1] + self.vals[n // 2]) / 2


@O
class MedianFinder:
    def __init__(self):
        self.low, self.high = [], []  # low is a max-heap (negated)

    def addNum(self, num):
        import heapq
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))
        T(f"addNum({num}) and rebalance", H("low half (max-heap)", [-x for x in self.low], hl=[0]), H("high half (min-heap)", self.high, hl=[0]), at="prev")

    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


# 8 ---------------------------------------------------------------
Q(767, "Reorganize String", "Medium", "Max-heap, alternate the top two",
  "Rearrange <code>s</code> so no two adjacent characters are equal; return any such string or <code>\"\"</code>.",
  [(("aab",), "aba"), (("aaab",), ""), (("vvvlo",), "vlvov")],
  ("Try permutations until one has no equal neighbours.", "O(n! · n)", "O(n)"),
  ("Always place the most frequent remaining letter that differs from the last one: pop the top; if it equals the last placed, pop the next one instead and push the first back.", "O(n log σ)", "O(σ)"),
  check=lambda a, out: (out == "" and max(a[0].count(c) for c in a[0]) > (len(a[0]) + 1) // 2) or (sorted(out) == sorted(a[0]) and all(x != y for x, y in zip(out, out[1:]))))


@B
def reorganize_string(s):
    from itertools import permutations
    for p in set(permutations(s)):
        if all(a != b for a, b in zip(p, p[1:])):
            return "".join(p)
    return ""


@O
def reorganize_string(s):
    import heapq
    from collections import Counter
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    res = []
    while heap:
        c, ch = heapq.heappop(heap)
        if res and res[-1] == ch:
            if not heap:
                return ""
            c2, ch2 = heapq.heappop(heap)
            res.append(ch2)
            if c2 + 1:
                heapq.heappush(heap, (c2 + 1, ch2))
            heapq.heappush(heap, (c, ch))
        else:
            res.append(ch)
            if c + 1:
                heapq.heappush(heap, (c + 1, ch))
        T(f"Place '{res[-1]}'", H("heap of (−count, char)", heap), A("result", res, hl=[len(res) - 1]), at="prev")
    return "".join(res)


# 9 ---------------------------------------------------------------
Q(451, "Sort Characters By Frequency", "Medium", "Max-heap of counts",
  "Sort the characters of <code>s</code> by decreasing frequency (equal letters stay together).",
  [(("tree",), "eert"), (("cccaaa",), "aaaccc"), (("Aabb",), "bbAa")],
  ("Count, then sort the characters with key (−count, char).", "O(n log n)", "O(n)"),
  ("Count, push (−count, char) into a heap, pop each and write it count times. (Bucket sort by count gives O(n).)", "O(n + σ log σ)", "O(σ)"),
  check=lambda a, out: sorted(out) == sorted(a[0]) and _grouped_desc(out))


def _grouped_desc(out):
    runs = []
    for ch in out:
        if runs and runs[-1][0] == ch:
            runs[-1][1] += 1
        else:
            runs.append([ch, 1])
    chars = [r[0] for r in runs]
    return len(chars) == len(set(chars)) and all(runs[i][1] >= runs[i + 1][1] for i in range(len(runs) - 1))


@B
def frequency_sort(s):
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    return "".join(sorted(s, key=lambda ch: (-count[ch], ch)))


@O
def frequency_sort(s):
    import heapq
    from collections import Counter
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    out = []
    while heap:
        c, ch = heapq.heappop(heap)
        out.append(ch * -c)
        T(f"Write '{ch}' × {-c}", H("heap of (−count, char)", heap), V(result="".join(out)), at="prev")
    return "".join(out)


# 10 --------------------------------------------------------------
Q(373, "Find K Pairs with Smallest Sums", "Medium", "Heap frontier on a sorted grid",
  "Given two sorted arrays, return the <code>k</code> pairs (u, v) with the smallest sums.",
  [(([1, 7, 11], [2, 4, 6], 3), [[1, 2], [1, 4], [1, 6]]), (([1, 1, 2], [1, 2, 3], 2), [[1, 1], [1, 1]])],
  ("Generate all m·n pairs and sort by sum.", "O(mn log(mn))", "O(mn)"),
  ("Think of an m × n grid of sums sorted along rows and columns. Seed the heap with (nums1[i] + nums2[0]) for each row, and after popping (i, j) push (i, j + 1).", "O(k log min(k, m))", "O(min(k, m))"),
  norm=lambda r: sorted(r))


@B
def k_smallest_pairs(nums1, nums2, k):
    pairs = [[a, b] for a in nums1 for b in nums2]
    pairs.sort(key=lambda p: p[0] + p[1])
    return pairs[:k]


@O
def k_smallest_pairs(nums1, nums2, k):
    import heapq
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(heap)
    res = []
    while heap and len(res) < k:
        s, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        T(f"Pop pair ({nums1[i]}, {nums2[j]}) sum {s}; push its right neighbour", G("sum grid", [[a + b for b in nums2] for a in nums1], ok=[(r, c) for r, c in [(nums1.index(p[0]), nums2.index(p[1])) for p in res]], hl=[(ii, jj) for _, ii, jj in heap], rl=nums1, cl=nums2), V(result=res), at="prev")
    return res


# 11 --------------------------------------------------------------
Q(378, "Kth Smallest Element in a Sorted Matrix", "Medium", "Heap of row heads",
  "Every row and column of an n × n matrix is sorted. Return the k-th smallest element.",
  [(([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8), 13), (([[-5]], 1), -5)],
  ("Flatten and sort.", "O(n² log n)", "O(n²)"),
  ("Push the first element of each row. Pop k − 1 times, each time pushing the next element in the popped row. The top is the answer. (Binary search on value also works.)", "O(k log n)", "O(n)"))


@B
def kth_smallest_matrix(matrix, k):
    return sorted(x for row in matrix for x in row)[k - 1]


@O
def kth_smallest_matrix(matrix, k):
    import heapq
    heap = [(row[0], r, 0) for r, row in enumerate(matrix)]
    heapq.heapify(heap)
    popped = []
    for _ in range(k - 1):
        v, r, c = heapq.heappop(heap)
        popped.append((r, c))
        if c + 1 < len(matrix[0]):
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))
        T(f"Pop {v} (#{len(popped)} smallest)", G("matrix", matrix, ok=popped, hl=[(rr, cc) for _, rr, cc in heap]), at="prev")
    T(f"The heap top {heap[0][0]} is the {k}-th smallest", G("matrix", matrix, ok=popped, bad=[(heap[0][1], heap[0][2])]))
    return heap[0][0]


# 12 --------------------------------------------------------------
Q(502, "IPO", "Hard", "Sort by capital + max-heap of profit",
  "You start with capital <code>w</code> and may finish at most <code>k</code> projects; a project needs <code>capital[i]</code> to start and adds <code>profits[i]</code>. Maximise final capital.",
  [((2, 0, [1, 2, 3], [0, 1, 1]), 4), ((3, 0, [1, 2, 3], [0, 1, 2]), 6)],
  ("Each round, scan every unused project you can afford and take the most profitable.", "O(k · n)", "O(n)"),
  ("Sort projects by capital. Each round push every newly affordable project's profit into a max-heap, then take the top.", "O((n + k) log n)", "O(n)"),
  viz=(3, 0, [1, 2, 3, 5], [0, 1, 1, 3]))


@B
def find_maximized_capital(k, w, profits, capital):
    used = [False] * len(profits)
    for _ in range(k):
        best = -1
        for i in range(len(profits)):
            if not used[i] and capital[i] <= w and (best < 0 or profits[i] > profits[best]):
                best = i
        if best < 0:
            break
        used[best] = True
        w += profits[best]
    return w


@O
def find_maximized_capital(k, w, profits, capital):
    import heapq
    projects = sorted(zip(capital, profits))
    heap, i = [], 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])
            i += 1
        if not heap:
            break
        gain = -heapq.heappop(heap)
        w += gain
        T(f"Affordable profits in the heap; take {gain} → capital {w}", A("projects (capital, profit)", projects, ok=range(i)), H("max-heap of profits", [-x for x in heap]), V(capital=w), at="prev")
    return w


# 13 --------------------------------------------------------------
Q(632, "Smallest Range Covering Elements from K Lists", "Hard", "Heap of one per list + running max",
  "Find the smallest range [a, b] that includes at least one number from each of the k sorted lists.",
  [(([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]],), [20, 24]), (([[1, 2, 3], [1, 2, 3], [1, 2, 3]],), [1, 1])],
  ("Try every pair of values as the range ends and check that each list has a value inside.", "O(N² · k log)", "O(1)"),
  ("Hold one element from every list in a min-heap and track the max. The range [heap min, max] covers all lists. Advance the list that gave the min; stop when a list runs out.", "O(N log k)", "O(k)"))


@B
def smallest_range(nums):
    from bisect import bisect_left
    vals = sorted({x for row in nums for x in row})
    best = None
    for a in vals:
        for b in vals:
            if b < a:
                continue
            if all(bisect_left(row, a) < len(row) and row[bisect_left(row, a)] <= b for row in nums):
                if best is None or (b - a, a) < (best[1] - best[0], best[0]):
                    best = [a, b]
                break
    return best


@O
def smallest_range(nums):
    import heapq
    heap = [(row[0], r, 0) for r, row in enumerate(nums)]
    heapq.heapify(heap)
    high = max(row[0] for row in nums)
    best = [heap[0][0], high]
    while True:
        low, r, c = heapq.heappop(heap)
        if high - low < best[1] - best[0]:
            best = [low, high]
        T(f"Current range [{low}, {high}] covers every list; best {best}", A("picked (one per list)", sorted([low] + [v for v, _, _ in heap])), V(low=low, high=high, best=best))
        if c + 1 == len(nums[r]):
            return best
        nxt = nums[r][c + 1]
        high = max(high, nxt)
        heapq.heappush(heap, (nxt, r, c + 1))


# 14 --------------------------------------------------------------
Q(264, "Ugly Number II", "Medium", "Heap of multiples",
  "Ugly numbers have no prime factors other than 2, 3 and 5 (1 counts). Return the n-th one.",
  [((10,), 12), ((1,), 1), ((15,), 24)],
  ("Test 1, 2, 3, … dividing out 2, 3 and 5 until n ugly numbers are found.", "O(answer · log)", "O(1)"),
  ("Pop the smallest ugly number x from a heap and push 2x, 3x, 5x (skipping ones already seen). The n-th pop is the answer. (Three pointers give O(n).)", "O(n log n)", "O(n)"))


@B
def nth_ugly_number(n):
    x, found = 0, 0
    while found < n:
        x += 1
        y = x
        for p in (2, 3, 5):
            while y % p == 0:
                y //= p
        found += y == 1
    return x


@O
def nth_ugly_number(n):
    import heapq
    heap, seen = [1], {1}
    for i in range(n):
        x = heapq.heappop(heap)
        for p in (2, 3, 5):
            if x * p not in seen:
                seen.add(x * p)
                heapq.heappush(heap, x * p)
        T(f"Ugly #{i + 1} = {x}; push {x * 2}, {x * 3}, {x * 5}", H("heap", heap, hl=[0]), at="prev")
    return x


# 15 --------------------------------------------------------------
Q(1834, "Single-Threaded CPU", "Medium", "Sort by time + heap by (duration, index)",
  "Task i becomes available at <code>tasks[i][0]</code> and takes <code>tasks[i][1]</code>. An idle CPU picks the shortest available task (smallest index on ties). Return the order tasks run.",
  [(([[1, 2], [2, 4], [3, 2], [4, 1]],), [0, 2, 3, 1]), (([[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]],), [4, 3, 2, 0, 1])],
  ("At each step scan all tasks for available ones and pick the best.", "O(n²)", "O(n)"),
  ("Sort task indices by start time. Push every task that has arrived into a heap keyed by (duration, index); if none has arrived, jump time forward.", "O(n log n)", "O(n)"))


@B
def get_order(tasks):
    done, order, time = [False] * len(tasks), [], 0
    while len(order) < len(tasks):
        avail = [i for i in range(len(tasks)) if not done[i] and tasks[i][0] <= time]
        if not avail:
            time = min(tasks[i][0] for i in range(len(tasks)) if not done[i])
            continue
        i = min(avail, key=lambda i: (tasks[i][1], i))
        done[i] = True
        order.append(i)
        time += tasks[i][1]
    return order


@O
def get_order(tasks):
    import heapq
    idx = sorted(range(len(tasks)), key=lambda i: tasks[i][0])
    heap, order, time, j = [], [], 0, 0
    while len(order) < len(tasks):
        if not heap and time < tasks[idx[j]][0]:
            time = tasks[idx[j]][0]
        while j < len(idx) and tasks[idx[j]][0] <= time:
            heapq.heappush(heap, (tasks[idx[j]][1], idx[j]))
            j += 1
        d, i = heapq.heappop(heap)
        time += d
        order.append(i)
        T(f"Run task {i} (duration {d}); time is now {time}", H("available (duration, index)", heap), A("order", order), at="prev")
    return order


# 16 --------------------------------------------------------------
Q(1642, "Furthest Building You Can Reach", "Medium", "Min-heap of ladder climbs",
  "Climbing up costs bricks equal to the height gain, or one ladder. Return the furthest building index you can reach.",
  [(([4, 2, 7, 6, 9, 14, 12], 5, 1), 4), (([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2), 7), (([14, 3, 19, 3], 17, 0), 3)],
  ("Try both choices (bricks or ladder) at every climb.", "O(2ⁿ)", "O(n)"),
  ("Use ladders on the biggest climbs. Push each climb into a min-heap; once it holds more climbs than ladders, pay for the smallest one with bricks. Stop when bricks go negative.", "O(n log L)", "O(L)"))


@B
def furthest_building(heights, bricks, ladders):
    def go(i, b, l):
        if i == len(heights) - 1:
            return i
        d = heights[i + 1] - heights[i]
        if d <= 0:
            return go(i + 1, b, l)
        best = i
        if b >= d:
            best = max(best, go(i + 1, b - d, l))
        if l:
            best = max(best, go(i + 1, b, l - 1))
        return best
    return go(0, bricks, ladders)


@O
def furthest_building(heights, bricks, ladders):
    import heapq
    heap = []
    for i in range(len(heights) - 1):
        d = heights[i + 1] - heights[i]
        if d <= 0:
            continue
        heapq.heappush(heap, d)
        if len(heap) > ladders:
            bricks -= heapq.heappop(heap)
        T(f"Climb {d} to building {i + 1}; ladders cover the biggest climbs, bricks left {bricks}", A("heights", heights, hl=[i, i + 1], i=i), H("climbs on ladders (min-heap)", heap), V(bricks=bricks), at="prev")
        if bricks < 0:
            return i
    return len(heights) - 1


# 17 --------------------------------------------------------------
Q(846, "Hand of Straights", "Medium", "Count + min-heap of starts",
  "Can the cards in <code>hand</code> be split into groups of <code>groupSize</code> consecutive values?",
  [(([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), True), (([1, 2, 3, 4, 5], 4), False)],
  ("Sort; repeatedly remove the smallest card and the next groupSize − 1 values from the list.", "O(n²)", "O(n)"),
  ("The smallest remaining card must start a group. Keep counts and a min-heap of values; take groupSize consecutive values from the smallest, decrementing counts.", "O(n log n)", "O(n)"))


@B
def is_n_straight_hand(hand, group_size):
    cards = sorted(hand)
    while cards:
        start = cards[0]
        for v in range(start, start + group_size):
            if v not in cards:
                return False
            cards.remove(v)
    return True


@O
def is_n_straight_hand(hand, group_size):
    import heapq
    from collections import Counter
    if len(hand) % group_size:
        return False
    count = Counter(hand)
    heap = list(count)
    heapq.heapify(heap)
    while heap:
        start = heap[0]
        for v in range(start, start + group_size):
            if count[v] == 0:
                return False
            count[v] -= 1
            if count[v] == 0:
                if v != heap[0]:
                    return False
                heapq.heappop(heap)
        T(f"Group {list(range(start, start + group_size))} formed", M("count", {k: c for k, c in sorted(count.items()) if c}), H("min-heap of values", heap), at="prev")
    return True


# 18 --------------------------------------------------------------
Q(253, "Meeting Rooms II", "Medium", "Min-heap of end times",
  "Given meeting intervals, return the minimum number of rooms needed.",
  [(([[0, 30], [5, 10], [15, 20]],), 2), (([[7, 10], [2, 4]],), 1), (([[1, 5], [2, 6], [3, 7], [6, 8]],), 3)],
  ("For every meeting start, count how many meetings are running at that moment.", "O(n²)", "O(1)"),
  ("Sort by start. A min-heap holds end times of rooms in use; if the earliest-ending room is free by this start, reuse it (pop), then push this meeting's end. The heap size is the answer.", "O(n log n)", "O(n)"))


@B
def min_meeting_rooms(intervals):
    best = 0
    for s, _ in intervals:
        best = max(best, sum(1 for a, b in intervals if a <= s < b))
    return best


@O
def min_meeting_rooms(intervals):
    import heapq
    intervals = sorted(intervals)
    ends = []
    for s, e in intervals:
        if ends and ends[0] <= s:
            heapq.heappop(ends)
        heapq.heappush(ends, e)
        T(f"Meeting [{s}, {e}): rooms in use end at {sorted(ends)}", A("meetings", [f"{a}-{b}" for a, b in intervals], hl=[intervals.index([s, e])]), H("end times (min-heap)", ends, hl=[0]), V(rooms=len(ends)), at="prev")
    return len(ends)


# 19 --------------------------------------------------------------
Q(2542, "Maximum Subsequence Score", "Medium", "Sort by multiplier + min-heap of sums",
  "Choose k indices; score = (sum of their nums1) × (min of their nums2). Return the max score.",
  [(([1, 3, 3, 2], [2, 1, 3, 4], 3), 12), (([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1), 30)],
  ("Try every combination of k indices.", "O(C(n, k) · k)", "O(k)"),
  ("Sort pairs by nums2 descending so the current nums2 is the minimum. Keep the k largest nums1 seen in a min-heap with their sum; score = sum × current nums2.", "O(n log n)", "O(k)"))


@B
def max_score_subseq(nums1, nums2, k):
    from itertools import combinations
    return max(sum(nums1[i] for i in c) * min(nums2[i] for i in c) for c in combinations(range(len(nums1)), k))


@O
def max_score_subseq(nums1, nums2, k):
    import heapq
    pairs = sorted(zip(nums2, nums1), reverse=True)
    heap, total, best = [], 0, 0
    for m, x in pairs:
        heapq.heappush(heap, x)
        total += x
        if len(heap) > k:
            total -= heapq.heappop(heap)
        if len(heap) == k:
            best = max(best, total * m)
        T(f"min nums2 = {m}; keep the {k} largest nums1 (sum {total})", A("pairs (nums2, nums1) sorted", pairs), H("chosen nums1 (min-heap)", heap), V(score=total * m if len(heap) == k else "-", best=best), at="prev")
    return best


# 20 --------------------------------------------------------------
Q(1962, "Remove Stones to Minimize the Total", "Medium", "Max-heap",
  "<code>k</code> times, pick a pile and remove ⌊pile / 2⌋ stones from it. Return the minimum total left.",
  [(([5, 4, 9], 2), 12), (([4, 3, 6, 7], 3), 12)],
  ("Each time, scan for the largest pile.", "O(k · n)", "O(1)"),
  ("Always halve the largest pile: max-heap, pop, push back pile − pile // 2.", "O(n + k log n)", "O(n)"),
  viz=([4, 3, 6, 7], 3))


@B
def min_stone_sum(piles, k):
    piles = list(piles)
    for _ in range(k):
        i = piles.index(max(piles))
        piles[i] -= piles[i] // 2
    return sum(piles)


@O
def min_stone_sum(piles, k):
    import heapq
    heap = [-p for p in piles]
    heapq.heapify(heap)
    for _ in range(k):
        p = -heapq.heappop(heap)
        heapq.heappush(heap, -(p - p // 2))
        T(f"Halve the biggest pile {p} → {p - p // 2}", H("max-heap (piles)", [-x for x in heap]), V(total=-sum(heap)), at="prev")
    return -sum(heap)
