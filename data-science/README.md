# Python for Data Science

8 topics · theory with 50 theory questions · 42 lessons from basics to advanced · 160 practice questions with answers · NumPy, Pandas, Matplotlib, Seaborn and statistics · every question has a plain-Python brute-force answer and an optimal vectorised or library answer, both shown running line by line, with the charts they draw.

**Live site:** https://abpandey-dev.github.io/python-dsa-visualizer/data-science/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [NumPy Basics](#numpy-basics) — Arrays: creating them, their shape and dtype, indexing, slicing, reshaping and fancy indexing.
- [NumPy Operations](#numpy-operations) — Vectorised maths, aggregation along axes, broadcasting, matrix algebra and common numeric recipes.
- [Pandas Basics](#pandas-basics) — Series and DataFrames: building tables, selecting columns and rows, filtering, sorting and adding columns.
- [Data Cleaning with Pandas](#data-cleaning-with-pandas) — Missing values, duplicates, wrong types, messy text, dates and outliers — getting raw data ready for analysis.
- [Grouping, Merging & Reshaping](#grouping-merging-reshaping) — Split-apply-combine with groupby, joining tables with merge and concat, pivot tables, melt and time-based windows.
- [Matplotlib](#matplotlib) — Draw line, bar, scatter, histogram, pie and box charts; add labels, legends and annotations; build multi-panel figures.
- [Seaborn](#seaborn) — Statistical charts from DataFrames in one line: distributions, categories, relationships, heat maps and multi-panel grids.
- [Statistics for Data Analysis](#statistics-for-data-analysis) — Describe and compare data: centre, spread, percentiles, outliers, correlation, simple regression and basic probability.

## NumPy Basics

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Double Every Number](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/double-every-number) | Easy | Vectorised arithmetic |
| 2 | [Shape and Size](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/shape-and-size) | Easy | shape · size · ndim |
| 3 | [Evenly Spaced Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/evenly-spaced-numbers) | Easy | linspace |
| 4 | [Identity Matrix](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/identity-matrix) | Easy | np.eye |
| 5 | [Read One Cell](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/read-one-cell) | Easy | 2-D indexing |
| 6 | [Last Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/last-column) | Easy | Column slicing |
| 7 | [Reverse an Array](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/reverse-an-array) | Easy | Slicing with step −1 |
| 8 | [Every Second Element](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/every-second-element) | Easy | Step slicing |
| 9 | [Top-Left Block](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/top-left-block) | Easy | 2-D slicing |
| 10 | [Count Values Above a Threshold](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/count-values-above-a-threshold) | Easy | Boolean arrays |
| 11 | [Replace Negatives With Zero](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/replace-negatives-with-zero) | Easy | np.where |
| 12 | [Floats to Whole Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/floats-to-whole-numbers) | Easy | astype |
| 13 | [Flatten a Table](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/flatten-a-table) | Easy | ravel / flatten |
| 14 | [Reshape Into Rows](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/reshape-into-rows) | Easy | reshape |
| 15 | [Stack Two Rows](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/stack-two-rows) | Easy | vstack / hstack |
| 16 | [Main Diagonal](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/main-diagonal) | Easy | np.diag |
| 17 | [Position of the Largest Value](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/position-of-the-largest-value) | Easy | argmax |
| 18 | [Unique Values and Their Counts](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/unique-values-and-their-counts) | Medium | np.unique |
| 19 | [Pick Items by Position](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/pick-items-by-position) | Easy | Fancy indexing |
| 20 | [Checkerboard](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-basics/checkerboard) | Medium | Index arithmetic |

## NumPy Operations

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Add Two Lists Element by Element](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/add-two-lists-element-by-element) | Easy | Element-wise + |
| 2 | [Dot Product](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/dot-product) | Easy | @ / np.dot |
| 3 | [Mean and Standard Deviation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/mean-and-standard-deviation) | Easy | Aggregations |
| 4 | [Scale to 0–1 (Min-Max)](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/scale-to-0-1-min-max) | Easy | Vectorised formula |
| 5 | [Z-Scores](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/z-scores) | Medium | Standardisation |
| 6 | [Row Totals](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/row-totals) | Easy | sum(axis=1) |
| 7 | [Column Averages](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/column-averages) | Easy | mean(axis=0) |
| 8 | [Add a Row to Every Row](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/add-a-row-to-every-row) | Medium | Broadcasting |
| 9 | [Multiplication Table](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/multiplication-table) | Easy | Outer product |
| 10 | [Matrix Multiplication](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/matrix-multiplication) | Medium | @ operator |
| 11 | [Transpose](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/transpose) | Easy | .T |
| 12 | [Running Total](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/running-total) | Easy | cumsum |
| 13 | [Moving Average](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/moving-average) | Medium | cumsum trick / convolve |
| 14 | [Clip to a Range](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/clip-to-a-range) | Easy | np.clip |
| 15 | [Keep the Even Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/keep-the-even-numbers) | Easy | Mask filtering |
| 16 | [Day-to-Day Percent Change](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/day-to-day-percent-change) | Medium | np.diff |
| 17 | [Distance Matrix](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/distance-matrix) | Hard | Broadcasting in 2-D |
| 18 | [Solve Two Equations](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/solve-two-equations) | Medium | np.linalg.solve |
| 19 | [Count Each Value](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/count-each-value) | Easy | np.bincount |
| 20 | [Sort Rows by a Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/numpy-ops/sort-rows-by-a-column) | Medium | argsort |

## Pandas Basics

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Rows and Columns](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/rows-and-columns) | Easy | DataFrame · shape |
| 2 | [Column Names](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/column-names) | Easy | df.columns |
| 3 | [Pick a Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/pick-a-column) | Easy | df[col] → Series |
| 4 | [Pick Several Columns](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/pick-several-columns) | Easy | df[[...]] |
| 5 | [Filter Rows](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/filter-rows) | Easy | Boolean filtering |
| 6 | [Top n by Score](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/top-n-by-score) | Easy | sort_values / nlargest |
| 7 | [Add a Computed Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/add-a-computed-column) | Easy | Vectorised column maths |
| 8 | [loc vs iloc](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/loc-vs-iloc) | Medium | Label vs position |
| 9 | [Rename Columns](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/rename-columns) | Easy | rename |
| 10 | [Count Each Category](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/count-each-category) | Easy | value_counts |
| 11 | [How Many Different Values](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/how-many-different-values) | Easy | nunique |
| 12 | [Quick Summary of a Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/quick-summary-of-a-column) | Easy | describe / agg |
| 13 | [Read CSV Text](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/read-csv-text) | Easy | read_csv |
| 14 | [Drop a Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/drop-a-column) | Easy | drop |
| 15 | [Two Conditions](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/two-conditions) | Medium | & and | |
| 16 | [Rows From a List of Values](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/rows-from-a-list-of-values) | Easy | isin |
| 17 | [Letter Grades Column](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/letter-grades-column) | Easy | apply / map |
| 18 | [Best Subject per Student](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/best-subject-per-student) | Medium | idxmax(axis=1) |
| 19 | [Sort by Two Columns](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/sort-by-two-columns) | Medium | sort_values with a list |
| 20 | [Mean Score per Row Condition](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-basics/mean-score-per-row-condition) | Easy | Boolean mask + aggregation |

## Data Cleaning with Pandas

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Count Missing Values](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/count-missing-values) | Easy | isna().sum() |
| 2 | [Drop Incomplete Rows](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/drop-incomplete-rows) | Easy | dropna |
| 3 | [Fill Gaps With the Average](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/fill-gaps-with-the-average) | Easy | fillna(mean) |
| 4 | [Fill Missing Text](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/fill-missing-text) | Easy | fillna(value) |
| 5 | [Remove Duplicate Rows](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/remove-duplicate-rows) | Easy | drop_duplicates |
| 6 | [Text to Numbers](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/text-to-numbers) | Medium | pd.to_numeric(errors='coerce') |
| 7 | [Tidy Up Text](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/tidy-up-text) | Easy | .str accessor |
| 8 | [Prices From Messy Text](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/prices-from-messy-text) | Medium | str.replace with regex |
| 9 | [Split Full Names](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/split-full-names) | Medium | str.split(expand=True) |
| 10 | [Month From a Date](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/month-from-a-date) | Easy | to_datetime · .dt |
| 11 | [Days Between Two Dates](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/days-between-two-dates) | Medium | Date arithmetic |
| 12 | [Recode Categories](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/recode-categories) | Easy | map with a dict |
| 13 | [Age Groups](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/age-groups) | Medium | pd.cut |
| 14 | [Cap Outliers](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/cap-outliers) | Easy | clip |
| 15 | [Clean Column Names](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/clean-column-names) | Easy | Renaming with str methods |
| 16 | [Fix Column Types](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/fix-column-types) | Medium | astype |
| 17 | [Carry the Last Reading Forward](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/carry-the-last-reading-forward) | Easy | ffill |
| 18 | [Find Invalid Emails](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/find-invalid-emails) | Medium | str.contains with regex |
| 19 | [Fill Gaps by Interpolation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/fill-gaps-by-interpolation) | Medium | interpolate |
| 20 | [Drop Mostly-Empty Columns](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-cleaning/drop-mostly-empty-columns) | Medium | dropna(axis=1, thresh=…) |

## Grouping, Merging & Reshaping

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Total per Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/total-per-group) | Easy | groupby + sum |
| 2 | [Average per Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/average-per-group) | Easy | groupby + mean |
| 3 | [Rows per Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/rows-per-group) | Easy | groupby + size |
| 4 | [Several Statistics at Once](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/several-statistics-at-once) | Medium | agg with named outputs |
| 5 | [Best Product per Region](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/best-product-per-region) | Medium | idxmax within groups |
| 6 | [Join Customers and Orders](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/join-customers-and-orders) | Medium | merge (inner) |
| 7 | [Customers With Their Spending](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/customers-with-their-spending) | Medium | left join + fillna |
| 8 | [Stack Two Tables](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/stack-two-tables) | Easy | concat |
| 9 | [Pivot Table](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/pivot-table) | Medium | pivot_table |
| 10 | [Wide to Long (melt)](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/wide-to-long-melt) | Medium | melt |
| 11 | [Cross Tabulation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/cross-tabulation) | Medium | crosstab |
| 12 | [Share of Group Total](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/share-of-group-total) | Medium | transform |
| 13 | [Rank Within Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/rank-within-group) | Medium | groupby + rank |
| 14 | [Running Total per Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/running-total-per-group) | Medium | groupby + cumsum |
| 15 | [Monthly Totals From Daily Data](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/monthly-totals-from-daily-data) | Medium | Group by month |
| 16 | [Rolling 3-Day Average](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/rolling-3-day-average) | Medium | rolling |
| 17 | [Groups From Two Keys to a Table](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/groups-from-two-keys-to-a-table) | Medium | unstack |
| 18 | [Keep Big Groups Only](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/keep-big-groups-only) | Medium | groupby + filter |
| 19 | [Customers Without Orders](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/customers-without-orders) | Medium | Anti-join |
| 20 | [First and Last per Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/pandas-grouping/first-and-last-per-group) | Easy | groupby + first / last |

## Matplotlib

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Line Chart](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/line-chart) | Easy | plot · title |
| 2 | [Two Lines With a Legend](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/two-lines-with-a-legend) | Easy | label · legend |
| 3 | [Bar Chart](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/bar-chart) | Easy | bar |
| 4 | [Sorted Horizontal Bars](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/sorted-horizontal-bars) | Medium | barh + sorting |
| 5 | [Scatter Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/scatter-plot) | Easy | scatter |
| 6 | [Histogram](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/histogram) | Easy | hist |
| 7 | [Pie Chart With Percentages](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/pie-chart-with-percentages) | Easy | pie · autopct |
| 8 | [Two Charts Side by Side](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/two-charts-side-by-side) | Medium | subplots(1, 2) |
| 9 | [Labels and Limits](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/labels-and-limits) | Easy | ax.set |
| 10 | [Stacked Bars](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/stacked-bars) | Medium | bottom= |
| 11 | [Grouped Bars](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/grouped-bars) | Medium | Offsetting bar positions |
| 12 | [Mark the Highest Point](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/mark-the-highest-point) | Medium | annotate |
| 13 | [Markers and Line Styles](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/markers-and-line-styles) | Easy | Format options |
| 14 | [Error Bars](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/error-bars) | Medium | errorbar |
| 15 | [Shaded Range](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/shaded-range) | Medium | fill_between |
| 16 | [Two Different Y Scales](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/two-different-y-scales) | Hard | twinx |
| 17 | [Box Plot of Groups](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/box-plot-of-groups) | Medium | boxplot |
| 18 | [Logarithmic Scale](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/logarithmic-scale) | Easy | set_yscale('log') |
| 19 | [2 × 2 Small Multiples](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/2-2-small-multiples) | Medium | subplots grid |
| 20 | [Save a Chart as PNG](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/matplotlib/save-a-chart-as-png) | Easy | savefig |

## Seaborn

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Histogram](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/histogram) | Easy | histplot |
| 2 | [Smooth Density Curve](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/smooth-density-curve) | Medium | kdeplot |
| 3 | [Box Plot by Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/box-plot-by-group) | Easy | boxplot |
| 4 | [Violin Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/violin-plot) | Easy | violinplot |
| 5 | [Count Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/count-plot) | Easy | countplot |
| 6 | [Bar Plot of Averages](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/bar-plot-of-averages) | Easy | barplot |
| 7 | [Scatter Coloured by Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/scatter-coloured-by-group) | Easy | scatterplot(hue=) |
| 8 | [Lines per Group Over Time](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/lines-per-group-over-time) | Medium | lineplot(hue=) |
| 9 | [Correlation Heat Map](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/correlation-heat-map) | Medium | heatmap(annot=True) |
| 10 | [Scatter With a Trend Line](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/scatter-with-a-trend-line) | Medium | regplot |
| 11 | [Strip Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/strip-plot) | Easy | stripplot |
| 12 | [Point Plot of Means](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/point-plot-of-means) | Medium | pointplot |
| 13 | [Stacked Histogram by Group](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/stacked-histogram-by-group) | Medium | histplot(hue=, multiple='stack') |
| 14 | [Cumulative Distribution (ECDF)](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/cumulative-distribution-ecdf) | Medium | ecdfplot |
| 15 | [Bars in a Chosen Order](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/bars-in-a-chosen-order) | Easy | order= |
| 16 | [One Panel per Category](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/one-panel-per-category) | Medium | relplot(col=) |
| 17 | [Pair Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/pair-plot) | Medium | pairplot |
| 18 | [Joint Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/joint-plot) | Hard | jointplot |
| 19 | [Totals, Largest First](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/totals-largest-first) | Medium | barplot(estimator=sum, order=…) |
| 20 | [Grouped Count Plot](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/seaborn/grouped-count-plot) | Medium | countplot(hue=) |

