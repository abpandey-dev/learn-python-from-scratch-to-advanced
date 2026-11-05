from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import functools


LESSON("Basics", "Names, objects and the traps they cause", """
<p>A variable is a label on an object. Assignment never copies; it adds another label.</p>
<pre><code class="py">a = [1, 2]
b = a          # the same list, with two labels
b.append(3)
print(a)       # [1, 2, 3]</code></pre>
<p><b><code>==</code> vs <code>is</code>:</b> <code>==</code> asks "same value?" and <code>is</code> asks "same object?". Use <code>is</code> only for None. Small integers and some strings are cached, so <code>is</code> sometimes appears to work on them, and that luck is unreliable.</p>
<p><b>Trap 1: mutable default arguments.</b> A default is created once, when the function is defined:</p>
<pre><code class="py">def add(x, items=[]):    # the same list on every call!
    items.append(x)
    return items
add(1)   # [1]
add(2)   # [1, 2]  surprise</code></pre>
<p>The fix is <code>items=None</code>, then <code>items = [] if items is None else items</code>.</p>
<p><b>Trap 2: late binding.</b> A closure remembers the <i>variable</i>, not its value at that moment:</p>
<pre><code class="py">fns = [lambda v: v * i for i in range(3)]
[f(10) for f in fns]     # [20, 20, 20], because i is 2 by the time they run</code></pre>
<p>The fix is <code>lambda v, i=i: v * i</code>, which gives [0, 10, 20].</p>
<p><b>Trap 3: shallow copies.</b> After <code>b = copy.copy(a)</code> on a nested list, the outer list is new but the inner lists are shared:</p>
<table><tr><th>Copy</th><th>Change a[0][0] = 99, then b[0] is</th></tr>
<tr><td><code>b = a</code></td><td>[99, 2]</td></tr><tr><td><code>copy.copy(a)</code></td><td>[99, 2]</td></tr><tr><td><code>copy.deepcopy(a)</code></td><td>[1, 2]</td></tr></table>
""", practice=["Mutable Default Argument", "Late-Binding Closures", "Shallow vs Deep Copy", "A Closure With State"])


@LD
def late_binding_demo():
    wrong = [lambda v: v * i for i in range(3)]
    right = [lambda v, i=i: v * i for i in range(3)]
    print("late binding:", [f(10) for f in wrong])
    print("fixed:       ", [f(10) for f in right])


LESSON("Core", "Decorators, from nothing", """
<p>Functions are values, so you can pass one in and return another. A <b>decorator</b> is a function that takes a function and returns an improved version.</p>
<pre><code class="py">def shout(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    return "hi " + name

greet("sam")     # 'HI SAM'</code></pre>
<p>The <code>@shout</code> line is only shorthand for <code>greet = shout(greet)</code>. There's no magic beyond that.</p>
<p><b>Always use <code>functools.wraps</code>.</b> Otherwise the decorated function reports its name as "wrapper", which confuses debugging, logging and documentation. <code>wraps</code> copies the name and docstring across.</p>
<p><b>A decorator with arguments has three levels,</b> because <code>@retry(3)</code> must first run and <i>return</i> a decorator:</p>
<pre><code class="py">def retry(times):            # 1. takes the settings
    def deco(fn):            # 2. takes the function
        @functools.wraps(fn)
        def wrapper(*a, **k):    # 3. runs at each call
            for attempt in range(times):
                try:
                    return fn(*a, **k)
                except ValueError:
                    if attempt == times - 1:
                        raise
        return wrapper
    return deco</code></pre>
<p><b>Memoisation shows the payoff.</b> Plain recursive fib(30) makes 2,692,537 calls. With <code>@functools.lru_cache</code>, the body runs just <b>31</b> times, once for each of 0 to 30.</p>
<p>Common real uses are logging, timing, retries, caching, access checks, and registering routes in web frameworks.</p>
""", practice=["Count-Calls Decorator", "Why functools.wraps Matters", "Memoize Decorator", "Decorator With Arguments"])


