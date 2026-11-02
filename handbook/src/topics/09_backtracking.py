from lib import *

TOPIC(
    id="backtracking", title="Recursion & Backtracking", glyph="choose·undo",
    blurb="Build answers one choice at a time, undo the choice, try the next — with pruning to skip dead branches.",
    demo_title="The decision tree of subsets: include or skip each element",
    theory="""
<h3>What it is</h3>
<p><b>Recursion</b> solves a problem by solving smaller copies of it. <b>Backtracking</b> is recursion over a <b>decision tree</b>: at each level you make one choice (pick this number, place a queen here), recurse to make the rest, then <b>undo</b> the choice and try the next one. Every leaf is a complete candidate.</p>
<h3>The three questions</h3>
<ol>
<li><b>What is the state?</b> Usually a <code>path</code> of choices so far and an index of where to choose next.</li>
<li><b>What are the choices at this state?</b> Remaining numbers, letters for a digit, cells next to you…</li>
<li><b>When is it done / dead?</b> Base case records the answer; <b>pruning</b> stops early when the path can't work (sum too big, invalid queen, not enough elements left).</li>
</ol>
<h3>Template</h3>
<pre><code class="py">res = []
def backtrack(start, path):
    if is_complete(path):
        res.append(path[:])          # copy!
        return
    for i in range(start, len(choices)):
        if not valid(choices[i], path):
            continue                 # prune
        path.append(choices[i])      # choose
        backtrack(i + 1, path)       # explore
        path.pop()                   # un-choose
backtrack(0, [])</code></pre>
<h3>Variations you must know</h3>
<table>
<tr><th>Problem type</th><th>Next call</th><th>Duplicates in input?</th></tr>
<tr><td>Subsets / combinations (each item once)</td><td><code>backtrack(i + 1)</code></td><td>sort, then skip <code>i &gt; start and a[i] == a[i−1]</code></td></tr>
<tr><td>Combination sum (reuse allowed)</td><td><code>backtrack(i)</code></td><td>—</td></tr>
<tr><td>Permutations</td><td>loop over all i with a <code>used[]</code> array</td><td>sort, skip if <code>a[i] == a[i−1]</code> and <code>not used[i−1]</code></td></tr>
<tr><td>Grid search (word search)</td><td>4 neighbours, mark visited, unmark on return</td><td>—</td></tr>
</table>
<h3>Complexity</h3>
<p>Backtracking is exponential by nature: subsets O(n·2ⁿ), permutations O(n·n!), N-Queens about O(n!). The win over brute force is <b>pruning</b>, which cuts whole subtrees and makes it fast in practice.</p>
<h3>Common mistakes</h3>
<ul>
<li>Appending <code>path</code> instead of <code>path[:]</code> — every stored answer becomes the same (later emptied) list.</li>
<li>Forgetting to undo (pop / unmark) after the recursive call.</li>
<li>Skipping duplicates with the wrong condition, which drops valid answers.</li>
</ul>
""")

SORT2 = lambda r: sorted(sorted(x) for x in r)


@D
def subsets_demo():
    nums = [1, 2, 3]
    res, path = [], []

    def go(i):
        if i == len(nums):
            res.append(path[:])
            T(f"Leaf → record {path}", A("nums", nums), A("path", path, ok=range(len(path))), V(subsets=res), at="prev")
            return
        path.append(nums[i])
        T(f"Include {nums[i]}", A("nums", nums, hl=[i], i=i), A("path", path, hl=[len(path) - 1]), at="prev")
        go(i + 1)
        path.pop()
        T(f"Undo, now skip {nums[i]}", A("nums", nums, i=i), A("path", path), at="prev")
        go(i + 1)

    go(0)
    return res


# 1 ---------------------------------------------------------------
Q(78, "Subsets", "Medium", "Include / skip",
  "Return all subsets (the power set) of distinct integers <code>nums</code>.",
  [(([1, 2, 3],), [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]), (([0],), [[], [0]])],
  ("Count a bitmask from 0 to 2ⁿ − 1; bit i set means nums[i] is in the subset.", "O(n · 2ⁿ)", "O(n · 2ⁿ)"),
  ("Backtracking with a start index: every node of the tree is a subset, so record the path on entry, then extend it with each later element.", "O(n · 2ⁿ)", "O(n) + output"),
  norm=SORT2)


