from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import sqlite3

DEMO_SCHEMA = """
CREATE TABLE employees (name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES ('Asha','Eng',150), ('Ben','Eng',120), ('Chen','Eng',120), ('Dara','Eng',90), ('Eli','Sales',100), ('Fay','Sales',70);
"""


def run(query):
    con = sqlite3.connect(":memory:")
    con.executescript(DEMO_SCHEMA)
    return con.execute(query).fetchall()


LESSON("Basics", "How to read a query: the order SQL really runs in", """
<p>SQL is written in one order and runs in another. Most beginner confusion comes from here:</p>
<table><tr><th>Step</th><th>Clause</th><th>What it does</th></tr>
<tr><td>1</td><td>FROM / JOIN</td><td>gather the rows</td></tr>
<tr><td>2</td><td>WHERE</td><td>keep rows</td></tr>
<tr><td>3</td><td>GROUP BY</td><td>make piles</td></tr>
<tr><td>4</td><td>HAVING</td><td>keep piles</td></tr>
<tr><td>5</td><td>SELECT</td><td>choose and compute columns</td></tr>
<tr><td>6</td><td>ORDER BY</td><td>sort</td></tr>
<tr><td>7</td><td>LIMIT</td><td>cut off</td></tr></table>
<p>This explains two classic errors. You can't use <code>WHERE COUNT(*) &gt; 2</code>, because counts don't exist yet at step 2, so that's what HAVING is for. And in standard SQL, a column alias from SELECT isn't visible in WHERE, because SELECT happens later.</p>
<p><b>Worked example.</b> "Departments with at least 2 people, and an average salary above 80":</p>
<pre><code class="py">SELECT dept_id, AVG(salary)
FROM employees
WHERE dept_id IS NOT NULL      -- step 2: drop Ivan, who has no department
GROUP BY dept_id               -- step 3: piles for 1, 2, 3
HAVING COUNT(*) >= 2 AND AVG(salary) > 80;   -- step 4: pile 3 has only Hana, so it goes</code></pre>
<p>Pile 1 is 150, 120, 120, 90, with an average of 120. Pile 2 is 100, 70, 80, with an average of 83.33. Both survive.</p>
<p><b>In the interview,</b> say the steps as you write. Interviewers want to see how you think, and a wrong column name won't sink you if your logic is clear.</p>
""", practice=["Filter and Sort", "Count per Group", "Groups Above a Limit", "COUNT and NULL"])


LESSON("Basics", "Joins, and how they multiply rows", """
<p>A join matches rows from two tables. Picture two lists side by side, with lines drawn between matches.</p>
<table><tr><th>Join</th><th>Keeps</th><th>Unmatched columns</th></tr>
<tr><td>INNER</td><td>only rows that match</td><td>none are kept</td></tr>
<tr><td>LEFT</td><td>all left rows</td><td>right side becomes NULL</td></tr>
<tr><td>RIGHT</td><td>all right rows</td><td>left side becomes NULL</td></tr>
<tr><td>FULL</td><td>all rows from both</td><td>NULL on the missing side</td></tr>
<tr><td>CROSS</td><td>every combination</td><td>n × m rows</td></tr></table>
<p><b>Two important questions interviewers like:</b></p>
<p><b>1. Join two tables of 3 rows each. How many rows can result?</b> Anything from 0 to 9. If the key is duplicated, every match pairs up: a key appearing 2 times on the left and 3 on the right makes 6 rows. This is the classic cause of an inflated total, where revenue suddenly doubles after a join.</p>
<p><b>2. A filter on a LEFT JOIN's right table.</b> <code>WHERE o.amount &gt; 0</code> throws away the NULL rows, so your LEFT JOIN quietly becomes an INNER JOIN. To keep unmatched rows, put the condition in <code>ON</code> instead.</p>
<p><b>Finding what's missing</b> is a very common question. LEFT JOIN, then keep rows where the right side is NULL. In our data, the Legal department has no employees, and customer Dev has no orders.</p>
<p><b>NOT IN has a trap:</b> <code>x NOT IN (1, NULL)</code> is never true, because comparing with NULL gives "unknown". One NULL in the subquery and you get no rows at all.</p>
<p><b>Self join:</b> a table joined to itself, using two aliases, such as employee and manager. In our data, Fay earns 70 and her manager Hana earns 60, so Fay out-earns her manager.</p>
""", practice=["Inner Join", "Rows With No Match", "Employee and Their Manager"])


