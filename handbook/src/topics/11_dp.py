from lib import *

TOPIC(
    id="dp", title="Dynamic Programming", glyph="dp[i]",
    blurb="Recursion that remembers: define a state, write the recurrence, fill a table in the right order.",
    demo_title="Fibonacci: plain recursion repeats work, a table computes each value once",
    theory="""
<h3>What it is</h3>
<p><b>Dynamic programming</b> is for problems where the answer is built from answers to <b>smaller overlapping sub-problems</b>. Plain recursion solves the same sub-problem again and again (exponential time). DP solves each one <b>once</b> and stores it — either with a cache on the recursion (<b>memoisation</b>, top-down) or by filling a table from the smallest case up (<b>tabulation</b>, bottom-up).</p>
<h3>The four steps</h3>
<ol>
<li><b>State</b> — what does <code>dp[i]</code> (or <code>dp[i][j]</code>) mean, in words? e.g. "fewest coins to make amount i".</li>
<li><b>Recurrence</b> — how does a state follow from smaller ones? e.g. <code>dp[i] = 1 + min(dp[i − c] for c in coins)</code>.</li>
<li><b>Base cases</b> — the smallest states you know directly (<code>dp[0] = 0</code>).</li>
<li><b>Order</b> — fill so every state's dependencies are ready; read the answer.</li>
</ol>
<h3>The common shapes</h3>
<table>
<tr><th>Shape</th><th>State</th><th>Examples</th></tr>
<tr><td>1-D linear</td><td><code>dp[i]</code> = best for the first i items</td><td>climbing stairs, house robber, decode ways</td></tr>
<tr><td>Knapsack / coins</td><td><code>dp[amount]</code> or <code>dp[i][capacity]</code></td><td>coin change, partition subset sum, target sum</td></tr>
<tr><td>Two strings</td><td><code>dp[i][j]</code> = answer for prefixes a[:i], b[:j]</td><td>LCS, edit distance</td></tr>
<tr><td>Grid</td><td><code>dp[r][c]</code> from top and left</td><td>unique paths, min path sum, maximal square</td></tr>
<tr><td>Interval</td><td><code>dp[l][r]</code> over a sub-range, by length</td><td>palindromes, burst balloons</td></tr>
<tr><td>State machine</td><td>a few states per day (hold / sold / rest)</td><td>stock with cooldown</td></tr>
</table>
<h3>Template: top-down then bottom-up</h3>
<pre><code class="py">from functools import cache
@cache
def f(i):                    # top-down: write the recurrence directly
    if i &lt;= 1: return i
    return f(i - 1) + f(i - 2)

dp = [0] * (n + 1)           # bottom-up: same recurrence, explicit order
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i - 1] + dp[i - 2]</code></pre>
<h3>Spot the pattern</h3>
<ul>
<li>"Count the ways", "minimum / maximum cost", "is it possible" with choices at each step.</li>
<li>A greedy choice fails on a small counter-example.</li>
<li>The recursion tree repeats the same arguments.</li>
<li>When <code>dp[i]</code> only needs the last one or two values, keep two variables instead of the array (O(1) space).</li>
</ul>
<h3>Common mistakes</h3>
<ul>
<li>A fuzzy state definition — write it as a sentence first.</li>
<li>Coin change II: the loop order decides <b>combinations</b> (coins outer) vs <b>permutations</b> (amount outer).</li>
<li>0/1 knapsack in 1-D must loop capacity <b>downwards</b> so each item is used once.</li>
</ul>
""")


@D
def fib_demo():
    n = 7
    dp = [0] * (n + 1)
    dp[1] = 1
    T("Base cases dp[0] = 0, dp[1] = 1", A("dp", dp, ok=[0, 1]))
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        T(f"dp[{i}] = dp[{i - 1}] + dp[{i - 2}] = {dp[i - 1]} + {dp[i - 2]} = {dp[i]} (recursion would recompute both)", A("dp", dp, hl=[i - 1, i - 2], ok=[i], i=i), at="prev")
    return dp[n]


