from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier

X = np.array([[1, 2], [2, 1], [3, 3], [4, 2], [5, 5], [6, 4], [2, 3], [5, 2], [7, 6], [3, 6], [6, 1], [1, 5]], dtype=float)
Y = np.array([0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1])

LESSON("Basics", "The wisdom of crowds", """
<p>One deep decision tree overfits: change a few rows and it changes completely (high <b>variance</b>). Average many different models and their individual mistakes cancel out. That's an <b>ensemble</b>.</p>
<ul>
<li><b>Voting</b>: train different models (logistic regression, a tree, k-NN) and let them vote (<b>hard</b>) or average their probabilities (<b>soft</b>).</li>
<li>Averaging k models with error variance σ² and correlation ρ gives variance ρσ² + (1 − ρ)σ²/k: it only helps if the models are <b>different</b> (low ρ).</li>
</ul>
""", practice=["Hard Voting by Hand", "Soft Voting", "Why Averaging Helps"])


@LD
def variance_curve():
    k = np.arange(1, 51)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    for rho in [0.0, 0.3, 0.7]:
        ax.plot(k, rho + (1 - rho) / k, label=f"ρ = {rho}")
    ax.set_xlabel("number of models averaged")
    ax.set_ylabel("variance of the average (σ² = 1)")
    ax.legend(fontsize=8)


LESSON("Core", "Bagging and random forests", """
<p><b>Bagging</b> (bootstrap aggregating): train each model on a <b>bootstrap sample</b> — n rows drawn <i>with replacement</i>, so some rows repeat and about 37% are left out. Average (regression) or vote (classification).</p>
<p>A <b>random forest</b> = bagging of deep trees + at every split, only a <b>random subset of features</b> is considered (√d for classification). This decorrelates the trees, so averaging removes much more variance.</p>
<ul>
<li>The left-out rows are free validation data: the <b>out-of-bag (OOB) score</b>.</li>
<li>Few hyper-parameters, robust defaults, no scaling, gives feature importances — a superb first model for tabular data.</li>
</ul>
""", practice=["A Bootstrap Sample", "Out-of-Bag Rows", "Chance a Row Is Left Out", "Forest Probability = Average of Its Trees", "Count the Trees' Votes", "Forest Feature Importances", "Bagging = Average of Trees", "Features Tried at Each Split"])


@LD
def tree_vs_forest():
    xx, yy = np.meshgrid(np.linspace(0, 8, 150), np.linspace(0, 7, 150))
    grid = np.column_stack([xx.ravel(), yy.ravel()])
    models = [("one deep tree", DecisionTreeClassifier(random_state=0)),
              ("forest of 200 trees", RandomForestClassifier(n_estimators=200, random_state=0))]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, (name, model) in zip(axes, models):
        prob = model.fit(X, Y).predict_proba(grid)[:, 1].reshape(xx.shape)
        ax.contourf(xx, yy, prob, levels=10, cmap="coolwarm", alpha=0.5)
        ax.scatter(X[:, 0], X[:, 1], c=Y, cmap="coolwarm", edgecolor="black")
        ax.set_title(name, fontsize=9)
    fig.tight_layout()


LESSON("Core", "Gradient boosting: fixing mistakes one tree at a time", """
<p><b>Boosting</b> builds the ensemble <b>sequentially</b>. Gradient boosting for regression:</p>
<ol>
<li>Start with a constant prediction: the mean of y.</li>
<li>Compute the <b>residuals</b> (what's still wrong).</li>
<li>Fit a small tree to the residuals.</li>
<li>Add it, scaled down by the <b>learning rate</b>: prediction += lr × tree.</li>
<li>Repeat for n_estimators rounds.</li>
</ol>
<p>Residuals are the negative gradient of squared error — swap in other losses' gradients for classification or ranking. Small learning rate + many trees + shallow trees (depth 3–8) generalises best; stop early when validation error rises. XGBoost, LightGBM, CatBoost and sklearn's HistGradientBoosting are fast versions — the usual winners on tabular data.</p>
""", practice=["Boosting Starts From the Mean", "The First Tree Fits the Residuals", "Gradient Boosting From Scratch", "Watching Boosting Improve", "Learning Rate vs Training Error"])


