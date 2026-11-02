from lib import *

THEORY("Definitions", """
<p><b>Recursion</b> is a technique where a function solves a problem by calling itself on smaller instances of the same problem, until reaching a <b>base case</b> that is solved directly.</p>
<p><b>Backtracking</b> is an algorithmic paradigm that builds a solution incrementally, one choice at a time, and <b>abandons (backtracks from)</b> a partial solution as soon as it determines it cannot lead to a valid complete solution. It is a depth-first search over the <b>state-space tree</b> of choices.</p>
""")

THEORY("Parts of a recursive function", """
<ol>
<li><b>Base case</b> — the stopping condition; returns without recursing.</li>
<li><b>Recursive case</b> — breaks the problem into a smaller sub-problem and calls itself.</li>
<li><b>Progress</b> — each call must move toward the base case, or recursion never ends.</li>
</ol>
<p>Each call creates a <b>stack frame</b> holding its parameters and local variables. Too many nested calls exhaust the stack: <code>RecursionError</code> in Python (default limit ~1000), stack overflow in other languages.</p>
""")

THEORY("Types of recursion", """
<table>
<tr><th>Type</th><th>Description</th><th>Example</th></tr>
<tr><td><b>Direct</b></td><td>function calls itself</td><td><code>fact(n) = n * fact(n − 1)</code></td></tr>
<tr><td><b>Indirect</b></td><td>A calls B, B calls A</td><td><code>is_even ↔ is_odd</code></td></tr>
<tr><td><b>Tail</b></td><td>the recursive call is the last action</td><td><code>gcd(a, b) = gcd(b, a % b)</code></td></tr>
<tr><td><b>Non-tail (head)</b></td><td>work remains after the call returns</td><td><code>n * fact(n − 1)</code></td></tr>
<tr><td><b>Linear</b></td><td>one recursive call per invocation</td><td>sum of a list</td></tr>
<tr><td><b>Tree (multiple)</b></td><td>two or more calls per invocation</td><td>Fibonacci, subsets, permutations</td></tr>
</table>
<p>Tail recursion can be turned into a loop (some languages do this automatically; Python does not).</p>
""")

THEORY("Analysing recursive algorithms", """
<p>Write a <b>recurrence relation</b> for the running time, then solve it.</p>
<table>
<tr><th>Recurrence</th><th>Example</th><th>Solution</th></tr>
<tr><td>T(n) = T(n − 1) + O(1)</td><td>factorial, linear recursion</td><td>O(n)</td></tr>
<tr><td>T(n) = T(n / 2) + O(1)</td><td>binary search</td><td>O(log n)</td></tr>
<tr><td>T(n) = 2T(n / 2) + O(n)</td><td>merge sort</td><td>O(n log n)</td></tr>
<tr><td>T(n) = 2T(n − 1) + O(1)</td><td>subsets, Tower of Hanoi</td><td>O(2ⁿ)</td></tr>
<tr><td>T(n) = T(n − 1) + T(n − 2)</td><td>naive Fibonacci</td><td>O(φⁿ) ≈ O(1.618ⁿ)</td></tr>
<tr><td>T(n) = n · T(n − 1)</td><td>permutations</td><td>O(n!)</td></tr>
</table>
<p><b>Master theorem</b> for T(n) = a·T(n/b) + O(nᵈ): if d &gt; log_b a → O(nᵈ); if d = log_b a → O(nᵈ log n); if d &lt; log_b a → O(n^(log_b a)).</p>
<p>Space = maximum recursion depth × space per frame (plus any stored results).</p>
""")

