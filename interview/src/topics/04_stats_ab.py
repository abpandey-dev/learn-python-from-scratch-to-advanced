from lib import *
import math
import numpy as np
import pandas as pd


TOPIC(
    id="stats-ab", title="Statistics & A/B Testing", glyph="p < 0.05?",
    blurb="What data-science interviews ask: confidence intervals, z and t tests, sample size, multiple testing, Bayes base rates, Simpson's paradox, and the pandas behind retention, funnels and top-N reports.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">se = sqrt(p * (1 - p) / n)                                    # standard error
z = (p2 - p1) / sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))   # two-proportion test
n = 2 * (1.96 + 0.84)**2 * p * (1 - p) / delta**2             # per group, 95%/80%
P(A|B) = P(B|A) * P(A) / P(B)                                  # Bayes</code></pre>
""")

EVENTS = pd.DataFrame({
    "user": [1, 1, 1, 2, 2, 3, 3, 4],
    "step": ["visit", "cart", "buy", "visit", "cart", "visit", "cart", "visit"],
    "week": [0, 0, 1, 0, 2, 1, 1, 1],
    "cohort": [0, 0, 0, 0, 0, 1, 1, 1],
})
SALES = pd.DataFrame({
    "region": ["N", "N", "N", "S", "S", "E"],
    "product": ["a", "b", "c", "a", "b", "c"],
    "revenue": [50, 30, 20, 40, 60, 10],
})


Q(None, "Standard Error of a Proportion", "Easy", "How noisy is a rate?",
  "Given conversions and visitors, return (rate, standard error), rounded to 4 decimals.",
  [((50, 1000), (0.05, 0.0069)), ((500, 10000), (0.05, 0.0022))],
  ("Write the formula step by step.", "O(1)", "O(1)"),
  ("NumPy, one line.", "O(1)", "O(1)"),
  names=["conversions", "n"])


@B
def rate_se(conversions, n):
    p = conversions / n
    variance = p * (1 - p) / n
    return (round(p, 4), round(math.sqrt(variance), 4))


@O
def rate_se(conversions, n):
    p = conversions / n
    return (round(p, 4), round(float(np.sqrt(p * (1 - p) / n)), 4))


Q(None, "95% Confidence Interval", "Easy", "A range, not a point",
  "Return the 95% interval for a proportion, using 1.96, rounded to 4 decimals.",
  [((50, 1000), (0.0365, 0.0635))],
  ("Rate, standard error, then plus or minus.", "O(1)", "O(1)"),
  ("A NumPy array of ±1.96.", "O(1)", "O(1)"),
  names=["conversions", "n"])


@B
def proportion_ci(conversions, n):
    p = conversions / n
    se = math.sqrt(p * (1 - p) / n)
    return (round(p - 1.96 * se, 4), round(p + 1.96 * se, 4))


@O
def proportion_ci(conversions, n):
    p = conversions / n
    low, high = p + np.array([-1.96, 1.96]) * np.sqrt(p * (1 - p) / n)
    return (round(float(low), 4), round(float(high), 4))


Q(None, "CI of a Mean", "Easy", "Using the sample",
  "Return (mean, lower, upper) of a 95% interval using the sample standard deviation and 1.96, rounded to 4 decimals. (With few points you'd use t rather than 1.96.)",
  [(([10, 12, 14, 16, 18],), (14.0, 11.2281, 16.7719))],
  ("Compute mean and variance with loops.", "O(n)", "O(1)"),
  ("<code>np.std(x, ddof=1)</code>.", "O(n)", "O(n)"))


@B
def mean_ci(x):
    n = len(x)
    mean = sum(x) / n
    s = math.sqrt(sum((v - mean) ** 2 for v in x) / (n - 1))
    half = 1.96 * s / math.sqrt(n)
    return (round(mean, 4), round(mean - half, 4), round(mean + half, 4))


@O
def mean_ci(x):
    x = np.array(x, dtype=float)
    half = 1.96 * x.std(ddof=1) / np.sqrt(len(x))
    return (round(float(x.mean()), 4), round(float(x.mean() - half), 4), round(float(x.mean() + half), 4))


Q(None, "Two-Proportion z-Test", "Medium", "The A/B test",
  "Return (z, two-sided p-value), rounded to 4 decimals, using the pooled rate.",
  [((200, 2000, 250, 2000), (2.502, 0.0124)), ((10, 100, 11, 100), (0.2307, 0.8176))],
  ("Pool, standard error, z, and the normal CDF, step by step.", "O(1)", "O(1)"),
  ("Compact with <code>math.erf</code>.", "O(1)", "O(1)"),
  names=["x1", "n1", "x2", "n2"])


@B
def ab_test(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    pool = (x1 + x2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se
    cdf = 0.5 * (1 + math.erf(abs(z) / math.sqrt(2)))
    return (round(z, 4), round(2 * (1 - cdf), 4))


@O
def ab_test(x1, n1, x2, n2):
    pool = (x1 + x2) / (n1 + n2)
    z = (x2 / n2 - x1 / n1) / math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    return (round(z, 4), round(math.erfc(abs(z) / math.sqrt(2)), 4))


Q(None, "Sample Size for an A/B Test", "Medium", "Before you run it",
  "Return visitors per group, rounded up: 2·(1.96 + 0.84)²·p(1−p)/δ², for base rate p and smallest difference δ worth detecting.",
  [((0.1, 0.01), 14112), ((0.1, 0.02), 3528)],
  ("Step by step.", "O(1)", "O(1)"),
  ("One line.", "O(1)", "O(1)"),
  names=["p", "delta"])


@B
def sample_size(p, delta):
    z_total = 1.96 + 0.84
    numerator = 2 * z_total * z_total * p * (1 - p)
    return math.ceil(numerator / (delta * delta))


@O
def sample_size(p, delta):
    return math.ceil(2 * 2.8 ** 2 * p * (1 - p) / delta ** 2)


Q(None, "Welch's t Statistic", "Medium", "Comparing two means",
  "Return (a̅ − b̅) / √(s²a/na + s²b/nb), with sample variances, rounded to 4 decimals.",
  [(([12, 14, 16, 18], [10, 11, 12, 13]), 2.4249)],
  ("Means and variances by hand.", "O(n)", "O(1)"),
  ("NumPy with <code>ddof=1</code>.", "O(n)", "O(n)"),
  names=["a", "b"])


@B
def welch_t(a, b):
    def stats(x):
        m = sum(x) / len(x)
        return m, sum((v - m) ** 2 for v in x) / (len(x) - 1)
    ma, va = stats(a)
    mb, vb = stats(b)
    return round((ma - mb) / math.sqrt(va / len(a) + vb / len(b)), 4)


@O
def welch_t(a, b):
    a, b = np.array(a, float), np.array(b, float)
    return round(float((a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))), 4)


Q(None, "Chi-Square for a 2×2 Table", "Medium", "Independent?",
  "Return Σ(observed − expected)²/expected, rounded to 4 decimals.",
  [(([[20, 30], [30, 20]],), 4.0)],
  ("Row and column totals, with loops.", "O(1)", "O(1)"),
  ("<code>np.outer(rows, cols) / total</code>.", "O(1)", "O(1)"))


@B
def chi_square(table):
    rows = [sum(r) for r in table]
    cols = [sum(r[j] for r in table) for j in range(len(table[0]))]
    total = sum(rows)
    stat = 0.0
    for i, r in enumerate(table):
        for j, obs in enumerate(r):
            exp = rows[i] * cols[j] / total
            stat += (obs - exp) ** 2 / exp
    return round(stat, 4)


@O
def chi_square(table):
    t = np.array(table, float)
    exp = np.outer(t.sum(axis=1), t.sum(axis=0)) / t.sum()
    return round(float(((t - exp) ** 2 / exp).sum()), 4)


Q(None, "Bonferroni and False Positives", "Easy", "Testing many things",
  "For m independent tests at level a, return (chance of at least one false positive, Bonferroni level a/m), rounded to 4 decimals.",
  [((20, 0.05), (0.6415, 0.0025)), ((1, 0.05), (0.05, 0.05))],
  ("Multiply the 'no false positive' chance in a loop.", "O(m)", "O(1)"),
  ("A power.", "O(1)", "O(1)"),
  names=["m", "a"])


@B
def false_positives(m, a):
    none = 1.0
    for _ in range(m):
        none *= 1 - a
    return (round(1 - none, 4), round(a / m, 4))


@O
def false_positives(m, a):
    return (round(1 - (1 - a) ** m, 4), round(a / m, 4))


Q(None, "Bayes: The Rare-Disease Test", "Easy", "Base rates",
  "Given prevalence, sensitivity and false-positive rate, return P(disease | positive), rounded to 4 decimals.",
  [((0.01, 0.9, 0.05), 0.1538), ((0.5, 0.9, 0.05), 0.9474)],
  ("Count imaginary people out of 100,000.", "O(1)", "O(1)"),
  ("Bayes' rule directly.", "O(1)", "O(1)"),
  names=["prev", "sens", "fpr"])


@B
def disease_given_positive(prev, sens, fpr):
    people = 100000
    sick = people * prev
    true_pos = sick * sens
    false_pos = (people - sick) * fpr
    return round(true_pos / (true_pos + false_pos), 4)


@O
def disease_given_positive(prev, sens, fpr):
    return round(prev * sens / (prev * sens + (1 - prev) * fpr), 4)


Q(None, "Simpson's Paradox", "Medium", "Aggregates can flip",
  "Each group is (A wins, A trials, B wins, B trials). Return (groups where A's rate beats B's, overall A rate, overall B rate), rounded to 4 decimals.",
  [(([(81, 87, 234, 270), (192, 263, 55, 80)],), (2, 0.78, 0.8257))],
  ("Loop with running totals.", "O(g)", "O(1)"),
  ("Array columns.", "O(g)", "O(g)"))


@B
def simpson(groups):
    wins = 0
    aw = at = bw = bt = 0
    for a, n, b, m in groups:
        if a / n > b / m:
            wins += 1
        aw += a
        at += n
        bw += b
        bt += m
    return (wins, round(aw / at, 4), round(bw / bt, 4))


@O
def simpson(groups):
    g = np.array(groups, float)
    return (int((g[:, 0] / g[:, 1] > g[:, 2] / g[:, 3]).sum()),
            round(float(g[:, 0].sum() / g[:, 1].sum()), 4), round(float(g[:, 2].sum() / g[:, 3].sum()), 4))


Q(None, "Bootstrap a Median", "Medium", "When there's no neat formula",
  "Given explicit resamples of row indices, return the median of the data in each, sorted. (Real code would draw thousands at random.)",
  [(([1, 2, 3, 100], [[0, 1, 2, 3], [3, 3, 2, 1], [0, 0, 1, 1]]), [1.5, 2.5, 51.5])],
  ("Sort each resample and pick the middle.", "O(r·n log n)", "O(n)"),
  ("<code>np.median(x[idx], axis=1)</code>.", "O(r·n)", "O(r·n)"),
  names=["x", "resamples"])


@B
def bootstrap_medians(x, resamples):
    out = []
    for rows in resamples:
        s = sorted(x[i] for i in rows)
        m = len(s) // 2
        out.append((s[m - 1] + s[m]) / 2 if len(s) % 2 == 0 else s[m])
    return sorted(out)


@O
def bootstrap_medians(x, resamples):
    return np.sort(np.median(np.array(x)[np.array(resamples)], axis=1))


Q(None, "Expected Value of a Bet", "Easy", "Should you play?",
  "Given (probability, payoff) outcomes and a cost to play, return the expected profit, rounded to 4 decimals.",
  [(([(0.5, 10), (0.5, 0)], 4), 1.0), (([(1 / 6, 6)] * 6, 3.5), 2.5)],
  ("Add up in a loop.", "O(n)", "O(1)"),
  ("A dot product.", "O(n)", "O(n)"),
  names=["outcomes", "cost"])


@B
def expected_profit(outcomes, cost):
    total = 0.0
    for p, pay in outcomes:
        total += p * pay
    return round(total - cost, 4)


@O
def expected_profit(outcomes, cost):
    o = np.array(outcomes)
    return round(float(o[:, 0] @ o[:, 1] - cost), 4)


Q(None, "Correlation by Hand", "Easy", "Pearson's r",
  "Return Pearson's correlation, rounded to 4 decimals.",
  [(([1, 2, 3, 4], [2, 4, 6, 8]), 1.0), (([1, 2, 3, 4], [4, 1, 3, 2]), -0.4)],
  ("Covariance over the two standard deviations.", "O(n)", "O(1)"),
  ("<code>np.corrcoef</code>.", "O(n)", "O(n)"),
  names=["x", "y"])


@B
def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return round(cov / (sx * sy), 4)


@O
def pearson(x, y):
    return round(float(np.corrcoef(x, y)[0, 1]), 4)


Q(None, "Sample Ratio Mismatch", "Medium", "Is the split broken?",
  "With an intended 50/50 split, return (z, whether |z| &gt; 3). A real experiment failing this check shouldn't be trusted.",
  [((5000, 5100), (-0.995, False)), ((5000, 5400), (-3.9223, True))],
  ("Compute the expected count and standard deviation.", "O(1)", "O(1)"),
  ("One formula.", "O(1)", "O(1)"),
  names=["a", "b"])


@B
def sample_ratio(a, b):
    n = a + b
    expected = n / 2
    sd = math.sqrt(n * 0.5 * 0.5)
    z = (a - expected) / sd
    return (round(z, 4), abs(z) > 3)


@O
def sample_ratio(a, b):
    z = (a - b) / math.sqrt(a + b)
    return (round(z, 4), bool(abs(z) > 3))


Q(None, "Funnel Conversion", "Medium", "pandas",
  "From EVENTS, return distinct users at each of visit, cart, buy, and the share of the previous step, rounded to 4 decimals (first share 1.0).",
  [((["visit", "cart", "buy"],), [['visit', 4, 1.0], ['cart', 3, 0.75], ['buy', 1, 0.3333]])],
  ("A set per step in a loop.", "O(n·s)", "O(n)"),
  ("<code>groupby('step').user.nunique()</code>, then <code>pct_change</code>-style division.", "O(n)", "O(s)"),
  names=["steps"])


@B
def funnel(steps):
    out, prev = [], None
    for s in steps:
        n = len(set(EVENTS[EVENTS.step == s].user))
        out.append([s, n, 1.0 if prev is None else round(n / prev, 4)])
        prev = n
    return out


@O
def funnel(steps):
    counts = EVENTS.groupby("step").user.nunique().reindex(steps)
    share = (counts / counts.shift()).fillna(1.0).round(4)
    return [[s, int(counts[s]), float(share[s])] for s in steps]


Q(None, "Cohort Retention", "Hard", "A real analytics task",
  "For cohort c from EVENTS, return the share of its users active in each week 0 to last_week, rounded to 4 decimals.",
  [((0, 2), [1.0, 0.5, 0.5])],
  ("Set of cohort users, then a set per week.", "O(n·w)", "O(n)"),
  ("<code>groupby('week').user.nunique()</code>, then <code>reindex</code>.", "O(n)", "O(w)"),
  names=["c", "last_week"])


@B
def retention(c, last_week):
    rows = EVENTS[EVENTS.cohort == c]
    total = len(set(rows.user))
    return [round(len(set(rows[rows.week == w].user)) / total, 4) for w in range(last_week + 1)]


@O
def retention(c, last_week):
    rows = EVENTS[EVENTS.cohort == c]
    weekly = rows.groupby("week").user.nunique().reindex(range(last_week + 1), fill_value=0)
    return (weekly / rows.user.nunique()).round(4).tolist()


Q(None, "Top N per Group in pandas", "Medium", "SQL's RANK, in pandas",
  "From SALES, return the [region, product] with the top n revenues in each region, ordered by region, then by revenue descending.",
  [((1,), [['E', 'c'], ['N', 'a'], ['S', 'b']]), ((2,), [['E', 'c'], ['N', 'a'], ['N', 'b'], ['S', 'b'], ['S', 'a']])],
  ("Loop over regions and sort each.", "O(r·n log n)", "O(n)"),
  ("<code>sort_values</code> then <code>groupby().head(n)</code>.", "O(n log n)", "O(n)"),
  names=["n"])


@B
def top_n(n):
    out = []
    for region in sorted(SALES.region.unique()):
        rows = SALES[SALES.region == region].sort_values("revenue", ascending=False)
        out += [[region, p] for p in rows["product"].head(n)]
    return out


@O
def top_n(n):
    top = SALES.sort_values(["region", "revenue"], ascending=[True, False]).groupby("region").head(n)
    return top[["region", "product"]].values.tolist()


Q(None, "Percent of Group Total", "Medium", "transform",
  "From SALES, return each row's revenue as a percentage of its region's total, rounded to 1 decimal, in the original row order.",
  [((), [50.0, 30.0, 20.0, 40.0, 60.0, 100.0])],
  ("Compute a dictionary of totals, then divide.", "O(n)", "O(r)"),
  ("<code>groupby().transform('sum')</code> keeps the shape.", "O(n)", "O(n)"))


@B
def percent_of_region():
    totals = {}
    for r, v in zip(SALES.region, SALES.revenue):
        totals[r] = totals.get(r, 0) + v
    return [round(100 * v / totals[r], 1) for r, v in zip(SALES.region, SALES.revenue)]


@O
def percent_of_region():
    return (100 * SALES.revenue / SALES.groupby("region").revenue.transform("sum")).round(1).tolist()


Q(None, "Rolling Average", "Easy", "Smoothing a metric",
  "Return the k-period rolling mean, with None for the first k−1 positions, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5], 3), [None, None, 2.0, 3.0, 4.0])],
  ("Average each slice.", "O(n·k)", "O(n)"),
  ("<code>Series.rolling(k).mean()</code>.", "O(n)", "O(n)"),
  names=["x", "k"])


@B
def rolling_mean(x, k):
    return [None if i + 1 < k else round(sum(x[i + 1 - k:i + 1]) / k, 4) for i in range(len(x))]


@O
def rolling_mean(x, k):
    s = pd.Series(x, dtype=float).rolling(k).mean().round(4)
    return [None if pd.isna(v) else float(v) for v in s]


Q(None, "Margin of Error vs Sample Size", "Easy", "Quadruple the data, halve the error",
  "Return the 95% margin of error (1.96·SE) of a proportion p for each sample size, rounded to 4 decimals.",
  [((0.5, [100, 400, 1600]), [0.098, 0.049, 0.0245])],
  ("Loop over sizes.", "O(k)", "O(k)"),
  ("Vectorised with NumPy.", "O(k)", "O(k)"),
  names=["p", "sizes"])


@B
def margins(p, sizes):
    return [round(1.96 * math.sqrt(p * (1 - p) / n), 4) for n in sizes]


@O
def margins(p, sizes):
    return (1.96 * np.sqrt(p * (1 - p) / np.array(sizes))).round(4)
