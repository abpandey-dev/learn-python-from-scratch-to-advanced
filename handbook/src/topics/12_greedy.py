from lib import *

TOPIC(
    id="greedy", title="Greedy & Intervals", glyph="sort→pick",
    blurb="Make the locally best choice and prove it never hurts — usually after sorting, often on intervals.",
    demo_title="Merge intervals: sort by start, then extend or start a new block",
    theory="""
<h3>What it is</h3>
<p>A <b>greedy</b> algorithm commits to the choice that looks best right now and never revisits it. It's only correct when you can argue an <b>exchange</b>: any optimal answer can be changed to include the greedy choice without getting worse. When that argument fails, the problem usually needs DP.</p>
<h3>Interval problems</h3>
<p>Intervals <code>[start, end]</code> almost always start with a sort:</p>
<table>
<tr><th>Goal</th><th>Sort by</th><th>Rule</th></tr>
<tr><td>Merge overlapping</td><td>start</td><td>if <code>start ≤ last.end</code> extend, else open a new interval</td></tr>
<tr><td>Max non-overlapping / min removals</td><td><b>end</b></td><td>keep the interval that finishes first, skip ones that overlap it</td></tr>
<tr><td>Min arrows / points to hit all</td><td>end</td><td>shoot at the current end, skip everything it hits</td></tr>
<tr><td>Max overlap at once (rooms, car pooling)</td><td>events (+1 at start, −1 at end)</td><td>sweep and track the running count</td></tr>
<tr><td>Intersect two sorted lists</td><td>already sorted</td><td>two pointers, advance the one that ends first</td></tr>
</table>
<h3>Other greedy shapes</h3>
<ul>
<li><b>Reach / jump</b> — track the furthest index reachable so far.</li>
<li><b>Running balance</b> — gas station, valid parenthesis string: if the balance drops below zero, restart or adjust a range.</li>
<li><b>Two passes</b> — candy: satisfy the left neighbour rule left→right, then the right rule right→left.</li>
<li><b>Custom sort order</b> — largest number compares <code>a + b</code> vs <code>b + a</code>; two-city scheduling sorts by cost difference.</li>
</ul>
<h3>Template: merge intervals</h3>
<pre><code class="py">intervals.sort()
out = [intervals[0]]
for s, e in intervals[1:]:
    if s &lt;= out[-1][1]:
        out[-1][1] = max(out[-1][1], e)   # overlap → extend
    else:
        out.append([s, e])                # gap → new interval</code></pre>
<h3>Common mistakes</h3>
<ul>
<li>Sorting by start when the proof needs sorting by end (non-overlapping intervals, arrows).</li>
<li>Off-by-one on touching intervals: does <code>[1, 2]</code> overlap <code>[2, 3]</code>? Read the problem — it differs between questions.</li>
<li>Trusting a greedy without a counter-example check. Try a tiny tricky case by hand.</li>
</ul>
""")


@D
def merge_demo():
    intervals = [[1, 3], [8, 10], [2, 6], [15, 18], [9, 12]]
    intervals.sort()
    T("Sort by start", A("intervals", [f"{a}-{b}" for a, b in intervals]))
    out = [intervals[0][:]]
    for i in range(1, len(intervals)):
        s, e = intervals[i]
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
            T(f"[{s},{e}] overlaps the last block → extend it", A("intervals", [f"{a}-{b}" for a, b in intervals], hl=[i], i=i), A("merged", [f"{a}-{b}" for a, b in out], hl=[len(out) - 1]), at="prev")
        else:
            out.append([s, e])
            T(f"[{s},{e}] starts after the last block ends → new block", A("intervals", [f"{a}-{b}" for a, b in intervals], hl=[i], i=i), A("merged", [f"{a}-{b}" for a, b in out], ok=[len(out) - 1]), at="prev")
    return out


IV = lambda xs: [f"{a}-{b}" for a, b in xs]


# 1 ---------------------------------------------------------------
Q(55, "Jump Game", "Medium", "Furthest reach",
  "<code>nums[i]</code> is the maximum jump length from index i. Can you reach the last index from index 0?",
  [(([2, 3, 1, 1, 4],), True), (([3, 2, 1, 0, 4],), False)],
  ("Recursively try every jump length from every index.", "O(2ⁿ)", "O(n)"),
  ("Track the furthest index reachable. If you stand beyond it, you're stuck; otherwise extend it with i + nums[i].", "O(n)", "O(1)"))


