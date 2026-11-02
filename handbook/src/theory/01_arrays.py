from lib import *

THEORY("Definition", """
<p>An <b>array</b> is a <b>linear data structure</b> that stores a collection of elements in <b>contiguous</b> (side-by-side) memory locations. Each element is identified by an <b>index</b>; in most languages, including Python, indexing starts at 0.</p>
<p>Because the elements are contiguous and of equal size, the address of element i is computed directly:</p>
<div class="pic">address(a[i]) = base_address + i × element_size</div>
<p>This formula is why arrays support <b>random access</b> — reaching any index in O(1) time.</p>
<p>A <b>hash table</b> is a data structure that maps <b>keys</b> to <b>values</b> using a <b>hash function</b> to compute an index (bucket) where each key is stored. Python's <code>dict</code> (key → value) and <code>set</code> (keys only) are hash tables.</p>
""")

THEORY("Types of arrays", """
<table>
<tr><th>Type</th><th>Meaning</th><th>Example</th></tr>
<tr><td><b>Static array</b></td><td>size fixed when created</td><td>C <code>int a[10]</code>, Java <code>int[]</code></td></tr>
<tr><td><b>Dynamic array</b></td><td>grows automatically by reallocating a larger block</td><td>Python <code>list</code>, Java <code>ArrayList</code>, C++ <code>vector</code></td></tr>
<tr><td><b>1-D array</b></td><td>a single row of elements</td><td><code>[3, 1, 4]</code></td></tr>
<tr><td><b>2-D array (matrix)</b></td><td>rows × columns; stored row by row (row-major) in C/Python</td><td><code>grid[r][c]</code></td></tr>
<tr><td><b>Multi-dimensional</b></td><td>3 or more indices</td><td>images (height × width × colour)</td></tr>
<tr><td><b>Jagged array</b></td><td>rows of different lengths</td><td><code>[[1], [2, 3], [4, 5, 6]]</code></td></tr>
</table>
<p><b>Strings</b> are arrays of characters. In Python they are <b>immutable</b>: <code>s[0] = "x"</code> is an error, and <code>s += c</code> in a loop copies the string each time (O(n²) overall) — build a list and <code>"".join()</code> it instead.</p>
""")

THEORY("Operations and their time complexity", """
<table>
<tr><th>Operation</th><th>How it works</th><th>Time</th></tr>
<tr><td>Access <code>a[i]</code></td><td>address formula</td><td>O(1)</td></tr>
<tr><td>Update <code>a[i] = x</code></td><td>address formula</td><td>O(1)</td></tr>
<tr><td>Traverse</td><td>visit each element once</td><td>O(n)</td></tr>
<tr><td>Linear search</td><td>compare with each element</td><td>O(n)</td></tr>
<tr><td>Binary search (sorted)</td><td>halve the range each step</td><td>O(log n)</td></tr>
<tr><td>Insert at end (dynamic)</td><td>use spare capacity; resize when full</td><td>O(1) amortised</td></tr>
<tr><td>Insert at index i</td><td>shift n − i elements right</td><td>O(n)</td></tr>
<tr><td>Delete at index i</td><td>shift n − i − 1 elements left</td><td>O(n)</td></tr>
<tr><td>Sort</td><td>Timsort in Python</td><td>O(n log n)</td></tr>
</table>
<h4>Amortised O(1) append — why</h4>
<p>When a dynamic array is full it allocates double the capacity and copies every element. Starting from capacity 1 and appending n items, the copies cost 1 + 2 + 4 + … + n/2 &lt; n in total. Adding the n writes themselves, n appends cost less than 2n operations, so each append costs O(1) <b>on average</b>, even though one particular append can cost O(n).</p>
""")

THEORY("Hashing in depth", """
<h4>Hash function</h4>
<p>Converts a key into an integer. A good hash function is <b>deterministic</b> (same key → same hash), <b>fast</b>, and spreads keys <b>uniformly</b> across buckets. The bucket is usually <code>hash(key) % number_of_buckets</code>.</p>
<h4>Collisions and how they are resolved</h4>
<p>A <b>collision</b> happens when two keys map to the same bucket. Two main strategies:</p>
<ul>
<li><b>Separate chaining</b>: each bucket stores a list of entries. Lookup scans that short list.</li>
<li><b>Open addressing</b>: all entries live in the array itself; on collision, <b>probe</b> other slots — linear probing (next slot), quadratic probing, or double hashing. Python's <code>dict</code> uses open addressing.</li>
</ul>
<h4>Load factor and rehashing</h4>
<p><b>Load factor</b> α = number of entries ÷ number of buckets. As α grows, collisions increase. When α passes a threshold (about 2/3 in Python), the table <b>rehashes</b>: allocates more buckets and reinserts every key. Like array resizing, this keeps operations O(1) amortised.</p>
<table>
<tr><th>Operation</th><th>Average</th><th>Worst case (all keys collide)</th></tr>
<tr><td>insert / lookup / delete</td><td>O(1)</td><td>O(n)</td></tr>
</table>
<p>Only <b>immutable</b> (hashable) objects can be keys: int, str, tuple, frozenset. Lists and dicts can't — their hash would change if they changed.</p>
""")

