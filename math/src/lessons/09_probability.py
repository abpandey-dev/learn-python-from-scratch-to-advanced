from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LESSON("Basics", "What is probability?", """
<p><b>Probability</b> is a number from 0 to 1 measuring how likely something is: 0 = impossible, 1 = certain, 0.5 = a coin flip.</p>
<ul>
<li>An <b>experiment</b> (rolling a die) has <b>outcomes</b> (1 … 6). All possible outcomes form the <b>sample space</b>.</li>
<li>An <b>event</b> is a set of outcomes ("an even number" = {2, 4, 6}).</li>
<li>When outcomes are equally likely: <b>P(event) = favourable outcomes / total outcomes</b>. P(even) = 3/6 = 0.5.</li>
<li><b>Complement</b>: P(not A) = 1 − P(A). Often the easy way round: P(at least one six in 4 rolls) = 1 − (5/6)⁴.</li>
</ul>
<p>A classifier that outputs "spam: 0.93" is giving a probability.</p>
""", practice=["Rolling a Total With Two Dice", "At Least One Six", "Drawing a Card: Or"])


@LD
def two_dice():
    sums = np.add.outer(np.arange(1, 7), np.arange(1, 7))
    totals, counts = np.unique(sums, return_counts=True)
    probs = counts / 36
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(totals, probs, color="#0f766e")
    ax.set_xticks(totals)
    ax.set_xlabel("sum of two dice")
    ax.set_ylabel("probability")
    ax.set_title("7 is most likely: 6 of 36 ways", fontsize=9)


LESSON("Basics", "Counting: permutations and combinations", """
<p>Probabilities often need you to count outcomes without listing them all.</p>
<ul>
<li><b>Multiplication principle</b>: 3 shirts × 4 trousers = 12 outfits.</li>
<li><b>Permutations</b> (order matters): choosing gold/silver/bronze from 10 runners: 10·9·8 = 720 = n!/(n − k)!.</li>
<li><b>Combinations</b> (order doesn't matter): choosing a 3-person team from 10: 720/3! = 120 = C(10, 3) = n!/(k!(n − k)!).</li>
<li>Repeated items: BANANA has 6!/(3!·2!) = 60 arrangements.</li>
</ul>
""", practice=["Permutations", "Combinations", "Arrangements With Repeated Letters", "At Least k Heads", "The Birthday Problem"])


@LD
def pascal():
    rows = [[1]]
    for _ in range(6):
        prev = rows[-1]
        rows.append([1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1])
    check = math.comb(6, 2)


LESSON("Core", "Combining events: and, or, conditional", """
<table>
<tr><th>Rule</th><th>Formula</th></tr>
<tr><td>Or (addition)</td><td>P(A or B) = P(A) + P(B) − P(A and B)</td></tr>
<tr><td>And (multiplication)</td><td>P(A and B) = P(A) · P(B | A)</td></tr>
<tr><td>Independent</td><td>P(A and B) = P(A) · P(B)</td></tr>
<tr><td>Conditional</td><td>P(A | B) = P(A and B) / P(B)</td></tr>
</table>
<p><b>P(A | B)</b> reads "probability of A <b>given</b> B": shrink your world to only the cases where B happened. From a table of counts, divide the cell by its row or column total.</p>
<p>Independence means knowing B tells you nothing about A (two coin flips). Drawing cards <b>without replacement</b> is not independent: the first draw changes the second.</p>
""", practice=["Conditional Probability From a Table", "Two Draws Without Replacement", "All Parts Must Work", "Are the Events Independent?", "Marginal Probabilities", "Law of Total Probability"])


@LD
def contingency():
    table = np.array([[30, 10], [20, 40]])
    total = table.sum()
    p_row0 = table[0].sum() / total
    p_col0 = table[:, 0].sum() / total
    p_row0_given_col0 = table[0, 0] / table[:, 0].sum()
    p_both = table[0, 0] / total
    independent = np.isclose(p_both, p_row0 * p_col0)


LESSON("Core", "Bayes' theorem: updating beliefs", """
<p>Bayes' theorem flips a conditional probability around:</p>
<p style="text-align:center"><b>P(A | B) = P(B | A) · P(A) / P(B)</b></p>
<p>Classic example: a disease affects 1% of people; a test catches 99% of cases but also flags 5% of healthy people. If you test positive, how worried should you be? Picture 10 000 people: 100 sick → 99 test positive; 9 900 healthy → 495 test positive. Of 594 positives only 99 are sick: <b>about 17%</b>. The rare <b>prior</b> dominates.</p>
<p>The <b>Naive Bayes</b> classifier applies Bayes to every word of an email and multiplies the evidence — fast, simple and still used for spam filtering.</p>
""", practice=["Bayes' Theorem: Medical Test", "Naive Bayes Spam Score", "Monty Hall"])


@LD
def bayes_picture():
    people = 10000
    sick = people * 0.01
    healthy = people - sick
    true_pos = sick * 0.99
    false_pos = healthy * 0.05
    p_sick_given_pos = true_pos / (true_pos + false_pos)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.barh(["tested positive"], [true_pos], color="#b91c1c", label=f"sick ({true_pos:.0f})")
    ax.barh(["tested positive"], [false_pos], left=[true_pos], color="#9ca3af", label=f"healthy ({false_pos:.0f})")
    ax.legend(fontsize=8)
    ax.set_title(f"P(sick | positive) = {p_sick_given_pos:.0%}", fontsize=9)


LESSON("Advanced", "Random variables and expected value", """
<p>A <b>random variable</b> X assigns a number to each outcome (the value of a die, your winnings in a game). Its <b>distribution</b> lists each value with its probability.</p>
<ul>
<li><b>Expected value</b> E[X] = Σ x·P(x): the long-run average. A die: 3.5.</li>
<li><b>Variance</b> Var(X) = E[(X − μ)²] = E[X²] − (E[X])²: how spread out the outcomes are. Its square root is the standard deviation.</li>
<li>Waiting for a success with chance p takes 1/p tries on average.</li>
</ul>
<p>ML models are often judged by <b>expected loss</b> — the average error over all the data they might see.</p>
""", practice=["Expected Value", "Variance of a Random Variable", "Waiting for the First Success"])


@LD
def expected_value_demo():
    values = np.arange(1, 7)
    probs = np.full(6, 1 / 6)
    mean = values @ probs
    variance = probs @ (values - mean) ** 2
    running = np.cumsum([3, 6, 1, 4, 4, 2, 5, 6, 3, 1, 2, 5, 4, 6, 3, 2, 5, 1, 4, 3]) / np.arange(1, 21)
    fig, ax = plt.subplots(figsize=(5, 2.8))
    ax.plot(np.arange(1, 21), running, "o-", markersize=3, label="running average of rolls")
    ax.axhline(mean, color="#b45309", linestyle="--", label="E[X] = 3.5")
    ax.legend(fontsize=8)
    ax.set_xlabel("number of rolls")
