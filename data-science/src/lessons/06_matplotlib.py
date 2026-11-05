from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Figure and Axes", """
<p>Every Matplotlib chart lives in a <b>Figure</b> (the whole image) that contains one or more <b>Axes</b> (a single plot area with its own x and y axis). Most of your work is calling methods on an Axes.</p>
<pre><code class="py">import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))   # width, height in inches
ax.plot([1, 2, 3], [4, 1, 6])
ax.set_title("My first chart")
plt.show()                               # in a script: open the window</code></pre>
<p>Matplotlib has two styles: the quick <b>pyplot</b> style (<code>plt.plot</code>, <code>plt.title</code> — acts on "the current Axes") and the <b>object-oriented</b> style above. Prefer the OO style: it's explicit, and it's what you need once a figure has several charts. In the animations, the chart appears on the last step.</p>
""", practice=["Line Chart", "Labels and Limits"])


@LD
def first_chart():
    fig, ax = plt.subplots(figsize=(5, 3))
    days = [1, 2, 3, 4, 5]
    visitors = [12, 18, 15, 22, 30]
    ax.plot(days, visitors, marker="o")
    ax.set(title="Visitors per day", xlabel="day", ylabel="visitors")


LESSON("Basics", "Choosing the right chart", """
<table>
<tr><th>You want to show…</th><th>Chart</th><th>Method</th></tr>
<tr><td>change over time / an ordered x</td><td>line</td><td><code>ax.plot</code></td></tr>
<tr><td>comparison between categories</td><td>bar (horizontal for long names)</td><td><code>ax.bar</code>, <code>ax.barh</code></td></tr>
<tr><td>relationship between two numbers</td><td>scatter</td><td><code>ax.scatter</code></td></tr>
<tr><td>distribution of one number</td><td>histogram, box plot</td><td><code>ax.hist</code>, <code>ax.boxplot</code></td></tr>
<tr><td>parts of a whole (few parts)</td><td>pie (or a stacked bar)</td><td><code>ax.pie</code></td></tr>
<tr><td>uncertainty</td><td>error bars, shaded band</td><td><code>ax.errorbar</code>, <code>ax.fill_between</code></td></tr>
</table>
""", practice=["Bar Chart", "Scatter Plot", "Histogram", "Pie Chart With Percentages", "Box Plot of Groups"])


@LD
def chart_types():
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.6))
    axes[0].bar(["A", "B", "C"], [5, 8, 3])
    axes[0].set_title("bar: compare")
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 60)
    axes[1].scatter(x, x * 2 + rng.normal(0, 0.5, 60), s=10)
    axes[1].set_title("scatter: relate")
    axes[2].hist(x, bins=8, edgecolor="white")
    axes[2].set_title("hist: distribute")
    fig.tight_layout()


LESSON("Core", "Labels, legends and styles", """
<pre><code class="py">ax.plot(x, a, label="2024", color="C0", linestyle="-", marker="o", linewidth=2)
ax.plot(x, b, label="2023", color="gray", linestyle="--")
ax.set(title="Sales", xlabel="month", ylabel="₹ (thousands)", ylim=(0, 100))
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)
ax.annotate("launch", xy=(3, 80), xytext=(1, 90), arrowprops={"arrowstyle": "->"})</code></pre>
<p>Every chart needs a clear title, axis labels with units, and a legend when there's more than one series. Colours <code>"C0"</code>, <code>"C1"</code> … are the default palette.</p>
""", practice=["Two Lines With a Legend", "Markers and Line Styles", "Mark the Highest Point"])


@LD
def labels_demo():
    months = ["Jan", "Feb", "Mar", "Apr"]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(months, [40, 55, 80, 72], marker="o", label="2024")
    ax.plot(months, [35, 40, 52, 60], linestyle="--", color="gray", label="2023")
    ax.set(title="Sales", xlabel="month", ylabel="₹ thousands", ylim=(0, 100))
    ax.annotate("best month", xy=(2, 80), xytext=(0.2, 90), arrowprops={"arrowstyle": "->"})
    ax.legend()
    ax.grid(True, alpha=0.3)


LESSON("Core", "Several bars and several charts", """
<p><b>Grouped bars</b>: shift each series left/right by half a bar width. <b>Stacked bars</b>: pass <code>bottom=</code> the previous series.</p>
<p><b>Several charts in one figure</b>:</p>
<pre><code class="py">fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharex=True)
for ax, (name, values) in zip(axes.flat, data.items()):
    ax.plot(values); ax.set_title(name)
