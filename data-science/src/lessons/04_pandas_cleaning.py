from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
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


LESSON("Basics", "How missing values really behave", """
<p>Missing values are quietly treated differently from what you may expect. Take <code>s = pd.Series([1, None, 5])</code>:</p>
<table><tr><th>Code</th><th>Result</th><th>Why</th></tr>
<tr><td><code>s.sum()</code></td><td>6</td><td>skips the gap</td></tr>
<tr><td><code>s.mean()</code></td><td>3</td><td>6 / 2, not 6 / 3</td></tr>
<tr><td><code>s.count()</code></td><td>2</td><td>counts present values</td></tr>
<tr><td><code>len(s)</code></td><td>3</td><td>counts all rows</td></tr>
<tr><td><code>s == None</code></td><td>all False</td><td>never test for gaps this way</td></tr>
<tr><td><code>s.isna()</code></td><td>False, True, False</td><td>the right way</td></tr>
<tr><td>the dtype</td><td>float64</td><td>a gap turned the whole-number column to decimals</td></tr></table>
<p>So if ids suddenly look like 3.0, a gap is probably the reason. <code>convert_dtypes()</code> or the <code>Int64</code> type keeps them whole.</p>
<h4>Ask why it's missing</h4>
<ul><li><b>Random:</b> a form glitch. Filling is fairly safe.</li>
<li><b>Linked to other columns:</b> younger people skip the income question. Fill within groups.</li>
<li><b>Linked to the value itself:</b> very high earners hide their income. Any fill will bias results, so keep a "was missing" flag.</li></ul>
""", practice=["Count Missing Values", "Drop Incomplete Rows"])


@LD
def missing_behaviour():
    s = pd.Series([1, None, 5])
    total = s.sum()
    average = s.mean()
    present = s.count()
    rows = len(s)
    wrong_test = (s == None).sum()
    right_test = s.isna().sum()
    kind = str(s.dtype)


LESSON("Core", "Choosing how to fill gaps, worked", """
<table><tr><th>Situation</th><th>Choice</th></tr>
<tr><td>Very few rows affected</td><td>drop those rows</td></tr>
<tr><td>Numbers, roughly symmetric</td><td>mean</td></tr>
<tr><td>Numbers with outliers</td><td>median</td></tr>
<tr><td>Categories</td><td>most common, or "Unknown"</td></tr>
<tr><td>Time series</td><td>carry forward, or interpolate</td></tr>
<tr><td>Values depend on a group</td><td>the group's own average</td></tr>
<tr><td>Over 60–70% missing</td><td>consider dropping the column</td></tr></table>
<h4>Worked example: group filling</h4>
<table><tr><th>City</th><th>Rent</th><th>Global mean fill</th><th>Group mean fill</th></tr>
<tr><td>Pune</td><td>10</td><td>10</td><td>10</td></tr>
<tr><td>Pune</td><td>missing</td><td>20</td><td><b>15</b></td></tr>
<tr><td>Pune</td><td>20</td><td>20</td><td>20</td></tr>
<tr><td>Delhi</td><td>30</td><td>30</td><td>30</td></tr>
<tr><td>Delhi</td><td>missing</td><td>20</td><td><b>30</b></td></tr></table>
<p>The global mean (20) gives a Delhi flat a Pune-like price. The group mean respects the difference:</p>
<pre><code class="py">df["rent"].fillna(df.groupby("city")["rent"].transform("mean"))</code></pre>
<p><b>Filling shrinks the spread,</b> since many rows get the same value, and can make relationships look different. Note how much you filled when you report results.</p>
""", practice=["Fill Gaps With the Average", "Fill Missing Text", "Carry the Last Reading Forward", "Fill Gaps by Interpolation", "Drop Mostly-Empty Columns"])


@LD
def group_fill():
    df = pd.DataFrame({"city": ["Pune", "Pune", "Pune", "Delhi", "Delhi"], "rent": [10, None, 20, 30, None]})
    global_mean = df["rent"].mean()
    global_filled = df["rent"].fillna(global_mean)
    group_means = df.groupby("city")["rent"].transform("mean")
    group_filled = df["rent"].fillna(group_means)


