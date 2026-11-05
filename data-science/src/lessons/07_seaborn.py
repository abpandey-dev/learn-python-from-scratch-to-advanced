from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

TIPS = pd.DataFrame({
    "bill": [10, 20, 30, 40, 50, 15, 25, 35, 45, 18, 28, 38],
    "tip": [1.5, 3.0, 4.2, 5.8, 7.1, 2.0, 3.9, 5.0, 6.2, 2.4, 4.0, 5.5],
    "day": ["Sat", "Sun", "Sat", "Sun", "Sat", "Fri", "Fri", "Sun", "Sat", "Fri", "Sun", "Sat"],
    "sex": ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"],
})

LESSON("Basics", "Why Seaborn?", """
<p><b>Seaborn</b> is built on Matplotlib and designed for <b>statistical</b> charts from <b>DataFrames</b>. You name the columns, and Seaborn groups, counts, averages, colours and labels for you:</p>
<pre><code class="py">import seaborn as sns
sns.barplot(data=df, x="day", y="bill")      # mean bill per day, with error bars
sns.scatterplot(data=df, x="bill", y="tip", hue="sex")</code></pre>
<p>The same charts in plain Matplotlib need loops to split groups, compute statistics and build legends — exactly what the "brute force" answers in this topic do. Seaborn functions return a Matplotlib Axes, so you can still customise with <code>ax.set_title(...)</code>.</p>
""", practice=["Bar Plot of Averages", "Scatter Coloured by Group"])


@LD
def why_seaborn():
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.scatterplot(data=TIPS, x="bill", y="tip", hue="sex", ax=ax)
    ax.set_title("Tip vs bill")


LESSON("Basics", "Distributions of one variable", """
<table>
<tr><th>Function</th><th>Shows</th></tr>
<tr><td><code>sns.histplot(data=df, x="bill", bins=10)</code></td><td>counts in bins (add <code>kde=True</code> for a curve)</td></tr>
<tr><td><code>sns.kdeplot(data=df, x="bill")</code></td><td>smooth density estimate</td></tr>
<tr><td><code>sns.ecdfplot(data=df, x="bill")</code></td><td>share of values ≤ x (no binning choices)</td></tr>
<tr><td><code>hue="sex"</code>, <code>multiple="stack" | "dodge" | "fill"</code></td><td>compare groups</td></tr>
</table>
<p>Look for: centre, spread, skew (a long tail on one side), several peaks, and outliers.</p>
""", practice=["Histogram", "Smooth Density Curve", "Cumulative Distribution (ECDF)", "Stacked Histogram by Group"])


@LD
def distributions_demo():
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
    sns.histplot(data=TIPS, x="bill", bins=5, kde=True, ax=left)
    sns.ecdfplot(data=TIPS, x="bill", hue="sex", ax=right)
    fig.tight_layout()


LESSON("Core", "Comparing categories", """
<table>
<tr><th>Function</th><th>Shows per category</th></tr>
<tr><td><code>countplot</code></td><td>number of rows</td></tr>
<tr><td><code>barplot</code></td><td>mean (or <code>estimator="sum"</code>) with a confidence interval (<code>errorbar=None</code> to hide)</td></tr>
<tr><td><code>pointplot</code></td><td>mean as points joined by lines</td></tr>
<tr><td><code>boxplot</code></td><td>median, quartiles, whiskers, outliers</td></tr>
<tr><td><code>violinplot</code></td><td>box plot + density shape</td></tr>
<tr><td><code>stripplot</code> / <code>swarmplot</code></td><td>every individual value</td></tr>
</table>
<p>Control category order with <code>order=[...]</code>, add a second grouping with <code>hue=</code>, and flip to horizontal by swapping x and y.</p>
""", practice=["Count Plot", "Box Plot by Group", "Violin Plot", "Strip Plot", "Point Plot of Means", "Bars in a Chosen Order", "Grouped Count Plot", "Totals, Largest First"])


