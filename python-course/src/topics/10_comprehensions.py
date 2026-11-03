from lib import *

TOPIC(
    id="comprehensions", title="Comprehensions, Iterators & Generators", glyph="[x for x]",
    blurb="Build collections in one line, use the iteration built-ins, and produce values lazily with generators.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">[x * x for x in nums]                 # list comprehension
[x for x in nums if x &gt; 0]            # with a filter
[a if c else b for x in xs]           # if/else inside goes BEFORE for
{w: len(w) for w in words}            # dict comprehension
{x % 3 for x in nums}                 # set comprehension
(x * x for x in nums)                 # generator expression (lazy)
enumerate, zip, map, filter, sorted, reversed, any, all, sum, min, max
def gen():                            # generator function
    yield 1
    yield 2
it = iter([1, 2]); next(it)           # iterator protocol</code></pre>
""")

LIST = lambda r: list(r)


Q(None, "Squares", "Easy", "List comprehension",
  "Return the squares of the numbers in the list.",
  [(([1, 2, 3],), [1, 4, 9]), (([],), [])],
  ("Loop and append.", "O(n)", "O(n)"),
  ("<code>[x * x for x in nums]</code>.", "O(n)", "O(n)"))


@B
def squares(nums):
    result = []
    for x in nums:
        result.append(x * x)
    return result


@O
def squares(nums):
    return [x * x for x in nums]


Q(None, "Keep the Even Numbers", "Easy", "Filtering",
  "Return only the even numbers, in order.",
  [(([1, 2, 3, 4, 6],), [2, 4, 6]), (([1, 3],), [])],
  ("Loop with an if and append.", "O(n)", "O(n)"),
  ("A comprehension with an <code>if</code> clause.", "O(n)", "O(n)"))


@B
def evens(nums):
    out = []
    for x in nums:
        if x % 2 == 0:
            out.append(x)
    return out


@O
def evens(nums):
    return [x for x in nums if x % 2 == 0]


Q(None, "Word Lengths", "Easy", "Dict comprehension",
  "Return a dict mapping each word to its length.",
  [((["hi", "there"],), {"hi": 2, "there": 5}), (([],), {})],
  ("Loop and assign keys.", "O(n)", "O(n)"),
  ("<code>{w: len(w) for w in words}</code>.", "O(n)", "O(n)"))


@B
def word_lengths(words):
    d = {}
    for w in words:
        d[w] = len(w)
    return d


@O
def word_lengths(words):
    return {w: len(w) for w in words}


Q(None, "Distinct Word Lengths", "Easy", "Set comprehension",
  "Return the sorted list of different word lengths in a sentence.",
  [(("the cat sat on a mat",), [1, 2, 3]), (("",), [])],
  ("Collect lengths into a list, skipping ones already present, then sort.", "O(n²)", "O(n)"),
  ("A set comprehension removes duplicates automatically.", "O(n log n)", "O(n)"))


@B
def distinct_lengths(sentence):
    lengths = []
    for w in sentence.split():
        if len(w) not in lengths:
            lengths.append(len(w))
    lengths.sort()
    return lengths


@O
def distinct_lengths(sentence):
    return sorted({len(w) for w in sentence.split()})


Q(None, "Multiplication Grid", "Medium", "Nested comprehension",
  "Return an n × n grid where cell (r, c) is (r + 1) × (c + 1).",
  [((3,), [[1, 2, 3], [2, 4, 6], [3, 6, 9]]), ((1,), [[1]])],
  ("Two nested loops building rows.", "O(n²)", "O(n²)"),
  ("A comprehension inside a comprehension: the outer one builds rows.", "O(n²)", "O(n²)"),
  viz=(3,))


@B
def grid(n):
    rows = []
    for r in range(1, n + 1):
        row = []
        for c in range(1, n + 1):
            row.append(r * c)
        rows.append(row)
    return rows


@O
def grid(n):
    return [[r * c for c in range(1, n + 1)] for r in range(1, n + 1)]


Q(None, "Label Even and Odd", "Easy", "if/else inside a comprehension",
  "Return 'even' or 'odd' for each number.",
  [(([1, 2, 3],), ["odd", "even", "odd"]), (([],), [])],
  ("Loop with if/else and append.", "O(n)", "O(n)"),
  ("A conditional expression before the <code>for</code>: <code>['even' if x % 2 == 0 else 'odd' for x in nums]</code>.", "O(n)", "O(n)"))


@B
def labels(nums):
    out = []
    for x in nums:
        if x % 2 == 0:
            out.append("even")
        else:
            out.append("odd")
    return out


@O
def labels(nums):
    return ["even" if x % 2 == 0 else "odd" for x in nums]


Q(None, "Parse and Keep Positives", "Medium", "map and filter",
  "Given number strings like ['3', '-1', '7'], return the positive values as ints.",
  [((["3", "-1", "7", "0"],), [3, 7]), (([],), [])],
  ("Loop, convert, test, append.", "O(n)", "O(n)"),
  ("<code>filter(lambda x: x &gt; 0, map(int, texts))</code> — or a comprehension.", "O(n)", "O(n)"))


@B
def positives(texts):
    out = []
    for t in texts:
        value = int(t)
        if value > 0:
            out.append(value)
    return out


@O
def positives(texts):
    return list(filter(lambda x: x > 0, map(int, texts)))


Q(None, "Pairwise Sums", "Easy", "zip",
  "Return [a[0] + b[0], a[1] + b[1], …] for two lists of equal length.",
  [(([1, 2, 3], [10, 20, 30]), [11, 22, 33]), (([], []), [])],
  ("Loop over indices.", "O(n)", "O(n)"),
  ("<code>[x + y for x, y in zip(a, b)]</code>.", "O(n)", "O(n)"))


@B
def pairwise_sums(a, b):
    out = []
    for i in range(len(a)):
        out.append(a[i] + b[i])
    return out


@O
def pairwise_sums(a, b):
    return [x + y for x, y in zip(a, b)]


Q(None, "All Positions of a Value", "Easy", "enumerate",
  "Return every index where <code>value</code> appears.",
  [(([1, 3, 1, 2, 1], 1), [0, 2, 4]), ((["a"], "b"), [])],
  ("Loop over range(len()) and compare.", "O(n)", "O(k)"),
  ("<code>[i for i, x in enumerate(items) if x == value]</code>.", "O(n)", "O(k)"))


@B
def positions(items, value):
    out = []
    for i in range(len(items)):
        if items[i] == value:
            out.append(i)
    return out


@O
def positions(items, value):
    return [i for i, x in enumerate(items) if x == value]


Q(None, "All Positive?", "Easy", "all() and any()",
  "Return True if every number is positive.",
  [(([1, 5, 9],), True), (([3, -1],), False), (([],), True)],
  ("Loop and return False at the first non-positive number.", "O(n)", "O(1)"),
  ("<code>all(x &gt; 0 for x in nums)</code> — it also stops at the first False.", "O(n)", "O(1)"))


@B
def all_positive(nums):
    for x in nums:
        if x <= 0:
            return False
    return True


@O
def all_positive(nums):
    return all(x > 0 for x in nums)


Q(None, "Sort People by Age, Then Name", "Medium", "Tuple keys",
  "Sort (name, age) pairs by age ascending, and by name for equal ages.",
  [(([("cy", 30), ("ana", 25), ("ben", 25)],), [("ana", 25), ("ben", 25), ("cy", 30)]), (([],), [])],
  ("Sort by name first, then by age — Python's sort is stable, so names stay ordered within each age.", "O(n log n) × 2", "O(n)"),
  ("One sort with a tuple key <code>(age, name)</code>.", "O(n log n)", "O(n)"))


@B
def sort_people(people):
    by_name = sorted(people, key=lambda p: p[0])
    return sorted(by_name, key=lambda p: p[1])


@O
def sort_people(people):
    return sorted(people, key=lambda p: (p[1], p[0]))


Q(None, "First n Squares (Generator)", "Easy", "yield",
  "Write a generator that yields 1², 2², …, n². (Shown as a list.)",
  [((4,), [1, 4, 9, 16]), ((0,), [])],
  ("Build and return the whole list at once.", "O(n)", "O(n)"),
  ("<code>yield</code> each square — values are produced one at a time, on demand.", "O(n)", "O(1) per value"),
  post=LIST, viz=(4,))


@B
def squares_upto(n):
    result = []
    for i in range(1, n + 1):
        result.append(i * i)
    return result


@O
def squares_upto(n):
    for i in range(1, n + 1):
        yield i * i


Q(None, "Take From an Endless Stream", "Medium", "Infinite generator · islice",
  "Return the first <code>k</code> even numbers starting from 0, using an endless counter in the optimal answer.",
  [((5,), [0, 2, 4, 6, 8]), ((0,), [])],
  ("A while loop with a counter and a list.", "O(k)", "O(k)"),
  ("An infinite generator plus <code>itertools.islice</code> to take just k values.", "O(k)", "O(k)"),
  viz=(4,))


@B
def first_evens(k):
    out, n = [], 0
    while len(out) < k:
        out.append(n)
        n += 2
    return out


@O
def first_evens(k):
    from itertools import count, islice

    def evens():
        for n in count(0, 2):
            yield n

    return list(islice(evens(), k))


Q(None, "Running Average", "Medium", "Generator with state",
  "Return the running averages of a list (rounded to 2 decimals) using a generator in the optimal answer.",
  [(([2, 4, 6],), [2.0, 3.0, 4.0]), (([5],), [5.0]), (([],), [])],
  ("For each position, average the slice up to it.", "O(n²)", "O(n)"),
  ("A generator keeps a running total and count between yields.", "O(n)", "O(1) state"),
  viz=([2, 4, 6],))


@B
def running_avg(nums):
    out = []
    for i in range(len(nums)):
        part = nums[:i + 1]
        out.append(round(sum(part) / len(part), 2))
    return out


@O
def running_avg(nums):
    def averages():
        total = 0
        for count, x in enumerate(nums, start=1):
            total += x
            yield round(total / count, 2)

    return list(averages())


Q(None, "Batches (Generator)", "Medium", "yield slices",
  "Yield the items in batches of size k (last batch may be shorter). Shown as a list.",
  [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([], 3), [])],
  ("Build all the batches in a list first.", "O(n)", "O(n)"),
  ("Yield one slice at a time — memory stays small even for huge inputs.", "O(n)", "O(k)"),
  post=LIST, viz=([1, 2, 3, 4, 5], 2))


@B
def batches(items, k):
    result = []
    for i in range(0, len(items), k):
        result.append(items[i:i + k])
    return result


@O
def batches(items, k):
    for i in range(0, len(items), k):
        yield items[i:i + k]


Q(None, "Fibonacci Up To a Limit", "Medium", "Generator",
  "Yield Fibonacci numbers 0, 1, 1, 2, … that are ≤ limit. Shown as a list.",
  [((10,), [0, 1, 1, 2, 3, 5, 8]), ((0,), [0])],
  ("Build a list with a while loop.", "O(k)", "O(k)"),
  ("A generator with two running variables.", "O(k)", "O(1) state"),
  post=LIST, viz=(10,))


@B
def fib_upto(limit):
    seq = [0, 1]
    while seq[-1] + seq[-2] <= limit:
        seq.append(seq[-1] + seq[-2])
    return [x for x in seq if x <= limit]


@O
def fib_upto(limit):
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


Q(None, "Sum of Squares Without a List", "Easy", "Generator expression",
  "Return 1² + 2² + … + n².",
  [((3,), 14), ((10,), 385), ((0,), 0)],
  ("Build the full list of squares, then sum it.", "O(n)", "O(n)"),
  ("A generator expression inside <code>sum</code> produces each square on demand — no list in memory.", "O(n)", "O(1)"),
  viz=(4,))


@B
def sum_squares(n):
    squares = [i * i for i in range(1, n + 1)]
    return sum(squares)


@O
def sum_squares(n):
    return sum(i * i for i in range(1, n + 1))


Q(None, "Countdown Iterator", "Medium", "Iterator protocol vs generator",
  "Produce n, n − 1, …, 1 as an iterator. (Shown as a list.)",
  [((3,), [3, 2, 1]), ((0,), [])],
  ("A class implementing <code>__iter__</code> and <code>__next__</code>, raising StopIteration at the end.", "O(n)", "O(1)"),
  ("A generator function does the same in three lines — Python writes __next__ for you.", "O(n)", "O(1)"),
  post=LIST, viz=(3,))


@B
def countdown(n):
    class Countdown:
        def __init__(self, start):
            self.current = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            value = self.current
            self.current -= 1
            return value

    return Countdown(n)


@O
def countdown(n):
    while n > 0:
        yield n
        n -= 1


Q(None, "Chain Several Lists", "Easy", "itertools.chain",
  "Return one list with the items of all the given lists in order.",
  [(([1, 2], [3], [4, 5]), [1, 2, 3, 4, 5]), (([],), [])],
  ("Loop over each list and extend a result.", "O(n)", "O(n)"),
  ("<code>itertools.chain(*lists)</code> walks them one after another without copying.", "O(n)", "O(n)"),
  viz=([1, 2], [3], [4, 5]))


@B
def chain_all(*lists):
    out = []
    for lst in lists:
        for x in lst:
            out.append(x)
    return out


@O
def chain_all(*lists):
    from itertools import chain
    return list(chain(*lists))


Q(None, "Adjacent Differences", "Easy", "zip with a shifted copy",
  "Return [b − a for each neighbouring pair (a, b)].",
  [(([1, 4, 9, 16],), [3, 5, 7]), (([5],), []), (([],), [])],
  ("Loop over indices 0 … n − 2.", "O(n)", "O(n)"),
  ("Pair each item with the next using <code>zip(nums, nums[1:])</code> (or <code>itertools.pairwise</code>).", "O(n)", "O(n)"))


@B
def differences(nums):
    out = []
    for i in range(len(nums) - 1):
        out.append(nums[i + 1] - nums[i])
    return out


@O
def differences(nums):
    return [b - a for a, b in zip(nums, nums[1:])]
