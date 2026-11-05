from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Eigenvectors: directions a matrix only stretches", """
<p>Multiply most vectors by a matrix and they get <b>turned</b> as well as stretched. But some special vectors only get <b>stretched</b> (or shrunk, or flipped) — they stay on their own line. These are <b>eigenvectors</b> ("own vectors"), and the stretch factor is the <b>eigenvalue</b> λ:</p>
<p style="text-align:center"><b>A·v = λ·v</b></p>
<p>Example: A = [[2, 1], [1, 2]]. A·[1, 1] = [3, 3] = 3·[1, 1], so [1, 1] is an eigenvector with λ = 3. A·[1, −1] = [1, −1], so λ = 1 there. A·[1, 0] = [2, 1] — turned, so not an eigenvector.</p>
<p>Eigenvectors are a matrix's "natural axes". Along them a complicated transformation becomes simple stretching.</p>
""", practice=["Is It an Eigenvector?", "Eigenvalues of a Triangular Matrix"])


@LD
def eigen_picture():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    vectors = {"[1, 1]": np.array([1.0, 1.0]), "[1, −1]": np.array([1.0, -1.0]), "[1, 0]": np.array([1.0, 0.0])}
    fig, axes = plt.subplots(1, 3, figsize=(8, 2.8))
    for ax, (name, v) in zip(axes, vectors.items()):
        Av = A @ v
        ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#0f766e", lw=2))
        ax.annotate("", xy=Av, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#b45309", lw=2))
        ax.set_xlim(-2, 3.5)
        ax.set_ylim(-2, 3.5)
        ax.set_aspect("equal")
        ax.set_title(f"v = {name}, Av = {Av.astype(int).tolist()}", fontsize=8)
        ax.grid(alpha=0.3)


LESSON("Core", "Finding eigenvalues", """
<p>A·v = λv can be rewritten (A − λI)v = 0. A non-zero v exists only if A − λI squashes space flat, i.e. <b>det(A − λI) = 0</b> — the <b>characteristic equation</b>.</p>
<p>For a 2 × 2 matrix it is a quadratic: λ² − (trace)λ + det = 0. So the eigenvalues always add up to the trace and multiply to the determinant.</p>
<p>For big matrices we use algorithms instead. The simplest is <b>power iteration</b>: multiply any starting vector by A again and again (normalising each time). The biggest eigenvalue wins, and the vector swings round to its eigenvector — this is how Google's original PageRank was computed.</p>
""", practice=["Eigenvalues of a 2×2", "Sum and Product of Eigenvalues", "Power Iteration: Biggest Eigenvalue", "Power Iteration: Main Direction"])


@LD
def power_iteration():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    v = np.array([1.0, 0.0])
    path = [v]
    for step in range(5):
        v = A @ v
        v = v / np.linalg.norm(v)
        path.append(v)
    estimate = v @ A @ v
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    for i, p in enumerate(path):
        ax.annotate("", xy=p, xytext=(0, 0), arrowprops=dict(arrowstyle="->", alpha=0.3 + 0.7 * i / 5, color="#0f766e"))
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect("equal")
    ax.set_title(f"turns toward [0.71, 0.71], λ ≈ {estimate:.2f}", fontsize=8)


LESSON("Core", "Principal Component Analysis (PCA)", """
<p>Real data often has many correlated features. <b>PCA</b> finds new axes, ordered by how much the data spreads along them, so you can keep the few that matter.</p>
<ol>
<li><b>Centre</b> the data: subtract each column's mean.</li>
<li>Compute the <b>covariance matrix</b> C = XᵀX / (n − 1).</li>
<li>Its <b>eigenvectors</b> are the principal components; its <b>eigenvalues</b> are the variance along each.</li>
<li><b>Project</b> the data onto the top k components (scores = X·PC) — fewer numbers, most of the information.</li>
</ol>
<p>The <b>explained variance ratio</b> λᵢ / Σλ tells you what share each component keeps. Uses: compressing data, plotting high-dimensional data in 2-D, removing noise, speeding up models.</p>
""", practice=["Centre the Data", "First Principal Component", "Project Onto the First Component", "Explained Variance Ratio", "Compress and Rebuild With One Component"])


@LD
def pca_demo():
    X = np.array([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2, 1.6], [1, 1.1], [1.5, 1.6], [1.1, 0.9]])
    mean = X.mean(axis=0)
    Xc = X - mean
    C = Xc.T @ Xc / (len(X) - 1)
    vals, vecs = np.linalg.eigh(C)
    pc1 = vecs[:, -1]
    ratio = vals[-1] / vals.sum()
    fig, ax = plt.subplots(figsize=(4, 3.2))
    ax.scatter(X[:, 0], X[:, 1])
    for val, vec in zip(vals, vecs.T):
        ax.annotate("", xy=mean + vec * 2 * np.sqrt(val), xytext=mean, arrowprops=dict(arrowstyle="->", color="#b45309", lw=2))
    ax.set_aspect("equal")
    ax.set_title(f"PC1 keeps {ratio:.0%} of the variance", fontsize=9)


LESSON("Advanced", "Orthogonal matrices and diagonalisation", """
<p>A symmetric matrix (like a covariance matrix) has <b>real</b> eigenvalues and <b>perpendicular</b> eigenvectors. Collecting them as columns gives an <b>orthogonal</b> matrix Q (QᵀQ = I — a pure rotation), and A = Q·D·Qᵀ with D diagonal.</p>
<p>This <b>diagonalisation</b> makes hard things easy: Aⁿ = Q·Dⁿ·Qᵀ (just power the diagonal) — e.g. Fibonacci numbers in one formula, or where a <b>Markov chain</b> settles: its steady state is the eigenvector with λ = 1.</p>
<p><b>Gram–Schmidt</b> turns any independent vectors into perpendicular unit vectors; NumPy's QR decomposition does it.</p>
""", practice=["Is the Matrix Orthogonal?", "Gram–Schmidt", "Powers by Diagonalising", "Markov Chain Steady State", "Fibonacci From Eigenvalues", "PageRank of a Tiny Web"])


@LD
def markov_demo():
    P = np.array([[0.9, 0.1], [0.5, 0.5]])
    state = np.array([0.0, 1.0])
    history = [state]
    for _ in range(12):
        state = state @ P
        history.append(state)
    history = np.array(history)
    fig, ax = plt.subplots(figsize=(4.5, 2.8))
    ax.plot(history[:, 0], "o-", markersize=3, label="P(sunny)")
    ax.plot(history[:, 1], "o-", markersize=3, label="P(rainy)")
    ax.set_xlabel("day")
    ax.legend()
    ax.set_title("Settles at the λ = 1 eigenvector", fontsize=9)


LESSON("Advanced", "Singular Value Decomposition (SVD)", """
<p>Eigenvectors need a square matrix. The <b>SVD</b> works for <b>any</b> matrix: A = U·Σ·Vᵀ — rotate (Vᵀ), stretch along the axes (Σ, the <b>singular values</b> σ₁ ≥ σ₂ ≥ … ≥ 0), rotate again (U). The σ's are the square roots of the eigenvalues of AᵀA.</p>
<ul>
<li>Keeping only the biggest k singular values gives the <b>best rank-k approximation</b> (Eckart–Young) — image compression, recommender systems, LSA for text.</li>
<li>PCA is the SVD of the centred data matrix.</li>
<li>σ_max / σ_min is the <b>condition number</b>: large means the matrix is nearly singular and results are sensitive to rounding.</li>
</ul>
""", practice=["Singular Values of a 2×2", "Condition Number", "Error of the Best Rank-1 Approximation"])


@LD
def svd_demo():
    angle = np.linspace(0, 2 * np.pi, 100)
    circle = np.vstack([np.cos(angle), np.sin(angle)])
    A = np.array([[3.0, 0.0], [4.0, 5.0]])
    ellipse = A @ circle
    U, s, Vt = np.linalg.svd(A)
    fig, ax = plt.subplots(figsize=(4, 3.4))
    ax.plot(circle[0], circle[1], label="unit circle")
    ax.plot(ellipse[0], ellipse[1], label="after A")
    for sigma, u in zip(s, U.T):
        ax.annotate("", xy=sigma * u, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#b45309", lw=2))
    ax.set_aspect("equal")
    ax.legend(fontsize=7)
    ax.set_title(f"σ = {s.round(2).tolist()}", fontsize=9)


LESSON("Core", "Eigenvalues and eigenvectors, fully by hand", """
<p>A = [[2, 1], [1, 2]].</p>
<h4>Step 1: find the eigenvalues</h4>
<p>Solve det(A − λI) = 0:</p>
<pre><code class="py">det [[2−λ, 1], [1, 2−λ]] = (2−λ)² − 1 = λ² − 4λ + 3 = 0
(λ − 3)(λ − 1) = 0     so λ = 3 or λ = 1</code></pre>
<p><b>Quick check:</b> they add to the trace (2 + 2 = 4) and multiply to the determinant (4 − 1 = 3) ✓.</p>
<h4>Step 2: find each eigenvector</h4>
<table><tr><th>λ</th><th>A − λI</th><th>Equation</th><th>Eigenvector</th></tr>
<tr><td>3</td><td>[[−1, 1], [1, −1]]</td><td>−x + y = 0</td><td>(1, 1)</td></tr>
<tr><td>1</td><td>[[1, 1], [1, 1]]</td><td>x + y = 0</td><td>(1, −1)</td></tr></table>
<h4>Step 3: verify</h4>
<p>A·(1, 1) = (3, 3) = 3·(1, 1) ✓, and A·(1, −1) = (1, −1) = 1·(1, −1) ✓.</p>
<p><b>Notes:</b> any multiple of an eigenvector also works, so (2, 2) is just as valid, and libraries return length-1 versions, with either sign. Here the two eigenvectors are perpendicular, as they always are for a symmetric matrix.</p>
""", practice=["Eigenvalues of a 2×2", "Sum and Product of Eigenvalues", "Is It an Eigenvector?", "Eigenvalues of a Triangular Matrix"])


@LD
def eigen_by_hand():
    A = np.array([[2.0, 1], [1, 2]])
    roots = np.sort(np.roots([1, -4, 3]))
    trace_and_det = (np.trace(A), np.linalg.det(A))
    first = A @ np.array([1.0, 1])
    second = A @ np.array([1.0, -1])
    library_values, library_vectors = np.linalg.eigh(A)
    perpendicular = library_vectors[:, 0] @ library_vectors[:, 1]


LESSON("Core", "Power iteration, step by step", """
<p>With the same A, start from v = (1, 0). Multiply by A, then rescale to length 1, and repeat.</p>
<table><tr><th>Step</th><th>A·v</th><th>Length</th><th>New v</th><th>Estimate of λ (v·Av)</th></tr>
<tr><td>1</td><td>(2, 1)</td><td>2.236</td><td>(0.894, 0.447)</td><td>2.800</td></tr>
<tr><td>2</td><td>(2.236, 1.789)</td><td>2.864</td><td>(0.781, 0.625)</td><td>2.976</td></tr>
<tr><td>3</td><td>(2.186, 2.030)</td><td>2.984</td><td>(0.733, 0.680)</td><td>2.997</td></tr>
<tr><td>4</td><td>(2.146, 2.094)</td><td>2.998</td><td>(0.716, 0.698)</td><td>3.000</td></tr></table>
<p>v heads towards (0.707, 0.707), and the estimate towards 3.</p>
<h4>Why it works</h4>
<p>Any starting vector is a mix of eigenvectors: here (1, 0) = ½(1, 1) + ½(1, −1). Each multiply stretches the first part by 3 and the second by 1. After k steps the ratio is 3ᵏ to 1, so the first part takes over.</p>
<p><b>Speed</b> depends on |λ₂ / λ₁|: here 1/3, which is fast. When two eigenvalues are close, it's slow.</p>
""", practice=["Power Iteration: Biggest Eigenvalue", "Power Iteration: Main Direction"])


@LD
def power_steps():
    A = np.array([[2.0, 1], [1, 2]])
    v = np.array([1.0, 0])
    history = []
    for step in range(6):
        w = A @ v
        v = w / np.linalg.norm(w)
        history.append(round(float(v @ A @ v), 4))
    mix = 0.5 * np.array([1.0, 1]) + 0.5 * np.array([1.0, -1])
    after_ten = 0.5 * 3 ** 10 * np.array([1.0, 1]) + 0.5 * 1 ** 10 * np.array([1.0, -1])
    ratio = after_ten[0] / after_ten[1]


LESSON("Core", "PCA, fully by hand", """
<p>Four rows with two features: (1, 2), (2, 3), (3, 5), (4, 4).</p>
<h4>Step 1: centre</h4>
<p>The means are 2.5 and 3.5, giving (−1.5, −1.5), (−0.5, −0.5), (0.5, 1.5), (1.5, 0.5).</p>
<h4>Step 2: covariance matrix (divide by n − 1 = 3)</h4>
<ul><li>Var(x) = (2.25 + 0.25 + 0.25 + 2.25) / 3 = 1.667</li>
<li>Var(y) = (2.25 + 0.25 + 2.25 + 0.25) / 3 = 1.667</li>
<li>Cov(x, y) = (2.25 + 0.25 + 0.75 + 0.75) / 3 = 1.333</li></ul>
<p>C = [[1.667, 1.333], [1.333, 1.667]].</p>
<h4>Step 3: eigenvalues and eigenvectors</h4>
<p>λ₁ = 1.667 + 1.333 = <b>3</b> with direction (0.707, 0.707). λ₂ = 1.667 − 1.333 = <b>0.333</b> with direction (0.707, −0.707).</p>
<h4>Step 4: how much does each keep?</h4>
<p>3 / 3.333 = <b>90%</b> and 0.333 / 3.333 = 10%. One number can hold 90% of the spread.</p>
<h4>Step 5: project</h4>
<p>Score = centred row · (0.707, 0.707). So (−1.5, −1.5) gives −2.121, and the four scores are −2.121, −0.707, 1.414, 1.414. Two columns became one.</p>
""", practice=["Centre the Data", "First Principal Component", "Project Onto the First Component", "Explained Variance Ratio", "Compress and Rebuild With One Component"])


@LD
def pca_by_hand():
    X = np.array([[1.0, 2], [2, 3], [3, 5], [4, 4]])
    centred = X - X.mean(axis=0)
    C = centred.T @ centred / 3
    values, vectors = np.linalg.eigh(C)
    shares = values[::-1] / values.sum()
    direction = np.array([1.0, 1]) / math.sqrt(2)
    scores = centred @ direction
    rebuilt = X.mean(axis=0) + np.outer(scores, direction)


LESSON("Advanced", "PCA pitfalls", """
<ol><li><b>Scale first.</b> The demo has income (thousands) and age (tens). Unscaled, the first component is simply income, with about 100% of the "variance". After scaling, both matter.</li>
<li><b>Fit on training data only</b>, then apply the same means and directions to the test data.</li>
<li><b>Variance isn't usefulness.</b> PCA ignores the target. The feature that best predicts y may have low variance and get dropped.</li>
<li><b>Only straight directions.</b> Data on a curve won't compress well.</li>
<li><b>Components are mixtures,</b> so they're harder to explain. Signs can flip between runs, so don't read meaning into a sign alone.</li>
<li><b>Outliers distort it,</b> as squared distances dominate.</li></ol>
<h4>How many components?</h4>
<p>Plot cumulative explained variance and keep enough for, say, 95%. Or choose by testing a downstream model with cross-validation.</p>
""", practice=["Explained Variance Ratio"])


@LD
def pca_scaling():
    r = np.random.default_rng(0)
    age = r.normal(40, 10, 200)
    income = 1000 * age + r.normal(0, 20000, 200)
    X = np.column_stack([income, age])

    def first_direction(data):
        c = data - data.mean(axis=0)
        values, vectors = np.linalg.eigh(c.T @ c)
        return np.abs(vectors[:, -1]).round(3), round(float(values[-1] / values.sum()), 3)

    unscaled = first_direction(X)
    scaled = first_direction((X - X.mean(axis=0)) / X.std(axis=0))


LESSON("Advanced", "Diagonalising: powers and steady states by hand", """
<h4>Powers made simple</h4>
<p>If A = P D P⁻¹, then in A⁵ the inner P⁻¹P pairs cancel, leaving A⁵ = P D⁵ P⁻¹. Powering a diagonal is easy: just power each entry.</p>
<p>For A = [[2, 1], [1, 2]], with eigenvalues 3 and 1:</p>
<ul><li>Diagonal entries of A⁵: (3⁵ + 1⁵) / 2 = (243 + 1) / 2 = <b>122</b></li>
<li>Off-diagonal: (3⁵ − 1⁵) / 2 = 242 / 2 = <b>121</b></li></ul>
<h4>Markov chain steady state</h4>
<p>Sunny stays sunny with chance 0.9; rainy turns sunny with chance 0.5. In the long run, the share π of sunny days must not change:</p>
<pre><code class="py">π = 0.9π + 0.5(1 − π)
0.6π = 0.5
π = 5/6 = 0.833</code></pre>
<p>That's the eigenvector of Pᵀ with eigenvalue 1, and it's where the chain settles from any start. PageRank uses the same idea.</p>
""", practice=["Powers by Diagonalising", "Markov Chain Steady State", "Is the Matrix Orthogonal?", "Gram–Schmidt", "Fibonacci From Eigenvalues", "PageRank of a Tiny Web"])


@LD
def diagonalise_demo():
    A = np.array([[2.0, 1], [1, 2]])
    values, P = np.linalg.eigh(A)
    fifth = (P @ np.diag(values ** 5) @ P.T).round(6)
    direct = np.linalg.matrix_power(A, 5)
    T = np.array([[0.9, 0.1], [0.5, 0.5]])
    state = np.array([0.0, 1.0])
    for day in range(40):
        state = state @ T
    long_run = state.round(4)


LESSON("Advanced", "SVD by hand, and compressing a picture", """
<p>A = [[3, 0], [4, 5]]. Singular values come from AᵀA:</p>
<pre><code class="py">AᵀA = [[25, 20],
       [20, 25]]
