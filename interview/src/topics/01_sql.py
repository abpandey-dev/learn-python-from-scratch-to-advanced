from lib import *
import sqlite3


TOPIC(
    id="sql", title="SQL for Interviews", glyph="SELECT",
    blurb="The SQL that interviews ask: joins, GROUP BY and HAVING, subqueries, CTEs and window functions, including second-highest salary, top N per group, running totals and finding gaps.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">SELECT dept, COUNT(*) AS n        -- written in this order...
FROM employees e
JOIN departments d ON ...
WHERE salary > 50000              -- filters rows, before grouping
GROUP BY dept
HAVING COUNT(*) > 2               -- filters groups, after grouping
ORDER BY n DESC
LIMIT 5;
RANK() OVER (PARTITION BY dept ORDER BY salary DESC)</code></pre>
<p>Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.</p>
<p>Every question here runs on a real in-memory SQLite database through <code>run_sql</code>.</p>
""")

SCHEMA = """
CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO departments VALUES (1, 'Eng'), (2, 'Sales'), (3, 'HR'), (4, 'Legal');

CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, manager_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1, 'Asha', 1, NULL, 150), (2, 'Ben', 1, 1, 120), (3, 'Chen', 1, 1, 120), (4, 'Dara', 1, 2, 90),
 (5, 'Eli', 2, 1, 100), (6, 'Fay', 2, 8, 70), (7, 'Gus', 2, 5, 80), (8, 'Hana', 3, 1, 60), (9, 'Ivan', NULL, 1, 50);

CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
INSERT INTO customers VALUES (1, 'Ann', 'Pune'), (2, 'Bob', 'Delhi'), (3, 'Cid', 'Pune'), (4, 'Dev', 'Goa');

CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, order_date TEXT);
INSERT INTO orders VALUES
 (1, 1, 100, '2024-01-05'), (2, 1, 50, '2024-01-20'), (3, 2, 200, '2024-01-25'), (4, 1, 70, '2024-02-02'),
 (5, 3, 30, '2024-02-10'), (6, 2, 80, '2024-03-01'), (7, 2, 80, '2024-03-02');

CREATE TABLE logins (user_id INTEGER, day INTEGER);
INSERT INTO logins VALUES (1, 1), (1, 2), (1, 3), (1, 5), (2, 2), (2, 3), (3, 7);

