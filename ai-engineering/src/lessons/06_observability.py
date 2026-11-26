from lib import *

LESSON("Basics", "Why AI apps need tracing", """
<p>When an AI feature gives a bad answer, the cause could be the retrieval, a tool that failed, a prompt change, the model, or a context that overflowed. A <b>trace</b> records one request end to end as a tree of <b>spans</b> — each LLM call, tool call and retrieval, with its timing, inputs, outputs, tokens and errors. Without traces, agents are black boxes.</p>
<pre><code class="text">chat_request            4.2 s
  retrieve              0.5 s
  llm_call (big)        2.2 s   6,000 in / 400 out tokens
    tool:search         0.6 s
  llm_call (small)      1.1 s</code></pre>
<p>Use standard formats (OpenTelemetry with GenAI attribute names) so any backend — Langfuse, LangSmith, Arize Phoenix, Datadog — can read them, and give every span in a request the same trace id, including across agents.</p>
""", practice=["Draw the Trace Tree", "Standard Attributes for an LLM Span", "Replay a Conversation From Events"])

LESSON("Core", "Reading traces: time, cost and errors", """
<ul>
<li><b>Self time</b> (a span's duration minus its children's) shows where time is really spent, without counting nested work twice.</li>
<li><b>Cost per trace</b>: add up input and output tokens per model. Roll it up per feature, per customer and per day — cost surprises usually come from one feature or one runaway agent.</li>
<li><b>Error rates per span type</b>: tool timeouts, malformed JSON, refusals, rate-limit errors.</li>
</ul>
<p>Store everything for errors, and sample the rest deterministically (by hashing the trace id) to control storage cost. Redact secrets and personal data <b>before</b> logs are written.</p>
""", practice=["Where Did the Time Go?", "Which Step Type Eats the Time?", "What Did This Request Cost?", "Cost and Errors per Feature", "Which Traces to Keep?", "Never Log Secrets"])

LESSON("Core", "Evals: offline tests for AI features", """
<p>An <b>eval</b> is a test suite for model behaviour: a set of inputs, and a way to score outputs. Build the set from real logged traffic, stratified so rare but important cases are represented, and add every bug you fix as a new case.</p>
<table>
<tr><th>Scorer</th><th>Good for</th></tr>
<tr><td>Exact match / token F1</td><td>short factual answers</td></tr>
<tr><td>Code checks (JSON valid, tests pass, SQL runs)</td><td>structured output, code</td></tr>
<tr><td>LLM-as-judge with a rubric</td><td>open-ended quality: correctness, grounding, tone</td></tr>
<tr><td>Pairwise judge (A vs B)</td><td>comparing two prompts or models</td></tr>
<tr><td>Human review</td><td>calibrating everything above</td></tr>
</table>
<p>Run evals on every prompt or model change and <b>gate releases</b>: ship only if the average doesn't drop and no important case regresses.</p>
""", practice=["Token F1 Against a Reference", "Build a Balanced Eval Set", "Gate the Release on Regressions", "Weighted Rubric Score"])

LESSON("Core", "LLM-as-judge, done carefully", """
<p>Judges are powerful and biased. Make them reliable:</p>
<ul>
<li><b>Specific rubric</b>: one criterion per question ("Is every claim supported by the context?"), a small scale, and examples of each score.</li>
<li><b>Structured output</b>: ask for JSON with a score and a reason; parse defensively.</li>
<li><b>Calibrate against humans</b>: label 50–100 cases yourself and check agreement with Cohen's kappa (above about 0.6 is usually workable).</li>
<li><b>Position bias</b>: in A-vs-B comparisons, judges favour the first answer. Judge both orders and count only consistent wins.</li>
<li><b>Grounding checks</b>: score whether each sentence of the answer is supported by the retrieved context — the main defence against hallucinated policies.</li>
</ul>
""", practice=["Parse the Judge's Verdict", "Does the Judge Agree With Humans?", "Pairwise Comparison Without Position Bias", "Is the Answer Grounded?"])

LESSON("Advanced", "Monitoring in production", """
<p>Offline evals don't see everything users do. In production, watch:</p>
<ul>
<li><b>Quality signals</b>: thumbs up/down, retries, conversations abandoned, escalations to humans — per prompt version.</li>
<li><b>Online evals</b>: run cheap judges on a sample of live traffic and alert when the rolling average drops.</li>
<li><b>Security</b>: flag likely prompt-injection attempts (in user input <i>and</i> in tool outputs like fetched web pages) and review them.</li>
<li><b>Cost and latency</b> per feature, with budgets and alerts.</li>
</ul>
<p>The loop that makes AI products improve: trace → find failures → add them to the eval set → fix → eval → ship → monitor.</p>
""", practice=["Thumbs Up Rate per Prompt Version", "Alert When Quality Slips", "Flag Prompt-Injection Attempts"])
