from lib import *

THEORY("Data cleaning (data wrangling)", """
<p><b>Data cleaning</b> is the process of detecting and correcting (or removing) inaccurate, incomplete, inconsistent, duplicated or irrelevant data so that analysis is valid. It is part of <b>data wrangling / data preparation</b>, which commonly takes the majority of an analyst's time.</p>
<h4>Dimensions of data quality</h4>
<table>
<tr><th>Dimension</th><th>Question</th><th>Example problem</th></tr>
<tr><td>Completeness</td><td>Is anything missing?</td><td>blank ages</td></tr>
<tr><td>Validity</td><td>Does it follow the rules?</td><td>age = −4, email without @</td></tr>
<tr><td>Accuracy</td><td>Is it correct?</td><td>typo in a salary</td></tr>
<tr><td>Consistency</td><td>Is it the same everywhere?</td><td>"Pune", "pune ", "PNQ"</td></tr>
<tr><td>Uniqueness</td><td>Any duplicates?</td><td>the same order twice</td></tr>
<tr><td>Timeliness</td><td>Is it current?</td><td>last year's prices</td></tr>
</table>
""")

THEORY("Missing data", """
<p>Representations: <code>np.nan</code> (float), <code>None</code> (object), <code>pd.NA</code> (nullable dtypes), <code>pd.NaT</code> (datetimes). <code>isna()</code> detects all of them.</p>
<h4>Why data is missing</h4>
<ul>
<li><b>MCAR</b> — missing completely at random (a sensor glitch): dropping rows is unbiased.</li>
<li><b>MAR</b> — missing at random given other columns (older people skip the income question): impute using those columns.</li>
<li><b>MNAR</b> — missing not at random (high earners hide income): any simple fix is biased; flag it.</li>
</ul>
<h4>Strategies</h4>
<table>
<tr><th>Strategy</th><th>pandas</th><th>Trade-off</th></tr>
<tr><td>Delete rows / columns</td><td><code>dropna</code></td><td>loses data; biased unless MCAR</td></tr>
<tr><td>Constant / "Unknown"</td><td><code>fillna(value)</code></td><td>simple; may create a fake category</td></tr>
<tr><td>Mean / median / mode</td><td><code>fillna(s.mean())</code></td><td>keeps rows; shrinks variance (median is robust to outliers)</td></tr>
<tr><td>Forward / backward fill</td><td><code>ffill</code>, <code>bfill</code></td><td>good for ordered/time data</td></tr>
<tr><td>Interpolation</td><td><code>interpolate</code></td><td>smooth series; assumes a trend</td></tr>
<tr><td>Model-based</td><td>scikit-learn imputers</td><td>most accurate; more work</td></tr>
</table>
<p>Adding an indicator column (<code>df["age_missing"] = df["age"].isna()</code>) keeps the information that a value was imputed.</p>
""")

THEORY("Types, duplicates and text", """
<ul>
<li><b>Type conversion</b>: <code>astype</code> (strict), <code>pd.to_numeric(errors="coerce")</code>, <code>pd.to_datetime(errors="coerce", format=…)</code>, <code>astype("category")</code>.</li>
<li><b>Duplicates</b>: <code>duplicated(subset=, keep="first"|"last"|False)</code>, <code>drop_duplicates</code>. Decide which columns define "the same record".</li>
<li><b>Text normalisation</b>: strip whitespace, unify case, remove punctuation/currency symbols, standardise spellings with <code>replace</code>/<code>map</code>.</li>
<li><b>Regular expressions</b> in <code>.str.replace/contains/extract/match</code>: <code>\\d</code> digit, <code>\\D</code> non-digit, <code>\\s</code> whitespace, <code>+</code> one or more, <code>^ $</code> start/end.</li>
</ul>
""")

THEORY("Dates and times", """
<table>
<tr><th>Object</th><th>Meaning</th></tr>
<tr><td><code>Timestamp</code> / <code>datetime64</code></td><td>a moment in time</td></tr>
<tr><td><code>Timedelta</code></td><td>a duration (difference of two timestamps)</td></tr>
<tr><td><code>Period</code></td><td>a span such as a month (<code>to_period("M")</code>)</td></tr>
<tr><td><code>DatetimeIndex</code></td><td>an index of dates, enabling <code>resample</code> and date slicing</td></tr>
</table>
<p>The <code>.dt</code> accessor exposes parts: <code>year, month, day, dayofweek, day_name(), hour, quarter, is_month_end</code>. Time zones: <code>tz_localize</code>, <code>tz_convert</code>.</p>
""")

THEORY("Outliers", """
<p>An <b>outlier</b> is a value far from the rest. It may be an error (typo, unit mix-up) or a genuine extreme (a celebrity's income).</p>
<table>
<tr><th>Detection rule</th><th>Outlier if</th></tr>
<tr><td>IQR (Tukey's fences)</td><td>x &lt; Q1 − 1.5·IQR or x &gt; Q3 + 1.5·IQR</td></tr>
<tr><td>Z-score</td><td>|x − mean| / std &gt; 3</td></tr>
<tr><td>Domain rules</td><td>age &gt; 120, negative price</td></tr>
</table>
<p>Treatments: correct, remove, cap (<b>winsorise</b> with <code>clip</code>), transform (log), or keep and use robust statistics (median, IQR).</p>
""")

FAQ("dropna or fillna?", "<p>Drop when few rows are affected and missingness is random; fill when you can't afford to lose rows or the gap has a sensible value. Always record the choice, and consider an indicator column.</p>")
FAQ("Why fill with the median rather than the mean?", "<p>The median isn't pulled by outliers, so it's a safer typical value for skewed data such as incomes or prices.</p>")
FAQ("What does errors='coerce' do?", "<p>Values that can't be converted become NaN (or NaT for dates) instead of raising an error, so you can count and handle them afterwards.</p>")
FAQ("How do you find duplicate rows?", "<p><code>df.duplicated()</code> marks repeats (all but the first by default); <code>df.duplicated().sum()</code> counts them; <code>drop_duplicates(subset=[...])</code> removes them based on chosen columns.</p>")
FAQ("ffill vs interpolate?", "<p>ffill copies the last known value forward (step-like). interpolate draws a line between known neighbours (smooth). Both need the data in a meaningful order.</p>")
FAQ("What is the category dtype for?", "<p>Columns with few distinct repeated values (city, grade). Values are stored as small integer codes plus a lookup table, saving memory and speeding up groupby.</p>")
