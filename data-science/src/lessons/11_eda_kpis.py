from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ORDERS = pd.DataFrame({
    "user": ["u1", "u2", "u3", "u1", "u3", "u4", "u5", "u1", "u5"],
    "month": ["2026-01"] * 3 + ["2026-02"] * 4 + ["2026-03"] * 2,
    "segment": ["Retail", "Retail", "Business", "Retail", "Business", "Retail", "Business", "Retail", "Business"],
    "amount": [120.0, 80, 400, 60, 650, 90, 300, 110, 150],
})

LESSON("Basics", "EDA: a checklist for any new dataset", """
<p><b>Exploratory Data Analysis</b> is getting to know a dataset before you trust it. Do it in the same order every time:</p>
<ol>
<li><b>Shape and grain</b>: how many rows, and what does one row mean (one order? one user per day?). <code>df.shape</code>, <code>df.head()</code>.</li>
<li><b>Types and gaps</b>: <code>df.info()</code>, <code>df.isna().sum()</code>, <code>df.nunique()</code>. Is a date stored as text? Is an ID column numeric by accident?</li>
<li><b>Univariate</b>: each column alone. Numbers: <code>describe()</code>, a histogram, skewness. Categories: <code>value_counts()</code>.</li>
<li><b>Bivariate</b>: pairs. Number vs number: scatter and correlation. Category vs number: groupby and box plots. Category vs category: crosstab.</li>
<li><b>Sanity checks</b>: duplicates, impossible values (negative ages), totals that should match a known figure.</li>
<li><b>Write down questions and findings</b> as you go; EDA ends with a short list of facts and open questions, not 50 charts.</li>
</ol>
<p>Skewed money data (most orders small, a few huge) is the norm: report the median with the mean, and try a log scale on charts.</p>
""", practice=["Profile a New Dataset", "Which Way Is It Skewed?", "Most Correlated Pair of Columns", "Segment Summary", "Bucket Values into Ranges"])

LESSON("Core", "From Excel to pandas", """
<p>Most business teams live in Excel. Every Excel habit has a pandas twin that is repeatable and handles millions of rows:</p>
<table>
<tr><th>Excel</th><th>pandas</th></tr>
<tr><td>VLOOKUP / XLOOKUP</td><td><code>df.merge(lookup, on="key", how="left")</code> or <code>df.key.map(dict)</code></td></tr>
<tr><td>Pivot table</td><td><code>df.pivot_table(index=…, columns=…, values=…, aggfunc="sum", margins=True)</code></td></tr>
<tr><td>SUMIFS / COUNTIFS</td><td><code>df.loc[mask1 &amp; mask2, "v"].sum()</code></td></tr>
<tr><td>Nested IF</td><td><code>np.select(conditions, choices, default=…)</code></td></tr>
<tr><td>FREQUENCY / bins</td><td><code>pd.cut(…).value_counts(sort=False)</code></td></tr>
<tr><td>Filters, sort</td><td><code>df.query(…)</code>, <code>sort_values</code></td></tr>
<tr><td>Conditional formatting</td><td><code>df.style.background_gradient()</code></td></tr>
<tr><td>Read / write sheets</td><td><code>pd.read_excel</code>, <code>df.to_excel</code> (needs openpyxl)</td></tr>
</table>
""", practice=["VLOOKUP in pandas", "Pivot Table With Totals", "SUMIFS", "Nested IF to Labels"])

LESSON("Core", "The KPIs every analyst should know", """
<table>
<tr><th>KPI</th><th>Formula</th><th>Answers</th></tr>
<tr><td>Conversion rate</td><td>users who did X ÷ users who could</td><td>is the funnel working?</td></tr>
<tr><td>AOV</td><td>revenue ÷ orders</td><td>how big is a typical basket?</td></tr>
<tr><td>ARPU / ARPPU</td><td>revenue ÷ all users / paying users</td><td>how much is a user worth per month?</td></tr>
<tr><td>Retention / churn</td><td>share still active / gone next period</td><td>do people stay?</td></tr>
<tr><td>DAU / MAU</td><td>average daily ÷ monthly actives</td><td>how habit-forming is the product?</td></tr>
<tr><td>LTV</td><td>ARPU × margin ÷ churn</td><td>how much can we pay to acquire a user?</td></tr>
<tr><td>CAC</td><td>marketing spend ÷ new customers</td><td>LTV/CAC above ~3 is healthy</td></tr>
<tr><td>Growth</td><td>(this − last) ÷ last</td><td>are we growing?</td></tr>
</table>
<p>Define every KPI precisely before computing it: which users count, which time zone, are refunds removed? Two teams with different definitions will "disagree" about the same data.</p>
""", practice=["ARPU and ARPPU", "Customer Lifetime Value", "Repeat Purchase Rate", "Month-over-Month Growth", "Stickiness: DAU / MAU"])

