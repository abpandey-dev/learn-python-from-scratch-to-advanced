from lib import *

LESSON("Basics", "What an array really is", """
<p>An <b>array</b> is a row of boxes placed side by side in memory. Every box has a number called its <b>index</b>, starting at 0. In Python, a <code>list</code> is an array.</p>
<div class="pic">nums  = [ 7 | 3 | 9 | 4 ]
index    0   1   2   3</div>
<p>Because the boxes are next to each other and all the same size, the computer can jump straight to box <code>i</code> with one calculation: <i>start address + i × box size</i>. That is why <code>nums[i]</code> takes the same time for index 2 or index 2,000,000. We write this as <b>O(1)</b> — "constant time".</p>
<h4>How a Python list grows</h4>
<p>A list keeps some spare boxes at the end. <code>append</code> just fills the next spare box (fast). When the spare boxes run out, Python makes a <b>bigger</b> block (about double), copies everything, and continues. Copying is slow, but it happens rarely, so on average <code>append</code> is still O(1). This is called <b>amortised O(1)</b>.</p>
<div class="tip">Rule of thumb: reading or writing by index and appending at the end are cheap. Anything that has to move many elements is expensive.</div>
""", practice=[217])


@LD
def append_growth():
    capacity, size, boxes = 1, 0, [None]
    for x in [5, 8, 2, 6, 1]:
        if size == capacity:
            capacity *= 2
            boxes = boxes[:size] + [None] * (capacity - size)
            T(f"No space left → allocate {capacity} boxes and copy the {size} old values", A("memory", boxes, ok=range(size)), V(size=size, capacity=capacity))
        boxes[size] = x
        size += 1
        T(f"append({x}) fills box {size - 1}", A("memory", boxes, ok=range(size), hl=[size - 1]), V(size=size, capacity=capacity), at="prev")
    return boxes


LESSON("Basics", "Insert, delete and search — what they cost", """
<p>Adding or removing at the <b>end</b> is cheap. Doing it at the <b>front or middle</b> is expensive, because every element after that spot must move one box over.</p>
<table>
<tr><th>Operation</th><th>Python</th><th>Cost</th><th>Why</th></tr>
<tr><td>read / write index i</td><td><code>a[i]</code></td><td>O(1)</td><td>direct jump</td></tr>
<tr><td>add at end</td><td><code>a.append(x)</code></td><td>O(1)*</td><td>fills a spare box</td></tr>
<tr><td>remove at end</td><td><code>a.pop()</code></td><td>O(1)</td><td>nothing moves</td></tr>
<tr><td>insert at i</td><td><code>a.insert(i, x)</code></td><td>O(n)</td><td>shift everything after i right</td></tr>
<tr><td>remove at i</td><td><code>a.pop(i)</code></td><td>O(n)</td><td>shift everything after i left</td></tr>
<tr><td>search for a value</td><td><code>x in a</code>, <code>a.index(x)</code></td><td>O(n)</td><td>must look at every box</td></tr>
<tr><td>copy a slice</td><td><code>a[i:j]</code></td><td>O(j − i)</td><td>creates a new list</td></tr>
</table>
<div class="warn">A hidden <code>x in a</code> or <code>a.pop(0)</code> inside a loop turns an O(n) solution into O(n²). Interviewers look for this.</div>
""")


@LD
def insert_shift():
    a = [10, 20, 30, 40, 50]
    i, x = 1, 15
    a.append(None)
    for k in range(len(a) - 1, i, -1):
        a[k] = a[k - 1]
        T(f"Shift a[{k - 1}] one box right", A("a", a, hl=[k], k=k))
    a[i] = x
    T(f"Now box {i} is free → place {x}. That took {len(a) - 1 - i} moves.", A("a", a, ok=[i]))
    return a


LESSON("Core", "Hash maps and hash sets", """
<p>Searching a list for a value is O(n). A <b>hash set</b> (<code>set</code>) and a <b>hash map</b> (<code>dict</code>) make that search O(1) on average.</p>
<h4>How it works</h4>
<ol>
<li>A <b>hash function</b> turns the key into a number, e.g. <code>hash(42)</code>.</li>
<li>That number, modulo the number of buckets, picks a <b>bucket</b>.</li>
<li>The key (and its value) is stored in that bucket. To look it up later, compute the same bucket and check only there.</li>
</ol>
<p>Two keys can land in the same bucket — a <b>collision</b>. The bucket then holds a short list. Python grows the table when it gets too full, so buckets stay short and lookups stay O(1) on average (O(n) only in a very unlucky worst case).</p>
<table>
<tr><th>You want</th><th>Use</th></tr>
<tr><td>"have I seen x?"</td><td><code>seen = set()</code>, <code>x in seen</code></td></tr>
<tr><td>remember something about x (index, count)</td><td><code>d = {}</code>, <code>d[x] = i</code></td></tr>
<tr><td>count things</td><td><code>collections.Counter(nums)</code></td></tr>
<tr><td>group things</td><td><code>collections.defaultdict(list)</code></td></tr>
</table>
<div class="tip">Keys must be <b>hashable</b> (unchangeable): numbers, strings, tuples. A list can't be a key — convert it with <code>tuple(lst)</code>.</div>
""", practice=[217, 242])


@LD
def hashing_demo():
    buckets = [[] for _ in range(5)]
    for key in [12, 7, 33, 22, 5, 18]:
        b = key % 5
        buckets[b].append(key)
        T(f"hash({key}) % 5 = {b} → put {key} in bucket {b}", A("buckets", [buckets[i] for i in range(5)], hl=[b]), at="prev")
    key = 22
    b = key % 5
    T(f"Look up {key}: go straight to bucket {b} and check only {buckets[b]}", A("buckets", [buckets[i] for i in range(5)], ok=[b]), V(found=key in buckets[b]))
    return buckets


