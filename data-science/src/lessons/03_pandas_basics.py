from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
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


LESSON("Basics", "A first look at any new dataset", """
<p>Run the same few checks every time, before any analysis:</p>
<table><tr><th>Code</th><th>Answers</th></tr>
<tr><td><code>df.shape</code></td><td>how many rows and columns?</td></tr>
<tr><td><code>df.head()</code></td><td>what does a row look like?</td></tr>
<tr><td><code>df.dtypes</code></td><td>are numbers stored as numbers? Is any date stored as text?</td></tr>
<tr><td><code>df.isna().sum()</code></td><td>where are the gaps?</td></tr>
<tr><td><code>df.describe()</code></td><td>any impossible values, such as age 300?</td></tr>
<tr><td><code>df["city"].value_counts()</code></td><td>are categories spelled consistently?</td></tr>
<tr><td><code>df.duplicated().sum()</code></td><td>any repeated rows?</td></tr></table>
<h4>What the demo's data reveals</h4>
<ul><li><code>price</code> has one gap.</li>
<li><code>describe</code> shows a max age of 200, which must be an error.</li>
<li>"pune" and "Pune" count as two cities.</li></ul>
<p>Five minutes here prevents wrong conclusions later.</p>
""", practice=["Rows and Columns", "Quick Summary of a Column", "Count Each Category", "How Many Different Values"])


@LD
def first_look():
    df = pd.DataFrame({"city": ["Pune", "pune", "Delhi", "Pune"], "age": [25, 31, 200, 40], "price": [100.0, None, 300.0, 150.0]})
    shape = df.shape
    gaps = df.isna().sum()
    summary = df["age"].describe()
    cities = df["city"].value_counts()
    fixed_cities = df["city"].str.title().value_counts()


LESSON("Core", "loc vs iloc: labels vs positions", """
<p>A DataFrame has labels (the index) and positions (0, 1, 2…). They look alike until they differ.</p>
<pre><code class="py">df = pd.DataFrame({"score": [50, 60, 70]}, index=[10, 20, 30])</code></pre>
<table><tr><th>Code</th><th>Means</th><th>Rows returned</th></tr>
<tr><td><code>df.loc[10:20]</code></td><td>labels 10 to 20, <b>end included</b></td><td>50, 60</td></tr>
<tr><td><code>df.iloc[0:2]</code></td><td>positions 0 and 1, <b>end excluded</b></td><td>50, 60</td></tr>
<tr><td><code>df.loc[20, "score"]</code></td><td>label 20, column score</td><td>60</td></tr>
<tr><td><code>df.iloc[1, 0]</code></td><td>row position 1, column position 0</td><td>60</td></tr></table>
<h4>The trap after filtering</h4>
<p>Filtering keeps the original labels. After <code>high = df[df.score &gt; 50]</code>, the labels are 20 and 30. So <code>high.loc[10]</code> fails, while <code>high.iloc[0]</code> gives the first remaining row.</p>
<p>Use <code>.reset_index(drop=True)</code> to renumber from 0.</p>
<p><b>Rule of thumb:</b> use <code>loc</code> with column names and conditions. Use <code>iloc</code> only for "the first 5 rows".</p>
""", practice=["loc vs iloc", "Pick a Column", "Pick Several Columns"])


@LD
def loc_iloc_demo():
    df = pd.DataFrame({"score": [50, 60, 70]}, index=[10, 20, 30])
    by_label = df.loc[10:20]
    by_position = df.iloc[0:2]
    high = df[df["score"] > 50]
    first_remaining = high.iloc[0]
    renumbered = high.reset_index(drop=True)


LESSON("Core", "Filtering, step by step", """
<p>A filter is two steps: build a True/False column, then use it to pick rows.</p>
<pre><code class="py">mask = df["score"] &gt; 60        # one True or False per row
df[mask]                       # only the True rows</code></pre>
<table><tr><th>Goal</th><th>Code</th></tr>
<tr><td>Both conditions</td><td><code>df[(df.score &gt; 60) &amp; (df.city == "Pune")]</code></td></tr>
<tr><td>Either condition</td><td><code>df[(df.score &gt; 60) | (df.city == "Pune")]</code></td></tr>
<tr><td>Not</td><td><code>df[~(df.city == "Pune")]</code></td></tr>
<tr><td>One of several values</td><td><code>df[df.city.isin(["Pune", "Goa"])]</code></td></tr>
<tr><td>A range, ends included</td><td><code>df[df.score.between(60, 80)]</code></td></tr>
<tr><td>Text contains</td><td><code>df[df.name.str.contains("an")]</code></td></tr>
<tr><td>Readable form</td><td><code>df.query("score &gt; 60 and city == 'Pune'")</code></td></tr></table>
<h4>The two most common errors</h4>
<ul><li>Using <code>and</code>/<code>or</code> gives "truth value of a Series is ambiguous". Use <code>&amp;</code> and <code>|</code>.</li>
<li>Leaving out brackets: <code>df.a &gt; 1 &amp; df.b &gt; 2</code> is read as <code>df.a &gt; (1 &amp; df.b) &gt; 2</code>.</li></ul>
""", practice=["Filter Rows", "Two Conditions", "Rows From a List of Values", "Sort by Two Columns", "Top n by Score"])


