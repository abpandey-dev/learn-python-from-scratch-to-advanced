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


LESSON("Basics", "Fitting a line by hand", """
<p>Let's fit y = wx + b to three points, doing every step: (1, 2), (2, 4), (3, 5).</p>
<h4>Step 1: find the means</h4>
<p>x̄ = 2 and ȳ = 11/3 = 3.667.</p>
<h4>Step 2: slope and intercept</h4>
<table><tr><th>x</th><th>y</th><th>x − x̄</th><th>y − ȳ</th><th>(x − x̄)(y − ȳ)</th><th>(x − x̄)²</th></tr>
<tr><td>1</td><td>2</td><td>−1</td><td>−1.667</td><td>1.667</td><td>1</td></tr>
<tr><td>2</td><td>4</td><td>0</td><td>0.333</td><td>0</td><td>0</td></tr>
<tr><td>3</td><td>5</td><td>1</td><td>1.333</td><td>1.333</td><td>1</td></tr>
<tr><td colspan="4"><b>Sum</b></td><td><b>3</b></td><td><b>2</b></td></tr></table>
<p>Slope w = 3 / 2 = <b>1.5</b>. Intercept b = 3.667 − 1.5 × 2 = <b>0.667</b>.</p>
<h4>Step 3: check the fit</h4>
<table><tr><th>x</th><th>y</th><th>ŷ</th><th>Residual y − ŷ</th><th>Squared</th></tr>
<tr><td>1</td><td>2</td><td>2.167</td><td>−0.167</td><td>0.028</td></tr>
<tr><td>2</td><td>4</td><td>3.667</td><td>0.333</td><td>0.111</td></tr>
<tr><td>3</td><td>5</td><td>5.167</td><td>−0.167</td><td>0.028</td></tr></table>
<p>The squared errors total 0.167. Predicting the mean every time gives a total of 4.667. So R² = 1 − 0.167 / 4.667 = <b>0.964</b>: the line explains 96.4% of the variation.</p>
<p><b>Why it always works:</b> the residuals add up to exactly 0, and no other straight line gets a smaller squared total.</p>
""", practice=["Fit a Line", "Residuals", "R² Score"])


@LD
def line_by_hand():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 5.0])
    x_mean, y_mean = x.mean(), y.mean()
    top = ((x - x_mean) * (y - y_mean)).sum()
    bottom = ((x - x_mean) ** 2).sum()
    slope = top / bottom
    intercept = y_mean - slope * x_mean
    pred = slope * x + intercept
    residuals = y - pred
    sse = (residuals ** 2).sum()
    sst = ((y - y_mean) ** 2).sum()
    r2 = 1 - sse / sst


LESSON("Core", "Where the slope formula comes from", """
<p>You don't need to memorise the formula; it follows from one idea: <b>the bottom of a bowl is where the slope is zero.</b></p>
<p>The total error L(w, b) = Σ(y − wx − b)² is a smooth bowl. Set both partial derivatives to zero:</p>
<ol>
<li><b>∂L/∂b = −2Σ(y − wx − b) = 0</b>, which gives b = ȳ − w·x̄. So the best line always passes through the point (x̄, ȳ).</li>
<li><b>∂L/∂w = −2Σx(y − wx − b) = 0.</b> Substitute b and rearrange to get w = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)².</li>
</ol>
<h4>The same answer with matrices</h4>
<p>With many features we write XᵀX·w = Xᵀy. For our three points, X has a column of 1s and a column of x:</p>
<pre><code class="py">XᵀX = [[3,  6],     Xᵀy = [11,
       [6, 14]]            25]
det = 3·14 − 6·6 = 6
inverse = (1/6)·[[14, −6], [−6, 3]]
b = (14·11 − 6·25) / 6 = 4/6 = 0.667
w = (−6·11 + 3·25) / 6 = 9/6 = 1.5</code></pre>
<p>Those match the hand calculation. Solving this system is what <code>LinearRegression</code> does, using a more numerically stable method.</p>
<p><b>When it breaks:</b> if one feature is an exact copy or combination of others, XᵀX has no inverse. <code>lstsq</code> still returns an answer, and Ridge fixes the problem directly.</p>
""", practice=["Multiple Linear Regression", "Fit a Line"])


@LD
def normal_equation_by_hand():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 5.0])
    X = np.column_stack([np.ones(3), x])
    XtX = X.T @ X
    Xty = X.T @ y
    det = np.linalg.det(XtX)
    weights = np.linalg.inv(XtX) @ Xty
    same_answer = LinearRegression().fit(x.reshape(-1, 1), y)
    sklearn_weights = (same_answer.intercept_, same_answer.coef_[0])


LESSON("Core", "Gradient descent, step by step", """
<p>Same three points, starting from w = b = 0 with learning rate 0.1. The gradients of the MSE are ∂/∂w = −2·mean(x·error) and ∂/∂b = −2·mean(error).</p>
<table><tr><th>Step</th><th>Errors</th><th>MSE</th><th>∂/∂w</th><th>∂/∂b</th><th>New w</th><th>New b</th></tr>
<tr><td>1</td><td>2, 4, 5</td><td>15</td><td>−16.667</td><td>−7.333</td><td>1.667</td><td>0.733</td></tr>
<tr><td>2</td><td>−0.4, −0.067, −0.733</td><td>0.234</td><td>1.822</td><td>0.8</td><td>1.484</td><td>0.653</td></tr>
<tr><td>3</td><td>−0.138, 0.378, −0.107</td><td>0.058</td><td>−0.199</td><td>−0.089</td><td>1.504</td><td>0.662</td></tr>
</table>
<p>In three steps w is already near the true 1.5 and b near 0.667. Notice step 1 overshot (w went above 1.5) and step 2 corrected it.</p>
<h4>The learning rate decides everything</h4>
<ul>
<li>Too small: correct, but very slow.</li>
<li>Good: the loss falls smoothly.</li>
<li>Too large: each step overshoots further and the loss explodes.</li>
</ul>
<p><b>Normal equations or gradient descent?</b> The direct solution is exact and simple but gets expensive as features grow (about d³). Gradient descent scales to huge data and is the only option for neural networks.</p>
""", practice=["Train by Gradient Descent", "Mean Squared Error"])


