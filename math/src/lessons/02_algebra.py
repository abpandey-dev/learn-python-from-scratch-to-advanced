from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Variables and expressions", """
<p>Algebra is arithmetic with <b>unknowns</b>. A letter like x is a box that holds a number we don't know yet — exactly like a variable in Python.</p>
<ul>
<li>An <b>expression</b> is a recipe: 3x + 2 means "multiply x by 3, then add 2". It has no equals sign.</li>
<li>To <b>evaluate</b> it, substitute a number: if x = 4, 3x + 2 = 14.</li>
<li><b>Like terms</b> have the same letter and power and can be combined: 3x + 5x = 8x, but 3x + 5x² cannot.</li>
<li>3x means 3 × x; x² means x × x; 2(x + 1) = 2x + 2 (the distributive rule).</li>
</ul>
<p>In ML, a model like <i>price = 3000 × size + 20000</i> is an expression: size is the input, 3000 and 20000 are numbers the model learns.</p>
""", practice=["Evaluate a Polynomial", "Collect Like Terms", "Factor Out the Common Factor"])


@LD
def expressions_demo():
    x = 4
    expression = 3 * x + 2
    size = 80
    price = 3000 * size + 20000
    like_terms = 3 * x + 5 * x
    same_as = 8 * x


LESSON("Basics", "Solving equations: keep the scales balanced", """
<p>An <b>equation</b> says two things are equal: 2x + 3 = 11. Think of a balance scale — whatever you do to one side, do to the other, and it stays balanced.</p>
<pre><code class="py">2x + 3 = 11
2x     = 8      (subtract 3 from both sides)
 x     = 4      (divide both sides by 2)</code></pre>
<p><b>Check</b> by substituting back: 2·4 + 3 = 11 ✓. Undo operations in reverse order: the last thing done to x is undone first.</p>
<p>Variables on both sides: 3x + 4 = x + 10 → 2x = 6 → x = 3. Gather the x's on one side and the numbers on the other.</p>
""", practice=["Solve a Linear Equation", "Variables on Both Sides", "Rearrange a Formula", "Solve a Proportion", "Absolute Value Equation"])


@LD
def balance_demo():
    left_coeff, left_const, right = 2, 3, 11
    right = right - left_const
    left_const = 0
    x = right / left_coeff
    check = 2 * x + 3


LESSON("Core", "Quadratic equations", """
<p>A <b>quadratic</b> has an x²: ax² + bx + c = 0. Its graph is a U-shaped curve called a <b>parabola</b>, and the solutions are where the curve crosses the x-axis.</p>
<p>The <b>discriminant</b> D = b² − 4ac tells you how many crossings:</p>
<table><tr><th>D</th><th>Solutions</th></tr><tr><td>&gt; 0</td><td>two</td></tr><tr><td>= 0</td><td>one (touches)</td></tr><tr><td>&lt; 0</td><td>none (real)</td></tr></table>
<p>The <b>quadratic formula</b> gives them: x = (−b ± √D) / 2a.</p>
<p>Expanding (x + 2)(x + 3) = x² + 5x + 6 and factorising go in opposite directions; the factors show the roots straight away: x = −2 or x = −3.</p>
""", practice=["How Many Real Solutions?", "Quadratic Formula", "Expand Two Brackets", "Multiply Two Polynomials", "Add Two Polynomials"])


@LD
def parabolas():
    x = np.linspace(-4, 4, 100)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, x ** 2 - 3 * x + 2, label="x² − 3x + 2   (D > 0)")
    ax.plot(x, x ** 2 + 2 * x + 1, label="x² + 2x + 1   (D = 0)")
    ax.plot(x, x ** 2 + 4, label="x² + 4   (D < 0)")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(-2, 12)
    ax.legend(fontsize=7)


LESSON("Core", "Two equations, two unknowns", """
<p>One equation with two unknowns has infinitely many answers. Two equations usually pin down exactly one: the point where two lines cross.</p>
<pre><code class="py">2x + y = 5
 x − y = 1
