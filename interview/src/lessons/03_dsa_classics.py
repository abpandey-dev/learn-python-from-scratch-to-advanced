from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np



LESSON("Basics", "Sorting: which, and why", """
<p>In real code you call <code>sorted()</code>. Interviews ask you to write one, to show you understand trade-offs.</p>
<p><b>Merge sort</b> splits in half until single items remain, then merges sorted pieces. Tracing [5, 2, 9, 1]:</p>
<pre><code class="py">[5, 2, 9, 1]
[5, 2]   [9, 1]         split
[2, 5]   [1, 9]         merge each half
[1, 2, 5, 9]            merge: compare the fronts, take the smaller</code></pre>
<p>There are log n levels, each doing n work, so it's O(n log n), always. It needs O(n) extra space. It's <b>stable</b>, meaning equal items keep their order, because the merge takes from the left on a tie.</p>
<p><b>Quick sort</b> picks a pivot, moves smaller items before it and larger ones after, then recurses. It's usually fastest in practice, and works in place, but a consistently bad pivot gives O(n²). A random or middle pivot makes that unlikely.</p>
<p><b>Heap sort</b> uses O(1) extra space and is O(n log n) always, but it isn't stable, and in practice it's often slower because of poor cache use.</p>
<p><b>Counting sort</b> beats O(n log n) by not comparing. For [3, 1, 2, 1, 0] with values up to 3: counts are 1, 2, 1, 1, so write 0, 1, 1, 2, 3. That's O(n + k), practical only when the range k is small.</p>
<table><tr><th></th><th>Average</th><th>Worst</th><th>Space</th><th>Stable?</th></tr>
<tr><td>Merge</td><td>n log n</td><td>n log n</td><td>n</td><td>yes</td></tr>
<tr><td>Quick</td><td>n log n</td><td><b>n²</b></td><td>log n</td><td>no</td></tr>
<tr><td>Heap</td><td>n log n</td><td>n log n</td><td>1</td><td>no</td></tr>
<tr><td>Counting</td><td>n + k</td><td>n + k</td><td>k</td><td>yes</td></tr>
<tr><td>Insertion</td><td>n²</td><td>n²</td><td>1</td><td>yes</td></tr></table>
<p><b>Why can't comparison sorts beat n log n?</b> There are n! possible orders, and each yes/no comparison at best halves the possibilities, which takes about log₂(n!) ≈ n log n comparisons.</p>
""", practice=["Merge Sort", "Quick Sort", "Heap Sort", "Counting Sort"])


@LD
def sort_growth():
    n = np.array([10, 100, 1000, 10000])
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.loglog(n, n ** 2, "o-", label="n² (insertion sort)")
    ax.loglog(n, n * np.log2(n), "s-", label="n log n (merge sort)")
    ax.loglog(n, n, "^-", label="n (counting sort, small range)")
    ax.set_xlabel("n")
    ax.set_ylabel("rough number of steps")
    ax.legend(fontsize=7)


LESSON("Core", "Counting inversions: divide and conquer pays off", """
<p>An inversion is a pair that's out of order. It measures how unsorted a list is, or how much two rankings disagree.</p>
<p>In [2, 4, 1, 3, 5], the pairs are (2, 1), (4, 1) and (4, 3): <b>3 inversions</b>. Checking all pairs is O(n²).</p>
<p><b>The insight comes during merge sort's merge step.</b> When an item from the right half goes first, it's smaller than <i>everything still waiting</i> in the left half, so each of those forms an inversion, and you can count them all at once:</p>
<pre><code class="py">left = [2, 4]    right = [1, 3]
take 1: 2 items left in the left half → +2 inversions
take 2
take 3: 1 item left in the left half → +1
take 4</code></pre>
<p>That's 3 in total, in O(n log n). Many hard problems have this same shape: a brute-force pair count, sped up by sorted halves.</p>
""", practice=["Count Inversions"])


