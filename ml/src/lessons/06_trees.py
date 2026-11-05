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


LESSON("Basics", "Impurity by hand", """
<p>A node has some mix of classes. Impurity puts a number on the mix.</p>
<h4>Gini = 1 − Σ(share)²</h4>
<p>You can read Gini as: pick two rows at random from the node; how often do their classes differ?</p>
<table><tr><th>Node</th><th>Shares</th><th>Calculation</th><th>Gini</th></tr>
<tr><td>4 yes, 4 no</td><td>0.5, 0.5</td><td>1 − 0.25 − 0.25</td><td>0.50 (most mixed)</td></tr>
<tr><td>1 no, 4 yes</td><td>0.2, 0.8</td><td>1 − 0.04 − 0.64</td><td>0.32</td></tr>
<tr><td>3 no, 0 yes</td><td>1, 0</td><td>1 − 1 − 0</td><td>0 (pure)</td></tr></table>
<h4>Entropy = −Σ share × log₂(share)</h4>
<p>This measures surprise in bits: how many yes/no questions you'd need on average to identify the class.</p>
<table><tr><th>Node</th><th>Calculation</th><th>Entropy</th></tr>
<tr><td>4 yes, 4 no</td><td>−0.5·log₂0.5 − 0.5·log₂0.5</td><td>1.000</td></tr>
<tr><td>1 no, 4 yes</td><td>−0.2·log₂0.2 − 0.8·log₂0.8</td><td>0.722</td></tr>
<tr><td>pure</td><td>−1·log₂1</td><td>0</td></tr></table>
""", practice=["Gini Impurity of a Node", "Entropy of a Node"])


@LD
def impurity_curves():
    p = np.linspace(0.001, 0.999, 200)
    gini_values = 2 * p * (1 - p)
    entropy_values = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.plot(p, gini_values, label="Gini")
    ax.plot(p, entropy_values, label="Entropy")
    ax.set_xlabel("share of class 1 in the node")
    ax.legend(fontsize=8)
    ax.set_title("Zero when pure, highest at 50/50", fontsize=9)


LESSON("Core", "Finding the best split, every candidate by hand", """
<p>x = 1 to 8, labels y = 0, 0, 0, 1, 1, 0, 1, 1. The parent has 4 of each, so its Gini is 0.5.</p>
<p>Candidate thresholds are the midpoints between neighbouring values. For each: compute each side's Gini, then weight by size.</p>
<table><tr><th>Threshold</th><th>Left (no, yes)</th><th>Right (no, yes)</th><th>Gini L</th><th>Gini R</th><th>Weighted</th><th>Gain</th></tr>
<tr><td>1.5</td><td>1, 0</td><td>3, 4</td><td>0</td><td>0.490</td><td>0.429</td><td>0.071</td></tr>
<tr><td>2.5</td><td>2, 0</td><td>2, 4</td><td>0</td><td>0.444</td><td>0.333</td><td>0.167</td></tr>
<tr><td><b>3.5</b></td><td><b>3, 0</b></td><td><b>1, 4</b></td><td><b>0</b></td><td><b>0.320</b></td><td><b>0.200</b></td><td><b>0.300</b></td></tr>
<tr><td>4.5</td><td>3, 1</td><td>1, 3</td><td>0.375</td><td>0.375</td><td>0.375</td><td>0.125</td></tr>
<tr><td>5.5</td><td>3, 2</td><td>1, 2</td><td>0.480</td><td>0.444</td><td>0.467</td><td>0.033</td></tr>
<tr><td>6.5</td><td>4, 2</td><td>0, 2</td><td>0.444</td><td>0</td><td>0.333</td><td>0.167</td></tr>
<tr><td>7.5</td><td>4, 3</td><td>0, 1</td><td>0.490</td><td>0</td><td>0.429</td><td>0.071</td></tr></table>
<p>Weighted example for 3.5: (3/8)(0) + (5/8)(0.32) = 0.2. The winner is <b>x ≤ 3.5</b>.</p>
<h4>Now the same split with entropy</h4>
<p>The parent is 1 bit. The right side is 0.722 bits, weighted (5/8) × 0.722 = 0.451. So <b>information gain = 1 − 0.451 = 0.549 bits</b>.</p>
<p><b>Then what?</b> The left side is pure, so it becomes a leaf predicting 0. The right side (1 no, 4 yes) repeats the whole search. With many features, this table is built for every feature, and the best row overall wins.</p>
<p><b>Greedy:</b> the tree takes the best split right now and never reconsiders, so it may miss a better tree overall.</p>
""", practice=["Best Split Threshold", "Weighted Gini of a Given Split", "Impurity Decrease of the Best Split", "Gini vs Entropy"])


