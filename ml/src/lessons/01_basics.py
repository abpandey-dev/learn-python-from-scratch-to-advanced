from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

LESSON("Basics", "What is machine learning?", """
<p>Normal programming: you write the rules, the computer applies them. <b>Machine learning</b>: you give the computer <b>examples</b> and it works out the rules itself.</p>
<ul>
<li><b>Features</b> X: the inputs (house size, rooms, age). One row per example, one column per feature.</li>
<li><b>Target / label</b> y: what we want to predict (price).</li>
<li><b>Model</b>: a function with adjustable numbers (<b>parameters</b>) that maps X to a prediction ŷ.</li>
<li><b>Training</b>: adjusting the parameters so ŷ is close to y on known examples.</li>
</ul>
<table><tr><th>Type</th><th>Has labels?</th><th>Examples</th></tr>
<tr><td><b>Regression</b> (supervised)</td><td>yes, numbers</td><td>price, temperature, demand</td></tr>
<tr><td><b>Classification</b> (supervised)</td><td>yes, categories</td><td>spam / not spam, disease, digit 0–9</td></tr>
<tr><td><b>Clustering</b> (unsupervised)</td><td>no</td><td>customer segments</td></tr>
</table>
""", practice=["Majority-Class Baseline", "Mean Baseline for Regression"])


@LD
def first_model():
    size = np.array([50, 70, 80, 100, 120, 150])
    price = np.array([150, 200, 230, 280, 330, 400])
    slope, intercept = np.polyfit(size, price, 1)
    prediction_for_90 = slope * 90 + intercept
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(size, price, label="examples (X, y)")
    ax.plot(size, slope * size + intercept, color="#b45309", label="learned rule")
    ax.plot(90, prediction_for_90, "k*", markersize=12, label="new house")
    ax.set_xlabel("size (m²)")
    ax.set_ylabel("price (k)")
    ax.legend(fontsize=7)


LESSON("Basics", "Train, validation and test sets", """
<p>A model can memorise its training data and still fail on new data. So we always hold some data back:</p>
<ul>
<li><b>Training set</b> (~60–80%): the model learns from it.</li>
<li><b>Validation set</b> (or cross-validation): used to choose settings and compare models.</li>
<li><b>Test set</b> (~20%): touched <b>once</b>, at the very end, to estimate real-world performance.</li>
</ul>
<p>Always compare against a <b>baseline</b> — predict the most common class, or the average value. A 95% accurate model is useless if 95% of emails aren't spam anyway.</p>
<p>In sklearn: <code>train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)</code>. <code>stratify</code> keeps class proportions the same in both parts.</p>
""", practice=["Train / Test Split Without Shuffling", "K-Fold Splits", "Majority-Class Baseline"])


@LD
def split_demo():
    X = np.arange(20).reshape(-1, 1)
    y = np.array([0] * 14 + [1] * 6)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
    train_share_of_1 = y_train.mean()
    test_share_of_1 = y_test.mean()


LESSON("Core", "Scaling features", """
<p>Many algorithms (k-NN, SVM, neural networks, gradient descent, PCA) treat features by their raw numbers. If income is in the tens of thousands and age in tens, income dominates. <b>Scaling</b> puts features on comparable ranges:</p>
<table><tr><th>Scaler</th><th>Formula</th><th>When</th></tr>
<tr><td>StandardScaler</td><td>(x − mean)/std</td><td>default choice</td></tr>
<tr><td>MinMaxScaler</td><td>(x − min)/(max − min)</td><td>need [0, 1] (images, NN inputs)</td></tr>
<tr><td>RobustScaler</td><td>(x − median)/IQR</td><td>outliers present</td></tr>
<tr><td>log1p</td><td>log(1 + x)</td><td>long right tail (income, counts)</td></tr></table>
<p><b>Golden rule</b>: fit the scaler on the <b>training</b> data only, then apply the same numbers to the test data. Fitting on all the data leaks test information into training (<b>data leakage</b>). Trees don't need scaling.</p>
""", practice=["Standard Scaling (Fit on Train Only)", "Min-Max Scaling", "Robust Scaling", "Log Transform a Skewed Feature", "Normalise Each Row"])


