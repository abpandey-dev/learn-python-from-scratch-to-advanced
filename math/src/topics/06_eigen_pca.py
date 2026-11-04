from lib import *
import math
import numpy as np

TOPIC(
    id="eigen-pca", title="Eigenvectors, PCA & SVD", glyph="λ",
    blurb="The special directions a matrix only stretches. Eigenvalues, power iteration, principal component analysis, singular values, Markov steady states and PageRank.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">vals, vecs = np.linalg.eig(A)        # columns of vecs are eigenvectors
vals, vecs = np.linalg.eigh(S)       # symmetric S: real, sorted ascending
# A v = λ v      det(A − λI) = 0      Σλ = trace,  Πλ = det
Xc = X - X.mean(axis=0)              # PCA step 1: centre
C = Xc.T @ Xc / (len(X) - 1)         # step 2: covariance
vals, vecs = np.linalg.eigh(C)       # step 3: eigenvectors = principal components
scores = Xc @ vecs[:, ::-1]          # step 4: project (largest first)
U, s, Vt = np.linalg.svd(A)          # A = U diag(s) Vt</code></pre>
""")


Q(None, "Is It an Eigenvector?", "Easy", "A·v = λ·v",
  "Return λ if v is an eigenvector of A (A·v is v scaled by λ), otherwise None. λ rounded to 4 decimals.",
  [(([[2, 1], [1, 2]], [1, 1]), 3.0), (([[2, 1], [1, 2]], [1, -1]), 1.0), (([[2, 1], [1, 2]], [1, 0]), None)],
  ("Compute A·v by hand, then check every component is the same multiple of v.", "O(n²)", "O(n)"),
  ("λ = (v·Av)/(v·v); then <code>np.allclose(A @ v, λ * v)</code>.", "O(n²)", "O(n)"))


@B
def eigen_check(A, v):
    Av = [sum(a * x for a, x in zip(row, v)) for row in A]
    ratio = None
    for out, x in zip(Av, v):
        if x == 0:
            if out != 0:
                return None
            continue
        r = out / x
        if ratio is None:
            ratio = r
        elif abs(r - ratio) > 1e-9:
            return None
    return round(ratio, 4)


@O
def eigen_check(A, v):
    A, v = np.array(A, dtype=float), np.array(v, dtype=float)
    lam = v @ A @ v / (v @ v)
    return round(lam, 4) if np.allclose(A @ v, lam * v) else None


Q(None, "Eigenvalues of a 2×2", "Medium", "Characteristic equation",
  "Return the (real) eigenvalues of a 2×2 matrix, sorted ascending and rounded to 4 decimals.",
  [(([[2, 1], [1, 2]],), [1.0, 3.0]), (([[4, 1], [2, 3]],), [2.0, 5.0]), (([[3, 0], [0, 1]],), [1.0, 3.0])],
  ("det(A − λI) = 0 gives λ² − (trace)λ + det = 0; solve with the quadratic formula.", "O(1)", "O(1)"),
  ("<code>np.linalg.eigvals(A)</code>.", "O(n³)", "O(n)"))


@B
def eig2(A):
    (a, b), (c, d) = A
    tr = a + d
    det = a * d - b * c
    disc = math.sqrt(tr * tr - 4 * det)
    return sorted([round((tr - disc) / 2, 4), round((tr + disc) / 2, 4)])


@O
def eig2(A):
    return np.sort(np.linalg.eigvals(A).real).round(4)


Q(None, "Sum and Product of Eigenvalues", "Easy", "trace and determinant",
  "Return (sum, product) of the eigenvalues of a square matrix, rounded to 4 decimals.",
  [(([[2, 1], [1, 2]],), (4.0, 3.0)), (([[1, 2, 0], [0, 3, 0], [0, 0, 2]],), (6.0, 6.0))],
  ("No eigenvalues needed: sum = trace, product = determinant (computed by hand).", "O(n) + det", "O(1)"),
  ("Compute them and add / multiply: <code>vals.sum(), vals.prod()</code>.", "O(n³)", "O(n)"))


@B
def eig_sum_prod(A):
    n = len(A)
    trace = sum(A[i][i] for i in range(n))
    M = [list(map(float, r)) for r in A]
    det = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            return (round(trace, 4), 0.0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            det = -det
        det *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return (round(trace, 4), round(det, 4))


@O
def eig_sum_prod(A):
    vals = np.linalg.eigvals(A)
    return (round(vals.sum().real, 4), round(vals.prod().real, 4))


Q(None, "Power Iteration: Biggest Eigenvalue", "Medium", "Repeatedly multiply",
  "Return the eigenvalue of largest size, rounded to 4 decimals.",
  [(([[2, 1], [1, 2]],), 3.0), (([[4, 1], [2, 3]],), 5.0), (([[3, 0], [0, 1]],), 3.0)],
  ("Start with any vector, multiply by A and normalise again and again; it turns toward the dominant eigenvector, and v·Av/v·v gives λ.", "O(k·n²)", "O(n)"),
  ("<code>np.linalg.eigvals</code>, take the one with the largest absolute value.", "O(n³)", "O(n)"))


@B
def dominant_value(A):
    v = [1.0] * len(A)
    for _ in range(100):
        w = [sum(a * x for a, x in zip(row, v)) for row in A]
        norm = math.sqrt(sum(x * x for x in w))
        v = [x / norm for x in w]
    Av = [sum(a * x for a, x in zip(row, v)) for row in A]
    return round(sum(x * y for x, y in zip(v, Av)), 4)


@O
def dominant_value(A):
    vals = np.linalg.eigvals(A)
    return round(vals[np.argmax(np.abs(vals))].real, 4)


Q(None, "Power Iteration: Main Direction", "Medium", "Dominant eigenvector",
  "Return the unit eigenvector for the largest eigenvalue, with its first non-zero component positive, rounded to 4 decimals.",
  [(([[2, 1], [1, 2]],), [0.7071, 0.7071]), (([[3, 0], [0, 1]],), [1.0, 0.0]), (([[4, 1], [2, 3]],), [0.7071, 0.7071])],
  ("Power iteration as before, then fix the sign.", "O(k·n²)", "O(n)"),
  ("<code>np.linalg.eig</code>: pick the column of the biggest eigenvalue.", "O(n³)", "O(n²)"))


@B
def dominant_vector(A):
    v = [1.0] + [0.5] * (len(A) - 1)
    for _ in range(200):
        w = [sum(a * x for a, x in zip(row, v)) for row in A]
        norm = math.sqrt(sum(x * x for x in w))
        v = [x / norm for x in w]
    first = next(x for x in v if abs(x) > 1e-9)
    sign = 1 if first > 0 else -1
    return [round(sign * x, 4) + 0.0 for x in v]


@O
def dominant_vector(A):
    vals, vecs = np.linalg.eig(np.array(A, dtype=float))
    v = vecs[:, np.argmax(np.abs(vals))].real
    first = v[np.flatnonzero(np.abs(v) > 1e-9)[0]]
    return (np.sign(first) * v).round(4) + 0.0


Q(None, "Eigenvalues of a Triangular Matrix", "Easy", "Read them off the diagonal",
  "Return the eigenvalues of a triangular (or diagonal) matrix, sorted ascending.",
  [(([[3, 5, 1], [0, 2, 4], [0, 0, 7]],), [2, 3, 7]), (([[1, 0], [9, 4]],), [1, 4])],
  ("det(A − λI) of a triangular matrix is the product of (diagonal − λ), so the eigenvalues are the diagonal.", "O(n log n)", "O(n)"),
  ("<code>np.linalg.eigvals</code> confirms it.", "O(n³)", "O(n)"))


@B
def triangular_eigs(A):
    return sorted(A[i][i] for i in range(len(A)))


@O
def triangular_eigs(A):
    return np.sort(np.linalg.eigvals(A).real).round(4)


Q(None, "Centre the Data", "Easy", "PCA step 1",
  "Subtract each column's mean from that column. Return the centred data rounded to 4 decimals.",
  [(([[1, 2], [2, 3], [3, 5], [4, 4]],), [[-1.5, -1.5], [-0.5, -0.5], [0.5, 1.5], [1.5, 0.5]])],
  ("Column means with loops, then subtract.", "O(n·d)", "O(n·d)"),
  ("Broadcasting: <code>X - X.mean(axis=0)</code>.", "O(n·d)", "O(n·d)"))


@B
def centre(X):
    n, d = len(X), len(X[0])
    means = [sum(row[j] for row in X) / n for j in range(d)]
    return [[round(row[j] - means[j], 4) for j in range(d)] for row in X]


@O
def centre(X):
    X = np.array(X, dtype=float)
    return (X - X.mean(axis=0)).round(4)


PCA_X = [[1, 2], [2, 3], [3, 5], [4, 4]]

Q(None, "First Principal Component", "Hard", "Direction of greatest spread",
  "Return the first principal component of 2-D data (unit vector, first component positive, rounded to 4 decimals).",
  [((PCA_X,), [0.7071, 0.7071]),
   (([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0], [2.3, 2.7], [2, 1.6], [1, 1.1], [1.5, 1.6], [1.1, 0.9]],), [0.6779, 0.7352])],
  ("Centre, build the covariance matrix by hand, power-iterate to its dominant eigenvector.", "O(n·d² + k·d²)", "O(d²)"),
  ("<code>np.linalg.eigh(np.cov(X, rowvar=False))</code> — last column is the largest.", "O(n·d² + d³)", "O(d²)"))


@B
def first_pc(X):
    n, d = len(X), len(X[0])
    means = [sum(r[j] for r in X) / n for j in range(d)]
    Xc = [[r[j] - means[j] for j in range(d)] for r in X]
    C = [[sum(r[i] * r[j] for r in Xc) / (n - 1) for j in range(d)] for i in range(d)]
    v = [1.0] * d
    for _ in range(200):
        w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
        norm = math.sqrt(sum(x * x for x in w))
        v = [x / norm for x in w]
    sign = 1 if v[0] > 0 else -1
    return [round(sign * x, 4) for x in v]


@O
def first_pc(X):
    vals, vecs = np.linalg.eigh(np.cov(np.array(X, dtype=float), rowvar=False))
    pc = vecs[:, -1]
    return (pc * np.sign(pc[0])).round(4)


Q(None, "Project Onto the First Component", "Medium", "PCA scores",
  "Centre the data and project each row onto the given unit direction pc. Return the scores rounded to 4 decimals.",
  [((PCA_X, [0.7071068, 0.7071068]), [-2.1213, -0.7071, 1.4142, 1.4142])],
  ("Score of a row = (centred row) · pc, in a loop.", "O(n·d)", "O(n)"),
  ("<code>(X - X.mean(0)) @ pc</code>.", "O(n·d)", "O(n)"),
  names=["X", "pc"])


@B
def scores(X, pc):
    n, d = len(X), len(X[0])
    means = [sum(r[j] for r in X) / n for j in range(d)]
    out = []
    for r in X:
        out.append(round(sum((r[j] - means[j]) * pc[j] for j in range(d)), 4))
    return out


@O
def scores(X, pc):
    X = np.array(X, dtype=float)
    return ((X - X.mean(axis=0)) @ np.array(pc)).round(4)


Q(None, "Explained Variance Ratio", "Medium", "How much each component keeps",
  "Return each principal component's share of the total variance, largest first, rounded to 4 decimals.",
  [((PCA_X,), [0.9, 0.1])],
  ("2-D covariance by hand, eigenvalues from the characteristic equation, divide by their sum.", "O(n)", "O(1)"),
  ("<code>eigh</code> of the covariance matrix, reverse, divide by the sum.", "O(n·d² + d³)", "O(d²)"))


@B
def explained(X):
    n = len(X)
    mx = sum(r[0] for r in X) / n
    my = sum(r[1] for r in X) / n
    a = sum((r[0] - mx) ** 2 for r in X) / (n - 1)
    d = sum((r[1] - my) ** 2 for r in X) / (n - 1)
    b = sum((r[0] - mx) * (r[1] - my) for r in X) / (n - 1)
    tr, det = a + d, a * d - b * b
    disc = math.sqrt(tr * tr - 4 * det)
    l1, l2 = (tr + disc) / 2, (tr - disc) / 2
    return [round(l1 / tr, 4), round(l2 / tr, 4)]


@O
def explained(X):
    vals = np.linalg.eigvalsh(np.cov(np.array(X, dtype=float), rowvar=False))[::-1]
    return (vals / vals.sum()).round(4)


Q(None, "Compress and Rebuild With One Component", "Hard", "Dimensionality reduction",
  "Keep only the first principal component: reconstruct each row as mean + score·pc. Return the rebuilt data rounded to 4 decimals.",
  [((PCA_X,), [[1.0, 2.0], [2.0, 3.0], [3.5, 4.5], [3.5, 4.5]])],
  ("Centre, find pc by power iteration, score each row, then map back point by point.", "O(n·d + k·d²)", "O(n·d)"),
  ("Matrix form: <code>mean + np.outer(Xc @ pc, pc)</code>.", "O(n·d)", "O(n·d)"))


@B
def rebuild(X):
    n, d = len(X), len(X[0])
    means = [sum(r[j] for r in X) / n for j in range(d)]
    Xc = [[r[j] - means[j] for j in range(d)] for r in X]
    C = [[sum(r[i] * r[j] for r in Xc) for j in range(d)] for i in range(d)]
    v = [1.0] * d
    for _ in range(200):
        w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
        nrm = math.sqrt(sum(x * x for x in w))
        v = [x / nrm for x in w]
    out = []
    for r in Xc:
        s = sum(a * b for a, b in zip(r, v))
        out.append([round(means[j] + s * v[j], 4) for j in range(d)])
    return out


@O
def rebuild(X):
    X = np.array(X, dtype=float)
    mean = X.mean(axis=0)
    Xc = X - mean
    pc = np.linalg.eigh(Xc.T @ Xc)[1][:, -1]
    return (mean + np.outer(Xc @ pc, pc)).round(4)


Q(None, "Is the Matrix Orthogonal?", "Easy", "QᵀQ = I",
  "Return True if the columns of Q are perpendicular unit vectors (QᵀQ = I, within 1e-6).",
  [(([[0, -1], [1, 0]],), True), (([[0.6, -0.8], [0.8, 0.6]],), True), (([[1, 1], [0, 1]],), False)],
  ("Check every pair of columns: dot product 1 with itself, 0 with the others.", "O(n³)", "O(1)"),
  ("<code>np.allclose(Q.T @ Q, np.eye(n))</code>.", "O(n³)", "O(n²)"))


@B
def is_orthogonal(Q):
    n = len(Q)
    for i in range(n):
        for j in range(n):
            d = sum(Q[k][i] * Q[k][j] for k in range(n))
            if abs(d - (1 if i == j else 0)) > 1e-6:
                return False
    return True


@O
def is_orthogonal(Q):
    Q = np.array(Q, dtype=float)
    return bool(np.allclose(Q.T @ Q, np.eye(len(Q)), atol=1e-6))


Q(None, "Gram–Schmidt", "Medium", "Make vectors perpendicular",
  "Turn two independent vectors a, b into an orthonormal pair: e₁ = a/‖a‖, e₂ = (b − proj)/‖…‖. Return [e₁, e₂] rounded to 4 decimals.",
  [(([3, 1], [1, 2]), [[0.9487, 0.3162], [-0.3162, 0.9487]]), (([1, 0, 0], [1, 1, 0]), [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])],
  ("Normalise a; subtract b's projection onto e₁; normalise what is left.", "O(n)", "O(n)"),
  ("QR decomposition <code>np.linalg.qr</code> does Gram–Schmidt; fix signs so R's diagonal is positive.", "O(n)", "O(n)"))


@B
def gram_schmidt(a, b):
    na = math.sqrt(sum(x * x for x in a))
    e1 = [x / na for x in a]
    proj = sum(x * y for x, y in zip(b, e1))
    r = [x - proj * y for x, y in zip(b, e1)]
    nr = math.sqrt(sum(x * x for x in r))
    e2 = [x / nr for x in r]
    return [[round(x, 4) + 0.0 for x in e1], [round(x, 4) + 0.0 for x in e2]]


@O
def gram_schmidt(a, b):
    Q, R = np.linalg.qr(np.array([a, b], dtype=float).T)
    Q = Q * np.sign(np.diag(R))
    return Q.T.round(4) + 0.0


Q(None, "Powers by Diagonalising", "Hard", "Aⁿ = P Dⁿ P⁻¹",
  "Return Aⁿ (rounded to whole numbers) using its eigen-decomposition.",
  [(([[2, 1], [1, 2]], 5), [[122, 121], [121, 122]]), (([[1, 1], [1, 0]], 10), [[89, 55], [55, 34]])],
  ("Multiply A by itself n times.", "O(n·k³)", "O(k²)"),
  ("A = PDP⁻¹, so Aⁿ = P·Dⁿ·P⁻¹ — only the diagonal gets powered.", "O(k³)", "O(k²)"))


@B
def power_by_eig(A, n):
    k = len(A)
    R = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    for _ in range(n):
        R = [[sum(R[i][t] * A[t][j] for t in range(k)) for j in range(k)] for i in range(k)]
    return R


@O
def power_by_eig(A, n):
    vals, P = np.linalg.eig(np.array(A, dtype=float))
    An = P @ np.diag(vals ** n) @ np.linalg.inv(P)
    return np.rint(An.real).astype(int)


Q(None, "Markov Chain Steady State", "Medium", "Eigenvector for λ = 1",
  "Return the long-run distribution π with π·P = π (entries rounded to 4 decimals).",
  [(([[0.9, 0.1], [0.5, 0.5]],), [0.8333, 0.1667]), (([[0.5, 0.5, 0], [0.2, 0.6, 0.2], [0, 0.4, 0.6]],), [0.2105, 0.5263, 0.2632])],
  ("Start uniform and keep multiplying by P until it stops changing (power iteration).", "O(k·n²)", "O(n)"),
  ("The eigenvector of Pᵀ with eigenvalue 1, scaled to sum to 1.", "O(n³)", "O(n²)"))


@B
def steady_state(P):
    n = len(P)
    pi = [1 / n] * n
    for _ in range(500):
        pi = [sum(pi[i] * P[i][j] for i in range(n)) for j in range(n)]
    return [round(x, 4) for x in pi]


@O
def steady_state(P):
    vals, vecs = np.linalg.eig(np.array(P, dtype=float).T)
    v = vecs[:, np.argmin(np.abs(vals - 1))].real
    return (v / v.sum()).round(4)


Q(None, "Singular Values of a 2×2", "Medium", "√ eigenvalues of AᵀA",
  "Return the singular values of a 2×2 matrix, largest first, rounded to 4 decimals.",
  [(([[3, 0], [4, 5]],), [6.7082, 2.2361]), (([[2, 1], [1, 2]],), [3.0, 1.0])],
  ("Form AᵀA by hand, find its eigenvalues with the quadratic formula, take square roots.", "O(1)", "O(1)"),
  ("<code>np.linalg.svd(A, compute_uv=False)</code>.", "O(n³)", "O(n)"))


@B
def singular_values(A):
    (a, b), (c, d) = A
    p, q, r = a * a + c * c, a * b + c * d, b * b + d * d
    tr, det = p + r, p * r - q * q
    disc = math.sqrt(tr * tr - 4 * det)
    return [round(math.sqrt((tr + disc) / 2), 4), round(math.sqrt(max(0, (tr - disc) / 2)), 4)]


@O
def singular_values(A):
    return np.linalg.svd(np.array(A, dtype=float), compute_uv=False).round(4)


Q(None, "Condition Number", "Medium", "σ_max / σ_min",
  "Return the condition number of a 2×2 matrix (largest / smallest singular value), rounded to 4 decimals. Large means solving A·x = b is sensitive to tiny errors.",
  [(([[3, 0], [4, 5]],), 3.0), (([[1, 2], [3, 4]],), 14.933)],
  ("Singular values by hand from AᵀA, then divide.", "O(1)", "O(1)"),
  ("<code>np.linalg.cond(A)</code>.", "O(n³)", "O(n)"))


@B
def condition(A):
    (a, b), (c, d) = A
    p, q, r = a * a + c * c, a * b + c * d, b * b + d * d
    tr, det = p + r, p * r - q * q
    disc = math.sqrt(tr * tr - 4 * det)
    return round(math.sqrt((tr + disc) / (tr - disc)), 4)


@O
def condition(A):
    return round(np.linalg.cond(np.array(A, dtype=float)), 4)


Q(None, "Error of the Best Rank-1 Approximation", "Hard", "Eckart–Young",
  "Return ‖A − A₁‖ (Frobenius norm) where A₁ is the best rank-1 approximation of the 2×2 matrix A, rounded to 4 decimals.",
  [(([[3, 1], [1, 3]],), 2.0), (([[4, 0], [3, -5]],), 3.1623)],
  ("Build A₁ = σ₁u₁v₁ᵀ by power iteration on AᵀA, subtract from A, take √(sum of squares).", "O(k)", "O(1)"),
  ("Eckart–Young: the error is just √(σ₂² + …) — the singular values you threw away.", "O(n³)", "O(n)"))


@B
def rank1_error(A):
    At_A = [[sum(A[k][i] * A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    v = [1.0, 0.3]
    for _ in range(200):
        w = [At_A[0][0] * v[0] + At_A[0][1] * v[1], At_A[1][0] * v[0] + At_A[1][1] * v[1]]
        nrm = math.sqrt(w[0] ** 2 + w[1] ** 2)
        v = [w[0] / nrm, w[1] / nrm]
    Av = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    A1 = [[Av[i] * v[j] for j in range(2)] for i in range(2)]
    err = sum((A[i][j] - A1[i][j]) ** 2 for i in range(2) for j in range(2))
    return round(math.sqrt(err), 4)


@O
def rank1_error(A):
    s = np.linalg.svd(np.array(A, dtype=float), compute_uv=False)
    return round(np.sqrt((s[1:] ** 2).sum()), 4)


Q(None, "PageRank of a Tiny Web", "Hard", "Eigenvector of the link matrix",
  "links[j] lists the pages page j links to. With damping 0.85, return each page's PageRank (sums to 1), rounded to 4 decimals.",
  [(([[1, 2], [2], [0]],), [0.3878, 0.2148, 0.3974]), (([[1], [0, 2], [0]],), [0.3974, 0.3878, 0.2148])],
  ("Power iteration: every page shares 0.85 of its rank equally among its links, plus 0.15/n for everyone; repeat.", "O(k·links)", "O(n)"),
  ("Solve the linear system (I − 0.85·M)·r = 0.15/n directly.", "O(n³)", "O(n²)"))


@B
def pagerank(links):
    n = len(links)
    rank = [1 / n] * n
    for _ in range(200):
        new = [0.15 / n] * n
        for j, outs in enumerate(links):
            for i in outs:
                new[i] += 0.85 * rank[j] / len(outs)
        rank = new
    return [round(r, 4) for r in rank]


@O
def pagerank(links):
    n = len(links)
    M = np.zeros((n, n))
    for j, outs in enumerate(links):
        M[outs, j] = 1 / len(outs)
    r = np.linalg.solve(np.eye(n) - 0.85 * M, np.full(n, 0.15 / n))
    return r.round(4)


Q(None, "Fibonacci From Eigenvalues", "Hard", "Binet's formula",
  "Return the n-th Fibonacci number (F₀ = 0, F₁ = 1).",
  [((10,), 55), ((1,), 1), ((30,), 832040)],
  ("Loop: keep the last two numbers.", "O(n)", "O(1)"),
  ("[[1, 1], [1, 0]] has eigenvalues φ = (1 + √5)/2 and ψ = (1 − √5)/2, so Fₙ = (φⁿ − ψⁿ)/√5.", "O(1)", "O(1)"))


@B
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@O
def fibonacci(n):
    phi, psi = np.linalg.eigvalsh(np.array([[1.0, 1.0], [1.0, 0.0]]))[::-1]
    return int(round((phi ** n - psi ** n) / math.sqrt(5)))
