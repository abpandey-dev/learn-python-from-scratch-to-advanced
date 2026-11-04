from lib import *
import pandas as pd

TOPIC(
    id="pandas-grouping", title="Grouping, Merging & Reshaping", glyph="groupby",
    blurb="Split-apply-combine with groupby, joining tables with merge and concat, pivot tables, melt and time-based windows.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">df.groupby("region")["amount"].sum()
df.groupby("region").agg(total=("amount", "sum"), avg=("amount", "mean"))
df.groupby(["region", "month"]).size()
df["share"] = df["amount"] / df.groupby("region")["amount"].transform("sum")
pd.merge(left, right, on="id", how="inner" | "left" | "right" | "outer")
pd.concat([df1, df2], ignore_index=True)
df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0)
df.melt(id_vars="name", var_name="subject", value_name="mark")
pd.crosstab(df["a"], df["b"])
s.rolling(3).mean(), df.resample("ME", on="date")["amount"].sum()</code></pre>
""")

SALES = {"region": ["North", "South", "North", "East", "South", "North"],
         "product": ["pen", "pen", "ink", "pen", "ink", "pen"],
         "month": ["Jan", "Jan", "Feb", "Feb", "Feb", "Mar"],
         "amount": [100, 80, 40, 60, 120, 70]}


Q(None, "Total per Group", "Easy", "groupby + sum",
  "Return the total amount for each region, as {region: total} sorted by region name.",
  [((SALES,), {"East": 60, "North": 210, "South": 200})],
  ("Accumulate totals in a dict, then sort the keys.", "O(n)", "O(k)"),
  ("<code>df.groupby('region')['amount'].sum()</code> — split, apply sum, combine.", "O(n)", "O(k)"),
  viz=(SALES,))


@B
def region_totals(data):
    totals = {}
    for r, a in zip(data["region"], data["amount"]):
        totals[r] = totals.get(r, 0) + a
    return dict(sorted(totals.items()))


@O
def region_totals(data):
    df = pd.DataFrame(data)
    return df.groupby("region")["amount"].sum()


Q(None, "Average per Group", "Easy", "groupby + mean",
  "Return the average amount per product, rounded to 2 decimals.",
  [((SALES,), {"ink": 80.0, "pen": 77.5})],
  ("Keep a sum and a count per product.", "O(n)", "O(k)"),
  ("<code>df.groupby('product')['amount'].mean()</code>.", "O(n)", "O(k)"))


@B
def product_avg(data):
    sums, counts = {}, {}
    for p, a in zip(data["product"], data["amount"]):
        sums[p] = sums.get(p, 0) + a
        counts[p] = counts.get(p, 0) + 1
    return {p: round(sums[p] / counts[p], 2) for p in sorted(sums)}


@O
def product_avg(data):
    return pd.DataFrame(data).groupby("product")["amount"].mean().round(2)


Q(None, "Rows per Group", "Easy", "groupby + size",
  "Return how many sales each region has.",
  [((SALES,), {"East": 1, "North": 3, "South": 2})],
  ("Count in a dict.", "O(n)", "O(k)"),
  ("<code>df.groupby('region').size()</code>.", "O(n)", "O(k)"))


@B
def rows_per_region(data):
    counts = {}
    for r in data["region"]:
        counts[r] = counts.get(r, 0) + 1
    return dict(sorted(counts.items()))


@O
def rows_per_region(data):
    return pd.DataFrame(data).groupby("region").size()


Q(None, "Several Statistics at Once", "Medium", "agg with named outputs",
  "Per region, return total, average (2 decimals) and largest amount as {'total': {...}, 'avg': {...}, 'max': {...}}.",
  [((SALES,), {"total": [60, 210, 200], "avg": [60.0, 70.0, 100.0], "max": [60, 100, 120]})],
  ("Group values into lists per region, then compute each statistic.", "O(n)", "O(n)"),
  ("Named aggregation: <code>agg(total=('amount', 'sum'), …)</code>.", "O(n)", "O(k)"),
  viz=(SALES,))


@B
def region_stats(data):
    groups = {}
    for r, a in zip(data["region"], data["amount"]):
        groups.setdefault(r, []).append(a)
    regions = sorted(groups)
    return {"total": [sum(groups[r]) for r in regions],
            "avg": [round(sum(groups[r]) / len(groups[r]), 2) for r in regions],
            "max": [max(groups[r]) for r in regions]}


@O
def region_stats(data):
    df = pd.DataFrame(data)
    stats = df.groupby("region").agg(total=("amount", "sum"), avg=("amount", "mean"), max=("amount", "max"))
    return stats.round(2)


Q(None, "Best Product per Region", "Medium", "idxmax within groups",
  "For each region, return the product with the highest total amount.",
  [((SALES,), {"East": "pen", "North": "pen", "South": "ink"})],
  ("Nested dicts of totals, then pick the max per region.", "O(n)", "O(n)"),
  ("Group by both, sum, then <code>idxmax</code> per region.", "O(n log n)", "O(n)"),
  viz=(SALES,))


@B
def best_product(data):
    totals = {}
    for r, p, a in zip(data["region"], data["product"], data["amount"]):
        totals.setdefault(r, {})
        totals[r][p] = totals[r].get(p, 0) + a
    return {r: max(totals[r], key=totals[r].get) for r in sorted(totals)}


@O
def best_product(data):
    df = pd.DataFrame(data)
    totals = df.groupby(["region", "product"])["amount"].sum().reset_index()
    best = totals.loc[totals.groupby("region")["amount"].idxmax()]
    return dict(zip(best["region"], best["product"]))


Q(None, "Join Customers and Orders", "Medium", "merge (inner)",
  "Return (customer name, order amount) for every order whose customer id exists.",
  [(({"id": [1, 2, 3], "name": ["Ana", "Ben", "Cy"]}, {"cust": [2, 1, 2, 9], "amount": [50, 30, 20, 99]}), [("Ben", 50), ("Ana", 30), ("Ben", 20)])],
  ("Build an id → name dict, then loop over orders.", "O(n + m)", "O(n)"),
  ("<code>pd.merge(orders, customers, left_on='cust', right_on='id')</code> — an inner join keeps only matches.", "O(n + m)", "O(n + m)"),
  viz=({"id": [1, 2, 3], "name": ["Ana", "Ben", "Cy"]}, {"cust": [2, 1, 2, 9], "amount": [50, 30, 20, 99]}))


@B
def join_orders(customers, orders):
    names = dict(zip(customers["id"], customers["name"]))
    out = []
    for c, a in zip(orders["cust"], orders["amount"]):
        if c in names:
            out.append((names[c], a))
    return out


@O
def join_orders(customers, orders):
    merged = pd.merge(pd.DataFrame(orders), pd.DataFrame(customers), left_on="cust", right_on="id", how="inner", sort=False)
    return list(zip(merged["name"], merged["amount"]))


Q(None, "Customers With Their Spending", "Medium", "left join + fillna",
  "Return {name: total spent} for every customer, including those with no orders (0).",
  [(({"id": [1, 2, 3], "name": ["Ana", "Ben", "Cy"]}, {"cust": [2, 1, 2], "amount": [50, 30, 20]}), {"Ana": 30, "Ben": 70, "Cy": 0})],
  ("Sum orders per id, then look up every customer with a default of 0.", "O(n + m)", "O(n)"),
  ("Group the orders, then a <b>left</b> merge keeps every customer; fill the gaps with 0.", "O(n + m)", "O(n)"))


@B
def spending(customers, orders):
    spent = {}
    for c, a in zip(orders["cust"], orders["amount"]):
        spent[c] = spent.get(c, 0) + a
    return {name: spent.get(i, 0) for i, name in zip(customers["id"], customers["name"])}


@O
def spending(customers, orders):
    totals = pd.DataFrame(orders).groupby("cust", as_index=False)["amount"].sum()
    merged = pd.DataFrame(customers).merge(totals, left_on="id", right_on="cust", how="left")
    merged["amount"] = merged["amount"].fillna(0).astype(int)
    return dict(zip(merged["name"], merged["amount"]))


Q(None, "Stack Two Tables", "Easy", "concat",
  "Combine two tables with the same columns, one under the other, and return the names.",
  [(({"name": ["Ana", "Ben"]}, {"name": ["Cy"]}), ["Ana", "Ben", "Cy"])],
  ("List concatenation of each column.", "O(n + m)", "O(n + m)"),
  ("<code>pd.concat([a, b], ignore_index=True)</code>.", "O(n + m)", "O(n + m)"))


@B
def stack_tables(a, b):
    return list(a["name"]) + list(b["name"])


@O
def stack_tables(a, b):
    both = pd.concat([pd.DataFrame(a), pd.DataFrame(b)], ignore_index=True)
    return both["name"].tolist()


Q(None, "Pivot Table", "Medium", "pivot_table",
  "Return a region × month table of total amounts (missing combinations = 0), regions sorted, months in Jan, Feb, Mar order.",
  [((SALES,), {"Jan": [0, 100, 80], "Feb": [60, 40, 120], "Mar": [0, 70, 0]})],
  ("Nested dict totals[region][month], then build columns by hand.", "O(n + R·M)", "O(R·M)"),
  ("<code>df.pivot_table(index='region', columns='month', values='amount', aggfunc='sum', fill_value=0)</code>.", "O(n log n)", "O(R·M)"),
  viz=(SALES,))


@B
def pivot(data):
    months = ["Jan", "Feb", "Mar"]
    regions = sorted(set(data["region"]))
    totals = {}
    for r, m, a in zip(data["region"], data["month"], data["amount"]):
        totals[(r, m)] = totals.get((r, m), 0) + a
    return {m: [totals.get((r, m), 0) for r in regions] for m in months}


@O
def pivot(data):
    df = pd.DataFrame(data)
    table = df.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0)
    return table[["Jan", "Feb", "Mar"]]


Q(None, "Wide to Long (melt)", "Medium", "melt",
  "Turn one column per subject into rows of (name, subject, mark), ordered by subject then name.",
  [(({"name": ["Ana", "Ben"], "maths": [90, 60], "art": [70, 85]},), [("Ana", "maths", 90), ("Ben", "maths", 60), ("Ana", "art", 70), ("Ben", "art", 85)])],
  ("Loop over subject columns, then over rows.", "O(n·s)", "O(n·s)"),
  ("<code>df.melt(id_vars='name', var_name='subject', value_name='mark')</code>.", "O(n·s)", "O(n·s)"),
  viz=({"name": ["Ana", "Ben"], "maths": [90, 60], "art": [70, 85]},))


@B
def to_long(data):
    out = []
    for subject in [c for c in data if c != "name"]:
        for name, mark in zip(data["name"], data[subject]):
            out.append((name, subject, mark))
    return out


@O
def to_long(data):
    long = pd.DataFrame(data).melt(id_vars="name", var_name="subject", value_name="mark")
    return list(long.itertuples(index=False, name=None))


Q(None, "Cross Tabulation", "Medium", "crosstab",
  "Count sales for each (region, product) pair; return {product: [counts in sorted region order]}.",
  [((SALES,), {"ink": [0, 1, 1], "pen": [1, 2, 1]})],
  ("Count pairs in a dict, then lay them out.", "O(n)", "O(R·P)"),
  ("<code>pd.crosstab(df['region'], df['product'])</code>.", "O(n)", "O(R·P)"))


@B
def crosstab(data):
    regions, products = sorted(set(data["region"])), sorted(set(data["product"]))
    counts = {}
    for r, p in zip(data["region"], data["product"]):
        counts[(r, p)] = counts.get((r, p), 0) + 1
    return {p: [counts.get((r, p), 0) for r in regions] for p in products}


@O
def crosstab(data):
    df = pd.DataFrame(data)
    return pd.crosstab(df["region"], df["product"])


Q(None, "Share of Group Total", "Medium", "transform",
  "For each sale, return its percentage of its region's total (rounded to 1 decimal).",
  [((SALES,), [47.6, 40.0, 19.0, 100.0, 60.0, 33.3])],
  ("Compute region totals in one pass, then divide in a second pass.", "O(n)", "O(k)"),
  ("<code>groupby(...).transform('sum')</code> returns the group total aligned to every row.", "O(n)", "O(n)"),
  viz=(SALES,))


@B
def shares(data):
    totals = {}
    for r, a in zip(data["region"], data["amount"]):
        totals[r] = totals.get(r, 0) + a
    return [round(a / totals[r] * 100, 1) for r, a in zip(data["region"], data["amount"])]


@O
def shares(data):
    df = pd.DataFrame(data)
    group_total = df.groupby("region")["amount"].transform("sum")
    return (df["amount"] / group_total * 100).round(1).tolist()


Q(None, "Rank Within Group", "Medium", "groupby + rank",
  "Rank each sale within its region by amount (1 = largest).",
  [((SALES,), [1, 2, 3, 1, 1, 2])],
  ("For each row, count bigger amounts in the same region.", "O(n²)", "O(n)"),
  ("<code>df.groupby('region')['amount'].rank(ascending=False, method='min')</code>.", "O(n log n)", "O(n)"))


@B
def ranks(data):
    out = []
    for r, a in zip(data["region"], data["amount"]):
        bigger = sum(1 for r2, a2 in zip(data["region"], data["amount"]) if r2 == r and a2 > a)
        out.append(bigger + 1)
    return out


@O
def ranks(data):
    df = pd.DataFrame(data)
    return df.groupby("region")["amount"].rank(ascending=False, method="min").astype(int).tolist()


Q(None, "Running Total per Group", "Medium", "groupby + cumsum",
  "Return each region's running total in row order.",
  [((SALES,), [100, 80, 140, 60, 200, 210])],
  ("Keep a running total per region in a dict.", "O(n)", "O(k)"),
  ("<code>df.groupby('region')['amount'].cumsum()</code>.", "O(n)", "O(n)"),
  viz=(SALES,))


@B
def running_by_region(data):
    running, out = {}, []
    for r, a in zip(data["region"], data["amount"]):
        running[r] = running.get(r, 0) + a
        out.append(running[r])
    return out


@O
def running_by_region(data):
    return pd.DataFrame(data).groupby("region")["amount"].cumsum().tolist()


Q(None, "Monthly Totals From Daily Data", "Medium", "Group by month",
  "Given daily dates and amounts, return totals per month as {'YYYY-MM': total}.",
  [(({"date": ["2024-01-05", "2024-01-20", "2024-02-02", "2024-03-15", "2024-03-16"], "amount": [10, 15, 7, 3, 4]},), {"2024-01": 25, "2024-02": 7, "2024-03": 7})],
  ("Slice the 'YYYY-MM' part of each date string and sum in a dict.", "O(n)", "O(k)"),
  ("Parse dates, convert to monthly periods and group: <code>groupby(d.dt.to_period('M'))</code>.", "O(n)", "O(k)"),
  viz=({"date": ["2024-01-05", "2024-01-20", "2024-02-02"], "amount": [10, 15, 7]},))


@B
def monthly(data):
    totals = {}
    for d, a in zip(data["date"], data["amount"]):
        totals[d[:7]] = totals.get(d[:7], 0) + a
    return totals


@O
def monthly(data):
    df = pd.DataFrame(data)
    month = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return df.groupby(month)["amount"].sum()


Q(None, "Rolling 3-Day Average", "Medium", "rolling",
  "Return the 3-day rolling average (the first two days are None), rounded to 1 decimal.",
  [(({"sales": [10, 20, 30, 40, 50]},), [None, None, 20.0, 30.0, 40.0])],
  ("Average the last 3 values for each position from index 2.", "O(n·k)", "O(n)"),
  ("<code>s.rolling(3).mean()</code>.", "O(n)", "O(n)"),
  viz=({"sales": [10, 20, 30, 40, 50]},))


@B
def rolling3(data):
    s = data["sales"]
    out = []
    for i in range(len(s)):
        out.append(None if i < 2 else round(sum(s[i - 2:i + 1]) / 3, 1))
    return out


@O
def rolling3(data):
    return pd.DataFrame(data)["sales"].rolling(3).mean().round(1).tolist()


Q(None, "Groups From Two Keys to a Table", "Medium", "unstack",
  "Group by region and product, sum the amounts, and spread products into columns (missing = 0).",
  [((SALES,), {"ink": [0, 40, 120], "pen": [60, 170, 80]})],
  ("Nested dict of totals laid out by hand.", "O(n)", "O(R·P)"),
  ("<code>groupby(['region', 'product']).sum().unstack(fill_value=0)</code>.", "O(n log n)", "O(R·P)"))


@B
def region_product(data):
    regions, products = sorted(set(data["region"])), sorted(set(data["product"]))
    totals = {}
    for r, p, a in zip(data["region"], data["product"], data["amount"]):
        totals[(r, p)] = totals.get((r, p), 0) + a
    return {p: [totals.get((r, p), 0) for r in regions] for p in products}


@O
def region_product(data):
    df = pd.DataFrame(data)
    return df.groupby(["region", "product"])["amount"].sum().unstack(fill_value=0)


Q(None, "Keep Big Groups Only", "Medium", "groupby + filter",
  "Return the amounts from regions that have at least <code>k</code> sales.",
  [((SALES, 2), [100, 80, 40, 120, 70]), ((SALES, 3), [100, 40, 70])],
  ("Count per region first, then filter the rows.", "O(n)", "O(k)"),
  ("<code>df.groupby('region').filter(lambda g: len(g) &gt;= k)</code>.", "O(n)", "O(n)"))


@B
def big_groups(data, k):
    counts = {}
    for r in data["region"]:
        counts[r] = counts.get(r, 0) + 1
    return [a for r, a in zip(data["region"], data["amount"]) if counts[r] >= k]


@O
def big_groups(data, k):
    df = pd.DataFrame(data)
    return df.groupby("region").filter(lambda g: len(g) >= k)["amount"].tolist()


Q(None, "Customers Without Orders", "Medium", "Anti-join",
  "Return the names of customers who never ordered.",
  [(({"id": [1, 2, 3, 4], "name": ["Ana", "Ben", "Cy", "Dia"]}, {"cust": [2, 2, 4]}), ["Ana", "Cy"])],
  ("Put ordering ids in a set and keep the others.", "O(n + m)", "O(m)"),
  ("Filter with <code>~customers['id'].isin(orders['cust'])</code> (or a left merge with <code>indicator=True</code>).", "O(n + m)", "O(n)"))


@B
def no_orders(customers, orders):
    ordered = set(orders["cust"])
    return [n for i, n in zip(customers["id"], customers["name"]) if i not in ordered]


@O
def no_orders(customers, orders):
    c = pd.DataFrame(customers)
    return c.loc[~c["id"].isin(orders["cust"]), "name"].tolist()


Q(None, "First and Last per Group", "Easy", "groupby + first / last",
  "For each region, return (first amount, last amount) in row order.",
  [((SALES,), {"East": (60, 60), "North": (100, 70), "South": (80, 120)})],
  ("Track the first and latest value per region in a dict.", "O(n)", "O(k)"),
  ("<code>groupby('region')['amount'].agg(['first', 'last'])</code>.", "O(n)", "O(k)"))


@B
def first_last(data):
    out = {}
    for r, a in zip(data["region"], data["amount"]):
        if r not in out:
            out[r] = [a, a]
        out[r][1] = a
    return {r: tuple(out[r]) for r in sorted(out)}


@O
def first_last(data):
    fl = pd.DataFrame(data).groupby("region")["amount"].agg(["first", "last"])
    return {r: (row["first"], row["last"]) for r, row in fl.iterrows()}
