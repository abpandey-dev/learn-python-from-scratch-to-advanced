from lib import *
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

TOPIC(
    id="matplotlib", title="Matplotlib", glyph="📈 plt",
    blurb="Draw line, bar, scatter, histogram, pie and box charts; add labels, legends and annotations; build multi-panel figures.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4))   # one Figure, one Axes
ax.plot(x, y, marker="o", linestyle="--", label="sales")
ax.bar(names, values); ax.barh(names, values)
ax.scatter(x, y, s=sizes, c=colors)
ax.hist(values, bins=10); ax.pie(parts, labels=names, autopct="%1.0f%%")
ax.set(title="…", xlabel="…", ylabel="…", xlim=(0, 10))
ax.legend(); ax.grid(True); ax.annotate("peak", xy=(x, y))
fig, axes = plt.subplots(2, 2)           # grid of Axes
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
plt.show()</code></pre>
""")



def bars(ax):
    from matplotlib.patches import Rectangle
    return [p for p in ax.patches if isinstance(p, Rectangle)]


def points(ax):
    return sum(len(c.get_offsets()) for c in ax.collections if hasattr(c, "get_offsets"))


Q(None, "Line Chart", "Easy", "plot · title",
  "Draw <code>values</code> as a line chart titled 'Daily visitors'. Return the Axes.",
  [(([5, 9, 7, 12],), "1 line, title 'Daily visitors'")],
  ("pyplot's state machine: <code>plt.figure</code>, <code>plt.plot</code>, <code>plt.title</code>, then grab the current Axes.", "O(n)", "O(n)"),
  ("Object-oriented API: <code>fig, ax = plt.subplots()</code>, then call methods on <code>ax</code> — explicit and safe with many charts.", "O(n)", "O(n)"),
  check=lambda a, ax: len(ax.lines) == 1 and ax.get_title() == "Daily visitors" and list(ax.lines[0].get_ydata()) == a[0])


@B
def line_chart(values):
    plt.figure(figsize=(5, 3))
    plt.plot(range(len(values)), values)
    plt.title("Daily visitors")
    return plt.gca()


@O
def line_chart(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(values)
    ax.set_title("Daily visitors")
    return ax


Q(None, "Two Lines With a Legend", "Easy", "label · legend",
  "Plot two series on the same Axes with labels 'this year' and 'last year' and show a legend.",
  [(([3, 5, 4], [2, 4, 6]), "2 lines and a legend")],
  ("Plot each line and build the legend by passing a list of names afterwards.", "O(n)", "O(n)"),
  ("Give each line a <code>label=</code>; <code>ax.legend()</code> collects them.", "O(n)", "O(n)"),
  check=lambda a, ax: len(ax.lines) == 2 and ax.get_legend() is not None and [t.get_text() for t in ax.get_legend().get_texts()] == ["this year", "last year"])


@B
def two_lines(this_year, last_year):
    plt.figure(figsize=(5, 3))
    plt.plot(this_year)
    plt.plot(last_year)
    plt.legend(["this year", "last year"])
    return plt.gca()


@O
def two_lines(this_year, last_year):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(this_year, label="this year")
    ax.plot(last_year, label="last year")
    ax.legend()
    return ax


Q(None, "Bar Chart", "Easy", "bar",
  "Draw one bar per category with the given values.",
  [((["Jan", "Feb", "Mar"], [30, 45, 25]), "3 bars")],
  ("Call <code>plt.bar</code> once per category in a loop.", "O(n)", "O(n)"),
  ("One <code>ax.bar(names, values)</code> call draws them all.", "O(n)", "O(n)"),
  check=lambda a, ax: [round(b.get_height()) for b in bars(ax)] == a[1])


@B
def bar_chart(names, values):
    plt.figure(figsize=(5, 3))
    for i in range(len(names)):
        plt.bar(names[i], values[i], color="C0")
    return plt.gca()


@O
def bar_chart(names, values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(names, values)
    return ax


Q(None, "Sorted Horizontal Bars", "Medium", "barh + sorting",
  "Draw horizontal bars sorted so the largest value is at the top.",
  [((["a", "b", "c"], [5, 9, 2]), "3 bars, widths 2, 5, 9 from bottom to top")],
  ("Sort with a manual selection sort, then draw each bar.", "O(n²)", "O(n)"),
  ("Sort once with <code>sorted(zip(...))</code> and pass both lists to <code>ax.barh</code>.", "O(n log n)", "O(n)"),
  check=lambda a, ax: [round(b.get_width()) for b in bars(ax)] == sorted(a[1]))


@B
def sorted_bars(names, values):
    pairs = list(zip(values, names))
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            if pairs[j][0] < pairs[i][0]:
                pairs[i], pairs[j] = pairs[j], pairs[i]
    plt.figure(figsize=(5, 3))
    for v, n in pairs:
        plt.barh(n, v, color="C0")
    return plt.gca()


@O
def sorted_bars(names, values):
    ordered = sorted(zip(values, names))
    widths, labels = zip(*ordered)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(labels, widths)
    return ax


Q(None, "Scatter Plot", "Easy", "scatter",
  "Plot height (x) against weight (y) as points, with axis labels 'height' and 'weight'.",
  [(([150, 160, 170, 180], [50, 58, 65, 80]), "4 points, labelled axes")],
  ("<code>plt.plot</code> with marker 'o' and no line, one point at a time.", "O(n)", "O(n)"),
  ("<code>ax.scatter(x, y)</code> — one call, and size/colour can encode extra columns.", "O(n)", "O(n)"),
  check=lambda a, ax: (points(ax) == 4 or sum(len(l.get_xdata()) for l in ax.lines) == 4) and ax.get_xlabel() == "height" and ax.get_ylabel() == "weight")


@B
def scatter(heights, weights):
    plt.figure(figsize=(5, 3))
    for h, w in zip(heights, weights):
        plt.plot(h, w, "o", color="C0")
    plt.xlabel("height")
    plt.ylabel("weight")
    return plt.gca()


@O
def scatter(heights, weights):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(heights, weights)
    ax.set(xlabel="height", ylabel="weight")
    return ax


Q(None, "Histogram", "Easy", "hist",
  "Draw a histogram of the values with <code>bins</code> equal-width bins.",
  [(([1, 2, 2, 3, 3, 3, 4, 4, 5], 4), "4 bars whose heights add up to 9")],
  ("Compute the bin edges and counts by hand, then draw bars.", "O(n · bins)", "O(bins)"),
  ("<code>ax.hist(values, bins=bins)</code> counts and draws.", "O(n)", "O(bins)"),
  check=lambda a, ax: len(bars(ax)) == a[1] and round(sum(b.get_height() for b in bars(ax))) == len(a[0]))


@B
def histogram(values, bins):
    lo, hi = min(values), max(values)
    width = (hi - lo) / bins
    counts = [0] * bins
    for v in values:
        i = min(int((v - lo) / width), bins - 1)
        counts[i] += 1
    plt.figure(figsize=(5, 3))
    plt.bar([lo + width * (i + 0.5) for i in range(bins)], counts, width=width, edgecolor="white")
    return plt.gca()


@O
def histogram(values, bins):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(values, bins=bins, edgecolor="white")
    return ax


Q(None, "Pie Chart With Percentages", "Easy", "pie · autopct",
  "Draw a pie chart of the parts with labels and percentage text on each slice.",
  [((["rent", "food", "fun"], [50, 30, 20]), "3 slices with percentage labels")],
  ("Compute each percentage and pass the formatted labels yourself.", "O(n)", "O(n)"),
  ("<code>ax.pie(parts, labels=names, autopct='%1.0f%%')</code>.", "O(n)", "O(n)"),
  check=lambda a, ax: len(ax.patches) == 3 and any("%" in t.get_text() for t in ax.texts))


@B
def pie(names, parts):
    total = sum(parts)
    labels = [f"{n} ({p / total * 100:.0f}%)" for n, p in zip(names, parts)]
    plt.figure(figsize=(5, 3))
    plt.pie(parts, labels=labels)
    return plt.gca()


@O
def pie(names, parts):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(parts, labels=names, autopct="%1.0f%%")
    return ax


Q(None, "Two Charts Side by Side", "Medium", "subplots(1, 2)",
  "Draw a line chart and a bar chart of the same values next to each other in one figure. Return the Figure.",
  [(([4, 7, 5],), "a figure with 2 Axes")],
  ("Create the figure, then add each panel with <code>plt.subplot(1, 2, i)</code>.", "O(n)", "O(n)"),
  ("<code>fig, (left, right) = plt.subplots(1, 2)</code> gives both Axes at once.", "O(n)", "O(n)"),
  check=lambda a, fig: len(fig.axes) == 2)


@B
def side_by_side(values):
    fig = plt.figure(figsize=(8, 3))
    plt.subplot(1, 2, 1)
    plt.plot(values)
    plt.subplot(1, 2, 2)
    plt.bar(range(len(values)), values)
    return fig


@O
def side_by_side(values):
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 3))
    left.plot(values)
    right.bar(range(len(values)), values)
    return fig


Q(None, "Labels and Limits", "Easy", "ax.set",
  "Plot the values and set title 'Temperature', x label 'hour', y label '°C' and y-axis limits 0–40.",
  [(([22, 25, 31, 28],), "labelled chart with y from 0 to 40")],
  ("Separate pyplot calls for each setting.", "O(n)", "O(n)"),
  ("One <code>ax.set(...)</code> call sets several properties.", "O(n)", "O(n)"),
  check=lambda a, ax: (ax.get_title(), ax.get_xlabel(), ax.get_ylabel(), tuple(ax.get_ylim())) == ("Temperature", "hour", "°C", (0.0, 40.0)))


@B
def labelled(values):
    plt.figure(figsize=(5, 3))
    plt.plot(values)
    plt.title("Temperature")
    plt.xlabel("hour")
    plt.ylabel("°C")
    plt.ylim(0, 40)
    return plt.gca()


@O
def labelled(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(values)
    ax.set(title="Temperature", xlabel="hour", ylabel="°C", ylim=(0, 40))
    return ax


Q(None, "Stacked Bars", "Medium", "bottom=",
  "Draw stacked bars: online sales on top of shop sales for each month.",
  [((["Jan", "Feb"], [10, 20], [5, 8]), "4 bars; online bars start where shop bars end")],
  ("Draw each month's two pieces separately with explicit bottoms.", "O(n)", "O(n)"),
  ("Two <code>ax.bar</code> calls; the second uses <code>bottom=shop</code>.", "O(n)", "O(n)"),
  check=lambda a, ax: len(bars(ax)) == 4 and sorted(round(b.get_y()) for b in bars(ax)) == sorted([0, 0] + a[1]))


@B
def stacked(months, shop, online):
    plt.figure(figsize=(5, 3))
    for i in range(len(months)):
        plt.bar(months[i], shop[i], color="C0")
        plt.bar(months[i], online[i], bottom=shop[i], color="C1")
    return plt.gca()


@O
def stacked(months, shop, online):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(months, shop, label="shop")
    ax.bar(months, online, bottom=shop, label="online")
    ax.legend()
    return ax


Q(None, "Grouped Bars", "Medium", "Offsetting bar positions",
  "Draw this year's and last year's values side by side for each category.",
  [((["A", "B", "C"], [5, 7, 3], [4, 6, 5]), "6 bars in 3 pairs")],
  ("Compute each bar's x position in a loop.", "O(n)", "O(n)"),
  ("Use NumPy positions <code>x − w/2</code> and <code>x + w/2</code>, then set the tick labels.", "O(n)", "O(n)"),
  check=lambda a, ax: len(bars(ax)) == 6)


@B
def grouped(names, this_year, last_year):
    plt.figure(figsize=(5, 3))
    for i in range(len(names)):
        plt.bar(i - 0.2, this_year[i], width=0.4, color="C0")
        plt.bar(i + 0.2, last_year[i], width=0.4, color="C1")
    plt.xticks(range(len(names)), names)
    return plt.gca()


@O
def grouped(names, this_year, last_year):
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(x - 0.2, this_year, width=0.4, label="this year")
    ax.bar(x + 0.2, last_year, width=0.4, label="last year")
    ax.set_xticks(x, names)
    ax.legend()
    return ax


Q(None, "Mark the Highest Point", "Medium", "annotate",
  "Plot the values and add an arrow annotation 'max: V' pointing at the highest value.",
  [(([3, 8, 5, 6],), "a line with the text 'max: 8'")],
  ("Find the max index with a loop; draw the text and arrow separately.", "O(n)", "O(1)"),
  ("<code>np.argmax</code> + <code>ax.annotate(text, xy=…, xytext=…, arrowprops=…)</code>.", "O(n)", "O(1)"),
  check=lambda a, ax: any(t.get_text() == f"max: {max(a[0])}" for t in ax.texts))


@B
def mark_max(values):
    best = 0
    for i in range(len(values)):
        if values[i] > values[best]:
            best = i
    plt.figure(figsize=(5, 3))
    plt.plot(values)
    plt.text(best, values[best] + 0.5, f"max: {values[best]}")
    plt.plot(best, values[best], "ro")
    return plt.gca()


@O
def mark_max(values):
    i = int(np.argmax(values))
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(values)
    ax.annotate(f"max: {values[i]}", xy=(i, values[i]), xytext=(i, values[i] + 1), arrowprops={"arrowstyle": "->"})
    return ax


Q(None, "Markers and Line Styles", "Easy", "Format options",
  "Plot the values with circle markers and a dashed red line.",
  [(([1, 4, 2],), "a dashed red line with 'o' markers")],
  ("A format string <code>'ro--'</code> (colour, marker, style in one code).", "O(n)", "O(n)"),
  ("Named keyword arguments — easier to read and to change.", "O(n)", "O(n)"),
  check=lambda a, ax: ax.lines[0].get_marker() == "o" and ax.lines[0].get_linestyle() == "--")


@B
def styled(values):
    plt.figure(figsize=(5, 3))
    plt.plot(values, "ro--")
    return plt.gca()


@O
def styled(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(values, color="red", marker="o", linestyle="--")
    return ax


Q(None, "Error Bars", "Medium", "errorbar",
  "Plot averages with error bars of the given sizes.",
  [(([10, 12, 9], [1, 2, 1.5]), "3 points with vertical error bars")],
  ("Draw each point and a vertical line for its error by hand.", "O(n)", "O(n)"),
  ("<code>ax.errorbar(x, means, yerr=errors, fmt='o', capsize=4)</code>.", "O(n)", "O(n)"),
  check=lambda a, ax: len(ax.lines) >= 1 and (len(ax.containers) >= 1 or len(ax.lines) >= 4))


@B
def error_bars(means, errors):
    plt.figure(figsize=(5, 3))
    for i, (m, e) in enumerate(zip(means, errors)):
        plt.plot([i, i], [m - e, m + e], color="C0")
        plt.plot(i, m, "o", color="C0")
    return plt.gca()


@O
def error_bars(means, errors):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.errorbar(range(len(means)), means, yerr=errors, fmt="o", capsize=4)
    return ax


Q(None, "Shaded Range", "Medium", "fill_between",
  "Plot a line of averages and shade the band between the low and high values.",
  [(([5, 6, 7], [3, 4, 6], [7, 8, 9]), "a line with a shaded band")],
  ("Draw the low and high values as two extra lines.", "O(n)", "O(n)"),
  ("<code>ax.fill_between(x, low, high, alpha=0.3)</code> shades the area.", "O(n)", "O(n)"),
  check=lambda a, ax: len(ax.collections) >= 1 or len(ax.lines) >= 3)


@B
def shaded(avg, low, high):
    plt.figure(figsize=(5, 3))
    plt.plot(avg)
    plt.plot(low, color="gray", linestyle=":")
    plt.plot(high, color="gray", linestyle=":")
    return plt.gca()


@O
def shaded(avg, low, high):
    x = range(len(avg))
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, avg)
    ax.fill_between(x, low, high, alpha=0.3)
    return ax


Q(None, "Two Different Y Scales", "Hard", "twinx",
  "Plot revenue (left axis) and number of orders (right axis) on one chart. Return the Figure.",
  [(([100, 150, 130], [3, 5, 4]), "revenue and orders both visible, each on a readable scale")],
  ("Rescale orders to the revenue range by hand and plot both on one axis.", "O(n)", "O(n)"),
  ("<code>ax.twinx()</code> creates a second y axis sharing the same x axis.", "O(n)", "O(n)"),
  check=lambda a, fig: sum(len(ax.lines) for ax in fig.axes) == 2)


@B
def two_scales(revenue, orders):
    fig = plt.figure(figsize=(5, 3))
    scale = max(revenue) / max(orders)
    plt.plot(revenue, label="revenue")
    plt.plot([o * scale for o in orders], label=f"orders × {scale:.0f}")
    plt.legend()
    return fig


@O
def two_scales(revenue, orders):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(revenue, color="C0")
    ax.set_ylabel("revenue")
    right = ax.twinx()
    right.plot(orders, color="C1")
    right.set_ylabel("orders")
    return fig


Q(None, "Box Plot of Groups", "Medium", "boxplot",
  "Draw one box per group (patch_artist so boxes are filled).",
  [(([[1, 2, 3, 4, 9], [3, 4, 5, 6, 7]], ["A", "B"]), "2 filled boxes")],
  ("Compute quartiles yourself and draw rectangles and lines.", "O(n log n)", "O(1)"),
  ("<code>ax.boxplot(groups, patch_artist=True)</code> computes median, quartiles, whiskers and outliers.", "O(n log n)", "O(1)"),
  check=lambda a, ax: len(ax.patches) == 2)


@B
def boxes(groups, names):
    from matplotlib.patches import Rectangle
    fig, ax = plt.subplots(figsize=(5, 3))
    for i, g in enumerate(groups):
        q1, med, q3 = np.percentile(g, [25, 50, 75])
        ax.add_patch(Rectangle((i + 0.75, q1), 0.5, q3 - q1, facecolor="C0", alpha=0.5))
        ax.plot([i + 0.75, i + 1.25], [med, med], color="black")
        ax.plot([i + 1, i + 1], [min(g), q1], color="black")
        ax.plot([i + 1, i + 1], [q3, max(g)], color="black")
    ax.set_xlim(0.5, len(groups) + 0.5)
    ax.set_ylim(0, max(max(g) for g in groups) + 1)
    ax.set_xticks(range(1, len(groups) + 1), names)
    return ax


@O
def boxes(groups, names):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.boxplot(groups, patch_artist=True)
    ax.set_xticks(range(1, len(names) + 1), names)
    return ax


Q(None, "Logarithmic Scale", "Easy", "set_yscale('log')",
  "Plot fast-growing values on a log-scale y axis.",
  [(([1, 10, 100, 1000],), "a line on a log y axis")],
  ("Plot log10 of every value instead, and relabel by hand.", "O(n)", "O(n)"),
  ("<code>ax.set_yscale('log')</code> keeps the real values and spaces the axis by powers of 10.", "O(n)", "O(n)"),
  check=lambda a, ax: ax.get_yscale() == "log")


@B
def log_scale(values):
    plt.figure(figsize=(5, 3))
    plt.plot([np.log10(v) for v in values])
    plt.yscale("log")
    return plt.gca()


@O
def log_scale(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(values)
    ax.set_yscale("log")
    return ax


Q(None, "2 × 2 Small Multiples", "Medium", "subplots grid",
  "Draw each of four series in its own panel of a 2 × 2 grid, titled with its name. Return the Figure.",
  [(({"a": [1, 2], "b": [2, 1], "c": [3, 3], "d": [1, 3]},), "a figure with 4 titled Axes")],
  ("Call <code>plt.subplot(2, 2, i)</code> four times.", "O(n)", "O(n)"),
  ("<code>fig, axes = plt.subplots(2, 2)</code> and loop over <code>axes.flat</code>.", "O(n)", "O(n)"),
  check=lambda a, fig: len(fig.axes) == 4 and sorted(ax.get_title() for ax in fig.axes) == ["a", "b", "c", "d"])


@B
def small_multiples(series):
    fig = plt.figure(figsize=(6, 4))
    i = 1
    for name, values in series.items():
        plt.subplot(2, 2, i)
        plt.plot(values)
        plt.title(name)
        i += 1
    return fig


@O
def small_multiples(series):
    fig, axes = plt.subplots(2, 2, figsize=(6, 4), sharex=True, sharey=True)
    for ax, (name, values) in zip(axes.flat, series.items()):
        ax.plot(values)
        ax.set_title(name)
    fig.tight_layout()
    return fig


Q(None, "Save a Chart as PNG", "Easy", "savefig",
  "Draw a bar chart and return its PNG image bytes (as you'd write to a file).",
  [(([3, 1, 2],), "PNG bytes")],
  ("Save to a temporary file on disk and read it back.", "O(pixels)", "O(pixels)"),
  ("<code>fig.savefig(buffer, format='png')</code> into an in-memory <code>io.BytesIO</code>.", "O(pixels)", "O(pixels)"),
  check=lambda a, data: isinstance(data, bytes) and data[:4] == b"\x89PNG")


@B
def png_bytes(values):
    import os
    import tempfile
    plt.figure(figsize=(5, 3))
    plt.bar(range(len(values)), values)
    path = os.path.join(tempfile.mkdtemp(), "chart.png")
    plt.savefig(path)
    with open(path, "rb") as f:
        data = f.read()
    return data


@O
def png_bytes(values):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(range(len(values)), values)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    return buffer.getvalue()