@B
def subsets(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


@O
def subsets(nums):
    res, path = [], []

    def go(start):
        res.append(path[:])
        T(f"Record {path}", A("nums", nums, hl=range(start, len(nums))), A("path", path), V(count=len(res)), at="prev")
        for i in range(start, len(nums)):
            path.append(nums[i])
            go(i + 1)
            path.pop()

    go(0)
    return res


# 2 ---------------------------------------------------------------
Q(90, "Subsets II", "Medium", "Sort + skip duplicates",
  "<code>nums</code> may contain duplicates. Return all distinct subsets.",
  [(([1, 2, 2],), [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), (([0],), [[], [0]])],
  ("Generate all 2ⁿ subsets, sort each, and deduplicate with a set.", "O(n · 2ⁿ log n)", "O(n · 2ⁿ)"),
  ("Sort first. At the same tree level, skip nums[i] if it equals nums[i − 1] — choosing either copy leads to identical subsets.", "O(n · 2ⁿ)", "O(n)"),
  norm=SORT2)


@B
def subsets_with_dup(nums):
    n, seen = len(nums), set()
    for mask in range(1 << n):
        seen.add(tuple(sorted(nums[i] for i in range(n) if mask >> i & 1)))
    return [list(t) for t in seen]


@O
def subsets_with_dup(nums):
    nums.sort()
    res, path = [], []

    def go(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                T(f"Skip the second {nums[i]} at this level (duplicate branch)", A("nums", nums, bad=[i], i=i), A("path", path))
                continue
            path.append(nums[i])
            T(f"Take {nums[i]} → {path}", A("nums", nums, hl=[i], i=i), A("path", path), at="prev")
            go(i + 1)
            path.pop()

    go(0)
    return res


# 3 ---------------------------------------------------------------
Q(46, "Permutations", "Medium", "used[] array",
  "Return all permutations of distinct integers <code>nums</code>.",
  [(([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), (([0, 1],), [[0, 1], [1, 0]]), (([1],), [[1]])],
  ("Generate all nⁿ sequences of picks and keep those with no repeated index.", "O(n · nⁿ)", "O(n)"),
  ("At each position try every unused element, mark it used, recurse, unmark.", "O(n · n!)", "O(n)"),
  norm=sorted)


@B
def permute(nums):
    from itertools import product
    n = len(nums)
    return [[nums[i] for i in p] for p in product(range(n), repeat=n) if len(set(p)) == n]


@O
def permute(nums):
    res, path, used = [], [], [False] * len(nums)

    def go():
        if len(path) == len(nums):
            res.append(path[:])
            T(f"Full permutation {path}", A("nums", nums, ok=[i for i, u in enumerate(used) if u]), A("path", path, ok=range(len(path))), V(count=len(res)), at="prev")
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            go()
            path.pop()
            used[i] = False

    go()
    return res


# 4 ---------------------------------------------------------------
Q(47, "Permutations II", "Medium", "Sort + skip used duplicates",
  "<code>nums</code> may contain duplicates. Return all distinct permutations.",
  [(([1, 1, 2],), [[1, 1, 2], [1, 2, 1], [2, 1, 1]]), (([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])],
  ("Generate every permutation and deduplicate with a set.", "O(n · n!)", "O(n · n!)"),
  ("Sort, then at each position skip nums[i] when it equals nums[i − 1] and nums[i − 1] is not currently used — that forces equal values to be placed in order.", "O(n · n!)", "O(n)"),
  norm=sorted)


@B
def permute_unique(nums):
    out = set()

    def go(path, rest):
        if not rest:
            out.add(tuple(path))
        for i in range(len(rest)):
            go(path + [rest[i]], rest[:i] + rest[i + 1:])
    go([], nums)
    return [list(p) for p in out]


@O
def permute_unique(nums):
    nums.sort()
    res, path, used = [], [], [False] * len(nums)

    def go():
        if len(path) == len(nums):
            res.append(path[:])
            T(f"Found {path}", A("nums", nums, ok=[i for i, u in enumerate(used) if u]), A("path", path), V(count=len(res)), at="prev")
            return
        for i in range(len(nums)):
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            path.append(nums[i])
            go()
            path.pop()
            used[i] = False

    go()
    return res


# 5 ---------------------------------------------------------------
Q(39, "Combination Sum", "Medium", "Reuse allowed · prune by sum",
  "Return all unique combinations of <code>candidates</code> (distinct, each reusable) that sum to <code>target</code>.",
  [(([2, 3, 6, 7], 7), [[2, 2, 3], [7]]), (([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), (([2], 1), [])],
  ("Build every ordered sequence that doesn't exceed target, then sort each and deduplicate.", "O(n^(t/min))", "O(t/min)"),
  ("Sort; recurse with start index i (not i + 1) so a number can repeat but order never goes backwards. Stop the loop once a candidate exceeds the remaining sum.", "O(n^(t/min)) worst, heavily pruned", "O(t/min)"),
  norm=SORT2)


@B
def combination_sum(candidates, target):
    found = set()

    def go(path, total):
        if total == target:
            found.add(tuple(sorted(path)))
            return
        for c in candidates:
            if total + c <= target:
                go(path + [c], total + c)
    go([], 0)
    return [list(t) for t in found]


@O
def combination_sum(candidates, target):
    candidates.sort()
    res, path = [], []

    def go(start, remain):
        if remain == 0:
            res.append(path[:])
            T(f"Sum hit {target}: {path}", A("candidates", candidates), A("path", path, ok=range(len(path))), V(result=res))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                T(f"{candidates[i]} > remaining {remain} → prune the rest", A("candidates", candidates, bad=range(i, len(candidates)), i=i), A("path", path))
                break
            path.append(candidates[i])
            go(i, remain - candidates[i])
            path.pop()

    go(0, target)
    return res


# 6 ---------------------------------------------------------------
Q(40, "Combination Sum II", "Medium", "Each once · skip duplicates",
  "Each candidate may be used once and the input may contain duplicates. Return unique combinations summing to <code>target</code>.",
  [(([10, 1, 2, 7, 6, 1, 5], 8), [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]), (([2, 5, 2, 1, 2], 5), [[1, 2, 2], [5]])],
  ("Try all 2ⁿ subsets, keep those that hit target, deduplicate sorted tuples.", "O(n · 2ⁿ)", "O(n · 2ⁿ)"),
  ("Sort; move to i + 1 after using candidates[i]; skip equal values at the same level; break when a value exceeds the remaining sum.", "O(2ⁿ) worst, pruned", "O(n)"),
  norm=SORT2, viz=([2, 1, 2, 3, 1], 4))


@B
def combination_sum2(candidates, target):
    n, found = len(candidates), set()
    for mask in range(1 << n):
        pick = [candidates[i] for i in range(n) if mask >> i & 1]
        if sum(pick) == target:
            found.add(tuple(sorted(pick)))
    return [list(t) for t in found]


@O
def combination_sum2(candidates, target):
    candidates.sort()
    res, path = [], []

    def go(start, remain):
        if remain == 0:
            res.append(path[:])
            T(f"Found {path}", A("candidates", candidates), A("path", path, ok=range(len(path))), V(result=res))
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            T(f"Take {candidates[i]}, remaining {remain - candidates[i]}", A("candidates", candidates, hl=[i], i=i), A("path", path), at="prev")
            go(i + 1, remain - candidates[i])
            path.pop()

    go(0, target)
    return res


# 7 ---------------------------------------------------------------
Q(77, "Combinations", "Medium", "Choose k · prune by count",
  "Return all combinations of <code>k</code> numbers chosen from 1..n.",
  [((4, 2), [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]), ((1, 1), [[1]])],
  ("Check all 2ⁿ bitmasks and keep those with exactly k bits.", "O(n · 2ⁿ)", "O(k)"),
  ("Backtrack from 'start'. Prune when there aren't enough numbers left: loop only up to n − (k − len(path)) + 1.", "O(k · C(n, k))", "O(k)"),
  norm=SORT2, viz=(5, 3))


@B
def combine(n, k):
    return [[i + 1 for i in range(n) if m >> i & 1] for m in range(1 << n) if bin(m).count("1") == k]


@O
def combine(n, k):
    res, path = [], []

    def go(start):
        if len(path) == k:
            res.append(path[:])
            T(f"Pick {path}", A("path", path, ok=range(k)), V(count=len(res)))
            return
        need = k - len(path)
        for x in range(start, n - need + 2):
            path.append(x)
            go(x + 1)
            path.pop()

    go(1)
    return res


# 8 ---------------------------------------------------------------
Q(17, "Letter Combinations of a Phone Number", "Medium", "One level per digit",
  "Given digits 2–9, return all letter combinations they could represent on a phone keypad.",
  [(("23",), ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]), (("",), []), (("2",), ["a", "b", "c"])],
  ("Cartesian product of the letter groups with itertools.product.", "O(4ⁿ · n)", "O(4ⁿ · n)"),
  ("Backtracking: level i chooses one letter for digits[i]; at depth n record the string.", "O(4ⁿ · n)", "O(n)"),
  norm=sorted)



@B
def letter_combinations(digits):
    PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    from itertools import product
    if not digits:
        return []
    return ["".join(p) for p in product(*(PHONE[d] for d in digits))]


@O
def letter_combinations(digits):
    PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    if not digits:
        return []
    res, path = [], []

    def go(i):
        if i == len(digits):
            res.append("".join(path))
            T(f"Record '{res[-1]}'", A("digits", digits), A("path", path, ok=range(len(path))), V(count=len(res)))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            go(i + 1)
            path.pop()

    go(0)
    return res


# 9 ---------------------------------------------------------------
Q(22, "Generate Parentheses", "Medium", "Open / close counts",
  "Return all well-formed strings of <code>n</code> pairs of parentheses.",
  [((3,), ["((()))", "(()())", "(())()", "()(())", "()()()"]), ((1,), ["()"])],
  ("Generate all 2²ⁿ strings of '(' and ')' and keep the balanced ones.", "O(n · 2²ⁿ)", "O(n)"),
  ("Add '(' while open &lt; n; add ')' only while close &lt; open. Every branch stays valid, so nothing is generated and thrown away.", "O(4ⁿ / √n) — the Catalan number", "O(n)"),
  norm=sorted, viz=(2,))


@B
def generate_parenthesis(n):
    from itertools import product

    def ok(s):
        bal = 0
        for c in s:
            bal += 1 if c == "(" else -1
            if bal < 0:
                return False
        return bal == 0
    return ["".join(p) for p in product("()", repeat=2 * n) if ok(p)]


@O
def generate_parenthesis(n):
    res, path = [], []

    def go(open_, close):
        if len(path) == 2 * n:
            res.append("".join(path))
            T(f"Complete: {res[-1]}", A("path", path, ok=range(2 * n)), V(result=res))
            return
        if open_ < n:
            path.append("(")
            T(f"Add '(' (open {open_ + 1})", A("path", path, hl=[len(path) - 1]), V(open=open_ + 1, close=close), at="prev")
            go(open_ + 1, close)
            path.pop()
        if close < open_:
            path.append(")")
            T(f"Add ')' (close {close + 1})", A("path", path, hl=[len(path) - 1]), V(open=open_, close=close + 1), at="prev")
            go(open_, close + 1)
            path.pop()

    go(0, 0)
    return res


# 10 --------------------------------------------------------------
Q(131, "Palindrome Partitioning", "Medium", "Cut where the prefix is a palindrome",
  "Split <code>s</code> so every piece is a palindrome. Return all such partitions.",
  [(("aab",), [["a", "a", "b"], ["aa", "b"]]), (("a",), [["a"]])],
  ("Try all 2ⁿ⁻¹ ways to place cuts and keep those whose pieces are all palindromes.", "O(n · 2ⁿ)", "O(n)"),
  ("From index i, try every end j where s[i..j] is a palindrome (precomputed in a DP table), and recurse from j + 1.", "O(n · 2ⁿ)", "O(n²) table"),
  norm=sorted, viz=("aabb",))


@B
def partition_pal(s):
    n, res = len(s), []
    for mask in range(1 << max(0, n - 1)):
        parts, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(s[start:i + 1])
                start = i + 1
        parts.append(s[start:])
        if all(p == p[::-1] for p in parts):
            res.append(parts)
    return res


@O
def partition_pal(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    res, path = [], []

    def go(i):
        if i == n:
            res.append(path[:])
            T(f"Partition {path}", A("s", s), A("pieces", path, ok=range(len(path))), V(count=len(res)))
            return
        for j in range(i, n):
            if pal[i][j]:
                path.append(s[i:j + 1])
                T(f"'{s[i:j + 1]}' is a palindrome → cut after index {j}", A("s", s, hl=range(i, j + 1), i=i, j=j), A("pieces", path), at="prev")
                go(j + 1)
                path.pop()

    go(0)
    return res


# 11 --------------------------------------------------------------
Q(79, "Word Search", "Medium", "Grid DFS · mark and unmark",
  "Can <code>word</code> be traced in the grid through horizontally or vertically adjacent cells, using each cell at most once?",
  [(([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"), True),
   (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"), True),
   (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"), False)],
  ("DFS from every cell, passing a fresh copy of the visited set on each step.", "O(m · n · 4ᴸ · L)", "O(L²)"),
  ("DFS from each cell that matches word[0]. Mark the cell in place while it's on the path, restore it on return. Quick prune: if the board lacks enough of some letter, return False up front.", "O(m · n · 3ᴸ)", "O(L)"),
  viz=([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"))


@B
def exist(board, word):
    m, n = len(board), len(board[0])

    def dfs(r, c, i, seen):
        if i == len(word):
            return True
        if not (0 <= r < m and 0 <= c < n) or (r, c) in seen or board[r][c] != word[i]:
            return False
        seen = seen | {(r, c)}
        return any(dfs(r + dr, c + dc, i + 1, seen) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return any(dfs(r, c, 0, set()) for r in range(m) for c in range(n))


@O
def exist(board, word):
    from collections import Counter
    m, n = len(board), len(board[0])
    have = Counter(ch for row in board for ch in row)
    if any(have[ch] < cnt for ch, cnt in Counter(word).items()):
        return False
    path = []

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
            return False
        board[r][c] = "#"
        path.append((r, c))
        T(f"Matched '{word[i]}' at ({r},{c})", G("board", board, ok=path), V(word=word, matched=word[:i + 1]), at="prev")
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = word[i]
        path.pop()
        return found

    return any(dfs(r, c, 0) for r in range(m) for c in range(n))


# 12 --------------------------------------------------------------
Q(51, "N-Queens", "Hard", "Row by row with column / diagonal sets",
  "Place <code>n</code> queens on an n × n board so none attack each other. Return every board.",
  [((4,), [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]), ((1,), [["Q"]])],
  ("Try every permutation of columns (one queen per row and column) and check the diagonals.", "O(n! · n)", "O(n)"),
  ("Place one queen per row. Keep sets of used columns, r − c diagonals and r + c anti-diagonals so each safety check is O(1), and backtrack on conflict.", "O(n!) with heavy pruning", "O(n)"),
  norm=sorted)


@B
def solve_n_queens(n):
    from itertools import permutations
    res = []
    for cols in permutations(range(n)):
        if len({r - c for r, c in enumerate(cols)}) == n and len({r + c for r, c in enumerate(cols)}) == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
    return res


@O
def solve_n_queens(n):
    res, cols = [], []
    used_c, diag, anti = set(), set(), set()

    def board():
        return [["Q" if cols[r] == c else "." for c in range(n)] if r < len(cols) else ["."] * n for r in range(n)]

    def go(r):
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            T(f"Solution #{len(res)}", G("board", board(), ok=[(i, c) for i, c in enumerate(cols)]))
            return
        for c in range(n):
            if c in used_c or r - c in diag or r + c in anti:
                continue
            cols.append(c)
            used_c.add(c); diag.add(r - c); anti.add(r + c)
            T(f"Queen at row {r}, column {c}", G("board", board(), hl=[(r, c)], ok=[(i, cc) for i, cc in enumerate(cols[:-1])]), at="prev")
            go(r + 1)
            cols.pop()
            used_c.remove(c); diag.remove(r - c); anti.remove(r + c)

    go(0)
    return res


# 13 --------------------------------------------------------------
Q(37, "Sudoku Solver", "Hard", "Constraint sets + most-constrained cell",
  "Fill the empty cells ('.') so every row, column and 3 × 3 box contains 1–9 exactly once. Modify the board in place.",
  [(([["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."], [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"], ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"], [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"], [".", ".", ".", ".", "8", ".", ".", "7", "9"]],),
    [["5", "3", "4", "6", "7", "8", "9", "1", "2"], ["6", "7", "2", "1", "9", "5", "3", "4", "8"], ["1", "9", "8", "3", "4", "2", "5", "6", "7"], ["8", "5", "9", "7", "6", "1", "4", "2", "3"], ["4", "2", "6", "8", "5", "3", "7", "9", "1"], ["7", "1", "3", "9", "2", "4", "8", "5", "6"], ["9", "6", "1", "5", "3", "7", "2", "8", "4"], ["2", "8", "7", "4", "1", "9", "6", "3", "5"], ["3", "4", "5", "2", "8", "6", "1", "7", "9"]])],
  ("Fill cells left to right, trying 1–9 and re-scanning the row, column and box to check each digit.", "O(9ᵐ · 27)", "O(m)"),
  ("Keep sets of digits used per row, column and box (O(1) checks). Always fill the empty cell with the fewest legal digits next — it fails fast and prunes most of the tree.", "O(9ᵐ) worst, tiny in practice", "O(81)"),
  inplace=0)


@B
def solve_sudoku(board):
    def ok(r, c, d):
        for i in range(9):
            if board[r][i] == d or board[i][c] == d or board[r // 3 * 3 + i // 3][c // 3 * 3 + i % 3] == d:
                return False
        return True

    def go(k):
        if k == 81:
            return True
        r, c = divmod(k, 9)
        if board[r][c] != ".":
            return go(k + 1)
        for d in "123456789":
            if ok(r, c, d):
                board[r][c] = d
                if go(k + 1):
                    return True
                board[r][c] = "."
        return False
    go(0)


@O
def solve_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == ".":
                empty.append((r, c))
            else:
                rows[r].add(d); cols[c].add(d); boxes[r // 3 * 3 + c // 3].add(d)
    filled = []

    def go():
        if not empty:
            return True
        best = max(empty, key=lambda rc: len(rows[rc[0]] | cols[rc[1]] | boxes[rc[0] // 3 * 3 + rc[1] // 3]))  # most digits ruled out
        r, c = best
        b = r // 3 * 3 + c // 3
        empty.remove(best)
        for d in "123456789":
            if d in rows[r] or d in cols[c] or d in boxes[b]:
                continue
            board[r][c] = d
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)
            filled.append((r, c))
            T(f"({r},{c}) has the fewest options → try {d}", G("board", board, hl=[(r, c)], ok=filled[:-1]), at="prev")
            if go():
                return True
            board[r][c] = "."
            rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
            filled.pop()
        empty.append(best)
        return False

    go()


# 14 --------------------------------------------------------------
Q(216, "Combination Sum III", "Medium", "Choose k from 1..9",
  "Find all combinations of <code>k</code> distinct numbers from 1–9 that sum to <code>n</code>.",
  [((3, 7), [[1, 2, 4]]), ((3, 9), [[1, 2, 6], [1, 3, 5], [2, 3, 4]]), ((4, 1), [])],
  ("Check all 2⁹ subsets of 1..9 for size k and sum n.", "O(9 · 2⁹)", "O(k)"),
  ("Backtrack from 'start', stopping when the remaining sum goes negative or the path is already k long.", "O(C(9, k) · k)", "O(k)"),
  norm=SORT2,
  viz=(3, 9))


@B
def combination_sum3(k, n):
    return [[d + 1 for d in range(9) if m >> d & 1] for m in range(1 << 9)
            if bin(m).count("1") == k and sum(d + 1 for d in range(9) if m >> d & 1) == n]


@O
def combination_sum3(k, n):
    res, path = [], []

    def go(start, remain):
        if len(path) == k:
            if remain == 0:
                res.append(path[:])
                T(f"Found {path}", A("path", path, ok=range(k)), V(result=res))
            return
        for x in range(start, 10):
            if x > remain:
                break
            path.append(x)
            go(x + 1, remain - x)
            path.pop()

    go(1, n)
    return res


# 15 --------------------------------------------------------------
Q(93, "Restore IP Addresses", "Medium", "Four parts with validity pruning",
  "Insert three dots into the digit string <code>s</code> to form all valid IPv4 addresses (each part 0–255, no leading zeros).",
  [(("25525511135",), ["255.255.11.135", "255.255.111.35"]), (("0000",), ["0.0.0.0"]), (("101023",), ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"])],
  ("Try every way to place 3 dots among the gaps and validate the four parts.", "O(n³)", "O(n)"),
  ("Backtrack part by part, taking 1–3 digits. Prune when the rest is too short or too long for the remaining parts, or the part is invalid.", "O(3⁴) = O(1)", "O(1)"),
  norm=sorted,
  viz=("101023",))


@B
def restore_ip_addresses(s):
    def valid(p):
        return len(p) > 0 and (p == "0" or p[0] != "0") and int(p) <= 255

    n, res = len(s), []
    for a in range(1, n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                parts = [s[:a], s[a:b], s[b:c], s[c:]]
                if all(len(p) <= 3 and valid(p) for p in parts):
                    res.append(".".join(parts))
    return res


@O
def restore_ip_addresses(s):
    def valid(p):
        return len(p) > 0 and (p == "0" or p[0] != "0") and int(p) <= 255

    res, parts = [], []

    def go(i):
        left = 4 - len(parts)
        if len(s) - i < left or len(s) - i > 3 * left:
            return
        if left == 0:
            res.append(".".join(parts))
            T(f"Valid address {res[-1]}", A("s", s), A("parts", parts, ok=range(4)))
            return
        for size in (1, 2, 3):
            part = s[i:i + size]
            if len(part) == size and valid(part):
                parts.append(part)
                go(i + size)
                parts.pop()

    go(0)
    return res


# 16 --------------------------------------------------------------
Q(50, "Pow(x, n)", "Medium", "Fast exponentiation",
  "Compute x raised to the integer power n (n may be negative).",
  [((2.0, 10), 1024.0), ((2.1, 3), 9.261), ((2.0, -2), 0.25)],
  ("Multiply x by itself |n| times.", "O(n)", "O(1)"),
  ("xⁿ = (x²)^(n/2) for even n, and x · xⁿ⁻¹ for odd n. Square the base and halve the exponent each step.", "O(log n)", "O(1)"),
  norm=lambda v: round(v, 6), viz=(3.0, 13))


@B
def my_pow(x, n):
    res = 1.0
    for _ in range(abs(n)):
        res *= x
    return res if n >= 0 else 1 / res


@O
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    res = 1.0
    while n:
        if n & 1:
            res *= x
        T(f"n = {n} ({bin(n)}): {'odd → res ×= base' if n & 1 else 'even'}; then square base", V(base=x, n=n, res=res), at="prev")
        x *= x
        n >>= 1
    return res


# 17 --------------------------------------------------------------
Q(784, "Letter Case Permutation", "Medium", "Branch on letters only",
  "Return every string obtainable by changing the case of each letter in <code>s</code>.",
  [(("a1b2",), ["a1b2", "a1B2", "A1b2", "A1B2"]), (("3z4",), ["3z4", "3Z4"])],
  ("Loop over a bitmask of the letters; bit i decides the case of letter i.", "O(n · 2ᴸ)", "O(n · 2ᴸ)"),
  ("Backtrack through s; digits have one branch, letters have two (lower, upper).", "O(n · 2ᴸ)", "O(n)"),
  norm=sorted)


@B
def letter_case_permutation(s):
    idx = [i for i, ch in enumerate(s) if ch.isalpha()]
    res = []
    for m in range(1 << len(idx)):
        cur = list(s.lower())
        for b, i in enumerate(idx):
            if m >> b & 1:
                cur[i] = cur[i].upper()
        res.append("".join(cur))
    return res


@O
def letter_case_permutation(s):
    res, path = [], []

    def go(i):
        if i == len(s):
            res.append("".join(path))
            T(f"Record '{res[-1]}'", A("s", s), A("path", path, ok=range(len(path))), V(count=len(res)))
            return
        options = {s[i].lower(), s[i].upper()} if s[i].isalpha() else {s[i]}
        for ch in sorted(options):
            path.append(ch)
            go(i + 1)
            path.pop()

    go(0)
    return res


# 18 --------------------------------------------------------------
Q(698, "Partition to K Equal Sum Subsets", "Medium", "Fill buckets · prune",
  "Can <code>nums</code> be split into <code>k</code> non-empty subsets with equal sums?",
  [(([4, 3, 2, 3, 5, 2, 1], 4), True), (([1, 2, 3, 4], 3), False)],
  ("Assign each number to one of k buckets in every possible way (kⁿ).", "O(kⁿ)", "O(n)"),
  ("target = sum / k. Sort descending, place each number into a bucket with room. Skip a bucket whose current sum equals one already tried (symmetry), and stop at the first empty bucket that fails.", "O(kⁿ) worst, heavily pruned", "O(n)"),
  viz=([4, 3, 2, 3, 5, 2, 1], 4))


@B
def can_partition_k_subsets(nums, k):
    from itertools import product
    total = sum(nums)
    if total % k:
        return False
    for assign in product(range(k), repeat=len(nums)):
        sums = [0] * k
        for x, b in zip(nums, assign):
            sums[b] += x
        if len(set(sums)) == 1:
            return True
    return False


@O
def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums.sort(reverse=True)
    if nums[0] > target:
        return False
    buckets = [0] * k

    def go(i):
        if i == len(nums):
            return True
        tried = set()
        for b in range(k):
            if buckets[b] + nums[i] > target or buckets[b] in tried:
                continue
            tried.add(buckets[b])
            buckets[b] += nums[i]
            T(f"Put {nums[i]} into bucket {b} (target {target})", A("nums", nums, hl=[i], ok=range(i), i=i), A("buckets", buckets, hl=[b]), at="prev")
            if go(i + 1):
                return True
            buckets[b] -= nums[i]
        return False

    return go(0)


# 19 --------------------------------------------------------------
Q(140, "Word Break II", "Hard", "Memoised DFS on start index",
  "Add spaces to <code>s</code> to form sentences where every word is in <code>wordDict</code>. Return all such sentences.",
  [(("catsanddog", ["cat", "cats", "and", "sand", "dog"]), ["cats and dog", "cat sand dog"]),
   (("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]), ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"]),
   (("catsandog", ["cats", "dog", "sand", "and", "cat"]), [])],
  ("Try all 2ⁿ⁻¹ ways to place spaces and keep those whose words are all in the dictionary.", "O(n · 2ⁿ)", "O(n)"),
  ("sentences(i) = for every dictionary word starting at i, that word + each sentence of the rest. Memoise on i so each suffix is solved once.", "O(n · 2ⁿ) output-bound, far less in practice", "O(n · answers)"),
  norm=sorted, viz=("catsanddog", ["cat", "cats", "and", "sand", "dog"]))


@B
def word_break(s, word_dict):
    words, n, res = set(word_dict), len(s), []
    for mask in range(1 << (n - 1)):
        parts, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(s[start:i + 1])
                start = i + 1
        parts.append(s[start:])
        if all(p in words for p in parts):
            res.append(" ".join(parts))
    return res


@O
def word_break(s, word_dict):
    words = set(word_dict)
    memo = {}

    def go(i):
        if i == len(s):
            return [""]
        if i in memo:
            T(f"Suffix '{s[i:]}' already solved → reuse", A("s", s, ok=range(i, len(s)), i=i), M("memo", {k: v for k, v in memo.items()}, hl=i))
            return memo[i]
        out = []
        for j in range(i + 1, len(s) + 1):
            if s[i:j] in words:
                for rest in go(j):
                    out.append(s[i:j] + (" " + rest if rest else ""))
        memo[i] = out
        T(f"Sentences for suffix '{s[i:]}': {out}", A("s", s, hl=range(i, len(s)), i=i), M("memo", memo, hl=i), at="prev")
        return out

    return go(0)


# 20 --------------------------------------------------------------
Q(473, "Matchsticks to Square", "Medium", "Four sides · sort + prune",
  "Can all matchsticks be used (each once, unbroken) to form a square?",
  [(([1, 1, 2, 2, 2],), True), (([3, 3, 3, 3, 4],), False)],
  ("Assign each stick to one of 4 sides in all 4ⁿ ways.", "O(4ⁿ)", "O(n)"),
  ("Side = total / 4. Place sticks longest first into sides with room; skip a side whose length equals one already tried for this stick.", "O(4ⁿ) worst, heavily pruned", "O(n)"),
  viz=([3, 1, 2, 2, 2, 1, 1],))


@B
def makesquare(sticks):
    from itertools import product
    total = sum(sticks)
    if total % 4:
        return False
    for assign in product(range(4), repeat=len(sticks)):
        sides = [0] * 4
        for x, b in zip(sticks, assign):
            sides[b] += x
        if len(set(sides)) == 1:
            return True
    return False


@O
def makesquare(sticks):
    total = sum(sticks)
    if total % 4 or not sticks:
        return False
    side = total // 4
    sticks.sort(reverse=True)
    sides = [0] * 4

    def go(i):
        if i == len(sticks):
            return True
        for b in range(4):
            if sides[b] + sticks[i] > side or sides[b] in sides[:b]:
                continue
            sides[b] += sticks[i]
            T(f"Stick {sticks[i]} → side {b} (each side must reach {side})", A("sticks", sticks, hl=[i], ok=range(i), i=i), A("sides", sides, hl=[b]), at="prev")
            if go(i + 1):
                return True
            sides[b] -= sticks[i]
        return False

    return go(0)
