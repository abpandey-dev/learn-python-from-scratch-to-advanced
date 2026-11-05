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


LESSON("Basics", "A full worked example: screening 1,000 people", """
<p>20 of 1,000 people have a disease. A test gives these results:</p>
<table><tr><th></th><th>Predicted healthy</th><th>Predicted sick</th><th>Total</th></tr>
<tr><th>Actually healthy</th><td>TN = 931</td><td>FP = 49</td><td>980</td></tr>
<tr><th>Actually sick</th><td>FN = 2</td><td>TP = 18</td><td>20</td></tr></table>
<table><tr><th>Metric</th><th>Calculation</th><th>Value</th><th>In plain words</th></tr>
<tr><td>Accuracy</td><td>(18 + 931) / 1000</td><td>0.949</td><td>right 94.9% of the time</td></tr>
<tr><td>Recall</td><td>18 / 20</td><td>0.90</td><td>finds 90% of sick people</td></tr>
<tr><td>Precision</td><td>18 / 67</td><td>0.269</td><td>only 27% of alarms are real</td></tr>
<tr><td>Specificity</td><td>931 / 980</td><td>0.95</td><td>clears 95% of healthy people</td></tr>
<tr><td>F1</td><td>36 / (36 + 49 + 2)</td><td>0.414</td><td>combined score</td></tr></table>
<h4>The surprise</h4>
<p>A useless test that says "healthy" to everyone scores <b>98% accuracy</b>, better than this real test, while finding nobody. Accuracy alone is misleading here.</p>
<p>The test is also fine for screening despite its low precision: most people who test positive are healthy, but a follow-up test can sort them out. A missed patient (FN) is what you must avoid.</p>
<p><b>Remember:</b> precision has "predicted positive" on the bottom; recall has "actually positive" on the bottom.</p>
""", practice=["Confusion Matrix", "Precision", "Recall", "F1 Score", "Specificity"])


@LD
def screening_numbers():
    tp, fn, fp, tn = 18, 2, 49, 931
    accuracy = (tp + tn) / 1000
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    specificity = tn / (tn + fp)
    f1 = 2 * tp / (2 * tp + fp + fn)
    useless_test_accuracy = 980 / 1000
    useless_test_recall = 0 / 20


LESSON("Core", "Why F1 uses the harmonic mean, and macro vs weighted", """
<h4>The harmonic mean punishes imbalance</h4>
<p>A model flags only one sure case: precision 1.0, recall 0.01.</p>
<ul><li>Ordinary average: (1 + 0.01) / 2 = 0.505, which looks acceptable.</li>
<li>F1: 2 × 1 × 0.01 / 1.01 = <b>0.020</b>, which is honest.</li></ul>
<p>F1 is only high when both are high. If one matters more, use Fβ: β &gt; 1 favours recall.</p>
<h4>Many classes: worked example</h4>
<p>90 rows of class A and 10 of class B. Of the A rows, 85 are right and 5 are called B. Of the B rows, 4 are right and 6 are called A. This gives F1(A) = 0.939 and F1(B) = 0.421.</p>
<table><tr><th>Average</th><th>How</th><th>Result</th><th>Use when</th></tr>
<tr><td>Macro</td><td>plain mean of class scores</td><td>0.680</td><td>every class matters equally</td></tr>
<tr><td>Weighted</td><td>mean weighted by class size</td><td>0.887</td><td>larger classes matter more</td></tr>
<tr><td>Micro</td><td>pool all counts (equals accuracy here)</td><td>0.890</td><td>each row matters equally</td></tr></table>
<p>The weak class B is obvious in the macro score and hidden in the other two. Always look at per-class scores too.</p>
""", practice=["Macro vs Weighted F1", "Per-Class Precision and Recall", "F1 Score"])


