from lib import *

THEORY("Logs, metrics and traces", """
<table>
<tr><th>Signal</th><th>Answers</th><th>Tools</th></tr>
<tr><td>Logs</td><td>what happened to this request?</td><td>logging, structlog → Loki, ELK, CloudWatch</td></tr>
<tr><td>Metrics</td><td>how is the system doing overall?</td><td>Prometheus, Grafana, Datadog</td></tr>
<tr><td>Traces</td><td>where did the time go across services?</td><td>OpenTelemetry → Jaeger, Tempo</td></tr>
<tr><td>Errors</td><td>which bugs hit the most users?</td><td>Sentry</td></tr>
</table>
""")

THEORY("Which level?", """
<table>
<tr><th>Level</th><th>Use for</th></tr>
<tr><td>DEBUG</td><td>details for developers, off in production</td></tr>
<tr><td>INFO</td><td>normal events worth recording (startup, order placed)</td></tr>
<tr><td>WARNING</td><td>something odd but handled (retry, fallback)</td></tr>
<tr><td>ERROR</td><td>an operation failed</td></tr>
<tr><td>CRITICAL</td><td>the service can't continue</td></tr>
</table>
""")

FAQ("Why not use print for debugging production code?", "<p>print has no levels, timestamps or context, can't be filtered or routed, and is easy to leave behind. Logging can be switched per module and sent to a central system.</p>")
FAQ("What should you never log?", "<p>Passwords, tokens, API keys, full card numbers and unnecessary personal data. Redact at the source, because logs are copied to many systems.</p>")
FAQ("Counter vs gauge vs histogram?", "<p>Counters only increase (requests, errors) and are graphed as rates; gauges go up and down (memory, queue size); histograms record distributions so you can estimate percentiles.</p>")
FAQ("What's a correlation (request) id?", "<p>A unique id created at the edge and passed through every service and log line for that request, so you can reconstruct its full path when debugging.</p>")
FAQ("Which errors should you retry?", "<p>Transient ones: timeouts, connection resets, 429 and 503 responses. Never retry validation errors or non-idempotent operations without an idempotency key.</p>")
FAQ("How do you avoid alert fatigue?", "<p>Alert on user-facing symptoms with SLO burn rates, group related alerts, use cooldowns, and route warnings to tickets rather than pages.</p>")
