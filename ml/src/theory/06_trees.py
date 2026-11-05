from lib import *

THEORY("How trees are built (CART)", """
<ol>
<li>At a node with samples S, for every feature j and threshold t (midpoints of sorted unique values), split S into S_L = {x_j ≤ t} and S_R.</li>
<li>Score = I(S) − (|S_L|/|S|)·I(S_L) − (|S_R|/|S|)·I(S_R), with impurity I = Gini, entropy or MSE.</li>
<li>Choose the best (j, t) — a <b>greedy</b>, locally optimal choice (finding the globally optimal tree is NP-hard).</li>
<li>Recurse until a stopping rule: pure node, max_depth, min_samples_split/leaf, no impurity decrease, max_leaf_nodes (best-first).</li>
</ol>
<p>Cost of training ≈ O(d · n log n · depth). sklearn implements CART (binary splits); ID3/C4.5 use entropy and multi-way splits.</p>
""")

THEORY("Impurity measures", """
<table>
<tr><th>Measure</th><th>Formula</th><th>Max (2 classes)</th></tr>
<tr><td>Gini</td><td>1 − Σ pₖ²</td><td>0.5</td></tr>
<tr><td>Entropy</td><td>−Σ pₖ log₂ pₖ</td><td>1</td></tr>
<tr><td>Misclassification</td><td>1 − max pₖ</td><td>0.5 (not used for growing: not sensitive enough)</td></tr>
<tr><td>MSE / variance</td><td>(1/n)Σ(y − ȳ)²</td><td>regression</td></tr>
<tr><td>MAE, Poisson, Friedman MSE</td><td>regression variants</td><td></td></tr>
</table>
""")

THEORY("Strengths, weaknesses, regularisation", """
<table>
<tr><th>Strengths</th><th>Weaknesses</th></tr>
<tr><td>interpretable rules; no scaling; mixed types; non-linear; interactions captured automatically; fast prediction</td><td>high variance / unstable; overfits when deep; axis-aligned steps; can't extrapolate; greedy splits; biased importances</td></tr>
</table>
<p>Pre-pruning: max_depth, min_samples_leaf, min_samples_split, max_leaf_nodes, min_impurity_decrease. Post-pruning: minimal cost-complexity pruning, R_α(T) = R(T) + α·|leaves|, choose α by CV (<code>cost_complexity_pruning_path</code>).</p>
""")

FAQ("How does a decision tree choose where to split?", "<p>It evaluates every feature and threshold and picks the split that reduces impurity (Gini, entropy or MSE) the most, weighted by the size of each child.</p>")
FAQ("Gini vs entropy?", "<p>Both measure node impurity and usually produce very similar trees. Gini is slightly cheaper (no logarithm); entropy ties to information gain.</p>")
FAQ("Why do decision trees overfit and how do you prevent it?", "<p>Grown fully, they keep splitting until each leaf is pure, fitting noise. Limit depth, require minimum samples per leaf, prune with ccp_alpha, or use ensembles.</p>")
FAQ("Do trees need feature scaling?", "<p>No. Splits compare a feature with a threshold, which is unaffected by monotonic rescaling.</p>")
FAQ("What is feature importance in a tree?", "<p>The total impurity decrease contributed by splits on each feature, weighted by the fraction of samples reaching those nodes and normalised. Prefer permutation importance for reliable conclusions.</p>")
FAQ("Can a regression tree predict values outside the training range?", "<p>No. Each leaf predicts an average of training targets, so predictions are bounded by the training data's range.</p>")

THEORY("Practical tuning guide", """
<table>
<tr><th>Symptom</th><th>Change</th></tr>
<tr><td>Train accuracy near 100%, test much lower</td><td>lower max_depth; raise min_samples_leaf; raise ccp_alpha</td></tr>
<tr><td>Both low</td><td>allow more depth; add better features; switch to boosting</td></tr>
<tr><td>Rules are too hard to read</td><td>max_depth of 3–5, or max_leaf_nodes</td></tr>
<tr><td>Results change with small data changes</td><td>use a random forest</td></tr>
<tr><td>Imbalanced classes</td><td>class_weight="balanced"</td></tr>
</table>
""")
