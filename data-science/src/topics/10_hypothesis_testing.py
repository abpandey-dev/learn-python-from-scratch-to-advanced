from lib import *
import math
from itertools import combinations
import numpy as np
import pandas as pd
from scipy import stats


TOPIC(
    id="hypothesis-testing", title="Hypothesis Testing & Inference", glyph="H₀",
    blurb="Decide whether a difference is real or luck: null and alternative hypotheses, p-values, z and t tests, chi-square, ANOVA, non-parametric and permutation tests, the bootstrap, power and sample size, effect sizes and multiple testing.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">from scipy import stats
stats.ttest_1samp(a, popmean=10)              # one sample vs a known value
stats.ttest_ind(a, b, equal_var=False)        # two independent groups (Welch)
stats.ttest_rel(before, after)                # paired: same people twice
stats.chi2_contingency(table, correction=False)  # independence of two categories
stats.chisquare(observed, expected)           # goodness of fit
stats.f_oneway(g1, g2, g3)                    # ANOVA: 3+ group means
stats.mannwhitneyu(a, b)                      # no normality assumption
stats.binomtest(k, n, p=0.5)                  # exact test for one proportion
stats.norm.sf(z), stats.norm.ppf(0.975)       # tail area, critical value 1.96
stats.false_discovery_control(pvals)          # Benjamini-Hochberg</code></pre>
<p>Decision: if p &lt; α (usually 0.05) reject H₀. A p-value is P(data at least this extreme | H₀ true) — not P(H₀ true).</p>
""")

GA = [12.1, 11.8, 12.6, 12.9, 12.3, 11.5, 12.8, 12.4]
GB = [11.2, 11.9, 11.4, 12.0, 11.1, 11.6, 11.8, 11.3]


def phi(z):
    """Standard normal CDF, from the error function."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def mean_var(x):
    m = sum(x) / len(x)
    return m, sum((v - m) ** 2 for v in x) / (len(x) - 1)


Q(None, "One-Sample z-Test", "Easy", "Known σ · two-sided p",
  "A machine should fill 500 ml with known σ = <code>sigma</code>. Given a sample, return <code>(z, two-sided p)</code>, rounded to 4 decimals.",
  [(([502, 498, 505, 503, 501, 499, 504, 506], 500, 3), (2.1213, 0.0339)), (([500, 500, 501, 499], 500, 2), (0.0, 1.0))],
  ("z = (x̄ − μ₀) / (σ / √n); the normal CDF from <code>math.erf</code>.", "O(n)", "O(1)"),
  ("<code>stats.norm.sf(|z|) × 2</code> — sf is the upper-tail area 1 − CDF.", "O(n)", "O(1)"),
  viz=([502, 498, 505, 503, 501, 499, 504, 506], 500, 3))


@B
def z_test(sample, mu0, sigma):
    n = len(sample)
    z = (sum(sample) / n - mu0) / (sigma / math.sqrt(n))
    p = 2 * (1 - phi(abs(z)))
    return (round(z, 4), round(p, 4))


@O
def z_test(sample, mu0, sigma):
    z = (np.mean(sample) - mu0) / (sigma / np.sqrt(len(sample)))
    return (round(z, 4), round(2 * stats.norm.sf(abs(z)), 4))


Q(None, "One-Sample t Statistic", "Easy", "Unknown σ",
  "Return <code>(t, degrees of freedom)</code> testing whether the mean of <code>sample</code> equals <code>mu0</code>.",
  [((GA, 12.0), (1.753, 7)), ((GB, 12.0), (-3.8726, 7))],
  ("t = (x̄ − μ₀) / (s / √n) with the sample std s; df = n − 1.", "O(n)", "O(1)"),
  ("<code>stats.ttest_1samp</code> returns the statistic and its <code>df</code>.", "O(n)", "O(1)"),
  viz=(GA, 12.0))


@B
def t_one(sample, mu0):
    m, v = mean_var(sample)
    t = (m - mu0) / math.sqrt(v / len(sample))
    return (round(t, 4), len(sample) - 1)


@O
def t_one(sample, mu0):
    r = stats.ttest_1samp(sample, mu0)
    return (round(float(r.statistic), 4), int(r.df))


Q(None, "Welch's t-Test", "Medium", "Two groups, unequal variances",
  "Return <code>(t, df)</code> for Welch's two-sample t-test (df rounded to 2 decimals).",
  [((GA, GB), (3.6538, 12.51)), ((GA, [12.0, 12.2, 11.9]), (1.3851, 8.99))],
  ("t = (x̄₁ − x̄₂)/√(s₁²/n₁ + s₂²/n₂); df from the Welch–Satterthwaite formula.", "O(n)", "O(1)"),
  ("<code>stats.ttest_ind(a, b, equal_var=False)</code> — the safe default.", "O(n)", "O(1)"),
  viz=(GA, GB))


@B
def welch(a, b):
    m1, v1 = mean_var(a)
    m2, v2 = mean_var(b)
    se1, se2 = v1 / len(a), v2 / len(b)
    t = (m1 - m2) / math.sqrt(se1 + se2)
    df = (se1 + se2) ** 2 / (se1 ** 2 / (len(a) - 1) + se2 ** 2 / (len(b) - 1))
    return (round(t, 4), round(df, 2))


@O
def welch(a, b):
    r = stats.ttest_ind(a, b, equal_var=False)
    return (round(float(r.statistic), 4), round(float(r.df), 2))


Q(None, "Pooled Two-Sample t-Test", "Medium", "Equal variances",
  "Return <code>(t, df)</code> for the classic (pooled variance) two-sample t-test.",
  [((GA, GB), (3.6538, 14))],
  ("Pool the variances: s² = ((n₁−1)s₁² + (n₂−1)s₂²)/(n₁+n₂−2).", "O(n)", "O(1)"),
  ("<code>stats.ttest_ind(a, b)</code> (equal_var=True is its default).", "O(n)", "O(1)"),
  viz=(GA, GB))


@B
def pooled(a, b):
    m1, v1 = mean_var(a)
    m2, v2 = mean_var(b)
    df = len(a) + len(b) - 2
    sp2 = ((len(a) - 1) * v1 + (len(b) - 1) * v2) / df
    t = (m1 - m2) / math.sqrt(sp2 * (1 / len(a) + 1 / len(b)))
    return (round(t, 4), df)


@O
def pooled(a, b):
    r = stats.ttest_ind(a, b)
    return (round(float(r.statistic), 4), int(r.df))


Q(None, "Paired t-Test", "Medium", "Before and after",
  "The same 6 users were timed before and after a redesign. Return <code>(t, two-sided p)</code>.",
  [(([31, 28, 35, 40, 30, 33], [27, 27, 30, 36, 29, 30]), (4.3916, 0.0071))],
  ("Take the differences and run a one-sample t-test on them against 0 (p from SciPy's t distribution).", "O(n)", "O(n)"),
  ("<code>stats.ttest_rel(before, after)</code>.", "O(n)", "O(n)"),
  viz=([31, 28, 35, 40, 30, 33], [27, 27, 30, 36, 29, 30]))


@B
def paired(before, after):
    d = [x - y for x, y in zip(before, after)]
    m, v = mean_var(d)
    t = m / math.sqrt(v / len(d))
    p = 2 * stats.t.sf(abs(t), len(d) - 1)
    return (round(t, 4), round(float(p), 4))


@O
def paired(before, after):
    r = stats.ttest_rel(before, after)
    return (round(float(r.statistic), 4), round(float(r.pvalue), 4))


Q(None, "A/B Test on Conversion Rates", "Medium", "Two-proportion z-test",
  "Control converted <code>c1</code> of <code>n1</code>, the variant <code>c2</code> of <code>n2</code>. Return <code>(z, two-sided p)</code>.",
  [((200, 2000, 250, 2000), (2.502, 0.0124)), ((48, 500, 52, 500), (0.4216, 0.6733))],
  ("Pooled rate p̂, SE = √(p̂(1−p̂)(1/n₁+1/n₂)), z = (p₂ − p₁)/SE.", "O(1)", "O(1)"),
  ("A 2×2 chi-square without continuity correction is the same test: χ² = z².", "O(1)", "O(1)"),
  viz=(200, 2000, 250, 2000))


@B
def ab_test(c1, n1, c2, n2):
    p1, p2 = c1 / n1, c2 / n2
    p = (c1 + c2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se
    return (round(z, 4), round(2 * (1 - phi(abs(z))), 4))


@O
def ab_test(c1, n1, c2, n2):
    table = [[c1, n1 - c1], [c2, n2 - c2]]
    chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
    z = np.sign(c2 / n2 - c1 / n1) * np.sqrt(chi2)
    return (round(float(z), 4), round(float(p), 4))


Q(None, "Is the Die Fair?", "Medium", "Chi-square goodness of fit",
  "Given counts of faces 1–6, return <code>(χ² statistic, reject fairness at 5%)</code>.",
  [(([16, 18, 16, 14, 12, 44],), (35.6, True)), (([20, 22, 17, 18, 19, 24],), (1.7, False))],
  ("Σ (O − E)²/E with E = total/6; compare to the table value 11.07 for 5 degrees of freedom.", "O(k)", "O(1)"),
  ("<code>stats.chisquare(observed)</code> gives the p-value directly.", "O(k)", "O(1)"),
  viz=([16, 18, 16, 14, 12, 44],))


@B
def fair_die(counts):
    e = sum(counts) / len(counts)
    chi2 = sum((o - e) ** 2 / e for o in counts)
    return (round(chi2, 4), chi2 > 11.0705)


@O
def fair_die(counts):
    r = stats.chisquare(counts)
    return (round(float(r.statistic), 4), bool(r.pvalue < 0.05))


Q(None, "Are Two Categories Related?", "Medium", "Chi-square independence",
  "<code>table</code> counts people by group (rows) and choice (columns). Return <code>(χ², degrees of freedom, expected count in the top-left cell)</code>.",
  [(([[30, 20, 10], [20, 30, 40]],), (16.6667, 2, 20.0)), (([[10, 10], [10, 10]],), (0.0, 1, 10.0))],
  ("Expected = row total × column total / grand total; sum (O − E)²/E; df = (r−1)(c−1).", "O(rc)", "O(rc)"),
  ("<code>stats.chi2_contingency(table, correction=False)</code> returns all of these.", "O(rc)", "O(rc)"),
  viz=([[30, 20, 10], [20, 30, 40]],))


@B
def independence(table):
    rows = [sum(r) for r in table]
    cols = [sum(c) for c in zip(*table)]
    total = sum(rows)
    chi2 = 0
    for i, r in enumerate(table):
        for j, o in enumerate(r):
            e = rows[i] * cols[j] / total
            chi2 += (o - e) ** 2 / e
    return (round(chi2, 4), (len(rows) - 1) * (len(cols) - 1), round(rows[0] * cols[0] / total, 4))


@O
def independence(table):
    chi2, p, dof, expected = stats.chi2_contingency(table, correction=False)
    return (round(float(chi2), 4), int(dof), round(float(expected[0][0]), 4))


Q(None, "One-Way ANOVA", "Medium", "Three or more means",
  "Return the F statistic comparing the means of all the groups.",
  [(([[85, 86, 88, 75, 78], [91, 92, 93, 85, 87], [79, 78, 88, 94, 92]],), 2.0), (([GA, GB],), 13.3506)],
  ("F = (between-group variance) / (within-group variance) from sums of squares.", "O(n)", "O(k)"),
  ("<code>stats.f_oneway(*groups)</code>.", "O(n)", "O(k)"),
  viz=([[85, 86, 88, 75, 78], [91, 92, 93, 85, 87], [79, 78, 88, 94, 92]],))


@B
def anova_f(groups):
    allv = [v for g in groups for v in g]
    grand = sum(allv) / len(allv)
    ssb = sum(len(g) * (sum(g) / len(g) - grand) ** 2 for g in groups)
    ssw = sum((v - sum(g) / len(g)) ** 2 for g in groups for v in g)
    k, n = len(groups), len(allv)
    return round((ssb / (k - 1)) / (ssw / (n - k)), 4)


@O
def anova_f(groups):
    return round(float(stats.f_oneway(*groups).statistic), 4)


Q(None, "One-Tailed or Two-Tailed?", "Easy", "Alternative hypotheses",
  "For a z statistic, return the p-value for <code>alternative</code> 'two-sided', 'greater' or 'less'.",
  [((1.8, "two-sided"), 0.0719), ((1.8, "greater"), 0.0359), ((1.8, "less"), 0.9641), ((-2.5, "less"), 0.0062)],
  ("Areas under the normal curve from <code>math.erf</code>.", "O(1)", "O(1)"),
  ("<code>norm.sf</code> (upper tail) and <code>norm.cdf</code> (lower tail).", "O(1)", "O(1)"),
  viz=(1.8, "greater"))


@B
def tail_p(z, alternative):
    if alternative == "greater":
        p = 1 - phi(z)
    elif alternative == "less":
        p = phi(z)
    else:
        p = 2 * (1 - phi(abs(z)))
    return round(p, 4)


@O
def tail_p(z, alternative):
    p = {"greater": stats.norm.sf(z), "less": stats.norm.cdf(z), "two-sided": 2 * stats.norm.sf(abs(z))}[alternative]
    return round(float(p), 4)


Q(None, "Confidence Interval for a Difference", "Medium", "Large-sample CI",
  "Return the 95% confidence interval <code>(low, high)</code> for mean(a) − mean(b), using the normal critical value and Welch's standard error.",
  [((GA, GB), (0.3535, 1.1715))],
  ("diff ± 1.959964 × √(s₁²/n₁ + s₂²/n₂).", "O(n)", "O(1)"),
  ("<code>stats.norm.ppf(0.975)</code> for the critical value, NumPy for the rest.", "O(n)", "O(1)"),
  viz=(GA, GB))


@B
def ci_diff(a, b):
    m1, v1 = mean_var(a)
    m2, v2 = mean_var(b)
    se = math.sqrt(v1 / len(a) + v2 / len(b))
    d = m1 - m2
    return (round(d - 1.959964 * se, 4), round(d + 1.959964 * se, 4))


@O
def ci_diff(a, b):
    a, b = np.array(a), np.array(b)
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    z = stats.norm.ppf(0.975)
    d = a.mean() - b.mean()
    return (round(d - z * se, 4), round(d + z * se, 4))


Q(None, "How Many Users Does the A/B Test Need?", "Hard", "Sample size",
  "Return the users needed <b>per group</b> to detect a change from rate <code>p1</code> to <code>p2</code> with two-sided α = <code>alpha</code> and power <code>power</code> (round up).",
  [((0.10, 0.12, 0.05, 0.8), 3839), ((0.30, 0.33, 0.05, 0.9), 5034)],
  ("n = (z₁₋α/₂ + z_power)² (p₁(1−p₁) + p₂(1−p₂)) / (p₁ − p₂)², with z found by bisection on the normal CDF.", "O(log 1/ε)", "O(1)"),
  ("<code>stats.norm.ppf</code> gives the z values directly.", "O(1)", "O(1)"),
  viz=(0.10, 0.12, 0.05, 0.8))


@B
def sample_size(p1, p2, alpha, power):
    def inv_phi(q):
        lo, hi = -10.0, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if phi(mid) < q:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    z = inv_phi(1 - alpha / 2) + inv_phi(power)
    return math.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2)


@O
def sample_size(p1, p2, alpha, power):
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return int(np.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2))


