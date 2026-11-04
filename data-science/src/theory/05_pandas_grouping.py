from lib import *

THEORY("Split-apply-combine", """
<p>The <b>split-apply-combine</b> strategy (Hadley Wickham, 2011) underlies <code>groupby</code>: split the data into groups by key, apply a function independently to each group, and combine the results. It's the pandas equivalent of SQL's <code>GROUP BY</code>.</p>
<p><code>df.groupby(keys)</code> returns a lazy <b>GroupBy</b> object; nothing is computed until you call an aggregation, transformation or filter. Keys can be column names, lists of them, Series, functions of the index, or <code>pd.Grouper(freq="M")</code> for time.</p>
<p>Options: <code>as_index=False</code> keeps keys as columns, <code>sort=False</code> keeps first-seen order, <code>dropna=False</code> keeps a NaN group, <code>observed=True</code> for categoricals.</p>
""")

THEORY("Aggregation vs transformation vs filtration", """
<table>
<tr><th>Kind</th><th>Output shape</th><th>Examples</th></tr>
<tr><td><b>Aggregation</b></td><td>one value per group</td><td><code>sum mean median min max count size nunique std first last agg</code></td></tr>
<tr><td><b>Transformation</b></td><td>same index as input</td><td><code>transform("mean")</code>, <code>cumsum</code>, <code>rank</code>, <code>shift</code>, <code>fillna</code> within group</td></tr>
<tr><td><b>Filtration</b></td><td>subset of original rows</td><td><code>filter(lambda g: …)</code>, <code>head(n)</code>, <code>nth</code></td></tr>
</table>
<p><code>count</code> excludes NaN; <code>size</code> counts all rows.</p>
""")

THEORY("Joins", """
<table>
<tr><th>pandas</th><th>SQL</th><th>Rows kept</th></tr>
<tr><td><code>merge(how="inner")</code></td><td>INNER JOIN</td><td>matching keys only</td></tr>
<tr><td><code>merge(how="left")</code></td><td>LEFT JOIN</td><td>all left rows</td></tr>
<tr><td><code>merge(how="right")</code></td><td>RIGHT JOIN</td><td>all right rows</td></tr>
<tr><td><code>merge(how="outer")</code></td><td>FULL OUTER JOIN</td><td>all keys</td></tr>
<tr><td><code>merge(how="cross")</code></td><td>CROSS JOIN</td><td>every pair</td></tr>
</table>
<p>Cardinality: one-to-one, one-to-many, many-to-many. Many-to-many multiplies rows. <code>validate="one_to_many"</code> makes pandas check the relationship; <code>indicator=True</code> adds a column saying where each row came from (useful for anti-joins). <code>join</code> merges on the index; <code>concat</code> stacks along an axis without matching keys.</p>
""")

THEORY("Tidy data and reshaping", """
<p><b>Tidy data</b>: each variable is a column, each observation is a row, each type of observational unit is a table. Long/tidy format is easiest to filter, group and plot.</p>
<table>
<tr><th>Function</th><th>Direction</th><th>Notes</th></tr>
<tr><td><code>pivot</code></td><td>long → wide</td><td>no aggregation; fails on duplicate pairs</td></tr>
<tr><td><code>pivot_table</code></td><td>long → wide</td><td>aggregates duplicates (aggfunc), margins=True adds totals</td></tr>
<tr><td><code>melt</code></td><td>wide → long</td><td>id_vars stay, other columns become variable/value</td></tr>
<tr><td><code>stack / unstack</code></td><td>columns ↔ index levels</td><td>work with MultiIndex</td></tr>
<tr><td><code>crosstab</code></td><td>frequency table</td><td>normalize= for proportions</td></tr>
</table>
""")

THEORY("MultiIndex", """
<p>Grouping by several keys produces a <b>MultiIndex</b> — a hierarchical index with several levels (region, product). Access with tuples <code>s.loc[("North", "pen")]</code> or <code>xs</code>; flatten with <code>reset_index()</code>; move a level to columns with <code>unstack()</code>.</p>
""")

THEORY("Windows and time series", """
<table>
<tr><th>Tool</th><th>Meaning</th></tr>
<tr><td><code>rolling(n)</code></td><td>fixed-size moving window (last n rows or a time span like "7D")</td></tr>
<tr><td><code>expanding()</code></td><td>everything up to the current row (running statistics)</td></tr>
<tr><td><code>ewm(span=n)</code></td><td>exponentially weighted (recent rows count more)</td></tr>
<tr><td><code>resample("ME")</code></td><td>group a DatetimeIndex by calendar period</td></tr>
<tr><td><code>shift(k)</code>, <code>diff()</code>, <code>pct_change()</code></td><td>lags, differences, growth rates</td></tr>
</table>
""")

FAQ("What does groupby return?", "<p>A GroupBy object — a lazy description of the groups. Calling an aggregation (sum, mean, agg), transformation (transform, cumsum) or filter on it produces the result.</p>")
FAQ("agg vs transform?", "<p>agg reduces each group to one row; transform returns a result for every original row (aligned to the original index), so it can be assigned as a new column.</p>")
FAQ("count vs size?", "<p>size counts all rows per group; count counts non-missing values per column.</p>")
FAQ("merge vs join vs concat?", "<p>merge matches rows on key columns (SQL-style); join is a convenience for merging on the index; concat stacks objects along an axis without matching keys.</p>")
FAQ("pivot vs pivot_table?", "<p>pivot only reshapes and fails if an index/column pair occurs twice; pivot_table aggregates duplicates with aggfunc and can fill missing cells.</p>")
FAQ("What is an anti-join and how do you do it in pandas?", "<p>Rows in one table with no match in another. Use <code>~a['key'].isin(b['key'])</code>, or a left merge with <code>indicator=True</code> and keep <code>_merge == 'left_only'</code>.</p>")
FAQ("Why do I get more rows after a merge?", "<p>Duplicate keys on both sides create every combination (many-to-many). Deduplicate first or pass <code>validate=</code> to catch it.</p>")
