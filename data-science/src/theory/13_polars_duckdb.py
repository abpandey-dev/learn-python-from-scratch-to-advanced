from lib import *

THEORY("pandas → Polars → DuckDB, side by side", """
<table>
<tr><th>Task</th><th>pandas</th><th>Polars</th><th>DuckDB SQL</th></tr>
<tr><td>Filter</td><td><code>df[df.x &gt; 5]</code></td><td><code>df.filter(pl.col("x") &gt; 5)</code></td><td><code>WHERE x &gt; 5</code></td></tr>
<tr><td>New column</td><td><code>df.assign(y=df.x * 2)</code></td><td><code>with_columns((pl.col("x") * 2).alias("y"))</code></td><td><code>SELECT *, x * 2 AS y</code></td></tr>
<tr><td>Group</td><td><code>groupby("g").x.sum()</code></td><td><code>group_by("g").agg(pl.col("x").sum())</code></td><td><code>GROUP BY g</code></td></tr>
<tr><td>Window</td><td><code>groupby("g").x.transform("sum")</code></td><td><code>pl.col("x").sum().over("g")</code></td><td><code>SUM(x) OVER (PARTITION BY g)</code></td></tr>
<tr><td>Join</td><td><code>merge(b, on="k", how="left")</code></td><td><code>join(b, on="k", how="left")</code></td><td><code>LEFT JOIN b USING (k)</code></td></tr>
<tr><td>Lazy</td><td>—</td><td><code>scan_parquet(...).collect()</code></td><td>always planned</td></tr>
</table>
""")

FAQ("When would you choose Polars over pandas?", "<p>For larger data or heavy transformations where speed and memory matter: Polars is multi-threaded, lazy and doesn't copy as much. pandas still wins on ecosystem coverage and familiarity; many teams use both.</p>")
FAQ("What is DuckDB good for?", "<p>Fast analytical SQL on local files and DataFrames without running a database server — exploring Parquet on a laptop, transformations in pipelines, and as a dbt engine for small to medium data.</p>")
FAQ("What does lazy evaluation buy you?", "<p>The engine sees the whole query before running it, so it can push filters and column selection into the file reader, combine steps and skip work — reading only what's needed.</p>")
FAQ("Is DuckDB a replacement for Postgres?", "<p>No. Postgres is for many concurrent transactional reads and writes; DuckDB is an embedded engine for analytical queries in one process. They complement each other — DuckDB can even read Postgres tables.</p>")
FAQ("How do pandas, Polars and DuckDB share data?", "<p>Through Apache Arrow: <code>pl.from_pandas</code>, <code>.to_pandas()</code>, and DuckDB's <code>.df()</code>, <code>.pl()</code> and <code>.arrow()</code> results, usually without copying much.</p>")
FAQ("What is an ASOF join?", "<p>A join that matches each row to the most recent row at or before its time in another table — e.g. each trade to the latest price quote — instead of requiring equal timestamps.</p>")