# 1 ---------------------------------------------------------------
Q(70, "Climbing Stairs", "Easy", "1-D · Fibonacci",
  "You climb 1 or 2 steps at a time. How many distinct ways reach the top of <code>n</code> steps?",
  [((2,), 2), ((3,), 3), ((5,), 8)],
  ("ways(n) = ways(n − 1) + ways(n − 2) as plain recursion.", "O(2ⁿ)", "O(n)"),
  ("Same recurrence bottom-up; only the last two values are needed.", "O(n)", "O(1)"),
  viz=(6,))


@B
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)


@O
def climb_stairs(n):
    a, b = 1, 1  # ways to reach step i - 1 and step i
    for i in range(2, n + 1):
        a, b = b, a + b
        T(f"ways({i}) = ways({i - 1}) + ways({i - 2}) = {b}", V(step=i, ways_prev=a, ways=b), at="prev")
    return b


# 2 ---------------------------------------------------------------
Q(746, "Min Cost Climbing Stairs", "Easy", "1-D · min of two",
  "<code>cost[i]</code> is paid when you step on stair i. Start at stair 0 or 1, climb 1 or 2 at a time, and return the minimum cost to pass the last stair.",
  [(([10, 15, 20],), 15), (([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],), 6)],
  ("Recursively try both moves from every stair.", "O(2ⁿ)", "O(n)"),
  ("dp[i] = cost to reach stair i = min(dp[i − 1] + cost[i − 1], dp[i − 2] + cost[i − 2]).", "O(n)", "O(n), or O(1) with two variables"),
  viz=([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],))


@B
def min_cost_climbing_stairs(cost):
    def go(i):
        if i >= len(cost):
            return 0
        return cost[i] + min(go(i + 1), go(i + 2))
    return min(go(0), go(1))


@O
def min_cost_climbing_stairs(cost):
    n = len(cost)
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
        T(f"dp[{i}] = min({dp[i - 1]} + {cost[i - 1]}, {dp[i - 2]} + {cost[i - 2]}) = {dp[i]}", A("cost", cost, hl=[i - 1, i - 2]), A("dp", dp, ok=[i], i=i), at="prev")
    return dp[n]


# 3 ---------------------------------------------------------------
Q(198, "House Robber", "Medium", "1-D · take or skip",
  "Adjacent houses can't both be robbed. Return the maximum amount you can rob.",
  [(([1, 2, 3, 1],), 4), (([2, 7, 9, 3, 1],), 12)],
  ("Recursively choose rob-or-skip for every house.", "O(2ⁿ)", "O(n)"),
  ("best(i) = max(best(i − 1), best(i − 2) + nums[i]): skip this house, or rob it plus the best up to two houses back.", "O(n)", "O(1)"))


@B
def rob(nums):
    def go(i):
        if i < 0:
            return 0
        return max(go(i - 1), go(i - 2) + nums[i])
    return go(len(nums) - 1)


@O
def rob(nums):
    prev2 = prev1 = 0
    dp = []
    for i, x in enumerate(nums):
        prev2, prev1 = prev1, max(prev1, prev2 + x)
        dp.append(prev1)
        T(f"House {i}: max(skip = {prev2}, rob = {dp[i - 2] if i >= 2 else 0} + {x}) = {prev1}", A("nums", nums, hl=[i], i=i), A("best so far", dp, ok=[i]), at="prev")
    return prev1


# 4 ---------------------------------------------------------------
Q(213, "House Robber II", "Medium", "Circle → two linear runs",
  "Houses are in a circle, so the first and last are adjacent. Return the maximum you can rob.",
  [(([2, 3, 2],), 3), (([1, 2, 3, 1],), 4), (([1, 2, 3],), 3)],
  ("Recurse with a flag for whether house 0 was robbed.", "O(2ⁿ)", "O(n)"),
  ("You can't take both ends, so answer = max(rob(nums[1:]), rob(nums[:-1])) using the linear House Robber.", "O(n)", "O(1)"))


