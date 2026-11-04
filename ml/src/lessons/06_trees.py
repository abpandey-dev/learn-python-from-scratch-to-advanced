from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree

X3 = np.array([[1, 1], [2, 5], [3, 2], [4, 6], [5, 3], [6, 7], [7, 1], [8, 4], [2, 8], [7, 8]], dtype=float)
Y3 = np.array([0, 1, 0, 1, 0, 1, 1, 1, 0, 0])

LESSON("Basics", "A model made of questions", """
<p>A <b>decision tree</b> predicts by asking yes/no questions about the features, like a game of 20 questions: "Is income ≤ 40k? → Is age ≤ 30? → predict 'decline'".</p>
<ul>
<li>The top question is the <b>root</b>; the final answers are <b>leaves</b>.</li>
<li>A classification leaf predicts the most common class of the training rows that reached it (and their shares as probabilities); a regression leaf predicts their average.</li>
<li>The boundary is made of axis-parallel steps. No scaling needed, handles mixed feature types, and is easy to explain.</li>
</ul>
""", practice=["Majority Class at the Root", "Predict With a Stump", "Which Leaf Does Each Row Reach?", "Leaf Probabilities"])


@LD
def draw_tree():
    tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X3, Y3)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    plot_tree(tree, feature_names=["x0", "x1"], class_names=["no", "yes"], filled=True, impurity=True, ax=ax, fontsize=7)


LESSON("Core", "Choosing a question: impurity", """
<p>A good question splits the data into groups that are each as <b>pure</b> (single-class) as possible. Impurity measures how mixed a group is:</p>
<table><tr><th>Measure</th><th>Formula</th><th>Pure</th><th>50/50</th></tr>
<tr><td><b>Gini</b></td><td>1 − Σpₖ²</td><td>0</td><td>0.5</td></tr>
<tr><td><b>Entropy</b></td><td>−Σpₖ log₂ pₖ</td><td>0</td><td>1</td></tr>
<tr><td>MSE (regression)</td><td>variance of the targets</td><td>0</td><td>—</td></tr></table>
<p>The algorithm tries <b>every feature</b> and <b>every threshold</b> (midpoints between neighbouring values) and picks the one with the largest <b>impurity decrease</b> = parent impurity − size-weighted child impurity (with entropy this is the <b>information gain</b>).</p>
""", practice=["Gini Impurity of a Node", "Entropy of a Node", "Weighted Gini of a Given Split", "Best Split Threshold", "Impurity Decrease of the Best Split", "Which Feature Splits Best?", "Gini vs Entropy", "Samples in Each Leaf"])


@LD
def split_search():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([0, 0, 0, 1, 1, 0, 1, 1])
    thresholds = (x[:-1] + x[1:]) / 2

    def gini(part):
        p = part.mean() if len(part) else 0
        return 1 - p ** 2 - (1 - p) ** 2

    weighted = [(len(y[x <= t]) * gini(y[x <= t]) + len(y[x > t]) * gini(y[x > t])) / len(y) for t in thresholds]
    best = thresholds[int(np.argmin(weighted))]
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(thresholds, weighted, "o-")
    ax.axvline(best, ls="--", color="#b45309")
    ax.set_xlabel("threshold")
    ax.set_ylabel("weighted Gini after split")
    ax.set_title(f"best threshold = {best}", fontsize=9)


LESSON("Core", "Growing, stopping and overfitting", """
<p>The tree splits recursively until every leaf is pure — which memorises the training data (100% training accuracy, poor test accuracy). Stop it earlier (<b>pre-pruning</b>):</p>
<table><tr><th>Hyper-parameter</th><th>Effect</th></tr>
<tr><td>max_depth</td><td>limit the number of questions in a row</td></tr>
<tr><td>min_samples_leaf</td><td>every leaf must keep at least this many rows</td></tr>
<tr><td>min_samples_split</td><td>a node needs this many rows to be split</td></tr>
<tr><td>max_leaf_nodes</td><td>grow best-first up to a leaf budget</td></tr>
<tr><td>ccp_alpha</td><td>post-pruning: remove branches that don't pay for their complexity</td></tr></table>
<p>Trees are <b>unstable</b>: a small change in data can change the whole tree. That weakness is what ensembles (next topic) fix.</p>
""", practice=["A Depth-2 Tree", "How Deep Does It Grow?", "Training Accuracy by Depth", "Minimum Samples per Leaf", "Best-First Growth With a Leaf Budget"])


@LD
def depth_regions():
    xx, yy = np.meshgrid(np.linspace(0, 9, 150), np.linspace(0, 9, 150))
    grid = np.column_stack([xx.ravel(), yy.ravel()])
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.7))
    for ax, depth in zip(axes, [1, 2, None]):
        tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X3, Y3)
        ax.contourf(xx, yy, tree.predict(grid).reshape(xx.shape), alpha=0.25, cmap="coolwarm")
        ax.scatter(X3[:, 0], X3[:, 1], c=Y3, cmap="coolwarm", edgecolor="black")
        ax.set_title(f"max_depth = {depth}", fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "Regression trees and feature importance", """
<p>For numbers, the impurity is the variance (MSE) and each leaf predicts the mean — so the prediction curve is a <b>staircase</b>. Trees can't extrapolate beyond the range they saw.</p>
<p><b>Feature importance</b> (mean decrease in impurity) adds up, for each feature, how much impurity its splits removed, weighted by the share of rows they affected, then normalises to 1. Fast, but biased towards features with many distinct values — <b>permutation importance</b> on validation data is more trustworthy.</p>
""", practice=["Regression Stump", "Regression Tree Predictions", "Feature Importances"])


@LD
def staircase():
    x = np.array([1, 2, 3, 4, 5, 6], dtype=float).reshape(-1, 1)
    y = np.array([5.0, 6.0, 5.5, 12.0, 13.0, 12.5])
    grid = np.linspace(0, 7, 300).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y, zorder=3)
    for depth in [1, 2]:
        ax.plot(grid, DecisionTreeRegressor(max_depth=depth, random_state=0).fit(x, y).predict(grid), label=f"depth {depth}")
    ax.legend(fontsize=8)
