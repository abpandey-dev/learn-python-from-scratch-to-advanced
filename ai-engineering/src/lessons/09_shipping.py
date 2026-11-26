from lib import *

LESSON("Basics", "Streaming: show words as they're written", """
<p>A long answer can take 10–30 seconds. Streaming shows the first words in under a second, which makes the product feel fast. The API sends <b>server-sent events</b>: <code>message_start</code>, then <code>content_block_delta</code> events carrying text pieces (<code>text_delta</code>) or tool-argument fragments (<code>input_json_delta</code>), then <code>message_stop</code>.</p>
<pre><code class="py">with client.messages.stream(model="claude-opus-5-5", max_tokens=1024, messages=messages) as stream:
    for text in stream.text_stream:
        yield f"data: {json.dumps({'text': text})}\\n\\n"      # relay to the browser
    final = stream.get_final_message()                         # usage, stop reason, full content</code></pre>
<p>Your backend relays chunks to the browser (FastAPI <code>StreamingResponse</code> with <code>text/event-stream</code>; the browser reads them with <code>EventSource</code> or <code>fetch</code>). Measure <b>time to first token</b> and tokens per second — users feel those, not total time.</p>
""", practice=["Parse a Server-Sent Event Stream", "Assemble Streamed Text", "Stream a Tool Call's Arguments", "Measure Streaming Speed", "Send Chunks to the Browser"])

LESSON("Core", "Reliable outputs and reliable calls", """
<ul>
<li><b>Structured output</b>: when code consumes the answer, use the API's structured-output or tool-use features with a JSON schema, validate the result, and keep a forgiving parser plus one retry as a safety net.</li>
<li><b>Errors</b>: retry rate limits (429), server errors (5xx) and overload (529) with exponential backoff, honouring any <code>retry-after</code> header. Don't retry 400-level errors — fix the request. The official SDKs already retry some of these for you.</li>
<li><b>Fallbacks</b>: a secondary model or provider for when the primary keeps failing.</li>
<li><b>Persistence</b>: store conversations (JSON Lines works well) so users can resume and you can debug.</li>
</ul>
""", practice=["Rescue JSON From a Reply", "What to Do About an API Error", "Save and Restore a Conversation"])

LESSON("Core", "How coding agents work", """
<p>Coding agents (Claude Code and others) are agents whose tools are a file system and a shell. Their reliability comes from a few disciplines:</p>
<ul>
<li><b>Precise edits</b>: replace an exact, <b>unique</b> snippet (or apply a diff) rather than rewriting whole files; refuse ambiguous edits.</li>
<li><b>The test–fix loop</b>: run the tests, read failures, edit, re-run — and stop after a few failed attempts instead of thrashing.</li>
<li><b>Sandboxing</b>: run commands in a container or with an allow-list; deny destructive patterns (<code>rm -rf /</code>, piping downloads into a shell, force-pushing) and ask a human for anything unusual.</li>
<li><b>Context</b>: project instructions files, just-in-time file reading, and compaction for long sessions (see Context Engineering).</li>
</ul>
<p><b>Computer-use</b> agents control a desktop through screenshots and mouse/keyboard actions. Screenshots are scaled, so coordinates must be mapped back to the real screen and checked against its bounds.</p>
""", practice=["A Safe Edit Tool", "Apply a Diff Hunk", "The Test–Fix Loop", "Which Shell Commands May the Agent Run?", "Scale a Computer-Use Click"])

LESSON("Core", "Guardrails around the model", """
<pre><code class="text">user input → input guardrail → (cache?) → model → output guardrail → user
                  ↓ reject                              ↓ redact / block</code></pre>
<ul>
<li><b>Input</b>: length limits, topics you don't serve, obvious injection attempts.</li>
<li><b>Output</b>: no personal data, no leaked system prompt or secrets, valid format; for high-stakes answers, grounding checks.</li>
<li><b>Budgets</b>: tokens per user per day, so one user (or a bug) can't run up the bill.</li>
<li><b>Semantic caching</b>: answer repeated questions from a cache keyed by meaning, not exact text.</li>
</ul>
<p>Guardrails reduce risk; they don't remove it. Keep secrets out of prompts entirely when you can.</p>
""", practice=["Input Guardrail", "Output Guardrail", "A Daily Budget per User", "A Semantic Cache"])

LESSON("Advanced", "Launching and running an AI feature", """
<ul>
<li><b>Version prompts like code</b> and roll new versions out gradually (by hashing user ids), watching evals and feedback.</li>
<li><b>Estimate cost before launch</b>: users × requests × tokens × price, then the effect of caching and smaller models.</li>
<li><b>Launch checklist</b>: evals pass, guardrails on, rate limits and budgets set, cost alerts, tracing, a fallback model, a privacy review — and a way to turn the feature off.</li>
</ul>
<p>The rest of this course is the toolkit behind each line of that checklist: MCP for tools, orchestration for agents, context engineering for quality and cost, reasoning where it pays, serving if you self-host, observability and evals to know it works, fine-tuning when prompting isn't enough, and multimodal inputs.</p>
""", practice=["Roll Out a New Prompt Version", "What Will This Feature Cost per Month?", "Ready to Launch?"])
