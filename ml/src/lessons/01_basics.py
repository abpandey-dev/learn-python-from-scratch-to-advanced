from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
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