THEORY("Advantages and disadvantages", """
<div class="two">
<div class="pro"><h5>Arrays — advantages</h5><ul><li>O(1) random access by index</li><li>Cache-friendly: neighbouring elements are loaded together, so traversal is very fast in practice</li><li>No extra memory per element (no pointers)</li><li>Simple to use; the basis of most other structures</li></ul></div>
<div class="con"><h5>Arrays — disadvantages</h5><ul><li>Insert/delete in the middle costs O(n)</li><li>Static arrays have a fixed size; dynamic arrays waste some spare capacity</li><li>Searching an unsorted array is O(n)</li><li>Need one large contiguous block of memory</li></ul></div>
<div class="pro"><h5>Hash tables — advantages</h5><ul><li>O(1) average insert, lookup and delete by key</li><li>Keys can be strings, tuples, etc., not just 0..n−1</li><li>Ideal for counting, de-duplication and caching</li></ul></div>
<div class="con"><h5>Hash tables — disadvantages</h5><ul><li>No ordering by key (no "smallest key" or range query)</li><li>O(n) worst case with bad hashing</li><li>More memory than an array (empty buckets, stored hashes)</li><li>Keys must be hashable</li></ul></div>
</div>
""")

THEORY("Applications", """
<ul>
<li><b>Arrays</b>: lookup tables, images and matrices, buffers, implementing stacks, queues, heaps and hash tables themselves, dynamic programming tables.</li>
<li><b>Prefix sums</b>: fast range-sum queries in analytics, 2-D prefix sums for image processing (summed-area tables).</li>
<li><b>Hash maps</b>: database indexes, caches (memoisation, LRU caches), counting word frequencies, symbol tables in compilers, de-duplicating records, sets of visited states in search.</li>
</ul>
""")

THEORY("Array vs linked list vs hash table", """
<table>
<tr><th></th><th>Array</th><th>Linked list</th><th>Hash table</th></tr>
<tr><td>Access by position</td><td>O(1)</td><td>O(n)</td><td>—</td></tr>
<tr><td>Search by value / key</td><td>O(n), O(log n) if sorted</td><td>O(n)</td><td>O(1) avg</td></tr>
<tr><td>Insert / delete at front</td><td>O(n)</td><td>O(1)</td><td>O(1) avg</td></tr>
<tr><td>Insert / delete at end</td><td>O(1) amortised</td><td>O(1) with tail pointer</td><td>—</td></tr>
<tr><td>Keeps order</td><td>yes</td><td>yes</td><td>insertion order in Python 3.7+, not sorted</td></tr>
<tr><td>Memory</td><td>compact</td><td>extra pointer per node</td><td>extra empty buckets</td></tr>
</table>
""")

FAQ("Why does array indexing start at 0?", "<p>The index is an <b>offset</b> from the start address: element i lives at <code>base + i × size</code>. The first element is at offset 0, so its index is 0. This avoids an extra subtraction on every access.</p>")
FAQ("What is the difference between a static and a dynamic array?", "<p>A static array has a fixed size chosen at creation. A dynamic array (Python list) grows automatically: when full, it allocates a bigger block (about 1.125–2× in practice), copies the elements, and frees the old block. Appends are O(1) amortised.</p>")
FAQ("Explain amortised O(1) for append.", "<p>Most appends just write into spare capacity (O(1)). Occasionally the array is full and must copy all n elements (O(n)). Because the capacity doubles, those expensive copies happen rarely: n appends cost under 2n total work, so the <b>average</b> per append is O(1).</p>")
FAQ("How does a hash map achieve O(1) lookup? When is it O(n)?", "<p>The hash function turns the key into a bucket index, so lookup checks one bucket instead of every element. With a good hash function and a bounded load factor, buckets hold O(1) entries on average. If many keys collide into the same bucket (bad hash or an attack), lookup degrades to O(n).</p>")
FAQ("What is a collision and how is it handled?", "<p>Two keys hashing to the same bucket. <b>Chaining</b> stores a list in each bucket; <b>open addressing</b> probes for another free slot (linear, quadratic, double hashing). Both keep working correctly; they differ in memory use and cache behaviour.</p>")
FAQ("Why can't a Python list be a dictionary key?", "<p>Lists are mutable. If a list changed after insertion, its hash would change and the dict would look in the wrong bucket. Only immutable (hashable) types — int, str, tuple of hashables, frozenset — can be keys. Convert with <code>tuple(lst)</code>.</p>")
FAQ("Subarray vs subsequence vs subset?", "<p><b>Subarray</b>: contiguous piece, order kept (n(n+1)/2 of them). <b>Subsequence</b>: any elements, order kept, gaps allowed (2ⁿ). <b>Subset</b>: any elements, order doesn't matter (2ⁿ).</p>")
FAQ("What is the time complexity of <code>x in list</code> vs <code>x in set</code>?", "<p><code>x in list</code> scans the list: O(n). <code>x in set</code> hashes x and checks one bucket: O(1) on average. Inside a loop this is the difference between O(n²) and O(n).</p>")