@LD
def averaging_compare():
    from sklearn.metrics import f1_score
    y = np.array(["A"] * 90 + ["B"] * 10)
    pred = np.array(["A"] * 85 + ["B"] * 5 + ["A"] * 6 + ["B"] * 4)
    per_class = f1_score(y, pred, average=None)
    macro = f1_score(y, pred, average="macro")
    weighted = f1_score(y, pred, average="weighted")
    micro = f1_score(y, pred, average="micro")


LESSON("Core", "ROC and PR curves, by hand", """
<p>Six rows sorted by score. Lower the threshold one row at a time:</p>
<table><tr><th>Row's score</th><th>True label</th><th>TP</th><th>FP</th><th>TPR (recall)</th><th>FPR</th><th>Precision</th></tr>
<tr><td>0.9</td><td>1</td><td>1</td><td>0</td><td>0.33</td><td>0</td><td>1.00</td></tr>
<tr><td>0.8</td><td>1</td><td>2</td><td>0</td><td>0.67</td><td>0</td><td>1.00</td></tr>
<tr><td>0.7</td><td>0</td><td>2</td><td>1</td><td>0.67</td><td>0.33</td><td>0.67</td></tr>
<tr><td>0.6</td><td>1</td><td>3</td><td>1</td><td>1.00</td><td>0.33</td><td>0.75</td></tr>
<tr><td>0.4</td><td>0</td><td>3</td><td>2</td><td>1.00</td><td>0.67</td><td>0.60</td></tr>
<tr><td>0.2</td><td>0</td><td>3</td><td>3</td><td>1.00</td><td>1.00</td><td>0.50</td></tr></table>
<p>A positive row moves the ROC curve up; a negative row moves it right.</p>
<h4>ROC AUC by counting pairs</h4>
<p>Compare each of the 3 positives with each of the 3 negatives (0.7, 0.4, 0.2). 0.9 beats 3, 0.8 beats 3, and 0.6 beats 2. So AUC = 8 / 9 = <b>0.889</b>: a random positive outranks a random negative 89% of the time.</p>
<h4>Average precision</h4>
<p>Add precision each time recall rises by 1/3: (1/3)(1.00) + (1/3)(1.00) + (1/3)(0.75) = <b>0.917</b>.</p>
<p><b>Which to use?</b> With rare positives, ROC AUC can look great while most alerts are false. Prefer PR-AUC there. Note that a random model's PR-AUC equals the share of positives, not 0.5.</p>
""", practice=["ROC Curve Points", "ROC AUC", "Average Precision (PR AUC)"])


@LD
def rare_positives():
    from sklearn.metrics import average_precision_score
    rng = np.random.default_rng(0)
    y = np.r_[np.zeros(1980, dtype=int), np.ones(20, dtype=int)]
    scores = np.r_[rng.normal(0, 1, 1980), rng.normal(2, 1, 20)]
    fpr, tpr, _ = roc_curve(y, scores)
    prec, rec, _ = precision_recall_curve(y, scores)
    auc = roc_auc_score(y, scores)
    ap = average_precision_score(y, scores)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.9))
    left.plot(fpr, tpr)
    left.set_title(f"ROC AUC = {auc:.2f}: looks great", fontsize=9)
    right.plot(rec, prec, color="#b45309")
    right.set_title(f"PR AUC = {ap:.2f}: the honest view (1% positive)", fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "Which metric for which problem?", """
<table><tr><th>Problem</th><th>Worst mistake</th><th>Focus on</th></tr>
<tr><td>Cancer screening</td><td>missing a patient (FN)</td><td>recall, at acceptable precision</td></tr>
<tr><td>Spam filter</td><td>losing real email (FP)</td><td>precision</td></tr>
<tr><td>Fraud detection</td><td>both, with rare positives</td><td>PR-AUC, cost in money</td></tr>
<tr><td>Ranking leads for a sales team</td><td>a poor order</td><td>ROC AUC, precision at top k</td></tr>
<tr><td>Weather probability</td><td>wrong probabilities</td><td>log-loss, Brier score, calibration</td></tr>
<tr><td>Balanced image classes</td><td>any error</td><td>accuracy, macro F1</td></tr>
<tr><td>House prices</td><td>typical error</td><td>MAE or RMSE in rupees</td></tr></table>
<h4>Calibration</h4>
<p>Of all cases given 80%, about 80% should turn out positive. A model can rank perfectly and still have wrong probabilities. A <b>calibration curve</b> shows this: a well-calibrated model follows the diagonal.</p>
<h4>Choosing the score you report</h4>
<ul>
<li>Agree on the metric <b>before</b> training.</li>
<li>Translate it for the business: "catches 90% of fraud with 1 false alarm in 200".</li>
<li>Report a spread, not just a mean: 0.82 ± 0.03 across folds.</li>
</ul>
""", practice=["Brier Score", "Cost of Mistakes", "Best Threshold for F1"])


