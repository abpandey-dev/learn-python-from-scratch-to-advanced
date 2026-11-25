from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
X = np.round(rng.uniform(0, 10, size=(60, 3)), 1)
y = 3 * X[:, 0] + 1.0 * X[:, 1] + rng.normal(0, 1, 60)

LESSON("Basics", "Why explain a model at all?", """
<p>A bank model rejects a loan. The customer asks why; the regulator asks whether it discriminates; the data scientist asks whether it learned something real or a quirk of the data. <b>Explainability</b> answers all three:</p>
<ul>
<li><b>Global</b> explanations: what matters to the model overall (feature importance, partial dependence).</li>
<li><b>Local</b> explanations: why <i>this</i> prediction (contributions, Shapley values, counterfactuals).</li>
</ul>
<p>Explanations also catch bugs. If "customer ID" is the most important feature, something has leaked.</p>
<p>For a linear model the explanation is exact: each feature contributes coef × (value − average value), and these add up from the average prediction to this prediction.</p>
""", practice=["Explain a Linear Prediction"])


@LD
def waterfall():
    m = LinearRegression().fit(X, y)
    row = X[0]
    contrib = m.coef_ * (row - X.mean(axis=0))
    base = m.predict(X).mean()
    fig, ax = plt.subplots(figsize=(5, 2.6))
    labels = ["average"] + [f"x{j}" for j in range(3)] + ["prediction"]
    starts = [0, base, base + contrib[0], base + contrib[:2].sum(), 0]
    heights = [base, *contrib, base + contrib.sum()]
    colors = ["#94a3b8"] + ["#0f766e" if c > 0 else "#b45309" for c in contrib] + ["#334155"]
    ax.bar(labels, heights, bottom=starts, color=colors)
    ax.set_title("From the average prediction to this one")


LESSON("Core", "Shapley values: fair credit", """
<p>When features interact, "how much did each one add?" depends on the order you add them. <b>Shapley values</b>, from game theory, average a feature's marginal contribution over <i>every</i> order. They are the only attribution that is fair in a precise sense: contributions add up to the prediction, identical features get equal credit, and a feature that never matters gets zero.</p>
<p>Exact Shapley values need every subset of features (2ⁿ), so the <code>shap</code> library approximates them, or computes them exactly and fast for trees (TreeSHAP). Typical plots: a <b>waterfall</b> for one prediction, a <b>beeswarm</b> for the whole dataset.</p>
<pre><code class="py">import shap
explainer = shap.Explainer(model, X_background)
sv = explainer(X_test); shap.plots.waterfall(sv[0])</code></pre>
""", practice=["Shapley Values by Hand"])

LESSON("Core", "Global explanations: importance and partial dependence", """
<ul>
<li><b>Permutation importance</b>: shuffle one column and see how much the score drops. Works for any model; measure it on validation data. Correlated features share credit, so both can look unimportant.</li>
<li><b>Impurity importance</b> (trees, forests): total impurity reduction from splits on a feature. Free to compute, but biased towards features with many distinct values.</li>
<li><b>Partial dependence</b>: set a feature to each value for every row, average the predictions, and plot. It shows the <i>shape</i> of the effect — linear, a threshold, a plateau. <b>ICE</b> curves show the same per row, revealing interactions.</li>
</ul>
""", practice=["Rank Features by Permutation Importance", "Where Tree Importances Come From", "Partial Dependence"])

LESSON("Core", "Counterfactuals: what would change the decision?", """
<p>"Your loan would be approved if your income were ₹3.13 lakh higher" is the explanation people actually want. A <b>counterfactual</b> is the smallest realistic change that flips the outcome. For a linear score w·x + b it has a closed form; for other models it's a search. Good counterfactuals change only things a person can act on — never age or gender.</p>
""", practice=["Counterfactual: What Would Change the Decision?"])

LESSON("Core", "Fairness: measuring bias across groups", """
<p>A model can be accurate overall and still treat groups differently. Compare these across a sensitive attribute (gender, age band, region):</p>
<table>
<tr><th>Criterion</th><th>Equal across groups</th><th>Check</th></tr>
<tr><td>Demographic parity</td><td>selection rate P(ŷ = 1)</td><td>difference, or ratio ≥ 0.8 (the "80% rule")</td></tr>
<tr><td>Equal opportunity</td><td>true positive rate</td><td>qualified people approved equally</td></tr>
<tr><td>Equalized odds</td><td>TPR and FPR</td><td>both kinds of mistakes equal</td></tr>
<tr><td>Calibration</td><td>P(y = 1 | score)</td><td>a score of 0.7 means 70% in every group</td></tr>
</table>
<p>These can't all hold at once when base rates differ, so choosing one is a policy decision, not a technical one. Dropping the sensitive column doesn't remove bias: <b>proxies</b> such as pincode can encode it. Measure, then mitigate: rebalance or reweight training data, add constraints, or set thresholds per group where the law allows.</p>
""", practice=["Demographic Parity Difference", "Disparate Impact and the 80% Rule", "Equal Opportunity", "Equalized Odds Gap", "Find Proxy Features"])

LESSON("Advanced", "Calibration and imbalanced data", """
<p>A model is <b>calibrated</b> if, among cases it scores 0.8, about 80% are positive. Check with a reliability curve, the Brier score and ECE; fix with Platt scaling or isotonic regression (<code>CalibratedClassifierCV</code>). Calibration matters whenever the probability itself drives a decision or a price.</p>
<p>With <b>imbalanced classes</b> (1% fraud), accuracy is useless: predicting "never fraud" scores 99%. Instead:</p>
<ul>
<li>Use balanced accuracy, precision/recall, PR-AUC.</li>
<li>Reweight with <code>class_weight="balanced"</code>, or resample (undersample the majority, oversample or SMOTE the minority — on training data only).</li>
<li><b>Move the threshold</b>: pick it on validation data to maximise F1, or to minimise expected cost when a missed fraud costs far more than a false alarm.</li>
</ul>
""", practice=["Reliability Curve", "Brier Score", "Expected Calibration Error", "Balanced Class Weights", "Threshold That Maximises F1", "Cost-Sensitive Threshold", "Accuracy vs Balanced Accuracy"])

LESSON("Advanced", "Responsible AI in practice", """
<ul>
<li><b>Privacy</b>: remove or mask personal data (names, emails, phone numbers, IDs) before training or sending text to an LLM. Check <b>k-anonymity</b>: every combination of quasi-identifiers (pincode, age band, gender) should match at least k people, or individuals can be re-identified.</li>
<li><b>Documentation</b>: a <b>model card</b> records intended use, training data, metrics per group, known limits and ethical considerations; a <b>datasheet</b> does the same for a dataset.</li>
<li><b>Human oversight</b>: high-stakes decisions (credit, hiring, health) need appeal routes and human review; laws such as the EU AI Act and India's DPDP Act set obligations.</li>
<li><b>Monitoring</b>: fairness and calibration can drift after deployment, so track them like accuracy.</li>
</ul>
""", practice=["Mask Personal Data", "k-Anonymity"])
