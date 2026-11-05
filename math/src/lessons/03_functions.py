from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "What is a function?", """
<p>A <b>function</b> is a machine: you put a number in, it gives exactly <b>one</b> number out. We write f(x) = 2x + 1: "f of x is two x plus one". f(3) = 7.</p>
<ul>
<li>The allowed inputs are the <b>domain</b> (you can't take √ of a negative or divide by zero).</li>
<li>The possible outputs are the <b>range</b>.</li>
<li>A <b>graph</b> plots every (input, output) pair as a point (x, f(x)).</li>
</ul>
<p>A Python function <code>def f(x): return 2*x + 1</code> is the same idea. A <b>machine-learning model is a function</b>: input features → prediction. Training means choosing the function's numbers well.</p>
""", practice=["Table of Values", "Is It a Function?", "Allowed Inputs (Domain)"])


@LD
def function_machine():
    def f(x):
        return 2 * x + 1
    inputs = [-2, -1, 0, 1, 2, 3]
    outputs = [f(x) for x in inputs]
    fig, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(inputs, outputs, "o-")
    ax.set_xlabel("input x")
    ax.set_ylabel("output f(x)")
    ax.set_title("f(x) = 2x + 1")
    ax.grid(alpha=0.3)


LESSON("Basics", "Straight lines: slope and intercept", """
<p>The simplest graph is a straight line: <b>y = mx + c</b>.</p>
<ul>
<li><b>m</b>, the <b>slope</b>, is how much y goes up when x goes up by 1: rise ÷ run. Positive slopes go up, negative go down, zero is flat.</li>
<li><b>c</b>, the <b>intercept</b>, is where the line crosses the y-axis (the value when x = 0).</li>
</ul>
<p>Through two points (x₁, y₁), (x₂, y₂): m = (y₂ − y₁)/(x₂ − x₁), then c = y₁ − m·x₁.</p>
<p><b>Linear regression</b>, the first ML model everyone learns, is nothing more than choosing the m and c that best fit the data.</p>
""", practice=["Slope Between Two Points", "Equation of a Line Through Two Points", "Where Two Lines Meet", "Inverse of a Line", "Average Rate of Change"])


@LD
def slopes_demo():
    x = np.linspace(-3, 3, 20)
    fig, ax = plt.subplots(figsize=(5, 3))
    for m, c in [(2, 1), (0.5, 1), (0, 1), (-1, 1)]:
        ax.plot(x, m * x + c, label=f"y = {m}x + {c}")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=0.6)
    ax.legend(fontsize=7)
    ax.set_title("Same intercept, different slopes")


LESSON("Core", "Parabolas and transforming graphs", """
<p>y = x² is a U-shape with its lowest point, the <b>vertex</b>, at (0, 0). For y = ax² + bx + c the vertex is at x = −b/2a; a &gt; 0 opens up (has a minimum), a &lt; 0 opens down (a maximum).</p>
<p>Any graph can be moved and stretched: <b>g(x) = a·f(x − h) + k</b></p>
<table><tr><th>Change</th><th>Effect</th></tr>
<tr><td>x − h</td><td>shift right by h</td></tr>
<tr><td>+ k</td><td>shift up by k</td></tr>
<tr><td>a ×</td><td>stretch vertically (flip if negative)</td></tr></table>
<p>Finding the lowest point of a U-shaped curve is exactly what "minimising a loss" means in ML.</p>
""", practice=["Vertex of a Parabola", "Shift and Stretch a Graph", "Even, Odd or Neither?", "Highest Point on a Grid", "Compose Two Functions"])


@LD
def transform_demo():
    x = np.linspace(-3, 5, 200)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, x ** 2, label="x²")
    ax.plot(x, (x - 2) ** 2, label="(x − 2)²  → right 2")
    ax.plot(x, 0.5 * (x - 2) ** 2 + 1, label="0.5(x − 2)² + 1")
    ax.set_ylim(-1, 10)
    ax.legend(fontsize=7)


