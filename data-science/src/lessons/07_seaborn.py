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