------------  add them: y cancels
3x     = 6   →  x = 2,  then y = 1</code></pre>
<p>This is <b>elimination</b>. Later you will write the same system as a matrix equation A·v = c and let NumPy solve it — the same idea scales to thousands of unknowns, which is what fitting a linear regression does.</p>
""", practice=["Solve Two Equations Together", "Which Values Satisfy an Inequality?"])


@LD
def two_lines():
    x = np.linspace(-1, 4, 50)
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(x, 5 - 2 * x, label="2x + y = 5")
    ax.plot(x, x - 1, label="x − y = 1")
    ax.plot(2, 1, "ko")
    ax.annotate("(2, 1)", (2, 1), xytext=(8, -12), textcoords="offset points")
    ax.legend()


LESSON("Advanced", "Growth, sequences and solving with logs", """
<p>An <b>arithmetic sequence</b> adds the same amount each step (3, 7, 11, …): aₙ = a₁ + (n−1)d. A <b>geometric sequence</b> multiplies by the same amount (1, 2, 4, 8, …): aₙ = a₁·rⁿ⁻¹.</p>
<p>Money with interest grows geometrically: P(1 + r)ⁿ. To ask "how many years until it doubles?" you must get n out of the exponent — that is what a <b>logarithm</b> does: n = log 2 / log(1 + r). (Logs are explained properly in the next topic.)</p>
<p>When no formula exists, you can still solve f(x) = 0 by <b>bisection</b>: keep halving an interval where f changes sign. Numerical methods like this are how computers solve the equations in ML.</p>
""", practice=["Arithmetic Sequence", "Sum of a Geometric Series", "Compound Growth", "Years to Double", "Find a Root by Halving"])


@LD
def growth_demo():
    years = np.arange(0, 21)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(years, 1000 + 100 * years, "o-", markersize=3, label="arithmetic: +100 a year")
    ax.plot(years, 1000 * 1.1 ** years, "o-", markersize=3, label="geometric: ×1.1 a year")
    ax.axhline(2000, color="gray", linestyle="--")
    ax.set_xlabel("year")
    ax.legend()


LESSON("Basics", "Expanding and factorising", """
<h4>Expanding: multiply everything by everything</h4>
<p>(x + 3)(x + 2): each term in the first bracket multiplies each term in the second.</p>
<table><tr><td></td><th>x</th><th>+2</th></tr><tr><th>x</th><td>x²</td><td>2x</td></tr><tr><th>+3</th><td>3x</td><td>6</td></tr></table>
<p>Add them up: x² + 5x + 6.</p>
<h4>Factorising: go backwards</h4>
<p>For x² + 5x + 6, find two numbers that <b>multiply to 6 and add to 5</b>: 2 and 3. So it equals (x + 2)(x + 3).</p>
<p><b>Why bother?</b> If (x + 2)(x + 3) = 0, one bracket must be 0, so x = −2 or x = −3. That solved the equation.</p>
<h4>Patterns to know</h4>
<table><tr><td>(a + b)² = a² + 2ab + b²</td><td>(3 + 4)² = 9 + 24 + 16 = 49 ✓</td></tr>
<tr><td>(a − b)² = a² − 2ab + b²</td><td>this is squared error</td></tr>
<tr><td>a² − b² = (a + b)(a − b)</td><td>9 − 4 = 5 × 1 ✓</td></tr></table>
<p><b>The most common mistake:</b> (a + b)² = a² + b². It leaves out 2ab.</p>
""", practice=["Expand Two Brackets", "Multiply Two Polynomials", "Add Two Polynomials", "Collect Like Terms", "Factor Out the Common Factor"])


@LD
def expand_check():
    coefficients = np.polymul([1, 3], [1, 2])
    roots = np.sort(np.roots(coefficients))
    x = 7
    same = ((x + 3) * (x + 2), x ** 2 + 5 * x + 6)
    a, b = 3, 4
    correct = ((a + b) ** 2, a ** 2 + 2 * a * b + b ** 2)
    wrong = a ** 2 + b ** 2


LESSON("Core", "The quadratic formula, step by step", """
<p>Solve 2x² − 4x − 6 = 0.</p>
<ol><li><b>Read off:</b> a = 2, b = −4, c = −6.</li>
<li><b>Discriminant:</b> D = b² − 4ac = 16 + 48 = 64.</li>
<li><b>Formula:</b> x = (−b ± √D) / 2a = (4 ± 8) / 4.</li>
<li><b>Two answers:</b> x = 12/4 = <b>3</b> or x = −4/4 = <b>−1</b>.</li>
<li><b>Check:</b> 2(9) − 4(3) − 6 = 0 ✓ and 2(1) + 4 − 6 = 0 ✓.</li></ol>
<h4>Where the formula comes from</h4>
<p>Take x² + bx + c = 0 (a = 1). Half of b, squared, completes a square:</p>
<pre><code class="py">x² + bx        = −c
x² + bx + b²/4 = b²/4 − c
(x + b/2)²     = b²/4 − c
x = −b/2 ± √(b²/4 − c)</code></pre>
<p>That's the same formula with a = 1. So x = −b/2a is the middle of the parabola, and ±√D / 2a is how far each root sits from it. This is also why the vertex is at x = −b/2a.</p>
<p><b>Slip to avoid:</b> with b = −4, −b is +4, and b² is +16.</p>
""", practice=["Quadratic Formula", "How Many Real Solutions?"])


@LD
def quadratic_steps():
    a, b, c = 2, -4, -6
    discriminant = b ** 2 - 4 * a * c
    root = math.sqrt(discriminant)
    x1, x2 = (-b + root) / (2 * a), (-b - root) / (2 * a)
    checks = (a * x1 ** 2 + b * x1 + c, a * x2 ** 2 + b * x2 + c)
    middle = -b / (2 * a)
    xs = np.linspace(-3, 5, 100)
    fig, ax = plt.subplots(figsize=(4.5, 2.9))
    ax.plot(xs, a * xs ** 2 + b * xs + c)
    ax.axhline(0, color="black", linewidth=0.7)
    ax.plot([x1, x2], [0, 0], "o", color="#b45309")
    ax.axvline(middle, ls="--", color="gray")
    ax.set_title("Roots sit equally either side of the middle", fontsize=9)


LESSON("Core", "Rearranging formulas", """
<p>Treat every letter like a number. Undo what was done to your target, in reverse order.</p>
<table><tr><th>Start</th><th>Make the subject</th><th>Steps</th><th>Result</th></tr>
<tr><td>y = mx + c</td><td>x</td><td>subtract c, divide by m</td><td>x = (y − c) / m</td></tr>
<tr><td>F = 9C/5 + 32</td><td>C</td><td>subtract 32, multiply by 5/9</td><td>C = 5(F − 32) / 9</td></tr>
<tr><td>z = (x − μ) / σ</td><td>x</td><td>multiply by σ, add μ</td><td>x = μ + zσ</td></tr>
<tr><td>A = P(1 + r)ⁿ</td><td>r</td><td>divide by P, take n-th root, subtract 1</td><td>r = (A/P)^(1/n) − 1</td></tr></table>
<h4>Check with numbers</h4>
<p>F = 212 gives C = 5(180)/9 = 100. Water boils at 100°C ✓. Trying a value you know is the quickest way to catch mistakes.</p>
<h4>Equations with fractions</h4>
<p>x/3 + 2 = 5 → x/3 = 3 → <b>x = 9</b>. Multiply by the bottom to clear a fraction, after moving other terms away.</p>
""", practice=["Rearrange a Formula", "Solve a Linear Equation", "Variables on Both Sides", "Solve a Proportion"])


@LD
def rearrange_checks():
    f = 212
    c = 5 * (f - 32) / 9
    back_to_f = 9 * c / 5 + 32
    mu, sigma, z = 70, 10, 1.5
    x = mu + z * sigma
    back_to_z = (x - mu) / sigma
    growth_rate = (1210 / 1000) ** (1 / 2) - 1


LESSON("Core", "Inequalities", """
<p>Solve them like equations, with one extra rule: <b>multiplying or dividing by a negative flips the sign.</b></p>
<h4>Worked example</h4>
<pre><code class="py">−2x + 1 &gt; 5
−2x     &gt; 4        subtract 1
  x     &lt; −2       divide by −2, so flip</code></pre>
