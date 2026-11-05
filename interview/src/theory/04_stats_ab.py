from lib import *

THEORY("Which test?", """
<table><tr><th>Comparing</th><th>Test</th></tr>
<tr><td>Two proportions</td><td>two-proportion z-test</td></tr>
<tr><td>Two means</td><td>Welch's t-test</td></tr>
<tr><td>Categories</td><td>chi-square</td></tr>
<tr><td>Skewed data, medians</td><td>bootstrap or Mann-Whitney</td></tr>
<tr><td>Same subjects, before and after</td><td>paired t-test</td></tr></table>
""")
FAQ("What is a p-value?", "<p>The probability of data at least this extreme if the null hypothesis were true. It isn't the probability that the null is true, or a measure of effect size.</p>")
FAQ("Type I vs Type II error?", "<p>Type I is a false alarm, claiming an effect that isn't there. Type II is a miss, failing to detect a real effect.</p>")
FAQ("What is statistical power?", "<p>The chance of detecting a real effect of a given size. It grows with sample size and effect size, and is usually targeted at 80%.</p>")
FAQ("What does a 95% confidence interval mean?", "<p>The procedure captures the true value in about 95% of repeated samples. It doesn't mean a 95% probability for this particular interval, in the frequentist view.</p>")
FAQ("Central limit theorem?", "<p>The average of many independent samples is approximately normal, whatever the original distribution (with finite variance). That's why z-tests work on conversion rates.</p>")
FAQ("Why does peeking at an A/B test cause problems?", "<p>Each look is another chance for a false positive, so stopping at the first significant result inflates the error rate. Fix the duration, or use sequential testing.</p>")
FAQ("Your test shows significance but a tiny effect. Launch?", "<p>Not automatically. Compare the confidence interval with the cost of launching and maintaining it, and check guardrail metrics. Statistical significance isn't practical significance.</p>")
FAQ("A metric dropped 10% this week. How do you investigate?", "<p>Check data pipelines first. Then segment by platform, region, new vs returning, and date. Look for releases and seasonality. Then ask whether the numerator or denominator changed.</p>")
FAQ("Mean vs median?", "<p>The mean uses every value and is pulled by outliers. The median is robust. For skewed data like income or latency, prefer the median or percentiles.</p>")
FAQ("Correlation vs causation?", "<p>Correlation is a pattern, which may be due to a hidden common cause or reverse causation. Randomised experiments establish causation.</p>")
FAQ("What is Simpson's paradox?", "<p>A trend in every subgroup reverses in the aggregate, because group sizes differ. Check the mix before trusting an overall number.</p>")
FAQ("What is selection bias?", "<p>The sample differs systematically from the population. A survey answered only by engaged users overstates satisfaction, for example.</p>")
FAQ("Can't run an experiment. What then?", "<p>Use observational methods: difference-in-differences, matching or regression discontinuity. State their assumptions clearly, since they give weaker evidence.</p>")
