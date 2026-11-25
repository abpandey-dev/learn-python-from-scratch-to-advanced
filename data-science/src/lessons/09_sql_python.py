from lib import *
import sqlite3
import pandas as pd

LESSON("Basics", "Why analysts need SQL as well as pandas", """
<p>Company data lives in <b>databases</b>, not CSV files. pandas works on what fits in your laptop's memory; a database holds billions of rows and lets many people query them at once. The everyday workflow is: <b>use SQL to filter and aggregate inside the database, then pull the small result into pandas</b> for charts and modelling.</p>
<p>Python's built-in <code>sqlite3</code> module gives you a real SQL database in one file (or in memory) with nothing to install, so it's perfect for learning. The same SQL runs, with small dialect changes, on PostgreSQL, MySQL, BigQuery or Snowflake — you'd just connect with a different driver (<code>psycopg</code>, <code>sqlalchemy</code>).</p>
<pre><code class="py">con = sqlite3.connect(":memory:")       # or a file: sqlite3.connect("shop.db")
con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, day TEXT)")
con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", rows)
con.commit()
con.execute("SELECT COUNT(*) FROM orders").fetchone()   # (6,)</code></pre>
<p>Want to practise pure SQL with automatic checking? The <a href="https://abpandey-dev.github.io/data-engineering-from-scratch-to-advanced/ide/sql.html">SQL IDE</a> in the Data Engineering course has 43 checked questions.</p>
""", practice=["Load Rows and Count Them"])


@LD
def first_query():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE orders (id INTEGER, city TEXT, amount REAL)")
    con.executemany("INSERT INTO orders VALUES (?, ?, ?)",
                    [(1, "Pune", 250.0), (2, "Delhi", 120.0), (3, "Pune", 90.0)])
    rows = con.execute("SELECT city, SUM(amount) FROM orders GROUP BY city ORDER BY city").fetchall()
    df = pd.read_sql_query("SELECT * FROM orders WHERE amount > ?", con, params=(100,))


LESSON("Basics", "Parameters, and why f-strings are dangerous", """
<p>Never build SQL by pasting user input into the text:</p>
<pre><code class="py">name = "x' OR '1'='1"
con.execute(f"SELECT * FROM users WHERE name = '{name}'")      # returns EVERY user — SQL injection
con.execute("SELECT * FROM users WHERE name = ?", (name,))     # safe: the value is sent as data</code></pre>
<p>With <code>?</code> placeholders the driver sends the query and the values separately, so quotes inside a value can never change the query. Parameters are also faster when the same query runs many times. (Table and column names can't be parameters — check them against an allow-list.)</p>
""", practice=["Orders Above an Amount", "Safe Lookup by Name"])

LESSON("Core", "Joins and aggregation", """
<table>
<tr><th>Clause</th><th>Does</th><th>pandas equivalent</th></tr>
<tr><td><code>JOIN … ON</code></td><td>rows that match in both tables</td><td><code>merge(how="inner")</code></td></tr>
<tr><td><code>LEFT JOIN</code></td><td>every left row; NULLs where nothing matches</td><td><code>merge(how="left")</code></td></tr>
<tr><td><code>GROUP BY</code></td><td>one row per group</td><td><code>groupby</code></td></tr>
<tr><td><code>HAVING</code></td><td>filter groups after aggregating</td><td>filter the grouped result</td></tr>
<tr><td><code>CASE WHEN</code></td><td>if / else inside a query</td><td><code>np.select</code>, <code>pd.cut</code></td></tr>
</table>
<p>The query runs in this order: <b>FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT</b>. That's why WHERE can't use a SUM (it doesn't exist yet) but HAVING can. To find "rows with no match", LEFT JOIN and keep rows where the right side <code>IS NULL</code>.</p>
""", practice=["Revenue per City", "Customers With No Orders", "Big Spenders", "Bucket Orders by Size", "Days With Several Customers"])

LESSON("Core", "Subqueries and window functions", """
<p>A <b>subquery</b> is a query inside a query: <code>WHERE amount &gt; (SELECT AVG(amount) FROM orders)</code>.</p>
<p>A <b>window function</b> computes across related rows but, unlike GROUP BY, keeps every row:</p>
<pre><code class="sql">ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC)   -- 1, 2, 3 within each customer
SUM(amount)  OVER (PARTITION BY customer_id ORDER BY day)           -- running total
LAG(amount)  OVER (ORDER BY day)                                   -- previous row's value
RANK() / DENSE_RANK()                                              -- ties share a rank</code></pre>
<p>"Top N per group", "latest record per user", running totals and day-over-day change are all window-function questions — the most common SQL interview topic.</p>
""", practice=["Orders Above Average", "Biggest Order per Customer", "Running Total per Customer", "Second-Highest Order Amount", "Keep the Latest Version of Each Record"])

LESSON("Core", "Dates and pivots in SQL", """
<p>SQLite stores dates as ISO text (<code>'2026-02-14'</code>), which sorts correctly. <code>strftime('%Y-%m', day)</code> gives the month, <code>date(day, '+7 days')</code> shifts it, <code>julianday(b) - julianday(a)</code> gives days between. Other databases use <code>DATE_TRUNC('month', day)</code> or <code>EXTRACT</code>.</p>
<p>To turn months into columns (a pivot), use <b>conditional aggregation</b>:</p>
<pre><code class="sql">SELECT city,
       SUM(CASE WHEN strftime('%m', day) = '01' THEN amount ELSE 0 END) AS jan,
       SUM(CASE WHEN strftime('%m', day) = '02' THEN amount ELSE 0 END) AS feb
FROM orders JOIN customers ON … GROUP BY city</code></pre>
""", practice=["Monthly Revenue", "Pivot Months into Columns"])

LESSON("Advanced", "SQL ↔ pandas, upserts, transactions and indexes", """
<pre><code class="py">df = pd.read_sql_query("SELECT ...", con, params=(...))   # SQL → DataFrame
df.to_sql("sales", con, index=False, if_exists="append")    # DataFrame → table</code></pre>
<ul>
<li><b>Upsert</b>: insert, or update if the key already exists — <code>INSERT … ON CONFLICT(key) DO UPDATE SET …</code> (MERGE in other databases). It makes loads safe to re-run.</li>
<li><b>Transactions</b>: several statements that succeed or fail together. <code>with con:</code> commits at the end, or rolls back if an error is raised. Constraints like <code>CHECK (balance &gt;= 0)</code> make the database refuse bad data.</li>
<li><b>Indexes</b>: a sorted lookup structure on a column, like the index at the back of a book. <code>WHERE customer_id = 1</code> becomes a fast search instead of reading every row. <code>EXPLAIN QUERY PLAN</code> shows which one happens. Indexes slow down writes a little and use space, so add them for columns you filter and join on.</li>
</ul>
""", practice=["Query Straight into a DataFrame", "From a DataFrame to a Table and Back", "Upsert Stock Levels", "All-or-Nothing Transfers", "Does the Query Use the Index?"])
