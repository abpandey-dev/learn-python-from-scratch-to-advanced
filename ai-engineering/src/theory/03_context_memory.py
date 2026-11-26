from lib import *

THEORY("What's in the window", """
<table>
<tr><th>Part</th><th>Changes</th><th>Typical lever</th></tr>
<tr><td>System prompt</td><td>rarely</td><td>keep it clear and short; cache it</td></tr>
<tr><td>Tool definitions</td><td>rarely</td><td>fewer, well-described tools; cache them</td></tr>
<tr><td>Documents / retrieval</td><td>per request</td><td>retrieve less but better; order by importance</td></tr>
<tr><td>Memory</td><td>per user</td><td>recall only the top few facts</td></tr>
<tr><td>History</td><td>every turn</td><td>trim, clear tool results, compact</td></tr>
<tr><td>Question</td><td>every turn</td><td>put it last</td></tr>
</table>
""")

THEORY("Kinds of memory", """
<ul>
<li><b>Working memory</b>: the context window itself.</li>
<li><b>Short-term</b>: recent turns of this conversation.</li>
<li><b>Long-term semantic</b>: stable facts and preferences ("prefers email").</li>
<li><b>Episodic</b>: past events and conversations, retrievable later.</li>
<li><b>Procedural</b>: learned instructions and notes about how to do tasks.</li>
</ul>
""")

FAQ("Why not just use the biggest context window?", "<p>Cost and latency grow with input size, and models use information less reliably as the context fills, especially in the middle. Curated, smaller context usually gives better answers.</p>")
FAQ("How does prompt caching work and how do you get hits?", "<p>The provider stores the processed prefix of a recent prompt and reuses it if a new prompt starts with exactly the same content. Put stable content first and the changing parts last, and keep the prefix byte-identical.</p>")
FAQ("Trimming vs compaction?", "<p>Trimming drops old turns and loses their information. Compaction replaces them with a summary, keeping decisions and facts at a fraction of the tokens.</p>")
FAQ("How would you build long-term memory for an assistant?", "<p>Extract facts after each conversation, consolidate them (add, update with history, skip duplicates), store them with timestamps, and recall the most relevant and recent few into the prompt. Let users view and delete them.</p>")
FAQ("What is 'lost in the middle'?", "<p>Models tend to use information at the start and end of a long context better than in the middle, so put the most important material at the edges.</p>")
FAQ("What is just-in-time context?", "<p>Giving the agent references (file names, IDs) and tools to fetch details when needed, instead of loading everything up front.</p>")
