from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LESSON("Basics", "Kinds of numbers", """
<p>Every number you will meet belongs to a family. Each family is bigger than the one before:</p>
<table>
<tr><th>Family</th><th>Examples</th><th>Used for</th></tr>
<tr><td><b>Natural</b> ℕ</td><td>1, 2, 3, …</td><td>counting things</td></tr>
<tr><td><b>Integers</b> ℤ</td><td>…, −2, −1, 0, 1, 2, …</td><td>gains and losses, floors above / below ground</td></tr>
<tr><td><b>Rational</b> ℚ</td><td>½, −3/4, 0.25</td><td>parts of a whole — anything written as a fraction</td></tr>
<tr><td><b>Real</b> ℝ</td><td>√2, π, 0.333…</td><td>every point on the number line, including ones no fraction reaches</td></tr>
</table>
<p>Picture a <b>number line</b>: zero in the middle, positives to the right, negatives to the left. The distance of a number from zero is its <b>absolute value</b>: |−3| = 3. The distance between a and b is |a − b|.</p>
<p>In Python, whole numbers are <code>int</code> and numbers with a decimal point are <code>float</code>. ML models work almost entirely with real numbers stored as floats.</p>
""", practice=["Distance on the Number Line", "Whole Number to Binary"])


@LD
def number_line():
    points = [-3, -1.5, 0, 0.5, 2, math.pi]
    fig, ax = plt.subplots(figsize=(6, 1.6))
    ax.axhline(0, color="black", linewidth=1)
    for p in points:
        ax.plot(p, 0, "o")
        ax.annotate(f"{p:g}" if p != math.pi else "π", (p, 0), xytext=(0, 8), textcoords="offset points", ha="center")
    ax.set_yticks([])
    ax.set_xlim(-4, 4)
    ax.set_title("The number line")


LESSON("Basics", "The four operations and their order", """
<p>Addition, subtraction, multiplication and division are the building blocks. When an expression mixes them, follow <b>BODMAS</b> (also called PEMDAS):</p>
<ol>
<li><b>B</b>rackets first</li>
<li><b>O</b>rders — powers and roots</li>
<li><b>D</b>ivision and <b>M</b>ultiplication, left to right</li>
<li><b>A</b>ddition and <b>S</b>ubtraction, left to right</li>
</ol>
<p>Example: 2 + 3 × 4² = 2 + 3 × 16 = 2 + 48 = 50, not 400.</p>
<p>Division of whole numbers gives a <b>quotient</b> and a <b>remainder</b>: 17 ÷ 5 = 3 remainder 2, because 5 × 3 + 2 = 17. Python: <code>17 // 5</code> and <code>17 % 5</code>.</p>
""", practice=["Divide With Remainder", "Greatest Common Divisor", "Least Common Multiple", "Is It Prime?", "Prime Factorisation"])


@LD
def order_of_operations():
    step1 = 4 ** 2
    step2 = 3 * step1
    answer = 2 + step2
    python_says = 2 + 3 * 4 ** 2
    quotient = 17 // 5
    remainder = 17 % 5
    check = 5 * quotient + remainder


LESSON("Basics", "Fractions, decimals and percentages", """
<p>A <b>fraction</b> a/b means "split into b equal parts, take a of them". The same amount can be written three ways:</p>
<table><tr><th>Fraction</th><th>Decimal</th><th>Percent</th></tr>
<tr><td>1/2</td><td>0.5</td><td>50%</td></tr>
<tr><td>3/4</td><td>0.75</td><td>75%</td></tr>
<tr><td>1/3</td><td>0.333…</td><td>33.3%</td></tr></table>
<ul>
<li><b>Simplify</b>: divide top and bottom by their greatest common divisor — 12/18 = 2/3.</li>
<li><b>Add</b>: get a common bottom first — 1/2 + 1/3 = 3/6 + 2/6 = 5/6.</li>
<li><b>Percent</b> means "per hundred". Percent change = (new − old) / old × 100.</li>
<li><b>Ratio</b> 2 : 3 means "2 parts to 3 parts" — 5 parts in all.</li>
</ul>
<p>In ML, accuracy, probabilities and learning rates are all fractions written as decimals.</p>
""", practice=["Simplify a Fraction", "Add Two Fractions", "Fraction to Decimal and Percent", "Percent Change", "Share in a Ratio"])