@LD
def learning_rates():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([2.0, 4.0, 5.0])
    fig, ax = plt.subplots(figsize=(4.8, 3))
    for lr, label in [(0.01, "too small: 0.01"), (0.1, "good: 0.1"), (0.19, "too large: 0.19")]:
        w = b = 0.0
        losses = []
        for _ in range(25):
            err = y - (w * x + b)
            losses.append((err ** 2).mean())
            w += lr * 2 * (x * err).mean()
            b += lr * 2 * err.mean()
        ax.plot(losses, label=label)
    ax.set_yscale("log")
    ax.set_xlabel("step")
    ax.set_ylabel("MSE (log scale)")
    ax.legend(fontsize=7)


LESSON("Advanced", "Reading residuals: is the model right?", """
<p>A high R² doesn't prove the model is suitable. Plot residuals against predictions. <b>You want a shapeless cloud around zero.</b></p>
<table><tr><th>Pattern</th><th>What it means</th><th>Try</th></tr>
<tr><td>Curve (U shape)</td><td>the true relationship isn't straight</td><td>polynomial features, a log transform, or a non-linear model</td></tr>
<tr><td>Funnel widening to the right</td><td>errors grow with the value</td><td>model log(y)</td></tr>
<tr><td>A few huge points</td><td>outliers pull the line</td><td>check the data; try Huber regression or MAE</td></tr>
<tr><td>Waves over time</td><td>errors are correlated</td><td>add time features; use time-series methods</td></tr></table>
<h4>Interpreting coefficients carefully</h4>
<ul>
<li>A coefficient is the effect of a feature <b>holding the others fixed</b>, in that feature's units.</li>
<li>To compare importance, standardise features first.</li>
<li><b>Collinearity:</b> if two features nearly duplicate each other, their individual coefficients become unstable, even though predictions stay fine.</li>
<li>A coefficient shows association, not cause. Advertising and sales may both rise at Diwali.</li>
</ul>
""", practice=["Residuals", "Which Feature Matters Most?", "Interaction Features"])


@LD
def residual_patterns():
    rng = np.random.default_rng(0)
    x = np.linspace(1, 10, 80)
    cases = [("good: no pattern", 2 * x + rng.normal(0, 1, 80)), ("curve: missing x²", x ** 2 + rng.normal(0, 1, 80)), ("funnel: growing errors", 2 * x + rng.normal(0, 0.4 * x))]
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.5))
    for ax, (name, y) in zip(axes, cases):
        model = LinearRegression().fit(x.reshape(-1, 1), y)
        pred = model.predict(x.reshape(-1, 1))
        ax.scatter(pred, y - pred, s=7)
        ax.axhline(0, color="black", linewidth=0.7)
        ax.set_title(name, fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "Ridge and Lasso, worked by hand", """
<p>Use the same three points. Centring gives Σxy = 3 and Σx² = 2.</p>
<h4>Ridge: slope = Σxy / (Σx² + α)</h4>
<table><tr><th>α</th><th>Slope</th><th>Intercept</th></tr>
<tr><td>0</td><td>3 / 2 = 1.5</td><td>0.667</td></tr>
<tr><td>1</td><td>3 / 3 = 1.0</td><td>1.667</td></tr></table>
<p>The penalty sits in the denominator, so the slope shrinks but never reaches 0.</p>
<h4>Lasso: slope = soft-threshold(ρ, α) / z</h4>
<p>Here ρ = Σxy / n = 1 and z = Σx² / n = 0.667. Soft-thresholding subtracts α from |ρ|, stopping at 0.</p>
<table><tr><th>α</th><th>Thresholded ρ</th><th>Slope</th></tr>
<tr><td>0.5</td><td>0.5</td><td>0.5 / 0.667 = 0.75</td></tr>
<tr><td>1.2</td><td>0 (cut off)</td><td><b>exactly 0</b></td></tr></table>
<p>That's why Lasso selects features: once the penalty beats a feature's usefulness, its weight becomes exactly zero.</p>
<h4>Practical guide</h4>
<ul>
<li>Start with Ridge when most features probably help a little.</li>
<li>Use Lasso when you expect only a few to matter or want a simpler model.</li>
<li>Use Elastic Net when features are correlated and you still want some sparsity.</li>
<li>Always scale first; the intercept is never penalised.</li>
</ul>
""", practice=["Ridge Regression (One Feature)", "Lasso Regression (One Feature)", "Elastic Net (One Feature)", "Ridge Path: Stronger Penalty, Smaller Slope"])


@LD
def shrink_by_hand():
    sxy, sxx, n = 3.0, 2.0, 3
    ridge_slopes = {alpha: sxy / (sxx + alpha) for alpha in [0, 1, 10]}
    rho, z = sxy / n, sxx / n
    lasso_slopes = {alpha: math.copysign(max(abs(rho) - alpha, 0.0), rho) / z for alpha in [0.5, 1.2]}
