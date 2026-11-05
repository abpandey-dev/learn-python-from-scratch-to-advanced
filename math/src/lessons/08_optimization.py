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


LESSON("Basics", "Gradient by hand", """
<p>f(x, y) = x² + 3y², at the point (2, 1).</p>
<ol><li><b>Partial derivatives:</b> ∂f/∂x = 2x, treating y as fixed; ∂f/∂y = 6y, treating x as fixed.</li>
<li><b>At (2, 1):</b> ∇f = (4, 6).</li>
<li><b>Steepness:</b> ‖∇f‖ = √(16 + 36) = 7.21.</li>
<li><b>Steepest way up:</b> (4, 6) / 7.21 = (0.555, 0.832).</li>
<li><b>Steepest way down:</b> the opposite direction.</li></ol>
<h4>Check it with a tiny step</h4>
<p>f(2, 1) = 7. Move 0.01 in x: f(2.01, 1) = 7.0401. The rise of 0.0401 for a step of 0.01 gives a slope of about 4 ✓.</p>
<h4>Reading contours</h4>
<p>Contour lines join points of equal height, like a hiking map. Lines close together mean steep ground, and the gradient always crosses them at right angles. Walking along a contour keeps your height constant, so all the change is across it.</p>
""", practice=["Partial Derivatives", "The Gradient Vector", "Directional Derivative", "Steepest Downhill Direction"])


@LD
def gradient_by_hand():
    def f(x, y):
        return x ** 2 + 3 * y ** 2

    gradient = np.array([2 * 2, 6 * 1])
    size = np.linalg.norm(gradient)
    uphill = gradient / size
    tiny_step = (f(2.01, 1) - f(2, 1)) / 0.01
    other_direction = (f(2, 1.01) - f(2, 1)) / 0.01


LESSON("Core", "Gradient descent in 2-D, by hand", """
<p>Minimise f = x² + 3y² from (2, 1), with learning rate 0.1. The gradient is (2x, 6y).</p>
<table><tr><th>Step</th><th>Point</th><th>f</th><th>Gradient</th><th>Move = −0.1 × gradient</th></tr>
<tr><td>0</td><td>(2.000, 1.000)</td><td>7.000</td><td>(4, 6)</td><td>(−0.4, −0.6)</td></tr>
<tr><td>1</td><td>(1.600, 0.400)</td><td>3.040</td><td>(3.2, 2.4)</td><td>(−0.32, −0.24)</td></tr>
<tr><td>2</td><td>(1.280, 0.160)</td><td>1.715</td><td>(2.56, 0.96)</td><td>(−0.256, −0.096)</td></tr>
<tr><td>3</td><td>(1.024, 0.064)</td><td>1.061</td><td></td><td></td></tr></table>
<p>Notice two things:</p>
<ul><li><b>Steps shrink on their own</b>, as the gradient gets smaller near the bottom.</li>
<li><b>y falls faster than x,</b> because the bowl is steeper in y. Different steepness in different directions is why feature scaling speeds up training.</li></ul>
""", practice=["One Gradient-Descent Step", "Descent in a Long Narrow Valley", "Gradient of a Quadratic Form"])


@LD
def descent_table():
    point = np.array([2.0, 1.0])
    history = []
    for step in range(4):
        value = point[0] ** 2 + 3 * point[1] ** 2
        history.append((point.round(3).tolist(), round(float(value), 3)))
        gradient = np.array([2 * point[0], 6 * point[1]])
        point = point - 0.1 * gradient


LESSON("Core", "Exactly why learning rates fail", """
<p>For f(x) = x², one step gives x − η·2x = <b>(1 − 2η)·x</b>. So each step multiplies x by the same factor. Starting from x = 5:</p>
<table><tr><th>η</th><th>Factor</th><th>x after each step</th><th>Behaviour</th></tr>
<tr><td>0.1</td><td>0.8</td><td>4, 3.2, 2.56, 2.05</td><td>slow and steady</td></tr>
<tr><td>0.25</td><td>0.5</td><td>2.5, 1.25, 0.63, 0.31</td><td>faster</td></tr>
<tr><td>0.5</td><td>0</td><td>0, 0, 0, 0</td><td>exact in one step</td></tr>
<tr><td>1.0</td><td>−1</td><td>−5, 5, −5, 5</td><td>bounces forever</td></tr>
<tr><td>1.1</td><td>−1.2</td><td>−6, 7.2, −8.64, 10.37</td><td>explodes</td></tr></table>
<p>So it converges only if |1 − 2η| &lt; 1, meaning η &lt; 1.</p>
<h4>The narrow valley problem</h4>
<p>On a bowl with different steepness, the steepest direction limits η. Too large and that direction explodes. Small enough for it, and the gentle direction crawls. The ratio of steepest to gentlest curvature is the <b>condition number</b>. Scaling features makes it smaller, and momentum and Adam help too.</p>
""", practice=["Is the Learning Rate Too Big?", "Gradient Descent in 1-D"])


