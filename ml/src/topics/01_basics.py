from lib import *
import math
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.preprocessing import (StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder, LabelEncoder,
                                   OrdinalEncoder, PolynomialFeatures, KBinsDiscretizer, FunctionTransformer, Normalizer)
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_regression
from sklearn.utils.class_weight import compute_class_weight
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression


TOPIC(
    id="basics", title="ML Basics & Data Preparation", glyph="X → y",
    blurb="What a model learns from, splitting data honestly, baselines, scaling, encoding categories, filling missing values, creating and selecting features, and folds for cross-validation.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler().fit(X_train)      # learn mean/std on TRAIN only
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)        # reuse train's numbers

OneHotEncoder(sparse_output=False), OrdinalEncoder(categories=[order])
SimpleImputer(strategy="mean" | "median" | "most_frequent")
PolynomialFeatures(degree=2, include_bias=False)
make_pipeline(StandardScaler(), LinearRegression())</code></pre>
<p>Every sklearn object follows the same pattern: <b>fit</b> learns from data, <b>transform</b>/<b>predict</b> applies what was learned.</p>
""")


Q(None, "Train / Test Split Without Shuffling", "Easy", "Holding data back",
  "Split X into (train, test) with the last test_size fraction (rounded up) as the test set, keeping the order.",
  [(([[1], [2], [3], [4], [5], [6], [7], [8]], 0.25), ([[1], [2], [3], [4], [5], [6]], [[7], [8]])), (([[1, 2], [3, 4], [5, 6]], 0.5), ([[1, 2]], [[3, 4], [5, 6]]))],
  ("Count how many rows go to the test set (round up), then slice.", "O(n)", "O(n)"),
  ("<code>train_test_split(X, test_size=…, shuffle=False)</code>. In real projects keep shuffle on and set random_state.", "O(n)", "O(n)"),
  names=["X", "test_size"])


@B
def split(X, test_size):
    n_test = math.ceil(len(X) * test_size)
    n_train = len(X) - n_test
    return (X[:n_train], X[n_train:])


@O
def split(X, test_size):
    train, test = train_test_split(X, test_size=test_size, shuffle=False)
    return (train, test)


Q(None, "Majority-Class Baseline", "Easy", "The score to beat",
  "Always predict the most common training label (ties → smallest label). Return the accuracy on the test labels, rounded to 4 decimals.",
  [((["a", "a", "b", "a", "c"], ["a", "b", "a"]), 0.6667), (([1, 0, 1, 0], [0, 0, 1]), 0.6667)],
  ("Count labels in a dictionary, pick the winner, compare with every test label.", "O(n + m)", "O(k)"),
  ("<code>DummyClassifier(strategy='most_frequent')</code> — every model must beat this.", "O(n + m)", "O(k)"),
  names=["y_train", "y_test"])


@B
def baseline_accuracy(y_train, y_test):
    counts = {}
    for label in y_train:
        counts[label] = counts.get(label, 0) + 1
    best = max(counts.values())
    guess = min(label for label, c in counts.items() if c == best)
    correct = sum(1 for label in y_test if label == guess)
    return round(correct / len(y_test), 4)


@O
def baseline_accuracy(y_train, y_test):
    model = DummyClassifier(strategy="most_frequent")
    model.fit(np.zeros((len(y_train), 1)), y_train)
    return round(model.score(np.zeros((len(y_test), 1)), y_test), 4)


Q(None, "Mean Baseline for Regression", "Easy", "Predict the average",
  "Always predict the mean of the training targets. Return the mean squared error on the test targets, rounded to 4 decimals.",
  [(([10, 20, 30], [15, 25]), 25.0), (([2, 4, 6, 8], [5, 5, 5]), 0.0)],
  ("Average the training targets, then average the squared errors on the test set.", "O(n + m)", "O(1)"),
  ("<code>DummyRegressor()</code> and <code>mean_squared_error</code>.", "O(n + m)", "O(1)"),
  names=["y_train", "y_test"])


@B
def baseline_mse(y_train, y_test):
    guess = sum(y_train) / len(y_train)
    total = 0
    for y in y_test:
        total += (y - guess) ** 2
    return round(total / len(y_test), 4)


@O
def baseline_mse(y_train, y_test):
    from sklearn.metrics import mean_squared_error
    model = DummyRegressor().fit(np.zeros((len(y_train), 1)), y_train)
    pred = model.predict(np.zeros((len(y_test), 1)))
    return round(mean_squared_error(y_test, pred), 4)


Q(None, "Standard Scaling (Fit on Train Only)", "Medium", "z = (x − mean) / std",
  "Learn each column's mean and standard deviation (population) from the training rows, then scale the test rows. Round to 4 decimals.",
  [(([[1, 10], [2, 20], [3, 30]], [[2, 40], [4, 10]]), [[0.0, 2.4495], [2.4495, -1.2247]])],
  ("Column means and stds with loops, then (x − mean)/std for each test value.", "O(n·d)", "O(d)"),
  ("<code>StandardScaler().fit(train).transform(test)</code>.", "O(n·d)", "O(d)"),
  names=["train", "test"])


@B
def standard_scale(train, test):
    d = len(train[0])
    means = [sum(r[j] for r in train) / len(train) for j in range(d)]
    stds = [math.sqrt(sum((r[j] - means[j]) ** 2 for r in train) / len(train)) for j in range(d)]
    return [[round((r[j] - means[j]) / stds[j], 4) for j in range(d)] for r in test]


@O
def standard_scale(train, test):
    scaler = StandardScaler().fit(train)
    return scaler.transform(test).round(4)


Q(None, "Min-Max Scaling", "Easy", "Squeeze into [0, 1]",
  "Learn each column's min and max from the training rows, then scale the test rows to (x − min)/(max − min). Round to 4 decimals.",
  [(([[0, 100], [10, 200]], [[5, 150], [20, 100]]), [[0.5, 0.5], [2.0, 0.0]])],
  ("Min and max per column with loops, then the formula.", "O(n·d)", "O(d)"),
  ("<code>MinMaxScaler().fit(train).transform(test)</code>.", "O(n·d)", "O(d)"),
  names=["train", "test"])


@B
def min_max(train, test):
    d = len(train[0])
    lo = [min(r[j] for r in train) for j in range(d)]
    hi = [max(r[j] for r in train) for j in range(d)]
    return [[round((r[j] - lo[j]) / (hi[j] - lo[j]), 4) for j in range(d)] for r in test]


@O
def min_max(train, test):
    return MinMaxScaler().fit(train).transform(test).round(4)


Q(None, "Robust Scaling", "Medium", "Median and IQR resist outliers",
  "Scale one column as (x − median) / IQR, where the IQR (Q3 − Q1) uses linear interpolation. Round to 4 decimals.",
  [(([1, 2, 3, 4, 100],), [-1.0, -0.5, 0.0, 0.5, 48.5]), (([10, 20, 30, 40],), [-1.0, -0.3333, 0.3333, 1.0])],
  ("Sort; compute the median, Q1 and Q3 by interpolating positions (n − 1)·p; then scale.", "O(n log n)", "O(n)"),
  ("<code>RobustScaler()</code> on a one-column matrix.", "O(n log n)", "O(n)"))


@B
def robust(values):
    s = sorted(values)

    def q(p):
        pos = (len(s) - 1) * p
        lo = int(pos)
        hi = min(lo + 1, len(s) - 1)
        return s[lo] + (s[hi] - s[lo]) * (pos - lo)

    median, iqr = q(0.5), q(0.75) - q(0.25)
    return [round((x - median) / iqr, 4) for x in values]


@O
def robust(values):
    col = np.array(values, dtype=float).reshape(-1, 1)
    return RobustScaler().fit_transform(col).ravel().round(4)


Q(None, "One-Hot Encoding", "Easy", "Categories → 0/1 columns",
  "Turn a list of categories into rows of 0/1 indicators, columns in sorted category order.",
  [((["red", "green", "blue", "green"],), [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]), ((["b", "a"],), [[0.0, 1.0], [1.0, 0.0]])],
  ("Sorted unique categories give the columns; each row has a single 1.", "O(n·k)", "O(n·k)"),
  ("<code>OneHotEncoder(sparse_output=False)</code> on a one-column matrix.", "O(n·k)", "O(n·k)"))


@B
def one_hot(values):
    cats = sorted(set(values))
    rows = []
    for v in values:
        rows.append([1.0 if v == c else 0.0 for c in cats])
    return rows


@O
def one_hot(values):
    enc = OneHotEncoder(sparse_output=False)
    return enc.fit_transform(np.array(values).reshape(-1, 1))


Q(None, "Label Encoding", "Easy", "Classes → 0, 1, 2, …",
  "Map each label to its position in the sorted list of distinct labels.",
  [((["cat", "dog", "cat", "bird"],), [1, 2, 1, 0]), (([30, 10, 20, 10],), [2, 0, 1, 0])],
  ("Build a dict from sorted unique labels to positions, look each one up.", "O(n log n)", "O(k)"),
  ("<code>LabelEncoder().fit_transform(y)</code> (meant for targets, not features).", "O(n log n)", "O(k)"))


@B
def label_encode(labels):
    lookup = {}
    for i, lab in enumerate(sorted(set(labels))):
        lookup[lab] = i
    return [lookup[lab] for lab in labels]


@O
def label_encode(labels):
    return LabelEncoder().fit_transform(labels)


Q(None, "Ordinal Encoding With an Order", "Easy", "Low < Medium < High",
  "Encode each value by its position in the given order list.",
  [((["low", "high", "medium", "low"], ["low", "medium", "high"]), [0.0, 2.0, 1.0, 0.0]), ((["S", "XL"], ["S", "M", "L", "XL"]), [0.0, 3.0])],
  ("<code>order.index(value)</code> for each value.", "O(n·k)", "O(n)"),
  ("<code>OrdinalEncoder(categories=[order])</code>.", "O(n log k)", "O(n)"),
  names=["values", "order"])


@B
def ordinal(values, order):
    return [float(order.index(v)) for v in values]


@O
def ordinal(values, order):
    enc = OrdinalEncoder(categories=[order])
    return enc.fit_transform(np.array(values).reshape(-1, 1)).ravel()


Q(None, "Fill Missing Values With the Mean", "Easy", "Imputation",
  "None marks a missing value. Replace it with its column's mean (computed from the values present). Round to 4 decimals.",
  [(([[1, None], [3, 4], [None, 8]],), [[1.0, 6.0], [3.0, 4.0], [2.0, 8.0]]), (([[None], [2], [4]],), [[3.0], [2.0], [4.0]])],
  ("Per column, average the non-missing values, then fill the gaps.", "O(n·d)", "O(d)"),
  ("<code>SimpleImputer(strategy='mean')</code> (NaN marks missing).", "O(n·d)", "O(d)"))


@B
def impute_mean(rows):
    d = len(rows[0])
    means = []
    for j in range(d):
        present = [r[j] for r in rows if r[j] is not None]
        means.append(sum(present) / len(present))
    return [[round(r[j] if r[j] is not None else means[j], 4) for j in range(d)] for r in rows]


@O
def impute_mean(rows):
    X = np.array([[np.nan if v is None else v for v in r] for r in rows], dtype=float)
    return SimpleImputer(strategy="mean").fit_transform(X).round(4)


Q(None, "Fill Missing Categories With the Mode", "Easy", "Most frequent value",
  "Replace None with the most common category (ties → alphabetically first).",
  [((["a", None, "b", "a", None],), ['a', 'a', 'b', 'a', 'a']), ((["x", "y", None],), ['x', 'y', 'x'])],
  ("Count the present values, pick the winner, fill.", "O(n)", "O(k)"),
  ("<code>SimpleImputer(strategy='most_frequent')</code>.", "O(n)", "O(k)"))


@B
def impute_mode(values):
    counts = {}
    for v in values:
        if v is not None:
            counts[v] = counts.get(v, 0) + 1
    best = max(counts.values())
    mode = min(v for v, c in counts.items() if c == best)
    return [mode if v is None else v for v in values]


@O
def impute_mode(values):
    X = np.array(values, dtype=object).reshape(-1, 1)
    imp = SimpleImputer(strategy="most_frequent", missing_values=None)
    return imp.fit_transform(X).ravel().tolist()


Q(None, "Polynomial Features", "Medium", "x₁, x₂ → x₁, x₂, x₁², x₁x₂, x₂²",
  "For rows with two features, return [x1, x2, x1², x1·x2, x2²] for each row.",
  [(([[2, 3], [1, -1]],), [[2.0, 3.0, 4.0, 6.0, 9.0], [1.0, -1.0, 1.0, -1.0, 1.0]])],
  ("Compute the five terms by hand for each row.", "O(n)", "O(n)"),
  ("<code>PolynomialFeatures(degree=2, include_bias=False)</code>.", "O(n)", "O(n)"))


@B
def poly2(rows):
    out = []
    for x1, x2 in rows:
        out.append([x1, x2, x1 * x1, x1 * x2, x2 * x2])
    return out


@O
def poly2(rows):
    return PolynomialFeatures(degree=2, include_bias=False).fit_transform(rows)


Q(None, "Equal-Width Binning", "Medium", "Numbers → bins",
  "Split the range [min, max] into k equal-width bins and return each value's bin number (0 … k − 1; the max goes in the last bin).",
  [(([1, 2, 3, 4, 5, 10], 3), [0.0, 0.0, 0.0, 1.0, 1.0, 2.0]), (([0, 5, 10], 2), [0.0, 1.0, 1.0])],
  ("Width = (max − min)/k; bin = floor((x − min)/width), capped at k − 1.", "O(n)", "O(n)"),
  ("<code>KBinsDiscretizer(n_bins=k, encode='ordinal', strategy='uniform')</code>.", "O(n)", "O(n)"),
  names=["values", "k"])


@B
def bins(values, k):
    lo, hi = min(values), max(values)
    width = (hi - lo) / k
    return [float(min(int((x - lo) / width), k - 1)) for x in values]


@O
def bins(values, k):
    kb = KBinsDiscretizer(n_bins=k, encode="ordinal", strategy="uniform")
    return kb.fit_transform(np.array(values, dtype=float).reshape(-1, 1)).ravel()


Q(None, "Log Transform a Skewed Feature", "Easy", "log(1 + x)",
  "Return log(1 + x) for each value, rounded to 4 decimals — tames long right tails like incomes.",
  [(([0, 9, 99, 999],), [0.0, 2.3026, 4.6052, 6.9078])],
  ("<code>math.log1p</code> in a loop.", "O(n)", "O(n)"),
  ("<code>FunctionTransformer(np.log1p)</code> — a transformer you can put in a pipeline.", "O(n)", "O(n)"))


@B
def log_transform(values):
    return [round(math.log1p(x), 4) for x in values]


@O
def log_transform(values):
    ft = FunctionTransformer(np.log1p)
    return ft.fit_transform(np.array(values, dtype=float).reshape(-1, 1)).ravel().round(4)


Q(None, "Balanced Class Weights", "Medium", "Help the rare class",
  "Return {class: weight} with weight = n_samples / (n_classes × count of that class), rounded to 4 decimals.",
  [(([0, 0, 0, 0, 1],), {0: 0.625, 1: 2.5}), ((["a", "b", "b", "c", "c", "c"],), {'a': 2.0, 'b': 1.0, 'c': 0.6667})],
  ("Count each class and apply the formula.", "O(n)", "O(k)"),
  ("<code>compute_class_weight('balanced', classes=…, y=…)</code>.", "O(n)", "O(k)"))


@B
def class_weights(y):
    counts = {}
    for label in y:
        counts[label] = counts.get(label, 0) + 1
    k = len(counts)
    return {c: round(len(y) / (k * counts[c]), 4) for c in sorted(counts)}


@O
def class_weights(y):
    classes = np.unique(y)
    w = compute_class_weight("balanced", classes=classes, y=np.array(y))
    return {c: round(x, 4) for c, x in zip(classes.tolist(), w)}


Q(None, "Drop Near-Constant Features", "Easy", "Variance threshold",
  "Return the indices of columns whose (population) variance is greater than threshold.",
  [(([[1, 5, 0], [1, 6, 0], [1, 7, 1]], 0.1), [1, 2]), (([[2, 2], [2, 2]], 0.0), [])],
  ("Variance of each column with loops; keep the ones above the threshold.", "O(n·d)", "O(d)"),
  ("<code>VarianceThreshold(threshold).fit(X).get_support(indices=True)</code>.", "O(n·d)", "O(d)"),
  names=["X", "threshold"])


@B
def keep_varied(X, threshold):
    keep = []
    for j in range(len(X[0])):
        col = [r[j] for r in X]
        mean = sum(col) / len(col)
        var = sum((v - mean) ** 2 for v in col) / len(col)
        if var > threshold:
            keep.append(j)
    return keep


@O
def keep_varied(X, threshold):
    try:
        return VarianceThreshold(threshold).fit(X).get_support(indices=True)
    except ValueError:  # every feature removed
        return []


Q(None, "Select the k Best Features", "Medium", "Correlation with the target",
  "Return the indices (sorted) of the k columns most correlated (by |r|) with the target y.",
  [(([[1, 5, 3], [2, 3, 3.5], [3, 4, 2], [4, 1, 3.1]], [2, 4, 6, 8], 2), [0, 1])],
  ("Pearson r of every column with y by hand, take the k largest |r|.", "O(n·d)", "O(d)"),
  ("<code>SelectKBest(f_regression, k=k)</code> — its F-score ranks features exactly like r².", "O(n·d)", "O(d)"),
  names=["X", "y", "k"])


@B
def k_best(X, y, k):
    my = sum(y) / len(y)
    scores = []
    for j in range(len(X[0])):
        col = [r[j] for r in X]
        mx = sum(col) / len(col)
        sxy = sum((a - mx) * (b - my) for a, b in zip(col, y))
        sxx = sum((a - mx) ** 2 for a in col)
        syy = sum((b - my) ** 2 for b in y)
        scores.append(abs(sxy / math.sqrt(sxx * syy)))
    best = sorted(range(len(scores)), key=lambda j: -scores[j])[:k]
    return sorted(best)


@O
def k_best(X, y, k):
    return SelectKBest(f_regression, k=k).fit(X, y).get_support(indices=True)


Q(None, "K-Fold Splits", "Medium", "Every row is tested once",
  "Split n rows (in order) into k folds; return each fold's test indices. The first n mod k folds get one extra row.",
  [((10, 3), [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]), ((6, 3), [[0, 1], [2, 3], [4, 5]])],
  ("Fold sizes n // k, plus one for the first n % k folds; walk through the indices.", "O(n)", "O(n)"),
  ("<code>KFold(n_splits=k).split(X)</code>.", "O(n)", "O(n)"),
  names=["n", "k"])


@B
def kfold(n, k):
    folds, start = [], 0
    for i in range(k):
        size = n // k + (1 if i < n % k else 0)
        folds.append(list(range(start, start + size)))
        start += size
    return folds


@O
def kfold(n, k):
    return [test.tolist() for _, test in KFold(n_splits=k).split(np.zeros((n, 1)))]


Q(None, "Normalise Each Row", "Easy", "Unit-length samples",
  "Divide each row by its Euclidean length (useful for text vectors). Round to 4 decimals.",
  [(([[3, 4], [1, 0], [1, 1]],), [[0.6, 0.8], [1.0, 0.0], [0.7071, 0.7071]])],
  ("Length of each row by hand, then divide.", "O(n·d)", "O(n·d)"),
  ("<code>Normalizer()</code> (works row by row, unlike scalers).", "O(n·d)", "O(n·d)"))


@B
def normalise_rows(rows):
    out = []
    for r in rows:
        length = math.sqrt(sum(v * v for v in r))
        out.append([round(v / length, 4) for v in r])
    return out


@O
def normalise_rows(rows):
    return Normalizer().fit_transform(rows).round(4)


Q(None, "A Scale-Then-Fit Pipeline", "Medium", "Pipelines prevent leakage",
  "Fit standard scaling + linear regression on (x_train, y_train) — one feature — and predict for x_test. Round to 4 decimals.",
  [(([1, 2, 3, 4], [3, 5, 7, 9], [5, 10]), [11.0, 21.0]), (([0, 1, 2], [1, 1, 4], [1.5]), [2.75])],
  ("Scale x by hand, fit slope/intercept on the scaled values, scale the test x the same way, predict.", "O(n)", "O(1)"),
  ("<code>make_pipeline(StandardScaler(), LinearRegression())</code> — one object that fits and predicts in order.", "O(n)", "O(n)"),
  names=["x_train", "y_train", "x_test"])


@B
def pipeline_predict(x_train, y_train, x_test):
    n = len(x_train)
    mean = sum(x_train) / n
    std = math.sqrt(sum((x - mean) ** 2 for x in x_train) / n)
    z = [(x - mean) / std for x in x_train]
    my = sum(y_train) / n
    slope = sum(a * (b - my) for a, b in zip(z, y_train)) / sum(a * a for a in z)
    return [round(my + slope * (x - mean) / std, 4) for x in x_test]


@O
def pipeline_predict(x_train, y_train, x_test):
    model = make_pipeline(StandardScaler(), LinearRegression())
    model.fit(np.array(x_train).reshape(-1, 1), y_train)
    return model.predict(np.array(x_test).reshape(-1, 1)).round(4)
