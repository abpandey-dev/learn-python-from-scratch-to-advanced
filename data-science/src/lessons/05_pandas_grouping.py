from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

LESSON("Basics", "Split, apply, combine", """
<p>Most business questions sound like "<b>total sales per region</b>" or "<b>average score per class</b>". <code>groupby</code> answers them in three steps:</p>
<ol>
<li><b>Split</b> the rows into groups by a key (region).</li>
<li><b>Apply</b> a function to each group (sum the amounts).</li>
<li><b>Combine</b> the results into a new Series or DataFrame indexed by the key.</li>
</ol>
<pre><code class="py">df.groupby("region")["amount"].sum()
df.groupby("region")["amount"].mean()
df.groupby("region").size()               # rows per group
df.groupby(["region", "product"])["amount"].sum()   # two keys</code></pre>
""", practice=["Total per Group", "Average per Group", "Rows per Group"])


@LD
def groupby_demo():
    df = pd.DataFrame({"region": ["North", "South", "North", "South"], "amount": [100, 80, 40, 120]})
    totals = df.groupby("region")["amount"].sum()
    average = df.groupby("region")["amount"].mean()
    counts = df.groupby("region").size()
    print(totals.to_dict(), average.to_dict(), counts.to_dict())


LESSON("Core", "agg, transform and filter", """
<table>
<tr><th>Method</th><th>Returns</th><th>Use for</th></tr>
<tr><td><code>agg</code></td><td>one row per group</td><td>summaries: <code>agg(total=("amount", "sum"), avg=("amount", "mean"))</code></td></tr>
<tr><td><code>transform</code></td><td>same length as the original</td><td>group values per row: share of group total, z-score within group</td></tr>
<tr><td><code>filter</code></td><td>original rows of some groups</td><td>keep groups that pass a test (≥ 3 sales)</td></tr>
<tr><td><code>apply</code></td><td>anything</td><td>custom logic (slowest)</td></tr>
</table>
<p>Also useful per group: <code>cumsum</code>, <code>rank</code>, <code>first</code>/<code>last</code>, <code>nlargest</code>, <code>idxmax</code>.</p>
""", practice=["Several Statistics at Once", "Share of Group Total", "Keep Big Groups Only", "Rank Within Group", "Running Total per Group", "First and Last per Group", "Best Product per Region"])


@LD
def agg_transform_demo():
    df = pd.DataFrame({"region": ["N", "S", "N", "S", "N"], "amount": [100, 80, 40, 120, 60]})
    summary = df.groupby("region").agg(total=("amount", "sum"), biggest=("amount", "max"))
    df["region_total"] = df.groupby("region")["amount"].transform("sum")
    df["share"] = (df["amount"] / df["region_total"] * 100).round(1)
    busy = df.groupby("region").filter(lambda g: len(g) >= 3)
    print(summary)
    print(df)
    print(busy["amount"].tolist())


LESSON("Core", "Joining tables: merge and concat", """
<p><code>pd.merge</code> combines tables on matching key columns, like SQL JOIN:</p>
<table>
<tr><th><code>how=</code></th><th>Keeps</th></tr>
<tr><td><code>"inner"</code> (default)</td><td>only keys in both tables</td></tr>
<tr><td><code>"left"</code></td><td>every row of the left table (missing matches → NaN)</td></tr>
<tr><td><code>"right"</code></td><td>every row of the right table</td></tr>
<tr><td><code>"outer"</code></td><td>every key from either table</td></tr>
</table>
<pre><code class="py">pd.merge(orders, customers, left_on="cust", right_on="id", how="left")
pd.concat([jan, feb], ignore_index=True)       # stack rows
pd.concat([a, b], axis=1)                      # side by side (aligned on index)</code></pre>
<div class="warn">If keys repeat on both sides, merge produces every combination — row counts can explode. Check <code>len()</code> before and after.</div>
""", practice=["Join Customers and Orders", "Customers With Their Spending", "Stack Two Tables", "Customers Without Orders"])


