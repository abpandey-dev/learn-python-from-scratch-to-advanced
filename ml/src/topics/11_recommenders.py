from lib import *
import math
from collections import Counter
from itertools import combinations
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import ndcg_score, mean_squared_error, jaccard_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


TOPIC(
    id="recommenders", title="Recommender Systems", glyph="★",
    blurb="Suggest what a user will like next: popularity baselines, similarity measures, user- and item-based collaborative filtering, content-based TF-IDF, matrix factorisation, market-basket rules, cold start, and the ranking metrics used to judge recommenders.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">R = df.pivot_table(index="user", columns="item", values="rating")   # user × item matrix
sim = cosine_similarity(R.fillna(0).T)             # item × item similarity
scores = R.fillna(0) @ sim                         # item-based CF scores
U, s, Vt = np.linalg.svd(R_filled, full_matrices=False)   # latent factors
TfidfVectorizer().fit_transform(descriptions)      # content-based
NearestNeighbors(metric="cosine").fit(X).kneighbors(x, k)
ndcg_score([true_relevance], [scores], k=10)       # ranking quality</code></pre>
""")

# ratings matrix: rows = users u0..u4, columns = items i0..i4, 0 = not rated
R = [[5, 3, 0, 1, 4],
     [4, 0, 0, 1, 5],
     [1, 1, 0, 5, 0],
     [0, 1, 5, 4, 0],
     [5, 4, 1, 0, 4]]
ITEMS = ["i0", "i1", "i2", "i3", "i4"]


Q(None, "Most Popular Unseen Items", "Easy", "Popularity baseline",
  "Rank items by how many users rated them (ties: lower index first) and return the top <code>n</code> item indexes that <code>user</code> hasn't rated.",
  [((R, 2, 2), [4, 2]), ((R, 1, 1), [1])],
  ("Count ratings per column in a loop, sort, skip seen ones.", "O(ui + i log i)", "O(i)"),
  ("NumPy: <code>(R &gt; 0).sum(axis=0)</code> and a stable <code>argsort</code>.", "O(ui + i log i)", "O(i)"),
  viz=(R, 2, 2))


@B
def popular(R, user, n):
    counts = [sum(1 for row in R if row[j] > 0) for j in range(len(R[0]))]
    order = sorted(range(len(counts)), key=lambda j: (-counts[j], j))
    return [j for j in order if R[user][j] == 0][:n]


@O
def popular(R, user, n):
    A = np.array(R)
    order = np.argsort(-(A > 0).sum(axis=0), kind="stable")
    return [int(j) for j in order if A[user, j] == 0][:n]


Q(None, "Cosine Similarity of Two Users", "Easy", "Angle between vectors",
  "Return the cosine similarity of users <code>a</code> and <code>b</code>'s rating rows (0 = not rated), rounded to 4.",
  [((R, 0, 1), 0.8859), ((R, 0, 2), 0.3503)],
  ("Dot product ÷ (length × length).", "O(i)", "O(1)"),
  ("<code>cosine_similarity</code>.", "O(i)", "O(1)"),
  viz=(R, 0, 1))


@B
def user_cosine(R, a, b):
    x, y = R[a], R[b]
    dot = sum(p * q for p, q in zip(x, y))
    return round(dot / (math.sqrt(sum(p * p for p in x)) * math.sqrt(sum(q * q for q in y))), 4)


@O
def user_cosine(R, a, b):
    A = np.array(R, float)
    return round(float(cosine_similarity(A[[a]], A[[b]])[0, 0]), 4)


Q(None, "Mean-Centred (Pearson) Similarity", "Medium", "Handling harsh and generous raters",
  "Subtract each user's mean of their <b>rated</b> items, then take cosine over items both users rated. Return it rounded to 4 (0 if undefined).",
  [((R, 0, 1), 0.8836), ((R, 0, 2), -0.8561)],
  ("Means over non-zero entries, then a loop over co-rated items.", "O(i)", "O(i)"),
  ("Boolean masks select co-rated items; NumPy does the rest.", "O(i)", "O(i)"),
  viz=(R, 0, 2))


@B
def pearson_sim(R, a, b):
    x, y = R[a], R[b]
    mx = sum(v for v in x if v) / sum(1 for v in x if v)
    my = sum(v for v in y if v) / sum(1 for v in y if v)
    num = sx = sy = 0
    for p, q in zip(x, y):
        if p and q:
            num += (p - mx) * (q - my)
            sx += (p - mx) ** 2
            sy += (q - my) ** 2
    return round(num / math.sqrt(sx * sy), 4) if sx and sy else 0


@O
def pearson_sim(R, a, b):
    A = np.array(R, float)
    x, y = A[a], A[b]
    both = (x > 0) & (y > 0)
    dx, dy = x[both] - x[x > 0].mean(), y[both] - y[y > 0].mean()
    den = np.sqrt((dx ** 2).sum() * (dy ** 2).sum())
    return round(float(dx @ dy / den), 4) if den else 0


Q(None, "Most Similar Item", "Easy", "Item-item cosine",
  "Return the index of the item most similar to <code>item</code> by cosine similarity of rating columns (excluding itself; lowest index on ties).",
  [((R, 0), 4), ((R, 2), 3)],
  ("Cosine between the item's column and every other column.", "O(ui)", "O(u)"),
  ("<code>cosine_similarity(A.T)</code>, blank the diagonal, <code>argmax</code>.", "O(u i²)", "O(i²)"),
  viz=(R, 0))


@B
def similar_item(R, item):
    col = lambda j: [row[j] for row in R]
    x = col(item)
    best, best_s = None, -2
    for j in range(len(R[0])):
        if j == item:
            continue
        y = col(j)
        s = sum(p * q for p, q in zip(x, y)) / (math.sqrt(sum(p * p for p in x)) * math.sqrt(sum(q * q for q in y)))
        if s > best_s + 1e-12:
            best, best_s = j, s
    return best


@O
def similar_item(R, item):
    S = cosine_similarity(np.array(R, float).T)
    np.fill_diagonal(S, -np.inf)
    return int(S[item].argmax())


Q(None, "User-Based Rating Prediction", "Medium", "Neighbours' weighted average",
  "Predict <code>user</code>'s rating of <code>item</code> as the cosine-weighted average of the ratings from the <code>k</code> most similar users who rated it. Round to 4.",
  [((R, 1, 1, 2), 3.4778), ((R, 2, 4, 2), 4.4327)],
  ("Score every other user, keep raters of the item, take the top k, weighted average.", "O(u i)", "O(u)"),
  ("Similarity row from <code>cosine_similarity</code>, then NumPy masking and <code>argsort</code>.", "O(u i)", "O(u)"),
  viz=(R, 1, 1, 2))


@B
def predict_user_based(R, user, item, k):
    def cos(x, y):
        return sum(p * q for p, q in zip(x, y)) / (math.sqrt(sum(p * p for p in x)) * math.sqrt(sum(q * q for q in y)))
    cands = [(cos(R[user], R[v]), R[v][item]) for v in range(len(R)) if v != user and R[v][item] > 0]
    cands.sort(key=lambda t: -t[0])
    top = cands[:k]
    return round(sum(s * r for s, r in top) / sum(s for s, _ in top), 4)


@O
def predict_user_based(R, user, item, k):
    A = np.array(R, float)
    sims = cosine_similarity(A[[user]], A)[0]
    raters = [v for v in np.argsort(-sims, kind="stable") if v != user and A[v, item] > 0][:k]
    w = sims[raters]
    return round(float(w @ A[raters, item] / w.sum()), 4)


Q(None, "Item-Based Recommendations", "Medium", "Score = ratings × item similarity",
  "Score each unrated item for <code>user</code> as Σ over rated items of rating × cosine(item, rated item) ÷ Σ similarities. Return the top <code>n</code> unrated item indexes.",
  [((R, 1, 2), [1, 2]), ((R, 3, 1), [0])],
  ("Double loop over unrated × rated items.", "O(i² u)", "O(i²)"),
  ("One matrix product with the item-similarity matrix.", "O(i² u)", "O(i²)"),
  viz=(R, 1, 2))


@B
def item_based(R, user, n):
    cols = [[row[j] for row in R] for j in range(len(R[0]))]
    cos = lambda x, y: sum(p * q for p, q in zip(x, y)) / (math.sqrt(sum(p * p for p in x)) * math.sqrt(sum(q * q for q in y)))
    rated = [j for j in range(len(cols)) if R[user][j] > 0]
    scores = {}
    for j in range(len(cols)):
        if R[user][j] == 0:
            sims = [cos(cols[j], cols[r]) for r in rated]
            scores[j] = sum(s * R[user][r] for s, r in zip(sims, rated)) / sum(sims)
    return sorted(scores, key=lambda j: (-scores[j], j))[:n]


@O
def item_based(R, user, n):
    A = np.array(R, float)
    S = cosine_similarity(A.T)
    rated = A[user] > 0
    scores = (S[:, rated] @ A[user, rated]) / S[:, rated].sum(axis=1)
    order = np.argsort(-scores, kind="stable")
    return [int(j) for j in order if not rated[j]][:n]


DOCS = ["space adventure with aliens", "romantic comedy in paris", "aliens invade earth adventure",
        "paris love story comedy", "documentary about space telescopes"]


Q(None, "Content-Based: Similar Descriptions", "Medium", "TF-IDF",
  "Using TF-IDF (smooth idf, L2-normalised rows, like sklearn) of item descriptions, return the index of the description most similar to <code>docs[i]</code>.",
  [((DOCS, 0), 2), ((DOCS, 1), 3)],
  ("Build term counts and idf = ln((1 + n)/(1 + df)) + 1 by hand, normalise, then dot products.", "O(n · words)", "O(n · vocab)"),
  ("<code>TfidfVectorizer</code> plus <code>cosine_similarity</code>.", "O(n · words)", "O(n · vocab)"),
  viz=(DOCS, 0))


@B
def similar_doc(docs, i):
    toks = [d.split() for d in docs]
    vocab = sorted({w for t in toks for w in t})
    n = len(docs)
    idf = {w: math.log((1 + n) / (1 + sum(w in t for t in toks))) + 1 for w in vocab}
    vecs = []
    for t in toks:
        v = [t.count(w) * idf[w] for w in vocab]
        norm = math.sqrt(sum(x * x for x in v))
        vecs.append([x / norm for x in v])
    sims = [sum(a * b for a, b in zip(vecs[i], vecs[j])) if j != i else -1 for j in range(n)]
    return max(range(n), key=lambda j: sims[j])


@O
def similar_doc(docs, i):
    X = TfidfVectorizer().fit_transform(docs)
    s = cosine_similarity(X[i], X)[0]
    s[i] = -1
    return int(s.argmax())


Q(None, "Jaccard Similarity for Clicks", "Easy", "Implicit feedback",
  "For yes/no interactions, similarity = |both| ÷ |either|. Return the Jaccard similarity of users <code>a</code> and <code>b</code> (rated = interacted), rounded to 4.",
  [((R, 0, 1), 0.75), ((R, 2, 3), 0.5)],
  ("Sets of rated items: intersection ÷ union.", "O(i)", "O(i)"),
  ("<code>jaccard_score</code> on the boolean rows.", "O(i)", "O(i)"),
  viz=(R, 0, 1))


@B
def jaccard(R, a, b):
    x = {j for j, v in enumerate(R[a]) if v}
    y = {j for j, v in enumerate(R[b]) if v}
    return round(len(x & y) / len(x | y), 4)


@O
def jaccard(R, a, b):
    A = np.array(R) > 0
    return round(float(jaccard_score(A[a], A[b])), 4)


Q(None, "Rank-1 Matrix Factorisation", "Hard", "Latent factors",
  "Approximate the ratings matrix (0s included) by its best rank-1 matrix σ·u·vᵀ and return the reconstructed value at (<code>user</code>, <code>item</code>), rounded to 4.",
  [((R, 1, 1), 2.1921), ((R, 3, 0), 1.1804)],
  ("Power iteration: repeat v ← AᵀAv / ‖AᵀAv‖ until it settles; then u = Av/σ.", "O(iters · ui)", "O(u + i)"),
  ("<code>np.linalg.svd</code> and keep the largest singular value.", "O(ui · min(u, i))", "O(ui)"),
  viz=(R, 1, 1))


@B
def rank1(R, user, item):
    A = np.array(R, float)
    v = np.ones(A.shape[1])
    for _ in range(500):
        w = A.T @ (A @ v)
        v = w / math.sqrt(float(w @ w))
    Av = A @ v
    sigma = math.sqrt(float(Av @ Av))
    u = Av / sigma
    return round(float(sigma * u[user] * v[item]), 4)


@O
def rank1(R, user, item):
    U, s, Vt = np.linalg.svd(np.array(R, float), full_matrices=False)
    return round(float(s[0] * U[user, 0] * Vt[0, item]), 4)


Q(None, "Precision@k and Recall@k", "Easy", "Did we recommend the right things?",
  "Given a ranked list of recommendations and the set of relevant items, return <code>(precision@k, recall@k)</code> rounded to 4.",
  [((["a", "b", "c", "d", "e"], ["b", "e", "x"], 3), (0.3333, 0.3333)), ((["a", "b", "c", "d", "e"], ["b", "e", "x"], 5), (0.4, 0.6667))],
  ("Count hits in the first k.", "O(k)", "O(r)"),
  ("A set intersection.", "O(k)", "O(r)"),
  viz=(["a", "b", "c", "d", "e"], ["b", "e", "x"], 3))


@B
def precision_recall_at_k(ranked, relevant, k):
    hits = 0
    for item in ranked[:k]:
        if item in relevant:
            hits += 1
    return (round(hits / k, 4), round(hits / len(relevant), 4))


@O
def precision_recall_at_k(ranked, relevant, k):
    hits = len(set(ranked[:k]) & set(relevant))
    return (round(hits / k, 4), round(hits / len(relevant), 4))


Q(None, "NDCG@k", "Medium", "Position-aware quality",
  "Return NDCG@k for recommendation <code>scores</code> against graded <code>relevance</code> (same item order), using the standard log₂ discount. Round to 4.",
  [(([3, 2, 0, 1, 2], [0.9, 0.8, 0.7, 0.6, 0.1], 3), 0.81), (([3, 2, 0, 1, 2], [0.1, 0.2, 0.9, 0.8, 0.3], 5), 0.6417)],
  ("DCG = Σ rel / log₂(rank + 1) over the top k by score; divide by the DCG of the ideal order.", "O(n log n)", "O(n)"),
  ("<code>sklearn.metrics.ndcg_score</code>.", "O(n log n)", "O(n)"),
  viz=([3, 2, 0, 1, 2], [0.9, 0.8, 0.7, 0.6, 0.1], 3))


@B
def ndcg(relevance, scores, k):
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
    dcg = sum(relevance[i] / math.log2(r + 2) for r, i in enumerate(order))
    ideal = sorted(relevance, reverse=True)[:k]
    idcg = sum(rel / math.log2(r + 2) for r, rel in enumerate(ideal))
    return round(dcg / idcg, 4)


@O
def ndcg(relevance, scores, k):
    return round(float(ndcg_score([relevance], [scores], k=k)), 4)


Q(None, "Hit Rate and Mean Reciprocal Rank", "Easy", "Leave-one-out evaluation",
  "Each user has one held-out item and a ranked list. Return <code>(hit rate@k, MRR)</code>, where MRR uses 1/rank of the held-out item (0 if absent). Round to 4.",
  [(([["a", "b", "c"], ["c", "a", "b"], ["b", "c", "d"]], ["b", "b", "a"], 2), (0.3333, 0.2778))],
  ("Find each item's position with a loop.", "O(u·L)", "O(1)"),
  ("<code>list.index</code> in a comprehension, then NumPy means.", "O(u·L)", "O(u)"),
  viz=([["a", "b", "c"], ["c", "a", "b"], ["b", "c", "d"]], ["b", "b", "a"], 2))


@B
def hit_mrr(lists, held_out, k):
    hits = rr = 0
    for ranked, target in zip(lists, held_out):
        for pos, item in enumerate(ranked):
            if item == target:
                rr += 1 / (pos + 1)
                if pos < k:
                    hits += 1
                break
    n = len(lists)
    return (round(hits / n, 4), round(rr / n, 4))


@O
def hit_mrr(lists, held_out, k):
    ranks = np.array([L.index(t) + 1 if t in L else np.inf for L, t in zip(lists, held_out)])
    return (round(float((ranks <= k).mean()), 4), round(float((1 / ranks).mean()), 4))


def pop_rank(R, user, n):
    A = np.array(R)
    order = np.argsort(-(A > 0).sum(axis=0), kind="stable")
    return [int(j) for j in order if A[user, j] == 0][:n]


def item_rank(R, user, n):
    A = np.array(R, float)
    S = cosine_similarity(A.T)
    rated = A[user] > 0
    scores = (S[:, rated] @ A[user, rated]) / S[:, rated].sum(axis=1)
    return [int(j) for j in np.argsort(-scores, kind="stable") if not rated[j]][:n]


Q(None, "Cold Start Fallback", "Easy", "New users",
  "If <code>user</code> has rated fewer than <code>min_ratings</code> items, recommend the <code>n</code> most popular unseen items; otherwise use item-based scores. Return <code>(strategy, items)</code>.",
  [(([[5, 0, 0, 0, 0]] + R[1:], 0, 2, 2), ('popular', [1, 3])), ((R, 1, 2, 1), ('item-based', [1]))],
  ("An if / else choosing between the popularity and item-based helpers.", "O(i² u)", "O(i²)"),
  ("The same choice as one conditional expression; <code>np.count_nonzero</code> counts the ratings.", "O(i² u)", "O(i²)"),
  viz=([[5, 0, 0, 0, 0]] + R[1:], 0, 2, 2))


@B
def cold_start(R, user, min_ratings, n):
    if sum(1 for v in R[user] if v > 0) < min_ratings:
        return ("popular", pop_rank(R, user, n))
    return ("item-based", item_rank(R, user, n))


@O
def cold_start(R, user, min_ratings, n):
    is_new = np.count_nonzero(R[user]) < min_ratings
    return ("popular", pop_rank(R, user, n)) if is_new else ("item-based", item_rank(R, user, n))


BASKETS = [["bread", "milk"], ["bread", "butter", "milk"], ["beer", "chips"], ["bread", "butter"], ["milk", "butter", "bread", "jam"]]


Q(None, "Frequently Bought Together", "Easy", "Co-occurrence",
  "Return the pair of products (alphabetical) that appears together in the most baskets, with its count (alphabetically first pair on ties).",
  [((BASKETS,), (('bread', 'butter'), 3))],
  ("<code>combinations</code> of each sorted basket into a Counter.", "O(b · k²)", "O(p²)"),
  ("A basket × product 0/1 matrix B; Bᵀ B counts every pair at once.", "O(b p²)", "O(p²)"),
  viz=(BASKETS,))


@B
def top_pair(baskets):
    c = Counter()
    for b in baskets:
        for pair in combinations(sorted(set(b)), 2):
            c[pair] += 1
    best = min(c, key=lambda p: (-c[p], p))
    return (best, c[best])


@O
def top_pair(baskets):
    B = pd.DataFrame([{p: 1 for p in b} for b in baskets]).fillna(0).astype(int)
    B = B[sorted(B.columns)]
    C = B.T @ B
    M = np.triu(C.to_numpy(), k=1)
    i, j = np.unravel_index(M.argmax(), M.shape)
    return ((C.index[i], C.columns[j]), int(M[i, j]))


Q(None, "Association Rule Metrics", "Medium", "Support, confidence, lift",
  "For the rule A → B return <code>(support, confidence, lift)</code> rounded to 4: support = P(A and B), confidence = P(B | A), lift = confidence ÷ P(B).",
  [((BASKETS, "butter", "bread"), (0.6, 1.0, 1.25)), ((BASKETS, "milk", "jam"), (0.2, 0.3333, 1.6667))],
  ("Count baskets with A, with B, with both.", "O(b k)", "O(1)"),
  ("Boolean columns of a one-hot basket DataFrame, then means.", "O(b p)", "O(b p)"),
  viz=(BASKETS, "butter", "bread"))


@B
def rule(baskets, a, b):
    n = len(baskets)
    na = sum(a in x for x in baskets)
    nb = sum(b in x for x in baskets)
    nab = sum(a in x and b in x for x in baskets)
    conf = nab / na
    return (round(nab / n, 4), round(conf, 4), round(conf / (nb / n), 4))


@O
def rule(baskets, a, b):
    B = pd.DataFrame([{p: True for p in x} for x in baskets]).fillna(False).astype(bool)
    both = (B[a] & B[b]).mean()
    conf = both / B[a].mean()
    return (round(both, 4), round(conf, 4), round(conf / B[b].mean(), 4))


Q(None, "Leave-Last-Out Split", "Medium", "Time-aware evaluation",
  "<code>events</code> are (user, item, time). Hold out each user's latest event as test (users with one event stay entirely in train). Return <code>(train size, test pairs sorted)</code>.",
  [(([("u1", "a", 1), ("u1", "b", 5), ("u2", "a", 2), ("u1", "c", 3), ("u2", "c", 9), ("u3", "b", 4)],), (4, [('u1', 'b'), ('u2', 'c')]))],
  ("Find each user's max time in a dict, then split.", "O(n)", "O(n)"),
  ("<code>groupby('user')['time'].transform('max')</code> plus a count filter.", "O(n)", "O(n)"),
  viz=([("u1", "a", 1), ("u1", "b", 5), ("u2", "a", 2), ("u1", "c", 3), ("u2", "c", 9), ("u3", "b", 4)],))


@B
def leave_last_out(events):
    last, count = {}, {}
    for u, i, t in events:
        count[u] = count.get(u, 0) + 1
        if u not in last or t > last[u][1]:
            last[u] = (i, t)
    test = sorted((u, last[u][0]) for u in last if count[u] > 1)
    return (len(events) - len(test), test)


@O
def leave_last_out(events):
    df = pd.DataFrame(events, columns=["user", "item", "time"])
    is_last = df["time"] == df.groupby("user")["time"].transform("max")
    multi = df.groupby("user")["item"].transform("size") > 1
    test = df[is_last & multi]
    return (len(df) - len(test), sorted(zip(test["user"], test["item"])))


Q(None, "Catalogue Coverage", "Easy", "Beyond accuracy",
  "Return the % of the catalogue (<code>n_items</code>) that appears in at least one user's recommendation list, rounded to 1.",
  [(([["a", "b"], ["a", "c"], ["a", "b"]], 10), 30.0)],
  ("Add every item to a set in a loop.", "O(u k)", "O(items)"),
  ("A set comprehension.", "O(u k)", "O(items)"),
  viz=([["a", "b"], ["a", "c"], ["a", "b"]], 10))


@B
def coverage(lists, n_items):
    seen = set()
    for L in lists:
        for item in L:
            seen.add(item)
    return round(len(seen) / n_items * 100, 1)


@O
def coverage(lists, n_items):
    return round(len({i for L in lists for i in L}) / n_items * 100, 1)


Q(None, "Baseline Predictor With Biases", "Medium", "μ + user bias + item bias",
  "Predict rating = global mean + (user's mean − global mean) + (item's mean − global mean), using only rated (non-zero) entries. Clip to [1, 5] and round to 4.",
  [((R, 1, 1), 2.4069), ((R, 2, 2), 2.1569)],
  ("Three averages with loops.", "O(ui)", "O(1)"),
  ("A masked NumPy array: <code>np.nanmean</code> over rows and columns.", "O(ui)", "O(ui)"),
  viz=(R, 1, 1))


@B
def bias_predict(R, user, item):
    vals = [v for row in R for v in row if v]
    mu = sum(vals) / len(vals)
    ur = [v for v in R[user] if v]
    ir = [row[item] for row in R if row[item]]
    p = mu + (sum(ur) / len(ur) - mu) + (sum(ir) / len(ir) - mu)
    return round(min(5, max(1, p)), 4)


@O
def bias_predict(R, user, item):
    A = np.array(R, float)
    A[A == 0] = np.nan
    mu = np.nanmean(A)
    p = mu + (np.nanmean(A[user]) - mu) + (np.nanmean(A[:, item]) - mu)
    return round(float(np.clip(p, 1, 5)), 4)


Q(None, "RMSE of Rating Predictions", "Easy", "Rating accuracy",
  "Return the root mean squared error between true and predicted ratings, rounded to 4.",
  [(([4, 3, 5, 2], [3.5, 3, 4, 3]), 0.75)],
  ("Loop over squared errors.", "O(n)", "O(1)"),
  ("<code>sklearn.metrics.mean_squared_error</code>, then the square root.", "O(n)", "O(1)"),
  viz=([4, 3, 5, 2], [3.5, 3, 4, 3]))


@B
def rmse(y, p):
    return round(math.sqrt(sum((a - b) ** 2 for a, b in zip(y, p)) / len(y)), 4)


@O
def rmse(y, p):
    return round(float(np.sqrt(mean_squared_error(y, p))), 4)


Q(None, "k Nearest Items", "Easy", "NearestNeighbors with cosine",
  "Return the indexes of the <code>k</code> items closest to <code>item</code> by cosine distance of rating columns, closest first, excluding the item itself.",
  [((R, 0, 2), [4, 1]), ((R, 3, 2), [2, 1])],
  ("Compute every distance and sort.", "O(ui + i log i)", "O(i)"),
  ("<code>NearestNeighbors(metric='cosine').kneighbors</code>.", "O(ui)", "O(i)"),
  viz=(R, 0, 2))


@B
def nearest_items(R, item, k):
    cols = [[row[j] for row in R] for j in range(len(R[0]))]
    x = cols[item]
    def dist(y):
        return 1 - sum(p * q for p, q in zip(x, y)) / (math.sqrt(sum(p * p for p in x)) * math.sqrt(sum(q * q for q in y)))
    others = [j for j in range(len(cols)) if j != item]
    return sorted(others, key=lambda j: (round(dist(cols[j]), 12), j))[:k]


@O
def nearest_items(R, item, k):
    X = np.array(R, float).T
    nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine").fit(X)
    _, idx = nn.kneighbors(X[[item]])
    return [int(j) for j in idx[0] if j != item][:k]
