from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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


LESSON("Basics", "Negative numbers without fear", """
<p>Think of a number line. <b>Adding</b> moves right, and <b>subtracting</b> moves left.</p>
<table><tr><th>Calculation</th><th>Think of it as</th><th>Answer</th></tr>
<tr><td>−3 + 5</td><td>start at −3, move 5 right</td><td>2</td></tr>
<tr><td>2 − 6</td><td>start at 2, move 6 left</td><td>−4</td></tr>
<tr><td>−4 − 3</td><td>start at −4, move 3 further left</td><td>−7</td></tr>
<tr><td>5 − (−2)</td><td>taking away a debt is like gaining</td><td>7</td></tr></table>
<h4>Multiplying and dividing: count the minus signs</h4>
<table><tr><th>Signs</th><th>Result</th><th>Example</th></tr>
<tr><td>Same</td><td>positive</td><td>−2 × −4 = 8</td></tr>
<tr><td>Different</td><td>negative</td><td>−2 × 4 = −8</td></tr></table>
<p><b>Why is −2 × −4 positive?</b> Follow the pattern: −2 × 2 = −4, −2 × 1 = −2, −2 × 0 = 0. Each step adds 2. Continue: −2 × −1 = 2, −2 × −2 = 4.</p>
<h4>A common slip</h4>
<p>−3² means −(3²) = <b>−9</b>, because powers come before the minus. (−3)² = <b>9</b>. Python agrees: <code>-3**2</code> gives −9.</p>
""", practice=["Distance on the Number Line"])


@LD
def negatives():
    moves = [-3 + 5, 2 - 6, -4 - 3, 5 - (-2)]
    pattern = [-2 * k for k in [2, 1, 0, -1, -2]]
    power_first = -3 ** 2
    bracket_first = (-3) ** 2


LESSON("Basics", "GCD, LCM and primes by hand", """
<h4>Greatest common divisor, by Euclid's method</h4>
<p>GCD of 48 and 18. Keep dividing and use the remainder:</p>
<pre><code class="py">48 = 2 × 18 + 12
18 = 1 × 12 + 6
12 = 2 × 6  + 0      remainder 0, so the answer is 6</code></pre>
<p>Use it to simplify: 48/18 = 8/3, dividing both by 6.</p>
<h4>Least common multiple</h4>
<p>LCM × GCD = a × b, so LCM(48, 18) = 48 × 18 / 6 = <b>144</b>. You need this as the common bottom when adding fractions.</p>
<h4>Prime factors</h4>
<p>Keep dividing by the smallest prime that fits:</p>
<pre><code class="py">60 → 2 × 30 → 2 × 2 × 15 → 2 × 2 × 3 × 5</code></pre>
<p>To test if a number is prime, you only need to try divisors up to its square root. If 97 had a factor above √97 ≈ 9.8, it would also have one below it. Trying 2, 3, 5 and 7 finds none, so 97 is prime.</p>
""", practice=["Greatest Common Divisor", "Least Common Multiple", "Simplify a Fraction", "Is It Prime?", "Prime Factorisation"])


