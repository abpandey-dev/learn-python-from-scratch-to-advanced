from lib import *

THEORY("Big-O, in plain numbers", """
<p>A rough guide: a computer does about 10⁸ simple operations per second in fast languages, and far fewer in Python.</p>
<table><tr><th>Input size n</th><th>Usually acceptable</th></tr>
<tr><td>up to 20</td><td>O(2ⁿ), O(n!)</td></tr>
<tr><td>up to 500</td><td>O(n³)</td></tr>
<tr><td>up to 5,000</td><td>O(n²)</td></tr>
<tr><td>up to 10⁶</td><td>O(n log n), O(n)</td></tr>
<tr><td>larger</td><td>O(log n), O(1)</td></tr></table>
<p>So constraints in a question hint at the expected solution. Ask for them.</p>
""")
FAQ("Merge sort or quick sort?", "<p>Quick sort is usually faster in practice and in place, but its worst case is O(n²). Merge sort is always O(n log n) and stable, but needs O(n) extra memory. It also suits linked lists and external sorting.</p>")
FAQ("What does stable sorting mean?", "<p>Equal items keep their original order. It matters when sorting by one key after another.</p>")
FAQ("Why is O(n log n) the limit for comparison sorting?", "<p>There are n! possible orders and each comparison at best halves them, which takes about log₂(n!) ≈ n log n comparisons. Counting and radix sort avoid this by not comparing.</p>")
FAQ("How does a hash map handle collisions?", "<p>Chaining keeps a list per bucket. Open addressing probes for another free slot. Both resize when the load factor gets too high, keeping operations O(1) on average.</p>")
FAQ("What is amortised analysis?", "<p>Averaging cost over a sequence of operations. A dynamic array's occasional O(n) resize still averages O(1) per append.</p>")
FAQ("Dijkstra vs Bellman-Ford?", "<p>Dijkstra is faster but needs non-negative weights. Bellman-Ford handles negative weights and detects negative cycles, but it's slower.</p>")
FAQ("BFS vs DFS?", "<p>BFS explores level by level, and finds shortest paths in unweighted graphs. DFS goes deep first, using less memory on wide graphs, and suits cycle detection and backtracking.</p>")
FAQ("Dynamic programming vs greedy?", "<p>Greedy makes one locally best choice and never reconsiders, so it needs a proof. DP considers all choices over overlapping subproblems, and costs more.</p>")
FAQ("Recursion: what limits it?", "<p>Each call uses stack memory, and Python limits depth to about 1,000 by default. Very deep recursion is usually rewritten with an explicit stack.</p>")
FAQ("When use a heap rather than sorting?", "<p>When you only need the top k, or items arrive over time. A heap gives O(n log k) for top k, or O(log n) per insert.</p>")