Q(None, "Power of a z-Test", "Medium", "Chance of catching a real effect",
  "A true difference <code>delta</code> exists, σ = <code>sigma</code>, n per test, two-sided α = 0.05. Return the power (ignore the tiny opposite tail).",
  [((2, 5, 50), 0.8074), ((1, 5, 50), 0.2926), ((1, 5, 400), 0.9793)],
  ("Power = Φ(δ√n/σ − 1.959964).", "O(1)", "O(1)"),
  ("<code>norm.cdf(effect − norm.ppf(0.975))</code>.", "O(1)", "O(1)"),
  viz=(2, 5, 50))


@B
def power(delta, sigma, n):
    return round(phi(delta * math.sqrt(n) / sigma - 1.959964), 4)


@O
def power(delta, sigma, n):
    return round(float(stats.norm.cdf(delta * np.sqrt(n) / sigma - stats.norm.ppf(0.975))), 4)


Q(None, "Permutation Test", "Hard", "No formula needed",
  "Is the difference in means between <code>a</code> and <code>b</code> real? Shuffle the group labels in every possible way and return the two-sided p-value (twice the smaller one-sided p, at most 1).",
  [(([12, 15, 14, 17], [10, 11, 13, 9]), 0.0571), (([5, 6, 7], [5, 6, 8]), 1.0)],
  ("Try every way to choose which values form group a; count how often the difference is at least as extreme.", "O(C(n, k))", "O(n)"),
  ("<code>stats.permutation_test</code> with <code>n_resamples=np.inf</code> enumerates every split exactly.", "O(C(n, k))", "O(n)"),
  viz=([12, 15, 14, 17], [10, 11, 13, 9]))


