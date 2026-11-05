from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


LESSON("Basics", "Understanding axis once and for all", """
<p><code>axis</code> confuses almost everyone at first. Here's the rule: <b>the axis you name is the one that disappears.</b></p>
<pre><code class="py">m = [[1, 2, 3],
     [4, 5, 6]]      # shape (2, 3)</code></pre>
<table><tr><th>Code</th><th>What collapses</th><th>Result</th><th>Shape</th></tr>
<tr><td><code>m.sum()</code></td><td>everything</td><td>21</td><td>single value</td></tr>
<tr><td><code>m.sum(axis=0)</code></td><td>the rows: adds <b>down</b> each column</td><td>[5, 7, 9]</td><td>(3,)</td></tr>
<tr><td><code>m.sum(axis=1)</code></td><td>the columns: adds <b>across</b> each row</td><td>[6, 15]</td><td>(2,)</td></tr>
<tr><td><code>m.sum(axis=1, keepdims=True)</code></td><td>same, keeping a column shape</td><td>[[6], [15]]</td><td>(2, 1)</td></tr></table>
<h4>Why keepdims helps</h4>
<p>To turn each row into shares of its total, you need <code>m / m.sum(axis=1, keepdims=True)</code>. The result's first row is 1/6, 2/6, 3/6. Without <code>keepdims</code>, shapes (2, 3) and (2,) don't line up and you get an error.</p>
""", practice=["Row Totals", "Column Averages", "Mean and Standard Deviation"])


@LD
def axis_demo():
    m = np.array([[1, 2, 3], [4, 5, 6]])
    total = m.sum()
    down_columns = m.sum(axis=0)
    across_rows = m.sum(axis=1)
    kept = m.sum(axis=1, keepdims=True)
    shares = (m / kept).round(3)


LESSON("Core", "The broadcasting rule, step by step", """
<p>Line up the shapes <b>from the right</b>. Two sizes are compatible if they're <b>equal, or one of them is 1</b>. A missing size counts as 1.</p>
<table><tr><th>Shape A</th><th>Shape B</th><th>Compare from the right</th><th>Result</th></tr>
<tr><td>(3, 2)</td><td>a single number</td><td>number stretches everywhere</td><td>(3, 2)</td></tr>
<tr><td>(3, 2)</td><td>(2,)</td><td>2 = 2, then 3 vs missing</td><td>(3, 2)</td></tr>
<tr><td>(3, 1)</td><td>(1, 2)</td><td>1 vs 2, then 3 vs 1</td><td>(3, 2)</td></tr>
<tr><td>(3, 2)</td><td>(3,)</td><td><b>2 vs 3: neither is 1</b></td><td><b>error</b></td></tr></table>
<h4>Fixing the error</h4>
<p>To apply one value per <b>row</b>, make it a column: <code>b[:, None]</code> turns (3,) into (3, 1), and then (3, 2) with (3, 1) works.</p>
<h4>Worked example: centring columns</h4>
<p><code>X - X.mean(axis=0)</code> subtracts a shape (2,) array from (3, 2), so each column loses its own mean, with no loop.</p>
<h4>Be careful</h4>
<p>(3,) with (3, 1) doesn't raise an error. It silently gives a 3 × 3 table, which is a common bug. If a result is unexpectedly large, print the shapes.</p>
""", practice=["Add a Row to Every Row", "Multiplication Table", "Distance Matrix"])


@LD
def broadcasting_cases():
    X = np.array([[1, 2], [3, 4], [5, 6]])
    per_column = np.array([10, 20])
    add_columns = X + per_column
    per_row = np.array([1, 2, 3])
    add_rows = X + per_row[:, None]
    surprise = (per_row + per_row[:, None]).shape
    centred = X - X.mean(axis=0)


