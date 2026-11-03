from lib import *

TOPIC(
    id="operators", title="Operators & Expressions", glyph="+ − * /",
    blurb="Arithmetic, comparison, logical, assignment, identity, membership and bitwise operators — and the order Python applies them.",
    theory="""
<h3>Cheat sheet</h3>
<table>
<tr><th>Kind</th><th>Operators</th></tr>
<tr><td>Arithmetic</td><td><code>+ - * / // % **</code></td></tr>
<tr><td>Comparison</td><td><code>== != &lt; &gt; &lt;= &gt;=</code></td></tr>
<tr><td>Logical</td><td><code>and or not</code></td></tr>
<tr><td>Assignment</td><td><code>= += -= *= /= //= %= **=</code></td></tr>
<tr><td>Identity / membership</td><td><code>is</code>, <code>is not</code>, <code>in</code>, <code>not in</code></td></tr>
<tr><td>Bitwise</td><td><code>&amp; | ^ ~ &lt;&lt; &gt;&gt;</code></td></tr>
</table>
<p><code>7 / 2 = 3.5</code> · <code>7 // 2 = 3</code> · <code>7 % 2 = 1</code> · <code>2 ** 3 = 8</code> · <code>-7 // 2 = -4</code> (floors down)</p>
<p>Precedence (high → low): <code>**</code> → unary <code>-</code> → <code>* / // %</code> → <code>+ -</code> → comparisons → <code>not</code> → <code>and</code> → <code>or</code>. When unsure, add brackets.</p>
""")


Q(None, "Even or Odd", "Easy", "% operator",
  "Return <code>'even'</code> if <code>n</code> is even, otherwise <code>'odd'</code>.",
  [((4,), "even"), ((7,), "odd"), ((0,), "even"), ((-3,), "odd")],
  ("Keep subtracting 2 (or adding 2 for negatives) until you reach 0 or 1.", "O(n)", "O(1)"),
  ("A number is even exactly when <code>n % 2 == 0</code>.", "O(1)", "O(1)"),
  viz=(7,))


@B
def even_or_odd(n):
    n = abs(n)
    while n >= 2:
        n = n - 2
    if n == 0:
        return "even"
    return "odd"


@O
def even_or_odd(n):
    return "even" if n % 2 == 0 else "odd"


Q(None, "Leap Year", "Easy", "and / or",
  "A year is a leap year if it's divisible by 4, except years divisible by 100, unless also divisible by 400. Return True or False.",
  [((2024,), True), ((1900,), False), ((2000,), True), ((2023,), False)],
  ("Nested <code>if</code> statements, one rule at a time.", "O(1)", "O(1)"),
  ("Combine the rules into one boolean expression with <code>and</code>/<code>or</code>.", "O(1)", "O(1)"))