@LD
def calibration_demo():
    from sklearn.calibration import calibration_curve
    rng = np.random.default_rng(0)
    p_true = rng.uniform(0, 1, 4000)
    y = (rng.uniform(0, 1, 4000) < p_true).astype(int)
    overconfident = np.clip((p_true - 0.5) * 2 + 0.5, 0.001, 0.999)
    fig, ax = plt.subplots(figsize=(4, 3.1))
    ax.plot([0, 1], [0, 1], "--", color="gray", label="perfect")
    for name, p in [("calibrated", p_true), ("overconfident", overconfident)]:
        frac, mean_p = calibration_curve(y, p, n_bins=8)
        ax.plot(mean_p, frac, "o-", markersize=3, label=name)
    ax.set_xlabel("predicted probability")
    ax.set_ylabel("actual share positive")
    ax.legend(fontsize=7)


LESSON("Advanced", "Choosing a validation strategy", """
<p>Your validation must imitate how the model will be used. Otherwise the score is an illusion.</p>
<table><tr><th>Situation</th><th>Mistake</th><th>Use</th></tr>
<tr><td>Rare class</td><td>a fold with no positives</td><td>StratifiedKFold</td></tr>
<tr><td>Many rows per patient</td><td>same patient in train and test</td><td>GroupKFold</td></tr>
<tr><td>Forecasting</td><td>training on the future</td><td>TimeSeriesSplit</td></tr>
<tr><td>Tiny data (under ~50 rows)</td><td>a noisy single split</td><td>repeated k-fold or leave-one-out</td></tr>
<tr><td>Tuning and also reporting</td><td>the best score is optimistic</td><td>nested CV or a separate test set</td></tr></table>
<h4>Worked example: why groups matter</h4>
<p>Suppose each patient has 10 scans. A random split puts scans of the same patient on both sides. The model recognises the patient, not the disease, and scores 98%. With patients kept whole it may drop to 70%, and <b>70% is the true number</b>.</p>
<h4>How many folds?</h4>
<p>5 or 10 is the usual choice. More folds give more training data per fold but take longer. Don't read much into small differences: if the fold scores vary by ±0.03, a gain of 0.005 is noise.</p>
""", practice=["Cross-Validated R²", "Time-Series Splits", "Leave-One-Out Error"])


@LD
def group_leak_demo():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GroupKFold, cross_val_score
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(30), 10)
    fingerprint = np.repeat(rng.normal(size=(30, 5)), 10, axis=0) + rng.normal(0, 0.1, (300, 5))
    y = np.repeat(rng.integers(0, 2, 30), 10)
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    shuffled = cross_val_score(model, fingerprint, y, cv=KFold(5, shuffle=True, random_state=0)).mean()
    grouped = cross_val_score(model, fingerprint, y, cv=GroupKFold(5), groups=groups).mean()
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.bar(["random folds\n(leaky)", "groups kept whole\n(honest)"], [shuffled, grouped], color=["#b91c1c", "#0f766e"])
    ax.axhline(0.5, ls="--", color="gray")
    ax.set_ylabel("accuracy (labels are random)")
