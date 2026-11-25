from lib import *

THEORY("What EDA is for", """
<ul>
<li><b>Understand the grain</b>: what one row represents. Most analysis bugs come from getting this wrong (counting order lines as orders).</li>
<li><b>Find data problems</b> before they become wrong conclusions: gaps, duplicates, impossible values, units.</li>
<li><b>Form hypotheses</b> to test properly later; EDA alone shows associations, not causes.</li>
</ul>
""")

THEORY("Choosing a chart", """
<table>
<tr><th>Message</th><th>Chart</th></tr>
<tr><td>Change over time</td><td>line</td></tr>
<tr><td>Compare categories</td><td>sorted horizontal bar</td></tr>
<tr><td>Distribution</td><td>histogram, box plot</td></tr>
<tr><td>Relationship</td><td>scatter (add a trend line)</td></tr>
<tr><td>Part of a whole</td><td>stacked bar; a pie only for 2–3 parts</td></tr>
<tr><td>Cohorts, two categories</td><td>heat map</td></tr>
<tr><td>One headline number</td><td>a big number with its change vs last period</td></tr>
</table>
""")

THEORY("Good KPI definitions", """
<p>A KPI needs: a <b>name</b>, an exact <b>formula</b> (numerator and denominator), the <b>grain and time window</b>, <b>filters</b> (test accounts, refunds), the <b>owner</b>, and the <b>target</b>. Pair every KPI with a counter-metric so it can't be gamed: conversion with refund rate, speed with error rate.</p>
<p>A <b>North Star metric</b> captures the value customers get (e.g. weekly orders delivered on time). Input metrics are the levers that move it.</p>
""")

FAQ("What do you do first with a new dataset?", "<p>Check the shape and what one row means, the types, missing values and duplicates, then look at each column alone before relationships. Validate a total against a number you already know.</p>")
FAQ("Mean or median for revenue?", "<p>Usually report both. Revenue is right-skewed, so a few big customers pull the mean far above the typical customer; the median describes the typical one.</p>")
FAQ("What is a cohort analysis?", "<p>Grouping users by when they started and tracking each group over time, so you can see whether retention or spending improves for newer cohorts instead of mixing old and new users together.</p>")
FAQ("Revenue dropped 20% — how do you investigate?", "<p>Check data quality first (missing data, tracking changes), then split the change by dimensions (segment, region, channel, new vs returning, orders vs order value) to find which part explains most of it, then look for a cause (release, price change, seasonality, competitor).</p>")
FAQ("How do you make a chart persuasive?", "<p>One message per chart, stated in the title; sort the data; remove clutter; highlight what matters in colour and grey out the rest; label values directly.</p>")
FAQ("What is LTV/CAC?", "<p>Lifetime value per customer divided by the cost to acquire one. Below 1 you lose money on every customer; around 3 or more is usually considered healthy.</p>")
