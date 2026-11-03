from lib import *

LESSON("Basics", "Tuples: lists that can't change", """
<p>A <b>tuple</b> is an ordered collection like a list, written with round brackets — but it is <b>immutable</b>: once created, you can't add, remove or replace items.</p>
<pre><code class="py">point = (3, 4)
rgb = (255, 128, 0)
point[0]          # 3 — indexing and slicing work
point[0] = 9      # TypeError: 'tuple' object does not support item assignment</code></pre>
<p>The comma makes the tuple, not the brackets: <code>t = 1, 2</code> is a tuple, and a one-item tuple needs a trailing comma: <code>(5,)</code>. <code>(5)</code> is just the number 5.</p>
<p>Use a tuple for a fixed group of values that belong together: coordinates, a date (y, m, d), a database row.</p>
""", practice=["Count in a Tuple", "Swap a Pair"])


@LD
def tuple_demo():
    point = (3, 4)
    x = point[0]
    single = (5,)
    not_tuple = (5)
    t = 1, 2, 3
    print(point, x, single, not_tuple, t, type(single), type(not_tuple))


LESSON("Basics", "Packing and unpacking", """
<p><b>Packing</b>: writing values separated by commas creates a tuple. <b>Unpacking</b>: assigning a tuple to several names splits it:</p>
<pre><code class="py">record = ("Ana", 21, "Pune")       # packing
name, age, city = record           # unpacking
a, b = b, a                        # swap: pack (b, a), then unpack
first, *rest = [1, 2, 3, 4]        # first = 1, rest = [2, 3, 4]
for name, score in [("a", 1), ("b", 2)]:   # unpacking in loops
    ...</code></pre>
<p>Functions return several values the same way: <code>return lo, hi</code> returns one tuple, which the caller can unpack.</p>
""", practice=["Describe a Record", "Min and Max Together", "Sum, Mean and Max", "Unzip Pairs"])


@LD
def unpack_demo():
    record = ("Ana", 21, "Pune")
    name, age, city = record
    first, *rest = [10, 20, 30, 40]

    def low_high(nums):
        return min(nums), max(nums)

    lo, hi = low_high([4, 9, 1])
    print(name, age, city, first, rest, lo, hi)


LESSON("Core", "Sets: unique items, fast lookup", """
<p>A <b>set</b> is an <b>unordered</b> collection of <b>unique</b> items, written with curly braces:</p>
<pre><code class="py">colors = {"red", "green", "red"}   # {'red', 'green'} — duplicate dropped
empty = set()                      # {} would be an empty DICT
colors.add("blue")
colors.discard("pink")             # no error if missing (remove() would raise)
"red" in colors                    # True — and very fast</code></pre>
<p>Sets have no index (<code>colors[0]</code> is an error) and no fixed order. In return, checking membership takes about the same time no matter how big the set is — O(1) — while a list must scan every item.</p>
""", practice=["Count Unique Values", "Has Duplicates?", "Unique Words, Ignoring Case"])


@LD
def set_basics_demo():
    nums = [3, 1, 3, 2, 1, 3]
    unique = set(nums)
    unique.add(10)
    unique.discard(99)
    has_two = 2 in unique
    print(unique, len(unique), has_two)


LESSON("Core", "Set operations", """
<table>
<tr><th>Operation</th><th>Operator</th><th>Method</th><th>{1, 2, 3} with {2, 3, 4}</th></tr>
<tr><td>Union (either)</td><td><code>a | b</code></td><td><code>a.union(b)</code></td><td>{1, 2, 3, 4}</td></tr>
<tr><td>Intersection (both)</td><td><code>a &amp; b</code></td><td><code>a.intersection(b)</code></td><td>{2, 3}</td></tr>
<tr><td>Difference (a only)</td><td><code>a - b</code></td><td><code>a.difference(b)</code></td><td>{1}</td></tr>
<tr><td>Symmetric difference (exactly one)</td><td><code>a ^ b</code></td><td><code>a.symmetric_difference(b)</code></td><td>{1, 4}</td></tr>
<tr><td>Subset / superset</td><td><code>a &lt;= b</code>, <code>a &gt;= b</code></td><td><code>issubset</code>, <code>issuperset</code></td><td>False</td></tr>
<tr><td>No common items?</td><td>—</td><td><code>a.isdisjoint(b)</code></td><td>False</td></tr>
</table>
<p>These are the Venn diagrams from maths class, built in.</p>
""", practice=["Common Letters", "Union of Two Lists", "In First List Only", "In Exactly One List", "Is It a Subset?", "Missing Numbers"])


@LD
def set_ops_demo():
    python_club = {"ana", "ben", "cy"}
    chess_club = {"ben", "dia"}
    both = python_club & chess_club
    either = python_club | chess_club
    only_python = python_club - chess_club
    exactly_one = python_club ^ chess_club
    print(both, either, only_python, exactly_one)


LESSON("Advanced", "Hashability, frozenset and when to use what", """
<p>Sets and dict keys use <b>hashing</b>, so their items must be <b>hashable</b> — values that never change: numbers, strings, tuples of hashables, frozensets. Lists, dicts and sets are not hashable.</p>
<pre><code class="py">visited = {(0, 0), (1, 2)}        # tuples are fine
bad = {[0, 0]}                    # TypeError: unhashable type: 'list'
frozen = frozenset({1, 2})        # an immutable set — can go inside a set or be a dict key</code></pre>
<table>
<tr><th>Need</th><th>Use</th></tr>
<tr><td>ordered, changeable collection</td><td>list</td></tr>
<tr><td>fixed record, dict key, return several values</td><td>tuple</td></tr>
<tr><td>unique items, fast "is x in it?", set algebra</td><td>set</td></tr>
<tr><td>a set that must not change</td><td>frozenset</td></tr>
</table>
""", practice=["Distinct Cells Visited", "Two Numbers Add Up", "Pair Up Two Lists"])


@LD
def hashable_demo():
    seen = set()
    for move in [(0, 1), (1, 1), (0, 1)]:
        seen.add(move)
    groups = {frozenset({"a", "b"}): "team 1"}
    print(seen, groups[frozenset({"b", "a"})])
