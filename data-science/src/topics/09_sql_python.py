from lib import *
import sqlite3
import numpy as np
import pandas as pd


TOPIC(
    id="sql-python", title="SQL from Python", glyph="SQL",
    blurb="Query a real database from Python: sqlite3 connections, safe parameters, joins, GROUP BY and HAVING, subqueries, window functions, dates, upserts, transactions, and moving data between SQL and pandas.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">con = sqlite3.connect("shop.db")          # or ":memory:"
con.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
con.executemany("INSERT INTO t VALUES (?, ?)", rows)   # ? = safe parameters
rows = con.execute("SELECT * FROM t WHERE id = ?", (7,)).fetchall()
con.commit()                                # or: with con: ... (commit / rollback)
df = pd.read_sql_query("SELECT ...", con, params=(...,))
df.to_sql("t", con, index=False, if_exists="replace")</code></pre>
<p>SQL runs in this order: FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.</p>
""")

CUSTOMERS = [(1, "Asha", "Pune"), (2, "Ravi", "Delhi"), (3, "Meera", "Pune"), (4, "John", "Mumbai")]
ORDERS = [(101, 1, 250.0, "2026-01-05"), (102, 2, 120.0, "2026-01-05"), (103, 1, 90.0, "2026-01-20"),
          (104, 3, 400.0, "2026-02-02"), (105, 2, 60.0, "2026-02-14"), (106, 1, 310.0, "2026-02-20")]


def shop_db(customers, orders):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
    con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL, day TEXT)")
    con.executemany("INSERT INTO customers VALUES (?, ?, ?)", customers)
    con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    return con


Q(None, "Load Rows and Count Them", "Easy", "CREATE · executemany",
  "Load the two tables into SQLite and return <code>(number of customers, number of orders)</code>.",
  [((CUSTOMERS, ORDERS), (4, 6)), ((CUSTOMERS[:2], []), (2, 0))],
  ("Just count the Python lists.", "O(1)", "O(1)"),
  ("Build the database with <code>executemany</code> and ask it with <code>COUNT(*)</code>.", "O(n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def counts(customers, orders):
    return (len(customers), len(orders))


@O
def counts(customers, orders):
    con = shop_db(customers, orders)
    c = con.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    o = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    return (c, o)


Q(None, "Orders Above an Amount", "Easy", "WHERE with a parameter",
  "Return <code>(id, amount)</code> for orders with amount ≥ <code>minimum</code>, highest first.",
  [((CUSTOMERS, ORDERS, 200), [(104, 400.0), (106, 310.0), (101, 250.0)]), ((CUSTOMERS, ORDERS, 1000), [])],
  ("Filter and sort the list in Python.", "O(n log n)", "O(n)"),
  ("<code>WHERE amount &gt;= ?</code> with the value passed separately — never pasted into the SQL text.", "O(n log n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS, 200))


@B
def big_orders(customers, orders, minimum):
    rows = [(o[0], o[2]) for o in orders if o[2] >= minimum]
    return sorted(rows, key=lambda r: -r[1])


@O
def big_orders(customers, orders, minimum):
    con = shop_db(customers, orders)
    sql = "SELECT id, amount FROM orders WHERE amount >= ? ORDER BY amount DESC"
    return con.execute(sql, (minimum,)).fetchall()


Q(None, "Safe Lookup by Name", "Medium", "SQL injection",
  "Return the ids of customers whose name equals <code>name</code> exactly. The test includes an attack string, which must match nobody.",
  [((CUSTOMERS, ORDERS, "Ravi"), [2]), ((CUSTOMERS, ORDERS, "x' OR '1'='1"), [])],
  ("Compare names in Python — no SQL, so nothing to inject.", "O(n)", "O(n)"),
  ("A <code>?</code> placeholder: the driver sends the value as data, so quotes inside it can't change the query.", "O(n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS, "x' OR '1'='1"))


@B
def ids_named(customers, orders, name):
    return [c[0] for c in customers if c[1] == name]


@O
def ids_named(customers, orders, name):
    con = shop_db(customers, orders)
    rows = con.execute("SELECT id FROM customers WHERE name = ? ORDER BY id", (name,)).fetchall()
    return [r[0] for r in rows]


Q(None, "Revenue per City", "Easy", "JOIN + GROUP BY",
  "Return <code>(city, total amount)</code> for every city with orders, sorted by city.",
  [((CUSTOMERS, ORDERS), [('Delhi', 180.0), ('Pune', 1050.0)]), ((CUSTOMERS, ORDERS[:2]), [('Delhi', 120.0), ('Pune', 250.0)])],
  ("Map customer → city in a dict, then add up amounts per city.", "O(n + m)", "O(n)"),
  ("<code>JOIN</code> the tables and <code>GROUP BY city</code>.", "O(n + m)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def city_revenue(customers, orders):
    city_of = {c[0]: c[2] for c in customers}
    totals = {}
    for o in orders:
        city = city_of[o[1]]
        totals[city] = totals.get(city, 0) + o[2]
    return sorted(totals.items())


@O
def city_revenue(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT c.city, SUM(o.amount) FROM orders o
             JOIN customers c ON c.id = o.customer_id
             GROUP BY c.city ORDER BY c.city"""
    return con.execute(sql).fetchall()


Q(None, "Customers With No Orders", "Easy", "LEFT JOIN … IS NULL",
  "Return the names of customers who never ordered, sorted.",
  [((CUSTOMERS, ORDERS), ['John']), ((CUSTOMERS, []), ['Asha', 'John', 'Meera', 'Ravi'])],
  ("A set of customer ids that ordered, then the rest.", "O(n + m)", "O(m)"),
  ("<code>LEFT JOIN</code> keeps every customer; missing orders show up as NULL.", "O(n + m)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def never_ordered(customers, orders):
    buyers = {o[1] for o in orders}
    return sorted(c[1] for c in customers if c[0] not in buyers)


@O
def never_ordered(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id
             WHERE o.id IS NULL ORDER BY c.name"""
    return [r[0] for r in con.execute(sql)]


Q(None, "Big Spenders", "Medium", "HAVING",
  "Return <code>(name, total, number of orders)</code> for customers whose total spend is more than <code>limit</code>, biggest total first.",
  [((CUSTOMERS, ORDERS, 300), [('Asha', 650.0, 3), ('Meera', 400.0, 1)]), ((CUSTOMERS, ORDERS, 600), [('Asha', 650.0, 3)])],
  ("Total and count per customer in dicts, then filter.", "O(n + m)", "O(n)"),
  ("<code>GROUP BY</code> then <code>HAVING SUM(amount) &gt; ?</code> — WHERE can't see sums, HAVING can.", "O(n + m)", "O(n)"),
  viz=(CUSTOMERS, ORDERS, 300))


@B
def big_spenders(customers, orders, limit):
    name = {c[0]: c[1] for c in customers}
    total, count = {}, {}
    for o in orders:
        total[o[1]] = total.get(o[1], 0) + o[2]
        count[o[1]] = count.get(o[1], 0) + 1
    rows = [(name[k], total[k], count[k]) for k in total if total[k] > limit]
    return sorted(rows, key=lambda r: -r[1])


@O
def big_spenders(customers, orders, limit):
    con = shop_db(customers, orders)
    sql = """SELECT c.name, SUM(o.amount) AS total, COUNT(*) FROM orders o
             JOIN customers c ON c.id = o.customer_id
             GROUP BY c.id HAVING SUM(o.amount) > ? ORDER BY total DESC"""
    return con.execute(sql, (limit,)).fetchall()


Q(None, "Orders Above Average", "Medium", "Subquery",
  "Return the ids of orders whose amount is above the average order amount.",
  [((CUSTOMERS, ORDERS), [101, 104, 106]), ((CUSTOMERS, ORDERS[:3]), [101])],
  ("Two passes: compute the mean, then filter.", "O(n)", "O(n)"),
  ("A scalar subquery: <code>WHERE amount &gt; (SELECT AVG(amount) FROM orders)</code>.", "O(n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def above_average(customers, orders):
    avg = sum(o[2] for o in orders) / len(orders)
    return [o[0] for o in orders if o[2] > avg]


@O
def above_average(customers, orders):
    con = shop_db(customers, orders)
    sql = "SELECT id FROM orders WHERE amount > (SELECT AVG(amount) FROM orders) ORDER BY id"
    return [r[0] for r in con.execute(sql)]


Q(None, "Biggest Order per Customer", "Medium", "ROW_NUMBER() OVER (PARTITION BY …)",
  "Return <code>(customer_id, order id, amount)</code> of each customer's largest order, sorted by customer.",
  [((CUSTOMERS, ORDERS), [(1, 106, 310.0), (2, 102, 120.0), (3, 104, 400.0)])],
  ("Keep the best order per customer in a dict.", "O(n)", "O(n)"),
  ("Number the rows inside each customer by amount, keep row 1.", "O(n log n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def top_order(customers, orders):
    best = {}
    for o in orders:
        if o[1] not in best or o[2] > best[o[1]][2]:
            best[o[1]] = (o[1], o[0], o[2])
    return [best[k] for k in sorted(best)]


@O
def top_order(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT customer_id, id, amount FROM (
               SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn FROM orders)
             WHERE rn = 1 ORDER BY customer_id"""
    return con.execute(sql).fetchall()


Q(None, "Running Total per Customer", "Medium", "SUM() OVER (ORDER BY …)",
  "For customer <code>cid</code>, return <code>(day, amount, running total)</code> in date order.",
  [((CUSTOMERS, ORDERS, 1), [('2026-01-05', 250.0, 250.0), ('2026-01-20', 90.0, 340.0), ('2026-02-20', 310.0, 650.0)]), ((CUSTOMERS, ORDERS, 2), [('2026-01-05', 120.0, 120.0), ('2026-02-14', 60.0, 180.0)])],
  ("Sort that customer's orders and keep a running sum.", "O(n log n)", "O(n)"),
  ("A window <code>SUM(amount) OVER (ORDER BY day)</code>.", "O(n log n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS, 1))


@B
def running_total(customers, orders, cid):
    mine = sorted((o for o in orders if o[1] == cid), key=lambda o: o[3])
    out, total = [], 0
    for o in mine:
        total += o[2]
        out.append((o[3], o[2], total))
    return out


@O
def running_total(customers, orders, cid):
    con = shop_db(customers, orders)
    sql = """SELECT day, amount, SUM(amount) OVER (ORDER BY day) FROM orders
             WHERE customer_id = ? ORDER BY day"""
    return con.execute(sql, (cid,)).fetchall()


Q(None, "Bucket Orders by Size", "Easy", "CASE WHEN",
  "Label each order 'small' (&lt; 100), 'medium' (&lt; 300) or 'large', and return <code>(label, count)</code> sorted by label.",
  [((CUSTOMERS, ORDERS), [('large', 2), ('medium', 2), ('small', 2)])],
  ("An if-chain and a dict of counts.", "O(n)", "O(1)"),
  ("<code>CASE WHEN … END</code> inside the SELECT, then GROUP BY the label.", "O(n)", "O(1)"),
  viz=(CUSTOMERS, ORDERS))


@B
def size_buckets(customers, orders):
    counts = {}
    for o in orders:
        label = "small" if o[2] < 100 else "medium" if o[2] < 300 else "large"
        counts[label] = counts.get(label, 0) + 1
    return sorted(counts.items())


@O
def size_buckets(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT CASE WHEN amount < 100 THEN 'small' WHEN amount < 300 THEN 'medium' ELSE 'large' END AS label,
                    COUNT(*) FROM orders GROUP BY label ORDER BY label"""
    return con.execute(sql).fetchall()


Q(None, "Monthly Revenue", "Easy", "Dates with strftime",
  "Return <code>(month 'YYYY-MM', revenue, orders)</code> in month order.",
  [((CUSTOMERS, ORDERS), [('2026-01', 460.0, 3), ('2026-02', 770.0, 3)])],
  ("Slice the first 7 characters of each date and add up.", "O(n)", "O(months)"),
  ("<code>strftime('%Y-%m', day)</code> and GROUP BY it.", "O(n)", "O(months)"),
  viz=(CUSTOMERS, ORDERS))


@B
def monthly(customers, orders):
    rev, cnt = {}, {}
    for o in orders:
        m = o[3][:7]
        rev[m] = rev.get(m, 0) + o[2]
        cnt[m] = cnt.get(m, 0) + 1
    return [(m, rev[m], cnt[m]) for m in sorted(rev)]


@O
def monthly(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT strftime('%Y-%m', day) AS month, SUM(amount), COUNT(*) FROM orders
             GROUP BY month ORDER BY month"""
    return con.execute(sql).fetchall()


Q(None, "Second-Highest Order Amount", "Medium", "DISTINCT · LIMIT/OFFSET",
  "Return the second-highest distinct order amount, or None if there isn't one.",
  [((CUSTOMERS, ORDERS), 310.0), ((CUSTOMERS, ORDERS[:1]), None)],
  ("A set of amounts, sorted descending.", "O(n log n)", "O(n)"),
  ("<code>SELECT DISTINCT … ORDER BY … LIMIT 1 OFFSET 1</code>, wrapped so an empty result becomes NULL.", "O(n log n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def second_highest(customers, orders):
    amounts = sorted({o[2] for o in orders}, reverse=True)
    return amounts[1] if len(amounts) > 1 else None


@O
def second_highest(customers, orders):
    con = shop_db(customers, orders)
    sql = "SELECT (SELECT DISTINCT amount FROM orders ORDER BY amount DESC LIMIT 1 OFFSET 1)"
    return con.execute(sql).fetchone()[0]


Q(None, "Days With Several Customers", "Easy", "COUNT(DISTINCT …)",
  "Return the days on which at least 2 different customers ordered.",
  [((CUSTOMERS, ORDERS), ['2026-01-05']), ((CUSTOMERS, ORDERS + [(107, 4, 10.0, "2026-02-20")]), ['2026-01-05', '2026-02-20'])],
  ("A set of customers per day.", "O(n)", "O(n)"),
  ("<code>HAVING COUNT(DISTINCT customer_id) &gt;= 2</code>.", "O(n)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def busy_days(customers, orders):
    people = {}
    for o in orders:
        people.setdefault(o[3], set()).add(o[1])
    return sorted(d for d, s in people.items() if len(s) >= 2)


@O
def busy_days(customers, orders):
    con = shop_db(customers, orders)
    sql = "SELECT day FROM orders GROUP BY day HAVING COUNT(DISTINCT customer_id) >= 2 ORDER BY day"
    return [r[0] for r in con.execute(sql)]


Q(None, "Query Straight into a DataFrame", "Easy", "pd.read_sql_query",
  "Return a DataFrame with columns <code>name</code> and <code>orders</code> (order count, including 0), sorted by name.",
  [((CUSTOMERS, ORDERS), {'name': ['Asha', 'John', 'Meera', 'Ravi'], 'orders': [3, 0, 1, 2]})],
  ("Count in Python and build the DataFrame yourself.", "O(n + m)", "O(n)"),
  ("<code>pd.read_sql_query</code> runs the SQL and returns a DataFrame with the column names from the query.", "O(n + m)", "O(n)"),
  viz=(CUSTOMERS, ORDERS))


@B
def orders_frame(customers, orders):
    count = {c[0]: 0 for c in customers}
    for o in orders:
        count[o[1]] += 1
    rows = sorted((c[1], count[c[0]]) for c in customers)
    return pd.DataFrame(rows, columns=["name", "orders"])


@O
def orders_frame(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT c.name, COUNT(o.id) AS orders FROM customers c
             LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.id ORDER BY c.name"""
    return pd.read_sql_query(sql, con)


Q(None, "From a DataFrame to a Table and Back", "Medium", "df.to_sql",
  "<code>data</code> holds columns product, qty and price. Make it a DataFrame, write it to a table, then return <code>(product, revenue)</code> rows from SQL, highest revenue first.",
  [(({"product": ["pen", "book", "bag"], "qty": [10, 2, 1], "price": [5.0, 120.0, 300.0]},), [('bag', 300.0), ('book', 240.0), ('pen', 50.0)])],
  ("Compute revenue in plain Python and sort.", "O(n log n)", "O(n)"),
  ("<code>df.to_sql</code> creates the table; SQL does the maths.", "O(n log n)", "O(n)"),
  viz=({"product": ["pen", "book", "bag"], "qty": [10, 2, 1], "price": [5.0, 120.0, 300.0]},))


@B
def revenue_via_sql(data):
    rows = [(p, q * pr) for p, q, pr in zip(data["product"], data["qty"], data["price"])]
    return sorted(rows, key=lambda r: -r[1])


@O
def revenue_via_sql(data):
    df = pd.DataFrame(data)
    con = sqlite3.connect(":memory:")
    df.to_sql("sales", con, index=False)
    sql = "SELECT product, qty * price AS revenue FROM sales ORDER BY revenue DESC"
    return con.execute(sql).fetchall()


Q(None, "Upsert Stock Levels", "Medium", "INSERT … ON CONFLICT",
  "Start from <code>stock</code> (sku, qty). Apply <code>updates</code>: add the qty to an existing sku, or insert a new sku. Return all rows sorted by sku.",
  [(([("A", 5), ("B", 2)], [("B", 3), ("C", 7), ("A", -1)]), [('A', 4), ('B', 5), ('C', 7)])],
  ("A dict: <code>get(sku, 0) + qty</code>.", "O(n)", "O(n)"),
  ("<code>ON CONFLICT(sku) DO UPDATE SET qty = qty + excluded.qty</code>.", "O(n log n)", "O(n)"),
  viz=([("A", 5), ("B", 2)], [("B", 3), ("C", 7), ("A", -1)]))


@B
def upsert(stock, updates):
    levels = dict(stock)
    for sku, qty in updates:
        levels[sku] = levels.get(sku, 0) + qty
    return sorted(levels.items())


@O
def upsert(stock, updates):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER)")
    con.executemany("INSERT INTO stock VALUES (?, ?)", stock)
    con.executemany("""INSERT INTO stock VALUES (?, ?)
                       ON CONFLICT(sku) DO UPDATE SET qty = qty + excluded.qty""", updates)
    return con.execute("SELECT * FROM stock ORDER BY sku").fetchall()


Q(None, "All-or-Nothing Transfers", "Hard", "Transactions · rollback",
  "Accounts start with <code>balances</code>. Apply each transfer (from, to, amount) as one transaction: if it would make a balance negative, roll it back. Return final balances sorted by account.",
  [(({"A": 100, "B": 50}, [("A", "B", 30), ("B", "A", 500), ("B", "A", 80)]), [('A', 150), ('B', 0)])],
  ("Check the balance first, then move the money in a dict.", "O(n)", "O(a)"),
  ("A <code>CHECK (balance &gt;= 0)</code> constraint plus <code>with con:</code>, which commits or rolls back both updates together.", "O(n)", "O(a)"),
  viz=({"A": 100, "B": 50}, [("A", "B", 30), ("B", "A", 500), ("B", "A", 80)]))


@B
def transfers(balances, moves):
    bal = dict(balances)
    for src, dst, amount in moves:
        if bal[src] - amount >= 0:
            bal[src] -= amount
            bal[dst] += amount
    return sorted(bal.items())


@O
def transfers(balances, moves):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE acct (name TEXT PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")
    con.executemany("INSERT INTO acct VALUES (?, ?)", balances.items())
    con.commit()
    for src, dst, amount in moves:
        try:
            with con:
                con.execute("UPDATE acct SET balance = balance + ? WHERE name = ?", (amount, dst))
                con.execute("UPDATE acct SET balance = balance - ? WHERE name = ?", (amount, src))
        except sqlite3.IntegrityError:
            pass
    return con.execute("SELECT * FROM acct ORDER BY name").fetchall()


Q(None, "Pivot Months into Columns", "Medium", "Conditional aggregation",
  "Return <code>(city, January revenue, February revenue)</code> for every city with orders, sorted by city.",
  [((CUSTOMERS, ORDERS), [('Delhi', 120.0, 60.0), ('Pune', 340.0, 710.0)])],
  ("Nested dicts city → month → total.", "O(n)", "O(cities)"),
  ("<code>SUM(CASE WHEN month = … THEN amount ELSE 0 END)</code> — one column per month.", "O(n)", "O(cities)"),
  viz=(CUSTOMERS, ORDERS))


@B
def city_by_month(customers, orders):
    city_of = {c[0]: c[2] for c in customers}
    table = {}
    for o in orders:
        row = table.setdefault(city_of[o[1]], [0, 0])
        if o[3].startswith("2026-01"):
            row[0] += o[2]
        elif o[3].startswith("2026-02"):
            row[1] += o[2]
    return [(city, jan, feb) for city, (jan, feb) in sorted(table.items())]


@O
def city_by_month(customers, orders):
    con = shop_db(customers, orders)
    sql = """SELECT c.city,
               SUM(CASE WHEN strftime('%m', o.day) = '01' THEN o.amount ELSE 0 END),
               SUM(CASE WHEN strftime('%m', o.day) = '02' THEN o.amount ELSE 0 END)
             FROM orders o JOIN customers c ON c.id = o.customer_id
             GROUP BY c.city ORDER BY c.city"""
    return con.execute(sql).fetchall()


Q(None, "Keep the Latest Version of Each Record", "Hard", "De-duplication",
  "<code>events</code> are (user_id, updated_at, email) rows with repeats. Keep each user's most recent row; return them sorted by user.",
  [(([(1, "2026-01-01", "a@x.in"), (2, "2026-01-03", "b@x.in"), (1, "2026-02-10", "a@new.in"), (2, "2026-01-02", "old@x.in")],), [(1, '2026-02-10', 'a@new.in'), (2, '2026-01-03', 'b@x.in')])],
  ("A dict that keeps the row with the larger timestamp.", "O(n)", "O(users)"),
  ("<code>ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC)</code> and keep row 1.", "O(n log n)", "O(n)"),
  viz=([(1, "2026-01-01", "a@x.in"), (2, "2026-01-03", "b@x.in"), (1, "2026-02-10", "a@new.in")],))


@B
def latest(events):
    best = {}
    for e in events:
        if e[0] not in best or e[1] > best[e[0]][1]:
            best[e[0]] = e
    return [best[k] for k in sorted(best)]


@O
def latest(events):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE ev (user_id INTEGER, updated_at TEXT, email TEXT)")
    con.executemany("INSERT INTO ev VALUES (?, ?, ?)", events)
    sql = """SELECT user_id, updated_at, email FROM (
               SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn FROM ev)
             WHERE rn = 1 ORDER BY user_id"""
    return con.execute(sql).fetchall()


Q(None, "Does the Query Use the Index?", "Medium", "Indexes · EXPLAIN QUERY PLAN",
  "Run <code>SELECT * FROM orders WHERE customer_id = 1</code>. Return <code>(plan uses an index before, after creating one)</code> as two booleans.",
  [((CUSTOMERS, ORDERS), (False, True))],
  ("Reason about it: without an index the database must scan every row.", "O(1)", "O(1)"),
  ("Ask SQLite: <code>EXPLAIN QUERY PLAN</code> says SCAN (every row) or SEARCH … USING INDEX.", "O(log n) lookups", "O(n) index"),
  viz=(CUSTOMERS, ORDERS))


@B
def uses_index(customers, orders):
    has_index = False
    before = has_index
    has_index = True
    return (before, has_index)


@O
def uses_index(customers, orders):
    con = shop_db(customers, orders)
    sql = "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1"
    before = "USING INDEX" in " ".join(str(r) for r in con.execute(sql))
    con.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    after = "USING INDEX" in " ".join(str(r) for r in con.execute(sql))
    return (before, after)
