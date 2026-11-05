from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "The training loop, line by line", """
<p>All neural network training is this loop:</p>
<ol><li><b>Take a batch.</b></li>
<li><b>Forward:</b> compute predictions.</li>
<li><b>Loss:</b> measure the error.</li>
<li><b>Backward:</b> get every gradient.</li>
<li><b>Update:</b> nudge the weights.</li>
<li><b>Now and then:</b> check validation data, and save the best model.</li></ol>
<h4>What to watch</h4>
<table><tr><th>Curve</th><th>Meaning</th></tr>
<tr><td>Train and validation both falling</td><td>keep going</td></tr>
<tr><td>Train falling, validation rising</td><td>overfitting</td></tr>
<tr><td>Both flat and high</td><td>learning rate, or model too small</td></tr>
<tr><td>Loss becomes NaN</td><td>learning rate too high, or a bad input</td></tr></table>
<p><b>First test for any new model:</b> can it reach near-zero loss on 10 examples? If not, there's a bug, and more epochs won't help.</p>
""", practice=["SGD Update", "Smoothing a Loss Curve"])


@LD
def overfit_tiny_batch():
    r = np.random.default_rng(0)
    X = r.normal(size=(10, 5))
    y = r.integers(0, 2, 10).astype(float)
    W, b = r.normal(0, 0.5, (5, 16)), np.zeros(16)
    W2, b2 = r.normal(0, 0.5, 16), 0.0
    losses = []
    for step in range(600):
        H = np.tanh(X @ W + b)
        p = 1 / (1 + np.exp(-(H @ W2 + b2)))
        losses.append(-(y * np.log(p + 1e-9) + (1 - y) * np.log(1 - p + 1e-9)).mean())
        e = p - y
        dH = e[:, None] * W2 * (1 - H ** 2)
        W2 -= 0.5 * H.T @ e / 10
        b2 -= 0.5 * e.mean()
        W -= 0.5 * X.T @ dH / 10
        b -= 0.5 * dH.mean(axis=0)
    fig, ax = plt.subplots(figsize=(4.4, 2.7))
    ax.semilogy(losses)
    ax.set_xlabel("step")
    ax.set_title(f"10 random examples: loss reaches {losses[-1]:.3f}", fontsize=9)


LESSON("Core", "Momentum, RMSProp and Adam, by hand", """
<p>Take w = 1 and gradient 0.5 for three steps, with learning rate 0.1.</p>
<table><tr><th>Step</th><th>Plain SGD</th><th>Momentum (μ = 0.9)</th></tr>
<tr><td>1</td><td>0.95</td><td>v = −0.05, w = 0.95</td></tr>
<tr><td>2</td><td>0.90</td><td>v = −0.095, w = 0.855</td></tr>
<tr><td>3</td><td>0.85</td><td>v = −0.1355, w = 0.7195</td></tr></table>
<p>When gradients agree, momentum builds up speed; when they keep flipping, they cancel out.</p>
<h4>RMSProp: divide by the recent gradient size</h4>
<p>s ← 0.9s + 0.1g², then w ← w − η·g/√s. Starting from w = 1 with η = 0.01, two gradients of 2 end at <b>0.9454</b>, and two gradients of 200 also end at <b>0.9454</b>. So the step size no longer depends on the gradient's scale, and each weight effectively gets its own learning rate.</p>
<h4>Adam combines both</h4>
<p>It keeps an average gradient m (momentum) and an average squared gradient v (RMSProp), and corrects both for starting at zero. On the first step, this moves every weight by about the learning rate, whatever its gradient. Sensible default: lr = 0.001.</p>
""", practice=["SGD With Momentum", "RMSProp Step Sizes", "Adam With Bias Correction"])


