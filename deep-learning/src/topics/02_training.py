from lib import *
import math
import numpy as np


TOPIC(
    id="training", title="Training Deep Networks", glyph="↘",
    blurb="How to make deep networks learn: momentum, RMSProp, Adam and AdamW, learning-rate schedules and warm-up, batch and layer normalisation, gradient clipping, label smoothing, early stopping and gradient accumulation.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">lr_t = lr * 0.5 * (1 + cos(pi * t / T))       # cosine schedule
g = g * min(1, max_norm / norm(g))            # clip by norm
(X - X.mean(0)) / X.std(0)                    # batch norm (per feature)
(X - X.mean(1, keepdims=True)) / X.std(1, keepdims=True)   # layer norm (per row)
y * (1 - eps) + eps / k                       # label smoothing</code></pre>
<p>PyTorch: <code>torch.optim.AdamW</code>, <code>CosineAnnealingLR</code>, <code>nn.LayerNorm</code>, <code>clip_grad_norm_</code>.</p>
""")



Q(None, "SGD Update", "Easy", "w ← w − η·g",
  "Return the weights after one SGD step, rounded to 4 decimals.",
  [(([1.0, -2.0], [0.5, -1.0], 0.1), [0.95, -1.9])],
  ("Update each weight in a loop.", "O(d)", "O(d)"),
  ("Vector arithmetic.", "O(d)", "O(d)"),
  names=["w", "g", "lr"])


@B
def sgd(w, g, lr):
    return [round(a - lr * b, 4) for a, b in zip(w, g)]


@O
def sgd(w, g, lr):
    return (np.array(w) - lr * np.array(g)).round(4)


Q(None, "SGD With Momentum", "Medium", "Velocity",
  "Apply gradient steps for the given list of gradients, with v ← μv − η·g and w ← w + v, starting at v = 0. Return the final w, rounded to 4 decimals.",
  [((1.0, [0.5, 0.5, 0.5], 0.1, 0.9), 0.7195)],
  ("A loop over the gradients.", "O(steps)", "O(1)"),
  ("Each update is a discounted sum: use powers of μ with <code>np.cumsum</code>.", "O(steps²)", "O(steps)"),
  names=["w", "grads", "lr", "mu"])


@B
def momentum(w, grads, lr, mu):
    v = 0.0
    for g in grads:
        v = mu * v - lr * g
        w = w + v
    return round(w, 4)


@O
def momentum(w, grads, lr, mu):
    g = np.array(grads)
    velocities = [-lr * (g[:t + 1] * mu ** np.arange(t, -1, -1)).sum() for t in range(len(g))]
    return round(w + float(np.sum(velocities)), 4)


Q(None, "RMSProp Step Sizes", "Medium", "Divide by recent gradient size",
  "Run RMSProp on one weight: s ← βs + (1 − β)g², w ← w − η·g/√(s + ε) with β = 0.9, ε = 1e-8, s₀ = 0. Return the final w, rounded to 4 decimals.",
  [((1.0, [2.0, 2.0], 0.01), 0.9454), ((1.0, [200.0, 200.0], 0.01), 0.9454)],
  ("A loop.", "O(steps)", "O(1)"),
  ("The running average in closed form with weights 0.1·0.9ᵏ.", "O(steps²)", "O(steps)"),
  names=["w", "grads", "lr"])


@B
def rmsprop(w, grads, lr):
    s = 0.0
    for g in grads:
        s = 0.9 * s + 0.1 * g * g
        w = w - lr * g / math.sqrt(s + 1e-8)
    return round(w, 4)


@O
def rmsprop(w, grads, lr):
    g = np.array(grads, dtype=float)
    for t in range(len(g)):
        s = (0.1 * g[:t + 1] ** 2 * 0.9 ** np.arange(t, -1, -1)).sum()
        w = w - lr * g[t] / np.sqrt(s + 1e-8)
    return round(float(w), 4)


Q(None, "Adam With Bias Correction", "Hard", "The default optimiser",
  "Run Adam on the weight vector for the list of gradient vectors (β₁ = 0.9, β₂ = 0.999, ε = 1e-8). Return final weights, rounded to 4 decimals.",
  [(([1.0, -1.0], [[0.5, 100.0], [0.5, 100.0]], 0.1), [0.8, -1.2])],
  ("Lists of m and v for each weight.", "O(steps·d)", "O(d)"),
  ("Vector operations.", "O(steps·d)", "O(d)"),
  names=["w", "grads", "lr"])


@B
def adam(w, grads, lr):
    w = list(w)
    m, v = [0.0] * len(w), [0.0] * len(w)
    for t, g in enumerate(grads, start=1):
        for i in range(len(w)):
            m[i] = 0.9 * m[i] + 0.1 * g[i]
            v[i] = 0.999 * v[i] + 0.001 * g[i] ** 2
            m_hat = m[i] / (1 - 0.9 ** t)
            v_hat = v[i] / (1 - 0.999 ** t)
            w[i] -= lr * m_hat / (math.sqrt(v_hat) + 1e-8)
    return [round(x, 4) for x in w]


@O
def adam(w, grads, lr):
    w = np.array(w, dtype=float)
    m, v = np.zeros_like(w), np.zeros_like(w)
    for t, g in enumerate(np.array(grads, dtype=float), start=1):
        m = 0.9 * m + 0.1 * g
        v = 0.999 * v + 0.001 * g ** 2
        w = w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
    return w.round(4)


Q(None, "AdamW vs L2 Penalty", "Hard", "Decoupled weight decay",
  "One step from w with gradient g, lr, decay d. Return (Adam with L2 — adds d·w to g first; AdamW — subtracts lr·d·w separately), rounded to 4 decimals.",
  [((1.0, 100.0, 0.1, 0.1), (0.9, 0.89)), ((1.0, 0.001, 0.1, 0.1), (0.9, 0.89))],
  ("Run the first Adam step by hand both ways.", "O(1)", "O(1)"),
  ("On step 1 the bias-corrected ratio is g/|g|, so Adam moves by exactly lr·sign(g).", "O(1)", "O(1)"),
  names=["w", "g", "lr", "d"])


@B
def adamw_compare(w, g, lr, d):
    def first_step(weight, gradient):
        m = 0.1 * gradient
        v = 0.001 * gradient ** 2
        return weight - lr * (m / (1 - 0.9)) / (math.sqrt(v / (1 - 0.999)) + 1e-8)

    with_l2 = first_step(w, g + d * w)
    adamw = first_step(w, g) - lr * d * w
    return (round(with_l2, 4), round(adamw, 4))


@O
def adamw_compare(w, g, lr, d):
    with_l2 = w - lr * np.sign(g + d * w)
    adamw = w - lr * np.sign(g) - lr * d * w
    return (round(float(with_l2), 4), round(float(adamw), 4))


Q(None, "Step Decay Schedule", "Easy", "Drop every few epochs",
  "lr is multiplied by gamma every step_size epochs. Return the rate at each of the first n epochs, rounded to 5 decimals.",
  [((0.1, 0.5, 2, 6), [0.1, 0.1, 0.05, 0.05, 0.025, 0.025])],
  ("Loop, dropping when the epoch is a multiple of step_size.", "O(n)", "O(n)"),
  ("<code>lr * gamma ** (epochs // step_size)</code>.", "O(n)", "O(n)"),
  names=["lr", "gamma", "step_size", "n"])


@B
def step_decay(lr, gamma, step_size, n):
    out = []
    current = lr
    for e in range(n):
        if e > 0 and e % step_size == 0:
            current *= gamma
        out.append(round(current, 5))
    return out


@O
def step_decay(lr, gamma, step_size, n):
    return (lr * gamma ** (np.arange(n) // step_size)).round(5)


Q(None, "Cosine Schedule", "Easy", "Smooth decay",
  "Return lr·½(1 + cos(πt/T)) for each t in 0 … T, rounded to 4 decimals.",
  [((0.1, 4), [0.1, 0.0854, 0.05, 0.0146, 0.0])],
  ("<code>math.cos</code> in a loop.", "O(T)", "O(T)"),
  ("Vectorised with <code>np.cos</code>.", "O(T)", "O(T)"),
  names=["lr", "T"])


@B
def cosine_lr(lr, T):
    return [round(lr * 0.5 * (1 + math.cos(math.pi * t / T)), 4) + 0.0 for t in range(T + 1)]


@O
def cosine_lr(lr, T):
    t = np.arange(T + 1)
    return (lr * 0.5 * (1 + np.cos(np.pi * t / T))).round(4) + 0.0


Q(None, "Warm-Up Then Cosine", "Medium", "The transformer schedule",
  "Rise linearly from lr/warm up to lr over the first warm steps, then cosine to 0 by the end. Return the rate at each of T steps, rounded to 4 decimals.",
  [((0.1, 2, 6), [0.05, 0.1, 0.0854, 0.05, 0.0146, 0.0])],
  ("An if/else per step.", "O(T)", "O(T)"),
  ("<code>np.where</code> on the step array.", "O(T)", "O(T)"),
  names=["lr", "warm", "T"])


@B
def warm_cosine(lr, warm, T):
    out = []
    for t in range(T):
        if t < warm:
            value = lr * (t + 1) / warm
        else:
            value = lr * 0.5 * (1 + math.cos(math.pi * (t - warm + 1) / (T - warm)))
        out.append(round(value, 4) + 0.0)
    return out


@O
def warm_cosine(lr, warm, T):
    t = np.arange(T)
    cosine = lr * 0.5 * (1 + np.cos(np.pi * (t - warm + 1) / (T - warm)))
    return np.where(t < warm, lr * (t + 1) / warm, cosine).round(4) + 0.0


Q(None, "Clip Gradients by Norm", "Easy", "Stops explosions",
  "If ‖g‖ exceeds max_norm, scale g down to that length. Round to 4 decimals.",
  [(([3.0, 4.0], 1.0), [0.6, 0.8]), (([0.3, 0.4], 1.0), [0.3, 0.4])],
  ("Compute the length in a loop, then scale.", "O(d)", "O(d)"),
  ("<code>g * min(1, max_norm / norm)</code>.", "O(d)", "O(d)"),
  names=["g", "max_norm"])


@B
def clip_norm(g, max_norm):
    norm = math.sqrt(sum(x * x for x in g))
    if norm <= max_norm:
        return [round(x, 4) for x in g]
    return [round(x * max_norm / norm, 4) for x in g]


@O
def clip_norm(g, max_norm):
    g = np.array(g)
    return (g * min(1.0, max_norm / np.linalg.norm(g))).round(4)


Q(None, "Clip Gradients by Value", "Easy", "Keeps it simple, changes direction",
  "Limit each entry to [−c, c].",
  [(([3.0, -4.0, 0.5], 1.0), [1.0, -1.0, 0.5])],
  ("<code>max(-c, min(c, x))</code>.", "O(d)", "O(d)"),
  ("<code>np.clip</code>.", "O(d)", "O(d)"),
  names=["g", "c"])


@B
def clip_value(g, c):
    return [max(-c, min(c, x)) for x in g]


@O
def clip_value(g, c):
    return np.clip(g, -c, c)


Q(None, "Batch Normalisation", "Medium", "Per feature, across the batch",
  "Return (x − mean)/√(var + 1e-5) for each column of the batch (population variance), rounded to 4 decimals.",
  [(([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],), [[-1.2247, -1.2247], [0.0, 0.0], [1.2247, 1.2247]])],
  ("Mean and variance per column in loops.", "O(n·d)", "O(d)"),
  ("<code>X.mean(axis=0)</code>, <code>X.var(axis=0)</code>.", "O(n·d)", "O(n·d)"))


@B
def batch_norm(X):
    n, d = len(X), len(X[0])
    out = [[0.0] * d for _ in range(n)]
    for j in range(d):
        col = [row[j] for row in X]
        mean = sum(col) / n
        var = sum((v - mean) ** 2 for v in col) / n
        for i in range(n):
            out[i][j] = round((col[i] - mean) / math.sqrt(var + 1e-5), 4) + 0.0
    return out


@O
def batch_norm(X):
    X = np.array(X)
    return ((X - X.mean(axis=0)) / np.sqrt(X.var(axis=0) + 1e-5)).round(4) + 0.0


Q(None, "Layer Normalisation", "Medium", "Per row: used in transformers",
  "Return (x − mean)/√(var + 1e-5) within each row (population variance), rounded to 4 decimals.",
  [(([[1.0, 2.0, 3.0], [10.0, 10.0, 40.0]],), [[-1.2247, 0.0, 1.2247], [-0.7071, -0.7071, 1.4142]])],
  ("Mean and variance per row in loops.", "O(n·d)", "O(n·d)"),
  ("<code>axis=1, keepdims=True</code>.", "O(n·d)", "O(n·d)"))


@B
def layer_norm(X):
    out = []
    for row in X:
        mean = sum(row) / len(row)
        var = sum((v - mean) ** 2 for v in row) / len(row)
        out.append([round((v - mean) / math.sqrt(var + 1e-5), 4) + 0.0 for v in row])
    return out


@O
def layer_norm(X):
    X = np.array(X)
    return ((X - X.mean(axis=1, keepdims=True)) / np.sqrt(X.var(axis=1, keepdims=True) + 1e-5)).round(4) + 0.0


Q(None, "Running Statistics for Inference", "Medium", "Exponential moving average",
  "Batch norm keeps a running mean: r ← (1 − m)·r + m·batch_mean, starting at 0. Return it after the given batch means, rounded to 4 decimals (m = 0.1).",
  [(([2.0, 2.0, 2.0],), 0.542), (([1.0, 3.0],), 0.39)],
  ("A loop.", "O(n)", "O(1)"),
  ("Closed form: Σ m·(1 − m)^(n−1−i)·xᵢ.", "O(n)", "O(n)"))


@B
def running_mean(means):
    r = 0.0
    for x in means:
        r = 0.9 * r + 0.1 * x
    return round(r, 4)


@O
def running_mean(means):
    x = np.array(means)
    return round((0.1 * x * 0.9 ** np.arange(len(x) - 1, -1, -1)).sum(), 4)


Q(None, "L2 Penalty in the Gradient", "Easy", "Weight decay",
  "With loss + (λ/2)‖w‖², the gradient becomes g + λw. Return one SGD step from w, rounded to 4 decimals.",
  [(([1.0, -2.0], [0.0, 0.0], 0.1, 0.5), [0.95, -1.9]), (([1.0, -2.0], [1.0, 1.0], 0.1, 0.5), [0.85, -2.0])],
  ("Adjust each gradient in a loop, then step.", "O(d)", "O(d)"),
  ("<code>w - lr * (g + lam * w)</code>.", "O(d)", "O(d)"),
  names=["w", "g", "lr", "lam"])


@B
def l2_step(w, g, lr, lam):
    return [round(a - lr * (b + lam * a), 4) for a, b in zip(w, g)]


@O
def l2_step(w, g, lr, lam):
    w = np.array(w)
    return (w - lr * (np.array(g) + lam * w)).round(4)


Q(None, "Dropout During Training", "Medium", "Keep, then rescale",
  "Keep each value when np.random.RandomState(seed).rand(n) is below keep, and divide kept values by keep so the average is unchanged. Round to 4 decimals.",
  [(([1.0, 2.0, 3.0, 4.0], 0.8, 0), [1.25, 2.5, 3.75, 5.0])],
  ("One random draw per value.", "O(n)", "O(n)"),
  ("A mask times the array.", "O(n)", "O(n)"),
  names=["a", "keep", "seed"])


@B
def dropout(a, keep, seed):
    rng = np.random.RandomState(seed)
    return [round(v / keep, 4) if rng.rand() < keep else 0.0 for v in a]


@O
def dropout(a, keep, seed):
    mask = np.random.RandomState(seed).rand(len(a)) < keep
    return (np.array(a) * mask / keep).round(4)


Q(None, "Label Smoothing", "Easy", "Don't aim for 100%",
  "Return one-hot targets for the labels with smoothing: y(1 − ε) + ε/k, rounded to 4 decimals.",
  [(([1, 0], 3, 0.1), [[0.0333, 0.9333, 0.0333], [0.9333, 0.0333, 0.0333]])],
  ("Loops.", "O(n·k)", "O(n·k)"),
  ("<code>np.eye(k)[y] * (1 - eps) + eps / k</code>.", "O(n·k)", "O(n·k)"),
  names=["y", "k", "eps"])


@B
def smooth_labels(y, k, eps):
    return [[round((1.0 if c == label else 0.0) * (1 - eps) + eps / k, 4) for c in range(k)] for label in y]


@O
def smooth_labels(y, k, eps):
    return (np.eye(k)[y] * (1 - eps) + eps / k).round(4)


Q(None, "Early Stopping", "Medium", "Know when to stop",
  "Given validation losses, stop after patience epochs with no new best. Return (epoch to keep — the best so far, epoch where training stopped), counting from 0.",
  [(([1.0, 0.8, 0.7, 0.72, 0.71, 0.73, 0.6], 3), (2, 5)), (([1.0, 0.9, 0.8], 2), (2, 2))],
  ("Track the best and a counter.", "O(n)", "O(1)"),
  ("<code>np.minimum.accumulate</code> shows where new bests happen.", "O(n)", "O(n)"),
  names=["losses", "patience"])


@B
def early_stop(losses, patience):
    best, best_epoch, waited = float("inf"), 0, 0
    for e, loss in enumerate(losses):
        if loss < best:
            best, best_epoch, waited = loss, e, 0
        else:
            waited += 1
            if waited >= patience:
                return (best_epoch, e)
    return (best_epoch, len(losses) - 1)


@O
def early_stop(losses, patience):
    x = np.array(losses)
    prior = np.r_[np.inf, np.minimum.accumulate(x)[:-1]]
    new_best = np.flatnonzero(x < prior)
    for a, b in zip(new_best, np.r_[new_best[1:], len(x)]):
        if b - a > patience:
            return (int(a), int(a + patience))
    return (int(new_best[-1]), len(x) - 1)


Q(None, "Smoothing a Loss Curve", "Easy", "EMA with bias correction",
  "Return the smoothed curve: s ← βs + (1 − β)x from s = 0, reported as s/(1 − βᵗ), rounded to 4 decimals.",
  [(([1.0, 0.0, 1.0], 0.5),  [1.0, 0.3333, 0.7143])],
  ("A loop.", "O(n)", "O(n)"),
  ("A weighted average of the values so far, with weights βᵏ.", "O(n²)", "O(n)"),
  names=["x", "beta"])


@B
def smooth_curve(x, beta):
    s, out = 0.0, []
    for t, v in enumerate(x, start=1):
        s = beta * s + (1 - beta) * v
        out.append(round(s / (1 - beta ** t), 4))
    return out


@O
def smooth_curve(x, beta):
    x = np.array(x, dtype=float)
    out = []
    for t in range(len(x)):
        weights = beta ** np.arange(t, -1, -1)
        out.append(round((x[:t + 1] * weights).sum() / weights.sum(), 4))
    return out


Q(None, "Gradient Accumulation", "Medium", "Big batch on a small GPU",
  "Gradients from equal-sized micro-batches are averaged before one update. Return the update's weights: w − lr·mean(grads), rounded to 4 decimals.",
  [(([1.0, 2.0], [[0.2, 0.4], [0.4, 0.8]], 0.5), [0.85, 1.7])],
  ("Add up gradients in loops, divide, then update.", "O(m·d)", "O(d)"),
  ("<code>np.mean(grads, axis=0)</code>.", "O(m·d)", "O(d)"),
  names=["w", "grads", "lr"])


@B
def accumulate(w, grads, lr):
    total = [0.0] * len(w)
    for g in grads:
        for i, v in enumerate(g):
            total[i] += v
    return [round(a - lr * t / len(grads), 4) for a, t in zip(w, total)]


@O
def accumulate(w, grads, lr):
    return (np.array(w) - lr * np.mean(grads, axis=0)).round(4)


Q(None, "Pick a Learning Rate From a Range Test", "Medium", "Steepest fall",
  "Losses were measured while raising the rate. Return the rate where the loss fell most compared with the previous point.",
  [(([1e-4, 1e-3, 1e-2, 1e-1, 1.0], [2.3, 2.25, 1.8, 1.0, 5.0]),  0.1)],
  ("Track the biggest drop in a loop.", "O(n)", "O(1)"),
  ("<code>np.diff(losses).argmin() + 1</code>.", "O(n)", "O(n)"),
  names=["rates", "losses"])


@B
def pick_rate(rates, losses):
    best_i, best_drop = 1, float("inf")
    for i in range(1, len(losses)):
        change = losses[i] - losses[i - 1]
        if change < best_drop:
            best_i, best_drop = i, change
    return rates[best_i]


@O
def pick_rate(rates, losses):
    return rates[int(np.diff(losses).argmin()) + 1]
