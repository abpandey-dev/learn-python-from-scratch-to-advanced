from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression

LESSON("Basics", "From a line to a probability", """
<p>For yes/no questions (spam? fraud? will the customer leave?) we want a <b>probability</b> between 0 and 1, not any number. Logistic regression computes the same weighted sum as linear regression, z = w·x + b, then squashes it with the <b>sigmoid</b>:</p>
<p style="text-align:center"><b>p = σ(z) = 1 / (1 + e⁻ᶻ)</b></p>
<p>Large positive z → p near 1; large negative → near 0; z = 0 → 0.5. We predict class 1 when p ≥ 0.5, i.e. when z ≥ 0 — so the <b>decision boundary</b> w·x + b = 0 is a straight line (a plane in higher dimensions).</p>
<p>z is the <b>log-odds</b>: ln(p/(1 − p)). So each weight says how much the log-odds rise per unit of its feature; e^w is the <b>odds ratio</b>.</p>
""", practice=["Sigmoid Probabilities", "Odds and Log-Odds", "Predict With Given Weights", "Find the Decision Boundary", "Odds Ratio of a Feature"])


@LD
def sigmoid_fit():
    x = np.array([1, 2, 3, 4, 5, 6])
    y = np.array([0, 0, 1, 0, 1, 1])
    model = LogisticRegression(C=1e10).fit(x.reshape(-1, 1), y)
    grid = np.linspace(0, 7, 200)
    prob = model.predict_proba(grid.reshape(-1, 1))[:, 1]
    boundary = -model.intercept_[0] / model.coef_[0, 0]
    fig, ax = plt.subplots(figsize=(4.8, 3))
    ax.scatter(x, y, zorder=3)
    ax.plot(grid, prob, color="#b45309", label="P(y = 1)")
    ax.axvline(boundary, ls="--", color="gray", label=f"boundary x = {boundary:.2f}")
    ax.legend(fontsize=7)


LESSON("Core", "Training: log-loss", """
<p>We can't use squared error well here; instead we use <b>log-loss</b> (binary cross-entropy): for each example, −ln p if the true label is 1, −ln(1 − p) if it is 0. Confident wrong answers cost a lot; confident right answers cost almost nothing.</p>
<p>The log-loss is convex, so gradient descent (or Newton's method) always finds the best weights. Its gradient is beautifully simple: <b>Xᵀ(p − y)/n</b> — the error times the features, just like linear regression.</p>
<p>sklearn's <code>LogisticRegression</code> adds L2 regularisation by default with strength 1/C: small C = strong penalty = simpler model.</p>
""", practice=["Binary Log-Loss", "Gradient of the Log-Loss", "Train Logistic Regression (One Feature)", "Train Logistic Regression (Two Features)", "Stronger Regularisation, Smaller Weight", "Probabilities for New Points"])


@LD
def log_loss_shape():
    p = np.linspace(0.01, 0.99, 200)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(p, -np.log(p), label="true label 1")
    ax.plot(p, -np.log(1 - p), label="true label 0")
    ax.set_xlabel("predicted probability of 1")
    ax.set_ylabel("loss")
    ax.legend(fontsize=8)


LESSON("Core", "Decision boundaries in two dimensions", """
<p>With two features, the boundary w₁x₁ + w₂x₂ + b = 0 is a line through the plane: everything on one side is predicted class 1. Logistic regression can only draw <b>straight</b> boundaries — add polynomial features or use a non-linear model (trees, k-NN, kernel SVM, neural network) when the classes curve around each other.</p>
<p>The <b>threshold</b> 0.5 is a choice: lower it to catch more positives (higher recall, more false alarms), raise it to be more certain (higher precision). For imbalanced data, also try <code>class_weight="balanced"</code>.</p>
""", practice=["Accuracy", "Move the Threshold", "Count the Mistakes", "Class-Weighted Logistic Regression"])


