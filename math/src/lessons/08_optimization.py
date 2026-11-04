from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Functions of several variables and partial derivatives", """
<p>A model's loss depends on <b>many</b> weights at once: L(w₁, w₂, …). Picture a landscape: two inputs (x, y) and the height f(x, y).</p>
<p>A <b>partial derivative</b> ∂f/∂x asks: "if I move only in the x direction, keeping y fixed, how steep is it?" Compute it like an ordinary derivative, treating every other variable as a constant:</p>
<pre><code class="py">f(x, y) = x²y + 3y²
∂f/∂x = 2xy          (y is a constant)
∂f/∂y = x² + 6y      (x is a constant)</code></pre>
""", practice=["Partial Derivatives", "The Hessian Matrix"])


@LD
def landscape():
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = X ** 2 + 3 * Y ** 2
    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    cs = ax.contour(X, Y, Z, levels=12)
    ax.clabel(cs, fontsize=6)
    ax.set_title("f(x, y) = x² + 3y² seen from above", fontsize=9)
    ax.set_aspect("equal")


LESSON("Core", "The gradient: the uphill arrow", """
<p>Collect all the partial derivatives into one vector: the <b>gradient</b> ∇f = (∂f/∂x, ∂f/∂y, …).</p>
<ul>
<li>∇f points in the direction of <b>steepest ascent</b>; its length is how steep.</li>
<li>−∇f points <b>steepest downhill</b>.</li>
<li>The rate of change in any direction u is ∇f·u (the <b>directional derivative</b>).</li>
<li>At the bottom of a valley ∇f = 0.</li>
</ul>
<p>On a contour map the gradient arrows always cross the contour lines at right angles.</p>
""", practice=["The Gradient Vector", "Gradient of a Quadratic Form", "Directional Derivative", "Steepest Downhill Direction"])


@LD
def gradient_arrows():
    x = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, x)
    Z = X ** 2 + 3 * Y ** 2
    gx, gy = np.meshgrid(np.linspace(-2.5, 2.5, 7), np.linspace(-2.5, 2.5, 7))
    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    ax.contour(X, Y, Z, levels=10, alpha=0.6)
    ax.quiver(gx, gy, -2 * gx, -6 * gy, color="#b45309")
    ax.set_title("−∇f: arrows point downhill", fontsize=9)
    ax.set_aspect("equal")


LESSON("Core", "Gradient descent", """
<p>To find the lowest point when you can't see the whole landscape: look at the slope under your feet and take a small step downhill. Repeat.</p>
<p style="text-align:center"><b>w ← w − learning_rate × ∇L(w)</b></p>
<p>The <b>learning rate</b> controls the step size:</p>
<ul><li>too small → painfully slow</li><li>too big → overshoots, bounces, even <b>diverges</b> (the loss grows)</li><li>just right → smooth decrease</li></ul>
<p>Long narrow valleys (features on very different scales) make descent zig-zag — another reason to scale features. Every neural network, from a single neuron to GPT, is trained by variations of this loop (SGD, momentum, Adam).</p>
""", practice=["One Gradient-Descent Step", "Gradient Descent in 1-D", "Is the Learning Rate Too Big?", "Descent in a Long Narrow Valley"])


@LD
def descent_paths():
    def run(lr, steps=12):
        p = np.array([2.5, 1.5])
        path = [p]
        for _ in range(steps):
            p = p - lr * np.array([2 * p[0], 6 * p[1]])
            path.append(p)
        return np.array(path)
    x = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, x)
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    ax.contour(X, Y, X ** 2 + 3 * Y ** 2, levels=12, alpha=0.5)
    for lr, colour in [(0.05, "#0f766e"), (0.3, "#b45309")]:
        path = run(lr)
        ax.plot(path[:, 0], path[:, 1], "o-", markersize=3, color=colour, label=f"lr = {lr}")
    ax.legend(fontsize=7)
    ax.set_aspect("equal")


LESSON("Advanced", "Training a model: loss, gradient, loop", """
<p>Fit y ≈ m·x + b by gradient descent:</p>
<ol>
<li><b>Loss</b>: mean squared error L = (1/n) Σ (yᵢ − (m xᵢ + b))².</li>
<li><b>Gradient</b> by the chain rule: ∂L/∂m = −(2/n) Σ xᵢ·errᵢ, ∂L/∂b = −(2/n) Σ errᵢ.</li>
<li><b>Update</b> m and b, repeat until the loss stops falling.</li>
</ol>
<p>For logistic regression the loss is log-loss, and the gradient turns out beautifully simple: Xᵀ(p − y)/n. Computing the gradient on a small random <b>mini-batch</b> instead of all the data is stochastic gradient descent (SGD).</p>
""", practice=["Mean Squared Error of a Line", "Gradient of the MSE", "Fit a Line by Gradient Descent", "One Step of Logistic Regression", "Mini-batch Gradient"])


@LD
def training_loop():
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array([3.1, 4.9, 7.2, 8.8, 11.1])
    m = b = 0.0
    losses = []
    for step in range(60):
        err = y - (m * x + b)
        losses.append((err ** 2).mean())
        m -= 0.02 * -2 * (x * err).mean()
        b -= 0.02 * -2 * err.mean()
    fig, (left, right) = plt.subplots(1, 2, figsize=(7, 2.8))
    left.plot(losses)
    left.set_title("loss falls", fontsize=9)
    left.set_xlabel("step")
    right.scatter(x, y)
    right.plot(x, m * x + b, color="#b45309")
    right.set_title(f"y = {m:.2f}x + {b:.2f}", fontsize=9)
    fig.tight_layout()


LESSON("Advanced", "Backpropagation, curvature and convexity", """
<p><b>Backpropagation</b> is the chain rule run backwards. For one neuron ŷ = σ(wx + b) with loss (ŷ − y)²:</p>
<pre><code class="py">dL/dŷ = 2(ŷ − y)
dŷ/dz = ŷ(1 − ŷ)          z = wx + b
dL/dw = dL/dŷ · dŷ/dz · x
dL/db = dL/dŷ · dŷ/dz · 1</code></pre>
<p>A deep network just has more links in the chain. Always <b>gradient-check</b> new code against a numerical derivative.</p>
<p>The <b>Hessian</b> (matrix of second derivatives) describes curvature. If its eigenvalues are all ≥ 0 the loss is <b>convex</b> — a single bowl with no false valleys, so descent always finds the best answer. Newton's method uses the Hessian to take smarter steps.</p>
""", practice=["Chain Rule Through a Computation", "Backpropagation Through One Neuron", "The Hessian Matrix", "Is the Bowl Convex?", "Bottom of a Quadratic Bowl", "Newton's Method for a Minimum"])


@LD
def backprop_demo():
    w, b, x, y = 0.5, 0.1, 2.0, 1.0
    z = w * x + b
    y_hat = 1 / (1 + math.exp(-z))
    loss = (y_hat - y) ** 2
    dL_dyhat = 2 * (y_hat - y)
    dyhat_dz = y_hat * (1 - y_hat)
    dL_dw = dL_dyhat * dyhat_dz * x
    dL_db = dL_dyhat * dyhat_dz
    w_new = w - 1.0 * dL_dw
    b_new = b - 1.0 * dL_db
    y_hat_new = 1 / (1 + math.exp(-(w_new * x + b_new)))
    loss_new = (y_hat_new - y) ** 2
