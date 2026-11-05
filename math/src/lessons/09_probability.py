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


LESSON("Basics", "List the outcomes first", """
<p>Most probability mistakes come from not listing what can happen.</p>
<h4>Two coins: P(at least one head)?</h4>
<p>A tempting answer: "0, 1 or 2 heads, so 2 out of 3". But those three aren't equally likely. List properly:</p>
<table><tr><th>Outcome</th><th>HH</th><th>HT</th><th>TH</th><th>TT</th></tr><tr><th>Probability</th><td>1/4</td><td>1/4</td><td>1/4</td><td>1/4</td></tr></table>
<p>Three of the four have a head, so <b>P = 3/4</b>.</p>
<h4>Using a probability tree</h4>
<p>Multiply along branches, add across paths. For two flips, P(exactly one head) = ½·½ + ½·½ = ½.</p>
<h4>Helpful checks</h4>
<ul><li>All probabilities must add to 1.</li>
<li>"At least one" is usually easiest as 1 − P(none).</li>
<li>Results always lie between 0 and 1.</li></ul>
<h4>The gambler's fallacy</h4>
<p>After 5 heads in a row, the next flip is still 50/50. Coins have no memory. A run of bad luck doesn't make good luck "due".</p>
""", practice=["Rolling a Total With Two Dice", "At Least One Six", "Drawing a Card: Or"])


@LD
def coins_listing():
    from itertools import product
    outcomes = list(product("HT", repeat=2))
    with_a_head = [o for o in outcomes if "H" in o]
    probability = len(with_a_head) / len(outcomes)
    exactly_one = sum(o.count("H") == 1 for o in outcomes) / len(outcomes)
    three_flips = 1 - 0.5 ** 3


LESSON("Core", "Counting, worked", """
<p>Ask two questions: <b>does order matter?</b> and <b>can things repeat?</b></p>
<table><tr><th>Question</th><th>Order?</th><th>Repeats?</th><th>Calculation</th><th>Answer</th></tr>
<tr><td>4-digit PINs</td><td>yes</td><td>yes</td><td>10⁴</td><td>10,000</td></tr>
<tr><td>4-digit PINs with no repeats</td><td>yes</td><td>no</td><td>10·9·8·7</td><td>5,040</td></tr>
<tr><td>Team of 3 from 10</td><td>no</td><td>no</td><td>(10·9·8) / 3!</td><td>120</td></tr></table>
<p><b>Why divide by 3!?</b> Each team of Ana, Ben, Cy was counted in 6 orders: ABC, ACB, BAC, BCA, CAB, CBA.</p>
<h4>Using counts to get a probability</h4>
<p>Two cards from a deck. P(both aces)?</p>
<ul><li>Ways to choose 2 aces: C(4, 2) = 6.</li>
<li>Ways to choose any 2 cards: C(52, 2) = 1,326.</li>
<li>P = 6 / 1326 = <b>0.0045</b>.</li></ul>
<p>Step by step gives the same: (4/52) × (3/51) = 0.0045. Pick whichever seems easier.</p>
""", practice=["Permutations", "Combinations", "Arrangements With Repeated Letters", "At Least k Heads", "The Birthday Problem"])


@LD
def counting_checks():
    pins = 10 ** 4
    no_repeats = math.perm(10, 4)
    teams = math.comb(10, 3)
    orders_of_a_team = math.factorial(3)
    by_counting = math.comb(4, 2) / math.comb(52, 2)
    step_by_step = (4 / 52) * (3 / 51)


LESSON("Core", "Conditional probability with a table", """
<p>100 people:</p>
<table><tr><th></th><th>Smoker</th><th>Non-smoker</th><th>Total</th></tr>
<tr><th>Cough</th><td>30</td><td>10</td><td>40</td></tr>
<tr><th>No cough</th><td>20</td><td>40</td><td>60</td></tr>
<tr><th>Total</th><td>50</td><td>50</td><td>100</td></tr></table>
<p>Conditioning means <b>shrinking your world to one row or column.</b></p>
<table><tr><th>Question</th><th>Look only at</th><th>Answer</th></tr>
<tr><td>P(cough | smoker)</td><td>smokers: 50 people</td><td>30 / 50 = 0.6</td></tr>
<tr><td>P(smoker | cough)</td><td>coughers: 40 people</td><td>30 / 40 = 0.75</td></tr>
<tr><td>P(cough)</td><td>everyone</td><td>40 / 100 = 0.4</td></tr>
<tr><td>P(cough and smoker)</td><td>everyone</td><td>30 / 100 = 0.3</td></tr></table>
<h4>The biggest confusion</h4>
<p><b>P(A | B) isn't P(B | A).</b> Nearly all cats have four legs, but few four-legged animals are cats.</p>
<h4>Independent?</h4>
<p>Smoking and coughing would be independent if P(cough | smoker) equalled P(cough). Here 0.6 ≠ 0.4, so they're related. <b>Related doesn't prove one causes the other.</b></p>
""", practice=["Conditional Probability From a Table", "Are the Events Independent?", "Marginal Probabilities", "Two Draws Without Replacement", "All Parts Must Work", "Law of Total Probability"])