@B
def rob_circle(nums):
    n = len(nums)
    if n == 1:
        return nums[0]

    def go(i, first_taken):
        if i >= n:
            return 0
        if i == n - 1 and first_taken:
            return 0
        return max(go(i + 1, first_taken), nums[i] + go(i + 2, first_taken or i == 0))
    return go(0, False)


@O
def rob_circle(nums):
    if len(nums) == 1:
        return nums[0]

    def line(arr, label):
        a = b = 0
        for x in arr:
            a, b = b, max(b, a + x)
        T(f"Without the {label}: best = {b}", A("houses considered", arr, ok=range(len(arr))), V(best=b))
        return b

    return max(line(nums[1:], "first house"), line(nums[:-1], "last house"))


# 5 ---------------------------------------------------------------
Q(322, "Coin Change", "Medium", "Unbounded knapsack · min",
  "Return the fewest coins needed to make <code>amount</code>, or −1 if impossible.",
  [(([1, 2, 5], 11), 3), (([2], 3), -1), (([1], 0), 0)],
  ("Recursively try every coin for every remaining amount.", "O(Sⁿ) — exponential", "O(S)"),
  ("dp[a] = fewest coins for amount a = 1 + min(dp[a − c]) over coins c ≤ a; dp[0] = 0.", "O(S · n)", "O(S)"),
  viz=([1, 3, 4], 6))


@B
def coin_change(coins, amount):
    def go(a):
        if a == 0:
            return 0
        best = float("inf")
        for c in coins:
            if c <= a:
                best = min(best, 1 + go(a - c))
        return best
    r = go(amount)
    return -1 if r == float("inf") else r


@O
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
        T(f"dp[{a}] = {dp[a]} coins", A("dp (amount → coins)", dp, ok=[a], hl=[a - c for c in coins if c <= a], a=a), V(coins=coins), at="prev")
    return -1 if dp[amount] == INF else dp[amount]


# 6 ---------------------------------------------------------------
Q(518, "Coin Change II", "Medium", "Count combinations",
  "Return the number of combinations of <code>coins</code> (unlimited each) that make <code>amount</code>.",
  [((5, [1, 2, 5]), 4), ((3, [2]), 0), ((10, [10]), 1)],
  ("Recurse on (coin index, remaining amount): use this coin again or move to the next.", "O(2^(S/min)) — exponential", "O(S)"),
  ("dp[a] = ways to make a. Loop coins on the outside so each combination is counted once in coin order: dp[a] += dp[a − coin].", "O(S · n)", "O(S)"))


@B
def change(amount, coins):
    def go(i, a):
        if a == 0:
            return 1
        if i == len(coins) or a < 0:
            return 0
        return go(i, a - coins[i]) + go(i + 1, a)
    return go(0, amount)


@O
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
        T(f"After allowing coin {c}", A("dp (ways)", dp, ok=range(c, amount + 1)), V(coin=c), at="prev")
    return dp[amount]


# 7 ---------------------------------------------------------------
Q(300, "Longest Increasing Subsequence", "Medium", "Patience sorting · binary search",
  "Return the length of the longest strictly increasing subsequence.",
  [(([10, 9, 2, 5, 3, 7, 101, 18],), 4), (([0, 1, 0, 3, 2, 3],), 4), (([7, 7, 7, 7],), 1)],
  ("Classic DP: dp[i] = 1 + max(dp[j]) over j &lt; i with nums[j] &lt; nums[i].", "O(n²)", "O(n)"),
  ("Keep tails[k] = smallest possible tail of an increasing subsequence of length k + 1. For each x, binary search the first tail ≥ x and replace it (or append).", "O(n log n)", "O(n)"))