@LD
def fractions_demo():
    parts = [1, 2, 3, 4]
    fig, axes = plt.subplots(1, 3, figsize=(7, 2.4))
    for ax, (num, den, label) in zip(axes, [(1, 2, "1/2 = 50%"), (3, 4, "3/4 = 75%"), (1, 3, "1/3 ≈ 33%")]):
        ax.pie([num, den - num], colors=["#0f766e", "#e5e7eb"], startangle=90, counterclock=False)
        ax.set_title(label)


LESSON("Core", "Powers and roots", """
<p>A <b>power</b> is repeated multiplication: 2⁴ = 2 × 2 × 2 × 2 = 16. The small number is the <b>exponent</b>.</p>
<table>
<tr><th>Rule</th><th>Example</th></tr>
<tr><td>xᵃ · xᵇ = xᵃ⁺ᵇ</td><td>2³ · 2² = 2⁵ = 32</td></tr>
<tr><td>(xᵃ)ᵇ = xᵃᵇ</td><td>(2³)² = 2⁶ = 64</td></tr>
<tr><td>x⁰ = 1</td><td>7⁰ = 1</td></tr>
<tr><td>x⁻ⁿ = 1 / xⁿ</td><td>2⁻³ = 1/8</td></tr>
<tr><td>x^(1/n) = ⁿ√x</td><td>8^(1/3) = 2</td></tr>
</table>
<p>A <b>square root</b> undoes squaring: √25 = 5 because 5² = 25. Very large and very small numbers are written in <b>scientific notation</b>: 45 000 = 4.5 × 10⁴, 0.00321 = 3.21 × 10⁻³ (Python prints <code>4.5e4</code>).</p>
""", practice=["Power by Repeated Multiplication", "Negative and Fractional Exponents", "Square Root by Guessing", "Scientific Notation", "Round to Significant Figures"])


@LD
def powers_graph():
    xs = [x / 10 for x in range(0, 31)]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(xs, [x ** 2 for x in xs], label="x²")
    ax.plot(xs, [x ** 0.5 for x in xs], label="√x")
    ax.plot(xs, [2 ** x for x in xs], label="2ˣ")
    ax.set_ylim(0, 9)
    ax.legend()
    ax.set_title("Squares grow fast, roots grow slowly")


LESSON("Advanced", "Sigma notation, factorials and the language of formulas", """
<p>ML papers are full of <b>Σ</b> (capital sigma). It just means "add up":</p>
<pre><code class="py">  n
  Σ  k²   =  1² + 2² + … + n²          total = 0
 k=1                                    for k in range(1, n + 1):
                                            total += k ** 2</code></pre>
<p>Read it as a loop: k starts at the bottom number, stops at the top, and you add the expression each time. <b>Π</b> (capital pi) is the same with multiplication. The <b>factorial</b> n! = n × (n−1) × … × 1 counts the ways to arrange n things.</p>
<p>The mean of n numbers is written x̄ = (1/n) Σ xᵢ — that is all "average" means. Once you can read Σ, most formulas in data science become loops you already understand.</p>
""", practice=["Add 1 to n (Gauss's Trick)", "Sigma Notation: Sum of Squares", "Factorial"])


@LD
def sigma_demo():
    n = 5
    total = 0
    for k in range(1, n + 1):
        total += k ** 2
    formula = n * (n + 1) * (2 * n + 1) // 6
    product = 1
    for k in range(1, n + 1):
        product *= k