@LD
def scaling_demo():
    rng = np.random.default_rng(0)
    income = rng.normal(50000, 15000, 200)
    age = rng.normal(40, 12, 200)
    scaled = StandardScaler().fit_transform(np.column_stack([income, age]))
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    left.scatter(income, age, s=8)
    left.set_title("raw: income dominates", fontsize=9)
    right.scatter(scaled[:, 0], scaled[:, 1], s=8, color="#b45309")
    right.set_title("standardised: comparable", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Encoding categories and filling missing values", """
<p>Models need numbers. For categorical columns:</p>
<ul>
<li><b>One-hot encoding</b>: one 0/1 column per category (colour → is_red, is_green, is_blue). Safe default for unordered categories.</li>
<li><b>Ordinal encoding</b>: low → 0, medium → 1, high → 2 — only when the order is real.</li>
<li><b>Label encoding</b>: for the <b>target</b> of a classifier.</li>
</ul>
<p><b>Missing values</b>: drop rows if very few, otherwise <b>impute</b> — mean or median for numbers, most frequent for categories (learned on train only!). Adding a "was missing" flag column can help, because missingness itself can be informative.</p>
""", practice=["One-Hot Encoding", "Ordinal Encoding With an Order", "Label Encoding", "Fill Missing Values With the Mean", "Fill Missing Categories With the Mode"])


@LD
def encode_demo():
    colours = np.array(["red", "green", "blue", "green"])
    categories = np.unique(colours)
    one_hot = (colours[:, None] == categories).astype(int)
    sizes = ["low", "high", "medium"]
    order = ["low", "medium", "high"]
    ordinal = [order.index(s) for s in sizes]


LESSON("Advanced", "Feature engineering, selection and pipelines", """
<p>Better features usually beat fancier models:</p>
<ul>
<li><b>Create</b>: polynomial terms (x², x₁x₂) let linear models bend; ratios (price per m²); dates → day of week, month; text → word counts; bins for non-linear effects.</li>
<li><b>Select</b>: drop near-constant columns, keep the k most related to the target, or let regularisation (Lasso) or tree importances decide.</li>
<li><b>Imbalanced classes</b>: <code>class_weight="balanced"</code> makes rare-class mistakes cost more.</li>
</ul>
<p>A <b>Pipeline</b> chains preprocessing and the model into one object: <code>make_pipeline(StandardScaler(), LogisticRegression())</code>. It fits every step on training data only, so cross-validation stays leak-free, and one call deploys the whole thing.</p>
""", practice=["Polynomial Features", "Equal-Width Binning", "Drop Near-Constant Features", "Select the k Best Features", "Balanced Class Weights", "A Scale-Then-Fit Pipeline"])


@LD
def poly_demo():
    x = np.linspace(-3, 3, 30)
    y = x ** 2 + np.sin(3 * x) * 0.5
    straight = np.polyval(np.polyfit(x, y, 1), x)
    curved = np.polyval(np.polyfit(x, y, 2), x)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y, s=10)
    ax.plot(x, straight, label="features: x")
    ax.plot(x, curved, label="features: x, x²")
    ax.legend(fontsize=8)
    ax.set_title("Adding x² lets a linear model curve", fontsize=9)


LESSON("Basics", "Choosing the right kind of model", """
<p>Before any code, turn the question into a machine-learning task. Ask three things:</p>
<ol>
<li><b>Do I have the answers for past examples?</b> Yes means supervised learning. No means unsupervised.</li>
<li><b>What kind of answer do I want?</b> A number means regression. A category means classification.</li>
<li><b>How will I know it worked?</b> Pick the metric and the baseline before training.</li>
</ol>
<table><tr><th>Question</th><th>Task</th><th>First model to try</th><th>Baseline</th></tr>
<tr><td>What price will this flat sell for?</td><td>regression</td><td>linear regression, then boosting</td><td>the average price</td></tr>
<tr><td>Is this transaction fraud?</td><td>binary classification</td><td>logistic regression, then boosting</td><td>"never fraud"</td></tr>
<tr><td>Which topic is this article about?</td><td>multi-class classification</td><td>Naive Bayes or logistic regression</td><td>the most common topic</td></tr>
<tr><td>Which customers are alike?</td><td>clustering</td><td>k-means</td><td>none: judge usefulness</td></tr>
</table>
<h4>A checklist for every dataset</h4>
<ul>
<li>How many rows and columns? What does one row mean?</li>
<li>Which columns are numbers, categories, dates or free text?</li>
<li>How many values are missing, and is that pattern meaningful?</li>
<li>Is the target balanced? Are there duplicates or impossible values?</li>
<li>Would each column really be known at prediction time? If not, it leaks.</li>
</ul>
""", practice=["Majority-Class Baseline", "Mean Baseline for Regression"])


@LD
def explore_first():
    df = pd.DataFrame({"size": [50, 70, None, 100, 120, 900], "city": ["Pune", "Delhi", "Pune", None, "Pune", "Delhi"], "price": [150, 200, 230, 280, 330, 2500]})
    shape = df.shape
    missing = df.isna().sum()
    summary = df["size"].describe()
    city_counts = df["city"].value_counts()
    suspicious_rows = df[df["size"] > 500]


LESSON("Core", "Leakage, worked by hand", """
<p><b>Idea:</b> a model must only learn from what it would have at prediction time. Fitting a scaler on the full data quietly breaks this.</p>
<h4>Worked example</h4>
<p>Training values are 1, 2, 3 and the only test value is 10.</p>
<table><tr><th></th><th>Correct: fit on train</th><th>Leaky: fit on all data</th></tr>
<tr><td>Mean</td><td>2</td><td>4</td></tr>
<tr><td>Standard deviation</td><td>0.816</td><td>3.536</td></tr>
<tr><td>Scaled test value</td><td>(10 − 2) / 0.816 = <b>9.80</b></td><td>(10 − 4) / 3.536 = <b>1.70</b></td></tr>
</table>
<p>The correct version says plainly that 10 is far outside anything seen in training. The leaky version makes it look ordinary, because the outlier helped set the scale. The model was evaluated on data that had already shaped its inputs, so the score can't be trusted.</p>
<h4>Common mistakes</h4>
<ul>
<li>Calling <code>fit_transform</code> on the test set. Use <code>transform</code>.</li>
<li>Selecting features, or filling missing values, before splitting.</li>
<li>A column recorded after the outcome, such as "days in hospital" when predicting admission.</li>
<li>Shuffling time-series data, which lets the model see the future.</li>
</ul>
<p><b>Warning sign:</b> a score that looks too good. Check which feature is doing the work.</p>
""", practice=["Standard Scaling (Fit on Train Only)", "A Scale-Then-Fit Pipeline"])


@LD
def leakage_numbers():
    train = np.array([1.0, 2.0, 3.0])
    test_value = 10.0
    correct = (test_value - train.mean()) / train.std()
    everything = np.append(train, test_value)
    leaky = (test_value - everything.mean()) / everything.std()


LESSON("Core", "Imbalanced classes", """
<p><b>Idea:</b> when one class is rare, a model can score highly by ignoring it. If 95 of 100 emails are fine, predicting "fine" every time is 95% accurate and catches nothing.</p>
<h4>Worked example: balanced class weights</h4>
<p>weight = n_samples / (n_classes × count of that class)</p>
<table><tr><th>Class</th><th>Count</th><th>Weight</th></tr>
<tr><td>Normal</td><td>95</td><td>100 / (2 × 95) = 0.526</td></tr>
<tr><td>Fraud</td><td>5</td><td>100 / (2 × 5) = 10</td></tr></table>
<p>Each fraud row now counts 19 times as much as a normal row, so both classes contribute equally to the loss.</p>
<h4>What you can do, in the order to try it</h4>
<ol>
<li>Use a metric that sees the rare class: recall, precision, F1 or PR-AUC.</li>
<li>Use <code>stratify=y</code> when splitting, so every part contains the rare class.</li>
<li>Set <code>class_weight="balanced"</code>.</li>
<li>Move the decision threshold instead of staying at 0.5.</li>
<li>Resample the <b>training</b> data only. Oversampling before the split copies rows into the test set, which is leakage.</li>
</ol>
""", practice=["Balanced Class Weights", "Majority-Class Baseline"])


@LD
def imbalance_trap():
    y_true = np.array([0] * 95 + [1] * 5)
    always_normal = np.zeros(100, dtype=int)
    accuracy = (always_normal == y_true).mean()
    frauds_caught = always_normal[y_true == 1].sum()
    weight_normal = 100 / (2 * 95)
    weight_fraud = 100 / (2 * 5)
    balance = (95 * weight_normal, 5 * weight_fraud)


LESSON("Advanced", "A complete small project, start to finish", """
<p>Here is every step on one small dataset. The demo below runs all of them.</p>
<ol>
<li><b>Define:</b> predict the flat price; measure with mean absolute error (MAE).</li>
<li><b>Split first:</b> hold out a test set before looking closely at anything.</li>
<li><b>Baseline:</b> always predict the training average, and record its error.</li>
<li><b>Prepare:</b> fill missing sizes, scale numbers and one-hot encode the city, all inside one pipeline.</li>
<li><b>Train and compare:</b> the model must beat the baseline.</li>
<li><b>Test once:</b> report that score, and don't tune after seeing it.</li>
<li><b>Inspect errors:</b> which rows are worst, and why?</li>
</ol>
<p>Real projects spend most of their time on steps 1–4 and step 7.</p>
""", practice=["A Scale-Then-Fit Pipeline", "Train / Test Split Without Shuffling", "Mean Baseline for Regression"])


@LD
def whole_project():
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import OneHotEncoder
    rng = np.random.default_rng(0)
    size = rng.uniform(40, 150, 60)
    city = rng.choice(["Pune", "Delhi"], 60)
    price = 3 * size + np.where(city == "Delhi", 60, 0) + rng.normal(0, 15, 60)
    df = pd.DataFrame({"size": size, "city": city})
    df.loc[::10, "size"] = np.nan
    X_train, X_test, y_train, y_test = train_test_split(df, price, test_size=0.25, random_state=0)
    baseline_mae = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
    prep = ColumnTransformer([("num", make_pipeline(SimpleImputer(), StandardScaler()), ["size"]), ("cat", OneHotEncoder(), ["city"])])
    model = make_pipeline(prep, LinearRegression()).fit(X_train, y_train)
    model_mae = mean_absolute_error(y_test, model.predict(X_test))
    fig, ax = plt.subplots(figsize=(4.5, 2.6))
    ax.bar(["baseline", "model"], [baseline_mae, model_mae], color=["#9ca3af", "#0f766e"])
    ax.set_ylabel("test MAE (lower is better)")
