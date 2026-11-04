from lib import *

THEORY("Descriptive vs inferential statistics", """
<p><b>Descriptive statistics</b> summarise the data you have: centre, spread, shape, relationships. <b>Inferential statistics</b> use a sample to draw conclusions about a larger <b>population</b>, with a measure of uncertainty (confidence intervals, hypothesis tests). A <b>parameter</b> describes the population (μ, σ); a <b>statistic</b> is computed from the sample (x̄, s) and estimates it.</p>
""")

THEORY("Types of variables", """
<table>
<tr><th>Type</th><th>Examples</th><th>Typical summaries</th></tr>
<tr><td>Nominal (categorical)</td><td>city, colour</td><td>counts, mode, proportions</td></tr>
<tr><td>Ordinal</td><td>rating 1–5, size S/M/L</td><td>median, percentiles</td></tr>
<tr><td>Discrete numeric</td><td>number of children</td><td>mean, median, std</td></tr>
<tr><td>Continuous numeric</td><td>height, price</td><td>mean, median, std, histogram</td></tr>
</table>
""")

THEORY("Formulas", """
<table>
<tr><th>Measure</th><th>Formula</th><th>NumPy / pandas</th></tr>
<tr><td>Mean</td><td>x̄ = Σx / n</td><td><code>a.mean()</code></td></tr>
<tr><td>Population variance</td><td>σ² = Σ(x − μ)² / n</td><td><code>a.var()</code></td></tr>
<tr><td>Sample variance</td><td>s² = Σ(x − x̄)² / (n − 1)</td><td><code>a.var(ddof=1)</code>, <code>s.var()</code></td></tr>
<tr><td>z-score</td><td>(x − x̄) / s</td><td><code>(a - a.mean()) / a.std()</code></td></tr>
<tr><td>Covariance</td><td>Σ(x − x̄)(y − ȳ) / (n − 1)</td><td><code>np.cov(x, y)[0, 1]</code></td></tr>
<tr><td>Pearson r</td><td>cov(x, y) / (sₓ s_y)</td><td><code>np.corrcoef(x, y)[0, 1]</code></td></tr>
<tr><td>Slope (least squares)</td><td>Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²</td><td><code>np.polyfit(x, y, 1)</code></td></tr>
<tr><td>R²</td><td>1 − SS_res / SS_tot</td><td>—</td></tr>
<tr><td>Standard error</td><td>s / √n</td><td><code>s.sem()</code></td></tr>
</table>
<p>Dividing by <b>n − 1</b> (Bessel's correction) makes the sample variance an unbiased estimate of the population variance, because deviations are measured from x̄, which is itself fitted to the sample.</p>
""")

THEORY("Shape of a distribution", """
<ul>
<li><b>Symmetric</b> (e.g. normal): mean ≈ median. About 68% of values lie within 1σ, 95% within 2σ, 99.7% within 3σ (the empirical rule).</li>
<li><b>Right-skewed</b> (income, waiting times): long tail to the right, mean &gt; median, skewness &gt; 0.</li>
<li><b>Left-skewed</b> (exam scores near a ceiling): mean &lt; median, skewness &lt; 0.</li>
<li><b>Bimodal</b>: two peaks, often a sign of two mixed groups.</li>
</ul>
""")

THEORY("Common probability distributions", """
<table>
<tr><th>Distribution</th><th>Models</th><th>Parameters</th></tr>
<tr><td>Bernoulli</td><td>one yes/no trial</td><td>p</td></tr>
<tr><td>Binomial</td><td>number of successes in n trials</td><td>n, p</td></tr>
<tr><td>Poisson</td><td>count of events in an interval</td><td>λ</td></tr>
<tr><td>Uniform</td><td>every value equally likely</td><td>a, b</td></tr>
<tr><td>Normal</td><td>sums/averages of many effects</td><td>μ, σ</td></tr>
<tr><td>Exponential</td><td>waiting time between events</td><td>λ</td></tr>
</table>
<p>The <b>Central Limit Theorem</b> says the mean of a large enough sample is approximately normally distributed whatever the original shape — which is why mean ± 1.96·SE works as a 95% interval.</p>
""")

THEORY("Hypothesis testing in one paragraph", """
<p>State a <b>null hypothesis</b> H₀ (e.g. "both groups have the same mean"). Compute a test statistic from the data and its <b>p-value</b>: the probability of a result at least this extreme if H₀ were true. If p &lt; α (often 0.05), reject H₀. Common tests: t-test (compare means), chi-square (categorical association), ANOVA (several means). In Python these live in <code>scipy.stats</code> (<code>ttest_ind</code>, <code>chi2_contingency</code>, <code>pearsonr</code>).</p>
""")

FAQ("Mean or median?", "<p>Use the median when the data is skewed or has outliers (incomes, prices); use the mean for roughly symmetric data or when you need totals.</p>")
FAQ("Why does NumPy std differ from pandas std?", "<p>NumPy defaults to ddof=0 (population, divide by n); pandas defaults to ddof=1 (sample, divide by n − 1). Pass ddof explicitly to match.</p>")
FAQ("Correlation vs causation?", "<p>Correlation measures how two variables move together. Causation needs a controlled experiment or careful reasoning about confounders — a third variable can drive both.</p>")
FAQ("Pearson vs Spearman?", "<p>Pearson measures straight-line relationships and is sensitive to outliers. Spearman correlates ranks, so it captures any monotonic relationship and is robust to outliers.</p>")
FAQ("What does a 95% confidence interval mean?", "<p>If you repeated the sampling many times and built an interval each time, about 95% of those intervals would contain the true population value. It is not a 95% probability for one fixed interval.</p>")
FAQ("What is a p-value?", "<p>The probability of seeing data at least as extreme as yours if the null hypothesis were true. A small p-value is evidence against the null; it is not the probability that the null is true.</p>")
