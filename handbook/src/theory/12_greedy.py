from lib import *

THEORY("Definition", """
<p>A <b>greedy algorithm</b> builds a solution step by step, at each step making the choice that looks <b>best at that moment</b> (the locally optimal choice), and never reconsidering earlier choices. It is correct only for problems where local optimality leads to global optimality.</p>
<p>An <b>interval</b> is a pair [start, end]. Interval problems (merging, scheduling, covering) are among the most common uses of greedy algorithms.</p>
""")

THEORY("When greedy works", """
<h4>1. Greedy-choice property</h4>
<p>A globally optimal solution can be reached by making a locally optimal choice first. There exists some optimal solution that agrees with the greedy choice.</p>
<h4>2. Optimal substructure</h4>
<p>After making the greedy choice, what remains is a smaller instance of the same problem, whose optimal solution combines with the choice to give an optimal overall solution.</p>
<h4>How to prove it</h4>
<ul>
<li><b>Exchange argument</b>: take any optimal solution that differs from greedy; swap in the greedy choice and show the result is no worse.</li>
<li><b>Greedy stays ahead</b>: show after each step greedy's partial solution is at least as good as any other's.</li>
<li><b>Counter-example search</b>: before proving, try small inputs to break the idea. If one breaks it, switch to DP.</li>
</ul>
""")

THEORY("Classic greedy problems", """
<table>
<tr><th>Problem</th><th>Greedy rule</th><th>Time</th></tr>
<tr><td>Activity selection / max non-overlapping intervals</td><td>pick the interval that <b>ends earliest</b></td><td>O(n log n)</td></tr>
<tr><td>Fractional knapsack</td><td>take items by highest value/weight ratio, splitting the last</td><td>O(n log n)</td></tr>
<tr><td>Huffman coding</td><td>repeatedly merge the two least frequent symbols</td><td>O(n log n)</td></tr>
<tr><td>Minimum spanning tree (Kruskal, Prim)</td><td>add the cheapest safe edge</td><td>O(E log V)</td></tr>
<tr><td>Dijkstra</td><td>finalise the closest unvisited vertex</td><td>O(E log V)</td></tr>
<tr><td>Job sequencing with deadlines</td><td>schedule highest profit first in the latest free slot</td><td>O(n log n)</td></tr>
<tr><td>Coin change (canonical coins like 1, 2, 5, 10)</td><td>take the largest coin that fits</td><td>O(amount / coin)</td></tr>
</table>
<p><b>Greedy fails</b> for 0/1 knapsack and for coin change with arbitrary coins (e.g. coins 1, 3, 4 and amount 6) — those need DP.</p>
""")

THEORY("Interval theory", """
<p>Two intervals [a, b] and [c, d] <b>overlap</b> when <code>a ≤ d and c ≤ b</code> (use &lt; if touching endpoints don't count). Their intersection is <code>[max(a, c), min(b, d)]</code> when non-empty.</p>
<table>
<tr><th>Goal</th><th>Sort by</th><th>Why</th></tr>
<tr><td>Merge overlapping intervals</td><td>start</td><td>overlaps then become adjacent in order</td></tr>
<tr><td>Maximum non-overlapping set / minimum removals</td><td>end</td><td>finishing earliest leaves the most room (exchange argument)</td></tr>
<tr><td>Minimum points to stab all intervals</td><td>end</td><td>a point at the earliest end hits every interval that started before it</td></tr>
<tr><td>Maximum overlap (rooms, platforms)</td><td>events (start +1, end −1)</td><td>sweep line counts active intervals</td></tr>
<tr><td>Remove covered intervals</td><td>start asc, end desc</td><td>a covered interval has end ≤ the max end seen so far</td></tr>
</table>
""")

THEORY("Greedy vs dynamic programming", """
<table>
<tr><th></th><th>Greedy</th><th>Dynamic programming</th></tr>
<tr><td>Choices per step</td><td>one (the locally best)</td><td>all, keeps the best</td></tr>
<tr><td>Reconsiders?</td><td>never</td><td>effectively yes</td></tr>
<tr><td>Correctness</td><td>needs a proof (greedy-choice property)</td><td>follows from optimal substructure</td></tr>
<tr><td>Speed</td><td>usually O(n log n) or O(n)</td><td>usually O(n²) or O(n · W)</td></tr>
<tr><td>Memory</td><td>O(1) extra</td><td>table of states</td></tr>
<tr><td>Example where it's right</td><td>fractional knapsack</td><td>0/1 knapsack</td></tr>
</table>
""")

THEORY("Advantages, disadvantages and applications", """
<div class="two">
<div class="pro"><h5>Advantages</h5><ul><li>Simple and fast</li><li>Little memory</li><li>Often the optimal method for scheduling and MST problems</li><li>Good approximation when exact methods are too slow</li></ul></div>
<div class="con"><h5>Disadvantages</h5><ul><li>Not always correct — needs proof</li><li>Hard to know whether it applies without experience</li><li>Can give a poor answer silently</li></ul></div>
</div>
<h4>Applications</h4>
<ul>
<li>CPU and meeting scheduling, room / platform allocation, calendar apps.</li>
<li>Data compression (Huffman coding).</li>
<li>Network design (minimum spanning trees), routing (Dijkstra).</li>
<li>Making change at a cash register (canonical coin systems).</li>
<li>Load balancing and caching policies; approximation algorithms for NP-hard problems (set cover).</li>
</ul>
""")

FAQ("What is a greedy algorithm?", "<p>An algorithm that makes the locally optimal choice at each step without reconsidering, hoping it leads to a global optimum. It works when the problem has the greedy-choice property and optimal substructure.</p>")
FAQ("How do you prove a greedy algorithm is correct?", "<p>Usually by an exchange argument: show that any optimal solution can be transformed, step by step, into the greedy solution without becoming worse. Alternatively, show greedy 'stays ahead' of any other solution at every step.</p>")
FAQ("Why does activity selection sort by end time, not start time?", "<p>Choosing the interval that finishes earliest leaves the maximum remaining time for others. Sorting by start can pick a long early interval that blocks many short ones.</p>")
FAQ("Give an example where greedy fails.", "<p>Coin change with coins {1, 3, 4} and amount 6: greedy picks 4 + 1 + 1 (3 coins), but 3 + 3 (2 coins) is optimal. 0/1 knapsack by value/weight ratio also fails.</p>")
FAQ("Fractional vs 0/1 knapsack?", "<p>Fractional knapsack allows taking part of an item, so greedy by value/weight ratio is optimal (O(n log n)). In 0/1 knapsack items are indivisible, greedy fails, and DP (O(n · W)) is needed.</p>")
FAQ("How do you find the minimum number of meeting rooms?", "<p>Sort start and end times (or events) and sweep: +1 at a start, −1 at an end; the maximum running count is the answer. Equivalently, sort by start and keep a min-heap of end times.</p>")
