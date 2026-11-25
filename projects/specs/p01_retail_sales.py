import numpy as np
import pandas as pd


def make_data(rng):
    n_cust = 600
    seg = rng.choice(["Consumer", "Corporate", "Small Business"], n_cust, p=[0.6, 0.25, 0.15])
    region = rng.choice(["North", "South", "East", "West"], n_cust, p=[0.3, 0.3, 0.2, 0.2])
    signup = pd.to_datetime("2024-06-01") + pd.to_timedelta(rng.integers(0, 540, n_cust), unit="D")
    customers = pd.DataFrame({"customer_id": [f"C{i:04d}" for i in range(n_cust)], "segment": seg,
                              "region": region, "signup_date": signup.strftime("%Y-%m-%d")})
    cats = ["Electronics", "Home", "Fashion", "Grocery", "Beauty"]
    price = {"Electronics": 2400, "Home": 900, "Fashion": 700, "Grocery": 180, "Beauty": 350}
    days = pd.date_range("2025-01-01", "2026-06-30", freq="D")
    rows, oid = [], 100000
    weight = np.where(seg == "Corporate", 3.0, np.where(seg == "Small Business", 2.0, 1.0))
    weight = weight * rng.pareto(2.5, n_cust) + 0.05
    weight = weight / weight.sum()
    for d in days:
        season = 1.0 + 0.6 * (d.month in (10, 11)) + 0.9 * (d.month == 12) - 0.15 * (d.month in (2, 6))
        trend = 1.0 + 0.02 * ((d.year - 2025) * 12 + d.month - 1)
        n = rng.poisson(9 * season * trend)
        for _ in range(n):
            c = rng.choice(n_cust, p=weight)
            cat = rng.choice(cats, p=[0.18, 0.2, 0.24, 0.26, 0.12])
            units = int(rng.integers(1, 6 if cat == "Grocery" else 3))
            unit_price = round(price[cat] * rng.uniform(0.6, 1.5), 2)
            disc = rng.choice([0, 0.05, 0.1, 0.2], p=[0.55, 0.2, 0.15, 0.1])
            rows.append((f"O{oid}", d.strftime("%Y-%m-%d"), customers.customer_id[c], cat, units, unit_price, disc,
                         int(rng.random() < (0.09 if cat == "Fashion" else 0.03))))
            oid += 1
    orders = pd.DataFrame(rows, columns=["order_id", "order_date", "customer_id", "category", "units",
                                         "unit_price", "discount", "returned"])
    dup = orders.sample(40, random_state=1)
    orders = pd.concat([orders, dup]).sort_values(["order_date", "order_id"]).reset_index(drop=True)
    return {"retail_orders.csv": orders, "retail_customers.csv": customers}


