from lib import *
import math
import numpy as np
from sklearn.ensemble import (VotingClassifier, RandomForestClassifier, BaggingRegressor,
                              GradientBoostingRegressor)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import resample


TOPIC(
    id="ensembles", title="Ensembles: Bagging, Forests & Boosting", glyph="🌲🌲🌲",
    blurb="Many models beat one: voting, bootstrap samples and bagging, random forests from the inside, gradient boosting built from scratch, AdaBoost's weights, and why averaging reduces variance.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">VotingClassifier([("lr", lr), ("tree", tree), ("knn", knn)], voting="hard" | "soft")
RandomForestClassifier(n_estimators=300, max_features="sqrt", oob_score=True, random_state=0)
BaggingRegressor(DecisionTreeRegressor(), n_estimators=50)
GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=3)
HistGradientBoostingClassifier()     # fast boosting for big tables (like LightGBM)
StackingClassifier(estimators=[...], final_estimator=LogisticRegression())</code></pre>
<p><b>Bagging</b> averages independent models to cut variance; <b>boosting</b> adds models one after another, each fixing the last one's errors, to cut bias.</p>
""")

X = [[1, 2], [2, 1], [3, 3], [4, 2], [5, 5], [6, 4], [2, 3], [5, 2], [7, 6], [3, 6]]
Y = [0, 0, 1, 0, 1, 1, 0, 0, 1, 1]
QX = [[1, 1], [4, 4], [6, 6], [3, 2], [5, 3]]
XR = [[1], [2], [3], [4], [5], [6], [7], [8]]
YR = [3.0, 4.5, 4.0, 7.5, 8.0, 7.0, 11.5, 12.0]


def three_models():
    return [LogisticRegression(), DecisionTreeClassifier(max_depth=2, random_state=0), KNeighborsClassifier(n_neighbors=3)]


def stump_fit(x, r):
    """Regression stump on one feature: best threshold by squared error, leaf means."""
    best = None
    values = sorted(set(x))
    for lo, hi in zip(values, values[1:]):
        t = (lo + hi) / 2
        left = [v for a, v in zip(x, r) if a <= t]
        right = [v for a, v in zip(x, r) if a > t]
        ml, mr = sum(left) / len(left), sum(right) / len(right)
        sse = sum((v - ml) ** 2 for v in left) + sum((v - mr) ** 2 for v in right)
        if best is None or sse < best[0] - 1e-12:
            best = (sse, t, ml, mr)
    return best[1:]


Q(None, "Hard Voting by Hand", "Medium", "Majority of three models",
  "Fit logistic regression, a depth-2 tree and 3-NN on (X, y); predict each query by majority vote.",
  [((X, Y, QX), [0, 1, 1, 0, 1])],
  ("Fit the three models separately and count their votes per query.", "O(models·fit)", "O(m)"),
  ("<code>VotingClassifier(..., voting='hard')</code>.", "O(models·fit)", "O(m)"),
  names=["X", "y", "queries"])


@B
def hard_vote(X, y, queries):
    preds = [m.fit(X, y).predict(queries) for m in three_models()]
    out = []
    for i in range(len(queries)):
        votes = [int(p[i]) for p in preds]
        out.append(max(sorted(set(votes)), key=votes.count))
    return out


@O
def hard_vote(X, y, queries):
    names = ["lr", "tree", "knn"]
    vote = VotingClassifier(list(zip(names, three_models())), voting="hard").fit(X, y)
    return vote.predict(queries)


Q(None, "Soft Voting", "Medium", "Average the probabilities",
  "Average the three models' P(class 1) for each query and return them, rounded to 4 decimals.",
  [((X, Y, QX), [0.0093, 0.7993, 0.9942, 0.1642, 0.6293])],
  ("Fit each model, average their predict_proba columns by hand.", "O(models·fit)", "O(m)"),
  ("<code>VotingClassifier(..., voting='soft').predict_proba</code>.", "O(models·fit)", "O(m)"),
  names=["X", "y", "queries"])


@B
def soft_vote(X, y, queries):
    probs = [m.fit(X, y).predict_proba(queries)[:, 1] for m in three_models()]
    return [round(sum(p[i] for p in probs) / 3, 4) for i in range(len(queries))]


@O
def soft_vote(X, y, queries):
    vote = VotingClassifier(list(zip(["lr", "tree", "knn"], three_models())), voting="soft").fit(X, y)
    return vote.predict_proba(queries)[:, 1].round(4)


Q(None, "A Bootstrap Sample", "Easy", "Sampling with replacement",
  "Draw n row indices with replacement using np.random.RandomState(seed).randint(0, n, n).",
  [((8, 0), [4, 7, 5, 0, 3, 3, 3, 7]), ((5, 42), [3, 4, 2, 4, 4])],
  ("A seeded random generator, one randint call.", "O(n)", "O(n)"),
  ("<code>sklearn.utils.resample(range(n), random_state=seed)</code>.", "O(n)", "O(n)"),
  names=["n", "seed"])


@B
def bootstrap(n, seed):
    rng = np.random.RandomState(seed)
    return rng.randint(0, n, n)


@O
def bootstrap(n, seed):
    return resample(np.arange(n), random_state=seed)


Q(None, "Out-of-Bag Rows", "Easy", "Free validation data",
  "Given the indices of a bootstrap sample of n rows, return the rows that were never picked (sorted).",
  [(([0, 3, 3, 1, 7, 0, 5, 3], 8), [2, 4, 6]), (([2, 2, 2], 3), [0, 1])],
  ("Mark the picked rows, list the rest.", "O(n)", "O(n)"),
  ("<code>np.setdiff1d(np.arange(n), sample)</code>.", "O(n log n)", "O(n)"),
  names=["sample", "n"])


@B
def out_of_bag(sample, n):
    picked = set(sample)
    return [i for i in range(n) if i not in picked]


@O
def out_of_bag(sample, n):
    return np.setdiff1d(np.arange(n), sample)


Q(None, "Chance a Row Is Left Out", "Easy", "≈ 1/e ≈ 36.8%",
  "Return the probability that a given row is not in a bootstrap sample of size n, rounded to 4 decimals.",
  [((10,), 0.3487), ((1000,), 0.3677)],
  ("Each of the n draws misses it with probability (1 − 1/n); multiply n times.", "O(n)", "O(1)"),
  ("Formula (1 − 1/n)ⁿ, which tends to e⁻¹.", "O(1)", "O(1)"))


@B
def left_out(n):
    p = 1.0
    for _ in range(n):
        p *= 1 - 1 / n
    return round(p, 4)


@O
def left_out(n):
    return round((1 - 1 / n) ** n, 4)


Q(None, "Forest Probability = Average of Its Trees", "Medium", "Inside a random forest",
  "Fit RandomForestClassifier(n_estimators=5, random_state=0) and return P(class 1) for each query, rounded to 4 decimals.",
  [((X, Y, QX), [0.0, 0.8, 1.0, 0.0, 0.4])],
  ("Loop over <code>forest.estimators_</code> and average each tree's probabilities yourself.", "O(trees·depth)", "O(m)"),
  ("<code>forest.predict_proba</code>.", "O(trees·depth)", "O(m)"),
  names=["X", "y", "queries"])


@B
def forest_proba(X, y, queries):
    forest = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    total = np.zeros(len(queries))
    for tree in forest.estimators_:
        total += tree.predict_proba(np.array(queries, dtype=float))[:, 1]
    return (total / len(forest.estimators_)).round(4)


@O
def forest_proba(X, y, queries):
    forest = RandomForestClassifier(n_estimators=5, random_state=0).fit(X, y)
    return forest.predict_proba(queries)[:, 1].round(4)


Q(None, "Count the Trees' Votes", "Easy", "How confident is the forest?",
  "Fit RandomForestClassifier(n_estimators=7, random_state=0) and return, for each query, how many trees vote class 1.",
  [((X, Y, QX), [0, 6, 7, 0, 4])],
  ("Ask every tree and count.", "O(trees·m)", "O(m)"),
  ("Stack all trees' predictions into a matrix and sum the columns.", "O(trees·m)", "O(trees·m)"),
  names=["X", "y", "queries"])


@B
def tree_votes(X, y, queries):
    forest = RandomForestClassifier(n_estimators=7, random_state=0).fit(X, y)
    counts = [0] * len(queries)
    for tree in forest.estimators_:
        for i, p in enumerate(tree.predict(np.array(queries, dtype=float))):
            counts[i] += int(forest.classes_[int(p)] == 1)
    return counts


@O
def tree_votes(X, y, queries):
    forest = RandomForestClassifier(n_estimators=7, random_state=0).fit(X, y)
    votes = np.array([t.predict(np.array(queries, dtype=float)) for t in forest.estimators_])
    return (forest.classes_[votes.astype(int)] == 1).sum(axis=0)


Q(None, "Forest Feature Importances", "Medium", "Averaged over trees",
  "Fit RandomForestClassifier(n_estimators=10, random_state=0) and return the feature importances, rounded to 4 decimals.",
  [((X, Y), [0.272, 0.728])],
  ("Average every tree's <code>feature_importances_</code>, then normalise to sum to 1.", "O(trees·d)", "O(d)"),
  ("<code>forest.feature_importances_</code>.", "O(trees·d)", "O(d)"),
  names=["X", "y"])


@B
def forest_importances(X, y):
    forest = RandomForestClassifier(n_estimators=10, random_state=0).fit(X, y)
    total = [0.0] * len(X[0])
    for tree in forest.estimators_:
        for j, v in enumerate(tree.feature_importances_):
            total[j] += v
    s = sum(total)
    return [round(v / s, 4) for v in total]


@O
def forest_importances(X, y):
    return RandomForestClassifier(n_estimators=10, random_state=0).fit(X, y).feature_importances_.round(4)


Q(None, "Bagging = Average of Trees", "Medium", "Bagging for regression",
  "Fit BaggingRegressor(DecisionTreeRegressor(), n_estimators=4, random_state=0) and predict each query, rounded to 4 decimals.",
  [((XR, YR, [[0], [3.5], [6.2], [9]]), [3.25, 5.75, 8.125, 9.25])],
  ("Average the predictions of <code>bag.estimators_</code> yourself.", "O(trees·m)", "O(m)"),
  ("<code>bag.predict</code>.", "O(trees·m)", "O(m)"),
  names=["X", "y", "queries"])


@B
def bagging_predict(X, y, queries):
    bag = BaggingRegressor(DecisionTreeRegressor(), n_estimators=4, random_state=0).fit(X, y)
    Q_ = np.array(queries, dtype=float)
    preds = [est.predict(Q_[:, feats]) for est, feats in zip(bag.estimators_, bag.estimators_features_)]
    return [round(sum(p[i] for p in preds) / len(preds), 4) for i in range(len(queries))]


@O
def bagging_predict(X, y, queries):
    bag = BaggingRegressor(DecisionTreeRegressor(), n_estimators=4, random_state=0).fit(X, y)
    return bag.predict(queries).round(4)


Q(None, "Features Tried at Each Split", "Easy", "max_features",
  "A random forest with d features considers how many at each split for max_features = 'sqrt' and 'log2'? Return (sqrt count, log2 count).",
  [((16,), (4, 4)), ((10,), (3, 3))],
  ("int(√d) and int(log₂ d), at least 1.", "O(1)", "O(1)"),
  ("Fit tiny forests and read a tree's <code>max_features_</code>.", "O(fit)", "O(1)"))


@B
def features_per_split(d):
    return (max(1, int(math.sqrt(d))), max(1, int(math.log2(d))))


@O
def features_per_split(d):
    Xd, yd = np.eye(d + 2)[:, :d], np.arange(d + 2) % 2
    a = RandomForestClassifier(n_estimators=1, max_features="sqrt", random_state=0).fit(Xd, yd)
    b = RandomForestClassifier(n_estimators=1, max_features="log2", random_state=0).fit(Xd, yd)
    return (a.estimators_[0].max_features_, b.estimators_[0].max_features_)


Q(None, "Boosting Starts From the Mean", "Easy", "The initial guess",
  "Gradient boosting for squared error starts by predicting the mean of y. Return that value, rounded to 4 decimals.",
  [((XR, YR), 7.1875)],
  ("Average y.", "O(n)", "O(1)"),
  ("<code>GradientBoostingRegressor().fit(X, y).init_.predict</code>.", "O(fit)", "O(1)"),
  names=["X", "y"])


@B
def boost_init(X, y):
    return round(sum(y) / len(y), 4)


@O
def boost_init(X, y):
    gb = GradientBoostingRegressor(n_estimators=1, random_state=0).fit(X, y)
    return round(gb.init_.predict(np.array(X[:1], dtype=float))[0], 4)


Q(None, "The First Tree Fits the Residuals", "Medium", "Learning from mistakes",
  "With depth-1 trees, the first boosting tree is fitted to the residuals y − mean. Return (threshold, left leaf value, right leaf value), rounded to 4 decimals.",
  [((XR, YR), (6.5, -1.5208, 4.5625))],
  ("Residuals by hand, then a regression stump on them.", "O(n²)", "O(n)"),
  ("<code>gb.estimators_[0, 0].tree_</code> after fitting <code>GradientBoostingRegressor(max_depth=1)</code>.", "O(fit)", "O(1)"),
  names=["X", "y"])


@B
def first_tree(X, y):
    mean = sum(y) / len(y)
    residuals = [v - mean for v in y]
    t, left, right = stump_fit([row[0] for row in X], residuals)
    return (t, round(left, 4), round(right, 4))


@O
def first_tree(X, y):
    gb = GradientBoostingRegressor(n_estimators=1, max_depth=1, learning_rate=1.0, random_state=0).fit(X, y)
    t = gb.estimators_[0, 0].tree_
    return (float(t.threshold[0]), round(t.value[1][0][0], 4), round(t.value[2][0][0], 4))


Q(None, "Gradient Boosting From Scratch", "Hard", "Add stumps that fix the residuals",
  "Boost depth-1 trees on one feature: start at the mean; each stage fits a stump to the current residuals and adds learning_rate × its prediction. Predict the queries after n stages, rounded to 4 decimals.",
  [((XR, YR, 3, 0.5, [[2], [5.5], [8]]), [4.4818, 7.5943, 10.6359]), ((XR, YR, 10, 0.1, [[2], [5.5], [8]]), [5.4051, 7.3405, 9.6317])],
  ("The loop: residuals → stump → shrink → add. Repeat n times.", "O(stages·n²)", "O(n)"),
  ("<code>GradientBoostingRegressor(n_estimators=n, learning_rate=lr, max_depth=1)</code>.", "O(stages·n log n)", "O(n)"),
  names=["X", "y", "stages", "lr", "queries"])


@B
def boost_from_scratch(X, y, stages, lr, queries):
    x = [row[0] for row in X]
    base = sum(y) / len(y)
    pred = [base] * len(y)
    q_pred = [base] * len(queries)
    for _ in range(stages):
        residuals = [a - b for a, b in zip(y, pred)]
        t, left, right = stump_fit(x, residuals)
        pred = [p + lr * (left if a <= t else right) for p, a in zip(pred, x)]
        q_pred = [p + lr * (left if q[0] <= t else right) for p, q in zip(q_pred, queries)]
    return [round(v, 4) for v in q_pred]


@O
def boost_from_scratch(X, y, stages, lr, queries):
    gb = GradientBoostingRegressor(n_estimators=stages, learning_rate=lr, max_depth=1, random_state=0).fit(X, y)
    return gb.predict(queries).round(4)


Q(None, "Watching Boosting Improve", "Medium", "Staged predictions",
  "Boost depth-1 trees (learning rate 0.5) for n stages and return the prediction for one query after each stage, rounded to 4 decimals.",
  [((XR, YR, 4, [7]), [9.4688, 10.2469, 10.6359, 11.193])],
  ("Record the running prediction inside the boosting loop.", "O(stages·n²)", "O(stages)"),
  ("<code>gb.staged_predict([q])</code>.", "O(stages·n log n)", "O(stages)"),
  names=["X", "y", "stages", "q"])


@B
def staged(X, y, stages, q):
    x = [row[0] for row in X]
    pred = [sum(y) / len(y)] * len(y)
    current = sum(y) / len(y)
    history = []
    for _ in range(stages):
        t, left, right = stump_fit(x, [a - b for a, b in zip(y, pred)])
        pred = [p + 0.5 * (left if a <= t else right) for p, a in zip(pred, x)]
        current += 0.5 * (left if q[0] <= t else right)
        history.append(round(current, 4))
    return history


@O
def staged(X, y, stages, q):
    gb = GradientBoostingRegressor(n_estimators=stages, learning_rate=0.5, max_depth=1, random_state=0).fit(X, y)
    return [round(p[0], 4) for p in gb.staged_predict([q])]


Q(None, "Learning Rate vs Training Error", "Medium", "Shrinkage",
  "For each learning rate, boost 5 depth-1 trees and return the training MSE, rounded to 4 decimals.",
  [((XR, YR, [0.1, 0.5, 1.0]), [4.649, 0.205, 0.0911])],
  ("Run the from-scratch booster once per learning rate.", "O(k·stages·n²)", "O(n)"),
  ("Fit <code>GradientBoostingRegressor</code> per rate; MSE of <code>predict(X)</code>.", "O(k·stages·n log n)", "O(n)"),
  names=["X", "y", "rates"])


@B
def lr_errors(X, y, rates):
    x = [row[0] for row in X]
    out = []
    for lr in rates:
        pred = [sum(y) / len(y)] * len(y)
        for _ in range(5):
            t, left, right = stump_fit(x, [a - b for a, b in zip(y, pred)])
            pred = [p + lr * (left if a <= t else right) for p, a in zip(pred, x)]
        out.append(round(sum((a - b) ** 2 for a, b in zip(y, pred)) / len(y), 4))
    return out


@O
def lr_errors(X, y, rates):
    out = []
    for lr in rates:
        gb = GradientBoostingRegressor(n_estimators=5, learning_rate=lr, max_depth=1, random_state=0).fit(X, y)
        out.append(round(float(np.mean((np.array(y) - gb.predict(X)) ** 2)), 4))
    return out


Q(None, "Weighted Error of a Weak Learner", "Easy", "AdaBoost, step 1",
  "Return Σ wᵢ over misclassified rows divided by Σ wᵢ, rounded to 4 decimals.",
  [(([1, 0, 1, 1, 0], [1, 1, 1, 0, 0], [0.1, 0.3, 0.2, 0.2, 0.2]), 0.5)],
  ("Loop adding the weights of the mistakes.", "O(n)", "O(1)"),
  ("NumPy: <code>w[y != pred].sum() / w.sum()</code>.", "O(n)", "O(n)"),
  names=["y", "pred", "w"])


@B
def weighted_error(y, pred, w):
    wrong = sum(wi for a, b, wi in zip(y, pred, w) if a != b)
    return round(wrong / sum(w), 4)


@O
def weighted_error(y, pred, w):
    y, pred, w = np.array(y), np.array(pred), np.array(w)
    return round(w[y != pred].sum() / w.sum(), 4)


Q(None, "AdaBoost: How Much Say Does a Model Get?", "Medium", "α = ln((1 − err)/err) + ln(K − 1)",
  "Return the SAMME weight α of a weak learner with weighted error err on a K-class problem, rounded to 4 decimals.",
  [((0.3, 2), 0.8473), ((0.5, 2), 0.0), ((0.4, 3), 1.0986)],
  ("Apply the formula with <code>math.log</code>.", "O(1)", "O(1)"),
  ("Same with <code>np.log</code> (vectorises over many learners).", "O(1)", "O(1)"),
  names=["err", "K"])


@B
def ada_alpha(err, K):
    return round(math.log((1 - err) / err) + math.log(K - 1), 4) + 0.0


@O
def ada_alpha(err, K):
    return round(float(np.log((1 - err) / err) + np.log(K - 1)), 4) + 0.0


Q(None, "AdaBoost: Reweight the Mistakes", "Medium", "Focus on the hard rows",
  "Multiply the weights of misclassified rows by e^α, leave the others, then normalise to sum to 1. Rounded to 4 decimals.",
  [(([1, 0, 1, 1, 0], [1, 1, 1, 0, 0], [0.2] * 5, 0.8473), [0.1304, 0.3043, 0.1304, 0.3043, 0.1304])],
  ("Loop: multiply mistakes by e^α; divide all by the new total.", "O(n)", "O(n)"),
  ("Vectorised with a boolean mask.", "O(n)", "O(n)"),
  names=["y", "pred", "w", "alpha"])


@B
def ada_reweight(y, pred, w, alpha):
    new = [wi * math.exp(alpha) if a != b else wi for a, b, wi in zip(y, pred, w)]
    s = sum(new)
    return [round(v / s, 4) for v in new]


@O
def ada_reweight(y, pred, w, alpha):
    w = np.array(w, dtype=float) * np.where(np.array(y) != np.array(pred), np.exp(alpha), 1.0)
    return (w / w.sum()).round(4)


Q(None, "Why Averaging Helps", "Medium", "Variance of an average of models",
  "k models each have error variance σ² and pairwise correlation ρ. Return the variance of their average, rounded to 4 decimals.",
  [((1.0, 0.0, 10), 0.1), ((1.0, 0.5, 10), 0.55), ((4.0, 1.0, 5), 4.0)],
  ("Build the k × k covariance matrix (σ² on the diagonal, ρσ² elsewhere), add every entry, divide by k².", "O(k²)", "O(1)"),
  ("Formula ρσ² + (1 − ρ)σ²/k — decorrelating the trees (random features) is what makes forests strong.", "O(1)", "O(1)"),
  names=["sigma2", "rho", "k"])


@B
def average_variance(sigma2, rho, k):
    total = 0.0
    for i in range(k):
        for j in range(k):
            total += sigma2 if i == j else rho * sigma2
    return round(total / (k * k), 4)


@O
def average_variance(sigma2, rho, k):
    return round(rho * sigma2 + (1 - rho) * sigma2 / k, 4)


Q(None, "Stacking: Learn How to Blend", "Hard", "A model on top of models",
  "Given two models' predictions p1, p2 and the targets y, fit y ≈ a + b·p1 + c·p2 (the meta-model). Return [a, b, c] rounded to 4 decimals.",
  [(([2.0, 4.1, 6.2, 7.9, 10.1], [1.5, 4.5, 5.5, 8.5, 9.5], [2, 4, 6, 8, 10]), [-0.0367, 0.884, 0.1152])],
  ("Normal equations with NumPy on the columns [1, p1, p2].", "O(n)", "O(1)"),
  ("<code>LinearRegression</code> as the final estimator (what <code>StackingRegressor</code> does with out-of-fold predictions).", "O(n)", "O(n)"),
  names=["p1", "p2", "y"])


@B
def stack(p1, p2, y):
    A = np.column_stack([np.ones(len(y)), p1, p2])
    return np.linalg.solve(A.T @ A, A.T @ np.array(y, dtype=float)).round(4) + 0.0


@O
def stack(p1, p2, y):
    meta = LinearRegression().fit(np.column_stack([p1, p2]), y)
    return np.concatenate([[meta.intercept_], meta.coef_]).round(4) + 0.0
