from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "What deep learning adds", """
<p>Classic ML needs you to design the features. <b>Deep learning learns the features too.</b> Each layer turns its input into something a little more useful: pixels into edges, edges into shapes, shapes into objects.</p>
<table><tr><th></th><th>Classic ML</th><th>Deep learning</th></tr>
<tr><td>Features</td><td>designed by hand</td><td>learned</td></tr>
<tr><td>Best on</td><td>tables, small data</td><td>images, audio, text, large data</td></tr>
<tr><td>Needs</td><td>a CPU, minutes</td><td>often a GPU, hours or more</td></tr>
<tr><td>Interpretability</td><td>usually easier</td><td>harder</td></tr></table>
<p><b>Honest advice:</b> for ordinary tables, gradient boosting often wins with far less effort. Use deep learning when the input is unstructured, or when you can use a pre-trained model.</p>
<p>Every deep model, including the largest language models, is built from what you'll learn here: tensors, layers, a loss, gradients and an update rule.</p>
""")


LESSON("Basics", "Tensors and shapes", """
<p>A <b>tensor</b> is an array with any number of dimensions. Reading shapes is the most useful daily skill in deep learning.</p>
<table><tr><th>Data</th><th>Shape</th><th>Means</th></tr>
<tr><td>Table</td><td>(32, 20)</td><td>32 rows, 20 features</td></tr>
<tr><td>Colour images (PyTorch)</td><td>(32, 3, 224, 224)</td><td>batch, channels, height, width</td></tr>
<tr><td>Token ids</td><td>(8, 100)</td><td>8 texts, 100 tokens each</td></tr>
<tr><td>Token embeddings</td><td>(8, 100, 512)</td><td>each token is now a 512-number vector</td></tr>
<tr><td>Logits for next token</td><td>(8, 100, 50000)</td><td>a score for every word in the vocabulary, at every position</td></tr></table>
<p>The first dimension is nearly always the <b>batch</b>: we process many examples together, for speed and for steadier gradients.</p>
<p><b>Debugging habit:</b> write the expected shape beside each line. Most deep learning bugs are shape bugs, and the quiet ones come from broadcasting.</p>
""", practice=["Shape of a Nested List", "Flatten a Batch of Images", "Broadcast Result Shape", "Model Memory"])


@LD
def shapes_demo():
    images = np.zeros((32, 3, 224, 224))
    flat = images.reshape(32, -1)
    tokens = np.zeros((8, 100), dtype=int)
    embedding_table = np.zeros((50000, 512))
    embedded = embedding_table[tokens]
    shapes = (images.shape, flat.shape, embedded.shape)
    silent_bug = (np.zeros((3,)) + np.zeros((3, 1))).shape


LESSON("Basics", "A dense layer by hand", """
<p>Input x = (1, 2), going into 3 neurons. W has one row per input and one column per neuron:</p>
<pre><code class="py">W = [[0.5, -1.0,  2.0],     b = [0, 1, -1]
     [1.0,  0.0, -0.5]]</code></pre>
<table><tr><th>Neuron</th><th>Calculation</th><th>z</th><th>ReLU(z)</th></tr>
<tr><td>1</td><td>1(0.5) + 2(1.0) + 0</td><td>2.5</td><td>2.5</td></tr>
<tr><td>2</td><td>1(−1.0) + 2(0.0) + 1</td><td>0</td><td>0</td></tr>
<tr><td>3</td><td>1(2.0) + 2(−0.5) − 1</td><td>0</td><td>0</td></tr></table>
<p>All at once: <code>Z = X @ W + b</code>. Then an output layer with weights (1, −0.5, 0.25) and bias 0.5 gives 2.5 + 0.5 = <b>3.0</b>.</p>
<h4>Count the shapes</h4>
<p>X is (1, 2), W is (2, 3), and X·W is (1, 3): <b>the inner sizes must match</b>. This layer has 2 × 3 + 3 = 9 parameters.</p>
""", practice=["Dense Layer Forward", "Two-Layer Forward Pass"])


@LD
def dense_by_hand():
    X = np.array([[1.0, 2.0]])
    W = np.array([[0.5, -1.0, 2.0], [1.0, 0.0, -0.5]])
    b = np.array([0.0, 1.0, -1.0])
    Z = X @ W + b
    H = np.maximum(0, Z)
    output = H @ np.array([1.0, -0.5, 0.25]) + 0.5
    parameters = W.size + b.size