LESSON("Core", "Exponentials and logarithms", """
<p>An <b>exponential</b> function multiplies by the same factor every step: f(x) = a·bˣ. With b &gt; 1 it explodes (population, compound interest); with 0 &lt; b &lt; 1 it decays (radioactivity, learning-rate schedules). The special base <b>e ≈ 2.718</b> appears everywhere in ML: eˣ = <code>np.exp(x)</code>.</p>
<p>A <b>logarithm</b> answers the reverse question: "b to what power gives n?" log₂ 8 = 3 because 2³ = 8. ln means log base e.</p>
<table><tr><th>Log rule</th><th>Why it matters</th></tr>
<tr><td>log(ab) = log a + log b</td><td>turns products of many probabilities into sums (no underflow)</td></tr>
<tr><td>log(aⁿ) = n log a</td><td>brings exponents down so you can solve for them</td></tr></table>
<p>Logs squash huge ranges (1 to 1 000 000 becomes 0 to 6) — that's why skewed data such as incomes is often log-transformed.</p>
""", practice=["Exponential Growth Table", "Logarithm by Counting", "Solve an Exponential Equation", "Multiply Tiny Probabilities With Logs"])


@LD
def exp_log_demo():
    x = np.linspace(0.05, 4, 200)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, np.exp(x), label="eˣ")
    ax.plot(x, np.log(x), label="ln x")
    ax.plot(x, x, "--", color="gray", label="y = x (mirror line)")
    ax.set_ylim(-3, 6)
    ax.legend()
    ax.set_title("exp and log undo each other")


LESSON("Advanced", "Activation functions: the functions inside neural networks", """
<p>A neural network is a chain of simple functions. Between layers it applies an <b>activation function</b> so the network can bend and model curves, not just straight lines:</p>
<table><tr><th>Function</th><th>Formula</th><th>Output</th></tr>
<tr><td>Sigmoid</td><td>1 / (1 + e⁻ˣ)</td><td>(0, 1) — reads as a probability</td></tr>
<tr><td>tanh</td><td>(eˣ − e⁻ˣ)/(eˣ + e⁻ˣ)</td><td>(−1, 1)</td></tr>
<tr><td>ReLU</td><td>max(0, x)</td><td>[0, ∞) — the default in deep learning</td></tr>
<tr><td>Step</td><td>1 if x ≥ 0 else 0</td><td>{0, 1} — the original perceptron</td></tr></table>
<p>Piecewise functions like ReLU and tax brackets use different rules on different intervals. <b>Composition</b> f(g(x)) — feeding one function into another — is what "layers" are.</p>
""", practice=["Sigmoid Function", "ReLU Activation", "Piecewise Function: Tax Brackets", "Compose Two Functions"])


@LD
def activations():
    x = np.linspace(-5, 5, 200)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, 1 / (1 + np.exp(-x)), label="sigmoid")
    ax.plot(x, np.tanh(x), label="tanh")
    ax.plot(x, np.maximum(0, x), label="ReLU")
    ax.set_ylim(-1.2, 3)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend()


LESSON("Basics", "Reading a graph and substituting", """
<h4>The coordinate plane</h4>
<p>A point (3, 2) means 3 right, 2 up. For a function, x is the input and y = f(x) is the output.</p>
<table><tr><th>You see</th><th>It means</th></tr>
<tr><td>Line going up to the right</td><td>output grows with input (positive slope)</td></tr>
<tr><td>Flat part</td><td>no change: slope 0</td></tr>
<tr><td>Crosses the y-axis</td><td>the value at x = 0</td></tr>
<tr><td>Crosses the x-axis</td><td>a root, where f(x) = 0</td></tr>
<tr><td>Lowest or highest point</td><td>a minimum or maximum</td></tr></table>
<h4>Substituting anything</h4>
<p>f(x) = x² + 1. The x is a slot, and whatever you put in goes everywhere x appears:</p>
<ul><li>f(3) = 9 + 1 = 10</li><li>f(−2) = 4 + 1 = 5</li>
<li>f(a + 1) = (a + 1)² + 1 = a² + 2a + 2</li></ul>
<h4>Domain: what inputs are allowed?</h4>
<ul><li>√(x − 2) needs x ≥ 2.</li><li>1 / (x − 5) needs x ≠ 5.</li><li>log(x) needs x &gt; 0.</li></ul>
<p>These cause most <code>NaN</code> and <code>inf</code> values in real code.</p>
""", practice=["Table of Values", "Allowed Inputs (Domain)", "Is It a Function?"])


