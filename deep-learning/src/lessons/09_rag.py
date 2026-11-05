from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "Why RAG exists", """
<p>Ask a model about your company's refund policy and it has two problems: it never saw your documents, and it may answer confidently anyway. Pasting all your documents into every prompt is too slow and expensive, and may not even fit.</p>
<p><b>Retrieval-augmented generation</b> looks up only the relevant pieces, and puts those in the prompt:</p>
<table><tr><th>When</th><th>Step</th><th>What happens</th></tr>
<tr><td rowspan="2">Ahead of time</td><td>Chunk</td><td>split documents into pieces</td></tr>
<tr><td>Index</td><td>store them for fast search</td></tr>
<tr><td rowspan="3">Per question</td><td>Retrieve</td><td>find the pieces matching the question</td></tr>
<tr><td>Assemble</td><td>put them in a prompt, with instructions</td></tr>
<tr><td>Generate</td><td>the model answers from them</td></tr></table>
<p>The demo runs this whole thing, except the final model call, with about ten lines of NumPy. The question "how long do refunds take" finds the refund policy using TF-IDF, and builds the prompt.</p>
<p><b>What RAG gives you:</b> current information without retraining, access to private data, answers that can cite sources, and an easy way to update (just re-index a document).</p>
<p><b>What it doesn't:</b> it's not a guarantee of truth. If retrieval misses the right passage, the model has nothing to work with. <b>Most bad RAG answers are retrieval failures</b>, so when debugging, look at what was retrieved first.</p>
""", practice=[])


@LD
def tiny_rag():
    documents = ["Refunds are processed within 5 business days of the return.",
                 "Standard shipping takes 3 to 7 days within the country.",
                 "You can change your password from the account settings page."]
    question = "how long do refunds take"
    split = [d.lower().replace(".", "").split() for d in documents]
    words = question.split()
    tf = np.array([[d.count(w) / len(d) for w in words] for d in split])
    idf = np.log(len(split) / np.maximum((tf > 0).sum(axis=0), 1))
    scores = tf @ idf
    print("scores:", scores.round(3))
    best = documents[int(scores.argmax())]
    print(f"[1] {best}\n\nQuestion: {question}\nAnswer using only the source. Cite it like [1].")


LESSON("Core", "Chunking: splitting documents well", """
<p>You retrieve chunks rather than whole documents, so chunk boundaries directly affect quality.</p>
<table><tr><th>Too small</th><th>Too large</th></tr>
<tr><td>loses context: "It costs $5." What does?</td><td>the embedding blurs many topics, and costs more tokens</td></tr></table>
<p><b>Fixed size:</b> a, b, c, d, e, f, g with size 3 gives abc, def, g. It's simple, but "The fee is / $5" can be split in half across two chunks, and then neither chunk answers the question.</p>
<p><b>Overlap</b> repeats the end of each chunk at the start of the next. With size 4 and overlap 2, a to h gives abcd, cdef, efgh. Each new chunk moves on by 4 − 2 = 2. The fact that spanned a boundary is now whole in some chunk. The price is more chunks to store: with overlap of half the size, nearly double.</p>
<p><b>Respect structure</b> where possible. Sentence-aware splitting of "One here. Two is here! Is three? Yes." with a 20-character limit gives:</p>
<ul><li>"One here."</li><li>"Two is here!"</li><li>"Is three? Yes."</li></ul>
<p>Good documents give more clues: headings, paragraphs, table rows, and functions in code. Add a title or section name to each chunk so it stands on its own.</p>
<p>There's no universal best size. Treat size and overlap as settings to test with the metrics at the end of this topic, on your own questions.</p>
""", practice=["Fixed-Size Chunks", "Chunks With Overlap", "Sentence-Aware Chunks"])