@LD
def boundary_2d():
    X = np.array([[1, 2], [2, 1], [3, 3], [4, 2], [5, 5], [6, 4], [2, 3], [5, 2]], dtype=float)
    y = np.array([0, 0, 1, 0, 1, 1, 1, 0])
    model = LogisticRegression().fit(X, y)
    xx, yy = np.meshgrid(np.linspace(0, 7, 120), np.linspace(0, 6, 120))
    prob = model.predict_proba(np.column_stack([xx.ravel(), yy.ravel()]))[:, 1].reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(4.5, 3.4))
    ax.contourf(xx, yy, prob, levels=20, cmap="RdBu_r", alpha=0.5)
    ax.contour(xx, yy, prob, levels=[0.5], colors="black")
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="RdBu_r", edgecolor="black")
    ax.set_title("colour = P(class 1); line = boundary", fontsize=8)


LESSON("Advanced", "More than two classes, and the perceptron", """
<p><b>Multiclass</b> logistic regression keeps one weight vector per class, scores every class, and turns the scores into probabilities with <b>softmax</b>. The loss becomes categorical cross-entropy: −ln(probability of the true class). The alternative is <b>one-vs-rest</b>: train one yes/no model per class and pick the most confident.</p>
<p>The <b>perceptron</b> (1958) is the ancestor of neural networks: the same linear score, but a hard 0/1 output and a simple rule — when it's wrong, add the example (or subtract it) to the weights. It finds a separating line if one exists, but no probabilities.</p>
""", practice=["Softmax for Many Classes", "Multiclass Prediction From Weights", "Multiclass Log-Loss", "One-vs-Rest Targets", "Train a Perceptron"])


@LD
def softmax_demo():
    scores = np.array([2.0, 1.0, 0.1])
    exp = np.exp(scores - scores.max())
    probs = exp / exp.sum()
    predicted_class = int(np.argmax(probs))
    loss_if_true_is_0 = -math.log(probs[0])
    loss_if_true_is_2 = -math.log(probs[2])


LESSON("Basics", "The sigmoid and odds, by hand", """
<h4>From score to probability</h4>
<table><tr><th>Score z</th><th>−2</th><th>−1</th><th>0</th><th>1</th><th>2</th></tr>
<tr><th>σ(z) = 1 / (1 + e⁻ᶻ)</th><td>0.119</td><td>0.269</td><td>0.5</td><td>0.731</td><td>0.881</td></tr></table>
<p>The score can be any number, while the output always lies between 0 and 1.</p>
<h4>What are odds?</h4>
<p>Odds = p / (1 − p). A probability of 0.8 means odds of 4, or "4 to 1". The log-odds are ln 4 = 1.386, and that is the z the model computes. So logistic regression is <b>a straight line on the log-odds scale</b>.</p>
<h4>Worked example: reading a coefficient</h4>
<p>Suppose study hours have weight w = 0.7. Then e^0.7 = 2.01, so <b>each extra hour roughly doubles the odds of passing</b>.</p>
<ol>
<li>A student has p = 0.2, so the odds are 0.2 / 0.8 = 0.25.</li>
<li>One more hour: 0.25 × 2.01 = 0.503.</li>
<li>Back to probability: 0.503 / 1.503 = <b>0.335</b>.</li>
</ol>
<p>Notice that the probability doesn't double. The same weight moves p by different amounts depending on where you start, while it always multiplies the odds by the same factor.</p>
""", practice=["Sigmoid Probabilities", "Odds and Log-Odds", "Odds Ratio of a Feature"])


@LD
def odds_walkthrough():
    w = 0.7
    odds_ratio = math.exp(w)
    p_before = 0.2
    odds_before = p_before / (1 - p_before)
    odds_after = odds_before * odds_ratio
    p_after = odds_after / (1 + odds_after)
    log_odds_before = math.log(odds_before)
    log_odds_after = log_odds_before + w
    check = 1 / (1 + math.exp(-log_odds_after))


