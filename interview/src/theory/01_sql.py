from lib import *

THEORY("Picking the tool", """
<table><tr><th>Question sounds like</th><th>Reach for</th></tr>
<tr><td>"for each group, one total"</td><td>GROUP BY</td></tr>
<tr><td>"groups where…"</td><td>HAVING</td></tr>
<tr><td>"has no…", "never…"</td><td>LEFT JOIN … IS NULL</td></tr>
<tr><td>"top N per…"</td><td>ROW_NUMBER, RANK or DENSE_RANK in a CTE</td></tr>
<tr><td>"running…", "cumulative…"</td><td>SUM() OVER</td></tr>
<tr><td>"compared with the previous…"</td><td>LAG</td></tr>
<tr><td>"consecutive…"</td><td>value − ROW_NUMBER</td></tr>
<tr><td>"percent of total"</td><td>SUM(x) OVER ()</td></tr>
<tr><td>"reports to", "tree"</td><td>recursive CTE</td></tr></table>
""")
THEORY("NULL rules", """
<ul><li><code>x = NULL</code> is never true: use <code>IS NULL</code>.</li>
<li><code>COUNT(*)</code> counts rows, <code>COUNT(col)</code> skips NULLs.</li>
<li>SUM and AVG ignore NULLs, so AVG divides by non-NULL rows only.</li>
<li><code>COALESCE(x, 0)</code> gives a default.</li>
<li><code>NOT IN</code> with a NULL in the list returns nothing.</li></ul>
""")
FAQ("WHERE vs HAVING?", "<p>WHERE filters rows before grouping. HAVING filters groups after grouping, so it can use aggregates.</p>")
FAQ("INNER vs LEFT JOIN?", "<p>INNER keeps only matches. LEFT keeps every left row, with NULLs where there's no match.</p>")
FAQ("RANK vs DENSE_RANK vs ROW_NUMBER?", "<p>On ties, ROW_NUMBER still gives different numbers, RANK gives the same number then leaves a gap, and DENSE_RANK gives the same number with no gap.</p>")
FAQ("UNION vs UNION ALL?", "<p>UNION removes duplicates, which needs extra work. UNION ALL keeps everything and is faster, so use it when duplicates can't occur or are fine.</p>")
FAQ("DELETE vs TRUNCATE vs DROP?", "<p>DELETE removes chosen rows and can be filtered. TRUNCATE quickly removes all rows and keeps the table. DROP removes the table itself. Exact behaviour around rollback differs by database.</p>")
FAQ("What is a CTE, and why use one?", "<p>A named temporary result introduced by WITH. It makes complex queries readable, can be recursive, and lets you filter on window functions.</p>")
FAQ("Correlated subquery?", "<p>A subquery that refers to the outer row, so it conceptually runs once per row. It can often be rewritten as a join or window function for better performance.</p>")
FAQ("What is an index? What's the downside?", "<p>A sorted structure, often a B-tree, that speeds up lookups from O(n) to O(log n). It costs storage and slows writes.</p>")
FAQ("Clustered vs non-clustered index?", "<p>A clustered index determines how rows are stored, so there's one per table. A non-clustered index is a separate structure that points to rows.</p>")
FAQ("What does ACID mean?", "<p>Atomicity (all or nothing), consistency (rules hold), isolation (transactions don't interfere), durability (committed data survives failure).</p>")
FAQ("What is normalisation?", "<p>Organising tables so each fact lives in one place, which avoids update anomalies. Analytics systems often denormalise to make reads faster.</p>")
FAQ("How would you speed up a slow query?", "<p>Read the plan with EXPLAIN. Look for full scans and big joins. Add suitable indexes, filter early, select only needed columns, and avoid functions on indexed columns.</p>")