LESSON("Core", "Pattern: remember what you have seen", """
<p>Many "find a pair" problems look like they need two loops. The trick: walk the array <b>once</b> and keep a dict of what you've already passed. For each new element, ask the dict a question in O(1).</p>
<pre><code class="py"># Two Sum: is there an earlier number equal to target - x?
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i</code></pre>
<p>The same idea covers many problems — only the <i>question</i> changes:</p>
<ul>
<li><b>Duplicates</b>: "is x already in the set?"</li>
<li><b>Anagrams</b>: count letters with a dict; two words are anagrams when their counts match.</li>
<li><b>Grouping</b>: build a key that is equal for items in the same group (sorted letters, or a 26-count tuple), and use <code>defaultdict(list)</code>.</li>
<li><b>Top-k frequent</b>: count first, then pick the largest counts (bucket sort makes it O(n)).</li>
</ul>
""", practice=[1, 49, 347, 128])


LESSON("Core", "Prefix sums", """
<p>A <b>prefix sum</b> array stores running totals: <code>pre[i]</code> = sum of the first <code>i</code> elements. Building it is one pass, O(n).</p>
<div class="pic">nums = [3, 1, 4, 1, 5]
pre  = [0, 3, 4, 8, 9, 14]      pre[0] = 0 (nothing added yet)</div>
<p>Then the sum of any range <code>nums[l..r]</code> is just <b>one subtraction</b>: <code>pre[r + 1] − pre[l]</code>. Without it, each range sum is a loop.</p>
<h4>Prefix sums + hash map</h4>
<p>To count subarrays that sum to <code>k</code>: a subarray ending at <code>i</code> sums to <code>k</code> when some earlier prefix equals <code>pre − k</code>. Keep a dict counting each prefix value seen so far (start with <code>{0: 1}</code> for the empty prefix). This works even with negative numbers, where sliding window fails.</p>
<p>The same "running" idea gives <b>prefix products</b> (product of array except self) and <b>suffix</b> arrays scanned from the right.</p>
""", practice=[238, 560])


LESSON("Advanced", "Running state: Kadane and one-pass scans", """
<p>Some problems only need a few variables updated as you walk the array — no extra arrays at all.</p>
<h4>Kadane's algorithm (maximum subarray)</h4>
<p>Keep <code>cur</code> = the best sum of a subarray that <b>ends at the current index</b>. At each element you have two choices: extend the previous subarray or start fresh here.</p>
<pre><code class="py">cur = best = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)   # extend or restart
    best = max(best, cur)</code></pre>
<p>Why restart? If <code>cur</code> is negative, carrying it only makes the next sum smaller.</p>
<h4>Other one-pass ideas</h4>
<ul>
<li><b>Running minimum</b> (best time to buy and sell): track the cheapest price so far; profit today = price − cheapest.</li>
<li><b>Voting</b> (majority element): a candidate and a counter; equal → +1, different → −1.</li>
</ul>
""", practice=[53, 121, 169])


@LD
def kadane_lesson():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5]
    cur = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        choice = "restart at " + str(x) if x > cur + x else "extend to " + str(cur + x)
        cur = max(x, cur + x)
        best = max(best, cur)
        T(f"x = {x}: {choice}", A("nums", nums, hl=[i], i=i), V(cur=cur, best=best), at="prev")
    return best


LESSON("Advanced", "In-place tricks and matrices", """
<p>"Use O(1) extra space" means: no new arrays — rearrange the input itself.</p>
<ul>
<li><b>Write pointer</b>: one index reads, another writes the elements you keep (move zeroes).</li>
<li><b>Reverse trick</b>: rotating by k = reverse all, reverse first k, reverse the rest.</li>
<li><b>Value as index</b>: when values are 1..n, value v can point to index v (find duplicate as a cycle, or mark seen by making <code>nums[v−1]</code> negative).</li>
<li><b>Three-way partition</b> (Dutch flag): pointers for the 0-zone, the 2-zone and the scanner.</li>
</ul>
<h4>2-D arrays (matrices)</h4>
<p>A matrix is a list of rows: <code>grid[r][c]</code>. <code>m = len(grid)</code> rows, <code>n = len(grid[0])</code> columns. Common moves:</p>
<ul>
<li><b>Transpose</b>: swap <code>grid[r][c]</code> with <code>grid[c][r]</code> for <code>c &gt; r</code>.</li>
<li><b>Rotate 90° clockwise</b> = transpose + reverse each row.</li>
<li><b>Spiral</b>: keep four walls (top, bottom, left, right) and shrink them.</li>
<li><b>Flatten an index</b>: cell k ↔ <code>(k // n, k % n)</code>.</li>
</ul>
<div class="warn"><code>[[0] * n] * m</code> creates m references to the <b>same</b> row. Use <code>[[0] * n for _ in range(m)]</code>.</div>
""", practice=[283, 189, 75, 287, 48, 54, 73])


@LD
def mark_negative():
    nums = [4, 3, 2, 7, 8, 2, 3, 1]
    dup = []
    for i in range(len(nums)):
        v = abs(nums[i])
        if nums[v - 1] < 0:
            dup.append(v)
            T(f"Value {v}: box {v - 1} is already negative → {v} is a duplicate", A("nums", nums, hl=[i], bad=[v - 1], i=i), V(duplicates=dup))
        else:
            nums[v - 1] = -nums[v - 1]
            T(f"Value {v}: mark box {v - 1} as seen by making it negative", A("nums", nums, hl=[i], ok=[v - 1], i=i), V(duplicates=dup), at="prev")
    return dup
