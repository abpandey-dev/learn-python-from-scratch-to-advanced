from lib import *
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