LESSON("Core", "Iterators and generators", """
<p>A <code>for</code> loop actually does this: call <code>iter()</code> on the object, then call <code>next()</code> until <code>StopIteration</code>.</p>
<p><b>Iterable vs iterator:</b> a list is iterable, so you can loop over it many times. An iterator is a one-way stream with a position: once used up, it stays empty.</p>
<p>A <b>generator</b> is the easiest way to make an iterator. <code>yield</code> pauses the function and keeps all its local variables, and the next <code>next()</code> call resumes it.</p>
<pre><code class="py">def countdown(n):
    while n > 0:
        yield n        # pause here, handing n out
        n -= 1

c = countdown(3)
list(c)    # [3, 2, 1]
list(c)    # []  used up</code></pre>
<p><b>Why it matters: memory.</b> A list of a million numbers takes megabytes. A generator holds only its current state, whatever the length, so it can process a file larger than your RAM, or an endless stream.</p>
<p><b>Pipelines</b> chain lazily, and nothing happens until the last step asks for a value:</p>
<pre><code class="py">lines = (l.strip() for l in open(path))
kept = (l for l in lines if l and not l.startswith("#"))
for line in kept: ...</code></pre>
<p><b><code>yield from</code></b> hands over to another generator, which makes recursive ones short.</p>
<p>The demo measures the difference in memory.</p>
""", practice=["Generator Pipeline", "Sliding Window Generator", "Flatten With yield from", "Build an Iterator"])


@LD
def generator_memory():
    import sys
    as_list = [i * i for i in range(100000)]
    as_generator = (i * i for i in range(100000))
    print("list bytes:     ", sys.getsizeof(as_list))
    print("generator bytes:", sys.getsizeof(as_generator))
    print("same total:     ", sum(as_list) == sum(as_generator))


LESSON("Core", "Context managers and classes", """
<p><b>A context manager</b> guarantees clean-up. <code>with</code> calls <code>__enter__</code> at the start and <code>__exit__</code> at the end, even if an error occurs. If <code>__exit__</code> returns True, the error is suppressed.</p>
<pre><code class="py">with open("a.txt") as f:     # closed for you, even on an error
    data = f.read()</code></pre>
<p>Use one wherever something must be released: files, locks, database connections. <code>contextlib.contextmanager</code> makes one from a generator with a single yield.</p>
<p><b>Multiple inheritance and the MRO.</b> For the diamond <code>class D(B, C)</code> where B and C inherit from A, the method resolution order is <b>D, B, C, A, object</b>. <code>super()</code> means "the next class in the MRO", not "my parent". That's why each class's method runs exactly once, giving "DBCA".</p>
<p><b><code>__eq__</code> and <code>__hash__</code> go together.</b> Sets and dictionaries find an item by hash, then confirm with equality. If equal objects had different hashes, the set would keep both. Defining <code>__eq__</code> alone makes a class unhashable, on purpose. <code>@dataclass(frozen=True)</code> generates both correctly.</p>
<table><tr><th>Method kind</th><th>First parameter</th><th>Use for</th></tr>
<tr><td>Instance</td><td>self</td><td>work with one object's data</td></tr>
<tr><td><code>@classmethod</code></td><td>cls</td><td>alternative constructors</td></tr>
<tr><td><code>@staticmethod</code></td><td>nothing</td><td>a helper that lives with the class</td></tr>
<tr><td><code>@property</code></td><td>self</td><td>a computed or validated attribute</td></tr></table>
""", practice=["A Context Manager", "Method Resolution Order", "__eq__ and __hash__"])


