from lib import *

TOPIC(
    id="functions", title="Functions & Recursion", glyph="def f()",
    blurb="Package code into reusable functions: parameters, return values, scope, lambdas, closures and recursion.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">def area(w, h=1):            # h has a default value
    \"\"\"Return w × h.\"\"\"       # docstring
    return w * h

area(3), area(3, 4), area(h=4, w=3)   # positional, keyword
def total(*nums): return sum(nums)    # any number of positional args
def tag(**attrs): return attrs        # any number of keyword args
square = lambda x: x * x              # small anonymous function
sorted(words, key=len)                # functions are values

def fact(n):                          # recursion: base case + smaller call
    return 1 if n &lt;= 1 else n * fact(n - 1)</code></pre>
<ul><li>No <code>return</code> → the function returns <code>None</code>.</li><li>Never use a mutable default like <code>def f(x, acc=[])</code>.</li></ul>
""")


Q(None, "Greeting With a Default", "Easy", "Default parameters",
  "Write <code>greet(name, greeting='Hello')</code> that returns e.g. 'Hello, Ana!'. The greeting is optional.",
  [(("Ana",), "Hello, Ana!"), (("Ben", "Hi"), "Hi, Ben!")],
  ("Make greeting optional by passing None and filling it in inside.", "O(1)", "O(1)"),
  ("Give the parameter a default value in the signature.", "O(1)", "O(1)"))


@B
def greet(name, greeting=None):
    if greeting is None:
        greeting = "Hello"
    return greeting + ", " + name + "!"


@O
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


Q(None, "Circle Area (return, don't print)", "Easy", "return values",
  "Return the area of a circle of radius r, rounded to 2 decimals.",
  [((1,), 3.14), ((2.5,), 19.63), ((0,), 0.0)],
  ("Use 3.14159 typed by hand and several steps.", "O(1)", "O(1)"),
  ("Use <code>math.pi</code> and return the expression.", "O(1)", "O(1)"))


@B
def circle_area(r):
    pi = 3.14159265
    r_squared = r * r
    area = pi * r_squared
    return round(area, 2)


@O
def circle_area(r):
    import math
    return round(math.pi * r ** 2, 2)


Q(None, "Sum Any Number of Values", "Easy", "*args",
  "Write <code>total(*nums)</code> that adds any number of arguments: total(1, 2, 3) → 6, total() → 0.",
  [((1, 2, 3), 6), ((), 0), ((10,), 10)],
  ("Loop over the args tuple and add.", "O(n)", "O(1)"),
  ("<code>*nums</code> collects the arguments into a tuple; pass it to <code>sum</code>.", "O(n)", "O(1)"),
  viz=(4, 5, 6))


@B
def total(*nums):
    result = 0
    for x in nums:
        result += x
    return result


@O
def total(*nums):
    return sum(nums)


Q(None, "Keyword Arguments to Text", "Medium", "**kwargs",
  "Write <code>describe(**info)</code> that returns 'key=value' pairs sorted by key and joined by ', '.",
  [(({"name": "Ana", "age": 21},), "age=21, name=Ana"), (({},), "")],
  ("Loop over sorted keys and build the text with +.", "O(k log k)", "O(k)"),
  ("<code>**info</code> collects keyword arguments into a dict; join a generator over its sorted items.", "O(k log k)", "O(k)"),
  runner=lambda fn, a: fn(**a[0]), names=("**info",),
  viz=({"name": "Ana", "age": 21},))


@B
def describe(**info):
    text = ""
    for key in sorted(info):
        if text:
            text += ", "
        text += key + "=" + str(info[key])
    return text


@O
def describe(**info):
    return ", ".join(f"{k}={v}" for k, v in sorted(info.items()))


Q(None, "Factorial with Recursion", "Easy", "Recursion · base case",
  "Return n! using recursion in the long way.",
  [((5,), 120), ((0,), 1), ((1,), 1)],
  ("Recursive: n! = n × (n − 1)!, with 0! = 1 as the base case.", "O(n)", "O(n) call stack"),
  ("<code>math.factorial</code> — no recursion depth limit, implemented in C.", "O(n)", "O(1)"))


@B
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


@O
def factorial(n):
    import math
    return math.factorial(n)


Q(None, "n-th Fibonacci Number", "Medium", "Memoisation",
  "Return the n-th Fibonacci number (fib(0) = 0, fib(1) = 1).",
  [((10,), 55), ((0,), 0), ((20,), 6765)],
  ("Plain recursion fib(n − 1) + fib(n − 2) — recomputes the same values again and again.", "O(2ⁿ)", "O(n)"),
  ("Cache results with <code>functools.lru_cache</code> so each fib(k) is computed once.", "O(n)", "O(n)"),
  viz=(5,))


@B
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@O
def fib(n):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def f(k):
        return k if k < 2 else f(k - 1) + f(k - 2)
    return f(n)


Q(None, "Fast Power", "Medium", "Divide and conquer",
  "Return base ** exp for a non-negative integer exp using recursion.",
  [((2, 10), 1024), ((3, 0), 1), ((5, 3), 125)],
  ("power(b, e) = b × power(b, e − 1) — e recursive calls.", "O(e)", "O(e)"),
  ("Halve the exponent: power(b, e) = power(b, e // 2)², times b when e is odd.", "O(log e)", "O(log e)"),
  viz=(2, 10))


@B
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)


@O
def power(base, exp):
    if exp == 0:
        return 1
    half = power(base, exp // 2)
    return half * half if exp % 2 == 0 else half * half * base


Q(None, "Sum of Digits, Recursively", "Easy", "Recursion on numbers",
  "Return the sum of the digits of a non-negative integer.",
  [((1234,), 10), ((0,), 0), ((9,), 9)],
  ("Recursive: last digit + sum of the rest (n // 10).", "O(d)", "O(d)"),
  ("Convert to a string and sum the digits.", "O(d)", "O(d)"),
  viz=(1234,))


@B
def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


@O
def digit_sum(n):
    return sum(map(int, str(n)))


Q(None, "Reverse a String, Recursively", "Easy", "Recursion on strings",
  "Return the string reversed.",
  [(("abc",), "cba"), (("",), ""), (("x",), "x")],
  ("Recursive: last character + reverse of the rest.", "O(n²) (slices)", "O(n)"),
  ("Slice with step −1.", "O(n)", "O(n)"),
  viz=("abcd",))


@B
def reverse(s):
    if s == "":
        return ""
    return s[-1] + reverse(s[:-1])


@O
def reverse(s):
    return s[::-1]


Q(None, "Palindrome, Recursively", "Easy", "Two base cases",
  "Return True if s reads the same backwards.",
  [(("racecar",), True), (("abca",), False), (("",), True)],
  ("Recursive: first == last and the middle is a palindrome.", "O(n²) (slices)", "O(n)"),
  ("Compare with the reversed string.", "O(n)", "O(n)"),
  viz=("level",))


@B
def is_pal(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_pal(s[1:-1])


@O
def is_pal(s):
    return s == s[::-1]


Q(None, "Countdown List, Recursively", "Easy", "Building a list recursively",
  "Return [n, n − 1, …, 1] (empty for n ≤ 0).",
  [((4,), [4, 3, 2, 1]), ((0,), []), ((1,), [1])],
  ("Recursive: [n] + countdown(n − 1).", "O(n²) (list copies)", "O(n)"),
  ("<code>list(range(n, 0, -1))</code>.", "O(n)", "O(n)"),
  viz=(3,))


@B
def countdown(n):
    if n <= 0:
        return []
    return [n] + countdown(n - 1)


@O
def countdown(n):
    return list(range(n, 0, -1))


Q(None, "Apply an Operation by Name", "Medium", "Functions as values",
  "Apply <code>op</code> ('double', 'square' or 'negate') to every number and return the new list.",
  [(([1, 2, 3], "double"), [2, 4, 6]), (([1, 2, 3], "square"), [1, 4, 9]), (([4], "negate"), [-4])],
  ("An if/elif inside the loop for every number.", "O(n)", "O(n)"),
  ("Store the functions in a dict and <code>map</code> the chosen one.", "O(n)", "O(n)"),
  viz=([1, 2, 3], "square"))


@B
def apply_op(nums, op):
    result = []
    for x in nums:
        if op == "double":
            result.append(x * 2)
        elif op == "square":
            result.append(x * x)
        elif op == "negate":
            result.append(-x)
    return result


@O
def apply_op(nums, op):
    ops = {"double": lambda x: x * 2, "square": lambda x: x * x, "negate": lambda x: -x}
    return list(map(ops[op], nums))


Q(None, "Scale With a Closure", "Medium", "Closures",
  "Return every number multiplied by k, using a helper function built by <code>make_scaler(k)</code> in the optimal answer.",
  [(([1, 2, 3], 10), [10, 20, 30]), (([], 5), [])],
  ("A plain loop.", "O(n)", "O(n)"),
  ("An inner function remembers k from the outer function (a closure).", "O(n)", "O(n)"),
  viz=([1, 2, 3], 10))


@B
def scale_all(nums, k):
    out = []
    for x in nums:
        out.append(x * k)
    return out


@O
def scale_all(nums, k):
    def make_scaler(factor):
        def scale(x):
            return x * factor
        return scale

    scale = make_scaler(k)
    return [scale(x) for x in nums]


Q(None, "Validate an Order", "Medium", "Guard clauses",
  "Return 'ok', or the first problem: 'no items', 'bad quantity' (qty ≤ 0) or 'too expensive' (total &gt; budget). Order is a list of (price, qty).",
  [(([], 100), "no items"), (([(10, 0)], 100), "bad quantity"), (([(60, 2)], 100), "too expensive"), (([(20, 2)], 100), "ok")],
  ("Nested ifs, with the happy path deep inside.", "O(n)", "O(1)"),
  ("Guard clauses: return early on each problem, then the happy path is flat.", "O(n)", "O(1)"))


@B
def validate(order, budget):
    if order:
        valid_qty = True
        for price, qty in order:
            if qty <= 0:
                valid_qty = False
        if valid_qty:
            if sum(p * q for p, q in order) <= budget:
                return "ok"
            else:
                return "too expensive"
        else:
            return "bad quantity"
    else:
        return "no items"


@O
def validate(order, budget):
    if not order:
        return "no items"
    if any(qty <= 0 for _, qty in order):
        return "bad quantity"
    if sum(price * qty for price, qty in order) > budget:
        return "too expensive"
    return "ok"


Q(None, "Sort by Last Letter", "Easy", "lambda as a key",
  "Sort words by their last letter (ties keep their original order).",
  [((["apple", "kiwi", "banana", "fig"],), ["banana", "apple", "fig", "kiwi"]), (([],), [])],
  ("Insertion sort comparing the last letters by hand.", "O(n²)", "O(n)"),
  ("<code>sorted(words, key=lambda w: w[-1])</code>.", "O(n log n)", "O(n)"),
  viz=(["apple", "kiwi", "banana"],))


@B
def by_last_letter(words):
    result = words[:]
    for i in range(1, len(result)):
        j = i
        while j > 0 and result[j - 1][-1] > result[j][-1]:
            result[j - 1], result[j] = result[j], result[j - 1]
            j -= 1
    return result


@O
def by_last_letter(words):
    return sorted(words, key=lambda w: w[-1])


Q(None, "GCD, Recursively", "Easy", "Euclid's algorithm",
  "Return the greatest common divisor of a and b.",
  [((48, 18), 6), ((7, 3), 1), ((10, 0), 10)],
  ("Recursive Euclid: gcd(a, b) = gcd(b, a % b), with gcd(a, 0) = a.", "O(log)", "O(log) stack"),
  ("<code>math.gcd</code>.", "O(log)", "O(1)"),
  viz=(48, 18))


@B
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


@O
def gcd(a, b):
    import math
    return math.gcd(a, b)


Q(None, "Binary String, Recursively", "Medium", "Recursion on n // 2",
  "Return the binary representation of a non-negative integer as a string.",
  [((5,), "101"), ((0,), "0"), ((8,), "1000")],
  ("binary(n) = binary(n // 2) + last bit; base case n &lt; 2.", "O(log n)", "O(log n)"),
  ("<code>bin(n)[2:]</code> or <code>format(n, 'b')</code>.", "O(log n)", "O(log n)"),
  viz=(6,))


@B
def to_binary(n):
    if n < 2:
        return str(n)
    return to_binary(n // 2) + str(n % 2)


@O
def to_binary(n):
    return format(n, "b")


Q(None, "Flatten Any Depth", "Hard", "Recursion on nested lists",
  "Flatten lists nested to any depth: [1, [2, [3, [4]]], 5] → [1, 2, 3, 4, 5].",
  [(([1, [2, [3, [4]]], 5],), [1, 2, 3, 4, 5]), (([],), []), (([[[]]],),  [])],
  ("Recursively flatten each item and concatenate the results (lots of list copying).", "O(n · depth)", "O(n · depth)"),
  ("Recurse with one shared output list, appending leaves as you find them.", "O(n)", "O(n)"),
  viz=([1, [2, [3]], 4],))


@B
def flatten(items):
    result = []
    for x in items:
        if isinstance(x, list):
            result = result + flatten(x)
        else:
            result = result + [x]
    return result


@O
def flatten(items):
    out = []

    def walk(xs):
        for x in xs:
            if isinstance(x, list):
                walk(x)
            else:
                out.append(x)

    walk(items)
    return out


Q(None, "Tower of Hanoi Moves", "Medium", "Recursion vs formula",
  "How many moves are needed to move n discs in the Tower of Hanoi puzzle?",
  [((3,), 7), ((1,), 1), ((10,), 1023)],
  ("Recursive: move n − 1 discs away, move the big disc, move n − 1 back: T(n) = 2T(n − 1) + 1.", "O(2ⁿ)", "O(n)"),
  ("Solve the recurrence: T(n) = 2ⁿ − 1.", "O(1)", "O(1)"),
  viz=(3,))


@B
def hanoi_moves(n):
    if n == 0:
        return 0
    return hanoi_moves(n - 1) + 1 + hanoi_moves(n - 1)


@O
def hanoi_moves(n):
    return 2 ** n - 1


Q(None, "Climbing Stairs", "Medium", "Recursion + memo",
  "You climb 1 or 2 steps at a time. How many ways to reach step n?",
  [((3,), 3), ((5,), 8), ((1,), 1)],
  ("ways(n) = ways(n − 1) + ways(n − 2) with plain recursion.", "O(2ⁿ)", "O(n)"),
  ("Same recursion with a memo dict, so each step is solved once.", "O(n)", "O(n)"),
  viz=(5,))


@B
def stairs(n):
    if n <= 2:
        return n
    return stairs(n - 1) + stairs(n - 2)


@O
def stairs(n):
    memo = {1: 1, 2: 2}

    def ways(k):
        if k not in memo:
            memo[k] = ways(k - 1) + ways(k - 2)
        return memo[k]

    return ways(n)