fig.tight_layout()                     # stop labels overlapping
right = ax.twinx()                     # second y axis on the same chart</code></pre>
""", practice=["Grouped Bars", "Stacked Bars", "Two Charts Side by Side", "2 × 2 Small Multiples", "Two Different Y Scales"])


@LD
def grouped_demo():
    names = ["A", "B", "C"]
    x = np.arange(len(names))
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
    left.bar(x - 0.2, [5, 7, 3], width=0.4, label="2024")
    left.bar(x + 0.2, [4, 6, 5], width=0.4, label="2023")
    left.set_xticks(x, names)
    left.legend()
    right.bar(names, [5, 7, 3], label="shop")
    right.bar(names, [2, 1, 4], bottom=[5, 7, 3], label="online")
    right.legend()
    fig.tight_layout()


LESSON("Advanced", "Scales, uncertainty and saving", """
<ul>
<li><b>Log scale</b> (<code>ax.set_yscale("log")</code>) for values spanning several orders of magnitude.</li>
<li><b>Error bars</b> (<code>ax.errorbar</code>) and <b>bands</b> (<code>ax.fill_between</code>) show uncertainty.</li>
<li><b>Saving</b>: <code>fig.savefig("chart.png", dpi=200, bbox_inches="tight")</code>; use <code>.svg</code> or <code>.pdf</code> for sharp vector output.</li>
<li><b>Styles</b>: <code>plt.style.use("ggplot")</code>, or set defaults with <code>plt.rcParams["font.size"] = 12</code>.</li>
<li><b>Pandas shortcut</b>: <code>df.plot(x="month", y="sales", kind="bar")</code> uses Matplotlib underneath and returns the Axes.</li>
</ul>
<div class="warn">Close figures you don't need (<code>plt.close(fig)</code>) in loops — each open figure uses memory.</div>
""", practice=["Logarithmic Scale", "Error Bars", "Shaded Range", "Save a Chart as PNG", "Sorted Horizontal Bars"])


@LD
def uncertainty_demo():
    x = np.arange(6)
    mean = np.array([3, 4, 6, 7, 9, 12])
    spread = np.array([0.5, 0.8, 1.0, 1.2, 1.5, 2.0])
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, mean, color="C0", label="forecast")
    ax.fill_between(x, mean - spread, mean + spread, alpha=0.3, label="range")
    ax.errorbar(x, mean, yerr=spread, fmt="o", color="C0", capsize=3)
    ax.legend()


LESSON("Basics", "From a default chart to a clear one", """
<p>A chart should answer a question at a glance. The chart in the demo goes from default to clear in a few steps:</p>
<ol><li><b>Sort</b> the bars by value, unless they have a natural order.</li>
<li><b>Title with the finding:</b> "Pune leads sales", not "Sales by city".</li>
<li><b>Label the units</b> on the axis, such as "sales (₹ lakh)".</li>
<li><b>Remove clutter:</b> top and right borders, a pointless legend.</li>
<li><b>Highlight</b> what matters with colour, and grey out the rest.</li>
<li><b>Label values directly</b> when there are few of them: <code>ax.bar_label</code>.</li></ol>
<p>Every element should earn its place. If you removed it and nothing was lost, leave it out.</p>
""", practice=["Sorted Horizontal Bars", "Labels and Limits", "Bar Chart"])


@LD
def default_to_clear():
    sales = {"Goa": 12, "Pune": 41, "Delhi": 28, "Agra": 9}
    fig, (before, after) = plt.subplots(1, 2, figsize=(8, 2.9))
    before.bar(list(sales), list(sales.values()))
    before.set_title("Before: default", fontsize=9)
    ordered = sorted(sales.items(), key=lambda kv: kv[1])
    names = [k for k, v in ordered]
    values = [v for k, v in ordered]
    colours = ["#0f766e" if k == "Pune" else "#c9ced6" for k in names]
    bars = after.barh(names, values, color=colours)
    after.bar_label(bars, padding=3)
    after.set_title("After: Pune leads sales", fontsize=9)
    after.set_xlabel("sales (₹ lakh)")
    after.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()


LESSON("Core", "Charts that mislead", """
<p>The same honest numbers can tell a false story. Learn to spot and avoid these:</p>
<table><tr><th>Trick</th><th>Effect</th><th>Do this</th></tr>
<tr><td>Bar axis not starting at 0</td><td>a 2% gap looks huge</td><td>start bars at 0</td></tr>
<tr><td>Two y axes</td><td>any two lines can seem to move together</td><td>use two panels, or index both to 100</td></tr>
<tr><td>Chart areas for values</td><td>doubling the radius quadruples the area</td><td>use length</td></tr>
<tr><td>Picking a date range</td><td>a fall can be made to look like growth</td><td>show the full context</td></tr>
<tr><td>Pie with many slices</td><td>angles are hard to compare</td><td>sorted bars</td></tr>
<tr><td>Averages only</td><td>hides spread and outliers</td><td>show the points, or a box plot</td></tr></table>
<p>The demo plots 98 vs 100 twice. With a cut axis, one bar looks many times smaller than the other. With an axis from 0, they're almost equal, which is the truth.</p>
<p><b>Exception:</b> line charts don't need to start at 0, since they show change rather than size.</p>
""", practice=["Two Different Y Scales", "Pie Chart With Percentages"])


@LD
def truncated_axis():
    names, values = ["A", "B"], [98, 100]
    fig, (cut, honest) = plt.subplots(1, 2, figsize=(6.5, 2.7))
    cut.bar(names, values, color="#b91c1c")
    cut.set_ylim(97.5, 100.2)
    cut.set_title("Axis cut: B looks far ahead", fontsize=9)
    honest.bar(names, values, color="#0f766e")
    honest.set_ylim(0, 110)
    honest.set_title("Axis from 0: almost equal", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Working with many panels", """
