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
