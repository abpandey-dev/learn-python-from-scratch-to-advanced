from lib import *

THEORY("Definition", """
<p>A <b>dictionary</b> (<code>dict</code>) is a <b>mutable mapping</b> from unique, hashable <b>keys</b> to <b>values</b>. It is Python's built-in <b>hash table</b> (associative array): you look values up by key rather than by position.</p>
<p>Properties:</p>
<ul>
<li>Keys are unique — assigning to an existing key replaces the value.</li>
<li>Keys must be hashable (str, int, float, tuple of hashables, frozenset …); values can be any object.</li>
<li>Insertion-ordered since Python 3.7 (iteration follows insertion order).</li>
<li>Average O(1) lookup, insert and delete.</li>
</ul>
""")

THEORY("Creating dictionaries", """
<table>
<tr><th>Way</th><th>Example</th></tr>
<tr><td>Literal</td><td><code>{"a": 1, "b": 2}</code>, <code>{}</code></td></tr>
<tr><td>Constructor with keywords</td><td><code>dict(a=1, b=2)</code></td></tr>
<tr><td>From pairs</td><td><code>dict([("a", 1), ("b", 2)])</code>, <code>dict(zip(keys, values))</code></td></tr>
<tr><td>Comprehension</td><td><code>{k: v for k, v in pairs}</code></td></tr>
<tr><td>Same value for many keys</td><td><code>dict.fromkeys(["a", "b"], 0)</code></td></tr>
</table>
""")

THEORY("Methods and operations", """
<table>
<tr><th>Operation</th><th>Description</th><th>Time</th></tr>
<tr><td><code>d[k]</code></td><td>get value; KeyError if missing</td><td>O(1)</td></tr>
<tr><td><code>d[k] = v</code></td><td>add or update</td><td>O(1)*</td></tr>
<tr><td><code>del d[k]</code></td><td>remove; KeyError if missing</td><td>O(1)</td></tr>
<tr><td><code>k in d</code></td><td>key membership</td><td>O(1)</td></tr>
<tr><td><code>get(k, default=None)</code></td><td>value or default</td><td>O(1)</td></tr>
<tr><td><code>setdefault(k, default)</code></td><td>get value; insert default first if missing</td><td>O(1)</td></tr>
<tr><td><code>pop(k[, default])</code></td><td>remove and return value</td><td>O(1)</td></tr>
<tr><td><code>popitem()</code></td><td>remove and return the last inserted pair</td><td>O(1)</td></tr>
<tr><td><code>update(other)</code>, <code>|=</code></td><td>merge other into d</td><td>O(len other)</td></tr>
<tr><td><code>a | b</code></td><td>new merged dict (3.9+)</td><td>O(len a + len b)</td></tr>
<tr><td><code>keys() / values() / items()</code></td><td>dynamic views</td><td>O(1) to create</td></tr>
<tr><td><code>copy()</code></td><td>shallow copy</td><td>O(n)</td></tr>
<tr><td><code>clear()</code></td><td>remove everything</td><td>O(n)</td></tr>
</table>
<p>* amortised; occasionally the table is resized.</p>
""")

THEORY("How a dict works inside", """
<ol>
<li>Python computes <code>hash(key)</code>.</li>
<li>The hash picks a slot in an internal table.</li>
<li>If the slot holds a different key (a <b>collision</b>), Python probes other slots (open addressing).</li>
<li>When the table gets about two-thirds full, it grows and every key is re-inserted.</li>
</ol>
<p>This is why keys must be hashable and why equal keys must hash equally: <code>1</code>, <code>1.0</code> and <code>True</code> are the <b>same</b> key.</p>
""")

THEORY("The collections helpers", """
<table>
<tr><th>Class</th><th>What it adds</th><th>Example</th></tr>
<tr><td><code>Counter</code></td><td>counts hashable items; <code>most_common(n)</code>; arithmetic between counters</td><td><code>Counter("banana")</code> → {'a': 3, 'n': 2, 'b': 1}</td></tr>
<tr><td><code>defaultdict(factory)</code></td><td>missing keys get <code>factory()</code> automatically</td><td><code>defaultdict(list)</code>, <code>defaultdict(int)</code></td></tr>
<tr><td><code>OrderedDict</code></td><td>extra order operations (<code>move_to_end</code>)</td><td>LRU caches</td></tr>
<tr><td><code>ChainMap</code></td><td>search several dicts as one</td><td>layered config</td></tr>
</table>
""")

THEORY("Dict vs list vs set, and applications", """
<table>
<tr><th></th><th>list</th><th>set</th><th>dict</th></tr>
<tr><td>Access by</td><td>position</td><td>— (membership only)</td><td>key</td></tr>
<tr><td>Lookup cost</td><td>O(n) by value</td><td>O(1)</td><td>O(1) by key</td></tr>
<tr><td>Stores</td><td>values</td><td>unique values</td><td>key → value pairs</td></tr>
</table>
<h4>Applications</h4>
<ul>
<li>Counting and frequency tables; grouping records.</li>
<li>Caches and memoisation (remember computed results).</li>
<li>Configuration, JSON data and API responses.</li>
<li>Lookup tables, translations, phone books, inventories.</li>
<li>Representing objects and graphs (adjacency lists).</li>
</ul>
""")

FAQ("What can be a dictionary key?", "<p>Any hashable object: numbers, strings, booleans, None, tuples of hashable items, frozensets. Lists, dicts and sets can't be keys because they are mutable.</p>")
FAQ("d[key] vs d.get(key)?", "<p><code>d[key]</code> raises KeyError if the key is missing; <code>d.get(key, default)</code> returns the default (None if not given) instead.</p>")
FAQ("Are dictionaries ordered?", "<p>Yes, since Python 3.7 they preserve insertion order. They are still not sorted — use <code>sorted()</code> on keys or items for a sorted order.</p>")
FAQ("What is the time complexity of dict lookup?", "<p>O(1) on average thanks to hashing; O(n) in the rare worst case where many keys collide.</p>")
FAQ("setdefault vs defaultdict?", "<p>Both supply a starting value for missing keys. <code>setdefault</code> is a method you call each time with the default; <code>defaultdict</code> is a dict subclass that creates the default automatically for any missing key.</p>")
FAQ("How do you merge two dictionaries?", "<p><code>a | b</code> (Python 3.9+) or <code>{**a, **b}</code> create a new dict; <code>a.update(b)</code> or <code>a |= b</code> change a in place. On shared keys, b's values win.</p>")
FAQ("Why are 1 and True the same dict key?", "<p>They are equal (<code>1 == True</code>) and have the same hash, so the dict treats them as one key.</p>")
