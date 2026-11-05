from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "Discrete distributions: Bernoulli, binomial, Poisson", """
<p>A <b>distribution</b> lists every value a random variable can take and how likely each is. Three you'll meet constantly:</p>
<table>
<tr><th>Distribution</th><th>Models</th><th>P(X = k)</th><th>Mean</th></tr>
<tr><td><b>Bernoulli(p)</b></td><td>one yes/no trial (click or not)</td><td>p if k = 1, 1 − p if k = 0</td><td>p</td></tr>
<tr><td><b>Binomial(n, p)</b></td><td>number of yeses in n trials</td><td>C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ</td><td>np</td></tr>
<tr><td><b>Poisson(λ)</b></td><td>count of rare events in a time window (calls per hour)</td><td>λᵏe^(−λ)/k!</td><td>λ</td></tr>
</table>
""", practice=["Bernoulli Mean and Variance", "Binomial Probability Table", "Poisson Probability"])


@LD
def discrete_shapes():
    k = np.arange(0, 11)
    binom = np.array([math.comb(10, i) * 0.3 ** i * 0.7 ** (10 - i) for i in k])
    pois = np.array([3 ** i * math.exp(-3) / math.factorial(i) for i in k])
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(k - 0.2, binom, width=0.4, label="Binomial(10, 0.3)")
    ax.bar(k + 0.2, pois, width=0.4, label="Poisson(3)")
    ax.set_xticks(k)
    ax.legend(fontsize=8)


LESSON("Basics", "Continuous distributions and the normal curve", """
<p>Heights, temperatures and measurement errors can take any value, so we describe them with a <b>density curve</b> (PDF). Probability = <b>area</b> under the curve; the total area is 1.</p>
<ul>
<li><b>Uniform</b>: flat — every value in [a, b] equally likely.</li>
<li><b>Exponential</b>: waiting times between random events: P(wait ≤ t) = 1 − e^(−λt).</li>
<li><b>Normal</b> (Gaussian) N(μ, σ): the bell curve, centred at μ with spread σ.</li>
</ul>
<p>The <b>68–95–99.7 rule</b>: about 68% of a normal population lies within 1σ of the mean, 95% within 2σ, 99.7% within 3σ. A <b>z-score</b> z = (x − μ)/σ says how many σ's from the mean a value is.</p>
""", practice=["Uniform Distribution", "Height of the Normal Curve", "Area Under the Normal Curve", "The 68–95–99.7 Rule", "Z-Score to Percentile", "Exponential Waiting Time"])


@LD
def normal_areas():
    x = np.linspace(-4, 4, 400)
    pdf = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.plot(x, pdf, color="black")
    for k, colour in [(3, "#ccfbf1"), (2, "#5eead4"), (1, "#0f766e")]:
        mask = np.abs(x) <= k
        share = math.erf(k / math.sqrt(2))
        ax.fill_between(x[mask], pdf[mask], color=colour, label=f"±{k}σ: {share:.1%}")
    ax.legend(fontsize=8)
    ax.set_title("The 68–95–99.7 rule", fontsize=9)


LESSON("Core", "Why the normal curve is everywhere: the central limit theorem", """
<p>Add up many independent random things and the total's distribution becomes bell-shaped — whatever the shape of each piece. One die is flat; the sum of two is a triangle; three or more already looks like a bell. This is the <b>central limit theorem</b>.</p>
<p>That's why measurement errors, test scores and averages of samples are approximately normal, and why confidence intervals use 1.96 (the 95% point of the normal curve). Adding random variables <b>convolves</b> their distributions — <code>np.convolve</code>.</p>
""", practice=["Distribution of the Sum of Two Dice", "Sum of Three Dice"])


