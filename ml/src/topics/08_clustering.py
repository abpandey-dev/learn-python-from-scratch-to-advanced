from lib import *
import math
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import pairwise_distances_argmin, silhouette_score, silhouette_samples, rand_score
from sklearn.metrics.cluster import contingency_matrix
from sklearn.neighbors import NearestCentroid, NearestNeighbors
from sklearn.decomposition import PCA


TOPIC(
    id="clustering", title="Clustering & Unsupervised Learning", glyph="◉ ◉ ◉",
    blurb="Finding structure without labels: k-means step by step, choosing k with the elbow and silhouette, hierarchical clustering, DBSCAN for odd shapes and noise, comparing clusterings, PCA, and distance-based outliers.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
km.labels_, km.cluster_centers_, km.inertia_, km.predict(X_new)
silhouette_score(X, labels)                       # −1 … 1, higher is better
AgglomerativeClustering(n_clusters=3, linkage="ward" | "single" | "complete" | "average")
DBSCAN(eps=0.5, min_samples=5).fit_predict(X)      # −1 = noise
PCA(n_components=2).fit_transform(X), pca.explained_variance_ratio_</code></pre>
<p>Scale features first — every method here relies on distances.</p>
""")

P = [[1, 1], [1.5, 2], [2, 1.2], [8, 8], [8.5, 9], [9, 8.2], [1, 8], [1.5, 8.5], [2, 9]]
INIT = [[1, 1], [2, 1.2], [8, 8]]


def canon(labels):
    """Renumber clusters in order of first appearance (cluster ids are arbitrary); keep −1 for noise."""
    mapping, out = {}, []
    for lab in labels:
        lab = int(lab)
        if lab == -1:
            out.append(-1)
            continue
        if lab not in mapping:
            mapping[lab] = len(mapping)
        out.append(mapping[lab])
    return out


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def kmeans_scratch(X, centers, iters=100):
    for _ in range(iters):
        labels = [min(range(len(centers)), key=lambda c: dist(p, centers[c])) for p in X]
        new = []
        for c in range(len(centers)):
            members = [p for p, lab in zip(X, labels) if lab == c]
            new.append([sum(col) / len(members) for col in zip(*members)] if members else centers[c])
        if new == centers:
            break
        centers = new
    return labels, centers


Q(None, "Assign Points to the Nearest Centre", "Easy", "k-means step 1",
  "Return the index of the closest centre for every point.",
  [((P, INIT), [0, 1, 1, 2, 2, 2, 1, 2, 2])],
  ("Distance to each centre, keep the smallest.", "O(n·k·d)", "O(n)"),
  ("<code>pairwise_distances_argmin(X, centers)</code>.", "O(n·k·d)", "O(n)"),
  names=["X", "centers"])


@B
def assign(X, centers):
    return [min(range(len(centers)), key=lambda c: dist(p, centers[c])) for p in X]


@O
def assign(X, centers):
    return pairwise_distances_argmin(X, centers)


Q(None, "Move Each Centre to Its Points' Mean", "Easy", "k-means step 2",
  "Given cluster labels, return each cluster's centroid (clusters 0, 1, …), rounded to 4 decimals.",
  [((P, [0, 0, 0, 1, 1, 1, 2, 2, 2]), [[1.5, 1.4], [8.5, 8.4], [1.5, 8.5]])],
  ("Average the points in each cluster.", "O(n·d)", "O(k·d)"),
  ("<code>NearestCentroid().fit(X, labels).centroids_</code>.", "O(n·d)", "O(k·d)"),
  names=["X", "labels"])


@B
def centroids(X, labels):
    out = []
    for c in sorted(set(labels)):
        members = [p for p, lab in zip(X, labels) if lab == c]
        out.append([round(sum(col) / len(members), 4) for col in zip(*members)])
    return out


@O
def centroids(X, labels):
    return NearestCentroid().fit(X, labels).centroids_.round(4)


Q(None, "k-Means From Scratch", "Hard", "Repeat assign + update until stable",
  "Run k-means from the given starting centres until nothing changes. Return (labels, centres rounded to 4 decimals).",
  [((P, INIT), ([0, 0, 0, 2, 2, 2, 1, 1, 1], [[1.5, 1.4], [1.5, 8.5], [8.5, 8.4]])), ((P, [[1, 1], [8, 8], [1, 8]]), ([0, 0, 0, 1, 1, 1, 2, 2, 2], [[1.5, 1.4], [8.5, 8.4], [1.5, 8.5]]))],
  ("Loop the two steps until the centres stop moving (Lloyd's algorithm).", "O(iters·n·k·d)", "O(n + k·d)"),
  ("<code>KMeans(n_clusters=k, init=centers, n_init=1)</code>.", "O(iters·n·k·d)", "O(n + k·d)"),
  names=["X", "init"])


@B
def kmeans(X, init):
    labels, centers = kmeans_scratch(X, [list(map(float, c)) for c in init])
    return (labels, [[round(v, 4) for v in c] for c in centers])


@O
def kmeans(X, init):
    km = KMeans(n_clusters=len(init), init=np.array(init, dtype=float), n_init=1).fit(X)
    return (km.labels_, km.cluster_centers_.round(4))


Q(None, "Inertia", "Easy", "Within-cluster sum of squares",
  "After running k-means from the given centres, return the total squared distance of every point to its centre, rounded to 4 decimals.",
  [((P, INIT), 3.12), ((P, [[1, 1], [8, 8], [1, 8]]), 3.12)],
  ("Run the from-scratch k-means, then add up squared distances.", "O(iters·n·k·d)", "O(1)"),
  ("<code>KMeans(...).inertia_</code>.", "O(iters·n·k·d)", "O(1)"),
  names=["X", "init"])


@B
def inertia(X, init):
    labels, centers = kmeans_scratch(X, [list(map(float, c)) for c in init])
    return round(sum(dist(p, centers[lab]) ** 2 for p, lab in zip(X, labels)), 4)


@O
def inertia(X, init):
    return round(KMeans(n_clusters=len(init), init=np.array(init, dtype=float), n_init=1).fit(X).inertia_, 4)


Q(None, "The Elbow Curve", "Medium", "Inertia for k = 1 … K",
  "For k = 1 … max_k, start k-means from the first k points and return the final inertia of each, rounded to 1 decimal.",
  [((P, 4), [200.5, 76.6, 76.0, 2.5])],
  ("The from-scratch k-means for each k.", "O(K·iters·n·k·d)", "O(K)"),
  ("A <code>KMeans</code> per k.", "O(K·iters·n·k·d)", "O(K)"),
  names=["X", "max_k"])


@B
def elbow(X, max_k):
    out = []
    for k in range(1, max_k + 1):
        labels, centers = kmeans_scratch(X, [list(map(float, p)) for p in X[:k]])
        out.append(round(sum(dist(p, centers[lab]) ** 2 for p, lab in zip(X, labels)), 1))
    return out


@O
def elbow(X, max_k):
    A = np.array(X, dtype=float)
    return [round(KMeans(n_clusters=k, init=A[:k], n_init=1).fit(A).inertia_, 1) for k in range(1, max_k + 1)]


Q(None, "Cluster Sizes", "Easy", "How many points in each cluster?",
  "Run k-means from the given starting centres and return how many points end up in each cluster.",
  [((P, INIT), [3, 3, 3])],
  ("Count the from-scratch k-means labels.", "O(iters·n·k·d)", "O(k)"),
  ("<code>np.bincount(km.labels_)</code>.", "O(iters·n·k·d)", "O(k)"),
  names=["X", "init"])


@B
def cluster_sizes(X, init):
    labels, _ = kmeans_scratch(X, [list(map(float, c)) for c in init])
    return [labels.count(c) for c in range(len(init))]


@O
def cluster_sizes(X, init):
    km = KMeans(n_clusters=len(init), init=np.array(init, dtype=float), n_init=1).fit(X)
    return np.bincount(km.labels_, minlength=len(init))


Q(None, "Predict the Cluster of New Points", "Easy", "Using a fitted k-means",
  "Fit k-means from INIT-style starting centres, then return the cluster of each new point.",
  [((P, [[1, 1], [8, 8], [1, 8]], [[0, 0], [7, 9], [3, 7]]), [0, 1, 2])],
  ("Run k-means, then nearest-centre assignment for the new points.", "O(iters·n·k·d)", "O(m)"),
  ("<code>km.predict(X_new)</code>.", "O(iters·n·k·d)", "O(m)"),
  names=["X", "init", "X_new"])


@B
def predict_cluster(X, init, X_new):
    labels, centers = kmeans_scratch(X, [list(map(float, c)) for c in init])
    return [min(range(len(centers)), key=lambda c: dist(p, centers[c])) for p in X_new]


@O
def predict_cluster(X, init, X_new):
    return KMeans(n_clusters=len(init), init=np.array(init, dtype=float), n_init=1).fit(X).predict(X_new)


Q(None, "Silhouette of Each Point", "Medium", "(b − a) / max(a, b)",
  "a = mean distance to the other points in its cluster; b = mean distance to the nearest other cluster. Return each point's silhouette, rounded to 4 decimals.",
  [(([[1, 1], [1, 2], [5, 5], [6, 5], [5, 6]], [0, 0, 1, 1, 1]), [0.8375, 0.818, 0.8123, 0.8027, 0.7998])],
  ("Compute a and b for every point with loops.", "O(n²·d)", "O(n)"),
  ("<code>silhouette_samples(X, labels)</code>.", "O(n²·d)", "O(n²)"),
  names=["X", "labels"])


@B
def silhouettes(X, labels):
    out = []
    for i, p in enumerate(X):
        same = [dist(p, q) for j, q in enumerate(X) if labels[j] == labels[i] and j != i]
        a = sum(same) / len(same) if same else 0.0
        b = min(sum(dist(p, q) for j, q in enumerate(X) if labels[j] == c) / labels.count(c)
                for c in set(labels) if c != labels[i])
        out.append(round((b - a) / max(a, b), 4) if same else 0.0)
    return out


@O
def silhouettes(X, labels):
    return silhouette_samples(X, labels).round(4)


Q(None, "Silhouette Score", "Easy", "One number for cluster quality",
  "Return the mean silhouette over all points, rounded to 4 decimals.",
  [((P, [0, 0, 0, 1, 1, 1, 2, 2, 2]), 0.8558), ((P, [0, 0, 0, 1, 1, 1, 1, 1, 1]), 0.5878)],
  ("Average the per-point silhouettes computed by hand.", "O(n²·d)", "O(n)"),
  ("<code>silhouette_score</code>.", "O(n²·d)", "O(n²)"),
  names=["X", "labels"])


@B
def silhouette_mean(X, labels):
    total = 0
    for i, p in enumerate(X):
        same = [dist(p, q) for j, q in enumerate(X) if labels[j] == labels[i] and j != i]
        a = sum(same) / len(same)
        b = min(sum(dist(p, q) for j, q in enumerate(X) if labels[j] == c) / labels.count(c)
                for c in set(labels) if c != labels[i])
        total += (b - a) / max(a, b)
    return round(total / len(X), 4)


@O
def silhouette_mean(X, labels):
    return round(silhouette_score(X, labels), 4)


Q(None, "Choose k by Silhouette", "Medium", "Best number of clusters",
  "For k = 2 … max_k, run k-means from the first k points and return the k with the highest silhouette score.",
  [((P, 4), 4)],
  ("From-scratch k-means and silhouette for each k.", "O(K·n²)", "O(n)"),
  ("<code>KMeans</code> + <code>silhouette_score</code> per k.", "O(K·n²)", "O(n²)"),
  names=["X", "max_k"])


@B
def best_k(X, max_k):
    best = (None, -2)
    for k in range(2, max_k + 1):
        labels, _ = kmeans_scratch(X, [list(map(float, p)) for p in X[:k]])
        total = 0
        for i, p in enumerate(X):
            same = [dist(p, q) for j, q in enumerate(X) if labels[j] == labels[i] and j != i]
            if not same:
                continue
            a = sum(same) / len(same)
            b = min(sum(dist(p, q) for j, q in enumerate(X) if labels[j] == c) / labels.count(c)
                    for c in set(labels) if c != labels[i])
            total += (b - a) / max(a, b)
        if total / len(X) > best[1]:
            best = (k, total / len(X))
    return best[0]


@O
def best_k(X, max_k):
    A = np.array(X, dtype=float)
    scores = [silhouette_score(A, KMeans(n_clusters=k, init=A[:k], n_init=1).fit_predict(A)) for k in range(2, max_k + 1)]
    return 2 + int(np.argmax(scores))


def agglomerate(X, n_clusters, linkage):
    clusters = [[i] for i in range(len(X))]

    def gap(A, B):
        ds = [dist(X[i], X[j]) for i in A for j in B]
        if linkage == "single":
            return min(ds)
        if linkage == "complete":
            return max(ds)
        if linkage == "average":
            return sum(ds) / len(ds)
        def sse(idx):
            m = [sum(X[i][d] for i in idx) / len(idx) for d in range(len(X[0]))]
            return sum(dist(X[i], m) ** 2 for i in idx)
        return sse(A + B) - sse(A) - sse(B)

    while len(clusters) > n_clusters:
        a, b = min(((i, j) for i in range(len(clusters)) for j in range(i + 1, len(clusters))),
                   key=lambda ij: gap(clusters[ij[0]], clusters[ij[1]]))
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
    labels = [0] * len(X)
    for c, members in enumerate(clusters):
        for i in members:
            labels[i] = c
    return canon(labels)


CHAIN = [[0, 0], [1, 0], [2, 0], [3, 0], [10, 0], [11, 0], [5.5, 4], [6.5, 4]]


Q(None, "Hierarchical Clustering: Single Linkage", "Medium", "Merge the closest pair of points",
  "Start with every point alone and repeatedly merge the two clusters whose closest members are nearest, until n_clusters remain. Return labels numbered in order of first appearance.",
  [((CHAIN, 3), [0, 0, 0, 0, 1, 1, 2, 2]), ((P, 3), [0, 0, 0, 1, 1, 1, 2, 2, 2])],
  ("Naive agglomeration: compute all cluster gaps each round, merge the smallest.", "O(n³)", "O(n)"),
  ("<code>AgglomerativeClustering(n_clusters, linkage='single')</code>.", "O(n²)", "O(n²)"),
  names=["X", "n_clusters"])


@B
def single_link(X, n_clusters):
    return agglomerate(X, n_clusters, "single")


@O
def single_link(X, n_clusters):
    return canon(AgglomerativeClustering(n_clusters=n_clusters, linkage="single").fit_predict(X))


Q(None, "Hierarchical Clustering: Complete Linkage", "Medium", "Merge by the farthest members",
  "Same, but the gap between clusters is the distance between their farthest members.",
  [((CHAIN, 3), [0, 0, 0, 0, 1, 1, 2, 2])],
  ("Naive agglomeration with max instead of min.", "O(n³)", "O(n)"),
  ("<code>linkage='complete'</code>.", "O(n²)", "O(n²)"),
  names=["X", "n_clusters"])


@B
def complete_link(X, n_clusters):
    return agglomerate(X, n_clusters, "complete")


@O
def complete_link(X, n_clusters):
    return canon(AgglomerativeClustering(n_clusters=n_clusters, linkage="complete").fit_predict(X))


Q(None, "Hierarchical Clustering: Ward", "Hard", "Merge with the smallest rise in SSE",
  "Same, but merge the pair of clusters whose union increases the total within-cluster sum of squares the least.",
  [((CHAIN, 3), [0, 0, 0, 0, 1, 1, 2, 2]), ((P, 3), [0, 0, 0, 1, 1, 1, 2, 2, 2])],
  ("Naive agglomeration with the SSE increase as the gap.", "O(n³·d)", "O(n)"),
  ("<code>linkage='ward'</code> (the default).", "O(n²)", "O(n²)"),
  names=["X", "n_clusters"])


@B
def ward_link(X, n_clusters):
    return agglomerate(X, n_clusters, "ward")


@O
def ward_link(X, n_clusters):
    return canon(AgglomerativeClustering(n_clusters=n_clusters, linkage="ward").fit_predict(X))


NOISY = [[1, 1], [1.2, 1.1], [0.9, 1.3], [1.1, 0.8], [5, 5], [5.2, 5.1], [4.9, 5.3], [5.1, 4.8], [3, 9], [9, 1]]


def dbscan_scratch(X, eps, min_samples):
    n = len(X)
    neighbours = [[j for j in range(n) if dist(X[i], X[j]) <= eps] for i in range(n)]
    core = [len(nb) >= min_samples for nb in neighbours]
    labels = [-1] * n
    cluster = 0
    for i in range(n):
        if not core[i] or labels[i] != -1:
            continue
        stack = [i]
        labels[i] = cluster
        while stack:
            p = stack.pop()
            if not core[p]:
                continue
            for q in neighbours[p]:
                if labels[q] == -1:
                    labels[q] = cluster
                    stack.append(q)
        cluster += 1
    return labels, [i for i in range(n) if core[i]]


Q(None, "DBSCAN", "Hard", "Clusters of any shape, plus noise",
  "A core point has at least min_samples points (itself included) within eps. Grow clusters from core points; points reachable from none are noise (−1). Return the labels in order of first appearance.",
  [((NOISY, 0.5, 3), [0, 0, 0, 0, 1, 1, 1, 1, -1, -1]), ((CHAIN, 1.5, 2), [0, 0, 0, 0, 1, 1, 2, 2])],
  ("Find neighbours, mark core points, flood-fill clusters from each unvisited core point.", "O(n²)", "O(n²)"),
  ("<code>DBSCAN(eps, min_samples).fit_predict(X)</code>.", "O(n log n) with an index", "O(n)"),
  names=["X", "eps", "min_samples"])


@B
def dbscan(X, eps, min_samples):
    labels, _ = dbscan_scratch(X, eps, min_samples)
    return canon(labels)


@O
def dbscan(X, eps, min_samples):
    return canon(DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X))


Q(None, "DBSCAN Core Points", "Medium", "Who has enough neighbours?",
  "Return the indices of the core points.",
  [((NOISY, 0.5, 3), [0, 1, 2, 3, 4, 5, 6, 7]), ((NOISY, 0.5, 5), [])],
  ("Count each point's neighbours within eps.", "O(n²)", "O(n)"),
  ("<code>DBSCAN(...).fit(X).core_sample_indices_</code>.", "O(n log n)", "O(n)"),
  names=["X", "eps", "min_samples"])


@B
def core_points(X, eps, min_samples):
    return dbscan_scratch(X, eps, min_samples)[1]


@O
def core_points(X, eps, min_samples):
    return DBSCAN(eps=eps, min_samples=min_samples).fit(X).core_sample_indices_


Q(None, "Rand Index", "Medium", "Do two clusterings agree?",
  "Return the share of point pairs on which two labelings agree (both same cluster, or both different), rounded to 4 decimals.",
  [(([0, 0, 1, 1, 2, 2], [1, 1, 0, 0, 0, 2]), 0.8), (([0, 0, 1], [5, 5, 7]), 1.0)],
  ("Loop over all pairs.", "O(n²)", "O(1)"),
  ("<code>rand_score(a, b)</code> (and <code>adjusted_rand_score</code> corrects for chance).", "O(n)", "O(k²)"),
  names=["a", "b"])


@B
def rand_index(a, b):
    agree = total = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            total += 1
            agree += (a[i] == a[j]) == (b[i] == b[j])
    return round(agree / total, 4)


@O
def rand_index(a, b):
    return round(rand_score(a, b), 4)


Q(None, "Contingency Table", "Easy", "True classes vs found clusters",
  "Return a table whose row i, column j counts points with class i (sorted) in cluster j (sorted).",
  [((["a", "a", "b", "b", "b", "c"], [0, 0, 1, 1, 0, 2]), [[2, 0, 0], [1, 2, 0], [0, 0, 1]])],
  ("Nested counting.", "O(n·r·c)", "O(r·c)"),
  ("<code>contingency_matrix(classes, clusters)</code>.", "O(n)", "O(r·c)"),
  names=["classes", "clusters"])


@B
def contingency(classes, clusters):
    rows, cols = sorted(set(classes)), sorted(set(clusters))
    return [[sum(1 for a, b in zip(classes, clusters) if a == r and b == c) for c in cols] for r in rows]


@O
def contingency(classes, clusters):
    return contingency_matrix(classes, clusters)


Q(None, "PCA Explained Variance", "Medium", "How much each direction keeps",
  "Return PCA's explained-variance ratio for all components, rounded to 4 decimals.",
  [(([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2, 1.6], [1, 1.1], [1.5, 1.6], [1.1, 0.9]],), [0.9632, 0.0368])],
  ("Centre, covariance matrix, eigenvalues (NumPy), sorted and divided by their sum.", "O(n·d² + d³)", "O(d²)"),
  ("<code>PCA().fit(X).explained_variance_ratio_</code>.", "O(n·d²)", "O(d²)"))


@B
def pca_ratio(X):
    A = np.array(X, dtype=float)
    A = A - A.mean(axis=0)
    vals = np.linalg.eigvalsh(A.T @ A / (len(A) - 1))[::-1]
    return (vals / vals.sum()).round(4)


@O
def pca_ratio(X):
    return PCA().fit(X).explained_variance_ratio_.round(4)


Q(None, "Project Onto the First Component", "Medium", "Dimensionality reduction",
  "Return each row's PCA score on the first component (sign chosen so the first score is positive), rounded to 4 decimals.",
  [(([[1, 2], [2, 3], [3, 5], [4, 4]],), [2.1213, 0.7071, -1.4142, -1.4142])],
  ("Centre; top eigenvector of the covariance; dot each row with it.", "O(n·d² + d³)", "O(n)"),
  ("<code>PCA(n_components=1).fit_transform(X)</code>.", "O(n·d²)", "O(n)"))


@B
def pca_scores(X):
    A = np.array(X, dtype=float)
    A = A - A.mean(axis=0)
    vals, vecs = np.linalg.eigh(A.T @ A)
    scores = A @ vecs[:, -1]
    return (scores * np.sign(scores[0])).round(4)


@O
def pca_scores(X):
    scores = PCA(n_components=1).fit_transform(X)[:, 0]
    return (scores * np.sign(scores[0])).round(4)


Q(None, "Distance-Based Outliers", "Medium", "Far from your k-th neighbour",
  "Return each point's distance to its k-th nearest other point, rounded to 4 decimals. Large values flag outliers.",
  [((NOISY, 2), [0.2236, 0.3162, 0.3606, 0.3162, 0.2236, 0.3162, 0.3606, 0.3162, 4.4721, 5.5902])],
  ("For each point: sort distances to the others, take the k-th.", "O(n² log n)", "O(n)"),
  ("<code>NearestNeighbors(n_neighbors=k + 1).kneighbors(X)</code> (the first neighbour is the point itself).", "O(n log n)", "O(n·k)"),
  names=["X", "k"])


@B
def kth_distance(X, k):
    out = []
    for i, p in enumerate(X):
        ds = sorted(dist(p, q) for j, q in enumerate(X) if j != i)
        out.append(round(ds[k - 1], 4))
    return out


@O
def kth_distance(X, k):
    distances, _ = NearestNeighbors(n_neighbors=k + 1).fit(X).kneighbors(X)
    return distances[:, k].round(4)