@LD
def merge_demo():
    customers = pd.DataFrame({"id": [1, 2, 3], "name": ["Ana", "Ben", "Cy"]})
    orders = pd.DataFrame({"cust": [2, 1, 2, 9], "amount": [50, 30, 20, 99]})
    inner = orders.merge(customers, left_on="cust", right_on="id")
    left = customers.merge(orders, left_on="id", right_on="cust", how="left")
    print(len(inner), len(left))
    print(left[["name", "amount"]])


LESSON("Advanced", "Reshaping: pivot, melt, crosstab, stack", """
<p><b>Wide</b> data has one column per category (Jan, Feb, Mar). <b>Long</b> (tidy) data has one row per observation (region, month, amount). Analysis and Seaborn prefer long; reports prefer wide.</p>
<table>
<tr><th>Long → wide</th><th>Wide → long</th></tr>
<tr><td><code>pivot_table(index, columns, values, aggfunc)</code></td><td><code>melt(id_vars, var_name, value_name)</code></td></tr>
<tr><td><code>unstack()</code> (index level → columns)</td><td><code>stack()</code> (columns → index level)</td></tr>
<tr><td><code>pd.crosstab(a, b)</code> (counts)</td><td>—</td></tr>
</table>
""", practice=["Pivot Table", "Wide to Long (melt)", "Cross Tabulation", "Groups From Two Keys to a Table"])


@LD
def reshape_demo():
    sales = pd.DataFrame({"region": ["N", "S", "N", "S"], "month": ["Jan", "Jan", "Feb", "Feb"], "amount": [100, 80, 40, 120]})
    wide = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
    long = wide.reset_index().melt(id_vars="region", value_name="amount")
    counts = pd.crosstab(sales["region"], sales["month"])
    print(wide)
    print(long)
    print(counts)


LESSON("Advanced", "Time-based grouping and rolling windows", """
<pre><code class="py">df["date"] = pd.to_datetime(df["date"])
df.groupby(df["date"].dt.to_period("M"))["amount"].sum()      # per month
df.resample("ME", on="date")["amount"].sum()                  # same, with resample
df["amount"].rolling(7).mean()                                # 7-row moving average
df["amount"].pct_change()                                     # change vs previous row
df["amount"].shift(1)                                         # previous row's value</code></pre>
<p>Rolling windows smooth noisy daily data; the first <code>window − 1</code> results are NaN because there isn't enough history yet.</p>
""", practice=["Monthly Totals From Daily Data", "Rolling 3-Day Average"])


@LD
def time_demo():
    df = pd.DataFrame({"date": pd.date_range("2024-01-30", periods=6, freq="D"), "amount": [10, 20, 30, 40, 50, 60]})
    monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
    df["avg3"] = df["amount"].rolling(3).mean()
    df["change"] = df["amount"].pct_change().round(2)
    print(monthly.to_dict())
    print(df)


LESSON("Basics", "groupby by hand", """
<p>Sales: Pune 10, Delhi 20, Pune 30, Delhi 40, Goa 50. <code>df.groupby("city")["sales"].sum()</code> runs three steps:</p>
<table><tr><th>Split</th><th>Apply (sum)</th><th>Combine</th></tr>
<tr><td>Delhi: 20, 40</td><td>60</td><td rowspan="3">Delhi 60<br>Goa 50<br>Pune 40</td></tr>
<tr><td>Goa: 50</td><td>50</td></tr>
<tr><td>Pune: 10, 30</td><td>40</td></tr></table>
<p>The result is sorted by group name, and the groups become the index. <code>as_index=False</code> or <code>.reset_index()</code> gives a normal table.</p>
<h4>Common points</h4>
<ul><li>Rows with a missing group value are <b>dropped</b> unless you use <code>dropna=False</code>. Totals can come out short without warning.</li>
<li><code>size()</code> counts rows, while <code>count()</code> counts non-missing values.</li>
<li>Name your results: <code>agg(total=("sales", "sum"), average=("sales", "mean"))</code>.</li></ul>
""", practice=["Total per Group", "Average per Group", "Rows per Group", "Several Statistics at Once"])


@LD
def groupby_by_hand():
    df = pd.DataFrame({"city": ["Pune", "Delhi", "Pune", "Delhi", "Goa", None], "sales": [10, 20, 30, 40, 50, 60]})
    totals = df.groupby("city")["sales"].sum()
    with_missing_group = df.groupby("city", dropna=False)["sales"].sum()
    summary = df.groupby("city").agg(total=("sales", "sum"), average=("sales", "mean"), orders=("sales", "size"))
    as_table = totals.reset_index()


