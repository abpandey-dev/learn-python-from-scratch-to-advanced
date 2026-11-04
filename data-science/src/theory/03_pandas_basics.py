from lib import *

THEORY("What pandas is", """
<p><b>pandas</b> is the standard Python library for working with <b>tabular</b> (spreadsheet- or SQL-like) and <b>time-series</b> data. It provides fast, labelled data structures built on NumPy arrays, plus tools to read, clean, transform, aggregate and reshape data.</p>
<p>The name comes from "panel data". Typical workflow: <b>load</b> (read_csv) → <b>inspect</b> (head, info, describe) → <b>clean</b> → <b>transform</b> → <b>aggregate</b> (groupby) → <b>visualise / export</b>.</p>
""")

THEORY("Core data structures", """
<table>
<tr><th></th><th>Series</th><th>DataFrame</th></tr>
<tr><td>Dimensions</td><td>1-D</td><td>2-D</td></tr>
<tr><td>Made of</td><td>values + index</td><td>columns (Series) sharing one row index</td></tr>
<tr><td>dtype</td><td>one</td><td>one per column</td></tr>
<tr><td>Like</td><td>a labelled array / a column</td><td>a spreadsheet / SQL table</td></tr>
</table>
<p>An <b>Index</b> is an immutable sequence of labels (default <code>RangeIndex</code> 0, 1, 2 …). Labels need not be unique, but unique indexes make lookups fast. <b>Alignment</b>: arithmetic between Series/DataFrames matches rows by label; unmatched labels become NaN.</p>
""")

THEORY("Data types", """
<table>
<tr><th>pandas dtype</th><th>Holds</th></tr>
<tr><td><code>int64</code>, <code>float64</code></td><td>numbers (NaN forces float)</td></tr>
<tr><td><code>Int64</code> (capital I)</td><td>nullable integers (can hold <code>pd.NA</code>)</td></tr>
<tr><td><code>bool</code> / <code>boolean</code></td><td>True/False</td></tr>
<tr><td><code>object</code> / <code>string</code> (<code>str</code> in pandas 3)</td><td>text</td></tr>
<tr><td><code>category</code></td><td>repeated labels stored as codes (saves memory)</td></tr>
<tr><td><code>datetime64[ns]</code>, <code>timedelta64</code></td><td>dates/times and durations</td></tr>
</table>
<p>Convert with <code>astype</code>, <code>pd.to_numeric</code>, <code>pd.to_datetime</code>.</p>
""")

THEORY("Selection and indexing", """
<table>
<tr><th>Accessor</th><th>Selects by</th><th>Slice end</th></tr>
<tr><td><code>df[col]</code>, <code>df[[cols]]</code></td><td>column name(s)</td><td>—</td></tr>
<tr><td><code>df[mask]</code></td><td>boolean Series (rows)</td><td>—</td></tr>
<tr><td><code>df.loc[rows, cols]</code></td><td>labels / boolean masks</td><td><b>inclusive</b></td></tr>
<tr><td><code>df.iloc[rows, cols]</code></td><td>integer positions</td><td>exclusive</td></tr>
<tr><td><code>df.at[r, c]</code>, <code>df.iat[i, j]</code></td><td>a single cell (fast)</td><td>—</td></tr>
</table>
<p><b>Chained assignment</b> like <code>df[df.a &gt; 0]["b"] = 1</code> may modify a temporary copy (SettingWithCopyWarning). Use one <code>.loc</code> call: <code>df.loc[df.a &gt; 0, "b"] = 1</code>. pandas 3 uses Copy-on-Write, so chained assignment never changes the original.</p>
""")

THEORY("I/O and inspection", """
<table>
<tr><th>Read</th><th>Write</th></tr>
<tr><td><code>pd.read_csv(path, sep=",", usecols=…, parse_dates=…)</code></td><td><code>df.to_csv(path, index=False)</code></td></tr>
<tr><td><code>pd.read_excel</code></td><td><code>df.to_excel</code></td></tr>
<tr><td><code>pd.read_json</code></td><td><code>df.to_json</code></td></tr>
<tr><td><code>pd.read_sql(query, conn)</code></td><td><code>df.to_sql</code></td></tr>
<tr><td><code>pd.read_parquet</code></td><td><code>df.to_parquet</code> (fast, typed, compressed)</td></tr>
</table>
<p>Inspect with <code>head, tail, sample, shape, info, dtypes, describe, columns, index, value_counts, nunique, isna().sum()</code>.</p>
""")

THEORY("Vectorised operations vs apply", """
<p>Column arithmetic, comparisons and the <code>.str</code> / <code>.dt</code> accessors run vectorised on whole columns. <code>apply</code>, <code>map</code> with a Python function and <code>iterrows</code> loop in Python and are much slower on large data. Order of preference: built-in vectorised method → <code>np.where</code> / <code>pd.cut</code> / <code>map</code> with a dict → <code>apply</code> → explicit loops.</p>
""")

FAQ("Series vs DataFrame?", "<p>A Series is a one-dimensional labelled array (one column). A DataFrame is a two-dimensional table of columns that share a row index; each column is a Series.</p>")
FAQ("loc vs iloc?", "<p><code>loc</code> selects by labels (and its slices include the end label). <code>iloc</code> selects by integer positions (slices exclude the end, like Python).</p>")
FAQ("Why use & instead of and in filters?", "<p><code>and</code> needs a single True/False, but a mask is a whole Series of booleans. <code>&amp;</code>, <code>|</code>, <code>~</code> combine masks element-wise. Wrap each condition in parentheses because of operator precedence.</p>")
FAQ("What is the index for?", "<p>It labels rows: fast lookups with <code>loc</code>, automatic alignment in arithmetic and joins, and meaningful row labels in results such as groupby output.</p>")
FAQ("What is SettingWithCopyWarning?", "<p>A warning that you may be assigning into a temporary copy (chained indexing), so the original DataFrame might not change. Use a single <code>.loc[row_mask, col] = value</code>.</p>")
FAQ("Why is apply slow?", "<p>It calls a Python function once per row or element, so it runs at Python-loop speed. Vectorised column operations run in compiled code.</p>")
