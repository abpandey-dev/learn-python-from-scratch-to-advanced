from lib import *
import numpy as np

LESSON("Basics", "What a vector database does", """
<p>A vector database stores embeddings with an id and metadata, and answers "which stored vectors are closest to this one?" fast — with filters, updates and deletes, at millions to billions of vectors. Exact search compares the query with every vector (fine up to ~100k); beyond that you use an <b>approximate nearest neighbour (ANN)</b> index.</p>
<ul>
<li><b>Metric</b>: cosine, dot product or Euclidean. With normalised vectors they rank the same; use what your embedding model was trained for.</li>
<li><b>Filters</b>: metadata conditions (tenant, language, date). Filter <i>during</i> search; filtering after a top-k search can leave you with too few results.</li>
<li><b>Writes</b>: upserts and deletes go to segments with tombstones that compaction cleans up.</li>
</ul>
""", practice=["Cosine, Dot or Euclidean?", "Post-Filtering Loses Results", "Evaluate Metadata Filters", "Upserts, Deletes and Compaction"])


@LD
def normalise_demo():
    docs = np.array([[0.9, 0.1], [3.0, 1.0]])
    q = np.array([1.0, 0.2])
    print("dot   :", docs @ q, "-> the long vector wins")
    unit = docs / np.linalg.norm(docs, axis=1, keepdims=True)
    print("cosine:", np.round(unit @ (q / np.linalg.norm(q)), 3), "-> direction wins")


LESSON("Core", "Inside ANN indexes", """
<table>
<tr><th>Index</th><th>How it works</th><th>Trade-off</th></tr>
<tr><td><b>HNSW</b></td><td>a layered graph; search walks greedily towards the query</td><td>fast, high recall, memory-hungry</td></tr>
<tr><td><b>IVF</b></td><td>cluster vectors; scan only the nearest <code>nprobe</code> clusters</td><td>tune nprobe for recall vs speed</td></tr>
<tr><td><b>PQ</b></td><td>split vectors into parts, store each as a codebook index</td><td>32–64× smaller, some accuracy lost</td></tr>
<tr><td><b>Scalar (int8)</b></td><td>store each number in one byte</td><td>4× smaller, tiny error</td></tr>
</table>
<p>Size the index before choosing hardware: 10 million 1536-dimension float32 vectors are ~61 GB before the graph. Big indexes are <b>sharded</b>: each shard returns its top k and a coordinator merges them.</p>
""", practice=["Search an IVF Index", "Greedy Search on an HNSW Graph", "Product Quantization", "Scalar Quantization to int8", "How Much Memory Will the Index Need?", "Search Across Shards"])

LESSON("Core", "Vector search in practice", """
<p>Start with what you already run. <b>pgvector</b> adds vectors to PostgreSQL, so tenant filters, joins and transactions just work; dedicated stores (Qdrant, Weaviate, Milvus, Pinecone) add scale and features; <b>Chroma</b> and <b>FAISS</b> are great for prototypes and in-process search.</p>
<pre><code class="py"># pgvector
SELECT id, body, 1 - (embedding &lt;=&gt; :q) AS similarity
FROM chunks WHERE tenant = :tenant
ORDER BY embedding &lt;=&gt; :q LIMIT 5;

# Qdrant
from qdrant_client import QdrantClient, models
client = QdrantClient(":memory:")
client.create_collection("docs", vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE))
client.upsert("docs", points=[models.PointStruct(id=1, vector=v, payload={"lang": "en"})])
client.query_points("docs", query=q, limit=5,
    query_filter=models.Filter(must=[models.FieldCondition(key="lang", match=models.MatchValue(value="en"))]))

# Chroma
import chromadb
col = chromadb.Client().create_collection("docs")
col.add(ids=["c1"], documents=["refund policy"], metadatas=[{"lang": "en"}])
col.query(query_texts=["how do refunds work"], n_results=3, where={"lang": "en"})</code></pre>
<p>Combine keyword and vector scores (<b>hybrid search</b>) for names, codes and rare words; cache embeddings by model + text hash; and plan model migrations as a backfill into a new index, then a switch.</p>
""", practice=["Vector Search in SQL", "Hybrid Search With a Weighted Blend", "Cache Embeddings", "Plan an Embedding Model Migration", "A Semantic Cache for LLM Answers", "Choose a Vector Store"])

LESSON("Advanced", "The same ideas in LangChain and LlamaIndex", """
<p>Frameworks package these pieces — loaders, splitters, embeddings, vector stores, retrievers, prompts, models and parsers — behind common interfaces, so you can swap providers. Everything in this course maps onto them:</p>
<pre><code class="py"># LangChain (LCEL): steps composed with |
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_anthropic import ChatAnthropic

chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
store = Chroma.from_documents(chunks, embeddings)                  # or PGVector, Qdrant…
retriever = store.as_retriever(search_type="similarity_score_threshold",
                               search_kwargs={"k": 4, "score_threshold": 0.75})
prompt = ChatPromptTemplate.from_template("Use only this context:\\n{context}\\n\\nQuestion: {question}")
chain = ({"context": retriever, "question": RunnablePassthrough()}
         | prompt | ChatAnthropic(model="claude-sonnet-5-5") | StrOutputParser())
chain.invoke("How long do refunds take?")

# LlamaIndex: index → query engine
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
index = VectorStoreIndex.from_documents(SimpleDirectoryReader("docs").load_data())
index.as_query_engine(similarity_top_k=4).query("How long do refunds take?")</code></pre>
<p><b>When to use one:</b> frameworks speed up prototypes and give many integrations; for production paths, many teams keep the core loop in plain code (as this course does) and use framework pieces where they help. Either way, interviewers expect you to explain what happens inside — which is what the questions here practise.</p>
""", practice=["Compose a Chain Like LangChain", "Split Text Recursively", "Fill a Prompt Template Safely", "A Retriever With a Score Threshold"])
