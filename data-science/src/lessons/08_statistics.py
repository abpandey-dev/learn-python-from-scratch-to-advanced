from lib import *
import math
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


LESSON("Basics", "Variance and standard deviation by hand", """
<p>Values: 2, 4, 4, 4, 5, 5, 7, 9. The mean is 40 / 8 = 5.</p>
<table><tr><th>x</th><th>x − mean</th><th>(x − mean)²</th></tr>
<tr><td>2</td><td>−3</td><td>9</td></tr><tr><td>4</td><td>−1</td><td>1</td></tr><tr><td>4</td><td>−1</td><td>1</td></tr><tr><td>4</td><td>−1</td><td>1</td></tr>
<tr><td>5</td><td>0</td><td>0</td></tr><tr><td>5</td><td>0</td><td>0</td></tr><tr><td>7</td><td>2</td><td>4</td></tr><tr><td>9</td><td>4</td><td>16</td></tr>
<tr><th colspan="2">Total</th><th>32</th></tr></table>
<table><tr><th></th><th>Variance</th><th>Standard deviation</th></tr>
<tr><td>Population (÷ n)</td><td>32 / 8 = 4</td><td>2</td></tr>
<tr><td>Sample (÷ (n − 1))</td><td>32 / 7 = 4.571</td><td>2.138</td></tr></table>
<h4>Why square the differences?</h4>
<p>Plain differences always add up to 0, because positives cancel negatives. Squaring makes them all count. Taking the root at the end returns to the original units.</p>
<h4>Why n − 1?</h4>
<p>We measured distances from the sample's own mean, which sits closer to the data than the true mean does. So the sum is a little too small, and dividing by n − 1 corrects it.</p>
<p><b>Beware the defaults:</b> <code>np.std</code> divides by n, and pandas <code>.std()</code> divides by n − 1.</p>
""", practice=["Population vs Sample Standard Deviation", "Coefficient of Variation"])


@LD
def variance_by_hand():
    x = np.array([2, 4, 4, 4, 5, 5, 7, 9], dtype=float)
    differences = x - x.mean()
    add_to_zero = differences.sum()
    squares = differences ** 2
    population_variance = squares.sum() / len(x)
    sample_variance = squares.sum() / (len(x) - 1)
    numpy_default = x.std()
    pandas_default = pd.Series(x).std()


LESSON("Core", "Correlation by hand, and its traps", """
<p>x = 1, 2, 3, 4, 5 and y = 2, 4, 5, 4, 5. The means are 3 and 4.</p>
<table><tr><th>dx</th><th>dy</th><th>dx·dy</th><th>dx²</th><th>dy²</th></tr>
<tr><td>−2</td><td>−2</td><td>4</td><td>4</td><td>4</td></tr><tr><td>−1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td></tr><tr><td>2</td><td>1</td><td>2</td><td>4</td><td>1</td></tr>
<tr><th>Total</th><th></th><th>6</th><th>10</th><th>6</th></tr></table>
<p>r = 6 / √(10 × 6) = <b>0.775</b>. When x is above average, y usually is too, so the products are mostly positive.</p>
<h4>Three traps</h4>
<ol><li><b>Curves:</b> y = x² on x = −2 … 2 gives <b>r = 0</b>, although y depends entirely on x.</li>
<li><b>Outliers:</b> five points with r = −0.693 become r = <b>+0.963</b> when one extreme point is added. Try Spearman, and always plot.</li>
<li><b>Hidden causes:</b> ice-cream sales and drownings rise together because of summer.</li></ol>
""", practice=["Pearson Correlation", "Sample Covariance", "Spearman Rank Correlation"])


@LD
def correlation_traps():
    x = np.arange(-2, 3)
    curve_r = np.corrcoef(x, x ** 2)[0, 1]
    a = np.array([1, 2, 3, 4, 5, 20], dtype=float)
    b = np.array([5, 3, 4, 2, 3, 30], dtype=float)
    without_outlier = np.corrcoef(a[:-1], b[:-1])[0, 1]
    with_outlier = np.corrcoef(a, b)[0, 1]
    spearman = pd.Series(a).rank().corr(pd.Series(b).rank())
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.scatter(a, b)
    ax.set_title(f"r = {without_outlier:.2f} without the far point, {with_outlier:.2f} with it", fontsize=8)


