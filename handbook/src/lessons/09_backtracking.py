from lib import *

LESSON("Basics", "Recursion: a function that calls itself", """
<p>A <b>recursive</b> function solves a problem by calling itself on a <b>smaller</b> version of the same problem. It needs two parts:</p>
<ol>
<li><b>Base case</b> — a version so small you answer it directly (and stop).</li>
<li><b>Recursive case</b> — shrink the problem, call yourself, use the result.</li>
</ol>
<pre><code class="py">def factorial(n):
    if n &lt;= 1:                  # base case
        return 1
    return n * factorial(n - 1) # smaller problem</code></pre>
<p>Each call waits on the <b>call stack</b> until the smaller call returns. Forgetting the base case (or not shrinking) means infinite recursion → <code>RecursionError</code>.</p>
""", practice=[50])


@LD
def call_stack_lesson():
    frames = []

    def fact(n):
        frames.append(f"fact({n})")
        T(f"Call fact({n}) — pushed onto the call stack", S("call stack", frames, hl=[len(frames) - 1]))
        if n <= 1:
            result = 1
        else:
            result = n * fact(n - 1)
        frames.pop()
        T(f"fact({n}) returns {result} — popped", S("call stack", frames), V(returned=result))
        return result

    return fact(4)


LESSON("Basics", "The decision tree", """
<p>Many problems are "make a sequence of choices": include this element or not, which number goes next, where to place the next queen. Draw every possible sequence of choices and you get a <b>decision tree</b>: each level is one choice, each leaf is one complete candidate.</p>
<div class="pic">              []
         /          \\          include 1?
       [1]           []
      /   \\        /    \\      include 2?
  [1,2]  [1]     [2]    []     ← 4 leaves = 4 subsets of [1, 2]</div>
<p>The tree can be huge: 2ⁿ leaves for subsets, n! for permutations. That's why these problems have exponential cost — and why <b>pruning</b> (cutting branches that can't work) is the key skill.</p>
""")


LESSON("Core", "The backtracking template: choose, explore, un-choose", """
<p><b>Backtracking</b> walks the decision tree with DFS, keeping one shared <code>path</code>:</p>
<pre><code class="py">def backtrack(start, path):
    if done(path):
        res.append(path[:])        # save a COPY
        return
    for i in range(start, len(choices)):
        if not ok(choices[i]):     # prune
            continue
        path.append(choices[i])    # choose
        backtrack(i + 1, path)     # explore
        path.pop()                 # un-choose (backtrack)</code></pre>
<p>Using <code>start</code> and calling with <code>i + 1</code> means every combination is produced once, in increasing index order. For <b>subsets</b>, every node of the tree is an answer, so record the path at the start of each call.</p>
<div class="warn"><code>res.append(path)</code> without copying stores the same list again and again — at the end they're all empty.</div>
""", practice=[78, 77, 17, 784])


LESSON("Core", "Permutations", """
<p>For permutations the order matters and every element is used, so each level may choose <b>any</b> unused element, not just later ones. Track which are used:</p>
<pre><code class="py">def go():
    if len(path) == n:
        res.append(path[:]); return
    for i in range(n):
        if used[i]: continue
        used[i] = True; path.append(nums[i])
        go()
        path.pop(); used[i] = False</code></pre>
<p>There are n! permutations, each of length n → O(n · n!).</p>
""", practice=[46, 47])


@LD
def permute_lesson():
    nums = [1, 2, 3]
    path, used, res = [], [False] * 3, []

    def go():
        if len(path) == len(nums):
            res.append(path[:])
            T(f"Complete permutation #{len(res)}: {path}", A("nums", nums, ok=[i for i in range(3) if used[i]]), A("path", path, ok=range(3)))
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


LESSON("Core", "Pruning and duplicates", """
<p><b>Pruning</b> = stop exploring a branch as soon as you know it can't lead to an answer.</p>
<ul>
<li><b>Combination sum</b>: sort the candidates; once a candidate is bigger than the remaining target, every later one is too — <code>break</code>.</li>
<li><b>Count limits</b>: if fewer elements remain than you still need, stop.</li>
<li><b>Reuse allowed</b>: recurse with <code>i</code> instead of <code>i + 1</code>.</li>
</ul>
<h4>Avoiding duplicate answers</h4>
<p>If the input has repeated values, sort it and skip a value equal to the previous one <b>at the same level</b>:</p>
<pre><code class="py">for i in range(start, n):
    if i &gt; start and nums[i] == nums[i - 1]:
        continue</code></pre>
<p>The first copy explores every option; a second copy at the same level would only repeat it.</p>
""", practice=[39, 40, 90, 216, 22])


@LD
def pruning_lesson():
    cands, target = [2, 3, 5], 8
    res, path = [], []

    def go(start, remain):
        if remain == 0:
            res.append(path[:])
            T(f"Hit {target}: {path}", A("candidates", cands), A("path", path, ok=range(len(path))), V(found=res))
            return
        for i in range(start, len(cands)):
            if cands[i] > remain:
                T(f"{cands[i]} > remaining {remain} → prune, and skip all bigger ones", A("candidates", cands, bad=range(i, len(cands))), A("path", path), V(remain=remain))
                break
            path.append(cands[i])
            go(i, remain - cands[i])
            path.pop()

    go(0, target)
    return res


LESSON("Advanced", "Constraint problems", """
<p>N-Queens, Sudoku, word search and partitioning problems are backtracking with <b>constraints</b>. Two things make them fast:</p>
<ul>
<li><b>O(1) validity checks</b>: keep sets of used columns and diagonals (<code>r − c</code>, <code>r + c</code>) for queens; sets per row/column/box for Sudoku; mark grid cells in place for word search and unmark on return.</li>
<li><b>Smart order</b>: try the most constrained spot first (the Sudoku cell with the fewest options), place large items first (matchsticks, k-equal subsets), and skip symmetric choices (two empty buckets are interchangeable).</li>
</ul>
<p>Good pruning can turn "impossible" (9⁶⁰ for Sudoku) into milliseconds.</p>
""", practice=[51, 37, 79, 698, 473, 93])


LESSON("Advanced", "From backtracking to memoisation", """
<p>Sometimes different branches reach the <b>same sub-problem</b>. In word break II, the suffix starting at index 7 is solved again every time a different split reaches index 7.</p>
<p>If the answer for a sub-problem depends only on its arguments (here, the start index), store it in a dict the first time and reuse it — <b>memoisation</b>:</p>
<pre><code class="py">memo = {}
def go(i):
    if i in memo: return memo[i]
    ...
    memo[i] = answer
    return answer</code></pre>
<p>That's exactly the doorway to <b>dynamic programming</b>. Ask yourself: "is the result determined by a small state, and does that state repeat?" If yes, memoise.</p>
""", practice=[140, 131])
