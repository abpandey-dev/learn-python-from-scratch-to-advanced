from lib import *

THEORY("What Seaborn is", """
<p><b>Seaborn</b> is a high-level statistical visualisation library built on Matplotlib and tightly integrated with pandas (created by Michael Waskom). It maps DataFrame columns to visual properties — x, y, <b>hue</b> (colour), <b>size</b>, <b>style</b> — and performs the needed statistics (counting, averaging, density estimation, regression, confidence intervals) automatically.</p>
""")

THEORY("Function families", """
<table>
<tr><th>Family</th><th>Axes-level</th><th>Figure-level</th></tr>
<tr><td>Relational</td><td><code>scatterplot</code>, <code>lineplot</code></td><td><code>relplot</code></td></tr>
<tr><td>Distribution</td><td><code>histplot</code>, <code>kdeplot</code>, <code>ecdfplot</code>, <code>rugplot</code></td><td><code>displot</code></td></tr>
<tr><td>Categorical</td><td><code>stripplot</code>, <code>swarmplot</code>, <code>boxplot</code>, <code>violinplot</code>, <code>boxenplot</code>, <code>pointplot</code>, <code>barplot</code>, <code>countplot</code></td><td><code>catplot</code></td></tr>
<tr><td>Regression</td><td><code>regplot</code>, <code>residplot</code></td><td><code>lmplot</code></td></tr>
<tr><td>Matrix</td><td><code>heatmap</code></td><td><code>clustermap</code></td></tr>
<tr><td>Multi-plot</td><td>—</td><td><code>pairplot</code>, <code>jointplot</code>, <code>FacetGrid</code>, <code>PairGrid</code></td></tr>
</table>
<p>Axes-level functions accept <code>ax=</code> and return the Axes. Figure-level functions create their own figure and return a grid object (<code>FacetGrid</code>, <code>PairGrid</code>, <code>JointGrid</code>) whose <code>.figure</code> and <code>.axes</code> you can customise.</p>
""")

THEORY("Data formats and semantic mappings", """
<p>Seaborn works best with <b>long-form (tidy)</b> data: one row per observation, one column per variable. Wide-form data (one column per category) is accepted by many functions but offers less control; convert with <code>df.melt()</code>.</p>
<table>
<tr><th>Parameter</th><th>Maps a column to</th></tr>
<tr><td><code>x</code>, <code>y</code></td><td>position</td></tr>
<tr><td><code>hue</code></td><td>colour</td></tr>
<tr><td><code>size</code></td><td>marker size / line width</td></tr>
<tr><td><code>style</code></td><td>marker / dash style</td></tr>
<tr><td><code>col</code>, <code>row</code> (figure-level)</td><td>separate panels (facets)</td></tr>
</table>
""")

THEORY("Statistical estimation", """
<ul>
<li><code>barplot</code>/<code>pointplot</code>/<code>lineplot</code> aggregate repeated values with an <b>estimator</b> (mean by default; <code>estimator="median"</code> or <code>"sum"</code>) and show uncertainty with <code>errorbar=</code>: <code>("ci", 95)</code> bootstrap confidence interval (default), <code>"sd"</code>, <code>"se"</code>, <code>("pi", 50)</code>, or <code>None</code>.</li>
<li><code>kdeplot</code> uses a Gaussian <b>kernel density estimate</b>; <code>bw_adjust</code> changes smoothness.</li>
<li><code>regplot</code> fits ordinary least squares (<code>order=2</code> for polynomial, <code>logistic=True</code>, <code>lowess=True</code>).</li>
<li><code>boxplot</code> uses quartiles and 1.5 × IQR whiskers.</li>
</ul>
""")

THEORY("Themes, palettes and choosing a chart", """
<ul>
<li><b>Themes</b>: <code>sns.set_theme(style=…)</code> with darkgrid, whitegrid, dark, white, ticks; <code>context=</code> paper, notebook, talk, poster.</li>
<li><b>Palettes</b>: qualitative ("deep", "muted", "pastel", "colorblind") for categories; sequential ("rocket", "viridis", "Blues") for ordered values; diverging ("coolwarm", "vlag") for values around a centre such as correlation.</li>
</ul>
<table>
<tr><th>Question</th><th>Seaborn chart</th></tr>
<tr><td>How is one variable distributed?</td><td>histplot, kdeplot, ecdfplot, boxplot</td></tr>
<tr><td>How do groups compare?</td><td>barplot, boxplot, violinplot, stripplot</td></tr>
<tr><td>How do two numbers relate?</td><td>scatterplot, regplot, jointplot</td></tr>
<tr><td>How does a value change over time?</td><td>lineplot</td></tr>
<tr><td>Which variables are correlated?</td><td>heatmap of corr, pairplot</td></tr>
</table>
""")

FAQ("Seaborn vs Matplotlib?", "<p>Matplotlib is the low-level engine with full control. Seaborn is a high-level layer on top that works on DataFrames, computes statistics and styles plots automatically. Seaborn returns Matplotlib objects, so you can mix both.</p>")
FAQ("Axes-level vs figure-level functions?", "<p>Axes-level functions draw on one Axes (pass ax=) and return it. Figure-level functions (relplot, displot, catplot, pairplot, jointplot) create a whole figure, can facet into panels with col/row, and return a grid object.</p>")
FAQ("What does hue do?", "<p>It splits the data by a column and draws each group in a different colour, adding a legend automatically.</p>")
FAQ("What are the black lines on a barplot?", "<p>Error bars: by default a 95% bootstrap confidence interval for the mean. Set errorbar=None to hide them, or 'sd' for standard deviation.</p>")
FAQ("Long vs wide data for Seaborn?", "<p>Long (tidy) form — one row per observation — lets you map any column to x, y, hue, col. Convert wide tables with melt.</p>")
FAQ("How do you save a Seaborn plot?", "<p>Axes-level: <code>ax.figure.savefig('f.png')</code>. Figure-level: <code>g.savefig('f.png')</code> or <code>g.figure.savefig(...)</code>.</p>")
