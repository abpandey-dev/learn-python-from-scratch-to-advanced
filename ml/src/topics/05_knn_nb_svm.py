from lib import *
import math
import numpy as np
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics.pairwise import euclidean_distances, rbf_kernel, polynomial_kernel
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import hinge_loss, accuracy_score


TOPIC(
    id="knn-nb-svm", title="k-NN, Naive Bayes & SVM", glyph="k · P · ⟂",
    blurb="Three classic classifiers: k-nearest neighbours (vote of the closest examples), Naive Bayes (Bayes' rule with an independence shortcut) and support vector machines (the widest possible margin, plus kernels).",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">KNeighborsClassifier(n_neighbors=5, weights="uniform" | "distance", metric="euclidean")
KNeighborsRegressor(n_neighbors=5)
GaussianNB(), MultinomialNB(alpha=1.0), BernoulliNB(alpha=1.0)
SVC(kernel="linear" | "rbf" | "poly", C=1.0, gamma="scale"), LinearSVC(C=1.0)
rbf_kernel(X, Y, gamma), polynomial_kernel(X, Y, degree, gamma, coef0)</code></pre>
<p>Scale features before k-NN and SVM; Naive Bayes doesn't need it.</p>
""")

PTS = [[1, 1], [2, 1], [1, 2], [6, 5], [7, 7], [6, 7], [4, 3]]
LAB = [0, 0, 0, 1, 1, 1, 0]


Q(None, "Distances to Every Training Point", "Easy", "The heart of k-NN",
  "Return the Euclidean distance from the query to each training point, rounded to 4 decimals.",
  [((PTS, [3, 3]), [2.8284, 2.2361, 2.2361, 3.6056, 5.6569, 5.0, 1.0])],
  ("Pythagoras for each point.", "O(n·d)", "O(n)"),
  ("<code>euclidean_distances(X, [q])</code>.", "O(n·d)", "O(n)"),
  names=["X", "q"])


@B
def distances(X, q):
    return [round(math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q))), 4) for p in X]


@O
def distances(X, q):
    return euclidean_distances(X, [q]).ravel().round(4)


Q(None, "Classify One Point With k-NN", "Easy", "Majority vote of the k closest",
  "Return the majority label among the k nearest training points to q.",
  [((PTS, LAB, [3, 3], 3), 0), ((PTS, LAB, [5, 5], 3), 1)],
  ("Sort the training points by distance, take k, count the labels.", "O(n log n)", "O(n)"),
  ("<code>KNeighborsClassifier(n_neighbors=k).fit(X, y).predict([q])</code>.", "O(n·d)", "O(n)"),
  names=["X", "y", "q", "k"])


@B
def knn_one(X, y, q, k):
    order = sorted(range(len(X)), key=lambda i: sum((a - b) ** 2 for a, b in zip(X[i], q)))
    votes = {}
    for i in order[:k]:
        votes[y[i]] = votes.get(y[i], 0) + 1
    best = max(votes.values())
    return min(label for label, v in votes.items() if v == best)


@O
def knn_one(X, y, q, k):
    return KNeighborsClassifier(n_neighbors=k).fit(X, y).predict([q])[0]


Q(None, "k-NN for Many Points", "Medium", "Predicting a whole test set",
  "Predict the label of every query point with k-NN.",
  [((PTS, LAB, [[0, 0], [8, 8], [5, 4], [3, 2]], 3), [0, 1, 1, 0])],
  ("Repeat the single-point vote for each query.", "O(m·n log n)", "O(n)"),
  ("<code>predict</code> on all queries at once.", "O(m·n·d)", "O(m·n)"),
  names=["X", "y", "queries", "k"])


@B
def knn_many(X, y, queries, k):
    out = []
    for q in queries:
        order = sorted(range(len(X)), key=lambda i: sum((a - b) ** 2 for a, b in zip(X[i], q)))
        labels = [y[i] for i in order[:k]]
        out.append(max(sorted(set(labels)), key=labels.count))
    return out


@O
def knn_many(X, y, queries, k):
    return KNeighborsClassifier(n_neighbors=k).fit(X, y).predict(queries)


Q(None, "k-NN Regression", "Easy", "Average of the neighbours",
  "Predict a number for q as the mean target of its k nearest neighbours (one feature), rounded to 4 decimals.",
  [(([1, 2, 3, 5, 8, 9], [10, 12, 15, 20, 30, 33], 4.1, 3), 15.6667)],
  ("Sort by |x − q|, average the first k targets.", "O(n log n)", "O(n)"),
  ("<code>KNeighborsRegressor(n_neighbors=k)</code>.", "O(n)", "O(n)"),
  names=["x", "y", "q", "k"])


@B
def knn_regress(x, y, q, k):
    order = sorted(range(len(x)), key=lambda i: abs(x[i] - q))
    return round(sum(y[i] for i in order[:k]) / k, 4)


@O
def knn_regress(x, y, q, k):
    model = KNeighborsRegressor(n_neighbors=k).fit(np.array(x).reshape(-1, 1), y)
    return round(model.predict([[q]])[0], 4)


Q(None, "Distance-Weighted k-NN", "Medium", "Closer neighbours count more",
  "Predict q as the weighted mean of its k nearest targets with weights 1/distance, rounded to 4 decimals.",
  [(([1, 2, 3, 5, 8, 9], [10, 12, 15, 20, 30, 33], 4.1, 3), 16.6532)],
  ("Weights 1/|x − q| for the k nearest, then Σw·y / Σw.", "O(n log n)", "O(n)"),
  ("<code>KNeighborsRegressor(n_neighbors=k, weights='distance')</code>.", "O(n)", "O(n)"),
  names=["x", "y", "q", "k"])


@B
def knn_weighted(x, y, q, k):
    order = sorted(range(len(x)), key=lambda i: abs(x[i] - q))[:k]
    weights = [1 / abs(x[i] - q) for i in order]
    return round(sum(w * y[i] for w, i in zip(weights, order)) / sum(weights), 4)


@O
def knn_weighted(x, y, q, k):
    model = KNeighborsRegressor(n_neighbors=k, weights="distance").fit(np.array(x).reshape(-1, 1), y)
    return round(model.predict([[q]])[0], 4)


Q(None, "k-NN With Manhattan Distance", "Easy", "Changing the metric",
  "Classify q by majority vote of its k nearest points using Manhattan distance.",
  [(([[0, 0], [3, 0], [0, 3], [2, 2]], ["A", "B", "B", "A"], [2.1, 0.5], 1), 'B')],
  ("Sort by Σ|differences|, vote.", "O(n log n)", "O(n)"),
  ("<code>KNeighborsClassifier(metric='manhattan')</code>.", "O(n·d)", "O(n)"),
  names=["X", "y", "q", "k"])


@B
def knn_manhattan(X, y, q, k):
    order = sorted(range(len(X)), key=lambda i: sum(abs(a - b) for a, b in zip(X[i], q)))
    labels = [y[i] for i in order[:k]]
    return max(sorted(set(labels)), key=labels.count)


@O
def knn_manhattan(X, y, q, k):
    return KNeighborsClassifier(n_neighbors=k, metric="manhattan").fit(X, y).predict([q])[0]


Q(None, "Choose k on a Validation Set", "Medium", "Tuning k",
  "For each k in ks, train k-NN on (X, y) and measure accuracy on (Xv, yv). Return the k with the best accuracy (smallest k on ties).",
  [((PTS, LAB, [[2, 2], [6, 6], [4, 4], [5, 5], [3, 4]], [0, 1, 0, 1, 1], [1, 3, 5]), 1)],
  ("Loop over k; hand-written k-NN; count correct validation predictions.", "O(K·m·n log n)", "O(n)"),
  ("Fit <code>KNeighborsClassifier</code> per k and use <code>accuracy_score</code>.", "O(K·m·n)", "O(n)"),
  names=["X", "y", "Xv", "yv", "ks"])


@B
def choose_k(X, y, Xv, yv, ks):
    best_k, best_acc = None, -1
    for k in ks:
        correct = 0
        for q, truth in zip(Xv, yv):
            order = sorted(range(len(X)), key=lambda i: sum((a - b) ** 2 for a, b in zip(X[i], q)))
            labels = [y[i] for i in order[:k]]
            pred = max(sorted(set(labels)), key=labels.count)
            correct += pred == truth
        acc = correct / len(yv)
        if acc > best_acc:
            best_k, best_acc = k, acc
    return best_k


@O
def choose_k(X, y, Xv, yv, ks):
    scores = [accuracy_score(yv, KNeighborsClassifier(n_neighbors=k).fit(X, y).predict(Xv)) for k in ks]
    return ks[int(np.argmax(scores))]


Q(None, "Class Priors", "Easy", "P(class) before seeing features",
  "Return each class's share of the training labels (sorted classes), rounded to 4 decimals.",
  [((LAB,), [0.5714, 0.4286]), ((["spam", "ham", "ham", "ham"],), [0.75, 0.25])],
  ("Count and divide.", "O(n)", "O(k)"),
  ("<code>GaussianNB().fit(...).class_prior_</code>.", "O(n)", "O(k)"))


@B
def priors(y):
    return [round(y.count(c) / len(y), 4) for c in sorted(set(y))]


@O
def priors(y):
    return GaussianNB().fit(np.zeros((len(y), 1)), y).class_prior_.round(4)


Q(None, "Gaussian Naive Bayes: Means per Class", "Easy", "What GaussianNB learns",
  "Return the mean of each feature within each class (rows = sorted classes), rounded to 4 decimals.",
  [((PTS, LAB), [[2.0, 1.75], [6.3333, 6.3333]])],
  ("Group rows by class and average each column.", "O(n·d)", "O(k·d)"),
  ("<code>GaussianNB().fit(X, y).theta_</code>.", "O(n·d)", "O(k·d)"),
  names=["X", "y"])


@B
def class_means(X, y):
    out = []
    for c in sorted(set(y)):
        rows = [r for r, label in zip(X, y) if label == c]
        out.append([round(sum(r[j] for r in rows) / len(rows), 4) for j in range(len(X[0]))])
    return out


@O
def class_means(X, y):
    return GaussianNB().fit(X, y).theta_.round(4)


Q(None, "Gaussian Naive Bayes: Variances per Class", "Easy", "The width of each bell curve",
  "Return the (population) variance of each feature within each class, rows = sorted classes, rounded to 4 decimals.",
  [((PTS, LAB), [[1.5, 0.6875], [0.2222, 0.8889]])],
  ("Group by class; average squared distance from the class mean.", "O(n·d)", "O(k·d)"),
  ("<code>GaussianNB().fit(X, y).var_</code> (it adds a tiny ε for stability).", "O(n·d)", "O(k·d)"),
  names=["X", "y"])


@B
def class_vars(X, y):
    out = []
    for c in sorted(set(y)):
        rows = [r for r, label in zip(X, y) if label == c]
        row_out = []
        for j in range(len(X[0])):
            mean = sum(r[j] for r in rows) / len(rows)
            row_out.append(round(sum((r[j] - mean) ** 2 for r in rows) / len(rows), 4))
        out.append(row_out)
    return out


@O
def class_vars(X, y):
    return GaussianNB().fit(X, y).var_.round(4)


Q(None, "Gaussian Naive Bayes: Predict Probabilities", "Hard", "Bayes' rule with bell curves",
  "Fit Gaussian NB and return P(class | q) for each class, rounded to 4 decimals.",
  [((PTS, LAB, [4, 4]), [0.9999, 0.0001]), ((PTS, LAB, [2, 2]), [1.0, 0.0])],
  ("Per class: prior × Π normal-density(feature; class mean, class variance + tiny ε), then normalise.", "O(k·d + n·d)", "O(k·d)"),
  ("<code>GaussianNB().fit(X, y).predict_proba([q])</code>.", "O(n·d)", "O(k·d)"),
  names=["X", "y", "q"])


@B
def gnb_proba(X, y, q):
    d = len(X[0])
    all_var = [sum((r[j] - sum(t[j] for t in X) / len(X)) ** 2 for r in X) / len(X) for j in range(d)]
    eps = 1e-9 * max(all_var)
    scores = []
    for c in sorted(set(y)):
        rows = [r for r, label in zip(X, y) if label == c]
        log_p = math.log(len(rows) / len(X))
        for j in range(d):
            mean = sum(r[j] for r in rows) / len(rows)
            var = sum((r[j] - mean) ** 2 for r in rows) / len(rows) + eps
            log_p += -0.5 * math.log(2 * math.pi * var) - (q[j] - mean) ** 2 / (2 * var)
        scores.append(log_p)
    top = max(scores)
    exps = [math.exp(s - top) for s in scores]
    return [round(e / sum(exps), 4) for e in exps]


@O
def gnb_proba(X, y, q):
    return GaussianNB().fit(X, y).predict_proba([q])[0].round(4)


DOCS = [[2, 1, 0, 0], [3, 0, 1, 0], [0, 0, 2, 3], [0, 1, 1, 4]]
TOPICS = ["sport", "sport", "tech", "tech"]


Q(None, "Word Probabilities With Laplace Smoothing", "Medium", "Never multiply by zero",
  "Rows are word counts per document. For each class return P(word | class) = (count + α)/(total + α·vocab), α = 1, rounded to 4 decimals.",
  [((DOCS, TOPICS), [[0.5455, 0.1818, 0.1818, 0.0909], [0.0667, 0.1333, 0.2667, 0.5333]])],
  ("Sum the counts of each class's documents, add α, divide.", "O(n·V)", "O(k·V)"),
  ("<code>np.exp(MultinomialNB(alpha=1).fit(X, y).feature_log_prob_)</code>.", "O(n·V)", "O(k·V)"),
  names=["X", "y"])


@B
def word_probs(X, y):
    out = []
    for c in sorted(set(y)):
        totals = [sum(r[j] for r, label in zip(X, y) if label == c) for j in range(len(X[0]))]
        denom = sum(totals) + len(totals)
        out.append([round((t + 1) / denom, 4) for t in totals])
    return out


@O
def word_probs(X, y):
    return np.exp(MultinomialNB(alpha=1.0).fit(X, y).feature_log_prob_).round(4)


Q(None, "Multinomial Naive Bayes Classifier", "Hard", "Text classification",
  "Fit multinomial NB (α = 1) on word-count rows and return P(class | doc) for a new document, rounded to 4 decimals.",
  [((DOCS, TOPICS, [1, 0, 1, 1]), [0.4874, 0.5126]), ((DOCS, TOPICS, [4, 1, 0, 0]), [0.9998, 0.0002])],
  ("log prior + Σ count·log P(word | class) per class, then softmax.", "O(k·V)", "O(k·V)"),
  ("<code>MultinomialNB().fit(X, y).predict_proba([doc])</code>.", "O(n·V)", "O(k·V)"),
  names=["X", "y", "doc"])


@B
def mnb_proba(X, y, doc):
    classes = sorted(set(y))
    scores = []
    for c in classes:
        totals = [sum(r[j] for r, label in zip(X, y) if label == c) for j in range(len(doc))]
        denom = sum(totals) + len(totals)
        s = math.log(y.count(c) / len(y))
        for count, t in zip(doc, totals):
            s += count * math.log((t + 1) / denom)
        scores.append(s)
    top = max(scores)
    exps = [math.exp(s - top) for s in scores]
    return [round(e / sum(exps), 4) for e in exps]


@O
def mnb_proba(X, y, doc):
    return MultinomialNB(alpha=1.0).fit(X, y).predict_proba([doc])[0].round(4)


Q(None, "Bernoulli Naive Bayes", "Hard", "Word present or absent",
  "Features are 0/1 (word present). Fit Bernoulli NB (α = 1) and return P(class | x) rounded to 4 decimals. Absent words count too.",
  [(([[1, 1, 0], [1, 0, 0], [0, 1, 1], [0, 0, 1]], ["a", "a", "b", "b"], [1, 0, 1]), [0.5, 0.5])],
  ("P(word | class) = (docs with word + 1)/(docs + 2); multiply p for present words and (1 − p) for absent ones.", "O(k·V)", "O(k·V)"),
  ("<code>BernoulliNB()</code>.", "O(n·V)", "O(k·V)"),
  names=["X", "y", "x"])


@B
def bnb_proba(X, y, x):
    scores = []
    for c in sorted(set(y)):
        rows = [r for r, label in zip(X, y) if label == c]
        s = math.log(len(rows) / len(X))
        for j, present in enumerate(x):
            p = (sum(r[j] for r in rows) + 1) / (len(rows) + 2)
            s += math.log(p if present else 1 - p)
        scores.append(s)
    top = max(scores)
    exps = [math.exp(s - top) for s in scores]
    return [round(e / sum(exps), 4) for e in exps]


@O
def bnb_proba(X, y, x):
    return BernoulliNB(alpha=1.0).fit(X, y).predict_proba([x])[0].round(4)


Q(None, "Hinge Loss", "Easy", "The SVM's loss",
  "Labels are ±1 and scores are the model's raw outputs. Return mean max(0, 1 − y·score), rounded to 4 decimals.",
  [(([1, -1, 1, -1], [2.0, -0.5, 0.3, 1.2]), 0.85)],
  ("Loop with max(0, …).", "O(n)", "O(1)"),
  ("<code>hinge_loss(y, scores)</code>.", "O(n)", "O(1)"),
  names=["y", "scores"])


@B
def hinge(y, scores):
    return round(sum(max(0, 1 - a * s) for a, s in zip(y, scores)) / len(y), 4)


@O
def hinge(y, scores):
    return round(hinge_loss(y, scores), 4)


Q(None, "Widest Margin Between Two Points", "Hard", "Hard-margin SVM",
  "Train a linear SVM on just one positive point p and one negative point n. Return (w, b) rounded to 3 decimals.",
  [(([3, 3], [1, 1]), ([0.5, 0.5], -2.0)), (([4, 0], [0, 2]), ([0.4, -0.2], -0.6))],
  ("The best line is the perpendicular bisector with w·p + b = 1 and w·n + b = −1: w = 2(p − n)/‖p − n‖², b = −w·(p + n)/2.", "O(d)", "O(d)"),
  ("<code>SVC(kernel='linear', C=1e6)</code> (a huge C makes the margin hard).", "O(1)", "O(1)"),
  names=["p", "n"])


@B
def two_point_svm(p, n):
    diff = [a - b for a, b in zip(p, n)]
    sq = sum(d * d for d in diff)
    w = [2 * d / sq for d in diff]
    mid = [(a + b) / 2 for a, b in zip(p, n)]
    b = -sum(wi * m for wi, m in zip(w, mid))
    return ([round(v, 3) for v in w], round(b, 3))


@O
def two_point_svm(p, n):
    model = SVC(kernel="linear", C=1e6).fit([p, n], [1, -1])
    return (model.coef_[0].round(3), round(model.intercept_[0], 3))


Q(None, "Margin Width", "Medium", "2 / ‖w‖",
  "For the SVM trained on one positive point p and one negative point n, return the width of the margin, rounded to 4 decimals.",
  [(([3, 3], [1, 1]), 2.8284), (([4, 0], [0, 2]), 4.4721)],
  ("The margin is the full distance between the two points: ‖p − n‖.", "O(d)", "O(1)"),
  ("Fit <code>SVC</code> and compute 2/‖w‖.", "O(1)", "O(1)"),
  names=["p", "n"])


@B
def margin_width(p, n):
    return round(math.sqrt(sum((a - b) ** 2 for a, b in zip(p, n))), 4)


@O
def margin_width(p, n):
    model = SVC(kernel="linear", C=1e6).fit([p, n], [1, -1])
    return round(2 / np.linalg.norm(model.coef_[0]), 4)


Q(None, "Points Inside the Margin", "Medium", "Support vectors and violations",
  "A linear SVM has weights w and bias b. For each point return (predicted label ±1, True if |w·x + b| &lt; 1).",
  [(([[2, 2], [0, 0], [1, 0.8], [3, 0]], [1.0, 1.0], -2.0), [(1, False), (-1, False), (-1, True), (1, False)])],
  ("Score each point by hand.", "O(n·d)", "O(n)"),
  ("A <code>LinearSVC</code> holding those coefficients: <code>predict</code> and <code>decision_function</code>.", "O(n·d)", "O(n)"),
  names=["X", "w", "b"])


@B
def margin_check(X, w, b):
    out = []
    for row in X:
        z = b + sum(wi * xi for wi, xi in zip(w, row))
        out.append((1 if z > 0 else -1, abs(z) < 1))
    return out


@O
def margin_check(X, w, b):
    model = LinearSVC()
    model.coef_, model.intercept_, model.classes_ = np.array([w]), np.array([b]), np.array([-1, 1])
    z = model.decision_function(np.array(X, dtype=float))
    return [(int(p), bool(abs(s) < 1)) for p, s in zip(model.predict(np.array(X, dtype=float)), z)]


Q(None, "RBF Kernel", "Easy", "Similarity that fades with distance",
  "Return the matrix K[i][j] = exp(−γ·‖xᵢ − xⱼ‖²), rounded to 4 decimals.",
  [(([[0, 0], [1, 0], [3, 4]], 0.5), [[1.0, 0.6065, 0.0], [0.6065, 1.0, 0.0], [0.0, 0.0, 1.0]])],
  ("Double loop over pairs.", "O(n²·d)", "O(n²)"),
  ("<code>rbf_kernel(X, gamma=γ)</code>.", "O(n²·d)", "O(n²)"),
  names=["X", "gamma"])


@B
def rbf(X, gamma):
    return [[round(math.exp(-gamma * sum((a - b) ** 2 for a, b in zip(p, q))), 4) for q in X] for p in X]


@O
def rbf(X, gamma):
    return rbf_kernel(X, gamma=gamma).round(4)


Q(None, "The Kernel Trick", "Hard", "A dot product in a bigger space, without going there",
  "For 2-D points x and z, return (dot product of the explicit degree-2 feature maps, the polynomial kernel (x·z + 1)²). They are equal.",
  [(([1, 2], [3, 1]), (36, 36.0)), (([0.5, -1], [2, 2]), (0.0, 0.0))],
  ("Build φ(v) = [1, √2v₁, √2v₂, v₁², √2v₁v₂, v₂²] for both points and take their dot product — that value twice.", "O(d²)", "O(d²)"),
  ("<code>polynomial_kernel([x], [z], degree=2, gamma=1, coef0=1)</code> computes it directly from x·z.", "O(d)", "O(1)"),
  names=["x", "z"])


@B
def kernel_trick(x, z):
    def phi(v):
        r = math.sqrt(2)
        return [1, r * v[0], r * v[1], v[0] ** 2, r * v[0] * v[1], v[1] ** 2]
    value = round(sum(a * b for a, b in zip(phi(x), phi(z))), 4)
    return (value, value)


@O
def kernel_trick(x, z):
    k = polynomial_kernel([x], [z], degree=2, gamma=1, coef0=1)[0, 0]
    explicit = round((np.dot(x, z) + 1) ** 2, 4)
    return (explicit, round(k, 4))