LESSON("Core", "Know your standard library", """
<p>Interviewers notice when you reach for the right tool, because it means less code and fewer bugs.</p>
<table><tr><th>Tool</th><th>Does</th><th>Instead of</th></tr>
<tr><td><code>Counter(words).most_common(3)</code></td><td>counts, top k</td><td>a dict and a sort</td></tr>
<tr><td><code>defaultdict(list)</code></td><td>grouping</td><td>"if key not in d"</td></tr>
<tr><td><code>deque</code></td><td>O(1) at both ends</td><td><code>list.pop(0)</code>, which is O(n)</td></tr>
<tr><td><code>heapq.nlargest(k, xs)</code></td><td>top k in O(n log k)</td><td>a full sort</td></tr>
<tr><td><code>bisect</code></td><td>binary search on sorted lists</td><td>writing it by hand</td></tr>
<tr><td><code>OrderedDict</code></td><td>LRU with <code>move_to_end</code></td><td>a linked list by hand</td></tr>
<tr><td><code>itertools.groupby</code></td><td>runs of neighbours</td><td>tracking "previous"</td></tr>
<tr><td><code>functools.lru_cache</code></td><td>memoisation</td><td>a dict by hand</td></tr></table>
<p><b>Trap:</b> <code>groupby</code> only groups <i>neighbours</i>. "abca" gives a, b, c, a separately, so sort first if you want one group per key.</p>
<p><b>Costs worth memorising:</b></p>
<table><tr><th>Operation</th><th>Cost</th></tr>
<tr><td><code>list.append</code>, <code>dict[k]</code>, <code>x in set</code></td><td>O(1) (average or amortised)</td></tr>
<tr><td><code>x in list</code>, <code>list.insert(0, x)</code>, <code>list.pop(0)</code></td><td>O(n)</td></tr>
<tr><td><code>sorted</code> (Timsort, stable)</td><td>O(n log n)</td></tr>
<tr><td>Repeated <code>s += "x"</code> in a loop</td><td>O(n²) worst case, so use <code>"".join</code></td></tr></table>
""", practice=["LRU Cache With OrderedDict", "Group Consecutive Runs", "Top K With the Standard Library", "Keep a List Sorted"])


LESSON("Advanced", "Concurrency: GIL, threads, processes and async", """
<p>"What is the GIL?" is the most common advanced Python question.</p>
<p><b>The Global Interpreter Lock</b> lets only one thread run Python bytecode at a time in standard CPython. So threads don't speed up pure-Python number crunching. They do help when waiting, because the lock is released during I/O, and many libraries like NumPy release it during heavy work.</p>
<table><tr><th>Tool</th><th>Best for</th><th>Why</th></tr>
<tr><td><code>threading</code></td><td>I/O: network, files</td><td>threads wait without blocking each other</td></tr>
<tr><td><code>multiprocessing</code></td><td>CPU-heavy work</td><td>separate processes, each with its own GIL</td></tr>
<tr><td><code>asyncio</code></td><td>many thousands of waiting connections</td><td>one thread, cheap task switching at each <code>await</code></td></tr></table>
<pre><code class="py">from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:
    pages = list(pool.map(fetch, urls))         # I/O: threads

with ProcessPoolExecutor() as pool:
    results = list(pool.map(crunch, chunks))    # CPU: processes</code></pre>
<pre><code class="py">import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)    # gives way to other tasks while waiting
    return name

async def main():
    return await asyncio.gather(fetch("a", 0.2), fetch("b", 0.1))

print(asyncio.run(main()))   # ['a', 'b'], in about 0.2 seconds, not 0.3</code></pre>
<p>These snippets are shown as text, as they don't suit this site's browser IDE. Run them on your machine or in Colab (where a notebook's event loop means you'd write <code>await main()</code> instead of <code>asyncio.run</code>).</p>
<p><b>What async really is.</b> Tasks are paused functions, and a loop runs each until it next waits, which is the "Coroutines by Hand" question with generators. Note that one blocking call, like <code>time.sleep</code>, freezes every task.</p>
<p><b>Race condition:</b> <code>counter += 1</code> is several steps (read, add, write), so threads can overwrite each other. Protect shared data with a <code>Lock</code>, or better, don't share: pass messages with a <code>queue.Queue</code>.</p>
<p><b>Good to mention:</b> Python 3.13 added an optional free-threaded build without the GIL. It's still not the default, so assume the GIL unless told otherwise.</p>
""", practice=["Coroutines by Hand"])
