from lib import *

THEORY("Agent failure modes", """
<table><tr><th>Failure</th><th>Defence</th></tr>
<tr><td>Endless loops</td><td>step and cost limits, repeat detection</td></tr>
<tr><td>Bad tool inputs</td><td>schema validation; return errors to the model</td></tr>
<tr><td>Dangerous actions</td><td>allow-lists, approval, least privilege, sandboxes</td></tr>
<tr><td>Prompt injection</td><td>untrusted-data handling, limited tools, checks in code</td></tr>
<tr><td>Context filling up</td><td>trim old tool output, summarise</td></tr>
<tr><td>Silent wrong answers</td><td>evals, verification steps, logs</td></tr></table>
""")

THEORY("The LLM release checklist", """
<ol><li>An eval set exists, with real examples and hard cases.</li>
<li>A regression gate runs on each prompt or model change.</li>
<li>Latency, cost and error dashboards are live.</li>
<li>Budgets and rate limits are set per user.</li>
<li>Personal data is handled deliberately, in logs too.</li>
<li>Risky tools need approval.</li>
<li>Stop reasons, refusals and tool errors are all handled.</li>
<li>There's a fallback, and a way to roll back.</li></ol>
""")

THEORY("Formulas", """
<table><tr><th>Quantity</th><th>Formula</th></tr>
<tr><td>Token F1</td><td>2·shared / (predicted + gold)</td></tr>
<tr><td>Nearest-rank percentile</td><td>sorted[⌈p/100·n⌉ − 1]</td></tr>
<tr><td>Weights memory</td><td>params × bits / 8</td></tr>
<tr><td>LoRA size</td><td>r·(d_in + d_out)</td></tr>
<tr><td>PSI</td><td>Σ (a − e)·ln(a / e)</td></tr>
<tr><td>Chance all steps succeed</td><td>pⁿ</td></tr></table>
""")

FAQ("When should I use an agent?", "<p>When the steps truly can't be known in advance. If you can write a fixed flow, a workflow is cheaper, faster and easier to test.</p>")
FAQ("What makes a good eval set?", "<p>Real inputs, including past failures and hard cases, with a check that can run automatically. Start small and add to it every time something fails.</p>")
FAQ("Why not report mean latency?", "<p>A long tail hides in the average. Percentiles such as p95 and p99 show what slow requests actually experience.</p>")
FAQ("Should I fine-tune?", "<p>Usually not first. Try prompts, examples, RAG and structured output. Fine-tuning suits stable style or cost problems where you have good data and an eval to prove it helped.</p>")
FAQ("Can prompt injection be fully prevented?", "<p>Not with current methods. Reduce the risk, and limit the damage with least privilege, approvals and validation in code.</p>")