@LD
def clt_demo():
    die = np.full(6, 1 / 6)
    dist = die
    fig, axes = plt.subplots(1, 4, figsize=(9, 2.4))
    for n, ax in enumerate(axes, start=1):
        ax.bar(np.arange(n, 6 * n + 1), dist, color="#0f766e")
        ax.set_title(f"{n} dice", fontsize=9)
        ax.set_yticks([])
        dist = np.convolve(dist, die)
    fig.tight_layout()


LESSON("Advanced", "Information: entropy, cross-entropy, KL", """
<p><b>Entropy</b> H(p) = −Σ p log₂ p measures uncertainty in bits. A fair coin: 1 bit. A certain outcome: 0 bits. Four equal options: 2 bits.</p>
<p><b>Cross-entropy</b> H(p, q) = −Σ p log q measures how well a model's prediction q matches the truth p. If the true class is "cat" (p = [1, 0, 0]) and the model says q = [0.7, 0.2, 0.1], the loss is −log 0.7. <b>This is the loss function of almost every classifier</b>, including large language models predicting the next word.</p>
<p><b>KL divergence</b> D(p‖q) = H(p, q) − H(p) is the extra cost of using q instead of p; it's 0 only when they match. Decision trees choose splits by <b>information gain</b> (entropy drop) or <b>Gini impurity</b>.</p>
""", practice=["Entropy", "Cross-Entropy", "KL Divergence", "Gini Impurity", "Information Gain of a Split"])


@LD
def entropy_curve():
    p = np.linspace(0.001, 0.999, 300)
    H = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    gini = 1 - p ** 2 - (1 - p) ** 2
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(p, H, label="entropy (bits)")
    ax.plot(p, gini, label="Gini impurity")
    ax.set_xlabel("P(heads)")
    ax.legend(fontsize=8)
    ax.set_title("Most uncertain at p = 0.5", fontsize=9)


LESSON("Advanced", "From scores to probabilities to a loss: softmax, log-loss, likelihood", """
<p>A classifier first produces raw scores (logits). <b>Softmax</b> turns them into probabilities: exponentiate, then divide by the total (subtract the max first so huge scores don't overflow). For two classes, softmax reduces to the sigmoid.</p>
<p>The <b>log-loss</b> (binary cross-entropy) −[y log p + (1 − y) log(1 − p)] punishes confident wrong answers enormously: predicting 0.01 for a true 1 costs −log 0.01 ≈ 4.6.</p>
<p>Where do these losses come from? <b>Maximum likelihood</b>: choose the parameters that make the observed data most probable. Maximising the log-likelihood of a Bernoulli model <i>is</i> minimising log-loss; for a normal model it <i>is</i> minimising squared error. That's the bridge from probability to machine learning.</p>
""", practice=["Softmax", "Binary Log-Loss", "Maximum Likelihood for a Coin", "Log-Likelihood Under a Normal Model"])


@LD
def log_loss_curve():
    p = np.linspace(0.01, 0.99, 200)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.8))
    left.plot(p, -np.log(p), label="true label 1: −log p")
    left.plot(p, -np.log(1 - p), label="true label 0: −log(1 − p)")
    left.set_xlabel("predicted probability")
    left.legend(fontsize=7)
    data = [1, 0, 1, 1]
    ll = 3 * np.log(p) + np.log(1 - p)
    right.plot(p, ll)
    right.axvline(np.mean(data), color="#b45309", linestyle="--")
    right.set_title("log-likelihood peaks at p = mean = 0.75", fontsize=8)
    fig.tight_layout()