@LD
def optimiser_race():
    def grad(p):
        return np.array([0.2 * p[0], 4 * p[1]])

    def run(kind, steps=60, lr=0.05):
        p, m, v = np.array([-4.0, 2.0]), np.zeros(2), np.zeros(2)
        path = [p]
        for t in range(1, steps + 1):
            g = grad(p)
            if kind == "sgd":
                p = p - lr * g
            elif kind == "momentum":
                m = 0.9 * m - lr * g
                p = p + m
            else:
                m = 0.9 * m + 0.1 * g
                v = 0.999 * v + 0.001 * g ** 2
                p = p - 0.2 * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
            path.append(p)
        return np.array(path)

    x, y = np.meshgrid(np.linspace(-5, 5, 80), np.linspace(-3, 3, 80))
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.contour(x, y, 0.1 * x ** 2 + 2 * y ** 2, levels=12, alpha=0.4)
    for kind in ["sgd", "momentum", "adam"]:
        path = run(kind)
        ax.plot(path[:, 0], path[:, 1], "o-", markersize=2, label=kind)
    ax.legend(fontsize=7)


LESSON("Core", "Weight decay, and why AdamW exists", """
<p><b>L2 regularisation</b> adds (λ/2)‖w‖² to the loss, so the gradient gains λw. With zero data gradient, w = 1, lr = 0.1 and λ = 0.5: w becomes 1 − 0.1(0.5) = 0.95. The weight simply shrinks.</p>
<h4>The problem with Adam</h4>
<p>Adam divides by the size of the gradient. If you add λw into the gradient, the decay gets divided too. Look at one step with w = 1, lr = 0.1, λ = 0.1:</p>
<table><tr><th>Data gradient</th><th>Adam + L2</th><th>AdamW</th></tr>
<tr><td>100</td><td>0.9</td><td>0.89</td></tr>
<tr><td>0.001</td><td>0.9</td><td>0.89</td></tr></table>
<p>With Adam + L2, the decay is lost: on this first step the update only depends on the sign of the gradient. <b>AdamW</b> applies the decay separately, as w − lr·λ·w, so it takes effect at a predictable rate. It's the default for transformers.</p>
<p>Usually don't apply decay to biases and normalisation parameters.</p>
""", practice=["AdamW vs L2 Penalty", "L2 Penalty in the Gradient"])


LESSON("Core", "Learning-rate schedules", """
<p>Early on you want big steps; near the end, small careful ones.</p>
<table><tr><th>Schedule</th><th>Rate over steps (start at 0.1)</th></tr>
<tr><td>Step decay (halve every 2)</td><td>0.1, 0.1, 0.05, 0.05, 0.025, 0.025</td></tr>
<tr><td>Cosine (T = 4)</td><td>0.1, 0.0854, 0.05, 0.0146, 0</td></tr>
<tr><td>Warm-up 2, then cosine</td><td>0.05, 0.1, 0.0854, 0.05, 0.0146, 0</td></tr></table>
<h4>Why warm up?</h4>
<p>At the start, random weights give wild gradients, and Adam's running averages are still unreliable. A few gentle steps stop an early blow-up. Warm-up followed by cosine is the standard transformer recipe.</p>
<h4>Finding a starting rate</h4>
<p>Try a <b>range test</b>: raise the rate each batch from 1e-6 to 1, and plot the loss. Choose where it falls fastest, somewhat before it blows up.</p>
""", practice=["Step Decay Schedule", "Cosine Schedule", "Warm-Up Then Cosine", "Pick a Learning Rate From a Range Test"])


