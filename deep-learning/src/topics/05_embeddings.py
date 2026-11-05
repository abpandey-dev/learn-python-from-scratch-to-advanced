from lib import *
import math
import re
import numpy as np


TOPIC(
    id="embeddings", title="Tokens & Embeddings", glyph="abc→123",
    blurb="How text becomes numbers: tokenising, BPE merges, bag of words and TF-IDF, embedding tables, skip-gram and negative sampling, word analogies, co-occurrence and positional encoding.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">ids = [vocab[t] for t in tokens]
E[ids]                               # embedding lookup: (T, dim)
tf * log(n_docs / df)                # TF-IDF
unit = E / np.linalg.norm(E, axis=1, keepdims=True)
unit @ unit[q]                       # cosine similarity to everything</code></pre>
""")

DOCS = [["the", "cat", "sat"], ["the", "dog", "sat"], ["the", "dog", "ran", "fast"]]
EMB = {"king": [0.9, 0.8, 0.1], "queen": [0.9, 0.1, 0.8], "man": [0.5, 0.9, 0.1], "woman": [0.5, 0.1, 0.9], "apple": [0.1, 0.5, 0.5]}


Q(None, "Word Tokeniser", "Easy", "Splitting text",
  "Lower-case the text and return its runs of letters or digits as tokens.",
  [(("Hello, World! It's 2024.",), ['hello', 'world', 'it', 's', '2024'])],
  ("Walk the characters, building words.", "O(n)", "O(n)"),
  ("<code>re.findall(r'[a-z0-9]+', text.lower())</code>.", "O(n)", "O(n)"))


@B
def tokenise(text):
    tokens, current = [], ""
    for ch in text.lower():
        if ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            current += ch
        elif current:
            tokens.append(current)
            current = ""
    if current:
        tokens.append(current)
    return tokens


@O
def tokenise(text):
    return re.findall(r"[a-z0-9]+", text.lower())


Q(None, "Build a Vocabulary", "Easy", "With special tokens",
  "Return {token: id}: 0 = &lt;pad&gt;, 1 = &lt;unk&gt;, then tokens appearing at least min_count times, sorted alphabetically.",
  [((["b", "a", "b", "c", "a", "b"], 2), {'<pad>': 0, '<unk>': 1, 'a': 2, 'b': 3})],
  ("Count in a dictionary, filter, sort.", "O(n + k log k)", "O(k)"),
  ("<code>np.unique</code> with counts.", "O(n log n)", "O(k)"),
  names=["tokens", "min_count"])


@B
def build_vocab(tokens, min_count):
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    vocab = {"<pad>": 0, "<unk>": 1}
    for t in sorted(counts):
        if counts[t] >= min_count:
            vocab[t] = len(vocab)
    return vocab


@O
def build_vocab(tokens, min_count):
    words, counts = np.unique(tokens, return_counts=True)
    kept = words[counts >= min_count].tolist()
    return {"<pad>": 0, "<unk>": 1, **{w: i + 2 for i, w in enumerate(kept)}}


Q(None, "Encode With Unknowns", "Easy", "Unseen words",
  "Map tokens to ids, using 1 for anything not in the vocabulary.",
  [((["a", "z", "b"], {"<pad>": 0, "<unk>": 1, "a": 2, "b": 3}), [2, 1, 3])],
  ("A loop with an if.", "O(n)", "O(n)"),
  ("<code>dict.get(t, 1)</code> in a comprehension.", "O(n)", "O(n)"),
  names=["tokens", "vocab"])


@B
def encode(tokens, vocab):
    out = []
    for t in tokens:
        if t in vocab:
            out.append(vocab[t])
        else:
            out.append(1)
    return out


@O
def encode(tokens, vocab):
    return [vocab.get(t, 1) for t in tokens]


Q(None, "Bag of Words", "Easy", "Counts per document",
  "Return one row per document, counting each vocabulary word (columns = sorted distinct words).",
  [((DOCS,), [[1, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 1]])],
  ("Nested loops.", "O(n·V)", "O(n·V)"),
  ("Index dict + <code>np.add.at</code>.", "O(words)", "O(n·V)"))


@B
def bag_of_words(docs):
    vocab = sorted({w for d in docs for w in d})
    return [[d.count(w) for w in vocab] for d in docs]


@O
def bag_of_words(docs):
    vocab = {w: i for i, w in enumerate(sorted({w for d in docs for w in d}))}
    out = np.zeros((len(docs), len(vocab)), dtype=int)
    for i, d in enumerate(docs):
        np.add.at(out[i], [vocab[w] for w in d], 1)
    return out


Q(None, "TF-IDF", "Medium", "Rare words count more",
  "Score word w in document i: (count in doc / doc length) × ln(number of docs / docs containing w). Round to 4 decimals.",
  [((DOCS, 0, "cat"), 0.3662), ((DOCS, 0, "the"), 0.0), ((DOCS, 2, "dog"), 0.1014)],
  ("Count with loops.", "O(total words)", "O(1)"),
  ("Bag-of-words matrix, then column operations.", "O(n·V)", "O(n·V)"),
  names=["docs", "i", "w"])


@B
def tfidf(docs, i, w):
    tf = docs[i].count(w) / len(docs[i])
    df = sum(1 for d in docs if w in d)
    return round(tf * math.log(len(docs) / df), 4) + 0.0


@O
def tfidf(docs, i, w):
    has = np.array([w in d for d in docs])
    tf = docs[i].count(w) / len(docs[i])
    return round(tf * np.log(len(docs) / has.sum()), 4) + 0.0


Q(None, "BPE: Most Frequent Pair", "Medium", "How tokenisers are built",
  "words is a list of token lists. Count neighbouring pairs and return the most frequent (ties → first alphabetically), with its count.",
  [(([["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w"]],), (('l', 'o'), 2))],
  ("A dictionary of pair counts.", "O(total)", "O(pairs)"),
  ("<code>collections.Counter</code> over <code>zip</code>.", "O(total)", "O(pairs)"))


@B
def top_pair(words):
    counts = {}
    for w in words:
        for pair in zip(w, w[1:]):
            counts[pair] = counts.get(pair, 0) + 1
    best = max(counts.values())
    pair = min(p for p, c in counts.items() if c == best)
    return (pair, best)


@O
def top_pair(words):
    from collections import Counter
    counts = Counter(p for w in words for p in zip(w, w[1:]))
    return min(counts.items(), key=lambda kv: (-kv[1], kv[0]))


Q(None, "BPE: Apply a Merge", "Medium", "Joining a pair",
  "Replace every neighbouring (a, b) in each word with the joined token a + b.",
  [(([["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w"]], ("l", "o")), [['lo', 'w'], ['lo', 'w', 'e', 'r'], ['n', 'e', 'w']]), (([["a", "a", "a"]], ("a", "a")), [['aa', 'a']])],
  ("Walk each word; on a match, join and skip two.", "O(total)", "O(total)"),
  ("Join with spaces and use a regular expression, keeping token boundaries.", "O(total)", "O(total)"),
  names=["words", "pair"])


@B
def apply_merge(words, pair):
    out = []
    for w in words:
        new, i = [], 0
        while i < len(w):
            if i + 1 < len(w) and (w[i], w[i + 1]) == pair:
                new.append(w[i] + w[i + 1])
                i += 2
            else:
                new.append(w[i])
                i += 1
        out.append(new)
    return out


@O
def apply_merge(words, pair):
    pattern = re.compile(r"(?<!\S)" + re.escape(pair[0]) + r" " + re.escape(pair[1]) + r"(?!\S)")
    return [pattern.sub(pair[0] + pair[1], " ".join(w)).split(" ") for w in words]


Q(None, "BPE: Train n Merges", "Hard", "A tiny tokeniser",
  "Start from characters of each word. Repeatedly merge the top pair, n times. Return (merges in order, final words).",
  [((["low", "lower", "newest", "widest"], 3), ([('e', 's'), ('es', 't'), ('l', 'o')], [['lo', 'w'], ['lo', 'w', 'e', 'r'], ['n', 'e', 'w', 'est'], ['w', 'i', 'd', 'est']]))],
  ("The two steps above, in a loop.", "O(n·total)", "O(total)"),
  ("Counter for counts; list comprehension to join.", "O(n·total)", "O(total)"),
  names=["words", "n"])


@B
def train_bpe(words, n):
    words = [list(w) for w in words]
    merges = []
    for _ in range(n):
        counts = {}
        for w in words:
            for pair in zip(w, w[1:]):
                counts[pair] = counts.get(pair, 0) + 1
        if not counts:
            break
        best = max(counts.values())
        pair = min(p for p, c in counts.items() if c == best)
        merges.append(pair)
        new_words = []
        for w in words:
            new, i = [], 0
            while i < len(w):
                if i + 1 < len(w) and (w[i], w[i + 1]) == pair:
                    new.append(w[i] + w[i + 1])
                    i += 2
                else:
                    new.append(w[i])
                    i += 1
            new_words.append(new)
        words = new_words
    return (merges, words)


@O
def train_bpe(words, n):
    from collections import Counter
    words = [list(w) for w in words]
    merges = []
    for _ in range(n):
        counts = Counter(p for w in words for p in zip(w, w[1:]))
        if not counts:
            break
        pair = min(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        merges.append(pair)
        pattern = re.compile(r"(?<!\S)" + re.escape(pair[0]) + " " + re.escape(pair[1]) + r"(?!\S)")
        words = [pattern.sub(pair[0] + pair[1], " ".join(w)).split(" ") for w in words]
    return (merges, words)


Q(None, "Rough Token Estimate", "Easy", "Before you call an API",
  "A rule of thumb for English is about 4 characters per token. Return (estimate per text rounded up, the total).",
  [((["Hello there", "Tokenisers split text into pieces"],), ([3, 9], 12))],
  ("Divide and round up in a loop.", "O(n)", "O(n)"),
  ("<code>np.ceil</code> on an array of lengths.", "O(n)", "O(n)"))


@B
def estimate_tokens(texts):
    out = [math.ceil(len(t) / 4) for t in texts]
    return (out, sum(out))


@O
def estimate_tokens(texts):
    n = np.ceil(np.array([len(t) for t in texts]) / 4).astype(int)
    return (n, int(n.sum()))


Q(None, "Embedding Lookup", "Easy", "A table of vectors",
  "Return the embedding rows for the given token ids.",
  [(([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]], [2, 0, 2]), [[0.5, 0.6], [0.1, 0.2], [0.5, 0.6]])],
  ("A list of rows in a loop.", "O(T·d)", "O(T·d)"),
  ("<code>E[ids]</code>.", "O(T·d)", "O(T·d)"),
  names=["E", "ids"])


@B
def lookup(E, ids):
    return [E[i] for i in ids]


@O
def lookup(E, ids):
    return np.array(E)[ids]


Q(None, "Embedding Table Size", "Easy", "It adds up",
  "Return (parameters, MB at 4 bytes each) for a vocabulary and dimension, with MB rounded to 2 decimals (1 MB = 10⁶ bytes).",
  [((50000, 768), (38400000, 153.6)), ((30000, 128), (3840000, 15.36))],
  ("Multiply.", "O(1)", "O(1)"),
  ("Create a zero table of float32 and read <code>.nbytes</code> (small cases only).", "O(1)", "O(V·d)"),
  names=["vocab", "dim"])


@B
def embedding_size(vocab, dim):
    params = vocab * dim
    return (params, round(params * 4 / 1e6, 2))


@O
def embedding_size(vocab, dim):
    params = int(np.prod([vocab, dim]))
    return (params, round(params * np.float32(0).nbytes / 1e6, 2))


Q(None, "Most Similar Vectors", "Medium", "Cosine search",
  "Return the k names most similar to the query (excluding itself), highest cosine first.",
  [((EMB, "king", 2), ['man', 'queen'])],
  ("Compute cosine for each word in a loop, then sort.", "O(V·d + V log V)", "O(V)"),
  ("Normalise into a matrix; one matrix-vector product scores all.", "O(V·d)", "O(V·d)"),
  names=["emb", "query", "k"])


@B
def most_similar(emb, query, k):
    q = emb[query]
    q_len = math.sqrt(sum(a * a for a in q))
    scored = []
    for w, v in emb.items():
        if w == query:
            continue
        cos = sum(a * b for a, b in zip(q, v)) / (q_len * math.sqrt(sum(b * b for b in v)))
        scored.append((cos, w))
    scored.sort(reverse=True)
    return [w for _, w in scored[:k]]


@O
def most_similar(emb, query, k):
    words = [w for w in emb if w != query]
    M = np.array([emb[w] for w in words])
    M = M / np.linalg.norm(M, axis=1, keepdims=True)
    q = np.array(emb[query]) / np.linalg.norm(emb[query])
    return [words[i] for i in np.argsort(-(M @ q))[:k]]


Q(None, "Word Analogy", "Medium", "king − man + woman",
  "Return the word closest by cosine to b − a + c, excluding a, b and c.",
  [((EMB, "man", "king", "woman"), 'queen')],
  ("Build the target and loop over words.", "O(V·d)", "O(d)"),
  ("Matrix of normalised vectors with a mask for excluded words.", "O(V·d)", "O(V·d)"),
  names=["emb", "a", "b", "c"])


@B
def analogy(emb, a, b, c):
    target = [y - x + z for x, y, z in zip(emb[a], emb[b], emb[c])]
    t_len = math.sqrt(sum(v * v for v in target))
    best, best_cos = None, -2
    for w, v in emb.items():
        if w in (a, b, c):
            continue
        cos = sum(p * q for p, q in zip(target, v)) / (t_len * math.sqrt(sum(q * q for q in v)))
        if cos > best_cos:
            best, best_cos = w, cos
    return best


@O
def analogy(emb, a, b, c):
    words = [w for w in emb if w not in (a, b, c)]
    M = np.array([emb[w] for w in words])
    target = np.array(emb[b]) - np.array(emb[a]) + np.array(emb[c])
    scores = M @ target / (np.linalg.norm(M, axis=1) * np.linalg.norm(target))
    return words[int(scores.argmax())]


Q(None, "Skip-Gram Pairs", "Easy", "Word2vec's training data",
  "For each position, pair the word with every word within the window on either side. Return (centre, context) pairs in order.",
  [((["the", "cat", "sat"], 1), [('the', 'cat'), ('cat', 'the'), ('cat', 'sat'), ('sat', 'cat')])],
  ("Nested loops with bounds.", "O(T·w)", "O(T·w)"),
  ("A comprehension using slices.", "O(T·w)", "O(T·w)"),
  names=["tokens", "window"])


@B
def skip_gram(tokens, window):
    pairs = []
    for i in range(len(tokens)):
        for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
            if j != i:
                pairs.append((tokens[i], tokens[j]))
    return pairs


@O
def skip_gram(tokens, window):
    n = len(tokens)
    return [(tokens[i], tokens[j]) for i in range(n) for j in np.arange(max(0, i - window), min(n, i + window + 1)).tolist() if j != i]


Q(None, "Co-occurrence Matrix", "Medium", "Words known by their neighbours",
  "Count how often words appear within a window of each other. Rows and columns are sorted words.",
  [((["a", "b", "a", "c"], 1), [[0, 2, 1], [2, 0, 0], [1, 0, 0]])],
  ("Nested loops adding to a table.", "O(T·w)", "O(V²)"),
  ("<code>np.add.at</code> on index pairs.", "O(T·w)", "O(V²)"),
  names=["tokens", "window"])


@B
def cooccur(tokens, window):
    vocab = sorted(set(tokens))
    table = [[0] * len(vocab) for _ in vocab]
    for i, t in enumerate(tokens):
        for j in range(max(0, i - window), min(len(tokens), i + window + 1)):
            if j != i:
                table[vocab.index(t)][vocab.index(tokens[j])] += 1
    return table


@O
def cooccur(tokens, window):
    vocab = {w: i for i, w in enumerate(sorted(set(tokens)))}
    ids = np.array([vocab[t] for t in tokens])
    table = np.zeros((len(vocab), len(vocab)), dtype=int)
    for offset in range(1, window + 1):
        np.add.at(table, (ids[:-offset], ids[offset:]), 1)
        np.add.at(table, (ids[offset:], ids[:-offset]), 1)
    return table


Q(None, "Pointwise Mutual Information", "Medium", "More than chance?",
  "PMI = ln(P(x, y) / (P(x)·P(y))). Given the joint count, each word's count and total pairs N, return PMI, rounded to 4 decimals.",
  [((10, 20, 30, 300), 1.6094), ((2, 20, 30, 300), 0.0)],
  ("Three probabilities, then a log.", "O(1)", "O(1)"),
  ("Simplified: ln(c·N / (x·y)).", "O(1)", "O(1)"),
  names=["c", "x", "y", "N"])


@B
def pmi(c, x, y, N):
    pxy, px, py = c / N, x / N, y / N
    return round(math.log(pxy / (px * py)), 4)


@O
def pmi(c, x, y, N):
    return round(float(np.log(c * N / (x * y))), 4)


Q(None, "Negative Sampling Loss", "Hard", "Pull together, push apart",
  "Given centre vector c, true context vector p, and negative vectors N: loss = −ln σ(c·p) − Σ ln σ(−c·n). Round to 4 decimals.",
  [(([1.0, 0.0], [1.0, 0.0], [[-1.0, 0.0], [0.0, 1.0]]), 1.3197)],
  ("Dot products in loops.", "O(k·d)", "O(1)"),
  ("<code>np.logaddexp</code> computes −ln σ(z) as ln(1 + e^(−z)) safely.", "O(k·d)", "O(k)"),
  names=["c", "p", "N"])


@B
def neg_sampling(c, p, N):
    sig = lambda z: 1 / (1 + math.exp(-z))
    loss = -math.log(sig(sum(a * b for a, b in zip(c, p))))
    for n in N:
        loss -= math.log(sig(-sum(a * b for a, b in zip(c, n))))
    return round(loss, 4)


@O
def neg_sampling(c, p, N):
    c = np.array(c)
    return round(float(np.logaddexp(0, -(c @ np.array(p))) + np.logaddexp(0, np.array(N) @ c).sum()), 4)


Q(None, "Sentence Embedding by Mean Pooling", "Medium", "Ignore padding",
  "Average token vectors where the attention mask is 1, then scale to length 1. Round to 4 decimals.",
  [(([[3.0, 0.0], [0.0, 4.0], [9.0, 9.0]], [1, 1, 0]), [0.6, 0.8])],
  ("Add masked vectors, divide, normalise in loops.", "O(T·d)", "O(d)"),
  ("<code>(E * mask[:, None]).sum(0) / mask.sum()</code>, then divide by the norm.", "O(T·d)", "O(T·d)"),
  names=["E", "mask"])


@B
def sentence_embedding(E, mask):
    total = [0.0] * len(E[0])
    for row, m in zip(E, mask):
        if m:
            for j, v in enumerate(row):
                total[j] += v
    count = sum(mask)
    mean = [v / count for v in total]
    length = math.sqrt(sum(v * v for v in mean))
    return [round(v / length, 4) for v in mean]


@O
def sentence_embedding(E, mask):
    E, mask = np.array(E), np.array(mask)
    mean = (E * mask[:, None]).sum(axis=0) / mask.sum()
    return (mean / np.linalg.norm(mean)).round(4)


Q(None, "Sinusoidal Positional Encoding", "Medium", "Giving order to a set",
  "Return an (n, d) table: even columns sin(pos / 10000^(i/d)), odd columns cos(pos / 10000^((i−1)/d)). Round to 4 decimals.",
  [((3, 4), [[0.0, 1.0, 0.0, 1.0], [0.8415, 0.5403, 0.01, 1.0], [0.9093, -0.4161, 0.02, 0.9998]])],
  ("Nested loops.", "O(n·d)", "O(n·d)"),
  ("Broadcast positions against rates, then assign even and odd columns.", "O(n·d)", "O(n·d)"),
  names=["n", "d"])


@B
def positional(n, d):
    out = []
    for pos in range(n):
        row = []
        for i in range(d):
            if i % 2 == 0:
                row.append(round(math.sin(pos / 10000 ** (i / d)), 4) + 0.0)
            else:
                row.append(round(math.cos(pos / 10000 ** ((i - 1) / d)), 4) + 0.0)
        out.append(row)
    return out


@O
def positional(n, d):
    pos = np.arange(n)[:, None]
    rates = 10000 ** (np.arange(0, d, 2) / d)
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(pos / rates)
    pe[:, 1::2] = np.cos(pos / rates[: d // 2])
    return pe.round(4) + 0.0


Q(None, "Truncate and Pad to a Fixed Length", "Easy", "Every model has a limit",
  "Cut each id list to max_len, then pad on the right with 0 to exactly max_len.",
  [(([[1, 2, 3, 4], [5]], 3), [[1, 2, 3], [5, 0, 0]])],
  ("Slice, then add zeros, in a loop.", "O(n·L)", "O(n·L)"),
  ("Fill a zero matrix of shape (n, max_len).", "O(n·L)", "O(n·L)"),
  names=["seqs", "max_len"])


@B
def fit_length(seqs, max_len):
    out = []
    for s in seqs:
        cut = s[:max_len]
        out.append(cut + [0] * (max_len - len(cut)))
    return out


@O
def fit_length(seqs, max_len):
    out = np.zeros((len(seqs), max_len), dtype=int)
    for i, s in enumerate(seqs):
        cut = s[:max_len]
        out[i, :len(cut)] = cut
    return out
