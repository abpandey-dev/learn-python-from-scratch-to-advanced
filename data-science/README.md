# Python for Data Science

12 topics · theory with 75 theory questions · 101 lessons from basics to advanced · 240 practice questions with answers · NumPy, Pandas, Matplotlib, Seaborn, statistics, SQL from Python, hypothesis testing, EDA and business KPIs, and time series forecasting · every question has a plain-Python brute-force answer and an optimal vectorised or library answer, both shown running line by line, with the charts they draw.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/

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
- [SQL from Python](#sql-from-python) — Query a real database from Python: sqlite3 connections, safe parameters, joins, GROUP BY and HAVING, subqueries, window functions, dates, upserts, transactions, and moving data between SQL and pandas.
- [Hypothesis Testing & Inference](#hypothesis-testing-inference) — Decide whether a difference is real or luck: null and alternative hypotheses, p-values, z and t tests, chi-square, ANOVA, non-parametric and permutation tests, the bootstrap, power and sample size, effect sizes and multiple testing.
- [EDA, Business KPIs & Storytelling](#eda-business-kpis-storytelling) — Explore a new dataset systematically, turn Excel habits (VLOOKUP, pivot tables, SUMIFS, IF) into pandas, and compute the metrics businesses run on: funnels, cohorts and retention, churn, ARPU, LTV, growth, Pareto shares and what drove a change.
- [Time Series & Forecasting](#time-series-forecasting) — Work with data ordered in time: resampling and missing dates, lags, rolling and exponential averages, trend and seasonality, autocorrelation, baseline and smoothing forecasts, autoregression, honest time-based validation, forecast errors and anomaly flags.

## NumPy Basics

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Double Every Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/double-every-number) | Easy | Vectorised arithmetic |
| 2 | [Shape and Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/shape-and-size) | Easy | shape · size · ndim |
| 3 | [Evenly Spaced Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/evenly-spaced-numbers) | Easy | linspace |
| 4 | [Identity Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/identity-matrix) | Easy | np.eye |
| 5 | [Read One Cell](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/read-one-cell) | Easy | 2-D indexing |
| 6 | [Last Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/last-column) | Easy | Column slicing |
| 7 | [Reverse an Array](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/reverse-an-array) | Easy | Slicing with step −1 |
| 8 | [Every Second Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/every-second-element) | Easy | Step slicing |
| 9 | [Top-Left Block](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/top-left-block) | Easy | 2-D slicing |
| 10 | [Count Values Above a Threshold](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/count-values-above-a-threshold) | Easy | Boolean arrays |
| 11 | [Replace Negatives With Zero](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/replace-negatives-with-zero) | Easy | np.where |
| 12 | [Floats to Whole Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/floats-to-whole-numbers) | Easy | astype |
| 13 | [Flatten a Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/flatten-a-table) | Easy | ravel / flatten |
| 14 | [Reshape Into Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/reshape-into-rows) | Easy | reshape |
| 15 | [Stack Two Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/stack-two-rows) | Easy | vstack / hstack |
| 16 | [Main Diagonal](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/main-diagonal) | Easy | np.diag |
| 17 | [Position of the Largest Value](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/position-of-the-largest-value) | Easy | argmax |
| 18 | [Unique Values and Their Counts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/unique-values-and-their-counts) | Medium | np.unique |
| 19 | [Pick Items by Position](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/pick-items-by-position) | Easy | Fancy indexing |
| 20 | [Checkerboard](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-basics/checkerboard) | Medium | Index arithmetic |

## NumPy Operations

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Add Two Lists Element by Element](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/add-two-lists-element-by-element) | Easy | Element-wise + |
| 2 | [Dot Product](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/dot-product) | Easy | @ / np.dot |
| 3 | [Mean and Standard Deviation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/mean-and-standard-deviation) | Easy | Aggregations |
| 4 | [Scale to 0–1 (Min-Max)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/scale-to-0-1-min-max) | Easy | Vectorised formula |
| 5 | [Z-Scores](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/z-scores) | Medium | Standardisation |
| 6 | [Row Totals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/row-totals) | Easy | sum(axis=1) |
| 7 | [Column Averages](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/column-averages) | Easy | mean(axis=0) |
| 8 | [Add a Row to Every Row](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/add-a-row-to-every-row) | Medium | Broadcasting |
| 9 | [Multiplication Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/multiplication-table) | Easy | Outer product |
| 10 | [Matrix Multiplication](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/matrix-multiplication) | Medium | @ operator |
| 11 | [Transpose](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/transpose) | Easy | .T |
| 12 | [Running Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/running-total) | Easy | cumsum |
| 13 | [Moving Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/moving-average) | Medium | cumsum trick / convolve |
| 14 | [Clip to a Range](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/clip-to-a-range) | Easy | np.clip |
| 15 | [Keep the Even Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/keep-the-even-numbers) | Easy | Mask filtering |
| 16 | [Day-to-Day Percent Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/day-to-day-percent-change) | Medium | np.diff |
| 17 | [Distance Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/distance-matrix) | Hard | Broadcasting in 2-D |
| 18 | [Solve Two Equations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/solve-two-equations) | Medium | np.linalg.solve |
| 19 | [Count Each Value](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/count-each-value) | Easy | np.bincount |
| 20 | [Sort Rows by a Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/numpy-ops/sort-rows-by-a-column) | Medium | argsort |

## Pandas Basics

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Rows and Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/rows-and-columns) | Easy | DataFrame · shape |
| 2 | [Column Names](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/column-names) | Easy | df.columns |
| 3 | [Pick a Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/pick-a-column) | Easy | df[col] → Series |
| 4 | [Pick Several Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/pick-several-columns) | Easy | df[[...]] |
| 5 | [Filter Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/filter-rows) | Easy | Boolean filtering |
| 6 | [Top n by Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/top-n-by-score) | Easy | sort_values / nlargest |
| 7 | [Add a Computed Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/add-a-computed-column) | Easy | Vectorised column maths |
| 8 | [loc vs iloc](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/loc-vs-iloc) | Medium | Label vs position |
| 9 | [Rename Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/rename-columns) | Easy | rename |
| 10 | [Count Each Category](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/count-each-category) | Easy | value_counts |
| 11 | [How Many Different Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/how-many-different-values) | Easy | nunique |
| 12 | [Quick Summary of a Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/quick-summary-of-a-column) | Easy | describe / agg |
| 13 | [Read CSV Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/read-csv-text) | Easy | read_csv |
| 14 | [Drop a Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/drop-a-column) | Easy | drop |
| 15 | [Two Conditions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/two-conditions) | Medium | & and | |
| 16 | [Rows From a List of Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/rows-from-a-list-of-values) | Easy | isin |
| 17 | [Letter Grades Column](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/letter-grades-column) | Easy | apply / map |
| 18 | [Best Subject per Student](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/best-subject-per-student) | Medium | idxmax(axis=1) |
| 19 | [Sort by Two Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/sort-by-two-columns) | Medium | sort_values with a list |
| 20 | [Mean Score per Row Condition](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-basics/mean-score-per-row-condition) | Easy | Boolean mask + aggregation |

## Data Cleaning with Pandas

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Count Missing Values](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/count-missing-values) | Easy | isna().sum() |
| 2 | [Drop Incomplete Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/drop-incomplete-rows) | Easy | dropna |
| 3 | [Fill Gaps With the Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/fill-gaps-with-the-average) | Easy | fillna(mean) |
| 4 | [Fill Missing Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/fill-missing-text) | Easy | fillna(value) |
| 5 | [Remove Duplicate Rows](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/remove-duplicate-rows) | Easy | drop_duplicates |
| 6 | [Text to Numbers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/text-to-numbers) | Medium | pd.to_numeric(errors='coerce') |
| 7 | [Tidy Up Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/tidy-up-text) | Easy | .str accessor |
| 8 | [Prices From Messy Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/prices-from-messy-text) | Medium | str.replace with regex |
| 9 | [Split Full Names](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/split-full-names) | Medium | str.split(expand=True) |
| 10 | [Month From a Date](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/month-from-a-date) | Easy | to_datetime · .dt |
| 11 | [Days Between Two Dates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/days-between-two-dates) | Medium | Date arithmetic |
| 12 | [Recode Categories](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/recode-categories) | Easy | map with a dict |
| 13 | [Age Groups](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/age-groups) | Medium | pd.cut |
| 14 | [Cap Outliers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/cap-outliers) | Easy | clip |
| 15 | [Clean Column Names](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/clean-column-names) | Easy | Renaming with str methods |
| 16 | [Fix Column Types](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/fix-column-types) | Medium | astype |
| 17 | [Carry the Last Reading Forward](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/carry-the-last-reading-forward) | Easy | ffill |
| 18 | [Find Invalid Emails](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/find-invalid-emails) | Medium | str.contains with regex |
| 19 | [Fill Gaps by Interpolation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/fill-gaps-by-interpolation) | Medium | interpolate |
| 20 | [Drop Mostly-Empty Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-cleaning/drop-mostly-empty-columns) | Medium | dropna(axis=1, thresh=…) |