LESSON("Core", "Where log-loss comes from", """
<p>Log-loss isn't arbitrary. It comes from one question: <b>which weights make the labels we saw most probable?</b> This is called maximum likelihood.</p>
<h4>Worked example</h4>
<p>A model gives three examples these probabilities of their <b>true</b> labels: 0.9, 0.8, 0.7.</p>
<ul>
<li>Probability of getting all three right: 0.9 × 0.8 × 0.7 = 0.504.</li>
<li>Products of many small numbers underflow, so take logs: ln 0.9 + ln 0.8 + ln 0.7 = −0.685.</li>
<li>Flip the sign and average: <b>log-loss = 0.685 / 3 = 0.228</b>.</li>
</ul>
<p>So maximising the likelihood and minimising log-loss are the same thing.</p>
<h4>Confident mistakes are punished hard</h4>
<table><tr><th>Probability given to the true label</th><th>Loss for that row</th></tr>
<tr><td>0.9</td><td>0.105</td></tr><tr><td>0.5</td><td>0.693</td></tr><tr><td>0.01</td><td><b>4.605</b></td></tr></table>
<p><b>Why not squared error?</b> With a sigmoid, squared error becomes non-convex, with flat regions where wrong and confident predictions get almost no gradient. Log-loss is convex and its gradient stays strong exactly when the model is confidently wrong.</p>
""", practice=["Binary Log-Loss", "Gradient of the Log-Loss"])


@LD
def likelihood_by_hand():
    probs_of_truth = np.array([0.9, 0.8, 0.7])
    likelihood = probs_of_truth.prod()
    log_likelihood = np.log(probs_of_truth).sum()
    log_loss_value = -log_likelihood / len(probs_of_truth)
    costs = {p: -math.log(p) for p in [0.9, 0.5, 0.01]}


LESSON("Core", "One training step, by hand", """
<p>Two examples: (x = 1, y = 0) and (x = 3, y = 1). Start at w = 0, b = 0, with learning rate 1.</p>
<h4>Step 1: predict</h4>
<p>Both scores are 0, so both probabilities are 0.5. The loss is ln 2 = <b>0.693</b>.</p>
<h4>Step 2: gradient = mean of (p − y) × feature</h4>
<table><tr><th>x</th><th>y</th><th>p</th><th>p − y</th><th>(p − y)·x</th></tr>
<tr><td>1</td><td>0</td><td>0.5</td><td>0.5</td><td>0.5</td></tr>
<tr><td>3</td><td>1</td><td>0.5</td><td>−0.5</td><td>−1.5</td></tr></table>
<p>∂L/∂w = (0.5 − 1.5) / 2 = −0.5, and ∂L/∂b = (0.5 − 0.5) / 2 = 0.</p>
<h4>Step 3: update</h4>
<p>w = 0 − 1 × (−0.5) = 0.5, and b stays 0.</p>
<h4>Step 4: did it help?</h4>
<p>The new probabilities are σ(0.5) = 0.622 and σ(1.5) = 0.818. The first example actually got worse (y = 0, and p rose), but the second improved more. The loss falls to <b>0.588</b>.</p>
<p><b>Read the gradient like this:</b> each row pushes the weight in proportion to its error and its feature value. Rows the model already gets right barely push at all.</p>
""", practice=["Gradient of the Log-Loss", "Train Logistic Regression (One Feature)"])


@LD
def logistic_step():
    x = np.array([1.0, 3.0])
    y = np.array([0.0, 1.0])
    w, b = 0.0, 0.0
    p = 1 / (1 + np.exp(-(w * x + b)))
    loss_before = -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()
    grad_w = ((p - y) * x).mean()
    grad_b = (p - y).mean()
    w = w - 1.0 * grad_w
    b = b - 1.0 * grad_b
    p = 1 / (1 + np.exp(-(w * x + b)))
    loss_after = -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()


