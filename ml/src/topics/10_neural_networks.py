from lib import *
import math
import warnings
import numpy as np
from scipy.special import softmax as scipy_softmax
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.metrics import log_loss, mean_squared_error
from sklearn.utils import gen_batches


TOPIC(
    id="neural-networks", title="Neural Networks", glyph="○→○→○",
    blurb="From one neuron to a trained network: logic gates, why XOR needs a hidden layer, activations, forward passes, loss functions, backpropagation, SGD, momentum and Adam, initialisation, dropout and mini-batches.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">model = MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu", solver="adam",
                      alpha=1e-4, learning_rate_init=1e-3, max_iter=500, early_stopping=True)
model.fit(X_train, y_train)            # scale X first!
model.coefs_, model.intercepts_, model.loss_curve_
# one layer:   h = activation(W @ x + b)
# one step:    w = w - learning_rate * gradient
# backprop:    multiply local derivatives from the output back to each weight</code></pre>
<p>scikit-learn's MLP is good for learning and small tables. For images, text and large models, use PyTorch.</p>
""")

ACT = {"tanh": np.tanh, "relu": lambda z: np.maximum(0, z), "logistic": lambda z: 1 / (1 + np.exp(-z))}


def mlp_with_weights(W1, b1, W2, b2, activation):
    """A fitted MLPRegressor whose weights are replaced by ours. W rows hold one neuron each; sklearn stores the transpose."""
    W1, W2 = np.array(W1, dtype=float), np.array(W2, dtype=float)
    d, h, k = W1.shape[1], W1.shape[0], W2.shape[0]
    y = np.zeros(2) if k == 1 else np.zeros((2, k))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        net = MLPRegressor(hidden_layer_sizes=(h,), activation=activation, max_iter=1, random_state=0).fit(np.zeros((2, d)), y)
    net.coefs_ = [W1.T, W2.T]
    net.intercepts_ = [np.array(b1, dtype=float), np.array(b2, dtype=float)]
    return net


def sgd_net(W1, b1, W2, b2, X, y, lr):
    """sklearn MLP set up for plain full-batch gradient descent, starting from our weights."""
    net = MLPRegressor(hidden_layer_sizes=(len(W1),), activation="tanh", solver="sgd", learning_rate_init=lr,
                       momentum=0.0, alpha=0.0, batch_size=len(X), shuffle=False, random_state=0)
    net.partial_fit(X, y)  # builds the network and optimizer; overwrite in place so the optimizer keeps its references
    net.coefs_[0][:] = np.array(W1, dtype=float).T
    net.coefs_[1][:] = np.array(W2, dtype=float).T
    net.intercepts_[0][:] = b1
    net.intercepts_[1][:] = b2
    return net


def gd_step(W1, b1, W2, b2, X, y, lr):
    """One full-batch gradient step on ½·mean(ŷ − y)² for a tanh hidden layer and one linear output, by backprop."""
    n = len(X)
    h1 = X @ W1.T + b1
    a1 = np.tanh(h1)
    pred = (a1 @ W2.T + b2).ravel()
    err = pred - y
    dW2 = (a1.T @ err / n).reshape(1, -1)
    db2 = err.mean(keepdims=True)
    da = err[:, None] @ W2 * (1 - a1 ** 2)
    dW1 = (da.T @ X) / n
    db1 = da.mean(axis=0)
    return W1 - lr * dW1, b1 - lr * db1, W2 - lr * dW2, b2 - lr * db2


W1T = [[0.5, -0.2], [0.1, 0.4]]
B1T = [0.1, -0.1]
W2T = [[0.3, -0.6]]
B2T = [0.2]
XT = [[1.0, 2.0], [0.0, 1.0], [2.0, 0.0], [1.0, 1.0]]
YT = [1.0, 0.0, 1.0, 0.5]
GATE = [[0, 0], [0, 1], [1, 0], [1, 1]]


Q(None, "Logic Gates With One Neuron", "Easy", "Weights decide the rule",
  "A neuron outputs 1 when w·x + b ≥ 0, else 0. Return its output for every row.",
  [((GATE, [1, 1], -1.5), [0, 0, 0, 1]), ((GATE, [1, 1], -0.5), [0, 1, 1, 1]), (([[0], [1]], [-1], 0.5), [1, 0])],
  ("Score each row in a loop, compare with 0.", "O(n·d)", "O(n)"),
  ("Vectorised: <code>(X @ w + b >= 0).astype(int)</code>.", "O(n·d)", "O(n)"),
  names=["X", "w", "b"])


@B
def neuron(X, w, b):
    out = []
    for row in X:
        z = b + sum(wi * xi for wi, xi in zip(w, row))
        out.append(1 if z >= 0 else 0)
    return out


@O
def neuron(X, w, b):
    return (np.array(X) @ np.array(w) + b >= 0).astype(int)


Q(None, "XOR Needs a Hidden Layer", "Medium", "Stacking neurons",
  "No single line separates XOR. Build it from gates: h₁ = OR, h₂ = NAND, output = AND(h₁, h₂). Return the output for every row.",
  [((GATE,), [0, 1, 1, 0])],
  ("Compute each gate as a separate neuron, row by row.", "O(n)", "O(n)"),
  ("Two matrix layers: <code>H = (X @ W1 + b1 >= 0)</code>, then <code>(H @ W2 + b2 >= 0)</code>.", "O(n)", "O(n)"))


@B
def xor_net(X):
    out = []
    for a, b in X:
        h1 = 1 if a + b - 0.5 >= 0 else 0
        h2 = 1 if -a - b + 1.5 >= 0 else 0
        out.append(1 if h1 + h2 - 1.5 >= 0 else 0)
    return out


@O
def xor_net(X):
    W1 = np.array([[1, 1], [-1, -1]])
    b1 = np.array([-0.5, 1.5])
    H = (np.array(X) @ W1.T + b1 >= 0).astype(int)
    return (H @ np.array([1, 1]) - 1.5 >= 0).astype(int)


Q(None, "Activation Functions", "Easy", "Sigmoid, tanh, ReLU",
  "Return (sigmoid(x), tanh(x), ReLU(x)) for each x, rounded to 4 decimals.",
  [(([-2, 0, 1.5],), [(0.1192, -0.964, 0.0), (0.5, 0.0, 0.0), (0.8176, 0.9051, 1.5)])],
  ("Formulas with <code>math.exp</code> in a loop.", "O(n)", "O(n)"),
  ("NumPy on the whole array.", "O(n)", "O(n)"))


@B
def activations(xs):
    out = []
    for x in xs:
        s = 1 / (1 + math.exp(-x))
        t = (math.exp(x) - math.exp(-x)) / (math.exp(x) + math.exp(-x))
        out.append((round(s, 4), round(t, 4) + 0.0, round(max(0.0, x), 4)))
    return out


@O
def activations(xs):
    x = np.array(xs, dtype=float)
    table = np.column_stack([1 / (1 + np.exp(-x)), np.tanh(x), np.maximum(0, x)]).round(4) + 0.0
    return [tuple(row) for row in table.tolist()]


Q(None, "Slopes of the Activations", "Medium", "Why sigmoids make gradients vanish",
  "Return (σ′(x), tanh′(x), ReLU′(x)) for each x ≠ 0, rounded to 4 decimals.",
  [(([-3, 0.5, 2],), [(0.0452, 0.0099, 0.0), (0.235, 0.7864, 1.0), (0.105, 0.0707, 1.0)])],
  ("Numerical central difference of each function.", "O(n)", "O(n)"),
  ("Exact: σ(1 − σ), 1 − tanh², and 1 for x &gt; 0 else 0.", "O(n)", "O(n)"))


@B
def slopes(xs):
    fns = [lambda z: 1 / (1 + math.exp(-z)), math.tanh, lambda z: max(0.0, z)]
    h = 1e-5
    return [tuple(round((f(x + h) - f(x - h)) / (2 * h), 4) for f in fns) for x in xs]


@O
def slopes(xs):
    x = np.array(xs, dtype=float)
    s = 1 / (1 + np.exp(-x))
    table = np.column_stack([s * (1 - s), 1 - np.tanh(x) ** 2, (x > 0).astype(float)]).round(4)
    return [tuple(row) for row in table.tolist()]


Q(None, "Count the Parameters", "Easy", "Weights + biases",
  "A fully connected network has the given layer sizes, e.g. [3, 4, 2]. Return its number of parameters.",
  [(([3, 4, 2],), 26), (([2, 5, 5, 1],), 51)],
  ("Each layer has inputs × outputs weights plus one bias per output.", "O(layers)", "O(1)"),
  ("Build an <code>MLPRegressor</code> with those sizes and add up the sizes of <code>coefs_</code> and <code>intercepts_</code>.", "O(params)", "O(params)"))


@B
def count_params(sizes):
    total = 0
    for a, b in zip(sizes, sizes[1:]):
        total += a * b + b
    return total


@O
def count_params(sizes):
    d, hidden, k = sizes[0], tuple(sizes[1:-1]), sizes[-1]
    y = np.zeros(2) if k == 1 else np.zeros((2, k))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        net = MLPRegressor(hidden_layer_sizes=hidden, max_iter=1, random_state=0).fit(np.zeros((2, d)), y)
    return int(sum(c.size for c in net.coefs_) + sum(b.size for b in net.intercepts_))


Q(None, "Forward Pass With ReLU", "Medium", "Input → hidden → output",
  "Compute W2·ReLU(W1·x + b1) + b2 for each row of X (each row of W is one neuron). Round to 4 decimals.",
  [((W1T, B1T, W2T, B2T, XT), [-0.22, 0.02, 0.47, 0.08])],
  ("Loops over rows and neurons, one layer at a time.", "O(n·params)", "O(h)"),
  ("Put our weights in an <code>MLPRegressor</code> and call <code>predict</code>.", "O(n·params)", "O(n·h)"),
  names=["W1", "b1", "W2", "b2", "X"])


@B
def forward_relu(W1, b1, W2, b2, X):
    out = []
    for row in X:
        hidden = []
        for w, b in zip(W1, b1):
            hidden.append(max(0.0, b + sum(wi * xi for wi, xi in zip(w, row))))
        out.append(round(b2[0] + sum(wi * h for wi, h in zip(W2[0], hidden)), 4))
    return out


@O
def forward_relu(W1, b1, W2, b2, X):
    return mlp_with_weights(W1, b1, W2, b2, "relu").predict(X).round(4)


Q(None, "Forward Pass With tanh", "Medium", "Same network, different bend",
  "Compute W2·tanh(W1·x + b1) + b2 for each row of X. Round to 4 decimals.",
  [((W1T, B1T, W2T, B2T, XT), [-0.1392, -0.0047, 0.3803, 0.086])],
  ("NumPy matrix products, layer by layer.", "O(n·params)", "O(n·h)"),
  ("<code>MLPRegressor(activation='tanh')</code> holding our weights.", "O(n·params)", "O(n·h)"),
  names=["W1", "b1", "W2", "b2", "X"])


@B
def forward_tanh(W1, b1, W2, b2, X):
    hidden = np.tanh(np.array(X) @ np.array(W1).T + np.array(b1))
    return (hidden @ np.array(W2).T + np.array(b2)).ravel().round(4)


@O
def forward_tanh(W1, b1, W2, b2, X):
    return mlp_with_weights(W1, b1, W2, b2, "tanh").predict(X).round(4)


Q(None, "Classifier Output Layer", "Easy", "Softmax, then pick the winner",
  "For each row of raw output scores return (probabilities rounded to 4 decimals, predicted class).",
  [(([[2.0, 1.0, 0.1], [-1.0, 3.0, 0.0]],), [([0.659, 0.2424, 0.0986], 0), ([0.0171, 0.9362, 0.0466], 1)])],
  ("Exponentiate after subtracting the max, divide by the sum, find the largest.", "O(n·k)", "O(k)"),
  ("<code>scipy.special.softmax(z, axis=1)</code> and <code>argmax</code>.", "O(n·k)", "O(n·k)"))


@B
def output_layer(scores):
    out = []
    for row in scores:
        top = max(row)
        e = [math.exp(v - top) for v in row]
        p = [round(v / sum(e), 4) for v in e]
        out.append((p, p.index(max(p))))
    return out


@O
def output_layer(scores):
    p = scipy_softmax(np.array(scores, dtype=float), axis=1)
    return [(row.round(4).tolist(), int(row.argmax())) for row in p]


Q(None, "Regression Loss", "Easy", "½ · mean squared error",
  "Return ½·mean((ŷ − y)²), the loss sklearn's MLP minimises, rounded to 4 decimals. The ½ cancels when differentiating.",
  [(([1.0, 2.0, 3.0], [1.5, 2.0, 2.0]), 0.2083)],
  ("Loop of squared differences.", "O(n)", "O(1)"),
  ("<code>mean_squared_error(y, pred) / 2</code>.", "O(n)", "O(1)"),
  names=["y", "pred"])


@B
def half_mse(y, pred):
    return round(sum((a - b) ** 2 for a, b in zip(y, pred)) / (2 * len(y)), 4)


@O
def half_mse(y, pred):
    return round(mean_squared_error(y, pred) / 2, 4)


Q(None, "Cross-Entropy for a Batch", "Easy", "The classifier's loss",
  "Rows of P hold class probabilities and y holds the true class. Return the mean of −ln P[true class], rounded to 4 decimals.",
  [(([0, 1], [[0.8, 0.2], [0.3, 0.7]]), 0.2899)],
  ("Look up the true class's probability in each row.", "O(n)", "O(1)"),
  ("<code>log_loss(y, P)</code>.", "O(n·k)", "O(1)"),
  names=["y", "P"])


@B
def batch_ce(y, P):
    return round(sum(-math.log(row[c]) for c, row in zip(y, P)) / len(y), 4)


@O
def batch_ce(y, P):
    return round(log_loss(y, P, labels=list(range(len(P[0])))), 4)


Q(None, "Backpropagation Gradients", "Hard", "The chain rule, layer by layer",
  "For a tanh hidden layer and one linear output with loss ½·mean((ŷ − y)²), return the gradient with respect to W2's weights, rounded to 4 decimals.",
  [((W1T, B1T, W2T, B2T, XT, YT), [-0.2194, -0.2442])],
  ("Nudge each weight a little and watch the loss (numerical gradient).", "O(params·n)", "O(1)"),
  ("Backprop: the error times each hidden activation, averaged over rows.", "O(n·params)", "O(n·h)"),
  names=["W1", "b1", "W2", "b2", "X", "y"])


@B
def backprop_w2(W1, b1, W2, b2, X, y):
    def loss(w2):
        total = 0
        for row, target in zip(X, y):
            hidden = [math.tanh(b + sum(a * c for a, c in zip(w, row))) for w, b in zip(W1, b1)]
            pred = b2[0] + sum(a * c for a, c in zip(w2, hidden))
            total += (pred - target) ** 2
        return total / (2 * len(X))

    h = 1e-6
    grads = []
    for j in range(len(W2[0])):
        up, down = list(W2[0]), list(W2[0])
        up[j] += h
        down[j] -= h
        grads.append(round((loss(up) - loss(down)) / (2 * h), 4))
    return grads


@O
def backprop_w2(W1, b1, W2, b2, X, y):
    hidden = np.tanh(np.array(X) @ np.array(W1).T + np.array(b1))
    err = (hidden @ np.array(W2).T + np.array(b2)).ravel() - np.array(y)
    return (hidden.T @ err / len(X)).round(4)


Q(None, "One Training Step", "Hard", "Backprop + gradient descent",
  "Take one full-batch gradient step with learning rate lr. Return the network's predictions on X afterwards, rounded to 4 decimals.",
  [((W1T, B1T, W2T, B2T, XT, YT, 0.1), [-0.0077, 0.0908, 0.5114, 0.212]), ((W1T, B1T, W2T, B2T, XT, YT, 0.5), [0.5443, 0.4689, 0.9879, 0.7052])],
  ("Forward pass, backward pass by hand for all four weight arrays, update, forward again.", "O(n·params)", "O(n·h)"),
  ("<code>MLPRegressor(solver='sgd', momentum=0, alpha=0, batch_size=n)</code> starting from our weights; one <code>partial_fit</code>.", "O(n·params)", "O(n·h)"),
  names=["W1", "b1", "W2", "b2", "X", "y", "lr"])


@B
def one_step(W1, b1, W2, b2, X, y, lr):
    X, y = np.array(X), np.array(y)
    W1, b1, W2, b2 = gd_step(np.array(W1), np.array(b1), np.array(W2), np.array(b2), X, y, lr)
    return (np.tanh(X @ W1.T + b1) @ W2.T + b2).ravel().round(4)


@O
def one_step(W1, b1, W2, b2, X, y, lr):
    net = sgd_net(W1, b1, W2, b2, X, y, lr)
    net.partial_fit(X, y)
    return net.predict(X).round(4)


Q(None, "A Short Training Loop", "Hard", "Watch the loss fall",
  "Run n full-batch steps (learning rate 0.1) and return ½·mean((ŷ − y)²) after each one, rounded to 4 decimals.",
  [((W1T, B1T, W2T, B2T, XT, YT, 5), [0.1682, 0.1276, 0.1017, 0.0851, 0.0745])],
  ("Repeat the hand-written step and measure the loss.", "O(steps·n·params)", "O(steps)"),
  ("Repeat <code>partial_fit</code> on the sklearn network and measure its predictions.", "O(steps·n·params)", "O(steps)"),
  names=["W1", "b1", "W2", "b2", "X", "y", "n"])


@B
def training_loop(W1, b1, W2, b2, X, y, n):
    X, y = np.array(X), np.array(y)
    W1, b1, W2, b2 = np.array(W1), np.array(b1), np.array(W2), np.array(b2)
    losses = []
    for _ in range(n):
        W1, b1, W2, b2 = gd_step(W1, b1, W2, b2, X, y, 0.1)
        pred = (np.tanh(X @ W1.T + b1) @ W2.T + b2).ravel()
        losses.append(round(float(((pred - y) ** 2).mean() / 2), 4))
    return losses


@O
def training_loop(W1, b1, W2, b2, X, y, n):
    net = sgd_net(W1, b1, W2, b2, X, y, 0.1)
    losses = []
    for _ in range(n):
        net.partial_fit(X, y)
        losses.append(round(mean_squared_error(y, net.predict(X)) / 2, 4))
    return losses


Q(None, "Momentum", "Medium", "Build up speed",
  "Minimise f(w) = w² with v ← μ·v − lr·f′(w), w ← w + v, starting at v = 0. Return w after each step, rounded to 4 decimals.",
  [((5.0, 0.1, 0.9, 4), [4.0, 2.3, 0.31, -1.543]), ((5.0, 0.1, 0.0, 3), [4.0, 3.2, 2.56])],
  ("Plain Python loop.", "O(steps)", "O(steps)"),
  ("Treat (w, v) as a vector: each step multiplies it by the same 2 × 2 matrix.", "O(steps)", "O(steps)"),
  names=["w", "lr", "mu", "steps"])


@B
def momentum(w, lr, mu, steps):
    v = 0.0
    out = []
    for _ in range(steps):
        v = mu * v - lr * 2 * w
        w = w + v
        out.append(round(w, 4))
    return out


@O
def momentum(w, lr, mu, steps):
    A = np.array([[1 - 2 * lr, mu], [-2 * lr, mu]])
    state = np.array([w, 0.0])
    out = []
    for _ in range(steps):
        state = A @ state
        out.append(round(state[0], 4))
    return out


Q(None, "One Adam Update", "Hard", "Adaptive step sizes",
  "Apply t steps of Adam (β₁ = 0.9, β₂ = 0.999, ε = 1e-8, learning rate lr) to f(w) = Σwᵢ² from the given weights. Return the weights, rounded to 4 decimals.",
  [(([1.0, -2.0], 0.1, 3), [0.7016, -1.7006])],
  ("Track m and v for each weight in lists, with bias correction.", "O(t·d)", "O(d)"),
  ("The same update as NumPy array operations — each weight gets its own step size.", "O(t·d)", "O(d)"),
  names=["w", "lr", "t"])


@B
def adam(w, lr, t):
    w = list(w)
    m, v = [0.0] * len(w), [0.0] * len(w)
    for step in range(1, t + 1):
        for i in range(len(w)):
            g = 2 * w[i]
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g * g
            mh = m[i] / (1 - 0.9 ** step)
            vh = v[i] / (1 - 0.999 ** step)
            w[i] -= lr * mh / (math.sqrt(vh) + 1e-8)
    return [round(x, 4) for x in w]


@O
def adam(w, lr, t):
    w = np.array(w, dtype=float)
    m, v = np.zeros_like(w), np.zeros_like(w)
    for step in range(1, t + 1):
        g = 2 * w
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g ** 2
        w = w - lr * (m / (1 - 0.9 ** step)) / (np.sqrt(v / (1 - 0.999 ** step)) + 1e-8)
    return w.round(4)


Q(None, "L2 Regularisation in a Network", "Medium", "Weight decay",
  "Return (loss + (α/2n)·Σw², the same penalty sklearn's MLP adds) for the given data loss, weight arrays, α and batch size n, rounded to 4 decimals.",
  [((0.5, [[[1, 2], [3, 4]], [[-1, 0.5]]], 0.1, 10), 0.6562)],
  ("Nested loops to add up every squared weight.", "O(params)", "O(1)"),
  ("<code>sum(np.square(W).sum() for W in weights)</code>.", "O(params)", "O(1)"),
  names=["loss", "weights", "alpha", "n"])


@B
def l2_loss(loss, weights, alpha, n):
    total = 0.0
    for W in weights:
        for row in W:
            for v in row:
                total += v * v
    return round(loss + alpha * total / (2 * n), 4)


@O
def l2_loss(loss, weights, alpha, n):
    total = sum(np.square(np.array(W, dtype=float)).sum() for W in weights)
    return round(loss + alpha * total / (2 * n), 4)


Q(None, "Initialisation Range", "Easy", "Glorot: keep signals a sensible size",
  "sklearn's MLP draws each layer's starting weights uniformly in ±√(6 / (fan_in + fan_out)). For the given layer sizes, return each layer's bound, rounded to 4 decimals.",
  [(([3, 4, 2],), [0.9258, 1.0]), (([5, 16, 1],), [0.5345, 0.5941])],
  ("Apply the formula to each neighbouring pair of sizes.", "O(layers)", "O(layers)"),
  ("Build a real network, read each weight matrix's shape, and confirm its largest weight really is inside the bound.", "O(params)", "O(params)"))


@B
def init_bounds(sizes):
    out = []
    for fan_in, fan_out in zip(sizes, sizes[1:]):
        out.append(round(math.sqrt(6 / (fan_in + fan_out)), 4))
    return out


@O
def init_bounds(sizes):
    d, hidden, k = sizes[0], tuple(sizes[1:-1]), sizes[-1]
    y = np.zeros(2) if k == 1 else np.zeros((2, k))
    net = MLPRegressor(hidden_layer_sizes=hidden, solver="sgd", learning_rate_init=1e-12, momentum=0.0, random_state=0)
    net.partial_fit(np.zeros((2, d)), y)
    bounds = [math.sqrt(6 / sum(W.shape)) for W in net.coefs_]
    assert all(np.abs(W).max() <= b + 1e-6 for W, b in zip(net.coefs_, bounds))
    return [round(b, 4) for b in bounds]


Q(None, "Dropout", "Medium", "Randomly silence neurons",
  "Keep each activation with probability keep, using np.random.RandomState(seed).rand(n) &lt; keep; scale the kept ones by 1/keep so the expected value is unchanged. Round to 4 decimals.",
  [(([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 0.5, 0), [0.0, 0.0, 0.0, 0.0, 10.0, 0.0])],
  ("Draw one random number per activation in a loop.", "O(n)", "O(n)"),
  ("A boolean mask multiplied in one line.", "O(n)", "O(n)"),
  names=["a", "keep", "seed"])


@B
def dropout(a, keep, seed):
    rng = np.random.RandomState(seed)
    out = []
    for v in a:
        out.append(round(v / keep, 4) if rng.rand() < keep else 0.0)
    return out


@O
def dropout(a, keep, seed):
    mask = np.random.RandomState(seed).rand(len(a)) < keep
    return (np.array(a) * mask / keep).round(4)


Q(None, "Mini-Batches", "Easy", "Slice the data",
  "Return (start, stop) for each mini-batch of up to size rows when walking through n rows in order.",
  [((10, 4), [(0, 4), (4, 8), (8, 10)]), ((6, 2), [(0, 2), (2, 4), (4, 6)])],
  ("A while loop stepping by size.", "O(n / size)", "O(n / size)"),
  ("<code>sklearn.utils.gen_batches(n, size)</code>.", "O(n / size)", "O(n / size)"),
  names=["n", "size"])


@B
def batches(n, size):
    out, start = [], 0
    while start < n:
        out.append((start, min(start + size, n)))
        start += size
    return out


@O
def batches(n, size):
    return [(s.start, s.stop) for s in gen_batches(n, size)]


Q(None, "Learn XOR", "Hard", "Train a real network",
  "Train a one-hidden-layer network with 4 tanh neurons on XOR and return its predicted class for each row.",
  [((GATE, [0, 1, 1, 0]), [0, 1, 1, 0])],
  ("Full backprop in NumPy with a sigmoid output and log-loss: 5000 gradient steps from a seeded start.", "O(steps·n·params)", "O(params)"),
  ("<code>MLPClassifier(hidden_layer_sizes=(4,), activation='tanh', solver='lbfgs', random_state=1)</code>.", "O(steps·n·params)", "O(params)"),
  names=["X", "y"])


@B
def learn_xor(X, y):
    X, y = np.array(X, dtype=float), np.array(y, dtype=float)
    rng = np.random.RandomState(0)
    W1, b1 = rng.uniform(-1, 1, (4, 2)), rng.uniform(-1, 1, 4)
    W2, b2 = rng.uniform(-1, 1, 4), 0.0
    for _ in range(5000):
        a = np.tanh(X @ W1.T + b1)
        p = 1 / (1 + np.exp(-(a @ W2 + b2)))
        err = p - y
        da = err[:, None] * W2 * (1 - a ** 2)
        W2 = W2 - 0.5 * a.T @ err / len(y)
        b2 = b2 - 0.5 * err.mean()
        W1 = W1 - 0.5 * da.T @ X / len(y)
        b1 = b1 - 0.5 * da.mean(axis=0)
    p = 1 / (1 + np.exp(-(np.tanh(X @ W1.T + b1) @ W2 + b2)))
    return (p >= 0.5).astype(int)


@O
def learn_xor(X, y):
    net = MLPClassifier(hidden_layer_sizes=(4,), activation="tanh", solver="lbfgs", max_iter=2000, random_state=1)
    return net.fit(X, y).predict(X)
