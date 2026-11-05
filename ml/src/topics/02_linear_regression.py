from lib import *
import math
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             mean_absolute_percentage_error)


TOPIC(
    id="linear-regression", title="Linear Regression", glyph="ŷ = wx + b",
    blurb="The first model to learn: fitting a line by least squares and by gradient descent, multiple features, regression metrics, polynomial features, overfitting, and Ridge / Lasso regularisation.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_
y_pred = model.predict(X_test)
mean_squared_error(y, y_pred), mean_absolute_error(y, y_pred), r2_score(y, y_pred)
make_pipeline(PolynomialFeatures(2), LinearRegression())
Ridge(alpha=1.0), Lasso(alpha=0.1)        # regularised versions
# from scratch: w = solve(XᵀX, Xᵀy) with a column of 1s for the intercept</code></pre>
""")

X1 = [1, 2, 3, 4, 5]
Y1 = [3.1, 4.9, 7.2, 8.8, 11.0]


Q(None, "Fit a Line", "Easy", "Least squares",
  "Fit y ≈ slope·x + intercept. Return (slope, intercept) rounded to 4 decimals.",
  [((X1, Y1), (1.97, 1.09)), (([0, 1, 2], [1, 3, 5]), (2.0, 1.0))],
  ("slope = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)², intercept = ȳ − slope·x̄.", "O(n)", "O(1)"),
  ("<code>LinearRegression().fit(X, y)</code>, read <code>coef_</code> and <code>intercept_</code>.", "O(n)", "O(n)"),
  names=["x", "y"])


@B
def fit_line(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return (round(slope, 4), round(my - slope * mx, 4))


@O
def fit_line(x, y):
    model = LinearRegression().fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0], 4), round(model.intercept_, 4))


Q(None, "Predict New Values", "Easy", "Using the fitted line",
  "Fit on (x, y) and return predictions for new_x, rounded to 4 decimals.",
  [((X1, Y1, [6, 0]), [12.91, 1.09])],
  ("Fit the slope and intercept by hand, then apply them.", "O(n + m)", "O(m)"),
  ("<code>model.predict</code>.", "O(n + m)", "O(m)"),
  names=["x", "y", "new_x"])


@B
def predict(x, y, new_x):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    intercept = my - slope * mx
    return [round(slope * v + intercept, 4) for v in new_x]


@O
def predict(x, y, new_x):
    model = LinearRegression().fit(np.array(x).reshape(-1, 1), y)
    return model.predict(np.array(new_x).reshape(-1, 1)).round(4)


Q(None, "Multiple Linear Regression", "Medium", "Several features",
  "Fit y ≈ b + w₁x₁ + w₂x₂ + … Return [b, w₁, w₂, …] rounded to 4 decimals.",
  [(([[1, 1], [2, 1], [3, 2], [4, 3], [5, 5]], [6, 8, 12, 16, 22]), [2.0, 2.0, 2.0]),
   (([[0, 1], [1, 0], [1, 1], [2, 1]], [3, 2, 5, 7]), [0.0, 2.0, 3.0])],
  ("Add a column of 1s and solve the normal equations XᵀX·w = Xᵀy with NumPy.", "O(n·d² + d³)", "O(d²)"),
  ("<code>LinearRegression</code>: intercept_ and coef_.", "O(n·d²)", "O(n·d)"),
  names=["X", "y"])


@B
def multi_fit(X, y):
    A = np.column_stack([np.ones(len(X)), np.array(X, dtype=float)])
    w = np.linalg.solve(A.T @ A, A.T @ np.array(y, dtype=float))
    return w.round(4) + 0.0


@O
def multi_fit(X, y):
    model = LinearRegression().fit(X, y)
    return np.concatenate([[model.intercept_], model.coef_]).round(4) + 0.0


Q(None, "Mean Squared Error", "Easy", "MSE",
  "Return the mean of (y − ŷ)², rounded to 4 decimals.",
  [(([3, 5, 7], [2.5, 5, 8]), 0.4167), (([1, 1], [1, 1]), 0.0)],
  ("Loop: difference, square, average.", "O(n)", "O(1)"),
  ("<code>mean_squared_error(y, y_pred)</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def mse(y, y_pred):
    return round(sum((a - b) ** 2 for a, b in zip(y, y_pred)) / len(y), 4)


@O
def mse(y, y_pred):
    return round(mean_squared_error(y, y_pred), 4)


Q(None, "Root Mean Squared Error", "Easy", "RMSE — error in the target's units",
  "Return √MSE, rounded to 4 decimals.",
  [(([3, 5, 7], [2.5, 5, 8]), 0.6455), (([10, 20], [13, 16]), 3.5355)],
  ("Compute MSE by hand and take the square root.", "O(n)", "O(1)"),
  ("<code>np.sqrt(mean_squared_error(…))</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def rmse(y, y_pred):
    return round(math.sqrt(sum((a - b) ** 2 for a, b in zip(y, y_pred)) / len(y)), 4)


@O
def rmse(y, y_pred):
    return round(np.sqrt(mean_squared_error(y, y_pred)), 4)


Q(None, "Mean Absolute Error", "Easy", "MAE — robust to outliers",
  "Return the mean of |y − ŷ|, rounded to 4 decimals.",
  [(([3, 5, 7], [2.5, 5, 8]), 0.5), (([0, 0, 0, 100], [0, 0, 0, 0]), 25.0)],
  ("Loop of absolute differences.", "O(n)", "O(1)"),
  ("<code>mean_absolute_error</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def mae(y, y_pred):
    return round(sum(abs(a - b) for a, b in zip(y, y_pred)) / len(y), 4)


@O
def mae(y, y_pred):
    return round(mean_absolute_error(y, y_pred), 4)


Q(None, "R² Score", "Medium", "Share of variance explained",
  "Return R² = 1 − SS_res/SS_tot, rounded to 4 decimals. 1 is perfect, 0 is no better than predicting the mean.",
  [(([3, 5, 7, 9], [2.8, 5.3, 6.9, 9.2]), 0.991), (([1, 2, 3], [2, 2, 2]), 0.0)],
  ("Two sums of squares in loops.", "O(n)", "O(1)"),
  ("<code>r2_score</code>.", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def r2(y, y_pred):
    mean = sum(y) / len(y)
    ss_res = sum((a - b) ** 2 for a, b in zip(y, y_pred))
    ss_tot = sum((a - mean) ** 2 for a in y)
    return round(1 - ss_res / ss_tot, 4) + 0.0


@O
def r2(y, y_pred):
    return round(r2_score(y, y_pred), 4) + 0.0


Q(None, "Mean Absolute Percentage Error", "Easy", "MAPE",
  "Return the mean of |y − ŷ| / |y| as a fraction, rounded to 4 decimals.",
  [(([100, 200, 50], [110, 180, 50]), 0.0667)],
  ("Loop of relative errors.", "O(n)", "O(1)"),
  ("<code>mean_absolute_percentage_error</code> (returns a fraction, not %).", "O(n)", "O(1)"),
  names=["y", "y_pred"])


@B
def mape(y, y_pred):
    return round(sum(abs(a - b) / abs(a) for a, b in zip(y, y_pred)) / len(y), 4)


@O
def mape(y, y_pred):
    return round(mean_absolute_percentage_error(y, y_pred), 4)


Q(None, "Adjusted R²", "Medium", "Penalise useless features",
  "Given R², n samples and p features, return 1 − (1 − R²)(n − 1)/(n − p − 1), computing R² from y and ŷ. Rounded to 4 decimals.",
  [(([3, 5, 7, 9, 11, 13], [2.8, 5.3, 6.9, 9.2, 11.4, 12.6], 2), 0.9881)],
  ("R² by hand, then the adjustment.", "O(n)", "O(1)"),
  ("<code>r2_score</code>, then the adjustment (sklearn has no direct function).", "O(n)", "O(1)"),
  names=["y", "y_pred", "p"])


@B
def adjusted_r2(y, y_pred, p):
    n = len(y)
    mean = sum(y) / n
    r2 = 1 - sum((a - b) ** 2 for a, b in zip(y, y_pred)) / sum((a - mean) ** 2 for a in y)
    return round(1 - (1 - r2) * (n - 1) / (n - p - 1), 4)


@O
def adjusted_r2(y, y_pred, p):
    n = len(y)
    return round(1 - (1 - r2_score(y, y_pred)) * (n - 1) / (n - p - 1), 4)


Q(None, "Residuals", "Easy", "What the line missed",
  "Fit a line to (x, y) and return the residuals y − ŷ, rounded to 4 decimals. They always sum to ~0.",
  [((X1, Y1), [0.04, -0.13, 0.2, -0.17, 0.06])],
  ("Fit by hand, subtract predictions.", "O(n)", "O(n)"),
  ("<code>y - model.predict(X)</code>.", "O(n)", "O(n)"),
  names=["x", "y"])


@B
def residuals(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    intercept = my - slope * mx
    return [round(b - (slope * a + intercept), 4) + 0.0 for a, b in zip(x, y)]


@O
def residuals(x, y):
    X = np.array(x).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    return (np.array(y) - model.predict(X)).round(4) + 0.0


Q(None, "Train by Gradient Descent", "Medium", "Same answer, found by walking downhill",
  "Fit slope and intercept by gradient descent on the MSE (start at 0, learning rate 0.05, 5000 steps). Return (slope, intercept) rounded to 4 decimals.",
  [((X1, Y1), (1.97, 1.09)), (([0, 1, 2], [1, 3, 5]), (2.0, 1.0))],
  ("The training loop: predict, compute both gradients, step against them.", "O(steps·n)", "O(1)"),
  ("The exact least-squares answer from <code>LinearRegression</code> — gradient descent converges to it.", "O(n)", "O(n)"),
  names=["x", "y"])


@B
def gd_fit(x, y):
    m = b = 0.0
    n = len(x)
    for _ in range(5000):
        dm = sum(-2 * a * (t - (m * a + b)) for a, t in zip(x, y)) / n
        db = sum(-2 * (t - (m * a + b)) for a, t in zip(x, y)) / n
        m -= 0.05 * dm
        b -= 0.05 * db
    return (round(m, 4), round(b, 4))


@O
def gd_fit(x, y):
    model = LinearRegression().fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0], 4), round(model.intercept_, 4))


Q(None, "Polynomial Regression", "Medium", "Curves with a linear model",
  "Fit y ≈ a + bx + cx² and return predictions for new_x, rounded to 4 decimals.",
  [(([0, 1, 2, 3, 4], [1, 2, 5, 10, 17], [5, -1]), [26.0, 2.0]), (([1, 2, 3, 4], [2, 3, 6, 11], [2.5]), [4.25])],
  ("<code>np.polyfit(x, y, 2)</code> and <code>np.polyval</code> (least squares on x, x²).", "O(n)", "O(1)"),
  ("<code>make_pipeline(PolynomialFeatures(2), LinearRegression())</code>.", "O(n)", "O(n)"),
  names=["x", "y", "new_x"])


@B
def poly_predict(x, y, new_x):
    coeffs = np.polyfit(x, y, 2)
    return np.polyval(coeffs, new_x).round(4)


@O
def poly_predict(x, y, new_x):
    model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model.fit(np.array(x).reshape(-1, 1), y)
    return model.predict(np.array(new_x).reshape(-1, 1)).round(4)


Q(None, "Overfitting: Test Error by Degree", "Hard", "Too simple vs too complex",
  "Fit polynomials of degree 1 … max_degree on the training points and return each one's MSE on the test points, rounded to 2 decimals.",
  [(([0, 1, 2, 3, 4, 5], [1.0, 2.2, 4.8, 10.1, 17.2, 25.9], [1.5, 2.5, 3.5], [3.3, 7.2, 13.4], 4), [5.28, 0.01, 0.01, 0.0])],
  ("For each degree: <code>np.polyfit</code>, predict test x, average squared error.", "O(D·n)", "O(D)"),
  ("Same loop with a PolynomialFeatures + LinearRegression pipeline.", "O(D·n)", "O(D)"),
  names=["x_train", "y_train", "x_test", "y_test", "max_degree"])


@B
def degree_errors(x_train, y_train, x_test, y_test, max_degree):
    out = []
    for d in range(1, max_degree + 1):
        coeffs = np.polyfit(x_train, y_train, d)
        pred = np.polyval(coeffs, x_test)
        out.append(round(float(np.mean((np.array(y_test) - pred) ** 2)), 2))
    return out


@O
def degree_errors(x_train, y_train, x_test, y_test, max_degree):
    out = []
    for d in range(1, max_degree + 1):
        model = make_pipeline(PolynomialFeatures(d), LinearRegression())
        model.fit(np.array(x_train).reshape(-1, 1), y_train)
        pred = model.predict(np.array(x_test).reshape(-1, 1))
        out.append(round(mean_squared_error(y_test, pred), 2))
    return out


Q(None, "Ridge Regression (One Feature)", "Medium", "L2 penalty shrinks the slope",
  "Minimise Σ(y − ŷ)² + α·slope². Return (slope, intercept), rounded to 4 decimals.",
  [((X1, Y1, 1.0), (1.7909, 1.6273)), ((X1, Y1, 10.0), (0.985, 4.045))],
  ("Centre x and y; slope = Σxc·yc / (Σxc² + α); intercept = ȳ − slope·x̄ (the intercept isn't penalised).", "O(n)", "O(1)"),
  ("<code>Ridge(alpha=α)</code>.", "O(n)", "O(n)"),
  names=["x", "y", "alpha"])


@B
def ridge(x, y, alpha):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    slope = sxy / (sxx + alpha)
    return (round(slope, 4), round(my - slope * mx, 4))


@O
def ridge(x, y, alpha):
    model = Ridge(alpha=alpha).fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0], 4), round(model.intercept_, 4))


Q(None, "Ridge Path: Stronger Penalty, Smaller Slope", "Easy", "Effect of α",
  "Return the Ridge slope for each α in alphas, rounded to 4 decimals.",
  [((X1, Y1, [0.01, 1, 10, 100]), [1.968, 1.7909, 0.985, 0.1791])],
  ("Closed form for each α.", "O(k·n)", "O(k)"),
  ("Fit <code>Ridge</code> once per α.", "O(k·n)", "O(k)"),
  names=["x", "y", "alphas"])


@B
def ridge_path(x, y, alphas):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    return [round(sxy / (sxx + a), 4) for a in alphas]


@O
def ridge_path(x, y, alphas):
    X = np.array(x).reshape(-1, 1)
    return [round(Ridge(alpha=a).fit(X, y).coef_[0], 4) for a in alphas]


Q(None, "Lasso Regression (One Feature)", "Hard", "L1 penalty can zero a weight",
  "Minimise (1/2n)Σ(y − ŷ)² + α|slope|. Return (slope, intercept), rounded to 4 decimals.",
  [((X1, Y1, 0.5), (1.72, 1.84)), ((X1, Y1, 10.0), (0.0, 7.0))],
  ("Centre the data; slope = soft-threshold(Σxc·yc/n, α) / (Σxc²/n), where soft-threshold(z, α) = sign(z)·max(|z| − α, 0).", "O(n)", "O(1)"),
  ("<code>Lasso(alpha=α)</code> (coordinate descent).", "O(iterations·n)", "O(n)"),
  names=["x", "y", "alpha"])


@B
def lasso(x, y, alpha):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    rho = sum((a - mx) * (b - my) for a, b in zip(x, y)) / n
    z = sum((a - mx) ** 2 for a in x) / n
    shrunk = math.copysign(max(abs(rho) - alpha, 0.0), rho)
    slope = shrunk / z
    return (round(slope, 4) + 0.0, round(my - slope * mx, 4))


@O
def lasso(x, y, alpha):
    model = Lasso(alpha=alpha).fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0], 4) + 0.0, round(model.intercept_, 4))


Q(None, "Elastic Net (One Feature)", "Hard", "L1 + L2 together",
  "Minimise (1/2n)Σ(y − ŷ)² + α·r·|w| + ½·α·(1 − r)·w² with mixing ratio r. Return (slope, intercept), rounded to 4 decimals.",
  [((X1, Y1, 1.0, 0.5), (1.376, 2.872)), ((X1, Y1, 0.2, 0.9), (1.8614, 1.4158))],
  ("Centre the data; slope = soft-threshold(Σxc·yc/n, α·r) / (Σxc²/n + α(1 − r)).", "O(n)", "O(1)"),
  ("<code>ElasticNet(alpha=α, l1_ratio=r)</code>.", "O(iterations·n)", "O(n)"),
  names=["x", "y", "alpha", "r"])


@B
def elastic_net(x, y, alpha, r):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    rho = sum((a - mx) * (b - my) for a, b in zip(x, y)) / n
    z = sum((a - mx) ** 2 for a in x) / n
    slope = math.copysign(max(abs(rho) - alpha * r, 0.0), rho) / (z + alpha * (1 - r))
    return (round(slope, 4) + 0.0, round(my - slope * mx, 4))


@O
def elastic_net(x, y, alpha, r):
    model = ElasticNet(alpha=alpha, l1_ratio=r).fit(np.array(x).reshape(-1, 1), y)
    return (round(model.coef_[0], 4) + 0.0, round(model.intercept_, 4))


Q(None, "Which Feature Matters Most?", "Medium", "Standardised coefficients",
  "Standardise the features, fit a linear regression, and return the index of the feature with the largest |coefficient|.",
  [(([[1, 100], [2, 300], [3, 200], [4, 500], [5, 400]], [10, 25, 22, 41, 38]), 1)],
  ("Standardise by hand, solve the normal equations with NumPy, compare |weights|.", "O(n·d²)", "O(d²)"),
  ("<code>make_pipeline(StandardScaler(), LinearRegression())</code>, then argmax of |coef_|.", "O(n·d²)", "O(n·d)"),
  names=["X", "y"])


@B
def top_feature(X, y):
    A = np.array(X, dtype=float)
    A = (A - A.mean(axis=0)) / A.std(axis=0)
    A = np.column_stack([np.ones(len(A)), A])
    w = np.linalg.solve(A.T @ A, A.T @ np.array(y, dtype=float))[1:]
    return int(np.argmax(np.abs(w)))


@O
def top_feature(X, y):
    model = make_pipeline(StandardScaler(), LinearRegression()).fit(X, y)
    return int(np.argmax(np.abs(model[-1].coef_)))


Q(None, "Weighted Least Squares", "Medium", "Some points count more",
  "Fit a line where point i has weight w[i]. Return (slope, intercept), rounded to 4 decimals.",
  [((X1, Y1, [1, 1, 2, 1, 8]), (1.9775, 1.107)), (([0, 1, 2], [1, 3, 4], [1, 1, 1]), (1.5, 1.1667))],
  ("Weighted means, then slope = Σw(x − x̄)(y − ȳ) / Σw(x − x̄)².", "O(n)", "O(1)"),
  ("<code>LinearRegression().fit(X, y, sample_weight=w)</code>.", "O(n)", "O(n)"),
  names=["x", "y", "w"])


@B
def weighted_fit(x, y, w):
    W = sum(w)
    mx = sum(wi * a for wi, a in zip(w, x)) / W
    my = sum(wi * b for wi, b in zip(w, y)) / W
    slope = sum(wi * (a - mx) * (b - my) for wi, a, b in zip(w, x, y)) / sum(wi * (a - mx) ** 2 for wi, a in zip(w, x))
    return (round(slope, 4), round(my - slope * mx, 4))


@O
def weighted_fit(x, y, w):
    model = LinearRegression().fit(np.array(x).reshape(-1, 1), y, sample_weight=w)
    return (round(model.coef_[0], 4), round(model.intercept_, 4))


Q(None, "Interaction Features", "Hard", "x₁·x₂ as a feature",
  "Fit y ≈ b + w₁x₁ + w₂x₂ + w₃x₁x₂ and predict for the rows of X_new, rounded to 4 decimals.",
  [(([[1, 1], [1, 2], [2, 1], [2, 2], [3, 1], [3, 3]], [4, 6, 6, 10, 8, 18], [[2, 3], [0, 0]]), [13.2366, 1.145])],
  ("Build the x₁x₂ column by hand, solve the normal equations with NumPy.", "O(n)", "O(1)"),
  ("<code>PolynomialFeatures(2, interaction_only=True, include_bias=False)</code> + <code>LinearRegression</code>.", "O(n)", "O(n)"),
  names=["X", "y", "X_new"])


@B
def interaction_predict(X, y, X_new):
    def design(rows):
        return np.array([[1.0, a, b, a * b] for a, b in rows])
    A = design(X)
    w = np.linalg.solve(A.T @ A, A.T @ np.array(y, dtype=float))
    return (design(X_new) @ w).round(4) + 0.0


@O
def interaction_predict(X, y, X_new):
    model = make_pipeline(PolynomialFeatures(2, interaction_only=True, include_bias=False), LinearRegression())
    return model.fit(X, y).predict(X_new).round(4) + 0.0
