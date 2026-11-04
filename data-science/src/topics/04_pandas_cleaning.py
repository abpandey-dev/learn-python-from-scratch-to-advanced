from lib import *
import pandas as pd

TOPIC(
    id="pandas-cleaning", title="Data Cleaning with Pandas", glyph="NaN → ✓",
    blurb="Missing values, duplicates, wrong types, messy text, dates and outliers — getting raw data ready for analysis.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">df.isna().sum()                    # missing per column
df.dropna(), df.dropna(subset=["age"])
df["age"].fillna(df["age"].mean())
df.drop_duplicates()
pd.to_numeric(df["price"], errors="coerce")
df["name"].str.strip().str.lower()
df["phone"].str.replace(r"\\D", "", regex=True)
df["first"] = df["name"].str.split(" ").str[0]
df["date"] = pd.to_datetime(df["date"]); df["date"].dt.month
pd.cut(df["age"], bins=[0, 18, 60, 120], labels=["kid", "adult", "senior"])
df["temp"].ffill(), df["temp"].interpolate()</code></pre>
""")

N = None


Q(None, "Count Missing Values", "Easy", "isna().sum()",
  "Return {column: number of missing (None) values}.",
  [(({"a": [1, N, 3], "b": [N, N, "x"]},), {"a": 1, "b": 2})],
  ("Loop over each column and count the Nones.", "O(cells)", "O(cols)"),
  ("<code>df.isna().sum()</code> — a True/False table summed per column.", "O(cells)", "O(cells)"),
  viz=({"a": [1, N, 3], "b": [N, N, "x"]},))


@B
def missing_counts(data):
    out = {}
    for col, values in data.items():
        out[col] = sum(1 for v in values if v is None)
    return out


@O
def missing_counts(data):
    df = pd.DataFrame(data)
    return df.isna().sum()


Q(None, "Drop Incomplete Rows", "Easy", "dropna",
  "Remove every row that has a missing value; return the remaining names.",
  [(({"name": ["Ana", "Ben", "Cy"], "age": [21, N, 30], "city": ["Pune", "Goa", N]},), ["Ana"])],
  ("Keep row i only if no column has None at i.", "O(cells)", "O(n)"),
  ("<code>df.dropna()</code>.", "O(cells)", "O(n)"),
  viz=({"name": ["Ana", "Ben", "Cy"], "age": [21, N, 30], "city": ["Pune", "Goa", N]},))


@B
def complete_names(data):
    n = len(data["name"])
    keep = []
    for i in range(n):
        if all(data[c][i] is not None for c in data):
            keep.append(data["name"][i])
    return keep


@O
def complete_names(data):
    return pd.DataFrame(data).dropna()["name"].tolist()


Q(None, "Fill Gaps With the Average", "Easy", "fillna(mean)",
  "Replace missing ages with the average of the known ages (rounded to 1 decimal); return the ages.",
  [(({"age": [20, N, 30, N]},), [20.0, 25.0, 30.0, 25.0])],
  ("Average the known values, then rebuild the list.", "O(n)", "O(n)"),
  ("<code>s.fillna(s.mean())</code> — mean skips NaN automatically.", "O(n)", "O(n)"),
  viz=({"age": [20, N, 30, N]},))


@B
def fill_mean(data):
    known = [a for a in data["age"] if a is not None]
    avg = round(sum(known) / len(known), 1)
    return [float(a) if a is not None else avg for a in data["age"]]


@O
def fill_mean(data):
    age = pd.DataFrame(data)["age"]
    return age.fillna(round(age.mean(), 1)).tolist()


Q(None, "Fill Missing Text", "Easy", "fillna(value)",
  "Replace missing cities with 'Unknown'.",
  [(({"city": ["Pune", N, "Goa"]},), ["Pune", "Unknown", "Goa"])],
  ("List comprehension with a condition.", "O(n)", "O(n)"),
  ("<code>df['city'].fillna('Unknown')</code>.", "O(n)", "O(n)"))


@B
def fill_city(data):
    return [c if c is not None else "Unknown" for c in data["city"]]


@O
def fill_city(data):
    return pd.DataFrame(data)["city"].fillna("Unknown").tolist()


Q(None, "Remove Duplicate Rows", "Easy", "drop_duplicates",
  "Remove rows that are exact repeats of an earlier row; return the remaining (name, city) pairs.",
  [(({"name": ["Ana", "Ben", "Ana", "Ana"], "city": ["Pune", "Goa", "Pune", "Goa"]},), [("Ana", "Pune"), ("Ben", "Goa"), ("Ana", "Goa")])],
  ("Keep a set of seen rows (as tuples).", "O(n)", "O(n)"),
  ("<code>df.drop_duplicates()</code> (use <code>subset=</code> to compare only some columns).", "O(n)", "O(n)"),
  viz=({"name": ["Ana", "Ben", "Ana", "Ana"], "city": ["Pune", "Goa", "Pune", "Goa"]},))


@B
def unique_rows(data):
    seen, out = set(), []
    for row in zip(data["name"], data["city"]):
        if row not in seen:
            seen.add(row)
            out.append(row)
    return out


@O
def unique_rows(data):
    df = pd.DataFrame(data).drop_duplicates()
    return list(df.itertuples(index=False, name=None))


Q(None, "Text to Numbers", "Medium", "pd.to_numeric(errors='coerce')",
  "Convert a column of text to numbers; anything that isn't a number becomes missing (None).",
  [(({"price": ["10", "abc", "2.5", ""]},), [10.0, None, 2.5, None])],
  ("try float(...) except ValueError in a loop.", "O(n)", "O(n)"),
  ("<code>pd.to_numeric(s, errors='coerce')</code> turns bad values into NaN.", "O(n)", "O(n)"),
  viz=({"price": ["10", "abc", "2.5", ""]},))


@B
def to_numbers(data):
    out = []
    for v in data["price"]:
        try:
            out.append(float(v))
        except ValueError:
            out.append(None)
    return out


@O
def to_numbers(data):
    return pd.to_numeric(pd.DataFrame(data)["price"], errors="coerce").tolist()


Q(None, "Tidy Up Text", "Easy", ".str accessor",
  "Strip spaces and lower-case every name.",
  [(({"name": ["  Ana ", "BEN", "cY  "]},), ["ana", "ben", "cy"])],
  ("Call strip and lower on each string.", "O(n)", "O(n)"),
  ("The <code>.str</code> accessor applies string methods to the whole column: <code>.str.strip().str.lower()</code>.", "O(n)", "O(n)"))


@B
def tidy_names(data):
    return [n.strip().lower() for n in data["name"]]


@O
def tidy_names(data):
    return pd.DataFrame(data)["name"].str.strip().str.lower().tolist()


Q(None, "Prices From Messy Text", "Medium", "str.replace with regex",
  "Turn strings like '₹1,200' or 'Rs 75' into numbers by removing everything except digits.",
  [(({"price": ["₹1,200", "Rs 75", "300"]},), [1200, 75, 300])],
  ("Keep only digit characters in a loop, then int().", "O(total chars)", "O(n)"),
  ("<code>.str.replace(r'\\D', '', regex=True)</code> deletes every non-digit, then <code>astype(int)</code>.", "O(total chars)", "O(n)"),
  viz=({"price": ["₹1,200", "Rs 75", "300"]},))


@B
def clean_prices(data):
    out = []
    for text in data["price"]:
        digits = "".join(ch for ch in text if ch.isdigit())
        out.append(int(digits))
    return out


@O
def clean_prices(data):
    s = pd.DataFrame(data)["price"]
    return s.str.replace(r"\D", "", regex=True).astype(int).tolist()


Q(None, "Split Full Names", "Medium", "str.split(expand=True)",
  "Split 'First Last' names into two columns; return {'first': […], 'last': […]}.",
  [(({"name": ["Ada Lovelace", "Alan Turing"]},), {"first": ["Ada", "Alan"], "last": ["Lovelace", "Turing"]})],
  ("Split each string and append the parts to two lists.", "O(n)", "O(n)"),
  ("<code>s.str.split(' ', n=1, expand=True)</code> returns a DataFrame of the parts.", "O(n)", "O(n)"),
  viz=({"name": ["Ada Lovelace", "Alan Turing"]},))


@B
def split_names(data):
    first, last = [], []
    for full in data["name"]:
        f, l = full.split(" ", 1)
        first.append(f)
        last.append(l)
    return {"first": first, "last": last}


@O
def split_names(data):
    parts = pd.DataFrame(data)["name"].str.split(" ", n=1, expand=True)
    parts.columns = ["first", "last"]
    return parts


Q(None, "Month From a Date", "Easy", "to_datetime · .dt",
  "Dates are text like '2024-03-15'. Return the month number of each.",
  [(({"date": ["2024-03-15", "2023-12-01"]},), [3, 12])],
  ("Split the text on '-' and read the middle part.", "O(n)", "O(n)"),
  ("<code>pd.to_datetime(s).dt.month</code> — real dates understand any format pandas can parse.", "O(n)", "O(n)"))


@B
def months(data):
    return [int(d.split("-")[1]) for d in data["date"]]


@O
def months(data):
    return pd.to_datetime(pd.DataFrame(data)["date"]).dt.month.tolist()


Q(None, "Days Between Two Dates", "Medium", "Date arithmetic",
  "Return the number of days from <code>start</code> to <code>end</code> for each row.",
  [(({"start": ["2024-01-01", "2024-02-27"], "end": ["2024-01-31", "2024-03-01"]},), [30, 3])],
  ("Use datetime.date.fromisoformat and subtract in a loop.", "O(n)", "O(n)"),
  ("Subtract two datetime columns and read <code>.dt.days</code>.", "O(n)", "O(n)"))


@B
def days_between(data):
    from datetime import date
    out = []
    for s, e in zip(data["start"], data["end"]):
        out.append((date.fromisoformat(e) - date.fromisoformat(s)).days)
    return out


@O
def days_between(data):
    df = pd.DataFrame(data)
    return (pd.to_datetime(df["end"]) - pd.to_datetime(df["start"])).dt.days.tolist()


Q(None, "Recode Categories", "Easy", "map with a dict",
  "Replace short codes with full names using the mapping; unknown codes become 'other'.",
  [(({"code": ["M", "F", "X", "M"]}, {"M": "male", "F": "female"}), ["male", "female", "other", "male"])],
  ("Loop with <code>mapping.get(code, 'other')</code>.", "O(n)", "O(n)"),
  ("<code>s.map(mapping).fillna('other')</code>.", "O(n)", "O(n)"))


@B
def recode(data, mapping):
    return [mapping.get(c, "other") for c in data["code"]]


@O
def recode(data, mapping):
    return pd.DataFrame(data)["code"].map(mapping).fillna("other").tolist()


Q(None, "Age Groups", "Medium", "pd.cut",
  "Label ages: 0–17 'child', 18–59 'adult', 60+ 'senior'.",
  [(({"age": [5, 18, 45, 60, 82]},), ["child", "adult", "adult", "senior", "senior"])],
  ("if/elif in a loop.", "O(n)", "O(n)"),
  ("<code>pd.cut(age, bins=[-1, 17, 59, 200], labels=[…])</code> — bins are (left, right].", "O(n log bins)", "O(n)"),
  viz=({"age": [5, 18, 45, 60, 82]},))


@B
def age_groups(data):
    out = []
    for a in data["age"]:
        if a <= 17:
            out.append("child")
        elif a <= 59:
            out.append("adult")
        else:
            out.append("senior")
    return out


@O
def age_groups(data):
    groups = pd.cut(pd.DataFrame(data)["age"], bins=[-1, 17, 59, 200], labels=["child", "adult", "senior"])
    return groups.astype(str).tolist()


Q(None, "Cap Outliers", "Easy", "clip",
  "Limit incomes to the range [lo, hi] so extreme values don't distort averages.",
  [(({"income": [20, 35, 900, -5]}, 0, 100), [20, 35, 100, 0])],
  ("min/max in a loop.", "O(n)", "O(n)"),
  ("<code>s.clip(lo, hi)</code>.", "O(n)", "O(n)"))


@B
def cap(data, lo, hi):
    return [max(lo, min(v, hi)) for v in data["income"]]


@O
def cap(data, lo, hi):
    return pd.DataFrame(data)["income"].clip(lo, hi).tolist()


Q(None, "Clean Column Names", "Easy", "Renaming with str methods",
  "Turn column names like ' First Name ' into 'first_name' (strip, lower, spaces → _).",
  [(({" First Name ": [1], "AGE": [2], "Home City": [3]},), ["first_name", "age", "home_city"])],
  ("Loop over the names.", "O(cols)", "O(cols)"),
  ("<code>df.columns.str.strip().str.lower().str.replace(' ', '_')</code>.", "O(cols)", "O(cols)"))


@B
def clean_columns(data):
    return [c.strip().lower().replace(" ", "_") for c in data]


@O
def clean_columns(data):
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df.columns.tolist()


Q(None, "Fix Column Types", "Medium", "astype",
  "Convert 'qty' to integers and 'price' to floats; return {column: dtype name}.",
  [(({"qty": ["1", "2"], "price": ["9.5", "3"]},), {"qty": "int64", "price": "float64"})],
  ("Convert every value with int() / float() and report the Python types.", "O(n)", "O(n)"),
  ("<code>df.astype({'qty': 'int64', 'price': 'float64'})</code>, then read <code>df.dtypes</code>.", "O(n)", "O(n)"))


@B
def fixed_types(data):
    qty = [int(v) for v in data["qty"]]
    price = [float(v) for v in data["price"]]
    return {"qty": "int64" if all(isinstance(v, int) for v in qty) else "object",
            "price": "float64" if all(isinstance(v, float) for v in price) else "object"}


@O
def fixed_types(data):
    df = pd.DataFrame(data).astype({"qty": "int64", "price": "float64"})
    return {c: str(t) for c, t in df.dtypes.items()}


Q(None, "Carry the Last Reading Forward", "Easy", "ffill",
  "A sensor sometimes misses a reading (None). Replace each gap with the last known reading.",
  [(({"temp": [21, N, N, 24, N]},), [21.0, 21.0, 21.0, 24.0, 24.0])],
  ("Remember the last real value in a loop.", "O(n)", "O(n)"),
  ("<code>s.ffill()</code> (forward fill).", "O(n)", "O(n)"),
  viz=({"temp": [21, N, N, 24, N]},))


@B
def carry_forward(data):
    out, last = [], None
    for v in data["temp"]:
        if v is not None:
            last = v
        out.append(float(last) if last is not None else None)
    return out


@O
def carry_forward(data):
    return pd.DataFrame(data)["temp"].ffill().tolist()


Q(None, "Find Invalid Emails", "Medium", "str.contains with regex",
  "Return the emails that don't look like 'something@something.something'.",
  [(({"email": ["a@b.com", "bad.mail", "x@y", "z@q.org"]},), ["bad.mail", "x@y"])],
  ("Check with string methods: one '@' and a '.' after it.", "O(total chars)", "O(n)"),
  ("A regular expression with <code>.str.match</code> tests every row at once.", "O(total chars)", "O(n)"))


@B
def invalid_emails(data):
    bad = []
    for e in data["email"]:
        if e.count("@") != 1:
            bad.append(e)
            continue
        user, domain = e.split("@")
        if not user or "." not in domain or domain.startswith(".") or domain.endswith("."):
            bad.append(e)
    return bad


@O
def invalid_emails(data):
    s = pd.DataFrame(data)["email"]
    ok = s.str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    return s[~ok].tolist()


Q(None, "Fill Gaps by Interpolation", "Medium", "interpolate",
  "Fill missing values in a series by drawing a straight line between the known neighbours.",
  [(({"v": [10, N, 30, N, N, 60]},), [10.0, 20.0, 30.0, 40.0, 50.0, 60.0])],
  ("For each gap, find the known values on both sides and divide the difference evenly.", "O(n)", "O(n)"),
  ("<code>s.interpolate()</code> (linear by default).", "O(n)", "O(n)"),
  viz=({"v": [10, N, 30, N, N, 60]},))


@B
def interpolate(data):
    v = list(data["v"])
    known = [i for i, x in enumerate(v) if x is not None]
    for a, b in zip(known, known[1:]):
        step = (v[b] - v[a]) / (b - a)
        for i in range(a + 1, b):
            v[i] = v[a] + step * (i - a)
    return [float(x) for x in v]


@O
def interpolate(data):
    return pd.DataFrame(data)["v"].interpolate().tolist()


Q(None, "Drop Mostly-Empty Columns", "Medium", "dropna(axis=1, thresh=…)",
  "Remove columns where more than half the values are missing; return the remaining column names.",
  [(({"a": [1, 2, 3, 4], "b": [N, N, N, 1], "c": [1, N, 2, N]},), ["a", "c"])],
  ("Count missing values per column and keep the column if missing ≤ half.", "O(cells)", "O(cols)"),
  ("<code>df.dropna(axis=1, thresh=…)</code> keeps columns with at least thresh non-missing values.", "O(cells)", "O(cells)"))


@B
def keep_columns(data):
    out = []
    for col, values in data.items():
        missing = sum(v is None for v in values)
        if missing <= len(values) / 2:
            out.append(col)
    return out


@O
def keep_columns(data):
    df = pd.DataFrame(data)
    return df.dropna(axis=1, thresh=(len(df) + 1) // 2).columns.tolist()
