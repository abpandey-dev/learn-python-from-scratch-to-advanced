from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Rate of change and the idea of a limit", """
<p>Calculus is the math of <b>change</b>. Speed is change in distance per second; the slope of a line is change in y per change in x. But a <b>curve</b> has a different steepness at every point. How steep is y = x² exactly at x = 3?</p>
<p>Idea: take a second point a tiny step h away and compute the slope between them (a <b>secant</b>): (f(3 + h) − f(3))/h. Make h smaller and smaller:</p>
<table><tr><th>h</th><th>slope</th></tr><tr><td>0.1</td><td>6.1</td></tr><tr><td>0.01</td><td>6.01</td></tr><tr><td>0.001</td><td>6.001</td></tr></table>
<p>The numbers home in on 6. That target is a <b>limit</b>, and the slope at a single point is the <b>derivative</b>: f′(3) = 6.</p>
""", practice=["Derivative From the Definition", "Derivative of sin x"])


@LD
def secant_to_tangent():
    x = np.linspace(1, 5, 100)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, x ** 2, color="black", label="y = x²")
    for h in [1.5, 0.75, 0.25]:
        m = ((3 + h) ** 2 - 9) / h
        ax.plot(x, 9 + m * (x - 3), "--", label=f"h = {h}: slope {m:.2f}")
    ax.plot(x, 9 + 6 * (x - 3), color="#b45309", label="tangent: slope 6")
    ax.set_ylim(0, 25)
    ax.legend(fontsize=7)


LESSON("Basics", "Derivative rules", """
<p>Nobody computes limits every time. A few rules cover almost everything:</p>
<table>
<tr><th>Rule</th><th>Formula</th><th>Example</th></tr>
<tr><td>Constant</td><td>(c)′ = 0</td><td>(7)′ = 0</td></tr>
<tr><td>Power</td><td>(xⁿ)′ = n·xⁿ⁻¹</td><td>(x³)′ = 3x²</td></tr>
<tr><td>Sum</td><td>(f + g)′ = f′ + g′</td><td>(x² + x)′ = 2x + 1</td></tr>
<tr><td>Product</td><td>(fg)′ = f′g + fg′</td><td>(x·eˣ)′ = eˣ + x·eˣ</td></tr>
<tr><td>Chain</td><td>f(g(x))′ = f′(g(x))·g′(x)</td><td>((2x + 1)³)′ = 3(2x + 1)²·2</td></tr>
<tr><td>Exponential, log</td><td>(eˣ)′ = eˣ, (ln x)′ = 1/x</td><td></td></tr>
</table>
<p>The <b>chain rule</b> is the most important for ML: a neural network is functions inside functions, and <b>backpropagation is just the chain rule applied layer by layer</b>.</p>
""", practice=["Power Rule for Polynomials", "Slope of a Curve at a Point", "Product Rule", "Chain Rule", "Derivative of the Sigmoid", "Tangent Line"])


@LD
def function_and_derivative():
    x = np.linspace(-2.5, 2.5, 200)
    p = [1, 0, -3, 0]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, np.polyval(p, x), label="f(x) = x³ − 3x")
    ax.plot(x, np.polyval(np.polyder(p), x), label="f′(x) = 3x² − 3")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.legend()
    ax.set_title("f′ is zero exactly where f turns", fontsize=9)


LESSON("Core", "Finding maximums and minimums", """
<p>At the top of a hill or the bottom of a valley the curve is momentarily flat: <b>f′(x) = 0</b>. These are <b>critical points</b>.</p>
<p>The <b>second derivative</b> f″ (the derivative of the derivative) measures curvature and tells them apart:</p>
<ul><li>f″ &gt; 0: curve bends up like a cup → <b>minimum</b></li><li>f″ &lt; 0: bends down like a cap → <b>maximum</b></li></ul>
<p>Training an ML model <b>is</b> finding the minimum of a loss function. With one weight you could solve f′ = 0 by hand; with millions you follow the slope downhill step by step — gradient descent (next topic). <b>Newton's method</b> uses f′ (and f″) to jump towards roots or minimums very fast.</p>
""", practice=["Critical Points of a Cubic", "Maximum or Minimum?", "Second Derivative", "Lowest Point of a Curve", "Newton's Method"])


@LD
def newton_demo():
    f = lambda x: x ** 3 - x - 2
    df = lambda x: 3 * x ** 2 - 1
    x = 3.0
    steps = [x]
    for _ in range(4):
        x = x - f(x) / df(x)
        steps.append(x)
    xs = np.linspace(0, 3.2, 200)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(xs, f(xs), color="black")
    ax.axhline(0, color="gray", linewidth=0.6)
    for a, b in zip(steps, steps[1:]):
        ax.plot([a, b], [f(a), 0], "--", color="#b45309")
        ax.plot(a, f(a), "o", color="#0f766e")
    ax.set_title(f"Newton: 3 → {steps[-1]:.4f} in 4 steps", fontsize=9)


LESSON("Core", "Integrals: adding up tiny pieces", """
<p>The <b>integral</b> ∫ₐᵇ f(x) dx is the <b>area under the curve</b> between a and b. Estimate it by slicing into thin rectangles (a <b>Riemann sum</b>) or trapezoids; thinner slices give better answers.</p>
<p>The <b>Fundamental Theorem of Calculus</b> connects the two halves of calculus: integration undoes differentiation. If F′ = f, then ∫ₐᵇ f dx = F(b) − F(a). For powers: ∫ xⁿ dx = xⁿ⁺¹/(n + 1).</p>
<p>In data science, integrals give probabilities (area under a probability curve), expected values, and the AUC of an ROC curve.</p>
""", practice=["Area by Rectangles", "Distance From Speed Readings", "Antiderivative of a Polynomial", "Exact Area Under a Polynomial", "Average Value of a Function", "Area Between Two Curves"])


@LD
def riemann_demo():
    a, b, n = 0, 2, 8
    dx = (b - a) / n
    lefts = a + dx * np.arange(n)
    estimate = (lefts ** 2).sum() * dx
    exact = (b ** 3 - a ** 3) / 3
    xs = np.linspace(a, b, 100)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(xs, xs ** 2, color="black")
    ax.bar(lefts, lefts ** 2, width=dx, align="edge", alpha=0.4, edgecolor="#0f766e")
    ax.set_title(f"8 rectangles: {estimate:.3f}   exact: {exact:.3f}", fontsize=9)


LESSON("Advanced", "Derivatives of real data", """
<p>Real measurements come as samples, not formulas. Derivatives become <b>differences</b>: speed ≈ (next position − previous position)/(2·dt) — <code>np.gradient</code>. Integrals become sums — the trapezoid rule.</p>
<p>The same numerical tricks let you <b>check</b> hand-derived gradients in ML code: compare your formula against (f(x + h) − f(x − h))/2h. This "gradient check" catches most backprop bugs.</p>
""", practice=["Speed From Position Readings", "Derivative of sin x", "Derivative From the Definition"])


@LD
def data_derivative():
    t = np.arange(0, 6, 0.5)
    position = 2 * t ** 2
    speed = np.gradient(position, 0.5)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(t, position, "o-", label="position 2t²")
    ax.plot(t, speed, "s-", label="speed ≈ 4t (np.gradient)")
    ax.set_xlabel("time")
    ax.legend()


LESSON("Basics", "Limits by hand", """
<p>A limit asks: <b>what value does f approach as x gets close to a point?</b> It doesn't matter what happens exactly at that point.</p>
<h4>Example 1: a hole in a graph</h4>
<p>f(x) = (x² − 1) / (x − 1). At x = 1 this is 0/0, undefined. Try nearby values:</p>
<table><tr><th>x</th><th>1.1</th><th>1.01</th><th>1.001</th></tr><tr><th>f(x)</th><td>2.1</td><td>2.01</td><td>2.001</td></tr></table>
<p>The limit is <b>2</b>. Algebra agrees: (x² − 1) = (x − 1)(x + 1), so f(x) = x + 1 for x ≠ 1.</p>
<h4>Example 2: sin(x) / x near 0</h4>
<table><tr><th>x</th><th>1</th><th>0.1</th><th>0.01</th></tr><tr><th>sin(x) / x</th><td>0.84147</td><td>0.99833</td><td>0.99998</td></tr></table>
<p>The limit is <b>1</b>.</p>
<h4>Why do we care?</h4>
<p>A slope needs two points, but "the slope at a point" has only one. A limit solves this: make the two points closer and closer and see what the slope approaches. That's a derivative.</p>
""", practice=["Derivative From the Definition"])


@LD
def limit_tables():
    near_one = {x: round((x ** 2 - 1) / (x - 1), 4) for x in [1.1, 1.01, 1.001, 0.999]}
    near_zero = {x: round(math.sin(x) / x, 5) for x in [1, 0.1, 0.01]}
    xs = np.linspace(0, 2, 101)
    xs = xs[np.abs(xs - 1) > 1e-9]
    fig, ax = plt.subplots(figsize=(4.2, 2.7))
    ax.plot(xs, (xs ** 2 - 1) / (xs - 1))
    ax.plot(1, 2, "o", markerfacecolor="white", color="#b45309", markersize=8)
    ax.set_title("A hole at x = 1, yet the limit is 2", fontsize=9)


LESSON("Basics", "The derivative from first principles", """
<p>Find the derivative of f(x) = x² using the definition: the limit of (f(x + h) − f(x)) / h as h → 0.</p>
<ol><li>(x + h)² − x² = x² + 2xh + h² − x² = 2xh + h²</li>
<li>Divide by h: 2x + h</li>
<li>Let h → 0: <b>2x</b></li></ol>
<p>So at x = 3 the slope is 6, which matches the shrinking-secant table you saw earlier.</p>
<h4>Now use the rules</h4>
<p>f(x) = 3x² + 2x − 5, term by term:</p>
<table><tr><th>Term</th><th>Derivative</th><th>Rule</th></tr>
<tr><td>3x²</td><td>6x</td><td>bring the power down, reduce it by 1</td></tr>
<tr><td>2x</td><td>2</td><td>slope of a line</td></tr>
<tr><td>−5</td><td>0</td><td>constants don't change</td></tr></table>
<p>f′(x) = 6x + 2, so f′(1) = 8. At x = 1, a tiny increase in x raises f about 8 times as much.</p>
<p><b>What f′ tells you:</b> positive means rising, negative means falling, zero means flat, and a larger size means steeper.</p>
""", practice=["Power Rule for Polynomials", "Slope of a Curve at a Point", "Tangent Line", "Second Derivative"])


@LD
def first_principles():
    x = 3.0
    estimates = {h: round(((x + h) ** 2 - x ** 2) / h, 4) for h in [1, 0.1, 0.01, 0.001]}
    derivative = np.polyder([3, 2, -5])
    at_one = np.polyval(derivative, 1)
    h = 0.0001
    numeric_check = round(((3 * (1 + h) ** 2 + 2 * (1 + h) - 5) - (3 + 2 - 5)) / h, 3)


LESSON("Core", "Chain and product rule, worked", """
<h4>Chain rule: outside times inside</h4>
<p>f(x) = (3x + 1)².</p>
<ol><li>Outside: something² has derivative 2 × something.</li>
<li>Inside: 3x + 1 has derivative 3.</li>
<li>Multiply: 2(3x + 1) × 3 = <b>18x + 6</b>.</li></ol>
<p><b>Check by expanding:</b> 9x² + 6x + 1 has derivative 18x + 6 ✓.</p>
<table><tr><th>Function</th><th>Outside</th><th>Inside</th><th>Derivative</th></tr>
<tr><td>e^(2x)</td><td>eᵘ</td><td>2x</td><td>2e^(2x)</td></tr>
<tr><td>e^(−x²)</td><td>eᵘ</td><td>−x²</td><td>−2x·e^(−x²)</td></tr>
<tr><td>ln(x² + 1)</td><td>ln u</td><td>x² + 1</td><td>2x / (x² + 1)</td></tr>
<tr><td>(y − wx)²</td><td>u²</td><td>y − wx (with respect to w)</td><td>−2x(y − wx)</td></tr></table>
<p>The last row is exactly the gradient used to train linear regression.</p>
<h4>Product rule</h4>
<p>(x²·eˣ)′ = 2x·eˣ + x²·eˣ: first′ × second + first × second′.</p>
<p><b>Common mistake:</b> forgetting the inside derivative, as in writing e^(2x) instead of 2e^(2x).</p>
""", practice=["Chain Rule", "Product Rule", "Derivative of the Sigmoid", "Derivative of sin x"])


@LD
def chain_checks():
    def numeric(f, x, h=1e-6):
        return (f(x + h) - f(x - h)) / (2 * h)

    x = 1.5
    outer_inner = (numeric(lambda t: (3 * t + 1) ** 2, x), 18 * x + 6)
    exp_case = (numeric(lambda t: math.exp(-t ** 2), x), -2 * x * math.exp(-x ** 2))
    log_case = (numeric(lambda t: math.log(t ** 2 + 1), x), 2 * x / (x ** 2 + 1))
    w, y, xi = 2.0, 10.0, 3.0
    loss_case = (numeric(lambda t: (y - t * xi) ** 2, w), -2 * xi * (y - w * xi))


LESSON("Core", "Optimisation problems, worked", """
<h4>The biggest field</h4>
<p>You have 40 m of fence for a rectangle. What's the largest area?</p>
<ol><li><b>Variable:</b> width x, so height = 20 − x.</li>
<li><b>Goal:</b> A(x) = x(20 − x) = 20x − x².</li>
<li><b>Slope = 0:</b> A′ = 20 − 2x = 0, so x = 10.</li>
<li><b>Maximum?</b> A″ = −2 is negative, so yes.</li></ol>
<p>A 10 × 10 square gives <b>100 m²</b>.</p>
<h4>Why is the mean the "best single guess"?</h4>
<p>Choose a number c to minimise the total squared error Σ(xᵢ − c)². The derivative is −2Σ(xᵢ − c). Setting it to 0 gives Σxᵢ = n·c, so <b>c = the mean</b>.</p>
<p>Minimise absolute error instead, and the answer is the <b>median</b>. So the choice of loss decides what a model predicts. This explains why MSE models predict averages and why MAE resists outliers.</p>
""", practice=["Critical Points of a Cubic", "Maximum or Minimum?", "Lowest Point of a Curve"])


@LD
def best_guess():
    x = np.array([1.0, 2, 3, 4, 20])
    candidates = np.linspace(0, 20, 401)
    squared = ((x[:, None] - candidates) ** 2).sum(axis=0)
    absolute = np.abs(x[:, None] - candidates).sum(axis=0)
    best_squared = candidates[squared.argmin()]
    best_absolute = candidates[absolute.argmin()]
    mean_median = (x.mean(), np.median(x))
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 2.6))
    axes[0].plot(candidates, squared)
    axes[0].set_title(f"squared error: best at {best_squared:.1f} (mean)", fontsize=9)
    axes[1].plot(candidates, absolute, color="#b45309")
    axes[1].set_title(f"absolute error: best at {best_absolute:.1f} (median)", fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "Approximating with lines: Taylor and Newton", """
