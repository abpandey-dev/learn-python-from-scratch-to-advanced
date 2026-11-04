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
