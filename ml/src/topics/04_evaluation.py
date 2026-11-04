from lib import *
import math
import numpy as np
from sklearn.metrics import (confusion_matrix, precision_score, recall_score, f1_score, balanced_accuracy_score,
                             roc_curve, roc_auc_score, average_precision_score, matthews_corrcoef, cohen_kappa_score,
                             brier_score_loss, precision_recall_curve, precision_recall_fscore_support, top_k_accuracy_score, mean_squared_error)
from sklearn.model_selection import cross_val_score, KFold, LeaveOneOut, TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor


TOPIC(
    id="evaluation", title="Model Evaluation & Validation", glyph="✓ ✗",
    blurb="Measuring a model honestly: the confusion matrix, precision, recall, F1, ROC and PR curves, MCC and kappa, choosing thresholds, and cross-validation strategies.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">confusion_matrix(y, y_pred)            # [[TN, FP], [FN, TP]] for labels 0, 1
precision_score, recall_score, f1_score(y, y_pred, average="binary" | "macro" | "weighted")
roc_auc_score(y, scores), average_precision_score(y, scores)
roc_curve(y, scores), precision_recall_curve(y, scores)
cross_val_score(model, X, y, cv=5, scoring="f1")
KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit, LeaveOneOut</code></pre>
<table><tr><th></th><th>Predicted 0</th><th>Predicted 1</th></tr>
<tr><th>Actual 0</th><td>TN</td><td>FP (false alarm)</td></tr>
<tr><th>Actual 1</th><td>FN (miss)</td><td>TP</td></tr></table>
""")

Y = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
P = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0]
S = [0.9, 0.1, 0.4, 0.8, 0.3, 0.7, 0.6, 0.2, 0.65, 0.35]


def counts(y, p):
    tp = sum(1 for a, b in zip(y, p) if a == 1 and b == 1)
    fp = sum(1 for a, b in zip(y, p) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y, p) if a == 1 and b == 0)
    tn = sum(1 for a, b in zip(y, p) if a == 0 and b == 0)
    return tp, fp, fn, tn


Q(None, "Confusion Matrix", "Easy", "Where the mistakes are",
  "Return [[TN, FP], [FN, TP]] for binary labels 0/1.",
  [((Y, P), [[4, 1], [1, 4]]), (([0, 0, 1, 1], [1, 1, 1, 1]), [[0, 2], [0, 2]])],
  ("Count the four combinations of (actual, predicted).", "O(n)", "O(1)"),
  ("<code>confusion_matrix(y, y_pred)</code>.", "O(n)", "O(k²)"),
  names=["y", "y_pred"])


@B
def confusion(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    return [[tn, fp], [fn, tp]]


@O
def confusion(y, y_pred):
    return confusion_matrix(y, y_pred, labels=[0, 1])


Q(None, "Precision", "Easy", "Of the predicted positives, how many are right?",
  "Return TP / (TP + FP), rounded to 4 decimals.",
  [((Y, P), 0.8), (([1, 0, 0, 0], [1, 1, 1, 0]), 0.3333)],
  ("Count TP and FP.", "O(n)", "O(1)"),
  ("<code>precision_score</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def precision(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    return round(tp / (tp + fp), 4)


@O
def precision(y, y_pred):
    return round(precision_score(y, y_pred), 4)


Q(None, "Recall", "Easy", "Of the real positives, how many did we catch?",
  "Return TP / (TP + FN), rounded to 4 decimals.",
  [((Y, P), 0.8), (([1, 1, 1, 0], [1, 0, 0, 0]), 0.3333)],
  ("Count TP and FN.", "O(n)", "O(1)"),
  ("<code>recall_score</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def recall(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    return round(tp / (tp + fn), 4)


@O
def recall(y, y_pred):
    return round(recall_score(y, y_pred), 4)


Q(None, "F1 Score", "Easy", "Harmonic mean of precision and recall",
  "Return 2PR/(P + R), rounded to 4 decimals.",
  [((Y, P), 0.8), (([1, 1, 0, 0], [1, 0, 1, 0]), 0.5)],
  ("Precision and recall by hand, then the harmonic mean (= 2TP / (2TP + FP + FN)).", "O(n)", "O(1)"),
  ("<code>f1_score</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def f1(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    return round(2 * tp / (2 * tp + fp + fn), 4)


@O
def f1(y, y_pred):
    return round(f1_score(y, y_pred), 4)


Q(None, "Specificity", "Easy", "True negative rate",
  "Return TN / (TN + FP), rounded to 4 decimals.",
  [((Y, P), 0.8)],
  ("Count TN and FP.", "O(n)", "O(1)"),
  ("Recall of the negative class: <code>recall_score(y, y_pred, pos_label=0)</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def specificity(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    return round(tn / (tn + fp), 4)


@O
def specificity(y, y_pred):
    return round(recall_score(y, y_pred, pos_label=0), 4)


Q(None, "Macro vs Weighted F1", "Medium", "Averaging over classes",
  "For multiclass labels return (macro F1, weighted F1), rounded to 4 decimals.",
  [((["a", "a", "a", "a", "b", "b", "c"], ["a", "a", "a", "b", "b", "c", "c"]), (0.6746, 0.7279))],
  ("F1 per class (one-vs-rest counts), then a plain average and a support-weighted average.", "O(n·k)", "O(k)"),
  ("<code>f1_score(average='macro')</code> and <code>average='weighted'</code>.", "O(n·k)", "O(k)"),
  names=["y", "y_pred"])


@B
def macro_weighted_f1(y, y_pred):
    classes = sorted(set(y) | set(y_pred))
    scores, supports = [], []
    for c in classes:
        tp = sum(1 for a, b in zip(y, y_pred) if a == c and b == c)
        fp = sum(1 for a, b in zip(y, y_pred) if a != c and b == c)
        fn = sum(1 for a, b in zip(y, y_pred) if a == c and b != c)
        scores.append(2 * tp / (2 * tp + fp + fn) if tp + fp + fn else 0.0)
        supports.append(sum(1 for a in y if a == c))
    macro = sum(scores) / len(scores)
    weighted = sum(s * n for s, n in zip(scores, supports)) / sum(supports)
    return (round(macro, 4), round(weighted, 4))


@O
def macro_weighted_f1(y, y_pred):
    return (round(f1_score(y, y_pred, average="macro"), 4), round(f1_score(y, y_pred, average="weighted"), 4))


Q(None, "Per-Class Precision and Recall", "Medium", "The classification report",
  "For each class (sorted), return (precision list, recall list), rounded to 4 decimals.",
  [((["a", "a", "a", "a", "b", "b", "c"], ["a", "a", "a", "b", "b", "c", "c"]), ([1.0, 0.5, 0.5], [0.75, 0.5, 1.0]))],
  ("For each class, count one-vs-rest TP, FP and FN.", "O(n·k)", "O(k)"),
  ("<code>precision_recall_fscore_support(y, y_pred)</code> (what <code>classification_report</code> prints).", "O(n·k)", "O(k)"),
  names=["y", "y_pred"])


@B
def per_class(y, y_pred):
    precisions, recalls = [], []
    for c in sorted(set(y) | set(y_pred)):
        tp = sum(1 for a, b in zip(y, y_pred) if a == c and b == c)
        predicted = sum(1 for b in y_pred if b == c)
        actual = sum(1 for a in y if a == c)
        precisions.append(round(tp / predicted, 4) if predicted else 0.0)
        recalls.append(round(tp / actual, 4) if actual else 0.0)
    return (precisions, recalls)


@O
def per_class(y, y_pred):
    p, r, _, _ = precision_recall_fscore_support(y, y_pred, zero_division=0)
    return (p.round(4), r.round(4))


Q(None, "Balanced Accuracy", "Easy", "Average recall over classes",
  "Return the mean of each class's recall, rounded to 4 decimals — fair on imbalanced data.",
  [(([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]), 0.75)],
  ("Recall of each class by counting, then average.", "O(n·k)", "O(k)"),
  ("<code>balanced_accuracy_score</code>.", "O(n)", "O(k)"),
  names=["y", "y_pred"])


@B
def balanced_accuracy(y, y_pred):
    recalls = []
    for c in sorted(set(y)):
        total = sum(1 for a in y if a == c)
        hit = sum(1 for a, b in zip(y, y_pred) if a == c and b == c)
        recalls.append(hit / total)
    return round(sum(recalls) / len(recalls), 4)


@O
def balanced_accuracy(y, y_pred):
    return round(balanced_accuracy_score(y, y_pred), 4)


Q(None, "ROC Curve Points", "Medium", "Every threshold at once",
  "Using each distinct score as a threshold (highest first, predict 1 when score ≥ threshold), return (FPR list, TPR list), starting from (0, 0). Round to 4 decimals.",
  [((Y, S), ([0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.6, 0.8, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0]))],
  ("Sort thresholds descending; at each, count TP and FP to get TPR and FPR.", "O(n²)", "O(n)"),
  ("<code>roc_curve(y, scores, drop_intermediate=False)</code>.", "O(n log n)", "O(n)"),
  names=["y", "scores"])


@B
def roc_points(y, scores):
    pos = sum(y)
    neg = len(y) - pos
    fpr, tpr = [0.0], [0.0]
    for t in sorted(set(scores), reverse=True):
        tp = sum(1 for a, s in zip(y, scores) if s >= t and a == 1)
        fp = sum(1 for a, s in zip(y, scores) if s >= t and a == 0)
        fpr.append(round(fp / neg, 4))
        tpr.append(round(tp / pos, 4))
    return (fpr, tpr)


@O
def roc_points(y, scores):
    fpr, tpr, _ = roc_curve(y, scores, drop_intermediate=False)
    return (fpr.round(4), tpr.round(4))


Q(None, "ROC AUC", "Medium", "How well scores rank positives above negatives",
  "Return the area under the ROC curve, rounded to 4 decimals.",
  [((Y, S), 0.96), (([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.75)],
  ("AUC = probability a random positive scores higher than a random negative: compare every pair (ties count ½).", "O(n²)", "O(1)"),
  ("<code>roc_auc_score</code>.", "O(n log n)", "O(n)"),
  names=["y", "scores"])


@B
def auc(y, scores):
    pos = [s for a, s in zip(y, scores) if a == 1]
    neg = [s for a, s in zip(y, scores) if a == 0]
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += 1 if p > n else 0.5 if p == n else 0
    return round(wins / (len(pos) * len(neg)), 4)


@O
def auc(y, scores):
    return round(roc_auc_score(y, scores), 4)


Q(None, "Average Precision (PR AUC)", "Hard", "Area under precision–recall",
  "Return Σ (Rₙ − Rₙ₋₁)·Pₙ over thresholds from high to low, rounded to 4 decimals.",
  [((Y, S), 0.9667), (([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]), 0.8333)],
  ("Walk down the sorted scores, updating precision and recall at each threshold; add recall gain × precision.", "O(n²)", "O(n)"),
  ("<code>average_precision_score</code>.", "O(n log n)", "O(n)"),
  names=["y", "scores"])


@B
def average_precision(y, scores):
    pos = sum(y)
    ap, prev_recall = 0.0, 0.0
    for t in sorted(set(scores), reverse=True):
        tp = sum(1 for a, s in zip(y, scores) if s >= t and a == 1)
        fp = sum(1 for a, s in zip(y, scores) if s >= t and a == 0)
        rec = tp / pos
        ap += (rec - prev_recall) * tp / (tp + fp)
        prev_recall = rec
    return round(ap, 4)


@O
def average_precision(y, scores):
    return round(average_precision_score(y, scores), 4)


Q(None, "Matthews Correlation Coefficient", "Medium", "One balanced number",
  "Return MCC = (TP·TN − FP·FN) / √((TP+FP)(TP+FN)(TN+FP)(TN+FN)), rounded to 4 decimals.",
  [((Y, P), 0.6), (([1, 1, 1, 1, 0], [1, 1, 1, 1, 1]), 0.0)],
  ("Confusion counts, then the formula (0 if the denominator is 0).", "O(n)", "O(1)"),
  ("<code>matthews_corrcoef</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def mcc(y, y_pred):
    tp, fp, fn, tn = counts(y, y_pred)
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return round((tp * tn - fp * fn) / den, 4) if den else 0.0


@O
def mcc(y, y_pred):
    return round(matthews_corrcoef(y, y_pred), 4)


Q(None, "Cohen's Kappa", "Medium", "Agreement beyond chance",
  "Return κ = (p_o − p_e)/(1 − p_e) between two label lists, rounded to 4 decimals.",
  [((Y, P), 0.6), ((["yes", "yes", "no", "no", "yes"], ["yes", "no", "no", "no", "yes"]), 0.6154)],
  ("Observed agreement, and chance agreement from each rater's class shares.", "O(n·k)", "O(k)"),
  ("<code>cohen_kappa_score</code>.", "O(n)", "O(k)"),
  names=["a", "b"])


@B
def kappa(a, b):
    n = len(a)
    p_o = sum(1 for x, y in zip(a, b) if x == y) / n
    p_e = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return round((p_o - p_e) / (1 - p_e), 4)


@O
def kappa(a, b):
    return round(cohen_kappa_score(a, b), 4)


Q(None, "Brier Score", "Easy", "Squared error of probabilities",
  "Return the mean of (p − y)², rounded to 4 decimals. Lower = better calibrated.",
  [((Y, S), 0.1245)],
  ("Loop of squared differences.", "O(n)", "O(1)"),
  ("<code>brier_score_loss</code>.", "O(n)", "O(1)"),
  names=["y", "probs"])


@B
def brier(y, probs):
    return round(sum((p - a) ** 2 for a, p in zip(y, probs)) / len(y), 4)


@O
def brier(y, probs):
    return round(brier_score_loss(y, probs), 4)


Q(None, "Best Threshold for F1", "Hard", "Tuning the cut-off",
  "Try every distinct score as the threshold (predict 1 when score ≥ t) and return (best t, its F1), rounded to 4 decimals.",
  [((Y, S), (0.4, 0.9091))],
  ("Loop over thresholds, compute F1 each time, keep the best.", "O(n²)", "O(1)"),
  ("<code>precision_recall_curve</code> gives precision and recall at every threshold; compute F1 for all at once.", "O(n log n)", "O(n)"),
  names=["y", "scores"])


@B
def best_threshold(y, scores):
    best = (None, -1)
    for t in sorted(set(scores)):
        tp = sum(1 for a, s in zip(y, scores) if s >= t and a == 1)
        fp = sum(1 for a, s in zip(y, scores) if s >= t and a == 0)
        fn = sum(1 for a, s in zip(y, scores) if s < t and a == 1)
        f = 2 * tp / (2 * tp + fp + fn)
        if f > best[1]:
            best = (t, f)
    return (round(best[0], 4), round(best[1], 4))


@O
def best_threshold(y, scores):
    prec, rec, thr = precision_recall_curve(y, scores)
    f1s = 2 * prec[:-1] * rec[:-1] / np.maximum(prec[:-1] + rec[:-1], 1e-12)
    i = int(np.argmax(f1s))
    return (round(thr[i], 4), round(f1s[i], 4))


Q(None, "Top-k Accuracy", "Easy", "Right answer among the top guesses",
  "Each row of scores ranks the classes 0, 1, 2…. Return the share of rows whose true class is among the k highest scores, rounded to 4 decimals.",
  [(([0, 1, 2, 2], [[0.5, 0.3, 0.2], [0.4, 0.35, 0.25], [0.2, 0.5, 0.3], [0.6, 0.3, 0.1]], 2), 0.75)],
  ("Sort each row's classes by score and check the first k.", "O(n·k log k)", "O(k)"),
  ("<code>top_k_accuracy_score(y, scores, k=k)</code>.", "O(n·k)", "O(n)"),
  names=["y", "scores", "k"])


@B
def top_k(y, scores, k):
    hits = 0
    for label, row in zip(y, scores):
        ranked = sorted(range(len(row)), key=lambda c: -row[c])
        if label in ranked[:k]:
            hits += 1
    return round(hits / len(y), 4)


@O
def top_k(y, scores, k):
    return round(top_k_accuracy_score(y, scores, k=k, labels=list(range(len(scores[0])))), 4)


Q(None, "Cost of Mistakes", "Easy", "Business-aware evaluation",
  "A false positive costs fp_cost and a false negative fn_cost. Return the total cost of the predictions.",
  [((Y, P, 1, 10), 11), ((Y, [1] * 10, 1, 10), 5)],
  ("Count FP and FN by hand.", "O(n)", "O(1)"),
  ("<code>confusion_matrix(...).ravel()</code> gives TN, FP, FN, TP.", "O(n)", "O(1)"),
  names=["y", "y_pred", "fp_cost", "fn_cost"])


@B
def total_cost(y, y_pred, fp_cost, fn_cost):
    tp, fp, fn, tn = counts(y, y_pred)
    return fp * fp_cost + fn * fn_cost


@O
def total_cost(y, y_pred, fp_cost, fn_cost):
    tn, fp, fn, tp = confusion_matrix(y, y_pred, labels=[0, 1]).ravel()
    return int(fp * fp_cost + fn * fn_cost)


Q(None, "Cross-Validated R²", "Medium", "Score on every fold",
  "Run 3-fold cross-validation (in order, no shuffling) of a straight-line fit and return the R² of each fold, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5, 6, 7, 8, 9], [2.1, 3.9, 6.2, 7.8, 10.1, 12.2, 13.8, 16.1, 18.0]), [0.9875, 0.9901, 0.9854])],
  ("For each fold: fit slope/intercept on the other rows, predict the fold, compute R².", "O(k·n)", "O(n)"),
  ("<code>cross_val_score(LinearRegression(), X, y, cv=KFold(3))</code>.", "O(k·n)", "O(n)"),
  names=["x", "y"])


@B
def cv_r2(x, y):
    n, k = len(x), 3
    scores = []
    for f in range(k):
        test = list(range(f * n // k, (f + 1) * n // k))
        train = [i for i in range(n) if i not in test]
        tx, ty = [x[i] for i in train], [y[i] for i in train]
        mx, my = sum(tx) / len(tx), sum(ty) / len(ty)
        slope = sum((a - mx) * (b - my) for a, b in zip(tx, ty)) / sum((a - mx) ** 2 for a in tx)
        pred = [my + slope * (x[i] - mx) for i in test]
        actual = [y[i] for i in test]
        mean = sum(actual) / len(actual)
        r2 = 1 - sum((a - p) ** 2 for a, p in zip(actual, pred)) / sum((a - mean) ** 2 for a in actual)
        scores.append(round(r2, 4))
    return scores


@O
def cv_r2(x, y):
    return cross_val_score(LinearRegression(), np.array(x).reshape(-1, 1), y, cv=KFold(3)).round(4)


Q(None, "Leave-One-Out Error", "Medium", "n folds of size 1",
  "Leave each point out in turn, predict it with the mean of the others, and return the average squared error, rounded to 4 decimals.",
  [(([3, 5, 7, 9],), 8.8889)],
  ("Loop over points: mean of the rest, squared error.", "O(n²)", "O(1)"),
  ("<code>cross_val_score(DummyRegressor(), X, y, cv=LeaveOneOut(), scoring='neg_mean_squared_error')</code>.", "O(n²)", "O(n)"))


@B
def loo_error(y):
    total = 0
    for i in range(len(y)):
        rest = y[:i] + y[i + 1:]
        guess = sum(rest) / len(rest)
        total += (y[i] - guess) ** 2
    return round(total / len(y), 4)


@O
def loo_error(y):
    X = np.zeros((len(y), 1))
    scores = cross_val_score(DummyRegressor(), X, y, cv=LeaveOneOut(), scoring="neg_mean_squared_error")
    return round(-scores.mean(), 4)


Q(None, "Time-Series Splits", "Medium", "Never train on the future",
  "Return the test indices of each split of TimeSeriesSplit(n_splits) on n time-ordered rows: each test block has n // (n_splits + 1) rows and comes after its training rows.",
  [((10, 3), [[4, 5], [6, 7], [8, 9]]), ((12, 2), [[4, 5, 6, 7], [8, 9, 10, 11]])],
  ("Test size = n // (splits + 1); the last split ends at n; walk backwards.", "O(n)", "O(n)"),
  ("<code>TimeSeriesSplit(n_splits)</code>.", "O(n)", "O(n)"),
  names=["n", "n_splits"])


@B
def ts_splits(n, n_splits):
    size = n // (n_splits + 1)
    out = []
    for i in range(n_splits):
        end = n - (n_splits - 1 - i) * size
        out.append(list(range(end - size, end)))
    return out


@O
def ts_splits(n, n_splits):
    return [test.tolist() for _, test in TimeSeriesSplit(n_splits=n_splits).split(np.zeros((n, 1)))]
