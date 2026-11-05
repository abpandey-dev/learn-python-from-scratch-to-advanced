from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

PTS = np.array([[1, 1], [2, 1], [1, 2], [6, 5], [7, 7], [6, 7], [4, 3], [3, 5], [5, 2]], dtype=float)
LAB = np.array([0, 0, 0, 1, 1, 1, 0, 1, 0])


def regions(ax, model, title):
    xx, yy = np.meshgrid(np.linspace(0, 8, 150), np.linspace(0, 8, 150))
    zz = model.predict(np.column_stack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    ax.contourf(xx, yy, zz, alpha=0.25, cmap="coolwarm")
    ax.scatter(PTS[:, 0], PTS[:, 1], c=LAB, cmap="coolwarm", edgecolor="black")
    ax.set_title(title, fontsize=8)


LESSON("Basics", "k-nearest neighbours: ask the neighbours", """
<p>The simplest classifier: to label a new point, find the <b>k closest</b> training points and take a <b>majority vote</b> (for regression, average their values). There is no training step — the model is the data.</p>
<ul>
<li><b>Small k</b> (k = 1): follows every point — wiggly boundary, overfits noise.</li>
<li><b>Large k</b>: smooth boundary, may underfit. Choose k with validation; use an odd k for two classes to avoid ties.</li>
<li><b>Scale features</b> first — distance is everything. Optionally weight votes by 1/distance.</li>
<li>Prediction is slow on big data (compare with every point) and suffers in many dimensions (the "curse of dimensionality").</li>
</ul>
""", practice=["Distances to Every Training Point", "Classify One Point With k-NN", "k-NN for Many Points", "k-NN With Manhattan Distance", "Choose k on a Validation Set"])


@LD
def knn_regions():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, k in zip(axes, [1, 5]):
        regions(ax, KNeighborsClassifier(n_neighbors=k).fit(PTS, LAB), f"k = {k}")
    fig.tight_layout()


LESSON("Core", "k-NN for numbers", """
<p>k-NN regression predicts the average target of the k nearest neighbours. With <code>weights="distance"</code>, closer neighbours count more (weight 1/distance), which makes predictions pass through the training points and change smoothly between them.</p>
""", practice=["k-NN Regression", "Distance-Weighted k-NN"])


@LD
def knn_regression_curve():
    from sklearn.neighbors import KNeighborsRegressor
    x = np.array([1, 2, 3, 5, 8, 9], dtype=float)
    y = np.array([10, 12, 15, 20, 30, 33], dtype=float)
    grid = np.linspace(0, 10, 300).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y, zorder=3)
    for weights in ["uniform", "distance"]:
        model = KNeighborsRegressor(n_neighbors=3, weights=weights).fit(x.reshape(-1, 1), y)
        ax.plot(grid, model.predict(grid), label=weights)
    ax.legend(fontsize=8)


LESSON("Core", "Naive Bayes: Bayes' rule with a shortcut", """
<p>Naive Bayes picks the class with the highest P(class | features) ∝ P(class) × P(features | class). The "naive" shortcut assumes features are independent given the class, so P(features | class) is just a product of one-feature probabilities — easy to learn from little data, and very fast.</p>
<table><tr><th>Variant</th><th>Features</th><th>Each P(feature | class)</th></tr>
<tr><td>GaussianNB</td><td>numbers</td><td>a bell curve with the class's mean and variance</td></tr>
<tr><td>MultinomialNB</td><td>word counts</td><td>(count + α)/(total + α·vocab) — <b>Laplace smoothing</b> avoids zero probabilities</td></tr>
<tr><td>BernoulliNB</td><td>present / absent</td><td>share of the class's documents containing the word</td></tr></table>
<p>Computed with log-probabilities (sums, not products) to avoid underflow. Great baseline for text and spam filtering; probabilities tend to be over-confident.</p>
""", practice=["Class Priors", "Gaussian Naive Bayes: Means per Class", "Gaussian Naive Bayes: Variances per Class", "Gaussian Naive Bayes: Predict Probabilities", "Word Probabilities With Laplace Smoothing", "Multinomial Naive Bayes Classifier", "Bernoulli Naive Bayes"])


