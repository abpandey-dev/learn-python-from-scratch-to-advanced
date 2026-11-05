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


LESSON("Basics", "A forward pass by hand", """
<p>A network with 2 inputs, 2 hidden ReLU neurons and 1 output. Input x = (2, 1).</p>
<h4>Hidden layer</h4>
<table><tr><th>Neuron</th><th>Weights</th><th>Bias</th><th>z = w·x + b</th><th>ReLU(z)</th></tr>
<tr><td>h₁</td><td>0.5, −1</td><td>0</td><td>0.5·2 − 1·1 + 0 = 0</td><td>0</td></tr>
<tr><td>h₂</td><td>1, 1</td><td>−1</td><td>1·2 + 1·1 − 1 = 2</td><td>2</td></tr></table>
<h4>Output</h4>
<p>Weights 1 and −0.5, bias 0.5: ŷ = 1·0 + (−0.5)·2 + 0.5 = <b>−0.5</b>.</p>
<h4>In matrix form</h4>
<pre><code class="py">h = np.maximum(0, W1 @ x + b1)
y = W2 @ h + b2</code></pre>
<p><b>Parameters here:</b> (2 × 2 + 2) + (2 × 1 + 1) = 9. Training just means finding good values for these 9 numbers.</p>
<p><b>What a hidden neuron does:</b> each ReLU acts like a hinge, flat on one side and sloped on the other. A network adds many hinges to build a curve from straight pieces.</p>
""", practice=["Forward Pass With ReLU", "Count the Parameters"])


@LD
def forward_by_hand():
    x = np.array([2.0, 1.0])
    W1 = np.array([[0.5, -1.0], [1.0, 1.0]])
    b1 = np.array([0.0, -1.0])
    z = W1 @ x + b1
    hidden = np.maximum(0, z)
    W2 = np.array([1.0, -0.5])
    b2 = 0.5
    output = W2 @ hidden + b2
    number_of_parameters = W1.size + b1.size + W2.size + 1


LESSON("Core", "Backpropagation with real numbers", """
<p>One input, one tanh neuron, one output: w₁ = 0.5, b = 0.1, w₂ = −0.6, b₂ = 0.2. The example is x = 1, y = 1.</p>
<h4>Forward: store every value</h4>
<table><tr><th>Quantity</th><th>Calculation</th><th>Value</th></tr>
<tr><td>z</td><td>0.5 × 1 + 0.1</td><td>0.600</td></tr>
<tr><td>h</td><td>tanh(0.6)</td><td>0.537</td></tr>
<tr><td>ŷ</td><td>−0.6 × 0.537 + 0.2</td><td>−0.122</td></tr>
<tr><td>Loss</td><td>½(−0.122 − 1)²</td><td>0.630</td></tr></table>
<h4>Backward: multiply local slopes</h4>
<table><tr><th>Slope</th><th>Formula</th><th>Value</th></tr>
<tr><td>dL/dŷ</td><td>ŷ − y</td><td>−1.122</td></tr>
<tr><td>dŷ/dh</td><td>w₂</td><td>−0.6</td></tr>
<tr><td>dh/dz</td><td>1 − h²</td><td>0.712</td></tr>
<tr><td>dz/dw₁</td><td>x</td><td>1</td></tr></table>
<ul><li>dL/dw₁ = (−1.122)(−0.6)(0.712)(1) = <b>0.479</b></li>
<li>dL/dw₂ = (ŷ − y) × h = (−1.122)(0.537) = <b>−0.603</b></li></ul>
<h4>Update with learning rate 0.1</h4>
<p>w₁ = 0.5 − 0.1 × 0.479 = 0.452, and w₂ = −0.6 + 0.0603 = −0.540. The new prediction is −0.071, and the loss falls from 0.630 to <b>0.574</b>.</p>
<p><b>Why it's efficient:</b> dL/dŷ and dŷ/dh are shared by everything earlier in the network. Computing backwards reuses them instead of repeating that work for each weight.</p>
""", practice=["Backpropagation Gradients", "One Training Step"])