@B
def length_of_lis(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


@O
def length_of_lis(nums):
    from bisect import bisect_left
    tails = []
    for i, x in enumerate(nums):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
        T(f"{x} goes to position {k} of tails", A("nums", nums, hl=[i], i=i), A("tails", tails, hl=[k]), V(length=len(tails)), at="prev")
    return len(tails)


# 8 ---------------------------------------------------------------
Q(1143, "Longest Common Subsequence", "Medium", "Two strings · 2-D table",
  "Return the length of the longest subsequence common to <code>text1</code> and <code>text2</code>.",
  [(("abcde", "ace"), 3), (("abc", "abc"), 3), (("abc", "def"), 0)],
  ("Recurse on (i, j): match → 1 + f(i+1, j+1), else max(f(i+1, j), f(i, j+1)).", "O(2^(m+n))", "O(m + n)"),
  ("dp[i][j] = LCS of a[:i] and b[:j]. Equal last letters → dp[i−1][j−1] + 1, else max(dp[i−1][j], dp[i][j−1]).", "O(m · n)", "O(m · n)"))


@B
def longest_common_subsequence(a, b):
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))
    return go(0, 0)


@O
def longest_common_subsequence(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        T(f"Row for '{a[:i]}'", G("dp", dp, hl=[(i, j) for j in range(1, n + 1)], ok=[(i, j) for j in range(1, n + 1) if a[i - 1] == b[j - 1]], rl=[""] + list(a), cl=[""] + list(b)), at="prev")
    return dp[m][n]


# 9 ---------------------------------------------------------------
Q(72, "Edit Distance", "Medium", "Two strings · insert / delete / replace",
  "Return the minimum number of single-character inserts, deletes and replacements to turn <code>word1</code> into <code>word2</code>.",
  [(("horse", "ros"), 3), (("intention", "execution"), 5)],
  ("Recurse on (i, j) trying all three operations whenever letters differ.", "O(3^(m+n))", "O(m + n)"),
  ("dp[i][j] = cost for prefixes. Same letter → dp[i−1][j−1]; else 1 + min(delete dp[i−1][j], insert dp[i][j−1], replace dp[i−1][j−1]).", "O(m · n)", "O(m · n)"),
  viz=("horse", "ros"))


@B
def min_distance(w1, w2):
    def go(i, j):
        if i == len(w1):
            return len(w2) - j
        if j == len(w2):
            return len(w1) - i
        if w1[i] == w2[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j), go(i, j + 1), go(i + 1, j + 1))
    return go(0, 0)


