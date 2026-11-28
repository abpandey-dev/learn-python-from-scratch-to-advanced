from lib import *
import math
import re
from collections import Counter
from datetime import date

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.manifold import trustworthiness
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder

TOPIC(
    id="applied-ml", title="Applied ML: Features, Anomalies, Text & Vision", glyph="🧰",
    blurb="The practical skills between textbook ML and real projects: one-hot and target encoding, date features, filtering redundant features, spotting leakage, four ways to find anomalies and how to score them, judging a t-SNE/UMAP picture, bag-of-words, Naive Bayes text classification, n-grams, entity tagging and scoring, and the core of object detection — IoU, non-max suppression, matching detections — plus what transfer learning actually trains.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">OneHotEncoder(handle_unknown="ignore")          # categories → columns; unseen → all zeros
TargetEncoder()                                 # category → (smoothed) mean target, cross-fitted
IsolationForest(contamination=0.01)             # anomaly scores without labels
TSNE(n_components=2) / umap.UMAP()              # 2-D pictures of high-dimensional data
CountVectorizer(ngram_range=(1, 2))             # text → word and bigram counts
MultinomialNB().fit(X_counts, y)                # fast, strong text baseline
iou = intersection_area / union_area            # object detection's core measure</code></pre>
<p>In most real projects, good features and clean evaluation beat a fancier model.</p>
""")


Q(None, "One-Hot Encode Categories", "Easy", "Including unseen values",
  "Learn the categories from <code>train</code> (sorted), then one-hot encode both lists. A category never seen in training becomes a row of zeros instead of crashing — that's <code>handle_unknown='ignore'</code>. Return <code>(categories, train rows, test rows)</code>.",
  [((["red", "green", "blue", "green"], ["green", "purple", "red"]), (['blue', 'green', 'red'], [[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 0], [0, 0, 0], [0, 0, 1]]))],
  ("Build a column index and fill lists.", "O(n · c)", "O(n · c)"),
  ("<code>OneHotEncoder(handle_unknown='ignore', sparse_output=False)</code>.", "O(n · c)", "O(n · c)"),
  viz=((["a", "b"], ["c"])))


@B
def one_hot(train, test):
    cats = sorted(set(train))
    def enc(values):
        return [[1 if v == c else 0 for c in cats] for v in values]
    return (cats, enc(train), enc(test))


@O
def one_hot(train, test):
    oh = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(np.array(train).reshape(-1, 1))
    return (list(oh.categories_[0]), oh.transform(np.array(train).reshape(-1, 1)).astype(int).tolist(),
            oh.transform(np.array(test).reshape(-1, 1)).astype(int).tolist())


Q(None, "Smoothed Target Encoding", "Medium", "Turn categories into numbers carefully",
  "Replace each category with its mean target, pulled towards the overall mean so rare categories don't get extreme values: <code>(sum_y + m × prior) / (count + m)</code>. Return the encoding per category (rounded to 4) and the encoded <code>test</code> values (unseen categories get the prior). In real projects, compute it out-of-fold to avoid leaking the target.",
  [((["Pune", "Pune", "Goa", "Delhi", "Pune", "Delhi", "Goa", "Goa", "Pune", "Agra"], [1, 0, 1, 0, 1, 0, 1, 1, 1, 1], 2, ["Goa", "Agra", "Kochi"]), ({'Agra': 0.8, 'Delhi': 0.35, 'Goa': 0.88, 'Pune': 0.7333}, [0.88, 0.8, 0.7]))],
  ("Dicts of sums and counts.", "O(n)", "O(c)"),
  ("<code>groupby().agg(['sum', 'count'])</code>.", "O(n)", "O(c)"),
  viz=((["a", "a", "b"], [1, 0, 1], 1, ["b"])))


@B
def target_encode(cats, y, m, test):
    prior = sum(y) / len(y)
    sums, counts = {}, {}
    for c, t in zip(cats, y):
        sums[c] = sums.get(c, 0) + t
        counts[c] = counts.get(c, 0) + 1
    enc = {c: round((sums[c] + m * prior) / (counts[c] + m), 4) for c in sorted(sums)}
    return (enc, [enc.get(c, round(prior, 4)) for c in test])


@O
def target_encode(cats, y, m, test):
    df = pd.DataFrame({"c": cats, "y": y})
    prior = df["y"].mean()
    g = df.groupby("c")["y"].agg(["sum", "count"])
    enc = ((g["sum"] + m * prior) / (g["count"] + m)).round(4)
    return (enc.to_dict(), [float(enc.get(c, round(prior, 4))) for c in test])


Q(None, "Features From Dates", "Easy", "Day of week, month, weekend, recency",
  "For each date string, return <code>(weekday 0=Monday, month, is_weekend, days before ref)</code>. Raw dates are useless to most models; these derived features carry the signal (weekly patterns, seasonality, recency).",
  [((["2026-11-27", "2026-11-29", "2026-01-01", "2025-12-25"], "2026-11-30"), [(4, 11, False, 3), (6, 11, True, 1), (3, 1, False, 333), (3, 12, False, 340)])],
  ("<code>date.fromisoformat</code> in a loop.", "O(n)", "O(n)"),
  ("pandas <code>.dt</code> accessors on a whole column.", "O(n)", "O(n)"),
  viz=((["2026-01-03"], "2026-01-10")))


@B
def date_features(days, ref):
    r = date.fromisoformat(ref)
    out = []
    for d in days:
        x = date.fromisoformat(d)
        out.append((x.weekday(), x.month, x.weekday() >= 5, (r - x).days))
    return out


@O
def date_features(days, ref):
    s = pd.to_datetime(pd.Series(days))
    df = pd.DataFrame({"wd": s.dt.dayofweek, "m": s.dt.month, "we": s.dt.dayofweek >= 5, "age": (pd.Timestamp(ref) - s).dt.days})
    return [(int(a), int(b), bool(c), int(d)) for a, b, c, d in df.itertuples(index=False)]


Q(None, "Drop Useless and Redundant Features", "Medium", "Variance and correlation filters",
  "First drop features whose variance (population, ddof = 0) is below <code>var_min</code>; then, going left to right, drop any remaining feature whose absolute correlation with an already-kept feature is above <code>corr_max</code>. Return the kept column indexes.",
  [(([[1.0, 5.0, 2.0, 4.1, 0.0], [2.0, 5.0, 4.1, 3.9, 0.1], [3.0, 5.0, 5.9, 4.0, 0.0], [4.0, 5.0, 8.2, 4.2, 0.1], [5.0, 5.0, 9.8, 3.8, 0.0]], 0.01, 0.95), [0, 3])],
  ("Compute variances and correlations by hand.", "O(n · d²)", "O(d)"),
  ("<code>VarianceThreshold</code>, then <code>np.corrcoef</code>.", "O(n · d²)", "O(d²)"),
  viz=(([[1.0, 2.0], [2.0, 4.0], [3.0, 6.1]], 0.0, 0.9)))


@B
def select_features(X, var_min, corr_max):
    cols = list(zip(*X))
    def var(c):
        m = sum(c) / len(c)
        return sum((v - m) ** 2 for v in c) / len(c)
    def corr(a, b):
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        return cov / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    kept = []
    for j, c in enumerate(cols):
        if var(c) < var_min:
            continue
        if all(abs(corr(c, cols[k])) <= corr_max for k in kept):
            kept.append(j)
    return kept


@O
def select_features(X, var_min, corr_max):
    X = np.array(X)
    alive = np.flatnonzero(VarianceThreshold(var_min).fit(X).get_support())
    C = np.abs(np.corrcoef(X[:, alive], rowvar=False))
    kept = []
    for i, j in enumerate(alive):
        if all(C[i, list(alive).index(k)] <= corr_max for k in kept):
            kept.append(int(j))
    return kept


Q(None, "Spot Leaky Features", "Medium", "Too good to be true",
  "A feature that predicts the target almost perfectly usually leaks it — it was recorded <i>after</i> the outcome (e.g. <code>refund_issued</code> when predicting churn). Return <code>(feature, |correlation| rounded to 3)</code> for features with |correlation| with the target above <code>limit</code>, highest first.",
  [(({"tenure_months": [3, 40, 12, 1, 60, 8, 24, 2], "support_tickets": [5, 0, 2, 6, 1, 4, 1, 7], "cancel_page_visits": [4, 0, 1, 5, 0, 3, 0, 6], "account_closed_flag": [1, 0, 0, 1, 0, 1, 0, 1], "plan_price": [10, 30, 20, 10, 30, 20, 20, 10]}, [1, 0, 0, 1, 0, 1, 0, 1], 0.95), [('account_closed_flag', 1.0)])],
  ("Pearson correlation by hand per feature.", "O(f · n)", "O(f)"),
  ("<code>np.corrcoef</code> per feature.", "O(f · n)", "O(f)"),
  viz=(({"a": [1, 0, 1], "b": [3, 2, 9]}, [1, 0, 1], 0.9)))


@B
def leaky_features(features, target, limit):
    out = []
    my = sum(target) / len(target)
    for name, xs in features.items():
        mx = sum(xs) / len(xs)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, target))
        r = cov / math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in target))
        if abs(r) > limit:
            out.append((name, round(abs(r), 3)))
    return sorted(out, key=lambda x: -x[1])


@O
def leaky_features(features, target, limit):
    r = {n: abs(np.corrcoef(v, target)[0, 1]) for n, v in features.items()}
    return sorted(((n, round(float(v), 3)) for n, v in r.items() if v > limit), key=lambda x: -x[1])


AMOUNTS = [120, 95, 130, 110, 105, 98, 2400, 115, 101, 125, 90, 108, 15, 112, 99, 118, 1050, 104]


Q(None, "Z-Score Outliers", "Easy", "Distance from the mean in standard deviations",
  "Return the indexes of values whose z-score (population standard deviation) has absolute value above <code>limit</code>. Notice how one huge value inflates the standard deviation and hides others: the second test removes the 2,400 and the 1,050 suddenly appears. That's the reason for the robust methods next.",
  [((AMOUNTS, 2.0), [6]), (([v if v != 2400 else 100 for v in AMOUNTS], 2.0), [16])],
  ("Mean and standard deviation by hand.", "O(n)", "O(n)"),
  ("<code>scipy.stats.zscore</code>.", "O(n)", "O(n)"),
  viz=(([1, 2, 3, 50], 1.5)))


@B
def zscore_outliers(values, limit):
    m = sum(values) / len(values)
    sd = math.sqrt(sum((v - m) ** 2 for v in values) / len(values))
    return [i for i, v in enumerate(values) if abs((v - m) / sd) > limit]


@O
def zscore_outliers(values, limit):
    return np.flatnonzero(np.abs(stats.zscore(values)) > limit).tolist()


Q(None, "Tukey's IQR Fences", "Easy", "The box-plot rule",
  "Compute Q1 and Q3 (linear interpolation, like NumPy's default), the fences <code>Q1 − 1.5·IQR</code> and <code>Q3 + 1.5·IQR</code>, and return <code>(q1, q3, low fence, high fence, outlier indexes)</code>, rounded to 2.",
  [((AMOUNTS,), (99.5, 119.5, 69.5, 149.5, [6, 12, 16]))],
  ("Sort and interpolate percentiles by hand.", "O(n log n)", "O(n)"),
  ("<code>np.percentile</code>.", "O(n log n)", "O(n)"),
  viz=(([1, 2, 3, 4, 40],)))


@B
def iqr_outliers(values):
    s = sorted(values)
    def pct(p):
        pos = (len(s) - 1) * p
        lo = int(pos)
        frac = pos - lo
        return s[lo] + (s[min(lo + 1, len(s) - 1)] - s[lo]) * frac
    q1, q3 = pct(0.25), pct(0.75)
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    return (round(q1, 2), round(q3, 2), round(lo, 2), round(hi, 2), [i for i, v in enumerate(values) if v < lo or v > hi])


@O
def iqr_outliers(values):
    q1, q3 = np.percentile(values, [25, 75])
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    v = np.array(values)
    return (round(float(q1), 2), round(float(q3), 2), round(float(lo), 2), round(float(hi), 2), np.flatnonzero((v < lo) | (v > hi)).tolist())


Q(None, "Robust Z-Scores With the MAD", "Medium", "Outliers that don't hide each other",
  "The modified z-score uses the median and the median absolute deviation (MAD): <code>0.6745 × (x − median) / MAD</code>. Return the indexes with |modified z| above 3.5, and the values (rounded to 2) for those indexes.",
  [((AMOUNTS,), ([6, 12, 16], [147.17, -6.04, 60.45]))],
  ("Median and MAD by hand.", "O(n log n)", "O(n)"),
  ("<code>np.median</code> and <code>scipy.stats.median_abs_deviation</code>.", "O(n log n)", "O(n)"),
  viz=(([1, 2, 3, 4, 40],)))


@B
def mad_outliers(values):
    def median(xs):
        s = sorted(xs)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    med = median(values)
    mad = median([abs(v - med) for v in values])
    z = [0.6745 * (v - med) / mad for v in values]
    idx = [i for i, s in enumerate(z) if abs(s) > 3.5]
    return (idx, [round(z[i], 2) for i in idx])


@O
def mad_outliers(values):
    v = np.array(values, dtype=float)
    z = 0.6745 * (v - np.median(v)) / stats.median_abs_deviation(v)
    idx = np.flatnonzero(np.abs(z) > 3.5)
    return (idx.tolist(), [round(float(z[i]), 2) for i in idx])


PTS = [[1.0, 1.0], [1.2, 0.9], [0.9, 1.1], [1.1, 1.3], [5.0, 5.0], [5.2, 4.8], [4.9, 5.1], [5.1, 5.3], [3.0, 8.0], [9.0, 1.0], [1.0, 1.2], [5.0, 4.9]]


Q(None, "Anomalies by Distance to Neighbours", "Medium", "k-NN anomaly scores",
  "Score each point by its mean distance to its <code>k</code> nearest other points: isolated points score high, even in data with several clusters where a global z-score fails. Return the indexes of the <code>m</code> highest scores (highest first) and those scores rounded to 3.",
  [((PTS, 3, 2), ([9, 8], [5.539, 3.498]))],
  ("All pairwise distances, sort each row.", "O(n² log n)", "O(n²)"),
  ("<code>NearestNeighbors(n_neighbors=k+1)</code> (the first neighbour is the point itself).", "O(n² ) here, faster with trees", "O(n · k)"),
  viz=(([[0.0, 0.0], [0.1, 0.0], [5.0, 5.0]], 1, 1)))


@B
def knn_anomalies(points, k, m):
    scores = []
    for i, p in enumerate(points):
        d = sorted(math.dist(p, q) for j, q in enumerate(points) if j != i)
        scores.append(sum(d[:k]) / k)
    top = sorted(range(len(points)), key=lambda i: -scores[i])[:m]
    return (top, [round(scores[i], 3) for i in top])


@O
def knn_anomalies(points, k, m):
    dist, _ = NearestNeighbors(n_neighbors=k + 1).fit(points).kneighbors(points)
    scores = dist[:, 1:].mean(axis=1)
    top = np.argsort(-scores, kind="stable")[:m]
    return (top.tolist(), [round(float(scores[i]), 3) for i in top])


Q(None, "Score an Anomaly Detector", "Medium", "Precision@k and average precision",
  "Anomalies are rare, so accuracy is meaningless. Given detector scores (higher = more suspicious) and true labels (1 = fraud), return <code>(precision@k, recall@k, average precision)</code> rounded to 3. Average precision averages the precision at the rank of each true anomaly.",
  [(([0.91, 0.15, 0.78, 0.05, 0.66, 0.42, 0.88, 0.12, 0.30, 0.71], [1, 0, 0, 0, 1, 0, 1, 0, 0, 0], 3), (0.667, 0.667, 0.867))],
  ("Sort by score and walk the ranking.", "O(n log n)", "O(n)"),
  ("<code>precision_score</code>, <code>recall_score</code>, <code>average_precision_score</code>.", "O(n log n)", "O(n)"),
  viz=(([0.9, 0.1, 0.5], [1, 0, 0], 1)))


@B
def anomaly_metrics(scores, labels, k):
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    top = order[:k]
    tp = sum(labels[i] for i in top)
    pos = sum(labels)
    hits, ap = 0, 0.0
    for rank, i in enumerate(order, 1):
        if labels[i]:
            hits += 1
            ap += hits / rank
    return (round(tp / k, 3), round(tp / pos, 3), round(ap / pos, 3))


@O
def anomaly_metrics(scores, labels, k):
    s = np.array(scores)
    pred = np.zeros(len(s), dtype=int)
    pred[np.argsort(-s)[:k]] = 1
    return (round(precision_score(labels, pred), 3), round(recall_score(labels, pred), 3), round(average_precision_score(labels, s), 3))


HIGH = [[0.0, 0.0, 0.0, 0.0], [0.1, 0.0, 0.1, 0.0], [0.0, 0.2, 0.0, 0.1], [5.0, 5.0, 0.0, 0.0], [5.1, 4.9, 0.1, 0.0],
        [4.9, 5.2, 0.0, 0.1], [0.0, 0.0, 6.0, 6.0], [0.1, 0.1, 6.1, 5.9], [0.0, 0.2, 5.8, 6.2]]


Q(None, "Can You Trust That t-SNE Plot?", "Hard", "Trustworthiness of an embedding",
  "t-SNE and UMAP squash high-dimensional data into 2-D pictures, and can invent neighbours that aren't real. Trustworthiness (0–1) penalises points that are among a point's k nearest neighbours in 2-D but not in the original space, by how far down the original ranking they really are. Return it (rounded to 4) for a faithful and a scrambled 2-D layout of the same data.",
  [((HIGH, [[0.0, 0.0], [0.2, 0.1], [0.1, 0.3], [5.0, 0.0], [5.2, 0.1], [5.1, -0.2], [0.0, 5.0], [0.2, 5.1], [-0.1, 5.2]], [[0.0, 0.0], [5.0, 5.1], [0.1, 5.2], [5.2, 0.1], [0.2, 0.1], [0.1, 0.3], [5.1, -0.2], [0.0, 5.0], [5.0, 5.0]], 2), (1.0, 0.4242))],
  ("Rank all distances in both spaces and apply the formula.", "O(n² log n)", "O(n²)"),
  ("<code>sklearn.manifold.trustworthiness</code>.", "O(n² log n)", "O(n²)"),
  viz=(([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [9.0, 9.0, 9.0], [9.0, 8.0, 9.0]], [[0.0, 0.0], [1.0, 0.0], [9.0, 9.0], [9.0, 8.0]], [[0.0, 0.0], [9.0, 9.0], [1.0, 0.0], [9.0, 8.0]], 1)))


def trust_scratch(X, Y, k):
    n = len(X)
    total = 0
    for i in range(n):
        orig = sorted((math.dist(X[i], X[j]), j) for j in range(n) if j != i)
        rank = {j: r for r, (_, j) in enumerate(orig, 1)}
        low = [j for _, j in sorted((math.dist(Y[i], Y[j]), j) for j in range(n) if j != i)[:k]]
        total += sum(max(0, rank[j] - k) for j in low)
    return 1 - 2 / (n * k * (2 * n - 3 * k - 1)) * total


@B
def trust(X, good, bad, k):
    return (round(trust_scratch(X, good, k), 4), round(trust_scratch(X, bad, k), 4))


@O
def trust(X, good, bad, k):
    return (round(float(trustworthiness(np.array(X), np.array(good), n_neighbors=k)), 4),
            round(float(trustworthiness(np.array(X), np.array(bad), n_neighbors=k)), 4))


REVIEWS = ["Great battery and great camera", "Battery died fast, terrible phone", "Love the camera, love the screen",
           "Terrible support and slow delivery", "Fast delivery, great price", "Screen cracked, terrible build"]


Q(None, "Bag of Words", "Easy", "Text → a count matrix",
  "Lower-case each text, keep tokens of 2+ word characters (<code>\\b\\w\\w+\\b</code>), build a sorted vocabulary and count each word per text. Return <code>(vocabulary, count rows)</code> for the first three reviews — exactly what <code>CountVectorizer</code> does.",
  [((REVIEWS[:3],), (['and', 'battery', 'camera', 'died', 'fast', 'great', 'love', 'phone', 'screen', 'terrible', 'the'], [[1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0], [0, 0, 1, 0, 0, 0, 2, 0, 1, 0, 2]]))],
  ("Regex tokens, a vocabulary list and Counters.", "O(total tokens + n · v)", "O(n · v)"),
  ("<code>CountVectorizer().fit_transform</code>.", "O(total tokens + n · v)", "O(n · v)"),
  viz=((["a big dog", "big cat"],)))


@B
def bag_of_words(texts):
    toks = [re.findall(r"\b\w\w+\b", t.lower()) for t in texts]
    vocab = sorted({w for ts in toks for w in ts})
    rows = []
    for ts in toks:
        c = Counter(ts)
        rows.append([c[w] for w in vocab])
    return (vocab, rows)


@O
def bag_of_words(texts):
    cv = CountVectorizer()
    X = cv.fit_transform(texts)
    return (cv.get_feature_names_out().tolist(), X.toarray().tolist())


Q(None, "Classify Text With Naive Bayes", "Medium", "A strong, fast baseline",
  "Train multinomial Naive Bayes (add-one smoothing) on word counts of the labelled reviews (1 = positive), then return <code>(predicted label, P(positive) rounded to 3)</code> for each new text. Words never seen in training are ignored.",
  [((REVIEWS, [1, 0, 1, 0, 1, 0], ["great screen and fast", "terrible slow battery", "camera"]), [(1, 0.779), (0, 0.102), (1, 0.744)])],
  ("Count words per class and add log probabilities.", "O(tokens + t · v)", "O(c · v)"),
  ("<code>CountVectorizer</code> + <code>MultinomialNB(alpha=1)</code>.", "O(tokens + t · v)", "O(c · v)"),
  viz=((["good good", "bad"], [1, 0], ["good"])))


@B
def nb_text(texts, labels, new):
    tok = lambda t: re.findall(r"\b\w\w+\b", t.lower())
    vocab = sorted({w for t in texts for w in tok(t)})
    counts = {c: Counter() for c in (0, 1)}
    for t, y in zip(texts, labels):
        counts[y].update(tok(t))
    prior = {c: math.log(labels.count(c) / len(labels)) for c in (0, 1)}
    total = {c: sum(counts[c].values()) for c in (0, 1)}
    out = []
    for t in new:
        logp = {}
        for c in (0, 1):
            logp[c] = prior[c] + sum(math.log((counts[c][w] + 1) / (total[c] + len(vocab))) for w in tok(t) if w in vocab)
        p1 = 1 / (1 + math.exp(logp[0] - logp[1]))
        out.append((1 if p1 > 0.5 else 0, round(p1, 3)))
    return out


@O
def nb_text(texts, labels, new):
    cv = CountVectorizer()
    nb = MultinomialNB(alpha=1.0).fit(cv.fit_transform(texts), labels)
    Xn = cv.transform(new)
    return [(int(p), round(float(pr[1]), 3)) for p, pr in zip(nb.predict(Xn), nb.predict_proba(Xn))]


Q(None, "Most Common Bigrams", "Easy", "Two-word phrases",
  "Single words lose phrases like 'not good' or 'fast delivery'. Count two-word sequences (same tokenising as before) across all texts and return the <code>k</code> most frequent with counts, ties alphabetical.",
  [((["fast delivery and great price", "great price, fast delivery", "slow delivery and bad price", "great price again"], 3), [('great price', 3), ('delivery and', 2), ('fast delivery', 2)])],
  ("zip neighbouring tokens into a Counter.", "O(tokens)", "O(b)"),
  ("<code>CountVectorizer(ngram_range=(2, 2))</code> summed over rows.", "O(tokens)", "O(b)"),
  viz=((["big dog big dog"], 1)))


@B
def top_bigrams(texts, k):
    c = Counter()
    for t in texts:
        toks = re.findall(r"\b\w\w+\b", t.lower())
        c.update(" ".join(p) for p in zip(toks, toks[1:]))
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[:k]


@O
def top_bigrams(texts, k):
    cv = CountVectorizer(ngram_range=(2, 2))
    totals = np.asarray(cv.fit_transform(texts).sum(axis=0)).ravel()
    pairs = zip(cv.get_feature_names_out(), totals)
    return sorted(((w, int(n)) for w, n in pairs), key=lambda x: (-x[1], x[0]))[:k]


Q(None, "Tag Entities With BIO Labels", "Easy", "How NER data is labelled",
  "Named-entity recognition labels every token: <code>B-TYPE</code> at the start of an entity, <code>I-TYPE</code> inside it, <code>O</code> outside. Given tokens and entity spans <code>(start, end exclusive, type)</code>, return the tags.",
  [((["Asha", "Kulkarni", "flew", "from", "New", "Delhi", "to", "Pune", "on", "Air", "India", "."], [(0, 2, "PER"), (4, 6, "LOC"), (7, 8, "LOC"), (9, 11, "ORG")]), ['B-PER', 'I-PER', 'O', 'O', 'B-LOC', 'I-LOC', 'O', 'B-LOC', 'O', 'B-ORG', 'I-ORG', 'O'])],
  ("Loop tokens and check each span.", "O(t · s)", "O(t)"),
  ("Start from all O, then fill each span.", "O(t + s)", "O(t)"),
  viz=((["Asha", "runs"], [(0, 1, "PER")])))


@B
def bio_tags(tokens, spans):
    tags = []
    for i in range(len(tokens)):
        tag = "O"
        for s, e, t in spans:
            if i == s:
                tag = "B-" + t
            elif s < i < e:
                tag = "I-" + t
        tags.append(tag)
    return tags


@O
def bio_tags(tokens, spans):
    tags = ["O"] * len(tokens)
    for s, e, t in spans:
        tags[s:e] = [f"B-{t}"] + [f"I-{t}"] * (e - s - 1)
    return tags


Q(None, "Score Entity Predictions", "Medium", "Exact-match precision, recall and F1",
  "NER is scored on whole entities: a prediction counts only if its start, end and type all match a gold entity. Return <code>(precision, recall, F1)</code> rounded to 3, and the per-type F1 for each type in the gold data.",
  [(([(0, 2, "PER"), (4, 6, "LOC"), (7, 8, "LOC"), (9, 11, "ORG")], [(0, 2, "PER"), (4, 5, "LOC"), (7, 8, "LOC"), (9, 11, "LOC"), (12, 13, "ORG")]), (0.4, 0.5, 0.444, {'LOC': 0.4, 'ORG': 0.0, 'PER': 1.0}))],
  ("Count matches with loops.", "O(g · p)", "O(1)"),
  ("Set intersections.", "O(g + p)", "O(g + p)"),
  viz=(([(0, 1, "PER")], [(0, 1, "PER")])))


@B
def entity_f1(gold, pred):
    def prf(g, p):
        tp = 0
        for x in p:
            if x in g:
                tp += 1
        prec = tp / len(p) if p else 0.0
        rec = tp / len(g) if g else 0.0
        return prec, rec, (2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    p, r, f = prf(gold, pred)
    per = {}
    for t in sorted({x[2] for x in gold}):
        per[t] = round(prf([x for x in gold if x[2] == t], [x for x in pred if x[2] == t])[2], 3)
    return (round(p, 3), round(r, 3), round(f, 3), per)


@O
def entity_f1(gold, pred):
    def prf(g, p):
        g, p = set(g), set(p)
        tp = len(g & p)
        pr, rc = (tp / len(p) if p else 0.0), (tp / len(g) if g else 0.0)
        return pr, rc, 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    p, r, f = prf(gold, pred)
    per = {t: round(prf([x for x in gold if x[2] == t], [x for x in pred if x[2] == t])[2], 3) for t in sorted({x[2] for x in gold})}
    return (round(p, 3), round(r, 3), round(f, 3), per)


Q(None, "Intersection over Union", "Easy", "How much two boxes overlap",
  "Boxes are <code>(x1, y1, x2, y2)</code> with x2 &gt; x1 and y2 &gt; y1. IoU = overlap area ÷ union area (0 = disjoint, 1 = identical). Return the IoU of each pair, rounded to 4 — the measure behind every object-detection metric.",
  [(([((0, 0, 10, 10), (5, 5, 15, 15)), ((0, 0, 10, 10), (0, 0, 10, 10)), ((0, 0, 10, 10), (20, 20, 30, 30)), ((2, 2, 8, 6), (0, 0, 10, 10)), ((0, 0, 4, 4), (4, 0, 8, 4))],), [0.1429, 1.0, 0.0, 0.24, 0.0])],
  ("max/min of coordinates per pair.", "O(p)", "O(1)"),
  ("NumPy arrays for all pairs at once.", "O(p)", "O(p)"),
  viz=(([((0, 0, 2, 2), (1, 1, 3, 3))],)))


def iou(a, b):
    w = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = w * h
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union


@B
def iou_pairs(pairs):
    return [round(iou(a, b), 4) for a, b in pairs]


@O
def iou_pairs(pairs):
    A, B_ = np.array([p[0] for p in pairs], dtype=float), np.array([p[1] for p in pairs], dtype=float)
    w = np.clip(np.minimum(A[:, 2], B_[:, 2]) - np.maximum(A[:, 0], B_[:, 0]), 0, None)
    h = np.clip(np.minimum(A[:, 3], B_[:, 3]) - np.maximum(A[:, 1], B_[:, 1]), 0, None)
    area = lambda M: (M[:, 2] - M[:, 0]) * (M[:, 3] - M[:, 1])
    inter = w * h
    return np.round(inter / (area(A) + area(B_) - inter), 4).tolist()


BOXES = [(10, 10, 50, 50), (12, 12, 52, 52), (100, 100, 140, 150), (11, 9, 49, 51), (102, 98, 142, 148), (60, 60, 90, 90)]
SCORES = [0.95, 0.80, 0.90, 0.60, 0.70, 0.55]


Q(None, "Non-Maximum Suppression", "Medium", "One box per object",
  "Detectors output many overlapping boxes for the same object. NMS keeps the highest-scoring box, removes every remaining box with IoU above <code>thresh</code> with it, and repeats. Return the kept box indexes in the order they were kept.",
  [((BOXES, SCORES, 0.5), [0, 2, 5]), ((BOXES, SCORES, 0.95), [0, 2, 1, 4, 3, 5])],
  ("Repeatedly pick the max and filter the list.", "O(n²)", "O(n)"),
  ("Sort once; vectorised IoU of the best box against the rest.", "O(n²) worst case", "O(n)"),
  viz=(([(0, 0, 2, 2), (0, 0, 2, 2.2), (5, 5, 6, 6)], [0.9, 0.8, 0.7], 0.5)))


@B
def nms(boxes, scores, thresh):
    left = list(range(len(boxes)))
    kept = []
    while left:
        best = max(left, key=lambda i: scores[i])
        kept.append(best)
        left = [i for i in left if i != best and iou(boxes[best], boxes[i]) <= thresh]
    return kept


@O
def nms(boxes, scores, thresh):
    b = np.array(boxes, dtype=float)
    order = list(np.argsort(-np.array(scores), kind="stable"))
    kept = []
    while order:
        i, rest = order[0], np.array(order[1:], dtype=int)
        kept.append(int(i))
        if len(rest) == 0:
            break
        w = np.clip(np.minimum(b[i, 2], b[rest, 2]) - np.maximum(b[i, 0], b[rest, 0]), 0, None)
        h = np.clip(np.minimum(b[i, 3], b[rest, 3]) - np.maximum(b[i, 1], b[rest, 1]), 0, None)
        inter = w * h
        union = (b[i, 2] - b[i, 0]) * (b[i, 3] - b[i, 1]) + (b[rest, 2] - b[rest, 0]) * (b[rest, 3] - b[rest, 1]) - inter
        order = rest[inter / union <= thresh].tolist()
    return kept


Q(None, "Match Detections to Ground Truth", "Medium", "TP, FP, FN for detection",
  "Go through predictions from highest score down; a prediction is a true positive if its IoU with some still-unmatched ground-truth box is at least <code>thresh</code> (take the best such box), otherwise a false positive. Unmatched ground-truth boxes are false negatives. Return <code>(TP, FP, FN, precision, recall)</code>, rounded to 3. This matching is the first step of mAP.",
  [(([(10, 10, 50, 50), (100, 100, 140, 150), (200, 50, 240, 90)], [((12, 12, 52, 52), 0.95), ((11, 9, 49, 51), 0.80), ((102, 98, 142, 148), 0.90), ((300, 300, 320, 320), 0.60), ((205, 55, 260, 110), 0.70)], 0.5), (2, 3, 1, 0.4, 0.667))],
  ("Loop predictions and ground truth.", "O(p · g)", "O(g)"),
  ("An IoU matrix computed once.", "O(p · g)", "O(p · g)"),
  viz=(([(0, 0, 2, 2)], [((0, 0, 2, 2), 0.9)], 0.5)))


@B
def match_detections(gt, preds, thresh):
    used, tp, fp = set(), 0, 0
    for box, _ in sorted(preds, key=lambda p: -p[1]):
        best, best_iou = None, thresh
        for j, g in enumerate(gt):
            if j not in used and iou(box, g) >= best_iou:
                best, best_iou = j, iou(box, g)
        if best is None:
            fp += 1
        else:
            used.add(best)
            tp += 1
    fn = len(gt) - tp
    return (tp, fp, fn, round(tp / (tp + fp), 3), round(tp / len(gt), 3))


@O
def match_detections(gt, preds, thresh):
    preds = sorted(preds, key=lambda p: -p[1])
    M = np.array([[iou(p, g) for g in gt] for p, _ in preds])
    free, tp = np.ones(len(gt), dtype=bool), 0
    for row in M:
        cand = np.where(free & (row >= thresh), row, -1)
        j = int(np.argmax(cand))
        if cand[j] >= 0:
            free[j], tp = False, tp + 1
    fp = len(preds) - tp
    return (tp, fp, len(gt) - tp, round(tp / (tp + fp), 3), round(tp / len(gt), 3))


LAYERS = [("conv", 3, 32, 3), ("conv", 32, 64, 3), ("conv", 64, 128, 3), ("conv", 128, 256, 3), ("dense", 256, 512), ("dense", 512, 10)]


Q(None, "Transfer Learning: What Gets Trained?", "Easy", "Freeze the backbone, train the head",
  "Layers are <code>('conv', in, out, k)</code> with in·out·k·k weights + out biases, or <code>('dense', in, out)</code> with in·out + out. Freezing the first <code>frozen</code> layers (the pretrained backbone) leaves only the rest trainable. Return <code>(total parameters, trainable parameters, % trainable rounded to 2)</code> for each choice of <code>frozen</code>.",
  [((LAYERS, [0, 4, 5]), [(525130, 525130, 100.0), (525130, 136714, 26.03), (525130, 5130, 0.98)])],
  ("Add up each layer in a loop.", "O(f · l)", "O(l)"),
  ("Per-layer counts once, then prefix sums.", "O(l + f)", "O(l)"),
  viz=(([("dense", 2, 3), ("dense", 3, 1)], [1])))


@B
def trainable(layers, frozen_options):
    out = []
    for frozen in frozen_options:
        total = train = 0
        for i, layer in enumerate(layers):
            n = layer[1] * layer[2] * layer[3] ** 2 + layer[2] if layer[0] == "conv" else layer[1] * layer[2] + layer[2]
            total += n
            if i >= frozen:
                train += n
        out.append((total, train, round(train / total * 100, 2)))
    return out


@O
def trainable(layers, frozen_options):
    sizes = np.array([l[1] * l[2] * l[3] ** 2 + l[2] if l[0] == "conv" else l[1] * l[2] + l[2] for l in layers])
    total = int(sizes.sum())
    return [(total, int(sizes[f:].sum()), round(100 * float(sizes[f:].sum()) / total, 2)) for f in frozen_options]
