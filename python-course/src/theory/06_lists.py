from lib import *

THEORY("Definition", """
<p>A <b>list</b> is an <b>ordered</b>, <b>mutable</b> collection that can hold items of any type, including duplicates. It is written with square brackets: <code>[1, "two", 3.0]</code>.</p>
<ul>
<li><b>Ordered</b> — items keep the position you gave them and are accessed by index.</li>
<li><b>Mutable</b> — items can be added, removed or replaced after creation.</li>
<li><b>Heterogeneous</b> — different types can be mixed.</li>
<li><b>Dynamic</b> — grows and shrinks automatically.</li>
</ul>
<p>Internally CPython implements a list as a <b>dynamic array of references</b> to objects.</p>
""")

THEORY("Creating lists", """
<table>
<tr><th>Way</th><th>Example</th></tr>
<tr><td>Literal</td><td><code>[1, 2, 3]</code>, <code>[]</code></td></tr>
<tr><td>From an iterable</td><td><code>list("abc")</code>, <code>list(range(5))</code></td></tr>
<tr><td>Repetition</td><td><code>[0] * 5</code></td></tr>
<tr><td>Comprehension</td><td><code>[x * x for x in range(5)]</code></td></tr>
<tr><td>From splitting</td><td><code>"a,b".split(",")</code></td></tr>
</table>
""")

THEORY("Methods and operations", """
<table>
<tr><th>Method / operation</th><th>Description</th><th>Time</th></tr>
<tr><td><code>append(x)</code></td><td>add to the end</td><td>O(1)*</td></tr>
<tr><td><code>extend(it)</code> / <code>+=</code></td><td>add all items of an iterable</td><td>O(k)</td></tr>
<tr><td><code>insert(i, x)</code></td><td>insert before index i</td><td>O(n)</td></tr>
<tr><td><code>remove(x)</code></td><td>remove first x, ValueError if absent</td><td>O(n)</td></tr>
<tr><td><code>pop()</code> / <code>pop(i)</code></td><td>remove and return last / i-th item</td><td>O(1) / O(n)</td></tr>
<tr><td><code>clear()</code></td><td>remove all items</td><td>O(n)</td></tr>
<tr><td><code>index(x)</code></td><td>first position of x</td><td>O(n)</td></tr>
<tr><td><code>count(x)</code></td><td>number of x</td><td>O(n)</td></tr>
<tr><td><code>sort(key=, reverse=)</code></td><td>sort in place (stable Timsort)</td><td>O(n log n)</td></tr>
<tr><td><code>reverse()</code></td><td>reverse in place</td><td>O(n)</td></tr>
<tr><td><code>copy()</code></td><td>shallow copy</td><td>O(n)</td></tr>
<tr><td><code>a[i]</code>, <code>len(a)</code></td><td>index, length</td><td>O(1)</td></tr>
<tr><td><code>x in a</code></td><td>membership</td><td>O(n)</td></tr>
<tr><td><code>a[i:j:k]</code></td><td>slice (new list)</td><td>O(slice length)</td></tr>
<tr><td><code>del a[i:j]</code> / slice assignment</td><td>delete or replace a range</td><td>O(n)</td></tr>
</table>
<p>* amortised. Useful built-ins: <code>len, sum, min, max, sorted, reversed, enumerate, zip, any, all</code>.</p>
""")

THEORY("References, aliasing and copying", """
<p>A variable holds a <b>reference</b> to a list object. Assigning or passing a list copies the reference, not the list.</p>
<table>
<tr><th>Operation</th><th>New outer list?</th><th>Inner objects</th></tr>
<tr><td><code>b = a</code></td><td>no (alias)</td><td>shared</td></tr>
<tr><td><code>a[:]</code>, <code>a.copy()</code>, <code>list(a)</code></td><td>yes (<b>shallow copy</b>)</td><td>shared</td></tr>
<tr><td><code>copy.deepcopy(a)</code></td><td>yes (<b>deep copy</b>)</td><td>copied recursively</td></tr>
</table>
<p>Pitfalls caused by aliasing:</p>
<ul>
<li><code>[[0] * 3] * 2</code> creates two references to one inner list.</li>
<li>A mutable <b>default argument</b> (<code>def f(x, acc=[])</code>) is shared between calls.</li>
<li>Functions that modify a list argument change the caller's list.</li>
</ul>
""")

THEORY("List vs other sequences", """
<table>
<tr><th></th><th>list</th><th>tuple</th><th>array.array</th><th>collections.deque</th></tr>
<tr><td>Mutable</td><td>yes</td><td>no</td><td>yes</td><td>yes</td></tr>
<tr><td>Item types</td><td>any</td><td>any</td><td>one numeric type</td><td>any</td></tr>
<tr><td>Fast ends</td><td>right end</td><td>—</td><td>right end</td><td><b>both ends</b></td></tr>
<tr><td>Hashable</td><td>no</td><td>yes (if items are)</td><td>no</td><td>no</td></tr>
<tr><td>Typical use</td><td>general collection</td><td>fixed records, dict keys</td><td>compact numbers</td><td>queues</td></tr>
</table>
<p>For heavy numeric work, NumPy arrays are much faster and smaller than lists.</p>
""")

THEORY("Applications", """
<ul>
<li>Storing ordered data: records read from a file, user inputs, search results.</li>
<li>Stacks (<code>append</code>/<code>pop</code>) for undo or backtracking.</li>
<li>Matrices and grids as lists of lists (games, spreadsheets).</li>
<li>Building results step by step before joining or saving them.</li>
</ul>
""")

FAQ("What is the difference between append() and extend()?", "<p><code>append(x)</code> adds x as one item (even if x is a list). <code>extend(iterable)</code> adds each item of the iterable. <code>[1].append([2, 3])</code> → <code>[1, [2, 3]]</code>; <code>[1].extend([2, 3])</code> → <code>[1, 2, 3]</code>.</p>")
FAQ("sort() vs sorted()?", "<p><code>list.sort()</code> sorts the list in place and returns None. <code>sorted()</code> takes any iterable and returns a new sorted list, leaving the original unchanged.</p>")
FAQ("remove() vs pop() vs del?", "<p><code>remove(x)</code> deletes the first item equal to x. <code>pop(i)</code> deletes the item at index i (default last) and returns it. <code>del a[i]</code> deletes by index or slice and returns nothing.</p>")
FAQ("Shallow copy vs deep copy?", "<p>A shallow copy creates a new outer list but its items are the same objects as the original's. A deep copy recursively copies the nested objects too, so changes to inner lists don't affect the original.</p>")
FAQ("Why is <code>[[0] * 3] * 3</code> a bug?", "<p>The outer <code>* 3</code> repeats a reference to the same inner list three times. Changing <code>grid[0][0]</code> changes every row. Use <code>[[0] * 3 for _ in range(3)]</code>.</p>")
FAQ("List vs tuple?", "<p>Lists are mutable and use square brackets; tuples are immutable and use parentheses. Tuples can be dict keys and signal 'this record shouldn't change'; lists are for collections that grow or change.</p>")
FAQ("What is the time complexity of <code>x in list</code>?", "<p>O(n): Python compares x with each item in turn. Use a set or dict for O(1) membership tests.</p>")