PROJECT = dict(
    slug="retail-sales-analysis",
    title="Retail Sales Analysis & Forecast",
    role="Data Analyst",
    level="Beginner–Intermediate",
    hours="6–8",
    summary="An online retailer's head of sales wants to know where revenue comes from, who the best customers are, whether new customers come back, and what the next quarter looks like.",
    skills=["pandas", "data cleaning", "KPIs", "SQL (sqlite3)", "Pareto analysis", "cohort retention", "forecasting", "storytelling"],
    brief="""
**The situation.** You've joined the analytics team of *ShopKart*, an online retailer selling electronics, home goods, fashion, groceries and beauty products across four regions. The head of sales has a quarterly review next week and asks you:

1. How big is the business right now, and is it growing?
2. Which regions and customer segments bring in the money?
3. How dependent are we on a few big customers?
4. Do new customers come back the next month?
5. What revenue should we plan for over the next three months?

The raw export from the order system is messy: it has duplicate rows and returned orders mixed in.
""",
    deliverable="a cleaned dataset, a KPI summary, a regional breakdown from SQL, a Pareto and retention analysis, a 3-month forecast with the method you chose and why, and a one-page summary for the head of sales.",
    data_notes="""
Two files, 18 months of orders (Jan 2025 – Jun 2026):

**retail_orders.csv** — one row per order line

| Column | Meaning |
|---|---|
| order_id | order number (the export has some **duplicate rows**) |
| order_date | date, as text `YYYY-MM-DD` |
| customer_id | who ordered |
| category | product category |
| units, unit_price | quantity and price per unit (₹) |
| discount | share taken off, e.g. 0.1 = 10% |
| returned | 1 if the order was returned and refunded |

**retail_customers.csv** — customer_id, segment (Consumer / Corporate / Small Business), region, signup_date
""",
    setup="""
import sqlite3
import matplotlib.pyplot as plt
orders = load("retail_orders.csv")
customers = load("retail_customers.csv")
print(orders.shape, customers.shape)
""",
    explore=[("Take a first look before you start. What does one row mean? Which columns need fixing?",
              "display(orders.head())\nprint(orders.dtypes)\nprint('duplicate order ids:', orders.order_id.duplicated().sum())")],
    milestones=[
        dict(title="Clean the orders",
             task="""
Write `clean(orders)` that returns a **new** DataFrame where:
- duplicate rows are removed (keep the first row for each `order_id`),
- `order_date` is a real datetime,
- a `revenue` column = units × unit_price × (1 − discount), rounded to 2 decimals,
- **returned orders are removed** (they were refunded, so they aren't revenue).

The check compares the number of rows and the total revenue.
""",
             hint="`drop_duplicates(subset='order_id')`, `pd.to_datetime`, then filter with `df[df.returned == 0]`. Work on a copy so you don't change `orders`.",
             starter="""
def clean(orders):
    df = orders.copy()
    # 1. remove duplicate order_ids
    # 2. convert order_date
    # 3. add revenue
    # 4. drop returned orders
    raise NotImplementedError
""",
             solution="""
def clean(orders):
    df = orders.drop_duplicates(subset="order_id").copy()
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = (df["units"] * df["unit_price"] * (1 - df["discount"])).round(2)
    return df[df["returned"] == 0].reset_index(drop=True)
""",
             call="(len(clean(orders)), round(clean(orders)['revenue'].sum(), 2))", tol=1e-6),
        dict(title="Headline KPIs",
             task="""
Write `kpis(orders)` returning a dict with:
- `revenue`: total revenue of clean orders (rounded to 2)
- `orders`: number of clean orders
- `customers`: number of distinct customers who bought
- `aov`: average order value = revenue ÷ orders (rounded to 2)
- `return_rate_pct`: % of **de-duplicated** orders that were returned (rounded to 2)
""",
             hint="Use `clean()` for the first four. For the return rate you need the de-duplicated orders *before* returns were removed.",
             starter="""
def kpis(orders):
    sales = clean(orders)
    raise NotImplementedError
""",
             solution="""
def kpis(orders):
    sales = clean(orders)
    dedup = orders.drop_duplicates(subset="order_id")
    revenue = sales["revenue"].sum()
    return {"revenue": round(revenue, 2), "orders": len(sales), "customers": sales["customer_id"].nunique(),
            "aov": round(revenue / len(sales), 2), "return_rate_pct": round(dedup["returned"].mean() * 100, 2)}
""",
             call="kpis(orders)"),
        dict(title="Monthly revenue and growth",
             task="""
Write `monthly(sales)` that takes the **clean** data and returns a Series of revenue per month, indexed by text like `'2025-01'`, rounded to 2. Then look at the growth: which months are seasonal peaks?
""",
             hint="`sales.order_date.dt.strftime('%Y-%m')` gives the month text; group by it and sum.",
             starter="""
def monthly(sales):
    raise NotImplementedError
""",
             solution="""
def monthly(sales):
    month = sales["order_date"].dt.strftime("%Y-%m")
    return sales.groupby(month)["revenue"].sum().round(2)
""",
             call="monthly(clean(orders))", tol=1e-6,
             after="Plot it: `monthly(clean(orders)).plot(kind='bar', figsize=(10, 3))`. Then compute month-over-month growth with `.pct_change()`. Is the business growing once you look past the October–December peak?"),
        dict(title="Revenue by region and segment — in SQL",
             task="""
Managers will want this from the company database, so do it in SQL. Write `top_groups(sales, customers)`:
1. load both tables into an in-memory SQLite database (`df.to_sql`),
2. join sales to customers,
3. return the **top 5** `(region, segment, revenue)` rows by revenue, with revenue rounded to 2 **in SQL**.
""",
             hint="Store `order_date` as text before `to_sql` (or select only the columns you need). `SELECT c.region, c.segment, ROUND(SUM(s.revenue), 2) AS rev FROM sales s JOIN customers c ON ... GROUP BY ... ORDER BY rev DESC LIMIT 5`.",
             starter="""
def top_groups(sales, customers):
    con = sqlite3.connect(":memory:")
    raise NotImplementedError
""",
             solution="""
def top_groups(sales, customers):
    con = sqlite3.connect(":memory:")
    sales[["order_id", "customer_id", "revenue"]].to_sql("sales", con, index=False)
    customers.to_sql("customers", con, index=False)
    sql = '''SELECT c.region, c.segment, ROUND(SUM(s.revenue), 2) AS rev
             FROM sales s JOIN customers c ON c.customer_id = s.customer_id
             GROUP BY c.region, c.segment ORDER BY rev DESC LIMIT 5'''
    return con.execute(sql).fetchall()
""",
             call="top_groups(clean(orders), customers)", tol=1e-6),
        dict(title="How concentrated is revenue?",
             task="""
Write `pareto(sales, pct)` that returns the % of revenue (rounded to 1) that comes from the top `pct`% of customers by spend (round the number of customers **up**). Run it for 20% — is it close to the famous 80/20?
""",
             hint="Total per customer with groupby, `math.ceil(n * pct / 100)` customers, `nlargest`.",
             starter="""
def pareto(sales, pct):
    raise NotImplementedError
""",
             solution="""
def pareto(sales, pct):
    spend = sales.groupby("customer_id")["revenue"].sum()
    k = math.ceil(len(spend) * pct / 100)
    return round(spend.nlargest(k).sum() / spend.sum() * 100, 1)
""",
             call="[pareto(clean(orders), 20), pareto(clean(orders), 5)]", tol=1e-6),
        dict(title="Do new customers come back?",
             task="""
A customer's **cohort** is the month of their first purchase. Month-1 retention is the % of a cohort that buys again in the **next** calendar month.

Write `month1_retention(sales)` returning a dict `{cohort: retention %}` (rounded to 1) for every cohort except the last month in the data (it has no next month yet).
""",
             hint="Turn dates into monthly periods (`dt.to_period('M')`). First period per customer with `groupby().transform('min')`. A customer is retained if they have any order in cohort + 1.",
             starter="""
def month1_retention(sales):
    raise NotImplementedError
""",
             solution="""
def month1_retention(sales):
    p = sales["order_date"].dt.to_period("M")
    cohort = p.groupby(sales["customer_id"]).transform("min")
    active = set(zip(sales["customer_id"], p))
    first = pd.DataFrame({"customer_id": sales["customer_id"], "cohort": cohort}).drop_duplicates()
    out = {}
    for c, group in first.groupby("cohort"):
        if c == p.max():
            continue
        back = sum((cid, c + 1) in active for cid in group["customer_id"])
        out[str(c)] = round(back / len(group) * 100, 1)
    return out
""",
             call="month1_retention(clean(orders))", tol=1e-6,
             after="Cohorts get small later on (most customers have already bought once), so later percentages are noisier. Say that in your report rather than over-reading them."),
        dict(title="Forecast the next quarter",
             task="""
Write `forecast(sales)`:
1. Build monthly revenue (your `monthly`).
2. **Backtest**: hold out the last 3 months, forecast them from the rest with three methods, and compute each one's MAE:
   - `naive`: the last training month repeated,
   - `mean3`: the mean of the last 3 training months,
   - `seasonal`: the same month one year earlier (value 12 months back).
3. Pick the method with the lowest MAE, then use it on **all** the data to forecast the next 3 months.

Return `(best_method, [3 forecasts rounded to 0])`.
""",
             hint="With values `v` (a list) and training part `t = v[:-3]`: seasonal forecast for step i is `t[len(t) - 12 + i]`. For the final forecast use the full series the same way.",
             starter="""
def forecast(sales):
    v = monthly(sales).tolist()
    raise NotImplementedError
""",
             solution="""
def forecast(sales):
    v = monthly(sales).tolist()

    def predict(t, method):
        if method == "naive":
            return [t[-1]] * 3
        if method == "mean3":
            return [sum(t[-3:]) / 3] * 3
        return [t[len(t) - 12 + i] for i in range(3)]

    train, test = v[:-3], v[-3:]
    mae = {m: sum(abs(a - b) for a, b in zip(test, predict(train, m))) / 3 for m in ["naive", "mean3", "seasonal"]}
    best = min(mae, key=mae.get)
    return best, [round(x) for x in predict(v, best)]
""",
             call="forecast(clean(orders))", tol=1e-6,
             after="A forecast without an error range is a guess. Report the backtest MAE next to it, e.g. *\"₹X ± MAE per month\"*."),
    ],
    extra=[("## A chart for the slide\n\nOne message per chart, stated in the title. Change the title once you know your headline.",
            """
rev = load("retail_orders.csv").drop_duplicates("order_id")
rev = rev[rev.returned == 0].assign(revenue=lambda d: d.units * d.unit_price * (1 - d.discount))
by_month = rev.groupby(rev.order_date.str[:7])["revenue"].sum() / 1e5
ax = by_month.plot(kind="bar", figsize=(10, 3), color="#0f766e")
ax.set_ylabel("revenue (₹ lakh)")
ax.set_title("Revenue by month: peaks every Oct–Dec")
plt.show()
""")],
    present="""
Write a one-page summary for the head of sales (in a markdown cell, or a short slide deck):

1. **Headline** in one sentence: size and growth of the business.
2. **Where the money is**: top regions/segments, and the Pareto share — what it means for risk.
3. **Retention**: what share of new customers come back, and whether it's improving.
4. **Next quarter**: the forecast, the method, and its typical error.
5. **Recommendations** (2–3), each tied to a number above — e.g. a win-back campaign for one-time buyers.
6. **Caveats**: returns removed, duplicates removed, small late cohorts.
""",
    resume=[
        "Cleaned and analysed 18 months of e-commerce orders (≈10k rows) with pandas and SQL, removing duplicate and refunded orders",
        "Built KPI, regional and cohort-retention reports, finding the top 20% of customers drive **X%** of revenue",
        "Backtested naive, moving-average and seasonal forecasts; the chosen method's error was **₹Y** per month",
    ],
    interview=[
        "How did you decide what counts as revenue? What happens to the KPIs if you forget the duplicates or returns?",
        "Why did you choose that forecasting method, and how would you know if it stops working?",
        "Your top 20% of customers bring most of the revenue. What would you recommend, and how would you measure it?",
        "Month-1 retention dropped for later cohorts. Is that a real problem? How would you check?",
        "How would this analysis change if the data were 100 million rows in a warehouse?",
    ],
    extensions=[
        "Add a returns analysis: which categories are returned most, and how much revenue does that cost?",
        "Build an interactive dashboard of the KPIs (Streamlit, Power BI or Tableau) from your clean data.",
        "Forecast per category instead of in total, and compare the sum with the total forecast.",
        "Segment customers with RFM (recency, frequency, monetary) scores.",
    ],
)