@LD
def filter_steps():
    df = pd.DataFrame({"name": ["Ana", "Ben", "Cy", "Dee"], "city": ["Pune", "Delhi", "Goa", "Pune"], "score": [72, 45, 90, 58]})
    mask = df["score"] > 60
    high = df[mask]
    both = df[(df["score"] > 50) & (df["city"] == "Pune")]
    listed = df[df["city"].isin(["Pune", "Goa"])]
    in_range = df[df["score"].between(50, 75)]
    readable = df.query("score > 50 and city == 'Pune'")


LESSON("Advanced", "Changing data safely", """
<p>This goes wrong for many beginners:</p>
<pre><code class="py">high = df[df.score &gt; 60]
high["grade"] = "A"        # does this change df? No!</code></pre>
<p>A filtered result is its own table, and changing it doesn't reach back to <code>df</code>. Older pandas warns (<code>SettingWithCopyWarning</code>), and in newer pandas it never changes the original.</p>
<h4>Choose what you mean</h4>
<table><tr><th>You want</th><th>Write</th></tr>
<tr><td>To change the original</td><td><code>df.loc[df.score &gt; 60, "grade"] = "A"</code></td></tr>
<tr><td>A separate table to edit</td><td><code>high = df[df.score &gt; 60].copy()</code></td></tr></table>
<h4>Never chain assignments</h4>
<p><code>df[df.score &gt; 60]["grade"] = "A"</code> does nothing useful. Keep the row condition and the column inside one <code>.loc[...]</code>.</p>
<p>Most methods return a new table: <code>df.sort_values("score")</code> leaves <code>df</code> unchanged until you assign the result back.</p>
""", practice=["Add a Computed Column", "Drop a Column", "Rename Columns"])


@LD
def safe_changes():
    df = pd.DataFrame({"score": [72, 45, 90]})
    high = df[df["score"] > 60].copy()
    high["grade"] = "A"
    original_has_grade = "grade" in df.columns
    df.loc[df["score"] > 60, "grade"] = "A"
    sorted_copy = df.sort_values("score")
    first_row_still = df.iloc[0, 0]


LESSON("Advanced", "Vectorise before you apply", """
<p><code>df.apply</code> runs Python once per row, so it's slow on large tables. Prefer a built-in where one exists.</p>
<table><tr><th>Task</th><th>Slow</th><th>Better</th></tr>
<tr><td>Add columns</td><td><code>apply(lambda r: r.a + r.b, axis=1)</code></td><td><code>df.a + df.b</code></td></tr>
<tr><td>Two outcomes</td><td>a function with if/else</td><td><code>np.where(df.a &gt; 50, "pass", "fail")</code></td></tr>
<tr><td>Many outcomes</td><td>a long if/elif</td><td><code>np.select(conditions, choices)</code> or <code>pd.cut</code></td></tr>
<tr><td>Lookup</td><td>a function with a dict</td><td><code>df.city.map(lookup)</code></td></tr>
<tr><td>Text</td><td><code>apply(lambda s: s.lower())</code></td><td><code>df.name.str.lower()</code></td></tr></table>
<h4>Worked example: grades</h4>
<p>With marks 35, 55, 72, 90, <code>pd.cut(marks, [0, 50, 70, 100], labels=["F", "C", "A"])</code> returns F, C, A, A. Each bin includes its right edge, so a mark of exactly 50 would be F and exactly 70 would be C.</p>
<p>Use <code>apply</code> when the logic really can't be expressed any other way. It's fine on small data.</p>
""", practice=["Letter Grades Column", "Best Subject per Student", "Mean Score per Row Condition"])


@LD
def faster_columns():
    df = pd.DataFrame({"marks": [35, 55, 72, 90], "city": ["P", "D", "P", "G"]})
    two_way = np.where(df["marks"] >= 50, "pass", "fail")
    binned = pd.cut(df["marks"], [0, 50, 70, 100], labels=["F", "C", "A"]).astype(str)
    conditions = [df["marks"] >= 70, df["marks"] >= 50]
    many_way = np.select(conditions, ["A", "C"], default="F")
    looked_up = df["city"].map({"P": "Pune", "D": "Delhi", "G": "Goa"})