LESSON("Core", "Keyword search: from TF-IDF to BM25", """
<p>Keyword search is still excellent, particularly for exact terms: product codes, error messages, names.</p>
<p><b>TF-IDF</b> has a weakness: a word used 100 times scores 100 times higher than one used once. But a page that mentions "refund" 100 times isn't 100 times more about refunds.</p>
<p><b>BM25</b> fixes that with two changes, and it's the usual default:</p>
<p style="text-align:center"><b>score = Σ idf · tf·(k₁ + 1) / (tf + k₁·(1 − b + b·len/avg))</b></p>
<ul><li><b>Saturation (k₁ = 1.5):</b> repeats help less and less. See the chart.</li><li><b>Length normalisation (b = 0.75):</b> long documents contain more words by chance, so they're marked down.</li></ul>
<p><b>By hand.</b> Query "market", on a document of 5 words where it appears once. There are 4 documents, with average length 5.75, and 1 contains the word.</p>
<ol><li>idf = ln((4 − 1 + 0.5) / (1 + 0.5) + 1) = ln(3.333) = 1.2040</li>
<li>Length part = 1.5 · (0.25 + 0.75 · 5 / 5.75) = 1.3533</li>
<li>tf part = 1 · 2.5 / (1 + 1.3533) = 1.0623</li>
<li>Score = 1.2040 × 1.0623 = <b>1.279</b></li></ol>
<p>The weakness of keywords is synonyms. "How do I get my money back?" contains no word in "refund policy". That's what vector search is for.</p>
""", practice=["Rank by TF-IDF", "BM25 Score"])


@LD
def bm25_saturation():
    tf = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(tf, tf * 2.5 / (tf + 1.5), label="BM25 (average-length document)")
    ax.plot(tf[:11], tf[:11] * 0.25, label="linear growth, for comparison", linestyle="--")
    ax.axhline(2.5, color="gray", linewidth=0.7)
    ax.set_xlabel("times the word appears")
    ax.set_ylabel("tf part of the score")
    ax.legend(fontsize=7)


LESSON("Core", "Vector search", """
<p>An <b>embedding model</b> turns text into a vector so that similar meanings get nearby vectors, even with no shared words. To search, embed the question and find the closest stored vectors.</p>
<p><b>By hand</b> with query (1, 0.2), whose length is 1.0198:</p>
<table><tr><th>Vector</th><th>Dot</th><th>Length</th><th>Cosine</th></tr>
<tr><td>(1, 0)</td><td>1</td><td>1</td><td><b>0.9806</b></td></tr>
<tr><td>(1, 1)</td><td>1.2</td><td>1.4142</td><td><b>0.8321</b></td></tr>
<tr><td>(0, 1)</td><td>0.2</td><td>1</td><td>0.1961</td></tr></table>
<p>The top 2 are the first and third items in the index.</p>
<p><b>Use the same model</b> for documents and questions, or the vectors aren't comparable. Changing model means re-embedding everything.</p>
<p><b>Filter on metadata.</b> Similarity doesn't know about permissions, dates or teams. Among {a: hr 0.9, b: eng 0.7, c: eng 0.8}, an engineering user gets c, not the higher-scoring a. <b>For access control, filter in the retrieval layer</b>, so a user can't get text they're not allowed to read. Never rely on a prompt asking the model not to reveal it.</p>
<p>Brute-force search is simple and exact, and it's a matrix multiplication. It's fine for tens of thousands of chunks. Don't add a vector database until you need one.</p>
""", practice=["Vector Top-k", "Filter, Then Search"])


LESSON("Core", "Approximate search at scale", """
<p>With a billion vectors, comparing against all of them per question is too slow. <b>Approximate nearest-neighbour</b> indexes trade a little accuracy for a lot of speed.</p>
<p><b>IVF (inverted file)</b> is the easiest to understand:</p>
<ol><li>Cluster the vectors, for instance with k-means.</li><li>Store each vector in the list for its nearest centre.</li><li>For a query, find the closest <code>nprobe</code> centres, and search only their lists.</li></ol>
<p><b>By hand.</b> Vectors: 0: (0, 0), 1: (0, 1), 2: (10, 10), 3: (10, 11), 4: (5, 6). Centres (0, 0) and (10, 10). Query (4.5, 5).</p>
<ul><li>Vector 4 is at distance 6.40 from (10, 10), and 7.81 from (0, 0), so it's in the second list: {2, 3, 4}. The first list is {0, 1}.</li>
<li>The query is nearer the first centre (6.73 vs 7.43).</li>
<li><b>nprobe = 1:</b> searches {0, 1}, and returns vector 1, after 2 comparisons. <b>Wrong!</b> Vector 4 is the true nearest.</li>
<li><b>nprobe = 2:</b> searches everything, and returns 4, after 5 comparisons.</li></ul>
<p>That's the trade-off exactly: a query near a cluster's edge may have its true neighbour in the next cell. Raising <code>nprobe</code> buys accuracy with time.</p>
<p>The chart measures this on 5,000 clustered vectors, checked against exact search. Comparing against just 2.6% of them found the true nearest 93% of the time, and 6% found it every time in this run. Other methods exist, with HNSW (a layered graph) being a popular choice. Real data may be less neatly clustered than this synthetic set, so measure recall on your own vectors.</p>
""", practice=["An Approximate Index"])