@B
def can_jump(nums):
    def go(i):
        if i >= len(nums) - 1:
            return True
        return any(go(i + j) for j in range(1, nums[i] + 1))
    return go(0)


@O
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            T(f"Index {i} is beyond the furthest reach {reach} → stuck", A("nums", nums, ok=range(reach + 1), bad=[i], i=i))
            return False
        reach = max(reach, i + x)
        T(f"From {i} we can reach up to {reach}", A("nums", nums, ok=range(min(reach, len(nums) - 1) + 1), hl=[i], i=i), V(reach=reach), at="prev")
    return True


# 2 ---------------------------------------------------------------
Q(45, "Jump Game II", "Medium", "BFS by reach windows",
  "Return the minimum number of jumps to reach the last index (it's always reachable).",
  [(([2, 3, 1, 1, 4],), 2), (([2, 3, 0, 1, 4],), 2)],
  ("dp[i] = 1 + min(dp[j]) over every j that can jump to i.", "O(n²)", "O(n)"),
  ("Treat each jump as a BFS layer: the current window [start, end] is reachable in k jumps; the furthest index reachable from it is the end of the next window.", "O(n)", "O(1)"),
  viz=([2, 3, 1, 1, 2, 1, 4],))


@B
def jump(nums):
    n = len(nums)
    dp = [0] + [float("inf")] * (n - 1)
    for i in range(1, n):
        for j in range(i):
            if j + nums[j] >= i:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[-1]


@O
def jump(nums):
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            T(f"Window ends at {i}: jump #{jumps} lets us reach up to {far}", A("nums", nums, hl=range(i + 1, far + 1), i=i), V(jumps=jumps), at="prev")
            end = far
    return jumps


