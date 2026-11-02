from lib import *

THEORY("Definition", """
<p>A <b>heap</b> is a <b>complete binary tree</b> that satisfies the <b>heap property</b>:</p>
<ul>
<li><b>Min-heap</b>: every parent's key is ≤ its children's keys → the minimum is at the root.</li>
<li><b>Max-heap</b>: every parent's key is ≥ its children's keys → the maximum is at the root.</li>
</ul>
<p>A <b>priority queue</b> is an ADT where each element has a priority and the element with the highest priority is removed first. A binary heap is the standard way to implement it.</p>
<p>Note: a heap is <b>not sorted</b>. Siblings have no order between them; only the parent–child relationship is guaranteed.</p>
""")

THEORY("Array representation", """
<p>Because a heap is a complete tree, it is stored in an array with no gaps and no pointers. For a node at index i (0-based):</p>
<table>
<tr><th>Relation</th><th>Index</th></tr>
<tr><td>left child</td><td>2i + 1</td></tr>
<tr><td>right child</td><td>2i + 2</td></tr>
<tr><td>parent</td><td>(i − 1) // 2</td></tr>
<tr><td>leaves</td><td>indices n // 2 … n − 1</td></tr>
</table>
<p>Height of a heap with n nodes is ⌊log₂ n⌋.</p>
""")

THEORY("Operations", """
<table>
<tr><th>Operation</th><th>Steps</th><th>Time</th></tr>
<tr><td><b>Insert</b> (push)</td><td>append at the end, then <b>heapify-up</b> (sift up): swap with the parent while it violates the heap property</td><td>O(log n)</td></tr>
<tr><td><b>Extract-min/max</b> (pop)</td><td>save the root, move the last element to the root, then <b>heapify-down</b> (sift down): swap with the smaller (min-heap) child while it violates the property</td><td>O(log n)</td></tr>
<tr><td>Peek</td><td>read index 0</td><td>O(1)</td></tr>
<tr><td><b>Build heap</b> (heapify)</td><td>sift down every non-leaf from index n//2 − 1 down to 0</td><td><b>O(n)</b></td></tr>
<tr><td>Decrease / increase key</td><td>change the value, sift up or down</td><td>O(log n) (if index known)</td></tr>
<tr><td>Search arbitrary value</td><td>scan</td><td>O(n)</td></tr>
<tr><td>Delete arbitrary element</td><td>find, swap with last, sift</td><td>O(n) find + O(log n)</td></tr>
</table>
<h4>Why build-heap is O(n), not O(n log n)</h4>
<p>Most nodes are near the bottom and sift down only a little. About n/2 nodes are leaves (0 work), n/4 sift down at most 1 level, n/8 at most 2 levels, and so on. The total Σ (n / 2ᵏ⁺¹) · k is bounded by n, so building a heap from an array is linear.</p>
""")

THEORY("Heap sort", """
<ol>
<li>Build a max-heap from the array — O(n).</li>
<li>Repeat n times: swap the root (max) with the last element of the heap, shrink the heap by one, and sift down the new root — O(log n) each.</li>
</ol>
<p>Total <b>O(n log n)</b> in all cases, <b>O(1)</b> extra space (in place), but <b>not stable</b> and usually slower than quicksort in practice due to poor cache use.</p>
""")

THEORY("Python's heapq", """
<table>
<tr><th>Function</th><th>Does</th><th>Time</th></tr>
<tr><td><code>heappush(h, x)</code></td><td>insert</td><td>O(log n)</td></tr>
<tr><td><code>heappop(h)</code></td><td>remove smallest</td><td>O(log n)</td></tr>
<tr><td><code>heapify(lst)</code></td><td>build in place</td><td>O(n)</td></tr>
<tr><td><code>heappushpop(h, x)</code></td><td>push then pop (faster than both)</td><td>O(log n)</td></tr>
<tr><td><code>heapreplace(h, x)</code></td><td>pop then push</td><td>O(log n)</td></tr>
<tr><td><code>nlargest(k, it)</code> / <code>nsmallest</code></td><td>top k</td><td>O(n log k)</td></tr>
</table>
<p><code>heapq</code> implements a <b>min-heap</b> only. Max-heap: store negated values. Custom priority: store tuples <code>(priority, counter, item)</code>; the counter breaks ties and avoids comparing items.</p>
""")

THEORY("Comparison and applications", """
<table>
<tr><th>Structure</th><th>insert</th><th>get min</th><th>remove min</th><th>search</th></tr>
<tr><td>Unsorted array</td><td>O(1)</td><td>O(n)</td><td>O(n)</td><td>O(n)</td></tr>
<tr><td>Sorted array</td><td>O(n)</td><td>O(1)</td><td>O(1) (from the end)</td><td>O(log n)</td></tr>
<tr><td><b>Binary heap</b></td><td>O(log n)</td><td>O(1)</td><td>O(log n)</td><td>O(n)</td></tr>
<tr><td>Balanced BST</td><td>O(log n)</td><td>O(log n)</td><td>O(log n)</td><td>O(log n)</td></tr>
</table>
<h4>Applications</h4>
<ul>
<li>Operating system and job scheduling by priority.</li>
<li><b>Dijkstra's</b> and <b>Prim's</b> algorithms; A* search.</li>
<li>Event-driven simulation (process the earliest event next).</li>
<li>Top-k queries, leaderboards, streaming medians.</li>
<li>Merging k sorted files (external sorting); Huffman coding.</li>
<li>Load balancing (send work to the least-loaded server).</li>
</ul>
""")

FAQ("Is a heap sorted?", "<p>No. Only parent–child order is guaranteed, so you can read the min (or max) in O(1), but getting all elements in order requires popping them one by one (heap sort).</p>")
FAQ("Why is building a heap O(n)?", "<p>Sift-down cost depends on a node's height. Half the nodes are leaves (no work), a quarter move at most one level, an eighth at most two… The sum of heights over all nodes is O(n).</p>")
FAQ("How do you get a max-heap with heapq?", "<p>Push <code>-x</code> and negate when you pop. For tuples, negate the priority field.</p>")
FAQ("Heap vs BST for a priority queue?", "<p>Both give O(log n) insert and delete-min. A heap is simpler, uses an array (better cache, less memory) and builds in O(n). A balanced BST also supports search, delete-any and sorted iteration in O(log n), which a heap doesn't.</p>")
FAQ("How do you find the k largest elements efficiently?", "<p>Keep a min-heap of size k: push each element and pop when the size exceeds k. The heap holds the k largest; its root is the k-th largest. O(n log k) time, O(k) space. Quickselect gives O(n) average.</p>")
FAQ("How does a running median work with heaps?", "<p>A max-heap stores the lower half, a min-heap the upper half, sizes kept within one. The median is one root or the average of both roots: O(log n) per insert, O(1) per query.</p>")
FAQ("Is heap sort stable?", "<p>No. Swapping the root with the last element can reorder equal keys. It is O(n log n) in every case and in place.</p>")