@LD
def gnb_regions():
    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    regions(ax, GaussianNB().fit(PTS, LAB), "Gaussian NB: curved boundary")


LESSON("Advanced", "Support vector machines: the widest street", """
<p>Many lines separate two classes. An <b>SVM</b> picks the one with the widest <b>margin</b> — the widest street with no points on it. Only the points on the edge of the street, the <b>support vectors</b>, decide where it goes.</p>
<ul>
<li>Margin width = 2/‖w‖, so maximising the margin = minimising ‖w‖ subject to y·(w·x + b) ≥ 1.</li>
<li><b>Soft margin</b>: real data overlaps, so violations are allowed at a cost — the <b>hinge loss</b> max(0, 1 − y·score). <b>C</b> trades margin width against violations (large C = fewer violations, narrower margin).</li>
</ul>
""", practice=["Hinge Loss", "Widest Margin Between Two Points", "Margin Width", "Points Inside the Margin"])


@LD
def svm_margin():
    model = SVC(kernel="linear", C=10).fit(PTS, LAB)
    w, b = model.coef_[0], model.intercept_[0]
    xs = np.linspace(0, 8, 50)
    fig, ax = plt.subplots(figsize=(4, 3.4))
    ax.scatter(PTS[:, 0], PTS[:, 1], c=LAB, cmap="coolwarm", edgecolor="black")
    for offset, style in [(0, "-"), (1, "--"), (-1, "--")]:
        ax.plot(xs, (offset - b - w[0] * xs) / w[1], style, color="black")
    sv = model.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=200, facecolors="none", edgecolors="#b45309")
    ax.set_ylim(0, 8)
    ax.set_title(f"margin = {2 / np.linalg.norm(w):.2f}; circled = support vectors", fontsize=8)


LESSON("Advanced", "Kernels: curved boundaries for free", """
<p>When classes aren't linearly separable, map points to a bigger space where they are (e.g. add x², xy, y²). The <b>kernel trick</b>: SVMs only ever need dot products between points, and a <b>kernel</b> computes the dot product in the big space directly from the original points — without building it.</p>
<table><tr><th>Kernel</th><th>K(x, z)</th></tr>
<tr><td>Linear</td><td>x·z</td></tr>
<tr><td>Polynomial</td><td>(γ x·z + r)ᵈ</td></tr>
<tr><td>RBF (Gaussian)</td><td>exp(−γ‖x − z‖²) — the default; γ controls how local the boundary is</td></tr></table>
<p>Tune C and γ together with cross-validation, and always scale features.</p>
""", practice=["RBF Kernel", "The Kernel Trick"])


@LD
def rbf_regions():
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, gamma in zip(axes, [0.1, 2.0]):
        regions(ax, SVC(kernel="rbf", gamma=gamma, C=10).fit(PTS, LAB), f"RBF SVM, γ = {gamma}")
    fig.tight_layout()


LESSON("Basics", "k-NN worked by hand", """
<p>Training points: three of class 0 and two of class 1. Classify the new point q = (3, 2) with k = 3.</p>
<table><tr><th>Point</th><th>Class</th><th>Distance to q</th><th>Rank</th></tr>
<tr><td>(2, 1)</td><td>0</td><td>√(1 + 1) = 1.414</td><td>1</td></tr>
<tr><td>(1, 2)</td><td>0</td><td>√(4 + 0) = 2.000</td><td>2</td></tr>
<tr><td>(1, 1)</td><td>0</td><td>√(4 + 1) = 2.236</td><td>3</td></tr>
<tr><td>(6, 5)</td><td>1</td><td>√(9 + 9) = 4.243</td><td></td></tr>
<tr><td>(7, 7)</td><td>1</td><td>√(16 + 25) = 6.403</td><td></td></tr></table>
<p>All three nearest points are class 0, so the prediction is <b>class 0</b>, with probability 3/3.</p>
<h4>Why scaling is essential</h4>
<p>Compare a person (income 50,000, age 25) with two others:</p>
<ul>
<li>(51,000, age <b>60</b>): distance ≈ 1,000.6</li>
<li>(58,000, age <b>26</b>): distance ≈ 8,000.0</li>
</ul>
<p>A person 35 years older counts as far closer, because income's large numbers swamp age. After standardising, both features count fairly.</p>
<h4>Choosing k</h4>
<ul><li>k = 1 memorises the data: training accuracy is 100% and noise shapes the boundary.</li>
<li>Very large k approaches the majority class everywhere.</li>
<li>Plot validation accuracy against k and choose the peak.</li></ul>
""", practice=["Distances to Every Training Point", "Classify One Point With k-NN", "Choose k on a Validation Set"])