@LD
def backprop_numbers():
    w1, b, w2, b2 = 0.5, 0.1, -0.6, 0.2
    x, y = 1.0, 1.0
    z = w1 * x + b
    h = math.tanh(z)
    pred = w2 * h + b2
    loss = 0.5 * (pred - y) ** 2
    dL_dpred = pred - y
    dh_dz = 1 - h ** 2
    dL_dw1 = dL_dpred * w2 * dh_dz * x
    dL_dw2 = dL_dpred * h
    new_w1 = w1 - 0.1 * dL_dw1
    new_w2 = w2 - 0.1 * dL_dw2
    new_pred = new_w2 * math.tanh(new_w1 * x + b) + b2
    new_loss = 0.5 * (new_pred - y) ** 2


LESSON("Core", "How hidden neurons build curves", """
<p>A single tanh or ReLU neuron makes one bend. Add more neurons and the network adds more bends. The demo fits a wavy curve with 1, 3 and 20 hidden neurons.</p>
<ul><li><b>1 neuron:</b> one bend; it underfits.</li>
<li><b>3 neurons:</b> follows the main shape.</li>
<li><b>20 neurons:</b> follows it closely.</li></ul>
<h4>Wider or deeper?</h4>
<p>One hidden layer can in principle approximate any smooth function, if it's wide enough. In practice, <b>depth</b> is more efficient: layers reuse each other's features. In images, for example, edges combine into shapes and then objects.</p>
<h4>How big should it be?</h4>
<ol><li>Start small: one or two hidden layers of 32–128 neurons for tables.</li>
<li>Check that it can overfit a tiny sample. If it can't, there's a bug or the learning rate is wrong.</li>
<li>Grow until validation stops improving, then regularise.</li></ol>
""", practice=["XOR Needs a Hidden Layer", "Forward Pass With tanh", "Activation Functions"])


@LD
def neurons_fit_curve():
    from sklearn.neural_network import MLPRegressor
    x = np.linspace(-3, 3, 120).reshape(-1, 1)
    y = np.sin(2 * x.ravel()) + 0.3 * x.ravel()
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.5), sharey=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for ax, size in zip(axes, [1, 3, 20]):
            net = MLPRegressor(hidden_layer_sizes=(size,), activation="tanh", solver="lbfgs", max_iter=3000, random_state=0).fit(x, y)
            ax.plot(x, y, color="gray", label="target")
            ax.plot(x, net.predict(x), color="#b45309", label="network")
            ax.set_title(f"{size} hidden neuron(s)", fontsize=8)
    axes[0].legend(fontsize=7)
    fig.tight_layout()


LESSON("Core", "Momentum and Adam by hand", """
<h4>Momentum</h4>
<p>Minimise f(w) = w² from w = 5, with learning rate 0.1 and μ = 0.9. The slope is 2w.</p>
<table><tr><th>Step</th><th>Plain gradient descent</th><th>With momentum</th></tr>
<tr><td>1</td><td>4.00</td><td>v = −1, w = 4.00</td></tr>
<tr><td>2</td><td>3.20</td><td>v = 0.9(−1) − 0.8 = −1.7, w = 2.30</td></tr>
<tr><td>3</td><td>2.56</td><td>v = 0.9(−1.7) − 0.46 = −1.99, w = 0.31</td></tr>
<tr><td>4</td><td>2.05</td><td>v = 0.9(−1.99) − 0.062 = −1.853, w = −1.54</td></tr></table>
<p>Momentum moves much faster, then overshoots, like a heavy ball. It helps in narrow valleys where the zig-zags cancel out.</p>
<h4>Adam: one step at a time</h4>
<p>From w = 1 with learning rate 0.1:</p>
<table><tr><th>Step</th><th>Gradient</th><th>m̂ (average gradient)</th><th>v̂ (average squared)</th><th>New w</th></tr>
<tr><td>1</td><td>2.0</td><td>2.0</td><td>4.0</td><td>1 − 0.1 × 2 / 2 = 0.9</td></tr>
<tr><td>2</td><td>1.8</td><td>1.895</td><td>3.62</td><td>0.9 − 0.1 × 1.895 / 1.903 = 0.8</td></tr></table>
<p>Dividing by √v̂ makes the step about the size of the learning rate, <b>whatever the gradient's scale</b>. That's why Adam needs less tuning. A sensible default learning rate is 0.001.</p>
""", practice=["Momentum", "One Adam Update"])


