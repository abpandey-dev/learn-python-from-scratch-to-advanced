from lib import *

THEORY("Relational databases in one page", """
<ul>
<li>A <b>table</b> has rows (records) and typed columns. A <b>primary key</b> identifies each row; a <b>foreign key</b> points at a row in another table (orders.customer_id → customers.id).</li>
<li><b>Normalisation</b> stores each fact once (a customer's city lives in one place), and joins put the facts back together.</li>
<li><b>ACID</b>: transactions are Atomic (all or nothing), Consistent (constraints hold), Isolated (concurrent work doesn't interfere) and Durable (committed data survives crashes).</li>
<li><b>OLTP</b> databases (PostgreSQL, MySQL) handle many small reads and writes; <b>OLAP</b> warehouses (BigQuery, Snowflake, Redshift) scan huge tables for analytics.</li>
</ul>
""")

THEORY("Join types", """
<table>
<tr><th>Join</th><th>Keeps</th></tr>
<tr><td>INNER</td><td>only rows that match on both sides</td></tr>
<tr><td>LEFT</td><td>every left row; right columns NULL when unmatched</td></tr>
<tr><td>RIGHT / FULL OUTER</td><td>every right row / every row from both</td></tr>
<tr><td>CROSS</td><td>every combination (rows × rows)</td></tr>
<tr><td>Self join</td><td>a table joined to itself (employee → manager)</td></tr>
</table>
<p>If the join key isn't unique on both sides, rows multiply. Always check row counts before and after a join.</p>
""")

THEORY("NULL rules", """
<ul>
<li><code>NULL = NULL</code> is not true — use <code>IS NULL</code> / <code>IS NOT NULL</code>.</li>
<li><code>COUNT(*)</code> counts rows; <code>COUNT(col)</code> skips NULLs; <code>AVG</code>, <code>SUM</code> ignore NULLs.</li>
<li><code>COALESCE(col, 0)</code> replaces NULL with a default.</li>
<li><code>NOT IN (subquery)</code> returns nothing if the subquery contains a NULL; prefer <code>NOT EXISTS</code> or a LEFT JOIN.</li>
</ul>
""")

THEORY("SQL vs pandas", """
<table>
<tr><th>SQL</th><th>pandas</th></tr>
<tr><td><code>WHERE a &gt; 5</code></td><td><code>df[df.a &gt; 5]</code></td></tr>
<tr><td><code>GROUP BY k</code> + <code>SUM(v)</code></td><td><code>df.groupby("k")["v"].sum()</code></td></tr>
<tr><td><code>HAVING</code></td><td>filter after groupby</td></tr>
<tr><td><code>JOIN</code></td><td><code>merge</code></td></tr>
<tr><td><code>ORDER BY … LIMIT n</code></td><td><code>nlargest</code> / <code>sort_values().head(n)</code></td></tr>
<tr><td><code>ROW_NUMBER() OVER (PARTITION BY k ORDER BY v)</code></td><td><code>groupby("k")["v"].rank(method="first")</code></td></tr>
<tr><td><code>SUM(v) OVER (PARTITION BY k ORDER BY t)</code></td><td><code>groupby("k")["v"].cumsum()</code></td></tr>
</table>
""")

FAQ("WHERE vs HAVING?", "<p>WHERE filters rows before grouping; HAVING filters groups after aggregation, so it can use SUM, COUNT and so on.</p>")
FAQ("How do you prevent SQL injection?", "<p>Always pass values as parameters (<code>?</code> or <code>%s</code> placeholders), never with string formatting. Validate any identifiers (table or column names) against an allow-list.</p>")
FAQ("RANK vs DENSE_RANK vs ROW_NUMBER?", "<p>For values 10, 10, 8: ROW_NUMBER gives 1, 2, 3; RANK gives 1, 1, 3; DENSE_RANK gives 1, 1, 2.</p>")
FAQ("When should you add an index?", "<p>On columns used often in WHERE, JOIN and ORDER BY on large tables, especially when queries return a small share of rows. Not on tiny tables, or on columns that are written far more than read.</p>")
FAQ("Should you aggregate in SQL or in pandas?", "<p>Filter and aggregate in the database, so only the small result travels over the network and into memory. Use pandas for the last mile: reshaping, charts and modelling.</p>")
FAQ("What is a transaction?", "<p>A group of statements that either all take effect (commit) or none do (rollback), like debiting one account and crediting another.</p>")