LESSON("Core", "agg vs transform: same size or smaller?", """
<table><tr><th></th><th>Output size</th><th>Use it to</th></tr>
<tr><td><code>agg</code></td><td>one row per group</td><td>summarise</td></tr>
<tr><td><code>transform</code></td><td>same rows as the input</td><td>add a group result to every row</td></tr>
<tr><td><code>filter</code></td><td>some of the original rows</td><td>keep or drop whole groups</td></tr></table>
<h4>Worked example: share of region total</h4>
<table><tr><th>Region</th><th>Sales</th><th>transform("sum")</th><th>Share</th></tr>
<tr><td>A</td><td>10</td><td>40</td><td>0.25</td></tr>
<tr><td>A</td><td>30</td><td>40</td><td>0.75</td></tr>
<tr><td>B</td><td>5</td><td>20</td><td>0.25</td></tr>
<tr><td>B</td><td>15</td><td>20</td><td>0.75</td></tr></table>
<pre><code class="py">df["share"] = df["sales"] / df.groupby("region")["sales"].transform("sum")</code></pre>
<p>Because <code>transform</code> returns one value per original row, the division lines up. <code>sum()</code> alone returns just 2 rows, which wouldn't.</p>
<p>The same idea gives rank within a group, difference from a group average, and running totals with <code>cumsum</code>.</p>
""", practice=["Share of Group Total", "Rank Within Group", "Running Total per Group", "Keep Big Groups Only", "Best Product per Region", "First and Last per Group"])


@LD
def transform_vs_agg():
    df = pd.DataFrame({"region": ["A", "A", "B", "B"], "sales": [10, 30, 5, 15]})
    summary = df.groupby("region")["sales"].sum()
    same_size = df.groupby("region")["sales"].transform("sum")
    df["share"] = df["sales"] / same_size
    df["rank_in_region"] = df.groupby("region")["sales"].rank(ascending=False)
    df["running"] = df.groupby("region")["sales"].cumsum()


LESSON("Core", "Joins by hand", """
<p>Customers: 1 Ana, 2 Ben, 3 Cy. Orders by customer id: 1, 1, 2, 4.</p>
<table><tr><th>how=</th><th>Keeps</th><th>Rows</th><th>Result</th></tr>
<tr><td>inner</td><td>matches only</td><td>3</td><td>Ana, Ana, Ben</td></tr>
<tr><td>left</td><td>every customer</td><td>4</td><td>Ana, Ana, Ben, Cy (no order)</td></tr>
<tr><td>right</td><td>every order</td><td>4</td><td>Ana, Ana, Ben, and an order for unknown customer 4</td></tr>
<tr><td>outer</td><td>everything</td><td>5</td><td>all of the above</td></tr></table>
<h4>The row explosion</h4>
<p>If a key repeats on <b>both</b> sides, rows multiply: 2 rows × 3 rows with the same key give 6. This silently inflates totals. Check the row count after every join, and let pandas check it for you:</p>
<pre><code class="py">orders.merge(customers, on="id", validate="many_to_one", indicator=True)</code></pre>
<p><code>validate</code> raises an error if the keys aren't as expected, and <code>indicator=True</code> adds a column saying where each row came from. To find customers without orders, keep the rows marked <code>left_only</code>.</p>
<p><b>Check key types too:</b> an id stored as text won't match one stored as a number.</p>
""", practice=["Join Customers and Orders", "Customers With Their Spending", "Customers Without Orders", "Stack Two Tables"])


@LD
def joins_by_hand():
    customers = pd.DataFrame({"id": [1, 2, 3], "name": ["Ana", "Ben", "Cy"]})
    orders = pd.DataFrame({"id": [1, 1, 2, 4], "amount": [10, 20, 30, 40]})
    sizes = {how: len(customers.merge(orders, on="id", how=how)) for how in ["inner", "left", "right", "outer"]}
    marked = customers.merge(orders, on="id", how="left", indicator=True)
    no_orders = marked[marked["_merge"] == "left_only"]["name"]
    a = pd.DataFrame({"k": [1, 1], "x": [1, 2]})
    b = pd.DataFrame({"k": [1, 1, 1], "y": [7, 8, 9]})
    exploded = len(a.merge(b, on="k"))


