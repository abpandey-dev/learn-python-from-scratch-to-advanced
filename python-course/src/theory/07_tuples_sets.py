from lib import *

THEORY("Definitions", """
<p>A <b>tuple</b> is an <b>ordered, immutable</b> sequence of items of any type, written <code>(a, b, c)</code>. It supports indexing, slicing, iteration, <code>len</code>, <code>in</code>, <code>count</code> and <code>index</code>, but no methods that change it.</p>
<p>A <b>set</b> is an <b>unordered, mutable</b> collection of <b>unique, hashable</b> items, written <code>{a, b, c}</code>. It is modelled on mathematical sets and implemented with a hash table.</p>
<p>A <b>frozenset</b> is an immutable (and therefore hashable) set.</p>
""")

THEORY("Tuple features", """
<ul>
<li><b>Creation</b>: <code>(1, 2)</code>, <code>1, 2</code>, <code>tuple([1, 2])</code>, <code>()</code>, and <code>(x,)</code> for one item.</li>
<li><b>Packing/unpacking</b>: <code>a, b = 1, 2</code>; extended unpacking <code>head, *tail = seq</code>.</li>
<li><b>Immutability is shallow</b>: <code>t = ([1], 2)</code> — you can't replace <code>t[0]</code>, but you can append to the list inside it. Such a tuple isn't hashable.</li>
<li><b>Named tuples</b>: <code>collections.namedtuple("Point", "x y")</code> gives tuples whose fields have names: <code>p.x</code>. <code>typing.NamedTuple</code> and dataclasses are modern alternatives.</li>
</ul>
<h4>Why use a tuple instead of a list?</h4>
<ul>
<li>It signals "this group of values is fixed".</li>
<li>It's hashable (if its items are), so it can be a dict key or set item.</li>
<li>It's slightly smaller and faster to create than a list.</li>
</ul>
""")

THEORY("Set features and operations", """
<table>
<tr><th>Method</th><th>Effect</th><th>Time</th></tr>
<tr><td><code>add(x)</code></td><td>insert x</td><td>O(1)</td></tr>
<tr><td><code>remove(x)</code></td><td>delete x, KeyError if missing</td><td>O(1)</td></tr>
<tr><td><code>discard(x)</code></td><td>delete x if present</td><td>O(1)</td></tr>
<tr><td><code>pop()</code></td><td>remove an arbitrary item</td><td>O(1)</td></tr>
<tr><td><code>x in s</code></td><td>membership</td><td>O(1) average</td></tr>
<tr><td><code>update(it)</code> / <code>|=</code></td><td>add many</td><td>O(k)</td></tr>
<tr><td><code>a | b</code>, <code>a &amp; b</code>, <code>a - b</code>, <code>a ^ b</code></td><td>union, intersection, difference, symmetric difference</td><td>O(len a + len b) (intersection O(min))</td></tr>
<tr><td><code>a &lt;= b</code>, <code>a &lt; b</code></td><td>subset, proper subset</td><td>O(len a)</td></tr>
</table>
<p>Set comprehension: <code>{x % 3 for x in nums}</code>. Note <code>{}</code> is an empty <b>dict</b>; an empty set is <code>set()</code>.</p>
""")

THEORY("Hashing and hashability", """
<p>A <b>hash</b> is an integer computed from a value (<code>hash("abc")</code>). Sets and dicts use it to jump straight to the bucket where the item would be, which is why membership is O(1) on average.</p>
<p>An object is <b>hashable</b> if its hash never changes during its lifetime and it can be compared with <code>==</code>. Rule: equal objects must have equal hashes.</p>
<table>
<tr><th>Hashable</th><th>Not hashable</th></tr>
<tr><td>int, float, str, bool, None, tuple (of hashables), frozenset</td><td>list, dict, set, bytearray</td></tr>
</table>
""")

THEORY("Comparison: list, tuple, set", """
<table>
<tr><th></th><th>list</th><th>tuple</th><th>set</th></tr>
<tr><td>Syntax</td><td><code>[1, 2]</code></td><td><code>(1, 2)</code></td><td><code>{1, 2}</code></td></tr>
<tr><td>Ordered</td><td>yes</td><td>yes</td><td>no</td></tr>
<tr><td>Duplicates</td><td>allowed</td><td>allowed</td><td>removed</td></tr>
<tr><td>Mutable</td><td>yes</td><td>no</td><td>yes</td></tr>
<tr><td>Indexing</td><td>yes</td><td>yes</td><td>no</td></tr>
<tr><td>Membership</td><td>O(n)</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Hashable</td><td>no</td><td>yes*</td><td>no (frozenset yes)</td></tr>
</table>
""")

THEORY("Applications", """
<ul>
<li><b>Tuples</b>: returning several values, coordinates, RGB colours, rows from a database, dictionary keys like <code>(row, col)</code>.</li>
<li><b>Sets</b>: removing duplicates, fast membership tests (visited nodes, banned words), comparing groups (common friends, missing items), tags.</li>
</ul>
""")

FAQ("What's the difference between a list and a tuple?", "<p>Lists are mutable (items can change) and tuples are immutable. Tuples can be hashed and used as dict keys; lists can't. Use tuples for fixed records and lists for collections that change.</p>")
FAQ("How do you create a tuple with one element?", "<p>Add a trailing comma: <code>(5,)</code> or <code>5,</code>. <code>(5)</code> is just the int 5 in brackets.</p>")
FAQ("Can a tuple contain a list? Is it still immutable?", "<p>Yes. The tuple can't change which objects it holds, but the list inside can still be modified. Such a tuple is not hashable.</p>")
FAQ("Why is <code>{}</code> not an empty set?", "<p>Curly braces were used for dicts first, so <code>{}</code> is an empty dict. Create an empty set with <code>set()</code>.</p>")
FAQ("remove() vs discard() for sets?", "<p>Both delete an item. <code>remove</code> raises KeyError if the item is missing; <code>discard</code> does nothing.</p>")
FAQ("Why is membership faster in a set than in a list?", "<p>A set hashes the value and checks one bucket (O(1) average). A list compares the value with each element in order (O(n)).</p>")
FAQ("What is a frozenset?", "<p>An immutable set. It's hashable, so it can be stored in another set or used as a dict key.</p>")