@LD
def boosting_stages():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float).reshape(-1, 1)
    y = np.array([3.0, 4.5, 4.0, 7.5, 8.0, 7.0, 11.5, 12.0])
    grid = np.linspace(0, 9, 300).reshape(-1, 1)
    gb = GradientBoostingRegressor(n_estimators=20, learning_rate=0.5, max_depth=1, random_state=0).fit(x, y)
    stages = list(gb.staged_predict(grid))
    fig, ax = plt.subplots(figsize=(4.8, 3))
    ax.scatter(x, y, zorder=3)
    for i in [0, 2, 19]:
        ax.plot(grid, stages[i], label=f"after {i + 1} trees")
    ax.legend(fontsize=7)


LESSON("Advanced", "AdaBoost and stacking", """
<p><b>AdaBoost</b> (the original boosting): train a weak learner (a stump), measure its <b>weighted error</b>, give it a say α = ln((1 − err)/err), then <b>increase the weights of the rows it got wrong</b> so the next learner focuses on them. The final prediction is an α-weighted vote.</p>
<p><b>Stacking</b>: train several different models, then train a <b>meta-model</b> on their (out-of-fold) predictions to learn how much to trust each.</p>
<table><tr><th></th><th>Bagging / forests</th><th>Boosting</th></tr>
<tr><td>Builds models</td><td>in parallel, independently</td><td>in sequence, each fixing the last</td></tr>
<tr><td>Mainly reduces</td><td>variance</td><td>bias (and variance with shrinkage)</td></tr>
<tr><td>Base models</td><td>deep trees</td><td>shallow trees</td></tr>
<tr><td>Overfitting risk</td><td>low</td><td>higher — tune lr, depth, rounds</td></tr></table>
""", practice=["Weighted Error of a Weak Learner", "AdaBoost: How Much Say Does a Model Get?", "AdaBoost: Reweight the Mistakes", "Stacking: Learn How to Blend"])


@LD
def adaboost_weights():
    y = np.array([1, 0, 1, 1, 0, 1, 0, 0])
    pred = np.array([1, 1, 1, 0, 0, 1, 0, 1])
    w = np.full(len(y), 1 / len(y))
    err = w[y != pred].sum()
    alpha = math.log((1 - err) / err)
    new_w = w * np.where(y != pred, math.exp(alpha), 1.0)
    new_w = new_w / new_w.sum()
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.bar(np.arange(len(y)) - 0.2, w, width=0.4, label="before")
    ax.bar(np.arange(len(y)) + 0.2, new_w, width=0.4, label="after (mistakes heavier)")
    ax.set_xlabel("row")
    ax.legend(fontsize=7)


LESSON("Basics", "Why voting works, with numbers", """
<p>Suppose several models are each right 70% of the time and <b>make independent mistakes</b>. A majority vote is right when more than half are right.</p>
<h4>Worked example: three models</h4>
<ul><li>All three right: 0.7³ = 0.343</li>
<li>Exactly two right: 3 × 0.7² × 0.3 = 0.441</li>
<li>Majority right: 0.343 + 0.441 = <b>0.784</b></li></ul>
<table><tr><th>Models</th><th>1</th><th>3</th><th>5</th><th>11</th></tr>
<tr><th>Vote accuracy</th><td>0.700</td><td>0.784</td><td>0.837</td><td>0.922</td></tr></table>
<p><b>The catch is "independent".</b> If all models make the same mistakes, voting changes nothing. So ensembles need <b>diversity</b>: different data samples, features or algorithms. And each model must beat chance, since voting among models worse than 50% makes things worse.</p>
<p><b>Hard or soft voting?</b> Hard counts class votes. Soft averages probabilities, which respects each model's confidence and usually works better when probabilities are reasonable.</p>
""", practice=["Hard Voting by Hand", "Soft Voting", "Why Averaging Helps"])


