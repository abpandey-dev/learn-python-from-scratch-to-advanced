from lib import *
import math
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPClassifier

GATE = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)

rng = np.random.default_rng(1)
angle = rng.uniform(0, 2 * np.pi, 120)
radius = np.r_[rng.normal(1, 0.15, 60), rng.normal(2.2, 0.2, 60)]
RINGS = np.column_stack([radius * np.cos(angle), radius * np.sin(angle)])
RING_LABELS = np.r_[np.zeros(60, dtype=int), np.ones(60, dtype=int)]

LESSON("Basics", "One neuron, then many", """
<p>A <b>neuron</b> is a weighted sum passed through a function: <b>output = activation(w·x + b)</b>. You've met it already: with a sigmoid it's logistic regression, and with a step it's the perceptron.</p>
<p>One neuron can only draw one straight line. It can do AND and OR, but not <b>XOR</b> (true when the inputs differ), because no single line separates those points.</p>
<p>The fix is to <b>stack neurons</b>. A hidden layer computes new features, such as OR and NAND, and the next layer combines them: XOR = AND(OR, NAND). A network is layers of neurons, each feeding the next.</p>
""", practice=["Logic Gates With One Neuron", "XOR Needs a Hidden Layer", "Count the Parameters"])


@LD
def gates_picture():
    fig, axes = plt.subplots(1, 3, figsize=(8, 2.6))
    tables = [("AND", [0, 0, 0, 1], (1, 1, -1.5)), ("OR", [0, 1, 1, 1], (1, 1, -0.5)), ("XOR: no single line", [0, 1, 1, 0], None)]
    xs = np.linspace(-0.5, 1.5, 10)
    for ax, (name, y, line) in zip(axes, tables):
        ax.scatter(GATE[:, 0], GATE[:, 1], c=y, cmap="coolwarm", s=90, edgecolor="black")
        if line:
            ax.plot(xs, -(line[0] * xs + line[2]) / line[1], color="black")
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 1.5)
        ax.set_title(name, fontsize=9)
    fig.tight_layout()


LESSON("Core", "Activations and the forward pass", """
<p>Without a non-linear <b>activation</b>, stacking layers is pointless, because a line of a line is still a line. The usual choices:</p>
<table><tr><th>Activation</th><th>Output</th><th>Slope</th><th>Where</th></tr>
<tr><td><b>ReLU</b> max(0, x)</td><td>0 … ∞</td><td>1 or 0</td><td>hidden layers (default)</td></tr>
<tr><td><b>tanh</b></td><td>−1 … 1</td><td>at most 1</td><td>some hidden layers</td></tr>
<tr><td><b>sigmoid</b></td><td>0 … 1</td><td>at most 0.25</td><td>output for yes/no</td></tr>
<tr><td><b>softmax</b></td><td>probabilities</td><td></td><td>output for many classes</td></tr>
<tr><td>identity</td><td>any number</td><td>1</td><td>output for regression</td></tr></table>
<p>The <b>forward pass</b> goes layer by layer: h = activation(W·x + b), then the output = W₂·h + b₂. Each row of W holds one neuron's weights.</p>
""", practice=["Activation Functions", "Slopes of the Activations", "Forward Pass With ReLU", "Forward Pass With tanh", "Classifier Output Layer"])