LESSON("Core", "From a loop to one line", """
<p>Vectorising means describing the whole operation instead of each step. Use this recipe:</p>
<ol><li>Write the loop, and be sure it's correct.</li>
<li>Find what's computed per element.</li>
<li>Replace <code>if</code> with a mask or <code>np.where</code>.</li>
<li>Replace running totals with <code>.sum()</code>, <code>.cumsum()</code> or <code>.mean()</code>.</li>
<li>Test both on a small input.</li></ol>
<h4>Worked example</h4>
<p>Prices above 100 get 10% off, and we want the total.</p>
<pre><code class="py">total = 0                         # loop
for p in prices:
    if p &gt; 100:
        p = p * 0.9
    total += p

np.where(prices &gt; 100, prices * 0.9, prices).sum()   # same result</code></pre>
<p>For prices 50, 120, 200: the discounted values are 50, 108, 180, giving a total of 338 both ways.</p>
<p><b>Keep the loop when</b> each step depends on the previous result in a way NumPy has no function for. Clear, correct code beats clever code.</p>
""", practice=["Keep the Even Numbers", "Clip to a Range", "Running Total", "Moving Average", "Day-to-Day Percent Change"])


@LD
def vectorise_demo():
    prices = np.array([50.0, 120.0, 200.0])
    loop_total = 0
    for p in prices:
        if p > 100:
            p = p * 0.9
        loop_total += p
    discounted = np.where(prices > 100, prices * 0.9, prices)
    vector_total = discounted.sum()


LESSON("Advanced", "NaN, infinity and float traps", """
<table><tr><th>Code</th><th>Result</th><th>Why</th></tr>
<tr><td><code>0.1 + 0.2 == 0.3</code></td><td>False</td><td>binary floats can't hold 0.1 exactly</td></tr>
<tr><td><code>np.isclose(0.1 + 0.2, 0.3)</code></td><td>True</td><td>the right way to compare floats</td></tr>
<tr><td><code>np.nan == np.nan</code></td><td>False</td><td>NaN never equals anything; use <code>np.isnan</code></td></tr>
<tr><td><code>np.array([1, np.nan]).mean()</code></td><td>nan</td><td>one NaN poisons the result</td></tr>
<tr><td><code>np.nanmean([1, np.nan])</code></td><td>1.0</td><td>ignores NaN</td></tr>
<tr><td><code>np.array([1.0]) / 0</code></td><td>inf, with a warning</td><td>no exception is raised</td></tr></table>
<p><b>Debugging tip:</b> when results become NaN, find the first one: <code>np.isnan(a).any()</code> and <code>np.isinf(a).any()</code>. Common sources are dividing by zero and the log of 0 or of a negative number.</p>
<p>Unlike pandas, NumPy's plain <code>mean</code> and <code>sum</code> don't skip NaN.</p>
""", practice=["Mean and Standard Deviation", "Z-Scores"])


@LD
def nan_traps():
    float_equal = 0.1 + 0.2 == 0.3
    float_close = bool(np.isclose(0.1 + 0.2, 0.3))
    nan_equal = np.nan == np.nan
    with_gap = np.array([1.0, np.nan, 3.0])
    plain_mean = with_gap.mean()
    skip_mean = np.nanmean(with_gap)
    gaps = np.isnan(with_gap)


LESSON("Advanced", "Random numbers and simulation", """
<p>NumPy can simulate what's hard to calculate. Always create a generator with a <b>seed</b>, so the results can be repeated:</p>
<pre><code class="py">rng = np.random.default_rng(42)
rng.integers(1, 7, size=5)      # dice rolls (the top value is excluded)
rng.normal(0, 1, size=1000)     # bell curve
rng.choice(items, size=3)       # pick randomly
rng.permutation(10)             # shuffle</code></pre>
<h4>Worked example: dice</h4>
<p>The true average of a die is 3.5. The chart rolls more and more dice: the running average wobbles at first and then settles at 3.5. That's the <b>law of large numbers</b>, and it's why more data gives more stable estimates.</p>
<p><b>Common mistake:</b> <code>rng.integers(1, 6)</code> never gives a 6, since the top is excluded.</p>
""", practice=["Count Each Value"])


@LD
def dice_simulation():
    rng = np.random.default_rng(42)
    rolls = rng.integers(1, 7, size=2000)
    running = rolls.cumsum() / np.arange(1, 2001)
    final_average = running[-1]
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.plot(running)
    ax.axhline(3.5, ls="--", color="#b45309")
    ax.set_xscale("log")
    ax.set_xlabel("number of rolls (log scale)")
    ax.set_ylabel("running average")
