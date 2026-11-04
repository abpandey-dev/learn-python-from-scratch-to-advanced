from lib import *
import numpy as np

LESSON("Basics", "Element-wise maths", """
<p>Arithmetic between arrays of the same shape works <b>element by element</b>; arithmetic with a single number applies it to every element:</p>
<pre><code class="py">a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b        # [11 22 33]
a * b        # [10 40 90]   (not a matrix product!)
a ** 2       # [1 4 9]
a / 2        # [0.5 1.  1.5]</code></pre>
<p>NumPy's <b>universal functions</b> (ufuncs) do the same for maths functions: <code>np.sqrt, np.exp, np.log, np.abs, np.round, np.sin</code>…</p>
""", practice=["Add Two Lists Element by Element", "Scale to 0–1 (Min-Max)", "Clip to a Range"])


@LD
def elementwise_demo():
    a = np.array([1, 2, 3])
    b = np.array([10, 20, 30])
    total = a + b
    product = a * b
    squared = a ** 2
    roots = np.sqrt(b).round(2)
    print(total, product, squared, roots)


LESSON("Basics", "Aggregations and axes", """
<p>Aggregations reduce many numbers to one: <code>sum, mean, median, std, var, min, max, argmin, argmax, prod, cumsum</code>.</p>
<p>On a 2-D array, <code>axis</code> chooses the direction:</p>
<div class="pic">m = [[1, 2, 3],
     [4, 5, 6]]
m.sum()         → 21              everything
m.sum(axis=0)   → [5 7 9]         down the rows   (one per column)
m.sum(axis=1)   → [6 15]          across columns  (one per row)</div>
<p>Memory trick: the axis you name is the one that <b>disappears</b>.</p>
""", practice=["Mean and Standard Deviation", "Row Totals", "Column Averages", "Running Total"])


@LD
def axes_demo():
    m = np.array([[1, 2, 3], [4, 5, 6]])
    everything = m.sum()
    per_column = m.sum(axis=0)
    per_row = m.sum(axis=1)
    col_means = m.mean(axis=0)
    print(everything, per_column, per_row, col_means)


LESSON("Core", "Broadcasting", """
<p><b>Broadcasting</b> lets NumPy combine arrays of different shapes by virtually stretching the smaller one. Shapes are compared from the right; two sizes are compatible if they are equal or one of them is 1.</p>
<div class="pic">(3, 2) table  +  (2,) row      → row is repeated for each of the 3 rows
(3, 1) column +  (1, 4) row    → (3, 4) grid of every combination
(3, 2)        +  (3,)          → error: 2 vs 3 don't match</div>
<p>No data is actually copied, so broadcasting is fast and memory-friendly. It's how you subtract column means, scale features, or build multiplication tables and distance matrices in one line.</p>
""", practice=["Add a Row to Every Row", "Multiplication Table", "Z-Scores", "Distance Matrix"])


@LD
def broadcasting_demo():
    scores = np.array([[70, 80], [60, 90], [80, 70]])
    col_means = scores.mean(axis=0)
    centred = scores - col_means
    col = np.arange(1, 4).reshape(3, 1)
    row = np.arange(1, 5)
    table = col * row
    print(col_means, centred, table, sep="\n")


LESSON("Core", "Linear algebra", """
<table>
<tr><th>Task</th><th>Code</th></tr>
<tr><td>Dot product of vectors</td><td><code>a @ b</code> or <code>np.dot(a, b)</code></td></tr>
<tr><td>Matrix × matrix / vector</td><td><code>A @ B</code>, <code>A @ v</code></td></tr>
<tr><td>Transpose</td><td><code>A.T</code></td></tr>
<tr><td>Identity</td><td><code>np.eye(n)</code></td></tr>
<tr><td>Determinant / inverse</td><td><code>np.linalg.det(A)</code>, <code>np.linalg.inv(A)</code></td></tr>
<tr><td>Solve A x = b</td><td><code>np.linalg.solve(A, b)</code> (better than inv(A) @ b)</td></tr>
<tr><td>Vector length</td><td><code>np.linalg.norm(v)</code></td></tr>
</table>
<div class="warn"><code>A * B</code> multiplies element by element. The matrix product is <code>A @ B</code>; their inner dimensions must match.</div>
""", practice=["Dot Product", "Matrix Multiplication", "Transpose", "Solve Two Equations"])


@LD
def linalg_demo():
    A = np.array([[2, 1], [1, 3]])
    b = np.array([3, 5])
    x = np.linalg.solve(A, b)
    check = A @ x
    elementwise = A * A
    product = A @ A
    print(x.round(2), check, elementwise, product, sep="\n")


LESSON("Advanced", "Handy numeric recipes", """
<table>
<tr><th>Need</th><th>Recipe</th></tr>
<tr><td>Differences between neighbours</td><td><code>np.diff(a)</code></td></tr>
<tr><td>Percent change</td><td><code>np.diff(a) / a[:-1] * 100</code></td></tr>
<tr><td>Moving average</td><td><code>np.convolve(a, np.ones(k) / k, "valid")</code></td></tr>
<tr><td>Sort / order of sorting</td><td><code>np.sort(a)</code>, <code>a.argsort()</code></td></tr>
<tr><td>Count integers 0…k</td><td><code>np.bincount(a)</code></td></tr>
<tr><td>Random numbers (repeatable)</td><td><code>rng = np.random.default_rng(42); rng.normal(0, 1, 100)</code></td></tr>
<tr><td>Missing values</td><td><code>np.nan</code>, <code>np.isnan(a)</code>, <code>np.nanmean(a)</code></td></tr>
</table>
<p>The rule behind every optimal answer in this topic: <b>replace Python loops with whole-array operations</b>.</p>
""", practice=["Moving Average", "Day-to-Day Percent Change", "Count Each Value", "Sort Rows by a Column", "Keep the Even Numbers"])


@LD
def recipes_demo():
    prices = np.array([100.0, 110.0, 99.0, 121.0])
    change = np.diff(prices)
    pct = (change / prices[:-1] * 100).round(1)
    smooth = np.convolve(prices, np.ones(2) / 2, mode="valid")
    with_gap = np.array([1.0, np.nan, 3.0])
    print(pct, smooth, np.nanmean(with_gap))