@LD
def activation_plots():
    x = np.linspace(-5, 5, 200)
    s = 1 / (1 + np.exp(-x))
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    left.plot(x, s, label="sigmoid")
    left.plot(x, np.tanh(x), label="tanh")
    left.plot(x, np.maximum(0, x), label="ReLU")
    left.set_ylim(-1.2, 3)
    left.legend(fontsize=7)
    left.set_title("activation", fontsize=9)
    right.plot(x, s * (1 - s), label="sigmoid′")
    right.plot(x, 1 - np.tanh(x) ** 2, label="tanh′")
    right.plot(x, (x > 0).astype(float), label="ReLU′")
    right.legend(fontsize=7)
    right.set_title("slope: sigmoid's is tiny far from 0", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Backpropagation", """
<p>Training needs the gradient of the loss with respect to <b>every</b> weight. <b>Backpropagation</b> gets them all at once using the chain rule:</p>
<ol>
<li><b>Forward</b>: compute and remember every layer's values.</li>
<li><b>Loss</b>: ½·mean(ŷ − y)² for regression, cross-entropy for classification.</li>
<li><b>Backward</b>: start from the error at the output and multiply by each layer's local derivative, moving back towards the input.</li>
<li><b>Update</b>: w ← w − learning_rate × gradient.</li>
</ol>
<p>The total cost is about the same as one forward pass, which is why networks with billions of weights can be trained at all. Check hand-written gradients against a numerical estimate.</p>
<p><b>Vanishing gradients</b>: multiplying many slopes below 1 shrinks the signal. With sigmoid, ten layers multiply by at most 0.25¹⁰ ≈ 0.000001. ReLU, careful initialisation and skip connections fix this.</p>
""", practice=["Regression Loss", "Cross-Entropy for a Batch", "Backpropagation Gradients", "One Training Step", "A Short Training Loop"])


@LD
def backprop_by_hand():
    w1, b1, w2, b2 = 0.5, 0.1, -0.6, 0.2
    x, y = 1.0, 1.0
    z = w1 * x + b1
    h = math.tanh(z)
    pred = w2 * h + b2
    loss = 0.5 * (pred - y) ** 2
    dL_dpred = pred - y
    dpred_dh = w2
    dh_dz = 1 - h ** 2
    dz_dw1 = x
    dL_dw1 = dL_dpred * dpred_dh * dh_dz * dz_dw1
    dL_dw2 = dL_dpred * h
    new_w1 = w1 - 0.1 * dL_dw1
    new_w2 = w2 - 0.1 * dL_dw2
    new_pred = new_w2 * math.tanh(new_w1 * x + b1) + b2
    new_loss = 0.5 * (new_pred - y) ** 2


LESSON("Advanced", "Optimisers and practical training", """
<p>Plain gradient descent is rarely used alone:</p>
<ul>
<li><b>Mini-batches</b>: compute each step's gradient on a small group (32–512 rows), which is cheaper, and the noise can help.</li>
<li><b>Momentum</b>: keep a running velocity, which smooths zig-zags in narrow valleys.</li>
<li><b>Adam</b>: momentum plus a separate step size for each weight. The usual default.</li>
</ul>
<p><b>Initialisation</b>: start with small random weights (never all zeros, or neurons stay identical). Glorot and He ranges keep signal sizes steady across layers.</p>
<p><b>Fighting overfitting</b>: <b>L2 / weight decay</b>, <b>dropout</b> (randomly silence neurons while training), <b>early stopping</b>, and more data. Always scale inputs.</p>
""", practice=["Momentum", "One Adam Update", "Mini-Batches", "Initialisation Range", "L2 Regularisation in a Network", "Dropout"])


@LD
def optimiser_paths():
    def run(mu, steps=40, lr=0.02):
        w, v = np.array([4.0, 1.5]), np.zeros(2)
        path = [w]
        for _ in range(steps):
            g = np.array([2 * w[0], 40 * w[1]])
            v = mu * v - lr * g
            w = w + v
            path.append(w)
        return np.array(path)

    grid = np.linspace(-5, 5, 80)
    xx, yy = np.meshgrid(grid, grid / 2.5)
    fig, ax = plt.subplots(figsize=(5, 2.9))
    ax.contour(xx, yy, xx ** 2 + 20 * yy ** 2, levels=12, alpha=0.5)
    for mu, colour, name in [(0.0, "#b45309", "plain"), (0.6, "#0f766e", "momentum 0.6")]:
        path = run(mu)
        ax.plot(path[:, 0], path[:, 1], "o-", markersize=2, color=colour, label=name)
    ax.legend(fontsize=7)


LESSON("Advanced", "A real network in scikit-learn", """
<p><code>MLPClassifier</code> and <code>MLPRegressor</code> train a multi-layer perceptron in a few lines. Watch <code>loss_curve_</code>: a smooth fall is healthy, spikes mean the learning rate is too high, and a flat line means it's too low or the inputs aren't scaled.</p>
<p>A hidden layer lets the network bend its boundary. With enough neurons it can approximate any reasonable function (the <b>universal approximation theorem</b>), though that says nothing about how easy it is to train or whether it generalises.</p>
<p><b>Where next:</b> for tables, gradient boosting usually wins. For images (CNNs), sequences and language (transformers), you need deep learning frameworks such as PyTorch. Their building blocks are exactly what you've built here.</p>
""", practice=["Learn XOR"])


@LD
def rings_boundary():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        net = MLPClassifier(hidden_layer_sizes=(12,), activation="tanh", solver="adam", learning_rate_init=0.02,
                            max_iter=300, random_state=0).fit(RINGS, RING_LABELS)
    grid = np.linspace(-3.2, 3.2, 120)
    xx, yy = np.meshgrid(grid, grid)
    prob = net.predict_proba(np.column_stack([xx.ravel(), yy.ravel()]))[:, 1].reshape(xx.shape)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3))
    left.contourf(xx, yy, prob, levels=10, cmap="coolwarm", alpha=0.5)
    left.scatter(RINGS[:, 0], RINGS[:, 1], c=RING_LABELS, cmap="coolwarm", s=10, edgecolor="black", linewidth=0.3)
    left.set_aspect("equal")
    left.set_title(f"accuracy {net.score(RINGS, RING_LABELS):.0%}", fontsize=9)
    right.plot(net.loss_curve_)
    right.set_title("training loss", fontsize=9)
    right.set_xlabel("epoch")
    fig.tight_layout()