CREATE TABLE emails (id INTEGER, email TEXT);
INSERT INTO emails VALUES (1, 'a@x.com'), (2, 'b@x.com'), (3, 'a@x.com'), (4, 'c@x.com'), (5, 'b@x.com');
"""


def run_sql(query):
    """Run a query on a fresh database and return the rows as lists."""
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    rows = con.execute(query).fetchall()
    con.close()
    return [list(r) for r in rows]


Q(None, "Filter and Sort", "Easy", "WHERE, ORDER BY",
  "Return name and salary of employees earning more than 90, highest first, then by name.",
  [((), [['Asha', 150], ['Ben', 120], ['Chen', 120], ['Eli', 100]])],
  ("Select everything, then filter and sort in Python. Works, but it ignores what the database is for.", "O(n log n)", "O(n)"),
  ("<code>WHERE</code> and <code>ORDER BY</code> let the database do it.", "O(n log n)", "O(n)"))


@B
def high_earners():
    rows = run_sql("SELECT name, salary FROM employees")
    kept = [r for r in rows if r[1] > 90]
    return sorted(kept, key=lambda r: (-r[1], r[0]))


@O
def high_earners():
    return run_sql("""
        SELECT name, salary FROM employees
        WHERE salary > 90
        ORDER BY salary DESC, name""")


Q(None, "Count per Group", "Easy", "GROUP BY",
  "Return each dept_id and its employee count, ignoring employees with no department, ordered by dept_id.",
  [((), [[1, 4], [2, 3], [3, 1]])],
  ("A correlated subquery for each department.", "O(d·n)", "O(d)"),
  ("<code>GROUP BY</code>.", "O(n)", "O(d)"))


@B
def dept_counts():
    return run_sql("""
        SELECT id, (SELECT COUNT(*) FROM employees e WHERE e.dept_id = d.id) AS n
        FROM departments d
        WHERE n > 0
        ORDER BY id""")


@O
def dept_counts():
    return run_sql("""
        SELECT dept_id, COUNT(*) FROM employees
        WHERE dept_id IS NOT NULL
        GROUP BY dept_id
        ORDER BY dept_id""")


Q(None, "Groups Above a Limit", "Easy", "HAVING",
  "Return dept_id and average salary for departments with at least 2 employees and an average over 80, ordered by dept_id.",
  [((), [[1, 120.0], [2, 83.3333]])],
  ("Group in a subquery, then filter outside with WHERE.", "O(n)", "O(d)"),
  ("<code>HAVING</code> filters groups directly.", "O(n)", "O(d)"))


@B
def big_departments():
    return run_sql("""
        SELECT dept_id, avg_s FROM (
            SELECT dept_id, AVG(salary) AS avg_s, COUNT(*) AS n
            FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id)
        WHERE n >= 2 AND avg_s > 80
        ORDER BY dept_id""")


@O
def big_departments():
    return run_sql("""
        SELECT dept_id, AVG(salary) FROM employees
        WHERE dept_id IS NOT NULL
        GROUP BY dept_id
        HAVING COUNT(*) >= 2 AND AVG(salary) > 80
        ORDER BY dept_id""")


Q(None, "Inner Join", "Easy", "JOIN",
  "Return each employee's name and department name. Employees without a department are left out. Order by employee id.",
  [((), [['Asha', 'Eng'], ['Ben', 'Eng'], ['Chen', 'Eng'], ['Dara', 'Eng'], ['Eli', 'Sales'], ['Fay', 'Sales'], ['Gus', 'Sales'], ['Hana', 'HR']])],
  ("A subquery in SELECT, then drop the missing ones.", "O(n·d)", "O(n)"),
  ("<code>JOIN ... ON</code>.", "O(n)", "O(n)"))


@B
def with_department():
    return run_sql("""
        SELECT name, dept FROM (
            SELECT id, name, (SELECT d.name FROM departments d WHERE d.id = e.dept_id) AS dept
            FROM employees e)
        WHERE dept IS NOT NULL
        ORDER BY id""")


@O
def with_department():
    return run_sql("""
        SELECT e.name, d.name FROM employees e
        JOIN departments d ON e.dept_id = d.id
        ORDER BY e.id""")


Q(None, "Rows With No Match", "Easy", "LEFT JOIN ... IS NULL",
  "Return names of departments with no employees, and names of customers with no orders, as two lists in a tuple.",
  [((), (['Legal'], ['Dev']))],
  ("<code>NOT IN</code> with a subquery. Beware: NOT IN returns nothing if the subquery contains a NULL.", "O(n·m)", "O(n)"),
  ("<code>LEFT JOIN</code>, keeping rows where the right side is NULL. It handles NULLs safely.", "O(n + m)", "O(n)"))


@B
def no_match():
    depts = run_sql("""SELECT name FROM departments
                       WHERE id NOT IN (SELECT dept_id FROM employees WHERE dept_id IS NOT NULL)""")
    custs = run_sql("SELECT name FROM customers WHERE id NOT IN (SELECT customer_id FROM orders)")
    return ([r[0] for r in depts], [r[0] for r in custs])


@O
def no_match():
    depts = run_sql("""SELECT d.name FROM departments d
                       LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL""")
    custs = run_sql("""SELECT c.name FROM customers c
                       LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL""")
    return ([r[0] for r in depts], [r[0] for r in custs])


Q(None, "Employee and Their Manager", "Medium", "Self join",
  "Return names of employees who earn more than their manager, ordered by name.",
  [((), [['Fay']])],
  ("A correlated subquery looking up the manager's salary per row.", "O(n²)", "O(n)"),
  ("Join the table to itself, with two aliases.", "O(n)", "O(n)"))


@B
def out_earn_manager():
    return run_sql("""
        SELECT name FROM employees e
        WHERE salary > (SELECT m.salary FROM employees m WHERE m.id = e.manager_id)
        ORDER BY name""")


@O
def out_earn_manager():
    return run_sql("""
        SELECT e.name FROM employees e
        JOIN employees m ON e.manager_id = m.id
        WHERE e.salary > m.salary
        ORDER BY e.name""")


Q(None, "Second Highest Salary", "Medium", "The classic",
  "Return the second highest distinct salary.",
  [((), 120)],
  ("MAX of everything below the MAX.", "O(n)", "O(1)"),
  ("<code>DISTINCT</code>, <code>ORDER BY</code>, <code>LIMIT 1 OFFSET 1</code>. Change the offset for any N.", "O(n log n)", "O(n)"))


@B
def second_highest():
    return run_sql("""
        SELECT MAX(salary) FROM employees
        WHERE salary < (SELECT MAX(salary) FROM employees)""")[0][0]


@O
def second_highest():
    return run_sql("""
        SELECT DISTINCT salary FROM employees
        ORDER BY salary DESC LIMIT 1 OFFSET 1""")[0][0]


Q(None, "Find Duplicates", "Easy", "GROUP BY + HAVING",
  "Return email addresses appearing more than once, sorted.",
  [((), ['a@x.com', 'b@x.com'])],
  ("Self join on the same email with a different id.", "O(n²)", "O(n)"),
  ("Group and keep counts above 1.", "O(n)", "O(n)"))


@B
def duplicate_emails():
    rows = run_sql("""
        SELECT DISTINCT a.email FROM emails a
        JOIN emails b ON a.email = b.email AND a.id <> b.id
        ORDER BY a.email""")
    return [r[0] for r in rows]


@O
def duplicate_emails():
    rows = run_sql("SELECT email FROM emails GROUP BY email HAVING COUNT(*) > 1 ORDER BY email")
    return [r[0] for r in rows]


Q(None, "Keep the First of Each Duplicate", "Medium", "De-duplicating",
  "Return (id, email) of the row with the lowest id for each email, ordered by id.",
  [((), [[1, 'a@x.com'], [2, 'b@x.com'], [4, 'c@x.com']])],
  ("<code>NOT EXISTS</code> a lower id with the same email.", "O(n²)", "O(n)"),
  ("<code>ROW_NUMBER()</code> per email, keeping number 1. It also handles 'latest per user'.", "O(n log n)", "O(n)"))


@B
def first_of_each():
    return run_sql("""
        SELECT id, email FROM emails a
        WHERE NOT EXISTS (SELECT 1 FROM emails b WHERE b.email = a.email AND b.id < a.id)
        ORDER BY id""")


@O
def first_of_each():
    return run_sql("""
        WITH ranked AS (
            SELECT id, email, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
            FROM emails)
        SELECT id, email FROM ranked WHERE rn = 1 ORDER BY id""")


Q(None, "Above the Department Average", "Medium", "Correlated subquery vs window",
  "Return names of employees paid more than their own department's average, ordered by name.",
  [((), ['Asha', 'Eli'])],
  ("A correlated subquery recomputes the average per row.", "O(n²)", "O(1)"),
  ("Window <code>AVG(...) OVER (PARTITION BY ...)</code>, once.", "O(n log n)", "O(n)"))


@B
def above_dept_average():
    rows = run_sql("""
        SELECT name FROM employees e
        WHERE salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)
        ORDER BY name""")
    return [r[0] for r in rows]


@O
def above_dept_average():
    rows = run_sql("""
        WITH t AS (SELECT name, salary, AVG(salary) OVER (PARTITION BY dept_id) AS a
                   FROM employees WHERE dept_id IS NOT NULL)
        SELECT name FROM t WHERE salary > a ORDER BY name""")
    return [r[0] for r in rows]


Q(None, "Rank Salaries", "Medium", "ROW_NUMBER, RANK, DENSE_RANK",
  "For dept_id 1, return name, ROW_NUMBER, RANK and DENSE_RANK by salary (highest first, ties by name).",
  [((), [['Asha', 1, 1, 1], ['Ben', 2, 2, 2], ['Chen', 3, 2, 2], ['Dara', 4, 4, 3]])],
  ("Counting subqueries for each kind of rank.", "O(n²)", "O(n)"),
  ("Three window functions.", "O(n log n)", "O(n)"))


@B
def rank_salaries():
    return run_sql("""
        SELECT name,
          (SELECT COUNT(*) FROM employees b WHERE b.dept_id = 1
             AND (b.salary > a.salary OR (b.salary = a.salary AND b.name <= a.name))) AS rn,
          (SELECT COUNT(*) + 1 FROM employees b WHERE b.dept_id = 1 AND b.salary > a.salary) AS rk,
          (SELECT COUNT(DISTINCT salary) + 1 FROM employees b WHERE b.dept_id = 1 AND b.salary > a.salary) AS dr
        FROM employees a WHERE dept_id = 1 ORDER BY rn""")


@O
def rank_salaries():
    return run_sql("""
        SELECT name,
          ROW_NUMBER() OVER (ORDER BY salary DESC, name),
          RANK() OVER (ORDER BY salary DESC),
          DENSE_RANK() OVER (ORDER BY salary DESC)
        FROM employees WHERE dept_id = 1
        ORDER BY salary DESC, name""")


Q(None, "Top Earner per Department", "Medium", "Top N per group",
  "Return the department name and employee name of each department's highest paid person (all ties), ordered by department name, then employee.",
  [((), [['Eng', 'Asha'], ['HR', 'Hana'], ['Sales', 'Eli']])],
  ("Join to a subquery holding each department's MAX.", "O(n)", "O(d)"),
  ("<code>RANK()</code> per department, keeping rank 1. Change 1 to get top N.", "O(n log n)", "O(n)"))


@B
def top_per_department():
    return run_sql("""
        SELECT d.name, e.name FROM employees e
        JOIN departments d ON d.id = e.dept_id
        JOIN (SELECT dept_id, MAX(salary) AS m FROM employees GROUP BY dept_id) t
          ON t.dept_id = e.dept_id AND t.m = e.salary
        ORDER BY d.name, e.name""")


@O
def top_per_department():
    return run_sql("""
        WITH r AS (
            SELECT d.name AS dept, e.name AS emp,
                   RANK() OVER (PARTITION BY d.id ORDER BY e.salary DESC) AS rk
            FROM employees e JOIN departments d ON d.id = e.dept_id)
        SELECT dept, emp FROM r WHERE rk = 1 ORDER BY dept, emp""")


Q(None, "Top 2 Distinct Salaries per Department", "Hard", "DENSE_RANK",
  "Return department id, employee name and salary for everyone in their department's top 2 distinct salaries. Order by dept_id, salary descending, name.",
  [((), [[1, 'Asha', 150], [1, 'Ben', 120], [1, 'Chen', 120], [2, 'Eli', 100], [2, 'Gus', 80], [3, 'Hana', 60]])],
  ("Count how many distinct higher salaries exist in the department.", "O(n²)", "O(n)"),
  ("<code>DENSE_RANK() &lt;= 2</code>.", "O(n log n)", "O(n)"))


@B
def top_two_salaries():
    return run_sql("""
        SELECT dept_id, name, salary FROM employees a
        WHERE dept_id IS NOT NULL AND
          (SELECT COUNT(DISTINCT salary) FROM employees b
           WHERE b.dept_id = a.dept_id AND b.salary > a.salary) < 2
        ORDER BY dept_id, salary DESC, name""")


@O
def top_two_salaries():
    return run_sql("""
        WITH r AS (
            SELECT dept_id, name, salary,
                   DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dr
            FROM employees WHERE dept_id IS NOT NULL)
        SELECT dept_id, name, salary FROM r WHERE dr <= 2
        ORDER BY dept_id, salary DESC, name""")


Q(None, "Running Total", "Medium", "SUM OVER",
  "Return order id, amount and the running total of amount across all orders by date.",
  [((), [[1, 100, 100], [2, 50, 150], [3, 200, 350], [4, 70, 420], [5, 30, 450], [6, 80, 530], [7, 80, 610]])],
  ("Subquery summing all earlier rows, for each row.", "O(n²)", "O(1)"),
  ("<code>SUM(amount) OVER (ORDER BY ...)</code>.", "O(n log n)", "O(n)"))


@B
def running_total():
    return run_sql("""
        SELECT id, amount,
          (SELECT SUM(amount) FROM orders b WHERE b.order_date <= a.order_date)
        FROM orders a ORDER BY order_date""")


@O
def running_total():
    return run_sql("""
        SELECT id, amount, SUM(amount) OVER (ORDER BY order_date)
        FROM orders ORDER BY order_date""")


Q(None, "Month-Over-Month Change", "Hard", "LAG",
  "For each month, return the month (YYYY-MM), revenue, and the change from the previous month (NULL for the first).",
  [((), [['2024-01', 350, None], ['2024-02', 100, -250], ['2024-03', 160, 60]])],
  ("Self join each month's totals to the previous row in a CTE.", "O(m²)", "O(m)"),
  ("<code>LAG()</code> reads the previous row.", "O(m log m)", "O(m)"))


@B
def month_change():
    return run_sql("""
        WITH m AS (SELECT substr(order_date, 1, 7) AS mon, SUM(amount) AS rev FROM orders GROUP BY mon)
        SELECT a.mon, a.rev,
          a.rev - (SELECT b.rev FROM m b WHERE b.mon < a.mon ORDER BY b.mon DESC LIMIT 1)
        FROM m a ORDER BY a.mon""")


@O
def month_change():
    return run_sql("""
        WITH m AS (SELECT substr(order_date, 1, 7) AS mon, SUM(amount) AS rev FROM orders GROUP BY mon)
        SELECT mon, rev, rev - LAG(rev) OVER (ORDER BY mon) FROM m ORDER BY mon""")


Q(None, "Share of Total", "Medium", "Percent of the whole",
  "For each customer with orders, return name and their share of total revenue as a percentage rounded to 1 decimal, biggest first.",
  [((), [['Bob', 59.0], ['Ann', 36.1], ['Cid', 4.9]])],
  ("A scalar subquery for the grand total.", "O(n)", "O(c)"),
  ("A window over the grouped totals: <code>SUM(SUM(amount)) OVER ()</code>.", "O(n)", "O(c)"))


@B
def revenue_share():
    return run_sql("""
        SELECT c.name, ROUND(100.0 * SUM(o.amount) / (SELECT SUM(amount) FROM orders), 1) AS pct
        FROM orders o JOIN customers c ON c.id = o.customer_id
        GROUP BY c.id ORDER BY pct DESC""")


@O
def revenue_share():
    return run_sql("""
        SELECT c.name, ROUND(100.0 * SUM(o.amount) / SUM(SUM(o.amount)) OVER (), 1) AS pct
        FROM orders o JOIN customers c ON c.id = o.customer_id
        GROUP BY c.id ORDER BY pct DESC""")


Q(None, "Pivot With CASE", "Medium", "Rows to columns",
  "For each customer id with orders, return id and revenue in January, February and March as separate columns, ordered by id.",
  [((), [[1, 150, 70, 0], [2, 200, 0, 160], [3, 0, 30, 0]])],
  ("Three scalar subqueries per customer.", "O(c·n)", "O(c)"),
  ("Conditional aggregation: <code>SUM(CASE WHEN ...)</code>.", "O(n)", "O(c)"))


@B
def pivot_months():
    return run_sql("""
        SELECT id,
          (SELECT COALESCE(SUM(amount), 0) FROM orders WHERE customer_id = c.id AND order_date LIKE '2024-01%'),
          (SELECT COALESCE(SUM(amount), 0) FROM orders WHERE customer_id = c.id AND order_date LIKE '2024-02%'),
          (SELECT COALESCE(SUM(amount), 0) FROM orders WHERE customer_id = c.id AND order_date LIKE '2024-03%')
        FROM customers c WHERE id IN (SELECT customer_id FROM orders) ORDER BY id""")


@O
def pivot_months():
    return run_sql("""
        SELECT customer_id,
          SUM(CASE WHEN order_date LIKE '2024-01%' THEN amount ELSE 0 END),
          SUM(CASE WHEN order_date LIKE '2024-02%' THEN amount ELSE 0 END),
          SUM(CASE WHEN order_date LIKE '2024-03%' THEN amount ELSE 0 END)
        FROM orders GROUP BY customer_id ORDER BY customer_id""")


Q(None, "Consecutive Login Streaks", "Hard", "Gaps and islands",
  "For each user, return user_id and their longest run of consecutive days, ordered by user_id.",
  [((), [[1, 3], [2, 2], [3, 1]])],
  ("Fetch rows and walk them in Python, tracking the current run.", "O(n log n)", "O(n)"),
  ("Day minus ROW_NUMBER is constant within a streak, so group by that difference.", "O(n log n)", "O(n)"))


@B
def longest_streak():
    rows = run_sql("SELECT user_id, day FROM logins ORDER BY user_id, day")
    best = {}
    prev_user, prev_day, run = None, None, 0
    for user, day in rows:
        run = run + 1 if user == prev_user and day == prev_day + 1 else 1
        best[user] = max(best.get(user, 0), run)
        prev_user, prev_day = user, day
    return [[u, best[u]] for u in sorted(best)]


@O
def longest_streak():
    return run_sql("""
        WITH g AS (
            SELECT user_id, day - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS grp
            FROM logins),
        s AS (SELECT user_id, COUNT(*) AS n FROM g GROUP BY user_id, grp)
        SELECT user_id, MAX(n) FROM s GROUP BY user_id ORDER BY user_id""")


Q(None, "Walk the Org Chart", "Hard", "Recursive CTE",
  "Return every employee's name and depth below the top (Asha = 0), ordered by depth, then name.",
  [((), [['Asha', 0], ['Ben', 1], ['Chen', 1], ['Eli', 1], ['Hana', 1], ['Ivan', 1], ['Dara', 2], ['Fay', 2], ['Gus', 2]])],
  ("Fetch the table and search it level by level in Python.", "O(n·d)", "O(n)"),
  ("A recursive CTE starts at the root and joins down, one level at a time.", "O(n)", "O(n)"))


@B
def org_depth():
    rows = run_sql("SELECT id, name, manager_id FROM employees")
    depth = {}
    level, frontier = 0, {r[0] for r in rows if r[2] is None}
    while frontier:
        for i in frontier:
            depth[i] = level
        frontier = {r[0] for r in rows if r[2] in frontier}
        level += 1
    return sorted(([r[1], depth[r[0]]] for r in rows), key=lambda x: (x[1], x[0]))


@O
def org_depth():
    return run_sql("""
        WITH RECURSIVE tree(id, name, depth) AS (
            SELECT id, name, 0 FROM employees WHERE manager_id IS NULL
            UNION ALL
            SELECT e.id, e.name, t.depth + 1
            FROM employees e JOIN tree t ON e.manager_id = t.id)
        SELECT name, depth FROM tree ORDER BY depth, name""")


Q(None, "COUNT and NULL", "Easy", "A favourite trick question",
  "Return COUNT(*), COUNT(dept_id) and COUNT(DISTINCT dept_id) from employees, as one row.",
  [((), [9, 8, 3])],
  ("Fetch the column and count in Python.", "O(n)", "O(n)"),
  ("All three in one query. Only <code>COUNT(*)</code> includes NULLs.", "O(n)", "O(d)"))


@B
def count_kinds():
    values = [r[0] for r in run_sql("SELECT dept_id FROM employees")]
    known = [v for v in values if v is not None]
    return [len(values), len(known), len(set(known))]


@O
def count_kinds():
    return run_sql("SELECT COUNT(*), COUNT(dept_id), COUNT(DISTINCT dept_id) FROM employees")[0]
