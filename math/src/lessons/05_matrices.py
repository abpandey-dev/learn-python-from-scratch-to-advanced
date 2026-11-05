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


LESSON("Basics", "Matrix multiplication, one entry at a time", """
<pre><code class="py">A = [[1, 2, 3],      B = [[ 7,  8],
     [4, 5, 6]]           [ 9, 10],
                          [11, 12]]</code></pre>
<p><b>First check shapes:</b> (2 × <b>3</b>)·(<b>3</b> × 2). The inner numbers match, and the outer ones give the result's shape: 2 × 2.</p>
<p><b>Each entry is a row of A dotted with a column of B:</b></p>
<table><tr><th>Entry</th><th>Row of A · column of B</th><th>Value</th></tr>
<tr><td>(1, 1)</td><td>1·7 + 2·9 + 3·11</td><td>58</td></tr>
<tr><td>(1, 2)</td><td>1·8 + 2·10 + 3·12</td><td>64</td></tr>
<tr><td>(2, 1)</td><td>4·7 + 5·9 + 6·11</td><td>139</td></tr>
<tr><td>(2, 2)</td><td>4·8 + 5·10 + 6·12</td><td>154</td></tr></table>
<p>Result: [[58, 64], [139, 154]].</p>
<p><b>BA is a different thing:</b> here it would be 3 × 3. Order matters in matrix multiplication.</p>
""", practice=["Multiply Two Matrices", "Matrix Times Vector", "Transpose", "Add Two Matrices", "Is It the Identity Matrix?", "Trace"])


@LD
def multiply_by_hand():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[7, 8], [9, 10], [11, 12]])
    first_entry = A[0] @ B[:, 0]
    AB = A @ B
    BA_shape = (B @ A).shape
    shapes = (A.shape, B.shape, AB.shape)


LESSON("Core", "A matrix moves space", """
<p>Here's a very useful idea: <b>the columns of a matrix show where the basic arrows land.</b> In [[a, b], [c, d]], (1, 0) goes to (a, c) and (0, 1) goes to (b, d).</p>
<table><tr><th>Matrix</th><th>Effect</th><th>det</th></tr>
<tr><td>[[2, 0], [0, 2]]</td><td>doubles everything</td><td>4</td></tr>
<tr><td>[[2, 0], [0, 1]]</td><td>stretches sideways</td><td>2</td></tr>
<tr><td>[[0, −1], [1, 0]]</td><td>rotates 90°</td><td>1</td></tr>
<tr><td>[[1, 0], [0, −1]]</td><td>mirrors</td><td>−1</td></tr>
<tr><td>[[1, 1], [0, 1]]</td><td>shears</td><td>1</td></tr>
<tr><td>[[1, 2], [2, 4]]</td><td>squashes onto a line</td><td>0</td></tr></table>
<p><b>The determinant is the area factor.</b> A negative sign means the shape flipped. Zero means space collapsed, and no matrix can undo that, which is why det = 0 means no inverse.</p>
<p>A neural network layer does exactly this, stretching and rotating space, then bending it with an activation, until the classes can be separated.</p>
""", practice=["Rotate a Point", "Scale and Shear Shapes", "Determinant of a 2×2", "Determinant of a 3×3"])


@LD
def space_moves():
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
    matrices = {"stretch": [[2, 0], [0, 1]], "rotate": [[0, -1], [1, 0]], "shear": [[1, 1], [0, 1]], "squash": [[1, 2], [2, 4]]}
    fig, axes = plt.subplots(1, 4, figsize=(8.5, 2.3), sharex=True, sharey=True)
    for ax, (name, M) in zip(axes, matrices.items()):
        M = np.array(M, dtype=float)
        moved = square @ M.T
        ax.fill(square[:, 0], square[:, 1], alpha=0.25)
        ax.fill(moved[:, 0], moved[:, 1], alpha=0.5, edgecolor="#b45309")
        ax.set_title(f"{name}: det = {np.linalg.det(M):.0f}", fontsize=8)
        ax.set_aspect("equal")
    fig.tight_layout()


