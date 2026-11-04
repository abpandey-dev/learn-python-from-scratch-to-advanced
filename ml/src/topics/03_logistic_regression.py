from lib import *
import math
import numpy as np
from scipy.special import expit, logit, softmax
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.metrics import log_loss, accuracy_score, zero_one_loss
from sklearn.preprocessing import Binarizer, label_binarize


TOPIC(
    id="logistic-regression", title="Logistic Regression & Classification", glyph="σ(z)",
    blurb="Predicting categories: the sigmoid, odds and log-odds, log-loss, training by Newton's method, decision boundaries, thresholds, regularisation, softmax for many classes, and the perceptron.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">model = LogisticRegression(C=1.0).fit(X_train, y_train)   # C = 1/regularisation strength
model.predict_proba(X)[:, 1]          # P(class 1)
model.predict(X)                      # class with p ≥ 0.5
model.coef_, model.intercept_         # log-odds weights
np.exp(model.coef_)                   # odds ratios
log_loss(y, p), accuracy_score(y, y_pred)
# p = σ(w·x + b) = 1 / (1 + e^−(w·x + b))</code></pre>
""")

XS = [1, 2, 3, 4, 5, 6]
YS = [0, 0, 1, 0, 1, 1]
X2 = [[1, 2], [2, 1], [3, 3], [4, 2], [5, 5], [6, 4], [2, 3], [5, 2]]
Y2 = [0, 0, 1, 0, 1, 1, 1, 0]


def newton_logistic(X, y, C=None, iters=50, weights=None):
    """Fit logistic regression exactly by Newton's method (sklearn's objective: Σ weight·log-loss + ‖w‖²/2C)."""
    A = np.column_stack([np.ones(len(X)), np.array(X, dtype=float)])
    y = np.array(y, dtype=float)
    s = np.ones(len(y)) if weights is None else np.array(weights, dtype=float)
    w = np.zeros(A.shape[1])
    penalty = np.eye(A.shape[1]) / C if C else np.zeros((A.shape[1], A.shape[1]))
    penalty[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-A @ w))
        grad = A.T @ (s * (p - y)) + penalty @ w
        H = A.T @ (A * (s * p * (1 - p))[:, None]) + penalty
        w = w - np.linalg.solve(H, grad)
    return w


Q(None, "Sigmoid Probabilities", "Easy", "Score → probability",
  "Turn raw scores z into probabilities σ(z) = 1/(1 + e⁻ᶻ), rounded to 4 decimals.",
  [(([-2, 0, 1, 3],), [0.1192, 0.5, 0.7311, 0.9526])],
  ("<code>math.exp</code> in a loop.", "O(n)", "O(n)"),
  ("<code>scipy.special.expit</code> (sklearn uses it inside LogisticRegression).", "O(n)", "O(n)"))


@B
def sigmoid(z):
    return [round(1 / (1 + math.exp(-v)), 4) for v in z]


@O
def sigmoid(z):
    return expit(np.array(z, dtype=float)).round(4)


Q(None, "Odds and Log-Odds", "Easy", "p → p/(1 − p) → log",
  "For each probability p return (odds, log-odds), rounded to 4 decimals.",
  [(([0.5, 0.8, 0.2],), [(1.0, 0.0), (4.0, 1.3863), (0.25, -1.3863)])],
  ("odds = p/(1 − p); log-odds = ln(odds).", "O(n)", "O(n)"),
  ("<code>scipy.special.logit</code> — the inverse of the sigmoid.", "O(n)", "O(n)"))


@B
def odds(ps):
    out = []
    for p in ps:
        o = p / (1 - p)
        out.append((round(o, 4), round(math.log(o), 4) + 0.0))
    return out


@O
def odds(ps):
    p = np.array(ps)
    return [(round(o, 4), round(l, 4) + 0.0) for o, l in zip(p / (1 - p), logit(p))]


Q(None, "Predict With Given Weights", "Easy", "Which side of the line?",
  "A trained model has weights w and bias b. Return the predicted class (1 if σ(w·x + b) ≥ 0.5) for each row of X.",
  [(([[1, 2], [3, 1], [0, 0], [2, 2]], [1.0, -1.5], 0.5), [0, 1, 1, 0])],
  ("Score each row; positive score ⇔ probability ≥ 0.5.", "O(n·d)", "O(n)"),
  ("Give a <code>LogisticRegression</code> those coefficients and call <code>predict</code>.", "O(n·d)", "O(n)"),
  names=["X", "w", "b"])


@B
def predict_given(X, w, b):
    out = []
    for row in X:
        z = b + sum(wi * xi for wi, xi in zip(w, row))
        out.append(1 if z >= 0 else 0)
    return out


@O
def predict_given(X, w, b):
    model = LogisticRegression()
    model.coef_, model.intercept_, model.classes_ = np.array([w]), np.array([b]), np.array([0, 1])
    return model.predict(np.array(X, dtype=float))


Q(None, "Binary Log-Loss", "Easy", "The training loss",
  "Return the average log-loss of probabilities p for labels y, rounded to 4 decimals.",
  [(([1, 0, 1, 1], [0.9, 0.2, 0.6, 0.95]), 0.2227), (([0, 1], [0.5, 0.5]), 0.6931)],
  ("−ln p for positives, −ln(1 − p) for negatives, averaged.", "O(n)", "O(1)"),
  ("<code>sklearn.metrics.log_loss</code>.", "O(n)", "O(1)"),
  names=["y", "p"])


@B
def binary_log_loss(y, p):
    total = 0
    for label, prob in zip(y, p):
        total += -math.log(prob) if label == 1 else -math.log(1 - prob)
    return round(total / len(y), 4)


@O
def binary_log_loss(y, p):
    return round(log_loss(y, p), 4)


Q(None, "Train Logistic Regression (One Feature)", "Hard", "Newton's method",
  "Fit an unregularised logistic regression P(y = 1) = σ(w·x + b). Return (w, b) rounded to 3 decimals.",
  [((XS, YS), (1.214, -4.249))],
  ("Newton's method from scratch: gradient Aᵀ(p − y), Hessian AᵀSA, update w ← w − H⁻¹g, ~20 iterations.", "O(iters·n·d²)", "O(d²)"),
  ("<code>LogisticRegression(C=1e10)</code> — a huge C means (almost) no penalty.", "O(iters·n·d)", "O(n·d)"),
  names=["x", "y"])


@B
def train_1d(x, y):
    b, w = newton_logistic([[v] for v in x], y)
    return (round(w, 3), round(b, 3))


@O
def train_1d(x, y):
    model = LogisticRegression(C=1e10, tol=1e-10, max_iter=1000).fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0, 0], 3), round(model.intercept_[0], 3))


Q(None, "Train Logistic Regression (Two Features)", "Hard", "Regularised, C = 1",
  "Fit logistic regression with sklearn's default L2 penalty (C = 1). Return [b, w₁, w₂] rounded to 3 decimals.",
  [((X2, Y2), [-3.483, -0.013, 1.32])],
  ("Newton's method on Σ log-loss + ‖w‖²/2 (the bias isn't penalised).", "O(iters·n·d²)", "O(d²)"),
  ("<code>LogisticRegression(C=1.0)</code>.", "O(iters·n·d)", "O(n·d)"),
  names=["X", "y"])


@B
def train_2d(X, y):
    return newton_logistic(X, y, C=1.0).round(3)


@O
def train_2d(X, y):
    model = LogisticRegression(C=1.0, tol=1e-10, max_iter=1000).fit(X, y)
    return np.concatenate([model.intercept_, model.coef_[0]]).round(3)


Q(None, "Probabilities for New Points", "Medium", "predict_proba",
  "Train on (x, y) without regularisation and return P(y = 1) for each new x, rounded to 3 decimals.",
  [((XS, YS, [0, 3.5, 7]), [0.014, 0.5, 0.986])],
  ("Newton fit, then the sigmoid of w·x + b.", "O(iters·n)", "O(m)"),
  ("<code>model.predict_proba(X_new)[:, 1]</code>.", "O(iters·n)", "O(m)"),
  names=["x", "y", "new_x"])


@B
def proba_new(x, y, new_x):
    b, w = newton_logistic([[v] for v in x], y)
    return [round(1 / (1 + math.exp(-(w * v + b))), 3) for v in new_x]


@O
def proba_new(x, y, new_x):
    model = LogisticRegression(C=1e10, tol=1e-10, max_iter=1000).fit(np.array(x).reshape(-1, 1), y)
    return model.predict_proba(np.array(new_x).reshape(-1, 1))[:, 1].round(3)


Q(None, "Find the Decision Boundary", "Medium", "Where p = 0.5",
  "Train on (x, y) without regularisation. Return the x where the predicted probability is exactly 0.5, rounded to 3 decimals.",
  [((XS, YS), 3.5)],
  ("σ(z) = 0.5 ⇔ z = 0 ⇔ x = −b/w.", "O(iters·n)", "O(1)"),
  ("Same formula with the fitted sklearn coefficients.", "O(iters·n)", "O(1)"),
  names=["x", "y"])


@B
def boundary(x, y):
    b, w = newton_logistic([[v] for v in x], y)
    return round(-b / w, 3)


@O
def boundary(x, y):
    model = LogisticRegression(C=1e10, tol=1e-10, max_iter=1000).fit(np.array(x).reshape(-1, 1), y)
    return round(-model.intercept_[0] / model.coef_[0, 0], 3)


Q(None, "Odds Ratio of a Feature", "Medium", "Interpreting a coefficient",
  "Train on (x, y) without regularisation. Return e^w — how the odds of class 1 multiply when x grows by 1 — rounded to 3 decimals.",
  [((XS, YS), 3.367)],
  ("Newton fit, then exp of the weight.", "O(iters·n)", "O(1)"),
  ("<code>np.exp(model.coef_)</code>.", "O(iters·n)", "O(1)"),
  names=["x", "y"])


@B
def odds_ratio(x, y):
    b, w = newton_logistic([[v] for v in x], y)
    return round(math.exp(w), 3)


@O
def odds_ratio(x, y):
    model = LogisticRegression(C=1e10, tol=1e-10, max_iter=1000).fit(np.array(x).reshape(-1, 1), y)
    return round(np.exp(model.coef_[0, 0]), 3)


Q(None, "Accuracy", "Easy", "Share of correct predictions",
  "Return the fraction of predictions equal to the true labels, rounded to 4 decimals.",
  [(([1, 0, 1, 1, 0], [1, 0, 0, 1, 1]), 0.6), ((["a", "b"], ["a", "b"]), 1.0)],
  ("Count matches in a loop.", "O(n)", "O(1)"),
  ("<code>accuracy_score</code>.", "O(n)", "O(1)"),
  names=["y_true", "y_pred"])


@B
def accuracy(y_true, y_pred):
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return round(correct / len(y_true), 4)


@O
def accuracy(y_true, y_pred):
    return round(accuracy_score(y_true, y_pred), 4)


Q(None, "Move the Threshold", "Easy", "Trading precision for recall",
  "Return 1 for every probability strictly greater than threshold t, else 0.",
  [(([0.1, 0.4, 0.55, 0.8], 0.5), [0.0, 0.0, 1.0, 1.0]), (([0.1, 0.4, 0.55, 0.8], 0.3), [0.0, 1.0, 1.0, 1.0])],
  ("Compare each probability with t.", "O(n)", "O(n)"),
  ("<code>Binarizer(threshold=t)</code>.", "O(n)", "O(n)"),
  names=["probs", "t"])


@B
def threshold(probs, t):
    return [1.0 if p > t else 0.0 for p in probs]


@O
def threshold(probs, t):
    return Binarizer(threshold=t).fit_transform(np.array(probs).reshape(-1, 1)).ravel()


Q(None, "Stronger Regularisation, Smaller Weight", "Hard", "The C parameter",
  "Fit one-feature logistic regression for each C (penalty ‖w‖²/2C). Return the learned w for each, rounded to 3 decimals.",
  [((XS, YS, [0.01, 0.1, 1, 100]), [0.034, 0.245, 0.767, 1.204])],
  ("Newton's method once per C.", "O(k·iters·n)", "O(k)"),
  ("<code>LogisticRegression(C=c)</code> once per C.", "O(k·iters·n)", "O(k)"),
  names=["x", "y", "Cs"])


@B
def weight_by_c(x, y, Cs):
    return [round(newton_logistic([[v] for v in x], y, C=c)[1], 3) for c in Cs]


@O
def weight_by_c(x, y, Cs):
    X = np.array(x).reshape(-1, 1)
    return [round(LogisticRegression(C=c, tol=1e-10, max_iter=1000).fit(X, y).coef_[0, 0], 3) for c in Cs]


Q(None, "Class-Weighted Logistic Regression", "Hard", "Imbalanced data",
  "Only 2 of 8 examples are positive. Fit logistic regression (C = 1) with class_weight='balanced' and return [b, w] rounded to 3 decimals.",
  [(([1, 2, 3, 4, 5, 6, 7, 8], [0, 0, 0, 1, 0, 0, 1, 0]), [-1.363, 0.281])],
  ("Weight each example by n / (2 × count of its class), then Newton's method on the weighted loss.", "O(iters·n)", "O(d²)"),
  ("<code>LogisticRegression(class_weight='balanced')</code>.", "O(iters·n)", "O(n)"),
  names=["x", "y"])


@B
def weighted_logistic(x, y):
    n_pos = sum(y)
    n_neg = len(y) - n_pos
    weights = [len(y) / (2 * n_pos) if label == 1 else len(y) / (2 * n_neg) for label in y]
    return newton_logistic([[v] for v in x], y, C=1.0, weights=weights).round(3)


@O
def weighted_logistic(x, y):
    model = LogisticRegression(class_weight="balanced", tol=1e-10, max_iter=1000).fit(np.array(x).reshape(-1, 1), y)
    return np.concatenate([model.intercept_, model.coef_[0]]).round(3)


Q(None, "Softmax for Many Classes", "Easy", "Scores → class probabilities",
  "Turn each row of scores into probabilities with softmax, rounded to 4 decimals.",
  [(([[2, 1, 0], [0, 0, 0]],), [[0.6652, 0.2447, 0.09], [0.3333, 0.3333, 0.3333]])],
  ("Exponentiate (after subtracting the row max) and divide by the row sum.", "O(n·k)", "O(n·k)"),
  ("<code>scipy.special.softmax(scores, axis=1)</code>.", "O(n·k)", "O(n·k)"))


@B
def softmax_rows(scores):
    out = []
    for row in scores:
        top = max(row)
        e = [math.exp(v - top) for v in row]
        s = sum(e)
        out.append([round(v / s, 4) for v in e])
    return out


@O
def softmax_rows(scores):
    return softmax(np.array(scores, dtype=float), axis=1).round(4)


Q(None, "Multiclass Prediction From Weights", "Medium", "Highest score wins",
  "W has one row of weights per class (classes 0, 1, 2…), b one bias per class. Return the predicted class of each row of X.",
  [(([[1, 0], [0, 1], [-1, -1]], [[2, 1], [0, 3], [-2, -2]], [0, 0, 1]), [0, 1, 2])],
  ("Score every class for every row, take the largest.", "O(n·k·d)", "O(k)"),
  ("A <code>LogisticRegression</code> holding those coefficients; <code>predict</code> takes the argmax.", "O(n·k·d)", "O(n·k)"),
  names=["W", "X", "b"])


@B
def multiclass_predict(W, X, b):
    out = []
    for row in X:
        scores = [bk + sum(w * x for w, x in zip(wk, row)) for wk, bk in zip(W, b)]
        out.append(scores.index(max(scores)))
    return out


@O
def multiclass_predict(W, X, b):
    model = LogisticRegression()
    model.coef_, model.intercept_ = np.array(W, dtype=float), np.array(b, dtype=float)
    model.classes_ = np.arange(len(W))
    return model.predict(np.array(X, dtype=float))


Q(None, "Multiclass Log-Loss", "Medium", "Categorical cross-entropy",
  "Each row of P holds class probabilities; y holds the true class index. Return the mean of −ln P[true class], rounded to 4 decimals.",
  [(([0, 2, 1], [[0.7, 0.2, 0.1], [0.1, 0.1, 0.8], [0.3, 0.4, 0.3]]), 0.4987)],
  ("Pick out the true class's probability in each row.", "O(n)", "O(1)"),
  ("<code>log_loss(y, P, labels=[0, 1, 2])</code>.", "O(n·k)", "O(1)"),
  names=["y", "P"])


@B
def multi_log_loss(y, P):
    return round(sum(-math.log(row[c]) for c, row in zip(y, P)) / len(y), 4)


@O
def multi_log_loss(y, P):
    return round(log_loss(y, P, labels=list(range(len(P[0])))), 4)


Q(None, "One-vs-Rest Targets", "Easy", "One binary problem per class",
  "Turn class labels into a 0/1 column per class (sorted classes) — the targets of one-vs-rest training.",
  [((["cat", "dog", "bird", "cat"],), [[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]])],
  ("For each class, mark rows equal to it.", "O(n·k)", "O(n·k)"),
  ("<code>label_binarize(y, classes=…)</code>.", "O(n·k)", "O(n·k)"))


@B
def one_vs_rest(y):
    classes = sorted(set(y))
    return [[1 if label == c else 0 for c in classes] for label in y]


@O
def one_vs_rest(y):
    return label_binarize(y, classes=sorted(set(y)))


Q(None, "Count the Mistakes", "Easy", "Zero-one loss",
  "Return how many predictions are wrong.",
  [(([1, 0, 1, 1, 0], [1, 1, 1, 0, 0]), 2)],
  ("Count mismatches.", "O(n)", "O(1)"),
  ("<code>zero_one_loss(y, y_pred, normalize=False)</code>.", "O(n)", "O(1)"),
  names=["y_true", "y_pred"])


@B
def mistakes(y_true, y_pred):
    return sum(1 for a, b in zip(y_true, y_pred) if a != b)


@O
def mistakes(y_true, y_pred):
    return int(zero_one_loss(y_true, y_pred, normalize=False))


Q(None, "Gradient of the Log-Loss", "Medium", "Xᵀ(p − y) / n",
  "At weights w and bias b, return the gradient of the average log-loss as [∂/∂b, ∂/∂w₁, …], rounded to 4 decimals.",
  [((X2, Y2, [0.5, -0.5], 0.0), [0.0822, 0.222, -0.3085])],
  ("Loop over examples, accumulating (p − y)·x.", "O(n·d)", "O(d)"),
  ("Vectorised NumPy: <code>A.T @ (expit(A @ w) - y) / n</code> with a column of 1s in A.", "O(n·d)", "O(n·d)"),
  names=["X", "y", "w", "b"])


@B
def logloss_grad(X, y, w, b):
    n = len(X)
    g = [0.0] * (len(w) + 1)
    for row, target in zip(X, y):
        p = 1 / (1 + math.exp(-(b + sum(a * c for a, c in zip(w, row)))))
        g[0] += (p - target) / n
        for j, x in enumerate(row):
            g[j + 1] += (p - target) * x / n
    return [round(v, 4) for v in g]


@O
def logloss_grad(X, y, w, b):
    A = np.column_stack([np.ones(len(X)), np.array(X, dtype=float)])
    p = expit(A @ np.concatenate([[b], w]))
    return (A.T @ (p - np.array(y)) / len(y)).round(4)


Q(None, "Train a Perceptron", "Hard", "The original neural unit",
  "Train a perceptron (labels 0/1, learning rate 1, no shuffling, 10 passes): on each mistake add (or subtract) the example to the weights and bias. Return [b, w₁, w₂].",
  [(([[2, 1], [3, 4], [-1, -2], [-2, 1], [1, 3], [-3, -1]], [1, 1, 0, 0, 1, 0]), [1.0, 2.0, 1.0])],
  ("Loop over the data in order; if sign(w·x + b) is wrong, w += y·x and b += y with y as ±1.", "O(passes·n·d)", "O(d)"),
  ("<code>Perceptron(shuffle=False, eta0=1, max_iter=10, tol=None)</code>.", "O(passes·n·d)", "O(d)"),
  names=["X", "y"])


@B
def perceptron(X, y):
    w = [0.0] * len(X[0])
    b = 0.0
    for _ in range(10):
        for row, label in zip(X, y):
            target = 1 if label == 1 else -1
            score = b + sum(wi * xi for wi, xi in zip(w, row))
            if target * score <= 0:
                w = [wi + target * xi for wi, xi in zip(w, row)]
                b += target
    return [b] + w


@O
def perceptron(X, y):
    model = Perceptron(shuffle=False, eta0=1.0, max_iter=10, tol=None).fit(X, y)
    return np.concatenate([model.intercept_, model.coef_[0]])
