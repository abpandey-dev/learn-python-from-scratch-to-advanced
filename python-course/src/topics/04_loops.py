from lib import *

TOPIC(
    id="loops", title="Loops (for / while)", glyph="↻ for",
    blurb="Repeat work with for and while, control loops with break and continue, and nest loops for patterns.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">for i in range(5):            # 0 1 2 3 4
for i in range(2, 10, 3):     # 2 5 8
for ch in "hey":              # loop over any sequence
for i, x in enumerate(items): # index and value
while n &gt; 0:                  # repeat while the condition is True
    n -= 1
break      # leave the loop now
continue   # skip to the next round
for … else:  # else runs if the loop did NOT break</code></pre>
<ul>
<li><code>range(stop)</code>, <code>range(start, stop)</code>, <code>range(start, stop, step)</code> — stop is <b>excluded</b>.</li>
<li>Accumulator pattern: <code>total = 0</code> before the loop, <code>total += x</code> inside.</li>
<li>A while loop must change something in its condition, or it never ends.</li>
</ul>
""")


Q(None, "Multiplication Table", "Easy", "for · range",
  "Return the list <code>[n×1, n×2, …, n×10]</code>.",
  [((3,), [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]), ((1,), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])],
  ("A while loop with a manual counter and append.", "O(10)", "O(10)"),
  ("A for loop over <code>range(1, 11)</code> inside a list comprehension.", "O(10)", "O(10)"),
  viz=(3,))


@B
def table(n):
    result = []
    i = 1
    while i <= 10:
        result.append(n * i)
        i = i + 1
    return result


@O
def table(n):
    return [n * i for i in range(1, 11)]


Q(None, "Factorial", "Easy", "Accumulator",
  "Return n! = 1 × 2 × … × n (0! = 1).",
  [((5,), 120), ((0,), 1), ((10,), 3628800)],
  ("A while loop counting down and multiplying.", "O(n)", "O(1)"),
  ("A for loop over range, or <code>math.prod(range(1, n + 1))</code>.", "O(n)", "O(1)"),
  viz=(5,))


@B
def factorial(n):
    result = 1
    while n > 1:
        result = result * n
        n = n - 1
    return result


@O
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


Q(None, "Count Vowels", "Easy", "Loop over a string",
  "Return how many vowels (a, e, i, o, u, either case) are in <code>text</code>.",
  [(("Hello World",), 3), (("PYTHON",), 1), (("rhythm",), 0)],
  ("Loop over indices, compare each character with every vowel.", "O(n)", "O(1)"),
  ("Loop over characters directly and count with <code>sum</code> and <code>in</code>.", "O(n)", "O(1)"),
  viz=("Loop it",))


@B
def count_vowels(text):
    count = 0
    for i in range(len(text)):
        ch = text[i].lower()
        if ch == "a" or ch == "e" or ch == "i" or ch == "o" or ch == "u":
            count += 1
    return count


@O
def count_vowels(text):
    return sum(1 for ch in text.lower() if ch in "aeiou")


Q(None, "Sum of Even Numbers", "Easy", "range with step",
  "Return the sum of all even numbers from 1 to n.",
  [((10,), 30), ((7,), 12), ((1,), 0)],
  ("Loop over every number and add it when it's even.", "O(n)", "O(1)"),
  ("<code>range(2, n + 1, 2)</code> produces only even numbers.", "O(n)", "O(1)"),
  viz=(7,))


@B
def sum_even(n):
    total = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i
    return total


@O
def sum_even(n):
    return sum(range(2, n + 1, 2))


Q(None, "Fibonacci Sequence", "Easy", "Two running variables",
  "Return the first n Fibonacci numbers: 0, 1, 1, 2, 3, 5, …",
  [((7,), [0, 1, 1, 2, 3, 5, 8]), ((1,), [0]), ((2,), [0, 1])],
  ("Build the list by reading the last two elements each time.", "O(n)", "O(n)"),
  ("Keep just two variables and update them together: <code>a, b = b, a + b</code>.", "O(n)", "O(n) output"),
  viz=(6,))


@B
def fibonacci(n):
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[len(seq) - 1] + seq[len(seq) - 2])
    return seq[:n]


@O
def fibonacci(n):
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


Q(None, "Is It Prime?", "Medium", "Loop with early exit",
  "Return True if n is a prime number (only divisible by 1 and itself).",
  [((7,), True), ((12,), False), ((1,), False), ((97,), True)],
  ("Try every divisor from 2 to n − 1.", "O(n)", "O(1)"),
  ("Divisors come in pairs, so testing up to √n is enough; stop at the first divisor found.", "O(√n)", "O(1)"),
  viz=(29,))


@B
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


@O
def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


Q(None, "Greatest Common Divisor", "Medium", "while loop · Euclid",
  "Return the GCD of two positive integers.",
  [((48, 18), 6), ((17, 5), 1), ((100, 75), 25)],
  ("Count down from the smaller number until one divides both.", "O(min(a, b))", "O(1)"),
  ("Euclid's algorithm: replace (a, b) with (b, a % b) until b is 0.", "O(log min(a, b))", "O(1)"))


@B
def gcd(a, b):
    d = min(a, b)
    while d > 1:
        if a % d == 0 and b % d == 0:
            return d
        d -= 1
    return 1


@O
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


Q(None, "Countdown", "Easy", "range backwards",
  "Return the list <code>[n, n−1, …, 1]</code>.",
  [((5,), [5, 4, 3, 2, 1]), ((1,), [1]), ((0,), [])],
  ("A while loop that appends and decrements.", "O(n)", "O(n)"),
  ("<code>range(n, 0, -1)</code> counts down directly.", "O(n)", "O(n)"))


@B
def countdown(n):
    out = []
    while n > 0:
        out.append(n)
        n -= 1
    return out


@O
def countdown(n):
    return list(range(n, 0, -1))


Q(None, "First Position of a Value", "Easy", "break · enumerate",
  "Return the index of the first <code>target</code> in <code>items</code>, or −1 if it isn't there.",
  [(([4, 9, 2, 9], 9), 1), (([1, 2, 3], 7), -1), ((["a", "b"], "a"), 0)],
  ("Loop over indices with a 'found' flag and break.", "O(n)", "O(1)"),
  ("<code>enumerate</code> gives index and value; return as soon as you find it.", "O(n)", "O(1)"),
  viz=([4, 9, 2, 9], 2))


@B
def first_index(items, target):
    found = -1
    i = 0
    while i < len(items):
        if items[i] == target:
            found = i
            break
        i += 1
    return found


@O
def first_index(items, target):
    for i, x in enumerate(items):
        if x == target:
            return i
    return -1


Q(None, "Star Triangle", "Easy", "Nested loops · patterns",
  "Return the rows of a right triangle of stars of height n, e.g. n = 3 → ['*', '**', '***'].",
  [((3,), ["*", "**", "***"]), ((1,), ["*"])],
  ("An outer loop for rows and an inner loop that adds one star at a time.", "O(n²)", "O(n²)"),
  ("String repetition <code>'*' * i</code> replaces the inner loop.", "O(n²)", "O(n²)"),
  viz=(3,))


@B
def triangle_rows(n):
    rows = []
    for i in range(1, n + 1):
        row = ""
        for j in range(i):
            row = row + "*"
        rows.append(row)
    return rows


@O
def triangle_rows(n):
    return ["*" * i for i in range(1, n + 1)]


Q(None, "Collatz Steps", "Medium", "while with a changing condition",
  "Starting at n, if n is even halve it, otherwise make it 3n + 1. Return how many steps it takes to reach 1.",
  [((6,), 8), ((1,), 0), ((27,), 111)],
  ("Store every value in a list, then the answer is its length − 1.", "O(steps)", "O(steps)"),
  ("Only a counter is needed — no list.", "O(steps)", "O(1)"),
  viz=(6,))


@B
def collatz_steps(n):
    sequence = [n]
    while sequence[-1] != 1:
        last = sequence[-1]
        if last % 2 == 0:
            sequence.append(last // 2)
        else:
            sequence.append(3 * last + 1)
    return len(sequence) - 1


@O
def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


Q(None, "Digital Root", "Medium", "Nested while loops",
  "Keep adding the digits of n until a single digit remains (e.g. 9875 → 29 → 11 → 2). Return it.",
  [((9875,), 2), ((5,), 5), ((0,), 0), ((18,), 9)],
  ("Repeat the digit-sum loop while the number has more than one digit.", "O(d · rounds)", "O(1)"),
  ("Maths shortcut: the digital root is 1 + (n − 1) % 9 for n &gt; 0.", "O(1)", "O(1)"),
  viz=(9875,))


@B
def digital_root(n):
    while n >= 10:
        total = 0
        while n > 0:
            total += n % 10
            n //= 10
        n = total
    return n


@O
def digital_root(n):
    return 0 if n == 0 else 1 + (n - 1) % 9


Q(None, "Armstrong Number", "Medium", "Loop over digits",
  "An Armstrong number equals the sum of its digits each raised to the number of digits (153 = 1³ + 5³ + 3³). Return True or False.",
  [((153,), True), ((9474,), True), ((123,), False), ((5,), True)],
  ("Count the digits in one loop, then sum the powers in a second loop.", "O(d)", "O(1)"),
  ("Use the string form: its length is the power, and a generator sums the powers.", "O(d)", "O(d)"),
  viz=(153,))


@B
def is_armstrong(n):
    count = 0
    temp = n
    while temp > 0:
        count += 1
        temp //= 10
    total = 0
    temp = n
    while temp > 0:
        total += (temp % 10) ** count
        temp //= 10
    return total == n


@O
def is_armstrong(n):
    digits = str(n)
    return n == sum(int(d) ** len(digits) for d in digits)


Q(None, "Count Multiples in a Range", "Easy", "Loop vs formula",
  "How many numbers in [a, b] are divisible by k? (a ≥ 1)",
  [((1, 10, 3), 3), ((5, 25, 5), 5), ((7, 9, 10), 0)],
  ("Check every number in the range.", "O(b − a)", "O(1)"),
  ("Multiples up to b minus multiples below a: <code>b // k − (a − 1) // k</code>.", "O(1)", "O(1)"),
  viz=(1, 10, 3))


@B
def count_multiples(a, b, k):
    count = 0
    for x in range(a, b + 1):
        if x % k == 0:
            count += 1
    return count


@O
def count_multiples(a, b, k):
    return b // k - (a - 1) // k


Q(None, "Primes Up To n", "Hard", "Sieve of Eratosthenes",
  "Return all primes ≤ n in increasing order.",
  [((20,), [2, 3, 5, 7, 11, 13, 17, 19]), ((2,), [2]), ((1,), [])],
  ("Test each number with trial division.", "O(n√n)", "O(1) extra"),
  ("Sieve: assume everything is prime, then cross out multiples of each prime starting at p².", "O(n log log n)", "O(n)"),
  viz=(12,))


@B
def primes_up_to(n):
    primes = []
    for x in range(2, n + 1):
        is_p = True
        for d in range(2, int(x ** 0.5) + 1):
            if x % d == 0:
                is_p = False
                break
        if is_p:
            primes.append(x)
    return primes


@O
def primes_up_to(n):
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_p[p]:
            for m in range(p * p, n + 1, p):
                is_p[m] = False
    return [x for x in range(n + 1) if is_p[x]]


Q(None, "Largest in a List", "Easy", "Running maximum",
  "Return the largest number in a non-empty list.",
  [(([3, 9, 2, 7],), 9), (([-5, -2, -9],), -2), (([4],), 4)],
  ("Track the largest so far while looping.", "O(n)", "O(1)"),
  ("The built-in <code>max()</code>.", "O(n)", "O(1)"),
  viz=([3, 9, 2, 7],))


@B
def largest_in(items):
    best = items[0]
    for x in items[1:]:
        if x > best:
            best = x
    return best


@O
def largest_in(items):
    return max(items)


Q(None, "Perfect Number", "Medium", "Divisor pairs",
  "A perfect number equals the sum of its divisors other than itself (6 = 1 + 2 + 3). Return True or False.",
  [((6,), True), ((28,), True), ((12,), False), ((1,), False)],
  ("Add every divisor from 1 to n − 1.", "O(n)", "O(1)"),
  ("Divisors come in pairs (d, n // d), so loop only up to √n and add both.", "O(√n)", "O(1)"),
  viz=(28,))


@B
def is_perfect(n):
    total = 0
    for d in range(1, n):
        if n % d == 0:
            total += d
    return total == n


@O
def is_perfect(n):
    if n < 2:
        return False
    total = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
        d += 1
    return total == n


Q(None, "Sum Skipping Negatives", "Easy", "continue",
  "Return the sum of the non-negative numbers in a list.",
  [(([3, -1, 4, -5, 2],), 9), (([-1, -2],), 0), (([],), 0)],
  ("Use <code>continue</code> to skip negatives inside the loop.", "O(n)", "O(1)"),
  ("A generator with a filter inside <code>sum()</code>.", "O(n)", "O(1)"),
  viz=([3, -1, 4, -5, 2],))


@B
def sum_non_negative(items):
    total = 0
    for x in items:
        if x < 0:
            continue
        total += x
    return total


@O
def sum_non_negative(items):
    return sum(x for x in items if x >= 0)


Q(None, "Pairs With a Given Sum", "Medium", "Nested loops vs set",
  "Count pairs (i &lt; j) of positions whose values add up to <code>target</code>.",
  [(([1, 5, 7, -1, 5], 6), 3), (([1, 1, 1], 2), 3), (([1, 2], 9), 0)],
  ("Check every pair with two nested loops.", "O(n²)", "O(1)"),
  ("One loop: for each value, add how many earlier values equal target − value (kept in a dict).", "O(n)", "O(n)"),
  viz=([1, 5, 7, -1, 5], 6))


@B
def count_pairs(items, target):
    count = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] + items[j] == target:
                count += 1
    return count


@O
def count_pairs(items, target):
    seen = {}
    count = 0
    for x in items:
        count += seen.get(target - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return count


Q(None, "Smallest Divisor", "Easy", "for … else",
  "Return the smallest divisor of n greater than 1 (n ≥ 2). A prime is its own smallest divisor.",
  [((15,), 3), ((13,), 13), ((8,), 2)],
  ("Collect every divisor in a list, then take the first one.", "O(n)", "O(n)"),
  ("Return at the first divisor found; it only needs to check up to √n.", "O(√n)", "O(1)"),
  viz=(35,))


@B
def smallest_divisor(n):
    divisors = []
    for d in range(2, n + 1):
        if n % d == 0:
            divisors.append(d)
    return divisors[0]


@O
def smallest_divisor(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n
