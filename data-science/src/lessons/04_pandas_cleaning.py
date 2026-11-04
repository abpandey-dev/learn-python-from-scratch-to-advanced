from lib import *
import pandas as pd

LESSON("Basics", "Why clean data?", """
<p>Real data is messy: blank cells, the same customer entered twice, numbers stored as text, "  Pune" and "pune" counted as different cities, dates in strange formats, one salary typed as 9,000,000 by mistake. Analysts often spend most of their time cleaning, because <b>wrong input gives confident-looking wrong answers</b>.</p>
<p>A cleaning checklist:</p>
<ol>
<li>Look: <code>df.info()</code>, <code>df.describe()</code>, <code>df.isna().sum()</code>, <code>df.duplicated().sum()</code>.</li>
<li>Fix types (numbers, dates, categories).</li>
<li>Handle missing values.</li>
<li>Remove duplicates.</li>
<li>Standardise text.</li>
<li>Check ranges and outliers.</li>
</ol>
""")


LESSON("Core", "Missing values", """
<p>pandas marks missing data as <code>NaN</code> (or <code>None</code> / <code>pd.NA</code> / <code>NaT</code> for dates). Most calculations skip them automatically.</p>
<table>
<tr><th>Task</th><th>Code</th></tr>
<tr><td>Find</td><td><code>df.isna()</code>, <code>df.isna().sum()</code>, <code>df[df["age"].isna()]</code></td></tr>
<tr><td>Drop rows</td><td><code>df.dropna()</code>, <code>df.dropna(subset=["age"])</code></td></tr>
<tr><td>Drop columns</td><td><code>df.dropna(axis=1, thresh=n)</code></td></tr>
<tr><td>Fill with a value</td><td><code>df["city"].fillna("Unknown")</code></td></tr>
<tr><td>Fill with a statistic</td><td><code>s.fillna(s.mean())</code>, <code>s.fillna(s.median())</code></td></tr>
<tr><td>Fill from neighbours</td><td><code>s.ffill()</code>, <code>s.bfill()</code>, <code>s.interpolate()</code></td></tr>
</table>
<div class="warn">Dropping rows can bias results if the missing values aren't random. Filling with the mean shrinks the spread. Choose deliberately and say what you did.</div>
""", practice=["Count Missing Values", "Drop Incomplete Rows", "Fill Gaps With the Average", "Fill Missing Text", "Carry the Last Reading Forward", "Fill Gaps by Interpolation", "Drop Mostly-Empty Columns"])


@LD
def missing_demo():
    df = pd.DataFrame({"name": ["Ana", "Ben", "Cy", "Dia"], "age": [21, None, 30, None], "city": ["Pune", None, "Goa", "Pune"]})
    missing = df.isna().sum()
    complete = df.dropna()
    df["age"] = df["age"].fillna(df["age"].mean())
    df["city"] = df["city"].fillna("Unknown")
    print(missing.to_dict(), len(complete))
    print(df)


LESSON("Core", "Types and duplicates", """
<p>Numbers read as text can't be added (<code>"10" + "5"</code> is <code>"105"</code>). Fix types early:</p>
<pre><code class="py">df["qty"] = df["qty"].astype(int)
df["price"] = pd.to_numeric(df["price"], errors="coerce")   # bad values → NaN
df["date"] = pd.to_datetime(df["date"])
df["city"] = df["city"].astype("category")                 # saves memory</code></pre>
<p>Duplicates inflate counts and sums:</p>
<pre><code class="py">df.duplicated().sum()                      # how many repeats
df.drop_duplicates()                       # keep the first occurrence
df.drop_duplicates(subset=["email"])       # same email = same person</code></pre>
""", practice=["Text to Numbers", "Fix Column Types", "Remove Duplicate Rows"])


@LD
def types_demo():
    df = pd.DataFrame({"item": ["pen", "pen", "ink"], "qty": ["3", "3", "2"], "price": ["10", "10", "n/a"]})
    df["qty"] = df["qty"].astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    repeats = df.duplicated().sum()
    df = df.drop_duplicates()
    print(df.dtypes.astype(str).to_dict(), repeats)
    print(df)


LESSON("Core", "Cleaning text with .str", """
<p>The <code>.str</code> accessor applies string methods to a whole column:</p>
<table>
<tr><th>Task</th><th>Code</th></tr>
<tr><td>Trim and normalise case</td><td><code>s.str.strip().str.lower()</code></td></tr>
<tr><td>Replace</td><td><code>s.str.replace(",", "")</code>; with regex: <code>s.str.replace(r"\\D", "", regex=True)</code></td></tr>
<tr><td>Split into columns</td><td><code>s.str.split(" ", n=1, expand=True)</code></td></tr>
<tr><td>Take a piece</td><td><code>s.str[:3]</code>, <code>s.str.split("@").str[1]</code></td></tr>
<tr><td>Test</td><td><code>s.str.contains("pune", case=False)</code>, <code>s.str.match(regex)</code>, <code>s.str.startswith("A")</code></td></tr>
<tr><td>Extract with a pattern</td><td><code>s.str.extract(r"(\\d+)")</code></td></tr>
</table>
<p>Clean column names too: <code>df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")</code>.</p>
""", practice=["Tidy Up Text", "Prices From Messy Text", "Split Full Names", "Find Invalid Emails", "Clean Column Names"])


@LD
def text_demo():
    df = pd.DataFrame({"name": ["  ada LOVELACE", "Alan turing "], "price": ["₹1,200", "Rs 75"]})
    df["name"] = df["name"].str.strip().str.title()
    df["price"] = df["price"].str.replace(r"\D", "", regex=True).astype(int)
    parts = df["name"].str.split(" ", n=1, expand=True)
    df["first"] = parts[0]
    print(df)


LESSON("Advanced", "Dates, categories and outliers", """
<pre><code class="py">d = pd.to_datetime(df["date"])
d.dt.year, d.dt.month, d.dt.day_name()          # parts of a date
(d2 - d1).dt.days                               # durations
df["band"] = pd.cut(df["age"], bins=[0, 17, 59, 120], labels=["child", "adult", "senior"])
df["code"].map({"M": "male", "F": "female"})    # recode
df["income"].clip(lower, upper)                 # cap outliers</code></pre>
<p>Outliers: look at <code>describe()</code> and a box plot. Common rules mark values beyond 1.5 × IQR from the quartiles, or more than 3 standard deviations from the mean (see the Statistics topic). Decide whether they are errors (fix/drop) or real (keep, maybe cap).</p>
""", practice=["Month From a Date", "Days Between Two Dates", "Recode Categories", "Age Groups", "Cap Outliers"])


@LD
def dates_demo():
    df = pd.DataFrame({"start": ["2024-01-01", "2024-02-27"], "end": ["2024-01-31", "2024-03-01"], "age": [15, 64]})
    start = pd.to_datetime(df["start"])
    end = pd.to_datetime(df["end"])
    df["days"] = (end - start).dt.days
    df["month"] = start.dt.month_name()
    df["band"] = pd.cut(df["age"], bins=[0, 17, 59, 120], labels=["child", "adult", "senior"])
    print(df)