@LD
def categories_demo():
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
    order = ["Fri", "Sat", "Sun"]
    sns.boxplot(data=TIPS, x="day", y="bill", order=order, ax=left)
    sns.stripplot(data=TIPS, x="day", y="bill", order=order, color="black", size=3, ax=left)
    sns.barplot(data=TIPS, x="day", y="tip", hue="sex", order=order, errorbar=None, ax=right)
    fig.tight_layout()


LESSON("Core", "Relationships between numbers", """
<pre><code class="py">sns.scatterplot(data=df, x="bill", y="tip", hue="day", size="party")
sns.lineplot(data=df, x="month", y="sales", hue="region")   # averages repeated x values + band
sns.regplot(data=df, x="bill", y="tip")                     # scatter + fitted line
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", vmin=-1, vmax=1)</code></pre>
<p>A correlation heat map is the quickest overview of which numeric columns move together (+1), oppositely (−1) or not at all (0).</p>
""", practice=["Lines per Group Over Time", "Scatter With a Trend Line", "Correlation Heat Map"])


@LD
def relationships_demo():
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
    sns.regplot(data=TIPS, x="bill", y="tip", ax=left, seed=0, n_boot=200)
    corr = TIPS[["bill", "tip"]].assign(size=np.arange(len(TIPS)) % 4 + 1).corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=right)
    fig.tight_layout()


LESSON("Advanced", "Figure-level functions and themes", """
<p><b>Axes-level</b> functions (<code>scatterplot</code>, <code>boxplot</code> …) draw on one Axes you pass with <code>ax=</code>. <b>Figure-level</b> functions build a whole grid and return a grid object:</p>
<table>
<tr><th>Figure-level</th><th>Wraps</th><th>Grid by</th></tr>
<tr><td><code>relplot</code></td><td>scatterplot / lineplot</td><td><code>col=</code>, <code>row=</code></td></tr>
<tr><td><code>displot</code></td><td>histplot / kdeplot / ecdfplot</td><td><code>col=</code>, <code>row=</code></td></tr>
<tr><td><code>catplot</code></td><td>box / violin / bar / strip …</td><td><code>col=</code>, <code>row=</code></td></tr>
<tr><td><code>pairplot</code></td><td>every pair of columns</td><td>automatic</td></tr>
<tr><td><code>jointplot</code></td><td>scatter + marginal distributions</td><td>automatic</td></tr>
</table>
<p>Set the look once with <code>sns.set_theme(style="whitegrid", palette="deep", font_scale=1.1)</code>. Palettes: <code>"deep"</code>, <code>"pastel"</code>, <code>"viridis"</code>, <code>"coolwarm"</code> (diverging).</p>
""", practice=["One Panel per Category", "Pair Plot", "Joint Plot"])


@LD
def figure_level_demo():
    g = sns.relplot(data=TIPS, x="bill", y="tip", col="day", col_order=["Fri", "Sat", "Sun"], height=2.6, aspect=1)
    g.set_titles("{col_name}")


LESSON("Basics", "Tidy data: the shape Seaborn wants", """
<p>Seaborn works from <b>long</b> data: one row per observation, one column per variable. Then each visual choice simply names a column.</p>
<table><tr><th>Wide (hard to plot)</th><th>Long (tidy)</th></tr>
<tr><td>columns: name, math, english</td><td>columns: name, subject, score</td></tr></table>
<pre><code class="py">tidy = wide.melt(id_vars="name", var_name="subject", value_name="score")
sns.barplot(data=tidy, x="name", y="score", hue="subject")</code></pre>
<p><b>Test:</b> if a column name contains a value (2023, 2024, math, english), it's wide. Melt it.</p>
<p>Once it's tidy, moving a column from <code>hue</code> to <code>x</code>, or to <code>col</code> for separate panels, changes the question you're asking without any other work.</p>
""", practice=["Grouped Count Plot", "Lines per Group Over Time"])


