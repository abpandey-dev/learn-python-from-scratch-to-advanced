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