LESSON("Core", "Samples, standard error and confidence intervals", """
<p>A sample's mean changes from sample to sample. The <b>standard error</b> (SE) measures by how much: SE = s / √n.</p>
<h4>Worked example</h4>
<p>25 students score a mean of 70, with s = 10.</p>
<ol><li>SE = 10 / √25 = 2.</li>
<li>95% interval = 70 ± 1.96 × 2 = <b>66.08 to 73.92</b>.</li></ol>
<p>To <b>halve</b> the SE you need <b>four times</b> the data, as √n is on the bottom.</p>
<h4>Saying it correctly</h4>
<ul><li><b>Right:</b> if we repeated this many times, about 95% of such intervals would contain the true mean.</li>
<li><b>Wrong:</b> "95% of students score in this range." That describes the mean, not individuals. For individuals, you'd use s, not SE.</li></ul>
<p>The demo draws 1,000 samples from a very skewed population. Their means still form a bell shape that narrows as n grows: the central limit theorem at work.</p>
<p><b>With small samples</b> (say under 30), replace 1.96 with a slightly larger value from the t-distribution.</p>
""", practice=["95% Confidence Interval for the Mean", "Probability From Data"])


@LD
def sampling_means():
    r = np.random.default_rng(0)
    population = r.exponential(10, 100000)
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.5))
    axes[0].hist(population, bins=60, color="#9ca3af")
    axes[0].set_title("skewed population", fontsize=8)
    for ax, n in zip(axes[1:], [5, 50]):
        means = r.choice(population, (1000, n)).mean(axis=1)
        ax.hist(means, bins=40, color="#0f766e")
        ax.set_xlim(0, 30)
        ax.set_title(f"means of samples of {n}: SE {means.std():.2f}", fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "A hypothesis test by hand: an A/B test", """
<p>Page A: 200 of 2,000 visitors buy (10%). Page B: 250 of 2,000 buy (12.5%). Could that gap just be chance?</p>
<h4>The steps</h4>
<ol><li><b>Null hypothesis:</b> both pages have the same true rate.</li>
<li><b>Pooled rate:</b> 450 / 4000 = 0.1125.</li>
<li><b>Standard error of the gap:</b> √(0.1125 × 0.8875 × (1/2000 + 1/2000)) = 0.00999.</li>
<li><b>z-score:</b> (0.125 − 0.10) / 0.00999 = <b>2.50</b>.</li>
<li><b>p-value:</b> the chance of a gap this large, in either direction, if the null were true = <b>0.012</b>.</li></ol>
<p>That's below the usual 0.05, so we reject the null: the gap is unlikely to be chance alone.</p>
<h4>What it doesn't say</h4>
<ul><li>p isn't the chance that the null is true.</li>
<li><b>Significant isn't the same as important:</b> with huge data, a tiny useless gap can be significant. Report the size of the effect with an interval.</li>
<li><b>Don't peek and stop early</b> when the result looks good, and be careful testing many metrics: at 0.05, 1 in 20 tests of nothing looks "significant".</li></ul>
<table><tr><th>Error</th><th>Meaning</th></tr><tr><td>Type I (false positive)</td><td>you claim an effect that isn't there</td></tr><tr><td>Type II (false negative)</td><td>you miss a real effect; more data reduces this</td></tr></table>
""", practice=["Binomial Probability", "Relative Frequency Table"])


@LD
def ab_test():
    a_buy, b_buy, n = 200, 250, 2000
    p_a, p_b = a_buy / n, b_buy / n
    pooled = (a_buy + b_buy) / (2 * n)
    se = (pooled * (1 - pooled) * (2 / n)) ** 0.5
    z = (p_b - p_a) / se
    p_value = 2 * (1 - 0.5 * (1 + math.erf(z / 2 ** 0.5)))
    r = np.random.default_rng(0)
    null_gaps = (r.binomial(n, pooled, 20000) - r.binomial(n, pooled, 20000)) / n
    simulated_p = (np.abs(null_gaps) >= p_b - p_a).mean()
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.hist(null_gaps, bins=50, color="#9ca3af")
    ax.axvline(p_b - p_a, color="#b91c1c")
    ax.set_xlabel("gap in buying rate, if the pages were truly equal")
    ax.set_title(f"observed gap in red; simulated p = {simulated_p:.3f}", fontsize=9)