# 3 ---------------------------------------------------------------
Q(134, "Gas Station", "Medium", "Running tank, restart on deficit",
  "Station i gives <code>gas[i]</code>; driving to the next costs <code>cost[i]</code>. Return the start index that completes the circle, or −1.",
  [(([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3), (([2, 3, 4], [3, 4, 3]), -1)],
  ("Simulate the full loop from every start.", "O(n²)", "O(1)"),
  ("If total gas &lt; total cost it's impossible. Otherwise drive once; when the tank goes negative at i, no station from the current start to i can work, so restart at i + 1.", "O(n)", "O(1)"))


@B
def can_complete_circuit(gas, cost):
    n = len(gas)
    for s in range(n):
        tank = 0
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return s
    return -1


@O
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            T(f"Tank went negative at {i} → no start up to {i} works; restart at {i + 1}", A("gain = gas − cost", [g - c for g, c in zip(gas, cost)], bad=range(start, i + 1), i=i), V(tank=tank))
            start, tank = i + 1, 0
        else:
            T(f"Station {i}: tank {tank}", A("gain = gas − cost", [g - c for g, c in zip(gas, cost)], ok=range(start, i + 1), i=i), V(start=start, tank=tank))
    return start


# 4 ---------------------------------------------------------------
Q(56, "Merge Intervals", "Medium", "Sort by start",
  "Merge all overlapping intervals.",
  [(([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]), (([[1, 4], [4, 5]],), [[1, 5]])],
  ("Repeatedly look for any two overlapping intervals and merge them until none overlap.", "O(n³)", "O(n)"),
  ("Sort by start; extend the last merged interval while the next starts before it ends, otherwise start a new one.", "O(n log n)", "O(n)"))


@B
def merge_intervals(intervals):
    res = [list(x) for x in intervals]
    merged = True
    while merged:
        merged = False
        for i in range(len(res)):
            for j in range(i + 1, len(res)):
                a, b = res[i], res[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    res[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    res.pop(j)
                    merged = True
                    break
            if merged:
                break
    return sorted(res)


@O
def merge_intervals(intervals):
    intervals.sort()
    out = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
        T(f"Process [{s},{e}]", A("sorted", IV(intervals)), A("merged", IV(out), hl=[len(out) - 1]), at="prev")
    return out


# 5 ---------------------------------------------------------------
Q(57, "Insert Interval", "Medium", "Three phases: before, overlap, after",
  "Insert <code>newInterval</code> into a sorted list of non-overlapping intervals, merging where needed.",
  [(([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]), (([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]])],
  ("Append the new interval, sort everything, and run Merge Intervals.", "O(n log n)", "O(n)"),
  ("One pass: copy intervals ending before it, absorb every interval overlapping it into one, copy the rest.", "O(n)", "O(n)"))


@B
def insert(intervals, new_interval):
    allv = sorted(intervals + [new_interval])
    out = [allv[0]]
    for s, e in allv[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


@O
def insert(intervals, new_interval):
    s, e = new_interval
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:
        out.append(intervals[i])
        i += 1
    T("1) Copy intervals that end before the new one starts", A("intervals", IV(intervals), ok=range(i)), A("out", IV(out)), at="prev")
    while i < n and intervals[i][0] <= e:
        s, e = min(s, intervals[i][0]), max(e, intervals[i][1])
        T(f"2) Absorb [{intervals[i][0]},{intervals[i][1]}] → [{s},{e}]", A("intervals", IV(intervals), hl=[i], i=i), V(merged=[s, e]), at="prev")
        i += 1
    out.append([s, e])
    out += intervals[i:]
    T("3) Add the merged interval and copy the rest", A("out", IV(out), ok=[len(out) - (n - i) - 1]), at="prev")
    return out


# 6 ---------------------------------------------------------------
Q(435, "Non-overlapping Intervals", "Medium", "Sort by end, keep earliest finish",
  "Return the minimum number of intervals to remove so the rest don't overlap (touching ends are fine).",
  [(([[1, 2], [2, 3], [3, 4], [1, 3]],), 1), (([[1, 2], [1, 2], [1, 2]],), 2), (([[1, 2], [2, 3]],), 0)],
  ("Try every subset of intervals to keep and check it's non-overlapping.", "O(n · 2ⁿ)", "O(n)"),
  ("Sort by end time. Keep an interval if it starts at or after the last kept end; otherwise remove it. Finishing earliest leaves the most room.", "O(n log n)", "O(1)"),
  viz=([[1, 4], [2, 3], [3, 5], [4, 6], [5, 9]],))


@B
def erase_overlap_intervals(intervals):
    n, best = len(intervals), 0
    for mask in range(1 << n):
        keep = sorted(intervals[i] for i in range(n) if mask >> i & 1)
        if all(keep[k][1] <= keep[k + 1][0] for k in range(len(keep) - 1)):
            best = max(best, len(keep))
    return n - best


@O
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    end, removed, kept = float("-inf"), 0, []
    for i, (s, e) in enumerate(intervals):
        if s >= end:
            end = e
            kept.append(i)
        else:
            removed += 1
        T(f"[{s},{e}] {'keep' if kept and kept[-1] == i else 'overlaps → remove'}", A("sorted by end", IV(intervals), ok=kept, bad=[j for j in range(i + 1) if j not in kept], i=i), V(removed=removed), at="prev")
    return removed


# 7 ---------------------------------------------------------------
Q(452, "Minimum Number of Arrows to Burst Balloons", "Medium", "Sort by end, shoot at the end",
  "Each balloon spans [x_start, x_end]. An arrow at x bursts every balloon with start ≤ x ≤ end. Return the fewest arrows.",
  [(([[10, 16], [2, 8], [1, 6], [7, 12]],), 2), (([[1, 2], [3, 4], [5, 6], [7, 8]],), 4), (([[1, 2], [2, 3], [3, 4], [4, 5]],), 2)],
  ("Try every subset of candidate arrow positions (the balloon ends) and keep the smallest that hits all.", "O(n · 2ⁿ)", "O(n)"),
  ("Sort by end. Shoot at the first balloon's end; every balloon starting at or before that point is burst. The next unburst balloon needs a new arrow at its end.", "O(n log n)", "O(1)"))


@B
def find_min_arrow_shots(points):
    xs = sorted({e for _, e in points})
    for k in range(1, len(xs) + 1):
        from itertools import combinations
        for shots in combinations(xs, k):
            if all(any(s <= x <= e for x in shots) for s, e in points):
                return k
    return 0


@O
def find_min_arrow_shots(points):
    points.sort(key=lambda p: p[1])
    arrows, x = 0, float("-inf")
    for i, (s, e) in enumerate(points):
        if s > x:
            arrows += 1
            x = e
            T(f"Balloon [{s},{e}] not hit → new arrow at {x}", A("sorted by end", IV(points), hl=[i], i=i), V(arrows=arrows, arrow_at=x), at="prev")
        else:
            T(f"Balloon [{s},{e}] already burst by the arrow at {x}", A("sorted by end", IV(points), ok=[i], i=i), V(arrows=arrows))
    return arrows


# 8 ---------------------------------------------------------------
Q(763, "Partition Labels", "Medium", "Last occurrence",
  "Split <code>s</code> into as many parts as possible so each letter appears in at most one part. Return the part sizes.",
  [(("ababcbacadefegdehijhklij",), [9, 7, 8]), (("eccbbbbdec",), [10])],
  ("For each cut position, check that no letter appears on both sides; cut wherever it's safe.", "O(n²)", "O(σ)"),
  ("Record each letter's last index. Walk s extending the current part's end to the last index of every letter seen; when i reaches the end, cut.", "O(n)", "O(σ)"),
  viz=("abacdcbef",))


@B
def partition_labels(s):
    sizes, start = [], 0
    for i in range(len(s)):
        if not set(s[start:i + 1]) & set(s[i + 1:]):
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


@O
def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}
    sizes, start, end = [], 0, 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])
        T(f"'{ch}' last appears at {last[ch]} → this part ends at least at {end}", A("s", s, hl=range(start, end + 1), start=start, i=i, end=end), A("sizes", sizes), at="prev")
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


# 9 ---------------------------------------------------------------
Q(455, "Assign Cookies", "Easy", "Sort both, smallest that fits",
  "Child i is content with a cookie of size ≥ <code>g[i]</code>. Each child gets at most one cookie. Maximise the content children.",
  [(([1, 2, 3], [1, 1]), 1), (([1, 2], [1, 2, 3]), 2)],
  ("For each child, scan every unused cookie for the smallest that fits.", "O(n · m)", "O(m)"),
  ("Sort children and cookies. Walk the cookies; give the current cookie to the least greedy unfed child if it fits.", "O(n log n + m log m)", "O(1)"),
  viz=([1, 2, 3, 4], [1, 2, 2, 5]))


@B
def find_content_children(g, s):
    used, count = [False] * len(s), 0
    for need in sorted(g):
        best = -1
        for j, size in enumerate(s):
            if not used[j] and size >= need and (best < 0 or size < s[best]):
                best = j
        if best >= 0:
            used[best] = True
            count += 1
    return count


@O
def find_content_children(g, s):
    g.sort()
    s.sort()
    child = 0
    for j, size in enumerate(s):
        if child < len(g) and size >= g[child]:
            child += 1
        T(f"Cookie {size}: children fed so far {child}", A("greed (sorted)", g, ok=range(child), child=child if child < len(g) else None), A("cookies (sorted)", s, hl=[j], j=j), at="prev")
    return child


# 10 --------------------------------------------------------------
Q(860, "Lemonade Change", "Easy", "Give the biggest change first",
  "Lemonade costs 5. Customers pay with 5, 10 or 20 in order. Starting with no money, can you give everyone correct change?",
  [(([5, 5, 5, 10, 20],), True), (([5, 5, 10, 10, 20],), False)],
  ("Try every way to make change from the bills you hold (search).", "O(2ⁿ) worst", "O(n)"),
  ("Count 5s and 10s. For 20, prefer 10 + 5 (keeps more 5s, which are needed for every change) and fall back to 5 + 5 + 5.", "O(n)", "O(1)"))


@B
def lemonade_change(bills):
    def go(i, fives, tens):
        if i == len(bills):
            return True
        b = bills[i]
        if b == 5:
            return go(i + 1, fives + 1, tens)
        if b == 10:
            return fives > 0 and go(i + 1, fives - 1, tens + 1)
        return (tens > 0 and fives > 0 and go(i + 1, fives - 1, tens - 1)) or (fives >= 3 and go(i + 1, fives - 3, tens))
    return go(0, 0, 0)


@O
def lemonade_change(bills):
    fives = tens = 0
    for i, b in enumerate(bills):
        if b == 5:
            fives += 1
        elif b == 10:
            fives, tens = fives - 1, tens + 1
        elif tens:
            fives, tens = fives - 1, tens - 1
        else:
            fives -= 3
        T(f"Customer pays {b}", A("bills", bills, hl=[i], i=i), V(fives=fives, tens=tens), at="prev")
        if fives < 0:
            return False
    return True


# 11 --------------------------------------------------------------
Q(135, "Candy", "Hard", "Two passes",
  "Each child gets ≥ 1 candy, and a child with a higher rating than a neighbour gets more than that neighbour. Return the minimum total.",
  [(([1, 0, 2],), 5), (([1, 2, 2],), 4)],
  ("Start everyone at 1 and keep sweeping, fixing any violated neighbour, until nothing changes.", "O(n²)", "O(n)"),
  ("Left → right: if rating rises, candy = left + 1. Right → left: if rating rises toward the left, candy = max(candy, right + 1). Both rules then hold.", "O(n)", "O(n)"),
  viz=([1, 3, 4, 5, 2, 1],))


@B
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i > 0 and ratings[i] > ratings[i - 1] and c[i] <= c[i - 1]:
                c[i], changed = c[i - 1] + 1, True
            if i < n - 1 and ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
                c[i], changed = c[i + 1] + 1, True
    return sum(c)


@O
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1
    T("Pass 1 (left → right): beat your left neighbour", A("ratings", ratings), A("candy", c, hl=range(n)), at="prev")
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    T(f"Pass 2 (right → left): beat your right neighbour too. Total {sum(c)}", A("ratings", ratings), A("candy", c, ok=range(n)), at="prev")
    return sum(c)


# 12 --------------------------------------------------------------
Q(678, "Valid Parenthesis String", "Medium", "Range of open counts",
  "'*' can be '(' or ')' or empty. Is the string a valid parenthesis string?",
  [(("()",), True), (("(*)",), True), (("(*))",), True), ((")*(",), False)],
  ("Try all three meanings of every '*'.", "O(3ⁿ)", "O(n)"),
  ("Track the range [lo, hi] of possible open-bracket counts. '(' raises both, ')' lowers both, '*' lowers lo and raises hi. If hi &lt; 0 fail; clamp lo at 0; valid if lo == 0 at the end.", "O(n)", "O(1)"),
  viz=("(*))(*",))


@B
def check_valid_string(s):
    def go(i, open_):
        if open_ < 0:
            return False
        if i == len(s):
            return open_ == 0
        if s[i] == "(":
            return go(i + 1, open_ + 1)
        if s[i] == ")":
            return go(i + 1, open_ - 1)
        return go(i + 1, open_ + 1) or go(i + 1, open_ - 1) or go(i + 1, open_)
    return go(0, 0)


@O
def check_valid_string(s):
    lo = hi = 0
    for i, ch in enumerate(s):
        if ch == "(":
            lo, hi = lo + 1, hi + 1
        elif ch == ")":
            lo, hi = lo - 1, hi - 1
        else:
            lo, hi = lo - 1, hi + 1
        T(f"'{ch}': open count could be anywhere in [{max(lo, 0)}, {hi}]", A("s", s, hl=[i], i=i), V(lo=max(lo, 0), hi=hi), at="prev")
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0


# 13 --------------------------------------------------------------
Q(122, "Best Time to Buy and Sell Stock II", "Medium", "Take every rise",
  "You may trade any number of times (hold at most one share). Maximise profit.",
  [(([7, 1, 5, 3, 6, 4],), 7), (([1, 2, 3, 4, 5],), 4), (([7, 6, 4, 3, 1],), 0)],
  ("Recurse on (day, holding) trying buy, sell or wait.", "O(2ⁿ)", "O(n)"),
  ("Any profitable trade is a sum of day-to-day rises, so add every positive difference prices[i] − prices[i − 1].", "O(n)", "O(1)"))


@B
def max_profit_ii(prices):
    def go(i, holding):
        if i == len(prices):
            return 0
        wait = go(i + 1, holding)
        if holding:
            return max(wait, prices[i] + go(i + 1, False))
        return max(wait, -prices[i] + go(i + 1, True))
    return go(0, False)


@O
def max_profit_ii(prices):
    profit = 0
    for i in range(1, len(prices)):
        gain = prices[i] - prices[i - 1]
        if gain > 0:
            profit += gain
        T(f"Day {i - 1} → {i}: change {gain:+d}{' (take it)' if gain > 0 else ''}", A("prices", prices, ok=[i - 1, i] if gain > 0 else [], hl=[] if gain > 0 else [i - 1, i], i=i), V(profit=profit), at="prev")
    return profit


# 14 --------------------------------------------------------------
Q(179, "Largest Number", "Medium", "Custom comparator a+b vs b+a",
  "Arrange non-negative integers to form the largest number; return it as a string.",
  [(([10, 2],), "210"), (([3, 30, 34, 5, 9],), "9534330"), (([0, 0],), "0")],
  ("Try every permutation and keep the largest concatenation.", "O(n! · n)", "O(n)"),
  ("Sort with the rule: a goes before b if a + b &gt; b + a as strings. This order is transitive, and it gives the largest number. Handle all zeros.", "O(n log n · k)", "O(n)"))


@B
def largest_number(nums):
    from itertools import permutations
    best = max("".join(p) for p in permutations(map(str, nums)))
    return "0" if best[0] == "0" else best


@O
def largest_number(nums):
    from functools import cmp_to_key
    strs = [str(x) for x in nums]
    T("Compare pairs by which concatenation is bigger", A("as strings", strs))
    strs.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    T(f"Sorted: {strs}", A("sorted", strs, ok=range(len(strs))), at="prev")
    res = "".join(strs)
    return "0" if res[0] == "0" else res


# 15 --------------------------------------------------------------
Q(406, "Queue Reconstruction by Height", "Medium", "Tallest first, insert at k",
  "Each person is [h, k]: height h with exactly k people in front who are at least as tall. Rebuild the queue.",
  [(([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]],), [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]), (([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]],), [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]])],
  ("Try every ordering and check each person's k.", "O(n! · n²)", "O(n)"),
  ("Sort by height descending, k ascending. Insert each person at index k: everyone already placed is at least as tall, and shorter people added later don't change their counts.", "O(n²)", "O(n)"))


@B
def reconstruct_queue(people):
    from itertools import permutations
    for p in permutations(people):
        if all(sum(1 for j in range(i) if p[j][0] >= h) == k for i, (h, k) in enumerate(p)):
            return [list(x) for x in p]


@O
def reconstruct_queue(people):
    people.sort(key=lambda p: (-p[0], p[1]))
    queue = []
    for h, k in people:
        queue.insert(k, [h, k])
        T(f"Insert [{h},{k}] at index {k}", A("queue", IV(queue), hl=[k]), at="prev")
    return queue


# 16 --------------------------------------------------------------
Q(986, "Interval List Intersections", "Medium", "Two pointers on intervals",
  "Two lists of disjoint, sorted closed intervals. Return their intersection.",
  [(([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]), [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]), (([[1, 3], [5, 9]], []), [])],
  ("Intersect every interval in A with every interval in B.", "O(m · n)", "O(m + n)"),
  ("Two pointers: the overlap of A[i] and B[j] is [max starts, min ends] if non-empty. Then advance whichever interval ends first.", "O(m + n)", "O(1) extra"))


@B
def interval_intersection(first, second):
    res = []
    for a, b in first:
        for c, d in second:
            lo, hi = max(a, c), min(b, d)
            if lo <= hi:
                res.append([lo, hi])
    return sorted(res)


@O
def interval_intersection(first, second):
    i = j = 0
    res = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            res.append([lo, hi])
        T(f"Overlap of {first[i]} and {second[j]}: {'[' + str(lo) + ',' + str(hi) + ']' if lo <= hi else 'none'}", A("A", IV(first), hl=[i], i=i), A("B", IV(second), hl=[j], j=j), A("result", IV(res)), at="prev")
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return res


# 17 --------------------------------------------------------------
Q(1029, "Two City Scheduling", "Medium", "Sort by cost difference",
  "2n people; <code>costs[i] = [toA, toB]</code>. Send exactly n to each city at minimum total cost.",
  [(([[10, 20], [30, 200], [400, 50], [30, 20]],), 110), (([[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]],), 1859)],
  ("Try every way to choose n people for city A.", "O(C(2n, n) · n)", "O(n)"),
  ("Sort by toA − toB. The first n (who save the most by going to A) go to A, the rest to B.", "O(n log n)", "O(1)"))


@B
def two_city_sched_cost(costs):
    from itertools import combinations
    n = len(costs) // 2
    best = float("inf")
    for group in combinations(range(2 * n), n):
        g = set(group)
        best = min(best, sum(costs[i][0] if i in g else costs[i][1] for i in range(2 * n)))
    return best


@O
def two_city_sched_cost(costs):
    costs.sort(key=lambda c: c[0] - c[1])
    n = len(costs) // 2
    total = sum(a for a, _ in costs[:n]) + sum(b for _, b in costs[n:])
    T("Sorted by (toA − toB): first half fly to A, second half to B", A("costs [A, B]", [f"{a},{b}" for a, b in costs], ok=range(n), hl=range(n, 2 * n)), A("toA − toB", [a - b for a, b in costs]), V(total=total))
    return total


# 18 --------------------------------------------------------------
Q(1710, "Maximum Units on a Truck", "Easy", "Best units per box first",
  "<code>boxTypes[i] = [count, unitsPerBox]</code>. The truck holds <code>truckSize</code> boxes. Maximise total units.",
  [(([[1, 3], [2, 2], [3, 1]], 4), 8), (([[5, 10], [2, 5], [4, 7], [3, 9]], 10), 91)],
  ("Load boxes one at a time, each time scanning for the type with the most units left.", "O(truckSize · n)", "O(1)"),
  ("Sort box types by units per box, descending, and take as many of each as fit.", "O(n log n)", "O(1)"))


@B
def maximum_units(box_types, truck_size):
    left = [list(b) for b in box_types]
    total = 0
    for _ in range(truck_size):
        best = max((b for b in left if b[0] > 0), key=lambda b: b[1], default=None)
        if not best:
            break
        best[0] -= 1
        total += best[1]
    return total


@O
def maximum_units(box_types, truck_size):
    box_types.sort(key=lambda b: -b[1])
    total = 0
    for i, (count, units) in enumerate(box_types):
        take = min(count, truck_size)
        total += take * units
        truck_size -= take
        T(f"Take {take} box(es) of {units} units", A("types [count, units] by units", [f"{c},{u}" for c, u in box_types], hl=[i], i=i), V(space_left=truck_size, total=total), at="prev")
        if truck_size == 0:
            break
    return total


# 19 --------------------------------------------------------------
Q(1288, "Remove Covered Intervals", "Medium", "Sort by start asc, end desc",
  "Remove every interval covered by another (c ≤ a and b ≤ d). Return how many remain.",
  [(([[1, 4], [3, 6], [2, 8]],), 2), (([[1, 4], [2, 3]],), 1)],
  ("For each interval, check every other interval to see if it covers it.", "O(n²)", "O(1)"),
  ("Sort by start ascending and, for equal starts, end descending. An interval is covered exactly when its end ≤ the largest end seen so far.", "O(n log n)", "O(1)"))


@B
def remove_covered_intervals(intervals):
    n = len(intervals)
    return sum(1 for i in range(n) if not any(j != i and intervals[j][0] <= intervals[i][0] and intervals[i][1] <= intervals[j][1] for j in range(n)))


@O
def remove_covered_intervals(intervals):
    intervals.sort(key=lambda x: (x[0], -x[1]))
    keep, far, kept = 0, 0, []
    for i, (s, e) in enumerate(intervals):
        if e > far:
            keep += 1
            far = e
            kept.append(i)
        T(f"[{s},{e}] {'kept' if kept and kept[-1] == i else 'covered (end ≤ ' + str(far) + ')'}", A("sorted", IV(intervals), ok=kept, bad=[j for j in range(i + 1) if j not in kept], i=i), V(kept=keep, max_end=far), at="prev")
    return keep


# 20 --------------------------------------------------------------
Q(1094, "Car Pooling", "Medium", "Sweep line over stops",
  "<code>trips[i] = [passengers, from, to]</code>. The car has <code>capacity</code> seats and drives east only. Can it complete all trips?",
  [(([[2, 1, 5], [3, 3, 7]], 4), False), (([[2, 1, 5], [3, 3, 7]], 5), True)],
  ("For every kilometre, add up the passengers of every trip covering it.", "O(n · D)", "O(1)"),
  ("Events: +p at 'from', −p at 'to'. Sort events (drop-offs before pick-ups at the same point) and sweep the running load.", "O(n log n)", "O(n)"),
  viz=([[2, 1, 5], [3, 3, 7], [1, 5, 8]], 6))


@B
def car_pooling(trips, capacity):
    end = max(t for _, _, t in trips)
    for km in range(end):
        if sum(p for p, f, t in trips if f <= km < t) > capacity:
            return False
    return True


@O
def car_pooling(trips, capacity):
    events = sorted([(f, p) for p, f, _ in trips] + [(t, -p) for p, _, t in trips])
    load = 0
    for i, (x, delta) in enumerate(events):
        load += delta
        T(f"At {x}: {'pick up' if delta > 0 else 'drop off'} {abs(delta)} → load {load}", A("events (place, change)", [f"{a}:{b:+d}" for a, b in events], hl=[i], i=i), V(load=load, capacity=capacity), at="prev")
        if load > capacity:
            return False
    return True
