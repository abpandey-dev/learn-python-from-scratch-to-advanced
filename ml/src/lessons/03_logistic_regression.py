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
