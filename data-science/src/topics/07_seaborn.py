from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

TOPIC(
    id="seaborn", title="Seaborn", glyph="sns",
    blurb="Statistical charts from DataFrames in one line: distributions, categories, relationships, heat maps and multi-panel grids.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import seaborn as sns
sns.histplot(data=df, x="age", bins=10, hue="sex", kde=True)
sns.kdeplot(data=df, x="age"); sns.ecdfplot(data=df, x="age")
sns.boxplot(data=df, x="day", y="bill"); sns.violinplot(...); sns.stripplot(...)
sns.countplot(data=df, x="day"); sns.barplot(data=df, x="day", y="bill", errorbar=None)
sns.scatterplot(data=df, x="bill", y="tip", hue="sex", size="party")
sns.lineplot(data=df, x="month", y="sales", hue="region")
sns.regplot(data=df, x="bill", y="tip")
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
sns.relplot(..., col="day"); sns.catplot(..., kind="box"); sns.pairplot(df); sns.jointplot(...)
sns.set_theme(style="whitegrid", palette="deep")</code></pre>
""")

SCORES = {"group": ["A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C"],
          "value": [3, 5, 4, 6, 7, 8, 6, 9, 2, 3, 2, 4]}
BILLS = {"bill": [10, 20, 30, 40, 50, 15, 25, 35], "tip": [1.5, 3.0, 4.2, 5.8, 7.1, 2.0, 3.9, 5.0],
         "sex": ["F", "M", "F", "M", "F", "M", "F", "M"]}


def rects(ax):
    from matplotlib.patches import Rectangle
    return [p for p in ax.patches if isinstance(p, Rectangle) and p.get_height() > 0]


def ticks(ax, axis="x"):
    labels = ax.get_xticklabels() if axis == "x" else ax.get_yticklabels()
    return [t.get_text() for t in labels]


Q(None, "Histogram", "Easy", "histplot",
  "Draw a histogram of <code>values</code> with <code>bins</code> bins.",
  [(([1, 2, 2, 3, 3, 3, 4, 4, 5, 5], 4), "4 bars whose heights add up to 10")],
  ("Count values per bin with NumPy and draw bars with Matplotlib.", "O(n)", "O(bins)"),
  ("<code>sns.histplot(x=values, bins=bins)</code>.", "O(n)", "O(bins)"),
  check=lambda a, ax: len(rects(ax)) <= a[1] and round(sum(p.get_height() for p in rects(ax))) == len(a[0]))


@B
def histogram(values, bins):
    counts, edges = np.histogram(values, bins=bins)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(edges[:-1], counts, width=np.diff(edges), align="edge", edgecolor="white")
    ax.set_ylabel("Count")
    return ax


@O
def histogram(values, bins):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(x=values, bins=bins, ax=ax)
    return ax


Q(None, "Smooth Density Curve", "Medium", "kdeplot",
  "Draw a smooth density (KDE) curve of the values.",
  [(([2, 3, 3, 4, 4, 4, 5, 5, 6, 8],), "one smooth curve")],
  ("Add up a Gaussian bump around every value on a grid of x positions (kernel density estimation by hand).", "O(n · grid)", "O(grid)"),
  ("<code>sns.kdeplot(x=values)</code> picks the bandwidth for you.", "O(n · grid)", "O(grid)"),
  check=lambda a, ax: len(ax.lines) >= 1)


@B
def density(values):
    v = np.array(values, dtype=float)
    bw = 1.06 * v.std() * len(v) ** (-1 / 5)
    grid = np.linspace(v.min() - 3 * bw, v.max() + 3 * bw, 200)
    dens = np.exp(-0.5 * ((grid[:, None] - v[None, :]) / bw) ** 2).sum(axis=1)
    dens /= len(v) * bw * np.sqrt(2 * np.pi)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(grid, dens)
    ax.set_ylabel("Density")
    return ax


@O
def density(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.kdeplot(x=values, ax=ax)
    return ax


Q(None, "Box Plot by Group", "Easy", "boxplot",
  "Draw one box of <code>value</code> per <code>group</code>.",
  [((SCORES,), "3 boxes labelled A, B, C")],
  ("Split the values per group yourself and call Matplotlib's boxplot.", "O(n)", "O(n)"),
  ("<code>sns.boxplot(data=df, x='group', y='value')</code> — works directly on the DataFrame columns.", "O(n log n)", "O(n)"),
  check=lambda a, ax: ticks(ax) == ["A", "B", "C"])


@B
def box_by_group(data):
    groups = {}
    for g, v in zip(data["group"], data["value"]):
        groups.setdefault(g, []).append(v)
    names = sorted(groups)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.boxplot([groups[n] for n in names])
    ax.set_xticks(range(1, len(names) + 1), names)
    return ax


@O
def box_by_group(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.boxplot(data=pd.DataFrame(data), x="group", y="value", ax=ax)
    return ax


Q(None, "Violin Plot", "Easy", "violinplot",
  "Draw a violin (box plot + density shape) of value per group.",
  [((SCORES,), "3 violins labelled A, B, C")],
  ("Group values by hand and use Matplotlib's violinplot.", "O(n)", "O(n)"),
  ("<code>sns.violinplot(data=df, x='group', y='value')</code>.", "O(n · grid)", "O(n)"),
  check=lambda a, ax: ticks(ax) == ["A", "B", "C"])


@B
def violins(data):
    groups = {}
    for g, v in zip(data["group"], data["value"]):
        groups.setdefault(g, []).append(v)
    names = sorted(groups)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.violinplot([groups[n] for n in names], showmedians=True)
    ax.set_xticks(range(1, len(names) + 1), names)
    return ax


@O
def violins(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.violinplot(data=pd.DataFrame(data), x="group", y="value", ax=ax)
    return ax


Q(None, "Count Plot", "Easy", "countplot",
  "Draw one bar per category showing how many times it appears.",
  [((["tea", "coffee", "tea", "juice", "tea", "coffee"],), "bars of height 3, 2, 1")],
  ("Count in a dict, then draw bars.", "O(n)", "O(k)"),
  ("<code>sns.countplot(x=items)</code> counts and draws.", "O(n)", "O(k)"),
  check=lambda a, ax: sorted(round(p.get_height()) for p in rects(ax)) == [1, 2, 3])


@B
def count_plot(items):
    counts = {}
    for it in items:
        counts[it] = counts.get(it, 0) + 1
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(list(counts), list(counts.values()))
    ax.set_ylabel("count")
    return ax


@O
def count_plot(items):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(x=items, ax=ax)
    return ax


Q(None, "Bar Plot of Averages", "Easy", "barplot",
  "Draw the mean value per group as bars (no error bars).",
  [((SCORES,), "bars at the group means 4.5, 7.5, 2.75")],
  ("Compute each group's mean in a loop and draw bars.", "O(n)", "O(k)"),
  ("<code>sns.barplot(data=df, x='group', y='value', errorbar=None)</code> aggregates (mean by default).", "O(n)", "O(k)"),
  check=lambda a, ax: sorted(round(p.get_height(), 2) for p in rects(ax)) == [2.75, 4.5, 7.5])


@B
def mean_bars(data):
    sums, counts = {}, {}
    for g, v in zip(data["group"], data["value"]):
        sums[g] = sums.get(g, 0) + v
        counts[g] = counts.get(g, 0) + 1
    names = sorted(sums)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(names, [sums[n] / counts[n] for n in names])
    return ax


@O
def mean_bars(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(data=pd.DataFrame(data), x="group", y="value", errorbar=None, ax=ax)
    return ax


Q(None, "Scatter Coloured by Group", "Easy", "scatterplot(hue=)",
  "Scatter bill vs tip, coloured by sex, with a legend.",
  [((BILLS,), "8 points in 2 colours with a 2-entry legend")],
  ("Loop over groups, scatter each with its own label, then add a legend.", "O(n)", "O(n)"),
  ("<code>sns.scatterplot(data=df, x='bill', y='tip', hue='sex')</code> — colours and legend automatically.", "O(n)", "O(n)"),
  check=lambda a, ax: sum(len(c.get_offsets()) for c in ax.collections) == 8 and ax.get_legend() is not None and len(ax.get_legend().get_texts()) >= 2)


@B
def scatter_hue(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    for sex in sorted(set(data["sex"])):
        xs = [b for b, s in zip(data["bill"], data["sex"]) if s == sex]
        ys = [t for t, s in zip(data["tip"], data["sex"]) if s == sex]
        ax.scatter(xs, ys, label=sex)
    ax.set(xlabel="bill", ylabel="tip")
    ax.legend(title="sex")
    return ax


@O
def scatter_hue(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.scatterplot(data=pd.DataFrame(data), x="bill", y="tip", hue="sex", ax=ax)
    return ax


Q(None, "Lines per Group Over Time", "Medium", "lineplot(hue=)",
  "Draw one line per region of sales over months.",
  [(({"month": [1, 2, 3, 1, 2, 3], "sales": [5, 7, 6, 3, 4, 8], "region": ["N", "N", "N", "S", "S", "S"]},), "2 lines with a legend")],
  ("Filter each region and plot it separately.", "O(n·k)", "O(n)"),
  ("<code>sns.lineplot(data=df, x='month', y='sales', hue='region')</code>.", "O(n)", "O(n)"),
  check=lambda a, ax: len([l for l in ax.lines if len(l.get_xdata()) == 3]) == 2)


@B
def lines_by_region(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    for region in sorted(set(data["region"])):
        months = [m for m, r in zip(data["month"], data["region"]) if r == region]
        sales = [s for s, r in zip(data["sales"], data["region"]) if r == region]
        ax.plot(months, sales, label=region)
    ax.legend(title="region")
    return ax


@O
def lines_by_region(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.lineplot(data=pd.DataFrame(data), x="month", y="sales", hue="region", ax=ax)
    return ax


Q(None, "Correlation Heat Map", "Medium", "heatmap(annot=True)",
  "Draw the correlation matrix of the numeric columns as a heat map with the numbers written in each cell.",
  [(({"a": [1, 2, 3, 4], "b": [2, 4, 5, 8], "c": [4, 3, 2, 1]},), "3 × 3 coloured grid with 9 numbers")],
  ("imshow the matrix and loop over cells writing each number with ax.text.", "O(k²)", "O(k²)"),
  ("<code>sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)</code>.", "O(n·k²)", "O(k²)"),
  check=lambda a, ax: len([t for t in ax.texts if t.get_text().strip()]) == 9)


@B
def corr_heatmap(data):
    df = pd.DataFrame(data)
    corr = df.corr().values
    fig, ax = plt.subplots(figsize=(4, 3.2))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center")
    ax.set_xticks(range(len(df.columns)), df.columns)
    ax.set_yticks(range(len(df.columns)), df.columns)
    fig.colorbar(im)
    return ax


@O
def corr_heatmap(data):
    fig, ax = plt.subplots(figsize=(4, 3.2))
    sns.heatmap(pd.DataFrame(data).corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    return ax


Q(None, "Scatter With a Trend Line", "Medium", "regplot",
  "Scatter bill vs tip and add the best-fit straight line.",
  [((BILLS,), "8 points and a fitted line")],
  ("Fit the line with <code>np.polyfit</code> and plot it over the scatter.", "O(n)", "O(n)"),
  ("<code>sns.regplot(data=df, x='bill', y='tip')</code> — also shades a confidence band.", "O(n · boot)", "O(n)"),
  check=lambda a, ax: len(ax.lines) >= 1 and sum(len(c.get_offsets()) for c in ax.collections if c.get_offsets().shape[0] == 8) == 8)


@B
def trend_line(data):
    slope, intercept = np.polyfit(data["bill"], data["tip"], 1)
    xs = np.linspace(min(data["bill"]), max(data["bill"]), 50)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(data["bill"], data["tip"])
    ax.plot(xs, slope * xs + intercept, color="C1")
    return ax


@O
def trend_line(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.regplot(data=pd.DataFrame(data), x="bill", y="tip", ax=ax, seed=0, n_boot=200)
    return ax


Q(None, "Strip Plot", "Easy", "stripplot",
  "Show every individual value per group as a jittered dot.",
  [((SCORES,), "12 dots in 3 columns")],
  ("Add a small random horizontal jitter to each group's x position and scatter.", "O(n)", "O(n)"),
  ("<code>sns.stripplot(data=df, x='group', y='value', jitter=True)</code>.", "O(n)", "O(n)"),
  check=lambda a, ax: sum(len(c.get_offsets()) for c in ax.collections) == 12)


@B
def strip(data):
    rng = np.random.default_rng(0)
    names = sorted(set(data["group"]))
    fig, ax = plt.subplots(figsize=(5, 3))
    for i, n in enumerate(names):
        ys = [v for g, v in zip(data["group"], data["value"]) if g == n]
        ax.scatter(i + rng.uniform(-0.1, 0.1, len(ys)), ys)
    ax.set_xticks(range(len(names)), names)
    return ax


@O
def strip(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.stripplot(data=pd.DataFrame(data), x="group", y="value", jitter=0.1, ax=ax)
    return ax


Q(None, "Point Plot of Means", "Medium", "pointplot",
  "Show each group's mean as a point, joined by a line.",
  [((SCORES,), "3 points joined by a line")],
  ("Compute means per group and plot them with markers.", "O(n)", "O(k)"),
  ("<code>sns.pointplot(data=df, x='group', y='value', errorbar=None)</code>.", "O(n)", "O(k)"),
  check=lambda a, ax: any(len(l.get_xdata()) == 3 for l in ax.lines))


@B
def point_means(data):
    names = sorted(set(data["group"]))
    means = []
    for n in names:
        vals = [v for g, v in zip(data["group"], data["value"]) if g == n]
        means.append(sum(vals) / len(vals))
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(names, means, marker="o")
    return ax


@O
def point_means(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.pointplot(data=pd.DataFrame(data), x="group", y="value", errorbar=None, ax=ax)
    return ax


Q(None, "Stacked Histogram by Group", "Medium", "histplot(hue=, multiple='stack')",
  "Draw a histogram of value with groups stacked on top of each other (4 shared bins).",
  [((SCORES,), "stacked bars whose heights add up to 12")],
  ("np.histogram per group with shared edges, then stacked bars with bottom=.", "O(n · k)", "O(bins · k)"),
  ("<code>sns.histplot(data=df, x='value', hue='group', multiple='stack', bins=4)</code>.", "O(n)", "O(bins · k)"),
  check=lambda a, ax: round(sum(p.get_height() for p in rects(ax))) == 12)


@B
def stacked_hist(data):
    edges = np.histogram_bin_edges(data["value"], bins=4)
    bottom = np.zeros(4)
    fig, ax = plt.subplots(figsize=(5, 3))
    for g in sorted(set(data["group"])):
        vals = [v for gg, v in zip(data["group"], data["value"]) if gg == g]
        counts, _ = np.histogram(vals, bins=edges)
        ax.bar(edges[:-1], counts, width=np.diff(edges), bottom=bottom, align="edge", label=g)
        bottom += counts
    ax.legend()
    return ax


@O
def stacked_hist(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(data=pd.DataFrame(data), x="value", hue="group", multiple="stack", bins=4, ax=ax)
    return ax


Q(None, "Cumulative Distribution (ECDF)", "Medium", "ecdfplot",
  "Draw the empirical cumulative distribution: for each value, the share of data ≤ it.",
  [(([3, 1, 4, 1, 5, 9, 2, 6],), "a step line rising to 1.0")],
  ("Sort the values and step up by 1/n at each one.", "O(n log n)", "O(n)"),
  ("<code>sns.ecdfplot(x=values)</code>.", "O(n log n)", "O(n)"),
  check=lambda a, ax: len(ax.lines) >= 1 and round(max(max(l.get_ydata()) for l in ax.lines), 6) == 1.0)


@B
def ecdf(values):
    xs = sorted(values)
    ys = [(i + 1) / len(xs) for i in range(len(xs))]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.step(xs, ys, where="post")
    ax.set_ylabel("Proportion")
    return ax


@O
def ecdf(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.ecdfplot(x=values, ax=ax)
    return ax


Q(None, "Bars in a Chosen Order", "Easy", "order=",
  "Draw a count plot whose bars follow the given category order.",
  [((["low", "high", "mid", "low", "mid", "low"], ["low", "mid", "high"]), "bars labelled low, mid, high in that order")],
  ("Count, then draw the bars in the requested order by hand.", "O(n)", "O(k)"),
  ("<code>sns.countplot(x=items, order=order)</code>.", "O(n)", "O(k)"),
  check=lambda a, ax: ticks(ax) == a[1])


@B
def ordered_counts(items, order):
    counts = {k: 0 for k in order}
    for it in items:
        counts[it] += 1
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(order, [counts[k] for k in order])
    return ax


@O
def ordered_counts(items, order):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(x=items, order=order, ax=ax)
    return ax


Q(None, "One Panel per Category", "Medium", "relplot(col=)",
  "Draw bill vs tip in a separate panel for each sex. Return the Figure.",
  [((BILLS,), "a figure with 2 panels")],
  ("plt.subplots(1, k) and loop over the groups.", "O(n)", "O(n)"),
  ("Figure-level <code>sns.relplot(..., col='sex')</code> builds the grid (a FacetGrid) for you.", "O(n)", "O(n)"),
  check=lambda a, fig: len(fig.axes) == 2)


@B
def panels(data):
    groups = sorted(set(data["sex"]))
    fig, axes = plt.subplots(1, len(groups), figsize=(7, 3), sharey=True)
    for ax, g in zip(axes, groups):
        xs = [b for b, s in zip(data["bill"], data["sex"]) if s == g]
        ys = [t for t, s in zip(data["tip"], data["sex"]) if s == g]
        ax.scatter(xs, ys)
        ax.set_title(f"sex = {g}")
    return fig


@O
def panels(data):
    g = sns.relplot(data=pd.DataFrame(data), x="bill", y="tip", col="sex", height=3, aspect=1.1)
    return g.figure


Q(None, "Pair Plot", "Medium", "pairplot",
  "Draw scatter plots of every pair of numeric columns, with histograms on the diagonal. Return the Figure.",
  [(({"a": [1, 2, 3, 4, 5], "b": [2, 1, 4, 3, 5], "c": [5, 3, 4, 1, 2]},), "a 3 × 3 grid of panels")],
  ("Nested loops over columns on a k × k grid of subplots.", "O(n · k²)", "O(n)"),
  ("<code>sns.pairplot(df)</code>.", "O(n · k²)", "O(n)"),
  check=lambda a, fig: len(fig.axes) >= 9)


@B
def pairs(data):
    cols = list(data)
    k = len(cols)
    fig, axes = plt.subplots(k, k, figsize=(6, 6))
    for i, ci in enumerate(cols):
        for j, cj in enumerate(cols):
            if i == j:
                axes[i, j].hist(data[ci], bins=5)
            else:
                axes[i, j].scatter(data[cj], data[ci], s=10)
    return fig


@O
def pairs(data):
    g = sns.pairplot(pd.DataFrame(data), height=2)
    return g.figure


Q(None, "Joint Plot", "Hard", "jointplot",
  "Draw a scatter of bill vs tip with each variable's histogram on the top and right margins. Return the Figure.",
  [((BILLS,), "a figure with 3 Axes: the scatter and two margins")],
  ("Lay out three Axes with GridSpec and draw each part.", "O(n)", "O(n)"),
  ("<code>sns.jointplot(data=df, x='bill', y='tip')</code>.", "O(n)", "O(n)"),
  check=lambda a, fig: len(fig.axes) == 3)


@B
def joint(data):
    fig = plt.figure(figsize=(4.5, 4.5))
    grid = fig.add_gridspec(4, 4)
    main = fig.add_subplot(grid[1:, :3])
    top = fig.add_subplot(grid[0, :3], sharex=main)
    right = fig.add_subplot(grid[1:, 3], sharey=main)
    main.scatter(data["bill"], data["tip"])
    top.hist(data["bill"], bins=5)
    right.hist(data["tip"], bins=5, orientation="horizontal")
    return fig


@O
def joint(data):
    g = sns.jointplot(data=pd.DataFrame(data), x="bill", y="tip", height=4.5)
    return g.figure


Q(None, "Totals, Largest First", "Medium", "barplot(estimator=sum, order=…)",
  "Draw horizontal bars of total sales per region, largest at the top.",
  [(({"region": ["N", "S", "N", "E", "S"], "sales": [5, 9, 4, 3, 2]},), "bars 11, 9, 3 from top to bottom")],
  ("Sum per region in a dict, sort, draw with barh.", "O(n log n)", "O(k)"),
  ("Compute the order, then <code>sns.barplot(…, estimator=sum, order=order, errorbar=None)</code>.", "O(n log n)", "O(k)"),
  check=lambda a, ax: sorted([round(p.get_width()) for p in rects(ax)] or [0], reverse=True)[:3] == [11, 9, 3])


@B
def totals_sorted(data):
    totals = {}
    for r, s in zip(data["region"], data["sales"]):
        totals[r] = totals.get(r, 0) + s
    ordered = sorted(totals.items(), key=lambda kv: kv[1])
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh([r for r, _ in ordered], [t for _, t in ordered])
    return ax


@O
def totals_sorted(data):
    df = pd.DataFrame(data)
    order = df.groupby("region")["sales"].sum().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(data=df, y="region", x="sales", estimator="sum", order=order, errorbar=None, ax=ax)
    return ax


Q(None, "Grouped Count Plot", "Medium", "countplot(hue=)",
  "Count rows for each group, split by sex, as side-by-side bars.",
  [(({"group": ["A", "A", "B", "B", "B", "C"], "sex": ["F", "M", "F", "F", "M", "M"]},), "bar heights add up to 6")],
  ("Count (group, sex) pairs, then draw offset bars.", "O(n)", "O(k · h)"),
  ("<code>sns.countplot(data=df, x='group', hue='sex')</code>.", "O(n)", "O(k · h)"),
  check=lambda a, ax: round(sum(p.get_height() for p in rects(ax))) == 6)


@B
def grouped_counts(data):
    groups, sexes = sorted(set(data["group"])), sorted(set(data["sex"]))
    counts = {}
    for g, s in zip(data["group"], data["sex"]):
        counts[(g, s)] = counts.get((g, s), 0) + 1
    fig, ax = plt.subplots(figsize=(5, 3))
    width = 0.8 / len(sexes)
    for k, s in enumerate(sexes):
        xs = [i - 0.4 + width * (k + 0.5) for i in range(len(groups))]
        ax.bar(xs, [counts.get((g, s), 0) for g in groups], width=width, label=s)
    ax.set_xticks(range(len(groups)), groups)
    ax.legend(title="sex")
    return ax


@O
def grouped_counts(data):
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.countplot(data=pd.DataFrame(data), x="group", hue="sex", ax=ax)
    return ax