@B
def is_leap(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False


@O
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


Q(None, "Power Without **", "Easy", "** · loops",
  "Return <code>base</code> raised to a non-negative integer <code>exp</code>.",
  [((2, 10), 1024), ((5, 0), 1), ((3, 4), 81)],
  ("Multiply a result by base, exp times.", "O(exp)", "O(1)"),
  ("Python's <code>**</code> operator (or <code>pow</code>) does it directly.", "O(log exp)", "O(1)"),
  viz=(3, 4))


@B
def power(base, exp):
    result = 1
    for _ in range(exp):
        result = result * base
    return result


@O
def power(base, exp):
    return base ** exp


Q(None, "Absolute Value", "Easy", "Unary minus · abs()",
  "Return the absolute value (distance from zero) of <code>n</code>.",
  [((-8,), 8), ((5,), 5), ((0,), 0)],
  ("If n is negative, flip its sign with unary minus.", "O(1)", "O(1)"),
  ("Use the built-in <code>abs()</code>.", "O(1)", "O(1)"))


@B
def absolute(n):
    if n < 0:
        n = -n
    return n


@O
def absolute(n):
    return abs(n)


Q(None, "Largest of Three", "Easy", "Comparison operators",
  "Return the largest of <code>a</code>, <code>b</code>, <code>c</code>.",
  [((3, 9, 4), 9), ((7, 7, 2), 7), ((-1, -5, -3), -1)],
  ("Compare with <code>&gt;=</code> using if/elif.", "O(1)", "O(1)"),
  ("Built-in <code>max()</code> takes any number of values.", "O(1)", "O(1)"))


@B
def largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c


@O
def largest(a, b, c):
    return max(a, b, c)


Q(None, "FizzBuzz Word", "Easy", "% · and",
  "Return <code>'FizzBuzz'</code> if n is divisible by 3 and 5, <code>'Fizz'</code> if only by 3, <code>'Buzz'</code> if only by 5, else the number as a string.",
  [((15,), "FizzBuzz"), ((9,), "Fizz"), ((10,), "Buzz"), ((7,), "7")],
  ("Check the combined case first, then each single case.", "O(1)", "O(1)"),
  ("Build the word by adding 'Fizz' and 'Buzz' pieces; fall back to the number with <code>or</code>.", "O(1)", "O(1)"))


@B
def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


@O
def fizzbuzz(n):
    word = ("Fizz" if n % 3 == 0 else "") + ("Buzz" if n % 5 == 0 else "")
    return word or str(n)


Q(None, "Compound Interest", "Easy", "** operator",
  "Return the amount after <code>years</code> with yearly compound interest <code>rate</code> percent, rounded to 2 decimals.",
  [((1000, 10, 2), 1210.0), ((500, 5, 3), 578.81), ((100, 0, 5), 100.0)],
  ("Apply the interest year by year in a loop.", "O(years)", "O(1)"),
  ("Use the formula P × (1 + r/100) ** years.", "O(1)", "O(1)"))


@B
def compound(principal, rate, years):
    amount = principal
    for _ in range(years):
        amount = amount + amount * rate / 100
    return round(amount, 2)


@O
def compound(principal, rate, years):
    return round(principal * (1 + rate / 100) ** years, 2)


Q(None, "Perfect Square", "Easy", "** · math.isqrt",
  "Return True if <code>n</code> (≥ 0) is a perfect square like 16 or 25.",
  [((16,), True), ((15,), False), ((0,), True), ((1,), True)],
  ("Try i = 0, 1, 2, … while i × i ≤ n.", "O(√n)", "O(1)"),
  ("<code>math.isqrt(n)</code> is the whole-number square root; square it and compare.", "O(1)*", "O(1)"),
  viz=(16,))


@B
def is_square(n):
    i = 0
    while i * i <= n:
        if i * i == n:
            return True
        i += 1
    return False


@O
def is_square(n):
    import math
    r = math.isqrt(n)
    return r * r == n


Q(None, "Reverse a Number", "Medium", "// and %",
  "Return the digits of a positive integer in reverse order as an int, e.g. 1230 → 321.",
  [((1234,), 4321), ((1230,), 321), ((7,), 7)],
  ("Take the last digit with % 10, append it to the result with result × 10 + digit, drop it with // 10.", "O(d)", "O(1)"),
  ("Turn it into a string, reverse with a slice, and convert back.", "O(d)", "O(d)"),
  viz=(1230,))


@B
def reverse_number(n):
    result = 0
    while n > 0:
        digit = n % 10
        result = result * 10 + digit
        n //= 10
    return result


@O
def reverse_number(n):
    return int(str(n)[::-1])


Q(None, "Floats Almost Equal", "Easy", "Float comparison",
  "Return True if <code>a</code> and <code>b</code> are equal up to tiny rounding errors (e.g. 0.1 + 0.2 and 0.3).",
  [((0.1 + 0.2, 0.3), True), ((1.0, 1.001), False), ((2.5, 2.5), True)],
  ("Check that the difference is smaller than a tiny tolerance.", "O(1)", "O(1)"),
  ("<code>math.isclose</code> uses a sensible relative tolerance for you.", "O(1)", "O(1)"))


@B
def almost_equal(a, b):
    difference = a - b
    if difference < 0:
        difference = -difference
    return difference < 1e-9


@O
def almost_equal(a, b):
    import math
    return math.isclose(a, b)


Q(None, "Ceiling Division", "Easy", "// trick",
  "How many boxes of size <code>b</code> are needed for <code>a</code> items? Return ⌈a / b⌉ for positive integers.",
  [((10, 3), 4), ((9, 3), 3), ((1, 5), 1)],
  ("Divide with //, then add 1 if there's a remainder.", "O(1)", "O(1)"),
  ("Negating twice turns floor into ceiling: <code>-(-a // b)</code>.", "O(1)", "O(1)"))


@B
def ceil_div(a, b):
    boxes = a // b
    if a % b != 0:
        boxes += 1
    return boxes


@O
def ceil_div(a, b):
    return -(-a // b)


Q(None, "Power of Two", "Medium", "Bitwise &",
  "Return True if <code>n</code> is a power of two (1, 2, 4, 8, …).",
  [((8,), True), ((12,), False), ((1,), True), ((0,), False)],
  ("Divide by 2 while even; it's a power of two if you end at 1.", "O(log n)", "O(1)"),
  ("A power of two has a single 1-bit, so <code>n &amp; (n - 1)</code> is 0.", "O(1)", "O(1)"),
  viz=(8,))


@B
def is_power_of_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


@O
def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0


Q(None, "Count Digits", "Easy", "// · len(str())",
  "Return how many digits the integer <code>n</code> has (ignore the sign; 0 has 1 digit).",
  [((12345,), 5), ((-70,), 2), ((0,), 1)],
  ("Divide by 10 until it reaches 0, counting steps.", "O(d)", "O(1)"),
  ("Length of the number written as text.", "O(d)", "O(d)"),
  viz=(12345,))


@B
def count_digits(n):
    n = abs(n)
    count = 1
    while n >= 10:
        n //= 10
        count += 1
    return count


@O
def count_digits(n):
    return len(str(abs(n)))


Q(None, "Round to Nearest Multiple", "Medium", "// and arithmetic",
  "Round a non-negative integer <code>n</code> to the nearest multiple of <code>k</code> (halves round up).",
  [((23, 5), 25), ((22, 5), 20), ((15, 10), 20)],
  ("Look at the multiples just below and just above n, and pick the closer one.", "O(1)", "O(1)"),
  ("Add half of k and floor-divide: <code>(n + k // 2) // k * k</code>.", "O(1)", "O(1)"))


@B
def round_to(n, k):
    below = n - n % k
    above = below + k
    if n - below < above - n:
        return below
    return above


@O
def round_to(n, k):
    return (n + k // 2) // k * k


Q(None, "Exactly One Is True", "Easy", "Logical operators",
  "Given two booleans, return True if exactly one of them is True (exclusive or).",
  [((True, False), True), ((True, True), False), ((False, False), False)],
  ("Spell out both cases with <code>and</code>, <code>or</code> and <code>not</code>.", "O(1)", "O(1)"),
  ("For booleans, 'exactly one' is the same as 'they are different': <code>a != b</code>.", "O(1)", "O(1)"))


@B
def exactly_one(a, b):
    return (a and not b) or (b and not a)


@O
def exactly_one(a, b):
    return a != b


Q(None, "Within a Range", "Easy", "Chained comparison",
  "Return True if <code>lo ≤ x ≤ hi</code>.",
  [((5, 1, 10), True), ((0, 1, 10), False), ((10, 1, 10), True)],
  ("Two comparisons joined by <code>and</code>.", "O(1)", "O(1)"),
  ("Python allows chaining: <code>lo &lt;= x &lt;= hi</code>.", "O(1)", "O(1)"))


@B
def in_range(x, lo, hi):
    return x >= lo and x <= hi


@O
def in_range(x, lo, hi):
    return lo <= x <= hi


Q(None, "Sum From 1 to n", "Easy", "Formula vs loop",
  "Return 1 + 2 + … + n.",
  [((10,), 55), ((1,), 1), ((100,), 5050)],
  ("Add every number in a loop.", "O(n)", "O(1)"),
  ("Gauss's formula n × (n + 1) // 2.", "O(1)", "O(1)"),
  viz=(5,))


@B
def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


@O
def sum_to(n):
    return n * (n + 1) // 2


Q(None, "Weekly Pay With Overtime", "Medium", "min / max arithmetic",
  "Pay is <code>rate</code> per hour for the first 40 hours and 1.5 × rate for every hour above 40. Return total pay.",
  [((45, 10), 475.0), ((30, 20), 600.0), ((40, 15), 600.0)],
  ("Use if/else to handle the two cases.", "O(1)", "O(1)"),
  ("Split hours with min and max: normal = min(hours, 40), extra = max(hours − 40, 0).", "O(1)", "O(1)"))


@B
def weekly_pay(hours, rate):
    if hours <= 40:
        pay = hours * rate
    else:
        pay = 40 * rate
        extra = hours - 40
        pay = pay + extra * rate * 1.5
    return float(pay)


@O
def weekly_pay(hours, rate):
    return min(hours, 40) * rate + max(hours - 40, 0) * rate * 1.5


Q(None, "Number of Handshakes", "Easy", "Formula vs nested loop",
  "In a room of <code>n</code> people, everyone shakes hands with everyone else once. How many handshakes?",
  [((4,), 6), ((1,), 0), ((10,), 45)],
  ("Count every pair (i, j) with i &lt; j using two loops.", "O(n²)", "O(1)"),
  ("Each of n people shakes n − 1 hands, and each handshake is counted twice: n(n − 1) / 2.", "O(1)", "O(1)"),
  viz=(4,))


@B
def handshakes(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count


@O
def handshakes(n):
    return n * (n - 1) // 2


Q(None, "Clamp a Value", "Easy", "min and max",
  "Return <code>x</code> limited to the range [lo, hi]: below lo becomes lo, above hi becomes hi.",
  [((15, 0, 10), 10), ((-3, 0, 10), 0), ((7, 0, 10), 7)],
  ("Two if statements.", "O(1)", "O(1)"),
  ("<code>max(lo, min(x, hi))</code> in one line.", "O(1)", "O(1)"))


@B
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@O
def clamp(x, lo, hi):
    return max(lo, min(x, hi))
