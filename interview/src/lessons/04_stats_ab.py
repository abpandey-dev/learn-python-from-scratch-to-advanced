from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np



LESSON("Basics", "Uncertainty: standard error and confidence intervals", """
<p>A conversion rate of 5% from 100 visitors means something very different from 5% out of 100,000. <b>Standard error</b> measures how far an estimate tends to wander from the truth:</p>
<p style="text-align:center"><b>SE = √( p(1 − p) / n )</b></p>
<table><tr><th>Sample</th><th>Rate</th><th>Calculation</th><th>SE</th></tr>
<tr><td>1,000</td><td>5%</td><td>√(0.05 × 0.95 / 1000)</td><td>0.0069</td></tr>
<tr><td>10,000</td><td>5%</td><td>√(0.05 × 0.95 / 10000)</td><td>0.0022</td></tr></table>
<p>Ten times the data shrinks the error by only √10 ≈ 3.16. <b>To halve the error, you need four times the data.</b> Margins for p = 0.5: n = 100 gives 0.098, n = 400 gives 0.049, n = 1,600 gives 0.0245.</p>
<p><b>A 95% confidence interval</b> is estimate ± 1.96 × SE. For 50 out of 1,000: 0.05 ± 1.96 × 0.0069 = (0.0365, 0.0635).</p>
<p><b>The correct meaning is a favourite interview check.</b> It's not "95% chance the true value is in this interval". It means: if you repeated the sampling many times, about 95% of the intervals built this way would contain the true value. The demo draws 40 samples, and a few intervals miss. Across 2,000 samples, 93.1% contain the truth: this simple formula runs a little under 95% for rare events, which is why better intervals such as Wilson's exist.</p>
""", practice=["Standard Error of a Proportion", "95% Confidence Interval", "CI of a Mean", "Margin of Error vs Sample Size"])


@LD
def interval_coverage():
    rng = np.random.default_rng(0)
    true_p, n, trials = 0.05, 1000, 2000
    wins = rng.binomial(n, true_p, trials) / n
    half = 1.96 * np.sqrt(wins * (1 - wins) / n)
    covered = (wins - half <= true_p) & (true_p <= wins + half)
    print("intervals containing the truth:", round(float(covered.mean()), 3))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    for i in range(40):
        ax.plot([wins[i] - half[i], wins[i] + half[i]], [i, i], color="tab:blue" if covered[i] else "tab:red")
    ax.axvline(true_p, color="black")
    ax.set_xlabel("95% interval from each of 40 samples (black = truth)")
    ax.set_yticks([])


LESSON("Core", "The A/B test, end to end", """
<p>Control: 200 of 2,000 convert (10%). Treatment: 250 of 2,000 (12.5%). Is it real?</p>
<ol><li><b>Null hypothesis:</b> no real difference.</li>
<li><b>Pooled rate,</b> since under the null there's one rate: 450 / 4000 = 0.1125.</li>
<li><b>Standard error:</b> √(0.1125 × 0.8875 × (1/2000 + 1/2000)) = 0.00999.</li>
<li><b>z:</b> (0.125 − 0.10) / 0.00999 = <b>2.502</b>.</li>
<li><b>p-value:</b> two-sided, <b>0.0124</b>.</li></ol>
<p><b>What the p-value means:</b> if there were truly no difference, a gap at least this large would appear about 1.2% of the time. It is <b>not</b> the probability that the treatment doesn't work, and it says nothing about how big or valuable the effect is.</p>
<p>With 10 vs 11 out of 100, the same maths gives z = 0.23 and p = 0.82: no evidence, though that's not proof of no effect.</p>
<table><tr><th></th><th>Actually no effect</th><th>Actually an effect</th></tr>
<tr><td>Say "effect"</td><td>Type I error (rate α, often 5%)</td><td>Correct (rate = power, often 80%)</td></tr>
<tr><td>Say "no effect"</td><td>Correct</td><td>Type II error (rate β)</td></tr></table>
<p><b>Comparing means</b> uses a t-test. Welch's version doesn't assume equal variance. <b>Counts in categories</b> use chi-square: for [[20, 30], [30, 20]], every expected count is 25, so χ² = 4 × 25/25 = 4.0.</p>
""", practice=["Two-Proportion z-Test", "Welch's t Statistic", "Chi-Square for a 2×2 Table"])