@LD
def substitute_demo():
    def f(x):
        return x ** 2 + 1

    values = {x: f(x) for x in [3, -2, 0]}
    a = 4
    direct = f(a + 1)
    expanded = a ** 2 + 2 * a + 2
    xs = np.linspace(-3, 3, 100)
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    ax.plot(xs, f(xs))
    ax.plot(list(values), list(values.values()), "o", color="#b45309")
    ax.set_title("f(x) = x² + 1, with three points marked", fontsize=9)
    ax.grid(alpha=0.3)


LESSON("Core", "Logarithms by hand", """
<p>A log answers: <b>what power do I need?</b></p>
<table><tr><th>Log</th><th>Reads as</th><th>Answer</th></tr>
<tr><td>log₂ 8</td><td>2 to what power gives 8?</td><td>3</td></tr>
<tr><td>log₁₀ 1000</td><td>10 to what power gives 1000?</td><td>3</td></tr>
<tr><td>log₁₀ 0.01</td><td>10 to what power gives 0.01?</td><td>−2</td></tr>
<tr><td>log₅ 1</td><td>5 to what power gives 1?</td><td>0</td></tr></table>
<h4>The rules, checked with numbers</h4>
<ul><li><b>Product:</b> log₁₀(100 × 1000) = 5 = 2 + 3 ✓</li>
<li><b>Power:</b> log₂(8²) = log₂ 64 = 6 = 2 × 3 ✓</li>
<li><b>Change of base:</b> log₂ 10 = ln 10 / ln 2 = 2.303 / 0.693 = 3.322</li></ul>
<p><b>Rule of thumb:</b> log₂ n is how many times you can halve n before reaching 1. log₂ 1000 ≈ 10, which is why binary search is so fast.</p>
<p><b>Mistake:</b> log(a + b) isn't log a + log b. Only products become sums.</p>
<h4>Why logs matter in data</h4>
<p>They compress big ranges and turn multiplying into adding. The chart shows the same exponential growth with normal and log scales; on a log scale it's a straight line.</p>
""", practice=["Logarithm by Counting", "Solve an Exponential Equation", "Multiply Tiny Probabilities With Logs"])


