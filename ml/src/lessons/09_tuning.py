from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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


LESSON("Basics", "Grid search, worked by hand", """
<p>Choose k for k-NN with 3-fold CV. Suppose the fold accuracies come out like this:</p>
<table><tr><th>k</th><th>Fold 1</th><th>Fold 2</th><th>Fold 3</th><th>Mean</th></tr>
<tr><td>1</td><td>0.80</td><td>0.70</td><td>0.75</td><td>0.75</td></tr>
<tr><td><b>5</b></td><td><b>0.85</b></td><td><b>0.80</b></td><td><b>0.78</b></td><td><b>0.81</b></td></tr>
<tr><td>15</td><td>0.70</td><td>0.72</td><td>0.71</td><td>0.71</td></tr></table>
<ol><li>k = 1 is noisy and overfits; k = 15 is too smooth and underfits. k = 5 wins.</li>
<li><b>Refit</b> k = 5 on all the training data. That's <code>best_estimator_</code>.</li>
<li>Score it once on the test set.</li></ol>
<p><b>Cost:</b> 3 candidates × 3 folds = 9 fits, plus 1 refit = 10.</p>
<h4>Common mistakes</h4>
<ul><li>Reporting 0.81 as the expected performance. It's the best of several tries, so it's a little optimistic.</li>
<li>Picking a winner by a difference smaller than the fold-to-fold spread.</li>
<li>Stopping when the best value sits on the edge of the grid. Extend the grid and search again.</li></ul>
""", practice=["Grid Search by Hand", "Mean and Spread of CV Scores", "How Many Models Does a Grid Search Train?"])


@LD
def grid_table():
    scores = {1: [0.80, 0.70, 0.75], 5: [0.85, 0.80, 0.78], 15: [0.70, 0.72, 0.71]}
    means = {k: round(float(np.mean(v)), 3) for k, v in scores.items()}
    spread = {k: round(float(np.std(v)), 3) for k, v in scores.items()}
    best_k = max(means, key=means.get)
    number_of_fits = len(scores) * 3 + 1


LESSON("Core", "Randomised search and log scales", """
<p>Grids explode: 5 settings with 5 values each is 3,125 combinations, and 15,625 fits with 5-fold CV.</p>
<h4>Why random often beats a grid</h4>
<p>Usually only one or two settings matter much. Say you can afford 9 fits with two settings:</p>
<ul><li><b>Grid (3 × 3):</b> tries just 3 values of the important setting.</li>
<li><b>Random:</b> tries 9 different values of it.</li></ul>
<h4>Search on the right scale</h4>
<p>Going from α = 0.001 to 0.01 can matter as much as from 1 to 10. Sample these evenly on a <b>log</b> scale: learning rate, C, α, γ. Tree depth and leaf sizes are searched as plain integers.</p>
<h4>A practical plan</h4>
<ol><li>Run a wide random search, 20–50 tries.</li>
<li>Look at which regions did well.</li>
<li>Run a narrow search there.</li>
<li>Stop when improvements fall below the fold-to-fold noise.</li></ol>
<p>In sklearn: <code>RandomizedSearchCV(model, {"C": loguniform(1e-3, 1e3)}, n_iter=30)</code>. Optuna is a popular, smarter alternative.</p>
""", practice=["Expand a Parameter Grid", "Tune C for Logistic Regression", "Refit the Winner and Predict"])


@LD
def grid_vs_random():
    r = np.random.default_rng(0)

    def best_score(values, peak):
        return np.exp(-(np.asarray(values) - peak) ** 2 / 0.01).max()

    grid_values = [0.0, 0.5, 1.0]
    averages = {"grid": [], "random": []}
    for trial in range(500):
        peak = r.uniform()
        averages["grid"].append(best_score(grid_values, peak))
        averages["random"].append(best_score(r.uniform(size=9), peak))
    grid_mean = float(np.mean(averages["grid"]))
    random_mean = float(np.mean(averages["random"]))
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.bar(["grid: 3 values\nof the setting", "random: 9 values\nof the setting"], [grid_mean, random_mean], color=["#9ca3af", "#0f766e"])
    ax.set_ylabel("average best score (1 = perfect)")
    ax.set_title("9 fits each, averaged over 500 problems", fontsize=9)


LESSON("Core", "From a curve to a decision", """
<p>Read your train and validation scores, then act:</p>
<table><tr><th>Train</th><th>Validation</th><th>Diagnosis</th><th>Next step</th></tr>
<tr><td>0.65</td><td>0.63</td><td>underfitting</td><td>more features, a more flexible model, less regularisation</td></tr>
<tr><td>0.99</td><td>0.72</td><td>overfitting</td><td>more data, more regularisation, a simpler model, ensembling</td></tr>
<tr><td>0.86</td><td>0.84</td><td>healthy</td><td>check it against the goal; analyse the errors</td></tr>
<tr><td>0.86</td><td>0.97</td><td>suspicious</td><td>check for leakage or an unlucky split</td></tr></table>
<h4>Error analysis usually beats more tuning</h4>
<p>Take the 50 worst predictions and read them. You'll often find mislabelled rows, a missing feature, or one group where the model fails. Fixing those typically gains far more than another grid search.</p>
<h4>The order of work</h4>
<ol><li>Fix the data and the validation scheme.</li>
<li>Add better features.</li>
<li>Try a better model family.</li>
<li>Only then tune hyper-parameters.</li></ol>
""", practice=["Validation Curve", "Learning Curve", "Choose the Polynomial Degree by CV"])