## Grouping, Merging & Reshaping

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Total per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/total-per-group) | Easy | groupby + sum |
| 2 | [Average per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/average-per-group) | Easy | groupby + mean |
| 3 | [Rows per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/rows-per-group) | Easy | groupby + size |
| 4 | [Several Statistics at Once](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/several-statistics-at-once) | Medium | agg with named outputs |
| 5 | [Best Product per Region](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/best-product-per-region) | Medium | idxmax within groups |
| 6 | [Join Customers and Orders](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/join-customers-and-orders) | Medium | merge (inner) |
| 7 | [Customers With Their Spending](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/customers-with-their-spending) | Medium | left join + fillna |
| 8 | [Stack Two Tables](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/stack-two-tables) | Easy | concat |
| 9 | [Pivot Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/pivot-table) | Medium | pivot_table |
| 10 | [Wide to Long (melt)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/wide-to-long-melt) | Medium | melt |
| 11 | [Cross Tabulation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/cross-tabulation) | Medium | crosstab |
| 12 | [Share of Group Total](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/share-of-group-total) | Medium | transform |
| 13 | [Rank Within Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/rank-within-group) | Medium | groupby + rank |
| 14 | [Running Total per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/running-total-per-group) | Medium | groupby + cumsum |
| 15 | [Monthly Totals From Daily Data](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/monthly-totals-from-daily-data) | Medium | Group by month |
| 16 | [Rolling 3-Day Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/rolling-3-day-average) | Medium | rolling |
| 17 | [Groups From Two Keys to a Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/groups-from-two-keys-to-a-table) | Medium | unstack |
| 18 | [Keep Big Groups Only](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/keep-big-groups-only) | Medium | groupby + filter |
| 19 | [Customers Without Orders](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/customers-without-orders) | Medium | Anti-join |
| 20 | [First and Last per Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/pandas-grouping/first-and-last-per-group) | Easy | groupby + first / last |

