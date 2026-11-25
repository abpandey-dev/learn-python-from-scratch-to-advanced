from lib import *
import math
import numpy as np
import pandas as pd



TOPIC(
    id="eda-kpis", title="EDA, Business KPIs & Storytelling", glyph="KPI",
    blurb="Explore a new dataset systematically, turn Excel habits (VLOOKUP, pivot tables, SUMIFS, IF) into pandas, and compute the metrics businesses run on: funnels, cohorts and retention, churn, ARPU, LTV, growth, Pareto shares and what drove a change.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">df.info(); df.describe(include="all"); df.isna().sum(); df.nunique()
df["x"].skew(); df.corr(numeric_only=True)
df.merge(lookup, on="key", how="left")                          # VLOOKUP / XLOOKUP
df.pivot_table(index="a", columns="b", values="v", aggfunc="sum", margins=True)  # pivot table
df.loc[(df.a == "x") &amp; (df.b &gt; 5), "v"].sum()                   # SUMIFS
np.select([cond1, cond2], ["hi", "mid"], default="lo")         # nested IF
pd.cut(df.v, bins=[0, 100, 500, np.inf])                       # FREQUENCY / bins
s.pct_change() * 100                                           # growth %</code></pre>
""")

ORDERS = [
    {"user": "u1", "month": "2026-01", "segment": "Retail", "amount": 120.0},
    {"user": "u2", "month": "2026-01", "segment": "Retail", "amount": 80.0},
    {"user": "u3", "month": "2026-01", "segment": "Business", "amount": 400.0},
    {"user": "u1", "month": "2026-02", "segment": "Retail", "amount": 60.0},
    {"user": "u3", "month": "2026-02", "segment": "Business", "amount": 650.0},
    {"user": "u4", "month": "2026-02", "segment": "Retail", "amount": 90.0},
    {"user": "u5", "month": "2026-02", "segment": "Business", "amount": 300.0},
    {"user": "u1", "month": "2026-03", "segment": "Retail", "amount": 110.0},
    {"user": "u5", "month": "2026-03", "segment": "Business", "amount": 150.0},
]


Q(None, "Profile a New Dataset", "Easy", "First look",
  "For each column of <code>rows</code> (a list of dicts, None = missing) return <code>(missing count, distinct non-missing values)</code>, keyed by column.",
  [(([{"a": 1, "b": "x"}, {"a": None, "b": "x"}, {"a": 3, "b": None}, {"a": 1, "b": "y"}],), {'a': (1, 2), 'b': (1, 2)})],
  ("Loop over columns and rows, counting Nones and collecting a set.", "O(rc)", "O(rc)"),
  ("<code>df.isna().sum()</code> and <code>df.nunique()</code> — the first two lines of every EDA.", "O(rc)", "O(rc)"),
  viz=([{"a": 1, "b": "x"}, {"a": None, "b": "x"}, {"a": 3, "b": None}, {"a": 1, "b": "y"}],))


@B
def profile(rows):
    out = {}
    for col in rows[0]:
        values = [r[col] for r in rows]
        missing = sum(v is None for v in values)
        out[col] = (missing, len({v for v in values if v is not None}))
    return out


@O
def profile(rows):
    df = pd.DataFrame(rows)
    return {c: (int(df[c].isna().sum()), int(df[c].nunique())) for c in df.columns}


Q(None, "Which Way Is It Skewed?", "Medium", "Skewness",
  "Return pandas' (bias-adjusted) skewness of <code>values</code>, rounded to 4 decimals. Positive = long right tail.",
  [(([1, 2, 2, 3, 3, 3, 4, 20],), 2.7093), (([10, 9, 9, 8, 8, 8, 1],), -2.2944)],
  ("g₁ = m₃ / m₂^1.5 from the central moments, then × √(n(n−1)) / (n − 2).", "O(n)", "O(1)"),
  ("<code>pd.Series(values).skew()</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 2, 3, 3, 3, 4, 20],))


@B
def skewness(values):
    n = len(values)
    m = sum(values) / n
    m2 = sum((v - m) ** 2 for v in values) / n
    m3 = sum((v - m) ** 3 for v in values) / n
    g1 = m3 / m2 ** 1.5
    return round(g1 * math.sqrt(n * (n - 1)) / (n - 2), 4)


@O
def skewness(values):
    return round(float(pd.Series(values).skew()), 4)


Q(None, "Most Correlated Pair of Columns", "Medium", "Correlation matrix",
  "Given numeric columns (dict of lists), return <code>(col1, col2, r)</code> for the pair with the largest |Pearson r| (names in alphabetical order, r rounded to 4).",
  [(({"ads": [1, 2, 3, 4, 5], "visits": [10, 19, 32, 41, 48], "temp": [30, 28, 31, 29, 30]},), ('ads', 'visits', 0.995))],
  ("Compute r for every pair by formula.", "O(k² n)", "O(1)"),
  ("<code>df.corr()</code>, blank the diagonal, then find the largest absolute value.", "O(k² n)", "O(k²)"),
  viz=({"ads": [1, 2, 3, 4, 5], "visits": [10, 19, 32, 41, 48], "temp": [30, 28, 31, 29, 30]},))


@B
def top_pair(cols):
    def r(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y)
        sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
        sxx = sum((a - mx) ** 2 for a in x)
        syy = sum((b - my) ** 2 for b in y)
        return sxy / math.sqrt(sxx * syy)
    names = sorted(cols)
    best = None
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            v = r(cols[names[i]], cols[names[j]])
            if best is None or abs(v) > abs(best[2]):
                best = (names[i], names[j], v)
    return (best[0], best[1], round(best[2], 4))


@O
def top_pair(cols):
    c = pd.DataFrame(cols)[sorted(cols)].corr()
    a = c.abs().to_numpy().copy()
    np.fill_diagonal(a, -1)
    i, j = sorted(np.unravel_index(a.argmax(), a.shape))
    return (c.index[i], c.columns[j], round(float(c.iloc[i, j]), 4))


Q(None, "Segment Summary", "Easy", "Category vs number",
  "Return, per segment (sorted), <code>(orders, total, average order value)</code>, rounded to 2.",
  [((ORDERS,), {'Business': (4, 1500.0, 375.0), 'Retail': (5, 460.0, 92.0)})],
  ("Dicts of totals and counts.", "O(n)", "O(k)"),
  ("<code>groupby('segment')['amount'].agg(['count', 'sum', 'mean'])</code>.", "O(n)", "O(k)"),
  viz=(ORDERS,))


@B
def segment_summary(orders):
    total, count = {}, {}
    for o in orders:
        total[o["segment"]] = total.get(o["segment"], 0) + o["amount"]
        count[o["segment"]] = count.get(o["segment"], 0) + 1
    return {s: (count[s], round(total[s], 2), round(total[s] / count[s], 2)) for s in sorted(total)}


@O
def segment_summary(orders):
    g = pd.DataFrame(orders).groupby("segment")["amount"].agg(["count", "sum", "mean"]).round(2)
    return {s: (int(r["count"]), r["sum"], r["mean"]) for s, r in g.iterrows()}


Q(None, "VLOOKUP in pandas", "Easy", "Left merge",
  "Attach each order's region by looking up its <code>store</code> in <code>stores</code> (store → region). Unknown stores get None. Return the list of regions in order.",
  [(([{"id": 1, "store": "S1"}, {"id": 2, "store": "S9"}, {"id": 3, "store": "S2"}], {"S1": "North", "S2": "South"}), ['North', None, 'South'])],
  ("<code>dict.get</code> for each row — exactly what VLOOKUP does.", "O(n)", "O(m)"),
  ("<code>merge(how='left')</code> keeps every order, like VLOOKUP with IFERROR.", "O(n + m)", "O(n + m)"),
  viz=([{"id": 1, "store": "S1"}, {"id": 2, "store": "S9"}, {"id": 3, "store": "S2"}], {"S1": "North", "S2": "South"}))


@B
def lookup_region(orders, stores):
    return [stores.get(o["store"]) for o in orders]


@O
def lookup_region(orders, stores):
    left = pd.DataFrame(orders)
    right = pd.DataFrame(list(stores.items()), columns=["store", "region"])
    merged = left.merge(right, on="store", how="left")
    return [None if pd.isna(r) else r for r in merged["region"]]


Q(None, "Pivot Table With Totals", "Medium", "pivot_table(margins=True)",
  "Build segment × month revenue with a grand-total row and column named 'All'. Return it as <code>{segment: {month: value}}</code>, missing cells as 0.",
  [((ORDERS,), {'Business': {'2026-01': 400.0, '2026-02': 950.0, '2026-03': 150.0, 'All': 1500.0}, 'Retail': {'2026-01': 200.0, '2026-02': 150.0, '2026-03': 110.0, 'All': 460.0}, 'All': {'2026-01': 600.0, '2026-02': 1100.0, '2026-03': 260.0, 'All': 1960.0}})],
  ("Nested dicts, then add the row and column totals.", "O(n)", "O(rc)"),
  ("<code>pivot_table(..., aggfunc='sum', fill_value=0, margins=True)</code> — an Excel pivot in one line.", "O(n)", "O(rc)"),
  viz=(ORDERS,))


@B
def pivot(orders):
    months = sorted({o["month"] for o in orders})
    segs = sorted({o["segment"] for o in orders})
    t = {s: {m: 0.0 for m in months} for s in segs}
    for o in orders:
        t[o["segment"]][o["month"]] += o["amount"]
    for s in segs:
        t[s]["All"] = sum(t[s][m] for m in months)
    t["All"] = {m: sum(t[s][m] for s in segs) for m in months + ["All"]}
    return t


@O
def pivot(orders):
    p = pd.DataFrame(orders).pivot_table(index="segment", columns="month", values="amount",
                                         aggfunc="sum", fill_value=0, margins=True)
    return {s: {m: float(v) for m, v in row.items()} for s, row in p.iterrows()}


Q(None, "SUMIFS", "Easy", "Sum with several conditions",
  "Return total amount for <code>segment</code> in months from <code>start</code> to <code>end</code> (inclusive, 'YYYY-MM' text).",
  [((ORDERS, "Retail", "2026-02", "2026-03"), 260.0), ((ORDERS, "Business", "2026-01", "2026-01"), 400.0)],
  ("Loop with an if that checks all three conditions.", "O(n)", "O(1)"),
  ("Combine boolean masks with <code>&amp;</code> and <code>.between</code>.", "O(n)", "O(n)"),
  viz=(ORDERS, "Retail", "2026-02", "2026-03"))


@B
def sumifs(orders, segment, start, end):
    total = 0.0
    for o in orders:
        if o["segment"] == segment and start <= o["month"] <= end:
            total += o["amount"]
    return total


@O
def sumifs(orders, segment, start, end):
    df = pd.DataFrame(orders)
    mask = (df["segment"] == segment) & df["month"].between(start, end)
    return float(df.loc[mask, "amount"].sum())


Q(None, "Nested IF to Labels", "Easy", "np.select",
  "Label amounts: 'VIP' if ≥ 500, 'High' if ≥ 200, 'Mid' if ≥ 100, else 'Low'.",
  [(([650, 120, 80, 200, 499.99],), ['VIP', 'Mid', 'Low', 'High', 'High'])],
  ("An if / elif chain, like nested IF formulas.", "O(n)", "O(n)"),
  ("<code>np.select</code> checks the conditions in order, for the whole column at once.", "O(n)", "O(n)"),
  viz=([650, 120, 80, 200, 499.99],))


@B
def labels(amounts):
    out = []
    for a in amounts:
        if a >= 500:
            out.append("VIP")
        elif a >= 200:
            out.append("High")
        elif a >= 100:
            out.append("Mid")
        else:
            out.append("Low")
    return out


@O
def labels(amounts):
    a = np.array(amounts)
    return np.select([a >= 500, a >= 200, a >= 100], ["VIP", "High", "Mid"], default="Low").tolist()


Q(None, "Conversion Funnel", "Medium", "Step-to-step conversion",
  "<code>events</code> are (user, step) pairs. For each step in <code>steps</code>, return <code>(step, users who reached it, % of the previous step)</code> — the first step is 100.0. A user counts at a step only if they also reached every earlier step.",
  [(([("a", "visit"), ("b", "visit"), ("c", "visit"), ("d", "visit"), ("a", "cart"), ("b", "cart"), ("d", "buy"), ("a", "buy")], ["visit", "cart", "buy"]), [('visit', 4, 100.0), ('cart', 2, 50.0), ('buy', 1, 50.0)])],
  ("Sets of users per step, intersected step by step.", "O(n)", "O(n)"),
  ("A user × step crosstab, then <code>cumprod</code> across steps to require all earlier steps.", "O(n)", "O(us)"),
  viz=([("a", "visit"), ("b", "visit"), ("c", "visit"), ("a", "cart"), ("a", "buy")], ["visit", "cart", "buy"]))


@B
def funnel(events, steps):
    reached = {s: set() for s in steps}
    for u, s in events:
        reached[s].add(u)
    out, alive, prev = [], None, None
    for s in steps:
        alive = reached[s] if alive is None else alive & reached[s]
        pct = 100.0 if prev is None else round(len(alive) / prev * 100, 1)
        out.append((s, len(alive), pct))
        prev = len(alive)
    return out


@O
def funnel(events, steps):
    df = pd.DataFrame(events, columns=["user", "step"])
    hit = pd.crosstab(df["user"], df["step"]).reindex(columns=steps, fill_value=0).clip(upper=1)
    counts = hit.cumprod(axis=1).sum()
    pct = (counts / counts.shift(1) * 100).round(1).fillna(100.0)
    return [(s, int(counts[s]), float(pct[s])) for s in steps]


Q(None, "Cohort Retention Table", "Hard", "Cohorts",
  "Each user's cohort is their first month. Return <code>{cohort: [% of the cohort active in month 0, 1, 2, …]}</code> (rounded to 1), up to the last month in the data.",
  [((ORDERS,), {'2026-01': [100.0, 66.7, 33.3], '2026-02': [100.0, 50.0]})],
  ("First month per user, then sets of active users per (cohort, offset).", "O(n)", "O(n)"),
  ("Month offset column, then <code>pivot_table(aggfunc='nunique')</code> divided by column 0.", "O(n)", "O(n)"),
  viz=(ORDERS,))


@B
def retention(orders):
    def idx(m):
        y, mo = m.split("-")
        return int(y) * 12 + int(mo)
    first = {}
    for o in orders:
        first[o["user"]] = min(first.get(o["user"], o["month"]), o["month"])
    last = max(idx(o["month"]) for o in orders)
    active = {}
    for o in orders:
        c = first[o["user"]]
        active.setdefault((c, idx(o["month"]) - idx(c)), set()).add(o["user"])
    out = {}
    for c in sorted(set(first.values())):
        size = len(active[(c, 0)])
        out[c] = [round(len(active.get((c, k), set())) / size * 100, 1) for k in range(last - idx(c) + 1)]
    return out


@O
def retention(orders):
    df = pd.DataFrame(orders)
    p = pd.PeriodIndex(df["month"], freq="M")
    df["cohort"] = p.to_series(index=df.index).groupby(df["user"]).transform("min")
    df["offset"] = (p - pd.PeriodIndex(df["cohort"], freq="M")).map(lambda d: d.n)
    t = df.pivot_table(index="cohort", columns="offset", values="user", aggfunc="nunique")
    t = (t.div(t[0], axis=0) * 100).round(1).fillna(0.0)
    last = p.max()
    return {str(c): [float(v) for v in row.iloc[:(last - c).n + 1]] for c, row in t.iterrows()}


Q(None, "Monthly Churn Rate", "Medium", "Who didn't come back",
  "A user active in month m churns if they are not active in month m + 1. Return <code>{month: churn %}</code> for every month except the last (rounded to 1).",
  [((ORDERS,), {'2026-01': 33.3, '2026-02': 50.0})],
  ("Sets of active users per month; compare each with the next.", "O(n)", "O(n)"),
  ("Per-month user sets with <code>groupby(...).agg(set)</code>, then compare neighbours.", "O(n)", "O(n)"),
  viz=(ORDERS,))


@B
def churn(orders):
    active = {}
    for o in orders:
        active.setdefault(o["month"], set()).add(o["user"])
    months = sorted(active)
    out = {}
    for m, nxt in zip(months, months[1:]):
        lost = active[m] - active[nxt]
        out[m] = round(len(lost) / len(active[m]) * 100, 1)
    return out


@O
def churn(orders):
    s = pd.DataFrame(orders).groupby("month")["user"].agg(set)
    return {m: round(len(a - b) / len(a) * 100, 1) for m, a, b in zip(s.index, s, s.shift(-1)) if isinstance(b, set)}


Q(None, "ARPU and ARPPU", "Easy", "Revenue per user",
  "Given total users in the month and that month's orders, return <code>(ARPU, ARPPU)</code>: revenue per user, and revenue per paying user (rounded to 2).",
  [((ORDERS, "2026-02", 10), (110.0, 275.0))],
  ("Add the month's revenue and collect its paying users.", "O(n)", "O(n)"),
  ("Filter once, then <code>sum()</code> and <code>nunique()</code>.", "O(n)", "O(n)"),
  viz=(ORDERS, "2026-02", 10))


@B
def arpu(orders, month, total_users):
    revenue, payers = 0.0, set()
    for o in orders:
        if o["month"] == month:
            revenue += o["amount"]
            payers.add(o["user"])
    return (round(revenue / total_users, 2), round(revenue / len(payers), 2))


@O
def arpu(orders, month, total_users):
    m = pd.DataFrame(orders).query("month == @month")
    return (round(m["amount"].sum() / total_users, 2), round(m["amount"].sum() / m["user"].nunique(), 2))


Q(None, "Month-over-Month Growth", "Easy", "pct_change",
  "Return <code>{month: revenue growth % vs previous month}</code> (rounded to 1), skipping the first month.",
  [((ORDERS,), {'2026-02': 83.3, '2026-03': -76.4})],
  ("Monthly totals, then (this − last) / last.", "O(n)", "O(months)"),
  ("<code>groupby('month').sum().pct_change()</code>.", "O(n)", "O(months)"),
  viz=(ORDERS,))


@B
def mom_growth(orders):
    rev = {}
    for o in orders:
        rev[o["month"]] = rev.get(o["month"], 0) + o["amount"]
    months = sorted(rev)
    return {m: round((rev[m] - rev[p]) / rev[p] * 100, 1) for p, m in zip(months, months[1:])}


@O
def mom_growth(orders):
    g = pd.DataFrame(orders).groupby("month")["amount"].sum().pct_change().mul(100).round(1).dropna()
    return g.to_dict()


Q(None, "The 80/20 Check", "Medium", "Pareto share",
  "What share of revenue (percent, rounded to 1) comes from the top <code>pct</code>% of customers by spend? Round the number of top customers up.",
  [((ORDERS, 20), 53.6), ((ORDERS, 60), 91.3)],
  ("Total per user, sort descending, add up the first ⌈k⌉.", "O(n + u log u)", "O(u)"),
  ("<code>groupby().sum().nlargest(k)</code>.", "O(n + u log u)", "O(u)"),
  viz=(ORDERS, 20))


@B
def pareto(orders, pct):
    spend = {}
    for o in orders:
        spend[o["user"]] = spend.get(o["user"], 0) + o["amount"]
    ranked = sorted(spend.values(), reverse=True)
    k = math.ceil(len(ranked) * pct / 100)
    return round(sum(ranked[:k]) / sum(ranked) * 100, 1)


@O
def pareto(orders, pct):
    spend = pd.DataFrame(orders).groupby("user")["amount"].sum()
    k = math.ceil(len(spend) * pct / 100)
    return round(spend.nlargest(k).sum() / spend.sum() * 100, 1)


Q(None, "Customer Lifetime Value", "Easy", "LTV",
  "Simple LTV = average monthly revenue per customer × gross margin ÷ monthly churn rate. Return it rounded to 2.",
  [((40.0, 0.6, 0.05), 480.0), ((40.0, 0.6, 0.2), 120.0)],
  ("Expected lifetime is 1 / churn months; multiply it out.", "O(1)", "O(1)"),
  ("The same formula, written as one expression.", "O(1)", "O(1)"),
  viz=(40.0, 0.6, 0.05))


@B
def ltv(arpu, margin, churn_rate):
    months = 1 / churn_rate
    profit_per_month = arpu * margin
    return round(profit_per_month * months, 2)


@O
def ltv(arpu, margin, churn_rate):
    return round(arpu * margin / churn_rate, 2)


Q(None, "Repeat Purchase Rate", "Easy", "Loyalty",
  "Return the % of customers (rounded to 1) with more than one order, and the average order value (rounded to 2).",
  [((ORDERS,), (60.0, 217.78))],
  ("Count orders per user in a dict.", "O(n)", "O(u)"),
  ("<code>value_counts()</code> on user, then a boolean mean.", "O(n)", "O(u)"),
  viz=(ORDERS,))


@B
def repeat_rate(orders):
    counts = {}
    for o in orders:
        counts[o["user"]] = counts.get(o["user"], 0) + 1
    repeaters = sum(1 for c in counts.values() if c > 1)
    aov = sum(o["amount"] for o in orders) / len(orders)
    return (round(repeaters / len(counts) * 100, 1), round(aov, 2))


@O
def repeat_rate(orders):
    df = pd.DataFrame(orders)
    return (round((df["user"].value_counts() > 1).mean() * 100, 1), round(df["amount"].mean(), 2))


Q(None, "What Drove the Change?", "Medium", "Contribution analysis",
  "Revenue changed between months <code>a</code> and <code>b</code>. Return <code>(segment, change)</code> sorted from biggest absolute change to smallest.",
  [((ORDERS, "2026-02", "2026-03"), [('Business', -800.0), ('Retail', -40.0)]), ((ORDERS, "2026-01", "2026-02"), [('Business', 550.0), ('Retail', -50.0)])],
  ("Totals per (segment, month) in a dict; subtract.", "O(n)", "O(k)"),
  ("Pivot segment × month, subtract the two columns, sort by <code>abs</code>.", "O(n)", "O(k)"),
  viz=(ORDERS, "2026-02", "2026-03"))


@B
def drivers(orders, a, b):
    t = {}
    for o in orders:
        key = o["segment"]
        t.setdefault(key, {a: 0.0, b: 0.0})
        if o["month"] in (a, b):
            t[key][o["month"]] += o["amount"]
    diffs = [(s, t[s][b] - t[s][a]) for s in t]
    return sorted(diffs, key=lambda d: -abs(d[1]))


@O
def drivers(orders, a, b):
    p = pd.DataFrame(orders).pivot_table(index="segment", columns="month", values="amount", aggfunc="sum", fill_value=0)
    d = (p[b] - p[a]).sort_values(key=abs, ascending=False)
    return list(d.items())


Q(None, "Top N and 'Other'", "Easy", "Charts people can read",
  "Keep the <code>n</code> largest categories by value and add the rest together as 'Other'. Return a list of (name, value), largest first, 'Other' last (only if anything was grouped).",
  [(({"Pune": 50, "Delhi": 120, "Goa": 5, "Agra": 8, "Mumbai": 90}, 2), [('Delhi', 120), ('Mumbai', 90), ('Other', 63)]), (({"a": 1, "b": 2}, 3), [('b', 2), ('a', 1)])],
  ("Sort the items, split at n, add up the tail.", "O(k log k)", "O(k)"),
  ("<code>Series.nlargest(n)</code>, then the remainder from the total.", "O(k log k)", "O(k)"),
  viz=({"Pune": 50, "Delhi": 120, "Goa": 5, "Agra": 8, "Mumbai": 90}, 2))


@B
def top_n_other(values, n):
    items = sorted(values.items(), key=lambda kv: -kv[1])
    top, rest = items[:n], items[n:]
    if rest:
        top.append(("Other", sum(v for _, v in rest)))
    return top


@O
def top_n_other(values, n):
    s = pd.Series(values)
    top = s.nlargest(n)
    out = list(top.items())
    if len(s) > n:
        out.append(("Other", int(s.sum() - top.sum())))
    return out


Q(None, "Bucket Values into Ranges", "Easy", "pd.cut (Excel FREQUENCY)",
  "Count how many amounts fall in each bin <code>(edges[i], edges[i+1]]</code>. Return a list of counts.",
  [(([120, 80, 400, 60, 650, 90, 300, 110, 150], [0, 100, 250, 500, 1000]), [3, 3, 2, 1])],
  ("For each value, walk the edges until it fits.", "O(nb)", "O(b)"),
  ("<code>pd.cut</code> labels each value with its bin; <code>value_counts(sort=False)</code> counts them in bin order.", "O(n log b)", "O(b)"),
  viz=([120, 80, 400, 60, 650, 90, 300, 110, 150], [0, 100, 250, 500, 1000]))


@B
def bucket_counts(values, edges):
    counts = [0] * (len(edges) - 1)
    for v in values:
        for i in range(len(edges) - 1):
            if edges[i] < v <= edges[i + 1]:
                counts[i] += 1
                break
    return counts


@O
def bucket_counts(values, edges):
    return pd.Series(pd.cut(values, edges)).value_counts(sort=False).tolist()


VISITS = [("u1", "2026-03-01"), ("u2", "2026-03-01"), ("u1", "2026-03-02"), ("u3", "2026-03-02"),
          ("u1", "2026-03-03"), ("u1", "2026-03-03"), ("u4", "2026-03-03")]


Q(None, "Stickiness: DAU / MAU", "Medium", "Engagement",
  "From (user, day) visits in one month, return <code>(average daily active users, monthly active users, DAU/MAU %)</code>, averaging only over days that appear, rounded to 2. Repeat visits on a day count once.",
  [((VISITS,), (2.0, 4, 50.0)), ((VISITS[:2],), (2.0, 2, 100.0))],
  ("A set of users per day, and one set for the month.", "O(n)", "O(n)"),
  ("<code>groupby('day')['user'].nunique().mean()</code> and <code>nunique()</code>.", "O(n)", "O(n)"),
  viz=(VISITS,))


@B
def stickiness(visits):
    per_day = {}
    month = set()
    for user, day in visits:
        per_day.setdefault(day, set()).add(user)
        month.add(user)
    dau = sum(len(s) for s in per_day.values()) / len(per_day)
    return (round(dau, 2), len(month), round(dau / len(month) * 100, 2))


@O
def stickiness(visits):
    df = pd.DataFrame(visits, columns=["user", "day"])
    dau = df.groupby("day")["user"].nunique().mean()
    mau = df["user"].nunique()
    return (round(dau, 2), mau, round(dau / mau * 100, 2))
