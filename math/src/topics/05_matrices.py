from lib import *
import math
import numpy as np

TOPIC(
    id="matrices", title="Matrices", glyph="[ ]",
    blurb="Tables of numbers that transform vectors: multiplication, transpose, determinant, inverse, solving systems, rank — and the matrix form of a neural-network layer and linear regression.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">A = np.array([[1, 2], [3, 4]])
A.shape, A.T                     # (2, 2), transpose
A + B, 3 * A, A * B              # element-wise
A @ B, A @ v                     # matrix product, matrix × vector
np.eye(3), np.trace(A)           # identity, sum of diagonal
np.linalg.det(A)                 # determinant  (−2)
np.linalg.inv(A)                 # inverse
np.linalg.solve(A, b)            # solve A x = b (better than inv(A) @ b)
np.linalg.matrix_rank(A)
np.linalg.matrix_power(A, 5)
np.linalg.lstsq(X, y, rcond=None)[0]   # least-squares fit</code></pre>
<p>A (m × n) @ B (n × p) works only when the inner sizes match, and gives m × p.</p>
""")


Q(None, "Transpose", "Easy", "Rows become columns",
  "Return the transpose of matrix A.",
  [(([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]), (([[7]],), [[7]])],
  ("New row j is old column j: build it with nested loops.", "O(m·n)", "O(m·n)"),
  ("<code>A.T</code>.", "O(1) view", "O(1)"))


@B
def transpose(A):
    rows, cols = len(A), len(A[0])
    T = []
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(A[i][j])
        T.append(new_row)
    return T


@O
def transpose(A):
    return np.array(A).T


Q(None, "Add Two Matrices", "Easy", "Entry by entry",
  "Return A + B (same shape).",
  [(([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[6, 8], [10, 12]]), (([[1, -1]], [[-1, 1]]), [[0, 0]])],
  ("Nested loops adding matching entries.", "O(m·n)", "O(m·n)"),
  ("<code>A + B</code> on arrays.", "O(m·n)", "O(m·n)"))


@B
def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


@O
def mat_add(A, B):
    return np.array(A) + np.array(B)


Q(None, "Matrix Times Vector", "Easy", "Each row · the vector",
  "Return A·v.",
  [(([[1, 2], [3, 4]], [5, 6]), [17, 39]), (([[1, 0, 0], [0, 2, 0]], [3, 3, 3]), [3, 6])],
  ("Each output entry is the dot product of one row with v.", "O(m·n)", "O(m)"),
  ("<code>A @ v</code>.", "O(m·n)", "O(m)"))


@B
def mat_vec(A, v):
    out = []
    for row in A:
        total = 0
        for a, x in zip(row, v):
            total += a * x
        out.append(total)
    return out


@O
def mat_vec(A, v):
    return np.array(A) @ np.array(v)


Q(None, "Multiply Two Matrices", "Medium", "Row × column",
  "Return A·B. Entry (i, j) is row i of A dotted with column j of B.",
  [(([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]), (([[1, 2, 3]], [[1], [1], [1]]), [[6]])],
  ("Triple loop: for each (i, j) add A[i][k]·B[k][j] over k.", "O(m·n·p)", "O(m·p)"),
  ("<code>A @ B</code> (optimised BLAS code).", "O(m·n·p)", "O(m·p)"))


@B
def mat_mul(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


@O
def mat_mul(A, B):
    return np.array(A) @ np.array(B)


Q(None, "Is It the Identity Matrix?", "Easy", "1s on the diagonal, 0s elsewhere",
  "Return True if A is an identity matrix.",
  [(([[1, 0], [0, 1]],), True), (([[1, 0], [1, 1]],), False), (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), True)],
  ("Check every entry: 1 when i == j, else 0.", "O(n²)", "O(1)"),
  ("<code>np.array_equal(A, np.eye(len(A)))</code>.", "O(n²)", "O(n²)"))


@B
def is_identity(A):
    n = len(A)
    for i in range(n):
        for j in range(n):
            expected = 1 if i == j else 0
            if A[i][j] != expected:
                return False
    return True


@O
def is_identity(A):
    A = np.array(A)
    return bool(A.shape[0] == A.shape[1] and np.array_equal(A, np.eye(len(A))))


Q(None, "Trace", "Easy", "Sum of the diagonal",
  "Return the sum of the diagonal entries of a square matrix.",
  [(([[1, 2], [3, 4]],), 5), (([[2, 0, 0], [0, 3, 0], [0, 0, 4]],), 9)],
  ("Add A[i][i] in a loop.", "O(n)", "O(1)"),
  ("<code>np.trace(A)</code>.", "O(n)", "O(1)"))


@B
def trace(A):
    total = 0
    for i in range(len(A)):
        total += A[i][i]
    return total


@O
def trace(A):
    return np.trace(A)


Q(None, "Determinant of a 2×2", "Easy", "ad − bc",
  "Return det [[a, b], [c, d]] = ad − bc, rounded to 4 decimals.",
  [(([[1, 2], [3, 4]],), -2.0), (([[2, 0], [0, 3]],), 6.0), (([[1, 2], [2, 4]],), 0.0)],
  ("Multiply down the main diagonal, subtract the other diagonal.", "O(1)", "O(1)"),
  ("<code>np.linalg.det(A)</code>.", "O(n³)", "O(n²)"))


@B
def det2(A):
    a, b = A[0]
    c, d = A[1]
    return round(a * d - b * c, 4)


@O
def det2(A):
    return round(np.linalg.det(A), 4)


Q(None, "Determinant of a 3×3", "Medium", "Cofactor expansion",
  "Return the determinant of a 3×3 matrix, rounded to 4 decimals.",
  [(([[2, 0, 1], [1, 3, 2], [1, 1, 2]],), 6.0), (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 0.0), (([[1, 0, 0], [0, 2, 0], [0, 0, 3]],), 6.0)],
  ("Expand along the first row: a·det(minor) − b·det(minor) + c·det(minor).", "O(1) for 3×3 (O(n!) in general)", "O(1)"),
  ("<code>np.linalg.det</code> uses LU decomposition — O(n³).", "O(n³)", "O(n²)"))


@B
def det3(A):
    def d2(m):
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    total = 0
    for j in range(3):
        minor = [[A[r][c] for c in range(3) if c != j] for r in (1, 2)]
        sign = 1 if j % 2 == 0 else -1
        total += sign * A[0][j] * d2(minor)
    return round(total, 4)


@O
def det3(A):
    return round(np.linalg.det(A), 4)


Q(None, "Inverse of a 2×2", "Medium", "Swap, negate, divide by det",
  "Return the inverse of a 2×2 matrix (entries rounded to 4 decimals), or None if it has none.",
  [(([[4, 7], [2, 6]],), [[0.6, -0.7], [-0.2, 0.4]]), (([[1, 2], [2, 4]],), None), (([[2, 0], [0, 5]],), [[0.5, 0.0], [0.0, 0.2]])],
  ("Formula: (1/det)·[[d, −b], [−c, a]].", "O(1)", "O(1)"),
  ("<code>np.linalg.inv</code>, guarding a zero determinant.", "O(n³)", "O(n²)"))


@B
def inverse2(A):
    a, b = A[0]
    c, d = A[1]
    det = a * d - b * c
    if det == 0:
        return None
    return [[round(d / det, 4), round(-b / det, 4)], [round(-c / det, 4), round(a / det, 4)]]


@O
def inverse2(A):
    A = np.array(A, dtype=float)
    if np.isclose(np.linalg.det(A), 0):
        return None
    return np.linalg.inv(A).round(4)


Q(None, "Solve A·x = b", "Medium", "Gaussian elimination",
  "Solve the square system A·x = b, rounding each answer to 4 decimals.",
  [(([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]), [2.0, 3.0, -1.0]), (([[1, 1], [1, -1]], [4, 0]), [2.0, 2.0])],
  ("Elimination: use each pivot to zero out the entries below it, then back-substitute from the last row up.", "O(n³)", "O(n²)"),
  ("<code>np.linalg.solve(A, b)</code>.", "O(n³)", "O(n²)"))


@B
def solve(A, b):
    n = len(A)
    M = [list(map(float, row)) + [float(bi)] for row, bi in zip(A, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col]
            M[r] = [x - factor * y for x, y in zip(M[r], M[col])]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        known = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - known) / M[i][i]
    return [round(v, 4) for v in x]


@O
def solve(A, b):
    return np.linalg.solve(A, b).round(4)


Q(None, "Is It Symmetric?", "Easy", "A = Aᵀ",
  "Return True if A equals its transpose.",
  [(([[1, 2], [2, 3]],), True), (([[1, 2], [3, 1]],), False), (([[5]],), True)],
  ("Compare A[i][j] with A[j][i] for every pair.", "O(n²)", "O(1)"),
  ("<code>np.array_equal(A, A.T)</code>.", "O(n²)", "O(n²)"))


@B
def symmetric(A):
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != A[j][i]:
                return False
    return True


@O
def symmetric(A):
    A = np.array(A)
    return bool(np.array_equal(A, A.T))


Q(None, "Matrix Power", "Medium", "Aⁿ = A·A·…·A",
  "Return Aⁿ for a square matrix and n ≥ 0.",
  [(([[1, 1], [1, 0]], 5), [[8, 5], [5, 3]]), (([[2, 0], [0, 3]], 3), [[8, 0], [0, 27]]), (([[1, 2], [3, 4]], 0), [[1, 0], [0, 1]])],
  ("Start from the identity and multiply by A, n times (by hand).", "O(n·k³)", "O(k²)"),
  ("<code>np.linalg.matrix_power</code> (repeated squaring).", "O(log n · k³)", "O(k²)"))


@B
def mat_pow(A, n):
    k = len(A)
    result = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    for _ in range(n):
        result = [[sum(result[i][t] * A[t][j] for t in range(k)) for j in range(k)] for i in range(k)]
    return result


@O
def mat_pow(A, n):
    return np.linalg.matrix_power(np.array(A), n)


Q(None, "Rotate a Point", "Medium", "Rotation matrix",
  "Rotate point (x, y) anticlockwise by θ degrees about the origin. Return coordinates rounded to 4 decimals.",
  [(([1, 0], 90), [0.0, 1.0]), (([1, 1], 180), [-1.0, -1.0]), (([2, 0], 45), [1.4142, 1.4142])],
  ("Use the formulas x' = x cos θ − y sin θ, y' = x sin θ + y cos θ.", "O(1)", "O(1)"),
  ("Build R = [[cos, −sin], [sin, cos]] and compute <code>R @ p</code> — works for many points at once.", "O(1)", "O(1)"))


@B
def rotate(p, degrees):
    t = math.radians(degrees)
    x, y = p
    nx = x * math.cos(t) - y * math.sin(t)
    ny = x * math.sin(t) + y * math.cos(t)
    return [round(nx, 4) + 0.0, round(ny, 4) + 0.0]


@O
def rotate(p, degrees):
    t = np.radians(degrees)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return (R @ np.array(p)).round(4) + 0.0


Q(None, "Rank of a Matrix", "Hard", "Independent rows",
  "Return the rank: the number of linearly independent rows.",
  [(([[1, 2], [2, 4]],), 1), (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 2), (([[1, 0], [0, 1]],), 2), (([[0, 0], [0, 0]],), 0)],
  ("Row-reduce to echelon form and count the non-zero rows.", "O(n³)", "O(n²)"),
  ("<code>np.linalg.matrix_rank</code> (counts non-tiny singular values).", "O(n³)", "O(n²)"))


@B
def rank(A):
    M = [list(map(float, r)) for r in A]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if abs(M[i][c]) > 1e-9), None)
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        for i in range(r + 1, rows):
            f = M[i][c] / M[r][c]
            M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


@O
def rank(A):
    return np.linalg.matrix_rank(np.array(A))


Q(None, "Outer Product", "Easy", "u vᵀ",
  "Return the matrix whose (i, j) entry is u[i]·v[j].",
  [(([1, 2], [3, 4, 5]), [[3, 4, 5], [6, 8, 10]]), (([2], [1, 1]), [[2, 2]])],
  ("Nested loops.", "O(m·n)", "O(m·n)"),
  ("<code>np.outer(u, v)</code>.", "O(m·n)", "O(m·n)"))


@B
def outer(u, v):
    return [[a * b for b in v] for a in u]


@O
def outer(u, v):
    return np.outer(u, v)


Q(None, "Covariance Matrix", "Hard", "Xᵀ X / (n − 1) after centring",
  "Rows are observations, columns are features. Return the sample covariance matrix, rounded to 4 decimals.",
  [(([[1, 2], [2, 4], [3, 6]],), [[1.0, 2.0], [2.0, 4.0]]), (([[1, 5], [2, 3], [3, 1]],), [[1.0, -2.0], [-2.0, 4.0]])],
  ("Subtract each column's mean, then entry (j, k) = Σ (centred xⱼ · centred xₖ) / (n − 1).", "O(n·d²)", "O(d²)"),
  ("<code>Xc.T @ Xc / (n - 1)</code> or <code>np.cov(X, rowvar=False)</code>.", "O(n·d²)", "O(n·d)"))


@B
def covariance(X):
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    C = [[0.0] * d for _ in range(d)]
    for j in range(d):
        for k in range(d):
            s = sum((row[j] - means[j]) * (row[k] - means[k]) for row in X)
            C[j][k] = round(s / (n - 1), 4)
    return C


@O
def covariance(X):
    X = np.array(X, dtype=float)
    Xc = X - X.mean(axis=0)
    return (Xc.T @ Xc / (len(X) - 1)).round(4)


Q(None, "Linear Regression by the Normal Equation", "Hard", "w = (XᵀX)⁻¹Xᵀy",
  "Fit y ≈ w₀ + w₁x₁ + … (add a column of 1s for w₀). Return the weights rounded to 4 decimals.",
  [(([[1], [2], [3], [4]], [3, 5, 7, 9]), [1.0, 2.0]), (([[0, 1], [1, 0], [1, 1], [2, 1]], [3, 2, 5, 7]), [0.0, 2.0, 3.0])],
  ("Build XᵀX and Xᵀy with loops, then solve the small system by elimination.", "O(n·d² + d³)", "O(d²)"),
  ("<code>np.linalg.lstsq(X, y)</code> — numerically safer than inverting XᵀX.", "O(n·d²)", "O(n·d)"))


@B
def normal_equation(X, y):
    rows = [[1.0] + list(map(float, r)) for r in X]
    d = len(rows[0])
    XtX = [[sum(r[i] * r[j] for r in rows) for j in range(d)] for i in range(d)]
    Xty = [sum(r[i] * t for r, t in zip(rows, y)) for i in range(d)]
    M = [XtX[i] + [Xty[i]] for i in range(d)]
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, d):
            f = M[r][c] / M[c][c]
            M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    w = [0.0] * d
    for i in range(d - 1, -1, -1):
        w[i] = (M[i][d] - sum(M[i][j] * w[j] for j in range(i + 1, d))) / M[i][i]
    return [round(v, 4) + 0.0 for v in w]


@O
def normal_equation(X, y):
    X = np.column_stack([np.ones(len(X)), np.array(X, dtype=float)])
    w = np.linalg.lstsq(X, np.array(y, dtype=float), rcond=None)[0]
    return w.round(4) + 0.0


Q(None, "A Neural-Network Layer", "Medium", "ReLU(W·x + b)",
  "A layer has weight matrix W (one row per neuron) and bias vector b. Return ReLU(W·x + b).",
  [(([[1, -1], [2, 0.5], [-1, -1]], [0, 1, 0], [3, 2]), [1, 8.0, 0]), (([[1, 1]], [-5], [1, 1]), [0])],
  ("Each neuron: dot its weights with x, add its bias, clamp at 0.", "O(m·n)", "O(m)"),
  ("Whole layer in one line: <code>np.maximum(0, W @ x + b)</code>.", "O(m·n)", "O(m)"),
  names=["W", "b", "x"])


@B
def layer(W, b, x):
    out = []
    for row, bias in zip(W, b):
        z = bias
        for w, xi in zip(row, x):
            z += w * xi
        out.append(z if z > 0 else 0)
    return out


@O
def layer(W, b, x):
    return np.maximum(0, np.array(W) @ np.array(x) + np.array(b))


Q(None, "Markov Chain: Where Will We Be?", "Medium", "State × transition matrix",
  "P[i][j] is the chance of moving from state i to j. Starting from distribution s, return the distribution after n steps (rounded to 4 decimals).",
  [(([1, 0], [[0.9, 0.1], [0.5, 0.5]], 1), [0.9, 0.1]), (([1, 0], [[0.9, 0.1], [0.5, 0.5]], 2), [0.86, 0.14]), (([0.5, 0.5], [[0, 1], [1, 0]], 3), [0.5, 0.5])],
  ("Step by step: new[j] = Σᵢ s[i]·P[i][j], repeated n times.", "O(n·k²)", "O(k)"),
  ("<code>s @ np.linalg.matrix_power(P, n)</code>.", "O(log n · k³)", "O(k²)"),
  names=["s", "P", "n"])


@B
def markov(s, P, n):
    k = len(s)
    for _ in range(n):
        s = [sum(s[i] * P[i][j] for i in range(k)) for j in range(k)]
    return [round(x, 4) for x in s]


@O
def markov(s, P, n):
    return (np.array(s) @ np.linalg.matrix_power(np.array(P), n)).round(4)


Q(None, "Scale and Shear Shapes", "Medium", "Transforming many points",
  "Apply matrix T to every point (rows of pts). Return the new points rounded to 4 decimals.",
  [(([[2, 0], [0, 1]], [[1, 1], [0, 1], [1, 0]]), [[2.0, 1.0], [0.0, 1.0], [2.0, 0.0]]), (([[1, 1], [0, 1]], [[0, 1], [1, 1]]), [[1.0, 1.0], [2.0, 1.0]])],
  ("Multiply T by each point in a loop.", "O(n)", "O(n)"),
  ("All at once: <code>pts @ T.T</code>.", "O(n)", "O(n)"),
  names=["T", "pts"])


@B
def transform_points(T, pts):
    out = []
    for x, y in pts:
        out.append([round(T[0][0] * x + T[0][1] * y, 4) + 0.0, round(T[1][0] * x + T[1][1] * y, 4) + 0.0])
    return out


@O
def transform_points(T, pts):
    return (np.array(pts, dtype=float) @ np.array(T, dtype=float).T).round(4)