## Matplotlib

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Line Chart](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/line-chart) | Easy | plot · title |
| 2 | [Two Lines With a Legend](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/two-lines-with-a-legend) | Easy | label · legend |
| 3 | [Bar Chart](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/bar-chart) | Easy | bar |
| 4 | [Sorted Horizontal Bars](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/sorted-horizontal-bars) | Medium | barh + sorting |
| 5 | [Scatter Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/scatter-plot) | Easy | scatter |
| 6 | [Histogram](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/histogram) | Easy | hist |
| 7 | [Pie Chart With Percentages](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/pie-chart-with-percentages) | Easy | pie · autopct |
| 8 | [Two Charts Side by Side](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/two-charts-side-by-side) | Medium | subplots(1, 2) |
| 9 | [Labels and Limits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/labels-and-limits) | Easy | ax.set |
| 10 | [Stacked Bars](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/stacked-bars) | Medium | bottom= |
| 11 | [Grouped Bars](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/grouped-bars) | Medium | Offsetting bar positions |
| 12 | [Mark the Highest Point](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/mark-the-highest-point) | Medium | annotate |
| 13 | [Markers and Line Styles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/markers-and-line-styles) | Easy | Format options |
| 14 | [Error Bars](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/error-bars) | Medium | errorbar |
| 15 | [Shaded Range](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/shaded-range) | Medium | fill_between |
| 16 | [Two Different Y Scales](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/two-different-y-scales) | Hard | twinx |
| 17 | [Box Plot of Groups](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/box-plot-of-groups) | Medium | boxplot |
| 18 | [Logarithmic Scale](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/logarithmic-scale) | Easy | set_yscale('log') |
| 19 | [2 × 2 Small Multiples](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/2-2-small-multiples) | Medium | subplots grid |
| 20 | [Save a Chart as PNG](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/matplotlib/save-a-chart-as-png) | Easy | savefig |

