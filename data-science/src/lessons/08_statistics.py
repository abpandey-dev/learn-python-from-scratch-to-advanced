from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MARKS = [52, 61, 64, 68, 70, 71, 73, 75, 78, 82, 85, 98]

LESSON("Basics", "Centre: mean, median, mode", """
<p>A <b>statistic</b> is a single number that summarises many values. The first question is always <i>"what is a typical value?"</i></p>
<table>
<tr><th>Measure</th><th>How</th><th>Use when</th></tr>
<tr><td><b>Mean</b></td><td>sum ÷ count</td><td>data is roughly symmetric</td></tr>
<tr><td><b>Median</b></td><td>middle value after sorting</td><td>there are outliers or skew (salaries, house prices)</td></tr>
<tr><td><b>Mode</b></td><td>most frequent value</td><td>categories ("most common city")</td></tr>
</table>
<pre><code class="py">a = np.array(marks)
a.mean(), np.median(a)
pd.Series(marks).mode()     # can return several values</code></pre>
<p>One huge value drags the mean but barely moves the median — compare them to spot skew.</p>
""", practice=["Mean, Median and Mode", "Weighted Average", "Average Yearly Growth (CAGR)"])


@LD
def centre_demo():
    a = np.array(MARKS)
    mean = a.mean()
    median = np.median(a)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.hist(a, bins=6, color="#99c9c2", edgecolor="white")
    ax.axvline(mean, color="#b45309", label=f"mean {mean:.1f}")
    ax.axvline(median, color="#0f766e", linestyle="--", label=f"median {median:.1f}")
    ax.legend()


LESSON("Basics", "Spread: range, IQR, variance, standard deviation", """
<p>Two classes can share a mean of 70 yet one has everyone between 65 and 75 and the other ranges from 30 to 100. <b>Spread</b> tells them apart.</p>
<ul>
<li><b>Range</b> = max − min (one outlier ruins it).</li>
<li><b>Quartiles</b>: Q1 (25th percentile), Q2 = median, Q3 (75th). <b>IQR</b> = Q3 − Q1 — the middle half of the data.</li>
<li><b>Variance</b> = average squared distance from the mean. <b>Standard deviation</b> = √variance, back in the original units.</li>
</ul>
<pre><code class="py">np.percentile(a, [25, 50, 75])
a.std()           # NumPy: population (divide by n)
a.std(ddof=1)     # sample (divide by n − 1) — what pandas .std() uses</code></pre>
<p>Use <b>n − 1</b> (sample) when your data is a sample of a bigger population — the usual case.</p>
""", practice=["Range and Interquartile Range", "Population vs Sample Standard Deviation", "Coefficient of Variation", "Percentile Rank"])


@LD
def spread_demo():
    a = np.array(MARKS, dtype=float)
    q1, q3 = np.percentile(a, [25, 75])
    iqr = q3 - q1
    std = a.std(ddof=1)
    fig, ax = plt.subplots(figsize=(5, 2.4))
    ax.boxplot(a, vert=False)
    ax.set_title(f"IQR = {iqr:.1f}, std = {std:.1f}")


LESSON("Core", "Standardising and outliers", """
<p>A <b>z-score</b> says how many standard deviations a value is from the mean: <code>z = (x − mean) / std</code>. It lets you compare a 72 in Maths with an 80 in English.</p>
<p>Two common outlier rules:</p>
<table>
<tr><th>Rule</th><th>Outlier if</th><th>Good for</th></tr>
<tr><td>z-score</td><td>|z| &gt; 2 or 3</td><td>roughly bell-shaped data</td></tr>
<tr><td>IQR (Tukey)</td><td>below Q1 − 1.5·IQR or above Q3 + 1.5·IQR</td><td>any shape — what box plots use</td></tr>
</table>
<p><b>Skewness</b> measures lopsidedness: positive means a long right tail (mean &gt; median).</p>
""", practice=["Outliers by Z-Score", "Outliers by the IQR Rule", "Skewness"])