@LD
def vote_math():
    def vote_accuracy(n, p=0.7):
        return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1))

    sizes = [1, 3, 5, 11, 21, 51]
    good = [vote_accuracy(n) for n in sizes]
    bad = [vote_accuracy(n, 0.45) for n in sizes]
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.plot(sizes, good, "o-", label="each model 70% right")
    ax.plot(sizes, bad, "o-", label="each model 45% right")
    ax.set_xlabel("number of independent models")
    ax.set_ylabel("majority-vote accuracy")
    ax.legend(fontsize=7)


LESSON("Core", "Bootstrap and out-of-bag, by hand", """
<p>A <b>bootstrap sample</b> draws n rows <b>with replacement</b> from n rows. From rows 0–7 you might get 0, 3, 3, 1, 7, 0, 5, 3. Rows 0 and 3 repeat, while rows 2, 4 and 6 were never picked.</p>
<h4>Why about 37% get left out</h4>
<p>On a single draw, a given row is missed with probability 1 − 1/n. Over n draws it's missed with probability (1 − 1/n)ⁿ.</p>
<table><tr><th>n</th><th>10</th><th>1000</th><th>very large</th></tr>
<tr><th>Left out</th><td>0.349</td><td>0.368</td><td>1/e ≈ 0.368</td></tr></table>
<p>So each tree sees about 63% of the unique rows.</p>
<h4>The out-of-bag (OOB) score</h4>
<ol><li>For row 2, find the trees that never saw it (about 37% of them).</li>
<li>Let only those trees predict it.</li>
<li>Do this for every row and measure accuracy.</li></ol>
<p>That's a validation score without setting any data aside, and it often closely tracks cross-validation. The demo compares them while adding trees.</p>
""", practice=["A Bootstrap Sample", "Out-of-Bag Rows", "Chance a Row Is Left Out"])


@LD
def oob_curve():
    from sklearn.model_selection import cross_val_score
    rng = np.random.default_rng(0)
    data = rng.normal(size=(300, 6))
    target = (data[:, 0] + data[:, 1] * data[:, 2] + rng.normal(0, 0.5, 300) > 0).astype(int)
    sizes = [15, 30, 60, 120, 240]
    oob = [RandomForestClassifier(n_estimators=n, oob_score=True, random_state=0).fit(data, target).oob_score_ for n in sizes]
    cv = [cross_val_score(RandomForestClassifier(n_estimators=n, random_state=0), data, target, cv=3).mean() for n in sizes]
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.plot(sizes, oob, "o-", label="OOB score")
    ax.plot(sizes, cv, "o-", label="3-fold CV")
    ax.set_xlabel("number of trees")
    ax.set_ylabel("accuracy")
    ax.legend(fontsize=8)


LESSON("Core", "Random forests in depth", """
<h4>The algorithm</h4>
<ol><li>Draw a bootstrap sample.</li>
<li>Grow a deep tree. At each split, consider only a random subset of features, and pick the best split among them.</li>
<li>Repeat for every tree.</li>
<li>Predict by averaging probabilities (classification) or values (regression).</li></ol>
<h4>Why random features matter</h4>
<p>If one feature is very strong, every tree would start with it, the trees would look alike, and averaging would achieve little. Hiding it from some splits forces trees to find other patterns. From the variance formula ρσ² + (1 − ρ)σ²/k, lowering the correlation ρ is what breaks the floor that more trees alone can't.</p>
<h4>Tuning guide</h4>
<table><tr><th>Setting</th><th>Advice</th></tr>
<tr><td>n_estimators</td><td>more is never harmful, just slower; 200–500 is usual</td></tr>
<tr><td>max_features</td><td>the most important: 'sqrt' to start, then try a few values</td></tr>
<tr><td>min_samples_leaf</td><td>raise it (2–10) for noisy data, smoother probabilities</td></tr>
<tr><td>max_depth</td><td>often unlimited; limit it to save memory</td></tr>
<tr><td>class_weight</td><td>"balanced" for rare classes</td></tr></table>
<p><b>Limits:</b> can't extrapolate, large models, slower prediction, and importances suffer with correlated features.</p>
""", practice=["Forest Probability = Average of Its Trees", "Count the Trees' Votes", "Forest Feature Importances", "Features Tried at Each Split"])