## Seaborn

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Histogram](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/histogram) | Easy | histplot |
| 2 | [Smooth Density Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/smooth-density-curve) | Medium | kdeplot |
| 3 | [Box Plot by Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/box-plot-by-group) | Easy | boxplot |
| 4 | [Violin Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/violin-plot) | Easy | violinplot |
| 5 | [Count Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/count-plot) | Easy | countplot |
| 6 | [Bar Plot of Averages](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/bar-plot-of-averages) | Easy | barplot |
| 7 | [Scatter Coloured by Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/scatter-coloured-by-group) | Easy | scatterplot(hue=) |
| 8 | [Lines per Group Over Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/lines-per-group-over-time) | Medium | lineplot(hue=) |
| 9 | [Correlation Heat Map](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/correlation-heat-map) | Medium | heatmap(annot=True) |
| 10 | [Scatter With a Trend Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/scatter-with-a-trend-line) | Medium | regplot |
| 11 | [Strip Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/strip-plot) | Easy | stripplot |
| 12 | [Point Plot of Means](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/point-plot-of-means) | Medium | pointplot |
| 13 | [Stacked Histogram by Group](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/stacked-histogram-by-group) | Medium | histplot(hue=, multiple='stack') |
| 14 | [Cumulative Distribution (ECDF)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/cumulative-distribution-ecdf) | Medium | ecdfplot |
| 15 | [Bars in a Chosen Order](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/bars-in-a-chosen-order) | Easy | order= |
| 16 | [One Panel per Category](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/one-panel-per-category) | Medium | relplot(col=) |
| 17 | [Pair Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/pair-plot) | Medium | pairplot |
| 18 | [Joint Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/joint-plot) | Hard | jointplot |
| 19 | [Totals, Largest First](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/totals-largest-first) | Medium | barplot(estimator=sum, order=…) |
| 20 | [Grouped Count Plot](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/seaborn/grouped-count-plot) | Medium | countplot(hue=) |

## Statistics for Data Analysis

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Mean, Median and Mode](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/mean-median-and-mode) | Easy | Measures of centre |
| 2 | [Range and Interquartile Range](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/range-and-interquartile-range) | Easy | Spread · percentiles |
| 3 | [Population vs Sample Standard Deviation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/population-vs-sample-standard-deviation) | Medium | ddof |
| 4 | [Percentile Rank](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/percentile-rank) | Easy | Share of values ≤ x |
| 5 | [Outliers by Z-Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/outliers-by-z-score) | Medium | Standardisation |
| 6 | [Outliers by the IQR Rule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/outliers-by-the-iqr-rule) | Medium | Tukey's fences |
| 7 | [Pearson Correlation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/pearson-correlation) | Medium | np.corrcoef |
| 8 | [Sample Covariance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/sample-covariance) | Easy | np.cov |
| 9 | [Weighted Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/weighted-average) | Easy | np.average(weights=) |
| 10 | [Average Yearly Growth (CAGR)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/average-yearly-growth-cagr) | Easy | Geometric mean |
| 11 | [Coefficient of Variation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/coefficient-of-variation) | Easy | Relative spread |
| 12 | [Fit a Straight Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/fit-a-straight-line) | Medium | Least squares · polyfit |
| 13 | [Predict With the Line](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/predict-with-the-line) | Easy | Applying a model |
| 14 | [R² of a Fit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/r-of-a-fit) | Medium | Goodness of fit |
| 15 | [Relative Frequency Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/relative-frequency-table) | Easy | value_counts(normalize=True) |
| 16 | [Skewness](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/skewness) | Medium | Third standardised moment |
| 17 | [95% Confidence Interval for the Mean](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/95-confidence-interval-for-the-mean) | Medium | Standard error |
| 18 | [Probability From Data](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/probability-from-data) | Easy | Empirical probability |
| 19 | [Binomial Probability](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/binomial-probability) | Medium | math.comb |
| 20 | [Spearman Rank Correlation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/statistics/spearman-rank-correlation) | Hard | Correlation of ranks |

