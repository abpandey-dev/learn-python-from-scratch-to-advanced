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
