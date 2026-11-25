from lib import *

THEORY("Vocabulary", """
<table>
<tr><th>Term</th><th>Meaning</th></tr>
<tr><td>H₀ / H₁</td><td>null (no effect) / alternative hypothesis</td></tr>
<tr><td>α</td><td>significance level: the false-positive rate you accept (0.05)</td></tr>
<tr><td>p-value</td><td>P(statistic at least this extreme | H₀ true)</td></tr>
<tr><td>Power (1 − β)</td><td>P(reject H₀ | a real effect of a given size exists), target 0.8</td></tr>
<tr><td>Standard error</td><td>standard deviation of an estimate: s/√n for a mean, √(p(1−p)/n) for a proportion</td></tr>
<tr><td>Degrees of freedom</td><td>how many values are free to vary after estimating parameters</td></tr>
<tr><td>Confidence interval</td><td>estimate ± critical value × SE; 95% of such intervals contain the true value</td></tr>
</table>
""")

THEORY("Test statistics", """
<table>
<tr><th>Test</th><th>Statistic</th><th>df</th></tr>
<tr><td>z (one mean)</td><td>(x̄ − μ₀) / (σ/√n)</td><td>—</td></tr>
<tr><td>t (one mean)</td><td>(x̄ − μ₀) / (s/√n)</td><td>n − 1</td></tr>
<tr><td>Welch t</td><td>(x̄₁ − x̄₂) / √(s₁²/n₁ + s₂²/n₂)</td><td>Welch–Satterthwaite</td></tr>
<tr><td>Two proportions</td><td>(p̂₂ − p̂₁) / √(p̂(1−p̂)(1/n₁ + 1/n₂))</td><td>—</td></tr>
<tr><td>χ²</td><td>Σ (O − E)² / E</td><td>(r−1)(c−1) or k − 1</td></tr>
<tr><td>ANOVA F</td><td>(SSB/(k−1)) / (SSW/(n−k))</td><td>k − 1, n − k</td></tr>
</table>
""")

THEORY("Assumptions to check", """
<ul>
<li><b>Independence</b>: observations don't influence each other (no repeated users counted as separate samples).</li>
<li><b>Normality</b> of the mean: fine for n ≳ 30 by the central limit theorem; otherwise use ranks, permutations or the bootstrap.</li>
<li><b>Equal variances</b>: don't assume it — Welch's t-test is safe either way.</li>
<li><b>Expected counts ≥ 5</b> for χ²; otherwise use Fisher's exact test.</li>
</ul>
""")

FAQ("What does a p-value of 0.03 mean?", "<p>If there were truly no effect, data at least this extreme would occur 3% of the time. It is not the probability that H₀ is true, and not the probability the result is a fluke.</p>")
FAQ("Why not stop the A/B test as soon as p < 0.05?", "<p>Checking repeatedly gives many chances for noise to cross the line, so the real false-positive rate becomes much higher than 5%. Fix the sample size in advance, or use a sequential method designed for peeking.</p>")
FAQ("Type I vs Type II error?", "<p>Type I: rejecting a true H₀ (false alarm, rate α). Type II: missing a real effect (rate β). More data reduces Type II without raising Type I.</p>")
FAQ("When use a paired test?", "<p>When each observation in one group has a natural partner in the other: the same user before and after, the same product in two stores. Pairing removes between-subject variation.</p>")
FAQ("t-test vs Mann–Whitney?", "<p>The t-test compares means and assumes roughly normal sample means; Mann–Whitney compares ranks and is robust to outliers and skew, at a small cost in power for normal data.</p>")
FAQ("What is the multiple comparisons problem?", "<p>Running many tests makes some false positives almost certain. Correct with Bonferroni (controls any false positive) or Benjamini–Hochberg (controls the false discovery rate).</p>")
FAQ("Statistical vs practical significance?", "<p>Statistical significance says the effect is probably not zero; practical significance says it is big enough to matter. Always report effect sizes and confidence intervals.</p>")