THEORY("Backtracking: state-space tree and pruning", """
<p>The <b>state-space tree</b> has the empty partial solution at the root; each edge is one choice; each leaf is a complete candidate. Backtracking explores it depth-first:</p>
<ol>
<li><b>Choose</b> an option and add it to the partial solution.</li>
<li><b>Check constraints</b>; if violated, <b>prune</b> (don't go deeper).</li>
<li><b>Explore</b> recursively.</li>
<li><b>Un-choose</b> (undo) and try the next option.</li>
</ol>
<p>Pruning with a <b>bounding function</b> (a quick test that a branch can't succeed) is what separates backtracking from brute-force enumeration. Its worst case is still exponential, but practical performance improves dramatically.</p>
<table>
<tr><th>Problem class</th><th>Search space</th></tr>
<tr><td>Subsets / combinations</td><td>2ⁿ</td></tr>
<tr><td>k-combinations</td><td>C(n, k)</td></tr>
<tr><td>Permutations</td><td>n!</td></tr>
<tr><td>N-Queens</td><td>≈ n! (one queen per row and column)</td></tr>
<tr><td>Sudoku</td><td>9^(empty cells)</td></tr>
</table>
""")

THEORY("Recursion vs iteration, and related paradigms", """
<table>
<tr><th></th><th>Recursion</th><th>Iteration</th></tr>
<tr><td>Code</td><td>shorter, mirrors the definition</td><td>often longer</td></tr>
<tr><td>Memory</td><td>O(depth) stack frames</td><td>O(1) usually</td></tr>
<tr><td>Speed</td><td>function-call overhead</td><td>faster</td></tr>
<tr><td>Risk</td><td>stack overflow</td><td>infinite loops</td></tr>
<tr><td>Best for</td><td>trees, divide and conquer, backtracking</td><td>simple linear processing</td></tr>
</table>
<table>
<tr><th>Paradigm</th><th>Idea</th></tr>
<tr><td>Brute force</td><td>generate every candidate, test each</td></tr>
<tr><td><b>Backtracking</b></td><td>build candidates step by step, prune invalid partial ones</td></tr>
<tr><td>Branch and bound</td><td>backtracking for optimisation, pruning by a bound on the best possible value</td></tr>
<tr><td>Divide and conquer</td><td>split into <i>independent</i> sub-problems, combine (merge sort)</td></tr>
<tr><td>Dynamic programming</td><td>split into <i>overlapping</i> sub-problems, store results</td></tr>
</table>
""")

THEORY("Applications", """
<ul>
<li>Puzzles: N-Queens, Sudoku, crosswords, mazes.</li>
<li>Combinatorics: generating subsets, permutations, combinations, partitions.</li>
<li>Constraint satisfaction: scheduling, timetabling, graph colouring.</li>
<li>Parsing and regular-expression matching engines.</li>
<li>Game trees (with minimax and alpha-beta pruning) in chess engines.</li>
<li>Recursion generally: tree/graph traversal, divide-and-conquer sorts, fractals.</li>
</ul>
""")

FAQ("What is the base case and why is it needed?", "<p>The condition under which the function returns without recursing. Without it (or without progress toward it), calls never stop and the program crashes with a stack overflow.</p>")
FAQ("Backtracking vs brute force?", "<p>Brute force generates every complete candidate and tests it. Backtracking builds candidates incrementally and stops extending a partial candidate as soon as it violates a constraint, skipping whole subtrees.</p>")
FAQ("Backtracking vs dynamic programming?", "<p>Backtracking explores choices and is used to enumerate or find solutions; it's exponential. DP applies when sub-problems overlap and the answer depends only on a small state, so results can be cached — often making it polynomial. Memoised backtracking is DP.</p>")
FAQ("What is tail recursion?", "<p>Recursion where the recursive call is the final operation, so no work remains afterwards. It can be optimised into a loop by compilers that support tail-call optimisation (Python doesn't).</p>")
FAQ("What is the time complexity of generating all subsets / permutations?", "<p>Subsets: 2ⁿ subsets, each up to n long to copy → O(n · 2ⁿ). Permutations: n! of length n → O(n · n!).</p>")
FAQ("Why copy the path when recording an answer?", "<p>The path list is shared and modified throughout the search. Appending the list itself stores a reference that later changes; <code>path[:]</code> stores a snapshot.</p>")
FAQ("How do you avoid duplicate results when the input has duplicates?", "<p>Sort the input and, within the same recursion level, skip an element equal to the previous one (<code>i &gt; start and a[i] == a[i−1]</code>). For permutations, skip when the previous equal element hasn't been used.</p>")
