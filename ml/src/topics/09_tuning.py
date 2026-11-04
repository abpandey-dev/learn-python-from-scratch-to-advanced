from lib import *
import math
from itertools import product
import numpy as np
from sklearn.model_selection import (ParameterGrid, GridSearchCV, KFold, cross_val_score, cross_validate,
                                     validation_curve, learning_curve)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV, LassoCV, LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures, FunctionTransformer
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import make_pipeline, Pipeline, FeatureUnion
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import make_scorer, mean_absolute_error


TOPIC(
    id="tuning", title="Tuning, Pipelines & Regularisation", glyph="⚙",
    blurb="Turning a model into a reliable system: hyper-parameter grids and grid search, validation and learning curves, choosing regularisation by CV, ColumnTransformer and pipelines, avoiding leakage, custom scorers and target transforms.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">pipe = Pipeline([("scale", StandardScaler()), ("model", Ridge())])
search = GridSearchCV(pipe, {"model__alpha": [0.1, 1, 10]}, cv=5, scoring="neg_mean_squared_error")
search.fit(X_train, y_train)
search.best_params_, search.best_score_, search.best_estimator_.predict(X_test)
ColumnTransformer([("num", StandardScaler(), num_cols), ("cat", OneHotEncoder(), cat_cols)])
validation_curve(model, X, y, param_name=…, param_range=…), learning_curve(model, X, y)
RidgeCV(alphas=…), LassoCV(alphas=…, cv=5)</code></pre>
<p>Step names + double underscore address nested parameters: <code>model__alpha</code>.</p>
""")

XC = [[1, 2], [2, 1], [3, 3], [4, 2], [5, 5], [6, 4], [2, 3], [5, 2], [7, 6], [3, 6], [6, 1], [1, 5]]
YC = [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]
XQ = [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
YQ = [1.2, 1.9, 5.1, 9.8, 17.2, 25.9, 37.1, 50.2, 64.8, 81.3]


def folds(n, k):
    """Contiguous folds like KFold(k) without shuffling."""
    out, start = [], 0
    for i in range(k):
        size = n // k + (1 if i < n % k else 0)
        out.append(list(range(start, start + size)))
        start += size
    return out


Q(None, "Expand a Parameter Grid", "Easy", "Every combination",
  "Given a dict of parameter lists, return every combination as a dict (keys in sorted order, last key changing fastest).",
  [(({"k": [1, 3], "weights": ["uniform", "distance"]},), [{'k': 1, 'weights': 'uniform'}, {'k': 1, 'weights': 'distance'}, {'k': 3, 'weights': 'uniform'}, {'k': 3, 'weights': 'distance'}]), (({"alpha": [0.1, 1, 10]},), [{'alpha': 0.1}, {'alpha': 1}, {'alpha': 10}])],
  ("<code>itertools.product</code> over the sorted keys' value lists.", "O(Π sizes)", "O(Π sizes)"),
  ("<code>list(ParameterGrid(grid))</code>.", "O(Π sizes)", "O(Π sizes)"))


@B
def expand(grid):
    keys = sorted(grid)
    return [dict(zip(keys, combo)) for combo in product(*(grid[k] for k in keys))]


@O
def expand(grid):
    return list(ParameterGrid(grid))


Q(None, "Grid Search by Hand", "Medium", "Pick k with cross-validation",
  "For each k in ks, compute the mean 3-fold accuracy (contiguous folds) of k-NN. Return (best k, its mean accuracy rounded to 4 decimals); smallest k wins ties.",
  [((XC, YC, [1, 3, 5]), (5, 0.8333))],
  ("Two loops: over k, over folds; fit on the other folds, score on this one.", "O(K·folds·fit)", "O(n)"),
  ("<code>GridSearchCV(KNeighborsClassifier(), {'n_neighbors': ks}, cv=KFold(3))</code>.", "O(K·folds·fit)", "O(n)"),
  names=["X", "y", "ks"])


@B
def grid_search_knn(X, y, ks):
    best = (None, -1)
    for k in ks:
        scores = []
        for test in folds(len(X), 3):
            train = [i for i in range(len(X)) if i not in test]
            model = KNeighborsClassifier(n_neighbors=k).fit([X[i] for i in train], [y[i] for i in train])
            pred = model.predict([X[i] for i in test])
            scores.append(sum(p == y[i] for p, i in zip(pred, test)) / len(test))
        mean = sum(scores) / len(scores)
        if mean > best[1] + 1e-12:
            best = (k, mean)
    return (best[0], round(best[1], 4))


@O
def grid_search_knn(X, y, ks):
    search = GridSearchCV(KNeighborsClassifier(), {"n_neighbors": ks}, cv=KFold(3)).fit(X, y)
    return (search.best_params_["n_neighbors"], round(search.best_score_, 4))


Q(None, "Mean and Spread of CV Scores", "Easy", "Report mean ± std",
  "Return (mean, std) of the 3-fold accuracies of 3-NN, rounded to 4 decimals.",
  [((XC, YC), (0.75, 0.0))],
  ("Collect fold scores by hand; population std.", "O(folds·fit)", "O(folds)"),
  ("<code>cross_val_score(...)</code> then <code>.mean()</code>, <code>.std()</code>.", "O(folds·fit)", "O(folds)"),
  names=["X", "y"])


@B
def cv_summary(X, y):
    scores = []
    for test in folds(len(X), 3):
        train = [i for i in range(len(X)) if i not in test]
        pred = KNeighborsClassifier(n_neighbors=3).fit([X[i] for i in train], [y[i] for i in train]).predict([X[i] for i in test])
        scores.append(sum(p == y[i] for p, i in zip(pred, test)) / len(test))
    mean = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mean) ** 2 for s in scores) / len(scores))
    return (round(mean, 4), round(std, 4))


@O
def cv_summary(X, y):
    scores = cross_val_score(KNeighborsClassifier(n_neighbors=3), X, y, cv=KFold(3))
    return (round(scores.mean(), 4), round(scores.std(), 4))


Q(None, "Validation Curve", "Medium", "Train vs validation score per setting",
  "For polynomial degree d in degrees, return (mean train R², mean validation R²) over 5 contiguous folds, rounded to 3 decimals.",
  [((XQ, YQ, [1, 2, 3]), [(0.938, -685.756), (1.0, 0.457), (1.0, -0.126)])],
  ("Loops over degrees and folds; fit polynomial regression on train folds, score both parts.", "O(D·folds·fit)", "O(D)"),
  ("<code>validation_curve(pipe, X, y, param_name='poly__degree', param_range=…, cv=KFold(5))</code>.", "O(D·folds·fit)", "O(D)"),
  names=["X", "y", "degrees"])


@B
def val_curve(X, y, degrees):
    out = []
    for d in degrees:
        tr_scores, va_scores = [], []
        for test in folds(len(X), 5):
            train = [i for i in range(len(X)) if i not in test]
            coeffs = np.polyfit([X[i][0] for i in train], [y[i] for i in train], d)

            def r2(idx):
                actual = np.array([y[i] for i in idx])
                pred = np.polyval(coeffs, [X[i][0] for i in idx])
                return 1 - ((actual - pred) ** 2).sum() / ((actual - actual.mean()) ** 2).sum()

            tr_scores.append(r2(train))
            va_scores.append(r2(test))
        out.append((round(float(np.mean(tr_scores)), 3), round(float(np.mean(va_scores)), 3)))
    return out


@O
def val_curve(X, y, degrees):
    pipe = Pipeline([("poly", PolynomialFeatures()), ("lr", LinearRegression())])
    tr, va = validation_curve(pipe, X, y, param_name="poly__degree", param_range=degrees, cv=KFold(5))
    return [(round(a, 3), round(b, 3)) for a, b in zip(tr.mean(axis=1), va.mean(axis=1))]


Q(None, "Learning Curve", "Medium", "Would more data help?",
  "Using 3-NN and 3 contiguous folds, for each training size n (the first n rows of each fold's training part), return the mean validation accuracy, rounded to 4 decimals.",
  [((XC, YC, [4, 6, 8]), [0.5, 0.8333, 0.75])],
  ("Loops over sizes and folds: truncate the training indices, fit, score.", "O(S·folds·fit)", "O(S)"),
  ("<code>learning_curve(model, X, y, train_sizes=…, cv=KFold(3))</code>.", "O(S·folds·fit)", "O(S)"),
  names=["X", "y", "sizes"])


@B
def learn_curve(X, y, sizes):
    out = []
    for n in sizes:
        scores = []
        for test in folds(len(X), 3):
            train = [i for i in range(len(X)) if i not in test][:n]
            pred = KNeighborsClassifier(n_neighbors=3).fit([X[i] for i in train], [y[i] for i in train]).predict([X[i] for i in test])
            scores.append(sum(p == y[i] for p, i in zip(pred, test)) / len(test))
        out.append(round(sum(scores) / len(scores), 4))
    return out


@O
def learn_curve(X, y, sizes):
    _, _, va = learning_curve(KNeighborsClassifier(n_neighbors=3), X, y, train_sizes=sizes, cv=KFold(3))
    return va.mean(axis=1).round(4)


Q(None, "Choose the Polynomial Degree by CV", "Medium", "Grid search over a pipeline step",
  "Return the degree in degrees with the best mean 5-fold (contiguous) R².",
  [((XQ, YQ, [1, 2, 3, 4]), 2)],
  ("Same loops as the validation curve, keep the best validation score.", "O(D·folds·fit)", "O(1)"),
  ("<code>GridSearchCV(pipe, {'poly__degree': degrees}, cv=KFold(5))</code>.", "O(D·folds·fit)", "O(D)"),
  names=["X", "y", "degrees"])


@B
def best_degree(X, y, degrees):
    best = (None, -math.inf)
    for d in degrees:
        scores = []
        for test in folds(len(X), 5):
            train = [i for i in range(len(X)) if i not in test]
            coeffs = np.polyfit([X[i][0] for i in train], [y[i] for i in train], d)
            actual = np.array([y[i] for i in test])
            pred = np.polyval(coeffs, [X[i][0] for i in test])
            scores.append(1 - ((actual - pred) ** 2).sum() / ((actual - actual.mean()) ** 2).sum())
        if np.mean(scores) > best[1] + 1e-12:
            best = (d, np.mean(scores))
    return best[0]


@O
def best_degree(X, y, degrees):
    pipe = Pipeline([("poly", PolynomialFeatures()), ("lr", LinearRegression())])
    return GridSearchCV(pipe, {"poly__degree": degrees}, cv=KFold(5)).fit(X, y).best_params_["poly__degree"]


Q(None, "Ridge With Several Features", "Medium", "Closed form vs library",
  "Fit Ridge(alpha) on centred data: w = (XcᵀXc + αI)⁻¹Xcᵀyc, intercept = ȳ − x̄·w. Return [intercept, w…] rounded to 4 decimals.",
  [(([[1, 2], [2, 1], [3, 4], [4, 3], [5, 5]], [5, 4, 10, 9, 13], 1.0), [1.2526, 0.8246, 1.4912])],
  ("Centre, solve the regularised normal equations with NumPy.", "O(n·d² + d³)", "O(d²)"),
  ("<code>Ridge(alpha=α)</code>.", "O(n·d²)", "O(d²)"),
  names=["X", "y", "alpha"])


@B
def ridge_multi(X, y, alpha):
    A, t = np.array(X, dtype=float), np.array(y, dtype=float)
    mx, my = A.mean(axis=0), t.mean()
    Ac = A - mx
    w = np.linalg.solve(Ac.T @ Ac + alpha * np.eye(A.shape[1]), Ac.T @ (t - my))
    return np.concatenate([[my - mx @ w], w]).round(4)


@O
def ridge_multi(X, y, alpha):
    model = Ridge(alpha=alpha).fit(X, y)
    return np.concatenate([[model.intercept_], model.coef_]).round(4)


Q(None, "RidgeCV: Pick α by Leave-One-Out", "Hard", "Built-in efficient CV",
  "One feature. For each α, compute the leave-one-out mean squared error of ridge regression and return the best α.",
  [(([1, 2, 3, 4, 5, 6], [1.1, 1.9, 3.2, 3.8, 5.3, 5.9], [0.01, 1.0, 10.0, 100.0]), 0.01)],
  ("Literally leave each point out, fit the one-feature ridge formula, predict it, average the squared errors.", "O(A·n²)", "O(n)"),
  ("<code>RidgeCV(alphas=…).alpha_</code> — computes leave-one-out errors in closed form.", "O(A·n·d²)", "O(n)"),
  names=["x", "y", "alphas"])


@B
def ridge_cv(x, y, alphas):
    best = (None, math.inf)
    for a in alphas:
        err = 0
        for i in range(len(x)):
            tx, ty = x[:i] + x[i + 1:], y[:i] + y[i + 1:]
            mx, my = sum(tx) / len(tx), sum(ty) / len(ty)
            slope = sum((p - mx) * (q - my) for p, q in zip(tx, ty)) / (sum((p - mx) ** 2 for p in tx) + a)
            err += (y[i] - (my + slope * (x[i] - mx))) ** 2
        if err < best[1] - 1e-12:
            best = (a, err)
    return best[0]


@O
def ridge_cv(x, y, alphas):
    return RidgeCV(alphas=alphas).fit(np.array(x).reshape(-1, 1), y).alpha_


Q(None, "ColumnTransformer: Numbers and Categories", "Medium", "Different steps per column",
  "Columns 0 is numeric, column 1 is a category. Standardise column 0 and one-hot column 1 (sorted categories). Return the transformed rows, rounded to 4 decimals.",
  [(([[10, "red"], [20, "blue"], [30, "red"], [40, "green"]],), [[-1.3416, 0.0, 0.0, 1.0], [-0.4472, 1.0, 0.0, 0.0], [0.4472, 0.0, 0.0, 1.0], [1.3416, 0.0, 1.0, 0.0]])],
  ("Mean/std of the numbers, sorted categories for the one-hot columns, build each row.", "O(n·k)", "O(n·k)"),
  ("<code>ColumnTransformer([('num', StandardScaler(), [0]), ('cat', OneHotEncoder(), [1])])</code>.", "O(n·k)", "O(n·k)"))


@B
def column_transform(rows):
    nums = [r[0] for r in rows]
    mean = sum(nums) / len(nums)
    std = math.sqrt(sum((v - mean) ** 2 for v in nums) / len(nums))
    cats = sorted(set(r[1] for r in rows))
    return [[round((r[0] - mean) / std, 4)] + [1.0 if r[1] == c else 0.0 for c in cats] for r in rows]


@O
def column_transform(rows):
    ct = ColumnTransformer([("num", StandardScaler(), [0]), ("cat", OneHotEncoder(sparse_output=False), [1])])
    return ct.fit_transform(np.array(rows, dtype=object)).astype(float).round(4)


Q(None, "A Full Preprocessing Pipeline", "Medium", "Impute → scale → model",
  "Train mean-imputation + standard scaling + linear regression on (X, y) (None = missing), then predict X_new. Round to 4 decimals.",
  [(([[1, 10], [2, None], [3, 30], [4, 35], [None, 50]], [11, 19, 33, 39, 52], [[2.5, None], [5, 60]]), [30.8, 64.4447])],
  ("Do each step by hand with training statistics, solve the regression with NumPy, apply the same steps to X_new.", "O(n·d²)", "O(n·d)"),
  ("<code>make_pipeline(SimpleImputer(), StandardScaler(), LinearRegression())</code>.", "O(n·d²)", "O(n·d)"),
  names=["X", "y", "X_new"])


@B
def full_pipeline(X, y, X_new):
    def to_array(rows):
        return np.array([[np.nan if v is None else v for v in r] for r in rows], dtype=float)
    A, B = to_array(X), to_array(X_new)
    means = np.nanmean(A, axis=0)
    A = np.where(np.isnan(A), means, A)
    B = np.where(np.isnan(B), means, B)
    mu, sd = A.mean(axis=0), A.std(axis=0)
    A, B = (A - mu) / sd, (B - mu) / sd
    D = np.column_stack([np.ones(len(A)), A])
    w = np.linalg.lstsq(D, np.array(y, dtype=float), rcond=None)[0]
    return (np.column_stack([np.ones(len(B)), B]) @ w).round(4)


@O
def full_pipeline(X, y, X_new):
    def to_array(rows):
        return np.array([[np.nan if v is None else v for v in r] for r in rows], dtype=float)
    pipe = make_pipeline(SimpleImputer(), StandardScaler(), LinearRegression())
    return pipe.fit(to_array(X), y).predict(to_array(X_new)).round(4)


Q(None, "Leakage From Feature Selection", "Hard", "Why selection belongs inside the pipeline",
  "Make pure-noise data (np.random.RandomState(0): 30 rows × 200 features, random target). Return (CV R² when the 5 best features are picked on ALL data first, CV R² when picking happens inside each fold), 5 contiguous folds, rounded to 3 decimals.",
  [((), (0.346, -0.701))],
  ("Two hand-written CV loops: one selects features once using every row (leak), one re-selects on each training part.", "O(folds·n·d)", "O(n·d)"),
  ("<code>cross_val_score</code> on pre-selected data vs on <code>make_pipeline(SelectKBest(f_regression, k=5), LinearRegression())</code>.", "O(folds·n·d)", "O(n·d)"))


@B
def leakage_demo():
    rng = np.random.RandomState(0)
    X, y = rng.normal(size=(30, 200)), rng.normal(size=30)

    def top5(A, t):
        At, tt = A - A.mean(axis=0), t - t.mean()
        r = (At * tt[:, None]).sum(axis=0) / np.sqrt((At ** 2).sum(axis=0) * (tt ** 2).sum())
        return np.argsort(-np.abs(r), kind="stable")[:5]

    def cv(select_inside):
        leaked = top5(X, y)
        scores = []
        for test in folds(30, 5):
            train = [i for i in range(30) if i not in test]
            cols = top5(X[train], y[train]) if select_inside else leaked
            D = np.column_stack([np.ones(len(train)), X[train][:, cols]])
            w = np.linalg.lstsq(D, y[train], rcond=None)[0]
            pred = np.column_stack([np.ones(len(test)), X[test][:, cols]]) @ w
            scores.append(1 - ((y[test] - pred) ** 2).sum() / ((y[test] - y[test].mean()) ** 2).sum())
        return round(float(np.mean(scores)), 3)

    return (cv(False), cv(True))


@O
def leakage_demo():
    rng = np.random.RandomState(0)
    X, y = rng.normal(size=(30, 200)), rng.normal(size=30)
    leaked = SelectKBest(f_regression, k=5).fit_transform(X, y)
    leaky = cross_val_score(LinearRegression(), leaked, y, cv=KFold(5)).mean()
    honest = cross_val_score(make_pipeline(SelectKBest(f_regression, k=5), LinearRegression()), X, y, cv=KFold(5)).mean()
    return (round(leaky, 3), round(honest, 3))


Q(None, "What the Scaler Learns in Each Fold", "Medium", "Pipelines refit per fold",
  "Cross-validate make_pipeline(StandardScaler(), LinearRegression()) with 3 contiguous folds. Return the mean the scaler learned in each fold, rounded to 4 decimals — proof that test rows never leak into it.",
  [((XQ, YQ), [6.5, 4.2857, 3.0])],
  ("For each fold, average x over the training rows only.", "O(folds·n)", "O(folds)"),
  ("<code>cross_validate(pipe, …, return_estimator=True)</code>, then each estimator's <code>[0].mean_</code>.", "O(folds·n)", "O(folds)"),
  names=["X", "y"])


@B
def fold_means(X, y):
    out = []
    for test in folds(len(X), 3):
        train = [X[i][0] for i in range(len(X)) if i not in test]
        out.append(round(sum(train) / len(train), 4))
    return out


@O
def fold_means(X, y):
    res = cross_validate(make_pipeline(StandardScaler(), LinearRegression()), X, y, cv=KFold(3), return_estimator=True)
    return [round(est[0].mean_[0], 4) for est in res["estimator"]]


Q(None, "How Many Models Does a Grid Search Train?", "Easy", "The cost of tuning",
  "Return the number of fits for a grid search over the given grid with k-fold CV (not counting the final refit).",
  [(({"C": [0.1, 1, 10], "kernel": ["linear", "rbf"]}, 5), 30), (({"alpha": [1, 2, 3, 4]}, 3), 12)],
  ("Multiply the list sizes, then by k.", "O(params)", "O(1)"),
  ("<code>len(ParameterGrid(grid)) * k</code>.", "O(combos)", "O(combos)"),
  names=["grid", "k"])


@B
def n_fits(grid, k):
    combos = 1
    for values in grid.values():
        combos *= len(values)
    return combos * k


@O
def n_fits(grid, k):
    return len(ParameterGrid(grid)) * k


Q(None, "A Custom Scorer", "Easy", "Negative MAE",
  "Return the 3-fold (contiguous) cross-validated scores of a straight-line fit using negative mean absolute error, rounded to 4 decimals.",
  [((XQ, YQ), [-22.7452, -10.3969, -21.4405])],
  ("Loop over folds, fit, compute −MAE.", "O(folds·n)", "O(folds)"),
  ("<code>make_scorer(mean_absolute_error, greater_is_better=False)</code> in <code>cross_val_score</code>.", "O(folds·n)", "O(folds)"),
  names=["X", "y"])


@B
def neg_mae_cv(X, y):
    out = []
    for test in folds(len(X), 3):
        train = [i for i in range(len(X)) if i not in test]
        slope, intercept = np.polyfit([X[i][0] for i in train], [y[i] for i in train], 1)
        errors = [abs(y[i] - (slope * X[i][0] + intercept)) for i in test]
        out.append(round(-sum(errors) / len(errors), 4))
    return out


@O
def neg_mae_cv(X, y):
    scorer = make_scorer(mean_absolute_error, greater_is_better=False)
    return cross_val_score(LinearRegression(), X, y, cv=KFold(3), scoring=scorer).round(4)


Q(None, "Predict on a Log Scale", "Medium", "TransformedTargetRegressor",
  "Fit a line to log(y), then predict exp(…) for new x — good for targets that grow multiplicatively. Round to 2 decimals.",
  [(([[1], [2], [3], [4], [5]], [2.7, 7.4, 20.1, 54.6, 148.4], [[6], [2.5]]), [404.5, 12.16])],
  ("Take logs, fit slope/intercept with NumPy, exponentiate the predictions.", "O(n)", "O(n)"),
  ("<code>TransformedTargetRegressor(LinearRegression(), func=np.log, inverse_func=np.exp)</code>.", "O(n)", "O(n)"),
  names=["X", "y", "X_new"])


@B
def log_target(X, y, X_new):
    slope, intercept = np.polyfit([r[0] for r in X], np.log(y), 1)
    return [round(math.exp(slope * r[0] + intercept), 2) for r in X_new]


@O
def log_target(X, y, X_new):
    model = TransformedTargetRegressor(LinearRegression(), func=np.log, inverse_func=np.exp)
    return model.fit(X, y).predict(X_new).round(2)


Q(None, "Combine Feature Sets", "Easy", "FeatureUnion",
  "For one-column X, return rows [x, x², log(1 + x)] — three transformers applied side by side. Round to 4 decimals.",
  [(([[0], [1], [3]],), [[0.0, 0.0, 0.0], [1.0, 1.0, 0.6931], [3.0, 9.0, 1.3863]])],
  ("Compute the three columns by hand.", "O(n)", "O(n)"),
  ("<code>FeatureUnion</code> of three <code>FunctionTransformer</code>s.", "O(n)", "O(n)"))


@B
def union(X):
    return [[float(r[0]), float(r[0] ** 2), round(math.log1p(r[0]), 4)] for r in X]


@O
def union(X):
    fu = FeatureUnion([("x", FunctionTransformer()), ("sq", FunctionTransformer(np.square)), ("log", FunctionTransformer(np.log1p))])
    return fu.fit_transform(np.array(X, dtype=float)).round(4)


Q(None, "Missing-Value Indicator Columns", "Easy", "Keep the fact that it was missing",
  "Mean-impute each column and append a 0/1 column for every column that had missing values. None = missing. Round to 4 decimals.",
  [(([[1, 5], [None, 6], [3, 7]],), [[1.0, 5.0, 0.0], [2.0, 6.0, 1.0], [3.0, 7.0, 0.0]])],
  ("Impute by hand; for columns with gaps, add the indicator.", "O(n·d)", "O(n·d)"),
  ("<code>SimpleImputer(add_indicator=True)</code>.", "O(n·d)", "O(n·d)"))


@B
def impute_with_flags(rows):
    d = len(rows[0])
    means = [sum(r[j] for r in rows if r[j] is not None) / sum(1 for r in rows if r[j] is not None) for j in range(d)]
    gappy = [j for j in range(d) if any(r[j] is None for r in rows)]
    out = []
    for r in rows:
        filled = [round(float(means[j] if r[j] is None else r[j]), 4) for j in range(d)]
        out.append(filled + [1.0 if r[j] is None else 0.0 for j in gappy])
    return out


@O
def impute_with_flags(rows):
    A = np.array([[np.nan if v is None else v for v in r] for r in rows], dtype=float)
    return SimpleImputer(add_indicator=True).fit_transform(A).round(4)


Q(None, "Tune C for Logistic Regression", "Medium", "Regularisation strength by CV",
  "Return the C (from Cs) with the best mean 3-fold (contiguous) accuracy; smallest C wins ties.",
  [((XC, YC, [0.01, 0.1, 1, 10]), 0.1)],
  ("Loop over C and folds, fit, count correct predictions.", "O(C·folds·fit)", "O(n)"),
  ("<code>GridSearchCV(LogisticRegression(), {'C': Cs}, cv=KFold(3))</code>.", "O(C·folds·fit)", "O(n)"),
  names=["X", "y", "Cs"])


@B
def tune_c(X, y, Cs):
    best = (None, -1)
    for c in Cs:
        scores = []
        for test in folds(len(X), 3):
            train = [i for i in range(len(X)) if i not in test]
            pred = LogisticRegression(C=c).fit([X[i] for i in train], [y[i] for i in train]).predict([X[i] for i in test])
            scores.append(sum(p == y[i] for p, i in zip(pred, test)) / len(test))
        if sum(scores) / len(scores) > best[1] + 1e-12:
            best = (c, sum(scores) / len(scores))
    return best[0]


@O
def tune_c(X, y, Cs):
    return GridSearchCV(LogisticRegression(), {"C": Cs}, cv=KFold(3)).fit(X, y).best_params_["C"]


Q(None, "Refit the Winner and Predict", "Medium", "best_estimator_",
  "Grid-search Ridge α in alphas with 3-fold CV (contiguous) on (X, y), refit the best on all the data, and predict X_new. Round to 4 decimals.",
  [((XQ, YQ, [0.1, 10, 1000], [[10], [11]]), [73.3697, 81.3551])],
  ("CV loop to pick α, then fit Ridge on everything and predict.", "O(A·folds·fit)", "O(n)"),
  ("<code>GridSearchCV(Ridge(), …, refit=True).predict(X_new)</code> (refit is the default).", "O(A·folds·fit)", "O(n)"),
  names=["X", "y", "alphas", "X_new"])


@B
def refit_predict(X, y, alphas, X_new):
    best = (None, -math.inf)
    for a in alphas:
        scores = []
        for test in folds(len(X), 3):
            train = [i for i in range(len(X)) if i not in test]
            model = Ridge(alpha=a).fit([X[i] for i in train], [y[i] for i in train])
            actual = np.array([y[i] for i in test])
            pred = model.predict([X[i] for i in test])
            scores.append(1 - ((actual - pred) ** 2).sum() / ((actual - actual.mean()) ** 2).sum())
        if np.mean(scores) > best[1] + 1e-12:
            best = (a, np.mean(scores))
    return Ridge(alpha=best[0]).fit(X, y).predict(X_new).round(4)


@O
def refit_predict(X, y, alphas, X_new):
    search = GridSearchCV(Ridge(), {"alpha": alphas}, cv=KFold(3)).fit(X, y)
    return search.predict(X_new).round(4)


Q(None, "LassoCV: Pick α by K-Fold", "Hard", "Sparse model, tuned",
  "One feature. For each α, compute the mean 3-fold (contiguous) MSE of Lasso and return the best α.",
  [(([1, 2, 3, 4, 5, 6, 7, 8, 9], [1.0, 2.2, 2.8, 4.1, 5.2, 5.8, 7.1, 7.9, 9.2], [0.01, 0.5, 2.0]), 0.01)],
  ("Lasso for one feature in closed form (soft-thresholding) inside a hand-written CV loop.", "O(A·folds·n)", "O(n)"),
  ("<code>LassoCV(alphas=…, cv=KFold(3)).alpha_</code>.", "O(A·folds·n)", "O(n)"),
  names=["x", "y", "alphas"])


@B
def lasso_cv(x, y, alphas):
    best = (None, math.inf)
    for a in alphas:
        errs = []
        for test in folds(len(x), 3):
            tx = [x[i] for i in range(len(x)) if i not in test]
            ty = [y[i] for i in range(len(x)) if i not in test]
            n = len(tx)
            mx, my = sum(tx) / n, sum(ty) / n
            rho = sum((p - mx) * (q - my) for p, q in zip(tx, ty)) / n
            z = sum((p - mx) ** 2 for p in tx) / n
            slope = math.copysign(max(abs(rho) - a, 0.0), rho) / z
            errs.append(sum((y[i] - (my + slope * (x[i] - mx))) ** 2 for i in test) / len(test))
        if sum(errs) / len(errs) < best[1] - 1e-12:
            best = (a, sum(errs) / len(errs))
    return best[0]


@O
def lasso_cv(x, y, alphas):
    return LassoCV(alphas=alphas, cv=KFold(3)).fit(np.array(x).reshape(-1, 1), y).alpha_