LESSON("Basics", "PMF, PDF and CDF", """
<table><tr><th>Name</th><th>For</th><th>Gives</th></tr>
<tr><td>PMF</td><td>countable values (a die)</td><td>the probability of each value</td></tr>
<tr><td>PDF</td><td>continuous values (height)</td><td>density: probability is the <b>area</b></td></tr>
<tr><td>CDF</td><td>both</td><td>P(X ≤ x): always rises from 0 to 1</td></tr></table>
<h4>A die</h4>
<p>PMF: each value has 1/6. CDF at 4: P(X ≤ 4) = 4/6.</p>
<h4>Two facts about density that surprise people</h4>
<ul><li><b>A density can be above 1.</b> A uniform distribution on [0, 0.5] has height 2, and the area is still 0.5 × 2 = 1.</li>
<li><b>Exactly one value has probability 0.</b> P(height = exactly 170.000…) = 0, as a line has no area. Only ranges have probability.</li></ul>
<p>P(a ≤ X ≤ b) = CDF(b) − CDF(a).</p>
""", practice=["Uniform Distribution", "Height of the Normal Curve", "Area Under the Normal Curve"])


@LD
def pmf_pdf_cdf():
    values = np.arange(1, 7)
    pmf = np.full(6, 1 / 6)
    cdf = pmf.cumsum()
    at_four = cdf[3]
    fig, axes = plt.subplots(1, 3, figsize=(8.5, 2.4))
    axes[0].bar(values, pmf)
    axes[0].set_title("die: PMF", fontsize=9)
    axes[1].step(values, cdf, where="post")
    axes[1].set_title("die: CDF", fontsize=9)
    axes[2].fill_between([0, 0.5], [2, 2], alpha=0.4)
    axes[2].set_xlim(-0.2, 1)
    axes[2].set_title("uniform on [0, 0.5]: height 2, area 1", fontsize=9)
    fig.tight_layout()


LESSON("Core", "The binomial, by hand", """
<p>A player makes free throws with probability 0.8. What's the chance of exactly 4 from 5?</p>
<ol><li><b>One particular order</b> (hit, hit, hit, hit, miss): 0.8⁴ × 0.2 = 0.08192.</li>
<li><b>How many orders?</b> Choose which 4 shots hit: C(5, 4) = 5.</li>
<li><b>Multiply:</b> 5 × 0.08192 = <b>0.4096</b>.</li></ol>
<p>P(all 5) = 0.8⁵ = 0.3277, so P(at least 4) = 0.4096 + 0.3277 = 0.7373.</p>
<p><b>Shortcuts:</b> mean = np = 4; variance = np(1 − p) = 0.8.</p>
<h4>When to use it</h4>
<p>Check four conditions: a fixed number of tries, two outcomes, the same chance each time, and independent tries. Drawing cards without putting them back fails the last two.</p>
<h4>Related distributions</h4>
<ul><li>Many tries with a tiny chance (n large, p small) becomes <b>Poisson</b> with λ = np.</li>
<li>Many tries in general looks <b>normal</b>, as the chart shows.</li></ul>
""", practice=["Bernoulli Mean and Variance", "Binomial Probability Table", "Poisson Probability"])


@LD
def binomial_by_hand():
    one_order = 0.8 ** 4 * 0.2
    orders = math.comb(5, 4)
    exactly_four = orders * one_order
    all_five = 0.8 ** 5
    n, p = 100, 0.3
    k = np.arange(10, 51)
    pmf = np.array([math.comb(n, int(i)) * p ** int(i) * (1 - p) ** (n - int(i)) for i in k])
    mean, sd = n * p, (n * p * (1 - p)) ** 0.5
    normal = np.exp(-((k - mean) / sd) ** 2 / 2) / (sd * (2 * np.pi) ** 0.5)
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.bar(k, pmf, color="#99c9c2", label="Binomial(100, 0.3)")
    ax.plot(k, normal, color="#b45309", label="normal with same mean and sd")
    ax.legend(fontsize=7)