LESSON("Core", "Outliers: find them, then decide", """
<h4>Find them with the IQR rule</h4>
<p>Values: 10, 12, 13, 14, 15, 16, 100.</p>
<ol><li>Q1 = 12.5 and Q3 = 15.5, so IQR = 3.</li>
<li>Lower fence: 12.5 − 1.5 × 3 = 8. Upper fence: 15.5 + 1.5 × 3 = 20.</li>
<li>100 is outside the fences, so it's flagged.</li></ol>
<p>One value drags the mean from 13.33 up to <b>25.71</b>, while the median is just 14.</p>
<h4>Then decide, don't just delete</h4>
<table><tr><th>What it is</th><th>What to do</th></tr>
<tr><td>Data entry error (age 200)</td><td>fix it, or set it to missing</td></tr>
<tr><td>Wrong unit (height 170 among values in metres)</td><td>convert</td></tr>
<tr><td>Real but extreme (a billionaire's income)</td><td>keep it; use median or a log transform</td></tr>
<tr><td>Real and it distorts a model</td><td>cap it (<code>clip</code>) and say so</td></tr>
<tr><td>The thing you're looking for (fraud)</td><td><b>definitely keep it</b></td></tr></table>
<p>Always look at flagged rows yourself, and record what you removed and why.</p>
""", practice=["Cap Outliers"])


@LD
def outlier_steps():
    s = pd.Series([10, 12, 13, 14, 15, 16, 100])
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flagged = s[(s < low) | (s > high)]
    mean_with, mean_without, median = s.mean(), s[s <= high].mean(), s.median()
    capped = s.clip(low, high)


LESSON("Advanced", "A complete cleaning walk-through", """
<p>A small, realistically messy table, cleaned in order. The demo runs each step.</p>
<ol><li><b>Column names:</b> lower case, no spaces.</li>
<li><b>Duplicates:</b> remove repeated rows.</li>
<li><b>Text:</b> strip spaces, fix capitals, so " pune" and "PUNE" match.</li>
<li><b>Numbers stored as text:</b> remove "₹" and commas, then <code>pd.to_numeric(errors="coerce")</code> turns anything unreadable into a gap.</li>
<li><b>Dates:</b> <code>pd.to_datetime(errors="coerce")</code>. Check whether 03/04 means March or April: <code>dayfirst=True</code> sets it.</li>
<li><b>Gaps:</b> fill or drop, knowing why.</li>
<li><b>Check the result:</b> shape, types, and <code>describe()</code> again.</li></ol>
<p><b>Why <code>errors="coerce"</code>?</b> It turns bad values into visible gaps you can count, rather than crashing or hiding them. But check how many appeared: a sudden jump means your format assumption was wrong.</p>
<p>Keep cleaning in code, never by editing the file by hand, so it can be rerun on next month's data.</p>
""", practice=["Clean Column Names", "Remove Duplicate Rows", "Tidy Up Text", "Prices From Messy Text", "Fix Column Types", "Text to Numbers", "Month From a Date"])


@LD
def clean_walkthrough():
    raw = pd.DataFrame({"Customer Name": [" ana ", "BEN", "BEN", "cy"], "City": [" pune", "Delhi", "Delhi", "PUNE "], "Price": ["₹1,200", "₹900", "₹900", "n/a"], "Joined": ["2024-01-15", "2024-02-20", "2024-02-20", "bad date"]})
    df = raw.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))
    df = df.drop_duplicates()
    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["city"] = df["city"].str.strip().str.title()
    df["price"] = pd.to_numeric(df["price"].str.replace("₹", "").str.replace(",", ""), errors="coerce")
    df["joined"] = pd.to_datetime(df["joined"], errors="coerce")
    new_gaps = df.isna().sum()
    df["price"] = df["price"].fillna(df["price"].median())
    clean_shape = df.shape