@B
def perm_test(a, b):
    pool = a + b
    observed = sum(a) / len(a) - sum(b) / len(b)
    ge = le = total = 0
    for idx in combinations(range(len(pool)), len(a)):
        ga = [pool[i] for i in idx]
        gb = [pool[i] for i in range(len(pool)) if i not in idx]
        d = sum(ga) / len(ga) - sum(gb) / len(gb)
        total += 1
        ge += d >= observed - 1e-12
        le += d <= observed + 1e-12
    return round(min(1.0, 2 * min(ge, le) / total), 4)


@O
def perm_test(a, b):
    diff = lambda x, y: np.mean(x) - np.mean(y)
    r = stats.permutation_test((a, b), diff, permutation_type="independent", n_resamples=np.inf)
    return round(float(r.pvalue), 4)


Q(None, "Bootstrap Confidence Interval", "Medium", "Resampling",
  "Resample <code>data</code> with replacement 2,000 times (seed 0, NumPy <code>default_rng</code>), take each mean, and return the 2.5th and 97.5th percentiles.",
  [((GA,), (11.9875, 12.6))],
  ("Draw the same random row numbers, then average each resample in a plain loop, sort, and interpolate the percentiles by hand.", "O(Bn)", "O(B)"),
  ("Draw all resamples as one 2,000 × n matrix and use <code>np.percentile</code>.", "O(Bn)", "O(Bn)"),
  viz=(GA,))


