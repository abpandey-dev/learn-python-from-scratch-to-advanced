from lib import *

LESSON("Basics", "List comprehensions", """
<p>A <b>list comprehension</b> builds a list in one readable line. These two are the same:</p>
<pre><code class="py">squares = []
for x in range(5):
    squares.append(x * x)

squares = [x * x for x in range(5)]</code></pre>
<p>Read it as: "<i>x * x</i>, <b>for</b> each x <b>in</b> range(5)". Add a filter at the end:</p>
<pre><code class="py">evens = [x for x in nums if x % 2 == 0]</code></pre>
<p>And choose between two values with a conditional expression at the front:</p>
<pre><code class="py">labels = ["even" if x % 2 == 0 else "odd" for x in nums]</code></pre>
""", practice=["Squares", "Keep the Even Numbers", "Label Even and Odd", "All Positions of a Value"])


@LD
def list_comp_demo():
    nums = [3, 8, 5, 12]
    squares = [x * x for x in nums]
    evens = [x for x in nums if x % 2 == 0]
    labels = ["big" if x > 6 else "small" for x in nums]
    print(squares, evens, labels)


LESSON("Basics", "Dict and set comprehensions", """
<pre><code class="py">lengths = {w: len(w) for w in words}          # dict: key: value
unique_lengths = {len(w) for w in words}       # set: duplicates vanish
inverted = {v: k for k, v in d.items()}</code></pre>
<p>Nested comprehensions read in the same order as nested loops:</p>
<pre><code class="py">grid = [[r * c for c in range(3)] for r in range(3)]   # list of rows
flat = [x for row in grid for x in row]                # flatten</code></pre>
<div class="tip">If a comprehension no longer fits comfortably on one line, a normal loop is clearer.</div>
""", practice=["Word Lengths", "Distinct Word Lengths", "Multiplication Grid"])


@LD
def other_comp_demo():
    words = ["hi", "there", "you", "all"]
    lengths = {w: len(w) for w in words}
    unique_lengths = {len(w) for w in words}
    grid = [[r * c for c in range(1, 3)] for r in range(1, 3)]
    flat = [x for row in grid for x in row]
    print(lengths, unique_lengths, grid, flat)


LESSON("Core", "Built-ins that loop for you", """
<table>
<tr><th>Built-in</th><th>Does</th><th>Example</th></tr>
<tr><td><code>enumerate(xs, start=0)</code></td><td>(index, item) pairs</td><td><code>for i, x in enumerate(xs)</code></td></tr>
<tr><td><code>zip(a, b)</code></td><td>items side by side</td><td><code>for x, y in zip(a, b)</code></td></tr>
<tr><td><code>map(f, xs)</code></td><td>apply f to each item</td><td><code>map(int, ["1", "2"])</code></td></tr>
<tr><td><code>filter(f, xs)</code></td><td>keep items where f is true</td><td><code>filter(str.isdigit, parts)</code></td></tr>
<tr><td><code>sorted(xs, key=, reverse=)</code></td><td>new sorted list</td><td><code>sorted(people, key=lambda p: (p[1], p[0]))</code></td></tr>
<tr><td><code>any(xs)</code> / <code>all(xs)</code></td><td>is any / every item truthy?</td><td><code>all(x &gt; 0 for x in nums)</code></td></tr>
<tr><td><code>sum</code>, <code>min</code>, <code>max</code></td><td>aggregate</td><td><code>max(words, key=len)</code></td></tr>
<tr><td><code>reversed(xs)</code></td><td>iterate backwards</td><td><code>for x in reversed(xs)</code></td></tr>
</table>
""", practice=["Pairwise Sums", "Parse and Keep Positives", "All Positive?", "Sort People by Age, Then Name", "Adjacent Differences"])


@LD
def builtins_demo():
    names = ["ana", "ben", "cy"]
    ages = [25, 31, 19]
    for i, (name, age) in enumerate(zip(names, ages), start=1):
        print(i, name, age)
    adults = list(filter(lambda a: a >= 21, ages))
    upper = list(map(str.upper, names))
    print(adults, upper, any(a < 20 for a in ages), all(a > 18 for a in ages))


LESSON("Core", "Iterables and iterators", """
<p>An <b>iterable</b> is anything you can loop over (list, str, dict, range, file). An <b>iterator</b> is the object that actually hands out the items one at a time and remembers where it is.</p>
<pre><code class="py">nums = [10, 20]
it = iter(nums)      # get an iterator
next(it)             # 10
next(it)             # 20
next(it)             # StopIteration — no more items</code></pre>
<p>A <code>for</code> loop does exactly this behind the scenes. An iterator can be used <b>only once</b>; to loop again, ask the iterable for a new one.</p>
""", practice=["Countdown Iterator"])


@LD
def iterator_demo():
    nums = [10, 20, 30]
    it = iter(nums)
    first = next(it)
    second = next(it)
    rest = list(it)
    again = list(it)
    print(first, second, rest, again)


LESSON("Advanced", "Generators and yield", """
<p>A <b>generator function</b> contains <code>yield</code>. Calling it doesn't run the body — it returns a generator. Each <code>next()</code> runs the body until the next <code>yield</code>, hands out that value, and <b>pauses</b> there with all its variables kept.</p>
<pre><code class="py">def countdown(n):
    while n &gt; 0:
        yield n        # pause here, give n to the caller
        n -= 1         # resume from here on the next request

for x in countdown(3):
    print(x)           # 3, 2, 1</code></pre>
<p>In the animation, watch the generator's frame appear on the call stack each time a value is requested, and keep <code>n</code> between requests.</p>
<p>Generators are <b>lazy</b>: they produce values only when asked, so they can represent huge or even infinite sequences using almost no memory.</p>
""", practice=["First n Squares (Generator)", "Fibonacci Up To a Limit", "Batches (Generator)", "Running Average"])


@LD
def generator_demo():
    def countdown(n):
        while n > 0:
            yield n
            n -= 1

    gen = countdown(3)
    print(next(gen))
    for x in gen:
        print("loop got", x)


LESSON("Advanced", "Generator expressions and itertools", """
<p>A <b>generator expression</b> looks like a list comprehension with round brackets. It yields items lazily instead of building a list:</p>
<pre><code class="py">total = sum(x * x for x in range(1_000_000))   # no million-item list in memory</code></pre>
<p>The <code>itertools</code> module has ready-made iterator tools:</p>
<table>
<tr><th>Tool</th><th>Does</th></tr>
<tr><td><code>count(start, step)</code></td><td>endless counter</td></tr>
<tr><td><code>islice(it, n)</code></td><td>first n items of any iterator</td></tr>
<tr><td><code>chain(a, b, …)</code></td><td>one iterable after another</td></tr>
<tr><td><code>groupby(it, key)</code></td><td>runs of equal items</td></tr>
<tr><td><code>product</code>, <code>permutations</code>, <code>combinations</code></td><td>combinatorics</td></tr>
<tr><td><code>accumulate(it)</code></td><td>running totals</td></tr>
<tr><td><code>pairwise(it)</code></td><td>neighbouring pairs (3.10+)</td></tr>
</table>
""", practice=["Take From an Endless Stream", "Sum of Squares Without a List", "Chain Several Lists"])


@LD
def itertools_demo():
    from itertools import count, islice, accumulate
    evens = (n for n in count(0, 2))
    first_five = list(islice(evens, 5))
    totals = list(accumulate([1, 2, 3, 4]))
    big_sum = sum(x * x for x in range(1, 101))
    print(first_five, totals, big_sum)