<h4>Near a point, a curve looks straight</h4>
<p>f(x) ≈ f(a) + f′(a)(x − a). Estimate √4.1 using a = 4, where √4 = 2 and the slope 1/(2√4) = 1/4:</p>
<p>√4.1 ≈ 2 + 0.25 × 0.1 = <b>2.025</b>. The true value is 2.02485, so it's very close.</p>
<p><b>This is why gradient descent works:</b> for small steps, the slope predicts the change in the loss, and that's why steps must stay small.</p>
<h4>Adding terms improves it</h4>
<p>eˣ = 1 + x + x²/2! + x³/3! + … At x = 1: 1 + 1 + 0.5 + 0.1667 + 0.0417 = 2.7083. The true e is 2.7183.</p>
<h4>Newton's method by hand</h4>
<p>Find √2, a root of x² − 2. The update is x − (x² − 2)/(2x):</p>
<table><tr><th>Step</th><th>x</th></tr><tr><td>Start</td><td>1</td></tr><tr><td>1</td><td>1.5</td></tr><tr><td>2</td><td>1.41667</td></tr><tr><td>3</td><td>1.41422 (true: 1.41421)</td></tr></table>
<p>Correct digits roughly double each step.</p>
""", practice=["Newton's Method"])


@LD
def taylor_demo():
    approx = 2 + 0.25 * 0.1
    true_value = math.sqrt(4.1)
    newton = [1.0]
    for _ in range(3):
        x = newton[-1]
        newton.append(x - (x ** 2 - 2) / (2 * x))
    xs = np.linspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(xs, np.exp(xs), color="black", label="eˣ")
    ax.plot(xs, 1 + xs, label="1 + x")
    ax.plot(xs, 1 + xs + xs ** 2 / 2, label="adding x²/2")
    ax.plot(xs, 1 + xs + xs ** 2 / 2 + xs ** 3 / 6, label="adding x³/6")
    ax.set_ylim(-1, 7)
    ax.legend(fontsize=7)


LESSON("Advanced", "Integrals, worked", """
<h4>Rectangles approach the exact area</h4>
<p>Area under x² from 0 to 2, using left rectangles:</p>
<table><tr><th>Rectangles</th><th>4</th><th>8</th><th>100</th><th>1000</th><th>Exact</th></tr>
<tr><th>Estimate</th><td>1.75</td><td>2.1875</td><td>2.6268</td><td>2.6627</td><td>2.6667</td></tr></table>
<h4>The exact answer in two lines</h4>
<p>An antiderivative of x² is x³/3 (its derivative gives x² back). So the area = 2³/3 − 0³/3 = 8/3 = 2.6667.</p>
<p><b>Why does this work?</b> As you widen the region by a tiny dx, the area grows by height × dx. So the area's rate of growth is the height, f(x). Finding the area means undoing a derivative.</p>
<table><tr><th>Integral</th><th>Result</th></tr>
<tr><td>∫ x³ dx</td><td>x⁴/4 + C</td></tr><tr><td>∫ (2x + 1) dx</td><td>x² + x + C</td></tr><tr><td>∫ eˣ dx</td><td>eˣ + C</td></tr><tr><td>∫ 1/x dx</td><td>ln|x| + C</td></tr></table>
<p><b>Where it's used:</b> a probability is an area under a density. Expected value is ∫ x·f(x) dx. ROC AUC is an area, computed with the trapezoid rule.</p>
""", practice=["Area by Rectangles", "Antiderivative of a Polynomial", "Exact Area Under a Polynomial", "Average Value of a Function", "Area Between Two Curves", "Distance From Speed Readings", "Speed From Position Readings"])


@LD
def rectangles_converge():
    def left_sum(n):
        dx = 2 / n
        return float((np.arange(n) * dx) ** 2 @ np.full(n, dx))

    estimates = {n: round(left_sum(n), 4) for n in [4, 8, 100, 1000]}
    antiderivative = np.polyint([1, 0, 0])
    exact = np.polyval(antiderivative, 2) - np.polyval(antiderivative, 0)
    sizes = np.arange(2, 200)
    errors = [exact - left_sum(int(n)) for n in sizes]
    fig, ax = plt.subplots(figsize=(4.4, 2.7))
    ax.loglog(sizes, errors)
    ax.set_xlabel("number of rectangles")
    ax.set_ylabel("error")