@LD
def tidy_demo():
    wide = pd.DataFrame({"name": ["Ana", "Ben"], "math": [80, 60], "english": [70, 90]})
    tidy = wide.melt(id_vars="name", var_name="subject", value_name="score")
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    sns.barplot(data=tidy, x="name", y="score", hue="subject", ax=left)
    sns.barplot(data=tidy, x="subject", y="score", hue="name", ax=right)
    fig.tight_layout()


LESSON("Core", "Reading a box plot, by hand", """
<p>Values: 2, 4, 4, 5, 6, 7, 9, 15.</p>
<table><tr><th>Part of the box plot</th><th>Calculation</th><th>Value</th></tr>
<tr><td>Bottom of box (Q1)</td><td>25th percentile</td><td>4</td></tr>
<tr><td>Line in box (median)</td><td>between 5 and 6</td><td>5.5</td></tr>
<tr><td>Top of box (Q3)</td><td>75th percentile</td><td>7.5</td></tr>
<tr><td>Box height (IQR)</td><td>7.5 − 4</td><td>3.5</td></tr>
<tr><td>Upper fence</td><td>7.5 + 1.5 × 3.5</td><td>12.75</td></tr>
<tr><td>Lower fence</td><td>4 − 1.5 × 3.5</td><td>−1.25</td></tr>
<tr><td>Upper whisker</td><td>largest value within the fence</td><td>9</td></tr>
<tr><td>Lower whisker</td><td>smallest value within the fence</td><td>2</td></tr>
<tr><td>Dot</td><td>beyond the fence</td><td>15</td></tr></table>
<h4>How to read one</h4>
<ul><li>The box holds the middle 50% of the data.</li>
<li>Median near the bottom of the box, with a long upper whisker, means right-skewed data.</li>
<li>Comparing groups? Do the boxes overlap, or are they clearly apart?</li></ul>
<p><b>Limitation:</b> a box plot hides shape. Two peaks look just like one. Add a strip plot, or use a violin plot, when in doubt.</p>
""", practice=["Box Plot by Group", "Violin Plot", "Strip Plot"])


