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
