from lib import *
import math
import numpy as np


TOPIC(
    id="tensors", title="Tensors & Layers", glyph="[[ ]]",
    blurb="The language of deep learning: tensor shapes and batches, dense layers, logits, softmax and stable cross-entropy, initialisation, and backpropagation through real matrices.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">X.shape                      # (batch, features)
Z = X @ W + b                # dense layer: W is (features, outputs)
H = np.maximum(0, Z)         # activation
Z - Z.max(axis=1, keepdims=True)   # keeps softmax numerically safe
np.eye(k)[y]                 # one-hot
-(np.log(P[np.arange(n), y])).mean()   # cross-entropy</code></pre>
<p>In PyTorch: <code>torch.tensor</code>, <code>nn.Linear</code>, <code>nn.ReLU</code>, <code>nn.CrossEntropyLoss</code> (it takes raw logits).</p>
""")

XB = [[1.0, 2.0], [0.0, -1.0], [3.0, 0.5]]
W1 = [[0.5, -1.0, 2.0], [1.0, 0.0, -0.5]]
B1 = [0.0, 1.0, -1.0]
W2 = [[1.0], [-0.5], [0.25]]
B2 = [0.5]



Q(None, "Shape of a Nested List", "Easy", "What a tensor is",
  "Return the shape of a rectangular nested list as a tuple.",
  [(([[1, 2, 3], [4, 5, 6]],), (2, 3)), (([[[1], [2]], [[3], [4]], [[5], [6]]],), (3, 2, 1)), (([1, 2],), (2,))],
  ("Keep stepping into the first element and record each length.", "O(depth)", "O(depth)"),
  ("<code>np.shape(x)</code>.", "O(n)", "O(n)"))


@B
def shape_of(x):
    shape = []
    while isinstance(x, list):
        shape.append(len(x))
        x = x[0]
    return tuple(shape)


@O
def shape_of(x):
    return np.shape(x)


Q(None, "Flatten a Batch of Images", "Easy", "(n, h, w) → (n, h·w)",
  "Turn each image in the batch into one long row.",
  [(([[[1, 2], [3, 4]], [[5, 6], [7, 8]]],), [[1, 2, 3, 4], [5, 6, 7, 8]])],
  ("Nested loops per image.", "O(n·h·w)", "O(n·h·w)"),
  ("<code>x.reshape(len(x), -1)</code>.", "O(n·h·w)", "O(1) view"))


@B
def flatten_images(batch):
    out = []
    for image in batch:
        row = []
        for line in image:
            row.extend(line)
        out.append(row)
    return out


@O
def flatten_images(batch):
    x = np.array(batch)
    return x.reshape(len(x), -1)


Q(None, "Broadcast Result Shape", "Medium", "Will these tensors combine?",
  "Return the shape that two shapes broadcast to, or None if they can't.",
  [(((3, 1), (1, 4)), (3, 4)), (((2, 3), (3,)), (2, 3)), (((2, 3), (2,)), None), (((5, 1, 4), (3, 1)), (5, 3, 4))],
  ("Compare sizes from the right; each pair must match or contain a 1.", "O(d)", "O(d)"),
  ("<code>np.broadcast_shapes</code>, which raises an error when they don't fit.", "O(d)", "O(d)"),
  names=["a", "b"])


@B
def broadcast_shape(a, b):
    out = []
    for i in range(1, max(len(a), len(b)) + 1):
        x = a[-i] if i <= len(a) else 1
        y = b[-i] if i <= len(b) else 1
        if x != y and x != 1 and y != 1:
            return None
        out.append(max(x, y))
    return tuple(reversed(out))


@O
def broadcast_shape(a, b):
    try:
        return np.broadcast_shapes(a, b)
    except ValueError:
        return None


Q(None, "Dense Layer Forward", "Easy", "Z = X·W + b",
  "Compute a dense layer's outputs for a batch. W has one row per input feature and one column per output neuron.",
  [((XB, W1, B1), [[2.5, 0.0, 0.0], [-1.0, 1.0, -0.5], [2.0, -2.0, 4.75]])],
  ("Triple loop: each row, each neuron, each feature.", "O(n·d·k)", "O(n·k)"),
  ("<code>X @ W + b</code>.", "O(n·d·k)", "O(n·k)"),
  names=["X", "W", "b"])


@B
def dense(X, W, b):
    out = []
    for row in X:
        outputs = []
        for k in range(len(b)):
            z = b[k]
            for j, x in enumerate(row):
                z += x * W[j][k]
            outputs.append(z)
        out.append(outputs)
    return out


@O
def dense(X, W, b):
    return np.array(X) @ np.array(W) + np.array(b)


Q(None, "Two-Layer Forward Pass", "Medium", "Input → ReLU → output",
  "Compute ReLU(X·W1 + b1)·W2 + b2 for a batch; round to 4 decimals.",
  [((XB, W1, B1, W2, B2), [[3.0], [0.0], [3.6875]])],
  ("Loops layer by layer.", "O(n·params)", "O(n·h)"),
  ("Two matrix products.", "O(n·params)", "O(n·h)"),
  names=["X", "W1", "b1", "W2", "b2"])


@B
def two_layers(X, W1, b1, W2, b2):
    out = []
    for row in X:
        hidden = []
        for k in range(len(b1)):
            z = b1[k] + sum(x * W1[j][k] for j, x in enumerate(row))
            hidden.append(max(0.0, z))
        o = b2[0] + sum(h * W2[k][0] for k, h in enumerate(hidden))
        out.append([round(o, 4)])
    return out


@O
def two_layers(X, W1, b1, W2, b2):
    H = np.maximum(0, np.array(X) @ np.array(W1) + np.array(b1))
    return (H @ np.array(W2) + np.array(b2)).round(4)


Q(None, "Model Memory", "Easy", "Parameters × bytes",
  "Layer sizes are given. Return (parameter count, size in MB using 4 bytes per parameter, rounded to 3 decimals; 1 MB = 10⁶ bytes).",
  [(([784, 256, 10],), (203530, 0.814)), (([1000, 1000, 1000],), (2002000, 8.008))],
  ("Add weights and biases per layer in a loop.", "O(layers)", "O(1)"),
  ("Vectorised: <code>(a * b + b).sum()</code> on neighbouring sizes.", "O(layers)", "O(layers)"))


@B
def model_memory(sizes):
    total = 0
    for a, b in zip(sizes, sizes[1:]):
        total += a * b + b
    return (total, round(total * 4 / 1e6, 3))


@O
def model_memory(sizes):
    s = np.array(sizes)
    total = int((s[:-1] * s[1:] + s[1:]).sum())
    return (total, round(total * 4 / 1e6, 3))


Q(None, "One-Hot a Batch of Labels", "Easy", "Targets for softmax",
  "Return a one-hot matrix for labels, with k classes.",
  [(([0, 2, 1], 3), [[1, 0, 0], [0, 0, 1], [0, 1, 0]])],
  ("Build each row of zeros and set one position.", "O(n·k)", "O(n·k)"),
  ("<code>np.eye(k, dtype=int)[y]</code>.", "O(n·k)", "O(n·k)"),
  names=["y", "k"])


@B
def one_hot(y, k):
    out = []
    for label in y:
        row = [0] * k
        row[label] = 1
        out.append(row)
    return out


@O
def one_hot(y, k):
    return np.eye(k, dtype=int)[y]


Q(None, "Softmax for a Batch, Safely", "Medium", "No overflow",
  "Return softmax probabilities per row, rounded to 4 decimals. Must work for scores like 1000.",
  [(([[2.0, 1.0, 0.0], [1000.0, 1000.0, 999.0]],), [[0.6652, 0.2447, 0.09], [0.4223, 0.4223, 0.1554]])],
  ("Subtract each row's max, then exponentiate and normalise in loops.", "O(n·k)", "O(n·k)"),
  ("The same with <code>keepdims=True</code>.", "O(n·k)", "O(n·k)"))


@B
def softmax_batch(Z):
    out = []
    for row in Z:
        top = max(row)
        e = [math.exp(v - top) for v in row]
        s = sum(e)
        out.append([round(v / s, 4) for v in e])
    return out


@O
def softmax_batch(Z):
    Z = np.array(Z, dtype=float)
    e = np.exp(Z - Z.max(axis=1, keepdims=True))
    return (e / e.sum(axis=1, keepdims=True)).round(4)


Q(None, "Cross-Entropy From Logits", "Medium", "Log-sum-exp",
  "Return the mean cross-entropy given raw scores Z and integer labels y, rounded to 4 decimals. Work directly with logs so that huge scores don't overflow.",
  [(([[2.0, 1.0, 0.0], [0.0, 3.0, 0.0]], [0, 1]), 0.2513), (([[1000.0, 0.0], [0.0, 1000.0]], [0, 0]), 500.0)],
  ("For each row: −(score of the true class) + log Σ e^score, using a shift by the max.", "O(n·k)", "O(1)"),
  ("Vectorised with the same shift.", "O(n·k)", "O(n·k)"),
  names=["Z", "y"])


@B
def ce_from_logits(Z, y):
    total = 0.0
    for row, label in zip(Z, y):
        top = max(row)
        log_sum = top + math.log(sum(math.exp(v - top) for v in row))
        total += log_sum - row[label]
    return round(total / len(y), 4)


@O
def ce_from_logits(Z, y):
    Z = np.array(Z, dtype=float)
    shifted = Z - Z.max(axis=1, keepdims=True)
    log_p = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    return round(-log_p[np.arange(len(y)), y].mean(), 4)


Q(None, "Binary Cross-Entropy From a Logit", "Medium", "The stable formula",
  "Return the mean of max(z, 0) − z·y + log(1 + e^(−|z|)), the safe form of log-loss. Round to 4 decimals.",
  [(([2.0, -1.0, 0.0], [1, 0, 1]), 0.3778), (([800.0], [0]), 800.0)],
  ("Loop using <code>math.log1p</code> and <code>math.exp</code>.", "O(n)", "O(1)"),
  ("Vectorised; <code>np.logaddexp(0, -z·s)</code> computes the same thing.", "O(n)", "O(n)"),
  names=["z", "y"])


@B
def bce_logits(z, y):
    total = 0.0
    for score, label in zip(z, y):
        total += max(score, 0) - score * label + math.log1p(math.exp(-abs(score)))
    return round(total / len(z), 4)


@O
def bce_logits(z, y):
    z, y = np.array(z, dtype=float), np.array(y, dtype=float)
    return round(np.logaddexp(0, -z * (2 * y - 1)).mean(), 4)


Q(None, "Mean Squared Error of a Batch", "Easy", "Averaged over all entries",
  "Return the mean of (ŷ − y)² over every entry of two same-shaped tables, rounded to 4 decimals.",
  [(([[1.0, 2.0], [3.0, 4.0]], [[1.0, 0.0], [5.0, 4.0]]), 2.0)],
  ("Two nested loops.", "O(n·k)", "O(1)"),
  ("<code>((a - b) ** 2).mean()</code>.", "O(n·k)", "O(n·k)"),
  names=["pred", "target"])


@B
def batch_mse(pred, target):
    total, count = 0.0, 0
    for r1, r2 in zip(pred, target):
        for a, b in zip(r1, r2):
            total += (a - b) ** 2
            count += 1
    return round(total / count, 4)


@O
def batch_mse(pred, target):
    return round(((np.array(pred) - np.array(target)) ** 2).mean(), 4)


Q(None, "Accuracy From Logits", "Easy", "Argmax",
  "Return the share of rows whose highest score is the true class, rounded to 4 decimals.",
  [(([[2.0, 1.0], [0.0, 3.0], [1.0, 0.0]], [0, 1, 1]), 0.6667)],
  ("Find each row's biggest position.", "O(n·k)", "O(1)"),
  ("<code>(Z.argmax(axis=1) == y).mean()</code>.", "O(n·k)", "O(n)"),
  names=["Z", "y"])


@B
def logits_accuracy(Z, y):
    correct = 0
    for row, label in zip(Z, y):
        if row.index(max(row)) == label:
            correct += 1
    return round(correct / len(y), 4)


@O
def logits_accuracy(Z, y):
    return round((np.array(Z).argmax(axis=1) == np.array(y)).mean(), 4)


Q(None, "Top-k Predictions", "Easy", "Most likely classes",
  "For each row return the indices of the k largest scores, largest first.",
  [(([[0.1, 0.7, 0.2], [0.5, 0.2, 0.3]], 2), [[1, 2], [0, 2]])],
  ("Sort each row's indices by score.", "O(n·k log k)", "O(n·k)"),
  ("<code>np.argsort(-Z, axis=1)[:, :k]</code>.", "O(n·k log k)", "O(n·k)"),
  names=["Z", "k"])


@B
def top_k(Z, k):
    return [sorted(range(len(row)), key=lambda i: -row[i])[:k] for row in Z]


@O
def top_k(Z, k):
    return np.argsort(-np.array(Z), axis=1)[:, :k]


Q(None, "Steps per Epoch", "Easy", "Batches and updates",
  "With n rows, a batch size and a number of epochs, return (steps per epoch, total updates). A smaller last batch still counts.",
  [((10000, 32, 10), (313, 3130)), ((64, 32, 3), (2, 6))],
  ("Count batches by walking through the rows.", "O(n / batch)", "O(1)"),
  ("<code>math.ceil(n / batch)</code>.", "O(1)", "O(1)"),
  names=["n", "batch", "epochs"])


@B
def steps(n, batch, epochs):
    count, start = 0, 0
    while start < n:
        count += 1
        start += batch
    return (count, count * epochs)


@O
def steps(n, batch, epochs):
    per_epoch = math.ceil(n / batch)
    return (per_epoch, per_epoch * epochs)


Q(None, "Shuffled Mini-Batches", "Medium", "A new order each epoch",
  "Shuffle indices with np.random.RandomState(seed).permutation(n), then split into batches. Return the list of index batches.",
  [((7, 3, 0), [[6, 2, 1], [3, 0, 5], [4]])],
  ("Loop, slicing the shuffled list.", "O(n)", "O(n)"),
  ("<code>np.array_split</code> at multiples of the batch size.", "O(n)", "O(n)"),
  names=["n", "batch", "seed"])


@B
def shuffled_batches(n, batch, seed):
    order = np.random.RandomState(seed).permutation(n).tolist()
    return [order[i:i + batch] for i in range(0, n, batch)]


@O
def shuffled_batches(n, batch, seed):
    order = np.random.RandomState(seed).permutation(n)
    return [part.tolist() for part in np.array_split(order, range(batch, n, batch))]


Q(None, "Gradient of a Linear Layer", "Medium", "∂MSE/∂W",
  "For Ŷ = X·W + b and MSE = mean((Ŷ − Y)²) over all entries, with one output column, return ∂/∂W as a column, rounded to 4 decimals.",
  [(([[1.0, 2.0], [3.0, 4.0]], [[1.0], [2.0]], [[0.5], [-0.5]], [0.0]), [[-9.0], [-13.0]])],
  ("Loops: each row adds 2·error·x to each weight's gradient, then divide by n.", "O(n·d)", "O(d)"),
  ("<code>2 * X.T @ (Y_hat - Y) / n</code>.", "O(n·d)", "O(n)"),
  names=["X", "Y", "W", "b"])


@B
def linear_grad(X, Y, W, b):
    n, d = len(X), len(X[0])
    grad = [0.0] * d
    for row, target in zip(X, Y):
        pred = b[0] + sum(x * W[j][0] for j, x in enumerate(row))
        for j, x in enumerate(row):
            grad[j] += 2 * (pred - target[0]) * x / n
    return [[round(g, 4)] for g in grad]


@O
def linear_grad(X, Y, W, b):
    X, Y, W = np.array(X), np.array(Y), np.array(W)
    return (2 * X.T @ (X @ W + np.array(b) - Y) / len(X)).round(4)


Q(None, "Backprop Through Two Layers", "Hard", "Matrix gradients",
  "Network: H = tanh(X·W1 + b1), Ŷ = H·W2 + b2, loss ½·mean((Ŷ − Y)²). Return the gradient for W1, rounded to 4 decimals.",
  [(([[1.0, 2.0], [0.0, 1.0]], [[1.0], [0.0]], [[0.5, -0.2], [0.1, 0.4]], [0.1, -0.1], [[0.3], [-0.6]], [0.2]), [[-0.0736, 0.2072], [-0.1351, 0.3912]])],
  ("Numerical: nudge every weight in W1 and watch the loss.", "O(params·n)", "O(1)"),
  ("Backprop: error × W2ᵀ × (1 − H²), then Xᵀ× that, divided by n.", "O(n·params)", "O(n·h)"),
  names=["X", "Y", "W1", "b1", "W2", "b2"])


@B
def backprop_w1(X, Y, W1, b1, W2, b2):
    def loss(W):
        total = 0.0
        for row, target in zip(X, Y):
            hidden = [math.tanh(b1[k] + sum(x * W[j][k] for j, x in enumerate(row))) for k in range(len(b1))]
            pred = b2[0] + sum(h * W2[k][0] for k, h in enumerate(hidden))
            total += (pred - target[0]) ** 2
        return total / (2 * len(X))

    h = 1e-6
    grad = []
    for j in range(len(W1)):
        line = []
        for k in range(len(W1[0])):
            up = [list(r) for r in W1]
            down = [list(r) for r in W1]
            up[j][k] += h
            down[j][k] -= h
            line.append(round((loss(up) - loss(down)) / (2 * h), 4))
        grad.append(line)
    return grad


@O
def backprop_w1(X, Y, W1, b1, W2, b2):
    X, Y, W1, W2 = map(np.array, (X, Y, W1, W2))
    H = np.tanh(X @ W1 + np.array(b1))
    error = H @ W2 + np.array(b2) - Y
    dH = error @ W2.T * (1 - H ** 2)
    return (X.T @ dH / len(X)).round(4)


Q(None, "Gradient Check", "Medium", "Catching backprop bugs",
  "Return the relative error ‖a − n‖ / (‖a‖ + ‖n‖) between an analytic and a numerical gradient, rounded to 6 decimals. Under about 1e-5 is healthy.",
  [(([1.0, 2.0], [1.0, 2.00001]), 0.0), (([1.0, 2.0], [1.0, 3.0]), 0.1852)],
  ("Square, sum and root in loops.", "O(d)", "O(1)"),
  ("<code>np.linalg.norm</code>.", "O(d)", "O(d)"),
  names=["analytic", "numeric"])


@B
def grad_check(analytic, numeric):
    top = math.sqrt(sum((a - n) ** 2 for a, n in zip(analytic, numeric)))
    bottom = math.sqrt(sum(a * a for a in analytic)) + math.sqrt(sum(n * n for n in numeric))
    return round(top / bottom, 6)


@O
def grad_check(analytic, numeric):
    a, n = np.array(analytic), np.array(numeric)
    return round(np.linalg.norm(a - n) / (np.linalg.norm(a) + np.linalg.norm(n)), 6)


Q(None, "Initialisation Scales", "Easy", "Glorot and He",
  "Given fan_in and fan_out, return (Glorot std √(2/(in + out)), He std √(2/in)), rounded to 4 decimals.",
  [((100, 100), (0.1, 0.1414)), ((784, 256), (0.0439, 0.0505))],
  ("Apply the formulas with <code>math.sqrt</code>.", "O(1)", "O(1)"),
  ("The same with <code>np.sqrt</code>, which works on arrays of layer sizes.", "O(1)", "O(1)"),
  names=["fan_in", "fan_out"])


@B
def init_scales(fan_in, fan_out):
    return (round(math.sqrt(2 / (fan_in + fan_out)), 4), round(math.sqrt(2 / fan_in), 4))


@O
def init_scales(fan_in, fan_out):
    return (round(np.sqrt(2 / (fan_in + fan_out)), 4), round(np.sqrt(2 / fan_in), 4))


Q(None, "Variance Through a Layer", "Medium", "Why scale matters",
  "If inputs have variance v and weights variance w, each output of a linear layer with n inputs has variance n·w·v. Starting from v = 1, return the variance after each of L layers, using the given weight std.",
  [((100, 0.1, 3), [1.0, 1.0, 1.0]), ((100, 0.2, 3), [4.0, 16.0, 64.0]), ((100, 0.05, 3), [0.25, 0.0625, 0.0156])],
  ("Loop, multiplying by n·std² each layer.", "O(L)", "O(L)"),
  ("Powers: <code>(n * std**2) ** np.arange(1, L + 1)</code>.", "O(L)", "O(L)"),
  names=["n", "std", "L"])


@B
def variance_through(n, std, L):
    out = []
    v = 1.0
    for _ in range(L):
        v = n * std * std * v
        out.append(round(v, 4))
    return out


@O
def variance_through(n, std, L):
    return ((n * std ** 2) ** np.arange(1, L + 1)).round(4)
