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