@LD
def max_features_effect():
    from sklearn.model_selection import cross_val_score
    rng = np.random.default_rng(1)
    data = rng.normal(size=(250, 20))
    target = (data[:, :4].sum(axis=1) + rng.normal(0, 1, 250) > 0).astype(int)
    choices = [1, 2, 4, 8, 14, 20]
    scores = [cross_val_score(RandomForestClassifier(n_estimators=60, max_features=m, random_state=0), data, target, cv=3).mean() for m in choices]
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.plot(choices, scores, "o-")
    ax.set_xlabel("max_features (20 means plain bagging)")
    ax.set_ylabel("CV accuracy")


LESSON("Core", "Gradient boosting, by hand", """
<p>Data: x = 1, 2, 3, 4 and y = 2, 4, 7, 11. Learning rate 0.5, with stumps (one split each).</p>
<h4>Start: predict the mean, 6</h4>
<table><tr><th>Round</th><th>Current prediction</th><th>Residuals the tree must learn</th><th>Stump found</th><th>MSE after</th></tr>
<tr><td>1</td><td>6, 6, 6, 6</td><td>−4, −2, 1, 5</td><td>x ≤ 2.5 → −3, else +3</td><td>4.75</td></tr>
<tr><td>2</td><td>4.5, 4.5, 7.5, 7.5</td><td>−2.5, −0.5, −0.5, 3.5</td><td>x ≤ 3.5 → −1.167, else +3.5</td><td>1.69</td></tr>
<tr><td>3</td><td>3.92, 3.92, 6.92, 9.25</td><td>−1.92, 0.08, 0.08, 1.75</td><td>x ≤ 1.5 → −1.92, else +0.64</td><td>0.77</td></tr></table>
<p>Check round 1: for x = 1, the new prediction is 6 + 0.5 × (−3) = 4.5.</p>
<p>After three rounds the predictions are 2.96, 4.24, 7.24, 9.57, against true values of 2, 4, 7, 11. Each tree works on <b>what's still wrong</b>.</p>
<h4>Why "gradient"?</h4>
<p>For squared error L = ½(y − F)², the slope with respect to the prediction is −(y − F). So the residual is exactly the negative gradient, and adding a tree that fits residuals is one step of gradient descent, taken in the space of predictions. Other losses just change what the trees fit. For log-loss, they fit y − p.</p>
""", practice=["Boosting Starts From the Mean", "The First Tree Fits the Residuals", "Gradient Boosting From Scratch", "Watching Boosting Improve"])


@LD
def boosting_by_hand():
    x = np.array([1.0, 2, 3, 4])
    y = np.array([2.0, 4, 7, 11])
    pred = np.full(4, y.mean())
    history = []
    for round_number in range(3):
        residuals = y - pred
        best = None
        for t in (x[:-1] + x[1:]) / 2:
            left, right = residuals[x <= t], residuals[x > t]
            error = ((left - left.mean()) ** 2).sum() + ((right - right.mean()) ** 2).sum()
            if best is None or error < best[0] - 1e-12:
                best = (error, t, left.mean(), right.mean())
        pred = pred + 0.5 * np.where(x <= best[1], best[2], best[3])
        history.append(((y - pred) ** 2).mean())


