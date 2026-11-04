from lib import *
import math
import numpy as np

TOPIC(
    id="algebra", title="Algebra & Equations", glyph="x = ?",
    blurb="Letters that stand for numbers: expressions, solving equations, quadratics, polynomials, systems of equations, inequalities and sequences.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">ax + b = c          →  x = (c − b) / a
ax² + bx + c = 0    →  x = (−b ± √(b² − 4ac)) / 2a
np.roots([a, b, c])                 # roots of a polynomial
np.polyval([3, 2, -5], x)           # 3x² + 2x − 5 at x
np.polymul([1, 2], [1, 3])          # (x + 2)(x + 3) = x² + 5x + 6
np.linalg.solve([[2, 1], [1, -1]], [5, 1])   # 2x + y = 5, x − y = 1
P * (1 + r) ** n                    # compound growth</code></pre>
<p>Polynomials in NumPy are lists of coefficients from the <b>highest</b> power down: <code>[3, 2, -5]</code> = 3x² + 2x − 5.</p>
""")


Q(None, "Evaluate a Polynomial", "Easy", "Substitution",
  "Given coefficients (highest power first) and x, return the value. [3, 2, -5] at x = 2 → 3·4 + 2·2 − 5 = 11.",
  [(([3, 2, -5], 2), 11), (([1, 0, 0, 1], -1), 0), (([5], 9), 5)],
  ("Substitute: for each term compute coefficient × x^power and add.", "O(n²) multiplications", "O(1)"),
  ("Horner's rule <code>np.polyval</code>: ((3)x + 2)x − 5 — only n multiplications.", "O(n)", "O(1)"),
  viz=([3, 2, -5], 2))


@B
def evaluate(coeffs, x):
    n = len(coeffs) - 1
    total = 0
    for i, c in enumerate(coeffs):
        power = n - i
        term = c * x ** power
        total += term
    return total


@O
def evaluate(coeffs, x):
    return np.polyval(coeffs, x)


Q(None, "Solve a Linear Equation", "Easy", "ax + b = c",
  "Return x that solves a·x + b = c (a ≠ 0), rounded to 4 decimals.",
  [((2, 3, 11), 4.0), ((5, -2, 0), 0.4), ((-3, 6, 0), 2.0)],
  ("Do the same thing to both sides: subtract b, then divide by a — one step at a time.", "O(1)", "O(1)"),
  ("Formula x = (c − b) / a.", "O(1)", "O(1)"))


@B
def solve_linear(a, b, c):
    right = c
    right = right - b
    x = right / a
    return round(x, 4)


@O
def solve_linear(a, b, c):
    return round((c - b) / a, 4)


Q(None, "Variables on Both Sides", "Easy", "ax + b = cx + d",
  "Solve a·x + b = c·x + d (a ≠ c), rounded to 4 decimals.",
  [((3, 4, 1, 10), 3.0), ((5, -1, 2, 8), 3.0), ((1, 0, -1, 3), 1.5)],
  ("Collect x terms on the left (subtract cx), numbers on the right (subtract b), then divide.", "O(1)", "O(1)"),
  ("Formula x = (d − b) / (a − c).", "O(1)", "O(1)"))


@B
def both_sides(a, b, c, d):
    x_coeff = a - c
    number = d - b
    return round(number / x_coeff, 4)


@O
def both_sides(a, b, c, d):
    return round((d - b) / (a - c), 4)


Q(None, "Rearrange a Formula", "Easy", "Make y the subject",
  "Given a·x + b·y = c and a value of x, return y (b ≠ 0), rounded to 4 decimals.",
  [((2, 3, 12, 3), 2.0), ((1, -1, 4, 10), 6.0), ((4, 2, 0, 1), -2.0)],
  ("Move ax across (subtract it), then divide by b.", "O(1)", "O(1)"),
  ("y = (c − a·x) / b — vectorise it to get many points of the line at once.", "O(1)", "O(1)"))


@B
def make_y_subject(a, b, c, x):
    remaining = c - a * x
    y = remaining / b
    return round(y, 4)


@O
def make_y_subject(a, b, c, x):
    return round(float((c - a * np.asarray(x)) / b), 4)


Q(None, "How Many Real Solutions?", "Easy", "The discriminant",
  "For ax² + bx + c = 0, return how many real solutions there are (0, 1 or 2).",
  [((1, -3, 2), 2), ((1, 2, 1), 1), ((1, 0, 4), 0)],
  ("Compute b² − 4ac and test the sign with if/elif.", "O(1)", "O(1)"),
  ("<code>np.sign</code> maps negative/zero/positive to −1/0/1; add 1.", "O(1)", "O(1)"))


@B
def num_solutions(a, b, c):
    disc = b * b - 4 * a * c
    if disc > 0:
        return 2
    elif disc == 0:
        return 1
    else:
        return 0


@O
def num_solutions(a, b, c):
    return int(np.sign(b * b - 4 * a * c)) + 1


Q(None, "Quadratic Formula", "Medium", "x = (−b ± √D) / 2a",
  "Return the real solutions of ax² + bx + c = 0 sorted ascending (empty list if none), rounded to 4 decimals.",
  [((1, -3, 2), [1.0, 2.0]), ((1, 2, 1), [-1.0]), ((1, 0, 4), []), ((2, 1, -1), [-1.0, 0.5])],
  ("Discriminant first, then the ± formula.", "O(1)", "O(1)"),
  ("<code>np.roots([a, b, c])</code>, keeping only the real roots.", "O(1)", "O(1)"))


@B
def quadratic(a, b, c):
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    if disc == 0:
        return [round(-b / (2 * a), 4)]
    root = math.sqrt(disc)
    x1 = (-b - root) / (2 * a)
    x2 = (-b + root) / (2 * a)
    return sorted([round(x1, 4), round(x2, 4)])


@O
def quadratic(a, b, c):
    r = np.roots([a, b, c])
    real = np.unique(r[np.isclose(r.imag, 0)].real.round(4))
    return real


Q(None, "Expand Two Brackets", "Easy", "(x + a)(x + b)",
  "Return the coefficients of (x + a)(x + b) as [1, a + b, a·b].",
  [((2, 3), [1, 5, 6]), ((-1, 1), [1, 0, -1]), ((-4, -4), [1, -8, 16])],
  ("FOIL: First x·x, Outer x·b, Inner a·x, Last a·b — then collect like terms.", "O(1)", "O(1)"),
  ("<code>np.polymul([1, a], [1, b])</code>.", "O(1)", "O(1)"))


@B
def expand(a, b):
    first = 1
    outer = b
    inner = a
    last = a * b
    return [first, outer + inner, last]


@O
def expand(a, b):
    return np.polymul([1, a], [1, b])


Q(None, "Multiply Two Polynomials", "Medium", "Distribute every term",
  "Multiply two polynomials given as coefficient lists (highest power first).",
  [(([1, 2], [1, 3]), [1, 5, 6]), (([2, 0, 1], [1, -1]), [2, -2, 1, -1]), (([3], [1, 4]), [3, 12])],
  ("Every term of p times every term of q; the product of positions i and j lands at i + j.", "O(n·m)", "O(n + m)"),
  ("<code>np.polymul(p, q)</code>.", "O(n·m)", "O(n + m)"))


@B
def poly_multiply(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


@O
def poly_multiply(p, q):
    return np.polymul(p, q)


Q(None, "Add Two Polynomials", "Easy", "Like terms",
  "Add two polynomials (highest power first). Lists may have different lengths.",
  [(([1, 2, 3], [4, 5]), [1, 6, 8]), (([2, 0], [-2, 1]), [0, 1]), (([5], [1, 1, 1]), [1, 1, 6])],
  ("Pad the shorter list with zeros on the left so the powers line up, then add position by position.", "O(n)", "O(n)"),
  ("<code>np.polyadd(p, q)</code>.", "O(n)", "O(n)"))


@B
def poly_add(p, q):
    n = max(len(p), len(q))
    p = [0] * (n - len(p)) + list(p)
    q = [0] * (n - len(q)) + list(q)
    return [a + b for a, b in zip(p, q)]


@O
def poly_add(p, q):
    return np.polyadd(p, q)


Q(None, "Collect Like Terms", "Easy", "Simplifying",
  "Terms are (coefficient, power) pairs. Combine like powers and return {power: coefficient}, dropping zeros, highest power first.",
  [(([(3, 2), (2, 1), (-1, 2), (5, 0), (-2, 1)],), {2: 2, 0: 5}), (([(1, 1), (1, 1)],), {1: 2})],
  ("Add each coefficient into a dictionary keyed by its power.", "O(n log n)", "O(n)"),
  ("Scatter-add with NumPy: <code>np.add.at(coeffs, powers, values)</code>.", "O(n + max power)", "O(max power)"))


@B
def like_terms(terms):
    combined = {}
    for coef, pw in terms:
        combined[pw] = combined.get(pw, 0) + coef
    return {p: c for p, c in sorted(combined.items(), reverse=True) if c != 0}


@O
def like_terms(terms):
    t = np.array(terms)
    coeffs = np.zeros(t[:, 1].max() + 1, dtype=int)
    np.add.at(coeffs, t[:, 1], t[:, 0])
    return {int(p): int(coeffs[p]) for p in range(len(coeffs) - 1, -1, -1) if coeffs[p] != 0}


Q(None, "Solve Two Equations Together", "Medium", "Simultaneous equations",
  "Solve a1·x + b1·y = c1 and a2·x + b2·y = c2. Return (x, y) rounded to 4 decimals.",
  [((2, 1, 5, 1, -1, 1), (2.0, 1.0)), ((1, 1, 10, 1, -1, 2), (6.0, 4.0)), ((3, 2, 12, 1, 4, 14), (2.0, 3.0))],
  ("Elimination: multiply the equations so the y terms match, subtract to remove y, solve for x, substitute back.", "O(1)", "O(1)"),
  ("Write it as a matrix equation A·[x, y] = c and call <code>np.linalg.solve</code>.", "O(1)", "O(1)"))


@B
def solve_system(a1, b1, c1, a2, b2, c2):
    # multiply eq1 by b2 and eq2 by b1, then subtract: the y terms cancel
    x_coeff = a1 * b2 - a2 * b1
    right = c1 * b2 - c2 * b1
    x = right / x_coeff
    y = (c1 - a1 * x) / b1 if b1 != 0 else (c2 - a2 * x) / b2
    return (round(x, 4), round(y, 4))


@O
def solve_system(a1, b1, c1, a2, b2, c2):
    A = np.array([[a1, b1], [a2, b2]])
    c = np.array([c1, c2])
    x, y = np.linalg.solve(A, c)
    return (round(x, 4), round(y, 4))


Q(None, "Which Values Satisfy an Inequality?", "Easy", "ax + b > c",
  "Return the values from xs that make a·x + b > c true.",
  [(([0, 1, 2, 3, 4, 5], 2, 1, 6), [3, 4, 5]), (([-2, -1, 0, 1], -1, 0, 0), [-2, -1])],
  ("Test each value in a loop.", "O(n)", "O(n)"),
  ("Boolean mask: <code>xs[a * xs + b &gt; c]</code>. (Solving by hand: x &gt; (c − b)/a, and flip the sign if a &lt; 0.)", "O(n)", "O(n)"))


@B
def satisfies(xs, a, b, c):
    out = []
    for x in xs:
        if a * x + b > c:
            out.append(x)
    return out


@O
def satisfies(xs, a, b, c):
    xs = np.array(xs)
    return xs[a * xs + b > c]


Q(None, "Absolute Value Equation", "Easy", "|x − a| = b",
  "Return the solutions of |x − a| = b sorted ascending (b may be negative: then none).",
  [((3, 2), [1, 5]), ((0, 0), [0]), ((4, -1), [])],
  ("Split into two cases: x − a = b or x − a = −b.", "O(1)", "O(1)"),
  ("Same idea in one line with a set to merge the two cases when b = 0.", "O(1)", "O(1)"))


@B
def abs_equation(a, b):
    if b < 0:
        return []
    case1 = a + b
    case2 = a - b
    if case1 == case2:
        return [case1]
    return [case2, case1]


@O
def abs_equation(a, b):
    return sorted({a - b, a + b}) if b >= 0 else []


Q(None, "Solve a Proportion", "Easy", "Cross-multiplying",
  "Solve a / b = x / d for x, rounded to 4 decimals. (If 3 pens cost 45, 5 pens cost x.)",
  [((3, 45, 5), 75.0), ((2, 5, 7), 17.5)],
  ("Unitary method: find the value of one (b / a), then multiply by d.", "O(1)", "O(1)"),
  ("Cross-multiply: x = b·d / a.", "O(1)", "O(1)"),
  names=["a", "b", "d"])


@B
def proportion(a, b, d):
    one = b / a
    return round(one * d, 4)


@O
def proportion(a, b, d):
    return round(b * d / a, 4)


Q(None, "Compound Growth", "Easy", "P(1 + r)ⁿ",
  "Return the value of principal P after n years at rate r per year, compounded yearly, rounded to 2 decimals.",
  [((1000, 0.1, 2), 1210.0), ((500, 0.05, 10), 814.45), ((100, 0, 5), 100.0)],
  ("Year by year: value = value × (1 + r).", "O(n)", "O(1)"),
  ("Formula P·(1 + r)ⁿ.", "O(1)", "O(1)"))


@B
def compound(P, r, n):
    value = P
    for year in range(n):
        value = value * (1 + r)
    return round(value, 2)


@O
def compound(P, r, n):
    return round(P * (1 + r) ** n, 2)


Q(None, "Years to Double", "Medium", "Solving with a logarithm",
  "Return the smallest whole number of years for P to at least double at yearly rate r.",
  [((0.1,), 8), ((0.07,), 11), ((1.0,), 1)],
  ("Simulate year by year until the value reaches 2.", "O(answer)", "O(1)"),
  ("Solve (1 + r)ⁿ = 2: n = log 2 / log(1 + r), then round up.", "O(1)", "O(1)"))


@B
def years_to_double(r):
    value = 1.0
    years = 0
    while value < 2:
        value *= 1 + r
        years += 1
    return years


@O
def years_to_double(r):
    return math.ceil(math.log(2) / math.log(1 + r) - 1e-12)


Q(None, "Find a Root by Halving", "Medium", "Bisection",
  "f(x) = x³ − x − 2 changes sign between lo and hi. Return its root there, rounded to 4 decimals.",
  [((1, 2), 1.5214), ((0, 3), 1.5214)],
  ("Bisection: look at the midpoint, keep the half where the sign changes, repeat.", "O(log(1/ε))", "O(1)"),
  ("<code>np.roots([1, 0, -1, -2])</code> and keep the real root in [lo, hi].", "O(1)", "O(1)"))


@B
def bisect_root(lo, hi):
    f = lambda x: x ** 3 - x - 2
    for _ in range(50):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return round((lo + hi) / 2, 4)


@O
def bisect_root(lo, hi):
    r = np.roots([1, 0, -1, -2])
    real = r[np.isclose(r.imag, 0)].real
    return round(real[(real >= lo) & (real <= hi)][0], 4)


Q(None, "Arithmetic Sequence", "Easy", "aₙ = a₁ + (n − 1)d",
  "Return the n-th term of the sequence that starts at a and goes up by d each step.",
  [((3, 4, 10), 39), ((10, -2, 6), 0), ((5, 0, 100), 5)],
  ("Start at a and add d, n − 1 times.", "O(n)", "O(1)"),
  ("Formula a + (n − 1)·d.", "O(1)", "O(1)"))


@B
def nth_term(a, d, n):
    term = a
    for _ in range(n - 1):
        term += d
    return term


@O
def nth_term(a, d, n):
    return a + (n - 1) * d


Q(None, "Sum of a Geometric Series", "Medium", "a(1 − rⁿ)/(1 − r)",
  "Return a + ar + ar² + … (n terms), rounded to 4 decimals.",
  [((1, 2, 5), 31.0), ((1, 0.5, 4), 1.875), ((3, 1, 4), 12.0)],
  ("Generate each term by multiplying by r and add them up.", "O(n)", "O(1)"),
  ("Formula a(1 − rⁿ)/(1 − r) (or n·a when r = 1).", "O(1)", "O(1)"))


@B
def geometric_sum(a, r, n):
    total = 0
    term = a
    for _ in range(n):
        total += term
        term *= r
    return round(total, 4)


@O
def geometric_sum(a, r, n):
    if r == 1:
        return round(a * n, 4)
    return round(a * (1 - r ** n) / (1 - r), 4)


Q(None, "Factor Out the Common Factor", "Easy", "Factorising",
  "Given polynomial coefficients, return (g, rest) where g is the GCD of all coefficients and rest = coefficients / g. 6x² + 9x − 3 → (3, [2, 3, -1]).",
  [(([6, 9, -3],), (3, [2, 3, -1])), (([4, 8],), (4, [1, 2])), (([5, 7],), (1, [5, 7]))],
  ("Euclid's GCD pairwise across the coefficients, then divide each.", "O(n log m)", "O(n)"),
  ("<code>np.gcd.reduce</code> on the array, then integer-divide.", "O(n log m)", "O(n)"))


@B
def factor_out(coeffs):
    g = 0
    for c in coeffs:
        a, b = g, abs(c)
        while b:
            a, b = b, a % b
        g = a
    return (g, [c // g for c in coeffs])


@O
def factor_out(coeffs):
    c = np.array(coeffs)
    g = np.gcd.reduce(c)
    return (g, c // g)
