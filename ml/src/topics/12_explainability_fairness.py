from lib import *
import math
import re
from itertools import permutations, combinations
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance, partial_dependence
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, precision_recall_curve, balanced_accuracy_score, r2_score
from sklearn.utils.class_weight import compute_class_weight


TOPIC(
    id="explainability-fairness", title="Explainability, Fairness & Imbalanced Data", glyph="⚖",
    blurb="Open the black box and check it is fair: linear contributions and Shapley values, permutation importance, partial dependence, counterfactuals, fairness metrics across groups, calibration, thresholds and class weights for imbalanced data, and privacy basics.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">permutation_importance(model, X_val, y_val, n_repeats=10, random_state=0)
partial_dependence(model, X, [feature], kind="average")
shap.Explainer(model, X_background)(X_rows)          # Shapley values (shap library)
selection_rate = y_pred[group == g].mean()            # demographic parity
tpr = y_pred[(group == g) &amp; (y == 1)].mean()         # equal opportunity
calibration_curve(y, p, n_bins=10); brier_score_loss(y, p)
compute_class_weight("balanced", classes=c, y=y); LogisticRegression(class_weight="balanced")
precision_recall_curve(y, p)                          # choose a threshold</code></pre>
""")

rng = np.random.default_rng(0)
XR = np.round(rng.uniform(0, 10, size=(60, 3)), 1)
YR = np.round(3 * XR[:, 0] + 1.0 * XR[:, 1] + rng.normal(0, 1, 60), 2)
XR, YR = XR.tolist(), YR.tolist()


Q(None, "Explain a Linear Prediction", "Medium", "Contributions (exact SHAP for linear models)",
  "Fit a linear regression on X, y. For row <code>i</code>, return <code>(base, contributions)</code> where base = mean prediction and contribution_j = coef_j × (x_ij − mean_j); they add up to the prediction. Round to 3.",
  [((XR, YR, 0), (21.913, [2.867, -2.853, 0.192])), ((XR, YR, 5), (21.913, [-10.944, 2.771, -0.012]))],
  ("Solve the normal equations (XᵀX)β = Xᵀy with an intercept column yourself.", "O(nd² + d³)", "O(d²)"),
  ("<code>LinearRegression</code>, then coef × (row − column means).", "O(nd² + d³)", "O(d)"),
  viz=(XR, YR, 0))


@B
def linear_contrib(X, y, i):
    A = np.column_stack([np.ones(len(X)), np.array(X)])
    beta = np.linalg.solve(A.T @ A, A.T @ np.array(y))
    coef = beta[1:]
    means = np.array(X).mean(axis=0)
    base = beta[0] + coef @ means
    return (round(float(base), 3), [round(float(c), 3) for c in coef * (np.array(X[i]) - means)])


@O
def linear_contrib(X, y, i):
    X = np.array(X)
    m = LinearRegression().fit(X, y)
    base = m.predict(X).mean()
    return (round(float(base), 3), np.round(m.coef_ * (X[i] - X.mean(axis=0)), 3).tolist())


GAME = {(): 0, ("a",): 10, ("b",): 20, ("c",): 5, ("a", "b"): 40, ("a", "c"): 15, ("b", "c"): 25, ("a", "b", "c"): 50}


Q(None, "Shapley Values by Hand", "Hard", "Fair credit for each feature",
  "<code>v</code> maps every sorted tuple of players to the value that team earns. Return each player's Shapley value (sorted by player), rounded to 4.",
  [((GAME,), {'a': 16.6667, 'b': 26.6667, 'c': 6.6667})],
  ("Average each player's marginal contribution over every ordering of the players.", "O(n! · n)", "O(n)"),
  ("The subset formula: Σ |S|!(n−|S|−1)!/n! × (v(S ∪ {i}) − v(S)).", "O(2ⁿ · n)", "O(1)"),
  viz=(GAME,))


@B
def shapley(v):
    players = sorted(max(v, key=len))
    total = {p: 0.0 for p in players}
    orders = list(permutations(players))
    for order in orders:
        team = []
        for p in order:
            before = v[tuple(sorted(team))]
            team.append(p)
            total[p] += v[tuple(sorted(team))] - before
    return {p: round(total[p] / len(orders), 4) for p in players}


@O
def shapley(v):
    players = sorted(max(v, key=len))
    n = len(players)
    out = {}
    for p in players:
        others = [q for q in players if q != p]
        phi = 0.0
        for size in range(n):
            w = math.factorial(size) * math.factorial(n - size - 1) / math.factorial(n)
            for S in combinations(others, size):
                phi += w * (v[tuple(sorted(S + (p,)))] - v[S])
        out[p] = round(phi, 4)
    return out


Q(None, "Rank Features by Permutation Importance", "Medium", "Model-agnostic importance",
  "Fit a linear regression, then rank features (most important first) by how much R² drops when that column is shuffled (5 shuffles each, seed 0).",
  [((XR, YR), [0, 1, 2])],
  ("Shuffle each column yourself with a NumPy generator and re-score.", "O(d · r · n)", "O(n)"),
  ("<code>sklearn.inspection.permutation_importance</code>.", "O(d · r · n)", "O(n)"),
  viz=(XR, YR))


@B
def perm_rank(X, y):
    X, y = np.array(X), np.array(y)
    m = LinearRegression().fit(X, y)
    base = r2_score(y, m.predict(X))
    g = np.random.default_rng(0)
    drops = []
    for j in range(X.shape[1]):
        d = 0
        for _ in range(5):
            Xp = X.copy()
            Xp[:, j] = g.permutation(Xp[:, j])
            d += base - r2_score(y, m.predict(Xp))
        drops.append(d / 5)
    return sorted(range(X.shape[1]), key=lambda j: -drops[j])


@O
def perm_rank(X, y):
    m = LinearRegression().fit(X, y)
    r = permutation_importance(m, np.array(X), np.array(y), n_repeats=5, random_state=0)
    return [int(j) for j in np.argsort(-r.importances_mean)]


XT = [[x0, x1] for x0 in [1, 2, 3, 4] for x1 in [0, 5, 10]]
YT = [x0 * 10 + (5 if x1 > 4 else 0) for x0, x1 in XT]


Q(None, "Partial Dependence", "Medium", "Average effect of one feature",
  "Fit <code>DecisionTreeRegressor(max_depth=3, random_state=0)</code>. For each unique value g of feature <code>j</code> (sorted), set that column to g for every row and average the predictions. Return the list, rounded to 3.",
  [((XT, YT, 0), [13.333, 23.333, 33.333, 43.333]), ((XT, YT, 1), [25.0, 30.0, 30.0])],
  ("Loop over grid values, overwrite the column, predict, average.", "O(g · n · depth)", "O(n)"),
  ("<code>partial_dependence(model, X, [j], kind='average')</code>, which uses the unique values as the grid when there are few.", "O(g · n · depth)", "O(n)"),
  viz=(XT, YT, 0))


@B
def pdp(X, y, j):
    X = np.array(X, float)
    m = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
    out = []
    for g in sorted(set(X[:, j])):
        Xg = X.copy()
        Xg[:, j] = g
        out.append(round(float(m.predict(Xg).mean()), 3))
    return out


@O
def pdp(X, y, j):
    X = np.array(X, float)
    m = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
    return np.round(partial_dependence(m, X, [j], kind="average")["average"][0], 3).tolist()


Q(None, "Where Tree Importances Come From", "Hard", "Impurity decrease",
  "Fit <code>DecisionTreeRegressor(max_depth=3, random_state=0)</code> and return each feature's importance, computed from the tree: total (weighted) impurity decrease from its splits, normalised to sum to 1. Round to 4.",
  [((XR, YR), [0.9534, 0.0466, 0.0]), ((XT, YT), [0.9574, 0.0426])],
  ("Walk the tree arrays: for each split add w·imp − w_left·imp_left − w_right·imp_right to its feature.", "O(nodes)", "O(d)"),
  ("<code>model.feature_importances_</code>.", "O(1)", "O(d)"),
  viz=(XT, YT))


@B
def tree_importance(X, y):
    m = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
    t = m.tree_
    imp = [0.0] * len(X[0])
    for node in range(t.node_count):
        left, right = t.children_left[node], t.children_right[node]
        if left == -1:
            continue
        w, wl, wr = t.weighted_n_node_samples[node], t.weighted_n_node_samples[left], t.weighted_n_node_samples[right]
        imp[t.feature[node]] += w * t.impurity[node] - wl * t.impurity[left] - wr * t.impurity[right]
    total = sum(imp)
    return [round(v / total, 4) for v in imp]


@O
def tree_importance(X, y):
    m = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)
    return np.round(m.feature_importances_, 4).tolist()


Q(None, "Counterfactual: What Would Change the Decision?", "Medium", "Actionable explanations",
  "A logistic model approves when w·x + b ≥ 0. For a rejected applicant, return the smallest increase of feature <code>j</code> (rounded up to 0.01) that gets approval.",
  [(([0.8, -1.5, 0.3], -4.0, [3.0, 1.0, 2.0], 0), 3.13), (([0.8, -1.5, 0.3], -4.0, [3.0, 1.0, 2.0], 2), 8.34)],
  ("Raise the feature in steps of 0.01 until the score reaches 0.", "O(Δ / 0.01)", "O(1)"),
  ("Solve w·x + b + w_j·δ = 0 for δ, then round up.", "O(d)", "O(1)"),
  viz=([0.8, -1.5, 0.3], -4.0, [3.0, 1.0, 2.0], 0))


@B
def counterfactual(w, b, x, j):
    steps = 0
    while sum(wi * xi for wi, xi in zip(w, x)) + b + w[j] * steps / 100 < -1e-9:
        steps += 1
    return steps / 100


@O
def counterfactual(w, b, x, j):
    gap = -(np.dot(w, x) + b)
    return math.ceil(round(gap / w[j] * 100, 9)) / 100


GROUP = ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"]
YTRUE = [1, 1, 0, 0, 1, 1, 1, 0, 0, 0]
YPRED = [1, 1, 1, 0, 1, 1, 0, 0, 0, 0]


Q(None, "Demographic Parity Difference", "Easy", "Equal selection rates",
  "Return <code>(selection rate per group, largest minus smallest)</code>, rounded to 4. Selection rate = share predicted positive.",
  [((GROUP, YPRED), ({'A': 0.8, 'B': 0.2}, 0.6))],
  ("Count positives and totals per group.", "O(n)", "O(g)"),
  ("<code>groupby(group).mean()</code> on the predictions.", "O(n)", "O(g)"),
  viz=(GROUP, YPRED))


@B
def parity(group, pred):
    pos, tot = {}, {}
    for g, p in zip(group, pred):
        pos[g] = pos.get(g, 0) + p
        tot[g] = tot.get(g, 0) + 1
    rates = {g: round(pos[g] / tot[g], 4) for g in sorted(tot)}
    return (rates, round(max(rates.values()) - min(rates.values()), 4))


@O
def parity(group, pred):
    r = pd.Series(pred).groupby(pd.Series(group)).mean().round(4)
    return (r.to_dict(), round(r.max() - r.min(), 4))


Q(None, "Disparate Impact and the 80% Rule", "Easy", "Ratio of selection rates",
  "Return <code>(lowest rate ÷ highest rate, passes the 80% rule)</code>, ratio rounded to 4.",
  [((GROUP, YPRED), (0.25, False)), ((GROUP, [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]), (1.0, True))],
  ("Selection rates in a loop, then divide.", "O(n)", "O(g)"),
  ("Group means with pandas.", "O(n)", "O(g)"),
  viz=(GROUP, YPRED))


@B
def disparate_impact(group, pred):
    rates = {}
    for g in set(group):
        ps = [p for gg, p in zip(group, pred) if gg == g]
        rates[g] = sum(ps) / len(ps)
    ratio = min(rates.values()) / max(rates.values())
    return (round(ratio, 4), ratio >= 0.8)


@O
def disparate_impact(group, pred):
    r = pd.Series(pred).groupby(pd.Series(group)).mean()
    ratio = r.min() / r.max()
    return (round(float(ratio), 4), bool(ratio >= 0.8))


Q(None, "Equal Opportunity", "Medium", "True positive rate by group",
  "Among people who truly qualify (y = 1), what share did the model approve in each group? Return <code>(TPR per group, gap)</code>, rounded to 4.",
  [((GROUP, YTRUE, YPRED), ({'A': 1.0, 'B': 0.5}, 0.5))],
  ("Filter to y = 1 and count per group.", "O(n)", "O(g)"),
  ("A DataFrame filter and a groupby mean.", "O(n)", "O(g)"),
  viz=(GROUP, YTRUE, YPRED))


@B
def equal_opportunity(group, y, pred):
    hit, tot = {}, {}
    for g, t, p in zip(group, y, pred):
        if t == 1:
            hit[g] = hit.get(g, 0) + p
            tot[g] = tot.get(g, 0) + 1
    tpr = {g: round(hit[g] / tot[g], 4) for g in sorted(tot)}
    return (tpr, round(max(tpr.values()) - min(tpr.values()), 4))


@O
def equal_opportunity(group, y, pred):
    df = pd.DataFrame({"g": group, "y": y, "p": pred})
    tpr = df[df.y == 1].groupby("g")["p"].mean().round(4)
    return (tpr.to_dict(), round(tpr.max() - tpr.min(), 4))


Q(None, "Equalized Odds Gap", "Medium", "TPR and FPR together",
  "Return the larger of the TPR gap and the FPR gap between groups, rounded to 4.",
  [((GROUP, YTRUE, YPRED), 0.5)],
  ("Rates for y = 1 and y = 0 per group in loops.", "O(n)", "O(g)"),
  ("One groupby over (group, y), then take max − min of each column.", "O(n)", "O(g)"),
  viz=(GROUP, YTRUE, YPRED))


@B
def equalized_odds(group, y, pred):
    gaps = []
    for label in (1, 0):
        rates = []
        for g in sorted(set(group)):
            ps = [p for gg, t, p in zip(group, y, pred) if gg == g and t == label]
            rates.append(sum(ps) / len(ps))
        gaps.append(max(rates) - min(rates))
    return round(max(gaps), 4)


@O
def equalized_odds(group, y, pred):
    t = pd.DataFrame({"g": group, "y": y, "p": pred}).groupby(["y", "g"])["p"].mean().unstack()
    return round(float((t.max(axis=1) - t.min(axis=1)).max()), 4)


PROBS = [0.05, 0.15, 0.3, 0.35, 0.55, 0.62, 0.71, 0.78, 0.85, 0.93]
YCAL = [0, 0, 0, 1, 0, 1, 1, 1, 1, 1]


Q(None, "Reliability Curve", "Medium", "Calibration",
  "Split [0, 1] into <code>n_bins</code> equal bins. For each non-empty bin return <code>(mean predicted probability, observed positive rate)</code>, rounded to 4.",
  [((YCAL, PROBS, 5), [(0.1, 0.0), (0.325, 0.5), (0.55, 0.0), (0.7033, 1.0), (0.89, 1.0)])],
  ("Put each probability in bin ⌊p × n_bins⌋ and average.", "O(n)", "O(bins)"),
  ("<code>calibration_curve(y, p, n_bins)</code> returns both lists.", "O(n)", "O(bins)"),
  viz=(YCAL, PROBS, 5))


@B
def reliability(y, p, n_bins):
    sums = {}
    for t, q in zip(y, p):
        b = min(int(q * n_bins), n_bins - 1)
        s = sums.setdefault(b, [0, 0, 0])
        s[0] += q
        s[1] += t
        s[2] += 1
    return [(round(s[0] / s[2], 4), round(s[1] / s[2], 4)) for b, s in sorted(sums.items())]


@O
def reliability(y, p, n_bins):
    frac_pos, mean_pred = calibration_curve(y, p, n_bins=n_bins)
    return [(round(float(a), 4), round(float(b), 4)) for a, b in zip(mean_pred, frac_pos)]


Q(None, "Brier Score", "Easy", "Probability accuracy",
  "Return the mean squared difference between predicted probabilities and outcomes, rounded to 4.",
  [((YCAL, PROBS), 0.1144)],
  ("Loop and average (p − y)².", "O(n)", "O(1)"),
  ("<code>brier_score_loss</code>.", "O(n)", "O(1)"),
  viz=(YCAL, PROBS))


@B
def brier(y, p):
    return round(sum((q - t) ** 2 for t, q in zip(y, p)) / len(y), 4)


@O
def brier(y, p):
    return round(float(brier_score_loss(y, p)), 4)


Q(None, "Expected Calibration Error", "Medium", "One number for calibration",
  "ECE = Σ over non-empty bins of (bin size ÷ n) × |mean predicted − observed rate|, with <code>n_bins</code> equal bins. Round to 4.",
  [((YCAL, PROBS, 5), 0.221)],
  ("Accumulate per-bin sums in a dict.", "O(n)", "O(bins)"),
  ("<code>np.digitize</code> for bins and <code>np.bincount</code> for the sums.", "O(n)", "O(bins)"),
  viz=(YCAL, PROBS, 5))


@B
def ece(y, p, n_bins):
    bins = {}
    for t, q in zip(y, p):
        b = min(int(q * n_bins), n_bins - 1)
        bins.setdefault(b, []).append((q, t))
    total = 0
    for items in bins.values():
        conf = sum(q for q, _ in items) / len(items)
        acc = sum(t for _, t in items) / len(items)
        total += len(items) / len(y) * abs(conf - acc)
    return round(total, 4)


@O
def ece(y, p, n_bins):
    y, p = np.array(y), np.array(p)
    b = np.minimum((p * n_bins).astype(int), n_bins - 1)
    cnt = np.bincount(b, minlength=n_bins)
    conf = np.bincount(b, weights=p, minlength=n_bins)
    acc = np.bincount(b, weights=y, minlength=n_bins)
    keep = cnt > 0
    return round(float(np.abs(conf[keep] - acc[keep]).sum() / len(y)), 4)


Q(None, "Balanced Class Weights", "Easy", "Imbalanced data",
  "Return the 'balanced' weight for each class (sorted): n_samples ÷ (n_classes × class count), rounded to 4.",
  [(([0] * 90 + [1] * 10,), {0: 0.5556, 1: 5.0}), ((["a", "a", "b", "c", "c", "c"],), {'a': 1.0, 'b': 2.0, 'c': 0.6667})],
  ("Count classes and apply the formula.", "O(n)", "O(k)"),
  ("<code>compute_class_weight('balanced', ...)</code> — the same weights <code>class_weight='balanced'</code> uses.", "O(n)", "O(k)"),
  viz=([0] * 90 + [1] * 10,))


@B
def class_weights(y):
    counts = {}
    for c in y:
        counts[c] = counts.get(c, 0) + 1
    return {c: round(len(y) / (len(counts) * counts[c]), 4) for c in sorted(counts)}


@O
def class_weights(y):
    classes = np.unique(y)
    w = compute_class_weight("balanced", classes=classes, y=np.array(y))
    return {c: round(float(v), 4) for c, v in zip(classes.tolist(), w)}


Q(None, "Threshold That Maximises F1", "Medium", "Don't default to 0.5",
  "Among the predicted probabilities used as thresholds (predict positive if p ≥ t), return <code>(best threshold, its F1)</code>, F1 rounded to 4 (lowest threshold on ties).",
  [((YCAL, PROBS), (0.35, 0.9231)), (([0, 0, 0, 0, 0, 0, 0, 1, 0, 1], PROBS), (0.78, 0.8))],
  ("Try every threshold and compute precision, recall and F1.", "O(n²)", "O(1)"),
  ("<code>precision_recall_curve</code> gives every threshold's precision and recall at once.", "O(n log n)", "O(n)"),
  viz=(YCAL, PROBS))


@B
def best_f1(y, p):
    best = None
    for t in sorted(set(p)):
        tp = sum(1 for a, q in zip(y, p) if q >= t and a == 1)
        fp = sum(1 for a, q in zip(y, p) if q >= t and a == 0)
        fn = sum(1 for a, q in zip(y, p) if q < t and a == 1)
        f1 = 2 * tp / (2 * tp + fp + fn) if tp else 0
        if best is None or f1 > best[1] + 1e-12:
            best = (t, f1)
    return (best[0], round(best[1], 4))


@O
def best_f1(y, p):
    prec, rec, thr = precision_recall_curve(y, p)
    f1 = np.where(prec + rec > 0, 2 * prec * rec / np.maximum(prec + rec, 1e-12), 0)[:-1]
    i = max(range(len(thr)), key=lambda k: (round(f1[k], 12), -thr[k]))
    return (float(thr[i]), round(float(f1[i]), 4))


Q(None, "Cost-Sensitive Threshold", "Medium", "Errors have different prices",
  "A missed fraud costs <code>c_fn</code>, a false alarm costs <code>c_fp</code>. Among thresholds 0.05, 0.10, …, 0.95 return <code>(best threshold, total cost)</code> (lowest threshold on ties).",
  [((YCAL, PROBS, 1, 10), (0.35, 1)), ((YCAL, PROBS, 5, 1), (0.6, 1))],
  ("Loop over thresholds and rows counting the two error types.", "O(tn)", "O(1)"),
  ("Broadcast thresholds against probabilities to get every cost at once.", "O(tn)", "O(tn)"),
  viz=(YCAL, PROBS, 1, 10))


@B
def cost_threshold(y, p, c_fp, c_fn):
    best = None
    for k in range(1, 20):
        t = round(k * 0.05, 2)
        cost = 0
        for a, q in zip(y, p):
            if q >= t and a == 0:
                cost += c_fp
            elif q < t and a == 1:
                cost += c_fn
        if best is None or cost < best[1]:
            best = (t, cost)
    return best


@O
def cost_threshold(y, p, c_fp, c_fn):
    t = np.round(np.arange(1, 20) * 0.05, 2)
    y, p = np.array(y), np.array(p)
    pred = p[None, :] >= t[:, None]
    cost = c_fp * (pred & (y == 0)).sum(axis=1) + c_fn * (~pred & (y == 1)).sum(axis=1)
    i = int(cost.argmin())
    return (float(t[i]), int(cost[i]))


Q(None, "Accuracy vs Balanced Accuracy", "Easy", "The imbalance trap",
  "Return <code>(accuracy, balanced accuracy)</code> rounded to 4. Balanced accuracy averages the recall of each class.",
  [(([0] * 95 + [1] * 5, [0] * 100), (0.95, 0.5)), (([0, 0, 0, 1, 1], [0, 0, 1, 1, 0]), (0.6, 0.5833))],
  ("Per-class recall in loops.", "O(n)", "O(k)"),
  ("<code>balanced_accuracy_score</code>.", "O(n)", "O(k)"),
  viz=([0] * 95 + [1] * 5, [0] * 100))


@B
def balanced(y, pred):
    acc = sum(a == b for a, b in zip(y, pred)) / len(y)
    recalls = []
    for c in sorted(set(y)):
        idx = [i for i, a in enumerate(y) if a == c]
        recalls.append(sum(pred[i] == c for i in idx) / len(idx))
    return (round(acc, 4), round(sum(recalls) / len(recalls), 4))


@O
def balanced(y, pred):
    return (round(float(np.mean(np.array(y) == np.array(pred))), 4), round(float(balanced_accuracy_score(y, pred)), 4))


Q(None, "Mask Personal Data", "Medium", "Privacy before training",
  "Replace email addresses with <code>[EMAIL]</code> and 10-digit phone numbers (optionally starting +91) with <code>[PHONE]</code>.",
  [(("Call 9876543210 or mail asha.k@mail.com",), 'Call [PHONE] or mail [EMAIL]'), (("+91 9123456789, ravi@x.in, order 12345",), '[PHONE], [EMAIL], order 12345')],
  ("Scan word by word: '@' with a '.' after it is an email; strip punctuation and check for 10 digits.", "O(n)", "O(n)"),
  ("Two regular expressions with <code>re.sub</code>.", "O(n)", "O(n)"),
  viz=("Call 9876543210 or mail asha.k@mail.com",))


@B
def mask_pii(text):
    words = text.split(" ")
    out = []
    skip = False
    for i, w in enumerate(words):
        if skip:
            skip = False
            continue
        core = w.rstrip(",.")
        tail = w[len(core):]
        if "@" in core and "." in core.split("@")[-1]:
            out.append("[EMAIL]" + tail)
        elif core == "+91" and i + 1 < len(words) and words[i + 1].rstrip(",.").isdigit() and len(words[i + 1].rstrip(",.")) == 10:
            nxt = words[i + 1]
            out.append("[PHONE]" + nxt[len(nxt.rstrip(",.")):])
            skip = True
        elif core.isdigit() and len(core) == 10:
            out.append("[PHONE]" + tail)
        else:
            out.append(w)
    return " ".join(out)


@O
def mask_pii(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL]", text)
    return re.sub(r"(\+91\s?)?\b\d{10}\b", "[PHONE]", text)


PEOPLE = [("411001", 34, "F"), ("411001", 35, "F"), ("411002", 34, "M"), ("411001", 36, "F"), ("411002", 31, "M")]


Q(None, "k-Anonymity", "Medium", "Re-identification risk",
  "Generalise age to its decade (34 → '30s') and return the size of the smallest group of identical (pincode, decade, gender) rows — the dataset's k.",
  [((PEOPLE,), 2), ((PEOPLE + [("411003", 52, "F")],), 1)],
  ("Build keys and count in a dict.", "O(n)", "O(n)"),
  ("<code>groupby([...]).size().min()</code>.", "O(n)", "O(n)"),
  viz=(PEOPLE,))


@B
def k_anonymity(rows):
    counts = {}
    for pin, age, sex in rows:
        key = (pin, str(age // 10 * 10) + "s", sex)
        counts[key] = counts.get(key, 0) + 1
    return min(counts.values())


@O
def k_anonymity(rows):
    df = pd.DataFrame(rows, columns=["pin", "age", "sex"])
    df["decade"] = (df["age"] // 10 * 10).astype(str) + "s"
    return int(df.groupby(["pin", "decade", "sex"]).size().min())


Q(None, "Find Proxy Features", "Medium", "Bias sneaks back in",
  "Dropping a sensitive column isn't enough if other columns predict it. Return features whose |correlation| with the sensitive column is above <code>limit</code>, sorted.",
  [(({"pincode_income": [9, 8, 9, 3, 2, 3], "years_exp": [5, 2, 7, 4, 6, 3], "gym_member": [1, 1, 1, 0, 0, 1]}, [1, 1, 1, 0, 0, 0], 0.7), ['gym_member', 'pincode_income'])],
  ("Pearson r for each column by formula.", "O(dn)", "O(1)"),
  ("<code>DataFrame.corrwith</code>.", "O(dn)", "O(d)"),
  viz=({"pincode_income": [9, 8, 9, 3, 2, 3], "years_exp": [5, 2, 7, 4, 6, 3], "gym_member": [1, 1, 1, 0, 0, 1]}, [1, 1, 1, 0, 0, 0], 0.7))


@B
def proxies(features, sensitive, limit):
    out = []
    s = sensitive
    ms = sum(s) / len(s)
    for name, x in features.items():
        mx = sum(x) / len(x)
        sxy = sum((a - mx) * (b - ms) for a, b in zip(x, s))
        r = sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - ms) ** 2 for b in s))
        if abs(r) > limit:
            out.append(name)
    return sorted(out)


@O
def proxies(features, sensitive, limit):
    r = pd.DataFrame(features).corrwith(pd.Series(sensitive))
    return sorted(r[r.abs() > limit].index)
