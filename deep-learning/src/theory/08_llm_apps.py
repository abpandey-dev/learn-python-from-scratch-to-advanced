from lib import *

THEORY("Building blocks", """
<table><tr><th>Need</th><th>Technique</th></tr>
<tr><td>Consistent format</td><td>structured output, few-shot examples</td></tr>
<tr><td>Up-to-date or private facts</td><td>retrieval (RAG), tools</td></tr>
<tr><td>Actions</td><td>tools, with checks in your code</td></tr>
<tr><td>Long conversations</td><td>trimming, summaries</td></tr>
<tr><td>Lower cost</td><td>prompt caching, shorter output, batching, a smaller model</td></tr>
<tr><td>Reliability</td><td>retries, validation, fallbacks</td></tr>
<tr><td>Knowing it works</td><td>evaluation (see the last topic)</td></tr></table>
""")

THEORY("A production checklist", """
<ul><li>API keys are kept on the server, not in client code.</li>
<li>Every stop reason is handled, including <code>max_tokens</code> and <code>refusal</code>.</li>
<li>Output is validated before use, and never directly executed.</li>
<li>Retries only cover retryable errors, and don't repeat unsafe actions.</li>
<li>Loops have a step limit, and costs are monitored.</li>
<li>Outside text is treated as untrusted.</li>
<li>Inputs, outputs, tokens and latency are logged, respecting privacy.</li></ul>
""")

THEORY("Start simple", """
<table><tr><th>Level</th><th>Use when</th></tr>
<tr><td>Single call</td><td>classification, summarising, extraction, Q&amp;A</td></tr>
<tr><td>Workflow</td><td>fixed steps controlled by your code</td></tr>
<tr><td>Agent</td><td>the steps genuinely can't be known in advance</td></tr></table>
<p>Move to the next level only when the simpler one can't do the job. More autonomy brings more cost, more latency and more ways to fail.</p>
""")

FAQ("Does the model remember my earlier messages?", "<p>No. APIs are generally stateless, so you resend the conversation each time, and pay for it as input.</p>")
FAQ("Does the model run my tools?", "<p>No. It asks for a tool with some inputs. Your code decides whether to run it and returns the result.</p>")
FAQ("Which errors should be retried?", "<p>429 and 5xx errors, with backoff and jitter. Not 400, 401 or 403, which will fail again until something changes.</p>")
FAQ("How does prompt caching differ from a response cache?", "<p>A response cache skips the model when the whole request repeats. A prompt cache still calls the model, but reuses work for a matching prefix.</p>")
FAQ("How do I defend against prompt injection?", "<p>There's no complete fix. Separate untrusted text, give tools the least permissions needed, check actions in code, and require a person's approval for risky ones.</p>")
