from lib import *
import io
import pandas as pd

LESSON("Basics", "Series and DataFrame", """
<p>Pandas adds two labelled data structures on top of NumPy:</p>
<ul>
<li>A <b>Series</b> is a single column: values plus an <b>index</b> (the row labels).</li>
<li>A <b>DataFrame</b> is a table: several Series sharing the same index, one per column. Each column has its own dtype.</li>
</ul>
<pre><code class="py">import pandas as pd
s = pd.Series([82, 45, 67], index=["Ana", "Ben", "Cy"])
df = pd.DataFrame({"name": ["Ana", "Ben", "Cy"],
                   "score": [82, 45, 67]})</code></pre>
<p>In the animations, DataFrames are drawn as tables with the index on the left and column names on top; a Series is drawn as a row of boxes with its index under each value.</p>
""", practice=["Rows and Columns", "Column Names"])


@LD
def structures_demo():
    s = pd.Series([82, 45, 67], index=["Ana", "Ben", "Cy"])
    df = pd.DataFrame({"name": ["Ana", "Ben", "Cy"], "score": [82, 45, 67]})
    print(s["Ben"], df.shape, list(df.columns))
    print(df)


LESSON("Basics", "Loading and looking at data", """
<p>Real data usually comes from a file: <code>pd.read_csv("sales.csv")</code>, <code>pd.read_excel</code>, <code>pd.read_json</code>, <code>pd.read_sql</code>. Then look before you analyse:</p>
<table>
<tr><th>Call</th><th>Shows</th></tr>
<tr><td><code>df.head(5)</code> / <code>df.tail()</code></td><td>first / last rows</td></tr>
<tr><td><code>df.shape</code></td><td>(rows, columns)</td></tr>
<tr><td><code>df.columns</code>, <code>df.dtypes</code></td><td>column names and types</td></tr>
<tr><td><code>df.info()</code></td><td>types, non-null counts, memory</td></tr>
<tr><td><code>df.describe()</code></td><td>count, mean, std, min, quartiles, max of numeric columns</td></tr>
<tr><td><code>df["col"].value_counts()</code></td><td>frequency of each category</td></tr>
</table>
""", practice=["Read CSV Text", "Quick Summary of a Column", "Count Each Category", "How Many Different Values"])


@LD
def loading_demo():
    text = "name,city,score\nAna,Pune,82\nBen,Delhi,45\nCy,Pune,67\n"
    df = pd.read_csv(io.StringIO(text))
    summary = df["score"].describe().round(1)
    counts = df["city"].value_counts()
    print(df.head(2))
    print(summary["mean"], summary["max"], counts["Pune"])


LESSON("Core", "Selecting columns and rows", """
<table>
<tr><th>Code</th><th>Selects</th></tr>
<tr><td><code>df["score"]</code></td><td>one column (Series)</td></tr>
<tr><td><code>df[["name", "score"]]</code></td><td>several columns (DataFrame)</td></tr>
<tr><td><code>df.loc[label]</code>, <code>df.loc[label, "col"]</code></td><td>by index <b>label</b></td></tr>
<tr><td><code>df.iloc[0]</code>, <code>df.iloc[0, 1]</code>, <code>df.iloc[:3]</code></td><td>by <b>position</b></td></tr>
<tr><td><code>df.loc[2:4]</code></td><td>labels 2 to 4 <b>inclusive</b></td></tr>
<tr><td><code>df.iloc[2:4]</code></td><td>positions 2 and 3 (end excluded, like Python)</td></tr>
</table>
<p><code>set_index("name")</code> makes a column the index, so <code>df.loc["Ana"]</code> finds Ana's row.</p>
""", practice=["Pick a Column", "Pick Several Columns", "loc vs iloc", "Rename Columns", "Drop a Column"])


@LD
def selecting_demo():
    df = pd.DataFrame({"name": ["Ana", "Ben", "Cy"], "score": [82, 45, 67], "city": ["Pune", "Delhi", "Pune"]})
    scores = df["score"]
    two_cols = df[["name", "city"]]
    by_name = df.set_index("name")
    ben = by_name.loc["Ben", "score"]
    first_row = df.iloc[0]
    print(ben, first_row["name"], two_cols.shape)


LESSON("Core", "Filtering and sorting", """
<p>A comparison on a column gives a boolean Series (a <b>mask</b>); indexing with it keeps the matching rows:</p>
<pre><code class="py">df[df["score"] &gt; 60]
df[(df["score"] &gt; 60) &amp; (df["city"] == "Pune")]   # and → &amp;, or → |, not → ~
df[df["city"].isin(["Pune", "Goa"])]
df.query("score &gt; 60 and city == 'Pune'")         # same, as a string
df.sort_values("score", ascending=False)
df.sort_values(["city", "score"], ascending=[True, False])
df.nlargest(3, "score")</code></pre>
""", practice=["Filter Rows", "Two Conditions", "Rows From a List of Values", "Top n by Score", "Sort by Two Columns", "Mean Score per Row Condition"])


@LD
def filtering_demo():
    df = pd.DataFrame({"name": ["Ana", "Ben", "Cy", "Dia"], "score": [82, 45, 67, 91], "city": ["Pune", "Delhi", "Pune", "Goa"]})
    mask = (df["score"] > 60) & (df["city"] == "Pune")
    pune_good = df[mask]
    ranked = df.sort_values("score", ascending=False)
    print(pune_good["name"].tolist(), ranked["name"].tolist())


LESSON("Advanced", "New columns, apply and the index", """
<p>Create or overwrite a column by assigning to it — the maths runs on whole columns at once:</p>
<pre><code class="py">df["total"] = df["price"] * df["qty"]
df["passed"] = df["score"] &gt;= 40
df["grade"] = df["score"].apply(lambda s: "A" if s &gt;= 80 else "B")
df["city"] = df["city"].map({"Pune": "PN", "Goa": "GA"})
df = df.assign(bonus=df["score"] * 0.1)</code></pre>
<p>Prefer vectorised column maths; <code>apply</code> with a Python function runs a loop under the hood and is slower.</p>
<p>The <b>index</b> labels rows. Operations between Series <b>align on the index</b>, not on position — a common source of surprising NaNs. <code>reset_index()</code> turns the index back into a column.</p>
""", practice=["Add a Computed Column", "Letter Grades Column", "Best Subject per Student"])


@LD
def new_columns_demo():
    df = pd.DataFrame({"item": ["pen", "ink", "cap"], "price": [10, 25, 5], "qty": [3, 2, 4]})
    df["total"] = df["price"] * df["qty"]
    df["big"] = df["total"] >= 40
    df["label"] = df["item"].apply(str.upper)
    a = pd.Series([1, 2], index=["x", "y"])
    b = pd.Series([10, 20], index=["y", "z"])
    print(df)
    print(a + b)
