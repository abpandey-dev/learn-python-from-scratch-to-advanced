from lib import *
import math
import numpy as np


TOPIC(
    id="language-models", title="Language Models", glyph="P(next)",
    blurb="How an LLM predicts and generates: bigram models by hand, perplexity, the shifted cross-entropy loss, temperature, top-k, top-p, beam search, repetition penalties and the KV cache.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">x, y = tokens[:-1], tokens[1:]              # train on the next token
loss = cross_entropy(model(x), y)
probs = softmax(logits / temperature)       # generation
next_id = np.random.choice(len(probs), p=probs)
tokens.append(next_id)                      # repeat</code></pre>
""")

TOK = ["the", "cat", "sat", "the", "cat", "ran", "the", "dog", "ran"]


def softmax(z):
    z = np.array(z, dtype=float)
    e = np.exp(z - z.max())
    return e / e.sum()


Q(None, "Bigram Counts", "Easy", "What follows what",
  "Return {previous: {next: count}} with both levels in sorted key order.",
  [((TOK,), {'cat': {'ran': 1, 'sat': 1}, 'dog': {'ran': 1}, 'ran': {'the': 1}, 'sat': {'the': 1}, 'the': {'cat': 2, 'dog': 1}})],
  ("Nested dictionaries.", "O(n log n)", "O(pairs)"),
  ("<code>Counter(zip(t, t[1:]))</code>, then reshape.", "O(n log n)", "O(pairs)"))


@B
def bigram_counts(tokens):
    table = {}
    for a, b in zip(tokens, tokens[1:]):
        if a not in table:
            table[a] = {}
        table[a][b] = table[a].get(b, 0) + 1
    return {a: dict(sorted(table[a].items())) for a in sorted(table)}


@O
def bigram_counts(tokens):
    from collections import Counter
    out = {}
    for (a, b), c in sorted(Counter(zip(tokens, tokens[1:])).items()):
        out.setdefault(a, {})[b] = c
    return out


Q(None, "Bigram Probability With Smoothing", "Easy", "Unseen pairs aren't impossible",
  "Return (count(prev, next) + k) / (count(prev as a previous word) + k·V), where V is the number of distinct tokens. Round to 4 decimals.",
  [((TOK, "the", "cat", 0), 0.6667), ((TOK, "the", "ran", 0), 0.0), ((TOK, "the", "ran", 1), 0.125)],
  ("Count pairs in a loop.", "O(n)", "O(V)"),
  ("NumPy comparisons on arrays of neighbours.", "O(n)", "O(n)"),
  names=["tokens", "prev", "next_", "k"])


@B
def bigram_prob(tokens, prev, next_, k):
    pair = sum(1 for a, b in zip(tokens, tokens[1:]) if a == prev and b == next_)
    total = sum(1 for a in tokens[:-1] if a == prev)
    return round((pair + k) / (total + k * len(set(tokens))), 4)


@O
def bigram_prob(tokens, prev, next_, k):
    t = np.array(tokens)
    first = t[:-1] == prev
    return round(float((first & (t[1:] == next_)).sum() + k) / (first.sum() + k * len(set(tokens))), 4)


Q(None, "Log-Probability of a Sentence", "Medium", "Add logs, don't multiply",
  "Given bigram probabilities for each step, return (the product, the sum of natural logs), rounded to 6 and 4 decimals. Long products underflow; sums of logs don't.",
  [(([0.5, 0.25, 0.8],), (0.1, -2.3026)), (([0.1, 0.1, 0.1, 0.1],), (0.0001, -9.2103))],
  ("Two loops.", "O(n)", "O(1)"),
  ("<code>np.prod</code> and <code>np.log(...).sum()</code>.", "O(n)", "O(n)"))


@B
def sentence_logprob(probs):
    product, total = 1.0, 0.0
    for p in probs:
        product *= p
        total += math.log(p)
    return (round(product, 6), round(total, 4))


@O
def sentence_logprob(probs):
    p = np.array(probs)
    return (round(float(p.prod()), 6), round(float(np.log(p).sum()), 4))


Q(None, "Perplexity", "Easy", "The effective number of choices",
  "Perplexity = exp(average negative log probability of the true tokens). Round to 4 decimals.",
  [(([0.25, 0.25, 0.25],), 4.0), (([0.5, 0.125],), 4.0), (([1.0, 1.0],), 1.0)],
  ("Average in a loop, then <code>math.exp</code>.", "O(n)", "O(1)"),
  ("<code>np.exp(-np.log(p).mean())</code>.", "O(n)", "O(n)"))


@B
def perplexity(probs):
    total = 0.0
    for p in probs:
        total -= math.log(p)
    return round(math.exp(total / len(probs)), 4)


@O
def perplexity(probs):
    return round(float(np.exp(-np.log(probs).mean())), 4)


Q(None, "Next-Token Cross-Entropy", "Medium", "The loss of every LLM",
  "logits has one row per position. Return the mean of −ln softmax(row)[target], rounded to 4 decimals.",
  [(([[2.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [0, 1]), 0.3955), (([[0.0, 0.0, 0.0, 0.0]], [2]), 1.3863)],
  ("Softmax each row in a loop.", "O(T·V)", "O(V)"),
  ("Shift by max, index with <code>[np.arange(T), targets]</code>.", "O(T·V)", "O(T·V)"),
  names=["logits", "targets"])


@B
def lm_loss(logits, targets):
    total = 0.0
    for row, t in zip(logits, targets):
        e = [math.exp(v) for v in row]
        total -= math.log(e[t] / sum(e))
    return round(total / len(targets), 4)


@O
def lm_loss(logits, targets):
    L = np.array(logits, dtype=float)
    L = L - L.max(axis=1, keepdims=True)
    log_p = L - np.log(np.exp(L).sum(axis=1, keepdims=True))
    return round(float(-log_p[np.arange(len(L)), targets].mean()), 4)


Q(None, "Ignore Padding in the Loss", "Medium", "ignore_index = −100",
  "Same as above, but skip positions whose target is −100. Round to 4 decimals.",
  [(([[2.0, 0.0], [0.0, 3.0], [9.0, 0.0]], [0, 1, -100]), 0.0878)],
  ("Skip with an if.", "O(T·V)", "O(V)"),
  ("Boolean mask on targets.", "O(T·V)", "O(T·V)"),
  names=["logits", "targets"])


@B
def lm_loss_masked(logits, targets):
    total, count = 0.0, 0
    for row, t in zip(logits, targets):
        if t == -100:
            continue
        e = [math.exp(v) for v in row]
        total -= math.log(e[t] / sum(e))
        count += 1
    return round(total / count, 4)


@O
def lm_loss_masked(logits, targets):
    L, y = np.array(logits, dtype=float), np.array(targets)
    keep = y != -100
    L, y = L[keep], y[keep]
    log_p = L - np.log(np.exp(L).sum(axis=1, keepdims=True))
    return round(float(-log_p[np.arange(len(L)), y].mean()), 4)


Q(None, "Make a Training Batch", "Easy", "Random windows from a long text",
  "Given token ids, start offsets and block size, return (x, y), where y is x shifted by one.",
  [((list(range(10, 20)), [0, 5], 3), ([[10, 11, 12], [15, 16, 17]], [[11, 12, 13], [16, 17, 18]]))],
  ("Slice in a loop.", "O(n·b)", "O(n·b)"),
  ("Index an array with a broadcast grid.", "O(n·b)", "O(n·b)"),
  names=["data", "offsets", "block"])


@B
def get_batch(data, offsets, block):
    x = [data[i:i + block] for i in offsets]
    y = [data[i + 1:i + block + 1] for i in offsets]
    return (x, y)


@O
def get_batch(data, offsets, block):
    d = np.array(data)
    grid = np.array(offsets)[:, None] + np.arange(block)
    return (d[grid], d[grid + 1])


Q(None, "One Learning Step on Logits", "Medium", "Neural bigram",
  "With softmax and cross-entropy, the update for a row of logits is logits + lr·(one_hot(target) − probs). Return the new logits, rounded to 4 decimals.",
  [(([0.0, 0.0], 0, 1.0), [0.5, -0.5]), (([1.0, 0.0, -1.0], 2, 0.5), [0.6674, -0.1224, -0.545])],
  ("Softmax in a loop, then update each entry.", "O(V)", "O(V)"),
  ("<code>np.eye(V)[target]</code>.", "O(V)", "O(V)"),
  names=["logits", "target", "lr"])


@B
def learn_step(logits, target, lr):
    e = [math.exp(v) for v in logits]
    probs = [v / sum(e) for v in e]
    return [round(v + lr * ((1 if i == target else 0) - probs[i]), 4) for i, v in enumerate(logits)]


@O
def learn_step(logits, target, lr):
    return (np.array(logits) + lr * (np.eye(len(logits))[target] - softmax(logits))).round(4)


Q(None, "Backoff When a Pair Is Unseen", "Medium", "Fall back on the single word",
  "If the bigram (prev, w) was seen, return count(prev, w) / count(prev as previous). Otherwise return 0.4 × count(w) / number of tokens. Round to 4 decimals.",
  [((TOK, "the", "cat"), 0.6667), ((TOK, "dog", "cat"), 0.0889)],
  ("Count with loops.", "O(n)", "O(1)"),
  ("<code>Counter</code>s for pairs and words.", "O(n)", "O(V)"),
  names=["tokens", "prev", "w"])


@B
def backoff(tokens, prev, w):
    pair = 0
    total = 0
    for a, b in zip(tokens, tokens[1:]):
        if a == prev:
            total += 1
            if b == w:
                pair += 1
    if pair:
        return round(pair / total, 4)
    return round(0.4 * tokens.count(w) / len(tokens), 4)


@O
def backoff(tokens, prev, w):
    from collections import Counter
    pairs, firsts = Counter(zip(tokens, tokens[1:])), Counter(tokens[:-1])
    if pairs[(prev, w)]:
        return round(pairs[(prev, w)] / firsts[prev], 4)
    return round(0.4 * Counter(tokens)[w] / len(tokens), 4)


Q(None, "Temperature", "Easy", "Cautious or adventurous",
  "Return softmax(logits / T), rounded to 4 decimals.",
  [(([2.0, 1.0, 0.0], 1.0), [0.6652, 0.2447, 0.09]), (([2.0, 1.0, 0.0], 0.5), [0.8668, 0.1173, 0.0159]), (([2.0, 1.0, 0.0], 2.0), [0.5065, 0.3072, 0.1863])],
  ("Divide, exponentiate, normalise in loops.", "O(V)", "O(V)"),
  ("Vectorised.", "O(V)", "O(V)"),
  names=["logits", "T"])


@B
def with_temperature(logits, T):
    e = [math.exp(v / T) for v in logits]
    return [round(v / sum(e), 4) for v in e]


@O
def with_temperature(logits, T):
    return softmax(np.array(logits) / T).round(4)


Q(None, "Top-k Filtering", "Easy", "Keep the best k",
  "Set all but the k largest probabilities to 0, then renormalise. Round to 4 decimals.",
  [(([0.5, 0.2, 0.2, 0.1], 1), [1.0, 0.0, 0.0, 0.0]), (([0.4, 0.3, 0.2, 0.1], 2), [0.5714, 0.4286, 0.0, 0.0])],
  ("Sort indices, zero the rest.", "O(V log V)", "O(V)"),
  ("<code>np.argpartition</code> finds them in linear time.", "O(V)", "O(V)"),
  names=["probs", "k"])


@B
def top_k(probs, k):
    order = sorted(range(len(probs)), key=lambda i: -probs[i])[:k]
    kept = [probs[i] if i in order else 0.0 for i in range(len(probs))]
    return [round(v / sum(kept), 4) for v in kept]


@O
def top_k(probs, k):
    p = np.array(probs)
    out = np.zeros_like(p)
    keep = np.argpartition(-p, k - 1)[:k]
    out[keep] = p[keep]
    return (out / out.sum()).round(4)


Q(None, "Top-p (Nucleus) Filtering", "Medium", "Keep enough to reach p",
  "Keep the smallest set of most-likely tokens whose total probability is at least p, then renormalise. Round to 4 decimals.",
  [(([0.5, 0.3, 0.15, 0.05], 0.75), [0.625, 0.375, 0.0, 0.0]), (([0.9, 0.05, 0.05], 0.5), [1.0, 0.0, 0.0])],
  ("Sort, then add up in a loop until reaching p.", "O(V log V)", "O(V)"),
  ("<code>np.cumsum</code> + <code>np.searchsorted</code>.", "O(V log V)", "O(V)"),
  names=["probs", "p"])


@B
def top_p(probs, p):
    order = sorted(range(len(probs)), key=lambda i: -probs[i])
    kept, total = [0.0] * len(probs), 0.0
    for i in order:
        kept[i] = probs[i]
        total += probs[i]
        if total >= p:
            break
    return [round(v / sum(kept), 4) for v in kept]


@O
def top_p(probs, p):
    probs = np.array(probs)
    order = np.argsort(-probs)
    n = np.searchsorted(np.cumsum(probs[order]), p) + 1
    out = np.zeros_like(probs)
    out[order[:n]] = probs[order[:n]]
    return (out / out.sum()).round(4)


Q(None, "Sampling With a Random Number", "Easy", "How a choice is actually made",
  "Given probabilities and u in [0, 1), return the first index where the running total exceeds u.",
  [(([0.5, 0.3, 0.2], 0.1), 0), (([0.5, 0.3, 0.2], 0.6), 1), (([0.5, 0.3, 0.2], 0.95), 2)],
  ("Add up in a loop.", "O(V)", "O(1)"),
  ("<code>np.searchsorted(np.cumsum(p), u, side='right')</code>.", "O(V)", "O(V)"),
  names=["probs", "u"])


@B
def sample_index(probs, u):
    total = 0.0
    for i, p in enumerate(probs):
        total += p
        if total > u:
            return i
    return len(probs) - 1


@O
def sample_index(probs, u):
    return int(np.searchsorted(np.cumsum(probs), u, side="right"))


GRAPH = {"s": {"x": 0.6, "y": 0.4}, "x": {"a": 0.5, "b": 0.5}, "y": {"c": 0.9, "d": 0.1}}


Q(None, "Greedy Generation", "Medium", "Always the top choice",
  "Starting at start, repeatedly take the most likely next token, for the given number of steps. Return (path, total probability rounded to 4 decimals). Ties go to the first alphabetically.",
  [((GRAPH, "s", 2), (['s', 'x', 'a'], 0.3))],
  ("Loop and scan for the maximum.", "O(steps·V)", "O(steps)"),
  ("<code>min</code> with a sort key that handles ties.", "O(steps·V)", "O(steps)"),
  names=["graph", "start", "steps"])


@B
def greedy(graph, start, steps):
    path, prob, current = [start], 1.0, start
    for _ in range(steps):
        best, best_p = None, -1
        for token in sorted(graph[current]):
            if graph[current][token] > best_p:
                best, best_p = token, graph[current][token]
        path.append(best)
        prob *= best_p
        current = best
    return (path, round(prob, 4))


@O
def greedy(graph, start, steps):
    path, prob = [start], 1.0
    for _ in range(steps):
        options = graph[path[-1]]
        token = min(options, key=lambda t: (-options[t], t))
        prob *= options[token]
        path.append(token)
    return (path, round(prob, 4))


Q(None, "Beam Search", "Hard", "Keep several candidates",
  "Return (most likely path of the given number of steps, its probability rounded to 4 decimals), using beam width 2.",
  [((GRAPH, "s", 2), (['s', 'y', 'c'], 0.36))],
  ("Try every path. Fine for tiny graphs, but it grows exponentially.", "O(Vˢᵗᵉᵖˢ)", "O(steps)"),
  ("At each step, extend all candidates, and keep the best two.", "O(steps·width·V)", "O(width·steps)"),
  names=["graph", "start", "steps"])


@B
def beam(graph, start, steps):
    best_path, best_p = None, -1.0

    def walk(path, p):
        nonlocal best_path, best_p
        if len(path) == steps + 1:
            if p > best_p:
                best_path, best_p = path, p
            return
        for token, q in graph[path[-1]].items():
            walk(path + [token], p * q)

    walk([start], 1.0)
    return (best_path, round(best_p, 4))


@O
def beam(graph, start, steps):
    beams = [([start], 0.0)]
    for _ in range(steps):
        candidates = [(path + [t], lp + math.log(q)) for path, lp in beams for t, q in graph[path[-1]].items()]
        beams = sorted(candidates, key=lambda c: -c[1])[:2]
    path, lp = beams[0]
    return (path, round(math.exp(lp), 4))


Q(None, "Repetition Penalty", "Medium", "Stop saying the same thing",
  "For tokens already generated: divide a positive logit by the penalty, multiply a negative one by it. Return new logits, rounded to 4 decimals.",
  [(([2.0, 1.0, -1.0, 0.5], [0, 2], 1.5),  [1.3333, 1.0, -1.5, 0.5])],
  ("Loop with an if.", "O(V)", "O(V)"),
  ("<code>np.where</code> on the seen entries.", "O(V + n)", "O(V)"),
  names=["logits", "seen", "penalty"])


@B
def repetition_penalty(logits, seen, penalty):
    out = list(logits)
    for i in set(seen):
        out[i] = out[i] / penalty if out[i] > 0 else out[i] * penalty
    return [round(v, 4) for v in out]


@O
def repetition_penalty(logits, seen, penalty):
    out = np.array(logits, dtype=float)
    idx = np.unique(seen)
    out[idx] = np.where(out[idx] > 0, out[idx] / penalty, out[idx] * penalty)
    return out.round(4)


Q(None, "Stop Sequences", "Easy", "Know when to finish",
  "Cut text at the earliest stop sequence. Return (text before it, which stop was found or None).",
  [(("Answer: 42\nUser: next", ["User:", "END"]), ('Answer: 42\n', 'User:')), (("no stops here", ["User:"]), ('no stops here', None))],
  ("Find each and keep the smallest position.", "O(n·s)", "O(1)"),
  ("A regular expression alternation finds the earliest in one pass.", "O(n·s)", "O(s)"),
  names=["text", "stops"])


@B
def apply_stops(text, stops):
    best, which = len(text), None
    for s in stops:
        i = text.find(s)
        if i != -1 and i < best:
            best, which = i, s
    return (text[:best], which)


@O
def apply_stops(text, stops):
    import re
    m = re.search("|".join(map(re.escape, stops)), text)
    return (text[:m.start()], m.group()) if m else (text, None)


Q(None, "Context Window", "Easy", "The model only sees so much",
  "Keep only the last n tokens before each prediction. Generate: starting from a list, append each new token and return the window after each step.",
  [(([1, 2, 3], [4, 5], 3),  [[2, 3, 4], [3, 4, 5]])],
  ("Append, then slice.", "O(k·n)", "O(n)"),
  ("<code>collections.deque(maxlen=n)</code> drops the oldest automatically.", "O(k·n)", "O(n)"),
  names=["start", "new_tokens", "n"])


@B
def windows_over_time(start, new_tokens, n):
    tokens, out = list(start), []
    for t in new_tokens:
        tokens.append(t)
        out.append(tokens[-n:])
    return out


@O
def windows_over_time(start, new_tokens, n):
    from collections import deque
    window, out = deque(start, maxlen=n), []
    for t in new_tokens:
        window.append(t)
        out.append(list(window))
    return out


Q(None, "What the KV Cache Saves", "Medium", "Don't recompute the past",
  "A prompt of P tokens generates N tokens. Without a cache, each step reprocesses everything so far. With a cache, the first step does P, and each later step does 1. Return (positions without, positions with).",
  [((100, 50), (6225, 149)), ((1000, 200), (219900, 1199))],
  ("Add up in a loop.", "O(N)", "O(1)"),
  ("Arithmetic series: N·P + N(N−1)/2.", "O(1)", "O(1)"),
  names=["P", "N"])


@B
def kv_cache_cost(P, N):
    without = 0
    for step in range(N):
        without += P + step
    return (without, P + (N - 1))


@O
def kv_cache_cost(P, N):
    return (N * P + N * (N - 1) // 2, P + N - 1)


Q(None, "How Unsure Is the Model?", "Easy", "Entropy of the next token",
  "Return the entropy −Σ p·ln p (treat 0·ln 0 as 0), rounded to 4 decimals. Higher means more unsure.",
  [(([0.5, 0.5],), 0.6931), (([1.0, 0.0, 0.0],), 0.0), (([0.25, 0.25, 0.25, 0.25],), 1.3863)],
  ("Add up with a check for zero.", "O(V)", "O(1)"),
  ("Keep the non-zero entries with a mask.", "O(V)", "O(V)"))


@B
def next_entropy(probs):
    total = 0.0
    for p in probs:
        if p > 0:
            total -= p * math.log(p)
    return round(total, 4) + 0.0


@O
def next_entropy(probs):
    p = np.array(probs)
    p = p[p > 0]
    return round(float(-(p * np.log(p)).sum()), 4) + 0.0