@LD
def ivf_tradeoff():
    rng = np.random.default_rng(0)
    n, dim, clusters = 5000, 32, 50
    centres = rng.normal(size=(clusters, dim)) * 3
    data = centres[rng.integers(0, clusters, n)] + rng.normal(size=(n, dim))
    queries = centres[rng.integers(0, clusters, 100)] + rng.normal(size=(100, dim))
    found = data[rng.choice(n, clusters, replace=False)]
    for _ in range(5):
        owner = ((data[:, None] - found) ** 2).sum(axis=2).argmin(axis=1)
        found = np.array([data[owner == k].mean(axis=0) if (owner == k).any() else found[k] for k in range(clusters)])
    truth = [((data - q) ** 2).sum(axis=1).argmin() for q in queries]
    probes, recall, share = [1, 2, 3, 5, 10], [], []
    for nprobe in probes:
        hits, searched = 0, 0
        for q, answer in zip(queries, truth):
            lists = np.argsort(((found - q) ** 2).sum(axis=1))[:nprobe]
            members = np.flatnonzero(np.isin(owner, lists))
            searched += len(members)
            hits += members[((data[members] - q) ** 2).sum(axis=1).argmin()] == answer
        recall.append(hits / len(queries))
        share.append(searched / len(queries) / n)
    print("nprobe:", probes)
    print("recall:", np.round(recall, 2))
    print("share of data searched:", np.round(share, 3))
    fig, ax = plt.subplots(figsize=(4.6, 2.7))
    ax.plot(np.array(share) * 100, recall, "o-")
    ax.set_xlabel("% of vectors compared")
    ax.set_ylabel("recall of the true nearest")


LESSON("Core", "Hybrid search and re-ranking", """
<p>Keywords and vectors fail in different ways, so using both usually beats either alone. But how do you combine them? BM25 scores can be 12 while cosines are at most 1, so adding them is meaningless.</p>
<p><b>Reciprocal rank fusion</b> ignores scores and uses only positions: score = Σ 1 / (60 + rank).</p>
<p>With rankings [a, b, c] and [b, c, d]:</p>
<table><tr><th>Id</th><th>Calculation</th><th>Score</th></tr>
<tr><td>b</td><td>1/62 + 1/61</td><td><b>0.03252</b></td></tr>
<tr><td>c</td><td>1/63 + 1/62</td><td><b>0.03200</b></td></tr>
<tr><td>a</td><td>1/61</td><td>0.01639</td></tr>
<tr><td>d</td><td>1/63</td><td>0.01587</td></tr></table>
<p>Note that a was first in one list, but b and c win because both lists agree on them. The 60 keeps a single first place from dominating.</p>
<p><b>Re-ranking</b> adds a second stage. First-stage search is fast but rough, so fetch say 50 candidates, then re-score with a slower, more accurate model, such as a cross-encoder or an LLM, that reads the question and text together. Keep the top few. For candidates a, b, c, d scoring 0.1, 0.9, 0.4, 0.7, the top 2 are b and d.</p>
<table><tr><th>Stage</th><th>Candidates</th><th>Speed</th><th>Accuracy</th></tr>
<tr><td>Hybrid retrieval</td><td>millions → 50</td><td>fast</td><td>decent</td></tr>
<tr><td>Re-ranker</td><td>50 → 5</td><td>slow</td><td>good</td></tr>
<tr><td>LLM answer</td><td>5 → 1 answer</td><td>slowest</td><td>uses all context</td></tr></table>
""", practice=["Reciprocal Rank Fusion", "Re-Rank the Candidates"])