LESSON("Core", "String searching: KMP and rolling hash", """
<p>The simple search is O(n·m), because after a mismatch it starts again from the next position. Searching for "aaab" in "aaaaaaa" wastes a lot of work, since you knew those letters were all "a".</p>
<p><b>KMP</b> never moves backward in the text. It first computes, for each prefix of the pattern, the <b>longest proper prefix that's also a suffix</b>:</p>
<table><tr><th>Pattern</th><td>a</td><td>b</td><td>c</td><td>a</td><td>b</td><td>y</td></tr>
<tr><th>LPS</th><td>0</td><td>0</td><td>0</td><td>1</td><td>2</td><td>0</td></tr></table>
<p>At the second "b" the value is 2, because "ab" is both a prefix and a suffix of "abcab". Suppose you've matched "abcab" and the next letter fails. You already know the text ends in "ab", so you can carry on from position 2 in the pattern, without re-reading anything. That gives O(n + m).</p>
<p><b>Rabin-Karp</b> treats a window of text as a number, and updates it in O(1) as it slides:</p>
<pre><code class="py">new = (old − first_char × base^(m−1)) × base + next_char   (mod a large prime)</code></pre>
<p>If the hashes differ, it's definitely not a match. If they're equal, compare the actual text, since different strings can share a hash. It's expected O(n + m), and it extends well to searching for many patterns at once.</p>
<p>In Python, <code>in</code> and <code>str.find</code> are already well optimised, so only write these when asked. Interviewers are testing whether you can reason about re-using work.</p>
""", practice=["Substring Search With KMP", "All Matches With a Rolling Hash", "Longest Common Substring"])


LESSON("Core", "Union-find: who's connected?", """
<p>Suppose friends keep connecting and you need to ask "are these two in the same group?". Re-running a graph search each time is too slow.</p>
<p><b>Union-find</b> stores a forest: each item has a parent, and the root names the group.</p>
<pre><code class="py">find(x):   follow parents up to the root
union(a, b):  point one root at the other</code></pre>
<p>Two optimisations make it nearly O(1) per operation:</p>
<ul><li><b>Path compression:</b> while walking up, point nodes closer to the root.</li>
<li><b>Union by size:</b> attach the smaller tree under the larger one, so trees stay flat.</li></ul>
<p><b>Trace for 4 items:</b></p>
<table><tr><th>Operation</th><th>Result</th><th>Groups</th></tr>
<tr><td>union(0, 1)</td><td>True</td><td>3</td></tr><tr><td>union(1, 0)</td><td>False: already together</td><td>3</td></tr>
<tr><td>union(2, 3)</td><td>True</td><td>2</td></tr><tr><td>union(1, 2)</td><td>True</td><td>1</td></tr></table>
<p><b>When to think of it:</b> counting connected components, detecting a cycle in an undirected graph (a union returning False means a cycle), and Kruskal's minimum spanning tree.</p>
""", practice=["Union-Find"])


LESSON("Core", "Range queries: Fenwick and segment trees", """
<p>You have an array with updates and range questions. The simple options each have a slow side:</p>
<table><tr><th>Structure</th><th>Update</th><th>Range sum</th></tr>
<tr><td>Plain array</td><td>O(1)</td><td>O(n)</td></tr><tr><td>Prefix sums</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td><b>Fenwick tree</b></td><td>O(log n)</td><td>O(log n)</td></tr><tr><td><b>Segment tree</b></td><td>O(log n)</td><td>O(log n)</td></tr></table>
<p><b>Fenwick tree (binary indexed tree).</b> Each position stores a sum over a range whose length is its lowest set bit, found with <code>i &amp; -i</code>:</p>
<ul><li>To get prefix(7): 7 is 111 in binary. Add tree[7], tree[6], tree[4]: remove the lowest bit each time.</li>
<li>To update index 5: 101. Touch tree[5], tree[6], tree[8]: add the lowest bit each time.</li></ul>
<p>Every number has at most log n bits, so both are O(log n). The code is very short.</p>
<p><b>Segment tree.</b> A binary tree over the array where each node stores the answer for its range. It's longer to write, but handles any combinable operation, such as min, max or GCD, where prefix tricks can't help.</p>
<p>For [5, 2, 6, 3] with range minimum: leaves 5, 2, 6, 3; parents 2 and 3; root 2. A query for 2..3 reads one node: 3. After setting index 1 to 9, the left parent becomes 5, and the root becomes 3.</p>
<p>These come up less often than hash maps or graphs, so learn the others first. They're typical of competitive programming and of very strong companies.</p>
""", practice=["Fenwick Tree", "Segment Tree: Range Minimum", "Weighted Random Pick"])