LESSON("Core", "From logits to a loss, safely", """
<p>A classifier's last layer gives raw scores called <b>logits</b>. Suppose they are (2, 1, 0) and the true class is the first.</p>
<ol><li><b>Softmax:</b> e² = 7.389, e¹ = 2.718, e⁰ = 1. These total 11.107, so the probabilities are 0.665, 0.245, 0.090.</li>
<li><b>Cross-entropy:</b> −ln(0.665) = <b>0.408</b>.</li></ol>
<h4>Why not compute it that way in code?</h4>
<p>With logits like 1000, e¹⁰⁰⁰ overflows to infinity, and very small probabilities round to 0, so ln 0 gives −∞. Work with logs directly:</p>
<pre><code class="py">loss = log(Σ e^z) − z_true
log(Σ e^z) = max(z) + log(Σ e^(z − max(z)))     # the log-sum-exp trick</code></pre>
<p>That's why PyTorch's <code>CrossEntropyLoss</code> takes <b>logits</b>. Applying softmax first is a classic bug: the model still trains, but worse.</p>
""", practice=["Softmax for a Batch, Safely", "One-Hot a Batch of Labels", "Cross-Entropy From Logits", "Binary Cross-Entropy From a Logit", "Accuracy From Logits", "Top-k Predictions", "Mean Squared Error of a Batch"])


@LD
def safe_loss():
    z = np.array([2.0, 1.0, 0.0])
    naive = -math.log(math.exp(z[0]) / np.exp(z).sum())
    big = np.array([1000.0, 0.0, 0.0])
    with np.errstate(over="ignore"):
        overflowed = np.exp(big).sum()
    shifted = big - big.max()
    log_sum = big.max() + np.log(np.exp(shifted).sum())
    safe = log_sum - big[0]


LESSON("Core", "Batches, steps and epochs", """
<table><tr><th>Word</th><th>Meaning</th></tr>
<tr><td>Batch</td><td>the examples used for one update</td></tr>
<tr><td>Step (iteration)</td><td>one update of the weights</td></tr>
<tr><td>Epoch</td><td>one full pass through the data</td></tr></table>
<p><b>Worked example:</b> 10,000 rows with batch size 32 gives ⌈10000 / 32⌉ = <b>313 steps per epoch</b>, so 10 epochs make 3,130 updates.</p>
<h4>Choosing a batch size</h4>
<ul><li><b>Small:</b> noisy gradients, more updates per epoch, less memory.</li>
<li><b>Large:</b> smoother gradients, faster per example on a GPU, but needs more memory.</li>
<li>Common starting points: 32–256. If you run out of memory, halve it.</li></ul>
<p><b>Always shuffle</b> training data each epoch. If the data arrives sorted by class, each batch misleads the model. Don't shuffle time-ordered validation splits.</p>
""", practice=["Steps per Epoch", "Shuffled Mini-Batches"])


@LD
def batch_noise():
    r = np.random.default_rng(0)
    gradients = r.normal(1.0, 3.0, 100000)
    sizes = [1, 8, 32, 256]
    spreads = {b: round(float(gradients[:b * 300].reshape(-1, b).mean(axis=1).std()), 3) for b in sizes}
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.loglog(sizes, list(spreads.values()), "o-", label="measured")
    ax.loglog(sizes, [3 / b ** 0.5 for b in sizes], "--", label="3 / √batch")
    ax.set_xlabel("batch size")
    ax.set_ylabel("noise in the gradient")
    ax.legend(fontsize=8)


LESSON("Core", "Backpropagation with matrices", """
<p>For H = tanh(X·W₁ + b₁), Ŷ = H·W₂ + b₂, with loss ½·mean((Ŷ − Y)²). Follow the shapes with n rows, d features and h hidden neurons:</p>
<table><tr><th>Step</th><th>Code</th><th>Shape</th></tr>
<tr><td>Forward</td><td><code>H = tanh(X @ W1 + b1)</code></td><td>(n, h)</td></tr>
<tr><td></td><td><code>Y_hat = H @ W2 + b2</code></td><td>(n, 1)</td></tr>
<tr><td>Error</td><td><code>E = Y_hat - Y</code></td><td>(n, 1)</td></tr>
<tr><td>Into H</td><td><code>dH = E @ W2.T * (1 - H**2)</code></td><td>(n, h)</td></tr>
<tr><td>Into W1</td><td><code>X.T @ dH / n</code></td><td>(d, h)</td></tr>
<tr><td>Into W2</td><td><code>H.T @ E / n</code></td><td>(h, 1)</td></tr></table>
<p><b>The rule to remember:</b> a gradient has the same shape as the thing it belongs to. If it doesn't, the code is wrong.</p>
<p><b>Why go backwards?</b> <code>E @ W2.T</code> is shared by everything earlier, so computing from the output reuses it. Going forwards would repeat the work for every weight.</p>
<p>Check any hand-written gradient against a numerical one. A relative error below about 1e-5 is healthy.</p>
""", practice=["Gradient of a Linear Layer", "Backprop Through Two Layers", "Gradient Check"])


