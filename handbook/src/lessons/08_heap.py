from lib import *

LESSON("Basics", "What a priority queue is", """
<p>A normal queue serves people in arrival order. A <b>priority queue</b> always serves the <b>most important</b> item next — like an emergency room. You need two fast operations: add an item, and remove the smallest (or largest).</p>
<table>
<tr><th>Option</th><th>add</th><th>remove min</th></tr>
<tr><td>unsorted list</td><td>O(1)</td><td>O(n) — search</td></tr>
<tr><td>sorted list</td><td>O(n) — shift</td><td>O(1)</td></tr>
<tr><td><b>binary heap</b></td><td><b>O(log n)</b></td><td><b>O(log n)</b></td></tr>
</table>
<p>A heap is the best of both: never fully sorted, but always knows its smallest item.</p>
""")


LESSON("Basics", "How a heap is stored", """
<p>A <b>min-heap</b> is a binary tree where every parent ≤ its children, filled level by level from left to right. Because it's always that compact shape, it fits in a plain list with no pointers:</p>
<div class="pic">index i → children 2i + 1 and 2i + 2, parent (i − 1) // 2

heap = [1, 3, 2, 7, 4]          1
                              /   \\
                             3     2
                            / \\
                           7   4</div>
<ul>
<li><b>Push</b>: put the new value at the end, then <b>sift up</b> — swap with the parent while it is smaller.</li>
<li><b>Pop</b>: take <code>heap[0]</code>, move the last value to the root, then <b>sift down</b> — swap with the smaller child while it is bigger.</li>
</ul>
<p>The tree has about log₂ n levels, so each sift is O(log n). Building a heap from n items with <code>heapify</code> is O(n).</p>
""")


@LD
def sift_lesson():
    heap = [1, 3, 2, 7, 4]
    heap.append(0)
    i = len(heap) - 1
    T("push(0): place it at the end", H("heap", heap, hl=[i]), A("list", heap, hl=[i]))
    while i > 0 and heap[(i - 1) // 2] > heap[i]:
        p = (i - 1) // 2
        heap[i], heap[p] = heap[p], heap[i]
        i = p
        T(f"Parent is bigger → swap up to index {i}", H("heap", heap, hl=[i]), A("list", heap, hl=[i]), at="prev")
    top = heap[0]
    heap[0] = heap.pop()
    i = 0
    T(f"pop() returns {top}; the last value moves to the root", H("heap", heap, hl=[0]), A("list", heap, hl=[0]))
    while True:
        l, r, small = 2 * i + 1, 2 * i + 2, i
        if l < len(heap) and heap[l] < heap[small]:
            small = l
        if r < len(heap) and heap[r] < heap[small]:
            small = r
        if small == i:
            break
        heap[i], heap[small] = heap[small], heap[i]
        i = small
        T(f"A child is smaller → swap down to index {i}", H("heap", heap, hl=[i]), A("list", heap, hl=[i]), at="prev")
    return heap


LESSON("Core", "Using heapq in Python", """
<pre><code class="py">import heapq
h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappop(h)          # 1 — always the smallest
h[0]                      # peek the smallest without removing
heapq.heapify(nums)       # turn a list into a heap in O(n)
heapq.nlargest(3, nums)   # convenience helpers</code></pre>
<h4>Max-heap</h4>
<p><code>heapq</code> is min-only. For a max-heap push <code>-x</code> and negate again when popping.</p>
<h4>Custom priority</h4>
<p>Push tuples: <code>(priority, tiebreak, item)</code>. Tuples compare element by element, so the first field decides. Add an index as tiebreak when items themselves can't be compared (like nodes).</p>
""", practice=[1046, 1962, 264])


LESSON("Core", "Top-k with a heap of size k", """
<p>"Find the k largest" — sorting is O(n log n). Better: keep a <b>min</b>-heap of at most k items. For each new item push it; if the heap grows past k, pop the smallest. What remains are the k largest, and <code>heap[0]</code> is the k-th largest.</p>
<pre><code class="py">for x in nums:
    heapq.heappush(h, x)
    if len(h) &gt; k:
        heapq.heappop(h)</code></pre>
<p>Cost O(n log k), memory O(k) — great when k is small or data is a stream. It feels backwards (min-heap for largest), so explain it in interviews: "the heap's top is the weakest of my current top k, so it's the one to kick out".</p>
<p>For "k closest" use a max-heap of size k on distance (push negative distance).</p>
""", practice=[215, 703, 973, 692])


LESSON("Core", "Merging k sorted things", """
<p>When you have k sorted lists (or rows of a matrix, or a sorted grid of pair sums), the next smallest overall item is always one of the k current heads. Keep those heads in a heap:</p>
<ol>
<li>Push the first item of every list (with its list index and position).</li>
<li>Pop the smallest, output it, and push the next item from the same list.</li>
</ol>
<p>The heap never holds more than k items, so each step is O(log k). Used in merge k lists, k-th smallest in a sorted matrix, k pairs with smallest sums, and smallest range covering k lists (also track the current max).</p>
""", practice=[378, 373, 632])


LESSON("Advanced", "Two heaps for a running median", """
<p>Keep the smaller half of the numbers in a <b>max-heap</b> (<code>low</code>) and the larger half in a <b>min-heap</b> (<code>high</code>), with sizes equal or <code>low</code> one bigger. Then:</p>
<ul>
<li>the median is <code>low</code>'s top (odd count) or the average of both tops (even count) — O(1);</li>
<li>adding a number: push into <code>low</code>, move <code>low</code>'s top to <code>high</code>, and if <code>high</code> becomes bigger move its top back — O(log n).</li>
</ul>
<p>The two-heap idea also appears in sliding-window median and in "IPO"-style problems with one heap of locked items and one of available items.</p>
""", practice=[295, 502])


LESSON("Advanced", "Greedy scheduling with a heap", """
<p>A very common hard-problem pattern: <b>sort by time</b>, then sweep, and use a heap to always pick the best option <i>currently available</i>.</p>
<ul>
<li><b>Meeting rooms</b>: sort by start; a min-heap of end times tells you whether the earliest-finishing room is free.</li>
<li><b>Single-threaded CPU</b>: sort tasks by arrival; push every task that has arrived; run the shortest.</li>
<li><b>Task scheduler</b>: max-heap of remaining counts plus a cooldown queue.</li>
<li><b>Furthest building</b>: push every climb; when climbs exceed ladders, pay for the smallest climb with bricks.</li>
<li><b>Maximum subsequence score</b>: sort by the multiplier descending; keep the k largest sums in a min-heap.</li>
</ul>
""", practice=[253, 1834, 621, 1642, 2542, 846, 767, 451])