@LD
def schedules():
    T = 100
    t = np.arange(T)
    step = 0.1 * 0.5 ** (t // 25)
    cosine = 0.05 * (1 + np.cos(np.pi * t / T))
    warm = np.where(t < 10, 0.1 * (t + 1) / 10, 0.05 * (1 + np.cos(np.pi * (t - 9) / 90)))
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.plot(t, step, label="step decay")
    ax.plot(t, cosine, label="cosine")
    ax.plot(t, warm, label="warm-up + cosine")
    ax.set_xlabel("step")
    ax.set_ylabel("learning rate")
    ax.legend(fontsize=7)


LESSON("Core", "Batch norm and layer norm, by hand", """
<p>Both rescale values to mean 0, spread 1. The difference is <b>which way they look</b>.</p>
<pre><code class="py">X = [[1, 2],
     [3, 4],
     [5, 6]]</code></pre>
<p><b>Batch norm</b> works down each <b>column</b> (feature). Column 1 has mean 3 and variance 2.667, so it becomes −1.22, 0, 1.22.</p>
<p><b>Layer norm</b> works across each <b>row</b> (example). Row (1, 2, 3) has mean 2 and variance 0.667, so it becomes −1.22, 0, 1.22.</p>
<table><tr><th></th><th>Batch norm</th><th>Layer norm</th></tr>
<tr><td>Depends on other examples?</td><td>yes</td><td>no</td></tr>
<tr><td>Small batches</td><td>noisy</td><td>fine</td></tr>
<tr><td>Train vs inference</td><td>behaves differently: uses running averages at inference</td><td>same</td></tr>
<tr><td>Typical use</td><td>CNNs</td><td>transformers, RNNs</td></tr></table>
<p><b>Classic bug:</b> forgetting <code>model.eval()</code>, so batch norm uses the current batch when predicting and results change with batch size.</p>
""", practice=["Batch Normalisation", "Layer Normalisation", "Running Statistics for Inference"])


@LD
def norm_compare():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    batch_norm = ((X - X.mean(axis=0)) / X.std(axis=0)).round(2)
    layer_norm = ((X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)).round(2)
    Y = np.array([[1.0, 2.0, 3.0]])
    row_result = ((Y - Y.mean()) / Y.std()).round(2)


LESSON("Advanced", "Regularisation and clipping", """
<table><tr><th>Technique</th><th>Worked example</th><th>What it does</th></tr>
<tr><td><b>Dropout</b> (keep 0.8)</td><td>4 → 0 or 5</td><td>silence random neurons; divide survivors by keep so the average stays 4</td></tr>
<tr><td><b>Label smoothing</b> (ε = 0.1, k = 3)</td><td>[0, 1, 0] → [0.033, 0.933, 0.033]</td><td>stops the model chasing 100% certainty</td></tr>
<tr><td><b>Clip by norm</b> (max 1)</td><td>(3, 4) → (0.6, 0.8)</td><td>limits step size; keeps direction</td></tr>
<tr><td><b>Clip by value</b> (c = 1)</td><td>(3, −4) → (1, −1)</td><td>simple, but changes direction</td></tr>
<tr><td><b>Early stopping</b> (patience 3)</td><td>keep the best epoch</td><td>stops before overfitting grows</td></tr></table>
<h4>Early stopping example</h4>
<p>Validation losses 1.0, 0.8, 0.7, 0.72, 0.71, 0.73: the best is epoch 2. After 3 epochs with no new best, training stops at epoch 5 and we restore epoch 2. A later dip might have come (patience is a trade-off).</p>
<h4>Gradient accumulation</h4>
<p>Want batch 256 but only 64 fits on the GPU? Run 4 small batches and average their gradients before updating. It gives the same gradient, ignoring batch norm, at the cost of more time.</p>
""", practice=["Clip Gradients by Norm", "Clip Gradients by Value", "Label Smoothing", "Dropout During Training", "Early Stopping", "Gradient Accumulation"])


LESSON("Advanced", "A complete PyTorch training loop", """
<p>This code runs as shown on your own machine (PyTorch isn't available in this browser course):</p>
<pre><code class="py">optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
loss_fn = nn.CrossEntropyLoss(label_smoothing=0.1)

for epoch in range(10):
    model.train()                       # dropout and batch norm: training mode
    for xb, yb in loader:
        optimizer.zero_grad()           # clear the old gradients
        loss = loss_fn(model(xb), yb)   # forward + loss
        loss.backward()                 # backward
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()                # update
    scheduler.step()

    model.eval()                        # dropout off; batch norm uses running stats
    with torch.no_grad():               # no gradients needed: faster
        val_logits = model(xb)</code></pre>
<h4>The bugs almost everyone hits</h4>
<ul><li>Forgetting <code>zero_grad()</code>: gradients add up across steps.</li>
<li>Forgetting <code>model.eval()</code> for validation.</li>
<li>Calling <code>clip_grad_norm_</code> after <code>step()</code>, which is too late.</li>
<li>Keeping a tensor's graph alive with <code>total += loss</code>; use <code>loss.item()</code>.</li></ul>
""")
