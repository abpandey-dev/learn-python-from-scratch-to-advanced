from lib import *

THEORY("Logs, metrics, traces", """
<table>
<tr><th>Signal</th><th>Answers</th><th>AI example</th></tr>
<tr><td>Metrics</td><td>how much / how often</td><td>tokens per day, p95 latency, error rate, approval rate</td></tr>
<tr><td>Logs</td><td>what happened</td><td>prompt and response text (redacted)</td></tr>
<tr><td>Traces</td><td>how one request flowed</td><td>retrieval → LLM → tool → LLM, with timings and tokens</td></tr>
<tr><td>Evals</td><td>is it good?</td><td>offline suites and online judges</td></tr>
</table>
""")

THEORY("Judge biases to know", """
<ul>
<li><b>Position bias</b>: prefers the first (or second) answer shown.</li>
<li><b>Verbosity bias</b>: prefers longer answers.</li>
<li><b>Self-preference</b>: prefers answers in its own style or from its own model family.</li>
<li><b>Leniency</b>: scores cluster high — use pass/fail or pairwise instead of fine scales.</li>
</ul>
""")

FAQ("What's the difference between a trace and a span?", "<p>A trace is one end-to-end request; spans are the timed steps inside it (LLM calls, tool calls, retrieval), linked by parent ids into a tree.</p>")
FAQ("How do you evaluate an LLM feature?", "<p>Build an eval set from real cases, pick scorers (code checks, reference metrics, an LLM judge calibrated against human labels), run it on every change, and gate releases on regressions. Then monitor live quality signals.</p>")
FAQ("How do you make LLM-as-judge trustworthy?", "<p>Specific rubrics, structured output, calibration against human labels (kappa), swapping positions in pairwise comparisons, and periodic human spot-checks.</p>")
FAQ("What is Cohen's kappa?", "<p>Agreement between two raters corrected for the agreement you'd expect by chance from their label frequencies. 1 is perfect, 0 is chance level.</p>")
FAQ("What should never appear in your logs?", "<p>API keys, passwords, tokens and unnecessary personal data. Redact before writing, and restrict access to prompt logs.</p>")
FAQ("How do you catch quality regressions after launch?", "<p>Online evals on sampled traffic, user feedback per prompt version, rolling-average alerts, and reviewing traces of failures to add them to the offline eval set.</p>")
