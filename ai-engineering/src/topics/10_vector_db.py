from lib import *
import hashlib
import json
import math
import re
import heapq
from collections import defaultdict

import duckdb
import numpy as np

TOPIC(
    id="vector-db", title="Vector Databases & AI Frameworks", glyph="🧭",
    blurb="The infrastructure under RAG and agents: distance metrics, IVF, product and scalar quantization, HNSW graph search, post-filtering, upserts and deletes, memory sizing, sharded search, hybrid scoring, metadata filters, vector search in SQL, embedding and semantic caches, model migrations — and how LangChain-style frameworks compose chains, split text, template prompts and retrieve.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py"># pgvector (PostgreSQL)
CREATE EXTENSION vector;
CREATE TABLE chunks (id bigserial PRIMARY KEY, body text, tenant text, embedding vector(1536));
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
SELECT id, body FROM chunks WHERE tenant = 'acme' ORDER BY embedding &lt;=&gt; $1 LIMIT 5;

# Qdrant / Chroma (Python)
client.upsert(collection_name="docs", points=[PointStruct(id=1, vector=v, payload={"lang": "en"})])
collection.query(query_embeddings=[q], n_results=5, where={"lang": "en"})</code></pre>
<p>Exact search compares the query with every vector; approximate (ANN) indexes — HNSW graphs, IVF lists, quantized codes — trade a little recall for huge speed and memory savings.</p>
""")


def normalise(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


DOCS = {"d1": [0.9, 0.1, 0.0], "d2": [3.0, 1.0, 0.2], "d3": [0.2, 0.9, 0.1], "d4": [0.5, 0.5, 0.5], "d5": [0.05, 0.02, 0.0]}


Q(None, "Cosine, Dot or Euclidean?", "Easy", "Metrics rank differently",
  "Rank the documents for the query by cosine similarity, dot product (both higher is better) and Euclidean distance (lower is better). Return the three rankings, then the three rankings again after normalising every vector to length 1 — they agree once vectors are normalised, which is why most embedding models ship normalised vectors.",
  [((DOCS, [1.0, 0.2, 0.0]), [['d1', 'd2', 'd5', 'd4', 'd3'], ['d2', 'd1', 'd4', 'd3', 'd5'], ['d1', 'd4', 'd5', 'd3', 'd2'], ['d1', 'd2', 'd5', 'd4', 'd3'], ['d1', 'd2', 'd5', 'd4', 'd3'], ['d1', 'd2', 'd5', 'd4', 'd3']])],
  ("Compute each metric with loops.", "O(n · d)", "O(n)"),
  ("Matrix operations in NumPy.", "O(n · d)", "O(n)"),
  viz=(({"a": [1.0, 0.0], "b": [3.0, 3.0]}, [1.0, 0.1])))


@B
def metric_rankings(docs, query):
    def rank(vectors, q):
        cos, dot, l2 = {}, {}, {}
        for k, v in vectors.items():
            d = sum(a * b for a, b in zip(v, q))
            nv = math.sqrt(sum(a * a for a in v))
            nq = math.sqrt(sum(a * a for a in q))
            cos[k] = d / (nv * nq)
            dot[k] = d
            l2[k] = math.sqrt(sum((a - b) ** 2 for a, b in zip(v, q)))
        return [sorted(cos, key=lambda k: -cos[k]), sorted(dot, key=lambda k: -dot[k]), sorted(l2, key=lambda k: l2[k])]
    unit = lambda v: [x / math.sqrt(sum(y * y for y in v)) for x in v]
    return rank(docs, query) + rank({k: unit(v) for k, v in docs.items()}, unit(query))


@O
def metric_rankings(docs, query):
    names = list(docs)
    def rank(M, q):
        dot = M @ q
        cos = dot / (np.linalg.norm(M, axis=1) * np.linalg.norm(q))
        l2 = np.linalg.norm(M - q, axis=1)
        order = lambda s: [names[i] for i in np.argsort(s, kind="stable")]
        return [order(-cos), order(-dot), order(l2)]
    M, q = np.array([docs[n] for n in names], dtype=float), np.array(query, dtype=float)
    return rank(M, q) + rank(M / np.linalg.norm(M, axis=1, keepdims=True), q / np.linalg.norm(q))


POINTS = {"p1": [0.1, 0.2], "p2": [0.2, 0.1], "p3": [0.9, 0.8], "p4": [0.8, 0.95], "p5": [0.15, 0.9], "p6": [0.25, 0.8],
          "p7": [0.85, 0.15], "p8": [0.5, 0.45], "p9": [0.55, 0.6], "p10": [0.95, 0.3]}
CENTROIDS = [[0.15, 0.15], [0.85, 0.85], [0.2, 0.85], [0.85, 0.2]]


Q(None, "Search an IVF Index", "Medium", "Inverted file lists",
  "An IVF index assigns every vector to its nearest centroid (Euclidean). A query only scans the lists of its <code>nprobe</code> nearest centroids. For each nprobe, return <code>(vectors scanned, top-k ids found, recall vs exact top-k)</code>.",
  [((POINTS, CENTROIDS, [0.45, 0.5], 3, [1, 2, 4]), [(2, ['p6', 'p5'], 0.33), (4, ['p6', 'p1', 'p2'], 0.33), (10, ['p8', 'p9', 'p6'], 1.0)])],
  ("Loops for assignment and scanning.", "O(n · c + p · n)", "O(n)"),
  ("NumPy distances and argsort.", "O(n · c + p · n)", "O(n)"),
  viz=(({"a": [0.0, 0.0], "b": [1.0, 1.0]}, [[0.0, 0.0], [1.0, 1.0]], [0.4, 0.4], 1, [1])))


@B
def ivf_search(points, centroids, query, k, nprobes):
    dist = lambda a, b: math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    lists = defaultdict(list)
    for pid, v in points.items():
        best = min(range(len(centroids)), key=lambda c: dist(v, centroids[c]))
        lists[best].append(pid)
    exact = sorted(points, key=lambda p: (dist(points[p], query), p))[:k]
    order = sorted(range(len(centroids)), key=lambda c: dist(query, centroids[c]))
    out = []
    for nprobe in nprobes:
        cand = [p for c in order[:nprobe] for p in lists[c]]
        found = sorted(cand, key=lambda p: (dist(points[p], query), p))[:k]
        out.append((len(cand), found, round(len(set(found) & set(exact)) / k, 2)))
    return out


@O
def ivf_search(points, centroids, query, k, nprobes):
    ids = list(points)
    X, C, q = np.array([points[i] for i in ids]), np.array(centroids), np.array(query)
    assign = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), axis=1)
    d = np.linalg.norm(X - q, axis=1)
    rank = lambda idx: [ids[i] for i in sorted(idx, key=lambda i: (d[i], ids[i]))][:k]
    exact = set(rank(range(len(ids))))
    probe_order = np.argsort(np.linalg.norm(C - q, axis=1), kind="stable")
    out = []
    for n in nprobes:
        cand = [i for i in range(len(ids)) if assign[i] in set(probe_order[:n].tolist())]
        found = rank(cand)
        out.append((len(cand), found, round(len(set(found) & exact) / k, 2)))
    return out


Q(None, "Product Quantization", "Hard", "Compress vectors to a few bytes",
  "PQ splits each vector into <code>m</code> equal sub-vectors and replaces each with the index of its nearest codeword in that sub-space's codebook. Return the codes for each vector, the bytes per vector before (float32) and after (1 byte per code), and each vector's reconstruction error (Euclidean distance to the decoded vector, rounded to 3).",
  [(({"v1": [0.1, 0.9, 0.4, 0.4], "v2": [0.8, 0.2, 0.9, 0.1], "v3": [0.15, 0.85, 0.95, 0.05]}, [[[0.1, 0.9], [0.8, 0.2]], [[0.4, 0.4], [0.9, 0.1], [0.0, 0.0]]]), ({'v1': ([0, 0], 0.0), 'v2': ([1, 1], 0.0), 'v3': ([0, 1], 0.1)}, 16, 2))],
  ("Loops over sub-vectors and codewords.", "O(n · m · c · s)", "O(n · m)"),
  ("NumPy reshape and argmin per sub-space.", "O(n · m · c · s)", "O(n · m)"),
  viz=(({"a": [0.0, 1.0]}, [[[0.0], [1.0]], [[0.0], [1.0]]])))


@B
def pq_encode(vectors, codebooks):
    m = len(codebooks)
    out = {}
    for name, v in vectors.items():
        s = len(v) // m
        codes, decoded = [], []
        for j in range(m):
            sub = v[j * s:(j + 1) * s]
            best = min(range(len(codebooks[j])), key=lambda c: sum((a - b) ** 2 for a, b in zip(sub, codebooks[j][c])))
            codes.append(best)
            decoded += codebooks[j][best]
        err = math.sqrt(sum((a - b) ** 2 for a, b in zip(v, decoded)))
        out[name] = (codes, round(err, 3))
    return (out, len(next(iter(vectors.values()))) * 4, m)


@O
def pq_encode(vectors, codebooks):
    m = len(codebooks)
    out = {}
    for name, v in vectors.items():
        subs = np.array(v).reshape(m, -1)
        codes = [int(np.argmin(((np.array(codebooks[j]) - subs[j]) ** 2).sum(1))) for j in range(m)]
        decoded = np.concatenate([np.array(codebooks[j][c]) for j, c in enumerate(codes)])
        out[name] = (codes, round(float(np.linalg.norm(np.array(v) - decoded)), 3))
    return (out, len(next(iter(vectors.values()))) * 4, m)


Q(None, "Scalar Quantization to int8", "Medium", "4× smaller, tiny error",
  "Quantize each dimension to an integer 0–255 using that dimension's min and max over all vectors: <code>code = round((x − min) / (max − min) × 255)</code>. Return the codes, the largest absolute error after decoding (rounded to 4), and the memory ratio float32 ÷ int8.",
  [(([[0.12, -0.5, 0.33], [0.9, 0.1, -0.2], [-0.3, 0.45, 0.05], [0.5, -0.05, 0.8]],), ([[89, 0, 135], [255, 161, 0], [0, 255, 64], [170, 121, 255]], 0.0012, 4.0))],
  ("Loops over dimensions and values.", "O(n · d)", "O(n · d)"),
  ("Vectorised min, max and rounding.", "O(n · d)", "O(n · d)"),
  viz=(([[0.0, 1.0], [1.0, 0.0]],)))


@B
def int8_quantize(vectors):
    d = len(vectors[0])
    lo = [min(v[j] for v in vectors) for j in range(d)]
    hi = [max(v[j] for v in vectors) for j in range(d)]
    codes, worst = [], 0.0
    for v in vectors:
        row = []
        for j in range(d):
            c = round((v[j] - lo[j]) / (hi[j] - lo[j]) * 255)
            row.append(c)
            back = lo[j] + c / 255 * (hi[j] - lo[j])
            worst = max(worst, abs(back - v[j]))
        codes.append(row)
    return (codes, round(worst, 4), 4.0)


@O
def int8_quantize(vectors):
    X = np.array(vectors)
    lo, hi = X.min(0), X.max(0)
    codes = np.round((X - lo) / (hi - lo) * 255)
    back = lo + codes / 255 * (hi - lo)
    return (codes.astype(int).tolist(), round(float(np.abs(back - X).max()), 4), 4.0)


GRAPH = {"a": ["b", "c"], "b": ["a", "d", "e"], "c": ["a", "f"], "d": ["b", "g"], "e": ["b", "g", "h"], "f": ["c", "h"], "g": ["d", "e", "h"], "h": ["e", "f", "g"]}
COORDS = {"a": [0.0, 0.0], "b": [1.0, 0.5], "c": [0.5, 1.5], "d": [2.0, 0.2], "e": [2.0, 1.2], "f": [1.0, 2.5], "g": [3.0, 0.8], "h": [2.8, 2.0]}


Q(None, "Greedy Search on an HNSW Graph", "Medium", "Walk towards the query",
  "HNSW stores vectors as a graph where each node links to near neighbours. Search starts at an entry point and repeatedly moves to the neighbour closest to the query, stopping when no neighbour is closer. Return <code>(path taken, node found, true nearest node, distance computations made)</code> for each query.",
  [((GRAPH, COORDS, "a", [[2.9, 1.9], [2.1, 0.3], [0.9, 2.3]]), [(['a', 'b', 'e', 'h'], 'h', 'h', 12), (['a', 'b', 'd'], 'd', 'd', 8), (['a', 'c', 'f'], 'f', 'f', 7)])],
  ("Compare every neighbour with explicit loops.", "O(hops · degree)", "O(hops)"),
  ("min() over neighbours with a cached distance function.", "O(hops · degree)", "O(n)"),
  viz=(({"x": ["y"], "y": ["x"]}, {"x": [0.0, 0.0], "y": [1.0, 0.0]}, "x", [[1.0, 0.1]])))


@B
def hnsw_greedy(graph, coords, entry, queries):
    out = []
    for q in queries:
        dist = lambda n: math.dist(coords[n], q)
        cur, path, comps = entry, [entry], 1
        while True:
            best = cur
            for nb in graph[cur]:
                comps += 1
                if dist(nb) < dist(best):
                    best = nb
            if best == cur:
                break
            cur = best
            path.append(cur)
        out.append((path, cur, min(coords, key=dist), comps))
    return out


@O
def hnsw_greedy(graph, coords, entry, queries):
    out = []
    for q in queries:
        d = {n: math.dist(c, q) for n, c in coords.items()}
        cur, path, comps = entry, [entry], 1
        while (nxt := min(graph[cur], key=d.get)) and d[nxt] < d[cur]:
            comps += len(graph[cur])
            cur = nxt
            path.append(cur)
        comps += len(graph[cur])
        out.append((path, cur, min(d, key=d.get), comps))
    return out


Q(None, "Post-Filtering Loses Results", "Easy", "Filter before or after the search?",
  "Documents have a similarity score to the query and a <code>lang</code>. Post-filtering takes the top <code>k</code> by score and then keeps the matching language; pre-filtering keeps the language first, then takes the top k. Return both result lists — post-filtering can return fewer than k even when enough matching documents exist.",
  [(({"d1": (0.92, "en"), "d2": (0.90, "en"), "d3": (0.88, "hi"), "d4": (0.85, "en"), "d5": (0.80, "hi"), "d6": (0.71, "hi"), "d7": (0.65, "en")}, "hi", 3), (['d3'], ['d3', 'd5', 'd6']))],
  ("Sort, slice, filter by hand.", "O(n log n)", "O(n)"),
  ("Comprehensions around sorted().", "O(n log n)", "O(n)"),
  viz=(({"a": (0.9, "en"), "b": (0.5, "hi")}, "hi", 1)))


@B
def pre_vs_post(docs, lang, k):
    ranked = sorted(docs, key=lambda d: -docs[d][0])
    post = []
    for d in ranked[:k]:
        if docs[d][1] == lang:
            post.append(d)
    pre = []
    for d in ranked:
        if docs[d][1] == lang and len(pre) < k:
            pre.append(d)
    return (post, pre)


@O
def pre_vs_post(docs, lang, k):
    ranked = sorted(docs, key=lambda d: -docs[d][0])
    return ([d for d in ranked[:k] if docs[d][1] == lang], [d for d in ranked if docs[d][1] == lang][:k])


Q(None, "Upserts, Deletes and Compaction", "Medium", "Segments and tombstones",
  "Many vector stores append writes to segments: an upsert adds a new version of an id and hides older ones, a delete writes a tombstone. Process operations <code>('upsert', id)</code> and <code>('delete', id)</code> and return <code>(live ids sorted, stored entries before compaction, stored entries after compaction)</code>. Compaction keeps only live versions.",
  [(([("upsert", "a"), ("upsert", "b"), ("upsert", "a"), ("delete", "b"), ("upsert", "c"), ("upsert", "a"), ("delete", "zz"), ("upsert", "b")],), (['a', 'b', 'c'], 8, 3))],
  ("Append to a log and replay it.", "O(n)", "O(n)"),
  ("A dict of latest state plus a counter.", "O(n)", "O(k)"),
  viz=(([("upsert", "a"), ("delete", "a")],)))


@B
def segments(ops):
    log = []
    for op, i in ops:
        log.append((op, i))
    live = {}
    for op, i in log:
        if op == "upsert":
            live[i] = True
        else:
            live.pop(i, None)
    return (sorted(live), len(log), len(live))


@O
def segments(ops):
    state = {}
    for op, i in ops:
        state[i] = op == "upsert"
    live = sorted(i for i, alive in state.items() if alive)
    return (live, len(ops), len(live))


Q(None, "How Much Memory Will the Index Need?", "Easy", "Size before you buy",
  "For <code>n</code> vectors of dimension <code>d</code>, return GB (rounded to 1) for: float32 vectors, plus an HNSW graph with <code>M</code> links per node in both directions (2·M × 4-byte ids on the base layer), and the same with int8 vectors, and PQ with <code>m</code> bytes per vector (no graph). 1 GB = 10⁹ bytes.",
  [((10_000_000, 1536, 16, 96), {'float32+hnsw': 62.7, 'int8+hnsw': 16.6, 'pq': 1.0}), ((500_000, 384, 16, 48), {'float32+hnsw': 0.8, 'int8+hnsw': 0.3, 'pq': 0.0})],
  ("Arithmetic step by step.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((1000, 8, 4, 2)))


@B
def index_memory(n, d, M, m):
    graph = n * 2 * M * 4
    f32 = n * d * 4 + graph
    i8 = n * d + graph
    pq = n * m
    return {"float32+hnsw": round(f32 / 1e9, 1), "int8+hnsw": round(i8 / 1e9, 1), "pq": round(pq / 1e9, 1)}


@O
def index_memory(n, d, M, m):
    g = n * 8 * M
    return {k: round(v / 1e9, 1) for k, v in {"float32+hnsw": n * d * 4 + g, "int8+hnsw": n * d + g, "pq": n * m}.items()}


Q(None, "Search Across Shards", "Medium", "Scatter, then merge",
  "A big index is split across shards. Each shard returns its own top <code>k</code> (score, id); the coordinator merges them into the global top k. Return the global top-k ids and whether it equals searching all scores at once (it always does when every shard returns k).",
  [(([{"a": 0.91, "b": 0.55, "c": 0.77}, {"d": 0.95, "e": 0.40, "f": 0.88}, {"g": 0.60, "h": 0.93, "i": 0.79}], 4), (['d', 'h', 'a', 'f'], True))],
  ("Concatenate everything and sort.", "O(n log n)", "O(n)"),
  ("Each shard's top k, then heapq.merge.", "O(n log k + s·k log s)", "O(s · k)"),
  viz=(([{"a": 0.5}, {"b": 0.9}], 1)))


@B
def shard_search(shards, k):
    everything = {i: s for sh in shards for i, s in sh.items()}
    top = sorted(everything, key=lambda i: (-everything[i], i))[:k]
    return (top, True)


@O
def shard_search(shards, k):
    per_shard = [sorted(((-s, i) for i, s in sh.items()))[:k] for sh in shards]
    merged = [i for _, i in list(heapq.merge(*per_shard))[:k]]
    everything = {i: s for sh in shards for i, s in sh.items()}
    return (merged, merged == sorted(everything, key=lambda i: (-everything[i], i))[:k])


Q(None, "Hybrid Search With a Weighted Blend", "Medium", "Keyword + vector scores",
  "Min-max normalise the BM25 scores and the vector scores separately to 0–1 (missing scores count as 0 after normalising; if all scores in a list are equal, they all become 1), then blend: <code>alpha × vector + (1 − alpha) × keyword</code>. Return the top-3 ids for each alpha (ties by id). alpha = 1 is pure vector search, 0 is pure keyword search.",
  [(({"d1": 12.0, "d2": 3.5, "d4": 8.0, "d6": 0.5}, {"d1": 0.62, "d2": 0.91, "d3": 0.88, "d5": 0.70}, [0.0, 0.5, 1.0]), {0.0: ['d1', 'd4', 'd2'], 0.5: ['d2', 'd1', 'd3'], 1.0: ['d2', 'd3', 'd5']})],
  ("Normalise with loops, blend per alpha.", "O(a · n log n)", "O(n)"),
  ("A normaliser helper and sorted().", "O(a · n log n)", "O(n)"),
  viz=(({"a": 1.0, "b": 2.0}, {"a": 0.9, "b": 0.2}, [0.5])))


@B
def hybrid_blend(bm25, vec, alphas):
    def norm(s):
        lo, hi = min(s.values()), max(s.values())
        return {k: (v - lo) / (hi - lo) if hi > lo else 1.0 for k, v in s.items()}
    kb, vb = norm(bm25), norm(vec)
    ids = sorted(set(bm25) | set(vec))
    out = {}
    for a in alphas:
        scores = {}
        for i in ids:
            scores[i] = a * vb.get(i, 0.0) + (1 - a) * kb.get(i, 0.0)
        out[a] = sorted(ids, key=lambda i: (-scores[i], i))[:3]
    return out


@O
def hybrid_blend(bm25, vec, alphas):
    def norm(s):
        lo, hi = min(s.values()), max(s.values())
        return {k: (v - lo) / (hi - lo) if hi > lo else 1.0 for k, v in s.items()}
    kb, vb = norm(bm25), norm(vec)
    ids = bm25.keys() | vec.keys()
    score = lambda a, i: a * vb.get(i, 0.0) + (1 - a) * kb.get(i, 0.0)
    return {a: sorted(ids, key=lambda i: (-score(a, i), i))[:3] for a in alphas}


def matches(meta, cond):
    if "$and" in cond:
        return all(matches(meta, c) for c in cond["$and"])
    if "$or" in cond:
        return any(matches(meta, c) for c in cond["$or"])
    field, rule = next(iter(cond.items()))
    v = meta.get(field)
    if not isinstance(rule, dict):
        return v == rule
    op, arg = next(iter(rule.items()))
    if v is None:
        return op == "$ne"
    ops = {"$eq": lambda: v == arg, "$ne": lambda: v != arg, "$gt": lambda: v > arg, "$gte": lambda: v >= arg,
           "$lt": lambda: v < arg, "$lte": lambda: v <= arg, "$in": lambda: v in arg, "$nin": lambda: v not in arg}
    return ops[op]()


Q(None, "Evaluate Metadata Filters", "Medium", "Chroma/Qdrant-style where clauses",
  "Vector stores filter on metadata with nested conditions: <code>{'field': value}</code>, <code>{'field': {'$gte': 2024}}</code> (also <code>$eq $ne $gt $lt $lte $in $nin</code>), combined with <code>$and</code> / <code>$or</code>. Return the ids that match each filter (use <code>matches</code>). A missing field never matches, except with <code>$ne</code>.",
  [(({"c1": {"year": 2025, "lang": "en", "team": "billing"}, "c2": {"year": 2023, "lang": "hi", "team": "billing"}, "c3": {"year": 2024, "lang": "en"}, "c4": {"year": 2026, "lang": "ta", "team": "support"}},
     [{"lang": "en"}, {"$and": [{"year": {"$gte": 2024}}, {"lang": {"$in": ["en", "hi"]}}]}, {"$or": [{"team": "support"}, {"year": {"$lt": 2024}}]}, {"team": {"$ne": "billing"}}]), [['c1', 'c3'], ['c1', 'c3'], ['c2', 'c4'], ['c3', 'c4']])],
  ("Loop over documents for each filter.", "O(f · n · c)", "O(n)"),
  ("A comprehension per filter.", "O(f · n · c)", "O(n)"),
  viz=(({"a": {"x": 1}}, [{"x": {"$gt": 0}}])))


@B
def filter_ids(meta, filters):
    out = []
    for f in filters:
        ids = []
        for i, m in meta.items():
            if matches(m, f):
                ids.append(i)
        out.append(ids)
    return out


@O
def filter_ids(meta, filters):
    return [[i for i, m in meta.items() if matches(m, f)] for f in filters]


CHUNKS = [{"id": 1, "tenant": "acme", "body": "refund policy", "emb": [0.9, 0.1, 0.1]}, {"id": 2, "tenant": "acme", "body": "shipping times", "emb": [0.1, 0.9, 0.2]},
          {"id": 3, "tenant": "globex", "body": "refund rules", "emb": [0.85, 0.15, 0.05]}, {"id": 4, "tenant": "acme", "body": "return a parcel", "emb": [0.7, 0.4, 0.1]},
          {"id": 5, "tenant": "acme", "body": "invoice copy", "emb": [0.3, 0.2, 0.9]}]


Q(None, "Vector Search in SQL", "Medium", "pgvector-style queries with DuckDB",
  "Store chunks with an embedding column and search with SQL, as pgvector does in PostgreSQL: filter to the tenant, order by cosine similarity to the query, limit k. Return <code>(id, body, similarity rounded to 3)</code>. Keeping vectors next to your relational data makes tenant filters and joins easy.",
  [((CHUNKS, "acme", [1.0, 0.2, 0.0], 3), [(1, 'refund policy', 0.99), (4, 'return a parcel', 0.941), (5, 'invoice copy', 0.344)])],
  ("Cosine similarity in a loop, then sort.", "O(n · d)", "O(n)"),
  ("DuckDB <code>list_cosine_similarity</code> in a query.", "O(n · d)", "O(n)"),
  viz=((CHUNKS[:2], "acme", [1.0, 0.0, 0.0], 1)))


@B
def sql_vector_search(chunks, tenant, query, k):
    out = []
    for c in chunks:
        if c["tenant"] != tenant:
            continue
        dot = sum(a * b for a, b in zip(c["emb"], query))
        sim = dot / (math.sqrt(sum(a * a for a in c["emb"])) * math.sqrt(sum(b * b for b in query)))
        out.append((c["id"], c["body"], round(sim, 3)))
    return sorted(out, key=lambda r: (-r[2], r[0]))[:k]


@O
def sql_vector_search(chunks, tenant, query, k):
    con = duckdb.connect()
    con.execute("CREATE TABLE chunks (id BIGINT, tenant VARCHAR, body VARCHAR, emb DOUBLE[])")
    con.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?)", [[c["id"], c["tenant"], c["body"], c["emb"]] for c in chunks])
    return con.execute("""
        SELECT id, body, ROUND(list_cosine_similarity(emb, CAST(? AS DOUBLE[])), 3) AS sim
        FROM chunks WHERE tenant = ? ORDER BY sim DESC, id LIMIT ?""", [query, tenant, k]).fetchall()


Q(None, "Cache Embeddings", "Easy", "Never pay twice for the same text",
  "Embedding calls cost money and time. Cache by <code>model + sha256(text)</code>. For the stream of <code>(model, text)</code> requests, return <code>(API calls made, cache hits, % saved rounded to 1)</code>. Changing the model must miss the cache — vectors from different models aren't comparable.",
  [(([("e5-small", "refund policy"), ("e5-small", "shipping times"), ("e5-small", "refund policy"), ("bge-m3", "refund policy"), ("e5-small", "refund policy"), ("bge-m3", "refund policy"), ("e5-small", "Refund policy")],), (4, 3, 42.9))],
  ("A list of seen keys.", "O(n²)", "O(n)"),
  ("A set of hashed keys.", "O(n)", "O(n)"),
  viz=(([("m", "a"), ("m", "a")],)))


@B
def embedding_cache(requests):
    seen, calls, hits = [], 0, 0
    for model, text in requests:
        key = model + ":" + hashlib.sha256(text.encode()).hexdigest()
        if key in seen:
            hits += 1
        else:
            seen.append(key)
            calls += 1
    return (calls, hits, round(hits / len(requests) * 100, 1))


@O
def embedding_cache(requests):
    keys = [f"{m}:{hashlib.sha256(t.encode()).hexdigest()}" for m, t in requests]
    calls = len(set(keys))
    return (calls, len(keys) - calls, round(100 * (len(keys) - calls) / len(keys), 1))


Q(None, "Plan an Embedding Model Migration", "Medium", "Re-embed without downtime",
  "Switching embedding models means re-embedding every chunk into a <b>new</b> index while the old one serves traffic, then switching over. Given chunks, average tokens per chunk, the provider's rate limit (tokens per minute), the price per million tokens, and the share of capacity you can use, return <code>(hours to backfill rounded to 1, cost in $ rounded to 2, GB for both indexes during the switch rounded to 1)</code> with float32 vectors of the old and new dimensions.",
  [((4_000_000, 350, 1_000_000, 0.02, 0.7, 768, 1024), (33.3, 28.0, 28.7))],
  ("Step-by-step arithmetic.", "O(1)", "O(1)"),
  ("Same, compact.", "O(1)", "O(1)"),
  viz=((1000, 100, 10000, 0.1, 1.0, 4, 8)))


@B
def migration_plan(chunks, tokens_each, tpm, price, share, old_dim, new_dim):
    tokens = chunks * tokens_each
    minutes = tokens / (tpm * share)
    cost = tokens / 1_000_000 * price
    gb = chunks * (old_dim + new_dim) * 4 / 1e9
    return (round(minutes / 60, 1), round(cost, 2), round(gb, 1))


@O
def migration_plan(chunks, tokens_each, tpm, price, share, old_dim, new_dim):
    t = chunks * tokens_each
    return (round(t / (tpm * share) / 60, 1), round(t * price / 1e6, 2), round(chunks * (old_dim + new_dim) * 4 / 1e9, 1))


def fake_llm(prompt):
    topic = re.search(r"about (\w+)", prompt)
    return f'{{"answer": "{topic.group(1) if topic else "unknown"} is covered in our docs", "confidence": 0.8}}'


STEPS = {"prompt": lambda x: f"Answer briefly about {x['topic']}.", "llm": fake_llm,
         "parse_json": lambda s: json.loads(s), "pick_answer": lambda d: d["answer"], "upper": lambda s: s.upper()}


Q(None, "Compose a Chain Like LangChain", "Medium", "prompt | llm | parser",
  "LangChain's LCEL composes steps with <code>|</code>: each step's output feeds the next, and a dict of steps runs them in parallel on the same input. Given a pipeline of step names from <code>STEPS</code> (a step may also be a dict <code>{key: [step names]}</code> meaning 'run these sub-chains and collect a dict'), run it on the input. The brute force loops; the optimal builds a tiny <code>Runnable</code> class with <code>__or__</code>.",
  [((["prompt", "llm", "parse_json", "pick_answer"], {"topic": "refunds"}), 'refunds is covered in our docs'), (([{"short": ["prompt", "llm", "parse_json", "pick_answer"], "loud": ["prompt", "llm", "parse_json", "pick_answer", "upper"]}], {"topic": "shipping"}), {'short': 'shipping is covered in our docs', 'loud': 'SHIPPING IS COVERED IN OUR DOCS'})],
  ("A loop applying each step.", "O(s)", "O(1)"),
  ("Runnable objects composed with |.", "O(s)", "O(s)"),
  viz=((["prompt", "upper"], {"topic": "x"})))


@B
def run_chain(pipeline, value):
    for step in pipeline:
        if isinstance(step, dict):
            value = {k: run_chain(sub, value) for k, sub in step.items()}
        else:
            value = STEPS[step](value)
    return value


@O
def run_chain(pipeline, value):
    class Runnable:
        def __init__(self, fn):
            self.fn = fn
        def __or__(self, other):
            return Runnable(lambda x: other.fn(self.fn(x)))
        def invoke(self, x):
            return self.fn(x)
    def build(steps):
        def one(s):
            if isinstance(s, dict):
                parts = {k: build(v) for k, v in s.items()}
                return Runnable(lambda x: {k: r.invoke(x) for k, r in parts.items()})
            return Runnable(STEPS[s])
        chain = one(steps[0])
        for s in steps[1:]:
            chain = chain | one(s)
        return chain
    return build(pipeline).invoke(value)


Q(None, "Split Text Recursively", "Medium", "RecursiveCharacterTextSplitter",
  "Split text into chunks of at most <code>size</code> characters, trying separators in order (<code>'\\n\\n'</code>, <code>'\\n'</code>, <code>' '</code>, then single characters): split on the first separator that occurs, merge consecutive pieces (joined by that separator) while they fit, and recursively split any piece still too long with the next separators. Return the chunks.",
  [(("Refunds\n\nWe refund unused items within 30 days.\nOpened items get store credit.\n\nShipping\n\nOrders ship in 2 days.", 40), ['Refunds', 'We refund unused items within 30 days.', 'Opened items get store credit.', 'Shipping\n\nOrders ship in 2 days.'])],
  ("Recursive splitting with explicit loops.", "O(n · s)", "O(n)"),
  ("The same recursion with a merge helper.", "O(n · s)", "O(n)"),
  viz=(("aa bb cc", 5)))


@B
def recursive_split(text, size, seps=("\n\n", "\n", " ", "")):
    if len(text) <= size:
        return [text] if text else []
    sep = next(s for s in seps if s == "" or s in text)
    rest = seps[seps.index(sep) + 1:]
    pieces = list(text) if sep == "" else text.split(sep)
    chunks, cur = [], ""
    for p in pieces:
        candidate = p if not cur else cur + sep + p
        if len(candidate) <= size:
            cur = candidate
        else:
            if cur:
                chunks.append(cur)
            if len(p) > size:
                chunks += recursive_split(p, size, rest)
                cur = ""
            else:
                cur = p
    if cur:
        chunks.append(cur)
    return chunks


@O
def recursive_split(text, size, seps=("\n\n", "\n", " ", "")):
    if len(text) <= size:
        return [text] if text else []
    i = next(i for i, s in enumerate(seps) if s == "" or s in text)
    sep, rest = seps[i], seps[i + 1:]
    out, cur = [], ""
    for p in (list(text) if sep == "" else text.split(sep)):
        joined = f"{cur}{sep}{p}" if cur else p
        if len(joined) <= size:
            cur = joined
            continue
        out += [cur] if cur else []
        if len(p) > size:
            out += recursive_split(p, size, rest)
            cur = ""
        else:
            cur = p
    return out + ([cur] if cur else [])


Q(None, "Fill a Prompt Template Safely", "Easy", "PromptTemplate variables",
  "A template has <code>{variables}</code> (<code>{{</code> and <code>}}</code> are literal braces). For each input dict, return the filled prompt, or an error listing missing variables (sorted) — and separately list unused inputs (sorted). Catching a missing variable at build time beats sending <code>'{context}'</code> to the model.",
  [(("Use only this context:\n{context}\n\nQuestion: {question}\nAnswer as JSON like {{\"answer\": ...}}.", [{"context": "Refunds take 5 days.", "question": "How long do refunds take?"}, {"question": "Hi", "user": "asha"}]), [('Use only this context:\nRefunds take 5 days.\n\nQuestion: How long do refunds take?\nAnswer as JSON like {"answer": ...}.', []), ('error: missing context', ['user'])])],
  ("Scan for braces by hand.", "O(n · L)", "O(L)"),
  ("<code>string.Formatter().parse</code> and <code>str.format</code>.", "O(n · L)", "O(L)"),
  viz=(("Hi {name}", [{"name": "A"}])))


@B
def fill_template(template, inputs):
    names, i = [], 0
    while i < len(template):
        if template.startswith("{{", i) or template.startswith("}}", i):
            i += 2
        elif template[i] == "{":
            j = template.index("}", i)
            if template[i + 1:j] not in names:
                names.append(template[i + 1:j])
            i = j + 1
        else:
            i += 1
    out = []
    for vals in inputs:
        missing = sorted(n for n in names if n not in vals)
        unused = sorted(k for k in vals if k not in names)
        filled = None if missing else template.format(**{n: vals[n] for n in names})
        out.append((filled if filled else "error: missing " + ", ".join(missing), unused))
    return out


@O
def fill_template(template, inputs):
    import string
    names = {f for _, f, _, _ in string.Formatter().parse(template) if f}
    out = []
    for vals in inputs:
        missing = sorted(names - vals.keys())
        out.append((f"error: missing {', '.join(missing)}" if missing else template.format(**vals), sorted(vals.keys() - names)))
    return out


Q(None, "A Semantic Cache for LLM Answers", "Medium", "Reuse answers to similar questions",
  "Cache LLM answers by question <b>embedding</b>: if a new question's cosine similarity to a cached question is at least <code>threshold</code>, reuse that answer; otherwise call the model and cache it. Return <code>(for each question: 'hit:<i>i</i>' with the cached question's index or 'miss', model calls)</code>. Too low a threshold returns wrong answers; too high saves nothing.",
  [(([[0.9, 0.1, 0.0], [0.88, 0.12, 0.02], [0.1, 0.9, 0.1], [0.6, 0.6, 0.0], [0.12, 0.88, 0.1]], 0.97), (['miss', 'hit:0', 'miss', 'miss', 'hit:2'], 3)), (([[0.9, 0.1, 0.0], [0.88, 0.12, 0.02], [0.1, 0.9, 0.1], [0.6, 0.6, 0.0], [0.12, 0.88, 0.1]], 0.75), (['miss', 'hit:0', 'miss', 'hit:0', 'hit:2'], 2))],
  ("Compare with every cached question in a loop.", "O(n² · d)", "O(n · d)"),
  ("A matrix of cached normalised vectors and one dot product.", "O(n² · d)", "O(n · d)"),
  viz=(([[1.0, 0.0], [0.99, 0.1]], 0.9)))


@B
def semantic_cache(questions, threshold):
    cache, out = [], []
    for q in questions:
        best, best_sim = None, -1.0
        for i, c in cache:
            sim = sum(a * b for a, b in zip(q, c)) / (math.sqrt(sum(a * a for a in q)) * math.sqrt(sum(b * b for b in c)))
            if sim > best_sim:
                best, best_sim = i, sim
        if best is not None and best_sim >= threshold:
            out.append(f"hit:{best}")
        else:
            out.append("miss")
            cache.append((len(out) - 1, q))
    return (out, sum(o == "miss" for o in out))


@O
def semantic_cache(questions, threshold):
    keys, ids, out = [], [], []
    for n, q in enumerate(questions):
        v = normalise(q)
        if keys:
            sims = np.array(keys) @ v
            j = int(np.argmax(sims))
            if sims[j] >= threshold:
                out.append(f"hit:{ids[j]}")
                continue
        out.append("miss")
        keys.append(v)
        ids.append(n)
    return (out, out.count("miss"))


Q(None, "Choose a Vector Store", "Easy", "Match the tool to the job",
  "Recommend a store for each situation (a dict of facts) using these rules in order: already on Postgres and under 10 million vectors → <code>'pgvector'</code>; a prototype or notebook → <code>'Chroma'</code>; in-process search only, no server → <code>'FAISS'</code>; need no ops at all → <code>'managed (e.g. Pinecone)'</code>; otherwise → <code>'Qdrant or Weaviate'</code>.",
  [(([{"postgres": True, "vectors": 2_000_000}, {"prototype": True}, {"postgres": True, "vectors": 80_000_000, "no_ops": True}, {"in_process": True, "vectors": 5_000_000}, {"vectors": 300_000_000, "filters": True}],), ['pgvector', 'Chroma', 'managed (e.g. Pinecone)', 'FAISS', 'Qdrant or Weaviate'])],
  ("An if/elif chain.", "O(n)", "O(1)"),
  ("A rule table checked in order.", "O(n · r)", "O(1)"),
  viz=(([{"prototype": True}],)))


@B
def choose_store(cases):
    out = []
    for c in cases:
        if c.get("postgres") and c.get("vectors", 0) < 10_000_000:
            out.append("pgvector")
        elif c.get("prototype"):
            out.append("Chroma")
        elif c.get("in_process"):
            out.append("FAISS")
        elif c.get("no_ops"):
            out.append("managed (e.g. Pinecone)")
        else:
            out.append("Qdrant or Weaviate")
    return out


@O
def choose_store(cases):
    rules = [(lambda c: c.get("postgres") and c.get("vectors", 0) < 10_000_000, "pgvector"), (lambda c: c.get("prototype"), "Chroma"),
             (lambda c: c.get("in_process"), "FAISS"), (lambda c: c.get("no_ops"), "managed (e.g. Pinecone)")]
    return [next((name for test, name in rules if test(c)), "Qdrant or Weaviate") for c in cases]


Q(None, "A Retriever With a Score Threshold", "Easy", "search_type='similarity_score_threshold'",
  "Frameworks wrap a vector store as a <b>retriever</b>: return at most <code>k</code> documents, but only those with similarity ≥ <code>threshold</code> — so an off-topic question retrieves nothing instead of junk. Given each question's similarity scores, return the retrieved ids per question (highest score first, ties by id).",
  [(([{"d1": 0.82, "d2": 0.79, "d3": 0.41, "d4": 0.77}, {"d1": 0.31, "d2": 0.28, "d3": 0.35}, {"d5": 0.91, "d6": 0.90}], 0.75, 2), [['d1', 'd2'], [], ['d5', 'd6']])],
  ("Sort, then filter in a loop.", "O(q · n log n)", "O(n)"),
  ("A comprehension over sorted items.", "O(q · n log n)", "O(n)"),
  viz=(([{"a": 0.9, "b": 0.1}], 0.5, 2)))


@B
def threshold_retriever(score_sets, threshold, k):
    out = []
    for scores in score_sets:
        ranked = sorted(scores, key=lambda d: (-scores[d], d))
        got = []
        for d in ranked:
            if scores[d] >= threshold and len(got) < k:
                got.append(d)
        out.append(got)
    return out


@O
def threshold_retriever(score_sets, threshold, k):
    return [[d for d in sorted(s, key=lambda d: (-s[d], d)) if s[d] >= threshold][:k] for s in score_sets]
