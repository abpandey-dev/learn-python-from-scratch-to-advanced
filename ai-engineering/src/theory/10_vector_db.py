from lib import *

THEORY("Choosing a vector store", """
<table>
<tr><th>Option</th><th>Best for</th></tr>
<tr><td>pgvector</td><td>already on Postgres, up to tens of millions of vectors, relational filters and joins</td></tr>
<tr><td>Qdrant / Weaviate / Milvus</td><td>large scale, rich filtering, hybrid search, self-hosted or cloud</td></tr>
<tr><td>Pinecone and other managed services</td><td>no operations, pay per use</td></tr>
<tr><td>Chroma</td><td>prototypes and notebooks</td></tr>
<tr><td>FAISS</td><td>a fast in-process library, no server, no metadata store</td></tr>
<tr><td>DuckDB / LanceDB / OpenSearch</td><td>analytics, embedded files, or adding vectors to existing search</td></tr>
</table>
""")

THEORY("HNSW parameters", """
<ul>
<li><code>M</code> — links per node: more links, better recall, more memory.</li>
<li><code>ef_construction</code> — effort while building: slower builds, better graphs.</li>
<li><code>ef_search</code> — candidates explored per query: the main recall-vs-latency dial at query time.</li>
</ul>
""")

FAQ("Why not just use NumPy for vector search?", "<p>Exact search is O(n·d) per query — fine for thousands of vectors, too slow for millions at high QPS. Databases add ANN indexes, filtering, persistence, updates, replication and access control.</p>")
FAQ("What's the difference between pre- and post-filtering?", "<p>Post-filtering searches first and then drops non-matching results, which can leave fewer than k or none. Pre- or in-search filtering applies the condition during the search so you still get k matches.</p>")
FAQ("How do you measure an ANN index?", "<p>Recall@k against exact search on a sample of real queries, plus latency percentiles and memory. Tune ef_search or nprobe until recall is good enough for your RAG evaluation.</p>")
FAQ("How do you change embedding models?", "<p>Re-embed everything into a new index (vectors from different models aren't comparable), dual-write new documents during the backfill, evaluate retrieval on both, then switch reads and delete the old index.</p>")
FAQ("What is a semantic cache?", "<p>A cache keyed by query embeddings: a new question close enough to a previous one reuses its answer. It saves money and latency, but the threshold must be tuned — too loose returns wrong answers.</p>")
FAQ("Should you use LangChain or LlamaIndex?", "<p>They're useful for prototypes and integrations. Know what each abstraction does underneath — chunking, retrieval, prompts, parsing — so you can debug it or replace it with plain code when you need control.</p>")
