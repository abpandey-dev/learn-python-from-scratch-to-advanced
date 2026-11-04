from lib import *
import math
from itertools import product
import numpy as np

TOPIC(
    id="distributions", title="Distributions & Information", glyph="𝒩",
    blurb="The shapes randomness takes — Bernoulli, binomial, Poisson, uniform, normal, exponential — the central limit theorem, and the information theory behind ML losses: entropy, cross-entropy, KL divergence, softmax, log-loss, Gini and maximum likelihood.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">math.comb(n, k) * p**k * (1 - p)**(n - k)          # binomial P(X = k)
lam**k * math.exp(-lam) / math.factorial(k)        # Poisson P(X = k)
math.exp(-(x - mu)**2 / (2 * s**2)) / (s * math.sqrt(2 * math.pi))   # normal pdf
0.5 * (1 + math.erf((x - mu) / (s * math.sqrt(2))))                 # normal cdf
1 - math.exp(-lam * t)                             # exponential P(X ≤ t)
-(p * np.log2(p)).sum()                            # entropy (bits)
-(p * np.log(q)).sum()                             # cross-entropy (nats)
np.exp(z - z.max()) / np.exp(z - z.max()).sum()    # softmax
-(y*np.log(p) + (1-y)*np.log(1-p)).mean()          # binary log-loss</code></pre>
""")


Q(None, "Bernoulli Mean and Variance", "Easy", "One yes/no trial",
  "X is 1 with probability p, else 0. Return (E[X], Var(X)), rounded to 4 decimals.",
  [((0.3,), (0.3, 0.21)), ((0.5,), (0.5, 0.25)), ((1.0,), (1.0, 0.0))],
  ("Use the definitions over the two outcomes 0 and 1.", "O(1)", "O(1)"),
  ("Formulas: E = p, Var = p(1 − p).", "O(1)", "O(1)"))


@B
def bernoulli(p):
    outcomes = [(0, 1 - p), (1, p)]
    mean = sum(x * q for x, q in outcomes)
    var = sum((x - mean) ** 2 * q for x, q in outcomes)
    return (round(mean, 4), round(var, 4))


@O
def bernoulli(p):
    return (round(p, 4), round(p * (1 - p), 4))


Q(None, "Binomial Probability Table", "Medium", "k successes in n tries",
  "Return P(X = k) for k = 0 … n, where X ~ Binomial(n, p), rounded to 4 decimals.",
  [((4, 0.5), [0.0625, 0.25, 0.375, 0.25, 0.0625]), ((3, 0.2), [0.512, 0.384, 0.096, 0.008])],
  ("Enumerate all 2ⁿ success/fail sequences, add each one's probability to its k.", "O(2ⁿ · n)", "O(n)"),
  ("Formula C(n, k)·pᵏ(1 − p)ⁿ⁻ᵏ for every k at once with NumPy.", "O(n)", "O(n)"))


@B
def binomial_table(n, p):
    table = [0.0] * (n + 1)
    for seq in product([0, 1], repeat=n):
        k = sum(seq)
        table[k] += p ** k * (1 - p) ** (n - k)
    return [round(x, 4) for x in table]


@O
def binomial_table(n, p):
    k = np.arange(n + 1)
    comb = np.array([math.comb(n, i) for i in k])
    return (comb * p ** k * (1 - p) ** (n - k)).round(4)


Q(None, "Poisson Probability", "Easy", "Counts of rare events",
  "Events happen on average lam times per hour. Return P(exactly k events in an hour), rounded to 4 decimals.",
  [((3, 2), 0.224), ((1, 0), 0.3679), ((2, 4), 0.0902)],
  ("Build the term step by step: start at e^(−λ) and multiply by λ/i for i = 1 … k.", "O(k)", "O(1)"),
  ("Formula λᵏe^(−λ)/k!.", "O(k)", "O(1)"),
  names=["lam", "k"])


@B
def poisson(lam, k):
    term = math.exp(-lam)
    for i in range(1, k + 1):
        term *= lam / i
    return round(term, 4)


@O
def poisson(lam, k):
    return round(lam ** k * math.exp(-lam) / math.factorial(k), 4)


Q(None, "Uniform Distribution", "Easy", "Every value equally likely",
  "X is uniform on [lo, hi]. Return P(a ≤ X ≤ b), rounded to 4 decimals.",
  [((0, 10, 2, 5), 0.3), ((0, 4, 1, 3), 0.5), ((0, 4, 3, 9), 0.25)],
  ("Integrate the flat density 1/(hi − lo) numerically over [a, b] ∩ [lo, hi].", "O(n)", "O(1)"),
  ("Length of the overlap divided by the total length.", "O(1)", "O(1)"),
  names=["lo", "hi", "a", "b"])


@B
def uniform(lo, hi, a, b):
    a, b = max(a, lo), min(b, hi)
    if b <= a:
        return 0.0
    steps = 1000
    dx = (b - a) / steps
    area = 0
    for _ in range(steps):
        area += 1 / (hi - lo) * dx
    return round(area, 4)


@O
def uniform(lo, hi, a, b):
    overlap = max(0, min(b, hi) - max(a, lo))
    return round(overlap / (hi - lo), 4)


Q(None, "Height of the Normal Curve", "Easy", "The bell curve's PDF",
  "Return the normal density f(x) for each x, with mean mu and standard deviation s, rounded to 4 decimals.",
  [(([0, 1], 0, 1), [0.3989, 0.242]), (([70], 65, 5), [0.0484])],
  ("Apply the formula to each x in a loop.", "O(n)", "O(n)"),
  ("Vectorised with <code>np.exp</code>.", "O(n)", "O(n)"),
  names=["xs", "mu", "s"])


@B
def normal_pdf(xs, mu, s):
    out = []
    for x in xs:
        z = (x - mu) / s
        out.append(round(math.exp(-z * z / 2) / (s * math.sqrt(2 * math.pi)), 4))
    return out


@O
def normal_pdf(xs, mu, s):
    z = (np.array(xs, dtype=float) - mu) / s
    return (np.exp(-z ** 2 / 2) / (s * np.sqrt(2 * np.pi))).round(4)


Q(None, "Area Under the Normal Curve", "Medium", "CDF: P(X ≤ x)",
  "Return P(X ≤ x) for X ~ Normal(mu, s), rounded to 4 decimals.",
  [((0, 0, 1), 0.5), ((1.96, 0, 1), 0.975), ((80, 70, 10), 0.8413)],
  ("Add up thin strips of the PDF from far left (μ − 8σ) to x.", "O(n)", "O(1)"),
  ("Closed form with the error function: ½(1 + erf((x − μ)/(σ√2))).", "O(1)", "O(1)"),
  names=["x", "mu", "s"])


@B
def normal_cdf(x, mu, s):
    start = mu - 8 * s
    n = 20000
    dx = (x - start) / n
    area = 0
    for i in range(n):
        t = start + (i + 0.5) * dx
        area += math.exp(-((t - mu) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi)) * dx
    return round(area, 4)


@O
def normal_cdf(x, mu, s):
    return round(0.5 * (1 + math.erf((x - mu) / (s * math.sqrt(2)))), 4)


Q(None, "The 68–95–99.7 Rule", "Medium", "P(a ≤ X ≤ b)",
  "Return P(a ≤ X ≤ b) for X ~ Normal(mu, s), rounded to 4 decimals.",
  [((-1, 1, 0, 1), 0.6827), ((-2, 2, 0, 1), 0.9545), ((85, 110, 100, 15), 0.5889)],
  ("Integrate the PDF from a to b with thin strips.", "O(n)", "O(1)"),
  ("CDF(b) − CDF(a) using erf.", "O(1)", "O(1)"),
  names=["a", "b", "mu", "s"])


@B
def normal_between(a, b, mu, s):
    n = 20000
    dx = (b - a) / n
    area = 0
    for i in range(n):
        t = a + (i + 0.5) * dx
        area += math.exp(-((t - mu) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi)) * dx
    return round(area, 4)


@O
def normal_between(a, b, mu, s):
    cdf = lambda x: 0.5 * (1 + math.erf((x - mu) / (s * math.sqrt(2))))
    return round(cdf(b) - cdf(a), 4)


Q(None, "Z-Score to Percentile", "Easy", "Standardising",
  "A score x comes from Normal(mu, s). Return (z-score, percentile) — the percentage of scores below x — rounded to 2 decimals.",
  [((80, 70, 10), (1.0, 84.13)), ((70, 70, 10), (0.0, 50.0)), ((55, 70, 10), (-1.5, 6.68))],
  ("z = (x − μ)/σ, then integrate the standard normal curve up to z.", "O(n)", "O(1)"),
  ("z, then the erf formula for the CDF.", "O(1)", "O(1)"),
  names=["x", "mu", "s"])


@B
def percentile(x, mu, s):
    z = (x - mu) / s
    n = 20000
    start = -8.0
    dx = (z - start) / n
    area = 0
    for i in range(n):
        t = start + (i + 0.5) * dx
        area += math.exp(-t * t / 2) / math.sqrt(2 * math.pi) * dx
    return (round(z, 2), round(area * 100, 2))


@O
def percentile(x, mu, s):
    z = (x - mu) / s
    return (round(z, 2), round(50 * (1 + math.erf(z / math.sqrt(2))), 2))


Q(None, "Exponential Waiting Time", "Easy", "P(wait ≤ t)",
  "Buses arrive at rate lam per minute (exponential waiting times). Return P(you wait at most t minutes), rounded to 4 decimals.",
  [((0.5, 2), 0.6321), ((1, 3), 0.9502), ((2, 0), 0.0)],
  ("Integrate the density λe^(−λx) from 0 to t with thin strips.", "O(n)", "O(1)"),
  ("Closed form 1 − e^(−λt).", "O(1)", "O(1)"),
  names=["lam", "t"])


@B
def exp_wait(lam, t):
    n = 10000
    dx = t / n
    area = 0
    for i in range(n):
        x = (i + 0.5) * dx
        area += lam * math.exp(-lam * x) * dx
    return round(area, 4)


@O
def exp_wait(lam, t):
    return round(1 - math.exp(-lam * t), 4)


Q(None, "Distribution of the Sum of Two Dice", "Easy", "Convolution",
  "Return how many of the 36 outcomes give each total 2, 3, …, 12.",
  [((), [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])],
  ("Double loop over both dice, count each total.", "O(36)", "O(11)"),
  ("Adding random variables convolves their distributions: <code>np.convolve(ones, ones)</code>.", "O(36)", "O(11)"))


@B
def two_dice_counts():
    counts = [0] * 11
    for a in range(1, 7):
        for b in range(1, 7):
            counts[a + b - 2] += 1
    return counts


@O
def two_dice_counts():
    one_die = np.ones(6, dtype=int)
    return np.convolve(one_die, one_die)


Q(None, "Sum of Three Dice", "Medium", "Towards the bell curve",
  "Return P(three dice total exactly k), rounded to 4 decimals.",
  [((10,), 0.125), ((3,), 0.0046), ((19,), 0.0)],
  ("Triple loop over all 216 outcomes.", "O(216)", "O(1)"),
  ("Convolve the single-die distribution with itself twice.", "O(n²)", "O(n)"))


@B
def three_dice(k):
    hits = 0
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(1, 7):
                if a + b + c == k:
                    hits += 1
    return round(hits / 216, 4)


@O
def three_dice(k):
    d = np.full(6, 1 / 6)
    dist = np.convolve(np.convolve(d, d), d)
    return round(dist[k - 3], 4) if 3 <= k <= 18 else 0.0


Q(None, "Entropy", "Medium", "Average surprise in bits",
  "Return the entropy H(p) = −Σ p log₂ p of a probability distribution (0·log 0 counts as 0), rounded to 4 decimals.",
  [(([0.5, 0.5],), 1.0), (([1, 0],), 0.0), (([0.25] * 4,), 2.0), (([0.7, 0.2, 0.1],), 1.1568)],
  ("Loop, skipping zeros.", "O(n)", "O(1)"),
  ("Mask the zeros, then <code>-(p * np.log2(p)).sum()</code>.", "O(n)", "O(n)"))


@B
def entropy(p):
    h = 0
    for x in p:
        if x > 0:
            h -= x * math.log2(x)
    return round(h, 4) + 0.0


@O
def entropy(p):
    p = np.array(p, dtype=float)
    p = p[p > 0]
    return round(-(p * np.log2(p)).sum(), 4) + 0.0


Q(None, "Cross-Entropy", "Medium", "How well q predicts p",
  "Return H(p, q) = −Σ p log₂ q (skip terms where p = 0), rounded to 4 decimals. p = true distribution, q = model's prediction.",
  [(([1, 0, 0], [0.7, 0.2, 0.1]), 0.5146), (([0.5, 0.5], [0.5, 0.5]), 1.0), (([0, 1], [0.9, 0.1]), 3.3219)],
  ("Loop over the pairs.", "O(n)", "O(1)"),
  ("Vectorised with a mask on p &gt; 0.", "O(n)", "O(n)"))


@B
def cross_entropy(p, q):
    h = 0
    for a, b in zip(p, q):
        if a > 0:
            h -= a * math.log2(b)
    return round(h, 4)


@O
def cross_entropy(p, q):
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    m = p > 0
    return round(-(p[m] * np.log2(q[m])).sum(), 4)


Q(None, "KL Divergence", "Medium", "Extra bits from using the wrong distribution",
  "Return D_KL(p ‖ q) = Σ p log₂(p/q) (skip p = 0), rounded to 4 decimals.",
  [(([0.5, 0.5], [0.9, 0.1]), 0.737), (([0.2, 0.8], [0.2, 0.8]), 0.0), (([0.7, 0.2, 0.1], [1 / 3] * 3), 0.4282)],
  ("Loop over the pairs.", "O(n)", "O(1)"),
  ("Identity: KL = cross-entropy − entropy; or vectorised directly.", "O(n)", "O(n)"))


@B
def kl(p, q):
    d = 0
    for a, b in zip(p, q):
        if a > 0:
            d += a * math.log2(a / b)
    return round(d, 4) + 0.0


@O
def kl(p, q):
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    m = p > 0
    return round((p[m] * np.log2(p[m] / q[m])).sum(), 4) + 0.0


Q(None, "Softmax", "Medium", "Scores → probabilities",
  "Turn raw scores into probabilities that sum to 1, rounded to 4 decimals. Must not overflow for large scores.",
  [(([2, 1, 0],), [0.6652, 0.2447, 0.09]), (([1, 1],), [0.5, 0.5]), (([1000, 1000, 999],), [0.4223, 0.4223, 0.1554])],
  ("Subtract the max (prevents overflow), exponentiate each in a loop, divide by the total.", "O(n)", "O(n)"),
  ("Vectorised: <code>e = np.exp(z - z.max()); e / e.sum()</code>.", "O(n)", "O(n)"))


@B
def softmax(z):
    top = max(z)
    exps = [math.exp(v - top) for v in z]
    total = sum(exps)
    return [round(e / total, 4) for e in exps]


@O
def softmax(z):
    z = np.array(z, dtype=float)
    e = np.exp(z - z.max())
    return (e / e.sum()).round(4)


Q(None, "Binary Log-Loss", "Medium", "The loss of logistic regression",
  "Return the average binary cross-entropy (natural log) of predicted probabilities p for labels y, rounded to 4 decimals.",
  [(([1, 0, 1], [0.9, 0.1, 0.8]), 0.1446), (([1, 0], [0.5, 0.5]), 0.6931)],
  ("For each example: −log p if y = 1, else −log(1 − p); average.", "O(n)", "O(1)"),
  ("Vectorised formula −mean(y log p + (1 − y) log(1 − p)).", "O(n)", "O(n)"))


@B
def log_loss(y, p):
    total = 0
    for label, prob in zip(y, p):
        if label == 1:
            total += -math.log(prob)
        else:
            total += -math.log(1 - prob)
    return round(total / len(y), 4)


@O
def log_loss(y, p):
    y, p = np.array(y, dtype=float), np.array(p, dtype=float)
    return round(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean(), 4)


Q(None, "Gini Impurity", "Easy", "How mixed is a group?",
  "Return 1 − Σ (share of each class)² for a list of labels, rounded to 4 decimals. 0 = pure.",
  [((["a", "a", "b", "b"],), 0.5), ((["a", "a", "a"],), 0.0), ((["a", "b", "c"],), 0.6667)],
  ("Count each label in a dictionary, then apply the formula.", "O(n)", "O(k)"),
  ("<code>np.unique(..., return_counts=True)</code>.", "O(n log n)", "O(k)"))


@B
def gini(labels):
    counts = {}
    for lab in labels:
        counts[lab] = counts.get(lab, 0) + 1
    total = 1.0
    for c in counts.values():
        total -= (c / len(labels)) ** 2
    return round(total, 4) + 0.0


@O
def gini(labels):
    _, counts = np.unique(labels, return_counts=True)
    shares = counts / counts.sum()
    return round(1 - (shares ** 2).sum(), 4) + 0.0


Q(None, "Information Gain of a Split", "Hard", "How decision trees choose questions",
  "Return entropy(parent) − weighted average entropy of the two children, rounded to 4 decimals.",
  [((["y", "y", "y", "n", "n", "n"], ["y", "y", "y", "n"], ["n", "n"]), 0.4591),
   ((["y", "n", "y", "n"], ["y", "n"], ["y", "n"]), 0.0)],
  ("Entropy by counting labels in loops, for each group.", "O(n)", "O(k)"),
  ("A small vectorised entropy helper using <code>np.unique</code>.", "O(n log n)", "O(k)"),
  names=["parent", "left", "right"])


@B
def info_gain(parent, left, right):
    def H(labels):
        counts = {}
        for lab in labels:
            counts[lab] = counts.get(lab, 0) + 1
        h = 0
        for c in counts.values():
            p = c / len(labels)
            h -= p * math.log2(p)
        return h
    n = len(parent)
    children = len(left) / n * H(left) + len(right) / n * H(right)
    return round(H(parent) - children, 4) + 0.0


@O
def info_gain(parent, left, right):
    def H(labels):
        _, c = np.unique(labels, return_counts=True)
        p = c / c.sum()
        return -(p * np.log2(p)).sum()
    n = len(parent)
    return round(H(parent) - (len(left) * H(left) + len(right) * H(right)) / n, 4) + 0.0


Q(None, "Maximum Likelihood for a Coin", "Medium", "Best p for the data",
  "Given coin results (1 = heads), return the p that makes the data most likely, rounded to 4 decimals.",
  [(([1, 0, 1, 1],), 0.75), (([0, 0, 0, 1, 1],), 0.4)],
  ("Try every p on a fine grid and keep the one with the highest log-likelihood.", "O(grid · n)", "O(1)"),
  ("Calculus: setting d/dp of the log-likelihood to 0 gives p̂ = mean of the data.", "O(n)", "O(1)"))


@B
def coin_mle(data):
    heads = sum(data)
    tails = len(data) - heads
    best_p, best_ll = None, None
    for i in range(1, 1000):
        p = i / 1000
        ll = heads * math.log(p) + tails * math.log(1 - p)
        if best_ll is None or ll > best_ll:
            best_p, best_ll = p, ll
    return round(best_p, 4)


@O
def coin_mle(data):
    return round(np.mean(data), 4)


Q(None, "Log-Likelihood Under a Normal Model", "Medium", "Σ log f(xᵢ)",
  "Return the total log-likelihood (natural log) of the data under Normal(mu, s), rounded to 4 decimals.",
  [(([1, 2, 3], 2, 1), -3.7568), (([1, 2, 3], 0, 2), -6.5863)],
  ("Loop: log of each density value, add them up.", "O(n)", "O(1)"),
  ("Simplify the log first: −½log(2πσ²) − (x − μ)²/(2σ²), then sum with NumPy.", "O(n)", "O(n)"),
  names=["data", "mu", "s"])


@B
def log_likelihood(data, mu, s):
    total = 0
    for x in data:
        density = math.exp(-((x - mu) / s) ** 2 / 2) / (s * math.sqrt(2 * math.pi))
        total += math.log(density)
    return round(total, 4)


@O
def log_likelihood(data, mu, s):
    x = np.array(data, dtype=float)
    return round((-0.5 * np.log(2 * np.pi * s ** 2) - (x - mu) ** 2 / (2 * s ** 2)).sum(), 4)