@LD
def split_table():
    x = np.arange(1, 9)
    y = np.array([0, 0, 0, 1, 1, 0, 1, 1])

    def gini_of(part):
        p = part.mean()
        return 1 - p ** 2 - (1 - p) ** 2

    table = {}
    for t in x[:-1] + 0.5:
        left, right = y[x <= t], y[x > t]
        weighted = (len(left) * gini_of(left) + len(right) * gini_of(right)) / len(y)
        table[float(t)] = round(0.5 - weighted, 3)
    best = max(table, key=table.get)


LESSON("Core", "Regression trees by hand", """
<p>The target is a number, so impurity becomes squared error around the mean. A leaf predicts its mean.</p>
<p>x = 1 to 6, y = 5, 6, 5.5, 12, 13, 12.5. The mean is 9, and the total squared error is <b>74.5</b>.</p>
<table><tr><th>Threshold</th><th>Left mean</th><th>Right mean</th><th>Total squared error after split</th></tr>
<tr><td>1.5</td><td>5</td><td>9.8</td><td>55.3</td></tr>
<tr><td>2.5</td><td>5.5</td><td>10.75</td><td>37.75</td></tr>
<tr><td><b>3.5</b></td><td><b>5.5</b></td><td><b>12.5</b></td><td><b>1.0</b></td></tr>
<tr><td>4.5</td><td>7.125</td><td>12.75</td><td>32.31</td></tr>
<tr><td>5.5</td><td>8.3</td><td>12.5</td><td>59.8</td></tr></table>
<p>The split at 3.5 removes almost all the error (from 74.5 down to 1.0). So: if x ≤ 3.5, predict 5.5; otherwise predict 12.5.</p>
<h4>Consequences</h4>
<ul><li>Predictions are a <b>staircase</b>: a tree can only output values it stored.</li>
<li>Asked about x = 100, it still says 12.5. <b>Trees can't extrapolate</b> a trend, so they struggle with forecasting growing values.</li>
<li>Outliers: squared error is affected by them; try <code>criterion="absolute_error"</code>.</li></ul>
""", practice=["Regression Stump", "Regression Tree Predictions"])


@LD
def no_extrapolation():
    x = np.arange(1, 21, dtype=float).reshape(-1, 1)
    y = 2 * x.ravel() + 1
    grid = np.linspace(0, 35, 300).reshape(-1, 1)
    tree = DecisionTreeRegressor(max_depth=4, random_state=0).fit(x, y)
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.scatter(x, y, s=10, label="training data")
    ax.plot(grid, tree.predict(grid), color="#b45309", label="tree")
    ax.plot(grid, 2 * grid + 1, "--", color="gray", label="true trend")
    ax.legend(fontsize=7)
    ax.set_title("Beyond the data, a tree goes flat", fontsize=9)


