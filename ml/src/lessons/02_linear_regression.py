from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline

LESSON("Basics", "The model: a straight line", """
<p>Linear regression predicts a number with a weighted sum of the features:</p>
<p style="text-align:center"><b>ŷ = w₁x₁ + w₂x₂ + … + b</b></p>
<p>With one feature that's a straight line: <b>w</b> is the slope (how much ŷ changes per unit of x) and <b>b</b> is the intercept. "Training" means choosing w and b. The usual choice is <b>least squares</b>: make the sum of squared vertical distances from the points to the line as small as possible.</p>
<p>For one feature there's a formula: slope = Σ(x − x̄)(y − ȳ)/Σ(x − x̄)², intercept = ȳ − slope·x̄.</p>
""", practice=["Fit a Line", "Predict New Values", "Residuals"])


@LD
def least_squares_picture():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
    model = LinearRegression().fit(x.reshape(-1, 1), y)
    pred = model.predict(x.reshape(-1, 1))
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y, zorder=3)
    ax.plot(x, pred, color="#b45309")
    for a, b, p in zip(x, y, pred):
        ax.plot([a, a], [b, p], ":", color="gray")
    ax.set_title(f"ŷ = {model.coef_[0]:.2f}x + {model.intercept_:.2f}: dotted = residuals", fontsize=8)


LESSON("Core", "Measuring regression error", """
<table><tr><th>Metric</th><th>Formula</th><th>Read as</th></tr>
<tr><td><b>MSE</b></td><td>mean (y − ŷ)²</td><td>squared units; punishes big errors</td></tr>
<tr><td><b>RMSE</b></td><td>√MSE</td><td>typical error in the target's own units</td></tr>
<tr><td><b>MAE</b></td><td>mean |y − ŷ|</td><td>typical error; less sensitive to outliers</td></tr>
<tr><td><b>MAPE</b></td><td>mean |y − ŷ|/|y|</td><td>percentage error (bad near y = 0)</td></tr>
<tr><td><b>R²</b></td><td>1 − SS_res/SS_tot</td><td>share of variance explained; 1 perfect, 0 = predicting the mean</td></tr>
<tr><td>Adjusted R²</td><td>penalises extra features</td><td>for comparing models with different feature counts</td></tr></table>
<p>Always report errors on the <b>test</b> set, and look at the <b>residuals</b>: a pattern in them (a curve, a funnel) means the model is missing something.</p>
""", practice=["Mean Squared Error", "Root Mean Squared Error", "Mean Absolute Error", "Mean Absolute Percentage Error", "R² Score", "Adjusted R²"])


@LD
def metrics_demo():
    y = np.array([3, 5, 7, 9, 11])
    y_pred = np.array([2.8, 5.3, 6.9, 9.6, 10.4])
    errors = y - y_pred
    mse = (errors ** 2).mean()
    rmse = math.sqrt(mse)
    mae = np.abs(errors).mean()
    r2 = 1 - (errors ** 2).sum() / ((y - y.mean()) ** 2).sum()


LESSON("Core", "Many features and gradient descent", """
<p>With d features we stack them into a matrix X (plus a column of 1s for b) and the least-squares weights solve the <b>normal equations</b> XᵀX·w = Xᵀy. sklearn's <code>LinearRegression</code> does this (via a stable least-squares solver).</p>
<p>For huge datasets or other models, we instead use <b>gradient descent</b> on the MSE — it reaches the same answer step by step. Coefficients tell you each feature's effect <i>holding the others fixed</i>; to compare their importance, standardise the features first.</p>
""", practice=["Multiple Linear Regression", "Train by Gradient Descent", "Which Feature Matters Most?", "Weighted Least Squares", "Interaction Features"])


@LD
def gd_convergence():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([3.1, 4.9, 7.2, 8.8, 11.0])
    m = b = 0.0
    path = []
    for _ in range(300):
        err = y - (m * x + b)
        m -= 0.02 * -2 * (x * err).mean()
        b -= 0.02 * -2 * err.mean()
        path.append((m, b))
    path = np.array(path)
    exact = LinearRegression().fit(x.reshape(-1, 1), y)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(path[:, 0], label="slope by GD")
    ax.plot(path[:, 1], label="intercept by GD")
    ax.axhline(exact.coef_[0], ls="--", color="gray")
    ax.axhline(exact.intercept_, ls="--", color="gray")
    ax.set_xlabel("step")
    ax.legend(fontsize=7)


LESSON("Advanced", "Curves, overfitting and the bias–variance trade-off", """
<p>Add polynomial features (x², x³, …) and the "linear" model can fit curves. But more flexibility is not always better:</p>
<ul>
<li><b>Underfitting</b> (high <b>bias</b>): too simple — high error on train <i>and</i> test.</li>
<li><b>Overfitting</b> (high <b>variance</b>): so flexible it fits the noise — low train error, high test error.</li>
</ul>
<p>The sweet spot is found by checking error on data the model didn't train on. Test error typically falls, then rises again as complexity grows.</p>
""", practice=["Polynomial Regression", "Overfitting: Test Error by Degree"])


@LD
def overfit_demo():
    rng = np.random.default_rng(1)
    x = np.sort(rng.uniform(0, 1, 12))
    y = np.sin(2 * np.pi * x) + rng.normal(0, 0.2, 12)
    grid = np.linspace(0, 1, 200)
    fig, axes = plt.subplots(1, 3, figsize=(8, 2.5), sharey=True)
    for ax, degree, name in zip(axes, [1, 3, 11], ["underfit", "good fit", "overfit"]):
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression()).fit(x.reshape(-1, 1), y)
        ax.scatter(x, y, s=12)
        ax.plot(grid, model.predict(grid.reshape(-1, 1)), color="#b45309")
        ax.set_ylim(-2, 2)
        ax.set_title(f"degree {degree}: {name}", fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "Regularisation: Ridge and Lasso", """
<p>Regularisation adds a penalty on large weights to the loss, trading a little bias for much less variance:</p>
<table><tr><th>Model</th><th>Loss</th><th>Effect</th></tr>
<tr><td><b>Ridge</b> (L2)</td><td>MSE + α Σw²</td><td>shrinks all weights smoothly; great with correlated features</td></tr>
<tr><td><b>Lasso</b> (L1)</td><td>MSE + α Σ|w|</td><td>sets some weights exactly to 0 → automatic feature selection</td></tr>
<tr><td>Elastic Net</td><td>both</td><td>a mix</td></tr></table>
<p>α is a hyper-parameter: α = 0 is plain regression, large α pushes weights to 0. Choose it with cross-validation (<code>RidgeCV</code>, <code>LassoCV</code>). Always scale features first, or the penalty treats them unfairly.</p>
""", practice=["Ridge Regression (One Feature)", "Ridge Path: Stronger Penalty, Smaller Slope", "Lasso Regression (One Feature)", "Elastic Net (One Feature)"])


@LD
def regularisation_paths():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(60, 5))
    y = X @ np.array([3, -2, 0.5, 0, 0]) + rng.normal(0, 0.5, 60)
    alphas = np.logspace(-2, 1.5, 30)
    ridge = np.array([Ridge(alpha=a * 20).fit(X, y).coef_ for a in alphas])
    lasso = np.array([Lasso(alpha=a / 5).fit(X, y).coef_ for a in alphas])
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 2.8), sharey=True)
    left.semilogx(alphas, ridge)
    left.set_title("Ridge: weights shrink", fontsize=9)
    right.semilogx(alphas, lasso)
    right.set_title("Lasso: weights hit 0", fontsize=9)
    left.set_xlabel("α")
    right.set_xlabel("α")
    fig.tight_layout()