LESSON("Advanced", "Choosing the decision threshold", """
<p>The model gives probabilities. Turning them into decisions is <b>your</b> choice, and 0.5 is only the default.</p>
<h4>Worked example</h4>
<p>True labels 1, 1, 0, 1, 0, 0 with scores 0.9, 0.8, 0.7, 0.6, 0.4, 0.2:</p>
<table><tr><th>Threshold</th><th>TP</th><th>FP</th><th>FN</th><th>Precision</th><th>Recall</th></tr>
<tr><td>0.75</td><td>2</td><td>0</td><td>1</td><td>1.00</td><td>0.67</td></tr>
<tr><td>0.50</td><td>3</td><td>1</td><td>0</td><td>0.75</td><td>1.00</td></tr>
<tr><td>0.30</td><td>3</td><td>2</td><td>0</td><td>0.60</td><td>1.00</td></tr></table>
<h4>How to choose</h4>
<ul>
<li><b>Missing a case is costly</b> (cancer screening): choose a low threshold for high recall.</li>
<li><b>False alarms are costly</b> (blocking a real customer's payment): choose a high threshold for high precision.</li>
<li><b>You know the costs:</b> choose the threshold with the lowest total cost.</li>
</ul>
<p>Choose it on validation data, never on the test set.</p>
<p><b>Can you trust the probabilities?</b> Regularisation, class weights and resampling all distort them. Class weights especially push them away from the true frequencies, so recalibrate if the numbers themselves matter (<code>CalibratedClassifierCV</code>).</p>
""", practice=["Move the Threshold", "Class-Weighted Logistic Regression"])


@LD
def threshold_table():
    y = np.array([1, 1, 0, 1, 0, 0])
    scores = np.array([0.9, 0.8, 0.7, 0.6, 0.4, 0.2])
    table = {}
    for t in [0.75, 0.5, 0.3]:
        pred = scores >= t
        tp = int((pred & (y == 1)).sum())
        fp = int((pred & (y == 0)).sum())
        fn = int((~pred & (y == 1)).sum())
        table[t] = (tp, fp, fn, round(tp / (tp + fp), 2), round(tp / (tp + fn), 2))


LESSON("Advanced", "Softmax by hand, and when weights explode", """
<h4>Softmax for three classes</h4>
<p>Scores 2, 1, 0:</p>
<ol>
<li>Exponentiate: e² = 7.389, e¹ = 2.718, e⁰ = 1.</li>
<li>Add them up: 11.107.</li>
<li>Divide: <b>0.665, 0.245, 0.090</b>.</li>
</ol>
<p>Exponentials exaggerate differences while keeping every probability positive and the total at 1. If the true class is the first, the loss is −ln 0.665 = 0.408.</p>
<h4>Perfectly separable data</h4>
<p>If a line separates the classes perfectly, the loss keeps falling as the weights grow, since larger weights push every probability closer to 0 or 1. Without a penalty the weights head towards infinity and the model becomes absurdly overconfident.</p>
<p>This is why sklearn regularises by default. The demo shows the weight growing as C rises (less regularisation).</p>
<h4>Feature scaling</h4>
<p>Unlike plain linear regression, regularised logistic regression <b>needs</b> scaled features: the penalty treats all weights alike, so a feature's units change how hard it gets penalised. Solvers also converge faster on scaled data.</p>
""", practice=["Softmax for Many Classes", "Multiclass Log-Loss", "Stronger Regularisation, Smaller Weight"])


@LD
def separable_weights():
    x = np.array([1, 2, 3, 6, 7, 8], dtype=float).reshape(-1, 1)
    y = np.array([0, 0, 0, 1, 1, 1])
    Cs = np.logspace(-3, 4, 15)
    weights = [LogisticRegression(C=c, max_iter=5000).fit(x, y).coef_[0, 0] for c in Cs]
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.semilogx(Cs, weights, "o-", markersize=3)
    ax.set_xlabel("C (larger = less regularisation)")
    ax.set_ylabel("learned weight")
    ax.set_title("Separable data: the weight keeps growing", fontsize=9)