@LD
def hidden_shape():
    r = np.random.default_rng(0)
    one_peak = r.normal(0, 2.2, 150)
    two_peaks = np.r_[r.normal(-1.5, 0.3, 75), r.normal(1.5, 0.3, 75)]
    df = pd.DataFrame({"group": ["one peak"] * 150 + ["two peaks"] * 150, "value": np.r_[one_peak, two_peaks]})
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    sns.boxplot(data=df, x="group", y="value", ax=left)
    left.set_title("Box plots look similar", fontsize=9)
    sns.violinplot(data=df, x="group", y="value", ax=right)
    right.set_title("Violins reveal the two peaks", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Bins and smoothing can change the story", """
<p>Histograms and density curves involve a choice, and that choice can hide or invent features.</p>
<ul><li><b>Too few bins:</b> a two-peaked distribution can look flat, or like one lump.</li>
<li><b>Too many bins:</b> random noise looks like real structure.</li>
<li><b>KDE smoothing:</b> <code>bw_adjust</code> does the same job. A KDE can also show values that can't exist, such as negative ages.</li></ul>
<p><b>Good habit:</b> try several bin counts before concluding anything. If your finding disappears when the bins change, it wasn't solid.</p>
<p>To compare groups with different sizes, use <code>stat="density"</code> and <code>common_norm=False</code>, so a larger group doesn't appear more important. The <b>ECDF</b> avoids bins entirely: it shows the share of values at or below each point.</p>
""", practice=["Histogram", "Smooth Density Curve", "Stacked Histogram by Group", "Cumulative Distribution (ECDF)"])


@LD
def bins_change_story():
    r = np.random.default_rng(1)
    values = np.r_[r.normal(40, 4, 120), r.normal(55, 4, 120)]
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.5), sharex=True)
    for ax, bins, name in zip(axes, [3, 15, 120], ["3 bins: looks flat", "15 bins: two peaks", "120 bins: noisy"]):
        sns.histplot(values, bins=bins, ax=ax)
        ax.set_title(name, fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "Hidden averages and Simpson's paradox", """
<p><code>sns.barplot</code> quietly <b>computes an average</b> and draws an error bar. Very different data can yield identical bars, so look at the raw points too.</p>
<h4>Simpson's paradox: a real shock</h4>
<p>Recovery rates for two treatments, from a well-known kidney-stone study:</p>
<table><tr><th>Stone size</th><th>Treatment A</th><th>Treatment B</th><th>Better</th></tr>
<tr><td>Small</td><td>81 / 87 = <b>93%</b></td><td>234 / 270 = 87%</td><td>A</td></tr>
<tr><td>Large</td><td>192 / 263 = <b>73%</b></td><td>55 / 80 = 69%</td><td>A</td></tr>
<tr><td><b>All patients</b></td><td>273 / 350 = 78%</td><td>289 / 350 = <b>83%</b></td><td><b>B?!</b></td></tr></table>
<p>A wins in <b>both</b> groups but loses overall. The reason: doctors gave A mostly to the hard, large-stone cases. Stone size affects both the choice of treatment and the outcome.</p>
<p><b>Lesson:</b> before trusting an overall comparison, split by likely confounders, which is what <code>hue</code> and <code>col</code> make easy. Which view is right depends on how the data arose, so think about the cause, not just the numbers.</p>
""", practice=["Bar Plot of Averages", "Point Plot of Means", "Bars in a Chosen Order", "Totals, Largest First"])


@LD
def simpson_chart():
    df = pd.DataFrame({"stones": ["small", "small", "large", "large", "all", "all"], "treatment": ["A", "B", "A", "B", "A", "B"], "recovered": [81, 234, 192, 55, 273, 289], "patients": [87, 270, 263, 80, 350, 350]})
    df["rate"] = df["recovered"] / df["patients"]
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    sns.barplot(data=df, x="stones", y="rate", hue="treatment", ax=ax)
    ax.set_ylim(0.5, 1)
    ax.set_ylabel("recovery rate")
    ax.set_title("A wins each group, but B wins overall", fontsize=9)


LESSON("Advanced", "Correlation heat maps, without fooling yourself", """
<p>A heat map of <code>df.corr(numeric_only=True)</code> gives a fast overview. Use it well:</p>
<ul><li>Use a <b>diverging</b> palette with <code>vmin=-1, vmax=1, center=0</code>, so colour means the same in every chart.</li>
<li>Add numbers with <code>annot=True, fmt=".2f"</code>, and hide the repeated half with a <code>mask</code>.</li></ul>
<h4>What it can't tell you</h4>
<ul><li>Only straight-line relationships count: a perfect U shape can have r = 0.</li>
<li>One outlier can create or destroy a correlation.</li>
<li>With 20 columns you're looking at 190 pairs, so a few will look strong by chance.</li>
<li>Correlation isn't cause.</li></ul>
<p>So check interesting cells with a scatter plot, or a <code>pairplot</code> of a few columns.</p>
""", practice=["Correlation Heat Map", "Scatter With a Trend Line", "Pair Plot", "Joint Plot"])


@LD
def masked_heatmap():
    r = np.random.default_rng(0)
    a = r.normal(size=100)
    df = pd.DataFrame({"a": a, "b": a * 2 + r.normal(size=100), "c": -a + r.normal(size=100), "u_shape": a ** 2, "noise": r.normal(size=100)})
    corr = df.corr()
    hide_upper = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(4.6, 3.3))
    sns.heatmap(corr, mask=hide_upper, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title("u_shape depends on a, yet r is near 0", fontsize=9)
