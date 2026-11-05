from lib import *
import math
import re
import numpy as np


TOPIC(
    id="rag", title="RAG & Retrieval", glyph="🔍→",
    blurb="Answering from your own documents: chunking, TF-IDF and BM25, vector search, approximate indexes, fusion, MMR, re-ranking, citations and measuring retrieval with recall, MRR and nDCG.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">chunks = split(documents)
index = embed(chunks)                      # once, ahead of time
hits = top_k(embed(question), index)       # at question time
prompt = instructions + hits + question
answer = call_model(prompt)</code></pre>
""")

DOCS = [["the", "cat", "sat", "on", "the", "mat"],
        ["dogs", "chase", "cats", "in", "the", "park"],
        ["the", "stock", "market", "fell", "today"],
        ["cats", "and", "dogs", "are", "popular", "pets"]]


Q(None, "Fixed-Size Chunks", "Easy", "The simplest splitter",
  "Split tokens into chunks of the given size. The last may be shorter.",
  [((list("abcdefg"), 3), [['a', 'b', 'c'], ['d', 'e', 'f'], ['g']])],
  ("Slices in a loop.", "O(n)", "O(n)"),
  ("A comprehension with a step.", "O(n)", "O(n)"),
  names=["tokens", "size"])


@B
def fixed_chunks(tokens, size):
    out, i = [], 0
    while i < len(tokens):
        out.append(tokens[i:i + size])
        i += size
    return out


@O
def fixed_chunks(tokens, size):
    return [tokens[i:i + size] for i in range(0, len(tokens), size)]


Q(None, "Chunks With Overlap", "Easy", "Don't cut facts in half",
  "Chunks of the given size, each starting (size − overlap) after the previous. Stop once a chunk reaches the end.",
  [((list("abcdefgh"), 4, 2), [['a', 'b', 'c', 'd'], ['c', 'd', 'e', 'f'], ['e', 'f', 'g', 'h']]), ((list("abcde"), 3, 1), [['a', 'b', 'c'], ['c', 'd', 'e']])],
  ("A while loop with a break.", "O(n)", "O(n·s)"),
  ("Work out how many chunks first.", "O(n)", "O(n·s)"),
  names=["tokens", "size", "overlap"])


@B
def overlap_chunks(tokens, size, overlap):
    out, i = [], 0
    while True:
        out.append(tokens[i:i + size])
        if i + size >= len(tokens):
            break
        i += size - overlap
    return out


@O
def overlap_chunks(tokens, size, overlap):
    step = size - overlap
    n = max(0, math.ceil((len(tokens) - size) / step)) + 1
    return [tokens[i * step:i * step + size] for i in range(n)]


Q(None, "Sentence-Aware Chunks", "Medium", "Keep sentences whole",
  "Split text into sentences, then greedily join them up to max_chars (joined with a space). A sentence is never split.",
  [(("One here. Two is here! Is three? Yes.", 20), ['One here.', 'Two is here!', 'Is three? Yes.'])],
  ("Scan for ending punctuation, then fill chunks.", "O(n)", "O(n)"),
  ("A regular expression to split, then the same greedy fill.", "O(n)", "O(n)"),
  names=["text", "max_chars"])


@B
def sentence_chunks(text, max_chars):
    sentences, current = [], ""
    for ch in text:
        current += ch
        if ch in ".!?":
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    chunks, chunk = [], ""
    for s in sentences:
        if chunk and len(chunk) + 1 + len(s) > max_chars:
            chunks.append(chunk)
            chunk = s
        else:
            chunk = chunk + " " + s if chunk else s
    if chunk:
        chunks.append(chunk)
    return chunks


@O
def sentence_chunks(text, max_chars):
    chunks = []
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        if chunks and len(chunks[-1]) + 1 + len(s) <= max_chars:
            chunks[-1] += " " + s
        else:
            chunks.append(s)
    return chunks


Q(None, "Rank by TF-IDF", "Medium", "Keyword search",
  "Score each doc as Σ over query words of (count / doc length) × ln(N / df), skipping words in no document. Return doc indices best first, keeping those with a score above 0.",
  [((DOCS, ["cats", "dogs"]), [1, 3]), ((DOCS, ["market", "the"]), [2, 0, 1])],
  ("Nested loops per word and document.", "O(q·total)", "O(n)"),
  ("Count words once in a table, then use array operations.", "O(total + q·n)", "O(n·V)"),
  names=["docs", "query"])


@B
def tfidf_rank(docs, query):
    scored = []
    for i, d in enumerate(docs):
        score = 0.0
        for w in query:
            df = sum(1 for doc in docs if w in doc)
            if df:
                score += d.count(w) / len(d) * math.log(len(docs) / df)
        if score > 0:
            scored.append((-score, i))
    return [i for _, i in sorted(scored)]


@O
def tfidf_rank(docs, query):
    tf = np.array([[d.count(w) / len(d) for w in query] for d in docs])
    df = (tf > 0).sum(axis=0)
    idf = np.log(len(docs) / np.maximum(df, 1))
    scores = tf @ idf
    order = sorted(range(len(docs)), key=lambda i: (-scores[i], i))
    return [i for i in order if scores[i] > 0]


Q(None, "BM25 Score", "Hard", "The standard for keyword search",
  "Score doc i: Σ idf·tf·(k1 + 1) / (tf + k1·(1 − b + b·len/avg_len)), with idf = ln((N − df + 0.5)/(df + 0.5) + 1), k1 = 1.5, b = 0.75. Round to 4 decimals.",
  [((DOCS, ["market"], 2), 1.279), ((DOCS, ["cats", "dogs"], 3), 1.3597)],
  ("Loops over query words and documents.", "O(q·total)", "O(1)"),
  ("Array of lengths; set membership for df.", "O(q·n)", "O(n)"),
  names=["docs", "query", "i"])


@B
def bm25(docs, query, i):
    k1, b = 1.5, 0.75
    N = len(docs)
    avg = sum(len(d) for d in docs) / N
    score = 0.0
    for w in query:
        df = sum(1 for d in docs if w in d)
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        tf = docs[i].count(w)
        score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(docs[i]) / avg))
    return round(score, 4)


@O
def bm25(docs, query, i):
    k1, b = 1.5, 0.75
    lengths = np.array([len(d) for d in docs])
    tf = np.array([docs[i].count(w) for w in query])
    df = np.array([sum(w in d for d in docs) for w in query])
    idf = np.log((len(docs) - df + 0.5) / (df + 0.5) + 1)
    return round(float((idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * lengths[i] / lengths.mean()))).sum()), 4)


Q(None, "Vector Top-k", "Easy", "Semantic search",
  "Return indices of the k vectors with the highest cosine similarity to the query, with scores rounded to 4 decimals.",
  [(([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], [1.0, 0.2], 2), ([0, 2], [0.9806, 0.8321]))],
  ("Compute cosine in a loop, then sort.", "O(n·d + n log n)", "O(n)"),
  ("Normalise, then a matrix-vector product and <code>argsort</code>.", "O(n·d + n log n)", "O(n·d)"),
  names=["vectors", "query", "k"])


@B
def vector_top_k(vectors, query, k):
    q_len = math.sqrt(sum(v * v for v in query))
    scored = []
    for i, vec in enumerate(vectors):
        dot = sum(a * b for a, b in zip(vec, query))
        scored.append((-dot / (math.sqrt(sum(a * a for a in vec)) * q_len), i))
    scored.sort()
    return ([i for _, i in scored[:k]], [round(-s, 4) for s, _ in scored[:k]])


@O
def vector_top_k(vectors, query, k):
    V, q = np.array(vectors), np.array(query)
    scores = V @ q / (np.linalg.norm(V, axis=1) * np.linalg.norm(q))
    top = np.argsort(-scores)[:k]
    return (top, scores[top].round(4))


Q(None, "Filter, Then Search", "Medium", "Metadata matters",
  "Only consider items whose metadata has the given team. Return the id with the highest score, or None.",
  [(([{"id": "a", "team": "hr", "score": 0.9}, {"id": "b", "team": "eng", "score": 0.7}, {"id": "c", "team": "eng", "score": 0.8}], "eng"), 'c'), (([{"id": "a", "team": "hr", "score": 0.9}], "eng"), None)],
  ("A loop tracking the best.", "O(n)", "O(1)"),
  ("<code>max</code> with a generator and a default.", "O(n)", "O(1)"),
  names=["items", "team"])


@B
def filtered_best(items, team):
    best, best_score = None, -1
    for item in items:
        if item["team"] == team and item["score"] > best_score:
            best, best_score = item["id"], item["score"]
    return best


@O
def filtered_best(items, team):
    match = max((x for x in items if x["team"] == team), key=lambda x: x["score"], default=None)
    return match["id"] if match else None


Q(None, "An Approximate Index", "Hard", "Search only part of the data",
  "IVF: each vector belongs to its nearest centroid. Find the nprobe centroids nearest to the query, then search only their vectors. Return (best index by distance, distances computed to vectors).",
  [(([[0.0, 0.0], [0.0, 1.0], [10.0, 10.0], [10.0, 11.0], [5.0, 6.0]], [[0.0, 0.0], [10.0, 10.0]], [4.5, 5.0], 1), (1, 2)),
   (([[0.0, 0.0], [0.0, 1.0], [10.0, 10.0], [10.0, 11.0], [5.0, 6.0]], [[0.0, 0.0], [10.0, 10.0]], [4.5, 5.0], 2), (4, 5))],
  ("Loops for assigning and for searching.", "O(n·c)", "O(n)"),
  ("Distance matrices with broadcasting.", "O(n·c)", "O(n·c)"),
  names=["vectors", "centroids", "query", "nprobe"])


@B
def ivf_search(vectors, centroids, query, nprobe):
    def dist(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    lists = [[] for _ in centroids]
    for i, v in enumerate(vectors):
        nearest = min(range(len(centroids)), key=lambda c: dist(v, centroids[c]))
        lists[nearest].append(i)
    probes = sorted(range(len(centroids)), key=lambda c: dist(query, centroids[c]))[:nprobe]
    best, best_d, count = None, float("inf"), 0
    for c in probes:
        for i in lists[c]:
            count += 1
            d = dist(vectors[i], query)
            if d < best_d:
                best, best_d = i, d
    return (best, count)


@O
def ivf_search(vectors, centroids, query, nprobe):
    V, C, q = np.array(vectors), np.array(centroids), np.array(query)
    owner = np.linalg.norm(V[:, None] - C, axis=2).argmin(axis=1)
    probes = np.argsort(np.linalg.norm(C - q, axis=1))[:nprobe]
    members = np.flatnonzero(np.isin(owner, probes))
    return (int(members[np.linalg.norm(V[members] - q, axis=1).argmin()]), len(members))


Q(None, "Reciprocal Rank Fusion", "Medium", "Combine two rankings",
  "Score each id as Σ 1 / (k + rank), with ranks from 1 and k = 60. Return ids best first. RRF needs no comparable scores, just ranks.",
  [(([["a", "b", "c"], ["b", "c", "d"]],), ['b', 'c', 'a', 'd'])],
  ("A dictionary of scores.", "O(total log total)", "O(ids)"),
  ("<code>defaultdict</code> with <code>sorted</code>.", "O(total log total)", "O(ids)"))


@B
def rrf(rankings):
    scores = {}
    for ranking in rankings:
        for pos in range(len(ranking)):
            doc = ranking[pos]
            scores[doc] = scores.get(doc, 0) + 1 / (60 + pos + 1)
    return sorted(scores, key=lambda d: -scores[d])


@O
def rrf(rankings):
    from collections import defaultdict
    scores = defaultdict(float)
    for ranking in rankings:
        for rank, doc in enumerate(ranking, 1):
            scores[doc] += 1 / (60 + rank)
    return sorted(scores, key=scores.get, reverse=True)


Q(None, "Maximal Marginal Relevance", "Hard", "Relevant but not repetitive",
  "Pick k items. Each round, maximise λ·relevance − (1 − λ)·(highest similarity to anything chosen). Return the picks in order.",
  [(([0.9, 0.85, 0.5], [[1.0, 0.95, 0.1], [0.95, 1.0, 0.1], [0.1, 0.1, 1.0]], 2, 0.5), [0, 2]), (([0.9, 0.85, 0.5], [[1.0, 0.95, 0.1], [0.95, 1.0, 0.1], [0.1, 0.1, 1.0]], 2, 1.0), [0, 1])],
  ("Nested loops each round.", "O(k²·n)", "O(k)"),
  ("Maintain the highest similarity in an array, updating each round.", "O(k·n)", "O(n)"),
  names=["rel", "sim", "k", "lam"])


@B
def mmr(rel, sim, k, lam):
    chosen = []
    while len(chosen) < k:
        best, best_score = None, -float("inf")
        for i in range(len(rel)):
            if i in chosen:
                continue
            penalty = max((sim[i][j] for j in chosen), default=0)
            score = lam * rel[i] - (1 - lam) * penalty
            if score > best_score:
                best, best_score = i, score
        chosen.append(best)
    return chosen


@O
def mmr(rel, sim, k, lam):
    rel, sim = np.array(rel), np.array(sim)
    penalty = np.zeros(len(rel))
    available = np.ones(len(rel), dtype=bool)
    chosen = []
    for _ in range(k):
        score = lam * rel - (1 - lam) * penalty
        score[~available] = -np.inf
        best = int(score.argmax())
        chosen.append(best)
        available[best] = False
        penalty = np.maximum(penalty, sim[best])
    return chosen


Q(None, "Re-Rank the Candidates", "Easy", "Cheap first, careful second",
  "Given candidate ids and a re-ranker's scores, return the top k ids by those scores.",
  [((["a", "b", "c", "d"], [0.1, 0.9, 0.4, 0.7], 2), ['b', 'd'])],
  ("Sort pairs.", "O(n log n)", "O(n)"),
  ("<code>np.argsort</code>.", "O(n log n)", "O(n)"),
  names=["ids", "scores", "k"])


@B
def rerank(ids, scores, k):
    pairs = sorted(zip(scores, ids), reverse=True)
    return [doc for _, doc in pairs[:k]]


@O
def rerank(ids, scores, k):
    return [ids[i] for i in np.argsort(scores)[::-1][:k]]


Q(None, "Say When You Don't Know", "Easy", "A retrieval threshold",
  "If the best score is below the threshold, return 'no_answer'. Otherwise return the ids at or above it, best first.",
  [(([("a", 0.8), ("b", 0.4), ("c", 0.6)], 0.5), ['a', 'c']), (([("a", 0.3)], 0.5), 'no_answer')],
  ("Filter and sort in a loop.", "O(n log n)", "O(n)"),
  ("A sorted comprehension.", "O(n log n)", "O(n)"),
  names=["hits", "threshold"])


@B
def threshold_hits(hits, threshold):
    kept = []
    for doc, score in hits:
        if score >= threshold:
            kept.append((score, doc))
    if not kept:
        return "no_answer"
    kept.sort(reverse=True)
    return [doc for _, doc in kept]


@O
def threshold_hits(hits, threshold):
    kept = [doc for doc, s in sorted(hits, key=lambda h: -h[1]) if s >= threshold]
    return kept or "no_answer"


Q(None, "Remove Near-Duplicates", "Medium", "Don't pay for repeats",
  "Keep a chunk only if its Jaccard word overlap with every kept chunk is below the limit. Return kept indices.",
  [((["the cat sat", "the cat sat down", "stocks fell today"], 0.7), [0, 2])],
  ("Compare to each kept chunk.", "O(n²·w)", "O(n·w)"),
  ("Pre-compute sets, and use <code>all</code>.", "O(n²·w)", "O(n·w)"),
  names=["chunks", "limit"])


@B
def dedupe(chunks, limit):
    kept = []
    for i, text in enumerate(chunks):
        words = text.split()
        duplicate = False
        for j in kept:
            other = chunks[j].split()
            shared = len([w for w in set(words) if w in other])
            union = len(set(words + other))
            if shared / union >= limit:
                duplicate = True
                break
        if not duplicate:
            kept.append(i)
    return kept


@O
def dedupe(chunks, limit):
    sets = [set(c.split()) for c in chunks]
    kept = []
    for i, s in enumerate(sets):
        if all(len(s & sets[j]) / len(s | sets[j]) < limit for j in kept):
            kept.append(i)
    return kept


Q(None, "Fit Chunks Into the Budget", "Easy", "Best first, until full",
  "Go through chunk sizes in rank order, keeping each that still fits (later smaller chunks may still fit). Return kept indices.",
  [(([500, 800, 300, 400], 1000),  [0, 2])],
  ("A loop with a running total.", "O(n)", "O(n)"),
  ("It's already simple; a loop is the right tool.", "O(n)", "O(n)"),
  names=["sizes", "budget"])


@B
def fit_chunks(sizes, budget):
    kept, used = [], 0
    for i in range(len(sizes)):
        if used + sizes[i] <= budget:
            kept.append(i)
            used = used + sizes[i]
    return kept


@O
def fit_chunks(sizes, budget):
    kept = []
    for i, size in enumerate(sizes):
        if size <= budget:
            kept.append(i)
            budget -= size
    return kept


Q(None, "Build the Prompt With Sources", "Easy", "Make answers checkable",
  "Return lines '[1] text', '[2] text'… then a blank line, then 'Question: …', then the instruction 'Answer using only the sources. Cite them like [1].'",
  [((["Paris is in France.", "It has the Louvre."], "Where is Paris?"), '[1] Paris is in France.\n[2] It has the Louvre.\n\nQuestion: Where is Paris?\nAnswer using only the sources. Cite them like [1].')],
  ("Append with a counter.", "O(total)", "O(total)"),
  ("<code>enumerate(..., 1)</code> and <code>join</code>.", "O(total)", "O(total)"),
  names=["chunks", "question"])


@B
def rag_prompt(chunks, question):
    lines = []
    n = 1
    for c in chunks:
        lines.append("[" + str(n) + "] " + c)
        n += 1
    lines.append("")
    lines.append("Question: " + question)
    lines.append("Answer using only the sources. Cite them like [1].")
    return "\n".join(lines)


@O
def rag_prompt(chunks, question):
    sources = "\n".join(f"[{i}] {c}" for i, c in enumerate(chunks, 1))
    return f"{sources}\n\nQuestion: {question}\nAnswer using only the sources. Cite them like [1]."


Q(None, "Check the Citations", "Medium", "Catch invented sources",
  "Find every [n] in the answer. Return (sorted valid numbers, sorted invalid numbers), given n_sources sources.",
  [(("Paris is in France [1]. It is big [2][1]. Also [7].", 2), ([1, 2], [7]))],
  ("Scan for brackets by hand.", "O(n)", "O(c)"),
  ("<code>re.findall(r'\\[(\\d+)\\]', …)</code> and sets.", "O(n)", "O(c)"),
  names=["answer", "n_sources"])


@B
def check_citations(answer, n_sources):
    valid, invalid = [], []
    i = 0
    while i < len(answer):
        if answer[i] == "[":
            j = answer.find("]", i)
            if j != -1 and answer[i + 1:j].isdigit():
                n = int(answer[i + 1:j])
                target = valid if 1 <= n <= n_sources else invalid
                if n not in target:
                    target.append(n)
        i += 1
    return (sorted(valid), sorted(invalid))


@O
def check_citations(answer, n_sources):
    found = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    return (sorted(n for n in found if 1 <= n <= n_sources), sorted(n for n in found if not 1 <= n <= n_sources))


Q(None, "Recall@k", "Easy", "Did we find it?",
  "Return the fraction of relevant ids in the first k retrieved, rounded to 4 decimals.",
  [((["a", "b", "c", "d"], ["b", "d", "e"], 2), 0.3333), ((["a", "b", "c", "d"], ["b", "d", "e"], 4), 0.6667)],
  ("Count in a loop.", "O(k·r)", "O(1)"),
  ("Set intersection.", "O(k + r)", "O(k)"),
  names=["retrieved", "relevant", "k"])


@B
def recall_at_k(retrieved, relevant, k):
    found = 0
    for r in relevant:
        if r in retrieved[:k]:
            found += 1
    return round(found / len(relevant), 4)


@O
def recall_at_k(retrieved, relevant, k):
    return round(len(set(retrieved[:k]) & set(relevant)) / len(relevant), 4)


Q(None, "Precision@k", "Easy", "How much is noise?",
  "Return the fraction of the first k retrieved that are relevant, rounded to 4 decimals.",
  [((["a", "b", "c", "d"], ["b", "d", "e"], 2), 0.5), ((["a", "b", "c", "d"], ["b", "d", "e"], 4), 0.5)],
  ("Count in a loop.", "O(k·r)", "O(1)"),
  ("Set intersection.", "O(k + r)", "O(k)"),
  names=["retrieved", "relevant", "k"])


@B
def precision_at_k(retrieved, relevant, k):
    found = 0
    for r in retrieved[:k]:
        if r in relevant:
            found += 1
    return round(found / k, 4)


@O
def precision_at_k(retrieved, relevant, k):
    return round(len(set(retrieved[:k]) & set(relevant)) / k, 4)


Q(None, "Mean Reciprocal Rank", "Medium", "How high is the first hit?",
  "For each query, score 1 / (rank of first relevant result), or 0 if none. Return the mean, rounded to 4 decimals.",
  [(([(["a", "b", "c"], ["a"]), (["a", "b", "c"], ["c"]), (["a", "b"], ["z"])],), 0.4444)],
  ("Loops.", "O(q·k·r)", "O(1)"),
  ("<code>next</code> with a generator, sets for relevance.", "O(q·k)", "O(r)"))


@B
def mrr(results):
    total = 0.0
    for retrieved, relevant in results:
        for pos in range(len(retrieved)):
            if retrieved[pos] in relevant:
                total += 1 / (pos + 1)
                break
    return round(total / len(results), 4)


@O
def mrr(results):
    scores = [next((1 / rank for rank, d in enumerate(ret, 1) if d in set(rel)), 0) for ret, rel in results]
    return round(float(np.mean(scores)), 4)


Q(None, "nDCG@k", "Hard", "Graded relevance, order matters",
  "DCG = Σ relᵢ / log₂(i + 1), with i from 1. Return DCG@k ÷ the DCG@k of the ideal order, rounded to 4 decimals.",
  [(([3, 2, 3, 0, 1, 2], 6), 0.9608), (([2, 1, 0], 3), 1.0), (([0, 1, 2], 3), 0.6199)],
  ("Loops for both.", "O(n log n)", "O(n)"),
  ("A discount array shared by both.", "O(n log n)", "O(n)"),
  names=["rel", "k"])


@B
def ndcg(rel, k):
    def dcg(values):
        total = 0.0
        for i, v in enumerate(values[:k]):
            total += v / math.log2(i + 2)
        return total
    return round(dcg(rel) / dcg(sorted(rel, reverse=True)), 4)


@O
def ndcg(rel, k):
    r = np.array(rel, dtype=float)
    discount = 1 / np.log2(np.arange(2, len(r) + 2))
    return round(float((r[:k] * discount[:k]).sum() / (np.sort(r)[::-1][:k] * discount[:k]).sum()), 4)
