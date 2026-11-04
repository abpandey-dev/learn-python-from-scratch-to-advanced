from lib import *

THEORY("Vectorisation", """
<p><b>Vectorisation</b> means expressing a computation as operations on whole arrays instead of explicit Python loops over elements. NumPy then executes the loop in optimised C (often using CPU SIMD instructions), avoiding per-element interpreter overhead and type checks.</p>
<p>Typical speed-ups over pure Python are 10–100×. Vectorised code is also shorter and closer to the mathematical formula.</p>
""")

THEORY("Universal functions (ufuncs)", """
<p>A <b>ufunc</b> is a function that operates element-wise on arrays, supporting broadcasting and type casting.</p>
<table>
<tr><th>Group</th><th>Examples</th></tr>
<tr><td>Arithmetic</td><td><code>add subtract multiply divide floor_divide mod power negative</code> (operators <code>+ - * / // % **</code>)</td></tr>
<tr><td>Comparison</td><td><code>greater less equal</code> (operators <code>&gt; &lt; ==</code>) → bool arrays</td></tr>
<tr><td>Logical</td><td><code>logical_and logical_or logical_not</code> (operators <code>&amp; | ~</code>)</td></tr>
<tr><td>Maths</td><td><code>sqrt exp log log10 abs sin cos round floor ceil</code></td></tr>
</table>
<p>Ufuncs also have methods: <code>np.add.reduce</code> (= sum), <code>np.add.accumulate</code> (= cumsum), <code>np.multiply.outer</code>.</p>
""")

THEORY("Broadcasting rules", """
<ol>
<li>If the arrays have different numbers of dimensions, prepend 1s to the shape of the smaller one.</li>
<li>Two dimensions are compatible when they are equal or one of them is 1.</li>
<li>The result's size along each dimension is the maximum of the two; dimensions of size 1 are stretched.</li>
<li>If any dimension is incompatible, NumPy raises <code>ValueError: operands could not be broadcast together</code>.</li>
</ol>
<table>
<tr><th>A</th><th>B</th><th>Result</th></tr>
<tr><td>(3, 4)</td><td>(4,)</td><td>(3, 4)</td></tr>
<tr><td>(3, 1)</td><td>(1, 4)</td><td>(3, 4)</td></tr>
<tr><td>(5, 1, 3)</td><td>(4, 1)</td><td>(5, 4, 3)</td></tr>
<tr><td>(3, 4)</td><td>(3,)</td><td>error</td></tr>
</table>
""")

THEORY("Aggregations and the axis argument", """
<table>
<tr><th>Function</th><th>NaN-safe version</th></tr>
<tr><td><code>sum, prod</code></td><td><code>nansum, nanprod</code></td></tr>
<tr><td><code>mean, median</code></td><td><code>nanmean, nanmedian</code></td></tr>
<tr><td><code>std, var</code> (ddof=0 by default)</td><td><code>nanstd, nanvar</code></td></tr>
<tr><td><code>min, max, argmin, argmax</code></td><td><code>nanmin, nanmax …</code></td></tr>
<tr><td><code>percentile, quantile</code></td><td><code>nanpercentile</code></td></tr>
<tr><td><code>any, all</code></td><td>—</td></tr>
</table>
<p><code>axis=0</code> collapses rows (result per column); <code>axis=1</code> collapses columns (result per row); <code>keepdims=True</code> keeps the reduced axis with size 1 so the result broadcasts back against the original.</p>
<p><b>ddof</b>: <code>std(ddof=0)</code> is the population standard deviation (divide by n); <code>ddof=1</code> is the sample version (divide by n − 1), which pandas uses by default.</p>
""")

THEORY("Linear algebra", """
<table>
<tr><th>Operation</th><th>NumPy</th><th>Shape rule</th></tr>
<tr><td>Dot product</td><td><code>a @ b</code></td><td>(n,) · (n,) → scalar</td></tr>
<tr><td>Matrix product</td><td><code>A @ B</code></td><td>(m, k) @ (k, n) → (m, n)</td></tr>
<tr><td>Inverse</td><td><code>np.linalg.inv(A)</code></td><td>square, non-singular</td></tr>
<tr><td>Determinant</td><td><code>np.linalg.det(A)</code></td><td>square</td></tr>
<tr><td>Solve linear system</td><td><code>np.linalg.solve(A, b)</code></td><td>A square; more stable than inv</td></tr>
<tr><td>Eigenvalues</td><td><code>np.linalg.eig(A)</code></td><td>square</td></tr>
<tr><td>Least squares</td><td><code>np.linalg.lstsq(A, b)</code></td><td>any</td></tr>
</table>
""")

THEORY("Performance tips", """
<ul>
<li>Avoid Python loops over array elements; look for a ufunc, aggregation or broadcasting expression.</li>
<li>Avoid growing arrays with <code>np.append</code> in a loop (it copies every time); collect in a list and convert once, or preallocate with <code>np.empty</code>.</li>
<li>Prefer views (slices) to copies when you don't need independent data.</li>
<li>Choose smaller dtypes (<code>float32</code>, <code>int32</code>) for large data when precision allows.</li>
<li>Use in-place operators (<code>a += 1</code>, <code>np.multiply(a, 2, out=a)</code>) to save memory.</li>
</ul>
""")

FAQ("What is broadcasting?", "<p>NumPy's rule for combining arrays of different shapes: dimensions are matched from the right and sizes of 1 are virtually stretched, so a row can be added to every row of a table without copying it.</p>")
FAQ("What is the difference between * and @?", "<p><code>*</code> multiplies element by element (shapes must broadcast). <code>@</code> is matrix multiplication (inner dimensions must match).</p>")
FAQ("axis=0 vs axis=1?", "<p>axis=0 aggregates down the rows (one result per column); axis=1 aggregates across the columns (one result per row).</p>")
FAQ("Why is np.std different from pandas .std()?", "<p>NumPy defaults to ddof=0 (population), pandas to ddof=1 (sample, divides by n − 1). Pass ddof explicitly when it matters.</p>")
FAQ("What is a ufunc?", "<p>A universal function: a vectorised function that applies element-wise to arrays with broadcasting, e.g. np.add, np.sqrt, np.exp.</p>")
FAQ("Why is np.append slow in a loop?", "<p>Arrays have a fixed size, so each append allocates a new array and copies all existing data — O(n²) overall. Build a list and convert once, or preallocate.</p>")
