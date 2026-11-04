from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SQUARE = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)

LESSON("Basics", "What is a matrix?", """
<p>A <b>matrix</b> is a rectangle of numbers with rows and columns. A 2 × 3 matrix has 2 rows and 3 columns. Entry A<sub>ij</sub> sits in row i, column j.</p>
<p>Two ways to think of one:</p>
<ul>
<li><b>A table of data</b>: each row is one example (a house), each column one feature (size, rooms, age). A dataset with 1000 houses and 3 features is a 1000 × 3 matrix, usually called <b>X</b>.</li>
<li><b>A machine that transforms vectors</b>: multiply a vector by a matrix and it gets rotated, stretched or squashed.</li>
</ul>
<p>Adding matrices and multiplying by a number work entry by entry. The <b>transpose</b> Aᵀ flips rows into columns.</p>
""", practice=["Transpose", "Add Two Matrices", "Is It Symmetric?", "Trace"])


@LD
def matrix_demo():
    X = np.array([[120, 3, 15], [80, 2, 30], [150, 4, 5]])
    shape = X.shape
    first_house = X[0]
    all_sizes = X[:, 0]
    XT = X.T


LESSON("Basics", "Multiplying a matrix by a vector", """
<p>A·v: take the dot product of <b>each row</b> of A with v. Each row gives one number of the answer.</p>
<pre><code class="py">[1 2] [5]   [1·5 + 2·6]   [17]
[3 4] [6] = [3·5 + 4·6] = [39]</code></pre>
<p>Why care? A whole layer of a neural network is one matrix-vector product: each row of W holds one neuron's weights, so W·x computes every neuron at once.</p>
<p>Geometrically, a 2 × 2 matrix moves every point of the plane: the first column is where [1, 0] lands, the second column is where [0, 1] lands.</p>
""", practice=["Matrix Times Vector", "A Neural-Network Layer", "Rotate a Point", "Scale and Shear Shapes"])


@LD
def transform_demo():
    shear = np.array([[1, 1], [0, 1]])
    rotate = np.array([[0, -1], [1, 0]])
    sheared = SQUARE @ shear.T
    rotated = SQUARE @ rotate.T
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(SQUARE[:, 0], SQUARE[:, 1], label="original square")
    ax.plot(sheared[:, 0], sheared[:, 1], label="sheared")
    ax.plot(rotated[:, 0], rotated[:, 1], label="rotated 90°")
    ax.set_aspect("equal")
    ax.legend(fontsize=7)
    ax.grid(alpha=0.3)


LESSON("Core", "Multiplying two matrices", """
<p>A·B: entry (i, j) = row i of A · column j of B. Sizes must fit: (m × <b>n</b>) · (<b>n</b> × p) → m × p.</p>
<ul>
<li>Order matters: A·B ≠ B·A in general.</li>
<li>The <b>identity matrix</b> I (1s on the diagonal) does nothing: A·I = A.</li>
<li>Multiplying matrices = doing one transformation then another. Aⁿ = applying A n times (used in Markov chains).</li>
</ul>
<p><b>Element-wise</b> product (<code>A * B</code>) is different from <b>matrix</b> product (<code>A @ B</code>) — a classic bug.</p>
""", practice=["Multiply Two Matrices", "Is It the Identity Matrix?", "Matrix Power", "Outer Product", "Markov Chain: Where Will We Be?"])


@LD
def matmul_demo():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    AB = A @ B
    BA = B @ A
    elementwise = A * B
    I = np.eye(2, dtype=int)
    same = A @ I


LESSON("Core", "Determinant and inverse", """
<p>The <b>determinant</b> of a 2 × 2 matrix [[a, b], [c, d]] is ad − bc. It measures how much the matrix scales <b>area</b>: det = 2 doubles areas, det = 0 squashes the plane flat onto a line (information is lost).</p>
<p>The <b>inverse</b> A⁻¹ undoes A: A⁻¹A = I. It exists only when det ≠ 0. For 2 × 2: A⁻¹ = (1/det)·[[d, −b], [−c, a]].</p>
<p>A system of equations A·x = b is solved by x = A⁻¹b — in practice with <code>np.linalg.solve</code> (Gaussian elimination), which is faster and more accurate than computing the inverse.</p>
""", practice=["Determinant of a 2×2", "Determinant of a 3×3", "Inverse of a 2×2", "Solve A·x = b"])


@LD
def det_demo():
    A = np.array([[2.0, 1.0], [1.0, 3.0]])
    det = np.linalg.det(A)
    A_inv = np.linalg.inv(A)
    check = A_inv @ A
    shape = SQUARE @ A.T
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.fill(SQUARE[:, 0], SQUARE[:, 1], alpha=0.4, label="area 1")
    ax.fill(shape[:, 0], shape[:, 1], alpha=0.4, label=f"area {det:.0f} = det")
    ax.set_aspect("equal")
    ax.legend()


LESSON("Advanced", "Rank, covariance and linear regression in matrix form", """
<p>The <b>rank</b> is the number of truly independent rows (or columns). If a feature is just 2 × another feature, it adds no information and the rank drops.</p>
<p>With centred data X (each column minus its mean), <b>XᵀX / (n − 1)</b> is the <b>covariance matrix</b>: diagonal = variances, off-diagonal = how pairs of features move together. It is the starting point of PCA (next topic).</p>
<p><b>Linear regression</b> for all features at once: find w so that X·w ≈ y. The best w (least squares) solves the <b>normal equation</b> XᵀX·w = Xᵀy. One line of matrix algebra replaces pages of formulas.</p>
""", practice=["Rank of a Matrix", "Covariance Matrix", "Linear Regression by the Normal Equation"])


@LD
def regression_demo():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([2.2, 4.1, 5.9, 8.2, 9.9])
    X = np.column_stack([np.ones_like(x), x])
    w = np.linalg.solve(X.T @ X, X.T @ y)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.scatter(x, y)
    ax.plot(x, X @ w, color="#b45309", label=f"y = {w[0]:.2f} + {w[1]:.2f}x")
    ax.legend()
