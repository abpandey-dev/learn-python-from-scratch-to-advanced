from lib import *
import duckdb

LESSON("Basics", "Why Polars and DuckDB?", """
<p>pandas is everywhere, but on bigger data it runs out of memory and uses one CPU core. Two newer tools fix that on a single machine, and many job posts now list them:</p>
<table>
<tr><th></th><th>pandas</th><th>Polars</th><th>DuckDB</th></tr>
<tr><td>Style</td><td>DataFrame methods</td><td>DataFrame <b>expressions</b></td><td><b>SQL</b></td></tr>
<tr><td>Engine</td><td>mostly single-threaded</td><td>multi-threaded, Rust</td><td>multi-threaded, columnar, C++</td></tr>
<tr><td>Lazy / optimised</td><td>no</td><td>yes (<code>lazy()</code>, <code>scan_*</code>)</td><td>yes, a query planner</td></tr>
<tr><td>Bigger than memory</td><td>no</td><td>streaming engine</td><td>spills to disk</td></tr>
<tr><td>Reads</td><td>CSV, Parquet…</td><td>CSV, Parquet, JSON, Delta</td><td>CSV, Parquet, JSON, S3, Postgres…</td></tr>
</table>
<p>They work together: DuckDB can query pandas or Polars frames by name, and both convert with <code>.to_pandas()</code>, <code>pl.from_pandas()</code> and Arrow without copying much.</p>
<p><b>Running the code:</b> DuckDB runs in this site's in-browser IDE. Polars doesn't run in the browser yet — use Colab (it's preinstalled there) or <code>pip install polars duckdb</code> locally. The IDE still checks plain-Python or pandas answers to every question.</p>
""", practice=["Filter and Add a Column", "Run SQL on a pandas DataFrame"])

LESSON("Core", "Polars expressions", """
<p>In Polars you describe <i>what</i> to compute with <b>expressions</b> — <code>pl.col("amount") * 1.18</code> — and hand them to <code>select</code>, <code>with_columns</code>, <code>filter</code> or <code>group_by().agg()</code>. Expressions in one call run in parallel, and there's no index to manage.</p>
<pre><code class="py">import polars as pl
orders = pl.read_csv("orders.csv")

(orders
 .filter(pl.col("status") == "completed")
 .with_columns(
     (pl.col("amount") * 1.18).round(2).alias("with_tax"),
     pl.when(pl.col("amount") &lt; 200).then(pl.lit("small"))
       .when(pl.col("amount") &lt; 1000).then(pl.lit("medium"))
       .otherwise(pl.lit("large")).alias("band"),
 )
 .group_by("city")
 .agg(pl.len().alias("orders"), pl.col("amount").sum().alias("revenue"), pl.col("amount").mean().round(1))
 .sort("revenue", descending=True))

# pandas equivalent of the group_by:
# df[df.status == "completed"].groupby("city").agg(orders=("id", "size"), revenue=("amount", "sum"))</code></pre>
<p><b>Lazy mode</b>: <code>pl.scan_csv(...)</code> or <code>df.lazy()</code> builds a query plan; Polars pushes filters and column selection down to the file reader and runs only on <code>.collect()</code>. <code>plan.explain()</code> shows the optimised plan.</p>
""", practice=["Bucket Values With when/then", "Group and Aggregate", "A Lazy Query", "Clean Strings and Extract Parts"])

LESSON("Core", "Reshaping and windows in Polars", """
<pre><code class="py"># window functions: compute per group, keep every row
df.with_columns(
    pl.col("amount").rank("dense", descending=True).over("city").alias("rank_in_city"),
    (pl.col("amount") / pl.col("amount").sum().over("city")).alias("share"),
    pl.col("temp").forward_fill().over("sensor"),
)
orders.join(customers, on="customer", how="left")       # also inner, full, semi, anti
customers.join(orders, on="customer", how="anti")        # customers with no orders
sales.pivot(on="city", index="month", values="revenue")  # long → wide; unpivot() goes back
daily.with_columns(pl.col("orders").rolling_mean(window_size=3))
posts.explode("tags")                                    # one row per list item
changes.sort("updated").unique("id", keep="last")        # latest version per id</code></pre>
""", practice=["Rank Within Groups", "Left Joins and Anti Joins", "Pivot Long to Wide", "A Rolling Average", "Fill Gaps Per Group", "Explode Lists Into Rows", "Keep the Latest Version of Each Row"])

LESSON("Core", "DuckDB: SQL on files and DataFrames", """
<p>DuckDB is an in-process analytical database — SQLite for analytics. There's no server: <code>import duckdb</code> and query CSV or Parquet files, folders of files, S3 paths, or DataFrames in memory.</p>
<pre><code class="py">import duckdb
duckdb.sql("SELECT city, SUM(amount) FROM 'orders/*.parquet' GROUP BY city").show()
duckdb.sql("SELECT * FROM orders_df WHERE amount &gt; 1000").pl()      # query a pandas frame, get Polars back

con = duckdb.connect("analytics.duckdb")                            # or a persistent file
con.execute("CREATE TABLE orders AS SELECT * FROM read_csv('orders.csv')")</code></pre>
<p>Its SQL has handy extras: <code>QUALIFY</code> (filter on window functions), <code>COUNT(*) FILTER (WHERE …)</code>, <code>ASOF JOIN</code> for time series, <code>list()</code> and <code>string_agg()</code>, <code>generate_series</code>, <code>PIVOT</code>, and <code>GROUP BY ALL</code>.</p>
""", practice=["SQL on Your Data With HAVING", "Running Totals and Month-Over-Month", "Top Row per Group With QUALIFY", "Conditional Counts With FILTER", "Match Each Trade to the Latest Quote", "Collect Values Into Lists", "Fill Missing Days With Zero"])


@LD
def duckdb_demo():
    con = duckdb.connect()
    con.execute("CREATE TABLE sales AS SELECT * FROM (VALUES ('Pune', 120.0), ('Delhi', 90.0), ('Pune', 150.0)) t(city, revenue)")
    print(con.execute("SELECT city, SUM(revenue) AS total FROM sales GROUP BY city ORDER BY total DESC").fetchall())
    print(con.execute("SELECT city, revenue FROM sales QUALIFY ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) = 1 ORDER BY city").fetchall())