LESSON("Core", "z-scores and the normal curve, worked", """
<p>Heights have mean 170 cm and standard deviation 10 cm.</p>
<table><tr><th>Question</th><th>Steps</th><th>Answer</th></tr>
<tr><td>P(height &lt; 185)?</td><td>z = (185 − 170)/10 = 1.5; table gives 0.9332</td><td>93.3%</td></tr>
<tr><td>P(160 to 180)?</td><td>z from −1 to 1; 0.8413 − 0.1587</td><td>68.3%</td></tr>
<tr><td>P(height &gt; 185)?</td><td>1 − 0.9332</td><td>6.7%</td></tr>
<tr><td>Height of the tallest 10%?</td><td>z for 0.90 is 1.2816; 170 + 1.2816 × 10</td><td>182.8 cm</td></tr></table>
<h4>Comparing different scales</h4>
<p>Ana scores 80 in maths (mean 70, sd 10) and 75 in English (mean 60, sd 5). Which is better?</p>
<ul><li>Maths: z = 1.0</li><li>English: z = 3.0</li></ul>
<p>The lower mark is far more impressive. Standardising puts everything on a common scale.</p>
<p><b>Beware:</b> these answers assume the data is roughly normal. For skewed data such as income, they can be badly wrong. Plot first.</p>
""", practice=["The 68–95–99.7 Rule", "Z-Score to Percentile", "Exponential Waiting Time"])


@LD
def z_score_steps():
    def cdf(z):
        return 0.5 * (1 + math.erf(z / 2 ** 0.5))

    below_185 = cdf((185 - 170) / 10)
    between = cdf(1) - cdf(-1)
    above_185 = 1 - below_185
    tallest_ten_percent = 170 + 1.2816 * 10
    maths_z, english_z = (80 - 70) / 10, (75 - 60) / 5


LESSON("Advanced", "Entropy and KL divergence by hand", """
<h4>Entropy</h4>
<p>P = (0.5, 0.25, 0.25).</p>
<p>H = −0.5·log₂0.5 − 0.25·log₂0.25 − 0.25·log₂0.25 = 0.5 + 0.5 + 0.5 = <b>1.5 bits</b>.</p>
<p><b>Why bits?</b> Ask "is it A?" (1 question, half the time), then "is it B?" (2 questions otherwise): an average of 1.5 yes/no questions. A heavily biased coin (0.9, 0.1) has only 0.469 bits: it's rarely surprising.</p>
<h4>Cross-entropy</h4>
<p>Reality P = (0.5, 0.25, 0.25), but you believe Q = (0.25, 0.5, 0.25).</p>
<p>H(P, Q) = −0.5·log₂0.25 − 0.25·log₂0.5 − 0.25·log₂0.25 = 1 + 0.25 + 0.5 = <b>1.75 bits</b>. Using a wrong belief costs extra.</p>
<h4>KL divergence</h4>
<p>The extra cost: 1.75 − 1.5 = <b>0.25 bits</b>.</p>
<p><b>It isn't a true distance,</b> since direction matters. P = (0.9, 0.1) and Q = (0.5, 0.5) give KL(P‖Q) = 0.531, but KL(Q‖P) = 0.737.</p>
<p>Training a classifier minimises cross-entropy. As H(P) is fixed by the data, that also minimises KL: the predictions move towards the truth.</p>
""", practice=["Entropy", "Cross-Entropy", "KL Divergence", "Gini Impurity", "Information Gain of a Split"])


@LD
def information_by_hand():
    def entropy(p):
        return -sum(a * math.log2(a) for a in p if a > 0)

    def cross(p, q):
        return -sum(a * math.log2(b) for a, b in zip(p, q) if a > 0)

    p, q = [0.5, 0.25, 0.25], [0.25, 0.5, 0.25]
    h = entropy(p)
    ce = cross(p, q)
    kl = ce - h
    forward = cross([0.9, 0.1], [0.5, 0.5]) - entropy([0.9, 0.1])
    backward = cross([0.5, 0.5], [0.9, 0.1]) - entropy([0.5, 0.5])