@LD
def knn_by_hand():
    X = np.array([[1, 1], [2, 1], [1, 2], [6, 5], [7, 7]], dtype=float)
    y = np.array([0, 0, 0, 1, 1])
    q = np.array([3.0, 2.0])
    d = np.sqrt(((X - q) ** 2).sum(axis=1))
    nearest = np.argsort(d)[:3]
    votes = y[nearest]
    prediction = np.bincount(votes).argmax()
    near_in_income = math.dist((50000, 25), (51000, 60))
    near_in_age = math.dist((50000, 25), (58000, 26))


LESSON("Core", "The curse of dimensionality", """
<p>k-NN assumes that nearby points are similar. In many dimensions, that assumption fails: <b>everything becomes about equally far away.</b></p>
<p>The demo draws random points and compares the nearest and farthest distance from a query. As dimensions grow, the ratio approaches 1, so "nearest" stops meaning much.</p>
<p>There's a simple intuition: to cover 10% of the data along one feature you need 10% of its range. To cover 10% of the data in 10 dimensions, you need about 79% of the range of every feature (0.1^(1/10) ≈ 0.79). Your "local" neighbourhood is no longer local.</p>
<h4>What to do</h4>
<ul><li>Remove irrelevant features, since each one adds pure noise to the distance.</li>
<li>Reduce dimensions with PCA first.</li>
<li>Use a model that picks features for itself, such as trees or regularised linear models.</li>
<li>For text and embeddings, use cosine similarity, which often behaves better.</li></ul>
<p><b>Speed:</b> plain k-NN compares against every row per prediction. KD-trees help in low dimensions, and approximate indexes (HNSW, FAISS) power the vector databases used in RAG systems, which are k-NN at scale.</p>
""", practice=["k-NN With Manhattan Distance", "k-NN for Many Points"])


@LD
def curse_demo():
    rng = np.random.default_rng(0)
    dims = [1, 2, 5, 10, 50, 100, 500]
    ratios = []
    for d in dims:
        points = rng.uniform(size=(500, d))
        query = rng.uniform(size=d)
        distances = np.sqrt(((points - query) ** 2).sum(axis=1))
        ratios.append(distances.min() / distances.max())
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.semilogx(dims, ratios, "o-")
    ax.set_xlabel("number of dimensions")
    ax.set_ylabel("nearest / farthest distance")
    ax.set_title("Close to 1 = 'nearest' means little", fontsize=9)


LESSON("Core", "Naive Bayes worked by hand: a spam filter", """
<p>Training counts: 40% of emails are spam. Word counts in each class:</p>
<table><tr><th>Word</th><th>In spam</th><th>In ham</th></tr>
<tr><td>free</td><td>4</td><td>1</td></tr><tr><td>win</td><td>3</td><td>0</td></tr><tr><td>hello</td><td>1</td><td>5</td></tr>
<tr><th>Total</th><th>8</th><th>6</th></tr></table>
<p>Classify the email "free win".</p>
<h4>Step 1: word probabilities with Laplace smoothing</h4>
<p>P(word | class) = (count + 1) / (total + vocabulary size), with vocabulary size 3.</p>
<table><tr><th></th><th>Spam</th><th>Ham</th></tr>
<tr><td>P(free)</td><td>5 / 11 = 0.455</td><td>2 / 9 = 0.222</td></tr>
<tr><td>P(win)</td><td>4 / 11 = 0.364</td><td>1 / 9 = 0.111</td></tr></table>
<p>Without smoothing, P(win | ham) would be 0, and one unseen word would zero out the whole class.</p>
<h4>Step 2: multiply prior × likelihoods</h4>
<ul><li>Spam: 0.4 × 0.455 × 0.364 = 0.0661</li>
<li>Ham: 0.6 × 0.222 × 0.111 = 0.0148</li></ul>
<h4>Step 3: normalise</h4>
<p>P(spam | email) = 0.0661 / (0.0661 + 0.0148) = <b>0.817</b>.</p>
<p><b>Why "naive"?</b> It treats "free" and "win" as independent, though they tend to appear together. So it counts the same evidence twice, and its probabilities are overconfident, yet the ranking is often good. Real code adds logs to avoid underflow.</p>
""", practice=["Word Probabilities With Laplace Smoothing", "Multinomial Naive Bayes Classifier", "Class Priors"])


