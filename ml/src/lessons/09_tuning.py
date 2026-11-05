from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV, KFold, ShuffleSplit, validation_curve, learning_curve
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer

rng = np.random.default_rng(0)
X_DEMO = np.sort(rng.uniform(0, 1, 40)).reshape(-1, 1)
Y_DEMO = np.sin(2 * np.pi * X_DEMO[:, 0]) + rng.normal(0, 0.25, 40)

LESSON("Basics", "Hyper-parameters and grid search", """
<p>Parameters are learned from the data; <b>hyper-parameters</b> are settings you choose before training: k in k-NN, tree depth, regularisation strength.</p>
<p><b>Grid search</b> tries every combination and scores each with cross-validation:</p>
<ol>
<li>List the candidate values (the <b>grid</b>).</li>
<li>For each combination, run k-fold CV and average the scores.</li>
<li>Keep the best combination, then refit it on all the training data.</li>
</ol>
<p>The cost multiplies: 3 values × 2 values × 5 folds = 30 fits. For big grids, <b>randomised search</b> samples combinations and usually finds something nearly as good for far less work.</p>
""", practice=["Expand a Parameter Grid", "Grid Search by Hand", "How Many Models Does a Grid Search Train?", "Mean and Spread of CV Scores", "Tune C for Logistic Regression", "Refit the Winner and Predict"])


@LD
def search_heatmap():
    pipe = Pipeline([("poly", PolynomialFeatures()), ("ridge", Ridge())])
    degrees, alphas = [1, 3, 5, 7, 9], [0.001, 0.01, 0.1, 1, 10]
    grid = {"poly__degree": degrees, "ridge__alpha": alphas}
    cv = ShuffleSplit(n_splits=5, test_size=0.25, random_state=0)
    search = GridSearchCV(pipe, grid, cv=cv).fit(X_DEMO, Y_DEMO)
    scores = search.cv_results_["mean_test_score"].reshape(len(degrees), len(alphas))
    fig, ax = plt.subplots(figsize=(4.8, 3))
    image = ax.imshow(np.clip(scores, 0, 1), cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(alphas)), alphas)
    ax.set_yticks(range(len(degrees)), degrees)
    ax.set_xlabel("ridge alpha")
    ax.set_ylabel("degree")
    fig.colorbar(image, label="mean CV R²")


LESSON("Core", "Reading validation and learning curves", """
<p>Two plots tell you what to do next.</p>
<ul>
<li><b>Validation curve</b>: score against one hyper-parameter. On the simple side both scores are low (underfitting). On the complex side the training score stays high while the validation score drops (overfitting). Choose the peak of the validation score.</li>
<li><b>Learning curve</b>: score against the amount of training data. If the two lines have met at a low score, more data won't help, so use a richer model. If there's a big gap, more data or more regularisation will.</li>
</ul>
""", practice=["Validation Curve", "Learning Curve", "Choose the Polynomial Degree by CV"])


@LD
def curves():
    pipe = Pipeline([("poly", PolynomialFeatures()), ("lr", LinearRegression())])
    cv = ShuffleSplit(n_splits=10, test_size=0.25, random_state=0)
    degrees = np.arange(1, 13)
    tr, va = validation_curve(pipe, X_DEMO, Y_DEMO, param_name="poly__degree", param_range=degrees, cv=cv)
    pipe.set_params(poly__degree=5)
    sizes, tr2, va2 = learning_curve(pipe, X_DEMO, Y_DEMO, train_sizes=np.linspace(0.3, 1.0, 6), cv=cv)
    fig, (left, right) = plt.subplots(1, 2, figsize=(8, 2.9))
    left.plot(degrees, tr.mean(axis=1), "o-", markersize=3, label="train")
    left.plot(degrees, np.clip(va.mean(axis=1), -1, 1), "o-", markersize=3, label="validation")
    left.set_xlabel("polynomial degree")
    left.legend(fontsize=7)
    right.plot(sizes, tr2.mean(axis=1), "o-", markersize=3, label="train")
    right.plot(sizes, va2.mean(axis=1), "o-", markersize=3, label="validation")
    right.set_xlabel("training rows")
    right.legend(fontsize=7)
    fig.tight_layout()