<p><b>Check</b> with x = −3: −2(−3) + 1 = 7, and 7 &gt; 5 ✓. With x = 0: 1 &gt; 5 is false ✓.</p>
<p><b>Why flip?</b> 2 &lt; 3, but multiplying by −1 gives −2 &gt; −3: the number line is mirrored.</p>
<h4>Absolute value</h4>
<ul><li>|x − 3| = 2 means x is 2 away from 3: x = 1 or x = 5.</li>
<li>|x − 3| &lt; 2 means <b>closer</b> than 2: 1 &lt; x &lt; 5.</li></ul>
<p>In data science, every filter such as <code>df[df.age &gt; 30]</code> or a tree's "x ≤ 3.5" is an inequality.</p>
""", practice=["Which Values Satisfy an Inequality?", "Absolute Value Equation"])


@LD
def inequality_checks():
    xs = np.arange(-5, 3)
    works = xs[-2 * xs + 1 > 5]
    formula_says = xs[xs < -2]
    within_two = np.arange(0, 7)[np.abs(np.arange(0, 7) - 3) < 2]


LESSON("Advanced", "Word problems, and when systems have no answer", """
<h4>From words to equations</h4>
<p>"5 fruits cost ₹13. Apples cost ₹3 and oranges ₹2. How many of each?"</p>
<ol><li><b>Name the unknowns:</b> a apples, o oranges.</li>
<li><b>Write what's known:</b> a + o = 5 and 3a + 2o = 13.</li>
<li><b>Eliminate:</b> multiply the first by 2: 2a + 2o = 10. Subtract: a = 3.</li>
<li><b>Substitute:</b> o = 2.</li>
<li><b>Check:</b> 3(3) + 2(2) = 13 ✓.</li></ol>
<h4>Three possible outcomes</h4>
<table><tr><th>Lines</th><th>Solutions</th><th>Example</th></tr>
<tr><td>Cross</td><td>one</td><td>y = x, y = −x + 2</td></tr>
<tr><td>Parallel</td><td>none</td><td>y = x, y = x + 2</td></tr>
<tr><td>Same line</td><td>infinitely many</td><td>y = x, 2y = 2x</td></tr></table>
<p><b>In ML:</b> real data has more equations than unknowns and no exact answer, so linear regression finds the closest one. With duplicate features, you get the "same line" case: many equally good answers, which regularisation resolves.</p>
""", practice=["Solve Two Equations Together"])


@LD
def three_cases():
    apples_oranges = np.linalg.solve([[1, 1], [3, 2]], [5, 13])
    x = np.linspace(-2, 4, 10)
    fig, axes = plt.subplots(1, 3, figsize=(8, 2.4), sharey=True)
    cases = [("one solution", x, -x + 2), ("no solution", x, x + 2), ("infinitely many", x, x)]
    for ax, (name, first, second) in zip(axes, cases):
        ax.plot(x, first, label="line 1")
        ax.plot(x, second, "--", label="line 2")
        ax.set_title(name, fontsize=9)
    fig.tight_layout()