LESSON("Advanced", "Maximum likelihood by hand", """
<p>A coin lands H, H, T, H. What p best explains this?</p>
<h4>Step 1: write the likelihood</h4>
<p>L(p) = p·p·(1 − p)·p = p³(1 − p).</p>
<table><tr><th>p</th><th>0.25</th><th>0.5</th><th>0.75</th><th>0.9</th></tr><tr><th>L(p)</th><td>0.0117</td><td>0.0625</td><td><b>0.1055</b></td><td>0.0729</td></tr></table>
<h4>Step 2: take logs, which turn products into sums</h4>
<p>ln L = 3 ln p + ln(1 − p).</p>
<h4>Step 3: set the derivative to zero</h4>
<p>3/p − 1/(1 − p) = 0, so 3(1 − p) = p and <b>p = 3/4</b>. It's simply the share of heads.</p>
<h4>The link to loss functions</h4>
<ul><li>Bernoulli likelihood → <b>log-loss</b></li><li>Normal likelihood → <b>squared error</b>, and the best μ is the mean</li><li>Categorical likelihood → <b>cross-entropy</b></li></ul>
<h4>Too little data</h4>
<p>After H, H, H the estimate is p = 1: "tails is impossible". Add one imaginary head and one imaginary tail (Laplace smoothing): (3 + 1) / (3 + 2) = 0.8. That's the same trick used in Naive Bayes, and it behaves like a prior.</p>
""", practice=["Maximum Likelihood for a Coin", "Log-Likelihood Under a Normal Model", "Binary Log-Loss", "Softmax"])


@LD
def coin_likelihood():
    p = np.linspace(0.01, 0.99, 197)
    likelihood = p ** 3 * (1 - p)
    log_likelihood = 3 * np.log(p) + np.log(1 - p)
    best = p[likelihood.argmax()]
    same_best = p[log_likelihood.argmax()]
    smoothed = (3 + 1) / (3 + 2)
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 2.6))
    left.plot(p, likelihood)
    left.axvline(best, ls="--", color="#b45309")
    left.set_title("likelihood", fontsize=9)
    right.plot(p, log_likelihood)
    right.axvline(same_best, ls="--", color="#b45309")
    right.set_title("log-likelihood: same peak", fontsize=9)
    fig.tight_layout()


LESSON("Core", "Means of samples: the central limit theorem at work", """
<p>Take a value from a skewed distribution, such as a waiting time. Now average 30 such values, and repeat many times. Those averages form a <b>bell curve</b> around the true mean, whatever the original shape.</p>
<p>Their spread, the standard error, is <b>σ / √n</b>:</p>
<table><tr><th>n</th><th>1</th><th>4</th><th>25</th><th>100</th></tr><tr><th>Spread when σ = 10</th><td>10</td><td>5</td><td>2</td><td>1</td></tr></table>
<p>So 4× the data halves the uncertainty, and 100× gives one-tenth. Diminishing returns, as the charts show.</p>
<h4>Why it matters</h4>
<ul><li><b>Confidence intervals</b> and A/B tests rely on it.</li>
<li><b>Mini-batch gradients</b> are averages. A larger batch gives a less noisy gradient, but quadrupling it only halves the noise, which is why small batches are usually efficient.</li></ul>
<p><b>Limits:</b> rows must be reasonably independent, and very heavy tails need many more samples.</p>
""", practice=["Distribution of the Sum of Two Dice", "Sum of Three Dice"])


@LD
def standard_error_demo():
    r = np.random.default_rng(0)
    sizes = [1, 4, 25, 100]
    fig, axes = plt.subplots(1, 4, figsize=(8.8, 2.3), sharex=True)
    measured = {}
    for ax, n in zip(axes, sizes):
        means = r.exponential(10, (5000, n)).mean(axis=1)
        measured[n] = round(float(means.std()), 2)
        ax.hist(means, bins=40, color="#0f766e")
        ax.set_xlim(0, 40)
        ax.set_yticks([])
        ax.set_title(f"n = {n}: spread {measured[n]}", fontsize=8)
    fig.tight_layout()