LESSON("Core", "Tuning regularisation", """
<p>Regularisation strength is the most common thing to tune. sklearn has fast built-ins: <code>RidgeCV</code> computes leave-one-out errors in closed form, and <code>LassoCV</code> walks along a path of α values. For logistic regression, tune C (small C = strong penalty).</p>
<p>Search on a <b>log scale</b> (0.001, 0.01, 0.1, 1, 10): what matters is the order of magnitude. If the best value sits at the edge of your grid, extend the grid.</p>
""", practice=["Ridge With Several Features", "RidgeCV: Pick α by Leave-One-Out", "LassoCV: Pick α by K-Fold"])


@LD
def alpha_sweep():
    pipe = make_pipeline(PolynomialFeatures(9), StandardScaler(), Ridge())
    alphas = np.logspace(-4, 3, 15)
    cv = ShuffleSplit(n_splits=10, test_size=0.25, random_state=0)
    tr, va = validation_curve(pipe, X_DEMO, Y_DEMO, param_name="ridge__alpha", param_range=alphas, cv=cv)
    fig, ax = plt.subplots(figsize=(4.6, 3))
    ax.semilogx(alphas, tr.mean(axis=1), label="train")
    ax.semilogx(alphas, va.mean(axis=1), label="validation")
    ax.set_xlabel("alpha")
    ax.set_ylabel("R²")
    ax.legend(fontsize=8)


LESSON("Advanced", "Pipelines and ColumnTransformer", """
<p>Real tables mix numbers, categories and gaps. A <b>ColumnTransformer</b> applies different steps to different columns, and a <b>Pipeline</b> chains those steps with the model:</p>
<pre><code class="py">num = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
cat = make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore"))
prep = ColumnTransformer([("num", num, ["age", "income"]), ("cat", cat, ["city"])])
model = make_pipeline(prep, LogisticRegression())</code></pre>
<p>The whole object fits, predicts, cross-validates and can be saved as one unit, so training and production run the same steps. Tune nested settings with step names and a double underscore: <code>logisticregression__C</code>.</p>
<p>Useful extras: <code>TransformedTargetRegressor</code> (model a log target), <code>FeatureUnion</code> (build features side by side), <code>add_indicator=True</code> (keep a flag for what was missing).</p>
""", practice=["ColumnTransformer: Numbers and Categories", "A Full Preprocessing Pipeline", "Predict on a Log Scale", "Combine Feature Sets", "Missing-Value Indicator Columns", "A Custom Scorer"])


@LD
def column_transformer_demo():
    rows = np.array([[10, "red"], [20, "blue"], [30, "red"], [40, "green"]], dtype=object)
    ct = ColumnTransformer([("num", StandardScaler(), [0]), ("cat", OneHotEncoder(sparse_output=False), [1])])
    table = ct.fit_transform(rows).astype(float).round(2)
    columns = ct.get_feature_names_out().tolist()


LESSON("Advanced", "Leakage: the mistake that flatters you", """
<p>If any preprocessing step sees validation rows, your score is too good to be true. A striking case: take <b>pure noise</b> with 200 features, choose the 5 most correlated with the target using all the data, then cross-validate. The score looks positive even though there is nothing to find.</p>
<p>Put the selection inside the pipeline and it is redone on each training part only. The score falls to where it belongs, at or below zero.</p>
<p><b>Rule:</b> everything learned from data (scalers, imputers, encoders, feature selection, PCA) goes inside the pipeline. And after tuning, use a separate test set or nested CV, because the best CV score was picked from many tries and is slightly optimistic.</p>
""", practice=["Leakage From Feature Selection", "What the Scaler Learns in Each Fold"])


@LD
def leakage_bars():
    from sklearn.feature_selection import SelectKBest, f_regression
    from sklearn.model_selection import cross_val_score
    r = np.random.RandomState(0)
    X, y = r.normal(size=(30, 200)), r.normal(size=30)
    leaked = SelectKBest(f_regression, k=5).fit_transform(X, y)
    leaky = cross_val_score(LinearRegression(), leaked, y, cv=KFold(5)).mean()
    honest = cross_val_score(make_pipeline(SelectKBest(f_regression, k=5), LinearRegression()), X, y, cv=KFold(5)).mean()
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.bar(["selected on all data\n(leak)", "selected inside each fold\n(honest)"], [leaky, honest], color=["#b91c1c", "#0f766e"])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("cross-validated R²")
    ax.set_title("The same pure-noise data", fontsize=9)
