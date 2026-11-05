from lib import *
import bisect
import copy
import functools
import heapq
import itertools
import re
from collections import Counter, OrderedDict, deque
from dataclasses import dataclass, field


TOPIC(
    id="python-advanced", title="Advanced Python", glyph="@wraps",
    blurb="The Python that separates seniors: closures and late binding, decorators, generators and iterators, context managers, copying, the MRO, dataclasses, standard-library tools, and concurrency concepts.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">@functools.wraps(fn)                  # keep a wrapped function's name
yield / yield from                    # make a generator
def __enter__ / __exit__              # make a context manager
def __iter__ / __next__               # make an iterator
copy.copy(x) / copy.deepcopy(x)       # shallow / deep
functools.lru_cache, collections.Counter, heapq, bisect, itertools</code></pre>
""")


Q(None, "Mutable Default Argument", "Easy", "The classic trap",
  "Write append_to(value, target=None) so each call without a target starts with a new list. Test: run calls [(1,), (2,)] and return results.",
  [(([(1,), (2,)],), [[1], [2]])],
  ("Without the fix, a default list is shared between calls. Check for None and build a list.", "O(n)", "O(n)"),
  ("Same idea written compactly. None is the standard sentinel.", "O(n)", "O(n)"),
  names=["calls"])


@B
def default_trap(calls):
    def append_to(value, target=None):
        if target is None:
            target = []
        target.append(value)
        return target
    results = []
    for c in calls:
        results.append(append_to(*c))
    return results


@O
def default_trap(calls):
    def append_to(value, target=None):
        target = [] if target is None else target
        target.append(value)
        return target
    return [append_to(*c) for c in calls]


Q(None, "Late-Binding Closures", "Medium", "The loop variable trap",
  "Return a list of n functions where the i-th multiplies its argument by i, then apply each to x. A plain lambda in a loop would give n−1 every time.",
  [((3, 10), [0, 10, 20])],
  ("A factory function captures each value in its own scope.", "O(n)", "O(n)"),
  ("A default argument, <code>lambda v, i=i: v * i</code>, binds the value at creation.", "O(n)", "O(n)"),
  names=["n", "x"])


@B
def multipliers(n, x):
    def make(i):
        def f(v):
            return v * i
        return f
    fns = []
    for i in range(n):
        fns.append(make(i))
    return [f(x) for f in fns]


@O
def multipliers(n, x):
    fns = [lambda v, i=i: v * i for i in range(n)]
    return [f(x) for f in fns]


Q(None, "A Closure With State", "Easy", "nonlocal",
  "Make a counter function starting at start. Call it n times and return the results.",
  [((5, 3), [6, 7, 8])],
  ("A class holding the count.", "O(n)", "O(1)"),
  ("A closure with <code>nonlocal</code>.", "O(n)", "O(1)"),
  names=["start", "n"])


@B
def counter_calls(start, n):
    class Counter_:
        def __init__(self):
            self.value = start

        def __call__(self):
            self.value += 1
            return self.value
    c = Counter_()
    return [c() for _ in range(n)]


@O
def counter_calls(start, n):
    def make():
        value = start

        def next_value():
            nonlocal value
            value += 1
            return value
        return next_value
    c = make()
    return [c() for _ in range(n)]


Q(None, "Count-Calls Decorator", "Easy", "Your first decorator",
  "Write a decorator that counts calls in wrapper.calls. Apply it to a square function, call it on each value, and return (results, count).",
  [(([2, 3, 4],), ([4, 9, 16], 3))],
  ("Wrap it by hand, without @.", "O(n)", "O(n)"),
  ("<code>@</code> syntax with <code>functools.wraps</code>.", "O(n)", "O(n)"),
  names=["values"])


@B
def count_calls(values):
    def counted(fn):
        def wrapper(*args):
            wrapper.calls += 1
            return fn(*args)
        wrapper.calls = 0
        return wrapper

    def square(x):
        return x * x
    square = counted(square)
    return ([square(v) for v in values], square.calls)


@O
def count_calls(values):
    def counted(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            wrapper.calls += 1
            return fn(*args, **kwargs)
        wrapper.calls = 0
        return wrapper

    @counted
    def square(x):
        return x * x
    return ([square(v) for v in values], square.calls)


Q(None, "Why functools.wraps Matters", "Easy", "Keeping the name",
  "Return (name without wraps, name with wraps) of a decorated function called greet.",
  [((), ('wrapper', 'greet'))],
  ("Set <code>wrapper.__name__</code> by hand in the second version.", "O(1)", "O(1)"),
  ("<code>functools.wraps</code> copies the name, docstring and more.", "O(1)", "O(1)"))


@B
def wraps_demo():
    def plain_deco(fn):
        def wrapper():
            return fn()
        return wrapper

    def named_deco(fn):
        def wrapper():
            return fn()
        wrapper.__name__ = fn.__name__
        return wrapper

    def greet():
        return "hi"
    return (plain_deco(greet).__name__, named_deco(greet).__name__)


@O
def wraps_demo():
    def plain_deco(fn):
        def wrapper():
            return fn()
        return wrapper

    def named_deco(fn):
        @functools.wraps(fn)
        def wrapper():
            return fn()
        return wrapper

    def greet():
        return "hi"
    return (plain_deco(greet).__name__, named_deco(greet).__name__)


Q(None, "Memoize Decorator", "Medium", "Build lru_cache yourself",
  "Compute fib(n) with memoisation, and return (fib(n), number of times the real body ran).",
  [((30,), (832040, 31)), ((10,), (55, 11))],
  ("A dictionary-based decorator written by hand.", "O(n)", "O(n)"),
  ("<code>functools.lru_cache</code>, and <code>cache_info()</code> reports misses.", "O(n)", "O(n)"),
  names=["n"])


@B
def memo_fib(n):
    def memoize(fn):
        cache = {}

        def wrapper(x):
            if x not in cache:
                cache[x] = fn(x)
            return cache[x]
        wrapper.cache = cache
        return wrapper

    @memoize
    def fib(k):
        return k if k < 2 else fib(k - 1) + fib(k - 2)
    return (fib(n), len(fib.cache))


@O
def memo_fib(n):
    @functools.lru_cache(maxsize=None)
    def fib(k):
        return k if k < 2 else fib(k - 1) + fib(k - 2)
    return (fib(n), fib.cache_info().misses)


Q(None, "Decorator With Arguments", "Medium", "Three levels of functions",
  "Write retry(times): it calls a function until it succeeds, re-raising after the last try. Apply it to a function that fails until its fails_before-th call. Return (result or 'gave up', calls made).",
  [((3, 2), ('ok', 3)), ((2, 5), ('gave up', 2))],
  ("A loop tracking the last error.", "O(t)", "O(1)"),
  ("A <code>for</code> loop that re-raises on the last attempt, with <code>functools.wraps</code> and any arguments.", "O(t)", "O(1)"),
  names=["times", "fails_before"])


@B
def retry_demo(times, fails_before):
    def retry(limit):
        def deco(fn):
            def wrapper():
                last = None
                count = 0
                while count < limit:
                    try:
                        return fn()
                    except ValueError as e:
                        last = e
                        count += 1
                raise last
            return wrapper
        return deco
    calls = [0]

    @retry(times)
    def flaky():
        calls[0] += 1
        if calls[0] <= fails_before:
            raise ValueError("not yet")
        return "ok"
    try:
        return (flaky(), calls[0])
    except ValueError:
        return ("gave up", calls[0])


@O
def retry_demo(times, fails_before):
    def retry(limit):
        def deco(fn):
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                for attempt in range(limit):
                    try:
                        return fn(*args, **kwargs)
                    except ValueError:
                        if attempt == limit - 1:
                            raise
            return wrapper
        return deco
    calls = [0]

    @retry(times)
    def flaky():
        calls[0] += 1
        if calls[0] <= fails_before:
            raise ValueError("not yet")
        return "ok"
    try:
        return (flaky(), calls[0])
    except ValueError:
        return ("gave up", calls[0])


Q(None, "Generator Pipeline", "Medium", "Lazy steps",
  "Using generators, take lines, strip them, drop empty ones and those starting with #, and return the upper-cased remainder as a list.",
  [(([" a ", "", "# note", "b"],), ['A', 'B'])],
  ("One loop doing all the steps.", "O(n)", "O(n)"),
  ("Three chained generator expressions. Nothing runs until consumed, so it can handle huge files.", "O(n)", "O(1) per item"))


@B
def clean_lines(lines):
    out = []
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#"):
            out.append(s.upper())
    return out


@O
def clean_lines(lines):
    stripped = (l.strip() for l in lines)
    kept = (l for l in stripped if l and not l.startswith("#"))
    return list(l.upper() for l in kept)


Q(None, "Sliding Window Generator", "Medium", "Streams of any length",
  "Yield tuples of the last k items of any iterable. It must work with an iterator that can't be indexed.",
  [(([1, 2, 3, 4], 2), [(1, 2), (2, 3), (3, 4)])],
  ("Keep a list, popping the front (O(k) each).", "O(n·k)", "O(k)"),
  ("<code>deque(maxlen=k)</code> drops the oldest automatically.", "O(n·k)", "O(k)"),
  names=["items", "k"], post=list)


@B
def sliding(items, k):
    window = []
    for x in items:
        window.append(x)
        if len(window) > k:
            window.pop(0)
        if len(window) == k:
            yield tuple(window)


@O
def sliding(items, k):
    window = deque(maxlen=k)
    for x in items:
        window.append(x)
        if len(window) == k:
            yield tuple(window)


Q(None, "Flatten With yield from", "Medium", "Recursive generators",
  "Flatten nested lists of any depth, lazily.",
  [(([1, [2, [3, 4]], 5],), [1, 2, 3, 4, 5])],
  ("An inner loop re-yields each value.", "O(n·d)", "O(d)"),
  ("<code>yield from</code> delegates to the inner generator.", "O(n·d)", "O(d)"),
  post=list)


@B
def flatten(items):
    for x in items:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x


@O
def flatten(items):
    for x in items:
        if isinstance(x, list):
            yield from flatten(x)
        else:
            yield x


Q(None, "Build an Iterator", "Medium", "__iter__ and __next__",
  "Make Countdown(n), which can be looped over from n to 1. Return list(Countdown(n)), and also whether a second pass over the same object gives nothing.",
  [((3,), ([3, 2, 1], True))],
  ("A class with <code>__iter__</code> and <code>__next__</code>.", "O(n)", "O(1)"),
  ("A generator gives the same behaviour in two lines.", "O(n)", "O(1)"),
  names=["n"])


@B
def countdown_demo(n):
    class Countdown:
        def __init__(self, start):
            self.current = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            self.current -= 1
            return self.current + 1
    c = Countdown(n)
    return (list(c), list(c) == [])


@O
def countdown_demo(n):
    def countdown(start):
        while start > 0:
            yield start
            start -= 1
    c = countdown(n)
    return (list(c), list(c) == [])


Q(None, "A Context Manager", "Medium", "__enter__ and __exit__",
  "Write a context manager that logs 'enter' and 'exit' even on error, and swallows only ValueError. For each flag in raises, run a with-block that raises ValueError if the flag is true. Return the log.",
  [(([False, True],), ['enter', 'exit', 'enter', 'exit'])],
  ("A class with <code>__enter__</code> and <code>__exit__</code>. Returning True suppresses the error.", "O(n)", "O(n)"),
  ("<code>contextlib.contextmanager</code> with try/except/finally.", "O(n)", "O(n)"),
  names=["raises"])


@B
def log_context(raises):
    log = []

    class Managed:
        def __enter__(self):
            log.append("enter")
            return self

        def __exit__(self, exc_type, exc, tb):
            log.append("exit")
            return exc_type is ValueError
    for flag in raises:
        with Managed():
            if flag:
                raise ValueError("boom")
    return log


@O
def log_context(raises):
    import contextlib
    log = []

    @contextlib.contextmanager
    def managed():
        log.append("enter")
        try:
            yield
        except ValueError:
            pass
        finally:
            log.append("exit")
    for flag in raises:
        with managed():
            if flag:
                raise ValueError("boom")
    return log


Q(None, "Shallow vs Deep Copy", "Easy", "Aliasing bugs",
  "Copy a nested list three ways (assignment, shallow, deep), then change original[0][0] to 99. Return each copy's first inner list.",
  [(([[1, 2], [3]],), ([99, 2], [99, 2], [1, 2]))],
  ("Build the shallow and deep copies by hand.", "O(n)", "O(n)"),
  ("<code>copy.copy</code> and <code>copy.deepcopy</code>.", "O(n)", "O(n)"),
  names=["original"])


@B
def copy_kinds(original):
    alias = original
    shallow = [row for row in original]
    deep = [[v for v in row] for row in original]
    original[0][0] = 99
    return (alias[0], shallow[0], deep[0])


@O
def copy_kinds(original):
    alias, shallow, deep = original, copy.copy(original), copy.deepcopy(original)
    original[0][0] = 99
    return (alias[0], shallow[0], deep[0])


Q(None, "Method Resolution Order", "Medium", "Diamond inheritance",
  "With class B(A), C(A), D(B, C), each defining who(), return D's MRO names, and the result of D().who() where each calls super and adds its name.",
  [((), (['D', 'B', 'C', 'A', 'object'], 'DBCA'))],
  ("Build the classes and read <code>__mro__</code>.", "O(1)", "O(1)"),
  ("<code>D.mro()</code>. Super follows the MRO, not just the parent.", "O(1)", "O(1)"))


@B
def mro_demo():
    class A:
        def who(self):
            return "A"

    class B(A):
        def who(self):
            return "B" + super().who()

    class C(A):
        def who(self):
            return "C" + super().who()

    class D(B, C):
        def who(self):
            return "D" + super().who()
    names = []
    for k in D.__mro__:
        names.append(k.__name__)
    return (names, D().who())


@O
def mro_demo():
    class A:
        def who(self):
            return "A"

    class B(A):
        def who(self):
            return "B" + super().who()

    class C(A):
        def who(self):
            return "C" + super().who()

    class D(B, C):
        def who(self):
            return "D" + super().who()
    return ([k.__name__ for k in D.mro()], D().who())


Q(None, "__eq__ and __hash__", "Medium", "Objects in sets",
  "A Point with x and y: make equal points count as one in a set. Return the number of distinct points in a list of pairs.",
  [(([(1, 2), (1, 2), (3, 4)],), 2)],
  ("A class defining <code>__eq__</code> and <code>__hash__</code> together.", "O(n)", "O(n)"),
  ("<code>@dataclass(frozen=True)</code> generates both.", "O(n)", "O(n)"),
  names=["pairs"])


@B
def distinct_points(pairs):
    class Point:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __eq__(self, other):
            return (self.x, self.y) == (other.x, other.y)

        def __hash__(self):
            return hash((self.x, self.y))
    return len({Point(*p) for p in pairs})


@O
def distinct_points(pairs):
    @dataclass(frozen=True)
    class Point:
        x: int
        y: int
    return len({Point(*p) for p in pairs})


Q(None, "LRU Cache With OrderedDict", "Medium", "Stdlib power",
  "Replay operations on an LRU cache of the given capacity: ('put', k, v) and ('get', k). Return the results of each get (−1 if missing).",
  [((2, [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("get", 3)]), [1, -1, 3])],
  ("A plain list of keys in recency order. Removal is O(n).", "O(n) per op", "O(c)"),
  ("<code>OrderedDict.move_to_end</code> and <code>popitem(last=False)</code>: O(1).", "O(1) per op", "O(c)"),
  names=["capacity", "ops"])


@B
def lru_replay(capacity, ops):
    data, order, out = {}, [], []
    for op in ops:
        if op[0] == "get":
            if op[1] in data:
                order.remove(op[1])
                order.append(op[1])
                out.append(data[op[1]])
            else:
                out.append(-1)
        else:
            if op[1] in data:
                order.remove(op[1])
            elif len(data) == capacity:
                del data[order.pop(0)]
            data[op[1]] = op[2]
            order.append(op[1])
    return out


@O
def lru_replay(capacity, ops):
    cache, out = OrderedDict(), []
    for op in ops:
        if op[0] == "get":
            if op[1] in cache:
                cache.move_to_end(op[1])
            out.append(cache.get(op[1], -1))
        else:
            cache[op[1]] = op[2]
            cache.move_to_end(op[1])
            if len(cache) > capacity:
                cache.popitem(last=False)
    return out


Q(None, "Group Consecutive Runs", "Easy", "itertools.groupby",
  "Compress 'aaabbc' into [('a', 3), ('b', 2), ('c', 1)]. Note groupby only groups neighbours.",
  [(("aaabbc",), [('a', 3), ('b', 2), ('c', 1)]), (("abca",), [('a', 1), ('b', 1), ('c', 1), ('a', 1)])],
  ("Track the current character in a loop.", "O(n)", "O(k)"),
  ("<code>itertools.groupby</code>.", "O(n)", "O(k)"))


@B
def runs(text):
    out = []
    for ch in text:
        if out and out[-1][0] == ch:
            out[-1] = (ch, out[-1][1] + 1)
        else:
            out.append((ch, 1))
    return out


@O
def runs(text):
    return [(k, len(list(g))) for k, g in itertools.groupby(text)]


Q(None, "Top K With the Standard Library", "Easy", "Counter, heapq",
  "Return the k most common words, as (word, count), ties alphabetical.",
  [((["b", "a", "b", "c", "a", "b"], 2), [('b', 3), ('a', 2)])],
  ("A dictionary, then a full sort.", "O(n log n)", "O(n)"),
  ("<code>heapq.nsmallest</code> over a Counter is O(n log k).", "O(n log k)", "O(n)"),
  names=["words", "k"])


@B
def top_words(words, k):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


@O
def top_words(words, k):
    return heapq.nsmallest(k, Counter(words).items(), key=lambda kv: (-kv[1], kv[0]))


Q(None, "Coroutines by Hand", "Hard", "What async does underneath",
  "Each task is a generator that yields when it would wait. Run tasks round robin until all finish, and return the order of events. This is how an event loop works.",
  [(([("a", 2), ("b", 1)],), ['a0', 'b0', 'a1'])],
  ("A list of tasks, removing finished ones.", "O(total)", "O(n)"),
  ("A <code>deque</code>: pop left, run one step, push back.", "O(total)", "O(n)"),
  names=["specs"])


@B
def round_robin(specs):
    log = []

    def task(name, steps):
        for i in range(steps):
            log.append(f"{name}{i}")
            yield
    tasks = [task(n, s) for n, s in specs]
    while tasks:
        for t in list(tasks):
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
    return log


@O
def round_robin(specs):
    log = []

    def task(name, steps):
        for i in range(steps):
            log.append(f"{name}{i}")
            yield
    ready = deque(task(n, s) for n, s in specs)
    while ready:
        t = ready.popleft()
        try:
            next(t)
            ready.append(t)
        except StopIteration:
            pass
    return log


Q(None, "Keep a List Sorted", "Easy", "bisect",
  "Insert each value into a sorted list, keeping it sorted, and return the final list and the position where target would go.",
  [(([5, 1, 3], 4), ([1, 3, 5], 2))],
  ("Scan for the position each time.", "O(n²)", "O(n)"),
  ("<code>bisect</code> finds the position in O(log n), though inserting still shifts items.", "O(n²) worst, fast finds", "O(n)"),
  names=["values", "target"])


@B
def sorted_insert(values, target):
    out = []
    for v in values:
        i = 0
        while i < len(out) and out[i] < v:
            i += 1
        out.insert(i, v)
    pos = 0
    while pos < len(out) and out[pos] < target:
        pos += 1
    return (out, pos)


@O
def sorted_insert(values, target):
    out = []
    for v in values:
        bisect.insort(out, v)
    return (out, bisect.bisect_left(out, target))