@LD
def z_demo():
    a = np.array(MARKS, dtype=float)
    z = (a - a.mean()) / a.std()
    flagged = a[np.abs(z) > 1.5]
    q1, q3 = np.percentile(a, [25, 75])
    fence_hi = q3 + 1.5 * (q3 - q1)


LESSON("Core", "Relationships: correlation and covariance", """
<p>Do two numbers move together? <b>Covariance</b> is positive if they rise together, negative if one falls as the other rises — but its size depends on units. <b>Pearson's r</b> rescales it to −1 … +1.</p>
<table>
<tr><th>r</th><th>Meaning</th></tr>
<tr><td>+1</td><td>perfect straight line up</td></tr>
<tr><td>≈ 0</td><td>no straight-line relationship</td></tr>
<tr><td>−1</td><td>perfect straight line down</td></tr>
</table>
<pre><code class="py">np.corrcoef(x, y)[0, 1]
df.corr(numeric_only=True)              # whole matrix
s.rank().corr(t.rank())                 # Spearman: monotonic, robust to outliers</code></pre>
<p><b>Correlation is not causation</b>: ice-cream sales and drownings correlate because both rise in summer.</p>
""", practice=["Pearson Correlation", "Sample Covariance", "Spearman Rank Correlation"])


@LD
def corr_demo():
    hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    score = np.array([52, 55, 61, 60, 68, 72, 75, 83])
    r = np.corrcoef(hours, score)[0, 1]
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.scatter(hours, score)
    ax.set_xlabel("hours studied")
    ax.set_ylabel("score")
    ax.set_title(f"r = {r:.2f}")


LESSON("Advanced", "Fitting a line: simple linear regression", """
<p>Regression goes one step further than correlation: it finds the line <code>y = slope·x + intercept</code> that minimises the squared vertical errors (<b>least squares</b>).</p>
<pre><code class="py">slope, intercept = np.polyfit(x, y, 1)
pred = slope * x + intercept
r2 = 1 - ((y - pred)**2).sum() / ((y - y.mean())**2).sum()</code></pre>
<ul>
<li><b>slope</b>: how much y changes when x grows by 1.</li>
<li><b>R²</b>: share of y's variation the line explains (0 … 1). For one predictor, R² = r².</li>
<li>Only predict inside the x range you trained on — extrapolation is risky.</li>
</ul>
""", practice=["Fit a Straight Line", "Predict With the Line", "R² of a Fit"])


@LD
def regression_demo():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([52, 55, 61, 60, 68, 72, 75, 83])
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.scatter(x, y)
    ax.plot(x, pred, color="#b45309")
    ax.set_title(f"y = {slope:.2f}x + {intercept:.1f},  R² = {r2:.2f}")


LESSON("Advanced", "Probability and confidence intervals", """
<p><b>Empirical probability</b> = favourable cases ÷ all cases in your data: <code>(a &gt;= 70).mean()</code>.</p>
<p>The <b>binomial</b> formula gives the chance of exactly k successes in n independent tries with chance p:
<code>C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ</code> (<code>math.comb(n, k)</code>).</p>
<p>A sample mean is only an estimate. Its <b>standard error</b> is <code>s / √n</code>, and a rough <b>95% confidence interval</b> is <code>mean ± 1.96 × SE</code>: if you repeated the sampling many times, about 95% of such intervals would contain the true mean. More data → smaller SE → narrower interval.</p>
""", practice=["Probability From Data", "Binomial Probability", "95% Confidence Interval for the Mean", "Relative Frequency Table"])


@LD
def binomial_demo():
    import math
    n, p = 10, 0.3
    ks = list(range(n + 1))
    probs = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in ks]
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.bar(ks, probs)
    ax.set_xlabel("successes in 10 tries (p = 0.3)")
    ax.set_ylabel("probability")
