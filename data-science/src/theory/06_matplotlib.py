from lib import *

THEORY("What Matplotlib is", """
<p><b>Matplotlib</b> is Python's foundational plotting library, created by John D. Hunter in 2003 and modelled on MATLAB's plotting. It produces static, animated and interactive charts and can export to PNG, SVG, PDF and more. Pandas' <code>.plot()</code> and Seaborn are built on top of it.</p>
""")

THEORY("Anatomy of a figure", """
<table>
<tr><th>Object</th><th>What it is</th></tr>
<tr><td><b>Figure</b></td><td>the whole canvas/window; holds one or more Axes, a suptitle, legends</td></tr>
<tr><td><b>Axes</b></td><td>one plotting area with a data coordinate system — the object you draw on</td></tr>
<tr><td><b>Axis</b></td><td>the x or y number line of an Axes: limits, ticks, tick labels, scale</td></tr>
<tr><td><b>Artist</b></td><td>everything visible: Line2D, Rectangle (bars), Text, PathCollection (scatter), Patch …</td></tr>
</table>
<p>Hierarchy: Figure → Axes → (Axis, Lines, Patches, Texts, Collections). <code>fig.axes</code> lists Axes; <code>ax.lines</code>, <code>ax.patches</code>, <code>ax.collections</code>, <code>ax.texts</code> list what's drawn — that's how the tests in this topic check your charts.</p>
""")

THEORY("Two interfaces", """
<table>
<tr><th></th><th>pyplot (state-based)</th><th>Object-oriented</th></tr>
<tr><td>Example</td><td><code>plt.plot(x); plt.title("t")</code></td><td><code>fig, ax = plt.subplots(); ax.plot(x); ax.set_title("t")</code></td></tr>
<tr><td>Acts on</td><td>the implicit "current" Figure/Axes</td><td>the object you name</td></tr>
<tr><td>Good for</td><td>quick interactive exploration</td><td>scripts, functions, multi-panel figures</td></tr>
</table>
<p>Method names differ slightly: <code>plt.title</code> ↔ <code>ax.set_title</code>, <code>plt.xlabel</code> ↔ <code>ax.set_xlabel</code>, <code>plt.xlim</code> ↔ <code>ax.set_xlim</code>.</p>
""")

THEORY("Plot types", """
<table>
<tr><th>Method</th><th>Chart</th><th>Data</th></tr>
<tr><td><code>plot</code></td><td>line</td><td>ordered x (time)</td></tr>
<tr><td><code>scatter</code></td><td>points</td><td>two numeric variables (+ size/colour)</td></tr>
<tr><td><code>bar / barh</code></td><td>bars</td><td>category → number</td></tr>
<tr><td><code>hist</code></td><td>histogram</td><td>distribution of one variable</td></tr>
<tr><td><code>boxplot / violinplot</code></td><td>box / violin</td><td>distribution summaries by group</td></tr>
<tr><td><code>pie</code></td><td>pie</td><td>parts of a whole</td></tr>
<tr><td><code>errorbar / fill_between</code></td><td>uncertainty</td><td>mean ± error</td></tr>
<tr><td><code>imshow / pcolormesh</code></td><td>heat map / image</td><td>2-D grid</td></tr>
<tr><td><code>stackplot</code>, <code>step</code>, <code>stem</code></td><td>area, step, stem</td><td>specialised</td></tr>
</table>
""")

THEORY("Customisation", """
<ul>
<li><b>Colours</b>: names (<code>"red"</code>), hex (<code>"#0F766E"</code>), cycle (<code>"C0"…"C9"</code>), colormaps for continuous data (<code>cmap="viridis"</code>).</li>
<li><b>Lines</b>: <code>linestyle</code> ("-", "--", ":", "-."), <code>linewidth</code>, <code>marker</code> ("o", "s", "^", "x").</li>
<li><b>Text</b>: <code>set_title/xlabel/ylabel</code>, <code>text</code>, <code>annotate</code>, <code>fig.suptitle</code>.</li>
<li><b>Axes</b>: <code>set_xlim/ylim</code>, <code>set_xscale("log")</code>, <code>set_xticks(positions, labels)</code>, <code>invert_yaxis</code>, <code>twinx</code>.</li>
<li><b>Layout</b>: <code>plt.subplots(nrows, ncols, sharex, sharey, figsize)</code>, <code>fig.tight_layout()</code> or <code>layout="constrained"</code>, <code>GridSpec</code> for uneven grids.</li>
<li><b>Global style</b>: <code>plt.style.use(...)</code>, <code>plt.rcParams[...]</code>.</li>
</ul>
""")

THEORY("Good chart practice", """
<ul>
<li>Pick the chart for the question (compare → bar; trend → line; relationship → scatter; distribution → histogram/box).</li>
<li>Bar charts should start at zero; line charts may not need to.</li>
<li>Label axes with units; title with the takeaway.</li>
<li>Sort bars by value unless the categories have a natural order.</li>
<li>Avoid 3-D effects and pies with many slices.</li>
<li>Use colour sparingly and make it colour-blind friendly (viridis, the default C0–C9 cycle).</li>
</ul>
""")

FAQ("Figure vs Axes?", "<p>The Figure is the whole canvas; an Axes is one plot area inside it with its own coordinate system. A figure can hold many Axes.</p>")
FAQ("plt.plot vs ax.plot?", "<p>plt.plot draws on pyplot's current Axes (implicit state). ax.plot draws on a specific Axes object you hold. Use the object-oriented form in scripts and multi-panel figures.</p>")
FAQ("How do you put several charts in one figure?", "<p><code>fig, axes = plt.subplots(rows, cols)</code>, then draw on each element of <code>axes</code> (use <code>axes.flat</code> to loop), and call <code>fig.tight_layout()</code>.</p>")
FAQ("How do you save a chart?", "<p><code>fig.savefig('name.png', dpi=200, bbox_inches='tight')</code>. The file format follows the extension (png, svg, pdf, jpg).</p>")
FAQ("Histogram vs bar chart?", "<p>A bar chart compares values of separate categories; a histogram shows how one numeric variable is distributed by counting values in adjacent bins (no gaps).</p>")
FAQ("How do you show two variables with different units on one chart?", "<p>Create a second y axis with <code>ax.twinx()</code>, plot the second variable on it, and label both axes. Use it sparingly — it can mislead.</p>")