eigenvalues: 25 + 20 = 45 and 25 − 20 = 5
σ₁ = √45 = 6.708     σ₂ = √5 = 2.236</code></pre>
<p>They say how much A stretches along its two main directions.</p>
<h4>Low-rank compression</h4>
<p>SVD writes A as a sum of simple layers, biggest first: A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + … Keep just the first few.</p>
<p>A 100 × 100 picture holds 10,000 numbers. Keeping k layers stores k × (100 + 100 + 1) numbers, so k = 5 needs just 1,005: about a tenth. The demo shows the picture sharpening as k grows.</p>
<p>The same idea powers recommender systems and LSA for text. <b>PCA is SVD</b> of the centred data.</p>
""", practice=["Singular Values of a 2×2", "Condition Number", "Error of the Best Rank-1 Approximation"])


@LD
def compress_picture():
    x, y = np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100))
    picture = (x ** 2 + y ** 2 < 0.5).astype(float) + 0.5 * (np.abs(x - y) < 0.1)
    U, s, Vt = np.linalg.svd(picture)
    fig, axes = plt.subplots(1, 4, figsize=(8.5, 2.3))
    for ax, k in zip(axes, [1, 5, 20, 100]):
        approx = (U[:, :k] * s[:k]) @ Vt[:k]
        ax.imshow(approx, cmap="gray")
        ax.set_title(f"k = {k}: {k * 201 if k < 100 else 10000} numbers", fontsize=8)
        ax.axis("off")
    fig.tight_layout()