@LD
def rate_table():
    table = {}
    for eta in [0.1, 0.25, 0.5, 1.0, 1.1]:
        x = 5.0
        path = []
        for _ in range(4):
            x = (1 - 2 * eta) * x
            path.append(round(x, 2))
        table[eta] = path
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    for eta, path in table.items():
        ax.plot([5] + path, "o-", markersize=3, label=f"η = {eta}")
    ax.set_xlabel("step")
    ax.set_ylabel("x")
    ax.legend(fontsize=7)


LESSON("Advanced", "Training one point by hand", """
<p>Model ŷ = wx + b. With one example x = 2, y = 10, and current weights w = 3, b = 1.</p>
<h4>Forward</h4>
<p>ŷ = 3(2) + 1 = 7. Error ŷ − y = −3. Loss L = (−3)² = 9.</p>
<h4>Backward, with the chain rule</h4>
<ul><li>∂L/∂w = 2(ŷ − y) × x = 2(−3)(2) = <b>−12</b></li>
<li>∂L/∂b = 2(ŷ − y) × 1 = <b>−6</b></li></ul>
<p>Negative gradients say: raising the weights lowers the loss. Sensible, since the prediction is too low. w gets a bigger push because x = 2 multiplies its effect.</p>
<h4>Update with η = 0.01</h4>
<p>w = 3 + 0.12 = 3.12 and b = 1 + 0.06 = 1.06. Then ŷ = 7.3, and the loss falls from 9 to <b>7.29</b>.</p>
<p>For many examples, average these gradients over all of them (or over a mini-batch). That's all the training of linear regression is. A neural network just has a longer chain.</p>
""", practice=["Mean Squared Error of a Line", "Gradient of the MSE", "Fit a Line by Gradient Descent", "Chain Rule Through a Computation", "Backpropagation Through One Neuron", "Mini-batch Gradient", "One Step of Logistic Regression"])


@LD
def one_point_training():
    x, y, w, b = 2.0, 10.0, 3.0, 1.0
    prediction = w * x + b
    loss = (prediction - y) ** 2
    dL_dw = 2 * (prediction - y) * x
    dL_db = 2 * (prediction - y)
    w_new = w - 0.01 * dL_dw
    b_new = b - 0.01 * dL_db
    new_prediction = w_new * x + b_new
    new_loss = (new_prediction - y) ** 2


LESSON("Advanced", "Local minimums, saddles and convexity", """
<p>A flat point (∇f = 0) isn't always the bottom. The second derivatives tell them apart.</p>
<table><tr><th>Function</th><th>Hessian eigenvalues at (0, 0)</th><th>Type</th></tr>
<tr><td>x² + y²</td><td>2, 2 (all positive)</td><td>minimum</td></tr>
<tr><td>−x² − y²</td><td>−2, −2 (all negative)</td><td>maximum</td></tr>
<tr><td>x² − y²</td><td>2, −2 (mixed)</td><td><b>saddle</b></td></tr></table>
<h4>Starting point matters</h4>
<p>f(x) = x⁴ − 3x² + x has two valleys. The demo starts gradient descent from two points, and each one reaches a different valley, with different final values.</p>
<h4>Convex: the easy case</h4>
<p>A bowl with one bottom: any valley is the best one. Linear and logistic regression are convex, so they always reach the best answer.</p>
<p>Neural networks aren't convex, yet they train well in practice. In very high dimensions most flat points are saddles rather than bad valleys, and the noise from mini-batches helps escape them.</p>
""", practice=["The Hessian Matrix", "Is the Bowl Convex?", "Bottom of a Quadratic Bowl", "Newton's Method for a Minimum"])


@LD
def two_valleys():
    def f(x):
        return x ** 4 - 3 * x ** 2 + x

    def descend(x, steps=100, lr=0.01):
        path = [x]
        for _ in range(steps):
            x = x - lr * (4 * x ** 3 - 6 * x + 1)
            path.append(x)
        return np.array(path)

    left, right = descend(-0.2), descend(0.5)
    ends = (round(float(left[-1]), 3), round(float(f(left[-1])), 3), round(float(right[-1]), 3), round(float(f(right[-1])), 3))
    xs = np.linspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.plot(xs, f(xs), color="black")
    ax.plot(left, f(left), "o-", markersize=2, label="start at −0.2")
    ax.plot(right, f(right), "o-", markersize=2, label="start at 0.5")
    ax.legend(fontsize=7)
