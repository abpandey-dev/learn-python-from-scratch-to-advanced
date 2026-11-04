from lib import *
import math
from fractions import Fraction
import numpy as np

TOPIC(
    id="arithmetic", title="Numbers & Arithmetic", glyph="1 + 1",
    blurb="The starting point: kinds of numbers, fractions, percentages, powers, roots, primes, rounding and the Σ notation every ML formula uses.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">7 // 2, 7 % 2          # 3 remainder 1
math.gcd(12, 18)       # 6   (greatest common divisor)
math.lcm(4, 6)         # 12  (least common multiple)
Fraction(3, 4) + Fraction(1, 6)   # 11/12
2 ** 10, 2 ** -1       # 1024, 0.5
math.sqrt(2), 8 ** (1/3)
round(3.14159, 2)      # 3.14
f"{1234567:.2e}"       # '1.23e+06'  scientific notation
sum(range(1, n + 1))   # Σ k  =  n(n + 1) / 2
math.factorial(5)      # 120</code></pre>
<p><b>Order of operations</b>: Brackets → Exponents → × and ÷ (left to right) → + and − (left to right). Python follows the same rule.</p>
""")


Q(None, "Greatest Common Divisor", "Easy", "Euclid's algorithm",
  "Return the largest whole number that divides both a and b exactly.",
  [((12, 18), 6), ((17, 5), 1), ((100, 75), 25)],
  ("Euclid: replace (a, b) with (b, a mod b) until b is 0 — the last non-zero value is the answer.", "O(log min(a, b))", "O(1)"),
  ("<code>math.gcd(a, b)</code>.", "O(log min(a, b))", "O(1)"))


@B
def gcd(a, b):
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return a


@O
def gcd(a, b):
    return math.gcd(a, b)


Q(None, "Least Common Multiple", "Easy", "LCM = a·b / gcd",
  "Return the smallest positive number that both a and b divide into.",
  [((4, 6), 12), ((3, 5), 15), ((8, 12), 24)],
  ("List multiples of the larger number until one is also a multiple of the smaller.", "O(min(a, b))", "O(1)"),
  ("<code>a * b // gcd(a, b)</code> (or <code>math.lcm</code>).", "O(log min(a, b))", "O(1)"))


@B
def lcm(a, b):
    big, small = max(a, b), min(a, b)
    multiple = big
    while multiple % small != 0:
        multiple += big
    return multiple


@O
def lcm(a, b):
    return a * b // math.gcd(a, b)


Q(None, "Simplify a Fraction", "Easy", "Lowest terms",
  "Return the fraction num/den in lowest terms as (numerator, denominator).",
  [((12, 18), (2, 3)), ((5, 10), (1, 2)), ((7, 3), (7, 3))],
  ("Try every divisor from the smaller number down; the first that divides both is the GCD.", "O(min(n, d))", "O(1)"),
  ("Divide both by <code>math.gcd</code> — or let <code>Fraction</code> do it.", "O(log n)", "O(1)"))


@B
def simplify(num, den):
    for d in range(min(num, den), 0, -1):
        if num % d == 0 and den % d == 0:
            return (num // d, den // d)


@O
def simplify(num, den):
    f = Fraction(num, den)
    return (f.numerator, f.denominator)


Q(None, "Add Two Fractions", "Easy", "Common denominator",
  "Return a/b + c/d in lowest terms as (numerator, denominator).",
  [((1, 2, 1, 3), (5, 6)), ((3, 4, 1, 6), (11, 12)), ((1, 4, 3, 4), (1, 1))],
  ("Common denominator b·d, numerator a·d + c·b, then simplify with Euclid.", "O(log bd)", "O(1)"),
  ("<code>Fraction(a, b) + Fraction(c, d)</code>.", "O(log bd)", "O(1)"))


@B
def add_fractions(a, b, c, d):
    num = a * d + c * b
    den = b * d
    x, y = num, den
    while y:
        x, y = y, x % y
    return (num // x, den // x)


@O
def add_fractions(a, b, c, d):
    f = Fraction(a, b) + Fraction(c, d)
    return (f.numerator, f.denominator)


Q(None, "Fraction to Decimal and Percent", "Easy", "Three ways to write a part",
  "Return (decimal, percent) for num/den, the decimal rounded to 4 places and the percent to 2.",
  [((3, 4), (0.75, 75.0)), ((1, 3), (0.3333, 33.33)), ((5, 2), (2.5, 250.0))],
  ("Long division digit by digit, then shift the point two places for percent.", "O(digits)", "O(1)"),
  ("<code>num / den</code> and multiply by 100.", "O(1)", "O(1)"))


@B
def to_decimal(num, den):
    whole = num // den
    rest = num % den
    digits = []
    for _ in range(6):
        rest *= 10
        digits.append(rest // den)
        rest = rest % den
    value = whole + sum(dg / 10 ** (i + 1) for i, dg in enumerate(digits))
    return (round(value, 4), round(value * 100, 2))


@O
def to_decimal(num, den):
    value = num / den
    return (round(value, 4), round(value * 100, 2))


Q(None, "Percent Change", "Easy", "(new − old) / old",
  "Return the percentage change from old to new, rounded to 2 decimals (negative means a decrease).",
  [((50, 60), 20.0), ((80, 60), -25.0), ((200, 200), 0.0)],
  ("Find the difference, then ask: what share of the old value is it?", "O(1)", "O(1)"),
  ("For many values at once: <code>(new - old) / old * 100</code> on NumPy arrays.", "O(1)", "O(1)"))


@B
def percent_change(old, new):
    difference = new - old
    share = difference / old
    return round(share * 100, 2)


@O
def percent_change(old, new):
    return round(float((np.array(new) - old) / old * 100), 2)


Q(None, "Is It Prime?", "Easy", "Trial division to √n",
  "Return True if n is prime (exactly two divisors: 1 and itself).",
  [((2,), True), ((15,), False), ((97,), True), ((1,), False)],
  ("Try every divisor from 2 to n − 1.", "O(n)", "O(1)"),
  ("Only test up to √n: if n = a·b, one of a, b is at most √n.", "O(√n)", "O(1)"))


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
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return False
    return True


Q(None, "Prime Factorisation", "Medium", "Every number is a product of primes",
  "Return the prime factors of n in increasing order, with repeats (60 → [2, 2, 3, 5]).",
  [((60,), [2, 2, 3, 5]), ((13,), [13]), ((360,), [2, 2, 2, 3, 3, 5])],
  ("Divide by 2, 3, 4, … up to n, repeating each divisor while it fits.", "O(n)", "O(log n)"),
  ("Stop at √n — whatever is left above 1 is itself prime.", "O(√n)", "O(log n)"),
  viz=(60,))


@B
def factorise(n):
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    return factors


@O
def factorise(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


Q(None, "Power by Repeated Multiplication", "Easy", "Exponents",
  "Return base ** exp for a whole number exp ≥ 0, without using **.",
  [((2, 10), 1024), ((5, 0), 1), ((3, 4), 81)],
  ("Start at 1 and multiply by the base exp times.", "O(exp)", "O(1)"),
  ("Squaring: x⁸ = ((x²)²)², so only O(log exp) multiplications (what <code>pow</code> does).", "O(log exp)", "O(1)"),
  viz=(3, 4))


@B
def power(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result


@O
def power(base, exp):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result *= base
        base *= base
        exp //= 2
    return result


Q(None, "Negative and Fractional Exponents", "Medium", "x⁻ⁿ = 1/xⁿ, x^(1/n) = ⁿ√x",
  "Return x ** p rounded to 4 decimals for p in the form whole/whole (given as num, den), e.g. 8^(2/3) = 4.",
  [((8, 2, 3), 4.0), ((2, -1, 1), 0.5), ((16, -1, 2), 0.25), ((27, 1, 3), 3.0)],
  ("Root first (find r with r^den = x by bisection), then raise to |num|, then flip if num is negative.", "O(log precision)", "O(1)"),
  ("<code>x ** (num / den)</code>.", "O(1)", "O(1)"))


@B
def frac_power(x, num, den):
    lo, hi = 0.0, max(1.0, x)
    for _ in range(60):
        mid = (lo + hi) / 2
        if mid ** den < x:
            lo = mid
        else:
            hi = mid
    root = (lo + hi) / 2
    value = 1.0
    for _ in range(abs(num)):
        value *= root
    if num < 0:
        value = 1 / value
    return round(value, 4)


@O
def frac_power(x, num, den):
    return round(x ** (num / den), 4)


Q(None, "Square Root by Guessing", "Medium", "Newton's method",
  "Return √n rounded to 4 decimals without math.sqrt.",
  [((2,), 1.4142), ((25,), 5.0), ((10,), 3.1623)],
  ("Newton: guess g, improve to (g + n/g)/2; each step roughly doubles the correct digits.", "O(log digits)", "O(1)"),
  ("<code>math.sqrt(n)</code> (or <code>np.sqrt</code> for arrays).", "O(1)", "O(1)"))


@B
def sqrt(n):
    guess = n / 2 if n > 1 else 1.0
    for _ in range(20):
        guess = (guess + n / guess) / 2
    return round(guess, 4)


@O
def sqrt(n):
    return round(math.sqrt(n), 4)


Q(None, "Scientific Notation", "Easy", "a × 10ⁿ with 1 ≤ a < 10",
  "Return (mantissa rounded to 3 decimals, exponent) for a positive number, e.g. 45000 → (4.5, 4).",
  [((45000,), (4.5, 4)), ((0.00321,), (3.21, -3)), ((7,), (7.0, 0))],
  ("Divide (or multiply) by 10 until the number is between 1 and 10, counting the steps.", "O(|exponent|)", "O(1)"),
  ("The exponent is <code>floor(log10(x))</code>.", "O(1)", "O(1)"))


@B
def sci(x):
    exp = 0
    while x >= 10:
        x /= 10
        exp += 1
    while x < 1:
        x *= 10
        exp -= 1
    return (round(x, 3), exp)


@O
def sci(x):
    exp = math.floor(math.log10(x))
    return (round(x / 10 ** exp, 3), exp)


Q(None, "Round to Significant Figures", "Medium", "Precision",
  "Round x (positive) to s significant figures: 0.012345, 2 → 0.012; 98765, 3 → 98800.",
  [((0.012345, 2), 0.012), ((98765, 3), 98800), ((3.14159, 3), 3.14)],
  ("Find which place the first digit is in, then round at the place s − 1 to its right.", "O(digits)", "O(1)"),
  ("<code>round(x, s - 1 - floor(log10(x)))</code>.", "O(1)", "O(1)"))


@B
def sig_figs(x, s):
    place = 0
    y = x
    while y >= 10:
        y /= 10
        place += 1
    while y < 1:
        y *= 10
        place -= 1
    return round(x, s - 1 - place)


@O
def sig_figs(x, s):
    return round(x, s - 1 - math.floor(math.log10(x)))


Q(None, "Divide With Remainder", "Easy", "Quotient and remainder",
  "Return (quotient, remainder) of a ÷ b for whole numbers, without // or %.",
  [((17, 5), (3, 2)), ((20, 4), (5, 0)), ((3, 7), (0, 3))],
  ("Repeated subtraction: take b away while you can, counting how many times.", "O(a / b)", "O(1)"),
  ("<code>divmod(a, b)</code>.", "O(1)", "O(1)"))


@B
def divide(a, b):
    count = 0
    while a >= b:
        a -= b
        count += 1
    return (count, a)


@O
def divide(a, b):
    return divmod(a, b)


Q(None, "Share in a Ratio", "Easy", "Ratios",
  "Split total into parts in the given ratio, e.g. 100 in 2:3 → [40, 60]. Round each to 2 decimals.",
  [((100, [2, 3]), [40.0, 60.0]), ((90, [1, 1, 1]), [30.0, 30.0, 30.0]), ((50, [3, 1]), [37.5, 12.5])],
  ("Add the ratio parts, find the value of one part, multiply each.", "O(k)", "O(k)"),
  ("Vectorised: <code>total * r / r.sum()</code>.", "O(k)", "O(k)"))


@B
def share(total, ratio):
    parts = 0
    for r in ratio:
        parts += r
    one_part = total / parts
    return [round(r * one_part, 2) for r in ratio]


@O
def share(total, ratio):
    r = np.array(ratio)
    return (total * r / r.sum()).round(2)


Q(None, "Whole Number to Binary", "Easy", "Place value in base 2",
  "Return the binary digits of n as a string (n ≥ 0).",
  [((13,), "1101"), ((0,), "0"), ((32,), "100000")],
  ("Divide by 2 repeatedly; the remainders read bottom-up are the digits.", "O(log n)", "O(log n)"),
  ("<code>format(n, 'b')</code> (or <code>bin(n)[2:]</code>).", "O(log n)", "O(log n)"))


@B
def to_binary(n):
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = str(n % 2) + digits
        n //= 2
    return digits


@O
def to_binary(n):
    return format(n, "b")


Q(None, "Add 1 to n (Gauss's Trick)", "Easy", "Σ k = n(n + 1)/2",
  "Return 1 + 2 + … + n.",
  [((10,), 55), ((100,), 5050), ((1,), 1)],
  ("Add the numbers one by one in a loop.", "O(n)", "O(1)"),
  ("Pair first and last: n/2 pairs each summing to n + 1.", "O(1)", "O(1)"))


@B
def sum_to(n):
    total = 0
    for k in range(1, n + 1):
        total += k
    return total


@O
def sum_to(n):
    return n * (n + 1) // 2


Q(None, "Sigma Notation: Sum of Squares", "Medium", "Σ k²",
  "Return Σ k² for k = 1 … n.",
  [((3,), 14), ((10,), 385), ((1,), 1)],
  ("Translate Σ literally: a loop from k = 1 to n adding k².", "O(n)", "O(1)"),
  ("Formula n(n + 1)(2n + 1)/6 — or vectorised <code>(np.arange(1, n+1)**2).sum()</code>.", "O(1)", "O(1)"))


@B
def sum_squares(n):
    total = 0
    for k in range(1, n + 1):
        total += k * k
    return total


@O
def sum_squares(n):
    return n * (n + 1) * (2 * n + 1) // 6


Q(None, "Factorial", "Easy", "n! = n·(n−1)·…·1",
  "Return n! (0! = 1).",
  [((5,), 120), ((0,), 1), ((10,), 3628800)],
  ("Multiply 1·2·…·n in a loop.", "O(n)", "O(1)"),
  ("<code>math.factorial(n)</code>.", "O(n)", "O(1)"))


@B
def factorial(n):
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


@O
def factorial(n):
    return math.factorial(n)


Q(None, "Distance on the Number Line", "Easy", "Absolute value",
  "Return the distances |a − b| for each pair in the list.",
  [(([(3, 7), (-2, 4), (5, 5)],), [4, 6, 0]), (([(-5, -1)],), [4])],
  ("Subtract, then drop the minus sign if there is one.", "O(n)", "O(n)"),
  ("NumPy: <code>np.abs(a - b)</code> for all pairs at once.", "O(n)", "O(n)"))


@B
def distances(pairs):
    out = []
    for a, b in pairs:
        d = a - b
        if d < 0:
            d = -d
        out.append(d)
    return out


@O
def distances(pairs):
    p = np.array(pairs)
    return np.abs(p[:, 0] - p[:, 1])
