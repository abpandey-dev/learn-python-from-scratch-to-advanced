from lib import *

LESSON("Basics", "Why plain recursion is slow", """
<p>Fibonacci: <code>fib(n) = fib(n − 1) + fib(n − 2)</code>. Written as plain recursion, <code>fib(5)</code> calls <code>fib(3)</code> twice, <code>fib(2)</code> three times, and so on. The number of calls roughly doubles with n — <b>O(2ⁿ)</b>. <code>fib(50)</code> would take hours.</p>
<div class="pic">               fib(5)
          /            \\
      fib(4)          fib(3)      ← fib(3) computed again
     /     \\          /    \\
  fib(3)  fib(2)   fib(2) fib(1)</div>
<p>The same small questions are asked again and again — <b>overlapping sub-problems</b>. That's the signal for dynamic programming.</p>
""")


@LD
def calls_lesson():
    calls = {}

    def fib(n):
        calls[n] = calls.get(n, 0) + 1
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(6)
    T(f"Plain recursion for fib(6) made {sum(calls.values())} calls — look how often small n repeat", M("times each fib(n) was computed", dict(sorted(calls.items()))))
    memo, mcalls = {}, {}

    def fib_memo(n):
        mcalls[n] = mcalls.get(n, 0) + 1
        if n <= 1:
            return n
        if n not in memo:
            memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
        return memo[n]

    fib_memo(6)
    T(f"With a memo dict: {sum(mcalls.values())} calls; every value is computed once", M("times each fib(n) was computed", dict(sorted(mcalls.items()))), M("memo", dict(sorted(memo.items()))))
    return fib_memo(6)


LESSON("Basics", "Two ways to do DP", """
<p><b>Dynamic programming</b> = solve each sub-problem once and store the answer.</p>
<table>
<tr><th></th><th>Top-down (memoisation)</th><th>Bottom-up (tabulation)</th></tr>
<tr><td>How</td><td>write the recursion, add a cache</td><td>fill a table from the smallest case up</td></tr>
<tr><td>Python</td><td><code>@functools.cache</code></td><td><code>dp = [0] * (n + 1)</code> and a loop</td></tr>
<tr><td>Pros</td><td>easy to write from the recurrence; only visits needed states</td><td>no recursion limit; easy to save memory</td></tr>
</table>
<h4>The four questions for every DP</h4>
<ol>
<li><b>State</b>: what does <code>dp[i]</code> mean? Write it as a sentence.</li>
<li><b>Transition</b>: how is <code>dp[i]</code> built from smaller states?</li>
<li><b>Base cases</b>: the smallest states you know directly.</li>
<li><b>Answer &amp; order</b>: which cell is the answer, and in what order to fill so dependencies are ready.</li>
</ol>
<p>Climbing stairs: state = ways to reach step i; transition = <code>dp[i − 1] + dp[i − 2]</code>; base <code>dp[0] = dp[1] = 1</code>; answer <code>dp[n]</code>.</p>
""", practice=[70, 746])


LESSON("Core", "1-D DP: take it or skip it", """
<p>A huge family of problems walks a sequence and, at each element, makes a choice.</p>
<ul>
<li><b>House robber</b>: <code>dp[i] = max(dp[i − 1], dp[i − 2] + nums[i])</code> — skip this house, or rob it and the best from two back.</li>
<li><b>Decode ways</b>: <code>dp[i] = dp[i − 1]</code> (one digit) <code>+ dp[i − 2]</code> (two digits, if 10–26).</li>
<li><b>Word break</b>: <code>dp[i]</code> is true if some <code>dp[j]</code> is true and <code>s[j:i]</code> is a word.</li>
<li><b>Circular houses</b>: run the line version twice — without the first house and without the last.</li>
</ul>
<div class="tip">If <code>dp[i]</code> only uses the last one or two values, keep two variables instead of a list — O(1) memory.</div>
""", practice=[198, 213, 91, 139])


@LD
def robber_lesson():
    nums = [2, 7, 9, 3, 1]
    dp = [0] * len(nums)
    for i, x in enumerate(nums):
        skip = dp[i - 1] if i >= 1 else 0
        take = (dp[i - 2] if i >= 2 else 0) + x
        dp[i] = max(skip, take)
        T(f"House {i}: skip → {skip}, rob → {take}; best {dp[i]}", A("nums", nums, hl=[i], i=i), A("dp (best up to i)", dp, ok=[i], hl=[i - 1, i - 2] if i >= 2 else [])  , at="prev")
    return dp[-1]