@LD
def backprop_shapes():
    r = np.random.default_rng(0)
    X, Y = r.normal(size=(4, 3)), r.normal(size=(4, 1))
    W1, b1 = r.normal(size=(3, 2)), np.zeros(2)
    W2, b2 = r.normal(size=(2, 1)), np.zeros(1)
    H = np.tanh(X @ W1 + b1)
    E = H @ W2 + b2 - Y
    dH = E @ W2.T * (1 - H ** 2)
    grad_W1 = X.T @ dH / len(X)

    def loss(W):
        return (((np.tanh(X @ W + b1) @ W2 + b2 - Y) ** 2).mean()) / 2

    bumped = W1.copy()
    bumped[0, 0] += 1e-6
    numeric = (loss(bumped) - loss(W1)) / 1e-6
    analytic = grad_W1[0, 0]
    shapes = (H.shape, E.shape, grad_W1.shape)


LESSON("Advanced", "Initialisation: why the starting numbers matter", """
<p>Each output of a linear layer is a sum of n terms, so its variance is <b>n × var(weights) × var(inputs)</b>. With n = 100 and inputs of variance 1:</p>
<table><tr><th>Weight std</th><th>Multiplier per layer</th><th>After 1, 2, 3 layers</th><th>Effect</th></tr>
<tr><td>0.05</td><td>0.25</td><td>0.25, 0.0625, 0.0156</td><td>signal dies</td></tr>
<tr><td>0.1</td><td>1</td><td>1, 1, 1</td><td>stays healthy</td></tr>
<tr><td>0.2</td><td>4</td><td>4, 16, 64</td><td>signal explodes</td></tr></table>
<p>So choose var(weights) ≈ 1/n. <b>Glorot</b> uses 2/(in + out), for tanh and sigmoid. <b>He</b> uses 2/in, for ReLU, which zeroes about half of its inputs and so needs double the variance.</p>
<p><b>Never start all at zero:</b> every neuron would compute the same thing and receive the same gradient, and would stay identical forever. Frameworks do this for you, but you need it when a custom model won't train. The chart measures it.</p>
""", practice=["Initialisation Scales", "Variance Through a Layer"])


@LD
def activations_by_layer():
    r = np.random.default_rng(0)
    width = 100
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    for std, name in [(0.05, "too small"), (0.1, "1/√n: right"), (0.2, "too large")]:
        x = r.normal(size=(200, width))
        sizes = []
        for layer in range(8):
            x = x @ r.normal(0, std, (width, width))
            sizes.append(x.std())
        ax.semilogy(range(1, 9), sizes, "o-", markersize=3, label=name)
    ax.set_xlabel("layer")
    ax.set_ylabel("spread of the signal")
    ax.legend(fontsize=7)


LESSON("Advanced", "The same network in PyTorch", """
<p>PyTorch does the tensor maths on a GPU and <b>computes the gradients for you</b>. It doesn't run in this browser course, so run it on your own machine or in Colab.</p>
<pre><code class="py">import torch
from torch import nn

model = nn.Sequential(nn.Linear(784, 256), nn.ReLU(), nn.Linear(256, 10))

x = torch.randn(32, 784)             # a batch
y = torch.randint(0, 10, (32,))      # class labels

logits = model(x)                    # shape (32, 10)
loss = nn.CrossEntropyLoss()(logits, y)   # takes raw logits
loss.backward()                      # backpropagation

model[0].weight.grad.shape           # (256, 784)</code></pre>
<p><b>One difference:</b> PyTorch stores a linear layer's weights as (outputs, inputs), the opposite of the X·W form used in this course. That's why the gradient's shape is (256, 784).</p>
<p>Now <code>loss.backward()</code> isn't magic. It does what you wrote by hand in the previous lesson, for any model.</p>
""")
