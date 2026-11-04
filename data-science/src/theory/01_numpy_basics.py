from lib import *

THEORY("What NumPy is", """
<p><b>NumPy</b> (Numerical Python) is the fundamental library for numerical computing in Python. Its core object is the <b>ndarray</b> — an N-dimensional, fixed-size, <b>homogeneous</b> array (all elements have the same data type) stored in one contiguous block of memory.</p>
<p>Operations on ndarrays are implemented in C and applied to whole arrays at once (<b>vectorisation</b>), which avoids the overhead of Python loops. NumPy is the base of the scientific Python stack: pandas, SciPy, Matplotlib, scikit-learn, TensorFlow and PyTorch all use or mirror its arrays.</p>
""")

THEORY("ndarray vs Python list", """
<table>
<tr><th></th><th>Python list</th><th>NumPy ndarray</th></tr>
<tr><td>Element types</td><td>any mix</td><td>one dtype</td></tr>
<tr><td>Memory</td><td>array of pointers to separate objects</td><td>one contiguous buffer of raw values</td></tr>
<tr><td>Size</td><td>grows with append</td><td>fixed (creating a bigger one copies)</td></tr>
<tr><td>Arithmetic</td><td><code>+</code> concatenates, <code>*</code> repeats</td><td>element-wise maths</td></tr>
<tr><td>Speed for maths</td><td>slow (interpreted loop)</td><td>fast (compiled, SIMD)</td></tr>
<tr><td>Multi-dimensional</td><td>lists of lists (ragged allowed)</td><td>true N-D with shape</td></tr>
</table>
""")

THEORY("Array attributes", """
<table>
<tr><th>Attribute</th><th>Meaning</th><th>For <code>np.zeros((2, 3))</code></th></tr>
<tr><td><code>ndim</code></td><td>number of axes</td><td>2</td></tr>
<tr><td><code>shape</code></td><td>length of each axis</td><td>(2, 3)</td></tr>
<tr><td><code>size</code></td><td>total elements</td><td>6</td></tr>
<tr><td><code>dtype</code></td><td>element type</td><td>float64</td></tr>
<tr><td><code>itemsize</code></td><td>bytes per element</td><td>8</td></tr>
<tr><td><code>nbytes</code></td><td>total bytes</td><td>48</td></tr>
<tr><td><code>T</code></td><td>transpose</td><td>shape (3, 2)</td></tr>
</table>
<p><b>Axes</b>: axis 0 runs down the rows, axis 1 runs across the columns. Many functions take <code>axis=</code> to choose which direction to work along.</p>
""")

THEORY("Data types (dtype)", """
<table>
<tr><th>Kind</th><th>dtypes</th></tr>
<tr><td>Integers</td><td><code>int8, int16, int32, int64</code>, unsigned <code>uint8 …</code></td></tr>
<tr><td>Floats</td><td><code>float16, float32, float64</code> (default)</td></tr>
<tr><td>Complex</td><td><code>complex64, complex128</code></td></tr>
<tr><td>Boolean</td><td><code>bool</code></td></tr>
<tr><td>Text</td><td><code>&lt;U10</code> (Unicode, fixed max length)</td></tr>
<tr><td>Dates</td><td><code>datetime64</code>, <code>timedelta64</code></td></tr>
<tr><td>Anything</td><td><code>object</code> (Python objects — loses the speed benefit)</td></tr>
</table>
<p><b>Upcasting</b>: when types mix, NumPy picks a type that holds all values: int + float → float. <b>Overflow</b>: fixed-size ints wrap around silently (an <code>int8</code> 127 + 1 becomes −128). Missing values are usually <code>np.nan</code>, which is a float.</p>
""")

THEORY("Indexing rules", """
<table>
<tr><th>Kind</th><th>Syntax</th><th>Returns</th></tr>
<tr><td>Basic index</td><td><code>a[i]</code>, <code>m[i, j]</code></td><td>a scalar or a lower-dimensional view</td></tr>
<tr><td>Slice</td><td><code>a[start:stop:step]</code>, <code>m[:, 1:3]</code></td><td><b>view</b> (shares memory)</td></tr>
<tr><td>Boolean mask</td><td><code>a[a &gt; 0]</code></td><td><b>copy</b> (always 1-D for a full-shape mask)</td></tr>
<tr><td>Fancy (integer array)</td><td><code>a[[0, 2, 4]]</code></td><td><b>copy</b></td></tr>
<tr><td>Ellipsis / new axis</td><td><code>a[..., 0]</code>, <code>a[:, np.newaxis]</code></td><td>view</td></tr>
</table>
<p>Element-wise logical operators for masks: <code>&amp;</code> (and), <code>|</code> (or), <code>~</code> (not), with each comparison in parentheses because <code>&amp;</code> binds tighter than <code>&gt;</code>.</p>
""")

THEORY("Views vs copies", """
<p>Slicing, reshaping (when possible), <code>ravel</code> and <code>.T</code> return <b>views</b>: new array objects that look at the same memory. Writing to a view changes the original. This makes slicing O(1) and memory-cheap.</p>
<p>Use <code>.copy()</code> for an independent array. Check with <code>np.shares_memory(a, b)</code> or <code>b.base is a</code>.</p>
""")

FAQ("Why is NumPy faster than lists?", "<p>Arrays store raw values of one type contiguously, and operations run as compiled loops (often SIMD) over that memory instead of interpreting Python bytecode and unboxing objects for each element.</p>")
FAQ("What is the difference between shape (3,) and (3, 1)?", "<p>(3,) is a 1-D array of 3 elements. (3, 1) is a 2-D column with 3 rows and 1 column. They broadcast differently and are not interchangeable.</p>")
FAQ("View vs copy?", "<p>A view shares data with the original array (slices, reshape, transpose), so changes show in both. A copy has its own data (masks, fancy indexing, <code>.copy()</code>).</p>")
FAQ("Why does <code>np.array([1, 2, 'a'])</code> become all strings?", "<p>An array has a single dtype; NumPy upcasts to a type that can represent every value, here a Unicode string.</p>")
FAQ("arange vs linspace?", "<p><code>arange(start, stop, step)</code> uses a step and excludes stop (like range). <code>linspace(start, stop, num)</code> uses a count and includes stop — better for floats.</p>")
FAQ("ravel vs flatten?", "<p>Both return a 1-D array. <code>ravel</code> returns a view when possible; <code>flatten</code> always returns a copy.</p>")
FAQ("What does axis=0 mean?", "<p>Operate down the rows (along the first axis), producing one result per column. axis=1 operates across the columns, one result per row.</p>")
