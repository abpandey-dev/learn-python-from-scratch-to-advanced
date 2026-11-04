from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

PTS = np.array([[1, 1], [2, 1], [1, 2], [6, 5], [7, 7], [6, 7], [4, 3], [3, 5], [5, 2]], dtype=float)
LAB = np.array([0, 0, 0, 1, 1, 1, 0, 1, 0])


def regions(ax, model, title):
    xx, yy = np.meshgrid(np.linspace(0, 8, 150), np.linspace(0, 8, 150))
    zz = model.predict(np.column_stack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    ax.contourf(xx, yy, zz, alpha=0.25, cmap="coolwarm")
    ax.scatter(PTS[:, 0], PTS[:, 1], c=LAB, cmap="coolwarm", edgecolor="black")
    ax.set_title(title, fontsize=8)


LESSON("Basics", "k-nearest neighbours: ask the neighbours", """
<p>The simplest classifier: to label a new point, find the <b>k closest</b> training points and take a <b>majority vote</b> (for regression, average their values). There is no training step — the model is the data.</p>
<ul>
<li><b>Small k</b> (k = 1): follows every point — wiggly boundary, overfits noise.</li>
<li><b>Large k</b>: smooth boundary, may underfit. Choose k with validation; use an odd k for two classes to avoid ties.</li>
<li><b>Scale features</b> first — distance is everything. Optionally weight votes by 1/distance.</li>
<li>Prediction is slow on big data (compare with every point) and suffers in many dimensions (the "curse of dimensionality").</li>
</ul>
""", practice=["Distances to Every Training Point", "Classify One Point With k-NN", "k-NN for Many Points", "k-NN With Manhattan Distance", "Choose k on a Validation Set"])


@LD
def knn_regions():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, k in zip(axes, [1, 5]):
        regions(ax, KNeighborsClassifier(n_neighbors=k).fit(PTS, LAB), f"k = {k}")
    fig.tight_layout()


LESSON("Core", "k-NN for numbers", """
<p>k-NN regression predicts the average target of the k nearest neighbours. With <code>weights="distance"</code>, closer neighbours count more (weight 1/distance), which makes predictions pass through the training points and change smoothly between them.</p>
""", practice=["k-NN Regression", "Distance-Weighted k-NN"])


@LD
def knn_regression_curve():
    from sklearn.neighbors import KNeighborsRegressor
    x = np.array([1, 2, 3, 5, 8, 9], dtype=float)
    y = np.array([10, 12, 15, 20, 30, 33], dtype=float)
    grid = np.linspace(0, 10, 300).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y, zorder=3)
    for weights in ["uniform", "distance"]:
        model = KNeighborsRegressor(n_neighbors=3, weights=weights).fit(x.reshape(-1, 1), y)
        ax.plot(grid, model.predict(grid), label=weights)
    ax.legend(fontsize=8)


LESSON("Core", "Naive Bayes: Bayes' rule with a shortcut", """
<p>Naive Bayes picks the class with the highest P(class | features) ∝ P(class) × P(features | class). The "naive" shortcut assumes features are independent given the class, so P(features | class) is just a product of one-feature probabilities — easy to learn from little data, and very fast.</p>
<table><tr><th>Variant</th><th>Features</th><th>Each P(feature | class)</th></tr>
<tr><td>GaussianNB</td><td>numbers</td><td>a bell curve with the class's mean and variance</td></tr>
<tr><td>MultinomialNB</td><td>word counts</td><td>(count + α)/(total + α·vocab) — <b>Laplace smoothing</b> avoids zero probabilities</td></tr>
<tr><td>BernoulliNB</td><td>present / absent</td><td>share of the class's documents containing the word</td></tr></table>
<p>Computed with log-probabilities (sums, not products) to avoid underflow. Great baseline for text and spam filtering; probabilities tend to be over-confident.</p>
""", practice=["Class Priors", "Gaussian Naive Bayes: Means per Class", "Gaussian Naive Bayes: Variances per Class", "Gaussian Naive Bayes: Predict Probabilities", "Word Probabilities With Laplace Smoothing", "Multinomial Naive Bayes Classifier", "Bernoulli Naive Bayes"])


@LD
def gnb_regions():
    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    regions(ax, GaussianNB().fit(PTS, LAB), "Gaussian NB: curved boundary")


LESSON("Advanced", "Support vector machines: the widest street", """
<p>Many lines separate two classes. An <b>SVM</b> picks the one with the widest <b>margin</b> — the widest street with no points on it. Only the points on the edge of the street, the <b>support vectors</b>, decide where it goes.</p>
<ul>
<li>Margin width = 2/‖w‖, so maximising the margin = minimising ‖w‖ subject to y·(w·x + b) ≥ 1.</li>
<li><b>Soft margin</b>: real data overlaps, so violations are allowed at a cost — the <b>hinge loss</b> max(0, 1 − y·score). <b>C</b> trades margin width against violations (large C = fewer violations, narrower margin).</li>
</ul>
""", practice=["Hinge Loss", "Widest Margin Between Two Points", "Margin Width", "Points Inside the Margin"])


@LD
def svm_margin():
    model = SVC(kernel="linear", C=10).fit(PTS, LAB)
    w, b = model.coef_[0], model.intercept_[0]
    xs = np.linspace(0, 8, 50)
    fig, ax = plt.subplots(figsize=(4, 3.4))
    ax.scatter(PTS[:, 0], PTS[:, 1], c=LAB, cmap="coolwarm", edgecolor="black")
    for offset, style in [(0, "-"), (1, "--"), (-1, "--")]:
        ax.plot(xs, (offset - b - w[0] * xs) / w[1], style, color="black")
    sv = model.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=200, facecolors="none", edgecolors="#b45309")
    ax.set_ylim(0, 8)
    ax.set_title(f"margin = {2 / np.linalg.norm(w):.2f}; circled = support vectors", fontsize=8)


LESSON("Advanced", "Kernels: curved boundaries for free", """
<p>When classes aren't linearly separable, map points to a bigger space where they are (e.g. add x², xy, y²). The <b>kernel trick</b>: SVMs only ever need dot products between points, and a <b>kernel</b> computes the dot product in the big space directly from the original points — without building it.</p>
<table><tr><th>Kernel</th><th>K(x, z)</th></tr>
<tr><td>Linear</td><td>x·z</td></tr>
<tr><td>Polynomial</td><td>(γ x·z + r)ᵈ</td></tr>
<tr><td>RBF (Gaussian)</td><td>exp(−γ‖x − z‖²) — the default; γ controls how local the boundary is</td></tr></table>
<p>Tune C and γ together with cross-validation, and always scale features.</p>
""", practice=["RBF Kernel", "The Kernel Trick"])


@LD
def rbf_regions():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, gamma in zip(axes, [0.1, 2.0]):
        regions(ax, SVC(kernel="rbf", gamma=gamma, C=10).fit(PTS, LAB), f"RBF SVM, γ = {gamma}")
    fig.tight_layout()