## Statistics for Data Analysis

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Mean, Median and Mode](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/mean-median-and-mode) | Easy | Measures of centre |
| 2 | [Range and Interquartile Range](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/range-and-interquartile-range) | Easy | Spread · percentiles |
| 3 | [Population vs Sample Standard Deviation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/population-vs-sample-standard-deviation) | Medium | ddof |
| 4 | [Percentile Rank](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/percentile-rank) | Easy | Share of values ≤ x |
| 5 | [Outliers by Z-Score](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/outliers-by-z-score) | Medium | Standardisation |
| 6 | [Outliers by the IQR Rule](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/outliers-by-the-iqr-rule) | Medium | Tukey's fences |
| 7 | [Pearson Correlation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/pearson-correlation) | Medium | np.corrcoef |
| 8 | [Sample Covariance](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/sample-covariance) | Easy | np.cov |
| 9 | [Weighted Average](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/weighted-average) | Easy | np.average(weights=) |
| 10 | [Average Yearly Growth (CAGR)](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/average-yearly-growth-cagr) | Easy | Geometric mean |
| 11 | [Coefficient of Variation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/coefficient-of-variation) | Easy | Relative spread |
| 12 | [Fit a Straight Line](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/fit-a-straight-line) | Medium | Least squares · polyfit |
| 13 | [Predict With the Line](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/predict-with-the-line) | Easy | Applying a model |
| 14 | [R² of a Fit](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/r-of-a-fit) | Medium | Goodness of fit |
| 15 | [Relative Frequency Table](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/relative-frequency-table) | Easy | value_counts(normalize=True) |
| 16 | [Skewness](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/skewness) | Medium | Third standardised moment |
| 17 | [95% Confidence Interval for the Mean](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/95-confidence-interval-for-the-mean) | Medium | Standard error |
| 18 | [Probability From Data](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/probability-from-data) | Easy | Empirical probability |
| 19 | [Binomial Probability](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/binomial-probability) | Medium | math.comb |
| 20 | [Spearman Rank Correlation](https://abpandey-dev.github.io/python-dsa-visualizer/data-science/#/q/statistics/spearman-rank-correlation) | Hard | Correlation of ranks |

## Build

```bash
python3 handbook/build.py --book data-science
```

Sources live in `data-science/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