## SQL from Python

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Load Rows and Count Them](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/load-rows-and-count-them) | Easy | CREATE · executemany |
| 2 | [Orders Above an Amount](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/orders-above-an-amount) | Easy | WHERE with a parameter |
| 3 | [Safe Lookup by Name](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/safe-lookup-by-name) | Medium | SQL injection |
| 4 | [Revenue per City](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/revenue-per-city) | Easy | JOIN + GROUP BY |
| 5 | [Customers With No Orders](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/customers-with-no-orders) | Easy | LEFT JOIN … IS NULL |
| 6 | [Big Spenders](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/big-spenders) | Medium | HAVING |
| 7 | [Orders Above Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/orders-above-average) | Medium | Subquery |
| 8 | [Biggest Order per Customer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/biggest-order-per-customer) | Medium | ROW_NUMBER() OVER (PARTITION BY …) |
| 9 | [Running Total per Customer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/running-total-per-customer) | Medium | SUM() OVER (ORDER BY …) |
| 10 | [Bucket Orders by Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/bucket-orders-by-size) | Easy | CASE WHEN |
| 11 | [Monthly Revenue](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/monthly-revenue) | Easy | Dates with strftime |
| 12 | [Second-Highest Order Amount](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/second-highest-order-amount) | Medium | DISTINCT · LIMIT/OFFSET |
| 13 | [Days With Several Customers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/days-with-several-customers) | Easy | COUNT(DISTINCT …) |
| 14 | [Query Straight into a DataFrame](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/query-straight-into-a-dataframe) | Easy | pd.read_sql_query |
| 15 | [From a DataFrame to a Table and Back](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/from-a-dataframe-to-a-table-and-back) | Medium | df.to_sql |
| 16 | [Upsert Stock Levels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/upsert-stock-levels) | Medium | INSERT … ON CONFLICT |
| 17 | [All-or-Nothing Transfers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/all-or-nothing-transfers) | Hard | Transactions · rollback |
| 18 | [Pivot Months into Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/pivot-months-into-columns) | Medium | Conditional aggregation |
| 19 | [Keep the Latest Version of Each Record](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/keep-the-latest-version-of-each-record) | Hard | De-duplication |
| 20 | [Does the Query Use the Index?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/sql-python/does-the-query-use-the-index) | Medium | Indexes · EXPLAIN QUERY PLAN |