LESSON("Advanced", "Wide and long, by hand", """
<table><tr><th>Name</th><th>Jan</th><th>Feb</th></tr>
<tr><td>Ana</td><td>10</td><td>20</td></tr><tr><td>Ben</td><td>30</td><td>40</td></tr></table>
<p>That's <b>wide</b>: good for reading. Plotting and <code>groupby</code> prefer <b>long</b>, with one observation per row:</p>
<table><tr><th>Name</th><th>Month</th><th>Sales</th></tr>
<tr><td>Ana</td><td>Jan</td><td>10</td></tr><tr><td>Ben</td><td>Jan</td><td>30</td></tr><tr><td>Ana</td><td>Feb</td><td>20</td></tr><tr><td>Ben</td><td>Feb</td><td>40</td></tr></table>
<pre><code class="py">long = wide.melt(id_vars="name", var_name="month", value_name="sales")
wide = long.pivot(index="name", columns="month", values="sales")</code></pre>
<h4>pivot or pivot_table?</h4>
<ul><li><code>pivot</code> only reshapes. Repeated name–month pairs raise an error.</li>
<li><code>pivot_table</code> also combines repeats, with the mean by default. So pass <code>aggfunc="sum"</code> if totals are what you want.</li></ul>
<p><b>Cross-tab with shares:</b> <code>pd.crosstab(a, b, normalize="index")</code> shows the share of each row.</p>
""", practice=["Wide to Long (melt)", "Pivot Table", "Cross Tabulation", "Groups From Two Keys to a Table"])


@LD
def reshape_by_hand():
    wide = pd.DataFrame({"name": ["Ana", "Ben"], "Jan": [10, 30], "Feb": [20, 40]})
    long = wide.melt(id_vars="name", var_name="month", value_name="sales")
    back = long.pivot(index="name", columns="month", values="sales")
    repeats = pd.DataFrame({"name": ["Ana", "Ana"], "month": ["Jan", "Jan"], "sales": [10, 5]})
    default_is_mean = repeats.pivot_table(index="name", columns="month", values="sales")
    summed = repeats.pivot_table(index="name", columns="month", values="sales", aggfunc="sum")


LESSON("Advanced", "Rolling windows and changes over time, by hand", """
<p>Values: 10, 20, 30, 40, 50.</p>
<table><tr><th>Value</th><th>rolling(3).mean()</th><th>shift(1)</th><th>diff()</th><th>pct_change()</th><th>cumsum()</th></tr>
<tr><td>10</td><td>–</td><td>–</td><td>–</td><td>–</td><td>10</td></tr>
<tr><td>20</td><td>–</td><td>10</td><td>10</td><td>1.00</td><td>30</td></tr>
<tr><td>30</td><td>20</td><td>20</td><td>10</td><td>0.50</td><td>60</td></tr>
<tr><td>40</td><td>30</td><td>30</td><td>10</td><td>0.33</td><td>100</td></tr>
<tr><td>50</td><td>40</td><td>40</td><td>10</td><td>0.25</td><td>150</td></tr></table>
<p>The first two rolling values are blank because a window of 3 isn't full yet (<code>min_periods=1</code> changes that). Rolling windows look <b>backwards</b> by default, so the value on each row uses that row and earlier ones.</p>
<h4>Time pitfalls</h4>
<ul><li>Sort by date first; these all use row order.</li>
<li><code>rolling("7D")</code> uses real time and copes with missing days, while <code>rolling(7)</code> just counts 7 rows.</li>
<li>In ML features, use <code>shift(1)</code> before rolling, or today's value leaks into the prediction of today.</li></ul>
""", practice=["Rolling 3-Day Average", "Monthly Totals From Daily Data"])


@LD
def rolling_by_hand():
    s = pd.Series([10, 20, 30, 40, 50])
    rolling = s.rolling(3).mean()
    previous = s.shift(1)
    change = s.diff()
    percent = s.pct_change().round(2)
    running = s.cumsum()
    safe_feature = s.shift(1).rolling(3).mean()