LESSON("Core", "Designing data structures", """
<p>"Design X" questions test whether you can combine simple structures. The method is always this:</p>
<ol><li>List the operations and required costs.</li><li>Ask which single structure gets closest.</li><li>Add a second structure to fix what it does badly.</li></ol>
<table><tr><th>Design</th><th>Structures combined</th><th>Why</th></tr>
<tr><td>LRU cache</td><td>hash map + doubly linked list</td><td>find fast, and reorder fast</td></tr>
<tr><td>LFU cache</td><td>hash map + one ordered map per frequency</td><td>evict the lowest frequency, oldest first</td></tr>
<tr><td>Random pick</td><td>array + hash map of indices</td><td>random index, plus fast lookup</td></tr>
<tr><td>Time-based store</td><td>hash map of sorted lists</td><td>binary search over history</td></tr>
<tr><td>Hash map</td><td>array of buckets</td><td>hash picks a bucket; grow when crowded</td></tr></table>
<p><b>The swap trick.</b> To delete from an array in O(1), when order doesn't matter: move the last item into the hole, then pop. Removing 1 from [1, 2, 3]: copy 3 to index 0, pop, giving [3, 2], and update the map entry for 3.</p>
<p><b>How a hash map stays fast.</b> Load factor = items ÷ buckets. When buckets get crowded, double the array and re-insert everything. One resize is expensive, but it's rare enough that the average per insertion stays O(1), which is <b>amortised</b> analysis. Worst-case lookup is O(n) if everything collides.</p>
<p><b>Tip:</b> state the required costs out loud, because they usually point straight to the answer. "O(1) lookup" means a hash map. "Sorted, with inserts" means a heap or balanced tree.</p>
""", practice=["LFU Cache", "Time-Based Key-Value Store", "Design a Hash Map", "Insert, Delete, Random in O(1)"])


LESSON("Advanced", "Shortest paths: which algorithm?", """
<table><tr><th>Situation</th><th>Use</th><th>Cost</th></tr>
<tr><td>All edges cost the same</td><td>BFS</td><td>O(V + E)</td></tr>
<tr><td>Non-negative weights</td><td>Dijkstra</td><td>O(E log V)</td></tr>
<tr><td>Negative edges possible</td><td>Bellman-Ford</td><td>O(V·E)</td></tr>
<tr><td>All pairs, small graph</td><td>Floyd-Warshall</td><td>O(V³)</td></tr></table>
<p><b>Why does Dijkstra fail with negative edges?</b> It finalises a node as soon as it's the closest, assuming that no later path can improve it. A negative edge breaks that assumption.</p>
<p><b>Bellman-Ford</b> relaxes every edge, V − 1 times, since a shortest path has at most V − 1 edges. If a further round still improves something, there's a negative cycle.</p>
<p>Edges 0→1 (4), 0→2 (5), 1→2 (−3), 2→3 (2): 0→1 is 4, then 1→2 gives 4 − 3 = 1, which beats the direct 5, then 2→3 gives 3. Distances: 0, 4, 1, 3.</p>
<p><b>Floyd-Warshall</b> is three nested loops: for each middle node k, can going via k improve the route from i to j? The order matters: k must be the outermost loop.</p>
<p><b>Topological order, as in Alien Dictionary.</b> Each adjacent word pair gives one rule, from its first differing letter. "wrt" before "wrf" means t comes before f. Build a graph and repeatedly remove letters with nothing before them. If you get stuck, there's a cycle, so the input is inconsistent. One trap is "abc" before "ab", which is impossible.</p>
""", practice=["Bellman-Ford", "Floyd-Warshall", "Alien Dictionary"])


LESSON("Advanced", "Knapsack: the DP template", """
<p>Choose items with weights and values to maximise value within a capacity. Greedy by value-per-weight fails: with capacity 7 and items (weight, value) (1, 1), (3, 4), (4, 5), (5, 7), the best ratio is the (5, 7) item, and adding (1, 1) gives value 8. But (3, 4) + (4, 5) gives <b>9</b>.</p>
<p><b>State:</b> <code>dp[room]</code> is the best value using the items so far within that much room.</p>
<p><b>Choice for each item:</b> skip it, or take it: <code>dp[room] = max(dp[room], dp[room − w] + v)</code>.</p>
<p><b>Why loop the room downward?</b> Going upward would let an item use a value that already includes itself, so you'd use it twice. That's exactly the difference between 0/1 knapsack (downward) and unbounded knapsack (upward).</p>
<p>Trying all subsets is O(2ⁿ). The table is O(n·C), where C is the capacity. Note this is "pseudo-polynomial": it depends on the size of the number C, not just the number of items.</p>
<p>Many questions are knapsack in disguise: subset sum, partition into equal sums, target sum, and coin change.</p>
""", practice=["0/1 Knapsack"])
