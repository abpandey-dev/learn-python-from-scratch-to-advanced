from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "From prompt engineering to context engineering", """
<p>A model only knows what is in its <b>context window</b> right now: the system prompt, tool definitions, retrieved documents, the conversation so far, tool results and the question. <b>Context engineering</b> is deciding what goes in, in what order, and what comes out as the task goes on.</p>
<p>More isn't better. Every token costs money and time, and models get worse at using information as the context fills up ("context rot"): details in the middle of a long context are easily missed. The goal is <b>the smallest set of high-signal tokens</b> that lets the model succeed.</p>
<p>Start by measuring. A rough estimate is 4 characters per English token; for real numbers use the provider's token-counting endpoint (Claude's API has one) and look at the <code>usage</code> field of every response.</p>
""", practice=["Estimate Tokens", "What's Eating the Window?"])

LESSON("Core", "Keeping long conversations inside the window", """
<p>Three tools, from simplest to smartest:</p>
<ol>
<li><b>Trim</b>: keep the system prompt and the most recent turns; drop the oldest. Cheap, but the agent forgets early decisions.</li>
<li><b>Clear tool results</b>: after the agent has used a big tool output (a file, a web page), replace it with a short placeholder. Usually the biggest win for agents. Some APIs, including Claude's, can do this automatically ("context editing").</li>
<li><b>Compact</b>: when the history passes a threshold, ask the model to summarise the oldest part (decisions made, open questions, file names) and continue from the summary. This is how long-running coding agents keep going for hours.</li>
</ol>
<p>Remember that every turn re-sends the whole history: without trimming, the total input over a conversation grows with the <b>square</b> of its length.</p>
""", practice=["Fit the History Into the Window", "Clear Old Tool Results", "Compact the Conversation", "The Hidden Cost of Long Chats"])


@LD
def growth_chart():
    turns = list(range(1, 41))
    plain, hist, compacted, total = [], 0, [], 0
    run = 0
    for t in turns:
        run += 2000 * t
        plain.append(run)
        hist = hist + 2000 if hist + 2000 <= 30000 else 5000
        total += hist
        compacted.append(total)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot(turns, plain, label="re-send everything")
    ax.plot(turns, compacted, label="compact at 30k")
    ax.set_xlabel("turn"); ax.set_ylabel("total input tokens"); ax.legend()


LESSON("Core", "Order matters: caching and 'lost in the middle'", """
<p><b>Prompt caching</b> lets the provider reuse the processed form of a prompt <i>prefix</i> it has seen recently. Cached input is billed at a small fraction of the normal price (on Claude, reads cost about 10% and writing the cache about 125%, with a minimum cacheable length), and it's faster. A cache hit needs the start of the prompt to be <b>byte-for-byte identical</b>, so put stable content first: system prompt, tool definitions, long documents — then per-user data — then the changing question.</p>
<pre><code class="py">client.messages.create(model="claude-opus-5-5", max_tokens=1000,
    system=[{"type": "text", "text": LONG_POLICY_DOC, "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": question}])</code></pre>
<p>Within the content, put the most important documents at the <b>start and end</b>, and restate the task at the end of a long prompt.</p>
""", practice=["Put Stable Content First", "What Does Caching Save?", "Is the Prefix Cached?", "Avoid 'Lost in the Middle'"])

LESSON("Core", "Choosing what to include", """
<ul>
<li><b>Budget by section</b>: give each part (system, memory, documents, history) a minimum and a share of what's left, so one huge section can't crowd out the rest.</li>
<li><b>Just-in-time retrieval</b>: instead of preloading every file, give the agent the list of names and tools to read what it needs — the way a person uses a file browser.</li>
<li><b>Dynamic few-shot examples</b>: pick the examples most similar to the current input instead of always the same ones.</li>
</ul>
""", practice=["Share the Budget Between Sections", "Load Files Just in Time", "Choose Few-Shot Examples", "Assemble the Final Prompt"])

LESSON("Advanced", "Memory that lasts beyond one conversation", """
<p>Long-term memory is context engineering across sessions. A typical pipeline:</p>
<ol>
<li><b>Extract</b> candidate facts from the conversation (usually with an LLM: "list stable facts about the user").</li>
<li><b>Consolidate</b> against the store: <b>ADD</b> new facts, <b>UPDATE</b> changed ones (keeping history), <b>SKIP</b> duplicates. Resolve conflicts by recency or by asking the user.</li>
<li><b>Recall</b> before answering: score memories by relevance to the question (keywords, embeddings or both) times a <b>recency decay</b>, and include only the top few.</li>
</ol>
<p>Tiers help: a short-term buffer of recent messages, and a long-term store for facts. For long tasks, agents also keep <b>notes files</b> (a to-do list, decisions made) that they re-read after compaction. Some APIs provide a memory tool so the model can create and edit such files itself.</p>
<p>Memory holds personal data: let users see and delete it, and never store secrets.</p>
""", practice=["Extract Facts to Remember", "Add, Update or Skip?", "Recall the Right Memories", "Newest Fact Wins", "Short-Term Buffer, Long-Term Store", "A Notes File the Agent Keeps"])
