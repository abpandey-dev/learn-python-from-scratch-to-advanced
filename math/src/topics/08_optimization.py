from lib import *
import math
import numpy as np

TOPIC(
    id="optimization", title="Gradients & Optimisation", glyph="∇",
    blurb="How machines learn: partial derivatives, the gradient, gradient descent and learning rates, fitting a line by descent, backpropagation through a neuron, logistic regression, Hessians and convexity.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">grad = np.array([df_dx, df_dy])           # the gradient: one partial derivative per input
w = w - lr * grad                          # one gradient-descent step
# MSE for y ≈ m·x + b:
err = y - (m * x + b)
dm, db = -2 * (x * err).mean(), -2 * err.mean()
# logistic regression:
p = 1 / (1 + np.exp(-(X @ w + b)))
grad_w, grad_b = X.T @ (p - y) / n, (p - y).mean()
# numerical gradient check:
(f(x + h) - f(x - h)) / (2 * h)</code></pre>
""")


Q(None, "Partial Derivatives", "Easy", "∂f/∂x and ∂f/∂y",
  "For f(x, y) = x²y + 3y², return (∂f/∂x, ∂f/∂y) at (x, y), rounded to 4 decimals.",
  [((1, 2), (4.0, 13.0)), ((3, -1), (-6.0, 3.0)), ((0, 0), (0.0, 0.0))],
  ("Numerically: nudge one variable at a time, keep the other fixed.", "O(1)", "O(1)"),
  ("By hand: treat the other variable as a constant → (2xy, x² + 6y).", "O(1)", "O(1)"))


@B
def partials(x, y):
    f = lambda x, y: x * x * y + 3 * y * y
    h = 1e-5
    dfdx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    dfdy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return (round(dfdx, 4) + 0.0, round(dfdy, 4) + 0.0)


@O
def partials(x, y):
    return (float(2 * x * y), float(x * x + 6 * y))


Q(None, "The Gradient Vector", "Easy", "∇f",
  "For f(x, y, z) = x² + 2y² + 3z² + xy, return ∇f at the point, rounded to 4 decimals.",
  [(([1, 1, 1],), [3.0, 5.0, 6.0]), (([2, -1, 0.5],), [3.0, -2.0, 3.0])],
  ("Central difference in each of the three directions.", "O(d)", "O(d)"),
  ("Analytic gradient (2x + y, 4y + x, 6z) with NumPy.", "O(1)", "O(d)"))


@B
def gradient(p):
    f = lambda v: v[0] ** 2 + 2 * v[1] ** 2 + 3 * v[2] ** 2 + v[0] * v[1]
    h = 1e-5
    out = []
    for i in range(3):
        up, down = list(p), list(p)
        up[i] += h
        down[i] -= h
        out.append(round((f(up) - f(down)) / (2 * h), 4) + 0.0)
    return out


@O
def gradient(p):
    x, y, z = p
    return np.array([2 * x + y, 4 * y + x, 6 * z], dtype=float).round(4)


Q(None, "Gradient of a Quadratic Form", "Medium", "∇(vᵀAv) = (A + Aᵀ)v",
  "Return the gradient of f(v) = vᵀ A v at v, rounded to 4 decimals.",
  [(([[2, 1], [0, 3]], [1, 2]), [6.0, 13.0]), (([[1, 2], [2, 1]], [1, -1]), [-2.0, 2.0])],
  ("Numerical partial derivative in each coordinate.", "O(d³)", "O(d)"),
  ("Matrix calculus: (A + Aᵀ)v — and 2Av when A is symmetric.", "O(d²)", "O(d)"))


@B
def quad_grad(A, v):
    def f(x):
        return sum(x[i] * A[i][j] * x[j] for i in range(len(x)) for j in range(len(x)))
    h = 1e-5
    out = []
    for i in range(len(v)):
        up, down = list(v), list(v)
        up[i] += h
        down[i] -= h
        out.append(round((f(up) - f(down)) / (2 * h), 4) + 0.0)
    return out


@O
def quad_grad(A, v):
    A = np.array(A, dtype=float)
    return ((A + A.T) @ np.array(v, dtype=float)).round(4)


Q(None, "Directional Derivative", "Medium", "∇f · u",
  "For f(x, y) = x² + y², return the rate of change at point p when moving in direction d (any length), rounded to 4 decimals.",
  [(([1, 2], [3, 4]), 4.4), (([1, 1], [1, 0]), 2.0)],
  ("Take a tiny step along the unit direction and measure the change.", "O(1)", "O(1)"),
  ("Dot the gradient (2x, 2y) with the unit direction.", "O(d)", "O(d)"))


@B
def directional(p, d):
    f = lambda x, y: x * x + y * y
    length = math.sqrt(d[0] ** 2 + d[1] ** 2)
    u = (d[0] / length, d[1] / length)
    h = 1e-5
    ahead = f(p[0] + h * u[0], p[1] + h * u[1])
    behind = f(p[0] - h * u[0], p[1] - h * u[1])
    return round((ahead - behind) / (2 * h), 4)


@O
def directional(p, d):
    g = 2 * np.array(p, dtype=float)
    u = np.array(d, dtype=float) / np.linalg.norm(d)
    return round(g @ u, 4)


Q(None, "Steepest Downhill Direction", "Easy", "−∇f / ‖∇f‖",
  "For f(x, y) = x² + 3y², return the unit direction of steepest descent at p, rounded to 4 decimals.",
  [(([1, 1],), [-0.3162, -0.9487]), (([2, 0],), [-1.0, 0.0]), (([0, -1],), [0.0, 1.0])],
  ("Numerical gradient, flip its sign, divide by its length.", "O(1)", "O(1)"),
  ("Analytic gradient (2x, 6y), then <code>-g / np.linalg.norm(g)</code>.", "O(1)", "O(1)"))


@B
def steepest(p):
    f = lambda x, y: x * x + 3 * y * y
    h = 1e-6
    gx = (f(p[0] + h, p[1]) - f(p[0] - h, p[1])) / (2 * h)
    gy = (f(p[0], p[1] + h) - f(p[0], p[1] - h)) / (2 * h)
    n = math.sqrt(gx * gx + gy * gy)
    return [round(-gx / n, 4) + 0.0, round(-gy / n, 4) + 0.0]


@O
def steepest(p):
    g = np.array([2 * p[0], 6 * p[1]], dtype=float)
    return (-g / np.linalg.norm(g)).round(4) + 0.0


Q(None, "One Gradient-Descent Step", "Easy", "w ← w − lr·∇f",
  "For f(x, y) = x² + 3y², return the point after one step from p with learning rate lr, rounded to 4 decimals.",
  [(([1, 1], 0.1), [0.8, 0.4]), (([2, -1], 0.05), [1.8, -0.7])],
  ("Gradient numerically, then move each coordinate against it.", "O(d)", "O(d)"),
  ("Analytic gradient and one vector update.", "O(d)", "O(d)"),
  names=["p", "lr"])


@B
def gd_step(p, lr):
    f = lambda x, y: x * x + 3 * y * y
    h = 1e-6
    gx = (f(p[0] + h, p[1]) - f(p[0] - h, p[1])) / (2 * h)
    gy = (f(p[0], p[1] + h) - f(p[0], p[1] - h)) / (2 * h)
    return [round(p[0] - lr * gx, 4), round(p[1] - lr * gy, 4)]


@O
def gd_step(p, lr):
    p = np.array(p, dtype=float)
    grad = np.array([2 * p[0], 6 * p[1]])
    return (p - lr * grad).round(4)


Q(None, "Gradient Descent in 1-D", "Easy", "Walking downhill",
  "Minimise f(x) = (x − 3)² starting at x0 with learning rate lr for n steps. Return the final x, rounded to 4 decimals.",
  [((0, 0.1, 10), 2.6779), ((10, 0.25, 3), 3.875), ((5, 0.5, 1), 3.0)],
  ("Loop: x ← x − lr·2(x − 3).", "O(n)", "O(1)"),
  ("Each step multiplies the distance to 3 by (1 − 2·lr), so x = 3 + (x0 − 3)(1 − 2lr)ⁿ.", "O(1)", "O(1)"),
  names=["x0", "lr", "n"])


@B
def gd_1d(x0, lr, n):
    x = x0
    for _ in range(n):
        grad = 2 * (x - 3)
        x = x - lr * grad
    return round(x, 4)


@O
def gd_1d(x0, lr, n):
    return round(3 + (x0 - 3) * (1 - 2 * lr) ** n, 4)


Q(None, "Is the Learning Rate Too Big?", "Medium", "Loss curve",
  "Minimise f(x) = x² from x0 with learning rate lr. Return the loss after each of n steps, rounded to 4 decimals. (Rising losses = diverging.)",
  [((1, 0.1, 4), [0.64, 0.4096, 0.2621, 0.1678]), ((1, 1.1, 4), [1.44, 2.0736, 2.986, 4.2998])],
  ("Simulate the steps and record x² each time.", "O(n)", "O(n)"),
  ("Closed form for every step at once: xₖ = x0(1 − 2lr)ᵏ.", "O(n)", "O(n)"),
  names=["x0", "lr", "n"])


@B
def loss_curve(x0, lr, n):
    x = x0
    losses = []
    for _ in range(n):
        x = x - lr * 2 * x
        losses.append(round(x * x, 4))
    return losses


@O
def loss_curve(x0, lr, n):
    xs = x0 * (1 - 2 * lr) ** np.arange(1, n + 1)
    return (xs ** 2).round(4)


Q(None, "Descent in a Long Narrow Valley", "Medium", "Different curvature per direction",
  "Minimise f(x, y) = x² + 10y² from p with learning rate lr for n steps. Return the final point, rounded to 4 decimals.",
  [(([1, 1], 0.05, 10), [0.3487, 0.0]), (([2, 1], 0.09, 5), [0.7415, -0.3277])],
  ("Loop the 2-D update.", "O(n)", "O(1)"),
  ("Each coordinate shrinks independently: x·(1 − 2lr)ⁿ and y·(1 − 20lr)ⁿ.", "O(1)", "O(1)"),
  names=["p", "lr", "n"])


@B
def narrow_valley(p, lr, n):
    x, y = p
    for _ in range(n):
        x, y = x - lr * 2 * x, y - lr * 20 * y
    return [round(x, 4) + 0.0, round(y, 4) + 0.0]


@O
def narrow_valley(p, lr, n):
    shrink = np.array([1 - 2 * lr, 1 - 20 * lr]) ** n
    return (np.array(p) * shrink).round(4) + 0.0


Q(None, "Mean Squared Error of a Line", "Easy", "The loss",
  "Return the MSE of predictions m·x + b on the data, rounded to 4 decimals.",
  [(([1, 2, 3], [2, 4, 7], 2, 0), 0.3333), (([1, 2, 3], [2, 4, 7], 1, 1), 3.3333)],
  ("Loop: error, square, average.", "O(n)", "O(1)"),
  ("Vectorised: <code>((y - (m*x + b))**2).mean()</code>.", "O(n)", "O(n)"),
  names=["x", "y", "m", "b"])


@B
def mse(x, y, m, b):
    total = 0
    for xi, yi in zip(x, y):
        total += (yi - (m * xi + b)) ** 2
    return round(total / len(x), 4)


@O
def mse(x, y, m, b):
    x, y = np.array(x), np.array(y)
    return round(((y - (m * x + b)) ** 2).mean(), 4)


Q(None, "Gradient of the MSE", "Medium", "∂L/∂m and ∂L/∂b",
  "Return (∂MSE/∂m, ∂MSE/∂b) for the line m·x + b, rounded to 4 decimals.",
  [(([1, 2, 3], [2, 4, 7], 2, 0), (-2.0, -0.6667)), (([1, 2, 3], [2, 4, 7], 1, 1), (-7.3333, -2.6667))],
  ("Chain rule term by term in a loop: each point contributes −2x·error and −2·error.", "O(n)", "O(1)"),
  ("Vectorised means of −2·x·err and −2·err.", "O(n)", "O(n)"),
  names=["x", "y", "m", "b"])


@B
def mse_grad(x, y, m, b):
    n = len(x)
    dm = db = 0
    for xi, yi in zip(x, y):
        err = yi - (m * xi + b)
        dm += -2 * xi * err / n
        db += -2 * err / n
    return (round(dm, 4), round(db, 4))


@O
def mse_grad(x, y, m, b):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    err = y - (m * x + b)
    return (round(-2 * (x * err).mean(), 4), round(-2 * err.mean(), 4))


Q(None, "Fit a Line by Gradient Descent", "Hard", "Training loop",
  "Start at m = b = 0 and run n steps of gradient descent on the MSE with learning rate lr. Return (m, b) rounded to 4 decimals.",
  [(([1, 2, 3, 4], [3, 5, 7, 9], 0.05, 2000), (2.0, 1.0)), (([1, 2, 3], [2, 4, 7], 0.05, 1000), (2.5, -0.6667))],
  ("Plain loops: compute both gradients point by point, update, repeat.", "O(n·steps)", "O(1)"),
  ("Same algorithm with vectorised gradients — the shape of every real training loop.", "O(n·steps)", "O(n)"),
  names=["x", "y", "lr", "steps"])


@B
def fit_line(x, y, lr, steps):
    m = b = 0.0
    n = len(x)
    for _ in range(steps):
        dm = db = 0.0
        for xi, yi in zip(x, y):
            err = yi - (m * xi + b)
            dm += -2 * xi * err / n
            db += -2 * err / n
        m -= lr * dm
        b -= lr * db
    return (round(m, 4), round(b, 4))


@O
def fit_line(x, y, lr, steps):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    m = b = 0.0
    for _ in range(steps):
        err = y - (m * x + b)
        m -= lr * -2 * (x * err).mean()
        b -= lr * -2 * err.mean()
    return (round(m, 4), round(b, 4))


Q(None, "Chain Rule Through a Computation", "Medium", "dy/dx of sin(3x² + 1)",
  "Return dy/dx of y = sin(3x² + 1) at x, rounded to 4 decimals.",
  [((0.5,), -0.5347), ((1.0,), -3.9219), ((0,), 0.0)],
  ("Numerical central difference of the whole expression.", "O(1)", "O(1)"),
  ("Chain rule stage by stage: u = 3x² + 1 → du/dx = 6x; y = sin u → dy/du = cos u; multiply.", "O(1)", "O(1)"))


@B
def chain(x):
    f = lambda t: math.sin(3 * t * t + 1)
    h = 1e-6
    return round((f(x + h) - f(x - h)) / (2 * h), 4) + 0.0


@O
def chain(x):
    u = 3 * x * x + 1
    du_dx = 6 * x
    dy_du = math.cos(u)
    return round(dy_du * du_dx, 4) + 0.0


Q(None, "Backpropagation Through One Neuron", "Hard", "ŷ = σ(wx + b), L = (ŷ − y)²",
  "Return (∂L/∂w, ∂L/∂b) for one training example, rounded to 4 decimals.",
  [((0.5, 0.1, 2, 1), (-0.1872, -0.0936)), ((-1, 0, 1, 0), (0.1058, 0.1058))],
  ("Numerical: nudge w (then b) and see how the loss changes.", "O(1)", "O(1)"),
  ("Backprop: dL/dŷ = 2(ŷ − y), dŷ/dz = ŷ(1 − ŷ), dz/dw = x, dz/db = 1 — multiply along the chain.", "O(1)", "O(1)"),
  names=["w", "b", "x", "y"])


@B
def backprop(w, b, x, y):
    def loss(w, b):
        y_hat = 1 / (1 + math.exp(-(w * x + b)))
        return (y_hat - y) ** 2
    h = 1e-6
    dw = (loss(w + h, b) - loss(w - h, b)) / (2 * h)
    db = (loss(w, b + h) - loss(w, b - h)) / (2 * h)
    return (round(dw, 4), round(db, 4))


@O
def backprop(w, b, x, y):
    z = w * x + b
    y_hat = 1 / (1 + math.exp(-z))
    dL_dyhat = 2 * (y_hat - y)
    dyhat_dz = y_hat * (1 - y_hat)
    dL_dz = dL_dyhat * dyhat_dz
    return (round(dL_dz * x, 4), round(dL_dz, 4))


Q(None, "One Step of Logistic Regression", "Hard", "Log-loss gradient",
  "Probabilities p = σ(X·w + b). Return (new w, new b) after one gradient step on the average log-loss with learning rate lr (rounded to 4 decimals).",
  [(([[1, 2], [2, 1], [3, 3], [0, 1]], [1, 0, 1, 0], [0, 0], 0, 0.5), ([0.125, 0.1875], 0.0)),
   (([[1, 2], [2, 1], [3, 3], [0, 1]], [1, 0, 1, 0], [0.5, -0.5], 0.1, 0.1), ([0.5183, -0.4606], 0.1007))],
  ("Loop over examples: p − y is each one's error; accumulate error × feature.", "O(n·d)", "O(d)"),
  ("Vectorised: ∇w = Xᵀ(p − y)/n, ∇b = mean(p − y).", "O(n·d)", "O(n)"),
  names=["X", "y", "w", "b", "lr"])


@B
def logreg_step(X, y, w, b, lr):
    n, d = len(X), len(w)
    gw = [0.0] * d
    gb = 0.0
    for row, target in zip(X, y):
        z = b + sum(wi * xi for wi, xi in zip(w, row))
        p = 1 / (1 + math.exp(-z))
        for j in range(d):
            gw[j] += (p - target) * row[j] / n
        gb += (p - target) / n
    new_w = [round(wi - lr * g, 4) for wi, g in zip(w, gw)]
    return (new_w, round(b - lr * gb, 4))


@O
def logreg_step(X, y, w, b, lr):
    X, y, w = np.array(X, dtype=float), np.array(y, dtype=float), np.array(w, dtype=float)
    p = 1 / (1 + np.exp(-(X @ w + b)))
    grad_w = X.T @ (p - y) / len(y)
    grad_b = (p - y).mean()
    return ((w - lr * grad_w).round(4), round(b - lr * grad_b, 4))


Q(None, "The Hessian Matrix", "Medium", "Second partial derivatives",
  "For f(x, y) = a·x² + b·xy + c·y², return the Hessian [[f_xx, f_xy], [f_yx, f_yy]] (rounded to 2 decimals).",
  [((1, 2, 3), [[2.0, 2.0], [2.0, 6.0]]), ((2, -1, 0.5), [[4.0, -1.0], [-1.0, 1.0]])],
  ("Numerical second differences at the origin.", "O(1)", "O(1)"),
  ("Differentiate twice by hand: [[2a, b], [b, 2c]].", "O(1)", "O(1)"))


@B
def hessian(a, b, c):
    f = lambda x, y: a * x * x + b * x * y + c * y * y
    h = 1e-3
    fxx = (f(h, 0) - 2 * f(0, 0) + f(-h, 0)) / (h * h)
    fyy = (f(0, h) - 2 * f(0, 0) + f(0, -h)) / (h * h)
    fxy = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
    return [[round(fxx, 2), round(fxy, 2)], [round(fxy, 2), round(fyy, 2)]]


@O
def hessian(a, b, c):
    return np.array([[2 * a, b], [b, 2 * c]], dtype=float)


Q(None, "Is the Bowl Convex?", "Medium", "Positive semi-definite Hessian",
  "f(x, y) = a·x² + b·xy + c·y². Return True if f is convex (its Hessian has no negative eigenvalues).",
  [((1, 2, 3), True), ((2, -1, 0.5), True), ((1, 3, 1), False), ((-1, 0, 1), False)],
  ("2×2 test by hand: diagonal entries ≥ 0 and determinant ≥ 0.", "O(1)", "O(1)"),
  ("<code>np.linalg.eigvalsh(H).min() &gt;= 0</code> — works for any size.", "O(d³)", "O(d)"))


@B
def is_convex(a, b, c):
    fxx, fyy, fxy = 2 * a, 2 * c, b
    det = fxx * fyy - fxy * fxy
    return fxx >= 0 and fyy >= 0 and det >= 0


@O
def is_convex(a, b, c):
    H = np.array([[2 * a, b], [b, 2 * c]], dtype=float)
    return bool(np.linalg.eigvalsh(H).min() >= -1e-12)


Q(None, "Bottom of a Quadratic Bowl", "Hard", "∇f = 0 ⇒ Av = b",
  "f(v) = ½ vᵀAv − bᵀv with A symmetric positive-definite. Return the minimiser, rounded to 4 decimals.",
  [(([[3, 1], [1, 2]], [1, 1]), [0.2, 0.4]), (([[2, 0], [0, 4]], [4, 2]), [2.0, 0.5])],
  ("Gradient descent: v ← v − lr·(Av − b), many small steps.", "O(steps·d²)", "O(d)"),
  ("Set the gradient to zero and solve the linear system <code>np.linalg.solve(A, b)</code>.", "O(d³)", "O(d²)"))


@B
def quad_min(A, b):
    v = [0.0] * len(b)
    for _ in range(2000):
        grad = [sum(A[i][j] * v[j] for j in range(len(v))) - b[i] for i in range(len(v))]
        v = [vi - 0.1 * g for vi, g in zip(v, grad)]
    return [round(x, 4) for x in v]


@O
def quad_min(A, b):
    return np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float)).round(4)


Q(None, "Mini-batch Gradient", "Medium", "Averaging over a batch",
  "Model ŷ = w·x, loss = mean (y − ŷ)². Return the gradient dL/dw over the batch, rounded to 4 decimals.",
  [((1.0, [1, 2, 3], [2, 4, 6]), -9.3333), ((0.0, [1, 2], [1, 1]), -3.0)],
  ("Loop over the batch adding each example's −2x(y − wx), then divide by the batch size.", "O(n)", "O(1)"),
  ("Vectorised mean.", "O(n)", "O(n)"),
  names=["w", "x", "y"])


@B
def batch_grad(w, x, y):
    total = 0
    for xi, yi in zip(x, y):
        total += -2 * xi * (yi - w * xi)
    return round(total / len(x), 4)


@O
def batch_grad(w, x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    return round((-2 * x * (y - w * x)).mean(), 4)


Q(None, "Newton's Method for a Minimum", "Hard", "x ← x − f′/f″",
  "Minimise f(x) = x⁴ − 3x² + x starting at x0 for n Newton steps. Return x rounded to 4 decimals.",
  [((1.0, 5), 1.1309), ((-2.0, 6), -1.3008)],
  ("Estimate f′ and f″ numerically from f at each step.", "O(n)", "O(1)"),
  ("Use the exact derivatives f′ = 4x³ − 6x + 1, f″ = 12x² − 6.", "O(n)", "O(1)"),
  names=["x0", "n"])


@B
def newton_min(x0, n):
    f = lambda x: x ** 4 - 3 * x ** 2 + x
    h = 1e-4
    x = x0
    for _ in range(n):
        d1 = (f(x + h) - f(x - h)) / (2 * h)
        d2 = (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)
        x = x - d1 / d2
    return round(x, 4)


@O
def newton_min(x0, n):
    x = x0
    for _ in range(n):
        x = x - (4 * x ** 3 - 6 * x + 1) / (12 * x ** 2 - 6)
    return round(x, 4)
