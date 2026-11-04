from lib import *
import math
import numpy as np
import pandas as pd

TOPIC(
    id="statistics", title="Statistics for Data Analysis", glyph="μ σ",
    blurb="Describe and compare data: centre, spread, percentiles, outliers, correlation, simple regression and basic probability.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">s.mean(), s.median(), s.mode(), s.std(), s.var()      # pandas: sample std (ddof=1)
np.mean(a), np.median(a), np.std(a), np.std(a, ddof=1)  # NumPy: population std by default
np.percentile(a, [25, 50, 75]); q3 - q1                # quartiles, IQR
(a - a.mean()) / a.std()                               # z-scores
np.corrcoef(x, y)[0, 1]; s.rank().corr(t.rank())      # Pearson / Spearman
slope, intercept = np.polyfit(x, y, 1)                 # straight-line fit
s.value_counts(normalize=True)                         # relative frequencies
math.comb(n, k) * p**k * (1 - p)**(n - k)              # binomial probability</code></pre>
""")

DATA = [2, 4, 4, 4, 5, 5, 7, 9]


Q(None, "Mean, Median and Mode", "Easy", "Measures of centre",
  "Return <code>(mean, median, mode)</code>. If several values tie for mode, return the smallest.",
  [((DATA,), (5.0, 4.5, 4)), (([1, 3, 3, 6, 7, 8, 9],), (5.2857, 6.0, 3))],
  ("Sum and divide; sort and take the middle; count each value.", "O(n log n)", "O(n)"),
  ("<code>np.mean</code>, <code>np.median</code> and pandas <code>Series.mode()</code>.", "O(n log n)", "O(n)"),
  viz=(DATA,))


@B
def centre(values):
    n = len(values)
    mean = sum(values) / n
    s = sorted(values)
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    best = max(counts.values())
    mode = min(v for v, c in counts.items() if c == best)
    return (mean, float(median), mode)


@O
def centre(values):
    a = np.array(values)
    mode = pd.Series(values).mode().min()
    return (a.mean(), np.median(a), mode)


Q(None, "Range and Interquartile Range", "Easy", "Spread · percentiles",
  "Return <code>(range, IQR)</code> where IQR = Q3 − Q1 using linear interpolation between data points.",
  [((DATA,), (7, 1.5)), (([1, 2, 3, 4],), (3, 1.5))],
  ("Sort, then compute each quartile's position (n − 1) × p and interpolate by hand.", "O(n log n)", "O(n)"),
  ("<code>np.ptp</code> for the range and <code>np.percentile(a, [25, 75])</code>.", "O(n log n)", "O(n)"),
  viz=(DATA,))


@B
def spread(values):
    s = sorted(values)

    def quantile(p):
        pos = (len(s) - 1) * p
        lo = int(pos)
        frac = pos - lo
        return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * frac

    return (s[-1] - s[0], quantile(0.75) - quantile(0.25))


@O
def spread(values):
    a = np.array(values)
    q1, q3 = np.percentile(a, [25, 75])
    return (np.ptp(a), q3 - q1)


Q(None, "Population vs Sample Standard Deviation", "Medium", "ddof",
  "Return <code>(population std, sample std)</code>, both rounded to 4 decimals.",
  [((DATA,), (2.0, 2.1381)), (([1, 2, 3, 4],), (1.118, 1.291))],
  ("Sum of squared deviations divided by n, and by n − 1, then square roots.", "O(n)", "O(1)"),
  ("<code>np.std(a)</code> (ddof=0) and <code>np.std(a, ddof=1)</code> — pandas' <code>.std()</code> uses ddof=1.", "O(n)", "O(n)"),
  viz=(DATA,))


@B
def stds(values):
    n = len(values)
    mean = sum(values) / n
    ss = sum((x - mean) ** 2 for x in values)
    return (round((ss / n) ** 0.5, 4), round((ss / (n - 1)) ** 0.5, 4))


@O
def stds(values):
    a = np.array(values, dtype=float)
    return (round(a.std(), 4), round(a.std(ddof=1), 4))


Q(None, "Percentile Rank", "Easy", "Share of values ≤ x",
  "Return the percentage of values that are ≤ x, rounded to 1 decimal.",
  [((DATA, 4), 50.0), ((DATA, 8), 87.5)],
  ("Count in a loop and divide.", "O(n)", "O(1)"),
  ("The mean of a boolean array is the share of Trues: <code>(a &lt;= x).mean() * 100</code>.", "O(n)", "O(n)"),
  viz=(DATA, 5))


@B
def percentile_rank(values, x):
    count = 0
    for v in values:
        if v <= x:
            count += 1
    return round(count / len(values) * 100, 1)


@O
def percentile_rank(values, x):
    a = np.array(values)
    return round((a <= x).mean() * 100, 1)


Q(None, "Outliers by Z-Score", "Medium", "Standardisation",
  "Return the values whose z-score (population std) has absolute value greater than <code>limit</code>.",
  [(([10, 11, 9, 10, 12, 30, 10], 2), [30]), ((DATA, 1.5), [9])],
  ("Compute mean and std by hand, then test each value.", "O(n)", "O(n)"),
  ("Vectorised z-scores and a boolean mask.", "O(n)", "O(n)"),
  viz=([10, 11, 9, 10, 12, 30, 10], 2))


@B
def z_outliers(values, limit):
    n = len(values)
    mean = sum(values) / n
    std = (sum((x - mean) ** 2 for x in values) / n) ** 0.5
    return [x for x in values if abs((x - mean) / std) > limit]


@O
def z_outliers(values, limit):
    a = np.array(values, dtype=float)
    z = (a - a.mean()) / a.std()
    return a[np.abs(z) > limit].astype(int)


Q(None, "Outliers by the IQR Rule", "Medium", "Tukey's fences",
  "Return values below Q1 − 1.5·IQR or above Q3 + 1.5·IQR.",
  [(([10, 11, 9, 10, 12, 30, 10],), [30]), ((DATA,), [9])],
  ("Interpolate quartiles by hand, then filter.", "O(n log n)", "O(n)"),
  ("<code>np.percentile</code> for Q1/Q3, then a mask with <code>|</code>.", "O(n log n)", "O(n)"),
  viz=([10, 11, 9, 10, 12, 30, 10],))


@B
def iqr_outliers(values):
    s = sorted(values)

    def q(p):
        pos = (len(s) - 1) * p
        lo = int(pos)
        return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * (pos - lo)

    q1, q3 = q(0.25), q(0.75)
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    return [x for x in values if x < lo or x > hi]


@O
def iqr_outliers(values):
    a = np.array(values)
    q1, q3 = np.percentile(a, [25, 75])
    iqr = q3 - q1
    return a[(a < q1 - 1.5 * iqr) | (a > q3 + 1.5 * iqr)]


Q(None, "Pearson Correlation", "Medium", "np.corrcoef",
  "Return the Pearson correlation coefficient r between x and y, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]), 0.7746), (([1, 2, 3], [3, 2, 1]), -1.0)],
  ("r = Σ(dx·dy) / √(Σdx² · Σdy²) in a loop.", "O(n)", "O(1)"),
  ("<code>np.corrcoef(x, y)[0, 1]</code>.", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]))


@B
def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sxx = syy = 0.0
    for a, b in zip(x, y):
        sxy += (a - mx) * (b - my)
        sxx += (a - mx) ** 2
        syy += (b - my) ** 2
    return round(sxy / (sxx * syy) ** 0.5, 4)


@O
def pearson(x, y):
    return round(np.corrcoef(x, y)[0, 1], 4)


Q(None, "Sample Covariance", "Easy", "np.cov",
  "Return the sample covariance of x and y (divide by n − 1), rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]), 1.5), (([1, 2], [2, 1]), -0.5)],
  ("Σ(dx·dy) / (n − 1).", "O(n)", "O(1)"),
  ("<code>np.cov(x, y)[0, 1]</code> (sample by default).", "O(n)", "O(n)"))


@B
def covariance(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    return round(sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1), 4)


@O
def covariance(x, y):
    return round(np.cov(x, y)[0, 1], 4)


Q(None, "Weighted Average", "Easy", "np.average(weights=)",
  "Return the weighted average of marks with the given credit weights, rounded to 2 decimals.",
  [(([80, 90, 70], [3, 1, 2]), 78.33), (([50, 100], [1, 1]), 75.0)],
  ("Σ(mark × weight) / Σ weight in a loop.", "O(n)", "O(1)"),
  ("<code>np.average(marks, weights=weights)</code>.", "O(n)", "O(n)"))


@B
def weighted(marks, weights):
    total = 0
    for m, w in zip(marks, weights):
        total += m * w
    return round(total / sum(weights), 2)


@O
def weighted(marks, weights):
    return round(np.average(marks, weights=weights), 2)


Q(None, "Average Yearly Growth (CAGR)", "Easy", "Geometric mean",
  "Given yearly values, return the compound annual growth rate in percent (2 decimals).",
  [(([100, 110, 121],), 10.0), (([200, 150, 300, 450],), 31.04)],
  ("Multiply the yearly growth factors, then take the n-th root.", "O(n)", "O(1)"),
  ("Only the first and last values matter: (last / first) ** (1 / years) − 1.", "O(1)", "O(1)"))


@B
def cagr(values):
    product = 1.0
    for a, b in zip(values, values[1:]):
        product *= b / a
    years = len(values) - 1
    return round((product ** (1 / years) - 1) * 100, 2)


@O
def cagr(values):
    v = np.array(values, dtype=float)
    return round(((v[-1] / v[0]) ** (1 / (len(v) - 1)) - 1) * 100, 2)


Q(None, "Coefficient of Variation", "Easy", "Relative spread",
  "Return std / mean × 100 (population std), rounded to 2 decimals — a unit-free measure of spread.",
  [((DATA,), 40.0), (([10, 10, 10],), 0.0)],
  ("Compute mean and std by hand.", "O(n)", "O(1)"),
  ("<code>a.std() / a.mean() * 100</code>.", "O(n)", "O(n)"))


@B
def cv(values):
    n = len(values)
    mean = sum(values) / n
    std = (sum((x - mean) ** 2 for x in values) / n) ** 0.5
    return round(std / mean * 100, 2)


@O
def cv(values):
    a = np.array(values, dtype=float)
    return round(a.std() / a.mean() * 100, 2)


Q(None, "Fit a Straight Line", "Medium", "Least squares · polyfit",
  "Return <code>(slope, intercept)</code> of the least-squares line y = slope·x + intercept, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]), (0.6, 2.2)), (([0, 1, 2], [1, 3, 5]), (2.0, 1.0))],
  ("slope = Σ(dx·dy) / Σdx², intercept = ȳ − slope·x̄.", "O(n)", "O(1)"),
  ("<code>np.polyfit(x, y, 1)</code> returns [slope, intercept].", "O(n)", "O(n)"),
  viz=([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]))


@B
def line_fit(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = sum((a - mx) ** 2 for a in x)
    slope = num / den
    return (round(slope, 4), round(my - slope * mx, 4))


@O
def line_fit(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    return (round(slope, 4), round(intercept, 4))


Q(None, "Predict With the Line", "Easy", "Applying a model",
  "Fit a line to (x, y) and return predictions for <code>new_x</code>, rounded to 2 decimals.",
  [(([1, 2, 3, 4, 5], [2, 4, 5, 4, 5], [6, 10]), [5.8, 8.2])],
  ("Fit by hand, then predict in a loop.", "O(n + m)", "O(m)"),
  ("<code>np.polyval(np.polyfit(x, y, 1), new_x)</code>.", "O(n + m)", "O(m)"))


@B
def predict(x, y, new_x):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    intercept = my - slope * mx
    return [round(slope * v + intercept, 2) for v in new_x]


@O
def predict(x, y, new_x):
    coeffs = np.polyfit(x, y, 1)
    return np.polyval(coeffs, new_x).round(2)


Q(None, "R² of a Fit", "Medium", "Goodness of fit",
  "Return R² = 1 − SS_res / SS_tot for predictions vs actual values, rounded to 4 decimals.",
  [(([2, 4, 5, 4, 5], [2.8, 3.4, 4.0, 4.6, 5.2]), 0.6), (([1, 2, 3], [1, 2, 3]), 1.0)],
  ("Two sums of squares in a loop.", "O(n)", "O(1)"),
  ("Vectorised sums of squares.", "O(n)", "O(n)"))


@B
def r_squared(actual, predicted):
    mean = sum(actual) / len(actual)
    ss_res = sum((a - p) ** 2 for a, p in zip(actual, predicted))
    ss_tot = sum((a - mean) ** 2 for a in actual)
    return round(1 - ss_res / ss_tot, 4)


@O
def r_squared(actual, predicted):
    a, p = np.array(actual, dtype=float), np.array(predicted, dtype=float)
    return round(1 - ((a - p) ** 2).sum() / ((a - a.mean()) ** 2).sum(), 4)


Q(None, "Relative Frequency Table", "Easy", "value_counts(normalize=True)",
  "Return {category: share of rows} rounded to 3 decimals, most common first.",
  [((["a", "b", "a", "c", "a", "b"],), {"a": 0.5, "b": 0.333, "c": 0.167})],
  ("Count in a dict, divide by n, sort.", "O(n log k)", "O(k)"),
  ("<code>s.value_counts(normalize=True)</code>.", "O(n)", "O(k)"))


@B
def rel_freq(items):
    counts = {}
    for it in items:
        counts[it] = counts.get(it, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    return {k: round(c / len(items), 3) for k, c in ordered}


@O
def rel_freq(items):
    return pd.Series(items).value_counts(normalize=True).round(3)


Q(None, "Skewness", "Medium", "Third standardised moment",
  "Return the population skewness mean(((x − μ) / σ)³), rounded to 4 decimals. Positive = long right tail.",
  [((DATA,), 0.6562), (([1, 2, 3],), 0.0)],
  ("Loop: standardise, cube, average.", "O(n)", "O(1)"),
  ("Vectorised: <code>(((a − a.mean()) / a.std()) ** 3).mean()</code>.", "O(n)", "O(n)"),
  viz=(DATA,))


@B
def skewness(values):
    n = len(values)
    mean = sum(values) / n
    std = (sum((x - mean) ** 2 for x in values) / n) ** 0.5
    return round(sum(((x - mean) / std) ** 3 for x in values) / n, 4)


@O
def skewness(values):
    a = np.array(values, dtype=float)
    return round((((a - a.mean()) / a.std()) ** 3).mean(), 4)


Q(None, "95% Confidence Interval for the Mean", "Medium", "Standard error",
  "Return (low, high) = mean ± 1.96 × s / √n using the sample std, rounded to 2 decimals.",
  [((DATA,), (3.52, 6.48)), (([10, 12, 14],), (9.74, 14.26))],
  ("Compute mean, sample std and standard error by hand.", "O(n)", "O(1)"),
  ("pandas <code>s.mean()</code> and <code>s.sem()</code> (standard error, ddof=1).", "O(n)", "O(n)"),
  viz=(DATA,))


@B
def ci95(values):
    n = len(values)
    mean = sum(values) / n
    s = (sum((x - mean) ** 2 for x in values) / (n - 1)) ** 0.5
    margin = 1.96 * s / n ** 0.5
    return (round(mean - margin, 2), round(mean + margin, 2))


@O
def ci95(values):
    s = pd.Series(values, dtype=float)
    margin = 1.96 * s.sem()
    return (round(s.mean() - margin, 2), round(s.mean() + margin, 2))


Q(None, "Probability From Data", "Easy", "Empirical probability",
  "Return the observed probability that a value is at least <code>t</code>, rounded to 3 decimals.",
  [((DATA, 5), 0.5), ((DATA, 10), 0.0)],
  ("Count favourable cases / all cases.", "O(n)", "O(1)"),
  ("<code>(a &gt;= t).mean()</code>.", "O(n)", "O(n)"))


@B
def prob_at_least(values, t):
    return round(sum(1 for v in values if v >= t) / len(values), 3)


@O
def prob_at_least(values, t):
    return round((np.array(values) >= t).mean(), 3)


Q(None, "Binomial Probability", "Medium", "math.comb",
  "Return the probability of exactly k successes in n independent tries with success chance p, rounded to 4 decimals.",
  [((4, 2, 0.5), 0.375), ((10, 3, 0.2), 0.2013), ((5, 0, 0.1), 0.5905)],
  ("List all 2ⁿ outcome sequences and add the probabilities of those with exactly k successes.", "O(2ⁿ · n)", "O(n)"),
  ("Formula: C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ.", "O(k)", "O(1)"),
  viz=(4, 2, 0.5))


@B
def binomial(n, k, p):
    from itertools import product
    total = 0.0
    for outcome in product([0, 1], repeat=n):
        if sum(outcome) == k:
            total += p ** k * (1 - p) ** (n - k)
    return round(total, 4)


@O
def binomial(n, k, p):
    import math
    return round(math.comb(n, k) * p ** k * (1 - p) ** (n - k), 4)


Q(None, "Spearman Rank Correlation", "Hard", "Correlation of ranks",
  "Return Spearman's ρ: the Pearson correlation of the ranks (ties get the average rank), rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5], [5, 6, 7, 8, 7]), 0.8208), (([10, 20, 30], [1, 100, 1000]), 1.0)],
  ("Rank each list by hand (averaging ties), then compute Pearson's r on the ranks.", "O(n log n)", "O(n)"),
  ("pandas <code>.rank()</code> averages ties for you; then Pearson's <code>.corr()</code> on the ranks. (<code>method='spearman'</code> does the same but needs SciPy.)", "O(n log n)", "O(n)"),
  viz=([1, 2, 3, 4, 5], [5, 6, 7, 8, 7]))


@B
def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r

    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return round(num / den, 4)


@O
def spearman(x, y):
    rx = pd.Series(x).rank()
    ry = pd.Series(y).rank()
    return round(rx.corr(ry), 4)