LESSON("Core", "Knapsack: choosing items under a limit", """
<p><b>0/1 knapsack</b>: each item can be used <b>once</b>. State <code>dp[c]</code> = best (or "possible?", or "number of ways") using capacity c. For each item, loop capacity <b>downwards</b> so the item isn't used twice in the same round:</p>
<pre><code class="py">for x in items:
    for c in range(cap, x - 1, -1):
        dp[c] = dp[c] or dp[c - x]       # partition equal subset sum</code></pre>
<p><b>Unbounded knapsack</b>: items reusable (coins). Loop capacity <b>upwards</b>.</p>
<pre><code class="py">dp = [0] + [inf] * amount
for a in range(1, amount + 1):
    for c in coins:
        if c &lt;= a: dp[a] = min(dp[a], dp[a - c] + 1)   # coin change</code></pre>
<p>Counting <b>combinations</b> (coin change II): coins in the outer loop. Coins in the inner loop would count orderings (permutations) instead.</p>
<p>Target sum turns into knapsack with algebra: the "+" group must sum to <code>(total + target) / 2</code>.</p>
""", practice=[416, 494, 322, 518])


@LD
def knapsack_lesson():
    nums = [1, 5, 11, 5]
    target = sum(nums) // 2
    dp = [True] + [False] * target
    T(f"dp[s] = can some subset sum to s? Only s = 0 at first. Target {target}", A("dp", dp, ok=[0]))
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
        T(f"After number {x} (looping s downwards so {x} is used once)", A("dp", dp, ok=[s for s in range(target + 1) if dp[s]]), at="prev")
    return dp[target]


LESSON("Core", "Grid DP", """
<p>On a grid where you move only right or down, cell <code>(r, c)</code> is reached from the top or the left:</p>
<ul>
<li><b>Unique paths</b>: <code>dp[r][c] = dp[r − 1][c] + dp[r][c − 1]</code>.</li>
<li><b>Minimum path sum</b>: <code>dp[r][c] = grid[r][c] + min(top, left)</code>.</li>
<li><b>Maximal square</b>: largest square ending at (r, c) = <code>1 + min(top, left, top-left)</code> when the cell is 1.</li>
</ul>
<p>The first row and first column have only one way in — fill them as base cases. Since each row only needs the row above, one 1-D array is enough.</p>
""", practice=[62, 64, 221])


LESSON("Core", "Two-string DP", """
<p>For two strings <code>a</code> and <code>b</code>, use <code>dp[i][j]</code> = answer for the prefixes <code>a[:i]</code> and <code>b[:j]</code>. Look at the last characters:</p>
<ul>
<li><b>Longest common subsequence</b>: equal → <code>dp[i−1][j−1] + 1</code>; else <code>max(dp[i−1][j], dp[i][j−1])</code>.</li>
<li><b>Edit distance</b>: equal → <code>dp[i−1][j−1]</code>; else <code>1 + min(delete, insert, replace)</code> = <code>1 + min(dp[i−1][j], dp[i][j−1], dp[i−1][j−1])</code>.</li>
</ul>
<p>Row 0 and column 0 represent an empty prefix and are the base cases. O(m · n) time; the table can shrink to two rows.</p>
""", practice=[1143, 72])


@LD
def lcs_lesson():
    a, b = "ace", "abcde"
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                T(f"'{a[i - 1]}' = '{b[j - 1]}' → diagonal + 1 = {dp[i][j]}", G("dp", dp, ok=[(i, j)], hl=[(i - 1, j - 1)], rl=[""] + list(a), cl=[""] + list(b)), at="prev")
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    T(f"LCS length = {dp[m][n]}", G("dp", dp, ok=[(m, n)], rl=[""] + list(a), cl=[""] + list(b)))
    return dp[m][n]


LESSON("Advanced", "Harder DP shapes", """
<h4>Longest increasing subsequence</h4>
<p>O(n²): <code>dp[i] = 1 + max(dp[j])</code> over earlier smaller values. O(n log n): keep <code>tails[k]</code> = smallest tail of an increasing subsequence of length k + 1, and binary search where each new number goes.</p>
<h4>State machines</h4>
<p>When each day can be in a few modes (holding a stock, just sold, resting), keep one variable per mode and write how each mode is reached from yesterday's modes.</p>
<h4>Max and min together</h4>
<p>Maximum product subarray: a negative number flips the biggest into the smallest, so track both.</p>
<h4>Interval DP</h4>
<p><code>dp[l][r]</code> for a range, filled by increasing length. Burst balloons: choose the balloon burst <b>last</b> inside (l, r) — then its neighbours are fixed as l and r. Palindromes: expand from centres, or <code>dp[l][r] = s[l] == s[r] and dp[l+1][r−1]</code>.</p>
<div class="tip">Stuck on the state? Write the brute-force recursion first. Whatever its arguments are, that's your DP state.</div>
""", practice=[300, 309, 152, 312, 5])