LESSON("Core", "Designing an experiment: sample size and traps", """
<p><b>Decide the sample size before you start:</b></p>
<p style="text-align:center"><b>n per group ≈ 2 (z_α + z_β)² p(1 − p) / δ²</b></p>
<p>With a 10% base rate, 95% confidence and 80% power (1.96 + 0.84 = 2.8):</p>
<table><tr><th>Smallest effect δ</th><th>Calculation</th><th>Per group</th></tr>
<tr><td>2 points</td><td>2 × 7.84 × 0.09 / 0.0004</td><td>3,528</td></tr>
<tr><td>1 point</td><td>2 × 7.84 × 0.09 / 0.0001</td><td>14,112</td></tr></table>
<p>Half the effect needs four times the traffic.</p>
<p><b>Trap 1: peeking.</b> Checking repeatedly and stopping as soon as p &lt; 0.05 inflates false positives a lot, because you get many chances to be fooled. The demo simulates A/A tests, which have no real effect at all. In this run, a single look at the end gives a 5.7% false-positive rate, close to the promised 5%, while stopping at the first significant peek out of 20 gives <b>25.7%</b>. Either fix the duration up front, or use a sequential method built for this.</p>
<p><b>Trap 2: many comparisons.</b> Test 20 metrics at 5%, and the chance of at least one false alarm is 1 − 0.95²⁰ = <b>64%</b>. Name one primary metric in advance, or correct: Bonferroni tests at 0.05 / 20 = 0.0025.</p>
<p><b>Trap 3: a broken split.</b> With a 50/50 design and counts of 5,000 and 5,400, z = −400 / √10400 = −3.92. Chance doesn't do that, so look for a bug. This <b>sample ratio mismatch</b> check should come first.</p>
<p><b>Other things to mention:</b></p>
<ul><li><b>Novelty effects:</b> run long enough, covering full weeks.</li>
<li><b>Interference:</b> in a social network or marketplace, groups affect each other, so consider splitting by region or cluster.</li>
<li><b>Guardrail metrics:</b> latency and unsubscribes must not worsen.</li>
<li><b>Statistical vs practical significance:</b> with huge samples, tiny and worthless effects become "significant".</li></ul>
""", practice=["Sample Size for an A/B Test", "Bonferroni and False Positives", "Sample Ratio Mismatch"])


@LD
def peeking_inflates():
    rng = np.random.default_rng(1)
    tests, peeks, per_peek = 2000, 20, 100
    p = 0.1
    a = rng.binomial(per_peek, p, (tests, peeks)).cumsum(axis=1)
    b = rng.binomial(per_peek, p, (tests, peeks)).cumsum(axis=1)
    n = per_peek * np.arange(1, peeks + 1)
    pool = (a + b) / (2 * n)
    z = np.abs(a - b) / n / np.sqrt(pool * (1 - pool) * 2 / n)
    print("false positive rate, one look at the end:", round(float((z[:, -1] > 1.96).mean()), 3))
    print("false positive rate, stop at any peek:   ", round(float((z > 1.96).any(axis=1).mean()), 3))
    so_far = (z > 1.96).cumsum(axis=1).astype(bool).mean(axis=0)
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(range(1, peeks + 1), so_far)
    ax.axhline(0.05, color="black", linestyle="--", label="the promised 5%")
    ax.set_xlabel("number of peeks")
    ax.set_ylabel("false alarms so far")
    ax.legend(fontsize=7)


