from lib import *

THEORY("Production architecture of an AI feature", """
<table>
<tr><th>Layer</th><th>Responsibilities</th></tr>
<tr><td>Client</td><td>streaming UI, cancel button, feedback buttons</td></tr>
<tr><td>API backend</td><td>auth, input guardrails, budgets, rate limits, caching, streaming relay</td></tr>
<tr><td>Orchestration</td><td>prompts (versioned), retrieval, tools/MCP, agents</td></tr>
<tr><td>Model gateway</td><td>provider SDKs, retries, fallbacks, routing between models</td></tr>
<tr><td>Observability</td><td>traces, costs, evals, alerts</td></tr>
</table>
""")

THEORY("Claude streaming events", """
<ul>
<li><code>message_start</code> — message metadata</li>
<li><code>content_block_start</code> / <code>content_block_stop</code> — each text, thinking or tool-use block</li>
<li><code>content_block_delta</code> — <code>text_delta</code>, <code>input_json_delta</code> (tool arguments), <code>thinking_delta</code></li>
<li><code>message_delta</code> — stop reason and final usage</li>
<li><code>message_stop</code>; <code>ping</code> events keep the connection alive; <code>error</code> events report problems mid-stream</li>
</ul>
""")

FAQ("Why stream responses?", "<p>Users see the first words in well under a second instead of waiting for the full answer, perceived latency drops sharply, and they can stop a bad answer early.</p>")
FAQ("Which API errors should you retry?", "<p>Rate limits (429), server errors (500, 502, 503, 504) and overload (529), with exponential backoff and jitter, honouring retry-after. Not client errors like 400 or 401 — those need a fixed request.</p>")
FAQ("How do coding agents edit files safely?", "<p>By replacing exact, unique snippets or applying diffs, checking for conflicts, running tests after each change, and running commands in a sandbox with allow- and deny-lists.</p>")
FAQ("What guardrails would you put around a customer-facing chatbot?", "<p>Input checks (length, scope, injection), output checks (PII, secrets, format, grounding), per-user budgets and rate limits, logging with redaction, and human escalation for sensitive cases.</p>")
FAQ("What is a semantic cache?", "<p>A cache keyed by the meaning of a request (usually an embedding) so paraphrased repeat questions reuse a stored answer, saving cost and latency. It needs expiry and care with personalised answers.</p>")
FAQ("How do you estimate the cost of an AI feature?", "<p>Requests per month × (input tokens × input price + output tokens × output price), then adjust for caching, routing to smaller models and batch discounts; add a margin and set alerts.</p>")