@LD
def spam_by_hand():
    spam_counts = {"free": 4, "win": 3, "hello": 1}
    ham_counts = {"free": 1, "win": 0, "hello": 5}
    vocab = len(spam_counts)
    spam_total, ham_total = sum(spam_counts.values()), sum(ham_counts.values())
    spam_score, ham_score = 0.4, 0.6
    for word in ["free", "win"]:
        spam_score *= (spam_counts[word] + 1) / (spam_total + vocab)
        ham_score *= (ham_counts[word] + 1) / (ham_total + vocab)
    p_spam = spam_score / (spam_score + ham_score)


LESSON("Advanced", "Gaussian Naive Bayes worked by hand", """
<p>Guess group from height. Group A: 170, 175, 180 (mean 175). Group B: 155, 160, 165 (mean 160). Both have variance 16.67 and the priors are equal. Who is a person of height 168?</p>
<p>Use the bell-curve height f(x) = e^(−(x − μ)² / 2σ²) / √(2πσ²):</p>
<table><tr><th>Group</th><th>Distance from mean</th><th>f(168)</th></tr>
<tr><td>A</td><td>7</td><td>0.0225</td></tr><tr><td>B</td><td>8</td><td>0.0143</td></tr></table>
<p>P(A | 168) = 0.0225 / (0.0225 + 0.0143) = <b>0.611</b>. It's closer to A's mean, though not by much, so the model is only mildly confident.</p>
<p>With more features, multiply each feature's bell-curve value together. When variances differ between classes the boundary curves, which is what you saw in the earlier chart.</p>
<h4>Generative vs discriminative</h4>
<p>Naive Bayes is <b>generative</b>: it models how each class produces data, P(x | class). Logistic regression is <b>discriminative</b>: it models P(class | x) directly. Naive Bayes often wins with very little data, and logistic regression usually wins once there's more.</p>
""", practice=["Gaussian Naive Bayes: Means per Class", "Gaussian Naive Bayes: Variances per Class", "Gaussian Naive Bayes: Predict Probabilities"])


@LD
def gaussian_nb_by_hand():
    a, b = np.array([170.0, 175, 180]), np.array([155.0, 160, 165])

    def bell(x, group):
        mean, var = group.mean(), group.var()
        return math.exp(-(x - mean) ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var)

    height_a = bell(168, a)
    height_b = bell(168, b)
    p_a = height_a / (height_a + height_b)
    grid = np.linspace(145, 195, 200)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.plot(grid, [bell(v, a) for v in grid], label="group A")
    ax.plot(grid, [bell(v, b) for v in grid], label="group B")
    ax.axvline(168, color="black", ls="--")
    ax.legend(fontsize=8)


LESSON("Advanced", "The SVM objective, margin and C", """
<h4>Why the margin is 2 / ‖w‖</h4>
<p>The boundary is w·x + b = 0, and the street's edges are w·x + b = ±1. The distance from a point to the boundary is |w·x + b| / ‖w‖, so each edge is 1 / ‖w‖ away and the street is 2 / ‖w‖ wide. A wider street means a smaller ‖w‖.</p>
<h4>The objective has two competing goals</h4>
<p style="text-align:center"><b>minimise ½‖w‖² + C · Σ hinge losses</b></p>
<h4>Hinge loss, worked by hand: max(0, 1 − y·score)</h4>
<table><tr><th>y</th><th>Score</th><th>Loss</th><th>Meaning</th></tr>
<tr><td>+1</td><td>2.0</td><td>0</td><td>correct, outside the street</td></tr>
<tr><td>+1</td><td>0.5</td><td>0.5</td><td>correct, but inside the street</td></tr>
<tr><td>+1</td><td>−0.3</td><td>1.3</td><td>wrong side</td></tr>
<tr><td>−1</td><td>−1.5</td><td>0</td><td>correct, outside the street</td></tr></table>
<p>Points with zero loss have no effect on the model, and that's why only support vectors matter.</p>
<h4>The role of C</h4>
<ul><li><b>Small C:</b> wide street, tolerates mistakes, stronger regularisation.</li>
<li><b>Large C:</b> narrow street, tries to classify every point, and may overfit.</li></ul>
<p>Note that C works like logistic regression's C: bigger means <i>less</i> regularisation.</p>
""", practice=["Hinge Loss", "Margin Width", "Points Inside the Margin", "Widest Margin Between Two Points"])