@LD
def log_checks():
    product_rule = (math.log10(100 * 1000), math.log10(100) + math.log10(1000))
    power_rule = (math.log2(8 ** 2), 2 * math.log2(8))
    change_of_base = math.log(10) / math.log(2)
    halvings = math.log2(1000)
    x = np.arange(0, 31)
    y = 2.0 ** x
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.6))
    left.plot(x, y)
    left.set_title("normal scale", fontsize=9)
    right.semilogy(x, y)
    right.set_title("log scale: a straight line", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Composition and inverses by hand", """
<p>f(x) = 2x + 3 and g(x) = x².</p>
<h4>Composition: feed one into the other</h4>
<table><tr><th>Expression</th><th>Inside first</th><th>Then</th><th>At x = 2</th></tr>
<tr><td>f(g(x))</td><td>g(2) = 4</td><td>f(4) = 11</td><td>11</td></tr>
<tr><td>g(f(x))</td><td>f(2) = 7</td><td>g(7) = 49</td><td>49</td></tr></table>
<p><b>Order matters.</b> A neural network is a long composition, with each layer feeding the next.</p>
<h4>Inverse: undo the function</h4>
<ol><li>Write y = 2x + 3.</li><li>Solve for x: x = (y − 3) / 2.</li><li>So f⁻¹(x) = (x − 3) / 2.</li><li>Check: f(5) = 13 and f⁻¹(13) = 5 ✓.</li></ol>
<p>A function needs one output to come from just one input to have an inverse. x² doesn't, since (−2)² = 2² = 4; restrict it to x ≥ 0 and √x undoes it.</p>
<p><b>Inverses in ML:</b> exp and ln undo each other, and the sigmoid's inverse is the logit (log-odds).</p>
""", practice=["Compose Two Functions", "Inverse of a Line"])


@LD
def compose_inverse():
    def f(x):
        return 2 * x + 3

    def g(x):
        return x ** 2

    def f_inverse(x):
        return (x - 3) / 2

    f_of_g = f(g(2))
    g_of_f = g(f(2))
    round_trip = f_inverse(f(5))
    not_one_to_one = (g(-2), g(2))
    logit_of_sigmoid = math.log((1 / (1 + math.exp(-1.5))) / (1 - 1 / (1 + math.exp(-1.5))))


LESSON("Advanced", "How fast do functions grow?", """
<p>When data grows, which part dominates? This decides whether code finishes.</p>
<table><tr><th>n</th><th>log₂ n</th><th>n</th><th>n log₂ n</th><th>n²</th><th>2ⁿ</th></tr>
<tr><td>10</td><td>3.3</td><td>10</td><td>33</td><td>100</td><td>1,024</td></tr>
<tr><td>100</td><td>6.6</td><td>100</td><td>664</td><td>10,000</td><td>about 10³⁰</td></tr>
<tr><td>1,000</td><td>10</td><td>1,000</td><td>9,966</td><td>1,000,000</td><td>unimaginable</td></tr></table>
<p>Going from 10 to 1,000 rows multiplies n² work by 10,000.</p>
<h4>Where you'll see them</h4>
<ul><li><b>log n:</b> binary search, tree depth</li><li><b>n log n:</b> sorting, tree building</li>
<li><b>n²:</b> comparing every pair of points (k-NN by brute force)</li><li><b>2ⁿ:</b> trying every subset of features, which is why nobody does</li></ul>
<p><b>Only the fastest-growing term matters</b> for large n: in n² + 100n, at n = 1,000,000 the first term is 10¹² and the second just 10⁸.</p>
""", practice=["Exponential Growth Table", "Highest Point on a Grid"])


@LD
def growth_rates():
    n = np.arange(1, 21)
    fig, ax = plt.subplots(figsize=(4.8, 3))
    ax.semilogy(n, np.log2(n) + 1, label="log n")
    ax.semilogy(n, n, label="n")
    ax.semilogy(n, n * np.log2(n) + 1, label="n log n")
    ax.semilogy(n, n ** 2, label="n²")
    ax.semilogy(n, 2.0 ** n, label="2ⁿ")
    ax.set_xlabel("n")
    ax.legend(fontsize=7)


LESSON("Advanced", "The number e and exponential decay", """
<h4>Where e comes from</h4>
<p>₹1 at 100% yearly interest, added in n equal parts through the year, grows to (1 + 1/n)ⁿ:</p>
<table><tr><th>n</th><th>1</th><th>2</th><th>10</th><th>100</th><th>1000</th></tr>
<tr><th>Value</th><td>2</td><td>2.25</td><td>2.5937</td><td>2.7048</td><td>2.7169</td></tr></table>
<p>It approaches <b>e ≈ 2.71828</b>. eˣ is special: its slope at any point equals its height, which makes all of calculus with it easy.</p>
<h4>Decay</h4>
<p>Multiply by a number below 1 repeatedly. With half-life steps, 100 → 50 → 25 → <b>12.5</b> after 3 steps.</p>
<p><b>In ML, a learning-rate schedule</b> does this: starting at 0.1 and multiplying by 0.9 each epoch gives 0.09 after 1 epoch, 0.059 after 5, and 0.035 after 10.</p>
""", practice=["Exponential Growth Table", "Sigmoid Function"])


@LD
def e_and_decay():
    approaching = {n: round((1 + 1 / n) ** n, 4) for n in [1, 2, 10, 100, 1000]}
    half_life = [100 * 0.5 ** k for k in range(4)]
    rates = 0.1 * 0.9 ** np.arange(21)
    fig, ax = plt.subplots(figsize=(4.4, 2.7))
    ax.plot(rates)
    ax.set_xlabel("epoch")
    ax.set_ylabel("learning rate")
