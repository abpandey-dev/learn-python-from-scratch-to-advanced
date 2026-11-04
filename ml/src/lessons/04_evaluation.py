from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve
from sklearn.model_selection import KFold

Y = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
S = np.array([0.9, 0.1, 0.4, 0.8, 0.3, 0.7, 0.6, 0.2, 0.65, 0.35])

LESSON("Basics", "The confusion matrix", """
<p>Accuracy hides <i>which</i> mistakes a model makes. The <b>confusion matrix</b> counts all four outcomes:</p>
<table><tr><th></th><th>Predicted no</th><th>Predicted yes</th></tr>
<tr><th>Actually no</th><td><b>TN</b> true negative</td><td><b>FP</b> false positive (false alarm)</td></tr>
<tr><th>Actually yes</th><td><b>FN</b> false negative (missed!)</td><td><b>TP</b> true positive</td></tr></table>
<p>Which mistake is worse depends on the problem. Missing a cancer (FN) is far worse than an extra test (FP). Flagging a good email as spam (FP) is worse than letting one spam through.</p>
""", practice=["Confusion Matrix", "Cost of Mistakes"])


@LD
def confusion_demo():
    y_pred = (S >= 0.5).astype(int)
    cm = confusion_matrix(Y, y_pred)
    fig, ax = plt.subplots(figsize=(3.4, 3))
    ax.imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, ["TN", "FP", "FN", "TP"][2 * i + j] + f"\n{cm[i, j]}", ha="center", va="center")
    ax.set_xticks([0, 1], ["pred 0", "pred 1"])
    ax.set_yticks([0, 1], ["actual 0", "actual 1"])


LESSON("Core", "Precision, recall and F1", """
<table><tr><th>Metric</th><th>Formula</th><th>Question it answers</th></tr>
<tr><td><b>Precision</b></td><td>TP / (TP + FP)</td><td>When the model says yes, how often is it right?</td></tr>
<tr><td><b>Recall</b> (sensitivity)</td><td>TP / (TP + FN)</td><td>Of all real yeses, how many did it find?</td></tr>
<tr><td>Specificity</td><td>TN / (TN + FP)</td><td>Of all real nos, how many did it clear?</td></tr>
<tr><td><b>F1</b></td><td>2PR / (P + R)</td><td>one number balancing both</td></tr>
<tr><td>Balanced accuracy</td><td>mean recall per class</td><td>fair accuracy for imbalanced data</td></tr>
<tr><td>MCC</td><td>correlation of predictions with truth</td><td>robust single score, −1 … 1</td></tr></table>
<p>For many classes, compute per-class scores and average them: <b>macro</b> (each class equal) or <b>weighted</b> (by class size).</p>
""", practice=["Precision", "Recall", "F1 Score", "Specificity", "Balanced Accuracy", "Macro vs Weighted F1", "Per-Class Precision and Recall", "Matthews Correlation Coefficient", "Cohen's Kappa"])


@LD
def tradeoff_demo():
    thresholds = np.linspace(0.05, 0.95, 50)
    precision, recall = [], []
    for t in thresholds:
        pred = S >= t
        tp = (pred & (Y == 1)).sum()
        precision.append(tp / max(pred.sum(), 1))
        recall.append(tp / (Y == 1).sum())
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(thresholds, precision, label="precision")
    ax.plot(thresholds, recall, label="recall")
    ax.set_xlabel("threshold")
    ax.legend(fontsize=8)
    ax.set_title("Raising the threshold: precision ↑, recall ↓", fontsize=8)


LESSON("Core", "ROC and precision–recall curves", """
<p>A model outputs scores; the threshold turns them into decisions. Instead of judging one threshold, curves judge them all:</p>
<ul>
<li><b>ROC curve</b>: true positive rate vs false positive rate. <b>ROC AUC</b> = chance a random positive is scored above a random negative (0.5 = coin flip, 1 = perfect).</li>
<li><b>Precision–recall curve</b> and its area, <b>average precision</b>: better than ROC when positives are rare (fraud, disease), because it ignores the huge pile of easy negatives.</li>
</ul>
<p>Pick the final threshold from the curve based on what mistakes cost, e.g. the one maximising F1 or meeting "recall ≥ 95%". <b>Brier score</b> and log-loss check whether the probabilities themselves are trustworthy (calibration).</p>
""", practice=["ROC Curve Points", "ROC AUC", "Average Precision (PR AUC)", "Best Threshold for F1", "Brier Score", "Top-k Accuracy"])


@LD
def roc_pr_curves():
    fpr, tpr, _ = roc_curve(Y, S)
    prec, rec, _ = precision_recall_curve(Y, S)
    auc = roc_auc_score(Y, S)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3))
    left.plot(fpr, tpr, marker="o", markersize=3)
    left.plot([0, 1], [0, 1], "--", color="gray")
    left.set_title(f"ROC (AUC = {auc:.2f})", fontsize=9)
    left.set_xlabel("FPR")
    left.set_ylabel("TPR")
    right.plot(rec, prec, marker="o", markersize=3, color="#b45309")
    right.set_title("Precision–recall", fontsize=9)
    right.set_xlabel("recall")
    fig.tight_layout()


LESSON("Advanced", "Cross-validation done right", """
<p>One train/test split is noisy — you might get lucky. <b>k-fold cross-validation</b> splits the data into k parts, trains on k − 1 and tests on the remaining one, k times, then averages. Every row is tested exactly once.</p>
<table><tr><th>Splitter</th><th>Use when</th></tr>
<tr><td>KFold</td><td>regression, plenty of data</td></tr>
<tr><td>StratifiedKFold</td><td>classification — keeps class shares in every fold</td></tr>
<tr><td>GroupKFold</td><td>several rows per patient/user — keep each group in one fold</td></tr>
<tr><td>TimeSeriesSplit</td><td>time-ordered data — always test on the future</td></tr>
<tr><td>LeaveOneOut</td><td>tiny datasets</td></tr></table>
<p>Tune hyper-parameters with cross-validation on the training set; keep the test set for one final check.</p>
""", practice=["Cross-Validated R²", "Leave-One-Out Error", "Time-Series Splits"])


@LD
def kfold_picture():
    n, k = 12, 4
    fig, ax = plt.subplots(figsize=(5, 2.2))
    for fold, (train, test) in enumerate(KFold(k).split(np.zeros((n, 1)))):
        ax.scatter(train, [fold] * len(train), marker="s", color="#99c9c2", s=80)
        ax.scatter(test, [fold] * len(test), marker="s", color="#b45309", s=80)
    ax.set_yticks(range(k), [f"fold {i + 1}" for i in range(k)])
    ax.set_xlabel("row (orange = test)")
    ax.invert_yaxis()