@LD
def c_effect():
    rng = np.random.default_rng(2)
    X = np.vstack([rng.normal([2, 2], 0.9, (25, 2)), rng.normal([5, 5], 0.9, (25, 2))])
    y = np.r_[np.zeros(25, dtype=int), np.ones(25, dtype=int)]
    xs = np.linspace(0, 7.5, 30)
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3))
    for ax, c in zip(axes, [0.01, 100]):
        model = SVC(kernel="linear", C=c).fit(X, y)
        w, b = model.coef_[0], model.intercept_[0]
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=14, edgecolor="black", linewidth=0.3)
        for offset, style in [(0, "-"), (1, "--"), (-1, "--")]:
            ax.plot(xs, (offset - b - w[0] * xs) / w[1], style, color="black", linewidth=0.8)
        ax.set_ylim(0, 7.5)
        ax.set_title(f"C = {c}: margin {2 / np.linalg.norm(w):.2f}, {len(model.support_)} support vectors", fontsize=8)
    fig.tight_layout()


LESSON("Advanced", "The kernel trick, with real numbers", """
<p>Take x = (1, 2) and z = (3, 1). We want the dot product after mapping into a bigger space.</p>
<h4>The long way</h4>
<p>φ(v) = (1, √2·v₁, √2·v₂, v₁², √2·v₁v₂, v₂²), so</p>
<ul><li>φ(x) = (1, 1.414, 2.828, 1, 2.828, 4)</li><li>φ(z) = (1, 4.243, 1.414, 9, 4.243, 1)</li></ul>
<p>Their dot product is 1 + 6 + 4 + 9 + 12 + 4 = <b>36</b>.</p>
<h4>The shortcut</h4>
<p>x·z = 3 + 2 = 5, then (x·z + 1)² = 6² = <b>36</b>. Same answer, and we never built the six-dimensional vectors. That's the trick, and it means even infinite-dimensional mappings can be used.</p>
<h4>The RBF kernel: exp(−γ‖x − z‖²)</h4>
<table><tr><th>γ</th><th>Squared distance 1</th><th>Squared distance 25</th></tr>
<tr><td>0.01</td><td>0.990</td><td>0.779</td></tr><tr><td>0.1</td><td>0.905</td><td>0.082</td></tr><tr><td>1</td><td>0.368</td><td>0.000</td></tr></table>
<p>Large γ means similarity fades fast, so each point influences only its neighbourhood, giving a wiggly boundary that can overfit. Small γ gives a smooth boundary.</p>
<p><b>Tuning recipe:</b> scale features, then grid-search C and γ together on log scales.</p>
""", practice=["The Kernel Trick", "RBF Kernel"])


@LD
def kernel_numbers():
    x, z = np.array([1.0, 2.0]), np.array([3.0, 1.0])
    root2 = math.sqrt(2)
    phi_x = np.array([1, root2 * x[0], root2 * x[1], x[0] ** 2, root2 * x[0] * x[1], x[1] ** 2])
    phi_z = np.array([1, root2 * z[0], root2 * z[1], z[0] ** 2, root2 * z[0] * z[1], z[1] ** 2])
    long_way = phi_x @ phi_z
    shortcut = (x @ z + 1) ** 2
    rbf_near = {g: round(math.exp(-g * 1), 3) for g in [0.01, 0.1, 1]}
    rbf_far = {g: round(math.exp(-g * 25), 3) for g in [0.01, 0.1, 1]}