LESSON("Core", "Subqueries and the second-highest salary", """
<p>Probably the most-asked SQL question. Salaries are 150, 120, 120, 100, 90, 80, 70, 60, 50.</p>
<p><b>Method 1, MAX below MAX:</b></p>
<pre><code class="py">SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);</code></pre>
<p>The inner query gives 150, and the outer gives the highest below it: <b>120</b>. It's easy to understand, but it doesn't extend to the 5th highest.</p>
<p><b>Method 2, OFFSET:</b></p>
<pre><code class="py">SELECT DISTINCT salary FROM employees
ORDER BY salary DESC LIMIT 1 OFFSET 1;</code></pre>
<p>DISTINCT matters here. Without it, the second row is the other 120 by luck, and the third highest would wrongly also be 120.</p>
<p><b>Method 3, DENSE_RANK,</b> which is best for "Nth per group": next lesson.</p>
<p><b>Follow-ups to expect:</b></p>
<ul><li><i>What if there's no second salary?</i> Method 1 returns NULL. Method 2 returns no rows, so wrap it in a subquery if you need a NULL.</li>
<li><i>Ties?</i> Ask whether "second highest" means distinct values. This kind of clarifying question scores points.</li></ul>
<p><b>Duplicates.</b> Finding them is GROUP BY plus HAVING COUNT(*) &gt; 1. To keep one of each, use ROW_NUMBER, again next.</p>
""", practice=["Second Highest Salary", "Find Duplicates"])


LESSON("Core", "Window functions: the interview favourite", """
<p>GROUP BY squashes each group into one row. A <b>window function</b> computes across related rows, but <b>keeps every row</b>.</p>
<pre><code class="py">function() OVER (PARTITION BY group_column ORDER BY sort_column)</code></pre>
<p><b>The three rankings differ only on ties.</b> Salaries 150, 120, 120, 90:</p>
<table><tr><th>Name</th><th>Salary</th><th>ROW_NUMBER</th><th>RANK</th><th>DENSE_RANK</th></tr>
<tr><td>Asha</td><td>150</td><td>1</td><td>1</td><td>1</td></tr>
<tr><td>Ben</td><td>120</td><td>2</td><td>2</td><td>2</td></tr>
<tr><td>Chen</td><td>120</td><td>3</td><td>2</td><td>2</td></tr>
<tr><td>Dara</td><td>90</td><td>4</td><td><b>4</b></td><td><b>3</b></td></tr></table>
<ul><li><b>ROW_NUMBER:</b> always unique, so use it to keep exactly one row per group.</li>
<li><b>RANK:</b> leaves a gap after a tie.</li>
<li><b>DENSE_RANK:</b> no gap, so use it for "top 2 distinct salaries".</li></ul>
<p><b>You can't filter a window function in WHERE</b>, because it's computed after WHERE. Wrap it in a CTE:</p>
<pre><code class="py">WITH r AS (
  SELECT name, dept, salary,
         DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
  FROM employees)
SELECT * FROM r WHERE dr <= 2;</code></pre>
<p><b>Others to know:</b></p>
<ul><li><code>SUM(x) OVER (ORDER BY d)</code>: a running total. For 100, 50, 200: 100, 150, 350.</li>
<li><code>LAG(x)</code>, <code>LEAD(x)</code>: the previous or next row. For monthly revenue 350, 100, 160, change is NULL, −250, +60.</li>
<li><code>AVG(x) OVER (PARTITION BY g)</code>: each row next to its group's average.</li>
<li><code>SUM(SUM(x)) OVER ()</code>: the grand total, inside a GROUP BY, for percentage of total.</li></ul>
<p><b>A trap the demo reveals:</b> Ben and Chen both show a running total of 390, not 270 and 390. With ties in ORDER BY, the default window treats equal rows as one group. To add row by row, order by something unique, or write <code>ROWS UNBOUNDED PRECEDING</code>.</p>
<p>Run the demo, then change PARTITION BY to see the ranks restart per department.</p>
""", practice=["Keep the First of Each Duplicate", "Above the Department Average", "Rank Salaries", "Top Earner per Department", "Top 2 Distinct Salaries per Department", "Running Total", "Month-Over-Month Change", "Share of Total"])


