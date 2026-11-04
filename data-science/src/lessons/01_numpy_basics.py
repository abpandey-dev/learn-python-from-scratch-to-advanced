from lib import *
import numpy as np

LESSON("Basics", "Why NumPy?", """
<p>Python lists can hold anything, but that flexibility makes maths on them slow: every item is a separate Python object and a loop handles one at a time. <b>NumPy</b> stores numbers in one compact block of memory, all of the same type, and runs operations on the whole block in fast compiled code.</p>
<pre><code class="py">import numpy as np          # the standard way to import it
prices = np.array([10, 20, 30])
prices * 1.18               # array([11.8, 23.6, 35.4]) — no loop</code></pre>
<p>That is called <b>vectorisation</b>: you write the operation once and it applies to every element. It is typically 10–100× faster than a Python loop and much shorter to read. Pandas, Matplotlib, Seaborn and scikit-learn are all built on NumPy arrays.</p>
""", practice=["Double Every Number"])


@LD
def why_numpy():
    prices = [10, 20, 30]
    with_tax = []
    for p in prices:
        with_tax.append(p * 1.18)
    arr = np.array(prices)
    arr_with_tax = arr * 1.18
    print(with_tax)
    print(arr_with_tax)


LESSON("Basics", "Creating arrays", """
<table>
<tr><th>Code</th><th>Gives</th></tr>
<tr><td><code>np.array([1, 2, 3])</code></td><td>from a list</td></tr>
<tr><td><code>np.array([[1, 2], [3, 4]])</code></td><td>2-D array from a nested list</td></tr>
<tr><td><code>np.zeros(5)</code>, <code>np.ones((2, 3))</code></td><td>filled with 0 / 1 (floats by default)</td></tr>
<tr><td><code>np.full((2, 2), 7)</code></td><td>filled with a value</td></tr>
<tr><td><code>np.arange(0, 10, 2)</code></td><td>like range: 0 2 4 6 8</td></tr>
<tr><td><code>np.linspace(0, 1, 5)</code></td><td>5 evenly spaced numbers, both ends included</td></tr>
<tr><td><code>np.eye(3)</code></td><td>identity matrix</td></tr>
<tr><td><code>np.random.default_rng(0).integers(1, 7, 10)</code></td><td>10 random dice rolls (seeded, so repeatable)</td></tr>
</table>
""", practice=["Evenly Spaced Numbers", "Identity Matrix", "Checkerboard"])


@LD
def creating_demo():
    a = np.array([1, 2, 3])
    zeros = np.zeros(4)
    grid = np.ones((2, 3), dtype=int)
    evens = np.arange(0, 10, 2)
    steps = np.linspace(0, 1, 5)
    rolls = np.random.default_rng(0).integers(1, 7, 6)
    print(a, zeros, evens, steps, rolls, sep="\n")


LESSON("Core", "Shape, dimensions and dtype", """
<p>Every array has:</p>
<ul>
<li><code>ndim</code> — number of dimensions (axes): 1 for a row of numbers, 2 for a table.</li>
<li><code>shape</code> — length along each axis: <code>(3,)</code> for 3 numbers, <code>(2, 3)</code> for 2 rows × 3 columns.</li>
<li><code>size</code> — total number of elements.</li>
<li><code>dtype</code> — the one type every element shares: <code>int64</code>, <code>float64</code>, <code>bool</code>, <code>&lt;U5</code> (text)…</li>
</ul>
<p>Mixing types upgrades everything to a common type: <code>np.array([1, 2.5])</code> is all floats. Convert with <code>arr.astype(int)</code>. In the animations, each array's dtype and shape appear in its label.</p>
""", practice=["Shape and Size", "Floats to Whole Numbers"])


@LD
def shape_demo():
    table = np.array([[1, 2, 3], [4, 5, 6]])
    rows, cols = table.shape
    mixed = np.array([1, 2.5, 3])
    as_int = mixed.astype(int)
    print(table.ndim, table.shape, table.size, table.dtype)
    print(mixed.dtype, as_int, as_int.dtype)