@O
def min_distance(w1, w2):
    m, n = len(w1), len(w2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    T("Base cases: turning a prefix into '' (or back) costs its length", G("dp", dp, ok=[(i, 0) for i in range(m + 1)] + [(0, j) for j in range(n + 1)], rl=[""] + list(w1), cl=[""] + list(w2)))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if w1[i - 1] == w2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        T(f"Row for '{w1[:i]}'", G("dp", dp, hl=[(i, j) for j in range(1, n + 1)], rl=[""] + list(w1), cl=[""] + list(w2)), at="prev")
    return dp[m][n]


# 10 --------------------------------------------------------------
Q(416, "Partition Equal Subset Sum", "Medium", "0/1 knapsack · reachable sums",
  "Can <code>nums</code> be split into two subsets with equal sums?",
  [(([1, 5, 11, 5],), True), (([1, 2, 3, 5],), False)],
  ("Try including or excluding each number (2ⁿ subsets) looking for sum / 2.", "O(2ⁿ)", "O(n)"),
  ("target = sum / 2. dp[s] = can some subset sum to s. For each number loop s downwards so it's used once: dp[s] |= dp[s − x].", "O(n · target)", "O(target)"),
  viz=([1, 5, 11, 5],))


@B
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False

    def go(i, s):
        if s == 0:
            return True
        if i == len(nums) or s < 0:
            return False
        return go(i + 1, s - nums[i]) or go(i + 1, s)
    return go(0, total // 2)


@O
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [True] + [False] * target
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
        T(f"After number {x}: reachable sums", A("dp (sum reachable?)", dp, ok=[s for s in range(target + 1) if dp[s]]), V(target=target), at="prev")
    return dp[target]


# 11 --------------------------------------------------------------
Q(139, "Word Break", "Medium", "1-D over prefixes",
  "Can <code>s</code> be split into a sequence of words from <code>wordDict</code>?",
  [(("leetcode", ["leet", "code"]), True), (("applepenapple", ["apple", "pen"]), True), (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False)],
  ("Recursively try every dictionary word as the next prefix.", "O(2ⁿ)", "O(n)"),
  ("dp[i] = s[:i] can be split. dp[i] is true if some j &lt; i has dp[j] and s[j:i] in the dictionary.", "O(n² · L)", "O(n)"))


@B
def word_break_dp(s, word_dict):
    def go(i):
        if i == len(s):
            return True
        return any(s.startswith(w, i) and go(i + len(w)) for w in word_dict)
    return go(0)


@O
def word_break_dp(s, word_dict):
    words = set(word_dict)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
        T(f"dp[{i}]: can '{s[:i]}' be split? {dp[i]}", A("s", s, hl=range(i)), A("dp", dp, ok=[k for k in range(i + 1) if dp[k]], i=i), at="prev")
    return dp[len(s)]


# 12 --------------------------------------------------------------
Q(62, "Unique Paths", "Medium", "Grid · from top and left",
  "A robot moves only right or down on an m × n grid. Count the paths from top-left to bottom-right.",
  [((3, 7), 28), ((3, 2), 3)],
  ("Recurse: paths(r, c) = paths(r − 1, c) + paths(r, c − 1).", "O(2^(m+n))", "O(m + n)"),
  ("Fill the grid: the first row and column are 1; every other cell is top + left. One row of memory is enough. (Or C(m+n−2, m−1).)", "O(m · n)", "O(n)"),
  viz=(3, 4))


@B
def unique_paths(m, n):
    if m == 1 or n == 1:
        return 1
    return unique_paths(m - 1, n) + unique_paths(m, n - 1)


@O
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
            T(f"dp[{r}][{c}] = top {dp[r - 1][c]} + left {dp[r][c - 1]} = {dp[r][c]}", G("dp", dp, hl=[(r - 1, c), (r, c - 1)], ok=[(r, c)]), at="prev")
    return dp[m - 1][n - 1]


# 13 --------------------------------------------------------------
Q(64, "Minimum Path Sum", "Medium", "Grid · min of top and left",
  "Moving only right or down, find the path from top-left to bottom-right with the smallest sum.",
  [(([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7), (([[1, 2, 3], [4, 5, 6]],), 12)],
  ("Recurse over both moves from every cell.", "O(2^(m+n))", "O(m + n)"),
  ("dp[r][c] = grid[r][c] + min(dp[r − 1][c], dp[r][c − 1]); the first row and column only have one way in.", "O(m · n)", "O(m · n), or O(n)"))


@B
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])

    def go(r, c):
        if r == m - 1 and c == n - 1:
            return grid[r][c]
        best = float("inf")
        if r + 1 < m:
            best = min(best, go(r + 1, c))
        if c + 1 < n:
            best = min(best, go(r, c + 1))
        return grid[r][c] + best
    return go(0, 0)


@O
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0:
                dp[r][c] = grid[0][0]
            elif r == 0:
                dp[r][c] = dp[r][c - 1] + grid[r][c]
            elif c == 0:
                dp[r][c] = dp[r - 1][c] + grid[r][c]
            else:
                dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])
            T(f"dp[{r}][{c}] = {dp[r][c]}", G("grid", grid, hl=[(r, c)]), G("dp", dp, ok=[(r, c)]), at="prev")
    return dp[m - 1][n - 1]


# 14 --------------------------------------------------------------
Q(91, "Decode Ways", "Medium", "1-D · one or two digits",
  "'A' = 1 … 'Z' = 26. Count the ways to decode the digit string <code>s</code>.",
  [(("12",), 2), (("226",), 3), (("06",), 0)],
  ("Recursively take one digit or two digits at every position.", "O(2ⁿ)", "O(n)"),
  ("dp[i] = ways to decode s[:i]. Add dp[i − 1] if s[i − 1] is 1–9, and dp[i − 2] if s[i−2:i] is 10–26.", "O(n)", "O(n), or O(1)"),
  viz=("11106",))