LESSON("Advanced", "Pruning: cost-complexity by hand", """
<p>Limits like <code>max_depth</code> stop growth early, and they may stop before a useful split. <b>Post-pruning</b> grows the full tree first, then removes branches that don't earn their place.</p>
<h4>The rule</h4>
<p style="text-align:center"><b>cost = impurity of the leaves + α × number of leaves</b></p>
<h4>Worked example</h4>
<table><tr><th>Option</th><th>Total impurity</th><th>Leaves</th><th>Cost with α = 0.01</th><th>Cost with α = 0.05</th></tr>
<tr><td>Keep the branch</td><td>0.10</td><td>4</td><td>0.14</td><td><b>0.30</b></td></tr>
<tr><td>Prune the branch</td><td>0.15</td><td>2</td><td>0.17</td><td><b>0.25</b></td></tr></table>
<p>At α = 0.01 keeping wins (0.14 is lower). At α = 0.05 pruning wins (0.25 is lower). A branch survives only if its drop in impurity pays for its extra leaves.</p>
<p>Larger α means a smaller tree. Choose α with cross-validation: <code>cost_complexity_pruning_path</code> lists the useful values. The demo shows it: training accuracy falls as the tree shrinks, while test accuracy first improves, because the removed branches were mostly fitting noise. Prune too far and test accuracy falls as well.</p>
""", practice=["Minimum Samples per Leaf", "Training Accuracy by Depth", "Best-First Growth With a Leaf Budget"])


@LD
def pruning_curve():
    rng = np.random.default_rng(0)
    X = rng.uniform(0, 10, (400, 2))
    y = ((X[:, 0] - 5) ** 2 + (X[:, 1] - 5) ** 2 < 9).astype(int)
    flip = rng.uniform(size=400) < 0.15
    y = np.where(flip, 1 - y, y)
    X_train, X_test, y_train, y_test = X[:250], X[250:], y[:250], y[250:]
    path = DecisionTreeClassifier(random_state=0).cost_complexity_pruning_path(X_train, y_train)
    alphas = path.ccp_alphas
    trees = [DecisionTreeClassifier(ccp_alpha=a, random_state=0).fit(X_train, y_train) for a in alphas]
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(alphas, [t.score(X_train, y_train) for t in trees], label="train")
    ax.plot(alphas, [t.score(X_test, y_test) for t in trees], label="test")
    ax.set_xlabel("ccp_alpha (larger = smaller tree)")
    ax.set_ylabel("accuracy")
    ax.legend(fontsize=8)


LESSON("Advanced", "Importance, instability and when to use trees", """
<h4>Two kinds of feature importance</h4>
<table><tr><th></th><th>Impurity-based</th><th>Permutation</th></tr>
<tr><td>How</td><td>adds up each feature's impurity decreases</td><td>shuffles one column, measures how much the score drops</td></tr>
<tr><td>Speed</td><td>instant</td><td>needs repeated scoring</td></tr>
<tr><td>Weakness</td><td>favours features with many distinct values; reflects training data</td><td>splits credit between correlated features</td></tr></table>
<p>The demo adds a random ID column. Impurity importance gives this useless column real credit. Permutation importance on test data shows it's worth nothing.</p>
<h4>Instability</h4>
<p>A small change in the data can change the first split, and then every split below it. That's high variance, and exactly why forests average many trees.</p>
<h4>Should you use a single tree?</h4>
<ul><li><b>Yes</b> when a human must follow the rules: credit policies, triage, explaining patterns.</li>
<li><b>Usually no</b> for best accuracy: use a forest or boosting.</li></ul>
""", practice=["Feature Importances", "Which Leaf Does Each Row Reach?"])


@LD
def fake_feature():
    from sklearn.inspection import permutation_importance
    rng = np.random.default_rng(0)
    signal = rng.normal(size=400)
    row_id = rng.permutation(400).astype(float)
    y = (signal + rng.normal(0, 0.7, 400) > 0).astype(int)
    X = np.column_stack([signal, row_id])
    tree = DecisionTreeClassifier(random_state=0).fit(X[:280], y[:280])
    perm = permutation_importance(tree, X[280:], y[280:], n_repeats=10, random_state=0)
    fig, axes = plt.subplots(1, 2, figsize=(7, 2.5))
    axes[0].bar(["signal", "random ID"], tree.feature_importances_)
    axes[0].set_title("impurity-based: ID gets credit", fontsize=9)
    axes[1].bar(["signal", "random ID"], perm.importances_mean, color="#b45309")
    axes[1].set_title("permutation on test: ID is useless", fontsize=9)
    fig.tight_layout()