LESSON("Core", "Diversity and removing repeats", """
<p>Top-k has a quiet flaw: it may return five near-identical passages. You pay for all of them, and learn just one fact.</p>
<p><b>Maximal marginal relevance</b> picks items one at a time, balancing relevance against similarity to what's already chosen:</p>
<p style="text-align:center"><b>score = λ·relevance − (1 − λ)·(highest similarity to anything chosen)</b></p>
<p>Relevance is 0.9, 0.85, 0.5. Items 0 and 1 are near-duplicates (similarity 0.95), and item 2 is different (0.1). With λ = 0.5:</p>
<ul><li><b>Round 1:</b> nothing is chosen yet, so pick the most relevant: item 0.</li>
<li><b>Round 2, item 1:</b> 0.5·0.85 − 0.5·0.95 = <b>−0.05</b>.</li>
<li><b>Round 2, item 2:</b> 0.5·0.5 − 0.5·0.1 = <b>+0.20</b>. Picked.</li></ul>
<p>Result: [0, 2]. With λ = 1, it's plain relevance, giving [0, 1].</p>
<p><b>Remove near-duplicates</b> using Jaccard overlap: shared words ÷ all distinct words. "the cat sat" and "the cat sat down" share 3 of 4 words: 0.75. At a 0.7 limit, the second is dropped. "stocks fell today" shares none and stays.</p>
<p>Overlapping chunks cause exactly this kind of repeat, so it's a good idea to dedupe after using overlap.</p>
""", practice=["Maximal Marginal Relevance", "Remove Near-Duplicates"])


LESSON("Core", "Assembling the prompt", """
<p>The last mile matters too. A good RAG prompt gives numbered sources, the question, and clear rules:</p>
<pre><code class="py">[1] Paris is in France.
[2] It has the Louvre.

Question: Where is Paris?
Answer using only the sources. Cite them like [1].</code></pre>
<p><b>Fit the budget.</b> With sizes 500, 800, 300, 400 and a budget of 1,000: keep 500; 800 doesn't fit; keep 300 (800 in total); 400 doesn't fit. Result: chunks 0 and 2.</p>
<p><b>Allow "I don't know".</b> If the best score is weak, don't force an answer. With threshold 0.5, scores 0.8, 0.4, 0.6 keep two chunks. A single score of 0.3 returns "no_answer", which beats a confident invention. Tell the model to say so as well, if the sources don't contain the answer. Thresholds differ per embedding model, so set them from your own data.</p>
<p><b>Check citations in code.</b> Models can cite sources that don't exist. For "Paris is in France [1]. It is big [2][1]. Also [7]." with 2 sources: valid are [1, 2], and <b>invalid is [7]</b>. A valid number doesn't prove that the source says it, though. That takes evaluation or human checks.</p>
<p><b>Retrieved text is untrusted</b>: a web page or document could contain instructions aimed at your model. Keep it in tags, and don't give the model powerful tools in the same task without checks.</p>
""", practice=["Fit Chunks Into the Budget", "Say When You Don't Know", "Build the Prompt With Sources", "Check the Citations"])


LESSON("Advanced", "Measuring retrieval", """
<p>Measure retrieval separately from the answer. You need a test set of questions with known relevant chunks, ideally from real user questions.</p>
<p>Retrieved: a, b, c, d. Relevant: b, d, e.</p>
<table><tr><th>Metric</th><th>Question</th><th>k = 2</th><th>k = 4</th></tr>
<tr><td>Recall@k</td><td>How much of what matters did we find?</td><td>1/3 = 0.333</td><td>2/3 = 0.667</td></tr>
<tr><td>Precision@k</td><td>How much of what we returned matters?</td><td>1/2 = 0.5</td><td>2/4 = 0.5</td></tr></table>
<p>For RAG, <b>recall usually matters most</b>. If a passage isn't retrieved, the model can't use it; a few extras are less harmful.</p>
<p><b>MRR</b> rewards a high first hit. Three queries, with the first relevant result at rank 1, rank 3 and nowhere: (1 + 1/3 + 0) / 3 = <b>0.4444</b>.</p>
<p><b>nDCG</b> handles graded relevance (2 = perfect, 1 = useful, 0 = no), and rewards putting the best first, by dividing each relevance by log₂(position + 1). For relevances 0, 1, 2:</p>
<ul><li>DCG = 0/1 + 1/1.585 + 2/2 = 1.631</li><li>Ideal order 2, 1, 0: 2/1 + 1/1.585 + 0 = 2.631</li><li>nDCG = 1.631 / 2.631 = <b>0.620</b></li></ul>
<p><b>A debugging order for a bad answer:</b></p>
<ol><li>Is the fact in your documents at all?</li><li>Was it split badly during chunking?</li><li>Was it retrieved? Check recall.</li><li>Did it survive re-ranking and the budget?</li><li>Did the model use it correctly?</li></ol>
<p>Change one thing at a time, and re-measure.</p>
""", practice=["Recall@k", "Precision@k", "Mean Reciprocal Rank", "nDCG@k"])
