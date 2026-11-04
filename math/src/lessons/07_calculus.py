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