@B
def num_decodings(s):
    def go(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        ways = go(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26:
            ways += go(i + 2)
        return ways
    return go(0)


@O
def num_decodings(s):
    n = len(s)
    dp = [1] + [0] * n
    for i in range(1, n + 1):
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]
        T(f"dp[{i}] for '{s[:i]}' = {dp[i]}", A("s", s, hl=range(max(0, i - 2), i)), A("dp", dp, ok=[i], i=i), at="prev")
    return dp[n]


# 15 --------------------------------------------------------------
Q(5, "Longest Palindromic Substring", "Medium", "Expand around centres",
  "Return the longest palindromic substring of <code>s</code>.",
  [(("babad",), "bab"), (("cbbd",), "bb"), (("a",), "a")],
  ("Check every substring with a reverse comparison.", "O(n³)", "O(1)"),
  ("Every palindrome has a centre — a character or a gap. Expand outward from each of the 2n − 1 centres while the ends match. (The DP table version is O(n²) space.)", "O(n²)", "O(1)"),
  check=lambda a, out: out == out[::-1] and out in a[0] and len(out) == max(len(a[0][i:j]) for i in range(len(a[0])) for j in range(i + 1, len(a[0]) + 1) if a[0][i:j] == a[0][i:j][::-1]),
  viz=("cabbad",))


@B
def longest_palindrome(s):
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            t = s[i:j + 1]
            if t == t[::-1] and len(t) > len(best):
                best = t
    return best


@O
def longest_palindrome(s):
    lo = hi = 0
    for c in range(2 * len(s) - 1):
        l, r = c // 2, (c + 1) // 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l, r = l - 1, r + 1
        if r - l - 1 > hi - lo + 1:
            lo, hi = l + 1, r - 1
        T(f"Centre {'at ' + str(c // 2) if c % 2 == 0 else 'between ' + str(c // 2) + ' and ' + str(c // 2 + 1)}: expands to '{s[l + 1:r]}'", A("s", s, hl=range(l + 1, r), ok=range(lo, hi + 1)), V(best=s[lo:hi + 1]), at="prev")
    return s[lo:hi + 1]


# 16 --------------------------------------------------------------
Q(152, "Maximum Product Subarray", "Medium", "Track max and min",
  "Return the largest product of a contiguous subarray.",
  [(([2, 3, -2, 4],), 6), (([-2, 0, -1],), 0), (([-2, 3, -4],), 24)],
  ("Try every subarray with a running product.", "O(n²)", "O(1)"),
  ("A negative number turns the smallest product into the largest. Keep both the max and min product ending at i: candidates are x, x · max, x · min.", "O(n)", "O(1)"),
  viz=([2, -5, -2, -4, 3],))


@B
def max_product(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best


@O
def max_product(nums):
    hi = lo = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        hi, lo = max(x, x * hi, x * lo), min(x, x * hi, x * lo)
        best = max(best, hi)
        T(f"x = {x}: max ending here {hi}, min ending here {lo}", A("nums", nums, hl=[i], i=i), V(max_here=hi, min_here=lo, best=best), at="prev")
    return best


# 17 --------------------------------------------------------------
Q(494, "Target Sum", "Medium", "Subset-sum count",
  "Put + or − before every number in <code>nums</code>. Count the expressions that equal <code>target</code>.",
  [(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1)],
  ("Try both signs for every number.", "O(2ⁿ)", "O(n)"),
  ("Let P be the numbers with +. Then P − (total − P) = target, so sum(P) = (total + target) / 2. Count subsets with that sum (0/1 knapsack counting, loop sums downward).", "O(n · S)", "O(S)"),
  viz=([1, 2, 1, 3], 1))


@B
def find_target_sum_ways(nums, target):
    def go(i, s):
        if i == len(nums):
            return int(s == target)
        return go(i + 1, s + nums[i]) + go(i + 1, s - nums[i])
    return go(0, 0)


@O
def find_target_sum_ways(nums, target):
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    goal = (total + target) // 2
    dp = [1] + [0] * goal
    for x in nums:
        for s in range(goal, x - 1, -1):
            dp[s] += dp[s - x]
        T(f"After {x}: ways to pick a '+' group summing to each value (need {goal})", A("dp", dp, ok=[goal]), at="prev")
    return dp[goal]


# 18 --------------------------------------------------------------
Q(309, "Best Time to Buy and Sell Stock with Cooldown", "Medium", "State machine DP",
  "Unlimited trades, but after selling you must wait one day before buying again. Maximise profit.",
  [(([1, 2, 3, 0, 2],), 3), (([1],), 0)],
  ("Recurse on (day, holding?) trying buy / sell / wait.", "O(2ⁿ)", "O(n)"),
  ("Three states per day: hold (own a stock), sold (sold today), rest (free to buy). hold = max(hold, rest − p); sold = hold + p; rest = max(rest, sold).", "O(n)", "O(1)"))


@B
def max_profit_cooldown(prices):
    def go(i, holding):
        if i >= len(prices):
            return 0
        wait = go(i + 1, holding)
        if holding:
            return max(wait, prices[i] + go(i + 2, False))
        return max(wait, -prices[i] + go(i + 1, True))
    return go(0, False)


@O
def max_profit_cooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for i, p in enumerate(prices):
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
        T(f"Day {i}, price {p}", A("prices", prices, hl=[i], i=i), V(hold=hold, sold=sold, rest=rest), at="prev")
    return max(sold, rest)


# 19 --------------------------------------------------------------
Q(312, "Burst Balloons", "Hard", "Interval DP · last balloon",
  "Bursting balloon i earns nums[left] · nums[i] · nums[right] with its current neighbours (outside = 1). Maximise the total.",
  [(([3, 1, 5, 8],), 167), (([1, 5],), 10)],
  ("Try every order of bursting balloons.", "O(n!)", "O(n)"),
  ("Think of the LAST balloon k burst inside (l, r): its neighbours are then l and r. dp[l][r] = max over k of dp[l][k] + a[l]·a[k]·a[r] + dp[k][r], filled by increasing interval length.", "O(n³)", "O(n²)"),
  viz=([3, 1, 5],))


@B
def max_coins(nums):
    def go(arr):
        if not arr:
            return 0
        best = 0
        for i in range(len(arr)):
            left = arr[i - 1] if i > 0 else 1
            right = arr[i + 1] if i + 1 < len(arr) else 1
            best = max(best, left * arr[i] * right + go(arr[:i] + arr[i + 1:]))
        return best
    return go(list(nums))


@O
def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r], dp[l][k] + a[l] * a[k] * a[r] + dp[k][r])
        T(f"Intervals of length {length} done", G("dp[l][r]", dp, hl=[(l, l + length) for l in range(n - length)], rl=a, cl=a), at="prev")
    return dp[0][n - 1]