LESSON("Core", "Probability puzzles: Bayes and base rates", """
<p>A disease affects 1% of people. A test catches 90% of cases, with a 5% false-positive rate. You test positive. What are the chances you're sick? Most people say about 90%.</p>
<p>Imagine 100,000 people:</p>
<table><tr><th></th><th>People</th><th>Test positive</th></tr>
<tr><td>Sick (1%)</td><td>1,000</td><td>900</td></tr><tr><td>Healthy (99%)</td><td>99,000</td><td>4,950</td></tr></table>
<p>P(sick | positive) = 900 / (900 + 4,950) = <b>15.4%</b>. False alarms outnumber real cases because healthy people are so common. It's the same reason a fraud model with high accuracy can still have poor precision.</p>
<p><b>Tip:</b> imagining counts of people is much harder to get wrong than the formula, and it's a good thing to do out loud.</p>
<p><b>Expected value.</b> Pay 4 to play: a 50% chance of 10, otherwise 0. EV = 0.5 × 10 − 4 = <b>+1</b>, so it's worth playing, on average.</p>
<p><b>Simpson's paradox.</b> Treatment A beats B in every group, yet loses overall:</p>
<table><tr><th>Group</th><th>A</th><th>B</th></tr>
<tr><td>Small stones</td><td>81/87 = 93.1%</td><td>234/270 = 86.7%</td></tr>
<tr><td>Large stones</td><td>192/263 = 73.0%</td><td>55/80 = 68.8%</td></tr>
<tr><td><b>Overall</b></td><td>273/350 = <b>78.0%</b></td><td>289/350 = <b>82.6%</b></td></tr></table>
<p>A gets more of the hard cases, so its overall number is dragged down. Always ask: <b>what's the mix, and could a hidden variable explain this?</b></p>
<p><b>Correlation isn't causation.</b> r runs from −1 to 1 and captures only linear relationships. Ice-cream sales and drownings correlate, because summer drives both. Randomised experiments are how you break that link.</p>
<p><b>When there's no neat formula,</b> as for a median, use the <b>bootstrap</b>: resample your data with replacement many times, and look at the spread of the statistic.</p>
""", practice=["Bayes: The Rare-Disease Test", "Expected Value of a Bet", "Simpson's Paradox", "Correlation by Hand", "Bootstrap a Median"])


LESSON("Advanced", "Analytics in pandas: the take-home classics", """
<p>Many data interviews have a practical round. These patterns come up constantly.</p>
<p><b>Funnel.</b> Count distinct users at each step, and divide by the previous step: visit 4, cart 3 (75%), buy 1 (33.3%). The biggest drop is where to look first. Count users, not events, as one user can trigger many events.</p>
<p><b>Cohort retention.</b> Group users by when they started, then ask what share is still active each week. Cohort 0 has 2 users: both in week 0, one in week 1, one in week 2, so retention is 1.0, 0.5, 0.5.</p>
<p><b>Top N per group:</b></p>
<pre><code class="py">df.sort_values(["region", "revenue"], ascending=[True, False]).groupby("region").head(n)</code></pre>
<p><b>Percent of group total.</b> <code>transform</code> returns a result the same shape as the input, unlike <code>agg</code>:</p>
<pre><code class="py">df.revenue / df.groupby("region").revenue.transform("sum")</code></pre>
<p><b>Rolling average.</b> <code>s.rolling(3).mean()</code> smooths noise. For 1, 2, 3, 4, 5 it gives NaN, NaN, 2, 3, 4.</p>
<table><tr><th>SQL</th><th>pandas</th></tr>
<tr><td>WHERE</td><td><code>df[df.x &gt; 1]</code></td></tr>
<tr><td>GROUP BY … SUM</td><td><code>df.groupby("g").x.sum()</code></td></tr>
<tr><td>HAVING</td><td><code>.filter(lambda g: …)</code>, or filter after grouping</td></tr>
<tr><td>JOIN</td><td><code>df.merge(other, on="k", how="left")</code></td></tr>
<tr><td>SUM() OVER (PARTITION BY)</td><td><code>.transform("sum")</code></td></tr>
<tr><td>LAG</td><td><code>.shift()</code></td></tr>
<tr><td>RANK</td><td><code>.rank(method="min", ascending=False)</code></td></tr></table>
""", practice=["Funnel Conversion", "Cohort Retention", "Top N per Group in pandas", "Percent of Group Total", "Rolling Average"])