@LD
def euclid_steps():
    a, b = 48, 18
    steps = []
    while b:
        steps.append((a, b, a % b))
        a, b = b, a % b
    gcd = a
    lcm = 48 * 18 // gcd
    simplified = (48 // gcd, 18 // gcd)


LESSON("Core", "The three kinds of percent problem", """
<table><tr><th>Question</th><th>Method</th><th>Answer</th></tr>
<tr><td>What is 20% of 250?</td><td>0.20 × 250</td><td>50</td></tr>
<tr><td>30 is what percent of 120?</td><td>30 / 120 × 100</td><td>25%</td></tr>
<tr><td>After 20% off, a price is 400. What was it?</td><td>400 / 0.80</td><td>500</td></tr></table>
<h4>The third one catches people</h4>
<p>The wrong way: 400 + 20% of 400 = 480. The discount was 20% of the <b>original</b>, not of 400. So 0.80 × original = 400.</p>
<h4>Percentages don't simply add</h4>
<p>₹100 rises 50% to ₹150, then falls 50% to <b>₹75</b>. The second percent is taken from a bigger number. Multiply instead: 100 × 1.5 × 0.5.</p>
<h4>Percent vs percentage points</h4>
<p>An accuracy rising from 80% to 88% is up <b>8 percentage points</b>, or <b>10 percent</b> (8 / 80). Say which you mean.</p>
""", practice=["Percent Change", "Fraction to Decimal and Percent", "Share in a Ratio"])


@LD
def percent_steps():
    share = 0.20 * 250
    what_percent = 30 / 120 * 100
    original = 400 / 0.80
    up_then_down = 100 * 1.5 * 0.5
    points = 88 - 80
    percent_rise = (88 - 80) / 80 * 100


LESSON("Core", "Exponent rules in action", """
<p>Each rule follows from "a power means repeated multiplying".</p>
<table><tr><th>Simplify</th><th>Why</th><th>Answer</th></tr>
<tr><td>2³ × 2⁴</td><td>(2·2·2)(2·2·2·2): 7 twos</td><td>2⁷ = 128</td></tr>
<tr><td>x⁵ / x²</td><td>two x's cancel</td><td>x³</td></tr>
<tr><td>(x²)³</td><td>x²·x²·x²</td><td>x⁶</td></tr>
<tr><td>5⁰</td><td>5³ / 5³ = 1</td><td>1</td></tr>
<tr><td>2⁻³</td><td>one over 2³</td><td>1/8</td></tr>
<tr><td>8^(2/3)</td><td>cube root of 8 is 2, then square it</td><td>4</td></tr></table>
<h4>Mistakes to avoid</h4>
<ul><li>2³ × 3² can't be combined, as the bases differ.</li>
<li>(a + b)² isn't a² + b². Try a = b = 1: it gives 4, not 2.</li></ul>
<h4>Scientific notation</h4>
<p>Multiply the front numbers and add the powers: (3 × 10⁴) × (2 × 10⁻²) = 6 × 10² = 600. This is how you estimate quickly, and why logs turn multiplying into adding.</p>
""", practice=["Power by Repeated Multiplication", "Negative and Fractional Exponents", "Scientific Notation", "Square Root by Guessing"])


@LD
def exponent_checks():
    product_rule = (2 ** 3 * 2 ** 4, 2 ** 7)
    power_rule = ((3 ** 2) ** 3, 3 ** 6)
    zero_power = 5 ** 0
    negative = 2 ** -3
    fractional = round(8 ** (2 / 3), 6)
    not_equal = ((1 + 1) ** 2, 1 ** 2 + 1 ** 2)
    scientific = 3e4 * 2e-2


LESSON("Advanced", "Reading the formulas you'll meet in ML", """
<p>Σ is just a loop. Here's how to expand any formula: write it out for i = 1, 2, 3.</p>
<table><tr><th>Formula</th><th>Written out</th><th>With numbers</th></tr>
<tr><td>Σᵢ₌₁³ 2i</td><td>2·1 + 2·2 + 2·3</td><td>12</td></tr>
<tr><td>x̄ = (1/n) Σ xᵢ</td><td>(x₁ + x₂ + x₃) / 3</td><td>x = 2, 4, 9 gives 5</td></tr>
<tr><td>MSE = (1/n) Σ (yᵢ − ŷᵢ)²</td><td>average of squared errors</td><td>errors 1, −2, 3 give 14/3 = 4.67</td></tr>
<tr><td>w·x = Σ wᵢxᵢ</td><td>w₁x₁ + w₂x₂</td><td>(2, 3)·(4, 5) = 23</td></tr></table>
<h4>Rules that make Σ easy</h4>
<ul><li>A constant comes out: Σ 3xᵢ = 3 Σ xᵢ.</li>
<li>Sums split: Σ (xᵢ + yᵢ) = Σ xᵢ + Σ yᵢ.</li>
<li>But products don't: Σ xᵢyᵢ isn't (Σ xᵢ)(Σ yᵢ).</li></ul>
<h4>Symbols to recognise</h4>
<table><tr><td>x̄</td><td>the mean of x</td><td>ŷ</td><td>a prediction</td></tr>
<tr><td>xᵢ</td><td>the i-th item</td><td>θ, w</td><td>model parameters</td></tr>
<tr><td>Π</td><td>multiply all</td><td>argmax</td><td>the input that gives the largest output</td></tr>
<tr><td>∈</td><td>"is in"</td><td>≈</td><td>about equal</td></tr></table>
""", practice=["Sigma Notation: Sum of Squares", "Add 1 to n (Gauss's Trick)", "Factorial"])


@LD
def formulas_as_code():
    x = [2, 4, 9]
    mean = sum(x) / len(x)
    errors = [1, -2, 3]
    mse = sum(e ** 2 for e in errors) / len(errors)
    w, features = [2, 3], [4, 5]
    weighted_sum = sum(a * b for a, b in zip(w, features))
    constant_out = (sum(3 * v for v in x), 3 * sum(x))
