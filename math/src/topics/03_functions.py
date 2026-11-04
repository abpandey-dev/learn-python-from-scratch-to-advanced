from lib import *
import math
import numpy as np

TOPIC(
    id="functions", title="Functions & Graphs", glyph="f(x)",
    blurb="A function is a machine: input in, one output out. Lines and slope, parabolas, exponentials, logarithms, and the activation functions used in neural networks.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">x = np.linspace(-5, 5, 101)         # many inputs at once
y = 2 * x + 1                        # a straight line: slope 2, intercept 1
m = (y2 - y1) / (x2 - x1)            # slope between two points
-b / (2 * a)                         # x of a parabola's vertex
np.exp(x), np.log(x), np.log10(x), np.log2(x)
1 / (1 + np.exp(-x))                 # sigmoid
np.maximum(0, x)                     # ReLU
plt.plot(x, y)                       # draw it</code></pre>
<p><b>Log rules</b>: log(ab) = log a + log b, log(a/b) = log a − log b, log(aⁿ) = n·log a, log_b(x) = ln x / ln b.</p>
""")


Q(None, "Table of Values", "Easy", "Evaluating a function",
  "For f(x) = 2x² − 3, return the outputs for every x in xs.",
  [(([-2, -1, 0, 1, 2],), [5, -1, -3, -1, 5]), (([3],), [15])],
  ("Loop over inputs, apply the rule to each.", "O(n)", "O(n)"),
  ("Vectorised: apply the formula to the whole array.", "O(n)", "O(n)"))


@B
def table(xs):
    ys = []
    for x in xs:
        ys.append(2 * x ** 2 - 3)
    return ys


@O
def table(xs):
    x = np.array(xs)
    return 2 * x ** 2 - 3


Q(None, "Slope Between Two Points", "Easy", "Rise over run",
  "Return the slope of the line through (x1, y1) and (x2, y2), rounded to 4 decimals (x1 ≠ x2).",
  [((1, 2, 3, 6), 2.0), ((0, 5, 4, 3), -0.5), ((-1, 1, 1, 1), 0.0)],
  ("Rise = change in y, run = change in x, slope = rise / run.", "O(1)", "O(1)"),
  ("<code>np.diff</code> of the y's over <code>np.diff</code> of the x's.", "O(1)", "O(1)"))


@B
def slope(x1, y1, x2, y2):
    rise = y2 - y1
    run = x2 - x1
    return round(rise / run, 4)


@O
def slope(x1, y1, x2, y2):
    return round(float(np.diff([y1, y2])[0] / np.diff([x1, x2])[0]), 4)


Q(None, "Equation of a Line Through Two Points", "Easy", "y = mx + c",
  "Return (m, c) of the line through two points, rounded to 4 decimals.",
  [((1, 3, 3, 7), (2.0, 1.0)), ((0, 4, 2, 0), (-2.0, 4.0)), ((2, 5, 6, 5), (0.0, 5.0))],
  ("Slope first, then substitute one point into y = mx + c and solve for c.", "O(1)", "O(1)"),
  ("<code>np.polyfit([x1, x2], [y1, y2], 1)</code> — a degree-1 fit through two points is exact.", "O(1)", "O(1)"))


@B
def line_through(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return (round(m, 4), round(c, 4))


@O
def line_through(x1, y1, x2, y2):
    m, c = np.polyfit([x1, x2], [y1, y2], 1)
    return (round(m, 4), round(c, 4))


Q(None, "Where Two Lines Meet", "Medium", "Intersection",
  "Lines y = m1·x + c1 and y = m2·x + c2 (m1 ≠ m2). Return the crossing point (x, y) rounded to 4 decimals.",
  [((2, 1, -1, 7), (2.0, 5.0)), ((1, 0, -1, 0), (0.0, 0.0)), ((0.5, 2, 3, -3), (2.0, 3.0))],
  ("Set the right-hand sides equal and solve the linear equation for x; substitute for y.", "O(1)", "O(1)"),
  ("Rewrite as a 2×2 system [−m, 1]·[x, y] = c and use <code>np.linalg.solve</code>.", "O(1)", "O(1)"))


@B
def intersect(m1, c1, m2, c2):
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return (round(x, 4), round(y, 4))


@O
def intersect(m1, c1, m2, c2):
    A = np.array([[-m1, 1], [-m2, 1]])
    x, y = np.linalg.solve(A, [c1, c2])
    return (round(x, 4), round(y, 4))


Q(None, "Is It a Function?", "Easy", "One output per input",
  "Given (x, y) pairs, return True if no x appears with two different y values.",
  [(([(1, 2), (2, 3), (3, 2)],), True), (([(1, 2), (1, 5)],), False), (([(4, 4), (4, 4)],), True)],
  ("Remember each x's y in a dictionary; a clash means not a function.", "O(n)", "O(n)"),
  ("Count distinct x's vs distinct (x, y) pairs — equal means a function.", "O(n)", "O(n)"))


@B
def is_function(pairs):
    seen = {}
    for x, y in pairs:
        if x in seen and seen[x] != y:
            return False
        seen[x] = y
    return True


@O
def is_function(pairs):
    unique_pairs = set(pairs)
    return len({x for x, _ in unique_pairs}) == len(unique_pairs)


Q(None, "Allowed Inputs (Domain)", "Medium", "√ and ÷ restrictions",
  "For f(x) = √(x − 2) / (x − 5), return the inputs from xs where f is defined.",
  [(([0, 2, 3, 5, 6, 10],), [2, 3, 6, 10]), (([1, 5],), [])],
  ("Check each rule separately: inside the root must be ≥ 0, the bottom must not be 0.", "O(n)", "O(n)"),
  ("One boolean mask combining both conditions.", "O(n)", "O(n)"))


@B
def domain(xs):
    ok = []
    for x in xs:
        if x - 2 < 0:
            continue
        if x - 5 == 0:
            continue
        ok.append(x)
    return ok


@O
def domain(xs):
    x = np.array(xs)
    return x[(x - 2 >= 0) & (x != 5)]


Q(None, "Vertex of a Parabola", "Easy", "x = −b / 2a",
  "Return the vertex (lowest or highest point) of y = ax² + bx + c, rounded to 4 decimals.",
  [((1, -4, 3), (2.0, -1.0)), ((-2, 4, 1), (1.0, 3.0)), ((1, 0, 0), (0.0, 0.0))],
  ("Scan a fine grid of x values and keep the best y (min if a &gt; 0, max if a &lt; 0).", "O(grid)", "O(1)"),
  ("Exact: x = −b/2a, then y = f(x).", "O(1)", "O(1)"))


@B
def vertex(a, b, c):
    best_x, best_y = None, None
    for i in range(-1000, 1001):
        x = i / 100
        y = a * x * x + b * x + c
        better = best_y is None or (y < best_y if a > 0 else y > best_y)
        if better:
            best_x, best_y = x, y
    return (round(best_x, 4), round(best_y, 4))


@O
def vertex(a, b, c):
    x = -b / (2 * a)
    return (round(x, 4), round(a * x * x + b * x + c, 4))


Q(None, "Compose Two Functions", "Medium", "f(g(x))",
  "f(x) = a·x + b and g(x) = c·x + d. Return (slope, intercept) of f(g(x)).",
  [((2, 1, 3, 4), (6, 9)), ((1, 0, 5, -2), (5, -2)), ((-1, 3, 2, 2), (-2, 1))],
  ("Plug g's output into f: a(cx + d) + b, then expand.", "O(1)", "O(1)"),
  ("Polynomial composition with <code>np.poly1d</code>: <code>f(g)</code>.", "O(1)", "O(1)"))


@B
def compose(a, b, c, d):
    slope = a * c
    intercept = a * d + b
    return (slope, intercept)


@O
def compose(a, b, c, d):
    f = np.poly1d([a, b])
    g = np.poly1d([c, d])
    h = f(g)
    return (int(h.coeffs[0]), int(h.coeffs[1]))


Q(None, "Inverse of a Line", "Easy", "Undo the function",
  "For f(x) = a·x + b (a ≠ 0), return (slope, intercept) of f⁻¹, rounded to 4 decimals.",
  [((2, 3), (0.5, -1.5)), ((-1, 4), (-1.0, 4.0)), ((4, 0), (0.25, 0.0))],
  ("Write y = ax + b, swap x and y, solve for y.", "O(1)", "O(1)"),
  ("Formula: f⁻¹(x) = (x − b)/a = (1/a)x − b/a.", "O(1)", "O(1)"))


@B
def inverse(a, b):
    # x = a*y + b  ->  y = (x - b) / a
    new_slope = 1 / a
    new_intercept = -b / a
    return (round(new_slope, 4), round(new_intercept, 4))


@O
def inverse(a, b):
    return (round(1 / a, 4), round(-b / a, 4))


Q(None, "Exponential Growth Table", "Easy", "a · bˣ",
  "Return a·bˣ for x = 0 … n, rounded to 2 decimals.",
  [((100, 2, 4), [100.0, 200.0, 400.0, 800.0, 1600.0]), ((80, 0.5, 3), [80.0, 40.0, 20.0, 10.0])],
  ("Each value is the previous one times b.", "O(n)", "O(n)"),
  ("Vectorised: <code>a * b ** np.arange(n + 1)</code>.", "O(n)", "O(n)"))


@B
def exp_table(a, b, n):
    out = []
    value = a
    for _ in range(n + 1):
        out.append(round(value, 2))
        value *= b
    return out


@O
def exp_table(a, b, n):
    return (a * float(b) ** np.arange(n + 1)).round(2)


Q(None, "Logarithm by Counting", "Easy", "How many times do I multiply?",
  "Return log base b of n when n is an exact power of b (log₂ 32 = 5).",
  [((2, 32), 5), ((10, 1000), 3), ((3, 1), 0)],
  ("Divide n by b repeatedly, counting, until you reach 1.", "O(answer)", "O(1)"),
  ("<code>math.log(n, b)</code>, rounded to the nearest whole number.", "O(1)", "O(1)"))


@B
def log_count(b, n):
    count = 0
    while n > 1:
        n //= b
        count += 1
    return count


@O
def log_count(b, n):
    return round(math.log(n, b))


Q(None, "Solve an Exponential Equation", "Medium", "bˣ = n  ⇒  x = log n / log b",
  "Return x with bˣ = n (b &gt; 1, n &gt; 0), rounded to 4 decimals.",
  [((2, 10), 3.3219), ((10, 0.01), -2.0), ((3, 81), 4.0)],
  ("Bisection on x: bˣ grows with x, so keep halving the interval that brackets n.", "O(log(1/ε))", "O(1)"),
  ("Take logs of both sides: x·log b = log n.", "O(1)", "O(1)"))


@B
def solve_exp(b, n):
    lo, hi = -100.0, 100.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if b ** mid < n:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 4)


@O
def solve_exp(b, n):
    return round(math.log(n) / math.log(b), 4)


Q(None, "Multiply Tiny Probabilities With Logs", "Medium", "log(ab) = log a + log b",
  "Return log₁₀ of the product of all numbers in ps, rounded to 4 decimals.",
  [(([0.1, 0.01, 0.5],), -3.301), (([10, 10, 10],), 3.0), (([0.2] * 5,), -3.4949)],
  ("Multiply everything, then take one log (overflows or underflows to 0 for long lists).", "O(n)", "O(1)"),
  ("Add the logs instead — the trick behind log-likelihood in ML.", "O(n)", "O(n)"))


@B
def log_product(ps):
    product = 1.0
    for p in ps:
        product *= p
    return round(math.log10(product), 4)


@O
def log_product(ps):
    return round(np.log10(ps).sum(), 4)


Q(None, "Sigmoid Function", "Easy", "Squash to (0, 1)",
  "Return σ(x) = 1 / (1 + e⁻ˣ) for each x, rounded to 4 decimals.",
  [(([0, 2, -2, 10],), [0.5, 0.8808, 0.1192, 1.0]), (([-5],), [0.0067])],
  ("Loop with <code>math.exp</code>.", "O(n)", "O(n)"),
  ("Vectorised with <code>np.exp</code>.", "O(n)", "O(n)"))


@B
def sigmoid(xs):
    out = []
    for x in xs:
        out.append(round(1 / (1 + math.exp(-x)), 4))
    return out


@O
def sigmoid(xs):
    x = np.array(xs, dtype=float)
    return (1 / (1 + np.exp(-x))).round(4)


Q(None, "ReLU Activation", "Easy", "max(0, x)",
  "Return ReLU(x) = max(0, x) for every x.",
  [(([-2, -0.5, 0, 1.5, 3],), [0, 0, 0, 1.5, 3]), (([-1, -1],), [0, 0])],
  ("If x is negative output 0, otherwise x.", "O(n)", "O(n)"),
  ("<code>np.maximum(0, x)</code>.", "O(n)", "O(n)"))


@B
def relu(xs):
    out = []
    for x in xs:
        if x < 0:
            out.append(0)
        else:
            out.append(x)
    return out


@O
def relu(xs):
    return np.maximum(0, np.array(xs))


Q(None, "Shift and Stretch a Graph", "Medium", "a·f(x − h) + k",
  "For f(x) = x², return the outputs of g(x) = a·f(x − h) + k at every x.",
  [(([0, 1, 2, 3], 2, 1, -1), [1, -1, 1, 7]), (([0, 1], 1, 0, 0), [0, 1])],
  ("Apply the transformations in order for each x: shift right by h, square, stretch by a, lift by k.", "O(n)", "O(n)"),
  ("Vectorised in one expression.", "O(n)", "O(n)"),
  names=["xs", "a", "h", "k"])


@B
def transform(xs, a, h, k):
    out = []
    for x in xs:
        shifted = x - h
        value = shifted ** 2
        value = a * value
        value = value + k
        out.append(value)
    return out


@O
def transform(xs, a, h, k):
    x = np.array(xs)
    return a * (x - h) ** 2 + k


Q(None, "Even, Odd or Neither?", "Medium", "Symmetry",
  "f is given as polynomial coefficients (highest first). Return 'even' if f(−x) = f(x), 'odd' if f(−x) = −f(x), else 'neither' (zero polynomial counts as even).",
  [(([1, 0, 0],), "even"), (([1, 0, 0, 0],), "odd"), (([1, 1],), "neither"), (([3, 0, -2, 0],), "odd")],
  ("Test the definition on many sample points.", "O(n·points)", "O(1)"),
  ("Look at the powers: only even powers present → even; only odd → odd.", "O(n)", "O(n)"))


@B
def parity(coeffs):
    f = lambda x: sum(c * x ** (len(coeffs) - 1 - i) for i, c in enumerate(coeffs))
    samples = [0.5, 1, 2, 3]
    if all(f(-x) == f(x) for x in samples):
        return "even"
    if all(f(-x) == -f(x) for x in samples):
        return "odd"
    return "neither"


@O
def parity(coeffs):
    c = np.array(coeffs)
    powers = np.arange(len(c) - 1, -1, -1)[c != 0]
    if np.all(powers % 2 == 0):
        return "even"
    if np.all(powers % 2 == 1):
        return "odd"
    return "neither"


Q(None, "Highest Point on a Grid", "Easy", "Maximum of a function",
  "Evaluate f(x) = −x² + 4x + 1 on xs and return the x with the largest output.",
  [(([0, 1, 2, 3, 4],), 2), (([-1, 5, 2.5],), 2.5)],
  ("Track the best (x, y) in a loop.", "O(n)", "O(1)"),
  ("<code>xs[np.argmax(f(xs))]</code>.", "O(n)", "O(n)"))


@B
def argmax(xs):
    best_x, best_y = None, None
    for x in xs:
        y = -x * x + 4 * x + 1
        if best_y is None or y > best_y:
            best_x, best_y = x, y
    return best_x


@O
def argmax(xs):
    x = np.array(xs)
    return x[np.argmax(-x ** 2 + 4 * x + 1)]


Q(None, "Average Rate of Change", "Easy", "Secant slope",
  "Return (f(b) − f(a)) / (b − a) for f(x) = x³, rounded to 4 decimals.",
  [((1, 3), 13.0), ((0, 1), 1.0), ((2, 2.001), 12.006)],
  ("Evaluate f at both ends and divide.", "O(1)", "O(1)"),
  ("Same with <code>np.diff</code> on arrays.", "O(1)", "O(1)"))


@B
def avg_rate(a, b):
    fa = a ** 3
    fb = b ** 3
    return round((fb - fa) / (b - a), 4)


@O
def avg_rate(a, b):
    x = np.array([a, b], dtype=float)
    return round(float(np.diff(x ** 3)[0] / np.diff(x)[0]), 4)


Q(None, "Piecewise Function: Tax Brackets", "Medium", "Different rules on different intervals",
  "Tax is 0% up to 10 000, 10% on the part between 10 000 and 40 000, and 30% above 40 000. Return the tax for each income.",
  [(([5000, 20000, 50000],), [0.0, 1000.0, 6000.0]), (([40000],), [3000.0])],
  ("if / elif on each income.", "O(n)", "O(n)"),
  ("<code>np.clip</code> each bracket's slice of income and add — no branches.", "O(n)", "O(n)"))


@B
def tax(incomes):
    out = []
    for x in incomes:
        if x <= 10000:
            t = 0.0
        elif x <= 40000:
            t = 0.1 * (x - 10000)
        else:
            t = 0.1 * 30000 + 0.3 * (x - 40000)
        out.append(round(t, 2))
    return out


@O
def tax(incomes):
    x = np.array(incomes, dtype=float)
    band2 = np.clip(x - 10000, 0, 30000)
    band3 = np.clip(x - 40000, 0, None)
    return (0.1 * band2 + 0.3 * band3).round(2)