# 20 --------------------------------------------------------------
Q(221, "Maximal Square", "Medium", "Grid · min of three neighbours",
  "In a binary matrix of '0' and '1', return the area of the largest square of 1s.",
  [(([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],), 4), (([["0", "1"], ["1", "0"]],), 1), (([["0"]],), 0)],
  ("For every cell as a top-left corner, grow the square while it stays all 1s.", "O((m·n)²)", "O(1)"),
  ("dp[r][c] = side of the largest square whose bottom-right corner is (r, c) = 1 + min(top, left, top-left) when the cell is '1'.", "O(m · n)", "O(m · n), or O(n)"))


@B
def maximal_square(matrix):
    m, n, best = len(matrix), len(matrix[0]), 0
    for r in range(m):
        for c in range(n):
            k = 0
            while r + k < m and c + k < n and all(matrix[r + i][c + j] == "1" for i in range(k + 1) for j in range(k + 1)):
                k += 1
            best = max(best, k)
    return best * best


@O
def maximal_square(matrix):
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if matrix[r - 1][c - 1] == "1":
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
                best = max(best, dp[r][c])
        T(f"Row {r - 1} done; largest side so far {best}", G("matrix", matrix, hl=[(r - 1, c) for c in range(n)]), G("dp (side ending here)", [row[1:] for row in dp[1:]], ok=[(i, j) for i in range(m) for j in range(n) if dp[i + 1][j + 1] == best and best]), at="prev")
    return best * best
