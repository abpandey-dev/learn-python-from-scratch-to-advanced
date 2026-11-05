from lib import *

THEORY("Retrieval methods", """
<table><tr><th>Method</th><th>Strength</th><th>Weakness</th></tr>
<tr><td>BM25</td><td>exact terms, codes, names</td><td>misses synonyms</td></tr>
<tr><td>Vector search</td><td>meaning, paraphrases</td><td>can miss exact identifiers</td></tr>
<tr><td>Hybrid (RRF)</td><td>the best of both, usually</td><td>two systems to run</td></tr>
<tr><td>Re-ranker</td><td>accuracy</td><td>added latency and cost</td></tr></table>
""")

THEORY("Settings to test", """
<table><tr><th>Setting</th><th>Lower</th><th>Higher</th></tr>
<tr><td>Chunk size</td><td>precise, little context</td><td>more context, blurrier</td></tr>
<tr><td>Overlap</td><td>less storage</td><td>fewer split facts</td></tr>
<tr><td>k</td><td>cheap, could miss facts</td><td>better recall, more tokens</td></tr>
<tr><td>nprobe</td><td>fast</td><td>better recall</td></tr>
<tr><td>MMR λ</td><td>more diverse</td><td>more relevant</td></tr></table>
""")

THEORY("Do you need RAG?", """
<ul><li><b>Small, stable knowledge:</b> just put it in the prompt, with prompt caching.</li>
<li><b>Large or changing documents:</b> RAG.</li>
<li><b>Live data such as orders or stock:</b> a tool that queries the system directly.</li>
<li><b>Style or format changes:</b> prompts first, fine-tuning if needed. RAG won't help.</li></ul>
""")

FAQ("Why chunk at all?", "<p>Embedding a whole document blurs its topics, and passing it entire costs many tokens. Chunks let you retrieve just the relevant part.</p>")
FAQ("BM25 or embeddings?", "<p>Often both. Keywords catch exact terms, embeddings catch paraphrases. Reciprocal rank fusion combines them without comparable scores.</p>")
FAQ("What does a re-ranker do?", "<p>It re-scores a shortlist with a slower, more accurate model that reads the query and passage together.</p>")
FAQ("Which metric matters most?", "<p>Usually recall@k, since the model can't use what wasn't retrieved. Then use MRR or nDCG to judge ordering.</p>")
FAQ("How should permissions work in RAG?", "<p>Filter in the retrieval layer, so unauthorised text never reaches the prompt. Don't rely on instructions to the model.</p>")
