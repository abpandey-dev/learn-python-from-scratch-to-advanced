from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

LESSON("Basics", "The logic of a hypothesis test", """
<p>Your new checkout page converted 12.5% of users; the old one 10%. Is the new page better, or did you just get a lucky week? A hypothesis test answers: <b>"if there were really no difference, how surprising would this data be?"</b></p>
<ol>
<li><b>Null hypothesis H₀</b>: no effect (the rates are equal). <b>Alternative H₁</b>: there is an effect.</li>
<li>Pick a <b>significance level α</b> before looking, usually 0.05.</li>
<li>Compute a <b>test statistic</b> (z, t, χ², F): how far the data is from H₀, in units of noise.</li>
<li>The <b>p-value</b> is the probability of a statistic at least this extreme if H₀ were true.</li>
<li>If p &lt; α, <b>reject H₀</b>. Otherwise you "fail to reject" — which is not proof that H₀ is true.</li>
</ol>
<p>Think of a courtroom: H₀ is "innocent", the data is the evidence, and α is how much doubt you tolerate before convicting.</p>
""", practice=["One-Sample z-Test", "One-Tailed or Two-Tailed?"])


@LD
def p_value_picture():
    z = 1.8
    x = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot(x, stats.norm.pdf(x), color="#0f766e")
    ax.fill_between(x, stats.norm.pdf(x), where=abs(x) >= z, color="#f59e0b", alpha=0.6)
    p = 2 * stats.norm.sf(z)
    ax.set_title(f"two-sided p for z = {z}: {p:.3f}")


LESSON("Basics", "Two kinds of mistakes", """
<table>
<tr><th></th><th>H₀ really true</th><th>H₀ really false</th></tr>
<tr><td><b>Reject H₀</b></td><td>Type I error (false positive), rate α</td><td>correct: you found it (power = 1 − β)</td></tr>
<tr><td><b>Don't reject</b></td><td>correct</td><td>Type II error (false negative), rate β</td></tr>
</table>
<p>Lowering α makes false alarms rarer but misses more real effects. The way to get both low is <b>more data</b>. That's why you decide the sample size before the experiment — and why peeking at the p-value every day and stopping when it dips below 0.05 inflates false positives.</p>
""", practice=["Power of a z-Test", "How Many Users Does the A/B Test Need?"])

LESSON("Core", "Which test? z, t, paired, Welch", """
<table>
<tr><th>Question</th><th>Test</th><th>SciPy</th></tr>
<tr><td>One mean vs a target, σ known</td><td>z-test</td><td><code>norm.sf</code></td></tr>
<tr><td>One mean vs a target, σ unknown</td><td>one-sample t</td><td><code>ttest_1samp</code></td></tr>
<tr><td>Two independent groups</td><td>Welch's t (default)</td><td><code>ttest_ind(equal_var=False)</code></td></tr>
<tr><td>Same people measured twice</td><td>paired t</td><td><code>ttest_rel</code></td></tr>
<tr><td>Two conversion rates</td><td>two-proportion z / 2×2 χ²</td><td><code>chi2_contingency</code></td></tr>
<tr><td>3+ group means</td><td>one-way ANOVA</td><td><code>f_oneway</code></td></tr>
<tr><td>Two categorical variables</td><td>χ² independence</td><td><code>chi2_contingency</code></td></tr>
<tr><td>Counts vs expected shares</td><td>χ² goodness of fit</td><td><code>chisquare</code></td></tr>
<tr><td>Skewed data or outliers</td><td>Mann–Whitney U</td><td><code>mannwhitneyu</code></td></tr>
</table>
<p>The t distribution is like the normal curve with fatter tails, because the standard deviation is itself estimated; with 30+ observations they're almost the same. Pairing removes person-to-person variation, so a paired test is far more powerful when it applies.</p>
""", practice=["One-Sample t Statistic", "Welch's t-Test", "Pooled Two-Sample t-Test", "Paired t-Test", "A/B Test on Conversion Rates"])

LESSON("Core", "Categories and many groups: χ² and ANOVA", """
<p><b>Chi-square</b> compares observed counts with the counts you'd expect if H₀ were true: χ² = Σ (O − E)² / E. For a table, E = row total × column total / grand total, and degrees of freedom = (rows − 1)(columns − 1). Expected counts should be at least about 5.</p>
<p><b>ANOVA</b> asks whether any of several means differ. F = variance between group means ÷ variance within groups. A big F says the groups differ more than their internal noise explains. ANOVA only tells you <i>some</i> group differs; follow up with pairwise tests (and a correction, below).</p>
""", practice=["Is the Die Fair?", "Are Two Categories Related?", "One-Way ANOVA"])

LESSON("Advanced", "When formulas don't fit: ranks, permutations, the bootstrap", """
<ul>
<li><b>Mann–Whitney U</b> compares ranks, so one huge value can't dominate. Use it for skewed data such as time on site or revenue per user.</li>
<li><b>Permutation test</b>: if group labels don't matter (H₀), shuffling them shouldn't change the difference much. The p-value is the share of shuffles at least as extreme as what you saw. No distribution assumptions.</li>
<li><b>Bootstrap</b>: resample your data with replacement thousands of times and recompute the statistic; the middle 95% of those values is a confidence interval. Works for medians, ratios, anything.</li>
<li><b>Exact binomial test</b>: for small samples of yes/no outcomes, add up the binomial probabilities instead of using the normal approximation.</li>
</ul>
""", practice=["Mann–Whitney U", "Permutation Test", "Bootstrap Confidence Interval", "Exact Binomial Test"])


@LD
def bootstrap_picture():
    rng = np.random.default_rng(0)
    data = np.array([12.1, 11.8, 12.6, 12.9, 12.3, 11.5, 12.8, 12.4])
    means = data[rng.integers(0, len(data), size=(2000, len(data)))].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.hist(means, bins=30, color="#99c9c2")
    ax.axvline(lo, color="#b45309")
    ax.axvline(hi, color="#b45309")
    ax.set_title(f"95% bootstrap CI: {lo:.2f} to {hi:.2f}")


LESSON("Advanced", "Significant is not the same as important", """
<ul>
<li><b>Effect size</b>: with a million users, a 0.01% lift can be "significant" and worthless. Report the size of the effect (difference, lift, Cohen's d ≈ 0.2 small, 0.5 medium, 0.8 large) with a <b>confidence interval</b>.</li>
<li><b>Multiple testing</b>: test 20 metrics at α = 0.05 and you expect one false positive by luck. <b>Bonferroni</b> divides α by the number of tests (strict); <b>Benjamini–Hochberg</b> controls the share of false discoveries (less strict, common in analytics).</li>
<li><b>Practical checklist</b> for an A/B test: one primary metric chosen in advance, sample size from a power calculation, randomise users (not sessions), run full weeks, check the split is really 50/50 (sample ratio mismatch), don't peek.</li>
</ul>
""", practice=["Confidence Interval for a Difference", "Effect Size: Cohen's d", "Bonferroni Correction", "False Discovery Rate (Benjamini–Hochberg)"])
