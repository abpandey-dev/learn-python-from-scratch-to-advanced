from lib import *
import math
import numpy as np


TOPIC(
    id="attention", title="Attention & Transformers", glyph="Q·Kᵀ",
    blurb="The idea behind every modern LLM: scaled dot-product attention by hand, masks, self- and cross-attention, multi-head attention, positional information and the full transformer block.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">scores = Q @ K.T / sqrt(d)                   # how much each query matches each key
scores[mask == 0] = -inf                     # hide what mustn't be seen
A = softmax(scores, axis=-1)                 # weights: each row sums to 1
out = A @ V                                  # weighted average of the values
mask = np.tril(np.ones((T, T)))              # causal mask</code></pre>
<p>PyTorch: <code>F.scaled_dot_product_attention</code>, <code>nn.MultiheadAttention</code>, <code>nn.TransformerEncoderLayer</code>.</p>
""")

X3 = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]


def softmax_rows(S):
    S = np.array(S, dtype=float)
    e = np.exp(S - S.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


Q(None, "Attention Scores", "Easy", "Query × key ÷ √d",
  "Return Q·Kᵀ/√d, where d is the vector size, rounded to 4 decimals.",
  [((X3, X3), [[0.7071, 0.0, 0.7071], [0.0, 0.7071, 0.7071], [0.7071, 0.7071, 1.4142]]), (([[1.0, 2.0]], [[3.0, 4.0], [1.0, 0.0]]), [[7.7782, 0.7071]])],
  ("Dot products in nested loops.", "O(q·k·d)", "O(q·k)"),
  ("<code>Q @ K.T / np.sqrt(d)</code>.", "O(q·k·d)", "O(q·k)"),
  names=["Q", "K"])


@B
def scores(Q, K):
    d = len(Q[0])
    return [[round(sum(a * b for a, b in zip(q, k)) / math.sqrt(d), 4) for k in K] for q in Q]


@O
def scores(Q, K):
    Q, K = np.array(Q), np.array(K)
    return (Q @ K.T / np.sqrt(Q.shape[1])).round(4)


Q(None, "Attention Weights", "Easy", "Softmax per query",
  "Softmax each row of a score table, rounded to 4 decimals.",
  [(([[0.7071, 0.0, 0.7071], [0.0, 0.0, 0.0]],), [[0.4011, 0.1978, 0.4011], [0.3333, 0.3333, 0.3333]])],
  ("Exponentiate and normalise in loops.", "O(q·k)", "O(q·k)"),
  ("Vectorised, shifting by the row max.", "O(q·k)", "O(q·k)"))


@B
def weights(S):
    out = []
    for row in S:
        e = [math.exp(v - max(row)) for v in row]
        out.append([round(v / sum(e), 4) for v in e])
    return out


@O
def weights(S):
    return softmax_rows(S).round(4)


Q(None, "Scaled Dot-Product Attention", "Medium", "The core formula",
  "Return softmax(Q·Kᵀ/√d)·V, rounded to 4 decimals.",
  [((X3, X3, X3), [[0.8022, 0.5989], [0.5989, 0.8022], [0.7517, 0.7517]]), (([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[10.0], [20.0]]), [[13.3024]])],
  ("Loops for scores, softmax and the weighted sum.", "O(q·k·d)", "O(q·d)"),
  ("Three matrix lines.", "O(q·k·d)", "O(q·k)"),
  names=["Q", "K", "V"])


@B
def attention(Q, K, V):
    d = len(Q[0])
    out = []
    for q in Q:
        s = [sum(a * b for a, b in zip(q, k)) / math.sqrt(d) for k in K]
        e = [math.exp(v - max(s)) for v in s]
        w = [v / sum(e) for v in e]
        out.append([round(sum(w[i] * V[i][j] for i in range(len(V))), 4) for j in range(len(V[0]))])
    return out


@O
def attention(Q, K, V):
    Q, K, V = np.array(Q), np.array(K), np.array(V)
    return (softmax_rows(Q @ K.T / np.sqrt(Q.shape[1])) @ V).round(4)


Q(None, "Soft Dictionary Lookup", "Easy", "The intuition in one dimension",
  "A dictionary has numeric keys and values. Weight each key by softmax(−(query − key)²), and return the weighted average of values, rounded to 4 decimals.",
  [((2.0, [1.0, 2.0, 3.0], [10.0, 20.0, 30.0]), 20.0), ((1.0, [1.0, 5.0], [10.0, 20.0]), 10.0)],
  ("Compute each weight in a loop.", "O(k)", "O(k)"),
  ("Vectorised.", "O(k)", "O(k)"),
  names=["q", "keys", "values"])


@B
def soft_lookup(q, keys, values):
    s = [-(q - k) ** 2 for k in keys]
    e = [math.exp(v) for v in s]
    return round(sum(a * v for a, v in zip(e, values)) / sum(e), 4)


@O
def soft_lookup(q, keys, values):
    s = -(q - np.array(keys)) ** 2
    w = np.exp(s) / np.exp(s).sum()
    return round(w @ np.array(values), 4)


Q(None, "Causal Mask", "Easy", "Can't look ahead",
  "Return a T × T table with 1 where position i may see position j (j ≤ i).",
  [((3,), [[1, 0, 0], [1, 1, 0], [1, 1, 1]])],
  ("Nested loops.", "O(T²)", "O(T²)"),
  ("<code>np.tril(np.ones((T, T), dtype=int))</code>.", "O(T²)", "O(T²)"))


@B
def causal_mask(T):
    return [[1 if j <= i else 0 for j in range(T)] for i in range(T)]


@O
def causal_mask(T):
    return np.tril(np.ones((T, T), dtype=int))


Q(None, "Masked Softmax", "Medium", "Hidden positions get zero",
  "Apply softmax per row, ignoring positions where the mask is 0. Round to 4 decimals.",
  [(([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], [[1, 0, 0], [1, 1, 0]]), [[1.0, 0.0, 0.0], [0.2689, 0.7311, 0.0]])],
  ("Only add up allowed entries.", "O(q·k)", "O(q·k)"),
  ("Set hidden scores to −∞; e^(−∞) is 0.", "O(q·k)", "O(q·k)"),
  names=["S", "mask"])


@B
def masked_softmax(S, mask):
    out = []
    for row, m in zip(S, mask):
        e = [math.exp(v) if flag else 0.0 for v, flag in zip(row, m)]
        out.append([round(v / sum(e), 4) for v in e])
    return out


@O
def masked_softmax(S, mask):
    S = np.where(np.array(mask) == 1, np.array(S, dtype=float), -np.inf)
    return softmax_rows(S).round(4)


Q(None, "Padding Plus Causal Mask", "Medium", "Both rules together",
  "Given a padding mask per position (1 = real), return the T × T mask: allowed only if j ≤ i and position j is real.",
  [(([1, 1, 0],), [[1, 0, 0], [1, 1, 0], [1, 1, 0]])],
  ("Nested loops.", "O(T²)", "O(T²)"),
  ("<code>np.tril(ones) * pad[None, :]</code>.", "O(T²)", "O(T²)"))


@B
def combined_mask(pad):
    T = len(pad)
    return [[1 if j <= i and pad[j] else 0 for j in range(T)] for i in range(T)]


@O
def combined_mask(pad):
    pad = np.array(pad)
    return np.tril(np.ones((len(pad), len(pad)), dtype=int)) * pad[None, :]


Q(None, "Masked Self-Attention", "Hard", "What a decoder does",
  "Compute self-attention (Q = K = V = X) with a causal mask, rounded to 4 decimals.",
  [((X3,), [[1.0, 0.0], [0.3302, 0.6698], [0.7517, 0.7517]])],
  ("Loops: each position only considers itself and earlier ones.", "O(T²·d)", "O(T·d)"),
  ("Scores + <code>np.tril</code> mask + softmax + matrix product.", "O(T²·d)", "O(T²)"))


@B
def causal_attention(X):
    d = len(X[0])
    out = []
    for i, q in enumerate(X):
        s = [sum(a * b for a, b in zip(q, X[j])) / math.sqrt(d) for j in range(i + 1)]
        e = [math.exp(v - max(s)) for v in s]
        w = [v / sum(e) for v in e]
        out.append([round(sum(w[j] * X[j][c] for j in range(i + 1)), 4) for c in range(d)])
    return out


@O
def causal_attention(X):
    X = np.array(X)
    S = X @ X.T / np.sqrt(X.shape[1])
    S = np.where(np.tril(np.ones_like(S)) == 1, S, -np.inf)
    return (softmax_rows(S) @ X).round(4)


Q(None, "Self-Attention With Learned Projections", "Medium", "Q, K and V from X",
  "Compute Q = X·Wq, K = X·Wk, V = X·Wv, then attention, rounded to 4 decimals.",
  [(([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [[0.0, 1.0], [1.0, 0.0]], [[2.0], [3.0]]), [[2.6698], [2.3302]])],
  ("Loops for each projection.", "O(T²·d)", "O(T·d)"),
  ("Matrix products.", "O(T²·d)", "O(T²)"),
  names=["X", "Wq", "Wk", "Wv"])


@B
def projected_attention(X, Wq, Wk, Wv):
    def mul(A, B):
        return [[sum(a * B[k][j] for k, a in enumerate(row)) for j in range(len(B[0]))] for row in A]

    Q, K, V = mul(X, Wq), mul(X, Wk), mul(X, Wv)
    d = len(Q[0])
    out = []
    for q in Q:
        s = [sum(a * b for a, b in zip(q, k)) / math.sqrt(d) for k in K]
        e = [math.exp(v - max(s)) for v in s]
        w = [v / sum(e) for v in e]
        out.append([round(sum(w[i] * V[i][c] for i in range(len(V))), 4) for c in range(len(V[0]))])
    return out


@O
def projected_attention(X, Wq, Wk, Wv):
    X = np.array(X)
    Q, K, V = X @ np.array(Wq), X @ np.array(Wk), X @ np.array(Wv)
    return (softmax_rows(Q @ K.T / np.sqrt(Q.shape[1])) @ V).round(4)


Q(None, "Split Into Heads", "Medium", "(T, d) → (h, T, d/h)",
  "Split each vector into h equal pieces, and return one table per head.",
  [(([[1, 2, 3, 4], [5, 6, 7, 8]], 2), [[[1, 2], [5, 6]], [[3, 4], [7, 8]]])],
  ("Loops over heads and rows.", "O(T·d)", "O(T·d)"),
  ("<code>reshape(T, h, -1).transpose(1, 0, 2)</code>.", "O(T·d)", "O(1) view"),
  names=["X", "h"])


@B
def split_heads(X, h):
    size = len(X[0]) // h
    return [[row[i * size:(i + 1) * size] for row in X] for i in range(h)]


@O
def split_heads(X, h):
    X = np.array(X)
    return X.reshape(len(X), h, -1).transpose(1, 0, 2)


Q(None, "Merge Heads", "Easy", "Back together",
  "Given one table per head, concatenate each position's pieces.",
  [(([[[1, 2], [5, 6]], [[3, 4], [7, 8]]],), [[1, 2, 3, 4], [5, 6, 7, 8]])],
  ("Loop and extend.", "O(T·d)", "O(T·d)"),
  ("<code>np.concatenate(heads, axis=-1)</code>.", "O(T·d)", "O(T·d)"))


@B
def merge_heads(heads):
    out = []
    for i in range(len(heads[0])):
        row = []
        for head in heads:
            row.extend(head[i])
        out.append(row)
    return out


@O
def merge_heads(heads):
    return np.concatenate(heads, axis=-1)


Q(None, "Multi-Head Parameters", "Medium", "Cost of attention",
  "With d_model = d, a multi-head layer has 4 linear maps (Q, K, V, output), each d × d, with no bias. Return its parameter count, and each head's size d/h.",
  [((512, 8), (1048576, 64)), ((768, 12), (2359296, 64))],
  ("Add up the four maps.", "O(1)", "O(1)"),
  ("A formula.", "O(1)", "O(1)"),
  names=["d", "h"])


@B
def mha_params(d, h):
    total = 0
    for _ in range(4):
        total += d * d
    return (total, d // h)


@O
def mha_params(d, h):
    return (4 * d ** 2, d // h)


Q(None, "Transformer Block Parameters", "Medium", "Where the size goes",
  "A block has attention (4d²), a feed-forward with hidden size 4d (each of two layers with bias), and two layer norms (2d each). Return its parameter count.",
  [((512,), 3150336), ((768,), 7084800)],
  ("Add each part.", "O(1)", "O(1)"),
  ("Add the same parts with <code>np.sum</code>; altogether 12d² + 9d.", "O(1)", "O(1)"))


@B
def block_params(d):
    attention_part = 4 * d * d
    ff_1 = d * 4 * d + 4 * d
    ff_2 = 4 * d * d + d
    norms = 2 * (2 * d)
    return attention_part + ff_1 + ff_2 + norms


@O
def block_params(d):
    return int(np.sum([4 * d ** 2, 4 * d ** 2 + 4 * d, 4 * d ** 2 + d, 4 * d]))


Q(None, "Position-Wise Feed-Forward", "Medium", "The same small network at every position",
  "Return ReLU(X·W1 + b1)·W2 + b2 for each position, rounded to 4 decimals.",
  [(([[1.0, 2.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, -1.0], [[1.0, 1.0], [1.0, -1.0]], [0.5, 0.5]), [[2.5, 0.5], [0.5, 0.5]])],
  ("A loop over each position.", "O(T·d²)", "O(T·d)"),
  ("Matrix products cover all positions at once.", "O(T·d²)", "O(T·d)"),
  names=["X", "W1", "b1", "W2", "b2"])


@B
def feed_forward(X, W1, b1, W2, b2):
    out = []
    for row in X:
        h = [max(0.0, b1[k] + sum(row[i] * W1[i][k] for i in range(len(row)))) for k in range(len(b1))]
        out.append([round(b2[k] + sum(h[i] * W2[i][k] for i in range(len(h))), 4) for k in range(len(b2))])
    return out


@O
def feed_forward(X, W1, b1, W2, b2):
    H = np.maximum(0, np.array(X) @ np.array(W1) + np.array(b1))
    return (H @ np.array(W2) + np.array(b2)).round(4)


Q(None, "Add and Norm", "Medium", "Residual + layer norm",
  "Return LayerNorm(x + sublayer) per row (population variance, ε = 1e-5), rounded to 4 decimals.",
  [(([[1.0, 2.0]], [[1.0, 0.0]]), [[0.0, 0.0]]), (([[1.0, 2.0, 3.0]], [[0.0, 0.0, 0.0]]), [[-1.2247, 0.0, 1.2247]])],
  ("Add, then normalise in loops.", "O(T·d)", "O(T·d)"),
  ("Vectorised.", "O(T·d)", "O(T·d)"),
  names=["x", "sub"])


@B
def add_norm(x, sub):
    out = []
    for r1, r2 in zip(x, sub):
        s = [a + b for a, b in zip(r1, r2)]
        mean = sum(s) / len(s)
        var = sum((v - mean) ** 2 for v in s) / len(s)
        out.append([round((v - mean) / math.sqrt(var + 1e-5), 4) + 0.0 for v in s])
    return out


@O
def add_norm(x, sub):
    s = np.array(x) + np.array(sub)
    return ((s - s.mean(axis=1, keepdims=True)) / np.sqrt(s.var(axis=1, keepdims=True) + 1e-5)).round(4) + 0.0


Q(None, "Cross-Attention", "Medium", "Decoder asks, encoder answers",
  "Queries come from Dq; keys and values from the encoder output E. Return attention results, rounded to 4 decimals.",
  [(([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]), [[0.8022, 0.5989]])],
  ("Loops as in attention, with different sources.", "O(q·k·d)", "O(q·d)"),
  ("Matrix form.", "O(q·k·d)", "O(q·k)"),
  names=["Dq", "E"])


@B
def cross_attention(Dq, E):
    d = len(Dq[0])
    out = []
    for q in Dq:
        s = [sum(a * b for a, b in zip(q, k)) / math.sqrt(d) for k in E]
        e = [math.exp(v - max(s)) for v in s]
        w = [v / sum(e) for v in e]
        out.append([round(sum(w[i] * E[i][c] for i in range(len(E))), 4) for c in range(d)])
    return out


@O
def cross_attention(Dq, E):
    Dq, E = np.array(Dq), np.array(E)
    return (softmax_rows(Dq @ E.T / np.sqrt(Dq.shape[1])) @ E).round(4)


Q(None, "Add Positions to Embeddings", "Easy", "Learned positions",
  "Return token embeddings + position embeddings (position table P indexed 0, 1, 2…).",
  [(([[1.0, 1.0], [2.0, 2.0]], [[0.1, 0.0], [0.2, 0.0], [0.3, 0.0]]), [[1.1, 1.0], [2.2, 2.0]])],
  ("Add row by row.", "O(T·d)", "O(T·d)"),
  ("<code>E + P[:len(E)]</code>.", "O(T·d)", "O(T·d)"),
  names=["E", "P"])


@B
def add_positions(E, P):
    return [[round(a + b, 4) for a, b in zip(e, P[i])] for i, e in enumerate(E)]


@O
def add_positions(E, P):
    return (np.array(E) + np.array(P)[:len(E)]).round(4)


Q(None, "Which Token Was Attended?", "Easy", "Reading the weights",
  "For each row of attention weights, return the token with the largest weight.",
  [(([[0.1, 0.7, 0.2], [0.8, 0.1, 0.1]], ["the", "cat", "sat"]), ['cat', 'the'])],
  ("Find each row's maximum.", "O(q·k)", "O(q)"),
  ("<code>A.argmax(axis=1)</code>.", "O(q·k)", "O(q)"),
  names=["A", "tokens"])


@B
def attended(A, tokens):
    return [tokens[row.index(max(row))] for row in A]


@O
def attended(A, tokens):
    return [tokens[i] for i in np.array(A).argmax(axis=1)]


Q(None, "Attention Cost vs Length", "Easy", "Why long inputs are expensive",
  "Attention compares every position with every position. Return T² for each length, and how many times bigger each is than the first.",
  [(([100, 1000, 4000],), ([10000, 1000000, 16000000], [1.0, 100.0, 1600.0]))],
  ("Square and divide in a loop.", "O(n)", "O(n)"),
  ("Vectorised.", "O(n)", "O(n)"))


@B
def attention_cost(lengths):
    squares = [t * t for t in lengths]
    return (squares, [s / squares[0] for s in squares])


@O
def attention_cost(lengths):
    s = np.array(lengths) ** 2
    return (s, s / s[0])


Q(None, "Weight Tying Savings", "Easy", "Input and output share a table",
  "A model's output layer can reuse its embedding table. Return (parameters saved, MB saved at 4 bytes), for a vocabulary and dimension (MB to 1 decimal, 1 MB = 10⁶ bytes).",
  [((50000, 768), (38400000, 153.6))],
  ("Multiply.", "O(1)", "O(1)"),
  ("<code>np.prod</code>.", "O(1)", "O(1)"),
  names=["vocab", "d"])


@B
def tying_savings(vocab, d):
    saved = vocab * d
    return (saved, round(saved * 4 / 1e6, 1))


@O
def tying_savings(vocab, d):
    saved = int(np.prod([vocab, d]))
    return (saved, round(saved * 4 / 1e6, 1))