## Hypothesis Testing & Inference

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [One-Sample z-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/one-sample-z-test) | Easy | Known σ · two-sided p |
| 2 | [One-Sample t Statistic](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/one-sample-t-statistic) | Easy | Unknown σ |
| 3 | [Welch's t-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/welchs-t-test) | Medium | Two groups, unequal variances |
| 4 | [Pooled Two-Sample t-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/pooled-two-sample-t-test) | Medium | Equal variances |
| 5 | [Paired t-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/paired-t-test) | Medium | Before and after |
| 6 | [A/B Test on Conversion Rates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/a-b-test-on-conversion-rates) | Medium | Two-proportion z-test |
| 7 | [Is the Die Fair?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/is-the-die-fair) | Medium | Chi-square goodness of fit |
| 8 | [Are Two Categories Related?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/are-two-categories-related) | Medium | Chi-square independence |
| 9 | [One-Way ANOVA](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/one-way-anova) | Medium | Three or more means |
| 10 | [One-Tailed or Two-Tailed?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/one-tailed-or-two-tailed) | Easy | Alternative hypotheses |
| 11 | [Confidence Interval for a Difference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/confidence-interval-for-a-difference) | Medium | Large-sample CI |
| 12 | [How Many Users Does the A/B Test Need?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/how-many-users-does-the-a-b-test-need) | Hard | Sample size |
| 13 | [Power of a z-Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/power-of-a-z-test) | Medium | Chance of catching a real effect |
| 14 | [Permutation Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/permutation-test) | Hard | No formula needed |
| 15 | [Bootstrap Confidence Interval](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/bootstrap-confidence-interval) | Medium | Resampling |
| 16 | [Bonferroni Correction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/bonferroni-correction) | Easy | Many tests at once |
| 17 | [False Discovery Rate (Benjamini–Hochberg)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/false-discovery-rate-benjamini-hochberg) | Hard | Adjusted p-values |
| 18 | [Mann–Whitney U](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/mann-whitney-u) | Medium | Ranks instead of means |
| 19 | [Effect Size: Cohen's d](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/effect-size-cohens-d) | Easy | How big, not just whether |
| 20 | [Exact Binomial Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/hypothesis-testing/exact-binomial-test) | Medium | Small samples, one proportion |

## EDA, Business KPIs & Storytelling

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Profile a New Dataset](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/profile-a-new-dataset) | Easy | First look |
| 2 | [Which Way Is It Skewed?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/which-way-is-it-skewed) | Medium | Skewness |
| 3 | [Most Correlated Pair of Columns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/most-correlated-pair-of-columns) | Medium | Correlation matrix |
| 4 | [Segment Summary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/segment-summary) | Easy | Category vs number |
| 5 | [VLOOKUP in pandas](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/vlookup-in-pandas) | Easy | Left merge |
| 6 | [Pivot Table With Totals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/pivot-table-with-totals) | Medium | pivot_table(margins=True) |
| 7 | [SUMIFS](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/sumifs) | Easy | Sum with several conditions |
| 8 | [Nested IF to Labels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/nested-if-to-labels) | Easy | np.select |
| 9 | [Conversion Funnel](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/conversion-funnel) | Medium | Step-to-step conversion |
| 10 | [Cohort Retention Table](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/cohort-retention-table) | Hard | Cohorts |
| 11 | [Monthly Churn Rate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/monthly-churn-rate) | Medium | Who didn't come back |
| 12 | [ARPU and ARPPU](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/arpu-and-arppu) | Easy | Revenue per user |
| 13 | [Month-over-Month Growth](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/month-over-month-growth) | Easy | pct_change |
| 14 | [The 80/20 Check](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/the-80-20-check) | Medium | Pareto share |
| 15 | [Customer Lifetime Value](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/customer-lifetime-value) | Easy | LTV |
| 16 | [Repeat Purchase Rate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/repeat-purchase-rate) | Easy | Loyalty |
| 17 | [What Drove the Change?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/what-drove-the-change) | Medium | Contribution analysis |
| 18 | [Top N and 'Other'](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/top-n-and-other) | Easy | Charts people can read |
| 19 | [Bucket Values into Ranges](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/bucket-values-into-ranges) | Easy | pd.cut (Excel FREQUENCY) |
| 20 | [Stickiness: DAU / MAU](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/eda-kpis/stickiness-dau-mau) | Medium | Engagement |

## Time Series & Forecasting

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Daily to Weekly Totals](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/daily-to-weekly-totals) | Easy | resample |
| 2 | [Fill Missing Dates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/fill-missing-dates) | Easy | asfreq |
| 3 | [Lags and Differences](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/lags-and-differences) | Easy | shift · diff |
| 4 | [Rolling Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/rolling-average) | Easy | Smoothing noise |
| 5 | [Exponential Moving Average](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/exponential-moving-average) | Medium | ewm |
| 6 | [Baseline Forecasts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/baseline-forecasts) | Easy | Naive, mean, seasonal naive |
| 7 | [Forecast Error Metrics](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/forecast-error-metrics) | Easy | MAE, RMSE, MAPE |
| 8 | [Which Baseline Wins?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/which-baseline-wins) | Medium | Backtesting |
| 9 | [Straight-Line Trend Forecast](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/straight-line-trend-forecast) | Easy | Linear trend |
| 10 | [Seasonal Indices](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/seasonal-indices) | Medium | Classical decomposition |
| 11 | [Autocorrelation at a Lag](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/autocorrelation-at-a-lag) | Medium | Does it repeat? |
| 12 | [Find the Season Length](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/find-the-season-length) | Medium | Peak autocorrelation |
| 13 | [Walk-Forward Validation Splits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/walk-forward-validation-splits) | Medium | Never train on the future |
| 14 | [Year-over-Year Change](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/year-over-year-change) | Easy | Compare with the same season |
| 15 | [Flag Anomalies](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/flag-anomalies) | Medium | Rolling z-score |
| 16 | [Returns and Compound Growth](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/returns-and-compound-growth) | Easy | pct_change · cumprod |
| 17 | [Average by Day of the Week](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/average-by-day-of-the-week) | Easy | Calendar features |
| 18 | [Turn a Series into a Supervised Dataset](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/turn-a-series-into-a-supervised-dataset) | Medium | Lag features |
| 19 | [Autoregressive Forecast AR(1)](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/autoregressive-forecast-ar-1) | Hard | Regress on the past |
| 20 | [Tune the Smoothing Factor](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/data-science/#/q/time-series/tune-the-smoothing-factor) | Medium | Simple exponential smoothing |

## Build

```bash
python3 handbook/build.py --book data-science
```

Sources live in `data-science/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
