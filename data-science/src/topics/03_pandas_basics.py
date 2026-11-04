from lib import *
import io
import pandas as pd

TOPIC(
    id="pandas-basics", title="Pandas Basics", glyph="DataFrame",
    blurb="Series and DataFrames: building tables, selecting columns and rows, filtering, sorting and adding columns.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import pandas as pd
df = pd.DataFrame({"name": ["Ana", "Ben"], "score": [82, 67]})
df = pd.read_csv("file.csv")
df.shape, df.columns, df.dtypes, df.head(), df.info(), df.describe()
df["score"]                       # one column → Series
df[["name", "score"]]             # several columns → DataFrame
df.loc[row_label, "col"]          # by label
df.iloc[0, 1]                     # by position
df[df["score"] &gt; 70]              # filter rows
df.sort_values("score", ascending=False)
df["passed"] = df["score"] &gt;= 40  # new column
df["city"].value_counts()</code></pre>
""")

STUDENTS = {"name": ["Ana", "Ben", "Cy", "Dia"], "score": [82, 45, 67, 91], "city": ["Pune", "Delhi", "Pune", "Goa"]}


Q(None, "Rows and Columns", "Easy", "DataFrame · shape",
  "Build a table from a dict of equal-length lists and return <code>(rows, columns)</code>.",
  [((STUDENTS,), (4, 3)), (({"a": [1]},), (1, 1))],
  ("Count the keys for columns and the length of any list for rows.", "O(1)", "O(1)"),
  ("Create a DataFrame and read <code>df.shape</code>.", "O(n)", "O(n)"))


@B
def table_shape(data):
    cols = len(data)
    rows = len(next(iter(data.values())))
    return (rows, cols)


@O
def table_shape(data):
    df = pd.DataFrame(data)
    return df.shape


Q(None, "Column Names", "Easy", "df.columns",
  "Return the column names of a table given as a list of row dicts, in first-seen order.",
  [(([{"a": 1, "b": 2}, {"a": 3, "c": 4}],), ["a", "b", "c"]), (([{"x": 1}],), ["x"])],
  ("Walk every row and remember keys you haven't seen.", "O(cells)", "O(cols)"),
  ("<code>pd.DataFrame(rows).columns</code> — pandas aligns the keys for you (missing cells become NaN).", "O(cells)", "O(cells)"))


@B
def column_names(rows):
    names = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


@O
def column_names(rows):
    df = pd.DataFrame(rows)
    return df.columns.tolist()


Q(None, "Pick a Column", "Easy", "df[col] → Series",
  "Return the values of one column as a list.",
  [((STUDENTS, "score"), [82, 45, 67, 91]), ((STUDENTS, "city"), ["Pune", "Delhi", "Pune", "Goa"])],
  ("Just take the list from the dict (or loop over row dicts).", "O(n)", "O(n)"),
  ("<code>df[col]</code> gives a Series; <code>.tolist()</code> turns it into a list.", "O(n)", "O(n)"),
  viz=(STUDENTS, "score"))


@B
def column_values(data, col):
    rows = [dict(zip(data, values)) for values in zip(*data.values())]
    return [row[col] for row in rows]


@O
def column_values(data, col):
    df = pd.DataFrame(data)
    return df[col].tolist()


Q(None, "Pick Several Columns", "Easy", "df[[...]]",
  "Return a table with only the requested columns, in the requested order.",
  [((STUDENTS, ["city", "name"]), {"city": ["Pune", "Delhi", "Pune", "Goa"], "name": ["Ana", "Ben", "Cy", "Dia"]})],
  ("Build a new dict with just those keys.", "O(n)", "O(n)"),
  ("Double brackets select a list of columns: <code>df[['city', 'name']]</code>.", "O(n)", "O(n)"),
  viz=(STUDENTS, ["city", "name"]))


@B
def some_columns(data, cols):
    out = {}
    for c in cols:
        out[c] = list(data[c])
    return out


@O
def some_columns(data, cols):
    df = pd.DataFrame(data)
    return df[cols]


Q(None, "Filter Rows", "Easy", "Boolean filtering",
  "Return the names of everyone with a score above <code>cut</code>.",
  [((STUDENTS, 60), ["Ana", "Cy", "Dia"]), ((STUDENTS, 95), [])],
  ("Loop over positions and test each score.", "O(n)", "O(n)"),
  ("A boolean Series selects rows: <code>df.loc[df['score'] &gt; cut, 'name']</code>.", "O(n)", "O(n)"),
  viz=(STUDENTS, 60))


@B
def above(data, cut):
    out = []
    for i in range(len(data["name"])):
        if data["score"][i] > cut:
            out.append(data["name"][i])
    return out


@O
def above(data, cut):
    df = pd.DataFrame(data)
    return df.loc[df["score"] > cut, "name"].tolist()


Q(None, "Top n by Score", "Easy", "sort_values / nlargest",
  "Return the names of the n highest scorers, best first.",
  [((STUDENTS, 2), ["Dia", "Ana"]), ((STUDENTS, 1), ["Dia"])],
  ("Zip names with scores, sort by score descending, take n.", "O(n log n)", "O(n)"),
  ("<code>df.nlargest(n, 'score')['name']</code>.", "O(n log n)", "O(n)"),
  viz=(STUDENTS, 2))


@B
def top_n(data, n):
    pairs = list(zip(data["score"], data["name"]))
    pairs.sort(reverse=True)
    return [name for score, name in pairs[:n]]


@O
def top_n(data, n):
    df = pd.DataFrame(data)
    return df.nlargest(n, "score")["name"].tolist()


Q(None, "Add a Computed Column", "Easy", "Vectorised column maths",
  "Add a column <code>total = price × qty</code> and return the table.",
  [(({"item": ["pen", "ink"], "price": [10, 25], "qty": [3, 2]},), {"item": ["pen", "ink"], "price": [10, 25], "qty": [3, 2], "total": [30, 50]})],
  ("Loop over positions computing each total.", "O(n)", "O(n)"),
  ("<code>df['total'] = df['price'] * df['qty']</code> — whole columns at once.", "O(n)", "O(n)"),
  viz=({"item": ["pen", "ink", "cap"], "price": [10, 25, 5], "qty": [3, 2, 4]},))


@B
def with_total(data):
    out = {k: list(v) for k, v in data.items()}
    out["total"] = []
    for i in range(len(out["price"])):
        out["total"].append(out["price"][i] * out["qty"][i])
    return out


@O
def with_total(data):
    df = pd.DataFrame(data)
    df["total"] = df["price"] * df["qty"]
    return df


Q(None, "loc vs iloc", "Medium", "Label vs position",
  "With names as the index, return <code>(score by label name, score at position pos)</code>.",
  [((STUDENTS, "Cy", 0), (67, 82)), ((STUDENTS, "Ana", 3), (82, 91))],
  ("Find the name's position with <code>index()</code>, and index the score list by position.", "O(n)", "O(1)"),
  ("<code>df.loc[name, 'score']</code> uses the index label; <code>df.iloc[pos, col]</code> uses the position.", "O(1) avg", "O(n)"),
  viz=(STUDENTS, "Cy", 0))


@B
def lookups(data, name, pos):
    by_label = data["score"][data["name"].index(name)]
    by_position = data["score"][pos]
    return (by_label, by_position)


@O
def lookups(data, name, pos):
    df = pd.DataFrame(data).set_index("name")
    by_label = df.loc[name, "score"]
    by_position = df.iloc[pos, df.columns.get_loc("score")]
    return (by_label, by_position)


Q(None, "Rename Columns", "Easy", "rename",
  "Rename columns using the mapping (old → new) and return the new column list.",
  [((STUDENTS, {"name": "student", "city": "town"}), ["student", "score", "town"])],
  ("Map each key through the dict by hand.", "O(cols)", "O(cols)"),
  ("<code>df.rename(columns=mapping)</code>.", "O(cols)", "O(n)"))


@B
def renamed(data, mapping):
    return [mapping.get(c, c) for c in data]


@O
def renamed(data, mapping):
    df = pd.DataFrame(data).rename(columns=mapping)
    return df.columns.tolist()


Q(None, "Count Each Category", "Easy", "value_counts",
  "Return how many rows have each city, as {city: count}, most common first.",
  [((STUDENTS,), {"Pune": 2, "Delhi": 1, "Goa": 1})],
  ("Count with a dict, then sort by count.", "O(n log n)", "O(k)"),
  ("<code>df['city'].value_counts()</code>.", "O(n)", "O(k)"),
  viz=(STUDENTS,))


@B
def city_counts(data):
    counts = {}
    for c in data["city"]:
        counts[c] = counts.get(c, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))


@O
def city_counts(data):
    df = pd.DataFrame(data)
    return df["city"].value_counts()


Q(None, "How Many Different Values", "Easy", "nunique",
  "Return the number of distinct values in column <code>col</code>.",
  [((STUDENTS, "city"), 3), ((STUDENTS, "name"), 4)],
  ("Put the values in a set and take its size.", "O(n)", "O(n)"),
  ("<code>df[col].nunique()</code>.", "O(n)", "O(n)"))


@B
def distinct(data, col):
    return len(set(data[col]))


@O
def distinct(data, col):
    return pd.DataFrame(data)[col].nunique()


Q(None, "Quick Summary of a Column", "Easy", "describe / agg",
  "Return {'mean', 'min', 'max'} of the score column (mean rounded to 2).",
  [((STUDENTS,), {"mean": 71.25, "min": 45, "max": 91})],
  ("Compute each statistic by hand.", "O(n)", "O(1)"),
  ("<code>df['score'].agg(['mean', 'min', 'max'])</code>.", "O(n)", "O(1)"))


@B
def score_summary(data):
    s = data["score"]
    return {"mean": round(sum(s) / len(s), 2), "min": min(s), "max": max(s)}


@O
def score_summary(data):
    stats = pd.DataFrame(data)["score"].agg(["mean", "min", "max"])
    return {"mean": round(stats["mean"], 2), "min": stats["min"], "max": stats["max"]}


Q(None, "Read CSV Text", "Easy", "read_csv",
  "Given the text of a CSV file, return <code>(rows, columns, column names)</code>.",
  [(("name,age\nAna,21\nBen,25\n",), (2, 2, ["name", "age"])), (("x\n1\n2\n3\n",), (3, 1, ["x"]))],
  ("Split the text into lines and the first line on commas.", "O(n)", "O(n)"),
  ("<code>pd.read_csv</code> parses it (here from <code>io.StringIO</code>, normally from a file path).", "O(n)", "O(n)"),
  viz=("name,age\nAna,21\nBen,25\n",))


@B
def csv_info(text):
    lines = [l for l in text.strip().split("\n") if l]
    header = lines[0].split(",")
    return (len(lines) - 1, len(header), header)


@O
def csv_info(text):
    import io
    df = pd.read_csv(io.StringIO(text))
    return (len(df), len(df.columns), df.columns.tolist())


Q(None, "Drop a Column", "Easy", "drop",
  "Return the column names after removing <code>col</code>.",
  [((STUDENTS, "city"), ["name", "score"])],
  ("List comprehension over the keys.", "O(cols)", "O(cols)"),
  ("<code>df.drop(columns=col)</code>.", "O(n)", "O(n)"))


@B
def without_column(data, col):
    return [c for c in data if c != col]


@O
def without_column(data, col):
    return pd.DataFrame(data).drop(columns=col).columns.tolist()


Q(None, "Two Conditions", "Medium", "& and |",
  "Count rows where score ≥ <code>cut</code> AND city equals <code>city</code>.",
  [((STUDENTS, 60, "Pune"), 2), ((STUDENTS, 70, "Pune"), 1)],
  ("Loop and test both conditions with <code>and</code>.", "O(n)", "O(1)"),
  ("Combine masks with <code>&amp;</code> (each condition in brackets) and sum the True values.", "O(n)", "O(n)"),
  viz=(STUDENTS, 60, "Pune"))


@B
def count_both(data, cut, city):
    count = 0
    for s, c in zip(data["score"], data["city"]):
        if s >= cut and c == city:
            count += 1
    return count


@O
def count_both(data, cut, city):
    df = pd.DataFrame(data)
    mask = (df["score"] >= cut) & (df["city"] == city)
    return mask.sum()


Q(None, "Rows From a List of Values", "Easy", "isin",
  "Return the names of people living in any of the given cities.",
  [((STUDENTS, ["Goa", "Delhi"]), ["Ben", "Dia"]), ((STUDENTS, []), [])],
  ("Loop and check <code>city in cities</code>.", "O(n·k)", "O(n)"),
  ("<code>df[df['city'].isin(cities)]</code>.", "O(n + k)", "O(n)"))


@B
def in_cities(data, cities):
    return [n for n, c in zip(data["name"], data["city"]) if c in cities]


@O
def in_cities(data, cities):
    df = pd.DataFrame(data)
    return df.loc[df["city"].isin(cities), "name"].tolist()


Q(None, "Letter Grades Column", "Easy", "apply / map",
  "Return the letter grade for every score: ≥ 80 'A', ≥ 60 'B', else 'C'.",
  [((STUDENTS,), ["A", "C", "B", "A"])],
  ("Loop with if/elif.", "O(n)", "O(n)"),
  ("Write a small function and <code>.apply</code> it to the column (or use <code>pd.cut</code>).", "O(n)", "O(n)"),
  viz=(STUDENTS,))


@B
def grades(data):
    out = []
    for s in data["score"]:
        if s >= 80:
            out.append("A")
        elif s >= 60:
            out.append("B")
        else:
            out.append("C")
    return out


@O
def grades(data):
    def letter(s):
        return "A" if s >= 80 else "B" if s >= 60 else "C"
    return pd.DataFrame(data)["score"].apply(letter).tolist()


Q(None, "Best Subject per Student", "Medium", "idxmax(axis=1)",
  "Rows are students, columns are subjects. Return {student: subject with the highest mark}.",
  [(({"name": ["Ana", "Ben"], "maths": [90, 60], "art": [70, 85]},), {"Ana": "maths", "Ben": "art"})],
  ("For each row, loop over subjects and track the best.", "O(rows·cols)", "O(rows)"),
  ("Make names the index and call <code>idxmax(axis=1)</code>.", "O(rows·cols)", "O(rows)"),
  viz=({"name": ["Ana", "Ben", "Cy"], "maths": [90, 60, 75], "art": [70, 85, 80]},))


@B
def best_subject(data):
    subjects = [c for c in data if c != "name"]
    out = {}
    for i, name in enumerate(data["name"]):
        best = subjects[0]
        for s in subjects:
            if data[s][i] > data[best][i]:
                best = s
        out[name] = best
    return out


@O
def best_subject(data):
    df = pd.DataFrame(data).set_index("name")
    return df.idxmax(axis=1)


Q(None, "Sort by Two Columns", "Medium", "sort_values with a list",
  "Sort by city A→Z, then by score high→low; return the names in that order.",
  [((STUDENTS,), ["Ben", "Dia", "Ana", "Cy"])],
  ("<code>sorted</code> with a tuple key (city, −score).", "O(n log n)", "O(n)"),
  ("<code>df.sort_values(['city', 'score'], ascending=[True, False])</code>.", "O(n log n)", "O(n)"))


@B
def sorted_names(data):
    rows = list(zip(data["city"], data["score"], data["name"]))
    rows.sort(key=lambda r: (r[0], -r[1]))
    return [r[2] for r in rows]


@O
def sorted_names(data):
    df = pd.DataFrame(data).sort_values(["city", "score"], ascending=[True, False])
    return df["name"].tolist()


Q(None, "Mean Score per Row Condition", "Easy", "Boolean mask + aggregation",
  "Return the average score of people from <code>city</code>, rounded to 2 decimals (0 if nobody).",
  [((STUDENTS, "Pune"), 74.5), ((STUDENTS, "Oslo"), 0)],
  ("Collect matching scores in a loop, then average.", "O(n)", "O(n)"),
  ("Filter with a mask, take the column and call <code>.mean()</code>.", "O(n)", "O(n)"),
  viz=(STUDENTS, "Pune"))


@B
def city_average(data, city):
    scores = [s for s, c in zip(data["score"], data["city"]) if c == city]
    return round(sum(scores) / len(scores), 2) if scores else 0


@O
def city_average(data, city):
    df = pd.DataFrame(data)
    scores = df.loc[df["city"] == city, "score"]
    return round(scores.mean(), 2) if len(scores) else 0
