from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


LESSON("Basics", "How arrays are stored, and why dtype matters", """
<p>A Python list holds pointers to separate objects scattered around memory. A NumPy array holds raw numbers side by side, <b>all of the same type</b>. That's why it's so fast and compact.</p>
<table><tr><th>dtype</th><th>Bytes each</th><th>Range or use</th><th>1,000 values</th></tr>
<tr><td>int8</td><td>1</td><td>−128 to 127</td><td>1,000 bytes</td></tr>
<tr><td>int64</td><td>8</td><td>very large whole numbers</td><td>8,000 bytes</td></tr>
<tr><td>float64</td><td>8</td><td>decimals (the default)</td><td>8,000 bytes</td></tr></table>
<h4>NumPy picks one type for everything</h4>
<ul><li><code>np.array([1, 2.5])</code> becomes all floats: [1.0, 2.5].</li>
<li><code>np.array([1, 2.5, "3"])</code> becomes all <b>text</b>. Maths now fails, a classic surprise when loading messy data.</li></ul>
<h4>Small types can overflow silently</h4>
<p><code>np.array([127], dtype=np.int8) + 1</code> gives <b>−128</b>, with no error. The value wraps around the end of the range. Use a smaller type only when you know the values fit.</p>
""", practice=["Shape and Size", "Floats to Whole Numbers"])


@LD
def dtype_demo():
    mixed_numbers = np.array([1, 2.5])
    mixed_text = np.array([1, 2.5, "3"])
    small = np.zeros(1000, dtype=np.int8).nbytes
    large = np.zeros(1000, dtype=np.int64).nbytes
    wrapped = np.array([127], dtype=np.int8) + 1
    converted = np.array(["1", "2"]).astype(int)


LESSON("Core", "Reading 2-D slices, worked examples", """
<p>Take <code>m = np.arange(12).reshape(3, 4)</code>:</p>
<pre><code class="py">[[ 0,  1,  2,  3],
 [ 4,  5,  6,  7],
 [ 8,  9, 10, 11]]</code></pre>
<p>Read <code>m[rows, columns]</code>, with a comma between the two.</p>
<table><tr><th>Code</th><th>Means</th><th>Result</th><th>Shape</th></tr>
<tr><td><code>m[1, 2]</code></td><td>row 1, column 2</td><td>6</td><td>single value</td></tr>
<tr><td><code>m[0]</code></td><td>row 0</td><td>[0, 1, 2, 3]</td><td>(4,)</td></tr>
<tr><td><code>m[:, 1]</code></td><td>column 1</td><td>[1, 5, 9]</td><td>(3,)</td></tr>
<tr><td><code>m[1:, 2:]</code></td><td>rows from 1, columns from 2</td><td>[[6, 7], [10, 11]]</td><td>(2, 2)</td></tr>
<tr><td><code>m[::2]</code></td><td>every second row</td><td>rows 0 and 2</td><td>(2, 4)</td></tr>
<tr><td><code>m[:, [1]]</code></td><td>column 1 kept as a column</td><td>[[1], [5], [9]]</td><td>(3, 1)</td></tr></table>
<p><b>Watch the shapes.</b> A single number drops that dimension, while a list or slice keeps it. Many "shape mismatch" errors come from (3,) versus (3, 1).</p>
<p><b>The stop value is excluded</b>, just like Python lists: <code>m[0:2]</code> gives rows 0 and 1.</p>
""", practice=["Read One Cell", "Last Column", "Top-Left Block", "Every Second Element"])


@LD
def slicing_shapes():
    m = np.arange(12).reshape(3, 4)
    cell = m[1, 2]
    row = m[0]
    column = m[:, 1]
    block = m[1:, 2:]
    alternate_rows = m[::2]
    column_kept_2d = m[:, [1]]
    shapes = (row.shape, column.shape, block.shape, column_kept_2d.shape)


LESSON("Core", "Views and copies: a bug worth knowing", """
<p>Slicing doesn't copy the data. It gives a <b>view</b>: a new window onto the same numbers.</p>
<pre><code class="py">a = np.array([1, 2, 3, 4])
b = a[1:3]        # a view
b[0] = 99
# a is now [1, 99, 3, 4]</code></pre>
<p>That's fast, but it can change your original data without you noticing.</p>
<table><tr><th>Operation</th><th>Gives</th></tr>
<tr><td><code>a[1:3]</code>, <code>a.reshape(...)</code>, <code>a.T</code></td><td>view (shares memory)</td></tr>
<tr><td><code>a[a &gt; 1]</code>, <code>a[[0, 2]]</code></td><td>copy</td></tr>
<tr><td><code>a.copy()</code></td><td>copy, on purpose</td></tr></table>
<p><b>Rule:</b> if you plan to change a slice and need the original intact, write <code>.copy()</code>.</p>
<p><b>Assigning through a mask</b> writes to the original, and that's usually what you want: <code>a[a &lt; 0] = 0</code>.</p>
""", practice=["Replace Negatives With Zero", "Flatten a Table"])


@LD
def view_copy_demo():
    a = np.array([1, 2, 3, 4])
    view = a[1:3]
    view[0] = 99
    a_after_view = a.copy()
    safe = a[1:3].copy()
    safe[0] = -1
    a_after_copy = a.copy()
    picked = a[a > 2]
    shares = (np.shares_memory(a, view), np.shares_memory(a, safe), np.shares_memory(a, picked))


LESSON("Advanced", "Masks, where and -1, step by step", """
<h4>Building a mask</h4>
<p>Marks are [35, 72, 90, 48].</p>
<ol><li><code>marks &gt;= 50</code> gives [False, True, True, False].</li>
<li><code>marks[marks &gt;= 50]</code> gives [72, 90].</li>
<li><code>(marks &gt;= 50).sum()</code> gives 2, because True counts as 1.</li>
<li><code>(marks &gt;= 50).mean()</code> gives 0.5: half passed.</li></ol>
<h4>Combining conditions</h4>
<p>Use <code>&amp;</code> (and), <code>|</code> (or), <code>~</code> (not), with <b>brackets around each part</b>:</p>
<pre><code class="py">marks[(marks &gt;= 50) &amp; (marks &lt; 80)]    # [72]</code></pre>
<p>Without brackets, or using the word <code>and</code>, Python raises an error.</p>
<h4>np.where is if/else for a whole array</h4>
<p><code>np.where(marks &gt;= 50, "pass", "fail")</code> gives one answer per element.</p>
<h4>Reshape with -1</h4>
<p>-1 means "work this out for me". With 12 values, <code>reshape(3, -1)</code> gives 3 rows of 4. <code>reshape(5, -1)</code> fails, because 12 doesn't divide by 5.</p>
""", practice=["Count Values Above a Threshold", "Reshape Into Rows", "Pick Items by Position", "Position of the Largest Value"])


@LD
def mask_steps():
    marks = np.array([35, 72, 90, 48])
    passed_mask = marks >= 50
    passed = marks[passed_mask]
    how_many = passed_mask.sum()
    share = passed_mask.mean()
    middle = marks[(marks >= 50) & (marks < 80)]
    labels = np.where(marks >= 50, "pass", "fail")
    rows = np.arange(12).reshape(3, -1)