LESSON("Core", "Indexing and slicing", """
<p>1-D arrays index like lists. 2-D arrays take <b>row, column</b> inside one pair of brackets:</p>
<pre><code class="py">m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
m[1, 2]        # 6        row 1, column 2
m[0]           # [1 2 3]  the whole first row
m[:, 0]        # [1 4 7]  every row, column 0
m[:2, 1:]      # [[2 3] [5 6]]  a block
m[::-1]        # rows in reverse order</code></pre>
<div class="warn">A slice is a <b>view</b>: it shares memory with the original, so changing the slice changes the original. Use <code>m[:2].copy()</code> when you need an independent array.</div>
""", practice=["Read One Cell", "Last Column", "Top-Left Block", "Reverse an Array", "Every Second Element", "Main Diagonal"])


@LD
def slicing_demo():
    m = np.arange(1, 10).reshape(3, 3)
    cell = m[1, 2]
    first_col = m[:, 0]
    block = m[:2, 1:]
    view = m[0]
    view[0] = 100
    print(cell, first_col, block, m, sep="\n")


LESSON("Advanced", "Boolean masks and fancy indexing", """
<p>Comparing an array gives an array of True/False — a <b>mask</b>. Indexing with a mask keeps the elements where it's True:</p>
<pre><code class="py">scores = np.array([45, 82, 67, 91])
mask = scores &gt;= 60            # [False  True  True  True]
scores[mask]                   # [82 67 91]
scores[(scores &gt; 50) &amp; (scores &lt; 90)]   # combine with &amp; | ~  (and brackets!)
np.where(scores &gt;= 60, "pass", "fail")
(scores &gt;= 60).sum()           # count: True counts as 1</code></pre>
<p><b>Fancy indexing</b> picks elements by a list of positions: <code>scores[[0, 3]]</code> → <code>[45 91]</code>. Unlike slices, masks and fancy indexing return <b>copies</b>.</p>
<div class="warn">Use <code>&amp;</code>, <code>|</code>, <code>~</code> with arrays, not <code>and</code>, <code>or</code>, <code>not</code> — and put each comparison in brackets.</div>
""", practice=["Count Values Above a Threshold", "Replace Negatives With Zero", "Pick Items by Position", "Position of the Largest Value"])


@LD
def mask_demo():
    scores = np.array([45, 82, 67, 91])
    passed = scores >= 60
    good = scores[passed]
    middle = scores[(scores > 50) & (scores < 90)]
    labels = np.where(passed, "pass", "fail")
    picked = scores[[0, 3]]
    print(good, middle, labels, picked, passed.sum())


LESSON("Advanced", "Reshaping and combining", """
<table>
<tr><th>Operation</th><th>Example</th></tr>
<tr><td>Reshape (same data, new shape)</td><td><code>np.arange(6).reshape(2, 3)</code>; use −1 for "work it out"</td></tr>
<tr><td>Flatten to 1-D</td><td><code>m.ravel()</code> (view if possible), <code>m.flatten()</code> (copy)</td></tr>
<tr><td>Transpose</td><td><code>m.T</code></td></tr>
<tr><td>Add an axis</td><td><code>a[:, np.newaxis]</code> or <code>a.reshape(-1, 1)</code> (column vector)</td></tr>
<tr><td>Stack vertically / horizontally</td><td><code>np.vstack([a, b])</code>, <code>np.hstack([a, b])</code></td></tr>
<tr><td>Join along an axis</td><td><code>np.concatenate([a, b], axis=0)</code></td></tr>
<tr><td>Unique values</td><td><code>np.unique(a, return_counts=True)</code></td></tr>
</table>
<p>Reshape never changes the number of elements — <code>reshape(4, 2)</code> on 6 elements raises an error.</p>
""", practice=["Flatten a Table", "Reshape Into Rows", "Stack Two Rows", "Unique Values and Their Counts"])


@LD
def reshape_demo():
    a = np.arange(6)
    grid = a.reshape(2, 3)
    tall = a.reshape(-1, 1)
    flipped = grid.T
    both = np.vstack([grid, grid * 10])
    values, counts = np.unique([3, 1, 3, 2, 3], return_counts=True)
    print(grid, flipped, both, values, counts, sep="\n")
