from lib import *

THEORY("Definition", """
<p><b>Dynamic programming (DP)</b> is an algorithm design technique for problems that can be broken into overlapping sub-problems. It solves each sub-problem <b>once</b>, stores the result, and reuses it — trading memory for time. The term was coined by Richard Bellman in the 1950s.</p>
""")

THEORY("When DP applies: the two properties", """
<h4>1. Optimal substructure</h4>
<p>An optimal solution to the problem contains optimal solutions to its sub-problems. Example: the shortest path A → C through B consists of the shortest path A → B and the shortest path B → C.</p>
<h4>2. Overlapping sub-problems</h4>
<p>The same sub-problems are solved many times by a naive recursion. Example: <code>fib(n)</code> calls <code>fib(n − 2)</code> both directly and through <code>fib(n − 1)</code>.</p>
<p>If sub-problems <b>don't overlap</b> (merge sort's halves are independent), the right technique is <b>divide and conquer</b>, not DP. If a <b>local choice</b> is always safe, <b>greedy</b> is simpler.</p>
""")

THEORY("Approaches", """
<table>
<tr><th></th><th>Top-down (memoisation)</th><th>Bottom-up (tabulation)</th></tr>
<tr><td>Idea</td><td>recursion + cache of computed results</td><td>iteratively fill a table from base cases</td></tr>
<tr><td>Order</td><td>computed on demand</td><td>must choose an order where dependencies come first</td></tr>
<tr><td>Visits</td><td>only states actually needed</td><td>usually every state</td></tr>
<tr><td>Overhead</td><td>function calls, recursion depth limit</td><td>none; tight loops</td></tr>
<tr><td>Space optimisation</td><td>harder</td><td>easy (keep only the rows you need)</td></tr>
<tr><td>Python</td><td><code>@functools.cache</code></td><td><code>dp = [0] * (n + 1)</code></td></tr>
</table>
""")

THEORY("Designing a DP solution", """
<ol>
<li><b>Define the state</b>: the smallest set of parameters that describes a sub-problem, e.g. <code>dp[i]</code> = best answer for the first i items; <code>dp[i][w]</code> = best value using items 0..i with capacity w.</li>
<li><b>Write the recurrence (transition)</b>: how a state is computed from smaller states.</li>
<li><b>Identify base cases</b>.</li>
<li><b>Decide the evaluation order</b> (bottom-up) or add memoisation (top-down).</li>
<li><b>Locate the answer</b> in the table (<code>dp[n]</code>, <code>max(dp)</code>, <code>dp[m][n]</code>).</li>
<li><b>Optimise space</b> if each state depends only on the previous row/values.</li>
</ol>
<p><b>Complexity</b> = (number of states) × (work per transition). Example: LCS has m·n states with O(1) work → O(m·n).</p>
""")

THEORY("Classic DP problem families", """
<table>
<tr><th>Family</th><th>State</th><th>Examples</th><th>Typical time</th></tr>
<tr><td>Linear / 1-D</td><td>dp[i]</td><td>Fibonacci, climbing stairs, house robber, decode ways</td><td>O(n)</td></tr>
<tr><td>0/1 knapsack</td><td>dp[i][w] or dp[w]</td><td>subset sum, partition, target sum</td><td>O(n · W)</td></tr>
<tr><td>Unbounded knapsack</td><td>dp[w]</td><td>coin change, rod cutting</td><td>O(n · W)</td></tr>
<tr><td>Subsequences</td><td>dp[i] / tails</td><td>LIS</td><td>O(n²) or O(n log n)</td></tr>
<tr><td>Two sequences</td><td>dp[i][j]</td><td>LCS, edit distance, interleaving strings</td><td>O(m · n)</td></tr>
<tr><td>Grid</td><td>dp[r][c]</td><td>unique paths, min path sum, maximal square</td><td>O(m · n)</td></tr>
<tr><td>Interval</td><td>dp[l][r]</td><td>matrix chain multiplication, burst balloons, palindromic substrings</td><td>O(n³) / O(n²)</td></tr>
<tr><td>State machine</td><td>dp[i][state]</td><td>stock buy/sell with cooldown or fee</td><td>O(n)</td></tr>
<tr><td>Bitmask</td><td>dp[mask]</td><td>travelling salesman, assignment</td><td>O(2ⁿ · n²)</td></tr>
<tr><td>Tree DP</td><td>dp[node]</td><td>house robber III, tree diameter</td><td>O(n)</td></tr>
</table>
<p><b>Pseudo-polynomial</b>: knapsack's O(n · W) depends on the <i>value</i> W, not just the input size, so it's slow for huge capacities.</p>
""")

THEORY("DP vs other paradigms", """
<table>
<tr><th>Paradigm</th><th>Sub-problems</th><th>Choice</th><th>Example</th></tr>
<tr><td>Divide and conquer</td><td>independent</td><td>—</td><td>merge sort, quicksort</td></tr>
<tr><td><b>Dynamic programming</b></td><td>overlapping</td><td>tries all choices, keeps the best</td><td>knapsack, LCS</td></tr>
<tr><td>Greedy</td><td>one at a time</td><td>commits to the locally best choice</td><td>interval scheduling, Huffman coding</td></tr>
<tr><td>Backtracking</td><td>explores a tree of choices</td><td>prunes invalid branches</td><td>N-Queens, Sudoku</td></tr>
</table>
""")

THEORY("Applications", """
<ul>
<li>Text: spell checkers and diff tools (edit distance, LCS); DNA sequence alignment in bioinformatics.</li>
<li>Resource allocation and budgeting (knapsack variants).</li>
<li>Shortest paths: Bellman–Ford and Floyd–Warshall are DP algorithms.</li>
<li>Speech recognition and part-of-speech tagging (Viterbi algorithm).</li>
<li>Finance: option pricing, optimal trading strategies.</li>
<li>Reinforcement learning: value iteration, Bellman equations.</li>
</ul>
""")

FAQ("What two properties must a problem have for DP?", "<p><b>Optimal substructure</b> (optimal solutions are built from optimal sub-solutions) and <b>overlapping sub-problems</b> (the same sub-problems recur). Without overlap, use divide and conquer; with a safe local choice, greedy may suffice.</p>")
FAQ("Memoisation vs tabulation?", "<p>Memoisation is top-down: write the recursion and cache results; computes only needed states but has recursion overhead. Tabulation is bottom-up: fill a table in dependency order; no recursion and easy to space-optimise.</p>")
FAQ("How do you find the time complexity of a DP solution?", "<p>Number of distinct states × time per state transition. For example, coin change has (amount + 1) states, each trying n coins → O(amount × n).</p>")
FAQ("What is the difference between DP and greedy?", "<p>Greedy makes one locally optimal choice per step and never reconsiders; it's only correct when a greedy-choice property can be proven. DP considers all choices for each sub-problem and keeps the best, so it's correct whenever optimal substructure holds — at a higher cost.</p>")
FAQ("Why does 0/1 knapsack iterate capacity backwards in a 1-D array?", "<p>Going from high to low capacity means <code>dp[c − w]</code> still holds the previous item's row, so each item is counted at most once. Going forwards would let the same item be reused (that's unbounded knapsack).</p>")
FAQ("Why is knapsack called pseudo-polynomial?", "<p>O(n · W) is polynomial in the numeric value W, but W can be exponential in the number of bits used to write it. Knapsack is NP-hard in general.</p>")
FAQ("How do you reconstruct the actual solution, not just its value?", "<p>Store the choice made at each state (or recompute it by checking which transition produced the stored value), then walk back from the answer state to the base case.</p>")