@B
def bootstrap_ci(data):
    rng = np.random.default_rng(0)
    idx = rng.integers(0, len(data), size=(2000, len(data)))
    means = sorted(sum(data[i] for i in row) / len(row) for row in idx.tolist())

    def pct(q):
        pos = (len(means) - 1) * q
        lo = int(pos)
        return means[lo] + (means[min(lo + 1, len(means) - 1)] - means[lo]) * (pos - lo)
    return (round(pct(0.025), 4), round(pct(0.975), 4))


@O
def bootstrap_ci(data):
    rng = np.random.default_rng(0)
    x = np.array(data)
    means = x[rng.integers(0, len(x), size=(2000, len(x)))].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return (round(lo, 4), round(hi, 4))


Q(None, "Bonferroni Correction", "Easy", "Many tests at once",
  "You ran several tests. Return the indexes still significant at family-wise α = <code>alpha</code> after Bonferroni (compare each p to α / number of tests).",
  [(([0.001, 0.02, 0.04, 0.3, 0.008], 0.05), [0, 4]), (([0.03, 0.04], 0.05), [])],
  ("Loop and compare with α/m.", "O(m)", "O(m)"),
  ("<code>np.flatnonzero(p &lt; alpha / len(p))</code>.", "O(m)", "O(m)"),
  viz=([0.001, 0.02, 0.04, 0.3, 0.008], 0.05))


