from lib import *
import math
import numpy as np


TOPIC(
    id="rnn", title="RNNs & Sequences", glyph="↻",
    blurb="Models with memory: the RNN cell, unrolling over time, vanishing gradients, LSTM and GRU cells by hand, padding and masks, teacher forcing and preparing sequence data.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">h = tanh(Wh @ h + Wx @ x + b)         # RNN step
f = sigmoid(...); i = sigmoid(...); o = sigmoid(...)
c = f * c + i * tanh(...)             # LSTM cell state
h = o * tanh(c)                       # LSTM output
inputs, targets = seq[:-1], seq[1:]   # next-item prediction</code></pre>
<p>PyTorch: <code>nn.LSTM(input_size, hidden_size, batch_first=True)</code>; <code>nn.Embedding</code>.</p>
""")

sig = lambda z: 1 / (1 + math.exp(-z))


Q(None, "One RNN Step", "Easy", "New memory from old memory",
  "Scalars: return tanh(w_h·h + w_x·x + b), rounded to 4 decimals.",
  [((0.5, 1.0, 0.8, 0.5, 0.1), 0.7616), ((0.0, 2.0, 0.8, 0.5, 0.0), 0.7616)],
  ("Compute inside, then tanh with exponentials.", "O(1)", "O(1)"),
  ("<code>np.tanh</code>.", "O(1)", "O(1)"),
  names=["h", "x", "w_h", "w_x", "b"])


@B
def rnn_step(h, x, w_h, w_x, b):
    z = w_h * h + w_x * x + b
    return round((math.exp(z) - math.exp(-z)) / (math.exp(z) + math.exp(-z)), 4)


@O
def rnn_step(h, x, w_h, w_x, b):
    return round(float(np.tanh(w_h * h + w_x * x + b)), 4)


Q(None, "Run an RNN Over a Sequence", "Easy", "Unrolling",
  "Start with h = 0 and return all hidden states, rounded to 4 decimals (b = 0).",
  [(([1.0, 0.0, -1.0], 0.5, 1.0), [0.7616, 0.3634, -0.6741])],
  ("A loop with exponentials for tanh.", "O(T)", "O(T)"),
  ("A loop with <code>np.tanh</code>; each step needs the previous one, so it can't be fully vectorised.", "O(T)", "O(T)"),
  names=["xs", "w_h", "w_x"])


@B
def rnn_run(xs, w_h, w_x):
    h, out = 0.0, []
    for x in xs:
        h = math.tanh(w_h * h + w_x * x)
        out.append(round(h, 4))
    return out


@O
def rnn_run(xs, w_h, w_x):
    h, out = 0.0, np.zeros(len(xs))
    for t, x in enumerate(xs):
        h = np.tanh(w_h * h + w_x * x)
        out[t] = h
    return out.round(4)


Q(None, "A Vector RNN Step", "Medium", "With matrices",
  "Return tanh(h·Wh + x·Wx + b), rounded to 4 decimals.",
  [(([0.5, -0.5], [1.0], [[0.5, 0.0], [0.0, 0.5]], [[1.0, -1.0]], [0.0, 0.1]), [0.8483, -0.8178])],
  ("Loops for each matrix product.", "O(h²)", "O(h)"),
  ("Matrix products with <code>@</code>.", "O(h²)", "O(h)"),
  names=["h", "x", "Wh", "Wx", "b"])


@B
def rnn_vector(h, x, Wh, Wx, b):
    out = []
    for k in range(len(b)):
        z = b[k]
        z += sum(h[i] * Wh[i][k] for i in range(len(h)))
        z += sum(x[i] * Wx[i][k] for i in range(len(x)))
        out.append(round(math.tanh(z), 4))
    return out


@O
def rnn_vector(h, x, Wh, Wx, b):
    return np.tanh(np.array(h) @ np.array(Wh) + np.array(x) @ np.array(Wx) + np.array(b)).round(4)


Q(None, "Parameters: RNN, GRU, LSTM", "Easy", "3, then 4 gates' worth",
  "For input size d and hidden size h, a cell has k·(d·h + h·h + h) parameters, with k = 1 (RNN), 3 (GRU), 4 (LSTM). Return all three as a tuple.",
  [((64, 128), (24704, 74112, 98816)), ((10, 20), (620, 1860, 2480))],
  ("Compute one block, then multiply three times.", "O(1)", "O(1)"),
  ("Vectorised over k.", "O(1)", "O(1)"),
  names=["d", "h"])


@B
def cell_params(d, h):
    one = d * h + h * h + h
    return (one, 3 * one, 4 * one)


@O
def cell_params(d, h):
    return tuple((np.array([1, 3, 4]) * (d * h + h * h + h)).tolist())


Q(None, "How Gradients Fade Through Time", "Easy", "wᵗ",
  "A signal passes through t steps, multiplied by w each time. Return the size left for each t in ts, rounded to 6 decimals.",
  [((0.9, [1, 10, 50]), [0.9, 0.3487, 0.0052]), ((1.1, [1, 10, 50]), [1.1, 2.5937, 117.3909])],
  ("Multiply in a loop for each t.", "O(k·T)", "O(k)"),
  ("<code>w ** np.array(ts)</code>.", "O(k)", "O(k)"),
  names=["w", "ts"])


@B
def fade(w, ts):
    out = []
    for t in ts:
        v = 1.0
        for _ in range(t):
            v *= w
        out.append(round(v, 6))
    return out


@O
def fade(w, ts):
    return (float(w) ** np.array(ts)).round(6)


Q(None, "Backprop Through Time", "Hard", "Chain over steps",
  "Linear RNN: h_t = w·h_{t−1} + x_t, h₀ = 0, loss = h_T. Return dL/dw, rounded to 4 decimals.",
  [((0.5, [1.0, 2.0, 3.0]), 3.0), ((1.0, [1.0, 1.0, 1.0, 1.0]), 6.0)],
  ("Numerical: nudge w and rerun the sequence.", "O(T)", "O(1)"),
  ("Forward: keep dh/dw alongside h: d ← h_prev + w·d.", "O(T)", "O(1)"),
  names=["w", "xs"])


@B
def bptt(w, xs):
    def run(weight):
        h = 0.0
        for x in xs:
            h = weight * h + x
        return h
    eps = 1e-6
    return round((run(w + eps) - run(w - eps)) / (2 * eps), 4)


@O
def bptt(w, xs):
    h, d = 0.0, 0.0
    for x in xs:
        d = h + w * d
        h = w * h + x
    return round(d, 4)


Q(None, "An LSTM Gate", "Easy", "A soft on/off switch",
  "A gate is σ(w_h·h + w_x·x + b). Return the gate value, and the kept part of c (gate × c), both rounded to 4 decimals.",
  [((0.5, 1.0, 1.0, 1.0, 0.0, 2.0), (0.8176, 1.6351)), ((0.5, 1.0, -3.0, -3.0, 0.0, 2.0), (0.011, 0.022))],
  ("Sigmoid with <code>math.exp</code>.", "O(1)", "O(1)"),
  ("<code>np.exp</code>.", "O(1)", "O(1)"),
  names=["h", "x", "w_h", "w_x", "b", "c"])


@B
def lstm_gate(h, x, w_h, w_x, b, c):
    g = 1 / (1 + math.exp(-(w_h * h + w_x * x + b)))
    return (round(g, 4), round(g * c, 4))


@O
def lstm_gate(h, x, w_h, w_x, b, c):
    g = 1 / (1 + np.exp(-(w_h * h + w_x * x + b)))
    return (round(float(g), 4), round(float(g * c), 4))


Q(None, "One LSTM Step", "Hard", "Forget, add, output",
  "Given gate values f, i, o, candidate z (before tanh), and old c: new c = f·c + i·tanh(z); new h = o·tanh(c). Return (h, c), rounded to 4 decimals.",
  [((0.9, 0.2, 0.5, 1.0, 2.0), (0.4802, 1.9523)), ((0.0, 1.0, 1.0, 0.5, 5.0), (0.4318, 0.4621))],
  ("Apply each equation in order with <code>math.tanh</code>.", "O(1)", "O(1)"),
  ("NumPy works the same, on whole vectors of cells.", "O(1)", "O(1)"),
  names=["f", "i", "o", "z", "c"])


@B
def lstm_step(f, i, o, z, c):
    c_new = f * c + i * math.tanh(z)
    h = o * math.tanh(c_new)
    return (round(h, 4), round(c_new, 4))


@O
def lstm_step(f, i, o, z, c):
    c_new = np.array(f) * c + np.array(i) * np.tanh(z)
    return (round(float(np.array(o) * np.tanh(c_new)), 4), round(float(c_new), 4))


Q(None, "Memory Across Many Steps", "Medium", "Why the cell state survives",
  "After T steps, an RNN's signal is ∏ w and an LSTM's is ∏ f. Return (w^T, f^T), rounded to 6 decimals.",
  [((0.5, 0.99, 20), (0.0, 0.8179)), ((0.9, 0.99, 100), (0.0, 0.366))],
  ("Multiply in a loop.", "O(T)", "O(1)"),
  ("Powers.", "O(1)", "O(1)"),
  names=["w", "f", "T"])


@B
def memory_compare(w, f, T):
    a = b = 1.0
    for _ in range(T):
        a *= w
        b *= f
    return (round(a, 6), round(b, 6))


@O
def memory_compare(w, f, T):
    return (round(w ** T, 6), round(f ** T, 6))


Q(None, "One GRU Step", "Hard", "A simpler LSTM",
  "Given update gate u and candidate z (before tanh): new h = (1 − u)·h + u·tanh(z). Round to 4 decimals.",
  [((0.5, 0.2, 1.0), 0.4808), ((0.0, 0.2, 1.0), 0.2), ((1.0, 0.2, 1.0), 0.7616)],
  ("Apply the blend with <code>math.tanh</code>.", "O(1)", "O(1)"),
  ("<code>np.interp</code>-style blend with NumPy.", "O(1)", "O(1)"),
  names=["u", "h", "z"])


@B
def gru_step(u, h, z):
    return round((1 - u) * h + u * math.tanh(z), 4)


@O
def gru_step(u, h, z):
    return round(float(np.dot([1 - u, u], [h, np.tanh(z)])), 4)


Q(None, "Pad a Batch of Sequences", "Easy", "Same length for a tensor",
  "Pad each list on the right with 0 up to the longest length.",
  [(([[5, 2, 9], [7], [3, 3]],), [[5, 2, 9], [7, 0, 0], [3, 3, 0]])],
  ("Add zeros in a loop.", "O(n·T)", "O(n·T)"),
  ("Fill a zero matrix.", "O(n·T)", "O(n·T)"))


@B
def pad(seqs):
    longest = max(len(s) for s in seqs)
    return [s + [0] * (longest - len(s)) for s in seqs]


@O
def pad(seqs):
    out = np.zeros((len(seqs), max(map(len, seqs))), dtype=int)
    for i, s in enumerate(seqs):
        out[i, :len(s)] = s
    return out


Q(None, "Mask From Lengths", "Easy", "1 for real, 0 for padding",
  "Return a 0/1 matrix with lengths[i] ones in row i, then zeros, up to the longest length.",
  [(([3, 1, 2],), [[1, 1, 1], [1, 0, 0], [1, 1, 0]])],
  ("Build each row in a loop.", "O(n·T)", "O(n·T)"),
  ("Compare <code>np.arange(T)</code> with lengths[:, None].", "O(n·T)", "O(n·T)"))


@B
def mask_from_lengths(lengths):
    T = max(lengths)
    return [[1] * n + [0] * (T - n) for n in lengths]


@O
def mask_from_lengths(lengths):
    n = np.array(lengths)
    return (np.arange(n.max()) < n[:, None]).astype(int)


Q(None, "Masked Average Loss", "Medium", "Ignore padding",
  "Average per-position losses only where the mask is 1, rounded to 4 decimals.",
  [(([[1.0, 2.0, 9.0], [3.0, 9.0, 9.0]], [[1, 1, 0], [1, 0, 0]]), 2.0)],
  ("Add up masked losses and count them.", "O(n·T)", "O(1)"),
  ("<code>(loss * mask).sum() / mask.sum()</code>.", "O(n·T)", "O(n·T)"),
  names=["loss", "mask"])


@B
def masked_loss(loss, mask):
    total, count = 0.0, 0
    for r1, r2 in zip(loss, mask):
        for l, m in zip(r1, r2):
            if m:
                total += l
                count += 1
    return round(total / count, 4)


@O
def masked_loss(loss, mask):
    loss, mask = np.array(loss), np.array(mask)
    return round((loss * mask).sum() / mask.sum(), 4)


Q(None, "Last Real Output of Each Sequence", "Medium", "Not the padding",
  "outputs is a table with one row per sequence, one value per step. Return each sequence's output at its last real position.",
  [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [3, 1, 2]), [3, 4, 8])],
  ("Loop with index lengths[i] − 1.", "O(n)", "O(n)"),
  ("<code>outputs[np.arange(n), lengths - 1]</code>.", "O(n)", "O(n)"),
  names=["outputs", "lengths"])


@B
def last_real(outputs, lengths):
    return [row[n - 1] for row, n in zip(outputs, lengths)]


@O
def last_real(outputs, lengths):
    o, n = np.array(outputs), np.array(lengths)
    return o[np.arange(len(o)), n - 1]


Q(None, "Bidirectional States", "Medium", "Read both ways",
  "Run a scalar RNN (h = tanh(0.5h + x)) forward and backward over xs. Return per-position pairs (forward h, backward h), rounded to 4 decimals.",
  [(([1.0, 0.0, -1.0],), [[0.7616, 0.6741], [0.3634, -0.3634], [-0.6741, -0.7616]])],
  ("Two loops, reversing the second's output.", "O(T)", "O(T)"),
  ("A helper run twice with NumPy, then <code>np.column_stack</code>.", "O(T)", "O(T)"))


@B
def bidirectional(xs):
    h, forward = 0.0, []
    for x in xs:
        h = math.tanh(0.5 * h + x)
        forward.append(h)
    h, backward = 0.0, []
    for x in reversed(xs):
        h = math.tanh(0.5 * h + x)
        backward.append(h)
    backward.reverse()
    return [[round(a, 4), round(b, 4)] for a, b in zip(forward, backward)]


@O
def bidirectional(xs):
    def run(values):
        out, h = [], 0.0
        for x in values:
            h = np.tanh(0.5 * h + x)
            out.append(h)
        return np.array(out)
    return np.column_stack([run(xs), run(xs[::-1])[::-1]]).round(4)


Q(None, "Sliding Windows for Forecasting", "Easy", "Turning a series into examples",
  "Return (X, y): each X row holds n consecutive values and y is the value after them.",
  [(([1, 2, 3, 4, 5], 2), ([[1, 2], [2, 3], [3, 4]], [3, 4, 5]))],
  ("Loop over start positions.", "O(T·n)", "O(T·n)"),
  ("<code>sliding_window_view</code>.", "O(T·n)", "O(T·n)"),
  names=["series", "n"])


@B
def windows(series, n):
    X, y = [], []
    for i in range(len(series) - n):
        X.append(series[i:i + n])
        y.append(series[i + n])
    return (X, y)


@O
def windows(series, n):
    s = np.array(series)
    return (np.lib.stride_tricks.sliding_window_view(s, n)[:-1], s[n:])


Q(None, "Teacher Forcing Targets", "Easy", "Predict the next token",
  "For a token list, return (inputs, targets): inputs drop the last, targets drop the first. Every language model is trained like this.",
  [(([5, 8, 2, 9],), ([5, 8, 2], [8, 2, 9]))],
  ("Slices of a list.", "O(T)", "O(T)"),
  ("Slices of an array, which works on whole batches with <code>[:, :-1]</code>.", "O(1)", "O(1)"))


@B
def shift(tokens):
    return (tokens[:-1], tokens[1:])


@O
def shift(tokens):
    t = np.array(tokens)
    return (t[:-1], t[1:])


Q(None, "Truncated BPTT Chunks", "Medium", "Long sequences in pieces",
  "Split the sequence into chunks of size k; drop a short leftover. Return the chunks.",
  [((list(range(10)), 3), [[0, 1, 2], [3, 4, 5], [6, 7, 8]]), (([1, 2, 3, 4], 2), [[1, 2], [3, 4]])],
  ("Step through with slices.", "O(T)", "O(T)"),
  ("Trim, then <code>reshape(-1, k)</code>.", "O(T)", "O(1) view"),
  names=["seq", "k"])


@B
def chunks(seq, k):
    return [seq[i:i + k] for i in range(0, len(seq) - k + 1, k)]


@O
def chunks(seq, k):
    s = np.array(seq)
    return s[:len(s) // k * k].reshape(-1, k)


Q(None, "Encode, Decode With a Vocabulary", "Easy", "Text ↔ numbers",
  "Build a character vocabulary from text (sorted unique characters). Return (ids of the text, the text decoded back).",
  [(("hello",), ([1, 0, 2, 2, 3], 'hello'))],
  ("Dictionaries both ways.", "O(n log n)", "O(k)"),
  ("<code>np.unique(..., return_inverse=True)</code> gives both directly.", "O(n log n)", "O(n)"))


@B
def encode_decode(text):
    chars = sorted(set(text))
    to_id = {c: i for i, c in enumerate(chars)}
    ids = [to_id[c] for c in text]
    return (ids, "".join(chars[i] for i in ids))


@O
def encode_decode(text):
    chars, ids = np.unique(list(text), return_inverse=True)
    return (ids.ravel(), "".join(chars[ids.ravel()]))


Q(None, "Average of the Real States", "Medium", "Mean pooling over time",
  "states has one row per step, and each row is a vector. Average only the rows where the mask is 1. Round to 4 decimals.",
  [(([[1.0, 2.0], [3.0, 4.0], [100.0, 100.0]], [1, 1, 0]), [2.0, 3.0])],
  ("Add up masked rows in a loop.", "O(T·d)", "O(d)"),
  ("<code>states[mask == 1].mean(axis=0)</code>.", "O(T·d)", "O(T·d)"),
  names=["states", "mask"])


@B
def mean_pool(states, mask):
    total = [0.0] * len(states[0])
    count = 0
    for row, m in zip(states, mask):
        if m:
            count += 1
            for j, v in enumerate(row):
                total[j] += v
    return [round(v / count, 4) for v in total]


@O
def mean_pool(states, mask):
    return np.array(states)[np.array(mask) == 1].mean(axis=0).round(4)
