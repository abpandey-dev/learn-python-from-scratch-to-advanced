from lib import *
import math
import numpy as np

TOPIC(
    id="calculus", title="Calculus: Derivatives & Integrals", glyph="d/dx",
    blurb="The math of change. Slopes of curves, the derivative rules, finding minimums and maximums, Newton's method, and areas under curves.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">(f(x + h) - f(x)) / h               # derivative from the definition (small h)
(f(x + h) - f(x - h)) / (2 * h)     # central difference — more accurate
np.polyder([3, 0, -2, 5])           # d/dx (3x³ − 2x + 5) = 9x² − 2
np.polyder(p, 2)                    # second derivative
np.polyint([3, 2, 1])               # ∫ (3x² + 2x + 1) dx = x³ + x² + x
np.gradient(y, dx)                  # derivative of sampled data
(y[:-1] + y[1:]).sum() * dx / 2     # trapezoid rule</code></pre>
<table><tr><th>f(x)</th><th>f′(x)</th></tr>
<tr><td>xⁿ</td><td>n·xⁿ⁻¹</td></tr><tr><td>eˣ</td><td>eˣ</td></tr><tr><td>ln x</td><td>1/x</td></tr>
<tr><td>sin x</td><td>cos x</td></tr><tr><td>σ(x)</td><td>σ(x)(1 − σ(x))</td></tr></table>
""")


Q(None, "Derivative From the Definition", "Easy", "Shrinking the secant",
  "For f(x) = x², return the slope estimates (f(a + h) − f(a))/h for h = 0.1, 0.01 and 0.001, rounded to 4 decimals. Watch them approach 2a.",
  [((3,), [6.1, 6.01, 6.001]), ((0,), [0.1, 0.01, 0.001]), ((-1,), [-1.9, -1.99, -1.999])],
  ("A loop over the three h values.", "O(1)", "O(1)"),
  ("All three at once with an array of h values.", "O(1)", "O(1)"))


@B
def secant_slopes(a):
    out = []
    for h in [0.1, 0.01, 0.001]:
        rise = (a + h) ** 2 - a ** 2
        out.append(round(rise / h, 4))
    return out


@O
def secant_slopes(a):
    h = np.array([0.1, 0.01, 0.001])
    return (((a + h) ** 2 - a ** 2) / h).round(4)


Q(None, "Derivative of sin x", "Easy", "Numerical vs exact",
  "Return the derivative of sin at x, rounded to 4 decimals.",
  [((1.0,), 0.5403), ((0,), 1.0), ((2,), -0.4161)],
  ("Central difference (sin(x + h) − sin(x − h)) / 2h with a tiny h.", "O(1)", "O(1)"),
  ("Use the rule: d/dx sin x = cos x.", "O(1)", "O(1)"))


@B
def dsin(x):
    h = 1e-5
    return round((math.sin(x + h) - math.sin(x - h)) / (2 * h), 4)


@O
def dsin(x):
    return round(math.cos(x), 4)


Q(None, "Power Rule for Polynomials", "Easy", "d/dx xⁿ = n·xⁿ⁻¹",
  "Return the derivative's coefficients (highest power first). [3, 0, -2, 5] = 3x³ − 2x + 5 → [9, 0, -2].",
  [(([3, 0, -2, 5],), [9, 0, -2]), (([1, 0, 0, 0, 0],), [4, 0, 0, 0]), (([2, 5],), [2])],
  ("Each term c·xᵏ becomes k·c·xᵏ⁻¹; the constant disappears.", "O(n)", "O(n)"),
  ("<code>np.polyder(p)</code>.", "O(n)", "O(n)"))


@B
def derivative(p):
    n = len(p) - 1
    if n == 0:
        return [0]
    out = []
    for i, c in enumerate(p[:-1]):
        power = n - i
        out.append(c * power)
    return out


@O
def derivative(p):
    return np.polyder(p)


Q(None, "Slope of a Curve at a Point", "Easy", "f′(a)",
  "Return the derivative of the polynomial p at x = a.",
  [(([1, -3, 2], 4), 5), (([2, 0, 0, -1], -1), 6), (([5, 1], 100), 5)],
  ("Power rule by hand, then substitute a.", "O(n)", "O(n)"),
  ("<code>np.polyval(np.polyder(p), a)</code>.", "O(n)", "O(n)"))


@B
def slope_at(p, a):
    n = len(p) - 1
    total = 0
    for i, c in enumerate(p[:-1]):
        k = n - i
        total += c * k * a ** (k - 1)
    return total


@O
def slope_at(p, a):
    return np.polyval(np.polyder(p), a)


Q(None, "Tangent Line", "Medium", "y = f′(a)(x − a) + f(a)",
  "Return (slope, intercept) of the tangent to the polynomial p at x = a.",
  [(([1, 0, 0], 3), (6, -9)), (([1, -2, 1], 0), (-2, 1)), (([1, 0, 0, 0], 2), (12, -16))],
  ("Slope by the power rule, point f(a), then c = f(a) − slope·a.", "O(n)", "O(1)"),
  ("NumPy <code>polyder</code> and <code>polyval</code>.", "O(n)", "O(n)"))


@B
def tangent(p, a):
    n = len(p) - 1
    fa = sum(c * a ** (n - i) for i, c in enumerate(p))
    m = sum(c * (n - i) * a ** (n - i - 1) for i, c in enumerate(p[:-1]))
    return (m, fa - m * a)


@O
def tangent(p, a):
    m = np.polyval(np.polyder(p), a)
    return (m, np.polyval(p, a) - m * a)


Q(None, "Product Rule", "Medium", "(fg)′ = f′g + fg′",
  "Return the coefficients of the derivative of f(x)·g(x) (polynomials, highest power first).",
  [(([1, 1], [1, -1]), [2, 0]), (([2, 0], [1, 0, 3]), [6, 0, 6])],
  ("Apply the product rule: multiply f′ by g, f by g′, add the two polynomials.", "O(n·m)", "O(n + m)"),
  ("Multiply first, then differentiate: <code>np.polyder(np.polymul(f, g))</code>.", "O(n·m)", "O(n + m)"))


@B
def product_rule(f, g):
    def der(p):
        n = len(p) - 1
        return [c * (n - i) for i, c in enumerate(p[:-1])] or [0]

    def mul(p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                out[i + j] += a * b
        return out

    left, right = mul(der(f), g), mul(f, der(g))
    size = max(len(left), len(right))
    left = [0] * (size - len(left)) + left
    right = [0] * (size - len(right)) + right
    return [a + b for a, b in zip(left, right)]


@O
def product_rule(f, g):
    return np.polyder(np.polymul(f, g))


Q(None, "Chain Rule", "Medium", "d/dx (ax + b)ⁿ",
  "Return the derivative of (a·x + b)ⁿ at x = x0.",
  [((2, 1, 3, 1), 54), ((3, -1, 2, 0), -6), ((1, 0, 5, 2), 80)],
  ("Chain rule: outer derivative n·(inside)ⁿ⁻¹ times inner derivative a.", "O(1)", "O(1)"),
  ("Expand (ax + b)ⁿ with <code>np.poly1d</code>, then differentiate and evaluate.", "O(n²)", "O(n)"),
  names=["a", "b", "n", "x0"])


@B
def chain_rule(a, b, n, x0):
    inside = a * x0 + b
    outer = n * inside ** (n - 1)
    inner = a
    return outer * inner


@O
def chain_rule(a, b, n, x0):
    p = np.poly1d([a, b]) ** n
    return int(p.deriv()(x0))


Q(None, "Derivative of the Sigmoid", "Medium", "σ′ = σ(1 − σ)",
  "Return σ′(x) for each x, rounded to 4 decimals.",
  [(([0, 2, -1],), [0.25, 0.105, 0.1966])],
  ("Numerically: central difference of σ for each x.", "O(n)", "O(n)"),
  ("Use the identity σ′(x) = σ(x)(1 − σ(x)) — no extra evaluations, which is why backprop loves it.", "O(n)", "O(n)"))


@B
def dsigmoid(xs):
    sig = lambda z: 1 / (1 + math.exp(-z))
    h = 1e-5
    return [round((sig(x + h) - sig(x - h)) / (2 * h), 4) for x in xs]


@O
def dsigmoid(xs):
    s = 1 / (1 + np.exp(-np.array(xs, dtype=float)))
    return (s * (1 - s)).round(4)


Q(None, "Critical Points of a Cubic", "Medium", "Where f′(x) = 0",
  "Return the x-values where the cubic's slope is zero, sorted, rounded to 4 decimals.",
  [(([1, 0, -3, 0],), [-1.0, 1.0]), (([1, -6, 9, 1],), [1.0, 3.0]), (([2, -3, -12, 0],), [-1.0, 2.0])],
  ("Differentiate by hand to a quadratic, solve it with the quadratic formula.", "O(1)", "O(1)"),
  ("<code>np.roots(np.polyder(p))</code>.", "O(1)", "O(1)"))


@B
def critical_points(p):
    a, b, c, d = p
    A, B, C = 3 * a, 2 * b, c
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    r = math.sqrt(disc)
    return sorted([round((-B - r) / (2 * A), 4), round((-B + r) / (2 * A), 4)])


@O
def critical_points(p):
    r = np.roots(np.polyder(p))
    return np.sort(r[np.isclose(r.imag, 0)].real).round(4)


Q(None, "Maximum or Minimum?", "Medium", "Second-derivative test",
  "For each critical point of the cubic, return 'max' if f″ &lt; 0 there, 'min' if f″ &gt; 0.",
  [(([1, 0, -3, 0],), ["max", "min"]), (([-1, 0, 3, 0],), ["min", "max"])],
  ("Find the critical points by the quadratic formula, then f″(x) = 6ax + 2b by hand.", "O(1)", "O(1)"),
  ("<code>np.roots</code> of f′, then the sign of <code>np.polyval(np.polyder(p, 2), x)</code>.", "O(1)", "O(1)"))


@B
def classify(p):
    a, b, c, d = p
    disc = (2 * b) ** 2 - 12 * a * c
    roots = sorted([(-2 * b - math.sqrt(disc)) / (6 * a), (-2 * b + math.sqrt(disc)) / (6 * a)])
    out = []
    for x in roots:
        second = 6 * a * x + 2 * b
        out.append("max" if second < 0 else "min")
    return out


@O
def classify(p):
    xs = np.sort(np.roots(np.polyder(p)).real)
    return ["max" if np.polyval(np.polyder(p, 2), x) < 0 else "min" for x in xs]


Q(None, "Second Derivative", "Easy", "Curvature",
  "Return the coefficients of f″ for polynomial p.",
  [(([1, 2, 3, 4],), [6, 4]), (([5, 0, 0],), [10])],
  ("Apply the power rule twice.", "O(n)", "O(n)"),
  ("<code>np.polyder(p, 2)</code>.", "O(n)", "O(n)"))


@B
def second_derivative(p):
    for _ in range(2):
        n = len(p) - 1
        p = [c * (n - i) for i, c in enumerate(p[:-1])]
    return p


@O
def second_derivative(p):
    return np.polyder(p, 2)


Q(None, "Newton's Method", "Medium", "x ← x − f(x)/f′(x)",
  "Find the root of x³ − x − 2 starting from x0, rounded to 4 decimals.",
  [((1.0,), 1.5214), ((3.0,), 1.5214)],
  ("Follow the tangent line down to the x-axis, repeat ~20 times.", "O(iterations)", "O(1)"),
  ("<code>np.roots([1, 0, -1, -2])</code> and take the real root.", "O(1)", "O(1)"))


@B
def newton(x0):
    x = x0
    for _ in range(20):
        fx = x ** 3 - x - 2
        dfx = 3 * x ** 2 - 1
        x = x - fx / dfx
    return round(x, 4)


@O
def newton(x0):
    r = np.roots([1, 0, -1, -2])
    return round(r[np.isclose(r.imag, 0)].real[0], 4)


Q(None, "Lowest Point of a Curve", "Medium", "Optimisation with f′ = 0",
  "Return (x, f(x)) of the global minimum of f(x) = x⁴ − 3x³ + 2, rounded to 4 decimals.",
  [((), (2.25, -6.543))],
  ("Scan a fine grid from −5 to 5 and keep the lowest value.", "O(grid)", "O(1)"),
  ("Solve f′(x) = 4x³ − 9x² = 0 with <code>np.roots</code>, evaluate f at each, keep the smallest.", "O(1)", "O(1)"))


@B
def lowest_point():
    best_x, best_y = None, None
    for i in range(-5000, 5001):
        x = i / 1000
        y = x ** 4 - 3 * x ** 3 + 2
        if best_y is None or y < best_y:
            best_x, best_y = x, y
    return (round(best_x, 4), round(best_y, 4))


@O
def lowest_point():
    p = [1, -3, 0, 0, 2]
    xs = np.roots(np.polyder(p)).real
    ys = np.polyval(p, xs)
    i = ys.argmin()
    return (round(xs[i], 4), round(ys[i], 4))


Q(None, "Area by Rectangles", "Easy", "Left Riemann sum",
  "Estimate the area under f(x) = x² from a to b with n left-endpoint rectangles, rounded to 4 decimals.",
  [((0, 2, 4), 1.75), ((0, 3, 6), 6.875), ((1, 2, 10), 2.185)],
  ("Loop over the rectangles: width × height at the left edge.", "O(n)", "O(1)"),
  ("Make all left edges with <code>np.arange</code> and sum.", "O(n)", "O(n)"))


@B
def left_sum(a, b, n):
    width = (b - a) / n
    total = 0
    for i in range(n):
        x = a + i * width
        total += x ** 2 * width
    return round(total, 4)


@O
def left_sum(a, b, n):
    dx = (b - a) / n
    x = a + dx * np.arange(n)
    return round((x ** 2).sum() * dx, 4)


Q(None, "Distance From Speed Readings", "Easy", "Trapezoid rule",
  "Speeds (m/s) were recorded every dt seconds. Return the distance travelled using the trapezoid rule.",
  [(([0, 1, 4, 9], 1), 9.5), (([2, 2, 2], 0.5), 2.0), (([0, 10, 15, 15, 10], 2), 90.0)],
  ("Each strip is a trapezoid: (left + right)/2 × dt; add them.", "O(n)", "O(1)"),
  ("Vectorised: <code>(v[:-1] + v[1:]).sum() * dt / 2</code>.", "O(n)", "O(n)"),
  names=["speeds", "dt"])


@B
def distance(speeds, dt):
    total = 0
    for i in range(len(speeds) - 1):
        total += (speeds[i] + speeds[i + 1]) / 2 * dt
    return total


@O
def distance(speeds, dt):
    v = np.array(speeds, dtype=float)
    return (v[:-1] + v[1:]).sum() * dt / 2


Q(None, "Antiderivative of a Polynomial", "Easy", "∫ xⁿ dx = xⁿ⁺¹/(n + 1)",
  "Return the coefficients of the antiderivative with constant 0. [3, 2, 1] → [1, 1, 1, 0].",
  [(([3, 2, 1],), [1, 1, 1, 0]), (([4, 0, 0, -2],), [1, 0, 0, -2, 0])],
  ("Reverse the power rule term by term.", "O(n)", "O(n)"),
  ("<code>np.polyint(p)</code>.", "O(n)", "O(n)"))


@B
def antiderivative(p):
    n = len(p) - 1
    out = []
    for i, c in enumerate(p):
        k = n - i
        out.append(c / (k + 1))
    return out + [0]


@O
def antiderivative(p):
    return np.polyint(p)


Q(None, "Exact Area Under a Polynomial", "Medium", "Fundamental theorem of calculus",
  "Return ∫ from a to b of the polynomial p, rounded to 4 decimals.",
  [(([3, 0, 0], 0, 2), 8.0), (([1, 1], 1, 3), 6.0), (([4, 0, -2, 0], -1, 1), 0.0)],
  ("Antiderivative F by hand, then F(b) − F(a).", "O(n)", "O(n)"),
  ("<code>np.polyint</code> and <code>np.polyval</code>.", "O(n)", "O(n)"))


@B
def definite(p, a, b):
    n = len(p) - 1
    F = lambda x: sum(c / (n - i + 1) * x ** (n - i + 1) for i, c in enumerate(p))
    return round(F(b) - F(a), 4)


@O
def definite(p, a, b):
    P = np.polyint(p)
    return round(np.polyval(P, b) - np.polyval(P, a), 4)


Q(None, "Average Value of a Function", "Medium", "(1/(b − a)) ∫ f",
  "Return the average value of f(x) = x² on [a, b], rounded to 4 decimals.",
  [((0, 3), 3.0), ((1, 2), 2.3333)],
  ("Midpoint rule with 1000 strips, divide by the width.", "O(n)", "O(1)"),
  ("Exact: (b³ − a³) / (3(b − a)).", "O(1)", "O(1)"))


@B
def average_value(a, b):
    n = 1000
    dx = (b - a) / n
    area = 0
    for i in range(n):
        x = a + (i + 0.5) * dx
        area += x * x * dx
    return round(area / (b - a), 4)


@O
def average_value(a, b):
    return round((b ** 3 - a ** 3) / (3 * (b - a)), 4)


Q(None, "Area Between Two Curves", "Hard", "∫ (top − bottom)",
  "Return the area enclosed between y = x and y = x² (between their crossing points) scaled by k: curves y = k·x and y = x². Rounded to 4 decimals.",
  [((1,), 0.1667), ((2,), 1.3333)],
  ("Midpoint rule on (kx − x²) between 0 and k with many strips.", "O(n)", "O(1)"),
  ("Crossing points from <code>np.roots</code>, then integrate the difference exactly with <code>np.polyint</code>.", "O(1)", "O(1)"))


@B
def area_between(k):
    n = 2000
    dx = k / n
    area = 0
    for i in range(n):
        x = (i + 0.5) * dx
        area += (k * x - x * x) * dx
    return round(area, 4)


@O
def area_between(k):
    diff = np.polysub([k, 0], [1, 0, 0])
    a, b = np.sort(np.roots(diff).real)
    F = np.polyint(diff)
    return round(np.polyval(F, b) - np.polyval(F, a), 4)


Q(None, "Speed From Position Readings", "Medium", "Derivative of data",
  "Positions were recorded every dt seconds. Return the speed at each reading: central differences inside, one-sided at the ends.",
  [(([0, 1, 4, 9, 16], 1), [1.0, 2.0, 4.0, 6.0, 7.0]), (([0, 5, 20, 45], 0.5), [10.0, 20.0, 40.0, 50.0])],
  ("Loop: (next − previous)/(2·dt) inside, simple differences at the two ends.", "O(n)", "O(n)"),
  ("<code>np.gradient(positions, dt)</code>.", "O(n)", "O(n)"),
  names=["positions", "dt"])


@B
def speeds(positions, dt):
    n = len(positions)
    out = [(positions[1] - positions[0]) / dt]
    for i in range(1, n - 1):
        out.append((positions[i + 1] - positions[i - 1]) / (2 * dt))
    out.append((positions[-1] - positions[-2]) / dt)
    return out


@O
def speeds(positions, dt):
    return np.gradient(np.array(positions, dtype=float), dt)