@LD
def window_demo():
    rows = run("""
        SELECT dept, name, salary,
          ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS row_num,
          DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dense,
          SUM(salary) OVER (PARTITION BY dept ORDER BY salary DESC) AS running
        FROM employees ORDER BY dept, salary DESC""")
    for row in rows:
        print(row)


LESSON("Advanced", "Hard patterns: gaps, islands, pivots and hierarchies", """
<p><b>Gaps and islands: find a streak.</b> The trick looks like magic until you see it. User 1 logged in on days 1, 2, 3 and 5. Subtract each row's position:</p>
<table><tr><th>Day</th><th>ROW_NUMBER</th><th>Day − row</th></tr>
<tr><td>1</td><td>1</td><td><b>0</b></td></tr><tr><td>2</td><td>2</td><td><b>0</b></td></tr><tr><td>3</td><td>3</td><td><b>0</b></td></tr><tr><td>5</td><td>4</td><td><b>1</b></td></tr></table>
<p>Within a streak, day and row number rise together, so their difference stays constant. Group by that difference and count: streaks of 3 and 1, so the longest is <b>3</b>.</p>
<p><b>Pivot with CASE.</b> Turn rows into columns, using conditional aggregation:</p>
<pre><code class="py">SELECT customer_id,
  SUM(CASE WHEN month = 'Jan' THEN amount ELSE 0 END) AS jan,
  SUM(CASE WHEN month = 'Feb' THEN amount ELSE 0 END) AS feb
FROM orders GROUP BY customer_id;</code></pre>
<p><b>Recursive CTE: walk a hierarchy.</b> It has two parts: a starting row, and a step joining back to itself, which repeats until no new rows appear.</p>
<pre><code class="py">WITH RECURSIVE tree(id, name, depth) AS (
    SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, t.depth + 1
    FROM employees e JOIN tree t ON e.manager_id = t.id)
SELECT * FROM tree;</code></pre>
<p>Round 1 finds Asha at depth 0. Round 2 finds those reporting to her at depth 1. Round 3 finds their reports at depth 2. Then it stops.</p>
""", practice=["Consecutive Login Streaks", "Pivot With CASE", "Walk the Org Chart"])


LESSON("Advanced", "Indexes, performance and design", """
<p>Senior interviews go beyond writing queries.</p>
<p><b>An index</b> is like the index at the back of a book. Usually it's a B-tree, which turns an O(n) scan into O(log n). With a billion rows, that's about 30 steps instead of a billion. The costs are extra storage and slower writes, because each index must be updated.</p>
<p><b>A composite index on (a, b)</b> helps queries on a, or on a and b, but generally not on b alone. Think of a phone book sorted by surname, then first name: you can't quickly find everyone called "Sam".</p>
<p><b>Things that stop an index being used:</b> a function on the column (<code>WHERE YEAR(d) = 2024</code>), a leading wildcard (<code>LIKE '%x'</code>), and low-selectivity columns.</p>
<p><b>How to diagnose a slow query:</b> read the plan with <code>EXPLAIN</code>, look for full scans on big tables, add suitable indexes, and filter early.</p>
<table><tr><th>Term</th><th>Meaning</th></tr>
<tr><td>Normalisation</td><td>each fact stored once, avoiding update errors</td></tr>
<tr><td>Denormalisation</td><td>deliberate duplication, for faster reads</td></tr>
<tr><td>ACID</td><td>atomic, consistent, isolated, durable transactions</td></tr>
<tr><td>Primary key</td><td>uniquely identifies a row</td></tr>
<tr><td>Foreign key</td><td>a reference to a row in another table</td></tr></table>
<p><b>Dialects differ.</b> Practice here uses SQLite. Window functions and CTEs are broadly the same elsewhere, but date functions and <code>LIMIT</code> vary. For example, SQL Server uses <code>TOP</code>. Ask which database the interviewer has in mind.</p>
""", practice=[])