LESSON("Advanced", "Tuning boosting, and XGBoost / LightGBM", """
<h4>The settings that matter</h4>
<table><tr><th>Setting</th><th>Effect</th><th>Typical</th></tr>
<tr><td>learning_rate + n_estimators</td><td>small steps need more trees, and generalise better</td><td>0.01–0.1, with early stopping</td></tr>
<tr><td>max_depth</td><td>how many features can interact</td><td>3–8</td></tr>
<tr><td>subsample</td><td>each tree sees a random share of rows</td><td>0.5–0.9</td></tr>
<tr><td>colsample</td><td>random share of features</td><td>0.5–0.9</td></tr>
<tr><td>min_samples_leaf, L2</td><td>smoother, safer leaf values</td><td>tune last</td></tr></table>
<h4>Recipe</h4>
<ol><li>Fix a small learning rate and use early stopping to find the number of trees.</li>
<li>Tune depth, then row and feature sampling.</li>
<li>Lower the rate further at the end.</li></ol>
<h4>Unlike a forest, boosting can overfit with more trees</h4>
<p>The demo shows training error always falling, while test error reaches a minimum and rises. Early stopping halts at that minimum.</p>
<h4>The popular libraries</h4>
<table><tr><th>Library</th><th>Known for</th></tr>
<tr><td>XGBoost</td><td>regularised objective using second derivatives</td></tr>
<tr><td>LightGBM</td><td>histogram-based, leaf-wise growth, very fast</td></tr>
<tr><td>CatBoost</td><td>strong native handling of categories</td></tr>
<tr><td>sklearn HistGradientBoosting</td><td>no extra install, handles missing values</td></tr></table>
""", practice=["Learning Rate vs Training Error", "Watching Boosting Improve"])


@LD
def boosting_overfit():
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 10, (200, 1))
    y = np.sin(x.ravel()) + rng.normal(0, 0.4, 200)
    gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.2, max_depth=4, random_state=0).fit(x[:120], y[:120])
    train_error = [((p - y[:120]) ** 2).mean() for p in gb.staged_predict(x[:120])]
    test_error = [((p - y[120:]) ** 2).mean() for p in gb.staged_predict(x[120:])]
    best_round = int(np.argmin(test_error))
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(train_error, label="train")
    ax.plot(test_error, label="test")
    ax.axvline(best_round, ls="--", color="gray")
    ax.set_xlabel("number of trees")
    ax.set_ylabel("MSE")
    ax.legend(fontsize=8)


LESSON("Advanced", "AdaBoost by hand, and picking an ensemble", """
<h4>One AdaBoost round</h4>
<p>Five rows start with weights of 0.2 each, and a stump gets 2 of them wrong.</p>
<ol><li>Weighted error = 0.2 + 0.2 = <b>0.4</b>.</li>
<li>The model's say: α = ln(0.6 / 0.4) = <b>0.405</b>. Better models get a larger say; at 50% error, α = 0.</li>
<li>Multiply the wrong rows' weights by e^α = 1.5: they become 0.3.</li>
<li>The total is now 3 × 0.2 + 2 × 0.3 = 1.2. Divide: right rows become <b>0.167</b> and wrong rows <b>0.25</b>.</li></ol>
<p>The wrong rows now hold half the total weight (0.25 × 2 = 0.5), so the next stump must focus on them. Because it chases hard rows, AdaBoost is sensitive to noisy labels.</p>
<h4>Which ensemble?</h4>
<table><tr><th>Situation</th><th>Choose</th></tr>
<tr><td>Quick, strong result with little tuning</td><td>random forest</td></tr>
<tr><td>Highest accuracy on tables, time to tune</td><td>gradient boosting</td></tr>
<tr><td>Very noisy labels</td><td>random forest</td></tr>
<tr><td>Several good, different models</td><td>soft voting or stacking</td></tr></table>
<p><b>Stacking warning:</b> train the meta-model on <b>out-of-fold</b> predictions. Using predictions on the base models' own training rows makes it trust whichever model overfit most.</p>
""", practice=["Weighted Error of a Weak Learner", "AdaBoost: How Much Say Does a Model Get?", "AdaBoost: Reweight the Mistakes", "Stacking: Learn How to Blend"])


@LD
def alpha_curve():
    err = np.linspace(0.02, 0.98, 200)
    alpha = np.log((1 - err) / err)
    weights_after = np.array([0.2, 0.2, 0.2, 0.2 * 1.5, 0.2 * 1.5])
    weights_after = weights_after / weights_after.sum()
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.plot(err, alpha)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlabel("weighted error")
    ax.set_ylabel("model's say α")