@LD
def momentum_vs_plain():
    def run(mu, steps=40, lr=0.1):
        w, v, path = 5.0, 0.0, []
        for _ in range(steps):
            v = mu * v - lr * 2 * w
            w = w + v
            path.append(w)
        return path

    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.plot(run(0.0), label="plain")
    ax.plot(run(0.5), label="momentum 0.5")
    ax.plot(run(0.9), label="momentum 0.9")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlabel("step")
    ax.set_ylabel("w")
    ax.legend(fontsize=7)


LESSON("Advanced", "Vanishing gradients", """
<p>Backprop multiplies a slope per layer. Sigmoid's slope is at most 0.25, so the signal shrinks quickly:</p>
<table><tr><th>Layers</th><th>2</th><th>5</th><th>10</th></tr>
<tr><th>Largest possible factor (0.25ⁿ)</th><td>0.0625</td><td>0.00098</td><td>0.00000095</td></tr></table>
<p>Early layers then learn almost nothing. The demo pushes a real signal through 10 layers and shows the gradient at each one.</p>
<h4>The fixes</h4>
<table><tr><th>Fix</th><th>How it helps</th></tr>
<tr><td>ReLU</td><td>slope 1 for active neurons</td></tr>
<tr><td>Good initialisation (He, Glorot)</td><td>keeps signals a steady size</td></tr>
<tr><td>Normalisation layers</td><td>keep each layer's inputs in a healthy range</td></tr>
<tr><td>Skip connections (ResNet, transformers)</td><td>give gradients a direct path back</td></tr></table>
<p><b>Exploding gradients</b> are the opposite problem: slopes above 1 multiply until the loss becomes NaN. Use gradient clipping and a lower learning rate.</p>
""", practice=["Slopes of the Activations", "Initialisation Range"])


@LD
def gradient_by_layer():
    r = np.random.default_rng(0)
    layers, width = 10, 64

    def run(activation, slope, weight_std):
        x = r.normal(size=(128, width))
        weights = [r.normal(0, weight_std, (width, width)) for _ in range(layers)]
        cache = []
        for W in weights:
            z = x @ W
            cache.append((W, slope(z)))
            x = activation(z)
        grad = np.ones_like(x)
        sizes = []
        for W, s in reversed(cache):
            grad = (grad * s) @ W.T
            sizes.append(np.abs(grad).mean())
        return sizes[::-1]

    sigmoid = run(lambda z: 1 / (1 + np.exp(-z)), lambda z: np.exp(-z) / (1 + np.exp(-z)) ** 2, 1 / math.sqrt(width))
    relu = run(lambda z: np.maximum(0, z), lambda z: (z > 0).astype(float), math.sqrt(2 / width))
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    ax.semilogy(range(1, layers + 1), sigmoid, "o-", label="sigmoid")
    ax.semilogy(range(1, layers + 1), relu, "o-", label="ReLU with He initialisation")
    ax.set_xlabel("layer (1 = nearest the input)")
    ax.set_ylabel("average gradient size")
    ax.legend(fontsize=7)