@LD
def table_conditioning():
    table = np.array([[30, 10], [20, 40]])
    cough_given_smoker = table[0, 0] / table[:, 0].sum()
    smoker_given_cough = table[0, 0] / table[0].sum()
    cough = table[0].sum() / table.sum()
    both = table[0, 0] / table.sum()
    expected_if_independent = cough * (table[:, 0].sum() / table.sum())


LESSON("Advanced", "Bayes: updating step by step", """
<p>Recall the test: 1% have the disease, it detects 99% of cases, and flags 5% of healthy people. One positive result means a <b>16.7%</b> chance of disease.</p>
<h4>A second positive test</h4>
<p>Today's answer becomes tomorrow's prior. Now start from 0.167:</p>
<p>P = (0.99 × 0.167) / (0.99 × 0.167 + 0.05 × 0.833) = <b>0.798</b>.</p>
<p>Two independent positive tests take us from 1% to about 80%. That's Bayesian updating.</p>
<h4>The prior matters enormously</h4>
<table><tr><th>How common is it?</th><th>0.1%</th><th>1%</th><th>10%</th><th>50%</th></tr>
<tr><th>P(disease | positive)</th><td>1.9%</td><td>16.7%</td><td>68.8%</td><td>95.2%</td></tr></table>
<p>The same test gives very different meanings. This is why screening for rare conditions gives many false alarms, and why a rare-class classifier can have high accuracy but low precision.</p>
""", practice=["Bayes' Theorem: Medical Test", "Naive Bayes Spam Score", "Monty Hall"])


@LD
def bayes_updates():
    def update(prior, sensitivity=0.99, false_alarm=0.05):
        return sensitivity * prior / (sensitivity * prior + false_alarm * (1 - prior))

    first = update(0.01)
    second = update(first)
    priors = np.logspace(-3, -0.01, 100)
    posteriors = update(priors)
    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    ax.semilogx(priors, posteriors)
    ax.set_xlabel("how common the disease is (prior)")
    ax.set_ylabel("P(disease | positive)")


LESSON("Advanced", "Expected value for decisions", """
<h4>Is this ticket worth it?</h4>
<p>A ₹10 ticket gives a 1 in 200 chance of ₹1,000. E[winnings] = 1000 × 1/200 = ₹5. Subtract the cost: <b>−₹5 per ticket on average</b>.</p>
<h4>Expected values simply add</h4>
<p>E[X + Y] = E[X] + E[Y], <b>even when they're related</b>. Two dice: 3.5 + 3.5 = 7. This makes hard-looking problems easy.</p>
<p><b>Example:</b> shuffle n name-tags and hand them out. On average, how many people get their own? Each person has a 1/n chance, so the total is n × 1/n = <b>1</b>, for any n.</p>
<h4>Variance adds only if independent</h4>
<p>One die has variance 2.92, and two independent dice 5.83.</p>
<h4>Expected cost in ML</h4>
<p>If a missed fraud costs ₹5,000 and a false alarm ₹50, flag when P(fraud) × 5000 &gt; (1 − P(fraud)) × 50, or P(fraud) &gt; about 0.0099. The threshold comes from the costs, not from 0.5.</p>
""", practice=["Expected Value", "Variance of a Random Variable", "Waiting for the First Success"])


@LD
def expected_checks():
    ticket = 1000 * (1 / 200) - 10
    r = np.random.default_rng(0)
    own_tags = [(r.permutation(10) == np.arange(10)).sum() for _ in range(5000)]
    average_fixed = float(np.mean(own_tags))
    two_dice = r.integers(1, 7, (20000, 2)).sum(axis=1)
    mean_var = (round(float(two_dice.mean()), 2), round(float(two_dice.var()), 2))
    threshold = 50 / (5000 + 50)