LESSON("Core", "Funnels, cohorts and churn", """
<p>A <b>funnel</b> counts users at each step (visit → cart → buy) and shows where they drop off. The step with the biggest drop is where to dig.</p>
<p>A <b>cohort</b> is a group that started at the same time (signed up in January). A <b>retention table</b> has cohorts as rows and months since start as columns; each cell is the share still active. Reading down a column compares cohorts — are newer users sticking better? Reading across a row shows how one cohort decays.</p>
<p><b>Churn</b> is the share of last period's active users who didn't come back. Monthly churn of 5% means an average lifetime of about 1 / 0.05 = 20 months.</p>
""", practice=["Conversion Funnel", "Cohort Retention Table", "Monthly Churn Rate"])


@LD
def cohort_heatmap():
    df = ORDERS.copy()
    p = pd.PeriodIndex(df["month"], freq="M")
    df["cohort"] = p.to_series(index=df.index).groupby(df["user"]).transform("min")
    df["offset"] = (p - pd.PeriodIndex(df["cohort"], freq="M")).map(lambda d: d.n)
    t = df.pivot_table(index="cohort", columns="offset", values="user", aggfunc="nunique")
    t = t.div(t[0], axis=0) * 100
    fig, ax = plt.subplots(figsize=(4.5, 2.4))
    ax.imshow(t.to_numpy(dtype=float), cmap="Greens", vmin=0, vmax=100)
    ax.set_xticks(range(len(t.columns)), [f"month {c}" for c in t.columns])
    ax.set_yticks(range(len(t.index)), [str(c) for c in t.index])
    ax.set_title("Retention % by cohort")


LESSON("Advanced", "Explaining a change, and telling the story", """
<p>"Revenue fell 76% in March — why?" Break the change into parts: by segment, by region, by new vs returning users, and by <b>volume × price</b> (fewer orders, or smaller ones?). Sort the parts by absolute change; usually one or two explain most of it. Check the boring causes first: a missing day of data, a tracking change, a holiday.</p>
<p><b>Data storytelling</b> turns analysis into a decision:</p>
<ol>
<li><b>Lead with the answer</b>: "March revenue fell because two Business accounts didn't reorder."</li>
<li><b>One chart, one message</b>, and the title states the message, not "Revenue by month".</li>
<li><b>Make it easy to read</b>: sort bars, group small categories into "Other", label directly instead of a legend, highlight the one bar that matters and grey the rest.</li>
<li><b>Say what to do next</b> and how sure you are.</li>
</ol>
<p><b>Dashboards</b> (Power BI, Tableau, Looker, or Python tools like Streamlit) show the same KPIs every day. Their skills are the same as here — clean data, precise KPI definitions, the right chart — plus point-and-click building. The tools themselves are best learned hands-on with their free desktop versions; everything they compute, you can now compute in pandas.</p>
""", practice=["What Drove the Change?", "The 80/20 Check", "Top N and 'Other'"])


@LD
def story_chart():
    rev = ORDERS.groupby("month")["amount"].sum()
    colors = ["#cbd5e1"] * len(rev)
    colors[-1] = "#b45309"
    fig, ax = plt.subplots(figsize=(4.5, 2.6))
    ax.bar(rev.index, rev.values, color=colors)
    for x, v in zip(rev.index, rev.values):
        ax.text(x, v, f"{v:,.0f}", ha="center", va="bottom")
    ax.set_title("March revenue fell 76%: Business didn't reorder")
    ax.spines[["top", "right"]].set_visible(False)
