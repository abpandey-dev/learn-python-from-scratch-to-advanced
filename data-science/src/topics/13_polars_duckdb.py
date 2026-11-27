from lib import *
import math
import re
from collections import Counter, defaultdict
from datetime import date, timedelta

import duckdb
import pandas as pd
import polars as pl

TOPIC(
    id="polars-duckdb", title="Polars & DuckDB", glyph="⚡",
    blurb="The modern, fast way to wrangle data on one machine: Polars expressions, lazy queries, window functions, joins, pivots, rolling windows, strings, nulls, lists and dedupe — and DuckDB SQL straight on your data: HAVING, running totals and LAG, QUALIFY, FILTER, ASOF joins, lists and gap-filled dates. Every answer is also shown in plain Python.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import polars as pl
df = pl.read_csv("orders.csv")                       # or pl.scan_csv(...) for lazy
(df.filter(pl.col("status") == "completed")
   .with_columns((pl.col("qty") * pl.col("price")).alias("revenue"))
   .group_by("city").agg(pl.len().alias("orders"), pl.col("revenue").sum())
   .sort("revenue", descending=True))

import duckdb
duckdb.sql("SELECT city, SUM(qty * price) AS revenue FROM 'orders.csv' GROUP BY city").df()
duckdb.sql("SELECT * FROM df WHERE amount > 100")    # query a pandas or Polars frame by name</code></pre>
<p><b>Running the answers:</b> DuckDB runs in this site's in-browser IDE. Polars does not run in the browser yet — run Polars answers in Colab or on your machine (<code>pip install polars duckdb</code>). The IDE's ✓ Check works for any answer that returns the right values, including plain Python or pandas.</p>
""")


def sql_table(con, name, rows):
    """Create a DuckDB table from a list of dicts (types taken from the first non-null value of each column)."""
    cols = list(rows[0])
    def sql_type(c):
        v = next((r[c] for r in rows if r[c] is not None), "")
        return "BOOLEAN" if isinstance(v, bool) else "BIGINT" if isinstance(v, int) else "DOUBLE" if isinstance(v, float) else "VARCHAR"
    con.execute(f"CREATE TABLE {name} ({', '.join(f'{c} {sql_type(c)}' for c in cols)})")
    con.executemany(f"INSERT INTO {name} VALUES ({', '.join('?' * len(cols))})", [[r[c] for c in cols] for r in rows])


ORDERS = [
    {"id": 1, "customer": "asha", "city": "Pune", "status": "completed", "amount": 1200.0},
    {"id": 2, "customer": "ravi", "city": "Delhi", "status": "cancelled", "amount": 450.0},
    {"id": 3, "customer": "meera", "city": "Pune", "status": "completed", "amount": 80.0},
    {"id": 4, "customer": "asha", "city": "Pune", "status": "completed", "amount": 640.0},
    {"id": 5, "customer": "dev", "city": "Goa", "status": "completed", "amount": 2100.0},
    {"id": 6, "customer": "ravi", "city": "Delhi", "status": "completed", "amount": 330.0},
    {"id": 7, "customer": "kim", "city": "Delhi", "status": "returned", "amount": 990.0},
    {"id": 8, "customer": "meera", "city": "Pune", "status": "completed", "amount": 150.0},
]


Q(None, "Filter and Add a Column", "Easy", "Polars · filter, with_columns",
  "From the orders, keep completed ones with amount ≥ <code>min_amount</code>, add <code>with_tax = round(amount × 1.18, 2)</code>, and return rows <code>(id, amount, with_tax)</code> sorted by id.",
  [((ORDERS, 300), [(1, 1200.0, 1416.0), (4, 640.0, 755.2), (5, 2100.0, 2478.0), (6, 330.0, 389.4)])],
  ("A loop with if-statements.", "O(n log n)", "O(n)"),
  ("<code>filter</code>, <code>with_columns</code>, <code>select</code>, <code>sort</code>.", "O(n log n)", "O(n)"),
  viz=((ORDERS[:3], 100)))


@B
def big_orders(rows, min_amount):
    out = []
    for r in rows:
        if r["status"] == "completed" and r["amount"] >= min_amount:
            out.append((r["id"], r["amount"], round(r["amount"] * 1.18, 2)))
    return sorted(out)


@O
def big_orders(rows, min_amount):
    df = pl.DataFrame(rows)
    return (df.filter((pl.col("status") == "completed") & (pl.col("amount") >= min_amount))
              .with_columns((pl.col("amount") * 1.18).round(2).alias("with_tax"))
              .select("id", "amount", "with_tax").sort("id").rows())


Q(None, "Bucket Values With when/then", "Easy", "Polars · conditional columns",
  "Label each order's amount as <code>'small'</code> (&lt; 200), <code>'medium'</code> (&lt; 1000) or <code>'large'</code>, and return the count of orders per band as <code>(band, count)</code> sorted by band.",
  [((ORDERS,), [('large', 2), ('medium', 4), ('small', 2)])],
  ("if/elif per row and a counting dict.", "O(n)", "O(1)"),
  ("<code>pl.when().then().otherwise()</code> then <code>group_by</code>.", "O(n)", "O(1)"),
  viz=((ORDERS[:3],)))


@B
def amount_bands(rows):
    counts = {}
    for r in rows:
        a = r["amount"]
        band = "small" if a < 200 else "medium" if a < 1000 else "large"
        counts[band] = counts.get(band, 0) + 1
    return sorted(counts.items())


@O
def amount_bands(rows):
    a = pl.col("amount")
    band = pl.when(a < 200).then(pl.lit("small")).when(a < 1000).then(pl.lit("medium")).otherwise(pl.lit("large"))
    return pl.DataFrame(rows).group_by(band.alias("band")).agg(pl.len()).sort("band").rows()


Q(None, "Group and Aggregate", "Easy", "Polars · group_by().agg()",
  "For completed orders, return per city <code>(city, orders, revenue, average order rounded to 1)</code> sorted by revenue, highest first.",
  [((ORDERS,), [('Goa', 1, 2100.0, 2100.0), ('Pune', 4, 2070.0, 517.5), ('Delhi', 1, 330.0, 330.0)])],
  ("A dict of [count, total] lists.", "O(n log c)", "O(c)"),
  ("<code>group_by('city').agg(...)</code> with several expressions.", "O(n log c)", "O(c)"),
  viz=((ORDERS[:4],)))


@B
def city_summary(rows):
    s = {}
    for r in rows:
        if r["status"] == "completed":
            s.setdefault(r["city"], [0, 0.0])
            s[r["city"]][0] += 1
            s[r["city"]][1] += r["amount"]
    out = [(c, n, t, round(t / n, 1)) for c, (n, t) in s.items()]
    return sorted(out, key=lambda x: -x[2])


@O
def city_summary(rows):
    return (pl.DataFrame(rows).filter(pl.col("status") == "completed")
              .group_by("city")
              .agg(pl.len().alias("orders"), pl.col("amount").sum().alias("revenue"), pl.col("amount").mean().round(1).alias("avg"))
              .sort("revenue", descending=True).rows())


Q(None, "A Lazy Query", "Medium", "Polars · lazy() and collect()",
  "Write the top-<code>k</code> customers by completed revenue as a <b>lazy</b> query: Polars builds a plan, pushes the filter down, and only computes on <code>collect()</code>. Return <code>(customer, revenue)</code> pairs, ties by name.",
  [((ORDERS, 3), [('dev', 2100.0), ('asha', 1840.0), ('ravi', 330.0)])],
  ("Sum per customer in a dict, sort, slice.", "O(n + c log c)", "O(c)"),
  ("<code>df.lazy()…head(k).collect()</code>.", "O(n + c log c)", "O(c)"),
  viz=((ORDERS[:4], 2)))


@B
def top_customers(rows, k):
    rev = {}
    for r in rows:
        if r["status"] == "completed":
            rev[r["customer"]] = rev.get(r["customer"], 0.0) + r["amount"]
    return sorted(rev.items(), key=lambda x: (-x[1], x[0]))[:k]


@O
def top_customers(rows, k):
    plan = (pl.DataFrame(rows).lazy()
              .filter(pl.col("status") == "completed")
              .group_by("customer").agg(pl.col("amount").sum().alias("revenue"))
              .sort(["revenue", "customer"], descending=[True, False])
              .head(k))
    return plan.collect().rows()


Q(None, "Rank Within Groups", "Medium", "Polars · window expressions with over()",
  "For completed orders, add each order's rank by amount within its city (1 = largest, dense) and its share of the city's revenue (% rounded to 1). Return <code>(id, city, rank, share)</code> sorted by city then rank.",
  [((ORDERS,), [(6, 'Delhi', 1, 100.0), (5, 'Goa', 1, 100.0), (1, 'Pune', 1, 58.0), (4, 'Pune', 2, 30.9), (8, 'Pune', 3, 7.2), (3, 'Pune', 4, 3.9)])],
  ("Group lists, sort each, compute shares.", "O(n log n)", "O(n)"),
  ("<code>rank(...).over('city')</code> and <code>sum().over('city')</code>.", "O(n log n)", "O(n)"),
  viz=((ORDERS[:4],)))


@B
def rank_in_city(rows):
    groups = {}
    for r in rows:
        if r["status"] == "completed":
            groups.setdefault(r["city"], []).append(r)
    out = []
    for city, rs in groups.items():
        total = sum(r["amount"] for r in rs)
        distinct = sorted({r["amount"] for r in rs}, reverse=True)
        for r in rs:
            out.append((r["id"], city, distinct.index(r["amount"]) + 1, round(r["amount"] / total * 100, 1)))
    return sorted(out, key=lambda x: (x[1], x[2], x[0]))


@O
def rank_in_city(rows):
    return (pl.DataFrame(rows).filter(pl.col("status") == "completed")
              .with_columns(pl.col("amount").rank("dense", descending=True).over("city").cast(pl.Int64).alias("rank"),
                            (pl.col("amount") / pl.col("amount").sum().over("city") * 100).round(1).alias("share"))
              .select("id", "city", "rank", "share").sort(["city", "rank", "id"]).rows())


CUSTOMERS = [{"customer": "asha", "segment": "pro"}, {"customer": "ravi", "segment": "free"}, {"customer": "meera", "segment": "pro"},
             {"customer": "dev", "segment": "enterprise"}, {"customer": "lee", "segment": "free"}, {"customer": "kim", "segment": "free"}]


Q(None, "Left Joins and Anti Joins", "Medium", "Polars · join(how=...)",
  "Return <code>(completed revenue per segment sorted by segment, customers with no orders at all sorted)</code>. Revenue per segment needs a join from orders to customers; customers without orders need an <b>anti join</b>.",
  [((ORDERS, CUSTOMERS), ([('enterprise', 2100.0), ('free', 330.0), ('pro', 2070.0)], ['lee']))],
  ("Dict lookups and set differences.", "O(n + c)", "O(c)"),
  ("<code>join(how='left')</code> and <code>join(how='anti')</code>.", "O(n + c)", "O(c)"),
  viz=((ORDERS[:2], CUSTOMERS[:3])))


@B
def segment_join(orders, customers):
    seg = {c["customer"]: c["segment"] for c in customers}
    rev = {}
    for o in orders:
        if o["status"] == "completed":
            s = seg[o["customer"]]
            rev[s] = rev.get(s, 0.0) + o["amount"]
    buyers = {o["customer"] for o in orders}
    return (sorted(rev.items()), sorted(c["customer"] for c in customers if c["customer"] not in buyers))


@O
def segment_join(orders, customers):
    o, c = pl.DataFrame(orders), pl.DataFrame(customers)
    rev = (o.filter(pl.col("status") == "completed").join(c, on="customer", how="left")
            .group_by("segment").agg(pl.col("amount").sum()).sort("segment").rows())
    never = c.join(o, on="customer", how="anti").sort("customer")["customer"].to_list()
    return (rev, never)


SALES = [{"month": "2026-01", "city": "Pune", "revenue": 120.0}, {"month": "2026-01", "city": "Delhi", "revenue": 90.0},
         {"month": "2026-02", "city": "Pune", "revenue": 150.0}, {"month": "2026-02", "city": "Goa", "revenue": 40.0},
         {"month": "2026-03", "city": "Delhi", "revenue": 110.0}, {"month": "2026-03", "city": "Pune", "revenue": 95.0}]


Q(None, "Pivot Long to Wide", "Medium", "Polars · pivot",
  "Turn long sales rows into one row per month with a column per city (missing values → 0.0). Return the column names, then the rows, sorted by month; city columns sorted alphabetically.",
  [((SALES,), (['month', 'Delhi', 'Goa', 'Pune'], [('2026-01', 90.0, 0.0, 120.0), ('2026-02', 0.0, 40.0, 150.0), ('2026-03', 110.0, 0.0, 95.0)]))],
  ("Nested dicts, then build rows.", "O(n + m · c)", "O(m · c)"),
  ("<code>pivot(on='city', index='month', values='revenue')</code>.", "O(n + m · c)", "O(m · c)"),
  viz=((SALES[:3],)))


@B
def pivot_sales(rows):
    cities = sorted({r["city"] for r in rows})
    table = {}
    for r in rows:
        table.setdefault(r["month"], {})[r["city"]] = r["revenue"]
    out = [tuple([m] + [table[m].get(c, 0.0) for c in cities]) for m in sorted(table)]
    return (["month"] + cities, out)


@O
def pivot_sales(rows):
    wide = pl.DataFrame(rows).pivot(on="city", index="month", values="revenue", aggregate_function="sum")
    cities = sorted(c for c in wide.columns if c != "month")
    wide = wide.select("month", *cities).fill_null(0.0).sort("month")
    return (wide.columns, wide.rows())


DAILY = [{"day": f"2026-11-{d:02d}", "orders": n} for d, n in zip(range(1, 11), [12, 15, 9, 22, 30, 28, 11, 14, 19, 25])]


Q(None, "A Rolling Average", "Easy", "Polars · rolling_mean",
  "Return each day's orders and the trailing 3-day average (rounded to 2; None for the first two days, which don't have 3 days yet).",
  [((DAILY,), [('2026-11-01', 12, None), ('2026-11-02', 15, None), ('2026-11-03', 9, 12.0), ('2026-11-04', 22, 15.33), ('2026-11-05', 30, 20.33), ('2026-11-06', 28, 26.67), ('2026-11-07', 11, 23.0), ('2026-11-08', 14, 17.67), ('2026-11-09', 19, 14.67), ('2026-11-10', 25, 19.33)])],
  ("Slice the previous 3 values in a loop.", "O(n · w)", "O(n)"),
  ("<code>pl.col('orders').rolling_mean(window_size=3)</code>.", "O(n)", "O(n)"),
  viz=((DAILY[:4],)))


@B
def rolling_avg(rows):
    out = []
    for i, r in enumerate(rows):
        avg = None if i < 2 else round(sum(x["orders"] for x in rows[i - 2:i + 1]) / 3, 2)
        out.append((r["day"], r["orders"], avg))
    return out


@O
def rolling_avg(rows):
    return pl.DataFrame(rows).with_columns(pl.col("orders").rolling_mean(window_size=3).round(2).alias("avg3")).rows()


USERS = [{"email": "Asha.K@Gmail.com"}, {"email": "ravi@company.in"}, {"email": "meera@gmail.com"}, {"email": " dev@Outlook.com "},
         {"email": "kim@company.in"}, {"email": "not-an-email"}, {"email": "lee@gmail.com"}]


Q(None, "Clean Strings and Extract Parts", "Easy", "Polars · str namespace",
  "Strip spaces, lower-case each email, extract the domain after <code>@</code> with a regex (rows that don't match are dropped), and return <code>(domain, users)</code> sorted by users then domain.",
  [((USERS,), [('gmail.com', 3), ('company.in', 2), ('outlook.com', 1)])],
  ("String methods and a dict.", "O(n)", "O(d)"),
  ("<code>str.strip_chars</code>, <code>str.to_lowercase</code>, <code>str.extract</code>.", "O(n)", "O(d)"),
  viz=((USERS[:3],)))


@B
def email_domains(rows):
    counts = {}
    for r in rows:
        e = r["email"].strip().lower()
        m = re.fullmatch(r"[^@\s]+@([^@\s]+)", e)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))


@O
def email_domains(rows):
    return (pl.DataFrame(rows)
              .with_columns(pl.col("email").str.strip_chars().str.to_lowercase().str.extract(r"^[^@\s]+@([^@\s]+)$", 1).alias("domain"))
              .drop_nulls("domain").group_by("domain").agg(pl.len().alias("users"))
              .sort(["users", "domain"], descending=[True, False]).rows())


READINGS = [{"sensor": "a", "t": 1, "temp": 21.0}, {"sensor": "a", "t": 2, "temp": None}, {"sensor": "a", "t": 3, "temp": None},
            {"sensor": "a", "t": 4, "temp": 23.5}, {"sensor": "b", "t": 1, "temp": None}, {"sensor": "b", "t": 2, "temp": 18.0},
            {"sensor": "b", "t": 3, "temp": None}]


Q(None, "Fill Gaps Per Group", "Medium", "Polars · forward_fill().over()",
  "Sensors miss readings. Forward-fill each sensor's temperature from its own previous reading (never from another sensor); a gap with no earlier reading stays None. Return <code>(nulls before, nulls after, filled rows)</code>.",
  [((READINGS,), (4, 1, [('a', 1, 21.0), ('a', 2, 21.0), ('a', 3, 21.0), ('a', 4, 23.5), ('b', 1, None), ('b', 2, 18.0), ('b', 3, 18.0)]))],
  ("Remember the last value per sensor while looping.", "O(n)", "O(s)"),
  ("<code>pl.col('temp').forward_fill().over('sensor')</code>.", "O(n)", "O(n)"),
  viz=((READINGS[:3],)))


@B
def fill_gaps(rows):
    last, out = {}, []
    for r in sorted(rows, key=lambda r: (r["sensor"], r["t"])):
        v = r["temp"] if r["temp"] is not None else last.get(r["sensor"])
        if r["temp"] is not None:
            last[r["sensor"]] = r["temp"]
        out.append((r["sensor"], r["t"], v))
    before = sum(r["temp"] is None for r in rows)
    return (before, sum(v is None for *_, v in out), out)


@O
def fill_gaps(rows):
    df = pl.DataFrame(rows).sort("sensor", "t")
    filled = df.with_columns(pl.col("temp").forward_fill().over("sensor"))
    return (df["temp"].null_count(), filled["temp"].null_count(), filled.rows())


POSTS = [{"post": 1, "tags": ["python", "pandas"]}, {"post": 2, "tags": ["python", "polars", "speed"]},
         {"post": 3, "tags": []}, {"post": 4, "tags": ["sql", "duckdb", "python"]}, {"post": 5, "tags": ["polars"]}]


Q(None, "Explode Lists Into Rows", "Easy", "Polars · explode",
  "Each post has a list of tags. Return <code>(tag, posts)</code> counts, most used first (ties alphabetical). <code>explode</code> turns one row per post into one row per tag.",
  [((POSTS,), [('python', 3), ('polars', 2), ('duckdb', 1), ('pandas', 1), ('speed', 1), ('sql', 1)])],
  ("Nested loops and a Counter.", "O(t)", "O(u)"),
  ("<code>explode('tags')</code>, then <code>group_by</code>.", "O(t)", "O(u)"),
  viz=((POSTS[:2],)))


@B
def tag_counts(rows):
    c = {}
    for r in rows:
        for t in r["tags"]:
            c[t] = c.get(t, 0) + 1
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))


@O
def tag_counts(rows):
    return (pl.DataFrame(rows).explode("tags").drop_nulls("tags")
              .group_by("tags").agg(pl.len().alias("posts"))
              .sort(["posts", "tags"], descending=[True, False]).rows())


UPDATES = [{"id": 1, "email": "a@x.in", "updated": "2026-11-01"}, {"id": 2, "email": "b@x.in", "updated": "2026-11-02"},
           {"id": 1, "email": "asha@x.in", "updated": "2026-11-05"}, {"id": 3, "email": "c@x.in", "updated": "2026-11-03"},
           {"id": 2, "email": "b@x.in", "updated": "2026-11-02"}, {"id": 1, "email": "asha.k@x.in", "updated": "2026-11-04"}]


Q(None, "Keep the Latest Version of Each Row", "Easy", "Polars · sort + unique",
  "A change feed has several versions per id. Keep each id's row with the latest <code>updated</code> date and return <code>(id, email)</code> sorted by id.",
  [((UPDATES,), [(1, 'asha@x.in'), (2, 'b@x.in'), (3, 'c@x.in')])],
  ("A dict of the newest row per id.", "O(n)", "O(k)"),
  ("<code>sort('updated').unique('id', keep='last')</code>.", "O(n log n)", "O(n)"),
  viz=((UPDATES[:3],)))


@B
def latest_rows(rows):
    best = {}
    for r in rows:
        if r["id"] not in best or r["updated"] > best[r["id"]]["updated"]:
            best[r["id"]] = r
    return sorted((i, r["email"]) for i, r in best.items())


@O
def latest_rows(rows):
    return (pl.DataFrame(rows).sort("updated").unique("id", keep="last", maintain_order=True)
              .select("id", "email").sort("id").rows())


EVENTS = [{"user": "u1", "day": "2026-01-03", "amount": 40.0}, {"user": "u2", "day": "2026-01-10", "amount": 15.0},
          {"user": "u1", "day": "2026-02-01", "amount": 55.0}, {"user": "u3", "day": "2026-02-14", "amount": 90.0},
          {"user": "u2", "day": "2026-02-20", "amount": 25.0}, {"user": "u1", "day": "2026-03-05", "amount": 30.0},
          {"user": "u3", "day": "2026-03-09", "amount": 10.0}, {"user": "u4", "day": "2026-03-21", "amount": 70.0},
          {"user": "u2", "day": "2026-03-28", "amount": 5.0}]


Q(None, "SQL on Your Data With HAVING", "Easy", "DuckDB · GROUP BY … HAVING",
  "With DuckDB, find users who spent more than <code>min_total</code> in total across at least <code>min_orders</code> purchases. Return <code>(user, purchases, total)</code> sorted by total, highest first.",
  [((EVENTS, 60.0, 2), [('u1', 3, 125.0), ('u3', 2, 100.0)])],
  ("Dicts of counts and totals.", "O(n log u)", "O(u)"),
  ("One SQL query with HAVING.", "O(n log u)", "O(u)"),
  viz=((EVENTS[:3], 10.0, 1)))


@B
def big_spenders(rows, min_total, min_orders):
    s = {}
    for r in rows:
        s.setdefault(r["user"], [0, 0.0])
        s[r["user"]][0] += 1
        s[r["user"]][1] += r["amount"]
    out = [(u, n, t) for u, (n, t) in s.items() if t > min_total and n >= min_orders]
    return sorted(out, key=lambda x: -x[2])


@O
def big_spenders(rows, min_total, min_orders):
    con = duckdb.connect()
    sql_table(con, "events", rows)
    return con.execute("""
        SELECT "user", COUNT(*) AS purchases, SUM(amount) AS total
        FROM events GROUP BY "user"
        HAVING SUM(amount) > ? AND COUNT(*) >= ?
        ORDER BY total DESC""", [min_total, min_orders]).fetchall()


Q(None, "Running Totals and Month-Over-Month", "Medium", "DuckDB · window functions, LAG",
  "Return per month <code>(month 'YYYY-MM', revenue, running total, growth % vs the previous month rounded to 1 — None for the first month)</code>.",
  [((EVENTS,), [('2026-01', 55.0, 55.0, None), ('2026-02', 170.0, 225.0, 209.1), ('2026-03', 115.0, 340.0, -32.4)])],
  ("Sum per month, then walk the sorted months.", "O(n + m log m)", "O(m)"),
  ("<code>SUM() OVER (ORDER BY …)</code> and <code>LAG()</code>.", "O(n + m log m)", "O(m)"),
  viz=((EVENTS[:4],)))


@B
def monthly_growth(rows):
    m = {}
    for r in rows:
        m[r["day"][:7]] = m.get(r["day"][:7], 0.0) + r["amount"]
    out, running, prev = [], 0.0, None
    for month in sorted(m):
        running += m[month]
        growth = None if prev is None else round((m[month] / prev - 1) * 100, 1)
        out.append((month, m[month], running, growth))
        prev = m[month]
    return out


@O
def monthly_growth(rows):
    con = duckdb.connect()
    sql_table(con, "events", rows)
    return con.execute("""
        WITH m AS (SELECT substr(day, 1, 7) AS month, SUM(amount) AS revenue FROM events GROUP BY 1)
        SELECT month, revenue,
               SUM(revenue) OVER (ORDER BY month) AS running,
               ROUND((revenue / LAG(revenue) OVER (ORDER BY month) - 1) * 100, 1) AS growth
        FROM m ORDER BY month""").fetchall()


Q(None, "Top Row per Group With QUALIFY", "Medium", "DuckDB · QUALIFY",
  "For each user, return their single largest purchase <code>(user, day, amount)</code> (ties: earliest day), sorted by user. DuckDB's <code>QUALIFY</code> filters on a window function without a subquery.",
  [((EVENTS,), [('u1', '2026-02-01', 55.0), ('u2', '2026-02-20', 25.0), ('u3', '2026-02-14', 90.0), ('u4', '2026-03-21', 70.0)])],
  ("Keep the best row per user in a dict.", "O(n)", "O(u)"),
  ("<code>QUALIFY ROW_NUMBER() OVER (PARTITION BY … ORDER BY …) = 1</code>.", "O(n log n)", "O(n)"),
  viz=((EVENTS[:3],)))


@B
def biggest_purchase(rows):
    best = {}
    for r in rows:
        b = best.get(r["user"])
        if b is None or r["amount"] > b["amount"] or (r["amount"] == b["amount"] and r["day"] < b["day"]):
            best[r["user"]] = r
    return [(u, best[u]["day"], best[u]["amount"]) for u in sorted(best)]


@O
def biggest_purchase(rows):
    con = duckdb.connect()
    sql_table(con, "events", rows)
    return con.execute("""
        SELECT "user", day, amount FROM events
        QUALIFY ROW_NUMBER() OVER (PARTITION BY "user" ORDER BY amount DESC, day) = 1
        ORDER BY "user" """).fetchall()


Q(None, "Conditional Counts With FILTER", "Easy", "DuckDB · aggregate FILTER",
  "Using the orders, return per city <code>(city, completed, cancelled_or_returned, completion % rounded to 1)</code> sorted by city, with <code>COUNT(*) FILTER (WHERE …)</code>.",
  [((ORDERS,), [('Delhi', 1, 2, 33.3), ('Goa', 1, 0, 100.0), ('Pune', 4, 0, 100.0)])],
  ("Two counting dicts.", "O(n log c)", "O(c)"),
  ("FILTER clauses in one GROUP BY.", "O(n log c)", "O(c)"),
  viz=((ORDERS[:3],)))


@B
def completion(rows):
    s = {}
    for r in rows:
        s.setdefault(r["city"], [0, 0])
        if r["status"] == "completed":
            s[r["city"]][0] += 1
        else:
            s[r["city"]][1] += 1
    return [(c, a, b, round(a / (a + b) * 100, 1)) for c, (a, b) in sorted(s.items())]


@O
def completion(rows):
    con = duckdb.connect()
    sql_table(con, "orders", rows)
    return con.execute("""
        SELECT city,
               COUNT(*) FILTER (WHERE status = 'completed') AS completed,
               COUNT(*) FILTER (WHERE status <> 'completed') AS other,
               ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'completed') / COUNT(*), 1) AS pct
        FROM orders GROUP BY city ORDER BY city""").fetchall()


TRADES = [{"t": 3, "symbol": "INFY", "qty": 10}, {"t": 7, "symbol": "TCS", "qty": 5}, {"t": 9, "symbol": "INFY", "qty": 20},
          {"t": 15, "symbol": "INFY", "qty": 5}, {"t": 16, "symbol": "TCS", "qty": 8}, {"t": 1, "symbol": "TCS", "qty": 2}]
QUOTES = [{"t": 0, "symbol": "INFY", "price": 1500.0}, {"t": 5, "symbol": "INFY", "price": 1510.0}, {"t": 12, "symbol": "INFY", "price": 1495.0},
          {"t": 2, "symbol": "TCS", "price": 3900.0}, {"t": 10, "symbol": "TCS", "price": 3925.0}]


Q(None, "Match Each Trade to the Latest Quote", "Medium", "DuckDB · ASOF JOIN",
  "For each trade, find the most recent quote for the same symbol at or before the trade time, and return <code>(t, symbol, qty, price, value = qty × price)</code> sorted by time; a trade before any quote is dropped. This 'as of' join is common for time-series and finance data.",
  [((TRADES, QUOTES), [(3, 'INFY', 10, 1500.0, 15000.0), (7, 'TCS', 5, 3900.0, 19500.0), (9, 'INFY', 20, 1510.0, 30200.0), (15, 'INFY', 5, 1495.0, 7475.0), (16, 'TCS', 8, 3925.0, 31400.0)])],
  ("For each trade, scan the quotes.", "O(t · q)", "O(1)"),
  ("<code>ASOF JOIN … ON symbol AND trades.t &gt;= quotes.t</code>.", "O((t + q) log q)", "O(q)"),
  viz=((TRADES[:2], QUOTES[:2])))


@B
def asof_prices(trades, quotes):
    out = []
    for tr in trades:
        best = None
        for q in quotes:
            if q["symbol"] == tr["symbol"] and q["t"] <= tr["t"] and (best is None or q["t"] > best["t"]):
                best = q
        if best:
            out.append((tr["t"], tr["symbol"], tr["qty"], best["price"], tr["qty"] * best["price"]))
    return sorted(out)


@O
def asof_prices(trades, quotes):
    con = duckdb.connect()
    sql_table(con, "trades", trades)
    sql_table(con, "quotes", quotes)
    return con.execute("""
        SELECT tr.t, tr.symbol, tr.qty, q.price, tr.qty * q.price AS value
        FROM trades tr ASOF JOIN quotes q ON tr.symbol = q.symbol AND tr.t >= q.t
        ORDER BY tr.t""").fetchall()


Q(None, "Collect Values Into Lists", "Easy", "DuckDB · list and string aggregates",
  "Return per user <code>(user, days they bought as a sorted list, amounts joined into one string like '40.0|55.0|30.0' in date order)</code>, sorted by user — with <code>list(… ORDER BY …)</code> and <code>string_agg</code>.",
  [((EVENTS,), [('u1', ['2026-01-03', '2026-02-01', '2026-03-05'], '40.0|55.0|30.0'), ('u2', ['2026-01-10', '2026-02-20', '2026-03-28'], '15.0|25.0|5.0'), ('u3', ['2026-02-14', '2026-03-09'], '90.0|10.0'), ('u4', ['2026-03-21'], '70.0')])],
  ("A dict of lists, sorted afterwards.", "O(n log n)", "O(n)"),
  ("<code>list(day ORDER BY day)</code> and <code>string_agg(…, '|' ORDER BY day)</code>.", "O(n log n)", "O(n)"),
  viz=((EVENTS[:3],)))


@B
def user_lists(rows):
    g = {}
    for r in sorted(rows, key=lambda r: r["day"]):
        g.setdefault(r["user"], []).append(r)
    return [(u, [r["day"] for r in rs], "|".join(str(r["amount"]) for r in rs)) for u, rs in sorted(g.items())]


@O
def user_lists(rows):
    con = duckdb.connect()
    sql_table(con, "events", rows)
    return con.execute("""
        SELECT "user", list(day ORDER BY day), string_agg(CAST(amount AS VARCHAR), '|' ORDER BY day)
        FROM events GROUP BY "user" ORDER BY "user" """).fetchall()


Q(None, "Fill Missing Days With Zero", "Medium", "DuckDB · generate_series + LEFT JOIN",
  "Purchases only exist on some days. Return <code>(day 'YYYY-MM-DD', purchases, revenue)</code> for <b>every</b> day from <code>start</code> to <code>end</code> inclusive, with 0 and 0.0 on days without purchases — charts and moving averages break on missing days.",
  [((EVENTS, "2026-03-03", "2026-03-10"), [('2026-03-03', 0, 0.0), ('2026-03-04', 0, 0.0), ('2026-03-05', 1, 30.0), ('2026-03-06', 0, 0.0), ('2026-03-07', 0, 0.0), ('2026-03-08', 0, 0.0), ('2026-03-09', 1, 10.0), ('2026-03-10', 0, 0.0)])],
  ("Walk the dates with timedelta and look up a dict.", "O(d + n)", "O(d)"),
  ("<code>generate_series</code> of dates LEFT JOIN the daily totals.", "O(d + n)", "O(d)"),
  viz=((EVENTS[5:7], "2026-03-04", "2026-03-06")))


@B
def daily_filled(rows, start, end):
    totals = {}
    for r in rows:
        n, s = totals.get(r["day"], (0, 0.0))
        totals[r["day"]] = (n + 1, s + r["amount"])
    out, d = [], date.fromisoformat(start)
    while d <= date.fromisoformat(end):
        n, s = totals.get(d.isoformat(), (0, 0.0))
        out.append((d.isoformat(), n, s))
        d += timedelta(days=1)
    return out


@O
def daily_filled(rows, start, end):
    con = duckdb.connect()
    sql_table(con, "events", rows)
    return con.execute("""
        WITH days AS (SELECT CAST(d AS DATE) AS day
                      FROM generate_series(CAST(? AS DATE), CAST(? AS DATE), INTERVAL 1 DAY) AS g(d)),
             t AS (SELECT CAST(day AS DATE) AS day, COUNT(*) AS n, SUM(amount) AS s FROM events GROUP BY 1)
        SELECT CAST(days.day AS VARCHAR), COALESCE(t.n, 0), COALESCE(t.s, 0.0)
        FROM days LEFT JOIN t USING (day) ORDER BY days.day""", [start, end]).fetchall()


Q(None, "Run SQL on a pandas DataFrame", "Easy", "DuckDB · query DataFrames in place",
  "DuckDB can query a pandas DataFrame directly, without copying it into a database. Build a DataFrame from the orders, register it, and return each customer's completed revenue and share of the total (% rounded to 1) with <code>SUM(...) OVER ()</code>, as <code>(customer, revenue, share)</code> sorted by revenue, highest first.",
  [((ORDERS,), [('dev', 2100.0, 46.7), ('asha', 1840.0, 40.9), ('ravi', 330.0, 7.3), ('meera', 230.0, 5.1)])],
  ("Two passes with a dict.", "O(n + c log c)", "O(c)"),
  ("<code>con.register('orders', df)</code> and a window over the whole result.", "O(n + c log c)", "O(c)"),
  viz=((ORDERS[:4],)))


@B
def revenue_share(rows):
    rev = {}
    for r in rows:
        if r["status"] == "completed":
            rev[r["customer"]] = rev.get(r["customer"], 0.0) + r["amount"]
    total = sum(rev.values())
    return sorted(((c, v, round(v / total * 100, 1)) for c, v in rev.items()), key=lambda x: (-x[1], x[0]))


@O
def revenue_share(rows):
    df = pd.DataFrame(rows)
    con = duckdb.connect()
    con.register("orders", df)
    return con.execute("""
        SELECT customer, SUM(amount) AS revenue, ROUND(100 * SUM(amount) / SUM(SUM(amount)) OVER (), 1) AS share
        FROM orders WHERE status = 'completed'
        GROUP BY customer ORDER BY revenue DESC, customer""").fetchall()
