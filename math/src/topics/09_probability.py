from lib import *
import math
from itertools import product, permutations
import numpy as np

TOPIC(
    id="probability", title="Probability", glyph="P(A)",
    blurb="Measuring uncertainty: counting outcomes, permutations and combinations, the rules of probability, conditional probability, Bayes' theorem, independence and expected value.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">P(A) = favourable / total            # equally likely outcomes
P(not A) = 1 − P(A)
P(A or B) = P(A) + P(B) − P(A and B)
P(A and B) = P(A) · P(B | A)          # = P(A)·P(B) if independent
P(A | B) = P(A and B) / P(B)
P(A | B) = P(B | A) · P(A) / P(B)      # Bayes
math.perm(n, k), math.comb(n, k)      # ordered / unordered selections
E[X] = Σ x·P(x),  Var(X) = E[X²] − E[X]²</code></pre>
""")


Q(None, "Rolling a Total With Two Dice", "Easy", "Count the outcomes",
  "Return the probability that two fair dice add up to k, rounded to 4 decimals.",
  [((7,), 0.1667), ((2,), 0.0278), ((12,), 0.0278), ((13,), 0.0)],
  ("List all 36 equally likely pairs and count the ones that add to k.", "O(36)", "O(1)"),
  ("Build the 6 × 6 table of sums with <code>np.add.outer</code> and take the mean of (table == k).", "O(36)", "O(36)"))


@B
def dice_total(k):
    favourable = 0
    total = 0
    for a in range(1, 7):
        for b in range(1, 7):
            total += 1
            if a + b == k:
                favourable += 1
    return round(favourable / total, 4)


@O
def dice_total(k):
    sums = np.add.outer(np.arange(1, 7), np.arange(1, 7))
    return round((sums == k).mean(), 4)


Q(None, "At Least One Six", "Easy", "The complement rule",
  "Return the probability of at least one six in n rolls of a die, rounded to 4 decimals.",
  [((1,), 0.1667), ((2,), 0.3056), ((4,), 0.5177)],
  ("Enumerate all 6ⁿ sequences and count those containing a 6.", "O(6ⁿ · n)", "O(n)"),
  ("1 − P(no six at all) = 1 − (5/6)ⁿ.", "O(1)", "O(1)"))


@B
def at_least_one_six(n):
    hits = total = 0
    for rolls in product(range(1, 7), repeat=n):
        total += 1
        if 6 in rolls:
            hits += 1
    return round(hits / total, 4)


@O
def at_least_one_six(n):
    return round(1 - (5 / 6) ** n, 4)


Q(None, "Permutations", "Easy", "Order matters: n!/(n − k)!",
  "Return the number of ways to arrange k items chosen from n (e.g. gold, silver, bronze from 10 runners).",
  [((5, 2), 20), ((10, 3), 720), ((4, 4), 24)],
  ("Multiply n · (n − 1) · … for k factors: n choices for first place, n − 1 for second, …", "O(k)", "O(1)"),
  ("<code>math.perm(n, k)</code>.", "O(k)", "O(1)"))


@B
def permutations_count(n, k):
    ways = 1
    for i in range(k):
        ways *= n - i
    return ways


@O
def permutations_count(n, k):
    return math.perm(n, k)


Q(None, "Combinations", "Easy", "Order doesn't matter: n choose k",
  "Return the number of ways to choose k items from n when order does not matter.",
  [((5, 2), 10), ((10, 3), 120), ((6, 0), 1)],
  ("Pascal's triangle: build rows by adding the two numbers above.", "O(n·k)", "O(k)"),
  ("<code>math.comb(n, k)</code> = n! / (k!(n − k)!).", "O(k)", "O(1)"))


@B
def combinations_count(n, k):
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row[k]


@O
def combinations_count(n, k):
    return math.comb(n, k)


Q(None, "Arrangements With Repeated Letters", "Medium", "n! / (a!·b!·…)",
  "Return how many distinct arrangements the letters of the word have.",
  [(("BANANA",), 60), (("ABC",), 6), (("AAB",), 3)],
  ("Generate every permutation and count the distinct ones (only for short words!).", "O(n!)", "O(n!)"),
  ("Divide n! by the factorial of each letter's count.", "O(n)", "O(n)"))


@B
def arrangements(word):
    return len(set(permutations(word)))


@O
def arrangements(word):
    result = math.factorial(len(word))
    for letter in set(word):
        result //= math.factorial(word.count(letter))
    return result


Q(None, "Drawing a Card: Or", "Easy", "Addition rule",
  "From a standard 52-card deck, return P(card is a heart OR a king), rounded to 4 decimals.",
  [((), 0.3077)],
  ("Build all 52 cards and count those that are hearts or kings.", "O(52)", "O(52)"),
  ("P(A) + P(B) − P(A and B) = 13/52 + 4/52 − 1/52.", "O(1)", "O(1)"))


@B
def heart_or_king():
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["hearts", "diamonds", "clubs", "spades"]
    count = 0
    for r in ranks:
        for s in suits:
            if s == "hearts" or r == "K":
                count += 1
    return round(count / 52, 4)


@O
def heart_or_king():
    return round(13 / 52 + 4 / 52 - 1 / 52, 4)


Q(None, "Conditional Probability From a Table", "Medium", "P(A | B)",
  "table[i][j] counts people with row-category i and column-category j. Return P(row 0 | column 0), rounded to 4 decimals.",
  [(([[30, 10], [20, 40]],), 0.6), (([[5, 5], [15, 75]],), 0.25)],
  ("Restrict to column 0: count of row 0 there divided by the column total.", "O(rows)", "O(1)"),
  ("NumPy: <code>T[0, 0] / T[:, 0].sum()</code>.", "O(rows)", "O(1)"))


@B
def conditional(table):
    column_total = 0
    for row in table:
        column_total += row[0]
    return round(table[0][0] / column_total, 4)


@O
def conditional(table):
    T = np.array(table)
    return round(T[0, 0] / T[:, 0].sum(), 4)


Q(None, "Bayes' Theorem: Medical Test", "Medium", "P(disease | positive)",
  "A disease affects a fraction prior of people. The test detects it with probability sens and gives false positives with probability fpr. Return P(disease | positive), rounded to 4 decimals.",
  [((0.01, 0.99, 0.05), 0.1667), ((0.1, 0.9, 0.2), 0.3333)],
  ("Imagine 1 000 000 people: count sick-and-positive and healthy-and-positive, then divide.", "O(1)", "O(1)"),
  ("Bayes: P(D|+) = P(+|D)P(D) / [P(+|D)P(D) + P(+|¬D)P(¬D)].", "O(1)", "O(1)"),
  names=["prior", "sens", "fpr"])


@B
def bayes(prior, sens, fpr):
    people = 1_000_000
    sick = people * prior
    healthy = people - sick
    true_positives = sick * sens
    false_positives = healthy * fpr
    return round(true_positives / (true_positives + false_positives), 4)


@O
def bayes(prior, sens, fpr):
    evidence = sens * prior + fpr * (1 - prior)
    return round(sens * prior / evidence, 4)


Q(None, "Law of Total Probability", "Easy", "Weighted average over cases",
  "Factories make shares[i] of the products with defect rates rates[i]. Return the overall defect rate, rounded to 4 decimals.",
  [(([0.5, 0.3, 0.2], [0.1, 0.2, 0.5]), 0.21), (([1.0], [0.03]), 0.03)],
  ("Loop: add share × rate for each factory.", "O(k)", "O(1)"),
  ("A dot product: <code>shares @ rates</code>.", "O(k)", "O(1)"))


@B
def total_probability(shares, rates):
    total = 0
    for s, r in zip(shares, rates):
        total += s * r
    return round(total, 4)


@O
def total_probability(shares, rates):
    return round(np.array(shares) @ np.array(rates), 4)


Q(None, "Expected Value", "Easy", "E[X] = Σ x·P(x)",
  "Return the expected value of a random variable with the given values and probabilities, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5, 6], [1 / 6] * 6), 3.5), (([0, 100], [0.9, 0.1]), 10.0), (([-5, 20], [0.8, 0.2]), 0.0)],
  ("Loop: add value × probability.", "O(n)", "O(1)"),
  ("<code>np.dot(values, probs)</code>.", "O(n)", "O(1)"))


@B
def expected(values, probs):
    total = 0
    for v, p in zip(values, probs):
        total += v * p
    return round(total, 4) + 0.0


@O
def expected(values, probs):
    return round(np.dot(values, probs), 4) + 0.0


Q(None, "Variance of a Random Variable", "Medium", "E[(X − μ)²]",
  "Return the variance of a discrete random variable, rounded to 4 decimals.",
  [(([1, 2, 3, 4, 5, 6], [1 / 6] * 6), 2.9167), (([0, 1], [0.5, 0.5]), 0.25)],
  ("Mean first, then the probability-weighted average of squared distances from it.", "O(n)", "O(1)"),
  ("Shortcut E[X²] − E[X]² with NumPy dot products.", "O(n)", "O(n)"))


@B
def variance(values, probs):
    mean = sum(v * p for v, p in zip(values, probs))
    total = 0
    for v, p in zip(values, probs):
        total += (v - mean) ** 2 * p
    return round(total, 4)


@O
def variance(values, probs):
    v, p = np.array(values, dtype=float), np.array(probs)
    return round(p @ v ** 2 - (p @ v) ** 2, 4)


Q(None, "The Birthday Problem", "Medium", "Surprisingly likely coincidences",
  "Return the probability that at least two of n people share a birthday (365 equally likely days), rounded to 4 decimals.",
  [((2,), 0.0027), ((23,), 0.5073), ((50,), 0.9704)],
  ("Multiply the chances that each new person avoids all earlier birthdays: 365/365 · 364/365 · …, then take 1 minus.", "O(n)", "O(1)"),
  ("<code>1 - math.perm(365, n) / 365 ** n</code>.", "O(n)", "O(1)"))


@B
def birthday(n):
    all_different = 1.0
    for i in range(n):
        all_different *= (365 - i) / 365
    return round(1 - all_different, 4)


@O
def birthday(n):
    return round(1 - math.perm(365, n) / 365 ** n, 4)


Q(None, "At Least k Heads", "Medium", "Summing binomial counts",
  "Return P(at least k heads in n fair coin flips), rounded to 4 decimals.",
  [((4, 2), 0.6875), ((10, 8), 0.0547), ((3, 0), 1.0)],
  ("Enumerate all 2ⁿ flip sequences and count those with ≥ k heads.", "O(2ⁿ · n)", "O(n)"),
  ("Σ C(n, i) for i ≥ k, divided by 2ⁿ.", "O(n)", "O(1)"))


@B
def at_least_k_heads(n, k):
    hits = 0
    for flips in product([0, 1], repeat=n):
        if sum(flips) >= k:
            hits += 1
    return round(hits / 2 ** n, 4)


@O
def at_least_k_heads(n, k):
    return round(sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n, 4)


Q(None, "All Parts Must Work", "Easy", "Independent events multiply",
  "A machine works only if every part works; part i works with probability ps[i], independently. Return (P(machine works), P(at least one part fails)), rounded to 4 decimals.",
  [(([0.9, 0.95, 0.98],), (0.8379, 0.1621)), (([0.5, 0.5],), (0.25, 0.75))],
  ("Multiply the probabilities in a loop; the failure chance is the complement.", "O(n)", "O(1)"),
  ("<code>np.prod(ps)</code>.", "O(n)", "O(1)"))


@B
def all_work(ps):
    works = 1.0
    for p in ps:
        works *= p
    return (round(works, 4), round(1 - works, 4))


@O
def all_work(ps):
    works = np.prod(ps)
    return (round(works, 4), round(1 - works, 4))


Q(None, "Are the Events Independent?", "Medium", "P(A and B) = P(A)·P(B)",
  "joint[i][j] = P(X = i and Y = j). Return True if X and Y are independent (within 1e-9).",
  [(([[0.06, 0.14], [0.24, 0.56]],), True), (([[0.1, 0.2], [0.3, 0.4]],), False)],
  ("Compute the row and column totals, then check every cell equals row total × column total.", "O(r·c)", "O(r + c)"),
  ("Compare the table with <code>np.outer</code> of its marginals.", "O(r·c)", "O(r·c)"))


@B
def independent(joint):
    rows = [sum(r) for r in joint]
    cols = [sum(r[j] for r in joint) for j in range(len(joint[0]))]
    for i in range(len(rows)):
        for j in range(len(cols)):
            if abs(joint[i][j] - rows[i] * cols[j]) > 1e-9:
                return False
    return True


@O
def independent(joint):
    J = np.array(joint)
    return bool(np.allclose(J, np.outer(J.sum(axis=1), J.sum(axis=0)), atol=1e-9))


Q(None, "Marginal Probabilities", "Easy", "Summing out a variable",
  "From a joint probability table, return (row totals, column totals), rounded to 4 decimals.",
  [(([[0.1, 0.2], [0.3, 0.4]],), ([0.3, 0.7], [0.4, 0.6]))],
  ("Add along each row and down each column with loops.", "O(r·c)", "O(r + c)"),
  ("<code>J.sum(axis=1)</code> and <code>J.sum(axis=0)</code>.", "O(r·c)", "O(r + c)"))


@B
def marginals(joint):
    rows = [round(sum(r), 4) for r in joint]
    cols = [round(sum(r[j] for r in joint), 4) for j in range(len(joint[0]))]
    return (rows, cols)


@O
def marginals(joint):
    J = np.array(joint)
    return (J.sum(axis=1).round(4), J.sum(axis=0).round(4))


Q(None, "Monty Hall", "Medium", "Should you switch?",
  "Three doors, one car. You pick a door; the host opens a different door with a goat. Return (P(win if you stay), P(win if you switch)), rounded to 4 decimals.",
  [((), (0.3333, 0.6667))],
  ("Enumerate every equally likely (car position, first pick) pair and play both strategies.", "O(9)", "O(1)"),
  ("Reason: staying wins only if the first pick was right (1/3); switching wins otherwise (2/3).", "O(1)", "O(1)"))


@B
def monty_hall():
    stay = switch = games = 0
    for car in range(3):
        for pick in range(3):
            games += 1
            opened = next(d for d in range(3) if d != pick and d != car)
            other = next(d for d in range(3) if d != pick and d != opened)
            stay += pick == car
            switch += other == car
    return (round(stay / games, 4), round(switch / games, 4))


@O
def monty_hall():
    return (round(1 / 3, 4), round(2 / 3, 4))


Q(None, "Naive Bayes Spam Score", "Hard", "Multiply likelihoods, normalise",
  "Given P(spam), and for each word in an email P(word | spam) and P(word | ham), return P(spam | words) assuming words are independent. Rounded to 4 decimals.",
  [((0.8, [0.6, 0.5, 0.4], [0.1, 0.3, 0.6]), 0.9639), ((0.5, [0.5], [0.5]), 0.5)],
  ("Multiply the prior by every likelihood for each class, then divide by the sum.", "O(n)", "O(1)"),
  ("Add logs instead of multiplying (safe for thousands of words), then convert back.", "O(n)", "O(n)"),
  names=["prior", "p_spam", "p_ham"])


@B
def spam_score(prior, p_spam, p_ham):
    spam = prior
    ham = 1 - prior
    for a, b in zip(p_spam, p_ham):
        spam *= a
        ham *= b
    return round(spam / (spam + ham), 4)


@O
def spam_score(prior, p_spam, p_ham):
    log_spam = np.log(prior) + np.log(p_spam).sum()
    log_ham = np.log(1 - prior) + np.log(p_ham).sum()
    return round(1 / (1 + np.exp(log_ham - log_spam)), 4)


Q(None, "Waiting for the First Success", "Medium", "Geometric distribution: E = 1/p",
  "Each try succeeds with probability p. Return the expected number of tries until the first success, rounded to 4 decimals.",
  [((0.5,), 2.0), ((0.2,), 5.0), ((1 / 6,), 6.0)],
  ("Add k·P(first success on try k) = k(1 − p)ᵏ⁻¹p for k = 1 … 2000.", "O(K)", "O(1)"),
  ("Known result: 1/p.", "O(1)", "O(1)"))


@B
def expected_tries(p):
    total = 0
    for k in range(1, 2001):
        total += k * (1 - p) ** (k - 1) * p
    return round(total, 4)


@O
def expected_tries(p):
    return round(1 / p, 4)


Q(None, "Two Draws Without Replacement", "Easy", "Multiplication rule",
  "A bag has red and blue balls. Draw two without putting the first back. Return P(both red), rounded to 4 decimals.",
  [((5, 3), 0.3571), ((3, 7), 0.0667)],
  ("List all ordered pairs of different balls and count the red-red ones.", "O(n²)", "O(1)"),
  ("P(red first) · P(red second | red first) = r/n · (r − 1)/(n − 1).", "O(1)", "O(1)"))


@B
def both_red(red, blue):
    balls = ["R"] * red + ["B"] * blue
    hits = total = 0
    for i in range(len(balls)):
        for j in range(len(balls)):
            if i != j:
                total += 1
                if balls[i] == "R" and balls[j] == "R":
                    hits += 1
    return round(hits / total, 4)


@O
def both_red(red, blue):
    n = red + blue
    return round(red / n * (red - 1) / (n - 1), 4)
