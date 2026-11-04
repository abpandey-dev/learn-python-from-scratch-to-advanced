from lib import *
import math
import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


TOPIC(
    id="trees", title="Decision Trees", glyph="if / else",
    blurb="Models that ask a sequence of yes/no questions: impurity (Gini, entropy, MSE), finding the best split, growing and stopping, predictions, depth and leaves, feature importance, and overfitting.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">tree = DecisionTreeClassifier(criterion="gini" | "entropy", max_depth=3,
                              min_samples_leaf=5, random_state=0).fit(X, y)
tree.predict(X), tree.predict_proba(X)
tree.get_depth(), tree.get_n_leaves(), tree.feature_importances_
tree.tree_.feature[0], tree.tree_.threshold[0]       # the root question
from sklearn.tree import plot_tree, export_text
DecisionTreeRegressor(max_depth=3)                   # leaves predict the mean</code></pre>
<p>Gini = 1 − Σpₖ², entropy = −Σpₖ log₂ pₖ. Split thresholds are midpoints between neighbouring values; x ≤ threshold goes left.</p>
""")


def impurity(labels, criterion="gini"):
    n = len(labels)
    shares = [labels.count(c) / n for c in set(labels)]
    if criterion == "gini":
        return 1 - sum(p * p for p in shares)
    if criterion == "entropy":
        return -sum(p * math.log2(p) for p in shares if p > 0)
    mean = sum(labels) / n
    return sum((v - mean) ** 2 for v in labels) / n


def best_split(X, y, criterion="gini", min_leaf=1):
    """Try every feature and every midpoint threshold; return (gain, feature, threshold)."""
    n, parent = len(y), impurity(y, criterion)
    best = (0.0, None, None)
    for f in range(len(X[0])):
        values = sorted(set(row[f] for row in X))
        for lo, hi in zip(values, values[1:]):
            t = (lo + hi) / 2
            left = [label for row, label in zip(X, y) if row[f] <= t]
            right = [label for row, label in zip(X, y) if row[f] > t]
            if len(left) < min_leaf or len(right) < min_leaf:
                continue
            child = (len(left) * impurity(left, criterion) + len(right) * impurity(right, criterion)) / n
            if parent - child > best[0] + 1e-12:
                best = (parent - child, f, t)
    return best


def grow(X, y, depth=0, max_depth=None, criterion="gini"):
    """A node is either {'leaf': labels} or {'f', 't', 'left', 'right', 'n', 'imp'}."""
    gain, f, t = best_split(X, y, criterion)
    if f is None or (max_depth is not None and depth >= max_depth):
        return {"leaf": y}
    li = [i for i, row in enumerate(X) if row[f] <= t]
    ri = [i for i, row in enumerate(X) if row[f] > t]
    return {"f": f, "t": t, "n": len(y), "imp": impurity(y, criterion),
            "left": grow([X[i] for i in li], [y[i] for i in li], depth + 1, max_depth, criterion),
            "right": grow([X[i] for i in ri], [y[i] for i in ri], depth + 1, max_depth, criterion)}


def leaf_for(node, row):
    while "leaf" not in node:
        node = node["left"] if row[node["f"]] <= node["t"] else node["right"]
    return node["leaf"]


def majority(labels):
    return max(sorted(set(labels)), key=labels.count)


X1 = [[1], [2], [3], [4], [5], [6], [7], [8]]
Y1 = [0, 0, 0, 1, 1, 0, 1, 1]
X2 = [[2, 3], [1, 1], [4, 5], [6, 2], [7, 6], [3, 7], [8, 4], [5, 1]]
Y2 = [0, 0, 1, 0, 1, 1, 1, 0]
X3 = [[1, 1], [2, 5], [3, 2], [4, 6], [5, 3], [6, 7], [7, 1], [8, 4], [2, 8], [7, 8]]
Y3 = [0, 1, 0, 1, 0, 1, 1, 1, 0, 0]
XR = [[1], [2], [3], [4], [5], [6]]
YR = [5.0, 6.0, 5.5, 12.0, 13.0, 12.5]


Q(None, "Gini Impurity of a Node", "Easy", "How mixed are the labels?",
  "Return 1 − Σ (share of each class)², rounded to 4 decimals.",
  [((Y1,), 0.5), (([1, 1, 1],), 0.0), ((["a", "b", "c", "c"],), 0.625)],
  ("Count each class, apply the formula.", "O(n)", "O(k)"),
  ("Fit a tree; the root node's <code>tree_.impurity[0]</code> is the Gini of all the labels.", "O(n log n)", "O(n)"))


@B
def gini(y):
    return round(impurity(y, "gini"), 4)


@O
def gini(y):
    tree = DecisionTreeClassifier(max_depth=1, random_state=0).fit(np.zeros((len(y), 1)), y)
    return round(tree.tree_.impurity[0], 4)


Q(None, "Entropy of a Node", "Easy", "Impurity in bits",
  "Return −Σ p log₂ p over the classes, rounded to 4 decimals.",
  [((Y1,), 1.0), ((["a", "b", "c", "c"],), 1.5)],
  ("Count each class, apply the formula.", "O(n)", "O(k)"),
  ("Root impurity of a tree with <code>criterion='entropy'</code>.", "O(n log n)", "O(n)"))


@B
def entropy(y):
    return round(impurity(y, "entropy"), 4)


@O
def entropy(y):
    tree = DecisionTreeClassifier(criterion="entropy", max_depth=1, random_state=0).fit(np.zeros((len(y), 1)), y)
    return round(tree.tree_.impurity[0], 4)


Q(None, "Weighted Gini of a Given Split", "Easy", "Scoring one candidate question",
  "Split one feature at threshold t (x ≤ t goes left). Return the size-weighted Gini of the two sides, rounded to 4 decimals.",
  [((X1, Y1, 3.5), 0.2), ((X1, Y1, 5.5), 0.4667)],
  ("Divide the labels, compute each side's Gini, weight by size.", "O(n)", "O(n)"),
  ("Vectorised with NumPy masks and class counts (<code>np.unique</code>).", "O(n)", "O(n)"),
  names=["X", "y", "t"])


@B
def split_gini(X, y, t):
    left = [label for row, label in zip(X, y) if row[0] <= t]
    right = [label for row, label in zip(X, y) if row[0] > t]
    return round((len(left) * impurity(left) + len(right) * impurity(right)) / len(y), 4)


@O
def split_gini(X, y, t):
    x, labels = np.array(X)[:, 0], np.array(y)

    def g(part):
        _, counts = np.unique(part, return_counts=True)
        return 1 - ((counts / counts.sum()) ** 2).sum()

    mask = x <= t
    return round((mask.sum() * g(labels[mask]) + (~mask).sum() * g(labels[~mask])) / len(labels), 4)


Q(None, "Best Split Threshold", "Medium", "The root question",
  "One feature. Return the threshold (midpoint between neighbouring values) that gives the largest drop in Gini.",
  [((X1, Y1), 3.5), (([[1], [3], [4], [7], [9]], ["a", "a", "b", "b", "b"]), 3.5)],
  ("Try every midpoint; compute the size-weighted Gini of both sides; keep the best.", "O(n²)", "O(n)"),
  ("A depth-1 tree (a <b>stump</b>): <code>tree_.threshold[0]</code>.", "O(n log n)", "O(n)"),
  names=["X", "y"])


@B
def best_threshold(X, y):
    return best_split(X, y)[2]


@O
def best_threshold(X, y):
    return DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_.threshold[0]


Q(None, "Impurity Decrease of the Best Split", "Medium", "Information gain (Gini)",
  "Return parent Gini − weighted child Gini for the best split, rounded to 4 decimals.",
  [((X1, Y1), 0.3), ((X2, Y2), 0.5)],
  ("The best_split search returns the gain directly.", "O(d·n²)", "O(n)"),
  ("From a stump: root impurity minus the size-weighted impurity of its two children.", "O(d·n log n)", "O(n)"),
  names=["X", "y"])


@B
def split_gain(X, y):
    return round(best_split(X, y)[0], 4)


@O
def split_gain(X, y):
    t = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_
    n = t.weighted_n_node_samples
    return round(t.impurity[0] - (n[1] * t.impurity[1] + n[2] * t.impurity[2]) / n[0], 4)


Q(None, "Which Feature Splits Best?", "Medium", "Choosing the question",
  "Two features. Return (feature index, threshold) of the root split.",
  [((X2, Y2), (1, 3.5))],
  ("Search both features and all midpoints.", "O(d·n²)", "O(n)"),
  ("Stump: <code>tree_.feature[0]</code> and <code>tree_.threshold[0]</code>.", "O(d·n log n)", "O(n)"),
  names=["X", "y"])


@B
def root_question(X, y):
    gain, f, t = best_split(X, y)
    return (f, t)


@O
def root_question(X, y):
    t = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_
    return (int(t.feature[0]), float(t.threshold[0]))


Q(None, "Predict With a Stump", "Easy", "One question, two answers",
  "Train a depth-1 tree on (X, y) and predict the class of each query row.",
  [((X2, Y2, [[1, 9], [7, 1], [5, 5]]), [1, 0, 1])],
  ("Find the root split; each side predicts its majority class.", "O(d·n²)", "O(n)"),
  ("<code>DecisionTreeClassifier(max_depth=1).predict</code>.", "O(d·n log n)", "O(n)"),
  names=["X", "y", "queries"])


@B
def stump_predict(X, y, queries):
    tree = grow(X, y, max_depth=1)
    return [majority(leaf_for(tree, q)) for q in queries]


@O
def stump_predict(X, y, queries):
    return DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).predict(queries)


Q(None, "Leaf Probabilities", "Easy", "Class shares inside a leaf",
  "Train a depth-1 tree and return P(class) for the query (sorted classes), rounded to 4 decimals.",
  [((X1, Y1, [7.5]), [0.2, 0.8]), ((X1, Y1, [2]), [1.0, 0.0])],
  ("Find the query's leaf; class shares of the training labels there.", "O(n²)", "O(n)"),
  ("<code>predict_proba</code>.", "O(n log n)", "O(n)"),
  names=["X", "y", "q"])


@B
def leaf_proba(X, y, q):
    labels = leaf_for(grow(X, y, max_depth=1), q)
    return [round(labels.count(c) / len(labels), 4) for c in sorted(set(y))]


@O
def leaf_proba(X, y, q):
    return DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).predict_proba([q])[0].round(4)


Q(None, "A Depth-2 Tree", "Hard", "Growing recursively",
  "Train a tree with max_depth = 2 and predict the class of each query row.",
  [((X3, Y3, [[1, 9], [7, 1], [5, 5], [2, 2], [8, 8]]), [0, 0, 1, 0, 0])],
  ("Recursive builder: best split, then the same on each side, stopping at depth 2 or pure nodes.", "O(d·n² · nodes)", "O(n)"),
  ("<code>DecisionTreeClassifier(max_depth=2)</code>.", "O(d·n log n · depth)", "O(n)"),
  names=["X", "y", "queries"])


@B
def depth2_predict(X, y, queries):
    tree = grow(X, y, max_depth=2)
    return [majority(leaf_for(tree, q)) for q in queries]


@O
def depth2_predict(X, y, queries):
    return DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y).predict(queries)


Q(None, "How Deep Does It Grow?", "Medium", "Unlimited depth",
  "Grow a tree with no depth limit until every leaf is pure. Return (depth, number of leaves).",
  [((X1, Y1), (3, 4)), ((X3, Y3), (3, 4))],
  ("Recursive builder, then count levels and leaves.", "O(d·n² · nodes)", "O(n)"),
  ("<code>get_depth()</code> and <code>get_n_leaves()</code>.", "O(d·n log n · depth)", "O(n)"),
  names=["X", "y"])


@B
def size_of_tree(X, y):
    def depth(node):
        return 0 if "leaf" in node else 1 + max(depth(node["left"]), depth(node["right"]))

    def leaves(node):
        return 1 if "leaf" in node else leaves(node["left"]) + leaves(node["right"])

    tree = grow(X, y)
    return (depth(tree), leaves(tree))


@O
def size_of_tree(X, y):
    tree = DecisionTreeClassifier(random_state=0).fit(X, y)
    return (tree.get_depth(), tree.get_n_leaves())


Q(None, "Best-First Growth With a Leaf Budget", "Hard", "max_leaf_nodes",
  "Grow a tree best-first: repeatedly split whichever leaf gives the largest size-weighted impurity decrease, until there are max_leaves leaves. Return the predictions for the queries.",
  [((X3, Y3, 3, [[1, 9], [7, 1], [5, 5], [2, 2], [8, 8]]), [0, 0, 1, 0, 0])],
  ("Keep a list of leaves; each round, find each leaf's best split, apply the one with the biggest weighted gain.", "O(leaves·d·n²)", "O(n)"),
  ("<code>DecisionTreeClassifier(max_leaf_nodes=…)</code> grows best-first.", "O(leaves·d·n log n)", "O(n)"),
  names=["X", "y", "max_leaves", "queries"])


@B
def leaf_budget(X, y, max_leaves, queries):
    leaves = [list(range(len(X)))]
    rules = [[]]
    while len(leaves) < max_leaves:
        best = None
        for i, idx in enumerate(leaves):
            gain, f, t = best_split([X[j] for j in idx], [y[j] for j in idx])
            if f is not None and (best is None or gain * len(idx) > best[0]):
                best = (gain * len(idx), i, f, t)
        if best is None:
            break
        _, i, f, t = best
        idx, rule = leaves.pop(i), rules.pop(i)
        leaves += [[j for j in idx if X[j][f] <= t], [j for j in idx if X[j][f] > t]]
        rules += [rule + [(f, t, True)], rule + [(f, t, False)]]
    out = []
    for q in queries:
        for idx, rule in zip(leaves, rules):
            if all((q[f] <= t) == left for f, t, left in rule):
                out.append(majority([y[j] for j in idx]))
    return out


@O
def leaf_budget(X, y, max_leaves, queries):
    return DecisionTreeClassifier(max_leaf_nodes=max_leaves, random_state=0).fit(X, y).predict(queries)


Q(None, "Training Accuracy by Depth", "Medium", "Deeper = memorises more",
  "Return the training accuracy of trees with max_depth = 1, 2, 3, rounded to 4 decimals.",
  [((X3, Y3), [0.7, 0.9, 1.0])],
  ("Build each tree from scratch and score it on its own training data.", "O(depth·d·n²)", "O(n)"),
  ("Fit three <code>DecisionTreeClassifier</code>s and call <code>score</code>.", "O(depth·d·n log n)", "O(n)"),
  names=["X", "y"])


@B
def accuracy_by_depth(X, y):
    out = []
    for d in (1, 2, 3):
        tree = grow(X, y, max_depth=d)
        correct = sum(majority(leaf_for(tree, row)) == label for row, label in zip(X, y))
        out.append(round(correct / len(y), 4))
    return out


@O
def accuracy_by_depth(X, y):
    return [round(DecisionTreeClassifier(max_depth=d, random_state=0).fit(X, y).score(X, y), 4) for d in (1, 2, 3)]


Q(None, "Feature Importances", "Hard", "Mean decrease in impurity",
  "For a depth-2 tree, return each feature's total (size-weighted) impurity decrease, normalised to sum to 1, rounded to 4 decimals.",
  [((X3, Y3), [0.0, 1.0])],
  ("Walk the grown tree: each split adds (n_node/N)·(impurity − weighted child impurity) to its feature.", "O(nodes)", "O(d)"),
  ("<code>feature_importances_</code>.", "O(nodes)", "O(d)"),
  names=["X", "y"])


@B
def importances(X, y):
    tree = grow(X, y, max_depth=2)
    total = [0.0] * len(X[0])

    def walk(node):
        if "leaf" in node:
            return
        nl, nr = len(gather(node["left"])), len(gather(node["right"]))
        child = (nl * node_imp(node["left"]) + nr * node_imp(node["right"])) / node["n"]
        total[node["f"]] += node["n"] / len(y) * (node["imp"] - child)
        walk(node["left"])
        walk(node["right"])

    def gather(node):
        return node["leaf"] if "leaf" in node else gather(node["left"]) + gather(node["right"])

    def node_imp(node):
        return impurity(gather(node))

    walk(tree)
    s = sum(total)
    return [round(v / s, 4) for v in total]


@O
def importances(X, y):
    return DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y).feature_importances_.round(4)


Q(None, "Minimum Samples per Leaf", "Medium", "A brake on overfitting",
  "Find the best stump threshold when each side must keep at least min_leaf samples.",
  [((X1, Y1, 1), 3.5), ((X1, Y1, 4), 4.5)],
  ("Same search, skipping splits that leave a side too small.", "O(n²)", "O(n)"),
  ("<code>DecisionTreeClassifier(max_depth=1, min_samples_leaf=…)</code>.", "O(n log n)", "O(n)"),
  names=["X", "y", "min_leaf"])


@B
def constrained_threshold(X, y, min_leaf):
    return best_split(X, y, min_leaf=min_leaf)[2]


@O
def constrained_threshold(X, y, min_leaf):
    tree = DecisionTreeClassifier(max_depth=1, min_samples_leaf=min_leaf, random_state=0).fit(X, y)
    return tree.tree_.threshold[0]


Q(None, "Gini vs Entropy", "Medium", "Do they pick the same question?",
  "Return (best threshold by Gini, best threshold by entropy) for a single feature.",
  [((X1, Y1), (3.5, 3.5)), (([[1], [2], [3], [4], [5], [6]], ["a", "a", "b", "c", "c", "c"]), (3.5, 3.5))],
  ("Run the split search with each criterion.", "O(n²)", "O(n)"),
  ("Two stumps with different <code>criterion</code>.", "O(n log n)", "O(n)"),
  names=["X", "y"])


@B
def gini_vs_entropy(X, y):
    return (best_split(X, y, "gini")[2], best_split(X, y, "entropy")[2])


@O
def gini_vs_entropy(X, y):
    g = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_.threshold[0]
    e = DecisionTreeClassifier(criterion="entropy", max_depth=1, random_state=0).fit(X, y).tree_.threshold[0]
    return (float(g), float(e))


Q(None, "Which Leaf Does Each Row Reach?", "Easy", "apply()",
  "For a depth-1 tree, return the node id each query lands in (left leaf = 1, right leaf = 2).",
  [((X1, Y1, [[1], [5], [8]]), [1, 2, 2])],
  ("Compare with the root threshold.", "O(n²)", "O(1)"),
  ("<code>tree.apply(queries)</code>.", "O(n log n)", "O(m)"),
  names=["X", "y", "queries"])


@B
def leaf_ids(X, y, queries):
    gain, f, t = best_split(X, y)
    return [1 if q[f] <= t else 2 for q in queries]


@O
def leaf_ids(X, y, queries):
    return DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).apply(queries)


Q(None, "Samples in Each Leaf", "Easy", "How the data is divided",
  "For a depth-1 tree, return (samples in the left leaf, samples in the right leaf).",
  [((X1, Y1), (3, 5)), ((X2, Y2), (4, 4))],
  ("Count rows on each side of the root threshold.", "O(d·n²)", "O(1)"),
  ("<code>tree_.n_node_samples[1:]</code>.", "O(d·n log n)", "O(1)"),
  names=["X", "y"])


@B
def leaf_sizes(X, y):
    gain, f, t = best_split(X, y)
    left = sum(1 for row in X if row[f] <= t)
    return (left, len(X) - left)


@O
def leaf_sizes(X, y):
    t = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_
    return (int(t.n_node_samples[1]), int(t.n_node_samples[2]))


Q(None, "Regression Stump", "Medium", "Split to reduce squared error",
  "One feature, numeric target. Return (threshold, left-leaf mean, right-leaf mean) of a depth-1 regression tree, rounded to 4 decimals.",
  [((XR, YR), (3.5, 5.5, 12.5))],
  ("Same split search with variance (MSE) as the impurity; leaves predict their mean.", "O(n²)", "O(n)"),
  ("<code>DecisionTreeRegressor(max_depth=1)</code>.", "O(n log n)", "O(n)"),
  names=["X", "y"])


@B
def regression_stump(X, y):
    gain, f, t = best_split(X, y, "mse")
    left = [v for row, v in zip(X, y) if row[f] <= t]
    right = [v for row, v in zip(X, y) if row[f] > t]
    return (t, round(sum(left) / len(left), 4), round(sum(right) / len(right), 4))


@O
def regression_stump(X, y):
    tree = DecisionTreeRegressor(max_depth=1, random_state=0).fit(X, y)
    t = tree.tree_
    return (float(t.threshold[0]), round(t.value[1][0][0], 4), round(t.value[2][0][0], 4))


Q(None, "Regression Tree Predictions", "Medium", "Step-shaped curves",
  "Train a regression tree with max_depth = 2 and predict each query, rounded to 4 decimals.",
  [((XR, YR, [[0], [2.5], [3.7], [6.5]]), [5.0, 5.75, 12.0, 12.75])],
  ("Recursive builder with MSE impurity; each leaf predicts the mean of its targets.", "O(n² · nodes)", "O(n)"),
  ("<code>DecisionTreeRegressor(max_depth=2).predict</code>.", "O(n log n · depth)", "O(n)"),
  names=["X", "y", "queries"])


@B
def regression_tree(X, y, queries):
    tree = grow(X, y, max_depth=2, criterion="mse")
    out = []
    for q in queries:
        values = leaf_for(tree, q)
        out.append(round(sum(values) / len(values), 4))
    return out


@O
def regression_tree(X, y, queries):
    return DecisionTreeRegressor(max_depth=2, random_state=0).fit(X, y).predict(queries).round(4)


Q(None, "Majority Class at the Root", "Easy", "A tree with no questions",
  "A tree of depth 0 would predict the most common class (smallest on ties). Return it, and the training accuracy of that guess (rounded to 4 decimals).",
  [((Y1,), (0, 0.5)), ((["b", "a", "b", "c"],), ('b', 0.5))],
  ("Count classes; the winner's share is the accuracy.", "O(n)", "O(k)"),
  ("The class with the largest share in the root's <code>tree_.value</code>.", "O(n log n)", "O(n)"))


@B
def root_majority(y):
    winner = majority(y)
    return (winner, round(y.count(winner) / len(y), 4))


@O
def root_majority(y):
    tree = DecisionTreeClassifier(max_depth=1, random_state=0).fit(np.zeros((len(y), 1)), y)
    shares = tree.tree_.value[0][0] / tree.tree_.value[0][0].sum()
    i = int(np.argmax(shares))
    return (tree.classes_[i].item(), round(shares[i], 4))