LESSON("Core", "Gaussian elimination by hand", """
<p>Solve this system:</p>
<pre><code class="py">x +  y +  z = 6
    2y + 5z = −4
2x + 5y −  z = 27</code></pre>
<h4>Step 1: remove x from row 3</h4>
<p>Row 3 − 2 × Row 1 gives 3y − 3z = 15, or y − z = 5.</p>
<h4>Step 2: remove y</h4>
<p>From y − z = 5 we have y = z + 5. Put that in row 2: 2(z + 5) + 5z = −4, so 7z = −14 and <b>z = −2</b>.</p>
<h4>Step 3: work backwards</h4>
<ul><li>y = −2 + 5 = <b>3</b></li><li>x = 6 − 3 − (−2) = <b>5</b></li></ul>
<h4>Step 4: check</h4>
<p>5 + 3 − 2 = 6 ✓, 6 − 10 = −4 ✓, 10 + 15 + 2 = 27 ✓.</p>
<p>The allowed moves are: swap rows, multiply a row, add a multiple of one row to another. None of them changes the solution. <code>np.linalg.solve</code> does the same thing, choosing the largest values as pivots to limit rounding errors.</p>
""", practice=["Solve A·x = b", "Rank of a Matrix"])


@LD
def elimination_steps():
    A = np.array([[1.0, 1, 1], [0, 2, 5], [2, 5, -1]])
    b = np.array([6.0, -4, 27])
    row3 = np.append(A[2], b[2]) - 2 * np.append(A[0], b[0])
    z = -2.0
    y = z + 5
    x = 6 - y - z
    answer = np.linalg.solve(A, b)
    check = A @ answer


LESSON("Core", "The inverse by hand", """
<p>A = [[4, 7], [2, 6]].</p>
<ol><li><b>Determinant:</b> 4·6 − 7·2 = 10.</li>
<li><b>Swap the diagonal, negate the others:</b> [[6, −7], [−2, 4]].</li>
<li><b>Divide by det:</b> A⁻¹ = [[0.6, −0.7], [−0.2, 0.4]].</li>
<li><b>Check:</b> the first entry of A·A⁻¹ is 4(0.6) + 7(−0.2) = 1 ✓, and multiplying fully gives the identity.</li></ol>
<h4>Using it</h4>
<p>To solve A·x = (1, 2): x = A⁻¹·(1, 2) = (0.6 − 1.4, −0.2 + 0.8) = (−0.8, 0.6).</p>
<h4>Useful rules</h4>
<ul><li>(AB)⁻¹ = B⁻¹A⁻¹: undo in reverse order, like taking off socks after shoes.</li>
<li>(AB)ᵀ = BᵀAᵀ: the same reversal for the transpose.</li>
<li>A symmetric matrix has A = Aᵀ. Covariance matrices are always symmetric.</li></ul>
<p>In practice, prefer <code>solve</code> to computing an inverse: it's faster and more accurate.</p>
""", practice=["Inverse of a 2×2", "Is It Symmetric?", "Matrix Power", "Outer Product"])


@LD
def inverse_by_hand():
    A = np.array([[4.0, 7], [2, 6]])
    det = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
    inverse = np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]]) / det
    identity = (A @ inverse).round(10)
    answer = inverse @ np.array([1.0, 2.0])
    same_answer = np.linalg.solve(A, [1.0, 2.0])


LESSON("Advanced", "Rank: how much information is really there?", """
<p>Rank counts the truly independent rows (or columns). Rows and columns always give the same number.</p>
<h4>Worked example</h4>
<pre><code class="py">[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]</code></pre>
<p>Row 3 = 2 × Row 2 − Row 1: for example 2(4) − 1 = 7. So the third row adds nothing, and the <b>rank is 2</b>, not 3. The determinant is 0.</p>
<h4>What it means in practice</h4>
<ul><li><b>Duplicate features</b> reduce the rank, so XᵀX has no inverse.</li>
<li><b>Fewer rows than columns</b> also lowers the rank, so many different weights fit equally well.</li>
<li><b>Recommenders:</b> a huge user × item table is often well described by a low-rank one, because tastes follow a few patterns.</li></ul>
<p>The chart shows a table of 100 rows × 5 features. Though it has 5 columns, it's built from only 2 hidden patterns, so nearly all the information sits in the first 2 singular values.</p>
""", practice=["Rank of a Matrix", "Covariance Matrix", "Linear Regression by the Normal Equation", "A Neural-Network Layer", "Markov Chain: Where Will We Be?"])


@LD
def low_rank_table():
    r = np.random.default_rng(0)
    hidden = r.normal(size=(100, 2))
    mix = r.normal(size=(2, 5))
    table = hidden @ mix + r.normal(0, 0.05, (100, 5))
    singular_values = np.linalg.svd(table, compute_uv=False)
    exact_rank = np.linalg.matrix_rank(hidden @ mix)
    three_by_three = np.linalg.matrix_rank([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    fig, ax = plt.subplots(figsize=(4.2, 2.7))
    ax.bar(range(1, 6), singular_values, color="#0f766e")
    ax.set_xlabel("singular value number")
    ax.set_title("2 hidden patterns: 2 large bars", fontsize=9)
