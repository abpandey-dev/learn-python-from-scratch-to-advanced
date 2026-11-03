from lib import *

THEORY("Definitions", """
<ul>
<li>A <b>comprehension</b> is a compact expression that builds a list, dict or set from an iterable, optionally filtering and transforming items: <code>[expr for x in iterable if condition]</code>.</li>
<li>An <b>iterable</b> is an object that can return an iterator — it implements <code>__iter__</code> (or the sequence protocol <code>__getitem__</code>).</li>
<li>An <b>iterator</b> is an object with <code>__next__</code> that returns the next item and raises <code>StopIteration</code> when exhausted; its <code>__iter__</code> returns itself.</li>
<li>A <b>generator</b> is an iterator created by a function containing <code>yield</code> (a generator function) or by a generator expression <code>(expr for x in it)</code>.</li>
</ul>
""")

THEORY("Comprehension syntax", """
<table>
<tr><th>Kind</th><th>Syntax</th><th>Produces</th></tr>
<tr><td>List</td><td><code>[f(x) for x in xs if p(x)]</code></td><td>list</td></tr>
<tr><td>Set</td><td><code>{f(x) for x in xs}</code></td><td>set</td></tr>
<tr><td>Dict</td><td><code>{k(x): v(x) for x in xs}</code></td><td>dict</td></tr>
<tr><td>Generator expression</td><td><code>(f(x) for x in xs)</code></td><td>generator (lazy)</td></tr>
<tr><td>Nested</td><td><code>[y for row in grid for y in row]</code></td><td>loops read left → right = outer → inner</td></tr>
<tr><td>With if/else</td><td><code>[a if c else b for x in xs]</code></td><td>the conditional goes before <code>for</code></td></tr>
</table>
<p>In Python 3 the loop variable of a comprehension is local to it and doesn't leak out. Comprehensions are usually faster than the equivalent loop with <code>append</code>.</p>
""")

THEORY("The iterator protocol", """
<ol>
<li><code>for x in obj:</code> calls <code>iter(obj)</code>, which calls <code>obj.__iter__()</code> and returns an iterator.</li>
<li>Each round calls <code>next(iterator)</code> → <code>iterator.__next__()</code>.</li>
<li>When <code>StopIteration</code> is raised, the loop ends quietly.</li>
</ol>
<p>Iterators are <b>single-pass</b>: after exhaustion, further <code>next()</code> calls keep raising StopIteration. Lists, strings and dicts are iterables, not iterators — they give a fresh iterator each time, which is why you can loop over them repeatedly.</p>
""")

THEORY("Generators", """
<ul>
<li>Calling a generator function returns a generator object without running the body.</li>
<li><code>next()</code> runs the body up to the next <code>yield</code>, returns the yielded value, and <b>suspends</b> the function, keeping its local variables and position.</li>
<li>When the function returns (or falls off the end), the generator raises <code>StopIteration</code>.</li>
<li><code>yield from iterable</code> delegates to another iterable or generator.</li>
<li>Generators also support <code>send()</code>, <code>throw()</code> and <code>close()</code> for coroutine-style use.</li>
</ul>
<table>
<tr><th></th><th>List</th><th>Generator</th></tr>
<tr><td>Evaluation</td><td>eager — all items now</td><td>lazy — one item when asked</td></tr>
<tr><td>Memory</td><td>O(n)</td><td>O(1) extra</td></tr>
<tr><td>Reusable</td><td>yes</td><td>no (single pass)</td></tr>
<tr><td>Indexing, len()</td><td>yes</td><td>no</td></tr>
<tr><td>Infinite sequences</td><td>impossible</td><td>possible</td></tr>
</table>
""")

THEORY("Functional built-ins and itertools", """
<p><code>map</code>, <code>filter</code>, <code>zip</code>, <code>enumerate</code> and <code>reversed</code> return <b>lazy iterators</b> in Python 3 — wrap them in <code>list()</code> to see all values. <code>sorted</code> returns a list. <code>any</code> and <code>all</code> short-circuit. <code>functools.reduce(f, xs)</code> folds a sequence into one value.</p>
<p><code>itertools</code> highlights: <code>count, cycle, repeat</code> (infinite); <code>islice, takewhile, dropwhile, chain, groupby, accumulate, pairwise, zip_longest</code> (processing); <code>product, permutations, combinations</code> (combinatorics).</p>
""")

THEORY("Applications", """
<ul>
<li>Transforming and filtering data in one line (cleaning a list of strings, extracting fields).</li>
<li>Reading huge files line by line (a file object is an iterator).</li>
<li>Data pipelines: chaining generators so each stage processes one item at a time.</li>
<li>Streams and infinite sequences: IDs, sensor readings, pagination through an API.</li>
</ul>
""")

FAQ("List comprehension vs generator expression?", "<p>Square brackets build the whole list immediately (uses memory, reusable, indexable). Round brackets create a lazy generator that produces items on demand (tiny memory, single use).</p>")
FAQ("What is the difference between an iterable and an iterator?", "<p>An iterable can produce an iterator (<code>iter(x)</code> works) and can usually be looped over many times. An iterator produces the items with <code>next()</code>, remembers its position and is used up after one pass.</p>")
FAQ("What does yield do?", "<p>It hands a value to the caller and pauses the function, keeping its state. The next request resumes right after the yield.</p>")
FAQ("return vs yield?", "<p><code>return</code> ends the function and sends back one value. <code>yield</code> produces a value but keeps the function alive so it can produce more later.</p>")
FAQ("When should you use a generator?", "<p>When the sequence is large, infinite, or expensive to build, and you only need to go through it once — e.g. processing a big log file line by line.</p>")
FAQ("Where does the if go in a comprehension?", "<p>A filter goes at the end: <code>[x for x in xs if x &gt; 0]</code>. A choice between two values goes at the front: <code>[x if x &gt; 0 else 0 for x in xs]</code>.</p>")
FAQ("Are comprehensions faster than loops?", "<p>Usually a little, because the loop runs in optimised bytecode without repeated <code>append</code> attribute lookups. Readability matters more: use a normal loop when the logic is complex.</p>")