<p><code>plt.subplots</code> returns a figure and <code>axes</code>. The shape of <code>axes</code> changes, and that's a common source of errors:</p>
<table><tr><th>Call</th><th>axes is</th><th>Access with</th></tr>
<tr><td><code>plt.subplots()</code></td><td>one Axes</td><td><code>ax.plot(...)</code></td></tr>
<tr><td><code>plt.subplots(1, 3)</code></td><td>array of shape (3,)</td><td><code>axes[0]</code></td></tr>
<tr><td><code>plt.subplots(2, 3)</code></td><td>array of shape (2, 3)</td><td><code>axes[1, 2]</code>, or loop over <code>axes.flat</code></td></tr></table>
<h4>Small multiples</h4>
<p>One panel per category, on <b>shared axes</b>, often beats many lines on one chart. Use <code>sharex=True, sharey=True</code> so panels can be compared at a glance. Without shared axes, a small value can look just as large as a big one.</p>
<p>Finish with <code>fig.tight_layout()</code> to stop labels overlapping.</p>
""", practice=["Two Charts Side by Side", "2 × 2 Small Multiples"])


@LD
def small_multiples():
    months = np.arange(1, 13)
    cities = {"Pune": 20 + 2 * months, "Delhi": 60 - 3 * months, "Goa": 30 + 10 * np.sin(months), "Agra": 15 + 0 * months}
    fig, axes = plt.subplots(2, 2, figsize=(6, 3.6), sharex=True, sharey=True)
    for ax, (city, values) in zip(axes.flat, cities.items()):
        ax.plot(months, values)
        ax.set_title(city, fontsize=9)
    fig.supxlabel("month", fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "Pointing at what matters", """
<p>Guide the reader's eye:</p>
<table><tr><th>Tool</th><th>Use</th></tr>
<tr><td><code>ax.annotate("Launch", xy=(x, y), xytext=(a, b), arrowprops={...})</code></td><td>explain one point</td></tr>
<tr><td><code>ax.axhline(100, ls="--")</code>, <code>ax.axvline(...)</code></td><td>a target or an event</td></tr>
<tr><td><code>ax.axvspan(a, b, alpha=0.2)</code></td><td>shade a period</td></tr>
<tr><td><code>ax.fill_between(x, low, high, alpha=0.2)</code></td><td>show uncertainty</td></tr>
<tr><td><code>ax.text(x, y, "label")</code></td><td>label a line directly, instead of a legend</td></tr></table>
<h4>Colour choices</h4>
<ul><li><b>Categories:</b> distinct colours, at most about 6–8 (<code>tab10</code>).</li>
<li><b>Ordered values:</b> one colour from light to dark (<code>viridis</code>).</li>
<li><b>Above or below a middle:</b> two colours (<code>coolwarm</code>, with the centre at 0).</li>
<li>Don't rely on red vs green alone, as many people can't tell them apart.</li></ul>
""", practice=["Mark the Highest Point", "Shaded Range", "Error Bars", "Markers and Line Styles"])


@LD
def annotated_story():
    weeks = np.arange(12)
    users = np.array([50, 52, 51, 55, 54, 58, 85, 92, 96, 101, 104, 110])
    fig, ax = plt.subplots(figsize=(5.2, 3))
    ax.plot(weeks, users, color="#0f766e")
    ax.axhline(100, ls="--", color="gray")
    ax.text(0, 102, "target: 100", fontsize=8)
    ax.axvspan(5.5, 6.5, alpha=0.15, color="#b45309")
    ax.annotate("App launch", xy=(6, 85), xytext=(1.5, 80), arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("week")
    ax.set_ylabel("users")
    ax.set_title("Users passed the target after launch", fontsize=9)