@LD
def diagnose():
    def diagnosis(train, val):
        if val > train + 0.03:
            return "suspicious"
        if train < 0.75:
            return "underfitting"
        if train - val > 0.1:
            return "overfitting"
        return "healthy"

    results = {pair: diagnosis(*pair) for pair in [(0.65, 0.63), (0.99, 0.72), (0.86, 0.84), (0.86, 0.97)]}


LESSON("Advanced", "Nested cross-validation", """
<p>If you choose settings using CV, then report that same CV score, you've measured the model on data that helped choose it. With little data or many candidates, the score is too high.</p>
<h4>The structure</h4>
<ul><li><b>Outer loop</b> (say 5 folds): holds out data to measure performance.</li>
<li><b>Inner loop</b> (say 3 folds), inside each outer training part: picks settings.</li></ul>
<p>Total fits = outer × candidates × inner, so 5 × 10 × 3 = 150, plus refits.</p>
<h4>Important</h4>
<p>Nested CV estimates how good the <b>whole tuning process</b> is. It doesn't give you one final model. For that, run the search once on all the data.</p>
<p>The demo uses pure-noise data, where nothing can truly beat 50%. The best inner score looks better than chance because it picks the luckiest candidate. Nested CV gives a much lower score, and any gap from 50% is just noise. With plenty of data and a real test set, you can skip nesting.</p>
""", practice=["Refit the Winner and Predict", "What the Scaler Learns in Each Fold"])


@LD
def nested_demo():
    from sklearn.model_selection import cross_val_score
    from sklearn.svm import SVC
    grid = {"C": [0.1, 1, 10, 100], "gamma": [0.001, 0.01, 0.1, 1]}
    plain_scores, nested_scores = [], []
    for seed in range(6):
        r = np.random.RandomState(seed)
        X, y = r.normal(size=(40, 20)), r.randint(0, 2, 40)
        search = GridSearchCV(SVC(), grid, cv=KFold(3, shuffle=True, random_state=seed))
        plain_scores.append(search.fit(X, y).best_score_)
        nested_scores.append(cross_val_score(search, X, y, cv=KFold(3, shuffle=True, random_state=seed + 100)).mean())
    plain = float(np.mean(plain_scores))
    nested = float(np.mean(nested_scores))
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.bar(["best inner score\n(optimistic)", "nested CV\n(honest)"], [plain, nested], color=["#b91c1c", "#0f766e"])
    ax.axhline(0.5, ls="--", color="gray")
    ax.set_ylabel("accuracy on random labels")
    ax.set_title("Averaged over 6 pure-noise datasets", fontsize=9)


LESSON("Advanced", "A production-style pipeline on messy data", """
<p>Real tables mix types and contain gaps. The demo builds the whole thing:</p>
<ol><li>Numbers: median imputation, then scaling.</li>
<li>Categories: most-frequent imputation, then one-hot encoding with <code>handle_unknown="ignore"</code>, so a new city in production won't crash the model.</li>
<li>A model, tuned by grid search using the name <code>logisticregression__C</code>.</li>
<li>Saving: <code>joblib.dump(search.best_estimator_, "model.joblib")</code>.</li></ol>
<h4>Before you deploy</h4>
<ul><li><b>Same steps everywhere:</b> the saved pipeline guarantees training and serving match.</li>
<li><b>Versions:</b> a saved model should be loaded with the same scikit-learn version.</li>
<li><b>Monitoring:</b> check input distributions and scores over time; the world changes (<b>drift</b>).</li>
<li><b>Security:</b> only load model files you trust, since loading can run code.</li></ul>
""", practice=["ColumnTransformer: Numbers and Categories", "A Full Preprocessing Pipeline", "Missing-Value Indicator Columns"])


@LD
def messy_pipeline():
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    r = np.random.default_rng(0)
    n = 120
    age = r.uniform(20, 60, n)
    city = r.choice(["Pune", "Delhi", "Goa"], n)
    bought = ((age > 40) ^ (r.uniform(size=n) < 0.15)).astype(int)
    df = pd.DataFrame({"age": age, "city": city})
    df.loc[::9, "age"] = np.nan
    df.loc[::13, "city"] = None
    numbers = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    categories = make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore"))
    prep = ColumnTransformer([("num", numbers, ["age"]), ("cat", categories, ["city"])])
    pipe = make_pipeline(prep, LogisticRegression())
    search = GridSearchCV(pipe, {"logisticregression__C": [0.01, 1, 100]}, cv=3).fit(df, bought)
    best = search.best_params_
    score = round(search.best_score_, 3)
    new_row = pd.DataFrame({"age": [55.0], "city": ["Mumbai"]})
    probability_for_unseen_city = round(search.predict_proba(new_row)[0, 1], 3)
