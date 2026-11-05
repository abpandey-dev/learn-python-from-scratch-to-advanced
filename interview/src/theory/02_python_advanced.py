from lib import *

THEORY("Memory in CPython", """
<ul><li><b>Reference counting:</b> each object tracks how many labels point at it, and it's freed at zero.</li>
<li><b>Garbage collector:</b> finds reference cycles that counting alone misses.</li>
<li><b><code>__slots__</code>:</b> removes each object's <code>__dict__</code>, saving memory when you have many small objects.</li>
<li><b>Everything is an object,</b> which is why a Python list of numbers uses far more memory than a NumPy array.</li></ul>
""")
THEORY("Mutable vs immutable", """
<table><tr><th>Immutable</th><th>Mutable</th></tr>
<tr><td>int, float, str, tuple, frozenset, bytes</td><td>list, dict, set, most objects</td></tr></table>
<p>Only hashable values, usually immutable ones, can be dictionary keys or set members. A tuple holding a list isn't hashable.</p>
""")
FAQ("What is the GIL?", "<p>A lock in standard CPython that lets one thread run Python bytecode at a time. CPU-heavy pure-Python code should use processes; I/O-heavy code does well with threads or asyncio.</p>")
FAQ("Threads vs processes vs asyncio?", "<p>Threads suit I/O with blocking libraries. Processes suit CPU-heavy work. Asyncio suits many concurrent waiting tasks in one thread, using libraries that support it.</p>")
FAQ("What is a decorator?", "<p>A function that takes a function and returns a new one, adding behaviour. <code>@d</code> above a definition means <code>f = d(f)</code>.</p>")
FAQ("Generator vs list?", "<p>A generator produces values lazily and holds only its state, so it can handle huge or endless streams. It can be consumed only once, and it can't be indexed.</p>")
FAQ("Iterable vs iterator?", "<p>An iterable can give you an iterator through <code>__iter__</code>. An iterator produces values through <code>__next__</code>, and it remembers its position.</p>")
FAQ("Shallow vs deep copy?", "<p>A shallow copy makes a new outer container that shares inner objects. A deep copy recursively copies everything.</p>")
FAQ("== vs is?", "<p><code>==</code> compares values, while <code>is</code> checks object identity. Use <code>is</code> for None.</p>")
FAQ("What are *args and **kwargs?", "<p>They collect extra positional arguments into a tuple and extra keyword arguments into a dictionary.</p>")
FAQ("@classmethod vs @staticmethod?", "<p>A classmethod receives the class, so it suits alternative constructors. A staticmethod receives nothing automatically, so it's a plain function that lives in the class.</p>")
FAQ("What is the MRO?", "<p>The order Python searches classes for a method, computed by C3 linearisation. <code>super()</code> moves to the next class in it.</p>")
FAQ("How do dictionaries work?", "<p>A hash table: the key's hash picks a slot, and equality confirms the match. Lookups are O(1) on average, and insertion order has been preserved since Python 3.7.</p>")
FAQ("How does Python's sort work?", "<p>Timsort, a hybrid of merge and insertion sort: O(n log n), stable, and fast on partly ordered data.</p>")
FAQ("What is duck typing?", "<p>Code cares what an object can do, not what class it is. If it has the method you call, it works. Type hints document intent, and they aren't enforced at run time.</p>")