@B
def bonferroni(pvals, alpha):
    m = len(pvals)
    return [i for i, p in enumerate(pvals) if p < alpha / m]


@O
def bonferroni(pvals, alpha):
    p = np.array(pvals)
    return np.flatnonzero(p < alpha / len(p)).tolist()


Q(None, "False Discovery Rate (Benjamini–Hochberg)", "Hard", "Adjusted p-values",
  "Return BH-adjusted p-values (rounded to 4 decimals) in the original order.",
  [(([0.001, 0.02, 0.04, 0.3, 0.008],), [0.005, 0.0333, 0.05, 0.3, 0.02]), (([0.01, 0.01, 0.5],), [0.015, 0.015, 0.5])],
  ("Sort; adjusted = p × m / rank; then a running minimum from the largest rank down; cap at 1.", "O(m log m)", "O(m)"),
  ("<code>stats.false_discovery_control(p)</code>.", "O(m log m)", "O(m)"),
  viz=([0.001, 0.02, 0.04, 0.3, 0.008],))


@B
def bh(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        running = min(running, pvals[i] * m / rank)
        adj[i] = round(running, 4)
    return adj


@O
def bh(pvals):
    return np.round(stats.false_discovery_control(pvals), 4).tolist()


Q(None, "Mann–Whitney U", "Medium", "Ranks instead of means",
  "Return the U statistic for <code>a</code>: the number of (a, b) pairs where the a value is bigger, counting ties as ½.",
  [(([3, 5, 8, 9], [1, 2, 5, 4]), 13.5), ((GA, GB), 57.5)],
  ("Compare every pair.", "O(nm)", "O(1)"),
  ("<code>stats.mannwhitneyu(a, b).statistic</code> — works from ranks, robust to outliers and skew.", "O((n+m) log(n+m))", "O(n+m)"),
  viz=([3, 5, 8, 9], [1, 2, 5, 4]))


@B
def mwu(a, b):
    u = 0
    for x in a:
        for y in b:
            u += 1 if x > y else 0.5 if x == y else 0
    return float(u)


@O
def mwu(a, b):
    return float(stats.mannwhitneyu(a, b).statistic)


Q(None, "Effect Size: Cohen's d", "Easy", "How big, not just whether",
  "Return Cohen's d = (mean a − mean b) / pooled standard deviation, rounded to 4 decimals.",
  [((GA, GB), 1.8269), (([10, 12, 14], [9, 11, 13]), 0.5)],
  ("Pool the two sample variances by degrees of freedom.", "O(n)", "O(1)"),
  ("NumPy's <code>var(ddof=1)</code>.", "O(n)", "O(1)"),
  viz=(GA, GB))


@B
def cohens_d(a, b):
    m1, v1 = mean_var(a)
    m2, v2 = mean_var(b)
    sp = math.sqrt(((len(a) - 1) * v1 + (len(b) - 1) * v2) / (len(a) + len(b) - 2))
    return round((m1 - m2) / sp, 4)


@O
def cohens_d(a, b):
    a, b = np.array(a), np.array(b)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return round((a.mean() - b.mean()) / sp, 4)


Q(None, "Exact Binomial Test", "Medium", "Small samples, one proportion",
  "A coin landed heads <code>k</code> times in <code>n</code> flips. Return the one-sided p-value P(X ≥ k) if the coin is fair (p = <code>p</code>).",
  [((8, 10, 0.5), 0.0547), ((60, 100, 0.5), 0.0284), ((3, 20, 0.1), 0.3231)],
  ("Add up C(n, i) pⁱ (1−p)ⁿ⁻ⁱ for i = k … n.", "O(n)", "O(1)"),
  ("<code>stats.binomtest(k, n, p, alternative='greater')</code>.", "O(n)", "O(1)"),
  viz=(8, 10, 0.5))


@B
def binom_p(k, n, p):
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * p ** i * (1 - p) ** (n - i)
    return round(total, 4)


@O
def binom_p(k, n, p):
    return round(float(stats.binomtest(k, n, p, alternative="greater").pvalue), 4)