LESSON("Advanced", "Debugging a network that won't learn", """
<table><tr><th>Loss curve</th><th>Likely cause</th><th>Fix</th></tr>
<tr><td>Explodes or becomes NaN</td><td>learning rate too high</td><td>divide it by 10; check for bad inputs</td></tr>
<tr><td>Flat from the start</td><td>rate too low, unscaled inputs, or a bug</td><td>scale inputs; try overfitting a tiny batch</td></tr>
<tr><td>Falls, then jumps around</td><td>rate too high near the minimum</td><td>use a schedule to lower it</td></tr>
<tr><td>Train falls, validation rises</td><td>overfitting</td><td>weight decay, dropout, early stopping, more data</td></tr></table>
<h4>The checklist, in order</h4>
<ol><li>Is the starting loss about what you'd expect? For k equal classes it's near ln k.</li>
<li>Can it overfit 10 rows? If not, there's a bug.</li>
<li>Are inputs scaled, and are labels aligned with rows?</li>
<li>Find a learning rate: try 0.1, 0.01, 0.001.</li>
<li>Only then add regularisation and size.</li></ol>
<p><b>Common bugs:</b> softmax applied before a loss that expects raw scores, forgetting to clear gradients in PyTorch, leaving dropout on during evaluation.</p>
""", practice=["A Short Training Loop", "Regression Loss", "Cross-Entropy for a Batch", "L2 Regularisation in a Network", "Dropout", "Mini-Batches"])


@LD
def learning_rate_curves():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, ax = plt.subplots(figsize=(4.8, 2.9))
        for lr in [0.0005, 0.5, 20.0]:
            net = MLPClassifier(hidden_layer_sizes=(12,), activation="tanh", solver="sgd", momentum=0.0, learning_rate_init=lr,
                                max_iter=120, tol=0, n_iter_no_change=1000, random_state=0).fit(RINGS, RING_LABELS)
            ax.plot(net.loss_curve_, label=f"learning rate {lr}")
    ax.set_xlabel("epoch")
    ax.set_ylabel("training loss")
    ax.legend(fontsize=7)


LESSON("Advanced", "A whole network from scratch", """
<p>Everything comes together here, in about 20 lines of NumPy and no framework. The demo trains on the rings dataset:</p>
<ol><li><b>Initialise</b> with small random weights.</li>
<li><b>Forward:</b> h = tanh(X·W₁ + b₁), then p = σ(h·W₂ + b₂).</li>
<li><b>Loss:</b> binary cross-entropy.</li>
<li><b>Backward:</b> the output's error p − y flows back through W₂, then through the slope of tanh, into W₁.</li>
<li><b>Update:</b> every weight moves against its gradient.</li>
<li>Repeat, recording the loss.</li></ol>
<p>Compare the code with sklearn's <code>MLPClassifier</code> in the earlier lesson. PyTorch adds automatic gradients, GPU speed and ready-made layers, but this loop of forward, loss, backward and update is what every deep learning model does, including the largest language models.</p>
""", practice=["Learn XOR", "One Training Step"])


@LD
def network_from_scratch():
    r = np.random.RandomState(0)
    X, y = RINGS, RING_LABELS.astype(float)
    W1, b1 = r.normal(0, 0.5, (2, 10)), np.zeros(10)
    W2, b2 = r.normal(0, 0.5, 10), 0.0
    losses = []
    for step in range(1500):
        h = np.tanh(X @ W1 + b1)
        p = 1 / (1 + np.exp(-(h @ W2 + b2)))
        losses.append(-(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9)).mean())
        error = p - y
        slope_h = error[:, None] * W2 * (1 - h ** 2)
        W2 -= 0.5 * h.T @ error / len(y)
        b2 -= 0.5 * error.mean()
        W1 -= 0.5 * X.T @ slope_h / len(y)
        b1 -= 0.5 * slope_h.mean(axis=0)
    accuracy = ((p >= 0.5) == y).mean()
    grid = np.linspace(-3.2, 3.2, 100)
    xx, yy = np.meshgrid(grid, grid)
    points = np.column_stack([xx.ravel(), yy.ravel()])
    surface = 1 / (1 + np.exp(-(np.tanh(points @ W1 + b1) @ W2 + b2)))
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3))
    left.contourf(xx, yy, surface.reshape(xx.shape), levels=10, cmap="coolwarm", alpha=0.5)
    left.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=10, edgecolor="black", linewidth=0.3)
    left.set_aspect("equal")
    left.set_title(f"from scratch: accuracy {accuracy:.0%}", fontsize=9)
    right.plot(losses)
    right.set_xlabel("step")
    right.set_title("loss", fontsize=9)
    fig.tight_layout()
